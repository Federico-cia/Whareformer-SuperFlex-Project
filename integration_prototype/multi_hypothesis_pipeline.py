"""Explicit live-tracker entry point; never falls back to legacy accumulation.

Caller supplies original detections and observed DA-aligned scene points. Query
features belong to the current detection; all shape publications follow matching.
"""
import numpy as np
from frame_coordinator import FrameCoordinator
from geometry_matcher import GeometryMatcher
from multi_hypothesis_memory import MultiHypothesisUpdater
from position_state_memory import PositionStateUpdater
from deferred_scene_superflex import DeferredSceneSuperflex
from scene_geometry import farthest_points
from shape_tools.geometry import normalize_shape
from shape_tools.metrics import descriptors


class MultiHypothesisPipeline:
    def __init__(self, tracker, video, matcher_config, memory_config, verifier,
                 *, registration_config=None, reconstruction_root=None, allow_test_results=False,
                 position_config=None, relative_resolution=None):
        if matcher_config.representation not in ('da_raw_points', 'da_raw_superflex'):
            raise ValueError('DA-aligned payload uses the existing DA interface names only')
        if matcher_config.mode == 'disabled':
            raise ValueError('Use diagnostic or active geometry mode explicitly')
        completed = matcher_config.representation.endswith('_superflex')
        if completed != (reconstruction_root is not None):
            raise ValueError('SuperFlex mode requires an explicit FPS reconstruction queue')
        baseline = tracker.matcher
        if isinstance(baseline, GeometryMatcher):
            if baseline.snapshot() or baseline._context is not None or baseline._pending:
                raise ValueError('Use a fresh tracker/matcher')
            baseline = baseline.baseline
        if tracker.tracks:
            raise ValueError('Use a fresh tracker')
        tracker.matcher = GeometryMatcher(baseline, video, matcher_config)
        service = DeferredSceneSuperflex(reconstruction_root, allow_test_results=allow_test_results) if completed else None
        # Option A (state = placement) when a PositionConfig is given; scene
        # observations must then carry their camera. The v1 policy stays as comparison.
        updater = (PositionStateUpdater(memory_config, verifier, registration_config, position_config,
                                        relative_resolution)
                   if position_config is not None else MultiHypothesisUpdater(memory_config, verifier, registration_config))
        self.coordinator = FrameCoordinator(tracker, updater, service)

    def step(self, detections, metadata, observation_keys, query_features, scene_observations):
        result = self.coordinator.step(detections, metadata, observation_keys,
                                       query_features, scene_observations)
        if self.coordinator.reconstructor is None:
            ready = {}
            for event in result['updates']:
                if not event.get('diagnostics', {}).get('shape_changed'):
                    continue
                tid = event['track_id'];m = result['after']['geometry'][tid]['value']
                p = m.cloud();sample = normalize_shape(p[farthest_points(p, 1024)])
                ready[tid] = (f'{m.shape_version}_{m.snapshot()["cloud_sha256"]}', (sample, *descriptors(sample)))
            self.coordinator.matcher.geometry.publish_accumulated_points(metadata['frame_idx'], ready)
        result['after'] = self.coordinator.snapshot()
        return result

    def resolve_reconstructions(self):
        return self.coordinator.resolve_reconstructions()

    def snapshot(self):
        return self.coordinator.snapshot()
