"""Independent artifact checks, including target recomputation on full surfaces."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree


def verify(root):
    root = Path(root)
    summary = json.loads((root / 'summary.json').read_text())
    for filename, expected in {**summary['inputs'], **summary['outputs']}.items():
        path = Path(filename) if Path(filename).is_absolute() else root / filename
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, filename
    samples = [json.loads(l) for l in (root / 'samples.jsonl').read_text().splitlines()]
    assert len(samples) == summary['samples']
    groups = {s: {r['group'] for r in samples if r['split'] == s} for s in ('train', 'validation')}
    assert groups['train'] and groups['validation'] and not groups['train'] & groups['validation']
    source_path = next(p for p in summary['inputs'] if p.endswith('.npz'))
    max_error = 0.
    correct = 0
    with np.load(root / 'examples.npz', allow_pickle=False) as data, np.load(source_path, allow_pickle=False) as originals:
        for row in samples:
            prefix = row['id'] + '__'
            get = lambda name: data[prefix + name]
            for name in ('source', 'target', 'aligned_source', 'features', 'error', 'estimate', 'ground_truth'):
                assert np.isfinite(get(name)).all(), (row['id'], name)
            assert get('source').shape == get('target').shape == (summary['points_per_view'], 3)
            estimate, gt = get('estimate'), get('ground_truth')
            for matrix in (estimate, gt):
                np.testing.assert_allclose(matrix[:3, :3].T @ matrix[:3, :3], np.eye(3), atol=1e-12)
                assert np.isclose(np.linalg.det(matrix[:3, :3]), 1)
            residual = estimate @ np.linalg.inv(gt)
            p = originals[row['observation_key'].replace('/', '__')].astype(float)
            p = (p - p.mean(0)) / np.sqrt(np.mean(np.sum((p - p.mean(0)) ** 2, axis=1)))
            q = p @ residual[:3, :3].T + residual[:3, 3]
            independent = (cKDTree(p).query(q)[0].mean() + cKDTree(q).query(p)[0].mean()) / 2
            error = float(get('error'))
            max_error = max(max_error, abs(independent - error))
            assert abs(independent - error) < 1e-10
            assert error == row['error']
            if row['angle_deg'] == row['translation_rms'] == 0:
                assert error == 0
                correct += 1
            assert not row['real_multiview_ground_truth']
    result = dict(verified_samples=len(samples), exact_zero_targets=correct,
                  disjoint_identity_groups=True, all_hashes_match=True,
                  maximum_target_recomputation_difference=max_error,
                  real_static_pairs_certified=0)
    (root / 'verification.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('root')
    verify(parser.parse_args().root)
