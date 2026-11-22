"""Local development data from single observed surfaces and known rigid errors.

Not real multiview ground truth. No old registration gates are used as labels.
Profiles and identity holdout are diagnostic fixtures, not a final protocol.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.spatial.transform import Rotation
from registration_verifier import pair_features
from scene_geometry import surface_error, transform


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def partial_indices(points, direction, fraction):
    projection = points @ direction
    count = max(3, int(np.ceil(len(points) * fraction)))
    return np.argsort(projection, kind='stable')[-count:]


def make_example(points, rng, *, angle_deg, translation_rms, noise_rms, count=256):
    """Known GT from one surface. Target is independent of cropping/noise."""
    center = points.mean(0)
    radius = np.sqrt(np.mean(np.sum((points - center) ** 2, axis=1)))
    if len(points) < 16 or not np.isfinite(points).all() or radius <= 1e-12:
        raise ValueError('Insufficient or degenerate surface')
    p = (points - center) / radius
    axis = rng.normal(size=3)
    axis /= np.linalg.norm(axis)
    residual = np.eye(4)
    residual[:3, :3] = Rotation.from_rotvec(axis * np.deg2rad(angle_deg)).as_matrix()
    shift = rng.normal(size=3)
    residual[:3, 3] = shift / np.linalg.norm(shift) * translation_rms
    # Moving-object fixture: input is displaced; true registration undoes it.
    motion = np.eye(4)
    motion[:3, :3] = Rotation.random(random_state=rng).as_matrix()
    motion[:3, 3] = rng.uniform(-2, 2, 3)
    ground_truth = np.linalg.inv(motion)
    estimate = residual @ ground_truth
    fractions = rng.uniform(.45, .9, 2)
    directions = rng.normal(size=(2, 3))
    selections = [partial_indices(p, d, f) for d, f in zip(directions, fractions)]
    indices = [rng.choice(i, count, replace=len(i) < count) for i in selections]
    source_clean = transform(p[indices[0]], motion)
    target_clean = p[indices[1]]
    source = source_clean + rng.normal(0, noise_rms, source_clean.shape)
    target = target_clean + rng.normal(0, noise_rms, target_clean.shape)
    aligned = transform(source, estimate)
    error = surface_error(p, residual, np.eye(4))
    overlap = len(np.intersect1d(*selections)) / min(map(len, selections))
    return dict(source=source, target=target, aligned_source=aligned,
                estimate=estimate, ground_truth=ground_truth,
                residual=residual, features=pair_features(aligned, target),
                error=error, source_indices=indices[0], target_indices=indices[1],
                center=center, radius=radius, crop_fractions=fractions,
                index_overlap=overlap)


def build(a):
    out = Path(a.out)
    if out.exists():
        raise FileExistsError('Use a fresh output directory')
    source_dir = Path(a.audit)
    observations = source_dir / 'per_observation.jsonl'
    clouds_path = source_dir / 'world_clouds_aligned.npz'
    rows = [json.loads(line) for line in observations.read_text().splitlines()]
    eligible = [r for r in rows if r.get('align_valid') and r.get('identity') is not None
                and r.get('mask_source') != 'catalogue_only']
    identities = sorted({r['identity'] for r in eligible},
                        key=lambda x: hashlib.sha256(f'{a.seed}:{x}'.encode()).hexdigest())
    if len(identities) < 2:
        raise ValueError('Need independent identities')
    validation = set(identities[:max(1, len(identities) // 4)])
    out.mkdir(parents=True)
    profiles = [(0., 0.), (5., .03), (20., .15), (60., .5)]
    samples, arrays, exclusions = [], {}, []
    with np.load(clouds_path, allow_pickle=False) as clouds:
        expected = {r['key'].replace('/', '__') for r in rows if r.get('align_valid')}
        if expected != set(clouds.files):
            raise ValueError('Audit/cloud key mismatch')
        for r in rows:
            if r not in eligible:
                exclusions.append(dict(key=r['key'], reason='invalid_alignment_or_identity_or_catalogue_only',
                                       mask_source=r.get('mask_source')))
        for row in eligible:
            key = row['key']
            p = np.asarray(clouds[key.replace('/', '__')], dtype=float)
            if len(p) < 16 or not np.isfinite(p).all() or np.max(np.std(p, axis=0)) <= 1e-12:
                exclusions.append(dict(key=key, reason='insufficient_or_degenerate_surface'))
                continue
            for noise in (0., .01):
                for angle, shift in profiles:
                    sample_id = f's{len(samples):06d}'
                    seed_text = f'{a.seed}:{key}:{noise}:{angle}:{shift}'
                    local_seed = int.from_bytes(hashlib.sha256(seed_text.encode()).digest()[:8], 'little')
                    example = make_example(p, np.random.default_rng(local_seed), angle_deg=angle,
                                           translation_rms=shift, noise_rms=noise, count=a.points)
                    for name, value in example.items():
                        arrays[f'{sample_id}__{name}'] = value
                    samples.append(dict(id=sample_id, observation_key=key,
                        video='P01_01', frame=row['frame'], identity=row['identity'],
                        oracle_track_id=row['track'], group=row['identity'],
                        split='validation' if row['identity'] in validation else 'train',
                        mask_source=row['mask_source'], local_seed=local_seed,
                        angle_deg=angle, translation_rms=shift, noise_rms=noise,
                        error=example['error'], target_kind='known_transform_on_same_observed_surface',
                        real_multiview_ground_truth=False))
    np.savez_compressed(out / 'examples.npz', **arrays)
    (out / 'samples.jsonl').write_text(''.join(json.dumps(s, allow_nan=False) + '\n' for s in samples))
    (out / 'exclusions.json').write_text(json.dumps(exclusions, indent=2))
    groups = {split: sorted({s['group'] for s in samples if s['split'] == split})
              for split in ('train', 'validation')}
    assert not set(groups['train']) & set(groups['validation'])
    summary = dict(schema='point3-known-transform-development-v1', seed=a.seed,
        observations_input=len(rows), observations_used=len({s['observation_key'] for s in samples}),
        samples=len(samples), counts={s: sum(r['split'] == s for r in samples) for s in groups},
        groups=groups, exclusions=len(exclusions), points_per_view=a.points,
        profiles=dict(angle_translation=profiles, noise_rms=[0., .01], crop_fraction=[.45, .9]),
        split_scope='identity-held-out within P01_01 development only; not independent video test',
        target='symmetric_surface_error_over_reference_rms',
        limitations=['single partial surface, not complete object',
                    'synthetic crops, noise and motion; realism not validated',
                    'no certified real static pairs or real post-movement registration',
                    'no scale errors or identity negatives; not fusion-utility ground truth',
                    'simultaneous frame/scene dependencies may remain across identities',
                    'not a training export for point 2; no memory replay yet'],
        inputs={str(p.resolve()): sha(p) for p in (observations, clouds_path)},
        code_sha256=sha(__file__))
    summary['outputs'] = {p.name: sha(p) for p in out.iterdir() if p.is_file()}
    (out / 'summary.json').write_text(json.dumps(summary, indent=2, allow_nan=False))
    print(json.dumps({k: summary[k] for k in ('observations_used', 'samples', 'counts', 'exclusions')}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audit', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--seed', type=int, default=20261122)
    parser.add_argument('--points', type=int, default=256)
    args = parser.parse_args()
    if args.points < 16:
        parser.error('At least 16 sampled points required')
    build(args)
