"""Safely import the remote geometry archive into the portable P01_01 delivery."""
import argparse
import hashlib
import json
from pathlib import Path
import tarfile
from p01_correction_data import read,save,sha,verify_geometry


def extract(archive,destination):
    destination=Path(destination).resolve()
    if destination.exists(): raise FileExistsError('Preserve existing geometry dataset')
    destination.mkdir(parents=True)
    seen=set()
    with tarfile.open(archive,'r:gz') as tar:
        for member in tar:
            path=(destination/member.name).resolve()
            if not path.is_relative_to(destination) or not member.isfile() or member.name in seen:
                raise ValueError('Unsafe or duplicate archive member')
            seen.add(member.name);path.parent.mkdir(parents=True,exist_ok=True)
            with tar.extractfile(member) as src,path.open('xb') as dst:
                for block in iter(lambda:src.read(1048576),b''): dst.write(block)
    receipt=read(destination/'geometry_receipt.json')
    if receipt['status']!='complete' or receipt['observations']!=8126: raise ValueError('Incomplete archive')
    for line in (destination/'SHA256SUMS').read_text().splitlines():
        expected,name=line.split('  ',1)
        path=(destination/name).resolve()
        if not path.is_relative_to(destination) or sha(path)!=expected: raise ValueError('Checksum '+name)
    save(destination/'verification.json',verify_geometry(destination))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('archive',type=Path)
    p.add_argument('--root',type=Path,default=Path('.'));a=p.parse_args()
    extract(a.archive,a.root/'data/geometry')
