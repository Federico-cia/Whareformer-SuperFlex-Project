"""Synthetic contracts: not EPIC performance, not trained-verifier validation."""
from copy import deepcopy
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from scene_geometry import align_da_to_scene, farthest_points, surface_error, transform
from scene_memory import SceneMemoryConfig, SceneObservation, SceneObjectMemory, WeightedVoxels, SceneMemoryUpdater
from registration_verifier import Verification, DiagnosticErrorVerifier, pair_features
from run_scene_memory import replay


def config(**changes):
    # Controlled-test parameters; NOT defaults/recommendations for real data.
    c = SceneMemoryConfig(.05, 100., 2, 1.5, .1, .5, 1, 10000, 3, 'synthetic-test-only')
    return replace(c, **changes)


def patch_points():
    return np.array([[x, y, z] for x in [-.2, .2] for y in [-.2, .2] for z in [-.2, .2]])


def obs(i, points=None, **changes):
    return replace(SceneObservation(f'obs{i}', i, float(i), patch_points() if points is None else points,
                                   True, 'stationary', f'external-test-evidence-{i}'), **changes)


class ControlledVerifier:
    """Synthetic stand-in; accepted decisions cannot be claimed as learned."""
    def __call__(self, a, b):
        # Only separates translated test fixtures, not real partial views.
        return Verification(float(np.linalg.norm(np.mean(a, 0) - np.mean(b, 0))), 'controlled-test-double')


class SceneGeometryTests(unittest.TestCase):
    def test_affine_depth_backprojection_and_camera_pose(self):
        d = np.arange(1., 17.).reshape(4, 4)
        s = 2 * d + 3
        mask = np.zeros((4, 4), bool); mask[1:3, 1:3] = True
        t = np.eye(4); t[:3, 3] = [2, 3, 4]
        result = align_da_to_scene(d, s, mask, mask, [2, 2, 1, 1], t, minimum_static_pixels=4)
        self.assertTrue(result.valid)
        v, u = np.nonzero(mask); z = s[v, u]
        expected = np.column_stack([(u-1)*z/2, (v-1)*z/2, z]) + [2, 3, 4]
        np.testing.assert_allclose(result.world_points, expected)

    def test_failed_alignment_has_no_raw_depth_fallback(self):
        d = np.ones((4, 4)); mask = np.zeros((4, 4), bool); mask[0] = True
        result = align_da_to_scene(d, d, mask, mask, [1, 1, 0, 0], np.eye(4), minimum_static_pixels=4)
        self.assertFalse(result.valid)
        self.assertIsNone(result.world_points)
        with self.assertRaises(ValueError):
            align_da_to_scene(d, d, mask, np.zeros_like(mask), [1, 1, 0, 0], np.eye(4), minimum_static_pixels=4)

    def test_nonpositive_object_depth_and_malformed_pose(self):
        d = np.arange(1., 17.).reshape(4, 4); s = 2*d-3
        mask = np.zeros((4, 4), bool); mask[0, 0] = True
        result = align_da_to_scene(d, s, mask, mask, [1, 1, 0, 0], np.eye(4), minimum_static_pixels=4)
        self.assertFalse(result.valid)
        with self.assertRaises(ValueError):
            transform(patch_points(), np.zeros((4, 4)))

    def test_surface_target_respects_discrete_symmetry(self):
        p = patch_points(); r = np.eye(4); r[:2, :2] *= -1
        self.assertAlmostEqual(surface_error(p, r, np.eye(4)), 0)
        # A true displacement remains detectable.
        r[:3, 3] = [4, 0, 0]
        self.assertGreater(surface_error(p, r, np.eye(4)), 1)

    def test_fps_no_repeats_until_exhausted_including_identical_points(self):
        p = np.zeros((10, 3))
        ids = farthest_points(p, 15)
        self.assertEqual(len(set(ids[:10])), 10)
        self.assertEqual(len(ids), 15)
        np.testing.assert_array_equal(ids, farthest_points(p, 15))


class SceneMemoryTests(unittest.TestCase):
    def memory(self, **kwargs):
        return SceneObjectMemory('V', 'T', config(**kwargs), ControlledVerifier())

    def test_no_model_never_confirms_or_fuses(self):
        m = SceneObjectMemory('V', 'T', config())
        for i in range(4):
            self.assertFalse(m.update(obs(i))['shape_changed'])
        self.assertEqual(len(m.cloud()), 0)
        self.assertLessEqual(len(m.states), 3)

    def test_candidate_temporal_confirmation_and_no_fixed_view_budget(self):
        m = self.memory()
        self.assertEqual(m.update(obs(0))['status'], 'pending_confirmation')
        self.assertEqual(m.update(obs(1))['status'], 'fused_stationary')
        for i in range(2, 7):
            m.update(obs(i))
        self.assertEqual(m.shape_version, 6)
        self.assertEqual(len(m.shape.cells), len(patch_points()))
        self.assertEqual(len(next(iter(m.states.values())).keys), 7)

    def test_failures_and_uncertain_staticity_never_add_points(self):
        m = self.memory(); m.update(obs(0)); m.update(obs(1))
        before = m.cloud().copy()
        for i, change in enumerate([dict(alignment_valid=False), dict(staticity='moving'),
                                    dict(staticity='unknown'), dict(evidence_id='')], 2):
            self.assertFalse(m.update(obs(i, **change))['shape_changed'])
            np.testing.assert_array_equal(m.cloud(), before)

    def test_duplicate_noncausal_source_completion_rejected_atomically(self):
        m = self.memory(); m.update(obs(0))
        before = m.snapshot()
        for item in [obs(0), obs(1, source='moge'), obs(1, observed_only=False), obs(1, timestamp=0.)]:
            with self.assertRaises(ValueError): m.update(item)
            self.assertEqual(m.snapshot(), before)

    def test_novel_partial_surface_retained_without_bidirectional_gate(self):
        # Controlled acceptance isolates memory behaviour from verifier quality.
        m = SceneObjectMemory('V', 'T', config(), lambda a, b: Verification(0., 'test-only'))
        old = patch_points()
        novel = old + [2, 0, 0]
        m.update(obs(0, old)); m.update(obs(1, old))
        before = len(m.cloud())
        event = m.update(obs(2, novel))
        self.assertTrue(event['shape_changed'])
        self.assertGreater(len(m.cloud()), before)

    def test_relocated_state_preserves_shape_and_stays_separate(self):
        m = self.memory(); m.update(obs(0)); m.update(obs(1))
        shape = m.cloud().copy()
        p = patch_points() + [4, 0, 0]
        m.update(obs(2, p))
        event = m.update(obs(3, p))
        self.assertEqual(event['status'], 'confirmed_placement_awaiting_shape_registration')
        np.testing.assert_array_equal(m.cloud(), shape)
        with self.assertRaises(ValueError):
            m.merge_placement(event['state_id'], np.eye(4), frame=3, timestamp=3., evidence_id='test')

    def test_explicit_verified_motion_fusion_keeps_one_shape(self):
        m = self.memory(fuse_after_motion=True)
        m.update(obs(0)); m.update(obs(1))
        p = patch_points() + [4, 0, 0]
        m.update(obs(2, p)); event = m.update(obs(3, p))
        before = m.cloud().copy()
        t = np.eye(4); t[0, 3] = -4
        merge = m.merge_placement(event['state_id'], t, frame=3, timestamp=3., evidence_id='known-synthetic-motion')
        self.assertTrue(merge['shape_changed'])
        np.testing.assert_allclose(m.cloud(), before, atol=1e-12)
        # Later views in that placement use the stored transform.
        self.assertTrue(m.update(obs(4, p))['shape_changed'])

    def test_cell_budget_failure_preserves_all_prior_state(self):
        m = SceneObjectMemory('V', 'T', config(maximum_cells=8), lambda a, b: Verification(0., 'test'))
        m.update(obs(0)); m.update(obs(1))
        before = m.snapshot()
        with self.assertRaises(ValueError): m.update(obs(2, patch_points() + [2, 0, 0]))
        self.assertEqual(m.snapshot(), before)

    def test_decay_changes_weight_without_deleting_unique_coverage(self):
        v = WeightedVoxels(config())
        v.add(np.array([[.001, 0, 0], [2., 0, 0]]), 0, 'a')
        before = v.weights(0).copy()
        v.add(np.array([[.002, 0, 0]]), 100, 'b')
        self.assertEqual(len(v.cloud()), 2)
        self.assertLess(v.weights(100)[1], before[1])
        self.assertGreater(v.cloud()[0, 0], .0015)

    def test_filter_outliers_not_novel_surface_and_density_not_support(self):
        c = config(outlier_radius=.1, minimum_neighbors=2)
        v = WeightedVoxels(c)
        result = v.add([[0, 0, 0], [.01, 0, 0], [100, 0, 0]], 0., 'a')
        self.assertEqual(result['kept_points'], 2)
        self.assertAlmostEqual(v.weights(0)[0], 1.)

    def test_export_fps_inverse_and_provenance_without_overwrite(self):
        m = self.memory(); m.update(obs(0)); m.update(obs(1))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.npz'; m.export_superflex(path)
            with np.load(path, allow_pickle=False) as z:
                self.assertEqual(z['normalized_points'].shape, (4096, 3))
                np.testing.assert_allclose(z['normalized_points'] * z['scale'] + z['translation'], z['selected_points'])
                self.assertTrue(z['observed_only'].item())
                self.assertEqual(json.loads(z['provenance_json'].item())['track_id'], 'T')
            with self.assertRaises(FileExistsError): m.export_superflex(path)


class VerifierTests(unittest.TestCase):
    def test_diagnostic_fit_group_separation_and_roundtrip(self):
        p = patch_points(); x = np.array([pair_features(p + [a, 0, 0], p) for a in [0., .1, .2, .3]])
        y = np.array([0., .1, .2, .3])
        kwargs = dict(training_groups=['A']*4, validation_groups=['B'], ridge=.01, target_provenance='known-test-transforms')
        model = DiagnosticErrorVerifier.fit(x, y, **kwargs)
        self.assertLess(model(p, p).error, model(p+[.3, 0, 0], p).error)
        with self.assertRaises(ValueError): DiagnosticErrorVerifier.fit(x, y, **dict(kwargs, validation_groups=['A']))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'verifier.json'; model.save(path)
            other = DiagnosticErrorVerifier(json.loads(path.read_text()))
            self.assertEqual(model(p, p), other(p, p))

    def test_invalid_predictions(self):
        for value in [-1., float('nan'), float('inf')]:
            with self.assertRaises(ValueError): Verification(value, 'test')


class ReplayTests(unittest.TestCase):
    def test_offline_no_model_replay_is_explicit_pending_and_hash_bound(self):
        from dataclasses import asdict
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); path = root/'cloud.npz'; np.savez(path, world_points=patch_points())
            spec = dict(path='cloud.npz', sha256=hashlib.sha256(path.read_bytes()).hexdigest())
            data = dict(schema='point3-scene-replay-v1', video='V', association_source='oracle-development',
                        config=asdict(config()), observations=[dict(key=f'o{i}', frame=i, timestamp=float(i),
                        track_id='T', source='da_aligned', coordinate_frame='scene', observed_only=True,
                        alignment_valid=True, alignment_provenance='synthetic-test', staticity='stationary',
                        evidence_id='synthetic-test', points=spec) for i in range(2)])
            manifest = root/'manifest.json'; manifest.write_text(json.dumps(data))
            summary = replay(manifest, root/'out')
            self.assertFalse(summary['trained_model_used'])
            self.assertTrue(summary['diagnostic_only'])
            self.assertEqual(summary['exports'], [])
            with self.assertRaises(FileExistsError): replay(manifest, root/'out')
            path.write_bytes(b'corrupt')
            with self.assertRaises(ValueError): replay(manifest, root/'bad')
            self.assertFalse((root/'bad').exists())


if __name__ == '__main__':
    unittest.main()
