"""Score completed common-runner exports with verified original evaluation code.

Writes a new report directory, preserving input reports. motmetrics is required
for IDF1; no package installation or inference is performed by this command.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil

from tracking_evaluation import EvaluationPolicy, OriginalTrackingEvaluator, evaluate_report


def evaluate_directory(input_dir,output_dir,source_root,policy):
    input_dir,output_dir=Path(input_dir),Path(output_dir)
    if output_dir.exists():raise FileExistsError('Preserve previous evaluation; choose a new output directory')
    summary=json.loads((input_dir/'summary.json').read_text(encoding='utf-8'))
    rows={};hashes={}
    for variant in summary['variants']:
        name=variant['config']['name']
        path=(input_dir/(name+'.jsonl')).resolve()
        if not path.is_relative_to(input_dir.resolve()):raise ValueError('Invalid variant path')
        rows[name]=[json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line]
        hashes[name]=hashlib.sha256(path.read_bytes()).hexdigest()
        if hashes[name]!=summary.get('prediction_export_sha256',{}).get(name):raise ValueError('Prediction export hash mismatch: '+name)
    evaluator=OriginalTrackingEvaluator(source_root,policy)
    scored=evaluate_report(summary,rows,evaluator)
    scored['evaluation_input_sha256']=hashlib.sha256((input_dir/'summary.json').read_bytes()).hexdigest()
    scored['prediction_export_sha256']=hashes
    output_dir.mkdir(parents=True)
    for name in rows:shutil.copyfile(input_dir/(name+'.jsonl'),output_dir/(name+'.jsonl'))
    for variant in scored['variants']:
        metrics=variant['tracking_metrics']
        if metrics:
            with (output_dir/(variant['config']['name']+'_pcl.csv')).open('x',newline='',encoding='utf-8') as stream:
                writer=csv.DictWriter(stream,fieldnames=['seconds','pcl_percent','correct','total']);writer.writeheader();writer.writerows(metrics['pcl_rows'])
    (output_dir/'summary.json').write_text(json.dumps(scored,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    return scored


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--source-root',type=Path,required=True,help='Verified original Whareformer src directory')
    parser.add_argument('--policy',type=Path,required=True,help='JSON with explicit fps, final_frame and scope')
    args=parser.parse_args()
    report=evaluate_directory(args.input,args.output,args.source_root,EvaluationPolicy(**json.loads(args.policy.read_text())))
    print(json.dumps([dict(name=v['config']['name'],evaluation=v['evaluation_status'],error=v.get('evaluation_error')) for v in report['variants']],indent=2))
    if any(v['evaluation_status']=='failed' for v in report['variants']):raise SystemExit(1)

    if any(v['evaluation_status']!='scored' for v in report['variants']):raise SystemExit(2)
