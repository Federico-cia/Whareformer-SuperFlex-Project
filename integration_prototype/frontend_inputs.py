"""Verified observation contract and cache adapter, independent of neural models.

This imports a verified history bundle; it never calls cached features a fresh
RGB extraction. Cold regeneration requires explicitly inventoried model assets.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

import numpy as np
from PIL import Image


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def artifact(path):
    path=Path(path).resolve()
    return dict(path=str(path),sha256=sha(path))


def verify(info):
    path=Path(info['path'])
    if sha(path)!=info['sha256']:raise ValueError('Artifact hash mismatch: '+str(path))
    return path


def verify_bundle(root):
    root=Path(root).resolve();plan=json.loads((root/'input_manifest.json').read_text())
    for name,digest in plan['prepared_hashes'].items():
        path=(root/name).resolve()
        if not path.is_relative_to(root) or sha(path)!=digest:raise ValueError('Bundle hash mismatch: '+name)
    frames=json.loads((root/'frames.json').read_text());offset=0;last=-1
    with np.load(root/'features.npz',allow_pickle=False) as data:
        app=data['app'].copy();loc=data['loc'].copy()
        for frame in frames:
            count=len(frame['annotations'])
            if frame['frame_index']<=last or frame['offset']!=offset:raise ValueError('Frame order/offset mismatch')
            if app[offset:offset+count].shape!=(count,256) or loc[offset:offset+count].shape!=(count,3):
                raise ValueError('Baseline feature dimensions mismatch')
            offset+=count;last=frame['frame_index']
        if offset!=len(app) or offset!=len(loc):raise ValueError('Observation count mismatch')
        if not np.isfinite(app).all() or not np.isfinite(loc).all():raise ValueError('Nonfinite baseline features')
    return plan,frames


def create_manifest(bundle,ready,targets,output):
    bundle,ready,output=Path(bundle).resolve(),Path(ready).resolve(),Path(output)
    if output.exists():raise FileExistsError(output)
    plan,frames=verify_bundle(bundle)
    annotations=json.loads((ready/'annotations.json').read_text())['video_annotations']
    cameras=json.loads((ready/'camera.json').read_text())
    observations=[]
    for frame in frames:
        idx=frame['frame_index']
        if idx not in targets:continue
        matches=[r for r in annotations if r['rgb_frame']==frame['frame']+'.jpg']
        if len(matches)!=1:raise ValueError('Missing or ambiguous RGB/VISOR mapping')
        row=matches[0];visor=int(row['image']['name'].rsplit('_',1)[1].split('.')[0])
        if visor!=idx:raise ValueError('Temporal alias excluded from this pilot')
        rgb=ready/row['rgb_frame']
        with Image.open(rgb) as image:rgb_size=list(image.size)
        pose=cameras['images'][row['rgb_frame']]
        if len(pose)!=7 or not np.isfinite(pose).all():raise ValueError('Invalid camera pose')
        for i,ann in enumerate(frame['annotations']):
            source=[a for a in row['annotations'] if a['id']==ann['id']]
            if len(source)!=1 or source[0]['name']!=ann['name']:raise ValueError('Annotation mapping mismatch')
            polygons=source[0]['segments']
            points=[p for polygon in polygons for p in polygon]
            if not points or np.asarray(points).ndim!=2 or np.asarray(points).shape[1]!=2:raise ValueError('Invalid mask polygons')
            bbox=[min(p[0] for p in points),min(p[1] for p in points),max(p[0] for p in points)+1,max(p[1] for p in points)+1]
            if list(map(int,bbox))!=ann['bounding_box']:raise ValueError('Mask/bbox mismatch')
            observations.append(dict(observation_key=f'{plan["video"]}/{frame["frame"]}__d{i}',video=plan['video'],
                frame_index=idx,visor_index=visor,annotation_id=ann['id'],detection_idx=i,category=ann['name'],
                bbox=ann['bounding_box'],rgb=artifact(rgb),rgb_resolution=rgb_size,
                mask=dict(annotations=artifact(ready/'annotations.json'),annotation_id=ann['id'],resolution=[854,480]),
                camera=artifact(ready/'camera.json'),intrinsics_resolution=[cameras['camera']['width'],cameras['camera']['height']],
                camera_pose=pose,baseline_xyz_reference='aligned scene; imported original features',
                shape_points_reference='camera; DA/MoGE source conventions retained'))
    if {o['frame_index'] for o in observations}!=set(targets):raise ValueError('Requested frame absent')
    manifest=dict(schema_version=1,mode='verified_cache',video=plan['video'],
        history_bundle=dict(path=str(bundle),manifest_sha256=sha(bundle/'input_manifest.json')),
        observation_frames=list(targets),history_policy='retain entire verified prefix; never restart tracker at sparse target frames',
        observations=observations,cold_regeneration_status='not_executed_requires_model_and_scene_preflight')
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    return manifest


def prepare(manifest_path,output):
    manifest=json.loads(Path(manifest_path).read_text());output=Path(output)
    if output.exists():raise FileExistsError(output)
    if manifest['schema_version']!=1 or manifest['mode']!='verified_cache':raise ValueError('Unsupported frontend mode')
    root=Path(manifest['history_bundle']['path'])
    if sha(root/'input_manifest.json')!=manifest['history_bundle']['manifest_sha256']:raise ValueError('History manifest mismatch')
    plan,frames=verify_bundle(root)
    lookup={(f['frame_index'],i):a for f in frames for i,a in enumerate(f['annotations'])}
    seen=set()
    for row in manifest['observations']:
        key=row['frame_index'],row['detection_idx']
        if key in seen or row['video']!=plan['video']:raise ValueError('Duplicate or foreign observation')
        seen.add(key);ann=lookup[key]
        if (ann['id'],ann['name'],ann['bounding_box'])!=(row['annotation_id'],row['category'],row['bbox']):raise ValueError('Detection/annotation mismatch')
        if row['visor_index']!=row['frame_index']:raise ValueError('Unverified temporal alias')
        with Image.open(verify(row['rgb'])) as image:
            if list(image.size)!=row['rgb_resolution']:raise ValueError('RGB resolution mismatch')
        verify(row['mask']['annotations']);camera=json.loads(verify(row['camera']).read_text())
        if row['camera_pose']!=camera['images'][Path(row['rgb']['path']).name]:raise ValueError('Camera pose mismatch')
        if row['intrinsics_resolution']!=[camera['camera']['width'],camera['camera']['height']]:raise ValueError('Intrinsics resolution mismatch')
        expected_key=f'{plan["video"]}/frame_{row["frame_index"]:010d}__d{row["detection_idx"]}'
        if row['observation_key']!=expected_key:raise ValueError('Observation key mismatch')
        if row['mask']['annotation_id']!=ann['id'] or row['mask']['resolution']!=[854,480]:raise ValueError('Mask convention mismatch')
    expected={(f['frame_index'],i) for f in frames if f['frame_index'] in manifest['observation_frames'] for i in range(len(f['annotations']))}
    if seen!=expected:raise ValueError('Incomplete target-frame detections')
    shutil.copytree(root,output,ignore=shutil.ignore_patterns('__pycache__','*.tar.gz','reconstructions'))
    verify_bundle(output)
    receipt=dict(mode='verified_cache',frontend_manifest_sha256=sha(manifest_path),
        history_frames=len(frames),observations=len(seen),arrays_exact=True,
        limits='Cache import, not regenerated neural features or source-JPEG provenance certification.')
    (output/'frontend_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    plan['source_bundle_manifest_sha256']=sha(root/'input_manifest.json')
    plan['frontend_contract_sha256']=sha(manifest_path)
    plan['prepared_hashes']['frontend_receipt.json']=sha(output/'frontend_receipt.json')
    (output/'input_manifest.json').write_text(json.dumps(plan,indent=2)+'\n')
    return receipt


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();print(json.dumps(prepare(args.manifest,args.output),indent=2))
