"""Run configured variants on an existing verified numeric prefix bundle.

No calibration or new data acquisition. Deferred workers execute only when a
runtime configuration is supplied; otherwise requests pause the affected run.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
import time
import types


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--cache',type=Path,required=True)
    parser.add_argument('--superflex-runtime',type=Path)
    args=parser.parse_args()
    if args.output.exists():raise FileExistsError('Preserve existing reports; use a new output directory')
    import numpy as np
    import torch
    import yaml
    from experiment_runner import ExperimentRunner, FrameData, Variant
    from deferred_superflex import process_request, SuperflexConfig
    from cloud_updater import ObservedCloudInput, CloudUpdateConfig
    from cloud_memory import RegistrationConfig
    started=time.perf_counter()
    sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
    root=args.root.resolve()
    plan=json.loads((root/'input_manifest.json').read_text())
    for name,digest in plan['prepared_hashes'].items():
        path=(root/name).resolve()
        if not path.is_relative_to(root) or sha(path)!=digest:raise ValueError('Prepared input hash mismatch: '+name)
    config=json.loads(args.config.read_text())
    variants=[Variant(**v) for v in config['variants']]
    if any(v.metric!='d2' for v in variants):
        raise ValueError('This prepared bundle exports D2 only; spectrum requires actual source descriptors')
    original=config.get('cloud_config',{})
    original=dict(original);registration=RegistrationConfig(**original.pop('registration',{}))
    cloud_config=CloudUpdateConfig(registration=registration,**original)
    superflex_config=SuperflexConfig(**config.get('superflex_config',{}))
    sys.path.insert(0,str(root/'original_src'))
    namespace=types.ModuleType('tracking');namespace.__path__=[str(root/'original_src/tracking')]
    sys.modules['tracking']=namespace
    from tracking.tracker.tracker import StandardTracker
    from tracking.tracker.detection import Detection
    cfg=yaml.safe_load((root/'effective_config.yaml').read_text())
    args.cache.mkdir(parents=True,exist_ok=True)
    assets=args.cache/'assets';assets.mkdir(exist_ok=True)
    checkpoint=root/'whareformer.pt'
    state=torch.load(checkpoint,map_location='cpu',weights_only=True)
    cpu=assets/(sha(checkpoint)+'_cpu.pt')
    if not cpu.exists():torch.save(state,cpu)
    restored=torch.load(cpu,map_location='cpu',weights_only=True)
    if state.keys()!=restored.keys() or not all(torch.equal(state[k],restored[k]) for k in state):
        raise ValueError('CPU checkpoint copy differs')
    torch.set_num_threads(2)
    seed=config.get('seed',0)
    params=copy.deepcopy(cfg['tracking']);params.update(model=cfg['model'],device_id=None,app_dim=256)
    params['matcher_params']['model_path']=str(cpu.resolve())
    def factory():
        torch.manual_seed(seed)
        return StandardTracker(copy.deepcopy(params),plan['fps'])
    with np.load(root/'features.npz',allow_pickle=False) as z:app=z['app'].copy();loc=z['loc'].copy()
    with np.load(root/'shape_features.npz',allow_pickle=False) as z:shapes={k:z[k].copy() for k in z.files}
    needs_clouds=any(v.accumulate for v in variants)
    clouds={}
    if needs_clouds:
        with np.load(root/'observed_clouds.npz',allow_pickle=False) as z:clouds={k:z[k].copy() for k in z.files}
    frames=[]
    for row in json.loads((root/'frames.json').read_text()):
        idx=row['frame_index'];offset=row['offset'];keys=[f'{plan["video"]}/{row["frame"]}__d{i}' for i in range(len(row['annotations']))]
        detections=[Detection(dict(frame=idx,detection_idx=i,obj_name=a['name'],bbox=a['bounding_box'],
                                   app=app[offset+i],loc=loc[offset+i])) for i,a in enumerate(row['annotations'])]
        features={rep:{} for rep in plan['representations']}
        for i,key in enumerate(keys):
            for rep in features:
                feature_id=row['shape_feature_ids'][i].get(rep)
                features[rep][key]=(None,shapes[feature_id],None) if feature_id else None
        raw={source:{} for source in ('da','moge')}
        if needs_clouds:
            for i,key in enumerate(keys):
                for source,cloud_id in row['cloud_ids'][i].items():
                    raw[source][key]=ObservedCloudInput(clouds[cloud_id],source,**plan['cloud_conventions'],
                        observed_only=True,provenance=plan['observed_cloud_artifacts'][cloud_id])
        frames.append(FrameData(detections,dict(frame_name=row['frame'],frame_idx=idx,timestamp=idx/plan['fps']),keys,features,raw))
    worker=None
    if args.superflex_runtime:
        runtime=json.loads(args.superflex_runtime.read_text())['superflex']
        for key in ('checkpoint','config'):
            runtime[key]=str((args.superflex_runtime.resolve().parent/runtime[key]).resolve())
        worker=lambda folder:process_request(folder,runtime=runtime)
    provenance=dict(input_manifest_sha256=sha(root/'input_manifest.json'),
                    baseline_checkpoint_sha256=sha(checkpoint),baseline_config_sha256=sha(root/'effective_config.yaml'),
                    seed=seed,execution_kind='original_pretrained_features',
                    experiment_config_sha256=sha(args.config),
                    code_sha256={n:sha(Path(__file__).parent/n) for n in ['experiment_runner.py','run_experiments.py','shape_adapter.py','frame_coordinator.py','cloud_updater.py','deferred_superflex.py','tracking_evaluation.py']})
    runner=ExperimentRunner(factory,plan['video'],variants,args.cache,cloud_config,superflex_config,
                            worker=worker,provenance=provenance)
    report=runner.run(frames)
    report['cli_wall_seconds_before_export']=time.perf_counter()-started
    runner.write(args.output,report)
    print(json.dumps([dict(name=v['config']['name'],status=v['status'],error=v['error']) for v in report['variants']],indent=2))
    if any(v['status']=='failed' or v['zero_baseline_exact'] is False for v in report['variants']):raise SystemExit(1)
    if any(v['status']=='waiting_for_results' for v in report['variants']):raise SystemExit(2)


if __name__=='__main__':main()
