"""Candidate NumPy boundary between baseline logits and causal shape memory.

Not a neural tracker: caller supplies baseline logits, observation features in
actual detection order and effective track IDs; commits after tracker updates.
Requires the existing shape_tools package. New Track is column zero.
"""
from dataclasses import dataclass

import numpy as np

from shape_tools.memory import ShapeMemory, MemoryConfig


@dataclass(frozen=True)
class FusionConfig:
    weight: float = 0.0
    neutral_distance: float = 0.0

    def __post_init__(self):
        if not np.isfinite(self.weight) or self.weight < 0:
            raise ValueError('Weight must be finite and nonnegative')
        if not np.isfinite(self.neutral_distance) or self.neutral_distance < 0:
            raise ValueError('Neutral distance must be finite and nonnegative')


class ShapeLogitAdapter:
    def __init__(self, video, memory_config: MemoryConfig, fusion=FusionConfig()):
        self.video = video
        self.memory = ShapeMemory(video, memory_config)
        self.fusion = fusion
        self.reconstructions = ShapeMemory(video, MemoryConfig(memory_config.representation, 1, memory_config.metric, memory_config.reduction))
        self._pending = False

    def score(self, frame_index, observation_keys, features, track_ids, baseline_logits):
        """Return copied logits + evidence. All queries precede a single commit.

        features must reference exactly observation_keys; keys explicitly carry
        row order, track_ids explicitly carry existing-track column order.
        Missing shape produces no direct correction. Other probabilities and
        assignments may still change through normalization and competition.
        """
        keys, ids = list(observation_keys), list(track_ids)
        if len(keys) != len(set(keys)) or set(features) != set(keys):
            raise ValueError('Observation keys must uniquely and exactly match features')
        original = np.asarray(baseline_logits)
        if (original.ndim != 2 or original.shape != (len(keys), len(ids) + 1)
                or original.dtype.kind != 'f' or not np.isfinite(original).all()):
            raise ValueError('Finite floating logits with columns [New Track, track_ids] required')
        scores = self.memory.score(self.video, frame_index, {k: features[k] for k in keys}, ids)
        corrected = original.copy()
        try:
            if self.reconstructions.snapshot():
                reconstructed = self.reconstructions.score(self.video, frame_index, {k: features[k] for k in keys}, ids)
                self.reconstructions.abort()
                mask = reconstructed['valid']
                scores['distances'][mask] = reconstructed['distances'][mask]
                scores['valid'][mask] = True
                scores['evidence'].update(reconstructed['evidence'])
            if self.fusion.weight:
                mask = scores['valid']
                existing = corrected[:, 1:]
                values = (existing[mask].astype(np.float64)
                          + self.fusion.weight * (self.fusion.neutral_distance - scores['distances'][mask]))
                if not np.isfinite(values).all():
                    raise ValueError('Nonfinite corrected logits')
                existing[mask] = values
                if not np.isfinite(corrected).all():
                    raise ValueError('Correction overflow for supplied dtype')
            self._pending = True
            return dict(logits=corrected, **scores)
        except Exception:
            self.abort()
            raise

    def commit(self, predicted_associations):
        """observation_key -> actual track_id, including IDs of newly spawned tracks."""
        self.memory.commit(predicted_associations)
        self._pending = False

    def abort(self):
        self.memory.abort()
        self.reconstructions.abort()
        self._pending = False

    def snapshot(self):
        return self.memory.snapshot()

    def publish_reconstructions(self, frame_index, results):
        """After frame commit only: track -> (request_id, validated feature tuple).

        Latest valid reconstruction supersedes separate-form distances for that
        track. Missing/failed results are omitted, preserving earlier geometry.
        Caller must bind results to this frame and cloud version before publishing.
        """
        return self._publish_track_features(frame_index, results, 'reconstruction')

    def publish_accumulated_points(self, frame_index, results):
        return self._publish_track_features(frame_index, results, 'accumulated_points')

    def _publish_track_features(self, frame_index, results, kind):
        if self._pending:
            raise RuntimeError('Commit the frame before publishing track features')
        if not results:
            return
        features = {f'{kind}/{rid}': feature for rid, feature in results.values()}
        if len(features) != len(results):
            raise ValueError('Reconstruction IDs must be unique')
        associations = {f'{kind}/{rid}': tid for tid, (rid, feature) in results.items()}
        try:
            self.reconstructions.score(self.video, frame_index, features, [])
            self.reconstructions.commit(associations)
        except Exception:
            self.reconstructions.abort()
            raise

    def reconstruction_snapshot(self):
        return self.reconstructions.snapshot()
