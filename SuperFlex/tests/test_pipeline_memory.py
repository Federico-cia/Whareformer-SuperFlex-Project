import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from shape_tools.memory import MemoryConfig, ShapeMemory, observation_features
from shape_tools.pipeline import cached, clouds, export, item_id, run_item, save_json


def feature(value):
    return None, np.array([value, value + 1.0]), np.array([value, 1.0, 0.0])


class MemoryTests(unittest.TestCase):
    def test_causality_missing_fifo_and_scope(self):
        m = ShapeMemory("v", MemoryConfig("da_points", capacity=2))
        r = m.score("v", 1, {"a": feature(0)}, ["t"])
        self.assertFalse(r["valid"].any())
        with self.assertRaises(RuntimeError):
            m.score("v", 2, {}, [])
        m.commit({"a": "t"})
        r = m.score("v", 2, {"b": feature(2), "missing": None}, ["t", "unknown"])
        self.assertEqual(r["distances"][0, 0], 2.0)
        self.assertFalse(r["valid"][1].any())
        self.assertEqual(r["evidence"]["b", "t"], ("a",))
        m.commit({"missing": "t"})
        self.assertEqual(m.snapshot()["t"][0]["observation_key"], "a")
        for frame in (3, 4):
            m.score("v", frame, {str(frame): feature(frame)}, ["t"])
            m.commit({str(frame): "t"})
        self.assertEqual([e["observation_key"] for e in m.snapshot()["t"]], ["3", "4"])
        for video, frame in [("v", 4), ("other", 5)]:
            with self.assertRaises(ValueError):
                m.score(video, frame, {}, [])

    def test_transaction_validation_and_copy(self):
        m = ShapeMemory("v", MemoryConfig("moge_superflex"))
        f = feature(0)
        m.score("v", 1, {"a": f, "b": feature(2)}, [])
        f[1][:] = 99
        with self.assertRaises(ValueError):
            m.commit({"a": "t", "b": "t"})
        self.assertEqual(m.snapshot(), {})
        m.commit({"a": "t"})
        r = m.score("v", 2, {"c": feature(0)}, ["t"])
        self.assertEqual(r["distances"][0, 0], 0)
        m.abort()
        with self.assertRaises(ValueError):
            m.score("v", 2, {"a": feature(0)}, [])


class PipelineTests(unittest.TestCase):
    def test_resume_detects_corruption_and_signature(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)

            def producer(dest):
                (dest / "data").write_text("ok")
                return {"data": dest / "data"}, {}

            first = run_item(root, root / "item", "one", producer)
            self.assertEqual(cached(root / "item", "one"), first)
            with self.assertRaises(ValueError):
                cached(root / "item", "two")
            (root / "item/data").write_text("corrupted")
            with self.assertRaises(ValueError):
                cached(root / "item", "one")

    def test_common_pixels_export_and_missing(self):
        from PIL import Image

        from shape_tools.pipeline import artifact

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            Image.fromarray(np.zeros((4, 4, 3), dtype=np.uint8)).save(root / "rgb.png")
            Image.fromarray(np.ones((4, 4), dtype=np.uint8)).save(root / "mask.png")
            row = dict(
                observation_key="v/a",
                video="v",
                frame_index=1,
                rgb=str(root / "rgb.png"),
                mask=str(root / "mask.png"),
                intrinsics=[4, 4, 2, 2],
                category="object",
            )
            data = dict(observations=[row])
            cfg = dict(sources=["da", "moge"], clouds=dict(pixel_policy="common", minimum_points=4))
            depth = np.ones((4, 4))
            from shape_tools.geometry import backproject

            valid = np.ones((4, 4), bool)
            valid[0, 0] = False
            np.savez(root / "da.npz", depth=depth)
            np.savez(root / "moge.npz", points=backproject(depth, row["intrinsics"]), mask=valid)
            for source in cfg["sources"]:
                save_json(
                    root / f"{source}_index.json",
                    {
                        item_id(row): dict(
                            status="ready",
                            artifacts={"prediction": artifact(root, root / f"{source}.npz")},
                        )
                    },
                )
            clouds(data, root, cfg)
            for source in cfg["sources"]:
                index = json.loads((root / f"clouds_{source}_index.json").read_text())
                self.assertEqual(index[item_id(row)]["points"], 15)
                save_json(
                    root / f"superflex_{source}_index.json",
                    {
                        item_id(row): dict(
                            status="failed", signature="missing", error="no primitives"
                        )
                    },
                )
            observations = export(data, root, cfg)
            self.assertIsNone(observations[0]["detection_idx"])
            self.assertIsNone(observation_features(observations[0], root, "moge_superflex"))
            self.assertEqual(
                observation_features(observations[0], root, "da_points")[0].shape, (1024, 3)
            )


if __name__ == "__main__":
    unittest.main()
