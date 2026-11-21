"""Pair-level learned-error interfaces; no fixed ICP gates as training labels.

No pretrained weights are bundled. Missing verifier returns unavailable, never
an implicit acceptance. Operating point must be selected on development data.
"""
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
from scene_geometry import cloud, farthest_points


@dataclass(frozen=True)
class Verification:
    error: object
    model_id: str

    def __post_init__(self):
        if not self.model_id or (self.error is not None
                and (not np.isfinite(self.error) or self.error < 0)):
            raise ValueError('Nonnegative finite predicted surface error required')


class UnavailableVerifier:
    def __call__(self, aligned_source, target):
        return Verification(None, 'unavailable-no-trained-model')


def pair_features(source, target):
    """Threshold-free diagnostics; intentionally not the old admission gates."""
    a, b = cloud(source), cloud(target)
    scale = np.sqrt(np.mean(np.sum((b - b.mean(0)) ** 2, axis=1)))
    if scale <= np.finfo(float).eps:
        raise ValueError('Degenerate reference cloud')
    da = cKDTree(b).query(a)[0] / scale
    db = cKDTree(a).query(b)[0] / scale
    return np.r_[np.quantile(da, [.1, .5, .9]), np.quantile(db, [.1, .5, .9]),
                 np.linalg.norm(a.mean(0) - b.mean(0)) / scale,
                 np.sqrt(np.mean(np.sum((a - a.mean(0)) ** 2, axis=1))) / scale]


class DiagnosticErrorVerifier:
    """Small regression BASELINE, not the approved direct point-pair network."""
    def __init__(self, artifact):
        self.artifact = artifact
        self.model_id = hashlib.sha256(json.dumps(artifact, sort_keys=True, allow_nan=False).encode()).hexdigest()
        if artifact.get('schema') != 'point3-diagnostic-error-v1':
            raise ValueError('Unsupported diagnostic artifact')
        self.mean = np.asarray(artifact['mean'], float)
        self.scale = np.asarray(artifact['scale'], float)
        self.weights = np.asarray(artifact['weights'], float)
        if (self.mean.shape != (8,) or self.scale.shape != (8,) or self.weights.shape != (9,)
                or not np.isfinite(np.r_[self.mean, self.scale, self.weights]).all()
                or np.any(self.scale <= 0)):
            raise ValueError('Invalid diagnostic weights')

    @classmethod
    def fit(cls, features, errors, *, training_groups, validation_groups, ridge, target_provenance):
        x, y = np.asarray(features, float), np.asarray(errors, float)
        train, valid = set(training_groups), set(validation_groups)
        if (x.ndim != 2 or x.shape[1] != 8 or y.shape != (len(x),) or len(x) < 2
                or len(training_groups) != len(x) or not train or not valid or train & valid
                or not np.isfinite(x).all() or not np.isfinite(y).all() or np.any(y < 0)
                or not np.isfinite(ridge) or ridge < 0 or not target_provenance):
            raise ValueError('Independent groups, known targets and valid training arrays required')
        mean, scale = x.mean(0), x.std(0)
        scale[scale == 0] = 1
        design = np.column_stack([np.ones(len(x)), (x - mean) / scale])
        penalty = np.diag([0.] + [float(ridge)] * 8)
        w = np.linalg.lstsq(np.vstack([design, np.sqrt(penalty)]), np.r_[y, np.zeros(9)], rcond=None)[0]
        return cls(dict(schema='point3-diagnostic-error-v1', mean=mean.tolist(), scale=scale.tolist(),
                        weights=w.tolist(), training_groups=sorted(train), validation_groups=sorted(valid),
                        target='symmetric_surface_error_over_reference_rms',
                        target_provenance=target_provenance, ridge=float(ridge)))

    def __call__(self, source, target):
        x = pair_features(source, target)
        return Verification(float(max(0, np.r_[1., (x - self.mean) / self.scale] @ self.weights)), self.model_id)

    def save(self, path):
        with Path(path).open('x', encoding='utf-8') as f:
            json.dump(self.artifact, f, indent=2, allow_nan=False)


class TorchScriptPairVerifier:
    """Adapter for a future trained/direct-pair model, NOT a chosen architecture.

    Contract: two [1,N,3] float tensors, common target-centred RMS-normalized
    frame; one predicted normalized surface error. An explicit checkpoint hash
    binds the model. No Torch import until explicitly instantiated.
    """
    def __init__(self, path, *, sha256, sample_points):
        if hashlib.sha256(Path(path).read_bytes()).hexdigest() != sha256:
            raise ValueError('Verifier checkpoint hash mismatch')
        if type(sample_points) is not int or sample_points < 1:
            raise ValueError('Explicit verifier sampling required')
        import torch
        self.torch, self.count, self.model_id = torch, sample_points, sha256
        self.model = torch.jit.load(str(path), map_location='cpu').eval()

    def __call__(self, source, target):
        a, b = cloud(source), cloud(target)
        center = b.mean(0)
        scale = np.sqrt(np.mean(np.sum((b - center) ** 2, axis=1)))
        if scale <= np.finfo(float).eps:
            raise ValueError('Degenerate reference cloud')
        arrays = [(p[farthest_points(p, self.count)] - center) / scale for p in (a, b)]
        with self.torch.inference_mode():
            value = self.model(*(self.torch.tensor(p[None], dtype=self.torch.float32) for p in arrays))
        return Verification(float(value.item()), self.model_id)
