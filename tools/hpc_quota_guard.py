"""Operational storage preflight; not a scientific acceptance threshold.

Read the site's personal quota before each batch. Exit 75 on low/unreadable
quota so the chain stops explicitly instead of filling the filesystem mid-write.
"""
import argparse
import json
import os
import re
import subprocess
import sys


def parse_quota(text):
    space = re.search(r'Space:\s*([\d.]+)([KMGT]i?B)\s+used\s*/\s*([\d.]+)([KMGT]i?B)\s+limit', text)
    files = re.search(r'Files:\s*([\d.]+)([kKM]?)\s+used\s*/\s*([\d.]+)([kKM]?)\s+limit', text)
    if not space or not files:
        raise ValueError('Unrecognized quota report; storage not certified')
    def size(n, unit):
        base = 1024 if 'i' in unit else 1000
        return float(n) * base**('KMGT'.index(unit[0]) + 1)
    def count(n, unit):
        return float(n) * {'':1, 'k':1000, 'K':1000, 'M':1000000}[unit]
    used, limit = size(space[1],space[2]), size(space[3],space[4])
    used_files, limit_files = count(files[1],files[2]), count(files[3],files[4])
    return dict(used_bytes=used, limit_bytes=limit, free_bytes=limit-used,
                used_files=used_files, limit_files=limit_files, free_files=limit_files-used_files)


def parse_native_quota(text, uid):
    """Same pool_home mirror factor (0.5) as the site's myquota helper.

    The helper exists only on login nodes; native BeeGFS can be queried on
    compute nodes. This converts physical mirrored accounting to logical quota.
    """
    for line in text.splitlines():
        values = line.split()
        if len(values) >= 6 and values[1] == str(uid) and values[2:4] == ['user', 'pool_home']:
            used, limit = values[4].split('/')
            files, file_limit = values[5].split('/')
            result = parse_quota(f'Space: {used} used / {limit} limit\nFiles: {files} used / {file_limit} limit')
            return {k: v * 0.5 for k, v in result.items()}
    raise ValueError('No own-user pool_home quota in native output')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--minimum-free-gib', type=float, required=True)
    parser.add_argument('--minimum-free-files', type=int, required=True)
    args = parser.parse_args()
    if args.minimum_free_gib <= 0 or args.minimum_free_files <= 0:
        parser.error('Positive operational reserve required')
    try:
        try:
            result = subprocess.run(['/userScripts/myquota'], stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True, timeout=20, check=True)
            quota = parse_quota(result.stdout)
        except (FileNotFoundError, subprocess.CalledProcessError):
            result = subprocess.run(['/usr/sbin/beegfs', 'quota', 'list-usage'], stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True, timeout=20, check=True)
            quota = parse_native_quota(result.stdout, os.getuid())
    except Exception as error:
        print('QUOTA_PREFLIGHT_UNAVAILABLE', type(error).__name__, str(error), flush=True)
        return 75
    enough = (quota['free_bytes'] >= args.minimum_free_gib * 1024**3
              and quota['free_files'] >= args.minimum_free_files)
    print('QUOTA_PREFLIGHT', json.dumps(dict(quota, sufficient=enough,
          minimum_free_gib=args.minimum_free_gib, minimum_free_files=args.minimum_free_files)), flush=True)
    if not enough:
        print('STORAGE_RESERVE_STOP: preserve completed outputs; free storage before restarting', flush=True)
        return 75
    return 0


if __name__ == '__main__':
    sys.exit(main())
