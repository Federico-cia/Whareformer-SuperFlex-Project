"""Portable DA-only geometry producer. No remote access or automatic job submission.

Paths in settings are relative to settings; use a new task for changed inputs/code.
Historical full_p01_enrichment.py is intentionally retained for old signed caches.
"""
import argparse
from collections import Counter
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import zipfile


def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))


def save(p, value):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + '.tmp')
    tmp.write_text(json.dumps(value, indent=2, allow_nan=False), encoding='utf-8')
    tmp.replace(p)


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''): h.update(block)
    return h.hexdigest()


def settings(path):
    path = Path(path).resolve(); s = read(path)
    if not re.fullmatch(r'P\d{2}_\d{2}', s['video']): raise ValueError('Invalid video')
    for k in ('task', 'frames', 'fields', 'mapping', 'annotations', 'rgb_tar', 'mesh',
              'runtime', 'superflex_repo', 'geometry_config', 'python_da', 'python_sf'):
        s[k] = str((path.parent / s[k]).resolve())
    if s.get('batch_size', 512) < 1: raise ValueError('Invalid batch_size')
    return s


def annotations(stream):
    # Same streaming parser as hpc_campaign; avoids loading the whole VISOR JSON.
    buffer = ''
    while True:
        b = stream.read(65536)
        if not b: raise ValueError('Missing video_annotations')
        buffer += b
        m = re.search(r'"video_annotations"\s*:\s*\[', buffer)
        if m: buffer = buffer[m.end():]; break
        if len(buffer) > 4*1024**2: raise ValueError('Unexpected annotation header')
    decoder = json.JSONDecoder()
    while True:
        buffer = buffer.lstrip(' \t\r\n,')
        if buffer.startswith(']'): return
        try: value, end = decoder.raw_decode(buffer)
        except json.JSONDecodeError:
            b = stream.read(65536)
            if not b: raise ValueError('Truncated annotation record')
            buffer += b
            if len(buffer) > 16*1024**2: raise ValueError('Oversized annotation record')
            continue
        buffer = buffer[end:]; yield value


def production_config(s):
    cfg = read(s['geometry_config'])
    cfg['sources'] = ['da']; cfg.pop('moge', None)
    cfg['clouds']['pixel_policy'] = 'source'
    for key in ('checkpoint', 'config'):
        p = (Path(s['geometry_config']).parent / cfg['superflex'][key]).resolve()
        if sha(p) != cfg['superflex'][key+'_sha256']: raise ValueError('SuperFlex hash: '+key)
        cfg['superflex'][key] = str(p)
    return cfg


def freeze(s):
    """Fingerprint scientific inputs/settings/code before accepting a resume."""
    files = {k: sha(s[k]) for k in ('frames', 'fields', 'mapping', 'annotations', 'mesh', 'rgb_tar')}
    code = {str(p.relative_to(s['runtime'])): sha(p)
            for p in sorted(Path(s['runtime']).rglob('*.py'))}
    authors = {str(p.relative_to(s['superflex_repo'])): sha(p)
               for p in sorted(Path(s['superflex_repo']).rglob('*.py'))}
    own = {p.name: sha(p) for p in Path(__file__).parent.glob('*.py')}
    return dict(settings=s, files=files, runtime=code, authors=authors, driver=own,
                geometry=production_config(s))


def guard(s):
    """statvfs is supplemented by a mandatory site quota command returning JSON."""
    task = Path(s['task']); task.mkdir(parents=True, exist_ok=True)
    free = shutil.disk_usage(task).free
    command = s.get('quota_command')
    if not command: raise ValueError('Configure quota_command: JSON free_bytes/free_files (personal quota)')
    try:
        quota = json.loads(subprocess.check_output(command, text=True, timeout=30))
        free_files = int(quota['free_files'])
        free_bytes = int(quota['free_bytes'])
    except (OSError,ValueError,KeyError,subprocess.SubprocessError) as error:
        print('Quota unavailable:',error,file=sys.stderr)
        raise SystemExit(75) from error
    free = min(free, free_bytes)
    if free < s.get('reserve_bytes', 2147483648) or free_files < s.get('reserve_files', 12000):
        raise SystemExit(75)
    return dict(free_bytes=free, free_files=free_files)


def prepare(s):
    import numpy as np
    import cv2
    from PIL import Image
    task = Path(s['task']); task.mkdir(parents=True, exist_ok=True)
    guard(s)
    frozen = freeze(s)
    receipt = task/'preparation.json'
    if receipt.exists():
        if read(receipt) != frozen: raise ValueError('Inputs/code/settings changed: use new task')
        if (task/'coverage.json').exists(): return
    save(receipt, frozen)
    video = s['video']; frames = read(s['frames'])
    if isinstance(frames, dict): frames = frames['frames']
    if not frames: raise ValueError('Empty original frame list')
    fields = read(s['fields']); mapping = read(s['mapping'])[video]
    baseline = {}
    targets = []
    for f in frames:
        frame = f['frame']
        if not re.fullmatch(r'frame_\d+', frame) or frame in baseline: raise ValueError('Invalid/duplicate frame')
        by_id = {a['id']: (i, a) for i, a in enumerate(f['annotations'])}
        if len(by_id) != len(f['annotations']): raise ValueError('Duplicate annotation ID')
        baseline[frame] = by_id
        targets.extend(f'{video}/{frame}__d{i}' for i in range(len(f['annotations'])))
    wanted = {mapping.get(video+'_'+f+'.jpg') for f in baseline} - {None}
    rgbdir = task/'inputs/rgb'; rgbdir.mkdir(parents=True, exist_ok=True)
    with tarfile.open(s['rgb_tar']) as tar:
        names = set()
        for member in tar:
            name = Path(member.name).name
            if not member.isfile() or name not in wanted: continue
            if name in names: raise ValueError('Duplicate JPEG in archive')
            names.add(name); dest = rgbdir/name
            if not dest.exists() or dest.stat().st_size != member.size:
                if len(names) % 256 == 1: guard(s)
                with tar.extractfile(member) as src, dest.with_suffix('.tmp').open('wb') as out:
                    shutil.copyfileobj(src, out)
                dest.with_suffix('.tmp').replace(dest)
    width, height = fields['camera']['width'], fields['camera']['height']
    if fields['camera'].get('model', 'PINHOLE') != 'PINHOLE': raise ValueError('Expected PINHOLE camera')
    masks = task/'inputs/masks'; masks.mkdir(exist_ok=True)
    matched = {}; conflicts = set(); rgbchecks = {}
    with zipfile.ZipFile(s['annotations']) as z:
        members = [n for n in z.namelist() if n.endswith('.json')]
        if len(members) != 1: raise ValueError('Ambiguous VISOR archive')
        with z.open(members[0]) as stream:
            for entry in annotations(io.TextIOWrapper(stream, encoding='utf-8')):
                visor = Path(entry['image']['name']).stem
                if not visor.startswith(video+'_'): raise ValueError('VISOR video mismatch')
                frame = 'frame_'+visor.rsplit('_', 1)[-1]; refs = baseline.get(frame)
                if refs is None: continue
                rgb = mapping.get(visor+'.jpg')
                if not rgb or not (rgbdir/rgb).is_file() or rgb not in fields['images']: continue
                if rgb not in rgbchecks:
                    with Image.open(rgbdir/rgb) as im:
                        im.load()
                        if im.size != (width, height): raise ValueError('RGB/camera size mismatch')
                    rgbchecks[rgb] = sha(rgbdir/rgb)
                for a in entry['annotations']:
                    found = refs.get(a['id'])
                    polys = [p for p in a['segments'] if p]
                    if found is None or not polys: continue
                    i, official = found; key = f'{video}/{frame}__d{i}'
                    pts = [p for poly in polys for p in poly]
                    box = [min(p[0] for p in pts), min(p[1] for p in pts),
                           max(p[0] for p in pts)+1, max(p[1] for p in pts)+1]
                    if a['name'] != official['name'] or list(map(int, box)) != official['bounding_box']: continue
                    mask = np.zeros((480,854), np.uint8)
                    cv2.fillPoly(mask, [np.asarray(p, np.int32) for p in polys], 1)
                    mask = cv2.resize(mask, (width,height), interpolation=cv2.INTER_NEAREST)
                    if not mask.any(): continue
                    mh = hashlib.sha256(mask.tobytes()).hexdigest()
                    if key in matched:
                        if matched[key]['mask_pixel_sha256'] != mh: conflicts.add(key)
                        continue
                    dest = masks/(key.split('/')[-1]+'.png'); Image.fromarray(mask*255).save(dest)
                    matched[key] = dict(observation_key=key, video=video, frame_index=int(frame.split('_')[-1]),
                        detection_idx=i, annotation_id=a['id'], category=a['name'], bbox=box,
                        expected_frame_objects=len(refs),
                        rgb=str((rgbdir/rgb).resolve()), mask=str(dest.resolve()),
                        intrinsics=fields['camera']['params'][:4], camera_pose=fields['images'][rgb],
                        rgb_sha256=rgbchecks[rgb], mask_sha256=sha(dest), mask_pixel_sha256=mh,
                        visor_frame=entry['image']['name'], temporal_alias=Path(rgb).stem != frame)
    rows = [matched[k] for k in targets if k in matched and k not in conflicts]
    save(task/'inputs/manifest.json', dict(schema_version=1, observations=rows))
    save(task/'inputs/config.json', production_config(s))
    size = s.get('batch_size',512); batches = []
    for i in range(0,len(rows),size):
        path = task/'batches'/f'{i//size:04d}.json'
        save(path,dict(schema_version=1,observations=rows[i:i+size])); batches.append(str(path))
    save(task/'batches.json', batches)
    save(task/'coverage.json', dict(video=video,target_observations=len(targets), eligible=len(rows),
         missing=[k for k in targets if k not in matched], conflicting_masks=sorted(conflicts),
         temporal_aliases=[r['observation_key'] for r in rows if r['temporal_alias']], batches=len(batches),
         note='Aliases are explicit; equivalence with original feature JPEGs is not certified.'))


def environment(s, python):
    env = os.environ.copy()
    env['PYTHONPATH'] = os.pathsep.join([s['runtime'],s['superflex_repo'],str(Path(__file__).parent)])
    env['PATH'] = str(Path(python).parent)+os.pathsep+env.get('PATH','')
    env.setdefault('PYOPENGL_PLATFORM','egl')
    env['HF_HUB_OFFLINE']='1'; env['TRANSFORMERS_OFFLINE']='1'
    return env


def pipeline(s, stage, manifest, output):
    python = s['python_da'] if stage == 'da' else s['python_sf']
    subprocess.run([python,'-u','-m','shape_tools.pipeline',stage,'--manifest',str(manifest),
                    '--config',str(Path(s['task'])/'inputs/config.json'),'--output',str(output)],
                   env=environment(s,python),check=True)


def run_block(s, index):
    task = Path(s['task']); batches = read(task/'batches.json')
    if not 0 <= index < len(batches): raise ValueError('Block outside manifest')
    if read(task/'preparation.json') != freeze(s): raise ValueError('Changed settings/input/code')
    manifest = Path(batches[index]); output = task/'geometry'/f'{index:04d}'
    guard(s)
    for stage in ('da','clouds','superflex','export'):
        pipeline(s,stage,manifest,output)
    subprocess.run([s['python_da'],'-u',str(Path(__file__).with_name('align_video_scene.py')),
                    '--settings',s['_settings_path'],'--index',str(index)],
                   env=environment(s,s['python_da']),check=True)
    aligned = task/'aligned'/f'{index:04d}'
    for stage in ('superflex','export'): pipeline(s,stage,manifest,aligned)
    raw = read(output/'observations.json'); al = {r['observation_key']:r for r in read(aligned/'observations.json')}
    originals = {r['observation_key']:r for r in read(manifest)['observations']}
    for row in raw:
        key=row['observation_key']; row['detection_idx']=originals[key]['detection_idx']
        row['detection_mapping_status']='verified_id_name_bbox_with_temporal_alias_flag'
        row['artifact_roots']={'raw':str(output),'aligned':str(aligned)}
        row['alignment']=read(aligned/'clouds_da'/__import__('hashlib').sha256(key.encode()).hexdigest()[:24]/'report.json')
        row['aligned_representations']={'da_aligned_'+k.removeprefix('da_'):v
                                      for k,v in al[key]['representations'].items()}
    save(task/'completed'/f'{index:04d}.json',dict(batch=index,observations=raw,
         status='exported; inspect representation/alignment failures'))


def aggregate(s):
    task=Path(s['task']); batches=read(task/'batches.json'); rows=[]; pending=[]
    for i in range(len(batches)):
        p=task/'completed'/f'{i:04d}.json'
        if not p.exists(): pending.append(i); continue
        rows.extend(read(p)['observations'])
    counts=Counter()
    for r in rows:
        for k,v in {**r['representations'],**r['aligned_representations']}.items():
            counts[k+':'+v['status']]+=1
    save(task/'all_geometry.json',dict(video=s['video'],observations=rows))
    save(task/'final_status.json',dict(coverage=read(task/'coverage.json'),pending_blocks=pending,
         exported=len(rows),representations=dict(counts),all_blocks_exported=not pending))


def verify_package(root):
    root=Path(root)
    for line in (root/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        if sha(root/name)!=digest: raise ValueError('Package hash: '+name)


def deliver(s):
    """Copy only validated output artifacts into a portable delivery tree."""
    aggregate(s); task=Path(s['task']); final=read(task/'final_status.json')
    if not final['all_blocks_exported']: raise ValueError('Pending blocks: delivery is incomplete')
    dest=task/'delivery'
    if dest.exists(): raise ValueError('Delivery exists; preserve it or choose a new task')
    dest.mkdir(); rows=read(task/'all_geometry.json')['observations']
    for row in rows:
        for family,field in [('raw','representations'),('aligned','aligned_representations')]:
            root=Path(row['artifact_roots'][family]); prefix=Path(family)/root.name
            for rep in row[field].values():
                for asset in rep.get('artifacts',{}).values():
                    src=root/asset['path']
                    if sha(src)!=asset['sha256']: raise ValueError('Corrupt delivery source: '+str(src))
                    dst=dest/prefix/asset['path']; dst.parent.mkdir(parents=True,exist_ok=True)
                    shutil.copy2(src,dst)
            row['artifact_roots'][family]=prefix.as_posix()
    save(dest/'observations.json',dict(video=s['video'],observations=rows))
    save(dest/'final_status.json',final)
    save(dest/'scientific_config.json',read(task/'inputs/config.json') | {'superflex':
        {k:v for k,v in read(task/'inputs/config.json')['superflex'].items() if k not in ('checkpoint','config')}})
    hashes=[sha(p)+'  '+p.relative_to(dest).as_posix() for p in sorted(dest.rglob('*')) if p.is_file()]
    (dest/'SHA256SUMS').write_text('\n'.join(hashes)+'\n',encoding='utf-8')
    with tarfile.open(task/(s['video']+'_geometry.tar.gz'),'w:gz') as tar: tar.add(dest,arcname=s['video'])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('stage',choices=['prepare','run','aggregate','deliver','verify'])
    p.add_argument('--settings',type=Path,default=Path('settings.json'))
    p.add_argument('--index',type=int,default=0); a=p.parse_args()
    if a.stage=='verify': verify_package(Path(__file__).parent); return
    s=settings(a.settings); s['_settings_path']=str(a.settings.resolve())
    if a.stage=='prepare': prepare(s)
    elif a.stage=='aggregate': aggregate(s)
    elif a.stage=='deliver': deliver(s)
    else:
        lock=Path(s['task'])/f'block_{a.index:04d}.lock'
        fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
        os.close(fd)
        try: run_block(s,a.index)
        finally: lock.unlink()


if __name__=='__main__': main()
