"""Coordinator contracts with original tracker.update and controlled model tensors."""
import ast
from copy import deepcopy
from types import SimpleNamespace
import unittest

import numpy as np

from frame_coordinator import FrameCoordinator, GeometryDecision
from geometry_matcher import GeometryMatcher, GeometryConfig
from test_geometry_matcher import original_matcher
from test_shape_adapter import SOURCE, feature


class ControlledTrack:
    def __init__(self, data, tid, timestamp):
        self.track_id = tid
        self.history = [deepcopy(data)]
        self.last_seen_time = timestamp
        self.time_since_update = 0

    def increase_age(self, timestamp):
        self.time_since_update = timestamp - self.last_seen_time

    def update(self, data, metadata):
        self.history.append(deepcopy(data))
        self.last_seen_time = metadata['timestamp']
        self.time_since_update = 0


def tracker(mode='active'):
    path = SOURCE.parent.parent/'tracker.py'
    tree = ast.parse(path.read_text(encoding='utf-8'))
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'StandardTracker')
    update = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == 'update')
    env = {}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[update], type_ignores=[])), str(path), 'exec'), env)
    result = type('OriginalTrackerUpdate', (), {'update': env['update']})()
    result.matcher = GeometryMatcher(original_matcher(np.array([[0, 3]], np.float32)), 'V',
                                     GeometryConfig(mode, 'moge_points'))
    result.tracks, result.last_track_id = [], 40
    result._create_track = lambda det, tid, meta: ControlledTrack(det.detection_data, tid, meta['timestamp'])
    return result


def inputs(frame, count=1, missing=False):
    keys = [f'V/f{frame}/d{i}' for i in range(count)]
    detections = [SimpleNamespace(detection_data=dict(frame=frame, detection_idx=i)) for i in range(count)]
    return dict(detections=detections, metadata=dict(frame_idx=frame, timestamp=float(frame)),
                observation_keys=keys, features={k: None if missing else feature(0) for k in keys})


class CoordinatorTests(unittest.TestCase):
    def test_actual_new_track_ids_and_versions(self):
        c = FrameCoordinator(tracker())
        result = c.step(**inputs(0, 2))
        self.assertEqual(result['assignments'], {'V/f0/d0': '40', 'V/f0/d1': '41'})
        self.assertEqual(result['before']['separate_shape_memory'], {})
        self.assertEqual(result['after']['shapes']['40']['version'], 1)
        self.assertEqual(result['after']['geometry'], {})

    def test_all_queries_use_previous_memory_then_callbacks_see_all_assignments(self):
        t = tracker()
        contexts = []
        holder = {}
        def updater(ctx):
            self.assertEqual([x.history[-1]['frame'] for x in t.tracks], [1, 1])
            self.assertEqual(holder['coordinator'].snapshot()['geometry'], {})
            contexts.append(ctx)
            return GeometryDecision(True, {'observed': ctx.observation})
        c = FrameCoordinator(t, updater)
        holder['coordinator'] = c
        c.step(**inputs(0))
        t.matcher.baseline.model.logits = np.array([[0, 3], [3, 0]], np.float32)
        args = inputs(1, 2)
        args['geometry_inputs'] = {k: k for k in args['observation_keys']}
        result = c.step(**args)
        self.assertEqual(result['assignments'], {'V/f1/d0': '40', 'V/f1/d1': '41'})
        for key in args['observation_keys']:
            self.assertEqual(t.matcher.last_score['evidence'][key, '40'], ('V/f0/d0',))
        self.assertEqual(len(contexts), 2)
        self.assertTrue(all(ctx.previous is None for ctx in contexts))
        self.assertEqual(result['after']['geometry']['40']['version'], 1)

    def test_rejection_error_and_missing_preserve_valid_state(self):
        calls = []
        def updater(ctx):
            calls.append(ctx.frame_index)
            if ctx.frame_index == 0:
                return GeometryDecision(True, {'cloud': [1, 2]})
            ctx.previous['value']['cloud'].append(99)
            if ctx.frame_index == 1:
                return GeometryDecision(False, reasons=('low_overlap',))
            raise RuntimeError('controlled reconstruction error')
        c = FrameCoordinator(tracker(), updater)
        first = inputs(0);first['geometry_inputs'] = {'V/f0/d0': 'points'}
        initial = c.step(**first)['after']['geometry']
        for frame, status in [(1, 'rejected'), (2, 'error'), (3, 'missing')]:
            args = inputs(frame, missing=True)
            if frame != 3:
                args['geometry_inputs'] = {f'V/f{frame}/d0': 'points'}
            result = c.step(**args)
            self.assertEqual(result['updates'][0]['status'], status)
            self.assertEqual(result['after']['geometry'], initial)
            self.assertEqual(result['after']['shapes']['40']['version'], 1)
        self.assertEqual(calls, [0, 1, 2])

    def test_accepted_versions_and_snapshots_are_detached(self):
        shared = {'points': [0]}
        c = FrameCoordinator(tracker(), lambda ctx: GeometryDecision(True, shared))
        for frame in (0, 1):
            args = inputs(frame);args['geometry_inputs'] = {f'V/f{frame}/d0': 'points'}
            result = c.step(**args)
        self.assertEqual(result['after']['geometry']['40']['version'], 2)
        shared['points'].append(99)
        result['after']['geometry']['40']['value']['points'].append(100)
        self.assertEqual(c.snapshot()['geometry']['40']['value'], {'points': [0]})

    def test_empty_frame_ages_tracks_without_inference_or_geometry_loss(self):
        for mode in ('disabled', 'diagnostic', 'active'):
            t = tracker(mode)
            c = FrameCoordinator(t)
            c.step(**inputs(0, missing=mode == 'disabled'))
            before = c.snapshot()
            result = c.step(**inputs(1, 0))
            self.assertEqual(result['assignments'], {})
            self.assertEqual(result['after']['shapes'], before['shapes'])
            self.assertEqual(result['after']['separate_shape_memory'], before['separate_shape_memory'])
            self.assertEqual(t.tracks[0].time_since_update, 1)
            self.assertIsNone(t.matcher.baseline.model.original_output)

    def test_input_validation_does_not_mutate_tracker_and_allows_retry(self):
        t = tracker();c = FrameCoordinator(t)
        args = inputs(0)
        args['detections'][0].detection_data['detection_idx'] = 8
        with self.assertRaises(ValueError):
            c.step(**args)
        self.assertEqual(t.tracks, [])
        c.step(**inputs(0))
        for args in (inputs(0), inputs(1)):
            if args['metadata']['frame_idx'] == 1:
                args['metadata']['timestamp'] = 0
            with self.assertRaises(ValueError):
                c.step(**args)
        c.step(**inputs(1))

    def test_core_error_poisoned_no_partial_retry(self):
        t = tracker();c = FrameCoordinator(t)
        c.step(**inputs(0))
        t.matcher.baseline._greedy_assignment = lambda p: (_ for _ in ()).throw(RuntimeError('controlled matcher failure'))
        with self.assertRaises(RuntimeError):
            c.step(**inputs(1))
        self.assertTrue(c.snapshot()['failed'])
        self.assertEqual(c.snapshot()['last_frame'], 0)
        self.assertEqual(t.matcher.baseline.model.hooks, [])
        with self.assertRaises(RuntimeError):
            c.step(**inputs(2))

    def test_invalid_updater_is_logged_not_accepted(self):
        c = FrameCoordinator(tracker(), lambda ctx: GeometryDecision(True))
        args = inputs(0);args['geometry_inputs'] = {'V/f0/d0': 'points'}
        result = c.step(**args)
        self.assertEqual(result['updates'][0]['status'], 'error')
        self.assertEqual(result['after']['geometry'], {})

    def test_invalid_actual_assignment_stops_before_shape_commit(self):
        t = tracker();c = FrameCoordinator(t)
        original = t.update
        def corrupt(detections, metadata):
            original(detections, metadata)
            t.tracks[-1].history[-1]['detection_idx'] = 999
        t.update = corrupt
        with self.assertRaises(RuntimeError):
            c.step(**inputs(0))
        self.assertEqual(t.matcher.snapshot(), {})
        self.assertTrue(c.snapshot()['failed'])

    def test_unusable_diagnostics_cannot_publish_accepted_state(self):
        class BadCopy:
            def __deepcopy__(self, memo):
                raise ValueError('controlled diagnostic copy failure')
        c = FrameCoordinator(tracker(), lambda ctx: GeometryDecision(True, {'points':[1]}, diagnostics={'bad':BadCopy()}))
        args = inputs(0);args['geometry_inputs'] = {'V/f0/d0':'points'}
        result = c.step(**args)
        self.assertEqual(result['updates'][0]['status'], 'error')
        self.assertEqual(result['after']['geometry'], {})

    def test_future_input_does_not_change_saved_past(self):
        results = []
        for future in (0, 100):
            c = FrameCoordinator(tracker())
            past = c.step(**inputs(0))
            args = inputs(1);args['features']['V/f1/d0'] = feature(future)
            c.step(**args)
            results.append(past)
        self.assertEqual(*results)

    def test_no_reentrant_frame_processing(self):
        holder = {}
        def updater(ctx):
            with self.assertRaises(RuntimeError):
                holder['c'].step(**inputs(1))
            return GeometryDecision(False, reasons=('controlled',))
        c = holder['c'] = FrameCoordinator(tracker(), updater)
        args = inputs(0);args['geometry_inputs'] = {'V/f0/d0': 'points'}
        c.step(**args)


if __name__ == '__main__':
    unittest.main()
