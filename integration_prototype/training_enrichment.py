"""Build labelled sparse geometry examples through the unmodified oracle.

No neural inference, invented physical identities, or geometric memory selection.
All available earlier geometry views are retained as provenance, not fused.
Numerical inputs are compared with the authors' manifest builder/loader contract.
"""
import argparse
from collections import Counter
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import types


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def save(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def benchmark_target(name, candidate_names):
    if len(candidate_names) != len(set(candidate_names)):
        raise ValueError('Ambiguous benchmark candidate names')
    return candidate_names.index(name) + 1 if name in candidate_names else 0


class GeometryHistory:
    """Unbounded audit index of earlier observed views, not a selected memory."""
    def __init__(self):
        self.rows = {}
        self.last_frame = -1

    def before(self, track_ids, frame):
        result = [list(self.rows.get(track_id, [])) for track_id in track_ids]
        if any(item['frame_index'] >= frame for row in result for item in row):
            raise ValueError('Current/future geometry leaked into a query')
        return [[item['observation_key'] for item in row] for row in result]

    def commit(self, frame, observations):
        if frame <= self.last_frame:
            raise ValueError('Geometry frames must commit exactly once in order')
        for track_id, key in observations:
            self.rows.setdefault(track_id, []).append(dict(
                observation_key=key, frame_index=frame))
        self.last_frame = frame


class MemoryTransaction:
    def __init__(self):
        self.values = {}

    def put(self, key, value):
        if key in self.values and self.values[key] != value:
            raise ValueError('Feature hash collision')
        self.values[key] = value


def inventory(project, scan_root, max_depth=7):
    """Bounded personal-space inventory; filenames only, no credential reads."""
    project, scan_root = Path(project).resolve(), Path(scan_root).resolve()
    patterns = {'object_annotations.json', '2D_feat_masked_PCA_256d.pkl',
                '3D_feat_aligned.pkl', 'data.mdb', 'train_manifest.txt'}
    pruned = {'.git', '.ssh', '.aws', '.cache', '.conda', 'hf_cache',
              'torch_extensions', 'node_modules', '__pycache__', 'site-packages'}
    matches, errors, visited = [], [], 0
    for base, dirs, files in os.walk(scan_root, onerror=lambda e: errors.append(str(e))):
        depth = len(Path(base).relative_to(scan_root).parts)
        dirs[:] = [d for d in dirs if d not in pruned]
        visited += 1
        if depth >= max_depth:
            dirs[:] = []
        for name in files:
            if (name in patterns or name.endswith('_manifest.pkl')
                    or ('train' in name.lower() and name.endswith(('.tar.gz', '.zip')))):
                path = Path(base) / name
                matches.append(dict(path=str(path), bytes=path.stat().st_size))
        if visited > 25000:
            errors.append('Inventory directory budget reached')
            break
    return dict(scan_root=str(scan_root), maximum_depth=max_depth,
                excluded_directory_names=sorted(pruned), visited_directories=visited,
                matches=matches, errors=errors,
                raw_compare200_videos=sorted(p.name for p in (project / 'data_compare200').glob('P*') if p.is_dir()),
                limits='Bounded inventory of authorized personal space; no global absence claim.')


def validate_sample_rows(samples, catalogue):
    seen = set()
    for sample in samples:
        key = sample['observation_key']
        if key in seen or key not in catalogue:
            raise ValueError('Duplicate or unlinked sample')
        seen.add(key)
        names, ids = sample['candidate_names'], sample['candidate_track_ids']
        target = benchmark_target(sample['benchmark_identity'], names)
        if target != sample['target_class'] or len(ids) != len(names):
            raise ValueError('Target/candidate mismatch')
        histories = sample['candidate_geometry_keys']
        if len(histories) != len(ids):
            raise ValueError('History/candidate mismatch')
        for identity, keys in zip(names, histories):
            for earlier in keys:
                if earlier not in catalogue:
                    raise ValueError('Unlinked geometry history')
                other = catalogue[earlier]
                if (other['source_observation']['frame_index'] >= sample['frame_index']
                        or other['source_observation']['category'] != identity):
                    raise ValueError('Future geometry or mixed benchmark identity')
    return dict(samples=len(samples), unique_samples=len(seen),
                labels_match_benchmark_names=True, all_geometry_strictly_past=True)


def build(campaign, output):
    import numpy as np
    import torch
    import yaml

    campaign, output = Path(campaign).resolve(), Path(output).resolve()
    bundle, geometry = campaign / 'bundle', campaign / 'geometry'
    if output.exists():
        raise FileExistsError('Preserve existing dataset; use a fresh output')
    output.mkdir(parents=True)
    started = time.perf_counter()
    plan = read(bundle / 'input_manifest.json')
    video, fps = plan['video'], plan['fps']
    cfg = yaml.safe_load((bundle / 'effective_config.yaml').read_text())
    original_cfg = yaml.safe_load((bundle / 'original_src/config/epic/whareformer_config.yaml').read_text())
    if video not in original_cfg['videos']['train']:
        raise ValueError('Input video is not in original training split')
    verification = {}
    for name, expected in plan['prepared_hashes'].items():
        if name.startswith('original_src/') or name in ('features.npz', 'frames.json', 'effective_config.yaml', 'shape_features.npz'):
            actual = sha(bundle / name)
            if actual != expected:
                raise ValueError('Source bundle mismatch: ' + name)
            verification[name] = actual
    frames = read(bundle / 'frames.json')
    with np.load(bundle / 'features.npz', allow_pickle=False) as arrays:
        app, loc = arrays['app'].copy(), arrays['loc'].copy()
    shape_archive = np.load(bundle / 'shape_features.npz', allow_pickle=False)
    inputs = read(campaign / 'inputs/manifest.json')['observations']
    selected = {r['observation_key']: r for r in inputs}
    products = read(geometry / 'observations.json')
    if len(selected) != len(inputs) or {r['observation_key'] for r in products} != set(selected):
        raise ValueError('Incomplete/duplicate geometry selection')
    catalogue, checked_artifacts = {}, {}
    for product in products:
        key = product['observation_key']
        source = selected[key]
        for field in ('rgb', 'mask'):
            path = campaign / 'inputs' / source[field]
            if sha(path) != source[field + '_sha256']:
                raise ValueError('Observation source mismatch: ' + key)
        for rep, info in product['representations'].items():
            if info['status'] != 'ready':
                continue
            for artifact in [dict(path=info['path'], sha256=info['sha256']), *info.get('artifacts', {}).values()]:
                path = (geometry / artifact['path']).resolve()
                if not path.is_relative_to(geometry):
                    raise ValueError('Geometry path escapes its root')
                if str(path) not in checked_artifacts:
                    if sha(path) != artifact['sha256']:
                        raise ValueError('Geometry hash mismatch: ' + str(path))
                    checked_artifacts[str(path)] = artifact['sha256']
        catalogue[key] = dict(source_observation=source, geometry=product,
                              descriptor_ids=None)

    original = bundle / 'original_src'
    sys.path.insert(0, str(original))
    package = types.ModuleType('tracking')
    package.__path__ = [str(original / 'tracking')]
    sys.modules['tracking'] = package
    from tracking.tracker.tracker import StandardTracker
    from tracking.tracker.detection import Detection
    from utils.manifest_builder import build_feature_manifest_entry
    torch.set_num_threads(2)
    params = copy.deepcopy(cfg['tracking'])
    params.update(matcher_type='oracle', device_id=None, app_dim=256)
    params['matcher_params'].pop('model_path', None)
    tracker = StandardTracker(params, fps)
    history, samples, numerical = GeometryHistory(), [], {}
    label_counts, offset, ledger_rows = Counter(), 0, []
    oracle_matches, first_frame_new = 0, 0
    for processed, frame in enumerate(frames, 1):
        index, annotations = frame['frame_index'], frame['annotations']
        if frame['offset'] != offset or len({a['name'] for a in annotations}) != len(annotations):
            raise ValueError('Offset mismatch or ambiguous simultaneous benchmark names')
        candidate_ids = [int(t.track_id) for t in tracker.tracks]
        candidate_names = [t.initial_object for t in tracker.tracks]
        names_before = list(candidate_names)
        histories = history.before(candidate_ids, index)
        keys = [f'{video}/{frame["frame"]}__d{i}' for i in range(len(annotations))]
        detections = [Detection(dict(frame=index, detection_idx=i, obj_name=a['name'],
            bbox=a['bounding_box'], app=app[offset+i], loc=loc[offset+i])) for i, a in enumerate(annotations)]
        metadata = dict(frame_name=frame['frame'], frame_idx=index, timestamp=index / fps)
        training = tracker.update(detections, metadata)
        assignments = {int(t.history[-1]['detection_idx']): int(t.track_id)
                       for t in tracker.tracks if t.time_since_update == 0}
        if len(assignments) != len(annotations):
            raise ValueError('Oracle did not cover every current observation')
        manifests, transaction = None, MemoryTransaction()
        if any(key in selected for key in keys) and training is not None:
            features, matches, new = training
            manifests = build_feature_manifest_entry(matches, new, features,
                video, index, transaction, {})
        staged = []
        for i, (key, ann) in enumerate(zip(keys, annotations)):
            target = benchmark_target(ann['name'], names_before)
            if target and assignments[i] != candidate_ids[target - 1]:
                raise ValueError('Original oracle disagrees with independent name target')
            if not target:
                if assignments[i] in candidate_ids:
                    raise ValueError('New identity assigned to a prior track')
                first_frame_new += 1
            oracle_matches += bool(target)
            ledger_rows.append(dict(observation_key=key, frame_index=index,
                detection_idx=i, annotation_id=ann['id'], benchmark_identity=ann['name'],
                oracle_track_id=assignments[i], target_class=target,
                geometric_observation=key in selected))
            if key not in selected:
                continue
            source = selected[key]
            if (source['annotation_id'], source['category'], source['bbox']) != (ann['id'], ann['name'], ann['bounding_box']):
                raise ValueError('Geometry/official annotation join mismatch: ' + key)
            descriptor_ids = frame['shape_feature_ids'][i]
            for rep, identifier in descriptor_ids.items():
                if identifier not in shape_archive.files or not np.isfinite(shape_archive[identifier]).all():
                    raise ValueError('Invalid geometry descriptor')
            catalogue[key]['descriptor_ids'] = descriptor_ids
            if manifests is None:
                raise ValueError('Selected observation lacks original training matrices')
            manifest = manifests[i]
            label = manifest['label']
            if int(label.sum()) != 1 or int(label.argmax()) != target:
                raise ValueError('Original one-hot target mismatch')
            def value(feature_key):
                return np.frombuffer(transaction.values[feature_key.encode('utf-8')], dtype=np.float32)
            det = np.concatenate([value(manifest['det_app_key']), value(manifest['det_loc_key'])])[None, :]
            tracks = np.stack([np.concatenate([value(a), value(l)])
                for a, l in zip(manifest['track_app_keys'], manifest['track_loc_keys'])])
            tensor = np.concatenate([det, tracks], axis=0)
            da, dl, ta, tl = training[0]
            direct = np.concatenate([np.concatenate([da[i], dl[i]])[None, :],
                                      np.concatenate([ta[i], tl[i]], axis=-1)])
            if not np.array_equal(tensor, direct) or tensor.shape != (len(candidate_ids) + 1, 259):
                raise ValueError('Original manifest/loader input differs from oracle features')
            array_key = f'sample_{len(samples):06d}'
            numerical[array_key] = tensor
            numerical[array_key + '_label'] = label
            samples.append(dict(observation_key=key, video=video, split='train',
                frame_index=index, detection_idx=i, annotation_id=ann['id'],
                benchmark_identity=ann['name'], oracle_track_id=assignments[i],
                target_class=target, target_track_id=None if target == 0 else candidate_ids[target - 1],
                candidate_track_ids=list(candidate_ids), candidate_names=list(candidate_names),
                candidate_geometry_keys=copy.deepcopy(histories),
                numerical_input_key=array_key, numerical_label_key=array_key + '_label',
                supervision='authors unmodified oracle / original annotation names',
                geometry_memory_policy='all available strictly earlier views; no fusion or view selection'))
            staged.append((assignments[i], key))
            label_counts['new_track' if target == 0 else 'existing_track'] += 1
        history.commit(index, staged)
        offset += len(annotations)
        if processed % 2500 == 0:
            print(json.dumps(dict(frames=processed, observations=offset,
                                  samples=len(samples), seconds=time.perf_counter()-started)), flush=True)
    shape_archive.close()
    if len(samples) != len(selected) or offset != len(app) or offset != len(loc):
        raise ValueError('Incomplete full-history replay or enriched selection')
    checks = validate_sample_rows(samples, catalogue)
    np.savez_compressed(output / 'training_inputs.npz', **numerical)
    save(output / 'samples.json', samples)
    save(output / 'geometry_catalogue.json', dict(schema_version=1,
        geometry_root=str(geometry), inputs_root=str(campaign / 'inputs'),
        descriptor_archive=str(bundle / 'shape_features.npz'),
        descriptor_archive_sha256=sha(bundle / 'shape_features.npz'), observations=catalogue))
    with (output / 'oracle_observation_ledger.jsonl').open('x', encoding='utf-8') as stream:
        for row in ledger_rows:
            stream.write(json.dumps(row, separators=(',', ':')) + '\n')
    repeated = sum(any(row) for row in (s['candidate_geometry_keys'] for s in samples))
    correct_geometry = sum(s['target_class'] > 0 and bool(s['candidate_geometry_keys'][s['target_class']-1]) for s in samples)
    save(output / 'source_verification.json', dict(bundle_root=str(bundle),
        prepared_hashes_verified=verification, checked_geometry_artifacts=len(checked_artifacts),
        geometry_artifact_hashes=checked_artifacts,
        selection_sha256=sha(campaign / 'inputs/manifest.json'),
        geometry_manifest_sha256=sha(geometry / 'observations.json'),
        official_acquisition=plan.get('acquisition'), source_manifests=plan.get('source_manifests')))
    receipt = dict(schema_version=1, status='complete', development_only=True, video=video,
        effective_bundle_training_videos=cfg['videos']['train'],
        original_training_videos=original_cfg['videos']['train'],
        original_split_config_sha256=sha(bundle / 'original_src/config/epic/whareformer_config.yaml'),
        replay_frames=len(frames), replay_observations=offset,
        oracle_tracks=len(tracker.tracks), oracle_existing_assignments=oracle_matches,
        oracle_new_assignments=first_frame_new, samples=len(samples), sample_labels=dict(label_counts),
        sample_frames=len({s['frame_index'] for s in samples}),
        sample_identities=len({s['benchmark_identity'] for s in samples}),
        samples_with_any_prior_geometry=repeated,
        samples_with_correct_candidate_prior_geometry=correct_geometry,
        numerical_inputs_match_original_manifest_builder=True,
        verified_geometry_artifacts=len(checked_artifacts), causal_validation=checks,
        all_views_preserved_without_new_memory_method=True,
        new_neural_inferences=0, new_manual_labels=0,
        seconds=time.perf_counter()-started,
        external_geometry_dependencies=True,
        limits=['Sparse availability sample from one training video; no validation/test split selected.',
                'Original benchmark names, not newly certified physical identities.',
                'Replay built from original observations; not byte equality to unavailable published training LMDB.',
                'Geometric history is a provenance archive, not a selected or fused deployed memory.'])
    receipt['output_hashes'] = {p.name: sha(p) for p in output.iterdir() if p.is_file()}
    save(output / 'receipt.json', receipt)
    print(json.dumps(receipt, indent=2), flush=True)
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    a = sub.add_parser('inventory')
    a.add_argument('--project', type=Path, required=True)
    a.add_argument('--scan-root', type=Path, required=True)
    a.add_argument('--output', type=Path, required=True)
    b = sub.add_parser('build')
    b.add_argument('--campaign', type=Path, required=True)
    b.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.command == 'inventory':
        result = inventory(args.project, args.scan_root)
        save(args.output, result)
        print(json.dumps(dict(matches=len(result['matches']), errors=result['errors'])))
    else:
        build(args.campaign, args.output)
