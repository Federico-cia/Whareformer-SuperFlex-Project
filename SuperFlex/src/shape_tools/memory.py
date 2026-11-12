"""Candidate causal FIFO shape memory, independent of tracking and identity labels."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class MemoryConfig:
    representation: str
    capacity: int = 1
    metric: str = "d2"
    reduction: str = "minimum"

    def __post_init__(self):
        if (
            not self.representation
            or type(self.capacity) is not int
            or self.capacity < 1
            or self.metric not in ("d2", "spectrum")
            or self.reduction not in ("minimum", "mean")
        ):
            raise ValueError("Invalid memory configuration")


class ShapeMemory:
    """One video per instance. Query all detections before committing associations.

    Features are (normalized points, sorted D2 samples, covariance spectrum),
    as returned by comparison.load_features. None means unavailable. This module
    does not select tracks, use identity annotations, or modify baseline logits.
    """

    def __init__(self, video, config):
        if not video:
            raise ValueError("A video scope is required")
        self.video, self.config = video, config
        self._tracks = {}
        self._last_frame = -1
        self._pending = None
        self._seen = set()
        self._descriptor_size = None

    def _feature(self, feature):
        if feature is None:
            return None
        value = np.asarray(feature[1 if self.config.metric == "d2" else 2], dtype=float)
        if value.ndim != 1 or not len(value) or not np.isfinite(value).all() or (value < 0).any():
            raise ValueError("Invalid descriptor")
        if self.config.metric == "spectrum" and value.shape != (3,):
            raise ValueError("Spectrum must have three values")
        if self.config.metric == "d2" and (np.diff(value) < 0).any():
            raise ValueError("D2 samples must be sorted")
        return value.copy()

    def score(self, video, frame_index, observations, track_ids):
        """Open one frame transaction and return distances plus explicit validity.

        observations maps unique observation keys to features or None. Input
        track order is preserved. Missing distances are NaN and valid=False;
        callers must use the mask and leave baseline scores neutral there.
        """
        if self._pending is not None:
            raise RuntimeError("Commit or abort the pending frame first")
        if (
            video != self.video
            or not isinstance(frame_index, int)
            or frame_index <= self._last_frame
        ):
            raise ValueError("Video mismatch or noncausal frame order")
        track_ids = list(track_ids)
        if len(track_ids) != len(set(track_ids)) or any(
            not isinstance(t, str) or not t for t in track_ids
        ):
            raise ValueError("Track identifiers must be unique nonempty strings")
        if any(not isinstance(k, str) or not k or k in self._seen for k in observations):
            raise ValueError("Invalid or previously committed observation key")
        features = {key: self._feature(value) for key, value in observations.items()}
        sizes = {len(f) for f in features.values() if f is not None}
        if self._descriptor_size is not None:
            sizes.add(self._descriptor_size)
        if len(sizes) > 1:
            raise ValueError("Descriptor dimensions differ")
        keys = list(features)
        distances = np.full((len(keys), len(track_ids)), np.nan)
        evidence = {}
        for i, key in enumerate(keys):
            feature = features[key]
            if feature is None:
                continue
            for j, track in enumerate(track_ids):
                entries = self._tracks.get(track, [])
                if not entries:
                    continue
                values = [
                    float(np.mean(np.abs(feature - e["feature"])))
                    if self.config.metric == "d2"
                    else float(np.linalg.norm(feature - e["feature"]))
                    for e in entries
                ]
                distances[i, j] = (
                    min(values) if self.config.reduction == "minimum" else np.mean(values)
                )
                evidence[key, track] = tuple(e["observation_key"] for e in entries)
        self._pending = (frame_index, features, next(iter(sizes), self._descriptor_size))
        return dict(
            observation_keys=keys,
            track_ids=track_ids,
            distances=distances,
            valid=np.isfinite(distances),
            evidence=evidence,
        )

    def commit(self, associations):
        """Commit externally predicted one-to-one observation -> track assignments.

        Unassigned observations are omitted. Missing shapes leave earlier valid
        memory intact. All validation precedes mutation, permitting safe retry.
        """
        if self._pending is None:
            raise RuntimeError("Score the current frame before committing")
        frame, features, size = self._pending
        tracks = list(associations.values())
        if (
            any(key not in features for key in associations)
            or any(not isinstance(t, str) or not t for t in tracks)
            or len(tracks) != len(set(tracks))
        ):
            raise ValueError("Assignments must be one-to-one and reference current observations")
        for key, track in associations.items():
            if features[key] is not None:
                entries = self._tracks.setdefault(track, [])
                entries.append(dict(observation_key=key, frame_index=frame, feature=features[key]))
                del entries[: -self.config.capacity]
        self._seen.update(features)
        self._descriptor_size = size
        self._last_frame = frame
        self._pending = None

    def abort(self):
        self._pending = None

    def forget(self, track_id):
        if self._pending is not None:
            raise RuntimeError("Cannot remove a track during a frame transaction")
        self._tracks.pop(track_id, None)

    def snapshot(self):
        return {
            track: [
                dict(observation_key=e["observation_key"], frame_index=e["frame_index"])
                for e in entries
            ]
            for track, entries in self._tracks.items()
        }


def observation_features(observation, root, representation):
    """Read one exported representation with mandatory content verification."""
    from pathlib import Path

    from .comparison import file_hash, load_features

    info = observation["representations"][representation]
    if info["status"] == "unavailable":
        return None
    if info["status"] != "ready" or not info.get("sha256"):
        raise ValueError("Invalid geometry status or missing checksum")
    root = Path(root).resolve()
    path = (root / info["path"]).resolve()
    if not path.is_relative_to(root) or file_hash(path) != info["sha256"]:
        raise ValueError("Artifact path or checksum invalid")
    return load_features(path)
