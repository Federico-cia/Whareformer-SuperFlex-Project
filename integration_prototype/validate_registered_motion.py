"""Controlled known-motion exercise with real observed surfaces, not real GT."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.spatial.transform import Rotation
from export_point3_training import config
from registered_scene_memory import RegisteredObjectMemory
from cloud_memory import RegistrationConfig
from registration_verifier import DiagnosticErrorVerifier
from scene_memory import SceneObservation
from scene_geometry import transform, surface_error


def validate(a):
    audit, trained, out = Path(a.audit), Path(a.model), Path(a.out)
    model = DiagnosticErrorVerifier(json.loads((trained / 'model.json').read_text()))
    report = json.loads((trained / 'report.json').read_text())
    observations = [json.loads(l) for l in (audit / 'per_observation.jsonl').read_text().splitlines()]
    chosen = {}
    for row in observations:
        if row.get('align_valid') and row.get('mask_source') != 'catalogue_only':
            chosen.setdefault(row['identity'], row)
    results = []
    rng = np.random.default_rng(20261122)
    with np.load(audit / 'world_clouds_aligned.npz', allow_pickle=False) as clouds:
        for name, row in chosen.items():
            p = clouds[row['key'].replace('/', '__')].astype(float)
            radius = np.sqrt(np.mean(np.sum((p - p.mean(0)) ** 2, axis=1)))
            m = RegisteredObjectMemory('known-motion-diagnostic', str(row['track']), config(radius, report), model,
                RegistrationConfig(fit_points=256, refine_points=700, validation_points=128, iterations=20))
            first = m.update(SceneObservation('seed', 1, 1., p, True, 'unknown', ''))
            if not m.states:
                results.append(dict(identity=name, status=first['status'], accepted=False))
                continue
            expected_origin = np.linalg.inv(m.states['registered-shape'].object_to_scene)
            motion = np.eye(4)
            motion[:3, :3] = Rotation.from_euler('xyz', [35, -45, 70], degrees=True).as_matrix()
            motion[:3, 3] = p.mean(0) - motion[:3, :3] @ p.mean(0) + radius * np.array([2, -1, .5])
            # Different partial views of the same observed surface; known motion.
            keep = np.argsort((p - p.mean(0)) @ rng.normal(size=3))[-max(64, int(.8 * len(p))):]
            moved = transform(p[keep], motion)
            event = m.update(SceneObservation('moved', 2, 2., moved, True, 'unknown', ''))
            error = None
            if 'world_to_object' in event:
                estimated = np.asarray(event['world_to_object']) @ motion
                error = surface_error(p, estimated, expected_origin)
            results.append(dict(identity=name, source_key=row['key'], status=event['status'],
                accepted=event['shape_changed'], true_error=error,
                predicted_error=event.get('predicted_error'),
                true_small_error=None if error is None else error <= report['target_error_tolerance']))
    summary = dict(cases=len(results), accepted=sum(r['accepted'] for r in results),
        accepted_small_error=sum(r['accepted'] and r.get('true_small_error') is True for r in results),
        accepted_excessive_error=sum(r['accepted'] and r.get('true_small_error') is False for r in results),
        scope='known simulated rigid motion and 80% crop of an observed surface; no independent real motion GT',
        selection_use='diagnostic only; model and threshold unchanged', cases_detail=results)
    with out.open('x') as f:
        json.dump(summary, f, indent=2)
    print(json.dumps({k: v for k, v in summary.items() if k != 'cases_detail'}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for arg in ('audit', 'model', 'out'):
        p.add_argument('--' + arg, required=True)
    validate(p.parse_args())
