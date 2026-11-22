"""Geometric adaptation of the appearance memory's multi-hypothesis lifecycle.

Scene-space compatibility grows placement hypotheses; only confirmed hypotheses
may be registered to the persistent object shape. Pruning never deletes shape
coverage. Invalid measurements are excluded; incompatible valid views spawn states.
"""
from copy import deepcopy
from dataclasses import asdict
import math
import json
import numpy as np
from cloud_memory import RegistrationConfig, register_rigid
from scene_geometry import cloud, transform
from scene_memory import SceneObjectMemory, SceneObservation, PlacementState, WeightedVoxels


class MultiHypothesisMemory(SceneObjectMemory):
    policy = 'multi-hypothesis-scene-memory-v1'

    def __init__(self, video, track_id, config, verifier=None, registration_config=None):
        super().__init__(video, str(track_id), config, verifier)
        if config.confirmation_weight <= 1:
            raise ValueError('Temporal promotion weight must exceed one')
        self.registration_config = registration_config or RegistrationConfig()
        self.fused_keys = []
        self.retired_states = []
        self.created_times = {}
        self._views = {}
        self.last_prune_time = None
        # Same expression as FeatureDenStream, with lambda=1/half_life.
        self.prune_interval = math.ceil(config.decay_half_life * math.log(
            config.confirmation_weight / (config.confirmation_weight - 1)))

    def _weight(self, state, now):
        return state.support * math.exp2(-(now - state.last_time) / self.config.decay_half_life)

    def _retire(self, sid, now, reason):
        s = self.states.pop(sid)
        self.retired_states.append(dict(state_id=sid, timestamp=now, reason=reason,
            confirmed=s.confirmed, keys=list(s.keys), merged_keys=list(s.merged_keys),
            decayed_support=self._weight(s, now)))
        self.created_times.pop(sid)
        for key in s.keys:
            self._views.pop(key, None)

    def _prune(self, now):
        if self.last_prune_time is None:
            self.last_prune_time = now
            return []
        if now - self.last_prune_time < self.prune_interval:
            return []
        removed = []
        mu, half = self.config.confirmation_weight, self.config.decay_half_life
        for sid, state in list(self.states.items()):
            if state.last_time == now:
                continue
            # Appearance-like potential/weak cluster survival rule. Active
            # descriptor exposure and physical surface fusion remain different.
            threshold = mu if state.confirmed else (
                math.exp2(-(now - self.created_times[sid] + self.prune_interval) / half) - 1
                ) / (math.exp2(-self.prune_interval / half) - 1)
            if self._weight(state, now) < threshold:
                self._retire(sid, now, 'temporal_pruning')
                removed.append(sid)
        self.last_prune_time = now
        return removed

    def _update(self, o):
        if (not isinstance(o, SceneObservation) or not o.key or o.key in self.seen
                or type(o.frame) is not int or o.frame <= self.last_frame
                or not np.isfinite(o.timestamp) or o.timestamp <= self.last_time
                or type(o.alignment_valid) is not bool or o.source != 'da_aligned'
                or o.observed_only is not True):
            raise ValueError('Unique causal observed DA-aligned scene input required')
        self.seen.add(o.key); self.last_frame = o.frame; self.last_time = float(o.timestamp)
        event = dict(key=o.key, frame=o.frame, timestamp=o.timestamp, policy=self.policy,
                     shape_changed=False, staticity_claim=False, provenance=deepcopy(o.provenance))
        if not o.alignment_valid:
            event['pruned_states'] = self._prune(o.timestamp)
            return self._record(event, 'alignment_failed')
        filtered = WeightedVoxels(self.config)
        quality = filtered.add(cloud(o.world_points), o.timestamp, o.key)
        event['point_filter'] = quality
        if not quality['added'] or len(filtered.cells) < 64:
            event['pruned_states'] = self._prune(o.timestamp)
            return self._record(event, 'insufficient_valid_points')
        p = filtered.cloud()
        self._views[o.key] = (p, o.timestamp)
        checks, matches = [], []
        # Prioritize compatible confirmed states, then compatible weak states,
        # like appearance. Compare in common scene frame: no motion ICP here.
        for confirmed in (True, False):
            for sid, state in self.states.items():
                if state.confirmed != confirmed:
                    continue
                result, accepted = self._verify(p, state.memory.cloud())
                checks.append(dict(state_id=sid, error=result.error, model_id=result.model_id,
                                   accepted=accepted, stage='scene_compatibility'))
                if accepted:
                    matches.append((result.error, sid))
            if matches:
                break
        event['compatibility'] = checks
        if matches:
            state = self.states[min(matches)[1]]
            state.support = self._weight(state, o.timestamp) + 1
            state.last_time = o.timestamp
            state.keys.append(o.key)
            state.memory.add(p, o.timestamp, o.key, filter_outliers=False)
            event['created_hypothesis'] = False
        else:
            pending = [s for s in self.states.values() if not s.confirmed]
            if len(pending) >= self.config.maximum_pending_states:
                weakest = min(pending, key=lambda s: (self._weight(s, o.timestamp), s.state_id))
                event['budget_retired_state'] = weakest.state_id
                self._retire(weakest.state_id, o.timestamp, 'pending_budget')
            state = PlacementState(o.key, filtered, [o.key], 1., o.timestamp)
            self.states[state.state_id] = state
            self.created_times[state.state_id] = o.timestamp
            event['created_hypothesis'] = True
        event['state_id'] = state.state_id
        promoted = not state.confirmed and len(state.keys) >= self.config.minimum_confirmations and state.support >= self.config.confirmation_weight
        if promoted:
            state.confirmed = True
        event['promoted'] = promoted
        status = 'hypothesis_pending'
        if state.confirmed:
            status = self._merge_confirmed(state, p, event)
        event['pruned_states'] = self._prune(o.timestamp)
        return self._record(event, status)

    def _merge_confirmed(self, state, latest, event):
        initial = not self.shape.cells
        if initial:
            object_to_scene = np.eye(4)
            object_to_scene[:3, 3] = state.memory.cloud().mean(0)
            matrix = np.linalg.inv(object_to_scene)
        elif state.object_to_scene is not None:
            matrix = np.linalg.inv(state.object_to_scene)
            waiting = [self._views[k][0] for k in state.keys if k not in state.merged_keys]
            result, accepted = self._verify(transform(np.concatenate(waiting), matrix), self.cloud())
            event['shape_verification'] = dict(error=result.error, model_id=result.model_id, accepted=accepted)
            if not accepted:
                return 'confirmed_state_separate'
        else:
            if not self.config.fuse_after_motion:
                return 'confirmed_state_separate'
            try:
                reg = register_rigid(state.memory.cloud(), self.cloud(), self.registration_config)
                matrix = np.eye(4)
                matrix[:3, :3] = np.asarray(reg['rotation']).T
                matrix[:3, 3] = reg['translation']
                result, accepted = self._verify(transform(state.memory.cloud(), matrix), self.cloud())
                event['registration'] = reg
                event['legacy_gate_used'] = False
                event['shape_verification'] = dict(error=result.error, model_id=result.model_id, accepted=accepted)
                if not accepted:
                    return 'confirmed_state_separate'
            except ValueError as error:
                event['registration_error'] = str(error)
                return 'confirmed_state_separate'
        # Add only unmerged views. Preserve per-view weighted sufficient statistics
        # until publication, so a failed attempt is not dropped on a later retry.
        unmerged = [k for k in state.keys if k not in state.merged_keys]
        if not unmerged:
            return 'confirmed_state_unchanged'
        if state.merged_keys:
            # Usually one new view. If older contributions were withheld, defer
            # to rebuild from retained view records (see _views below).
            for key in unmerged:
                points, timestamp = self._views[key]
                confidence = math.exp2(-(state.last_time - timestamp) / self.config.decay_half_life)
                self.shape.add(transform(points, matrix), state.last_time, key,
                               confidence=np.full(len(points), confidence), filter_outliers=False)
        else:
            self.shape.add(transform(state.memory.cloud(), matrix), state.last_time,
                'state:' + state.state_id, confidence=np.maximum(state.memory.weights(state.last_time),
                np.finfo(float).tiny), filter_outliers=False, aggregate=True)
        state.object_to_scene = np.linalg.inv(matrix)
        state.merged_keys = list(state.keys)
        self.fused_keys.extend(k for k in unmerged if k not in self.fused_keys)
        for key in unmerged:
            self._views.pop(key, None)
        self.shape_version += 1
        event.update(shape_changed=True, world_to_object=matrix.tolist(), fused_observation_keys=unmerged)
        return 'initialized_confirmed_shape' if initial else 'fused_confirmed_state'

    def update(self, observation):
        proposal = deepcopy(self)
        event = proposal._update(observation)
        self.__dict__.update(proposal.__dict__)
        return event

    def snapshot(self):
        result = super().snapshot()
        result.update(policy=self.policy, staticity_required=False,
            last_frame=self.last_frame, last_timestamp=self.last_time,
            registration_config=asdict(self.registration_config),
            fused_observation_keys=list(self.fused_keys), prune_interval=self.prune_interval,
            retired_states=deepcopy(self.retired_states), real_fusion_accuracy_validated=False)
        for sid, state in self.states.items():
            result['states'][sid].update(created_time=self.created_times[sid],
                decayed_support=self._weight(state, self.last_time),
                status='confirmed' if state.confirmed else 'weak')
        return result

    def export_hypotheses(self, path):
        arrays = {'snapshot_json': json.dumps(self.snapshot(), allow_nan=False)}
        for i, state in enumerate(self.states.values()):
            arrays[f'state_{i}_world_points'] = state.memory.cloud()
            arrays[f'state_{i}_weights'] = state.memory.weights(self.last_time)
            arrays[f'state_{i}_id'] = state.state_id
        with open(path, 'xb') as f:
            np.savez_compressed(f, **arrays)


class MultiHypothesisUpdater:
    supports_deferred_reconstruction = True
    required_reconstruction_contract = 'scene-fps-v1'

    def __init__(self, config, verifier=None, registration_config=None):
        self.config, self.verifier, self.registration_config = config, verifier, registration_config

    def __call__(self, context):
        from frame_coordinator import GeometryDecision
        o = context.observation
        if (not isinstance(o, SceneObservation) or o.key != context.observation_key
                or o.frame != context.frame_index or context.representation not in ('da_raw_points', 'da_raw_superflex')):
            raise ValueError('Observation/context mismatch')
        if context.previous is None:
            m = MultiHypothesisMemory(context.video, context.track_id, self.config, self.verifier, self.registration_config)
        else:
            m = deepcopy(context.previous['value'])
            if (not isinstance(m, MultiHypothesisMemory) or m.video != context.video or m.track_id != str(context.track_id)
                    or m.config != self.config or m.version != context.previous['version']):
                raise ValueError('Multi-hypothesis scope/config/version mismatch')
        return GeometryDecision(True, m, diagnostics=m.update(o))
