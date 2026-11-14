"""One command from verified prepared inputs to tracking/evaluation/comparison.

Does not acquire RGB, choose masks, regenerate feature extraction or calibrate
methods. Replays use fresh outputs and an explicitly reused compatible cache.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


def run_pipeline(root,config,output,cache,policy,runtime=None,command_runner=subprocess.run):
    root,config,output,cache,policy=map(Path,(root,config,output,cache,policy))
    if output.exists():raise FileExistsError('Choose a new output directory; preserve previous evidence')
    for path in [root/'input_manifest.json',config,policy]:
        if not path.is_file():raise FileNotFoundError(path)
    if runtime is not None and not Path(runtime).is_file():raise FileNotFoundError(runtime)
    output.mkdir(parents=True)
    code=Path(__file__).resolve().parent
    started=time.perf_counter()
    record=dict(status='running',stages=[],input_manifest_sha256=hashlib.sha256((root/'input_manifest.json').read_bytes()).hexdigest(),
                config_sha256=hashlib.sha256(config.read_bytes()).hexdigest(),policy_sha256=hashlib.sha256(policy.read_bytes()).hexdigest(),
                input_boundary='Prepared masks/appearance/XYZ and geometric artifacts; not an autonomous raw-video frontend.')
    def save():
        record['wall_seconds']=time.perf_counter()-started
        (output/'pipeline_status.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    inference=[sys.executable,str(code/'run_experiments.py'),'--root',str(root),'--config',str(config),
               '--output',str(output/'inference'),'--cache',str(cache)]
    if runtime is not None:inference+=['--superflex-runtime',str(runtime)]
    evaluate=[sys.executable,str(code/'evaluate_experiments.py'),'--input',str(output/'inference'),
              '--output',str(output/'evaluation'),'--source-root',str(root/'original_src'),'--policy',str(policy)]
    compare=[sys.executable,str(code/'summarize_experiments.py'),'--reports',str(output/'evaluation/summary.json'),
             '--output',str(output/'comparison')]
    save()
    for name,command in [('inference',inference),('evaluation',evaluate),('comparison',compare)]:
        begin=time.perf_counter()
        try:
            with (output/(name+'.log')).open('x',encoding='utf-8') as log:
                result=command_runner(command,stdout=log,stderr=subprocess.STDOUT)
            entry=dict(stage=name,returncode=result.returncode,seconds=time.perf_counter()-begin,log=name+'.log')
            record['stages'].append(entry)
            if result.returncode:
                record['status']='waiting_for_results' if name=='inference' and result.returncode==2 else 'failed'
                save();return record
        except Exception as error:
            record['stages'].append(dict(stage=name,error=f'{type(error).__name__}: {error}'))
            record['status']='failed';save();return record
        expected=output/('comparison/comparison.csv' if name=='comparison' else name+'/summary.json')
        if not expected.is_file():
            record['status']='failed';entry['error']='Stage returned success without expected artifact: '+str(expected)
            save();return record
        save()
    record['status']='completed';save()
    return record


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    inputs=parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument('--root',type=Path)
    inputs.add_argument('--frontend-manifest',type=Path)
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--cache',type=Path,required=True)
    parser.add_argument('--policy',type=Path,required=True)
    parser.add_argument('--superflex-runtime',type=Path)
    args=parser.parse_args()
    if args.frontend_manifest:
        from frontend_inputs import prepare
        prepared=args.output.parent/(args.output.name+'_inputs')
        prepare(args.frontend_manifest,prepared)
        args.root=prepared
    result=run_pipeline(args.root,args.config,args.output,args.cache,args.policy,args.superflex_runtime)
    print(json.dumps(result,indent=2))
    if result['status']=='waiting_for_results':raise SystemExit(2)
    if result['status']!='completed':raise SystemExit(1)
