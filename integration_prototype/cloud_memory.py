"""Candidate rigid registration + bounded observed-point memory (row vectors).

No identities, camera poses, metric scale correction or neural completion are
inferred here. Quality thresholds are diagnostic configuration, not calibrated.
"""
from dataclasses import dataclass, asdict
import itertools

import numpy as np
from scipy.spatial import cKDTree


def points(value):
    value = np.asarray(value, dtype=np.float64)
    if value.ndim != 2 or value.shape[1] != 3 or len(value) < 32 or not np.isfinite(value).all():
        raise ValueError('At least 32 finite 3D observed points required')
    if np.linalg.matrix_rank(value - value.mean(0), tol=1e-10) < 2:
        raise ValueError('Degenerate cloud')
    return value.copy()


def radius(p):
    return float(np.sqrt(np.mean(np.sum((p - p.mean(0)) ** 2, axis=1))))


def sample(p, count, seed):
    return p[np.random.default_rng(seed).choice(len(p), min(count, len(p)), replace=False)]


def fit(a, b):
    ca, cb = a.mean(0), b.mean(0)
    u, _, vt = np.linalg.svd((a-ca).T @ (b-cb))
    d = np.eye(3); d[-1, -1] = np.linalg.det(u @ vt)
    rot = u @ d @ vt
    return rot, cb - ca @ rot


def axes(p):
    _, v = np.linalg.eigh(np.cov(p.T))
    v = v[:, ::-1]
    if np.linalg.det(v) < 0:
        v[:, -1] *= -1
    return v


@dataclass(frozen=True)
class RegistrationConfig:
    fit_points: int = 700
    refine_points: int = 3000
    validation_points: int = 300
    iterations: int = 30
    trim_fraction: float = 0.8
    support_distance_rms: float = 0.08
    minimum_support: float = 0.65
    maximum_q90_rms: float = 0.15
    ambiguity_relative: float = 0.05
    ambiguity_degrees: float = 15.0
    seed: int = 1311

    def __post_init__(self):
        if (self.fit_points < 32 or self.refine_points < self.fit_points or self.validation_points < 16 or self.iterations < 1
                or not 0.1 <= self.trim_fraction <= 1
                or not 0 < self.minimum_support <= 1
                or not self.support_distance_rms > 0 or not self.maximum_q90_rms > 0
                or not self.ambiguity_relative >= 0 or not 0 < self.ambiguity_degrees <= 180):
            raise ValueError('Invalid diagnostic registration configuration')


def register_rigid(source, target, config=RegistrationConfig()):
    """Estimate on fit subsets; select starts there; validate on disjoint subsets.

    Returns transform source @ rotation + translation in target's reference.
    Validation points never choose the best initialization or refine the pose.
    """
    a, b = points(source), points(target)
    if len(a) < 64 or len(b) < 64:
        raise ValueError('Registration requires 64 points to split fit/validation')
    rng = np.random.default_rng(config.seed)
    def split(p):
        ids = rng.permutation(len(p)); cut = max(32, int(0.7 * len(p)))
        return p[ids[:cut][:config.fit_points]], p[ids[:cut][:config.refine_points]], p[ids[cut:][:config.validation_points]]
    af, ar, av = split(a); bf, br, bv = split(b)
    scale = radius(bf)
    if scale <= 1e-10:
        raise ValueError('Degenerate target scale')
    aa, ba = axes(af), axes(bf)
    bt = cKDTree(bf)
    candidates = []
    for permutation in itertools.permutations(range(3)):
        for signs in itertools.product((-1, 1), repeat=3):
            init = np.eye(3)[:, permutation] @ np.diag(signs)
            if np.linalg.det(init) < 0:
                continue
            rot = aa @ init @ ba.T
            trans = bf.mean(0) - af.mean(0) @ rot
            previous = float('inf')
            for _ in range(config.iterations):
                moved = af @ rot + trans
                distances, idx = bt.query(moved)
                keep = np.argsort(distances)[:max(16, int(len(af)*config.trim_fraction))]
                dr, dt = fit(moved[keep], bf[idx[keep]])
                rot, trans = rot @ dr, trans @ dr + dt
                err = float(np.mean(distances[keep] ** 2))
                if abs(previous-err) < 1e-10 * scale**2:
                    break
                previous = err
            # Refine each coarse candidate on denser fit-only points. No validation queries.
            fine_tree = cKDTree(br)
            previous = float('inf')
            for _ in range(config.iterations):
                moved = ar @ rot + trans
                distances, idx = fine_tree.query(moved)
                keep = np.argsort(distances)[:max(16,int(len(ar)*config.trim_fraction))]
                dr,dt=fit(moved[keep],br[idx[keep]])
                rot,trans=rot@dr,trans@dr+dt
                err=float(np.mean(distances[keep]**2))
                if abs(previous-err)<1e-10*scale**2:
                    break
                previous=err
            moved = ar @ rot + trans
            da = fine_tree.query(moved)[0]; db = cKDTree(moved).query(br)[0]
            score = float((np.mean(np.sort(da)[:max(16, int(len(da)*config.trim_fraction))])
                           + np.mean(np.sort(db)[:max(16, int(len(db)*config.trim_fraction))])) / 2)
            candidates.append((score, rot, trans))
    candidates.sort(key=lambda x: x[0])
    score, rot, trans = candidates[0]
    ambiguity = []
    for other_score, other_rot, other_trans in candidates[1:]:
        angle = float(np.degrees(np.arccos(np.clip((np.trace(rot.T @ other_rot)-1)/2, -1, 1))))
        # Compare displaced centroids, not translations about an arbitrary origin.
        shift = float(np.linalg.norm(a.mean(0)@other_rot+other_trans-a.mean(0)@rot-trans)/scale)
        if (other_score <= score*(1+config.ambiguity_relative) + 1e-6*scale
                and (angle > config.ambiguity_degrees or shift > config.support_distance_rms)):
            ambiguity.append(dict(fit_score_rms=other_score/scale, angle_degrees=angle, shift_rms=shift))
    moved_validation = av @ rot + trans
    d1 = cKDTree(br).query(moved_validation)[0]/scale
    d2 = cKDTree(ar@rot+trans).query(bv)[0]/scale
    supports = [float(np.mean(d < config.support_distance_rms)) for d in (d1, d2)]
    # Permit novel surface outside overlap; do not penalize every unmatched point.
    q90 = [float(np.quantile(np.sort(d)[:max(16, int(len(d)*config.trim_fraction))], .9)) for d in (d1, d2)]
    reasons = []
    if min(supports) < config.minimum_support:
        reasons.append('insufficient_heldout_support')
    if max(q90) > config.maximum_q90_rms:
        reasons.append('excessive_heldout_residual')
    if ambiguity:
        reasons.append('ambiguous_rigid_pose')
    return dict(accepted=not reasons, reasons=reasons, rotation=rot.tolist(), translation=trans.tolist(),
                fit_score_rms=score/scale, validation_support=supports, validation_trimmed_q90_rms=q90,
                radius_ratio_source_target=radius(a)/radius(b), target_fit_rms=scale,
                ambiguous_alternatives=ambiguity, config=asdict(config),
                fit_counts=[len(af),len(bf)], refine_counts=[len(ar),len(br)], validation_counts=[len(av),len(bv)],
                validation_reference='held-out queries against denser fit reference; queries never used in pose fitting/selection',
                convention='row vectors: source @ rotation + translation; rigid, no scale fitting')


class ObservedCloudMemory:
    """One instance per video/track/source; call update only after association.

    Anchor retained; remaining views FIFO. Equal per-view point quota avoids
    unbounded duplication. Rejected proposals do not change the valid version.
    """
    def __init__(self, video, track_id, source, views=4, points_per_view=512):
        if not video or not track_id or source not in ('da','moge') or views < 2 or points_per_view < 32:
            raise ValueError('Invalid memory scope/budget')
        self.video, self.track_id, self.source = video, track_id, source
        self.views, self.points_per_view = views, points_per_view
        self._entries = []; self._last_frame = -1; self._seen = set(); self._version = 0

    def cloud(self):
        if not self._entries:
            return None
        return np.concatenate([e['points'] for e in self._entries]).copy()

    def snapshot(self):
        return dict(video=self.video, track_id=self.track_id, source=self.source, version=self._version,
                    observation_keys=[e['key'] for e in self._entries], points=sum(len(e['points']) for e in self._entries))

    def update(self, key, frame, observed_points, *, registration=None, provenance=None):
        if not key or key in self._seen or type(frame) is not int or frame <= self._last_frame:
            raise ValueError('Duplicate observation or noncausal frame')
        p = points(observed_points)
        if self._entries:
            if registration is None:
                raise ValueError('Explicit registration decision required after initialization')
            if not registration['accepted']:
                self._last_frame = frame; self._seen.add(key)
                return dict(accepted=False, reasons=registration['reasons'], state=self.snapshot())
            rot = np.asarray(registration['rotation'],float); trans = np.asarray(registration['translation'],float)
            if (rot.shape != (3,3) or trans.shape != (3,) or not np.isfinite(rot).all()
                    or not np.isfinite(trans).all() or not np.allclose(rot.T@rot,np.eye(3),atol=1e-6)
                    or not np.isclose(np.linalg.det(rot),1,atol=1e-6)):
                raise ValueError('Invalid rigid transformation')
            p = p @ rot + trans
        else:
            rot, trans = np.eye(3), np.zeros(3)
        entry = dict(key=key, frame=frame, points=sample(p,self.points_per_view,frame),
                     provenance=dict(provenance or {}), rotation=rot.tolist(), translation=trans.tolist())
        pending = self._entries + [entry]
        if len(pending) > self.views:
            pending = pending[:1] + pending[-(self.views-1):]
        self._entries = pending; self._version += 1; self._last_frame = frame; self._seen.add(key)
        return dict(accepted=True, reasons=[], state=self.snapshot())

    def provenance(self):
        return [{k:v for k,v in e.items() if k != 'points'} for e in self._entries]
