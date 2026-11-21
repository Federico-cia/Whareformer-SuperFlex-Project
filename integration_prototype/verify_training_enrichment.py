"""Independent structural audit of an enriched original-oracle dataset."""
import argparse
from collections import Counter
import json
from pathlib import Path

from training_enrichment import read, save, sha, validate_sample_rows


def verify(root):
    import numpy as np
    root = Path(root)
    receipt = read(root / 'receipt.json')
    for name, expected in receipt['output_hashes'].items():
        if sha(root / name) != expected:
            raise ValueError('Dataset artifact changed: ' + name)
    samples = read(root / 'samples.json')
    catalog = read(root / 'geometry_catalogue.json')
    checks = validate_sample_rows(samples, catalog['observations'])
    ledger = [json.loads(line) for line in (root / 'oracle_observation_ledger.jsonl').read_text().splitlines()]
    prior, frame_seen, expected_samples, geometry_by_name = {}, {}, {}, {}
    for row in ledger:
        frame, name = row['frame_index'], row['benchmark_identity']
        if name not in prior:
            prior[name] = row['oracle_track_id']
            frame_seen[name] = frame
        if prior[name] != row['oracle_track_id']:
            raise ValueError('Oracle name/track mapping changed')
        if row['geometric_observation']:
            expected_samples[row['observation_key']] = row
            geometry_by_name.setdefault(name, []).append(row)
    with np.load(root / 'training_inputs.npz', allow_pickle=False) as data:
        for sample in samples:
            x, y = data[sample['numerical_input_key']], data[sample['numerical_label_key']]
            if (x.shape != (len(sample['candidate_track_ids']) + 1, 259)
                    or y.shape != (len(x),) or not np.isfinite(x).all()
                    or int(y.sum()) != 1 or int(y.argmax()) != sample['target_class']):
                raise ValueError('Invalid numerical training sample')
            reference = expected_samples[sample['observation_key']]
            if reference['oracle_track_id'] != sample['oracle_track_id']:
                raise ValueError('Sample/ledger mismatch')
            expected_new = frame_seen[sample['benchmark_identity']] == sample['frame_index']
            if expected_new != (sample['target_class'] == 0):
                raise ValueError('New-track target uses an incorrect temporal boundary')
            for candidate_name, track_id, history in zip(sample['candidate_names'],
                    sample['candidate_track_ids'], sample['candidate_geometry_keys']):
                if prior[candidate_name] != track_id:
                    raise ValueError('Candidate label mapping changed')
                expected = [other['observation_key'] for other in geometry_by_name.get(candidate_name, [])
                    if other['frame_index'] < sample['frame_index']]
                if history != expected:
                    raise ValueError('Geometry history omitted or added a view')
    if len(samples) != len(expected_samples):
        raise ValueError('Missing selected sample')
    return dict(status='passed', numerical_samples=len(samples),
        full_ledger_observations=len(ledger), benchmark_tracks=len(prior),
        candidate_history_complete=True, original_output_hashes_verified=True,
        labels=dict(Counter('new' if s['target_class'] == 0 else 'existing' for s in samples)), **checks)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.root)
    save(args.root / 'independent_verification.json', result)
    print(json.dumps(result, indent=2))
