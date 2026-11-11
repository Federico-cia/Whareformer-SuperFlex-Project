import csv
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from shape_tools.comparison import FIELDS, atomic_output, compare
from shape_tools.evaluation import evaluate, separation
from shape_tools.geometry import (
    backproject,
    normalize_shape,
    paired_clouds,
    prepare_superflex_input,
)
from shape_tools.metrics import descriptors, icp_distance


class GeometryTests(unittest.TestCase):
    def test_perspective_and_common_pixels(self):
        depth = np.array([[1.0, 2.0], [np.nan, -1.0]])
        points = backproject(depth, [2, 4, 0, 0])
        np.testing.assert_array_equal(points[0, 1], [1, 0, 2])
        valid = np.ones((2, 2), bool)
        valid[0, 0] = False
        da, moge, pixels = paired_clouds(depth, [2, 4, 0, 0], points, np.ones((2, 2)), valid)
        np.testing.assert_array_equal(da, [[1, 0, 2]])
        np.testing.assert_array_equal(da, moge)
        np.testing.assert_array_equal(pixels, [[1, 0]])

    def test_superflex_sample_and_roundtrip(self):
        points = np.random.default_rng(7).normal(size=(200, 3))
        normalized, center, scale, indices = prepare_superflex_input(points)
        self.assertEqual(normalized.shape, (4096, 3))
        self.assertLessEqual(np.abs(normalized).max(), 0.5)
        np.testing.assert_allclose(normalized * scale + center, points[indices])
        np.testing.assert_array_equal(indices, prepare_superflex_input(points)[3])
        for invalid in [np.zeros((8, 3)), np.full((8, 3), np.nan), np.ones((3, 3))]:
            with self.assertRaises(ValueError):
                prepare_superflex_input(invalid)

    def test_shape_invariance_and_registration_symmetry(self):
        rng = np.random.default_rng(75)
        points = rng.normal(size=(80, 3)) * [3, 1, 0.3]
        rotation, _ = np.linalg.qr(rng.normal(size=(3, 3)))
        if np.linalg.det(rotation) < 0:
            rotation[:, -1] *= -1
        a = normalize_shape(points)
        b = normalize_shape(2.7 * points @ rotation + [10, 3, -4])
        for original, transformed in zip(descriptors(a), descriptors(b), strict=True):
            np.testing.assert_allclose(original, transformed, atol=1e-12)
        self.assertLess(icp_distance(a, b), 1e-8)
        other = normalize_shape(rng.normal(size=(80, 3)))
        self.assertAlmostEqual(icp_distance(a, other), icp_distance(other, a), places=12)


class WorkflowTests(unittest.TestCase):
    def test_atomic_failure_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "result.csv"
            with self.assertRaisesRegex(RuntimeError, "interrupted"):
                with atomic_output(path) as stream:
                    stream.write("partial")
                    raise RuntimeError("interrupted")
            self.assertEqual(list(Path(folder).iterdir()), [])
            with atomic_output(path) as stream:
                stream.write("complete")
            with self.assertRaises(FileExistsError), atomic_output(path):
                pass
            self.assertEqual(path.read_text(), "complete")

    def test_compare_missing_output_and_same_frame_exclusion(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            np.savez(
                root / "cloud.npz", camera_points=np.random.default_rng(9).normal(size=(128, 3))
            )
            observations = [
                dict(
                    observation_key=key,
                    video="v",
                    rgb_frame=frame,
                    category="plate",
                    representations={
                        "points": dict(status="ready", path="cloud.npz"),
                        "surface": dict(status="unavailable"),
                    },
                )
                for key, frame in [("a", "1"), ("b", "1"), ("c", "2")]
            ]
            manifest = root / "observations.json"
            manifest.write_text(json.dumps(observations))
            self.assertEqual(compare(manifest, root, root / "distances.csv"), 2)
            with (root / "distances.csv").open(newline="") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows), 4)
            self.assertEqual(sum(r["status"] == "unavailable" for r in rows), 2)
            self.assertTrue(
                all(float(r["d2_wasserstein"]) == 0 for r in rows if r["status"] == "ready")
            )

    def test_auc_ties_and_no_negatives(self):
        self.assertEqual(separation([1, 1], [1, 1])["auc"], 0.5)
        self.assertEqual(separation([0, 1], [2, 3])["auc"], 1)
        self.assertIsNone(separation([1], [])["auc"])

    def test_evaluation_separates_categories_and_rejects_duplicates(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            review = root / "review.csv"
            labels = [
                dict(
                    observation_key=key,
                    video="v",
                    rgb_frame=key,
                    category=category,
                    physical_identity=identity,
                    identity_status="visually_verified",
                    evidence="review",
                )
                for key, category, identity in [
                    ("a", "plate", "p"),
                    ("b", "plate", "p"),
                    ("c", "plate", "q"),
                    ("d", "knife", "k"),
                ]
            ]
            with review.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(labels[0]))
                writer.writeheader()
                writer.writerows(labels)
            rows = [
                dict(
                    pair_id=index,
                    video="v",
                    left=left,
                    right=right,
                    representation="points",
                    same_category=right != "d",
                    status="ready",
                    d2_wasserstein=score,
                    covariance_spectrum_l2=score,
                )
                for index, (left, right, score) in enumerate(
                    [("a", "b", 0.1), ("a", "c", 0.4), ("b", "c", 0.5), ("a", "d", 0.01)]
                )
            ]
            distances = root / "distances.csv"
            with distances.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            result = evaluate(distances, review, root / "evaluation.json")
            score = result["by_video"]["v"]["plate"]["points"]["d2_wasserstein"]
            self.assertEqual(score["auc"], 1)
            self.assertEqual(score["different_pairs"], 2)
            with distances.open("a", newline="") as stream:
                csv.DictWriter(stream, fieldnames=FIELDS).writerow(rows[0])
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                evaluate(distances, review, root / "invalid.json")


if __name__ == "__main__":
    unittest.main()
