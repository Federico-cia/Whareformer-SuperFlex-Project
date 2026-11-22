"""Bind current-view DA-aligned queries to exact FPS inputs for SuperFlex."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scene_geometry import farthest_points


def write_input(p, path, key, frame):
    ids = farthest_points(p, 4096)
    center = p[ids].mean(0)
    scale = float(2 * np.max(np.abs(p[ids] - center)))
    with path.open('xb') as f:
        np.savez_compressed(f, object_points=p, selected_points=p[ids], sample_indices=ids,
            normalized_points=(p[ids] - center) / scale, translation=center, scale=scale,
            shape_version=0, observed_only=True, sampling='deterministic_fps_4096',
            provenance_json=json.dumps(dict(observation_key=key, frame_index=frame,
            role='current-query-never-candidate-memory', source='da_aligned')))


def prepare(export, audit):
    root, audit = Path(export), Path(audit)
    examples = json.loads((root / 'examples.json').read_text())
    requests = []
    with np.load(audit / 'world_clouds_aligned.npz', allow_pickle=False) as clouds:
        for row in examples:
            if row['query'] is None:
                continue
            key = row['observation_key']
            tag = hashlib.sha256(key.encode()).hexdigest()[:20]
            p = clouds[key.replace('/', '__')].astype(float)
            path = root / 'shapes' / f'query_{tag}.npz'
            write_input(p, path, key, row['frame_index'])
            requests.append(dict(observation_key=key, frame_index=row['frame_index'], shape_version=0,
                role='query', superflex_input=dict(path='shapes/' + path.name,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest())))
    with (root / 'query_requests.json').open('x') as f:
        json.dump(requests, f, indent=2)
    print(json.dumps(dict(query_requests=len(requests))))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--export', required=True)
    p.add_argument('--audit', required=True)
    a = p.parse_args()
    prepare(a.export, a.audit)
