"""Acquire official P01 RGB, join every original observation and run cached geometry."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import zipfile


def read(p): return json.loads(Path(p).read_text())
def save(p, x):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    temp=p.with_suffix(p.suffix+'.tmp');temp.write_text(json.dumps(x,indent=2));temp.replace(p)
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()


def acquire(task):
    import requests
    import numpy as np
    import cv2
    from PIL import Image
    from hpc_campaign import iter_annotations
    project=task.parent; old=project/'campaign_20261115_v1'
    frames=read(old/'bundle/frames.json');fields=read(project/'data_compare200/P01_01/fields.json')
    mapping=read(project/'data_compare200/mappings.json')['P01_01']
    existing={x['observation_key']:x for x in read(old/'geometry/observations.json')}
    url='https://data.bris.ac.uk/datasets/3h91syskeag572hl6tvuovwv4d/frames_rgb_flow/rgb/train/P01/P01_01.tar'
    archive=task/'P01_01.tar';partial=task/'P01_01.tar.partial'
    if not archive.exists():
        start=partial.stat().st_size if partial.exists() else 0
        with requests.get(url,headers={'Range':f'bytes={start}-'} if start else {},stream=True,timeout=(30,120)) as r:
            r.raise_for_status()
            if start and r.status_code!=206:raise RuntimeError('Server did not accept verified resume')
            with partial.open('ab' if start else 'wb') as f:
                for b in r.iter_content(1048576):f.write(b)
        expected=int(requests.head(url,timeout=30).headers['Content-Length'])
        if partial.stat().st_size!=expected:raise ValueError('Incomplete official RGB archive')
        partial.replace(archive)
    rgbdir=task/'inputs/rgb';rgbdir.mkdir(parents=True,exist_ok=True)
    wanted={f['frame']+'.jpg' for f in frames}
    wanted.update(mapping.get('P01_01_'+f['frame']+'.jpg') for f in frames)
    wanted.discard(None)
    # Include mapped adjacent indices, but avoid unrelated unannotated JPEGs.
    extracted=0
    with tarfile.open(archive) as tar:
        for member in tar:
            name=Path(member.name).name
            if not member.isfile() or name not in wanted:continue
            dest=rgbdir/name
            if not dest.exists() or dest.stat().st_size!=member.size:
                with tar.extractfile(member) as source,dest.open('wb') as target:
                    while True:
                        block=source.read(1048576)
                        if not block:break
                        target.write(block)
            extracted+=1
    baseline={f['frame']:{a['id']:(i,a) for i,a in enumerate(f['annotations'])} for f in frames}
    masks=task/'inputs/masks';masks.mkdir(exist_ok=True)
    matched={};conflicts=[];rgbchecks={}
    width,height=fields['camera']['width'],fields['camera']['height']
    annotations=project/'data_compare200/P01_01/annotations.zip'
    with zipfile.ZipFile(annotations) as z:
        member=[n for n in z.namelist() if n.endswith('.json')]
        if len(member)!=1:raise ValueError('Ambiguous official mask archive')
        with z.open(member[0]) as stream:
            for entry in iter_annotations(io.TextIOWrapper(stream,encoding='utf-8')):
                visor=Path(entry['image']['name']).stem
                frame='frame_'+visor.rsplit('_',1)[-1]
                refs=baseline.get(frame)
                if refs is None:continue
                rgb=mapping.get(Path(entry['image']['name']).stem+'.jpg')
                if not rgb or not (rgbdir/rgb).is_file() or rgb not in fields['images']:continue
                if rgb not in rgbchecks:
                    with Image.open(rgbdir/rgb) as im:
                        im.load()
                        if im.size!=(width,height):raise ValueError('RGB/intrinsics resolution mismatch')
                    rgbchecks[rgb]=sha(rgbdir/rgb)
                for a in entry['annotations']:
                    found=refs.get(a['id'])
                    if found is None or not a['segments']:continue
                    i,official=found;key=f'P01_01/{frame}__d{i}'
                    points=[p for poly in a['segments'] for p in poly]
                    if not points:continue
                    bbox=[min(p[0] for p in points),min(p[1] for p in points),max(p[0] for p in points)+1,max(p[1] for p in points)+1]
                    if a['name']!=official['name'] or list(map(int,bbox))!=official['bounding_box']:continue
                    mask=np.zeros((480,854),np.uint8)
                    cv2.fillPoly(mask,[np.asarray(p,np.int32) for p in a['segments'] if p],1)
                    mask=cv2.resize(mask,(width,height),interpolation=cv2.INTER_NEAREST)
                    if not mask.any():continue
                    dest=masks/(key.split('/')[-1]+'.png')
                    mh=hashlib.sha256(mask.tobytes()).hexdigest()
                    if key in matched:
                        if matched[key]['mask_pixel_sha256']!=mh:conflicts.append(key)
                        continue
                    Image.fromarray(mask*255).save(dest)
                    matched[key]=dict(observation_key=key,video='P01_01',frame_index=int(frame.split('_')[-1]),
                        detection_idx=i,annotation_id=a['id'],category=a['name'],bbox=bbox,
                        rgb=str((rgbdir/rgb).resolve()),mask=str(dest.resolve()),
                        intrinsics=fields['camera']['params'][:4],camera_pose=fields['images'][rgb],
                        rgb_sha256=rgbchecks[rgb],mask_sha256=sha(dest),mask_pixel_sha256=mh,
                        visor_frame=entry['image']['name'],rgb_frame=rgb,
                        temporal_alias=Path(rgb).stem!=frame,
                        baseline_alignment_limit='Official feature-frame naming retained; differing VISOR/RGB indices explicitly flagged.')
    targets=[f'P01_01/{f["frame"]}__d{i}' for f in frames for i in range(len(f['annotations']))]
    conflict=set(conflicts)
    pending=[matched[k] for k in targets if k in matched and k not in existing and k not in conflict]
    batches=[]
    for n in range(0,len(pending),512):
        path=task/'batches'/f'{n//512:04d}.json';save(path,dict(schema_version=1,observations=pending[n:n+512]));batches.append(str(path))
    save(task/'batches.json',batches)
    save(task/'inputs/manifest.json',dict(schema_version=1,observations=list(matched.values())))
    config=read(old/'inputs/config.json');save(task/'inputs/config.json',config)
    save(task/'coverage.json',dict(target_observations=len(targets),archive_bytes=archive.stat().st_size,
        archive_sha256=sha(archive),mask_archive_sha256=sha(annotations),extracted_jpegs=extracted,
        verified_rgb_frames=len(rgbchecks),matched_observations=len(matched),reused_geometry=len(existing),
        pending_inference=len(pending),batches=len(batches),conflicting_masks=sorted(conflict),
        missing=[k for k in targets if k not in matched],
        temporal_aliases=[k for k,v in matched.items() if v['temporal_alias']],
        missing_policy='Every target retained; absent or ambiguous masks are explicit and never silently counted as enriched.'))
    print(json.dumps(dict(stage='acquisition_complete',matched=len(matched),missing=len(targets)-len(matched),batches=len(batches))),flush=True)


def lane(task,lane,index):
    batches=read(task/'batches.json')
    if index>=len(batches):return
    manifest=Path(batches[index]);output=task/'geometry'/f'{index:04d}'
    project=task.parent
    env=os.environ.copy();runtime=project/'campaign_20261115_v1/runtime'
    env['PYTHONPATH']=str(runtime)+':'+str(project/'SuperFlex-repo')+':'+str(project/'external/rgb_sources/MoGe-07444410f1e33f402353b99d6ccd26bd31e469e8')
    for stage,environment in [('da','cv-epic-depth'),('moge','cv-moge2'),('clouds','cv-superflex'),('superflex','cv-superflex'),('export','cv-superflex')]:
        python=Path.home()/'.conda/envs'/environment/'bin/python'
        # The environment is not activated: expose its bin (e.g. ninja for SuperFlex C++ extensions).
        stage_env=dict(env,PATH=str(python.parent)+os.pathsep+env.get('PATH',''))
        adapter=task/'retention_tools/retained_pipeline.py'
        entrypoint=[str(adapter)] if (task/'retention_tools/enabled.json').is_file() else ['-m','shape_tools.pipeline']
        subprocess.run([str(python),'-u',*entrypoint,stage,'--manifest',str(manifest),
            '--config',str(task/'inputs/config.json'),'--output',str(output)],env=stage_env,check=True)
    save(task/'completed'/f'{index:04d}.json',dict(batch=index,observations=len(read(manifest)['observations']),
        geometry_manifest=str(output/'observations.json'),status='exported; inspect per-observation statuses'))
    next_index=index+2
    if next_index<len(batches):
        # Slurm account from the environment (not hard-coded); omitted when unset.
        account=os.environ.get('CV_SLURM_ACCOUNT')
        command=['sbatch','--parsable']+([f'--account={account}'] if account else [])+[str(task/'geometry.sbatch'),str(lane),str(next_index)]
        job=subprocess.check_output(command,cwd=task,text=True).strip()
        save(task/'submissions'/f'{next_index:04d}.json',dict(job_id=job,lane=lane,batch=next_index))
        print('NEXT_JOB',job,flush=True)
    completed=list((task/'completed').glob('*.json'))
    if len(completed)==len(batches):
        try:
            descriptor=os.open(task/'aggregation.lock',os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
        except FileExistsError:
            return
        os.close(descriptor)
        old=task.parent/'campaign_20261115_v1/geometry/observations.json'
        rows=read(old)
        for batch_index in range(len(batches)):
            for row in read(task/'geometry'/f'{batch_index:04d}'/'observations.json'):
                row['artifact_root']=str(task/'geometry'/f'{batch_index:04d}')
                rows.append(row)
        coverage=read(task/'coverage.json')
        save(task/'all_geometry.json',dict(existing_artifact_root=str(old.parent),observations=rows))
        save(task/'final_status.json',dict(target_observations=coverage['target_observations'],
            exported_observations=len(rows),missing_inputs=coverage['missing'],
            conflicting_masks=coverage['conflicting_masks'],status='all submitted batches exported; per-observation failures retained'))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['acquire','lane']);p.add_argument('--task',type=Path,required=True)
    p.add_argument('--lane',type=int,default=0);p.add_argument('--index',type=int,default=0);a=p.parse_args()
    if a.stage=='acquire':acquire(a.task.resolve())
    else:lane(a.task.resolve(),a.lane,a.index)
