"""Replay prepared scene observations; exports FPS inputs, does not run SuperFlex.

Usage: python run_scene_memory.py --manifest observations.json --out NEW_FOLDER
No threshold/model defaults: a development-selected configuration is mandatory.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scene_memory import SceneMemoryConfig, SceneObjectMemory, SceneObservation
from registration_verifier import DiagnosticErrorVerifier, TorchScriptPairVerifier, UnavailableVerifier


def artifact(root, spec):
    path = (root / spec['path']).resolve()
    if not path.is_relative_to(root) or hashlib.sha256(path.read_bytes()).hexdigest() != spec['sha256']:
        raise ValueError('Artifact path/hash mismatch')
    return path


def replay(manifest_path, output):
    source = Path(manifest_path).resolve()
    root = source.parent
    manifest = json.loads(source.read_text(encoding='utf-8'))
    if (manifest.get('schema') != 'point3-scene-replay-v1'
            or manifest.get('association_source') not in ('predicted', 'oracle-development')
            or not manifest.get('video') or not manifest.get('observations')):
        raise ValueError('Versioned scene manifest with explicit association source required')
    config = SceneMemoryConfig(**manifest['config'])
    if config.fuse_after_motion:
        raise ValueError('CLI stage one is static-only; motion registration uses the explicit API')
    spec = manifest.get('verifier')
    if spec is None:
        verifier = UnavailableVerifier()
    elif spec['backend'] == 'diagnostic-error':
        verifier = DiagnosticErrorVerifier(json.loads(artifact(root, spec).read_text(encoding='utf-8')))
    elif spec['backend'] == 'torchscript-pair-error':
        verifier = TorchScriptPairVerifier(artifact(root, spec), sha256=spec['sha256'], sample_points=spec['sample_points'])
    else:
        raise ValueError('Unknown verifier backend')
    # Validate file bindings/order before creating a deliverable directory.
    checked, keys, frame = [], set(), -1
    times = {}
    for row in manifest['observations']:
        if (type(row['frame']) is not int or row['frame'] < frame or row['key'] in keys
                or row['source'] != 'da_aligned' or row['coordinate_frame'] != 'scene'
                or row['observed_only'] is not True or not row.get('alignment_provenance')):
            raise ValueError('Sorted observed scene inputs and provenance required')
        tid = str(row['track_id'])
        if row['frame'] <= times.get(tid, -1):
            raise ValueError('One observation per predicted track per frame required')
        frame = row['frame']; times[tid] = frame; keys.add(row['key'])
        path = artifact(root, row['points']) if row['alignment_valid'] else None
        checked.append((row, tid, path))
    out = Path(output)
    out.mkdir(parents=True, exist_ok=False)
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2, allow_nan=False), encoding='utf-8')
    memories, trace, exports = {}, [], []
    try:
        for row, tid, path in checked:
            if tid not in memories:
                memories[tid] = SceneObjectMemory(manifest['video'], tid, config, verifier)
            memory = memories[tid]
            if path is None:
                p = None
            else:
                with np.load(path, allow_pickle=False) as z:
                    p = z['world_points'].copy()
            observation = SceneObservation(row['key'], row['frame'], row['timestamp'], p,
                row['alignment_valid'], row['staticity'], row.get('evidence_id', ''),
                provenance=dict(alignment=row['alignment_provenance'], artifact=row.get('points'),
                                association_source=manifest['association_source']))
            event = memory.update(observation)
            trace.append(dict(track_id=tid, **event))
            if event['shape_changed']:
                tag = hashlib.sha256(tid.encode()).hexdigest()[:16]
                filename = f'shape_{tag}_v{memory.shape_version}.npz'
                memory.export_superflex(out / filename)
                exports.append(dict(track_id=tid, shape_version=memory.shape_version, path=filename,
                                    sha256=hashlib.sha256((out / filename).read_bytes()).hexdigest()))
        summary = dict(status='completed', trained_model_used=spec is not None,
                       diagnostic_only=manifest['association_source'] != 'predicted',
                       manifest_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                       tracks={tid: m.snapshot() for tid, m in memories.items()}, exports=exports,
                       reconstruction_inference_run=False, tracking_efficacy_evaluated=False)
    except Exception as error:
        summary = dict(status='failed', error=f'{type(error).__name__}: {error}',
                       completed_observations=len(trace), exports=exports)
        raise
    finally:
        (out / 'events.jsonl').write_text(''.join(json.dumps(e, allow_nan=False) + '\n' for e in trace), encoding='utf-8')
        (out / 'summary.json').write_text(json.dumps(summary, indent=2, allow_nan=False), encoding='utf-8')
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(replay(args.manifest, args.out), indent=2))
