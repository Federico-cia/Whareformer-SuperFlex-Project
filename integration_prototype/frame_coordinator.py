"""Serial frame orchestration; no neural inference or registration implementation.

All frame queries precede every geometric update. Optional geometric updaters
must be pure: they receive detached copies and return a proposal, never mutate
the tracker or perform external writes. This interface does not certify poses.
"""
from copy import deepcopy
from dataclasses import dataclass, field
from numbers import Integral

import numpy as np

from geometry_matcher import GeometryMatcher


@dataclass(frozen=True)
class GeometryDecision:
    accepted: bool
    value: object = None
    reasons: tuple = ()
    diagnostics: dict = field(default_factory=dict)


@dataclass(frozen=True)
class UpdateContext:
    video: str
    representation: str
    frame_index: int
    observation_key: str
    track_id: str
    observation: object
    previous: object


class FrameCoordinator:
    """Own a fresh tracker with GeometryMatcher for exactly one video.

    Current features update the separate-form memory after association. Optional
    geometry_updater handles additional geometric state; accepted results do NOT
    automatically replace matching descriptors (SuperFlex connection is later).
    A core tracker/commit error poisons this instance: reconstruct and replay;
    abort alone cannot undo original track mutations. Updater failures instead
    preserve the old valid geometric state and are logged per observation.
    """
    def __init__(self, tracker, geometry_updater=None, reconstructor=None):
        if not isinstance(tracker.matcher, GeometryMatcher):
            raise TypeError('A GeometryMatcher wrapper is required')
        matcher = tracker.matcher
        if tracker.tracks or matcher.snapshot() or matcher.geometry.reconstruction_snapshot() or matcher._context is not None or matcher._pending:
            raise ValueError('Use a fresh tracker and matcher for a new coordinator')
        if geometry_updater is not None and not callable(geometry_updater):
            raise TypeError('geometry_updater must be callable')
        if reconstructor is not None and (matcher.config.mode == 'disabled'
                or not matcher.config.representation.endswith('_superflex') or geometry_updater is None):
            raise ValueError('Reconstruction requires enabled SuperFlex representation and cloud updater')
        self.reconstructor = reconstructor
        self._pending_reconstructions = []
        self.tracker, self.matcher = tracker, matcher
        self.geometry_updater = geometry_updater
        self._last_frame = -1
        self._last_timestamp = None
        self._seen = set()
        self._shape_versions = {}
        self._geometry_versions = {}
        self._failed = False
        self._busy = False

    def snapshot(self):
        return deepcopy(dict(video=self.matcher.video, last_frame=self._last_frame,
                             failed=self._failed, shapes=self._shape_versions,
                             pending_reconstructions=self._pending_reconstructions,
                             reconstructions=self.matcher.geometry.reconstruction_snapshot(),
                             geometry=self._geometry_versions,
                             separate_shape_memory=self.matcher.snapshot()))

    def step(self, detections, metadata, observation_keys, features=None, geometry_inputs=None):
        if self._failed:
            raise RuntimeError('Core failure: rebuild tracker/coordinator and replay')
        if self._pending_reconstructions:
            raise RuntimeError('Resolve deferred SuperFlex results before the next frame')
        if self._busy:
            raise RuntimeError('Concurrent or reentrant frame processing is forbidden')
        detections, keys = list(detections), list(observation_keys)
        frame, timestamp = metadata['frame_idx'], metadata['timestamp']
        if (type(frame) is not int or frame <= self._last_frame
                or not np.isfinite(timestamp)
                or self._last_timestamp is not None and timestamp <= self._last_timestamp):
            raise ValueError('Strictly increasing frame index and timestamp required')
        if (len(keys) != len(detections) or len(set(keys)) != len(keys)
                or any(not isinstance(k, str) or not k or k in self._seen for k in keys)):
            raise ValueError('Unique unused observation keys in actual detection order required')
        for i, detection in enumerate(detections):
            data = detection.detection_data
            if data['frame'] != frame or data['detection_idx'] != i:
                raise ValueError('Detection frame/index must match metadata and row order')
        features = {key: None for key in keys} if features is None else deepcopy(features)
        geometry_inputs = {} if geometry_inputs is None else deepcopy(geometry_inputs)
        if set(features) != set(keys) or not set(geometry_inputs) <= set(keys):
            raise ValueError('Feature/input keys must refer to this frame only')
        if self.matcher.config.mode == 'disabled' and (any(v is not None for v in features.values()) or geometry_inputs):
            raise ValueError('Disabled mode accepts no geometric features/inputs')
        old_lengths = {str(t.track_id): len(t.history) for t in self.tracker.tracks}
        if len(old_lengths) != len(self.tracker.tracks):
            raise ValueError('Track IDs must be unique')
        previous = self.snapshot()
        enabled = self.matcher.config.mode != 'disabled'
        self._busy = True
        try:
            if enabled:
                self.matcher.set_frame(frame, keys, features)
            if not detections and not enabled:
                # Baseline has no empty-detection input path; only age tracks.
                for track in self.tracker.tracks:
                    track.increase_age(timestamp)
                training_data = None
            else:
                training_data = self.tracker.update(detections, metadata)
            assignments = {}
            for track in self.tracker.tracks:
                tid = str(track.track_id)
                old_length = old_lengths.get(tid, 0)
                if len(track.history) == old_length:
                    continue
                if len(track.history) != old_length + 1:
                    raise RuntimeError('Unexpected track history mutation')
                row = track.history[-1]
                idx = row['detection_idx']
                if (not isinstance(idx, Integral) or idx < 0 or idx >= len(keys)
                        or row['frame'] != frame or keys[idx] in assignments):
                    raise RuntimeError('Invalid actual detection-to-track association')
                assignments[keys[idx]] = tid
            if set(assignments) != set(keys) or len(set(assignments.values())) != len(assignments):
                raise RuntimeError('Original tracker must assign every detection one-to-one')
            if enabled:
                self.matcher.commit(assignments)
                for key, tid in assignments.items():
                    if features[key] is not None:
                        old = self._shape_versions.get(tid, {})
                        self._shape_versions[tid] = dict(version=old.get('version', 0)+1,
                                                        frame_index=frame, observation_key=key)
            events = []
            proposed_versions = {}
            for key in keys:
                tid = assignments[key]
                value = geometry_inputs.get(key)
                if not enabled or self.geometry_updater is None:
                    events.append(dict(observation_key=key, track_id=tid, status='not_requested'))
                    continue
                if value is None:
                    events.append(dict(observation_key=key, track_id=tid, status='missing'))
                    continue
                # All proposals receive pre-frame state, never another proposal.
                old = previous['geometry'].get(tid)
                try:
                    context = UpdateContext(self.matcher.video, self.matcher.config.representation,
                                            frame, key, tid, value, deepcopy(old))
                    decision = self.geometry_updater(context)
                    if (not isinstance(decision, GeometryDecision) or type(decision.accepted) is not bool
                            or not isinstance(decision.reasons, tuple)
                            or any(not isinstance(r, str) for r in decision.reasons)
                            or not isinstance(decision.diagnostics, dict)
                            or decision.accepted and decision.value is None):
                        raise ValueError('Invalid geometric proposal')
                    diagnostics = deepcopy(decision.diagnostics)
                    if decision.accepted:
                        accepted_value = deepcopy(decision.value)
                        proposed_versions[tid] = dict(version=1 if old is None else old['version']+1,
                                                           frame_index=frame, observation_key=key, value=accepted_value)
                    events.append(dict(observation_key=key, track_id=tid,
                                       status='accepted' if decision.accepted else 'rejected',
                                       reasons=list(decision.reasons), diagnostics=diagnostics))
                except Exception as error:
                    events.append(dict(observation_key=key, track_id=tid, status='error',
                                       reasons=[type(error).__name__, str(error)]))
            self._geometry_versions.update(proposed_versions)
            self._last_frame, self._last_timestamp = frame, timestamp
            self._seen.update(keys)
            if self.reconstructor is not None and proposed_versions:
                self._pending_reconstructions = self.reconstructor.prepare(frame, proposed_versions)
            return dict(frame_index=frame, assignments=assignments, updates=events,
                        before=previous, after=self.snapshot(), training_data=training_data)
        except Exception:
            self.matcher.abort()
            self._failed = True
            raise
        finally:
            self._busy = False

    def resolve_reconstructions(self):
        """Validate ALL results, then publish together for future frames only.

        A missing/corrupt result keeps the replay blocked. An explicit failed
        worker result preserves the last valid form and allows continuation.
        """
        if self._failed or self._busy:
            raise RuntimeError('Cannot resolve results during a frame or after core failure')
        if not self._pending_reconstructions:
            return []
        ready, events = self.reconstructor.collect(self._pending_reconstructions, self._last_frame, self._geometry_versions)
        self.matcher.geometry.publish_reconstructions(self._last_frame, ready)
        self._pending_reconstructions = []
        return events
