"""Validate trusted official inputs against published rows and prepare a prefix.

Only unpickle files just acquired from the official public author release.
Numeric arrays are exported as allow_pickle=False NPZ for remote execution.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import pickle
import shutil
import sys
import tarfile

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'shared_exports/publish_candidate/SuperFlex/src'))
from shape_tools.memory import observation_features


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inputs',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    if args.output.exists():raise FileExistsError('Preserve previous prefix preparations')
    acquisition=json.loads((args.inputs/'acquisition.json').read_text())
    assert acquisition['status']=='complete'
    for name,info in acquisition['files'].items():assert sha(args.inputs/name)==info['sha256']
    with (args.inputs/'2D_feat_masked_PCA_256d.pkl').open('rb') as stream:apps=pickle.load(stream)
    with (args.inputs/'3D_feat_aligned.pkl').open('rb') as stream:locs=pickle.load(stream)
    raw=json.loads((args.inputs/'object_annotations.json').read_text())['video_annotations']
    annotations={r['frame_name']:r['annotations'] for r in raw};assert len(annotations)==len(raw)
    assert apps.keys()==locs.keys()
    assert list(apps)==sorted(apps)
    published=json.loads((ROOT/'outputs/github_handoff_bbf0e5e/tracks_by_id.json').read_text())
    pred={}
    for tid,items in published['tracks'].items():
        for row in items:
            key=(row['frame'],row['detection_idx']);assert key not in pred
            pred[key]=(int(tid),row)
    errors=[];rows=0
    for frame,features in apps.items():
        anns=annotations[frame];locations=np.asarray(locs[frame]);features=np.asarray(features)
        assert features.shape==(len(anns),256) and locations.shape==(len(anns),3)
        assert np.isfinite(features).all() and np.isfinite(locations).all()
        for i,ann in enumerate(anns):
            value=pred.get((frame,i))
            if value is None or (value[1]['observation_id'],value[1]['name'],value[1]['bbox'])!=(ann['id'],ann['name'],ann['bounding_box']):errors.append([frame,i,'annotation'])
            elif not np.array_equal(np.asarray(value[1]['xyz']),locations[i].astype(float)):errors.append([frame,i,'xyz'])
            rows+=1
    assert rows==len(pred)
    args.output.mkdir(parents=True)
    verification=dict(official_feature_frames=len(apps),official_rows=rows,matched_export_rows=len(pred),
                      metadata_xyz_mismatch_count=len(errors),examples=errors[:20],
                      input_hashes={name:info['sha256'] for name,info in acquisition['files'].items()},
                      limits='Order and XYZ verified against exported rows; original source JPEG provenance is not established by feature pickles.')
    (args.output/'official_input_verification.json').write_text(json.dumps(verification,indent=2)+'\n')
    assert not errors,'Official inputs differ from published observation rows; inspect verification before inference'
    joined=json.loads((ROOT/'outputs/github_handoff_bbf0e5e/compare200_joined_observations.json').read_text())
    lookup={(r['frame_name'],r['annotation_id']):r for r in joined if r['mapping_status']=='exact'}
    geometries={r['observation_key']:r for r in json.loads((ROOT/'outputs/geometric_closure_v1/observations.json').read_text())}
    reps=['da_raw_points','da_raw_superflex','moge_points','moge_superflex']
    frames=[];appearance=[];locations=[];shape_arrays={};cloud_arrays={};offset=0;artifacts={};cloud_artifacts={}
    for frame in apps:
        idx=int(frame.rsplit('_',1)[1])
        if idx>7508:break
        anns=annotations[frame];feature_ids=[];cloud_ids=[]
        for i,a in enumerate(anns):
            ids={};raw_ids={};geo=lookup.get((frame,a['id']))
            if geo:
                original=geometries[geo['observation_key']]
                for rep in reps:
                    feature=observation_features(original,ROOT/'outputs/compare200_749968',rep)
                    if feature is not None:
                        name='f'+str(len(shape_arrays));shape_arrays[name]=feature[1];ids[rep]=name
                        artifacts[geo['observation_key']+'/'+rep]=original['representations'][rep]['sha256']
                for source, rep in [('da','da_raw_points'),('moge','moge_points')]:
                    info=original['representations'][rep]
                    if info['status']=='unavailable':continue
                    path=ROOT/'outputs/compare200_749968'/info['path']
                    assert info['status']=='ready' and sha(path)==info['sha256']
                    with np.load(path,allow_pickle=False) as z:camera_points=z['camera_points'].copy()
                    cloud_id='c'+str(len(cloud_arrays));cloud_arrays[cloud_id]=camera_points
                    raw_ids[source]=cloud_id
                    cloud_artifacts[cloud_id]=dict(input_sha256=info['sha256'],observation_key=geo['observation_key'],source=source)
            cloud_ids.append(raw_ids)
            feature_ids.append(ids)
        frames.append(dict(frame=frame,frame_index=idx,offset=offset,annotations=anns,shape_feature_ids=feature_ids,cloud_ids=cloud_ids,
                           recorded_baseline_assignments={str(i):pred[frame,i][0] for i in range(len(anns))}))
        appearance.append(np.asarray(apps[frame]));locations.append(np.asarray(locs[frame]));offset+=len(anns)
    assert all(f'frame_{n:010d}' in {f['frame'] for f in frames} for n in [2893,5099,7508])
    np.savez_compressed(args.output/'features.npz',app=np.concatenate(appearance),loc=np.concatenate(locations))
    np.savez_compressed(args.output/'shape_features.npz',**shape_arrays)
    np.savez_compressed(args.output/'observed_clouds.npz',**cloud_arrays)
    (args.output/'frames.json').write_text(json.dumps(frames,indent=2)+'\n')
    csv_fps=float(next(r['fps'] for r in csv.DictReader((ROOT/'Whareformer-repo/data/epic_osnom/EPIC_100_video_info.csv').open()) if r['video_id']=='P01_01'))
    # Exact convention in original Config.get_video_data, not the raw CSV float.
    fps=60 if int(csv_fps)==59 else int(csv_fps)
    plan=dict(video='P01_01',fps=fps,csv_fps=csv_fps,fps_policy='original Config.get_video_data: int, 59 becomes 60',target_frames=[2893,5099,7508],representations=reps,
              prefix_frames=len(frames),prefix_observations=offset,shape_artifact_hashes=artifacts,
              observed_cloud_artifacts=cloud_artifacts,
              cloud_conventions=dict(coordinate_convention='camera_points optical camera coordinates',
                                     scale_convention='as exported depth units; inter-view scale unverified'),
              acquisition=acquisition,full_input_verification=verification)
    for source,name in [(ROOT/'integration_prototype/run_real_prefix.py','run_real_prefix.py'),(ROOT/'integration_prototype/shape_adapter.py','shape_adapter.py'),
                        (ROOT/'integration_prototype/geometry_matcher.py','geometry_matcher.py'),
                        (ROOT/'integration_prototype/frame_coordinator.py','frame_coordinator.py'),
                        (ROOT/'integration_prototype/cloud_updater.py','cloud_updater.py'),
                        (ROOT/'integration_prototype/deferred_superflex.py','deferred_superflex.py'),
                        (ROOT/'integration_prototype/cloud_memory.py','cloud_memory.py'),
                        (ROOT/'Whareformer-repo/Starting_checkpoint_whareformer/whareformer.pt','whareformer.pt'),
                        (ROOT/'outputs/github_handoff_fc5aa30/whareformer_config.yaml','effective_config.yaml')]:shutil.copyfile(source,args.output/name)
    shutil.copytree(ROOT/'Whareformer-repo/src',args.output/'original_src',ignore=shutil.ignore_patterns('__pycache__'))
    (args.output/'shape_tools').mkdir();(args.output/'shape_tools/__init__.py').write_text('')
    for module in ['memory.py','geometry.py','metrics.py','comparison.py','pipeline.py']:
        shutil.copyfile(ROOT/'shared_exports/publish_candidate/SuperFlex/src/shape_tools'/module,args.output/'shape_tools'/module)
    plan['prepared_hashes']={p.relative_to(args.output).as_posix():sha(p) for p in args.output.rglob('*') if p.is_file()}
    (args.output/'input_manifest.json').write_text(json.dumps(plan,indent=2)+'\n')
    job='''#!/bin/bash
#SBATCH --job-name=real_whare
#SBATCH --partition=stud
#SBATCH --qos=stud
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:15:00
#SBATCH --output=real_whare_%j.out
#SBATCH --error=real_whare_%j.err
set -euo pipefail
module load /software/modules/miniconda3
eval "$(conda shell.bash hook)"
conda activate "$HOME/.conda/envs/cv-superflex"
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
python -u "$HOME/cv_project/real_prefix_v1/run_real_prefix.py" --root "$HOME/cv_project/real_prefix_v1"
'''
    (args.output/'run.sbatch').write_text(job.replace('real_prefix_v1',args.output.name),newline='\n')
    with tarfile.open(args.output.with_suffix('.tar.gz'),'w:gz') as tar:
        for path in args.output.rglob('*'):
            if path.is_file():tar.add(path,arcname=path.relative_to(args.output).as_posix())
    print(json.dumps({'prefix_frames':len(frames),'prefix_observations':offset,'full_input_verification':verification,'shape_artifacts':len(artifacts)},indent=2))


if __name__=='__main__':main()
