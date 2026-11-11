"""Camera-frame geometry; normalization does not canonicalize orientation."""

import numpy as np


def validate_points(points):
    points = np.asarray(points)
    if points.ndim != 2 or points.shape[1] != 3 or len(points) < 4:
        raise ValueError("Expected at least four XYZ points")
    numeric = np.issubdtype(points.dtype, np.integer) or np.issubdtype(points.dtype, np.floating)
    if not numeric or not np.isfinite(points).all():
        raise ValueError("Points must be finite numbers")
    return points


def backproject(depth, intrinsics):
    """Perspective Z depth to XYZ: X right, Y down, Z forward."""
    depth = np.asarray(depth)
    camera = np.asarray(intrinsics, dtype=float)
    numeric = np.issubdtype(depth.dtype, np.integer) or np.issubdtype(depth.dtype, np.floating)
    if not numeric or depth.ndim != 2 or camera.shape != (4,) or not np.isfinite(camera).all():
        raise ValueError("Expected depth[H,W] and intrinsics[fx,fy,cx,cy]")
    fx, fy, cx, cy = camera
    if fx <= 0 or fy <= 0:
        raise ValueError("Focal lengths must be positive")
    yy, xx = np.indices(depth.shape)
    return np.stack([depth * (xx - cx) / fx, depth * (yy - cy) / fy, depth], axis=-1)


def paired_clouds(depth, intrinsics, moge_points, mask, moge_valid):
    da = backproject(depth, intrinsics)
    moge = np.asarray(moge_points)
    mask, moge_valid = np.asarray(mask, dtype=bool), np.asarray(moge_valid, dtype=bool)
    if moge.shape != da.shape or mask.shape != da.shape[:2] or moge_valid.shape != mask.shape:
        raise ValueError("Depth, masks and point map must use the same resolution")
    common = mask & moge_valid & np.isfinite(da).all(-1) & np.isfinite(moge).all(-1)
    common &= (da[..., 2] > 0) & (moge[..., 2] > 0)
    yy, xx = np.nonzero(common)
    return da[common], moge[common], np.stack([xx, yy], axis=-1)


def prepare_superflex_input(points, count=4096, seed=42):
    """Return normalized points, center, scale and original sample indices."""
    points = validate_points(points)
    if count < 4:
        raise ValueError("Sample count must be at least four")
    indices = np.random.RandomState(seed).choice(len(points), count, replace=len(points) < count)
    sampled = points[indices]
    center = sampled.mean(0)
    centered = sampled - center
    scale = float(2 * np.max(np.abs(centered)))
    if not np.isfinite(scale) or scale <= 1e-4:
        raise ValueError("Degenerate cloud")
    return centered / scale, center, scale, indices


def normalize_shape(points):
    points = validate_points(points).astype(np.float64)
    centered = points - points.mean(0)
    radius = float(np.sqrt(np.mean(np.sum(centered**2, axis=1))))
    if radius < 1e-10:
        raise ValueError("Degenerate cloud")
    return centered / radius
