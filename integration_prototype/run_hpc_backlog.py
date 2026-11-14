"""Isolated validation runs; replay deferred requests serially within one GPU job."""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--mode',choices=['zero','accumulate','reconstruct'],required=True)
    parser.add_argument('--runtime',type=Path)
    args=parser.parse_args()
    if args.output.exists():raise FileExistsError('Use a fresh output directory')
    if args.mode=='reconstruct' and args.runtime is None:parser.error('GPU mode requires runtime configuration')
    shutil.copytree(args.base,args.output)
    root=args.output.resolve()
    flags=[] if args.mode=='zero' else ['--accumulate']
    if args.mode=='reconstruct':flags+=['--reconstruct']
    plan=json.loads((root/'input_manifest.json').read_text())
    start=time.perf_counter()
    rounds=[]
    limit=2+len(plan['observed_cloud_artifacts']) if args.mode=='reconstruct' else 1
    if args.mode=='reconstruct':
        sys.path.insert(0,str(root))
        from deferred_superflex import process_request
        runtime=json.loads(args.runtime.read_text())['superflex']
    for number in range(limit):
        log=root/f'replay_{number:02d}.log'
        cmd=[sys.executable,'-u',str(root/'run_real_prefix.py'),'--root',str(root),*flags]
        with log.open('x') as stream:
            result=subprocess.run(cmd,stdout=stream,stderr=subprocess.STDOUT)
        content=log.read_text()
        print(content[-3500:],flush=True)
        rounds.append(dict(round=number,returncode=result.returncode,log=log.name))
        if result.returncode==0:
            break
        if args.mode!='reconstruct' or 'PENDING_SUPERFLEX' not in content:
            raise RuntimeError(f'Prefix failed; inspect {log}')
        pending=[p for p in sorted((root/'reconstructions').glob('*/*/request.json')) if not (p.parent/'result.json').exists()]
        if not pending:raise RuntimeError('Pending marker without new requests')
        for request in pending:
            print('WORKER',request.parent,flush=True)
            outcome=process_request(request.parent,runtime=runtime)
            print('WORKER_RESULT',outcome['request_id'],outcome['status'],outcome.get('error',''),flush=True)
    else:
        raise RuntimeError('Exceeded bounded replay count; check request identity stability')
    result=json.loads((root/'result.json').read_text())
    assert result['zero_associations_exact'] and result['zero_model_logits_exact']
    records=json.loads((root/'geometry_transactions.json').read_text())
    updates=[e for row in records for e in row['cloud_updates'] if e.get('diagnostics',{}).get('operation')]
    workers=[json.loads(p.read_text()) for p in (root/'reconstructions').glob('*/*/result.json')]
    summary=dict(mode=args.mode,slurm_job_id=os.environ.get('SLURM_JOB_ID'),rounds=rounds,
                 elapsed_seconds=time.perf_counter()-start,
                 update_statuses=dict(Counter(e['status'] for e in updates)),
                 initializations=sum(e['diagnostics']['operation']=='initialize' and e['status']=='accepted' for e in updates),
                 accepted_fusions=sum(e['diagnostics']['operation']=='register_and_accumulate' and e['status']=='accepted' for e in updates),
                 worker_statuses=dict(Counter(r['status'] for r in workers)),
                 real_superflex_ready=sum(r['status']=='ready' and r['backend']=='superflex' for r in workers),
                 zero_checks_passed=True,baseline_recorded_mismatch_frames=result['baseline_recorded_mismatch_frames'],
                 limits=['Prefix only, geometric weight zero; no tracking improvement assessed.',
                         'Initialization is not an accepted multi-view fusion.',
                         'Serial cached replay; no persistent full-tracker checkpoint.'])
    (root/'controller_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)
    if args.mode=='reconstruct' and not summary['real_superflex_ready']:
        raise RuntimeError('No real SuperFlex result ready; fallback alone does not validate GPU integration')


if __name__=='__main__':main()
