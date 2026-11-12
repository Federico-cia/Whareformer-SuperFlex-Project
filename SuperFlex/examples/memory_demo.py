"""Executable synthetic API example; assignments below are illustrative, not tracking."""

import numpy as np

from shape_tools.geometry import normalize_shape
from shape_tools.memory import MemoryConfig, ShapeMemory
from shape_tools.metrics import descriptors

rng = np.random.default_rng(7)
points = normalize_shape(rng.normal(size=(1024, 3)) * [3, 1, 0.5])
features = (points, *descriptors(points))
memory = ShapeMemory("example_video", MemoryConfig("da_points", capacity=2))
first = memory.score("example_video", 1, {"first": features}, [])
memory.commit({"first": "external_track_1"})
second = memory.score(
    "example_video", 2, {"current": features, "missing": None}, ["external_track_1"]
)
print("Distances:", second["distances"].tolist())
print("Availability:", second["valid"].tolist())
print("Only past observations:", second["evidence"])
memory.commit({"current": "external_track_1", "missing": "external_track_2"})
print("Memory:", memory.snapshot())
