"""Scene updater + actual original tracker.update with controlled model tensors."""
from copy import deepcopy
import unittest
import numpy as np
from frame_coordinator import FrameCoordinator, UpdateContext
from geometry_matcher import GeometryMatcher, GeometryConfig
from scene_memory import SceneMemoryUpdater
from test_frame_coordinator import tracker, inputs
from test_scene_memory import config, obs, ControlledVerifier


class SceneCoordinatorTests(unittest.TestCase):
    def coordinator(self, verifier=None):
        t = tracker()
        t.matcher = GeometryMatcher(t.matcher.baseline, 'V', GeometryConfig('diagnostic', 'da_raw_points'))
        return FrameCoordinator(t, SceneMemoryUpdater(config(), verifier))

    def step(self, coordinator, i, **changes):
        args = inputs(i)
        args['features'] = {k: None for k in args['observation_keys']}
        key = args['observation_keys'][0]
        args['geometry_inputs'] = {key: obs(i, key=key, **changes)}
        return coordinator.step(**args)

    def test_pending_commits_but_shape_advances_only_after_confirmation(self):
        c = self.coordinator(ControlledVerifier())
        a = self.step(c, 0)
        self.assertEqual(a['assignments'], {'V/f0/d0': '40'})
        self.assertEqual(a['updates'][0]['diagnostics']['status'], 'pending_confirmation')
        self.assertEqual(a['after']['geometry']['40']['value'].shape_version, 0)
        b = self.step(c, 1)
        self.assertEqual(b['updates'][0]['diagnostics']['status'], 'fused_stationary')
        self.assertEqual(b['after']['geometry']['40']['value'].shape_version, 1)
        self.assertEqual(a['after']['geometry']['40']['value'].shape_version, 0)
        self.assertEqual(b['after']['reconstructions'], {})

    def test_updater_is_pure_scope_and_prior_version_are_enforced(self):
        updater = SceneMemoryUpdater(config(), ControlledVerifier())
        item = obs(0)
        first = updater(UpdateContext('V', 'da_raw_points', 0, item.key, '40', item, None))
        before = first.value.snapshot()
        prior = dict(version=1, value=first.value)
        second = updater(UpdateContext('V', 'da_raw_points', 1, 'obs1', '40', obs(1), prior))
        self.assertEqual(first.value.snapshot(), before)
        self.assertTrue(second.diagnostics['shape_changed'])
        with self.assertRaises(ValueError):
            updater(UpdateContext('V', 'da_raw_points', 1, 'obs1', 'other', obs(1), prior))
        with self.assertRaises(ValueError):
            updater(UpdateContext('V', 'da_raw_points', 1, 'obs1', '40', obs(1), dict(version=7, value=first.value)))

    def test_missing_staticity_does_not_change_tracker_association_or_shape(self):
        c = self.coordinator(ControlledVerifier())
        self.step(c, 0); self.step(c, 1)
        before = c.snapshot()['geometry']['40']['value'].cloud()
        result = self.step(c, 2, staticity='unknown')
        self.assertEqual(result['assignments'], {'V/f2/d0': '40'})
        np.testing.assert_array_equal(result['after']['geometry']['40']['value'].cloud(), before)

    def test_legacy_reconstructor_rejected_before_tracker_mutation(self):
        t = tracker()
        with self.assertRaisesRegex(ValueError, 'FPS'):
            FrameCoordinator(t, SceneMemoryUpdater(config()), reconstructor=object())
        self.assertEqual(t.tracks, [])


if __name__ == '__main__':
    unittest.main()
