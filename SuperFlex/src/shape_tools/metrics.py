"""Rotation-invariant descriptors and optional rigid surface registration."""

import itertools

import numpy as np
from scipy.spatial import cKDTree


def descriptors(points, pairs=16384, seed=20261109):
    if pairs < 1:
        raise ValueError("Distance sample count must be positive")
    rng = np.random.default_rng(seed)
    i = rng.integers(0, len(points), pairs)
    j = rng.integers(0, len(points) - 1, pairs)
    j += j >= i
    distances = np.sort(np.linalg.norm(points[i] - points[j], axis=1))
    spectrum = np.sqrt(np.maximum(np.linalg.eigvalsh(points.T @ points / len(points)), 0))[::-1]
    return distances, spectrum


def _canonical(points):
    points = points - points.mean(0)
    _, axes = np.linalg.eigh(points.T @ points)
    axes = axes[:, ::-1]
    if np.linalg.det(axes) < 0:
        axes[:, -1] *= -1
    return points @ axes


def _rotations():
    for permutation in itertools.permutations(range(3)):
        for signs in itertools.product([-1, 1], repeat=3):
            rotation = np.eye(3)[:, permutation] @ np.diag(signs)
            if np.linalg.det(rotation) > 0:
                yield rotation


ROTATIONS = tuple(_rotations())


def _fit(a, b):
    ca, cb = a.mean(0), b.mean(0)
    u, _, vt = np.linalg.svd((a - ca).T @ (b - cb))
    correction = np.eye(3)
    correction[-1, -1] = np.linalg.det(u @ vt)
    rotation = u @ correction @ vt
    return rotation, cb - ca @ rotation


def _icp(a, b, iterations):
    tree = cKDTree(b)
    best = float("inf")
    for rotation in ROTATIONS:
        moved = a @ rotation
        previous = float("inf")
        for _ in range(iterations):
            distances, nearest = tree.query(moved)
            rotation, translation = _fit(moved, b[nearest])
            moved = moved @ rotation + translation
            error = float(np.mean(distances**2))
            if abs(previous - error) < 1e-8:
                break
            previous = error
        score = (tree.query(moved)[0].mean() + cKDTree(moved).query(b)[0].mean()) / 2
        best = min(best, float(score))
    return best


def icp_distance(a, b, iterations=12):
    if iterations < 1:
        raise ValueError("ICP iterations must be positive")
    a, b = _canonical(a), _canonical(b)
    return min(_icp(a, b, iterations), _icp(b, a, iterations))
