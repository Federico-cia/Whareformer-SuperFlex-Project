"""Raccoglie i descrittori SuperFlex delle osservazioni (output di scene_superflex_worker) in un NPZ
per run_memory_grid.py --query-features (chiavi <oss>__points, __d2, __spectrum). Le ricostruzioni
fallite restano assenti (nessun sostituto) e sono elencate nel riepilogo."""
import argparse, hashlib, json
from pathlib import Path
import numpy as np


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--export', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    if a.out.exists():
        raise FileExistsError(a.out)
    arrays, failed, missing = {}, [], []
    for q in json.loads((a.export / 'query_requests.json').read_text()):
        folder = a.export / 'reconstructions' / Path(q['superflex_input']['path']).stem
        if not (folder / 'result.json').exists():
            missing.append(q['observation_key']); continue
        result = json.loads((folder / 'result.json').read_text())
        if result['status'] != 'ready' or result['input_sha256'] != q['superflex_input']['sha256']:
            failed.append(dict(key=q['observation_key'], error=result.get('error', 'input mismatch'))); continue
        path = folder / result['features']['path']
        if hashlib.sha256(path.read_bytes()).hexdigest() != result['features']['sha256']:
            failed.append(dict(key=q['observation_key'], error='feature hash mismatch')); continue
        tag = q['observation_key'].replace('/', '__')
        with np.load(path, allow_pickle=False) as z:
            for k in ('points', 'd2', 'spectrum'):
                arrays[f'{tag}__{k}'] = z[k].copy()
    with open(a.out, 'xb') as f:
        np.savez_compressed(f, **arrays)
    summary = dict(ready=len(arrays) // 3, failed=len(failed), missing=len(missing), failures=failed[:50])
    a.out.with_suffix('.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps({k: v for k, v in summary.items() if k != 'failures'}))


if __name__ == '__main__':
    main()
