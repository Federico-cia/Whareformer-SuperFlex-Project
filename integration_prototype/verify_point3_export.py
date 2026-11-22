"""Independent temporal/provenance/label checks for the point-2 handoff."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import numpy as np


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify(root):
    root = Path(root).resolve()
    summary = json.loads((root / 'summary.json').read_text())
    source = next(Path(p) for p in summary['source_files'] if p.endswith('samples.json'))
    original = {r['observation_key']: r for r in json.loads(source.read_text())}
    for p, h in summary['source_files'].items():
        assert sha(p) == h, p
    numerical = next(Path(p) for p in summary['source_files'] if p.endswith('training_inputs.npz'))
    assert sha(root / 'training_inputs.npz') == sha(numerical)
    examples = json.loads((root / 'examples.json').read_text())
    versions = json.loads((root / 'versions.json').read_text())
    index = {(v['track_id'], v['shape_version']): v for v in versions}
    assert len(index) == len(versions)
    assert len(examples) == len(original) == summary['samples']
    feature_count, refs, missing = 0, 0, 0
    seen = set()

    def bound(spec):
        path = (root / spec['path']).resolve()
        assert path.is_relative_to(root)
        assert sha(path) == spec['sha256'], str(path)
        return path

    def check_feature(spec):
        nonlocal feature_count
        path = bound(spec)
        if path in seen:
            return
        seen.add(path)
        with np.load(path, allow_pickle=False) as z:
            assert z['points'].shape == (1024, 3) and z['spectrum'].shape == (3,)
            assert all(np.isfinite(z[k]).all() for k in ('points', 'd2', 'spectrum'))
            assert not bool(z['completed_by_superflex'])
        feature_count += 1

    for version in versions:
        assert version['observation_keys']
        assert all(original[k]['frame_index'] <= version['last_update_frame'] for k in version['observation_keys'])
        assert all(str(original[k]['oracle_track_id']) == version['track_id'] for k in version['observation_keys'])
        path = bound(version['superflex_input'])
        with np.load(path, allow_pickle=False) as z:
            assert int(z['shape_version']) == version['shape_version']
            assert bool(z['observed_only']) and str(z['sampling']) == 'deterministic_fps_4096'
            p, ids = z['object_points'], z['sample_indices']
            assert ids.shape == (4096,) and ids.min() >= 0 and ids.max() < len(p)
            np.testing.assert_array_equal(z['selected_points'], p[ids])
            np.testing.assert_array_equal(z['normalized_points'], (p[ids] - z['translation']) / z['scale'])
            snapshot = json.loads(str(z['provenance_json']))
            assert snapshot['shape_version'] == version['shape_version']
            assert snapshot['track_id'] == version['track_id']
            assert snapshot['policy'] == summary.get('policy', 'register-every-view-v1')
            if snapshot['policy'] == 'multi-hypothesis-scene-memory-v1':
                assert snapshot['fused_observation_keys'] == version['observation_keys']
                for e in json.loads(str(z['events_json'])):
                    if e['shape_changed']:
                        assert e['status'] in ('initialized_confirmed_shape', 'fused_confirmed_state')
            events = json.loads(str(z['events_json']))
            assert max(e['frame'] for e in events) <= version['last_update_frame']
        check_feature(version['points'])
    for row in examples:
        orig = original[row['observation_key']]
        for field in ('target_class', 'target_track_id', 'candidate_track_ids', 'numerical_input_key', 'numerical_label_key'):
            assert row[field] == orig[field], (row['observation_key'], field)
        if row['query']:
            check_feature(row['query'])
        for candidate in row['candidates']:
            memory = candidate['memory']
            if memory is None:
                missing += 1
                continue
            assert memory['track_id'] == str(candidate['track_id'])
            assert memory['last_update_frame'] < row['frame_index']
            assert memory == index[(memory['track_id'], memory['shape_version'])]
            assert all(original[k]['frame_index'] < row['frame_index'] for k in memory['observation_keys'])
            refs += 1
    results = dict(status='passed', examples=len(examples), shape_versions=len(versions),
        feature_files_verified=feature_count, strictly_past_memory_references=refs,
        missing_candidate_memories=missing, original_targets_preserved=True,
        numerical_inputs_byte_identical=True, current_or_future_memory_leaks=0,
        neural_reconstruction_certified=False)
    if summary.get('policy') == 'multi-hypothesis-scene-memory-v1':
        for tid, item in summary['hypothesis_artifacts'].items():
            path = bound(item)
            with np.load(path, allow_pickle=False) as z:
                snapshot = json.loads(str(z['snapshot_json']))
                assert snapshot == item['snapshot'] and snapshot['track_id'] == tid
                for state in snapshot['states'].values():
                    assert set(state['merged_keys']) <= set(snapshot['fused_observation_keys'])
                    assert all(str(original[k]['oracle_track_id']) == tid for k in state['keys'])
                    assert all(original[k]['frame_index'] <= snapshot['last_frame'] for k in state['keys'])
        results['hypothesis_tracks_verified'] = len(summary['hypothesis_artifacts'])
    (root / 'verification.json').write_text(json.dumps(results, indent=2))
    print(json.dumps(results))
    return results


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('export')
    verify(p.parse_args().export)
