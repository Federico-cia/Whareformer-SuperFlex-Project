"""Observed DA -> scene coordinates; no model inference or scene rendering.

Scene depth and object masks must be provided by the existing Whareformer
renderer/data loader. Alignment failure is explicit; raw depth is never fused.
"""
from dataclasses import dataclass
import numpy as np
from scipy.spatial import cKDTree


def cloud(value):
    p = np.asarray(value, dtype=np.float64)
    if p.ndim != 2 or p.shape[1] != 3 or len(p) < 1 or not np.isfinite(p).all():
        raise ValueError('Finite nonempty Nx3 points required')
    return p.copy()


def rigid(value):
    t = np.asarray(value, dtype=np.float64)
    if (t.shape != (4, 4) or not np.isfinite(t).all()
            or not np.allclose(t[3], [0, 0, 0, 1])
            or not np.allclose(t[:3, :3].T @ t[:3, :3], np.eye(3), atol=1e-6)
            or not np.isclose(np.linalg.det(t[:3, :3]), 1, atol=1e-6)):
        raise ValueError('Proper rigid homogeneous transform required')
    return t.copy()


def transform(p, matrix):
    p, t = cloud(p), rigid(matrix)
    return p @ t[:3, :3].T + t[:3, 3]


@dataclass(frozen=True)
class Alignment:
    valid: bool
    world_points: object
    diagnostics: dict


def align_da_to_scene(depth, scene_depth, object_mask, all_object_masks,
                      intrinsics, camera_to_world, *, minimum_static_pixels):
    """Affine least squares as Whareformer, with explicit validity guards.

    Caller must union ALL dynamic/object masks (including current object).
    Scene units remain EPIC-Fields units; physical metres are not certified.
    Additional guards differ from authors' silent raw-depth fallback.
    """
    d, s = np.asarray(depth, float), np.asarray(scene_depth, float)
    mask, union = np.asarray(object_mask, bool), np.asarray(all_object_masks, bool)
    k = np.asarray(intrinsics, float)
    pose = rigid(camera_to_world)
    if (d.ndim != 2 or s.shape != d.shape or mask.shape != d.shape or union.shape != d.shape
            or np.any(mask & ~union) or k.shape != (4,) or not np.isfinite(k).all()
            or min(k[:2]) <= 0 or type(minimum_static_pixels) is not int or minimum_static_pixels < 3):
        raise ValueError('Depth/mask/intrinsics or static-fit configuration mismatch')
    static = (~union) & np.isfinite(d) & np.isfinite(s) & (d > 0) & (s > 0)
    diag = dict(method='whareformer_affine_with_explicit_validity_guards',
                static_pixels=int(static.sum()), source='da', coordinate_frame='scene',
                scale='scene reconstruction units', raw_fallback=False)
    def failed(reason):
        return Alignment(False, None, dict(diag, reason=reason))
    if static.sum() < minimum_static_pixels:
        return failed('insufficient_static_pixels')
    a = np.column_stack([d[static], np.ones(static.sum())])
    if np.linalg.matrix_rank(a) < 2:
        return failed('unidentifiable_affine_fit')
    alpha, beta = np.linalg.lstsq(a, s[static], rcond=None)[0]
    diag.update(alpha=float(alpha), beta=float(beta))
    if not np.isfinite([alpha, beta]).all() or alpha <= 0:
        return failed('invalid_affine_fit')
    v, u = np.nonzero(mask)
    z = alpha * d[v, u] + beta
    if len(z) == 0 or not np.isfinite(z).all() or np.any(z <= 0):
        return failed('invalid_object_depth')
    fx, fy, cx, cy = k
    p = np.column_stack([(u - cx) * z / fx, (v - cy) * z / fy, z])
    diag['observed_points'] = len(p)
    return Alignment(True, transform(p, pose), diag)


def farthest_points(points, count=4096):
    """Deterministic FPS; repeat only when fewer than count distinct cells.

    Returns indices, including repeats when unavoidable. No random re-sampling
    should follow this selection before handing the points to SuperFlex.
    """
    p = cloud(points)
    if type(count) is not int or count < 1:
        raise ValueError('Positive FPS count required')
    chosen = np.empty(min(count, len(p)), dtype=np.int64)
    distance = np.full(len(p), np.inf)
    used = np.zeros(len(p), bool)
    idx = int(np.argmax(np.sum((p - p.mean(0)) ** 2, axis=1)))
    for i in range(len(chosen)):
        chosen[i] = idx
        used[idx] = True
        distance = np.minimum(distance, np.sum((p - p[idx]) ** 2, axis=1))
        distance[used] = -1
        idx = int(np.argmax(distance))
    return np.resize(chosen, count)


def surface_error(points, estimated_transform, reference_transform):
    """Symmetric mean NN surface distance / RMS radius of reference surface.

    For supervision, use a SAME reference surface under known transforms.
    Comparing two differently visible partial scans is not pose ground truth.
    This is invariant to discrete symmetries represented in the sampled surface,
    unlike mean displacement of corresponding indices. Not a complete metric.
    """
    a = transform(points, estimated_transform)
    b = transform(points, reference_transform)
    radius = np.sqrt(np.mean(np.sum((b - b.mean(0)) ** 2, axis=1)))
    if radius <= np.finfo(float).eps:
        raise ValueError('Degenerate reference surface')
    return float((cKDTree(b).query(a)[0].mean() + cKDTree(a).query(b)[0].mean()) / (2 * radius))
