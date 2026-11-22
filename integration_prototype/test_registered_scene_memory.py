from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from registered_scene_memory import RegisteredObjectMemory
from scene_geometry import transform
from scene_memory import SceneObservation
from registration_verifier import Verification
from test_scene_memory import config
from scene_superflex_worker import process, load_input
from shape_tools.geometry import normalize_shape
from shape_tools.metrics import descriptors


class Verifier:
    def __init__(self, error):
        self.error = error

    def __call__(self, a, b):
        return Verification(self.error, 'controlled-test-only')


def fake_registration(source, target, config):
    # Deliberately fails all legacy gates; only learned verifier may decide.
    return dict(rotation=np.eye(3).tolist(), translation=(target.mean(0) - source.mean(0)).tolist(),
                accepted=False, reasons=['legacy_gate_failed'])


class RegisteredMemoryTests(unittest.TestCase):
    def setUp(self):
        self.p = np.random.default_rng(11).normal(size=(200, 3)) * [.8, .5, .3]
        self.cfg = config(voxel_size=.005, minimum_neighbors=1, confirmation_weight=1., fuse_after_motion=True)

    def observation(self, i, p=None, valid=True):
        return SceneObservation(f'key{i}', i, float(i), self.p if p is None else p,
                                valid, 'unknown', '')

    @patch('registered_scene_memory.register_rigid', fake_registration)
    def test_confirm_unknown_staticity_and_move_without_legacy_gate(self):
        m = RegisteredObjectMemory('V', '0', self.cfg, Verifier(0))
        self.assertFalse(m.update(self.observation(1))['shape_changed'])
        event = m.update(self.observation(2, self.p + [3, 1, -2]))
        self.assertTrue(event['shape_changed'])
        self.assertFalse(event['legacy_gate_used'])
        self.assertEqual(m.shape_version, 1)
        self.assertFalse(m.snapshot()['staticity_required'])
        before = m.cloud().copy()
        m.verifier = Verifier(1)
        event = m.update(self.observation(3, self.p + 100))
        self.assertFalse(event['shape_changed'])
        np.testing.assert_array_equal(before, m.cloud())
        self.assertEqual(m.shape_version, 1)

    @patch('registered_scene_memory.register_rigid', fake_registration)
    def test_missing_verifier_never_promotes_and_bad_alignment_never_fuses(self):
        m = RegisteredObjectMemory('V', '1', self.cfg)
        m.update(self.observation(1))
        self.assertFalse(m.update(self.observation(2))['shape_changed'])
        self.assertEqual(len(m.cloud()), 0)
        self.assertEqual(m.update(self.observation(3, valid=False))['status'], 'alignment_failed')
        before = m.snapshot()
        with self.assertRaises(ValueError):
            m.update(self.observation(2))
        self.assertEqual(before, m.snapshot())

    @patch('registered_scene_memory.register_rigid', fake_registration)
    def test_fps_worker_exact_input_failure_and_tagged_test_output(self):
        m = RegisteredObjectMemory('V', '1', self.cfg, Verifier(0))
        m.update(self.observation(1)); m.update(self.observation(2))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / 'input.npz'
            m.export_superflex(path)
            from scene_superflex_worker import sha
            expected = m.superflex_input()['normalized_points']
            def backend(data, folder):
                np.testing.assert_array_equal(data['normalized'], expected)
                p = normalize_shape(self.p[np.resize(np.arange(len(self.p)), 1024)])
                return p, *descriptors(p)
            result = process(path, sha(path), root / 'good', backend=backend, test_backend=True)
            self.assertEqual(result['status'], 'ready')
            self.assertEqual(result['backend'], 'test-double')
            self.assertFalse(result['random_input_resampling'])
            def broken(data, folder):
                raise RuntimeError('controlled GPU failure')
            before = m.snapshot()
            failed = process(path, sha(path), root / 'failed', backend=broken, test_backend=True)
            self.assertEqual(failed['status'], 'failed')
            self.assertEqual(m.snapshot(), before)
            with self.assertRaises(ValueError):
                load_input(path, '0' * 64)
            with self.assertRaises(FileExistsError):
                process(path, sha(path), root / 'good', backend=backend, test_backend=True)

    def test_actual_registrar_recovers_large_known_motion(self):
        from scipy.spatial.transform import Rotation
        from cloud_memory import RegistrationConfig
        m = RegisteredObjectMemory('V', '1', self.cfg, Verifier(0),
            RegistrationConfig(fit_points=140, refine_points=200, validation_points=60, iterations=20))
        m.update(self.observation(1))
        motion = np.eye(4)
        motion[:3, :3] = Rotation.from_euler('xyz', [30, -50, 80], degrees=True).as_matrix()
        motion[:3, 3] = [3, -2, 1]
        event = m.update(self.observation(2, transform(self.p, motion)))
        self.assertTrue(event['shape_changed'])
        recovered = np.asarray(event['world_to_object']) @ motion
        expected = np.eye(4); expected[:3, 3] = -self.p.mean(0)
        np.testing.assert_allclose(recovered, expected, atol=.03)

    @patch('registered_scene_memory.register_rigid', fake_registration)
    def test_original_tracker_coordinator_adapter_preserves_assignment_and_prior(self):
        from frame_coordinator import FrameCoordinator
        from geometry_matcher import GeometryMatcher, GeometryConfig
        from registered_scene_memory import RegisteredMemoryUpdater
        from test_frame_coordinator import tracker, inputs
        t = tracker()
        t.matcher = GeometryMatcher(t.matcher.baseline, 'V', GeometryConfig('diagnostic', 'da_raw_points'))
        c = FrameCoordinator(t, RegisteredMemoryUpdater(self.cfg, Verifier(0)))
        outputs = []
        for i in range(2):
            args = inputs(i)
            key = args['observation_keys'][0]
            args['features'] = {key: None}
            args['geometry_inputs'] = {key: replace(self.observation(i), key=key)}
            outputs.append(c.step(**args))
        self.assertEqual(outputs[1]['assignments'], {'V/f1/d0': '40'})
        self.assertEqual(outputs[0]['after']['geometry']['40']['value'].shape_version, 0)
        self.assertEqual(outputs[1]['after']['geometry']['40']['value'].shape_version, 1)


if __name__ == '__main__':
    unittest.main()
