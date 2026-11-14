"""Submit downstream Slurm jobs only after the recorded preflight completes.

Run on the authorized HPC account. Saves each returned job ID immediately,
including partial submissions if a later scheduler request fails.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess


def grouped_script(task,lane):
    """One serial cohort per lane respects MaxSubmitJobsPU=4/MaxJobsPU=2."""
    spec=json.loads((task/'campaign.json').read_text(encoding='utf-8'))
    count=len(spec['variants'][lane]);minutes=count*45
    text=(task/(lane+'.sbatch')).read_text(encoding='utf-8')
    text=re.sub(r'^#SBATCH --array=.*\n','',text,flags=re.M)
    text=re.sub(r'^#SBATCH --time=.*$',f'#SBATCH --time={minutes//60:02}:{minutes%60:02}:00',text,flags=re.M)
    text=text.replace('cvx_'+lane,'cvx_'+lane+'_group').replace(f'logs/{lane}_%A_%a',f'logs/{lane}_group_%j')
    body=f'''BATCH_FAILURE=0
for VARIANT_INDEX in {' '.join(map(str,range(count)))}; do
  RETURN_CODE=0
  timeout --kill-after=30s 45m python -u runtime/integration_prototype/hpc_campaign.py variant --task "$TASK" --lane {lane} --index "$VARIANT_INDEX" || RETURN_CODE=$?
  printf '{{"lane":"{lane}","index":%s,"returncode":%s}}\\n' "$VARIANT_INDEX" "$RETURN_CODE" >> "group_{lane}_results.jsonl"
  if [ "$RETURN_CODE" -ne 0 ]; then BATCH_FAILURE=1; fi
done
python "$TASK/submit_hpc_campaign_grouped.py" --task "$TASK" --finalize
exit "$BATCH_FAILURE"
'''
    text=re.sub(r'^python -u runtime/integration_prototype/hpc_campaign.py variant.*$',lambda m:body,text,flags=re.M)
    path=task/(lane+'_group.sbatch')
    if path.exists() and path.read_text(encoding='utf-8')!=text:raise ValueError('Existing grouped script differs')
    path.write_text(text,encoding='utf-8',newline='\n')
    return path


def schedule_summary(task):
    task=Path(task).resolve();receipt=task/'submitted_jobs.json'
    record=json.loads(receipt.read_text(encoding='utf-8'))
    if 'summarize' in record['jobs']:return record
    lock=task/'summary_submission.lock'
    try:fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    except FileExistsError:return record
    os.close(fd)
    try:
        dependency='afterany:'+record['jobs']['cpu']['id']+':'+record['jobs']['gpu']['id']
        account=subprocess.check_output(['id','-un'],text=True).strip()
        value=subprocess.check_output(['sbatch','--parsable','--account='+account,'--dependency='+dependency,
            str(task/'summarize.sbatch')],cwd=task,text=True).strip().split(';')[0]
        if not re.fullmatch(r'\d+',value):raise ValueError('Unexpected scheduler response')
        record['jobs']['summarize']=dict(id=value,dependency=dependency)
        receipt.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
        print('summarize',value,dependency,flush=True)
        return record
    except Exception:
        lock.unlink();raise


def submit(task,preflight_job,resume=False):
    task=Path(task).resolve()
    receipt=task/'submitted_jobs.json'
    if receipt.exists() and not resume:raise FileExistsError('Preserve submitted jobs; use explicit resume after inspection')
    if not re.fullmatch(r'\d+',preflight_job):raise ValueError('Numeric preflight ID required')
    accounting=subprocess.check_output(['sacct','-j',preflight_job,'--format=JobIDRaw,State,ExitCode','--parsable2','--noheader'],text=True)
    state=[line.split('|') for line in accounting.splitlines() if line.split('|')[0]==preflight_job]
    if len(state)!=1 or state[0][1:3]!=['COMPLETED','0:0']:
        raise RuntimeError('Preflight has not passed: '+accounting)
    if not (task/'inputs/selection.json').is_file():raise FileNotFoundError('Frozen selection missing')
    record=json.loads(receipt.read_text(encoding='utf-8')) if receipt.exists() else dict(preflight=dict(id=preflight_job,state='COMPLETED',exit_code='0:0'),jobs={})
    if record['preflight']['id']!=preflight_job:raise ValueError('Foreign preflight receipt')
    if 'submission_error' in record:record.setdefault('submission_history',[]).append(record.pop('submission_error'))
    record['scheduler_adjustment']=dict(maximum_submitted_jobs=4,maximum_running_jobs=2,
        variant_grouping='19 CPU trials serially in one job, 10 GPU trials serially in one job',
        summary_submission='Submitted once by the first completed cohort; afterany dependency on both cohorts',
        unchanged_trials=True,maximum_gpu_resource_hours=9.5)
    def persist():
        receipt.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    persist()
    for name,dependency in [('geometry','afterok:'+preflight_job),('build',None),('cpu',None),('gpu',None)]:
        if name in record['jobs']:continue
        if name=='build':dependency='afterok:'+record['jobs']['geometry']['id']
        if name in ['cpu','gpu']:dependency='afterok:'+record['jobs']['build']['id']
        script=grouped_script(task,name) if name in ['cpu','gpu'] else task/(name+'.sbatch')
        command=['sbatch','--parsable','--account='+subprocess.check_output(['id','-un'],text=True).strip(),
                 '--dependency='+dependency,str(script)]
        try:
            value=subprocess.check_output(command,cwd=task,text=True).strip().split(';')[0]
            if not re.fullmatch(r'\d+',value):raise ValueError('Unexpected scheduler response: '+value)
            record['jobs'][name]=dict(id=value,dependency=dependency)
            persist();print(name,value,dependency,flush=True)
        except Exception as error:
            record['submission_error']=dict(stage=name,error=str(error));persist();raise
    return record


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--task',type=Path,required=True)
    p.add_argument('--preflight-job')
    p.add_argument('--resume',action='store_true')
    p.add_argument('--finalize',action='store_true')
    a=p.parse_args()
    if a.finalize:schedule_summary(a.task)
    else:
        if not a.preflight_job:p.error('--preflight-job required')
        submit(a.task,a.preflight_job,a.resume)
