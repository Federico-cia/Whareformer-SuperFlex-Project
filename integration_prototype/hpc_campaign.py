"""Bounded full-history development campaign using existing, verified assets.

Stages freeze selection before inference, regenerate sparse RGB geometry, merge
it into the full official feature history, then run isolated paired variants.
No fusion gate, network weight or PCA fitting is modified here.
"""
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import tarfile
import zipfile

import numpy as np


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(value,stream,indent=2,allow_nan=False);stream.write('\n')


def iter_annotations(stream):
    buffer=''
    while True:
        block=stream.read(65536)
        if not block:raise ValueError('Missing video_annotations')
        buffer+=block
        marker=re.search(r'"video_annotations"\s*:\s*\[',buffer)
        if marker:buffer=buffer[marker.end():];break
        if len(buffer)>4*1024**2:raise ValueError('Unexpected annotation header')
    decoder=json.JSONDecoder()
    while True:
        buffer=buffer.lstrip(' \t\r\n,')
        if buffer.startswith(']'):return
        try:value,end=decoder.raw_decode(buffer)
        except json.JSONDecodeError:
            block=stream.read(65536)
            if not block:raise ValueError('Truncated annotations')
            buffer+=block
            if len(buffer)>16*1024**2:raise ValueError('Oversized annotation record')
            continue
        buffer=buffer[end:];yield value


def exact_observations(entry,rgb,baseline,targets):
    """Join observation IDs only within the same exact frame; no track GT."""
    index=int(rgb.split('_')[-1].split('.')[0])
    visor=int(entry['image']['name'].rsplit('_',1)[1].split('.')[0])
    if visor!=index:return [],['temporal_alias']
    reference=baseline.get(Path(rgb).stem)
    if reference is None:return [],['frame_missing_official_features']
    by_id={a['id']:(i,a) for i,a in enumerate(reference)}
    if len(by_id)!=len(reference):raise ValueError('Duplicate official annotation ID')
    rows=[];excluded=[]
    for annotation_index,ann in enumerate(entry['annotations']):
        if not any(re.search(r'(?<!\w)'+re.escape(word)+r'(?!\w)',ann['name'].lower()) for word in targets):
            continue
        found=by_id.get(ann['id'])
        if found is None:excluded.append('annotation_id_not_in_official_frame');continue
        detection_idx,official=found
        points=[p for poly in ann['segments'] for p in poly]
        if not points:excluded.append('empty_mask');continue
        box=[min(p[0] for p in points),min(p[1] for p in points),max(p[0] for p in points)+1,max(p[1] for p in points)+1]
        if ann['name']!=official['name'] or list(map(int,box))!=official['bounding_box']:
            excluded.append('annotation_name_or_bbox_mismatch');continue
        rows.append(dict(annotation_index=annotation_index,detection_idx=detection_idx,
            annotation_id=ann['id'],category=ann['name'],segments=ann['segments'],bbox=official['bounding_box']))
    return rows,excluded


def select(task,spec):
    import cv2
    from PIL import Image
    from frontend_inputs import verify_bundle
    assets=spec['assets'];data=Path(assets['source_data']);base=Path(assets['baseline_bundle'])
    if sha(base/'input_manifest.json')!=assets['baseline_manifest_sha256']:
        raise ValueError('Unexpected baseline history manifest')
    plan,frames=verify_bundle(base)
    if plan['coverage']['complete_official_sequence'] is not True:raise ValueError('Incomplete baseline history')
    baseline={r['frame']:r['annotations'] for r in frames}
    source_receipt={}
    for name,expected in spec['source_hashes'].items():
        path=data/name
        actual=sha(path)
        if actual!=expected:raise ValueError('Source mismatch: '+name)
        source_receipt[name]=actual
    config=read(assets['geometry_config'])
    for source in ['moge','superflex']:
        for key in ['checkpoint']+(['config'] if source=='superflex' else []):
            if sha(config[source][key])!=config[source][key+'_sha256']:
                raise ValueError('Neural checkpoint/config mismatch')
    for relative,digest in config['external_code'].items():
        if sha(Path(assets['project'])/relative)!=digest:raise ValueError('External source mismatch')
    fields=read(data/'fields.json');mapping=read(assets['mapping'])['P01_01']
    targets=spec['selection']['target_nouns']
    if set(targets)!=set(read(data/'ready/selection.json')['target_nouns']):
        raise ValueError('Target category policy changed')
    blob=(data/'rgb_prefix.bin').read_bytes();recovered={}
    with tarfile.open(fileobj=io.BytesIO(blob),mode='r:') as archive:
        try:
            for member in archive:
                if member.offset_data+member.size>len(blob):break
                name=Path(member.name).name
                if member.isfile() and re.fullmatch(r'frame_\d{10}\.jpg',name):
                    value=blob[member.offset_data:member.offset_data+member.size]
                    if not value.startswith(b'\xff\xd8') or not value.endswith(b'\xff\xd9'):
                        raise ValueError('Incomplete JPEG')
                    recovered[name]=value
        except tarfile.ReadError:pass
    candidates={};exclusions=Counter();scanned=0
    width,height=fields['camera']['width'],fields['camera']['height']
    with zipfile.ZipFile(data/'annotations.zip') as archive:
        names=[n for n in archive.namelist() if n.endswith('.json')]
        if len(names)!=1:raise ValueError('Ambiguous annotation JSON')
        with archive.open(names[0]) as raw:
            for entry in iter_annotations(io.TextIOWrapper(raw,encoding='utf-8')):
                scanned+=1
                key=Path(entry['image']['name']).stem+'.jpg';rgb=mapping.get(key)
                if rgb not in recovered or rgb not in fields['images']:continue
                rows,why=exact_observations(entry,rgb,baseline,targets);exclusions.update(why)
                retained=[]
                for row in rows:
                    mask=np.zeros((480,854),np.uint8)
                    cv2.fillPoly(mask,[np.asarray(poly,np.int32) for poly in row['segments'] if poly],1)
                    mask=cv2.resize(mask,(width,height),interpolation=cv2.INTER_NEAREST)
                    if int(mask.sum())<spec['selection']['minimum_mask_pixels']:
                        exclusions['small_mask']+=1;continue
                    retained.append(row)
                if retained:
                    if rgb in candidates:raise ValueError('Multiple exact VISOR entries for one RGB')
                    candidates[rgb]=retained
    ordered=sorted(candidates);cap=spec['selection']['maximum_frames']
    chosen=ordered if len(ordered)<=cap else [ordered[round(i*(len(ordered)-1)/(cap-1))] for i in range(cap)]
    output=task/'inputs'
    if output.exists():raise FileExistsError('Preserve frozen selection')
    output.mkdir();(output/'rgb').mkdir();(output/'masks').mkdir()
    observations=[]
    for rgb in chosen:
        payload=recovered[rgb];dest=output/'rgb'/rgb;dest.write_bytes(payload)
        with Image.open(dest) as image:
            if image.size!=(width,height):raise ValueError('RGB/intrinsics resolution mismatch')
        pose=fields['images'][rgb]
        if len(pose)!=7 or not np.isfinite(pose).all():raise ValueError('Invalid camera pose')
        index=int(Path(rgb).stem.split('_')[-1])
        for selected in candidates[rgb]:
            i=selected['detection_idx'];mask=np.zeros((480,854),np.uint8)
            cv2.fillPoly(mask,[np.asarray(poly,np.int32) for poly in selected['segments'] if poly],1)
            mask=cv2.resize(mask,(width,height),interpolation=cv2.INTER_NEAREST)
            mask_path=output/'masks'/f'{Path(rgb).stem}__d{i}.png'
            Image.fromarray(mask*255).save(mask_path)
            observations.append(dict(observation_key=f'P01_01/{Path(rgb).stem}__d{i}',video='P01_01',
                frame_index=index,rgb='rgb/'+rgb,mask='masks/'+mask_path.name,
                category=selected['category'],annotation_index=selected['annotation_index'],
                detection_idx=i,annotation_id=selected['annotation_id'],bbox=selected['bbox'],
                intrinsics=fields['camera']['params'][:4],camera_pose=pose,
                rgb_sha256=sha(dest),mask_sha256=sha(mask_path),
                visor_frame=f'P01_01_frame_{index:010d}.png'))
    receipt=dict(source_hashes=source_receipt,source_mapping_sha256=sha(assets['mapping']),
        baseline_manifest_sha256=sha(base/'input_manifest.json'),
        recovered_rgb=len(recovered),scanned_visor_entries=scanned,eligible_frames=len(ordered),
        selected_frames=len(chosen),selected_observations=len(observations),exclusions=dict(exclusions),
        selection=spec['selection'],categories=dict(Counter(r['category'] for r in observations)),
        limits='Availability/development sample, not physical identity GT or held-out tracking test.')
    if len(chosen)<spec['selection']['minimum_frames'] or len(observations)<spec['selection']['minimum_observations']:
        save(task/'selection_insufficient.json',receipt);raise ValueError('Expanded coverage floor not met')
    save(output/'manifest.json',dict(schema_version=1,observations=observations))
    save(output/'selection.json',receipt)
    config['clouds']['minimum_points']=64
    save(output/'config.json',config)
    print(json.dumps(receipt,indent=2),flush=True)


def validate_geometry(task):
    from shape_tools.comparison import file_hash
    rows=read(task/'geometry/observations.json');inputs=read(task/'inputs/manifest.json')['observations']
    expected={r['observation_key']:r for r in inputs}
    if {r['observation_key'] for r in rows}!=set(expected):raise ValueError('Incomplete geometry export')
    counts=Counter()
    for row in rows:
        for rep,info in row['representations'].items():
            counts[rep+'/'+info['status']]+=1
            if info['status']=='ready':
                path=(task/'geometry'/info['path']).resolve()
                if not path.is_relative_to((task/'geometry').resolve()) or file_hash(path)!=info['sha256']:
                    raise ValueError('Geometry artifact path/hash mismatch')
    return dict(observations=len(rows),representations=dict(counts))


def build(task,spec):
    from frontend_inputs import verify_bundle
    from shape_tools.memory import observation_features
    base=Path(spec['assets']['baseline_bundle']);plan,frames=verify_bundle(base)
    expected=read(task/'inputs/manifest.json')['observations'];lookup={r['observation_key']:r for r in expected}
    geometry=read(task/'geometry/observations.json');validation=validate_geometry(task)
    out=task/'bundle'
    if out.exists():raise FileExistsError(out)
    out.mkdir();shapes={};clouds={};cloud_artifacts={};shape_artifacts={}
    for name in ['original_src','shape_tools']:
        shutil.copytree(base/name,out/name,ignore=shutil.ignore_patterns('__pycache__'))
    for name in ['features.npz','whareformer.pt','effective_config.yaml']:
        shutil.copyfile(base/name,out/name)
    by_frame={r['frame_index']:r for r in frames}
    for frame in frames:
        frame['shape_feature_ids']=[{} for _ in frame['annotations']]
        frame['cloud_ids']=[{} for _ in frame['annotations']]
    for row in geometry:
        key=row['observation_key'];entry=lookup[key];frame=by_frame[entry['frame_index']];i=entry['detection_idx']
        ann=frame['annotations'][i]
        if (ann['id'],ann['name'],ann['bounding_box'])!=(entry['annotation_id'],entry['category'],entry['bbox']):
            raise ValueError('Geometry/official observation mismatch')
        for source in ['da','moge']:
            for suffix in ['points','superflex']:
                rep=source+'_'+suffix;target=('da_raw_' if source=='da' else 'moge_')+suffix
                feature=observation_features(row,task/'geometry',rep)
                if feature is not None:
                    name='f'+str(len(shapes));shapes[name]=feature[1]
                    frame['shape_feature_ids'][i][target]=name
                    shape_artifacts[key+'/'+target]=row['representations'][rep]['sha256']
            info=row['representations'][source+'_points']
            if info['status']=='ready':
                with np.load(task/'geometry'/info['path'],allow_pickle=False) as z:cloud=z['camera_points'].copy()
                name='c'+str(len(clouds));clouds[name]=cloud;frame['cloud_ids'][i][source]=name
                cloud_artifacts[name]=dict(input_sha256=info['sha256'],observation_key=key,source=source)
    np.savez_compressed(out/'shape_features.npz',**shapes)
    np.savez_compressed(out/'observed_clouds.npz',**clouds)
    save(out/'frames.json',frames)
    coverage=dict(expected_feature_frames=len(frames),expected_observations=plan['coverage']['expected_observations'],
        prepared_frames=len(frames),prepared_observations=plan['coverage']['expected_observations'],
        first_frame=frames[0]['frame_index'],final_frame=frames[-1]['frame_index'],complete_official_sequence=True,
        geometry_frames=sum(any(r['cloud_ids']) for r in frames),
        shape_observations={rep:sum(rep in ids for frame in frames for ids in frame['shape_feature_ids']) for rep in plan['representations']},
        observed_clouds={s:sum(s in ids for frame in frames for ids in frame['cloud_ids']) for s in ['da','moge']},
        attempted_geometry_observations=len(expected),metadata_xyz_mismatch_count=0)
    ready=min(coverage['observed_clouds'].values())
    if ready<spec['selection']['minimum_observations']:raise ValueError('Geometry ready-coverage floor not met')
    manifest=dict(plan,coverage=coverage,observed_cloud_artifacts=cloud_artifacts,shape_artifact_hashes=shape_artifacts,
        input_boundary='Original official appearance/PCA/scene XYZ reused byte-identically; selected RGB/masks regenerated DA/MoGE clouds and SuperFlex observation forms.',
        campaign_spec_sha256=sha(task/'campaign.json'),selection_sha256=sha(task/'inputs/selection.json'),
        source_manifests=dict(baseline_input_manifest=sha(base/'input_manifest.json'),
            observation_manifest=sha(task/'inputs/manifest.json'),geometry_manifest=sha(task/'geometry/observations.json')),
        geometry_manifest_sha256=sha(task/'geometry/observations.json'))
    manifest['prepared_hashes']={p.relative_to(out).as_posix():sha(p) for p in out.rglob('*') if p.is_file()}
    save(out/'input_manifest.json',manifest);verify_bundle(out)
    save(task/'bundle_receipt.json',dict(coverage=coverage,geometry=validation,
        baseline_feature_bytes_identical=sha(out/'features.npz')==sha(base/'features.npz')))
    print(json.dumps(coverage,indent=2),flush=True)


def configurations():
    """Finite development sweep frozen before new results; no winner selected."""
    cpu=[dict(name='W0',method='W0')]
    gpu=[]
    for source in ['da','moge']:
        cpu.append(dict(name='G0_'+source,method='G0',source=source))
        gpu.append(dict(name='Sacc_'+source+'_zero',method='S-accumulo',source=source,weight=0.))
        for method,prefix in [('S-separata','Ssep'),('P-accumulo','Pacc'),('S-accumulo','Sacc')]:
            for weight,w in [(0.1,'01'),(1.,'10')]:
                for neutral,n in [(0.,'00'),(0.1,'01')]:
                    variant=dict(name=f'{prefix}_{source}_w{w}_n{n}',method=method,source=source,
                        weight=weight,neutral_distance=neutral,metric='d2',capacity=2)
                    (gpu if method=='S-accumulo' else cpu).append(variant)
    return dict(cpu=cpu,gpu=gpu)


def run_variant(task,spec,lane,index):
    import subprocess
    import sys
    rows=configurations()[lane];variant=rows[index];name=variant['name']
    configs=task/'configs';configs.mkdir(exist_ok=True)
    cfg=configs/(name+'.json')
    save(cfg,dict(seed=0,torch_threads=1,tracker_device='cpu',variants=[variant],
        purpose='Finite development sweep; no held-out score or efficacy conclusion. Fusion gates unchanged.'))
    output=task/'runs'/name;cache=task/'caches'/name
    code=Path(__file__).resolve().parent
    command=[sys.executable,str(code/'run_pipeline.py'),'--root',str(task/'bundle'),
        '--config',str(cfg),'--output',str(output),'--cache',str(cache),'--policy',str(task/'policy.json')]
    if lane=='gpu':command+=['--superflex-runtime',str(task/'inputs/config.json')]
    subprocess.run(command,check=True)


def summarize(task,spec):
    from summarize_experiments import write_tables
    expected=[row for lane in configurations().values() for row in lane]
    rows=[];paths=[];baseline=None
    baseline_path=task/'runs/W0/inference/W0.jsonl'
    if baseline_path.is_file():
        baseline=[json.loads(line)['assignments'] for line in baseline_path.open(encoding='utf-8')]
    for variant in expected:
        name=variant['name'];path=task/'runs'/name/'evaluation/summary.json';status=task/'runs'/name/'pipeline_status.json'
        entry=dict(name=name,pipeline=read(status) if status.is_file() else dict(status='not_completed'))
        if path.is_file():
            report=read(path);v=report['variants'][0];entry.update(counts=v['counts'],tracking_metrics=v['tracking_metrics'])
            predicted=[json.loads(line)['assignments'] for line in (task/'runs'/name/'inference'/(name+'.jsonl')).open(encoding='utf-8')]
            entry['assignment_differences_vs_W0']=None if baseline is None else sum(sum(a[k]!=b[k] for k in a) for a,b in zip(predicted,baseline))
            if variant.get('weight',0)==0 and baseline is not None and predicted!=baseline:
                raise ValueError('Zero control differs from W0: '+name)
            paths.append(path)
        rows.append(entry)
    output=task/'campaign_summary.json'
    save(output,dict(development_only=True,expected_variants=len(expected),
        complete=sum(r['pipeline']['status']=='completed' for r in rows),variants=rows,
        limits=['One development video, no held-out generalization.','Admission is not physical validation.','No automatic winner selection.']))
    if paths:write_tables(paths,task/'comparison')
    print(json.dumps(dict(expected=len(expected),complete=sum(r['pipeline']['status']=='completed' for r in rows)),indent=2))
    if any(r['pipeline']['status']!='completed' for r in rows):raise SystemExit(2)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('stage',choices=['select','build','variant','summarize'])
    p.add_argument('--task',type=Path,required=True)
    p.add_argument('--lane',choices=['cpu','gpu'])
    p.add_argument('--index',type=int)
    a=p.parse_args();task=a.task.resolve();spec=read(task/'campaign.json')
    if a.stage=='select':select(task,spec)
    elif a.stage=='build':build(task,spec)
    elif a.stage=='variant':run_variant(task,spec,a.lane,a.index)
    else:summarize(task,spec)
