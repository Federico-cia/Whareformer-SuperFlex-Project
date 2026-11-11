"""Compute paired distances from existing per-observation clouds and meshes."""

import csv
import hashlib
import itertools
import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import trimesh

from .geometry import normalize_shape
from .metrics import descriptors, icp_distance

METRICS = ("d2_wasserstein", "covariance_spectrum_l2", "multistart_icp_chamfer")
FIELDS = (
    "pair_id",
    "video",
    "left",
    "right",
    "representation",
    "same_category",
    "status",
    *METRICS,
)


def file_hash(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


@contextmanager
def atomic_output(path):
    path = Path(path)
    if path.exists():
        raise FileExistsError(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
            yield stream
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def load_features(path, count=1024, seed=20261109):
    path = Path(path)
    if path.suffix == ".npz":
        with np.load(path, allow_pickle=False) as data:
            points = data["camera_points"].copy()
        indices = np.random.default_rng(seed).choice(
            len(points), count, replace=len(points) < count
        )
        points = points[indices]
    elif path.suffix == ".ply":
        mesh = trimesh.load(path, process=False)
        points, _ = trimesh.sample.sample_surface(mesh, count, seed=seed)
    else:
        raise ValueError(f"Unsupported geometry file: {path.suffix}")
    points = normalize_shape(points)
    d2, spectrum = descriptors(points, seed=seed)
    return points, d2, spectrum


def compare(manifest, root, output, registration=False):
    manifest, root, output = Path(manifest), Path(root), Path(output)
    if output.exists() or output.with_suffix(".meta.json").exists():
        raise FileExistsError(output)
    observations = sorted(
        json.loads(manifest.read_text(encoding="utf-8-sig")), key=lambda r: r["observation_key"]
    )
    keys = [r["observation_key"] for r in observations]
    if len(keys) != len(set(keys)) or not observations:
        raise ValueError("Expected nonempty observations with unique keys")
    representations = sorted(observations[0]["representations"])
    features, hashes = {}, {}
    for row in observations:
        if sorted(row["representations"]) != representations:
            raise ValueError("Representation names differ between observations")
        for name, info in row["representations"].items():
            if info["status"] != "ready":
                continue
            path = root / info["path"]
            digest = file_hash(path)
            if info.get("sha256") and digest != info["sha256"]:
                raise ValueError(f"Geometry checksum mismatch: {row['observation_key']}/{name}")
            features[row["observation_key"], name] = load_features(path)
            hashes[f"{row['observation_key']}/{name}"] = digest
    pair_count = 0
    with atomic_output(output) as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        for left, right in itertools.combinations(observations, 2):
            if left["video"] != right["video"] or left["rgb_frame"] == right["rgb_frame"]:
                continue
            for name in representations:
                result = dict(
                    pair_id=pair_count,
                    video=left["video"],
                    left=left["observation_key"],
                    right=right["observation_key"],
                    representation=name,
                    same_category=left["category"] == right["category"],
                    status="unavailable",
                )
                a, b = (
                    features.get((left["observation_key"], name)),
                    features.get((right["observation_key"], name)),
                )
                if a is not None and b is not None:
                    result.update(
                        status="ready",
                        d2_wasserstein=float(np.mean(np.abs(a[1] - b[1]))),
                        covariance_spectrum_l2=float(np.linalg.norm(a[2] - b[2])),
                    )
                    if registration:
                        result[METRICS[2]] = icp_distance(a[0][::2], b[0][::2])
                writer.writerow(result)
            pair_count += 1
    metadata = dict(
        manifest_sha256=file_hash(manifest),
        geometry_sha256=hashes,
        pairs=pair_count,
        points=1024,
        d2_pairs=16384,
        seed=20261109,
        registration=registration,
        normalization="centroid and RMS radius, independently per representation",
    )
    with atomic_output(output.with_suffix(".meta.json")) as stream:
        json.dump(metadata, stream, indent=2, allow_nan=False)
    return pair_count
