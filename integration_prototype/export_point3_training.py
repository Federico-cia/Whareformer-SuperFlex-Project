"""Causal oracle development replay and portable accumulated-shape export.

All queries of a frame read the same PRE-update memories. Only afterwards are
the available views registered and committed. No predicted track is used as GT.
Observed-cloud descriptors are explicitly distinct from neural completion.
"""
import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import time
import numpy as np
from cloud_memory import RegistrationConfig
from registered_scene_memory import RegisteredObjectMemory
from multi_hypothesis_memory import MultiHypothesisMemory
from position_state_memory import PositionConfig, PositionStateMemory
from dataclasses import replace
from scene_memory import SceneMemoryConfig, SceneObservation
from registration_verifier import DiagnosticErrorVerifier
from shape_tools.geometry import normalize_shape
from shape_tools.metrics import descriptors
from scene_geometry import farthest_points


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_json(path, data):
    with Path(path).open('x', encoding='utf-8') as f:
        json.dump(data, f, indent=2, allow_nan=False)


def config(radius, model_report):
    # Minimal engineering settings relative to each track's first valid radius.
    # Not optimized against the held-out verifier evaluation or tracking metrics.
    return SceneMemoryConfig(voxel_size=radius * .04, decay_half_life=3600.,
        minimum_confirmations=2, confirmation_weight=1.,
        maximum_predicted_error=model_report['maximum_predicted_error'],
        outlier_radius=radius * .1, minimum_neighbors=2, maximum_cells=200000,
        maximum_pending_states=3, selection_provenance='prototype-v1:relative-resolution-.04R;'
        'density-.1R-two-neighbors;one-hour-half-life;two-view-confirmation;'
        'learned-error-threshold-from-simulated-calibration;not-tracking-tuned',
        fuse_after_motion=True)


def feature_file(path, points):
    # Reuse existing descriptors unchanged. This is the observed-points control,
    # not a fabricated SuperFlex result or a choice of the final matcher distance.
    ids = farthest_points(points, 1024)
    p = normalize_shape(points[ids])
    d2, spectrum = descriptors(p)
    with path.open('xb') as f:
        np.savez_compressed(f, points=p, d2=d2, spectrum=spectrum,
                            representation='accumulated_observed_points', completed_by_superflex=False)
    return dict(path=path.name, sha256=sha(path), representation='observed_points',
                completed_by_superflex=False)


def export(a):
    audit, dataset, trained, out = map(Path, (a.audit, a.dataset, a.model, a.out))
    report = json.loads((trained / 'report.json').read_text())
    if sha(trained / 'model.json') != report['model_sha256']:
        raise ValueError('Model hash mismatch')
    verifier = DiagnosticErrorVerifier(json.loads((trained / 'model.json').read_text()))
    samples = json.loads((dataset / 'samples.json').read_text())
    observations = {r['key']: r for r in map(json.loads,
        (audit / 'per_observation.jsonl').read_text().splitlines())}
    if {r['observation_key'] for r in samples} != set(observations):
        raise ValueError('Original labelled examples and audit keys differ')
    samples.sort(key=lambda r: (r['frame_index'], r['detection_idx']))
    out.mkdir(parents=True, exist_ok=False)
    feature_dir, shape_dir = out / 'features', out / 'shapes'
    feature_dir.mkdir(); shape_dir.mkdir()
    memories, latest, examples, events, versions = {}, {}, [], [], []
    configs, started = {}, time.perf_counter()
    policy = getattr(a, 'policy', 'multi')
    memory_class = dict(multi=MultiHypothesisMemory, position=PositionStateMemory).get(policy, RegisteredObjectMemory)
    position_config, cameras = None, {}
    if policy == 'position':
        # Option A: explicit position-test parameters, never defaults.
        if not getattr(a, 'position_config', None):
            raise ValueError('--position-config required for the position policy')
        position_config = PositionConfig(**json.loads(Path(a.position_config).read_text(encoding='utf-8')))
        catalogue = json.loads((dataset / 'geometry_catalogue.json').read_text(encoding='utf-8'))['observations']
        catalogue = catalogue.values() if isinstance(catalogue, dict) else catalogue
        intrinsics = {c['source_observation']['observation_key']: c['source_observation']['intrinsics'] for c in catalogue}
        for key, obs in observations.items():
            if key in intrinsics and obs.get('c2w') is not None:
                fx, fy, cx, cy = intrinsics[key]
                # DA depth grid of the audit: principal point at the image centre
                # (456x256 for P01_01; all aligned clouds verified inside it).
                cameras[key] = dict(world_to_camera=np.linalg.inv(np.asarray(obs['c2w'], float)).tolist(),
                                    intrinsics=[fx, fy, cx, cy], image_size=[int(round(2 * cx)), int(round(2 * cy))])
    rows_by_frame = {}
    for row in samples:
        rows_by_frame.setdefault(row['frame_index'], []).append(row)
    with np.load(audit / 'world_clouds_aligned.npz', allow_pickle=False) as clouds:
        for number, (frame, rows) in enumerate(sorted(rows_by_frame.items())):
            # All candidate snapshots are created before ANY current-frame update.
            for row in rows:
                key = row['observation_key']
                obs = observations[key]
                tag = hashlib.sha256(key.encode()).hexdigest()[:20]
                qspec = None
                if obs.get('align_valid') and obs.get('mask_source') != 'catalogue_only':
                    p = clouds[key.replace('/', '__')].astype(float)
                    qspec = feature_file(feature_dir / f'query_{tag}.npz', p)
                    qspec['path'] = 'features/' + qspec['path']
                candidates = []
                for tid, name in zip(row['candidate_track_ids'], row['candidate_names']):
                    prior = latest.get(str(tid))
                    if prior is not None:
                        assert prior['last_update_frame'] < frame
                    candidates.append(dict(track_id=tid, benchmark_name=name, memory=prior,
                                           missing_reason=None if prior else 'no_confirmed_past_geometry'))
                examples.append(dict(observation_key=key, frame_index=frame,
                    detection_idx=row['detection_idx'], video=row['video'],
                    target_class=row['target_class'], target_track_id=row['target_track_id'],
                    candidate_track_ids=row['candidate_track_ids'], candidates=candidates,
                    numerical_input_key=row['numerical_input_key'],
                    numerical_label_key=row['numerical_label_key'], query=qspec,
                    query_missing_reason=None if qspec else 'invalid_alignment_or_catalogue_only_masks',
                    point2_training_status='prototype-observed-memory-ready',
                    supervision='authors-oracle-original-targets', new_track_class=0))
            for row in rows:
                key, tid = row['observation_key'], str(row['oracle_track_id'])
                obs = observations[key]
                if not obs.get('align_valid') or obs.get('mask_source') == 'catalogue_only':
                    events.append(dict(key=key, track_id=tid, frame=frame, shape_changed=False,
                                       status='excluded_alignment_or_masks'))
                    continue
                p = clouds[key.replace('/', '__')].astype(float)
                if tid not in memories:
                    radius = float(np.sqrt(np.mean(np.sum((p - p.mean(0)) ** 2, axis=1))))
                    cfg = config(radius, report)
                    if policy in ('multi', 'position'):
                        cfg = replace(cfg, decay_half_life=1000., confirmation_weight=1.5,
                            maximum_pending_states=16,
                            selection_provenance=cfg.selection_provenance + ';multi-v1:half-life-1000s;'
                            'promotion-1.5/two-frames;16-pending;DenStream-like-pruning;engineering-development-settings')
                    configs[tid] = asdict(cfg)
                    registration = RegistrationConfig(fit_points=256, refine_points=700, validation_points=128, iterations=20)
                    memories[tid] = (PositionStateMemory('P01_01', tid, cfg, verifier, registration, position_config)
                                     if policy == 'position' else memory_class('P01_01', tid, cfg, verifier, registration))
                memory = memories[tid]
                observation = SceneObservation(key, frame, frame / 60., p, True,
                    'unknown', '', provenance=dict(audit_key=key, mask_source=obs['mask_source'],
                    association='authors-oracle', timestamp_basis='frame_index/60 diagnostic replay'),
                    camera=cameras.get(key))
                try:
                    event = memory.update(observation)
                except ValueError as error:
                    events.append(dict(key=key, track_id=tid, frame=frame, shape_changed=False,
                                       status='update_failed_preserved_previous', error=str(error)))
                    continue
                events.append(dict(track_id=tid, **event))
                if event['shape_changed']:
                    tag = hashlib.sha256(tid.encode()).hexdigest()[:12]
                    name = f'memory_{tag}_v{memory.shape_version:04d}'
                    fps_path = shape_dir / (name + '.npz')
                    memory.export_superflex(fps_path)
                    features = feature_file(feature_dir / (name + '.npz'), memory.cloud())
                    features['path'] = 'features/' + features['path']
                    current = dict(track_id=tid, shape_version=memory.shape_version,
                        last_update_frame=frame, observation_keys=list(memory.fused_keys if policy in ('multi', 'position')
                            else memory.states['registered-shape'].keys),
                        points=features, superflex_input=dict(path='shapes/' + fps_path.name, sha256=sha(fps_path)),
                        superflex_result=None, quality='experimental-verifier-simulated-calibration')
                    latest[tid] = current
                    versions.append(current)
            if number % 20 == 0:
                print(json.dumps(dict(frames=number + 1, total_frames=len(rows_by_frame),
                                      exports=len(versions), seconds=round(time.perf_counter() - started, 1))), flush=True)
    # Copy unchanged numerical labels/input; do not regenerate or reorder arrays.
    import shutil
    shutil.copyfile(dataset / 'training_inputs.npz', out / 'training_inputs.npz')
    save_json(out / 'examples.json', examples)
    save_json(out / 'versions.json', versions)
    (out / 'events.jsonl').write_text(''.join(json.dumps(e, allow_nan=False) + '\n' for e in events))
    save_json(out / 'configurations.json', configs)
    hypotheses = {}
    if policy in ('multi', 'position'):
        state_dir = out / 'hypotheses'; state_dir.mkdir()
        for tid, memory in memories.items():
            name = hashlib.sha256(tid.encode()).hexdigest()[:12] + '.npz'
            memory.export_hypotheses(state_dir / name)
            hypotheses[tid] = dict(path='hypotheses/' + name, sha256=sha(state_dir / name), snapshot=memory.snapshot())
        save_json(out / 'hypotheses.json', hypotheses)
    summary = dict(schema='point3-causal-accumulated-training-v1', video='P01_01',
        association_source='authors-oracle-development', samples=len(examples),
        query_ready=sum(e['query'] is not None for e in examples), shape_versions=len(versions),
        confirmed_tracks=len(latest), tracks_observed=len(memories),
        queries_with_correct_past_memory=sum(any(c['track_id'] == e['target_track_id'] and
            c['memory'] is not None for c in e['candidates']) for e in examples),
        new_track_examples=sum(e['target_class'] == 0 for e in examples),
        statuses=dict(Counter(e['status'] for e in events)),
        source_files={str(p.resolve()): sha(p) for p in
            (dataset / 'samples.json', dataset / 'training_inputs.npz',
             audit / 'per_observation.jsonl', audit / 'world_clouds_aligned.npz', trained / 'model.json', trained / 'report.json',
             *((dataset / 'geometry_catalogue.json', Path(a.position_config)) if policy == 'position' else ()))},
        representation='observed_accumulated_points', reconstruction_inference_run=False,
        learned_registration_used=True, real_fusion_accuracy_validated=False,
        all_frame_queries_before_updates=True,
        policy=dict(multi='multi-hypothesis-scene-memory-v1', position=PositionStateMemory.policy).get(
            policy, 'register-every-view-v1'),
        position_config=None if position_config is None else asdict(position_config),
        active_hypotheses=sum(len(m.states) for m in memories.values()),
        hypothesis_artifacts=hypotheses,
        limits=['sparse development sample; no new-track training examples',
                'simulated verifier supervision, substantial false acceptance on simulated holdout',
                'memory engineering settings not tuned for tracking',
                'SuperFlex FPS inputs ready; no new neural reconstruction in local replay',
                'oracle association does not measure predicted tracking benefit'],
        seconds=time.perf_counter() - started)
    save_json(out / 'summary.json', summary)
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('audit', 'dataset', 'model', 'out'):
        p.add_argument('--' + name, required=True)
    p.add_argument('--policy', choices=['position', 'multi', 'single'], default='position')
    p.add_argument('--position-config', help='JSON with explicit PositionConfig fields (position policy)')
    export(p.parse_args())
