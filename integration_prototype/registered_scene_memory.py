"""Approved prototype: register every view, then apply the learned verifier.

No staticity claim. Observed points only; completion never enters this memory.
The historical ICP acceptance gates are logged but never decide admission here.
"""
from copy import deepcopy
import math
import numpy as np
from cloud_memory import RegistrationConfig, register_rigid
from scene_geometry import cloud, transform
from scene_memory import SceneObjectMemory, WeightedVoxels, PlacementState, SceneObservation


class RegisteredObjectMemory(SceneObjectMemory):
    def __init__(self, video, track_id, config, verifier=None, registration_config=None):
        super().__init__(video, track_id, config, verifier)
        self.registration_config = registration_config or RegistrationConfig()

    def _update(self, o):
        if (not isinstance(o, SceneObservation) or not o.key or o.key in self.seen
                or type(o.frame) is not int or o.frame <= self.last_frame
                or not np.isfinite(o.timestamp) or o.timestamp <= self.last_time
                or type(o.alignment_valid) is not bool or o.source != 'da_aligned'
                or o.observed_only is not True):
            raise ValueError('Unique causal observed DA-aligned input required')
        self.seen.add(o.key)
        self.last_frame, self.last_time = o.frame, float(o.timestamp)
        event = dict(key=o.key, frame=o.frame, timestamp=o.timestamp, shape_changed=False,
                     policy='register-every-view-v1', staticity_claim=False,
                     provenance=deepcopy(o.provenance))
        if not o.alignment_valid:
            return self._record(event, 'alignment_failed')
        filtered = WeightedVoxels(self.config)
        quality = filtered.add(cloud(o.world_points), o.timestamp, o.key)
        event['point_filter'] = quality
        if not quality['added']:
            return self._record(event, 'all_points_filtered')
        p = filtered.cloud()
        if len(p) < 64:
            return self._record(event, 'insufficient_registration_points')
        if not self.states:
            pose = np.eye(4)
            pose[:3, 3] = p.mean(0)
            seed = WeightedVoxels(self.config)
            seed.add(p - pose[:3, 3], o.timestamp, o.key, filter_outliers=False)
            self.states['registered-shape'] = PlacementState('registered-shape', seed,
                [o.key], 1., o.timestamp, object_to_scene=pose)
            return self._record(event, 'pending_confirmation')
        state = self.states['registered-shape']
        target = self.cloud() if state.confirmed else state.memory.cloud()
        try:
            registration = register_rigid(p, target, self.registration_config)
        except ValueError as error:
            event['registration_error'] = str(error)
            return self._record(event, 'registration_failed')
        matrix = np.eye(4)
        # Legacy registrar returns row-vector rotation; our API uses columns.
        matrix[:3, :3] = np.asarray(registration['rotation']).T
        matrix[:3, 3] = registration['translation']
        aligned = transform(p, matrix)
        result, accepted = self._verify(aligned, target)
        event.update(predicted_error=result.error, model_id=result.model_id,
                     world_to_object=matrix.tolist(), registration=registration,
                     legacy_gate_used=False)
        if not accepted:
            return self._record(event, 'registration_not_verified')
        state.memory.add(aligned, o.timestamp, o.key, filter_outliers=False)
        state.support = state.support * math.exp2(-(o.timestamp - state.last_time) /
                                                 self.config.decay_half_life) + 1
        state.last_time = o.timestamp
        state.keys.append(o.key)
        state.object_to_scene = np.linalg.inv(matrix)
        if (len(state.keys) < self.config.minimum_confirmations or
                state.support < self.config.confirmation_weight):
            return self._record(event, 'pending_confirmation')
        if not state.confirmed:
            self.shape = deepcopy(state.memory)
            state.confirmed = True
        else:
            self.shape.add(aligned, o.timestamp, o.key, filter_outliers=False)
        state.merged_keys = list(state.keys)
        self.shape_version += 1
        event['shape_changed'] = True
        return self._record(event, 'fused_registered_view')

    def snapshot(self):
        result = super().snapshot()
        from dataclasses import asdict
        result.update(policy='register-every-view-v1',
                      registration_config=asdict(self.registration_config),
                      staticity_required=False, real_fusion_accuracy_validated=False)
        return result


class RegisteredMemoryUpdater:
    """Drop-in pure coordinator adapter; use FPS worker separately after commit."""
    supports_deferred_reconstruction = False

    def __init__(self, config, verifier, registration_config=None):
        self.config, self.verifier = config, verifier
        self.registration_config = registration_config

    def __call__(self, context):
        from frame_coordinator import GeometryDecision
        o = context.observation
        if (not isinstance(o, SceneObservation) or o.key != context.observation_key
                or o.frame != context.frame_index
                or context.representation not in ('da_raw_points', 'da_raw_superflex')):
            raise ValueError('Observation/context mismatch')
        previous = context.previous
        if previous is None:
            memory = RegisteredObjectMemory(context.video, context.track_id, self.config,
                                             self.verifier, self.registration_config)
        else:
            memory = deepcopy(previous['value'])
            if (not isinstance(memory, RegisteredObjectMemory) or memory.video != context.video
                    or memory.track_id != str(context.track_id) or memory.config != self.config
                    or memory.version != previous['version']):
                raise ValueError('Memory scope/version/configuration mismatch')
        return GeometryDecision(True, memory, diagnostics=memory.update(o))
