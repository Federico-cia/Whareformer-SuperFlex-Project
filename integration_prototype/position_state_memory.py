"""Option A geometric memory (Marco, 22 Nov 2026): one state = one placement.

* State assignment uses ONLY a position test: silhouette and free-space
  consistency by reprojection with the cameras of the views (Marco's choice C).
  Active confirmed states are tried first, then weak ones, as in the appearance
  memory. No active state at the same position -> new weak state.
* The learned verifier never chooses the state. Inside a confirmed state it only
  decides, view by view, whether the view is fused into the persistent shape.
  A non-admitted view stays in its state (support, history: ``withheld``),
  opens nothing and is not retried.
* When the object is confirmed in a placement, the other confirmed placements
  are closed: a later return to their position opens a NEW state (Marco's
  choice 2), because orientation may have changed and must be registered again.

The position test does not certify staticity. Its parameters are explicit
development choices (PositionConfig.selection_provenance); none is a default.
"""
from copy import deepcopy
from dataclasses import asdict, dataclass, replace
import math
import numpy as np
from scipy.spatial import cKDTree
from cloud_memory import register_rigid
from multi_hypothesis_memory import MultiHypothesisMemory
from scene_geometry import cloud, transform
from scene_memory import PlacementState, SceneObservation, WeightedVoxels


@dataclass(frozen=True)
class PositionConfig:
    minimum_consistency: float       # same placement if score >= this value
    depth_margin: float              # free-space margin in units of the state RMS radius
    silhouette_radius_factor: float  # splat radius = factor * median pixel spacing of the view
    minimum_projected_points: int    # fewer in-image reference points: direction undecidable
    reference_views: int             # most recent views per state used by the reverse test
    selection_provenance: str

    def __post_init__(self):
        if (not (np.isfinite(self.minimum_consistency) and 0 < self.minimum_consistency <= 1)
                or not (np.isfinite(self.depth_margin) and self.depth_margin >= 0)
                or not (np.isfinite(self.silhouette_radius_factor) and self.silhouette_radius_factor > 0)
                or type(self.minimum_projected_points) is not int or self.minimum_projected_points < 1
                or type(self.reference_views) is not int or self.reference_views < 1
                or not self.selection_provenance):
            raise ValueError('Explicit position-test parameters and provenance required')


class Camera:
    """Pinhole camera of one view; world_to_camera maps scene to camera (z forward)."""
    def __init__(self, mapping):
        try:
            w2c = np.asarray(mapping['world_to_camera'], float)
            fx, fy, cx, cy = (float(x) for x in mapping['intrinsics'])
            width, height = (int(x) for x in mapping['image_size'])
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError('Camera needs world_to_camera, intrinsics and image_size') from error
        if (w2c.shape != (4, 4) or not np.isfinite(w2c).all() or not np.allclose(w2c[3], [0, 0, 0, 1])
                or not np.allclose(w2c[:3, :3] @ w2c[:3, :3].T, np.eye(3), atol=1e-5)
                or min(fx, fy) <= 0 or min(width, height) <= 0):
            raise ValueError('Invalid rigid camera or intrinsics')
        self.w2c, self.k, self.size = w2c, (fx, fy, cx, cy), (width, height)

    def project(self, points):
        p = cloud(points) @ self.w2c[:3, :3].T + self.w2c[:3, 3]
        z = p[:, 2]
        with np.errstate(divide='ignore', invalid='ignore'):
            u = self.k[0] * p[:, 0] / z + self.k[2]
            v = self.k[1] * p[:, 1] / z + self.k[3]
        inside = (z > 0) & (u >= 0) & (u < self.size[0]) & (v >= 0) & (v < self.size[1])
        return u, v, z, inside


def surface_depth(camera, points, factor):
    """Front-most observed depth per pixel, splatted from the view's own points.

    The view's points come from its object mask, so their projection approximates
    that mask (silhouette) and their depth the visible surface.
    """
    u, v, z, inside = camera.project(points)
    if inside.sum() < 3:
        raise ValueError('View points must project inside their own image')
    u, v, z = u[inside], v[inside], z[inside]
    uv = np.c_[u, v]
    spacing = cKDTree(uv).query(uv, k=2)[0][:, 1]
    radius = factor * max(float(np.median(spacing)), 1.0)
    r = int(math.ceil(radius))
    width, height = camera.size
    depth = np.full(width * height, np.inf)
    iu, iv = np.floor(u).astype(np.int64), np.floor(v).astype(np.int64)
    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            if dx * dx + dy * dy > radius * radius:
                continue
            x, y = iu + dx, iv + dy
            ok = (x >= 0) & (x < width) & (y >= 0) & (y < height)
            np.minimum.at(depth, y[ok] * width + x[ok], z[ok])
    return depth.reshape(height, width), radius


def consistency(reference, view_points, camera, margin, factor, minimum_points):
    """Fraction of in-image reference points compatible with the view.

    Compatible: projects on the view's silhouette and is not in front of the
    observed surface by more than ``margin`` (that space is seen empty now).
    Points behind the surface (unseen sides) are compatible by construction.
    """
    depth, radius = surface_depth(camera, view_points, factor)
    u, v, z, inside = camera.project(reference)
    n = int(inside.sum())
    detail = dict(in_image=n, splat_radius_px=radius)
    if n < minimum_points:
        return None, detail
    d = depth[np.floor(v[inside]).astype(np.int64), np.floor(u[inside]).astype(np.int64)]
    on = np.isfinite(d)
    free = on & (z[inside] < d - margin)
    detail.update(on_silhouette=int(on.sum()), free_space=int(free.sum()))
    return float((on & ~free).mean()), detail


def rms_radius(p):
    return float(np.sqrt(np.mean(np.sum((p - p.mean(0)) ** 2, axis=1))))


class PositionStateMemory(MultiHypothesisMemory):
    policy = 'position-state-memory-v1'

    def __init__(self, video, track_id, config, verifier=None, registration_config=None, position_config=None,
                 relative_resolution=None):
        if not isinstance(position_config, PositionConfig):
            raise ValueError('Explicit PositionConfig required for option A')
        if relative_resolution is not None:
            v, o = relative_resolution
            if not all(np.isfinite(x) and x > 0 for x in (v, o)):
                raise ValueError('Relative voxel/outlier fractions must be positive')
        super().__init__(video, track_id, config, verifier, registration_config)
        # Optional: voxel/outlier sizes = fractions of the first valid view RMS radius,
        # as in the point-3 export (one configuration per track, fixed once).
        self.base_config, self.relative_resolution = config, relative_resolution
        self.resolution_fixed = relative_resolution is None
        self.position_config = position_config
        self.state_views = {}   # state id -> recent (key, points, Camera)
        self.withheld = {}      # state id -> keys assigned but not admitted to the shape
        self.closed = set()     # confirmed placements left by the object

    def _retire(self, sid, now, reason):
        super()._retire(sid, now, reason)
        self.retired_states[-1].update(withheld_keys=self.withheld.pop(sid, []),
                                       closed=sid in self.closed)
        self.state_views.pop(sid, None)
        self.closed.discard(sid)

    def _position_score(self, p, camera, sid):
        pc, state = self.position_config, self.states[sid]
        reference = state.memory.cloud()
        margin = pc.depth_margin * rms_radius(reference)
        forward, fd = consistency(reference, p, camera, margin, pc.silhouette_radius_factor,
                                  pc.minimum_projected_points)
        reverse, rd = [], []
        for _, points, cam in self.state_views[sid]:
            score, detail = consistency(p, points, cam, margin, pc.silhouette_radius_factor,
                                        pc.minimum_projected_points)
            rd.append(detail)
            if score is not None:
                reverse.append(score)
        parts = [s for s in (forward, float(np.mean(reverse)) if reverse else None) if s is not None]
        return (min(parts) if parts else None), dict(forward=forward, reverse=reverse,
                                                     forward_detail=fd, reverse_detail=rd)

    def _update(self, o):
        if (not isinstance(o, SceneObservation) or not o.key or o.key in self.seen
                or type(o.frame) is not int or o.frame <= self.last_frame
                or not np.isfinite(o.timestamp) or o.timestamp <= self.last_time
                or type(o.alignment_valid) is not bool or o.source != 'da_aligned'
                or o.observed_only is not True):
            raise ValueError('Unique causal observed DA-aligned scene input required')
        camera = Camera(o.camera) if o.alignment_valid else None
        self.seen.add(o.key); self.last_frame = o.frame; self.last_time = float(o.timestamp)
        event = dict(key=o.key, frame=o.frame, timestamp=o.timestamp, policy=self.policy,
                     shape_changed=False, staticity_claim=False, provenance=deepcopy(o.provenance))
        if not o.alignment_valid:
            event['pruned_states'] = self._prune(o.timestamp)
            return self._record(event, 'alignment_failed')
        raw = cloud(o.world_points)
        if not self.resolution_fixed:
            r = rms_radius(raw)
            self.config = replace(self.base_config, voxel_size=r * self.relative_resolution[0],
                                  outlier_radius=r * self.relative_resolution[1])
            self.shape = WeightedVoxels(self.config)
            self.resolution_fixed = True
            event['resolution_radius'] = r
        filtered = WeightedVoxels(self.config)
        quality = filtered.add(raw, o.timestamp, o.key)
        event['point_filter'] = quality
        if not quality['added'] or len(filtered.cells) < 64:
            event['pruned_states'] = self._prune(o.timestamp)
            return self._record(event, 'insufficient_valid_points')
        p = filtered.cloud()
        tests, chosen = [], None
        for confirmed in (True, False):
            candidates = []
            for sid, state in self.states.items():
                if state.confirmed != confirmed or sid in self.closed:
                    continue
                score, detail = self._position_score(p, camera, sid)
                tests.append(dict(state_id=sid, confirmed=confirmed, score=score, **detail))
                if score is not None and score >= self.position_config.minimum_consistency:
                    candidates.append((-score, sid))
            if candidates:
                chosen = min(candidates)[1]
                break
        event['position_tests'] = tests
        if chosen is not None:
            state = self.states[chosen]
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
            self.state_views[state.state_id] = []
            event['created_hypothesis'] = True
        sid = state.state_id
        self._views[o.key] = (p, o.timestamp)
        self.state_views[sid] = (self.state_views[sid] + [(o.key, p, camera)])[-self.position_config.reference_views:]
        event['state_id'] = sid
        promoted = (not state.confirmed and len(state.keys) >= self.config.minimum_confirmations
                    and state.support >= self.config.confirmation_weight)
        if promoted:
            state.confirmed = True
        event['promoted'] = promoted
        status = 'hypothesis_pending'
        if state.confirmed:
            newly_closed = sorted(k for k, s in self.states.items()
                                  if s.confirmed and k != sid and k not in self.closed)
            self.closed.update(newly_closed)
            event['closed_states'] = newly_closed
            status = self._fuse_views(state, event)
        event['pruned_states'] = self._prune(o.timestamp)
        return self._record(event, status)

    def _add_view(self, key, matrix, state):
        points, timestamp = self._views.pop(key)
        confidence = math.exp2(-(state.last_time - timestamp) / self.config.decay_half_life)
        self.shape.add(transform(points, matrix), state.last_time, key,
                       confidence=np.full(len(points), max(confidence, np.finfo(float).tiny)),
                       filter_outliers=False)

    def _fuse_views(self, state, event):
        """The verifier only decides fusion, one view at a time, in arrival order."""
        sid = state.state_id
        withheld = self.withheld.setdefault(sid, [])
        pending = [k for k in state.keys if k not in state.merged_keys and k not in withheld]
        if not pending:
            return 'confirmed_state_unchanged'
        initial = not self.shape.cells
        fused, rejected, checks = [], [], []
        if initial:
            # Arbitrary object origin; the first view of the first confirmed
            # placement cannot be verified against an empty shape.
            object_to_scene = np.eye(4)
            object_to_scene[:3, 3] = self._views[pending[0]][0].mean(0)
            matrix = np.linalg.inv(object_to_scene)
            self._add_view(pending[0], matrix, state)
            fused.append(pending[0])
            state.object_to_scene = object_to_scene
            pending = pending[1:]
        elif state.object_to_scene is None:
            if not self.config.fuse_after_motion:
                return 'confirmed_state_separate'
            try:
                reg = register_rigid(state.memory.cloud(), self.cloud(), self.registration_config)
            except ValueError as error:
                event['registration_error'] = str(error)
                return 'confirmed_state_separate'
            matrix = np.eye(4)
            matrix[:3, :3] = np.asarray(reg['rotation']).T
            matrix[:3, 3] = reg['translation']
            event['registration'] = reg
        else:
            matrix = np.linalg.inv(state.object_to_scene)
        for key in pending:
            result, accepted = self._verify(transform(self._views[key][0], matrix), self.cloud())
            checks.append(dict(key=key, error=result.error, model_id=result.model_id, accepted=accepted))
            if accepted:
                self._add_view(key, matrix, state)
                fused.append(key)
            else:
                rejected.append(key)
        event['shape_verification'] = checks
        if state.object_to_scene is None:
            if not fused:
                # Registration not confirmed by any view: pose not fixed, views stay
                # pending and are tried again with the next registration attempt.
                return 'confirmed_state_separate'
            state.object_to_scene = np.linalg.inv(matrix)
        for key in rejected:
            withheld.append(key)
            self._views.pop(key, None)
        event['withheld_keys'] = rejected
        if not fused:
            return 'view_withheld_in_state'
        state.merged_keys.extend(fused)
        self.fused_keys.extend(fused)
        self.shape_version += 1
        event.update(shape_changed=True, world_to_object=matrix.tolist(), fused_observation_keys=fused)
        return 'initialized_confirmed_shape' if initial else 'fused_confirmed_state'

    def snapshot(self):
        result = super().snapshot()
        result.update(position_config=asdict(self.position_config),
                      relative_resolution=None if self.relative_resolution is None else list(self.relative_resolution),
                      closed_states=sorted(self.closed), staticity_certified=False)
        for sid in result['states']:
            result['states'][sid].update(withheld_keys=list(self.withheld.get(sid, [])),
                                         closed=sid in self.closed)
        return result


class PositionStateUpdater:
    supports_deferred_reconstruction = True
    required_reconstruction_contract = 'scene-fps-v1'

    def __init__(self, config, verifier=None, registration_config=None, position_config=None,
                 relative_resolution=None):
        if not isinstance(position_config, PositionConfig):
            raise ValueError('Explicit PositionConfig required for option A')
        self.config, self.verifier = config, verifier
        self.registration_config, self.position_config = registration_config, position_config
        self.relative_resolution = relative_resolution

    def __call__(self, context):
        from frame_coordinator import GeometryDecision
        o = context.observation
        if (not isinstance(o, SceneObservation) or o.key != context.observation_key
                or o.frame != context.frame_index
                or context.representation not in ('da_raw_points', 'da_raw_superflex')):
            raise ValueError('Observation/context mismatch')
        if context.previous is None:
            m = PositionStateMemory(context.video, context.track_id, self.config, self.verifier,
                                    self.registration_config, self.position_config, self.relative_resolution)
        else:
            m = deepcopy(context.previous['value'])
            if (not isinstance(m, PositionStateMemory) or m.video != context.video
                    or m.track_id != str(context.track_id) or m.base_config != self.config
                    or m.relative_resolution != self.relative_resolution
                    or m.position_config != self.position_config or m.version != context.previous['version']):
                raise ValueError('Position-state scope/config/version mismatch')
        return GeometryDecision(True, m, diagnostics=m.update(o))
