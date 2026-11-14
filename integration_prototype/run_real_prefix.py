"""Original tracker vs shape-aware zero-weight tracker on official input prefix.

Requires a prepared numeric feature NPZ, real annotation rows, and shape
descriptors. No synthetic visual feature fallback is permitted.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
import time
import types

import numpy as np
import torch
import yaml


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True)
    p.add_argument('--accumulate',action='store_true',help='Enable candidate rigid accumulation after association; no new SuperFlex inference')
    p.add_argument('--reconstruct',action='store_true',help='Export deferred SuperFlex requests, block/replay until results exist; requires --accumulate')
    args=p.parse_args();root=args.root
    if args.reconstruct and not args.accumulate:p.error('--reconstruct requires --accumulate')
    sys.path.insert(0,str(root/'original_src'))
    # Isolate the tracker package: its top-level __init__ imports VideoInstance
    # and LMDB even though this runner already has prepared numeric inputs.
    # Computational tracker/matcher/model files remain unchanged.
    tracking_package=types.ModuleType('tracking')
    tracking_package.__path__=[str(root/'original_src/tracking')]
    sys.modules['tracking']=tracking_package
    from tracking.tracker.tracker import StandardTracker
    from tracking.tracker.detection import Detection
    from geometry_matcher import GeometryMatcher, GeometryConfig
    from frame_coordinator import FrameCoordinator

    assert not (root/'result.json').exists()
    checkpoint=root/'whareformer.pt'
    assert hashlib.sha256(checkpoint.read_bytes()).hexdigest()=='5b2e6692461f837ec662d0ac75a5f8c08e4fa9778e5c1b9833598cf90a58ee1d'
    # Original matcher torch.load has no map_location. Preserve its source and
    # prepare a CPU-serialized copy with bit-identical tensors for CPU-only jobs.
    state=torch.load(checkpoint,map_location='cpu',weights_only=True)
    cpu_checkpoint=root/'whareformer_cpu.pt'
    torch.save(state,cpu_checkpoint)
    roundtrip=torch.load(cpu_checkpoint,map_location='cpu',weights_only=True)
    assert state.keys()==roundtrip.keys() and all(torch.equal(state[k],roundtrip[k]) for k in state)
    cfg=yaml.safe_load((root/'effective_config.yaml').read_text())
    frames=json.loads((root/'frames.json').read_text())
    plan=json.loads((root/'input_manifest.json').read_text())
    with np.load(root/'features.npz',allow_pickle=False) as z:app=z['app'].copy();loc=z['loc'].copy()
    with np.load(root/'shape_features.npz',allow_pickle=False) as z:shapes={k:z[k].copy() for k in z.files}
    clouds={}
    if args.accumulate:
        from cloud_updater import ObservedCloudUpdater, ObservedCloudInput
    if args.reconstruct:
        from deferred_superflex import DeferredSuperflex
    if args.accumulate:
        cloud_path=root/'observed_clouds.npz'
        assert hashlib.sha256(cloud_path.read_bytes()).hexdigest()==plan['prepared_hashes']['observed_clouds.npz']
        with np.load(cloud_path,allow_pickle=False) as z:clouds={k:z[k].copy() for k in z.files}
    torch.set_num_threads(2);torch.manual_seed(0)
    params=copy.deepcopy(cfg['tracking']);params.update(model=cfg['model'],device_id=None,app_dim=256)
    params['matcher_params']['model_path']=str(cpu_checkpoint)
    baseline=StandardTracker(copy.deepcopy(params),plan['fps'])
    representations=plan['representations']
    augmented={}
    for rep in representations:
        tracker=StandardTracker(copy.deepcopy(params),plan['fps'])
        tracker.matcher=GeometryMatcher(tracker.matcher, 'P01_01',
            GeometryConfig(mode='active', representation=rep, weight=0))
        augmented[rep]=tracker
    coordinators={rep:FrameCoordinator(t,ObservedCloudUpdater() if args.accumulate else None,
        DeferredSuperflex(root/'reconstructions'/rep) if args.reconstruct and rep.endswith('_superflex') else None) for rep,t in augmented.items()}
    captures=[]
    baseline.matcher.model.register_forward_hook(lambda mod,inp,out:captures.append(out.detach().clone()))
    def assignment(tracker):
        return {int(t.history[-1]['detection_idx']):int(t.track_id) for t in tracker.tracks if t.time_since_update==0}
    checks={rep:dict(frames=0,model_logit_comparisons=0,valid_shape_distances=0) for rep in representations}
    observations_log=[];baseline_mismatches=[];start=time.perf_counter()
    for processed,frame in enumerate(frames,1):
        idx=frame['frame_index'];names=frame['annotations'];keys=[f'P01_01/{frame["frame"]}__d{i}' for i in range(len(names))]
        offset=frame['offset'];detections=[]
        for i,a in enumerate(names):
            detections.append(Detection(dict(frame=idx,detection_idx=i,obj_name=a['name'],bbox=a['bounding_box'],app=app[offset+i],loc=loc[offset+i])))
        metadata=dict(frame_name=frame['frame'],frame_idx=idx,timestamp=idx/plan['fps'])
        captures.clear();baseline.update(detections,metadata);expected=assignment(baseline)
        if expected!={int(k):v for k,v in frame['recorded_baseline_assignments'].items()}:
            baseline_mismatches.append(dict(frame=frame['frame'],reproduced=expected,recorded=frame['recorded_baseline_assignments']))
        for rep,tracker in augmented.items():
            features={}
            for i,key in enumerate(keys):
                feature_id=frame['shape_feature_ids'][i].get(rep)
                features[key]=(None,shapes[feature_id],np.zeros(3)) if feature_id else None
            geometry_inputs={}
            if args.accumulate:
                source='da' if rep.startswith('da_raw_') else 'moge'
                for i,key in enumerate(keys):
                    cloud_id=frame['cloud_ids'][i].get(source)
                    if cloud_id:
                        geometry_inputs[key]=ObservedCloudInput(clouds[cloud_id],source,
                            **plan['cloud_conventions'],observed_only=True,
                            provenance=plan['observed_cloud_artifacts'][cloud_id])
            transaction=coordinators[rep].step(detections,metadata,keys,features,geometry_inputs)
            reconstruction_events=[]
            if coordinators[rep].snapshot()['pending_reconstructions']:
                try:
                    reconstruction_events=coordinators[rep].resolve_reconstructions()
                except FileNotFoundError:
                    print('PENDING_SUPERFLEX',json.dumps(dict(representation=rep,frame_index=idx,
                        requests=coordinators[rep].snapshot()['pending_reconstructions'],
                        cache=str(root/'reconstructions'/rep))),flush=True)
                    raise SystemExit('Process deferred requests, then replay this prefix from the start; no future frames were processed.')
            assert assignment(tracker)==expected,(rep,frame['frame'],'association mismatch')
            if captures:
                assert np.array_equal(captures[-1].numpy(),tracker.matcher.last_logits),(rep,frame['frame'],'model logits mismatch')
                assert np.array_equal(captures[-1].numpy(),tracker.matcher.last_score['logits'])
                checks[rep]['model_logit_comparisons']+=1
            valid=int(tracker.matcher.last_score['valid'].sum());checks[rep]['valid_shape_distances']+=valid
            checks[rep]['frames']+=1
            if valid or idx in plan['target_frames'] or geometry_inputs:
                observations_log.append(dict(representation=rep,frame_index=idx,valid_shape_distances=valid,
                    assignments=transaction['assignments'],memory=tracker.matcher.snapshot(),
                    shape_versions_before=transaction['before']['shapes'],shape_versions_after=transaction['after']['shapes'],
                    cloud_updates=transaction['updates'],reconstruction_events=reconstruction_events,
                    published_reconstructions=tracker.matcher.geometry.reconstruction_snapshot(),
                    cloud_states={tid:state['value'].summary() for tid,state in transaction['after']['geometry'].items()}))
        if processed%500==0 or idx in plan['target_frames']:print('PROGRESS',processed,idx,flush=True)
    result=dict(video='P01_01',frames=len(frames),last_frame=frames[-1]['frame_index'],observations=len(app),
                checks=checks,zero_associations_exact=True,zero_model_logits_exact=True,
                accumulation_enabled=args.accumulate,reconstruction_enabled=args.reconstruct,
                cloud_code_sha256={n:hashlib.sha256((Path(__file__).parent/n).read_bytes()).hexdigest() for n in ['cloud_updater.py','cloud_memory.py']} if args.accumulate else {},
                baseline_recorded_mismatch_frames=len(baseline_mismatches),baseline_mismatch_examples=baseline_mismatches[:10],
                baseline_track_count=len(baseline.tracks),elapsed_seconds=time.perf_counter()-start,
                checkpoint_sha256=hashlib.sha256(checkpoint.read_bytes()).hexdigest(),torch=torch.__version__,
                cpu_checkpoint_sha256=hashlib.sha256(cpu_checkpoint.read_bytes()).hexdigest(),cpu_checkpoint_tensors_exact=True,
                source='original released appearance PCA-256 and aligned XYZ; no synthetic features',
                input_manifest_sha256=hashlib.sha256((root/'input_manifest.json').read_bytes()).hexdigest(),
                runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                geometry_matcher_sha256=hashlib.sha256((Path(__file__).parent/'geometry_matcher.py').read_bytes()).hexdigest(),
                frame_coordinator_sha256=hashlib.sha256((Path(__file__).parent/'frame_coordinator.py').read_bytes()).hexdigest(),
                geometry_configs={rep:t.matcher.config.to_dict() for rep,t in augmented.items()},
                package_initialization='tracking namespace isolated from unused VideoInstance/LMDB entry point',
                limits=['Prefix reproduction only, no full-video metrics or claimed tracking improvement.',
                        'Zero-weight integration; no calibrated nonzero method tested.',
                        'Accumulation alone retains separate forms; --reconstruct enables deferred SuperFlex publication. Input scale is unverified.',
                        'Shape memory updated only at available exact-mapped geometry; two temporal aliases not used.'])
    (root/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    (root/'geometry_transactions.json').write_text(json.dumps(observations_log,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
