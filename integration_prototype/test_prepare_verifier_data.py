import unittest
import numpy as np
from prepare_verifier_data import make_example
from scene_geometry import transform


class KnownTransformDataTests(unittest.TestCase):
    def setUp(self):
        self.points = np.random.default_rng(3).normal(size=(300, 3)) * [1, .6, .2]

    def test_correct_pose_stays_zero_under_cropping_and_noise(self):
        e = make_example(self.points, np.random.default_rng(4), angle_deg=0,
                         translation_rms=0, noise_rms=.01)
        self.assertEqual(e['error'], 0)
        self.assertGreater(np.linalg.norm(e['features']), 0)
        np.testing.assert_allclose(e['estimate'] @ np.linalg.inv(e['ground_truth']),
                                   np.eye(4), atol=1e-12)

    def test_motion_inverse_and_error_target(self):
        e = make_example(self.points, np.random.default_rng(5), angle_deg=20,
                         translation_rms=.15, noise_rms=0)
        normalized = (self.points - e['center']) / e['radius']
        aligned_correct = transform(e['source'], e['ground_truth'])
        np.testing.assert_allclose(aligned_correct, normalized[e['source_indices']], atol=1e-12)
        np.testing.assert_allclose(e['aligned_source'],
            transform(normalized[e['source_indices']], e['residual']), atol=1e-12)
        self.assertGreater(e['error'], 0)

    def test_target_invariant_to_units_and_origin(self):
        kwargs = dict(angle_deg=5, translation_rms=.03, noise_rms=.01)
        a = make_example(self.points, np.random.default_rng(7), **kwargs)
        b = make_example(self.points * 50 + [100, -10, 2], np.random.default_rng(7), **kwargs)
        self.assertAlmostEqual(a['error'], b['error'], places=12)
        np.testing.assert_allclose(a['features'], b['features'], atol=1e-12)


if __name__ == '__main__':
    unittest.main()
