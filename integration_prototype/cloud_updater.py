"""Pure adapter: associated observed camera points -> candidate cloud memory.

Rigid registration/gates are reused unchanged. This adapter never generates
points or replaces matching descriptors; accepted accumulation is not proof of
physical pose/scale correctness. Full state is in-memory, not a disk checkpoint.
"""
from copy import deepcopy
from dataclasses import asdict, dataclass, field
import hashlib
from pathlib import Path

import numpy as np

from cloud_memory import ObservedCloudMemory, RegistrationConfig, points, register_rigid, sample
from frame_coordinator import GeometryDecision


def cloud_hash(value):
    """Content hash with explicit float64 little-endian canonicalization."""
    a = np.ascontiguousarray(value, dtype='<f8')
    return hashlib.sha256(str(a.shape).encode('ascii') + a.tobytes()).hexdigest()


@dataclass(frozen=True)
class CloudUpdateConfig:
    views: int = 4
    points_per_view: int = 2048
    max_observation_points: int = 12000
    registration: RegistrationConfig = field(default_factory=RegistrationConfig)

    def __post_init__(self):
        if (type(self.views) is not int or self.views < 2
                or type(self.points_per_view) is not int or self.points_per_view < 64
                or type(self.max_observation_points) is not int or self.max_observation_points < 64
                or not isinstance(self.registration, RegistrationConfig)):
            raise ValueError('Invalid candidate cloud budget/configuration')


@dataclass(frozen=True)
class ObservedCloudInput:
    points: object
    source: str
    coordinate_convention: str
    scale_convention: str
    observed_only: bool
    provenance: dict = field(default_factory=dict)


@dataclass(frozen=True)
class CloudState:
    memory: ObservedCloudMemory
    coordinate_convention: str
    scale_convention: str
    config: dict
    registration: object

    def summary(self):
        p = self.memory.cloud()
        return dict(**self.memory.snapshot(), coordinate_convention=self.coordinate_convention,
                    scale_convention=self.scale_convention, config=deepcopy(self.config),
                    registration=deepcopy(self.registration), provenance=deepcopy(self.memory.provenance()),
                    cloud_sha256=cloud_hash(p), reference='camera of first accepted observation',
                    convention='row vectors: source @ rotation + translation; no scale fitting')


def load_observed_cloud(path, expected_sha256, source, coordinate_convention, scale_convention):
    """Load only camera_points from a content-verified numeric NPZ artifact.

    Caller must establish that artifact comes from observed masked depth points,
    not a completion. Hash and field name alone cannot certify this semantics.
    """
    path = Path(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != expected_sha256:
        raise ValueError('Observed-cloud artifact hash mismatch')
    with np.load(path, allow_pickle=False) as z:
        p = z['camera_points'].copy()
    return ObservedCloudInput(p, source, coordinate_convention, scale_convention, True,
                              dict(input_sha256=digest, array='camera_points'))


class ObservedCloudUpdater:
    def __init__(self, config=CloudUpdateConfig()):
        self.config = config

    def __call__(self, context):
        item = context.observation
        sources = {'da_raw_points':'da', 'da_raw_superflex':'da', 'moge_points':'moge', 'moge_superflex':'moge'}
        if context.representation not in sources:
            raise ValueError('Unknown representation')
        source = sources[context.representation]
        if (not isinstance(item, ObservedCloudInput) or item.source != source
                or item.observed_only is not True
                or not isinstance(item.coordinate_convention, str) or not item.coordinate_convention
                or not isinstance(item.scale_convention, str) or not item.scale_convention
                or not isinstance(item.provenance, dict)):
            raise ValueError('Explicit observed cloud, matching source and conventions required')
        p = points(item.points)
        if len(p) < 64:
            raise ValueError('At least 64 observed points required for future registration')
        digest = cloud_hash(p)
        p = sample(p, self.config.max_observation_points, context.frame_index)
        prior = context.previous
        if prior is None:
            memory = ObservedCloudMemory(context.video, context.track_id, source,
                                         self.config.views, self.config.points_per_view)
            decision = None
        else:
            old = prior['value']
            if (not isinstance(old, CloudState)
                    or (old.memory.video, old.memory.track_id, old.memory.source) != (context.video, context.track_id, source)
                    or old.coordinate_convention != item.coordinate_convention
                    or old.scale_convention != item.scale_convention
                    or old.config != asdict(self.config)
                    or old.memory.snapshot()['version'] != prior['version']):
                raise ValueError('Prior cloud scope, conventions, version or configuration mismatch')
            memory = deepcopy(old.memory)
            decision = register_rigid(p, memory.cloud(), self.config.registration)
        provenance = dict(input=deepcopy(item.provenance), observed_points_sha256=digest,
                          input_count=len(item.points), sampled_count=len(p), observed_only=True,
                          association='predicted by tracker before geometric update',
                          coordinate_convention=item.coordinate_convention,
                          scale_convention=item.scale_convention)
        outcome = memory.update(context.observation_key, context.frame_index, p,
                                registration=decision, provenance=provenance)
        diagnostics = dict(operation='initialize' if prior is None else 'register_and_accumulate',
                           source=source, registration=decision, candidate_memory=memory.snapshot(),
                           input=provenance)
        if not outcome['accepted']:
            return GeometryDecision(False, reasons=tuple(outcome['reasons']), diagnostics=diagnostics)
        state = CloudState(memory, item.coordinate_convention, item.scale_convention,
                           asdict(self.config), decision)
        diagnostics['cloud_sha256'] = cloud_hash(memory.cloud())
        return GeometryDecision(True, value=state, diagnostics=diagnostics)
