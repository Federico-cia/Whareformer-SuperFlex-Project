"""Option A: state = placement; position test chooses the state, verifier only fusion."""
from dataclasses import replace
import unittest
import numpy as np
from scipy.spatial import cKDTree
from position_state_memory import (Camera, PositionConfig, PositionStateMemory,
                                   PositionStateUpdater, consistency)
from registration_verifier import Verification
from scene_memory import SceneObservation
from test_scene_memory import config

SIZE = np.array([.4, .3, .2])


def box_surface(n=6000, seed=0):
    """Closed box surface with outward normals (convex: exact visibility test)."""
    rng = np.random.default_rng(seed)
    p = rng.uniform(-.5, .5, size=(n, 3)) * SIZE
    axis = rng.integers(0, 3, n); sign = rng.choice([-1., 1.], n)
    p[np.arange(n), axis] = sign * SIZE[axis] / 2
    normal = np.zeros((n, 3)); normal[np.arange(n), axis] = sign
    return p, normal


def camera(azimuth, target=(0., 0., 0.), distance=2., elevation=.4):
    target = np.asarray(target, float)
    eye = target + distance * np.array([np.cos(azimuth) * np.cos(elevation), np.sin(azimuth) * np.cos(elevation),
                                        np.sin(elevation)])
    forward = (target - eye) / np.linalg.norm(target - eye)
    right = np.cross(forward, [0, 0, 1.]); right /= np.linalg.norm(right)
    down = np.cross(forward, right)
    w2c = np.eye(4); w2c[:3, :3] = np.stack([right, down, forward]); w2c[:3, 3] = -w2c[:3, :3] @ eye
    return dict(world_to_camera=w2c.tolist(), intrinsics=[250., 250., 228., 128.], image_size=[456, 256]), eye


def view(azimuth, offset=(0., 0., 0.), target=None):
    p, n = box_surface()
    p = p + np.asarray(offset)
    cam, eye = camera(azimuth, np.asarray(offset) if target is None else target)
    visible = np.sum(n * (eye - p), axis=1) > 0
    return p[visible][:1500], cam


class Controlled:
    def __init__(self):
        self.deny = set()

    def __call__(self, a, b):
        if self.deny and len(b) and self.deny.pop():
            return Verification(1e9, 'controlled-denial')
        return Verification(float((cKDTree(a).query(b)[0].mean() + cKDTree(b).query(a)[0].mean()) / 2), 'controlled-test')


POSITION = PositionConfig(minimum_consistency=.6, depth_margin=.25, silhouette_radius_factor=2.,
                          minimum_projected_points=32, reference_views=3,
                          selection_provenance='synthetic-test-only')


class PositionStateTests(unittest.TestCase):
    def setUp(self):
        self.cfg = config(voxel_size=.01, decay_half_life=100., confirmation_weight=1.5,
                          maximum_predicted_error=10., minimum_neighbors=1, outlier_radius=.05,
                          maximum_pending_states=4, maximum_cells=100000, fuse_after_motion=True)
        self.verifier = Controlled()

    def memory(self):
        return PositionStateMemory('V', '0', self.cfg, self.verifier, position_config=POSITION)

    def obs(self, i, azimuth, offset=(0., 0., 0.), **changes):
        p, cam = view(azimuth, offset)
        return replace(SceneObservation(f'k{i}', i, float(i), p, True, 'unknown', '', camera=cam), **changes)

    def test_projection_and_score_semantics(self):
        p, cam = view(0.)
        u, v, z, inside = Camera(cam).project(p)
        self.assertTrue(inside.all() and (z > 0).all())
        back, back_cam = view(np.pi)
        same, _ = consistency(back, p, Camera(cam), .05, 2., 32)
        moved, _ = consistency(back + [.6, 0, 0], p, Camera(cam), .05, 2., 32)
        self.assertGreater(same, .9)      # unseen side lies behind the visible surface
        self.assertLess(moved, .3)

    def test_other_side_same_state_new_position_new_state(self):
        m = self.memory()
        m.update(self.obs(1, 0.)); e = m.update(self.obs(2, 2.6))
        self.assertFalse(e['created_hypothesis']); self.assertEqual(len(m.states), 1)
        e = m.update(self.obs(3, 1., offset=(1., 0., 0.)))
        self.assertTrue(e['created_hypothesis']); self.assertEqual(len(m.states), 2)

    def test_motion_along_camera_ray_detected_by_reverse_test(self):
        m = self.memory(); first, cam = view(0.)
        m.update(SceneObservation('k1', 1, 1., first, True, 'unknown', '', camera=cam))
        eye = camera(0.)[1]
        closer, _ = view(0., offset=tuple(.5 * eye / np.linalg.norm(eye)), target=np.zeros(3))
        e = m.update(SceneObservation('k2', 2, 2., closer, True, 'unknown', '', camera=cam))
        test = e['position_tests'][0]
        self.assertGreater(test['forward'], .6)   # old surface hidden behind the closer object
        self.assertLess(min(test['reverse']), .3)  # but the old camera now sees it in free space
        self.assertTrue(e['created_hypothesis'])

    def test_rejected_view_stays_in_state_and_is_not_retried(self):
        m = self.memory(); m.update(self.obs(1, 0.)); e = m.update(self.obs(2, .3))
        self.assertEqual(e['status'], 'initialized_confirmed_shape'); before = m.cloud().copy()
        m.verifier.deny = {True}  # update() commits a deep copy: patch the live verifier
        e = m.update(self.obs(3, .6))
        self.assertEqual(e['status'], 'view_withheld_in_state'); self.assertFalse(e['created_hypothesis'])
        self.assertEqual(len(m.states), 1); np.testing.assert_array_equal(before, m.cloud())
        self.assertEqual(m.snapshot()['states']['k1']['withheld_keys'], ['k3'])
        e = m.update(self.obs(4, .9))
        self.assertEqual(e['fused_observation_keys'], ['k4']); self.assertEqual(m.fused_keys, ['k1', 'k2', 'k4'])
        self.assertEqual(m._views, {})

    def test_new_placement_registered_and_return_opens_new_state(self):
        m = self.memory(); m.update(self.obs(1, 0.)); m.update(self.obs(2, .3))
        m.update(self.obs(3, .2, offset=(1.2, 0., 0.)))
        e = m.update(self.obs(4, .5, offset=(1.2, 0., 0.)))
        self.assertTrue(e['promoted']); self.assertEqual(e['closed_states'], ['k1'])
        self.assertEqual(e['status'], 'fused_confirmed_state')
        e = m.update(self.obs(5, .1))
        self.assertTrue(e['created_hypothesis']); self.assertNotEqual(e['state_id'], 'k1')
        self.assertTrue(all(t['state_id'] != 'k1' for t in e['position_tests']))

    def test_camera_required_and_atomic(self):
        m = self.memory(); m.update(self.obs(1, 0.)); before = m.snapshot()
        with self.assertRaises(ValueError):
            m.update(self.obs(2, .3, camera=None))
        self.assertEqual(before, m.snapshot())
        with self.assertRaises(ValueError):
            PositionStateMemory('V', '0', self.cfg, self.verifier)

    def test_relative_resolution_fixed_at_first_valid_view(self):
        m = PositionStateMemory('V', '0', self.cfg, self.verifier, position_config=POSITION,
                                relative_resolution=(.04, .1))
        e = m.update(self.obs(1, 0.))
        r = e['resolution_radius']
        self.assertAlmostEqual(m.config.voxel_size, .04 * r); self.assertAlmostEqual(m.config.outlier_radius, .1 * r)
        m.update(self.obs(2, .3, offset=(.01, 0., 0.)))
        self.assertAlmostEqual(m.config.voxel_size, .04 * r)
        self.assertEqual(m.snapshot()['relative_resolution'], [.04, .1])

    def test_coordinator_entry(self):
        from frame_coordinator import FrameCoordinator
        from geometry_matcher import GeometryMatcher, GeometryConfig
        from test_frame_coordinator import tracker, inputs
        t = tracker(); t.matcher = GeometryMatcher(t.matcher.baseline, 'V', GeometryConfig('diagnostic', 'da_raw_points'))
        c = FrameCoordinator(t, PositionStateUpdater(self.cfg, self.verifier, position_config=POSITION))
        for i in range(2):
            args = inputs(i); key = args['observation_keys'][0]
            args['features'] = {key: None}
            args['geometry_inputs'] = {key: replace(self.obs(i, .3 * i), key=key)}
            result = c.step(**args)
        self.assertEqual(result['after']['geometry']['40']['value'].shape_version, 1)


if __name__ == '__main__':
    unittest.main()
