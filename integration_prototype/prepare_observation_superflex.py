"""Ingressi FPS-4096 per SuperFlex di ogni osservazione, dalle nuvole DA allineate a piena risoluzione.

Stesso contratto della memoria e delle query del punto 3 (`prepare_query_reconstructions.write_input`):
così forma dell'osservazione e forma della memoria nascono dallo stesso dominio (DA allineata).
Produce una cartella compatibile con `scene_superflex_worker.py --export` (versions.json vuoto,
query_requests.json, shapes/). Cartella nuova, mai sovrascritta.
Uso: python prepare_observation_superflex.py --aligned CARTELLA --out NUOVA [--max-frame N]
"""
import argparse, hashlib, json
from multiprocessing import Pool
from pathlib import Path
import numpy as np
from prepare_query_reconstructions import write_input


def _one(job):
    aligned, out, key, frame = job
    with np.load(Path(aligned) / 'world_clouds_aligned_fullres.npz', allow_pickle=False) as clouds:
        p = clouds[key.replace('/', '__')].astype(float)
    tag = hashlib.sha256(key.encode()).hexdigest()[:20]
    path = Path(out) / 'shapes' / f'query_{tag}.npz'
    write_input(p, path, key, frame)
    return dict(observation_key=key, frame_index=frame, shape_version=0, role='query',
                superflex_input=dict(path='shapes/' + path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest()))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--aligned', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--max-frame', type=int)
    ap.add_argument('--workers', type=int, default=1)
    a = ap.parse_args()
    (a.out / 'shapes').mkdir(parents=True, exist_ok=False)
    rows = [r for r in map(json.loads, (a.aligned / 'per_observation.jsonl').read_text().splitlines())
            if r.get('status') == 'ok' and (a.max_frame is None or r['frame'] <= a.max_frame)]
    jobs = [(str(a.aligned), str(a.out), r['key'], r['frame']) for r in rows]
    with Pool(a.workers) as pool:
        requests = pool.map(_one, jobs, chunksize=8)   # ordine conservato
    (a.out / 'versions.json').write_text('[]')
    (a.out / 'query_requests.json').write_text(json.dumps(requests, indent=2))
    print(json.dumps(dict(query_requests=len(requests))))


if __name__ == '__main__':
    main()
