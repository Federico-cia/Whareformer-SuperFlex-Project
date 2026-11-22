"""Small self-contained FPS smoke package; no remote action from this script."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import numpy as np
from prepare_query_reconstructions import write_input


def prepare(export, output, audit=None):
    root, out = Path(export), Path(output)
    versions, queries = [], []
    # GPU contract smoke can start while the full replay is still running.
    for path in sorted((root / 'shapes').glob('memory_*.npz'))[:2]:
        with np.load(path, allow_pickle=False) as z:
            snapshot = json.loads(str(z['provenance_json']))
            versions.append(dict(track_id=snapshot['track_id'], shape_version=int(z['shape_version']),
                superflex_input=dict(path='shapes/' + path.name,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest())))
    if len(versions) < 2:
        raise ValueError('Two accumulated shapes required')
    out.mkdir(parents=True, exist_ok=False)
    (out / 'shapes').mkdir(); (out / 'code').mkdir()
    for row in versions:
        spec = row['superflex_input']
        source = root / spec['path']
        if hashlib.sha256(source.read_bytes()).hexdigest() != spec['sha256']:
            raise ValueError('Source shape checksum mismatch')
        shutil.copyfile(source, out / spec['path'])
    if (root / 'query_requests.json').exists():
        queries = json.loads((root / 'query_requests.json').read_text())[:2]
        for row in queries:
            shutil.copyfile(root / row['superflex_input']['path'], out / row['superflex_input']['path'])
    else:
        audit = Path(audit)
        rows = [json.loads(l) for l in (audit / 'per_observation.jsonl').read_text().splitlines()]
        rows = [r for r in rows if r.get('align_valid') and r.get('mask_source') != 'catalogue_only'][:2]
        with np.load(audit / 'world_clouds_aligned.npz', allow_pickle=False) as clouds:
            for row in rows:
                key = row['key']; tag = hashlib.sha256(key.encode()).hexdigest()[:20]
                path = out / 'shapes' / f'query_{tag}.npz'
                write_input(clouds[key.replace('/', '__')].astype(float), path, key, row['frame'])
                queries.append(dict(observation_key=key, shape_version=0, role='query',
                    superflex_input=dict(path='shapes/' + path.name,
                    sha256=hashlib.sha256(path.read_bytes()).hexdigest())))
    if len(queries) != 2:
        raise ValueError('Two query inputs required')
    (out / 'versions.json').write_text(json.dumps(versions, indent=2))
    (out / 'query_requests.json').write_text(json.dumps(queries, indent=2))
    code = Path(__file__).parent
    for name in ('scene_geometry.py', 'scene_superflex_worker.py'):
        shutil.copyfile(code / name, out / 'code' / name)
    shutil.copyfile(code.parent / 'strumenti_hpc' / 'hpc_quota_guard.py', out / 'code' / 'hpc_quota_guard.py')
    hashes = {str(p.relative_to(out)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in out.rglob('*') if p.is_file()}
    (out / 'files.sha256').write_text(''.join(f'{h}  {name}\n' for name, h in sorted(hashes.items())))
    archive = out.with_suffix('.tgz')
    if archive.exists():
        raise FileExistsError(archive)
    with tarfile.open(archive, 'w:gz') as tar:
        for p in out.iterdir():
            tar.add(p, arcname=p.name)
    report = dict(archive=str(archive.resolve()), bytes=archive.stat().st_size,
                  sha256=hashlib.sha256(archive.read_bytes()).hexdigest(), memory_requests=2, query_requests=2)
    (out / 'package_receipt.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--export', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--audit')
    a = p.parse_args()
    prepare(a.export, a.out, a.audit)
