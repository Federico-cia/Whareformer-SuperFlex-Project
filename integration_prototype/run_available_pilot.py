"""Three-frame annotated diagnostic replay on existing geometry, NOT tracking."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'shared_exports/publish_candidate/SuperFlex/src'))

from shape_adapter import ShapeLogitAdapter, FusionConfig
from shape_tools.memory import MemoryConfig, observation_features
from test_shape_adapter import original_assignment, softmax


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Preserve previous outputs; choose a new output directory')
    args.output.mkdir(parents=True)
    start = time.perf_counter()
    frames = [8115, 19311, 20618]
    identities = ['P03_04_orange_knife_A', 'P03_04_blue_board_A']
    reviews = {r['observation_key']: r for r in csv.DictReader(
        (ROOT / 'outputs/shape_identity_v1/identity_review.csv').open(encoding='utf-8-sig'))
        if r['identity_status'] == 'visually_verified' and r['physical_identity'] in identities}
    rows = [r for r in json.loads((ROOT / 'outputs/geometric_closure_v1/observations.json').read_text(encoding='utf-8'))
            if r['video'] == 'P03_04' and r['frame_index'] in frames and r['observation_key'] in reviews]
    rows.sort(key=lambda r: (r['frame_index'], r['annotation_index']))
    assert len(rows) == 5 and {r['frame_index'] for r in rows} == set(frames)
    source = ROOT / 'Whareformer-repo/src/tracking/tracker/matcher/matcher_types.py'
    results = []
    for representation in ['da_raw_points', 'da_raw_superflex', 'moge_points', 'moge_superflex']:
        zero = ShapeLogitAdapter('P03_04', MemoryConfig(representation, capacity=2))
        active = ShapeLogitAdapter('P03_04', MemoryConfig(representation, capacity=2), FusionConfig(1.0, 0.2))
        track_ids = []
        assign = original_assignment()
        for frame in frames:
            batch = [r for r in rows if r['frame_index'] == frame]
            keys = [r['observation_key'] for r in batch]
            feats = {r['observation_key']: observation_features(r, ROOT / 'outputs/compare200_749968', representation) for r in batch}
            # Arbitrary deterministic fixture; not Whareformer neural output.
            logits = np.zeros((len(keys), len(track_ids) + 1), dtype=np.float32)
            a = zero.score(frame, keys, feats, track_ids, logits)
            b = active.score(frame, keys, feats, track_ids, logits)
            assert np.array_equal(a['logits'], logits)
            assert assign(softmax(a['logits'])) == assign(softmax(logits))
            assert zero.snapshot() == active.snapshot()
            # Explicit oracle replay only for testing the adapter; no tracker claim.
            associations = {k: reviews[k]['physical_identity'] for k in keys}
            zero.commit(associations); active.commit(associations)
            for tid in associations.values():
                if tid not in track_ids:
                    track_ids.append(tid)
            results.append({'representation': representation, 'frame_index': frame,
                            'observations': keys, 'previous_track_ids': a['track_ids'],
                            'valid_distances': int(a['valid'].sum()),
                            'distances': [[float(x) if np.isfinite(x) else None for x in row] for row in a['distances']],
                            'zero_exact': True, 'fixture_assignment_equal': True,
                            'memory_after_annotated_commit': zero.snapshot()})
    summary = {'video': 'P03_04', 'frames': frames, 'observations': len(rows),
               'representations': 4, 'geometry_artifacts_verified_and_read': len(rows) * 4,
               'frame_transactions': len(results), 'elapsed_seconds': time.perf_counter() - start,
               'result': 'all zero-weight fixture comparisons and causal memory transactions passed',
               'baseline_logits': 'all-zero fixtures; no neural inference',
               'associations': 'existing visual labels injected as explicit diagnostic oracle',
               'fusion_parameters': 'weight=1, neutral_distance=0.2 are arbitrary test values, not calibrated choices',
               'limits': ['No learned Whareformer output, IDF1 or mPCL measured.',
                          'No registration, fusion, accumulated-cloud SuperFlex inference or real zero-weight tracker equivalence verified.',
                          'Visual identities retain original uncertainty; replay is not tracking validation.'],
               'assignment_source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
               'adapter_sha256': hashlib.sha256((Path(__file__).parent / 'shape_adapter.py').read_bytes()).hexdigest()}
    (args.output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    (args.output / 'transactions.json').write_text(json.dumps(results, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
