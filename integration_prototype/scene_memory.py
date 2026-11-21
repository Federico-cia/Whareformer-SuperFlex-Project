"""Point 3 memory: weighted observed voxels, placement hypotheses, one shape.

Parameters are explicit DEVELOPMENT choices, not learned/calibrated defaults.
This is a DenStream-inspired state machine, not an implementation of DenStream.
Staticity comes from external evidence; neither oracle identity nor this module
certifies it. Learned pair verification never uses the old rigid-pose gates.
"""
from copy import deepcopy
from dataclasses import asdict, dataclass, field
import hashlib
import json
import math
import numpy as np
from scipy.spatial import cKDTree
from scene_geometry import cloud, farthest_points, rigid, transform
from registration_verifier import UnavailableVerifier, Verification


@dataclass(frozen=True)
class SceneMemoryConfig:
    voxel_size: float
    decay_half_life: float
    minimum_confirmations: int
    confirmation_weight: float
    maximum_predicted_error: float
    outlier_radius: float
    minimum_neighbors: int
    maximum_cells: int
    maximum_pending_states: int
    selection_provenance: str
    fuse_after_motion: bool = False

    def __post_init__(self):
        positive = (self.voxel_size, self.decay_half_life, self.confirmation_weight, self.outlier_radius)
        integers = (self.minimum_confirmations, self.minimum_neighbors, self.maximum_cells, self.maximum_pending_states)
        if (not all(np.isfinite(v) and v > 0 for v in positive)
                or not all(type(v) is int and v >= 1 for v in integers)
                or self.minimum_confirmations < 2 or not np.isfinite(self.maximum_predicted_error)
                or self.maximum_predicted_error < 0 or not self.selection_provenance
                or type(self.fuse_after_motion) is not bool):
            raise ValueError('Explicit development parameters/provenance required; confirmations >= 2')


class WeightedVoxels:
    """One centroid per cell; decay reduces confidence, never deletes coverage.

    Per-view contributions are normalized within each cell: pixel density is not
    evidence of independent temporal support. Age affects old/new fusion, not FPS.
    """
    def __init__(self, config):
        self.config = config
        self.cells = {}
        self.observations = []
        self.time = None

    def cloud(self):
        if not self.cells:
            return np.empty((0, 3), float)
        return np.array([self.cells[k][0] for k in sorted(self.cells)])

    def weights(self, timestamp):
        return np.array([self.cells[k][1] * math.exp2(-(timestamp - self.cells[k][2]) / self.config.decay_half_life)
                         for k in sorted(self.cells)])

    def add(self, points, timestamp, key, *, confidence=None, filter_outliers=True, aggregate=False):
        p = cloud(points)
        w = np.ones(len(p)) if confidence is None else np.asarray(confidence, float)
        if (w.shape != (len(p),) or not np.isfinite(w).all() or np.any(w <= 0)
                or not aggregate and np.any(w > 1)
                or not np.isfinite(timestamp) or self.time is not None and timestamp < self.time
                or not key or key in self.observations):
            raise ValueError('Valid confidence, causal time and unique observation required')
        if filter_outliers:
            support = cKDTree(p).query_ball_point(p, self.config.outlier_radius, return_length=True)
            keep = support >= self.config.minimum_neighbors
            p, w = p[keep], w[keep]
        if not len(p):
            return dict(added=False, reason='all_points_filtered', input_points=len(points), kept_points=0)
        scaled = p / self.config.voxel_size
        if np.any(np.abs(scaled) >= 2**52):
            raise ValueError('Coordinates too large for reliable voxel indexing')
        # Rigid transforms can move a boundary by a few floating-point ULPs.
        nearest = np.rint(scaled)
        tolerance = 32 * np.finfo(float).eps * np.maximum(1, np.abs(scaled))
        scaled = np.where(np.abs(scaled - nearest) <= tolerance, nearest, scaled)
        ids = np.floor(scaled).astype(np.int64)
        keys, inverse = np.unique(ids, axis=0, return_inverse=True)
        cell_keys = [tuple(int(x) for x in k) for k in keys]
        if len(set(cell_keys) | self.cells.keys()) > self.config.maximum_cells:
            raise ValueError('Cell budget exceeded: preserve prior memory, no silent coverage deletion')
        weight_sums = np.bincount(inverse, weights=w)
        counts = np.bincount(inverse)
        weighted_points = np.zeros((len(keys), 3))
        np.add.at(weighted_points, inverse, p * w[:, None])
        centroids = weighted_points / weight_sums[:, None]
        updates = {}
        for i, k in enumerate(cell_keys):
            new_point = centroids[i]
            new_weight = float(weight_sums[i] if aggregate else weight_sums[i] / counts[i])
            if k in self.cells:
                old, weight, time = self.cells[k]
                weight *= math.exp2(-(timestamp - time) / self.config.decay_half_life)
                new_point = (old * weight + new_point * new_weight) / (weight + new_weight)
                new_weight += weight
            updates[k] = (new_point, new_weight, float(timestamp))
        new_cells = sum(k not in self.cells for k in updates)
        self.cells.update(updates)
        self.time = float(timestamp)
        self.observations.append(key)
        return dict(added=True, input_points=len(points), kept_points=len(p),
                    new_cells=new_cells, reinforced_cells=len(updates) - new_cells)


@dataclass(frozen=True)
class SceneObservation:
    key: str
    frame: int
    timestamp: float
    world_points: object
    alignment_valid: bool
    staticity: str
    evidence_id: str
    provenance: dict = field(default_factory=dict)
    source: str = 'da_aligned'
    observed_only: bool = True


@dataclass
class PlacementState:
    state_id: str
    memory: WeightedVoxels
    keys: list
    support: float
    last_time: float
    confirmed: bool = False
    object_to_scene: object = None
    merged_keys: list = field(default_factory=list)


class SceneObjectMemory:
    """One instance per video/predicted track; all views stay strictly causal."""
    def __init__(self, video, track_id, config, verifier=None):
        if not video or not track_id:
            raise ValueError('Video and predicted track scope required')
        self.video, self.track_id, self.config = video, str(track_id), config
        self.verifier = UnavailableVerifier() if verifier is None else verifier
        self.shape = WeightedVoxels(config)
        self.states = {}
        self.seen = set()
        self.last_frame, self.last_time = -1, -math.inf
        self.version = self.shape_version = 0
        self.events = []

    def _verify(self, a, b):
        result = self.verifier(a, b)
        if not isinstance(result, Verification):
            raise ValueError('Verifier must return an explicit Verification')
        return result, result.error is not None and result.error <= self.config.maximum_predicted_error

    def update(self, observation):
        """Atomic update; failures cannot contaminate valid shape or candidates."""
        proposal = deepcopy(self)
        event = proposal._update(observation)
        self.__dict__.update(proposal.__dict__)
        return event

    def _update(self, o):
        if (not isinstance(o, SceneObservation) or not o.key or o.key in self.seen
                or type(o.frame) is not int or o.frame <= self.last_frame
                or not np.isfinite(o.timestamp) or o.timestamp <= self.last_time
                or type(o.alignment_valid) is not bool or o.staticity not in ('stationary', 'moving', 'unknown')
                or o.source != 'da_aligned' or o.observed_only is not True or not isinstance(o.provenance, dict)):
            raise ValueError('Causal observed DA-aligned scene input required')
        self.seen.add(o.key)
        self.last_frame, self.last_time = o.frame, float(o.timestamp)
        event = dict(key=o.key, frame=o.frame, timestamp=o.timestamp, shape_changed=False,
                     staticity=o.staticity, evidence_id=o.evidence_id, provenance=deepcopy(o.provenance))
        if not o.alignment_valid:
            return self._record(event, 'alignment_failed')
        if o.staticity != 'stationary' or not o.evidence_id:
            return self._record(event, 'awaiting_independent_staticity_evidence')
        p = cloud(o.world_points)
        # Remove isolated measurement artefacts, NOT unmatched novel surfaces.
        filtered = WeightedVoxels(self.config)
        quality = filtered.add(p, o.timestamp, o.key)
        event['point_filter'] = quality
        if not quality['added']:
            return self._record(event, 'all_points_filtered')
        p = filtered.cloud()
        matches, verification = [], []
        for state in self.states.values():
            result, accepted = self._verify(p, state.memory.cloud())
            verification.append(dict(state_id=state.state_id, error=result.error, model_id=result.model_id))
            if accepted:
                matches.append((result.error, state.state_id))
        event['verification'] = verification
        if matches:
            state = self.states[min(matches)[1]]
            state.memory.add(p, o.timestamp, o.key, filter_outliers=False)
            state.support = state.support * math.exp2(-(o.timestamp - state.last_time) / self.config.decay_half_life) + 1
            state.last_time = o.timestamp
            state.keys.append(o.key)
        else:
            # Bounded pending hypotheses; shape/confirmed placements are never evicted.
            pending = [s for s in self.states.values() if not s.confirmed]
            if len(pending) >= self.config.maximum_pending_states:
                weakest = min(pending, key=lambda s: s.support * math.exp2(-(o.timestamp - s.last_time) / self.config.decay_half_life))
                del self.states[weakest.state_id]
                event['evicted_pending_state'] = weakest.state_id
            state = PlacementState(o.key, filtered, [o.key], 1., o.timestamp)
            self.states[state.state_id] = state
        event['state_id'] = state.state_id
        if len(state.keys) >= self.config.minimum_confirmations and state.support >= self.config.confirmation_weight:
            state.confirmed = True
        if not state.confirmed:
            return self._record(event, 'pending_confirmation')
        if not len(self.shape.cells):
            # Arbitrary object coordinate origin, not a permanently retained view.
            state.object_to_scene = np.eye(4)
            state.object_to_scene[:3, 3] = state.memory.cloud().mean(0)
        if state.object_to_scene is None:
            return self._record(event, 'confirmed_placement_awaiting_shape_registration')
        self._fuse_state(state, p)
        event['shape_changed'] = True
        return self._record(event, 'fused_stationary')

    def _record(self, event, status):
        event.update(status=status, shape_version=self.shape_version)
        self.version += 1
        self.events.append(deepcopy(event))
        return event

    def _fuse_state(self, state, latest_contribution=None):
        # Initial promotion adds aggregated candidate once; later, only new views.
        if not state.merged_keys:
            contribution = state.memory.cloud()
            key = 'state:' + state.state_id
            # Preserve temporal support/confidence when a candidate is promoted.
            confidence = np.maximum(state.memory.weights(state.last_time), np.finfo(float).tiny)
        else:
            contribution = cloud(latest_contribution)
            key = state.keys[-1]
            confidence = None
        self.shape.add(transform(contribution, np.linalg.inv(state.object_to_scene)),
                       state.last_time, key, confidence=confidence,
                       filter_outliers=False, aggregate=not state.merged_keys)
        state.merged_keys = list(state.keys)
        self.shape_version += 1

    def merge_placement(self, state_id, world_to_object, *, frame, timestamp, evidence_id):
        """Explicit future motion path: known/proposed rigid pose + learned check.

        Disabled in the first static-only stage. No reset of the one object shape.
        Caller must provide a registrar; this method never invents the pose.
        """
        if not self.config.fuse_after_motion:
            raise ValueError('Motion fusion disabled in the first-stage configuration')
        if (state_id not in self.states or type(frame) is not int or frame != self.last_frame
                or timestamp != self.last_time or not evidence_id or not self.shape.cells):
            raise ValueError('Current-frame registration and evidence required')
        proposal = deepcopy(self)
        state = proposal.states[state_id]
        if not state.confirmed or state.merged_keys or state.last_time != timestamp:
            raise ValueError('Only confirmed, not yet merged placements may be registered')
        t = rigid(world_to_object)
        aligned = transform(state.memory.cloud(), t)
        result, accepted = proposal._verify(aligned, proposal.shape.cloud())
        if not accepted:
            return dict(status='registration_not_verified', error=result.error, model_id=result.model_id,
                        shape_changed=False)
        state.object_to_scene = np.linalg.inv(t)
        proposal._fuse_state(state)
        event = dict(status='fused_after_motion', state_id=state_id, frame=frame, timestamp=timestamp,
                     evidence_id=evidence_id, shape_changed=True, shape_version=proposal.shape_version,
                     error=result.error, model_id=result.model_id)
        proposal.events.append(deepcopy(event))
        self.__dict__.update(proposal.__dict__)
        return event

    def cloud(self):
        return self.shape.cloud()

    def superflex_input(self):
        """Export observed object-space points, FPS and inverse normalization."""
        p = cloud(self.cloud())
        if len(p) < 4:
            raise ValueError('At least four observed cells required for SuperFlex')
        ids = farthest_points(p, 4096)
        # Keep the existing SuperFlex normalization, changing sampling to FPS only.
        center = p[ids].mean(0)
        scale = float(2 * np.max(np.abs(p[ids] - center)))
        if scale <= np.finfo(float).eps:
            raise ValueError('Degenerate shape for reconstruction')
        return dict(object_points=p, selected_points=p[ids], sample_indices=ids,
                    normalized_points=(p[ids] - center) / scale, translation=center, scale=scale,
                    shape_version=self.shape_version, observed_only=True, sampling='deterministic_fps_4096')

    def snapshot(self):
        p = self.cloud()
        return dict(video=self.video, track_id=self.track_id, version=self.version,
                    shape_version=self.shape_version, source='da_aligned',
                    shape_cells=len(p), cloud_sha256=hashlib.sha256(p.astype('<f8').tobytes()).hexdigest(),
                    config=asdict(self.config), states={k: dict(keys=list(s.keys), confirmed=s.confirmed,
                    merged_keys=list(s.merged_keys), support=s.support,
                    object_to_scene=None if s.object_to_scene is None else s.object_to_scene.tolist())
                    for k, s in self.states.items()})

    def export_superflex(self, path):
        """Create, never overwrite; no inference launched by this method."""
        data = self.superflex_input()
        with open(path, 'xb') as f:
            np.savez_compressed(f, **data, provenance_json=json.dumps(self.snapshot(), allow_nan=False),
                                events_json=json.dumps(self.events, allow_nan=False))


class SceneMemoryUpdater:
    """Pure FrameCoordinator adapter; no neural reconstruction request here.

    Pending-state commits intentionally advance geometry state, NOT shape.
    Use without the legacy DeferredSuperflex, whose sampling/CloudState contract
    is different. Export only when shape_changed, through export_superflex.
    """
    supports_deferred_reconstruction = False

    def __init__(self, config, verifier=None):
        self.config, self.verifier = config, verifier

    def __call__(self, context):
        from frame_coordinator import GeometryDecision
        o = context.observation
        if (not isinstance(o, SceneObservation) or o.key != context.observation_key or o.frame != context.frame_index
                or context.representation not in ('da_raw_points', 'da_raw_superflex')):
            raise ValueError('Scene input/context mismatch; legacy representation name is not source provenance')
        prior = context.previous
        if prior is None:
            memory = SceneObjectMemory(context.video, context.track_id, self.config, self.verifier)
        else:
            memory = deepcopy(prior['value'])
            if (not isinstance(memory, SceneObjectMemory) or memory.video != context.video
                    or memory.track_id != str(context.track_id) or memory.config != self.config
                    or memory.version != prior['version']):
                raise ValueError('Scene memory scope/config/version mismatch')
        event = memory.update(o)
        return GeometryDecision(True, memory, diagnostics=event)
