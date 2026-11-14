"""Reusable inference-only wrapper for the original Whareformer matcher.

No Torch import or copied inference/assignment code. A temporary model forward
hook supplies geometric logits to the original softmax and assignment. Instances
are scoped to one video and must not share a model or run concurrently.
"""
from dataclasses import asdict, dataclass

import numpy as np

from shape_adapter import FusionConfig, ShapeLogitAdapter
from shape_tools.memory import MemoryConfig


REPRESENTATIONS = ('da_raw_points', 'da_raw_superflex', 'moge_points', 'moge_superflex')


@dataclass(frozen=True)
class GeometryConfig:
    mode: str = 'disabled'
    representation: str = 'da_raw_superflex'
    capacity: int = 2
    metric: str = 'd2'
    reduction: str = 'minimum'
    weight: float = 0.0
    neutral_distance: float = 0.0

    def __post_init__(self):
        if self.mode not in ('disabled', 'diagnostic', 'active'):
            raise ValueError('Unknown geometry mode')
        if self.representation not in REPRESENTATIONS:
            raise ValueError('Unknown geometry representation')
        MemoryConfig(self.representation, self.capacity, self.metric, self.reduction)
        FusionConfig(self.weight, self.neutral_distance)
        if self.mode != 'active' and self.weight != 0:
            raise ValueError('Nonzero weight requires active mode')

    def to_dict(self):
        return asdict(self)


class GeometryMatcher:
    """Wrap an already constructed WhareformerMatcher without loading new weights.

    For enabled modes call set_frame before tracker.update; afterwards commit
    observation_key -> actual track_id, including IDs created by the tracker.
    Disabled mode delegates directly and requires no geometric inputs or commit.
    Features are precomputed tuples for config.representation, or None. This
    wrapper neither loads geometry nor registers/accumulates point clouds.
    """
    def __init__(self, baseline, video, config=GeometryConfig()):
        self.baseline, self.video, self.config = baseline, video, config
        self.geometry = ShapeLogitAdapter(
            video, MemoryConfig(config.representation, config.capacity, config.metric, config.reduction),
            FusionConfig(config.weight, config.neutral_distance))
        self._context = None
        self._pending = False
        self.last_score = None
        self.last_logits = None

    def set_frame(self, frame_index, observation_keys, features):
        if self.config.mode == 'disabled':
            raise RuntimeError('Disabled mode accepts no geometric context')
        if self._context is not None or self._pending:
            raise RuntimeError('Commit or abort the current frame first')
        keys = list(observation_keys)
        if type(frame_index) is not int or frame_index < 0:
            raise ValueError('A nonnegative integer frame index is required')
        if len(set(keys)) != len(keys) or set(keys) != set(features):
            raise ValueError('Unique keys must exactly match features in detection order')
        self._context = (frame_index, keys, dict(features))

    def match(self, tracks, detections, frame_metadata):
        if self.config.mode == 'disabled':
            return self.baseline.match(tracks, detections, frame_metadata)
        if self._pending or self._context is None:
            raise RuntimeError('Set one frame context before matching')
        frame, keys, features = self._context
        handle = None
        self.last_score = self.last_logits = None
        try:
            if frame != frame_metadata['frame_idx'] or len(keys) != len(detections):
                raise ValueError('Frame context must match actual metadata and detection order')
            ids = [str(t.track_id) for t in tracks]
            if len(ids) != len(set(ids)):
                raise ValueError('Actual track IDs must be unique')

            def score(logits):
                if self.last_score is not None:
                    raise RuntimeError('Expected exactly one model forward per match')
                self.last_logits = logits.copy()
                self.last_score = self.geometry.score(frame, keys, features, ids, logits)

            def hook(module, inputs, output):
                score(output.detach().cpu().numpy())
                # Preserve the original tensor object, dtype/device and arithmetic.
                if self.config.mode == 'diagnostic' or self.config.weight == 0:
                    return output
                return output.new_tensor(self.last_score['logits'])

            if not detections:
                # Explicit empty-frame extension: original feature construction
                # assumes at least one detection. No model inference is needed.
                score(np.zeros((0, len(tracks) + 1), dtype=np.float32))
                result = ([], list(range(len(tracks))), [], None)
            elif tracks:
                handle = self.baseline.model.register_forward_hook(hook)
                result = self.baseline.match(tracks, detections, frame_metadata)
            else:
                result = self.baseline.match(tracks, detections, frame_metadata)
                # Original matcher returns all detections as New Track without inference.
                score(np.zeros((len(detections), 1), dtype=np.float32))
            if self.last_score is None:
                raise RuntimeError('Original matcher did not call the expected model')
            self._pending = True
            self._context = None
            return result
        except Exception:
            self.abort()
            self.last_score = self.last_logits = None
            raise
        finally:
            if handle is not None:
                handle.remove()

    def commit(self, associations):
        if not self._pending:
            raise RuntimeError('Match a frame before committing')
        # Adapter validates all associations before mutation, allowing safe retry.
        self.geometry.commit(associations)
        self._pending = False

    def abort(self):
        self.geometry.abort()
        self._context = None
        self._pending = False

    def snapshot(self):
        return self.geometry.snapshot()
