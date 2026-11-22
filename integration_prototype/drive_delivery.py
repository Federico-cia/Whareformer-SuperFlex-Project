"""Immutable project delivery and verified Drive pilot. Never evicts source data."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import tarfile
import time


def digest(path, algorithm='sha256'):
    h=hashlib.new(algorithm)
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()


def save(path, value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.writing')
    tmp.write_text(json.dumps(value,indent=2,allow_nan=False),encoding='utf-8');tmp.replace(path)


def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))


def safe_relative(name):
    p=PurePosixPath(name)
    if not name or p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name:
        raise ValueError('Unsafe relative path')
    return p


def pack_directory(source, archive, prefix, extras=None):
    """Snapshot regular files only; all member contents are independently checksummed."""
    source=Path(source).resolve();archive=Path(archive).resolve();safe_relative(prefix)
    if archive.is_relative_to(source): raise ValueError('Archive cannot be inside its source')
    if (source/'.retention.lock').exists(): raise ValueError('Source block is locked')
    if archive.exists(): raise FileExistsError(archive)
    members={}
    for p in sorted(source.rglob('*')):
        if '__pycache__' in p.parts or p.name.endswith('.pyc'): continue
        if p.is_symlink(): raise ValueError('Resolve/curate symlinks explicitly: '+str(p))
        if not p.is_file():continue
        relative=(PurePosixPath(prefix)/p.relative_to(source).as_posix()).as_posix()
        if any(x in ('.ssh','.config') for x in PurePosixPath(relative).parts): raise ValueError('Private configuration in delivery')
        members[relative]=dict(sha256=digest(p),bytes=p.stat().st_size)
    extras=extras or {}
    for name,path in extras.items():
        safe_relative(name)
        if name in members:raise ValueError('Duplicate extra member')
        members[name]=dict(sha256=digest(path),bytes=Path(path).stat().st_size)
    manifest=dict(schema_version=1,prefix=prefix,members=members)
    archive.parent.mkdir(parents=True,exist_ok=True)
    temporary=archive.with_suffix(archive.suffix+'.partial')
    if temporary.exists():raise FileExistsError(temporary)
    with tarfile.open(temporary,'w') as tar:
        for relative in members:
            path=Path(extras[relative]) if relative in extras else source/str(PurePosixPath(relative).relative_to(prefix))
            tar.add(path,arcname=relative,recursive=False)
        data=json.dumps(manifest,sort_keys=True).encode()
        info=tarfile.TarInfo('CONTENTS_SHA256.json');info.size=len(data);info.mode=0o644
        tar.addfile(info,io.BytesIO(data))
    verify_archive(temporary)
    temporary.replace(archive)
    result=dict(path=str(archive),sha256=digest(archive),bytes=archive.stat().st_size,members=len(members),prefix=prefix)
    save(archive.with_suffix(archive.suffix+'.json'),result)
    return result


def verify_archive(archive, destination=None):
    destination=None if destination is None else Path(destination).resolve()
    if destination is not None:
        if destination.exists():raise FileExistsError(destination)
        destination.mkdir(parents=True)
    with tarfile.open(archive,'r:*') as tar:
        items=tar.getmembers();names=[x.name for x in items]
        if len(names)!=len(set(names)):raise ValueError('Duplicate archive members')
        for item in items:
            safe_relative(item.name)
            if not item.isfile():raise ValueError('Only regular files are accepted')
        manifest=json.load(tar.extractfile('CONTENTS_SHA256.json'))
        if set(names)!=set(manifest['members'])|{'CONTENTS_SHA256.json'}:raise ValueError('Unlisted archive members')
        for name,meta in manifest['members'].items():
            h=hashlib.sha256();size=0
            out=None
            if destination is not None:
                target=destination/str(safe_relative(name))
                if not target.resolve().is_relative_to(destination):raise ValueError('Path escapes destination')
                target.parent.mkdir(parents=True,exist_ok=True);out=target.open('xb')
            try:
                with tar.extractfile(name) as stream:
                    for chunk in iter(lambda:stream.read(1048576),b''):
                        h.update(chunk);size+=len(chunk)
                        if out:out.write(chunk)
            finally:
                if out:out.close()
            if h.hexdigest()!=meta['sha256'] or size!=meta['bytes']:raise ValueError('Archive member differs: '+name)
    return dict(members_verified=len(manifest['members']),archive_sha256=digest(archive))


def source_entry(source, destination, groups, description):
    source=Path(source).resolve();safe_relative(destination)
    if not source.is_file():raise FileNotFoundError(source)
    return dict(source=str(source),path=destination,sha256=digest(source),bytes=source.stat().st_size,
                groups=list(groups),description=description)


def validate_catalog(root, groups=None):
    root=Path(root).resolve();catalog=read(root/'CATALOG.json');result=[]
    for item in catalog['assets']:
        if groups and not set(groups).intersection(item['groups']):continue
        path=root/str(safe_relative(item['path']))
        state='missing' if not path.is_file() else 'verified' if path.stat().st_size==item['bytes'] and digest(path)==item['sha256'] else 'corrupt'
        result.append(dict(path=item['path'],state=state))
    return dict(status='passed' if all(x['state']=='verified' for x in result) and result else 'incomplete',files=result)


class Drive:
    def __init__(self, binary, config, remote='whareformer_drive:'):
        self.binary=str(binary);self.config=Path(config).expanduser()
        if not self.config.is_file():raise RuntimeError('AUTHORIZATION_REQUIRED: run the private authorization helper first')
        if remote!='whareformer_drive:':raise ValueError('Use the dedicated root-scoped remote')
        self.remote=remote

    def call(self, *args):
        command=[self.binary,*args,'--config',str(self.config),'--log-level','ERROR','--retries','3','--stats','0']
        return subprocess.run(command,check=True,capture_output=True,text=True).stdout

    def upload(self, entry):
        safe_relative(entry['path']);source=Path(entry['source'])
        if digest(source)!=entry['sha256']:raise ValueError('Source changed before upload: '+entry['path'])
        target=self.remote+entry['path']
        self.call('copyto',str(source),target,'--immutable','--checksum')
        info=json.loads(self.call('lsjson',target,'--stat','--hash'))
        if info.get('Size')!=entry['bytes']:raise ValueError('Remote size differs')
        remote_hash=info.get('Hashes',{}).get('MD5') or info.get('Hashes',{}).get('md5')
        if not remote_hash or remote_hash.lower()!=digest(source,'md5'):raise ValueError('Actual remote checksum required')
        return dict(path=entry['path'],drive_id=info.get('ID'),bytes=entry['bytes'],sha256=entry['sha256'],md5=remote_hash,status='remote_verified')

    def download(self, entry, destination):
        destination=Path(destination)
        if destination.exists():raise FileExistsError(destination)
        destination.parent.mkdir(parents=True,exist_ok=True)
        temp=destination.with_suffix(destination.suffix+'.partial')
        if temp.exists():raise FileExistsError(temp)
        self.call('copyto',self.remote+entry['path'],str(temp),'--immutable','--checksum')
        if digest(temp)!=entry['sha256']:raise ValueError('Downloaded SHA-256 differs')
        temp.replace(destination)


def publish(plan_path, binary, config, groups=None, pilot=False):
    plan=read(plan_path);drive=Drive(binary,config);receipts=[]
    entries=[e for e in plan['assets'] if groups is None or set(groups).intersection(e['groups'])]
    for entry in entries:
        receipts.append(drive.upload(entry));print('REMOTE_VERIFIED',entry['path'],flush=True)
    result=dict(status='passed',files=receipts,created_unix=time.time(),sources_evicted=False)
    work=Path(plan_path).parent/'transfer_receipts';work.mkdir(exist_ok=True)
    if pilot:
        entry=next(e for e in entries if e.get('role')=='pilot_block')
        destination=work/('pilot_download_'+str(int(time.time()))+'.tar')
        drive.download(entry,destination)
        extraction=destination.with_suffix('')
        result['roundtrip']=verify_archive(destination,extraction)
        result['roundtrip']['extracted_to']=str(extraction)
    save(work/('pilot_verified.json' if pilot else 'publication_verified.json'),result)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='command',required=True)
    v=s.add_parser('verify');v.add_argument('root',type=Path);v.add_argument('--group',action='append')
    a=s.add_parser('verify-archive');a.add_argument('archive',type=Path);a.add_argument('--destination',type=Path)
    u=s.add_parser('publish');u.add_argument('--plan',type=Path,required=True);u.add_argument('--rclone',type=Path,required=True)
    u.add_argument('--config',type=Path,required=True);u.add_argument('--group',action='append');u.add_argument('--pilot',action='store_true')
    args=p.parse_args()
    if args.command=='verify':
        result=validate_catalog(args.root,args.group);print(json.dumps(result,indent=2));return 0 if result['status']=='passed' else 2
    if args.command=='verify-archive':print(json.dumps(verify_archive(args.archive,args.destination)));return 0
    print(json.dumps(publish(args.plan,args.rclone,args.config,args.group,args.pilot),indent=2));return 0


if __name__=='__main__':raise SystemExit(main())
