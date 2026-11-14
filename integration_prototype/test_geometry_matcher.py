"""Local contract tests: original matcher methods, controlled model/tensor double.

The NumPy tensor double is not a Torch or checkpoint equivalence experiment.
"""
import ast
from contextlib import nullcontext
from types import SimpleNamespace
import unittest

import numpy as np

from geometry_matcher import GeometryConfig, GeometryMatcher, REPRESENTATIONS
from test_shape_adapter import SOURCE, feature


class ArrayTensor:
    def __init__(self, value):
        self.value = np.asarray(value)

    def to(self, *args, **kwargs):
        return self

    def detach(self):
        return self

    def cpu(self):
        return self

    def numpy(self):
        return self.value

    def new_tensor(self, value):
        return ArrayTensor(np.array(value, dtype=self.value.dtype))


class ControlledModel:
    def __init__(self, logits):
        self.logits = logits
        self.hooks = []
        self.original_output = self.returned_output = None

    def register_forward_hook(self, hook):
        self.hooks.append(hook)
        return SimpleNamespace(remove=lambda: self.hooks.remove(hook))

    def __call__(self, inputs):
        output = self.original_output = ArrayTensor(self.logits.copy())
        for hook in self.hooks:
            output = hook(self, (inputs,), output)
        self.returned_output = output
        return output


def original_matcher(logits):
    """Use actual original match/greedy/validation source with controlled tensors."""
    tree = ast.parse(SOURCE.read_text(encoding='utf-8'))
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'WhareformerMatcher')
    methods = [n for n in cls.body if isinstance(n, ast.FunctionDef)
               and n.name in ('match', '_greedy_assignment', '_validate_outputs')]

    def softmax(tensor, dim):
        value = tensor.value
        exp = np.exp(value - value.max(axis=dim, keepdims=True))
        return ArrayTensor(exp / exp.sum(axis=dim, keepdims=True))

    env = dict(np=np, torch=SimpleNamespace(no_grad=nullcontext, from_numpy=ArrayTensor,
                                          float32=np.float32, softmax=softmax))
    exec(compile(ast.fix_missing_locations(ast.Module(body=methods, type_ignores=[])), str(SOURCE), 'exec'), env)
    kind = type('OriginalMatcherMethods', (), {name: env[name] for name in ('match', '_greedy_assignment', '_validate_outputs')})
    result = kind()
    result.model, result.device = ControlledModel(np.asarray(logits)), 'cpu'
    result._get_representations = lambda t, d: (t, d)
    result._construct_model_inputs = lambda t, d: np.zeros((len(d), len(t)+1, 2), np.float32)
    return result


class GeometryMatcherTests(unittest.TestCase):
    def make(self, mode='active', weight=0, representation='da_raw_points'):
        base = original_matcher(np.array([[0, -0.1, -0.2]], np.float32))
        wrapper = GeometryMatcher(base, 'V', GeometryConfig(mode, representation, weight=weight, neutral_distance=0.5))
        return wrapper

    def seed(self, wrapper):
        wrapper.set_frame(0, ['seed'], {'seed': feature(0)})
        self.assertEqual(wrapper.match([], [object()], dict(frame_idx=0)), ([], [], [0], None))
        wrapper.commit({'seed': '9'})

    def query(self, wrapper, frame=1):
        wrapper.set_frame(frame, ['x'], {'x': feature(0)})
        return wrapper.match([SimpleNamespace(track_id=9), SimpleNamespace(track_id=8)], [object()], dict(frame_idx=frame))

    def test_disabled_delegates_without_context_or_model_access(self):
        sentinel = object()
        base = SimpleNamespace(match=lambda *args: sentinel)
        wrapper = GeometryMatcher(base, 'V')
        self.assertIs(wrapper.match([], [], {}), sentinel)
        self.assertEqual(wrapper.snapshot(), {})
        with self.assertRaises(RuntimeError):
            wrapper.set_frame(0, [], {})

    def test_diagnostic_and_zero_preserve_original_tensor_and_assignments(self):
        for mode in ('diagnostic', 'active'):
            for rep in REPRESENTATIONS:
                wrapper = self.make(mode, representation=rep)
                self.seed(wrapper)
                before = wrapper.snapshot()
                result = self.query(wrapper)
                self.assertEqual(result, ([], [0, 1], [0], None))
                self.assertIs(wrapper.baseline.model.original_output, wrapper.baseline.model.returned_output)
                np.testing.assert_array_equal(wrapper.last_logits, wrapper.last_score['logits'])
                self.assertEqual(wrapper.snapshot(), before)
                self.assertEqual(wrapper.last_score['evidence']['x', '9'], ('seed',))
                self.assertEqual(wrapper.baseline.model.hooks, [])
                wrapper.commit({'x': 'new_actual_id'})
                self.assertIn('new_actual_id', wrapper.snapshot())

    def test_active_changes_assignment_preserves_new_track_and_input(self):
        wrapper = self.make(weight=2)
        self.seed(wrapper)
        before = wrapper.baseline.model.logits.copy()
        self.assertEqual(self.query(wrapper), ([(0, 0)], [1], [], None))
        self.assertEqual(wrapper.last_score['logits'][0, 0], before[0, 0])
        np.testing.assert_array_equal(wrapper.baseline.model.logits, before)
        self.assertEqual(wrapper.last_score['logits'].dtype, np.float32)

    def test_actual_track_column_and_detection_row_order(self):
        wrapper = self.make(weight=2)
        self.seed(wrapper)
        wrapper.baseline.model.logits = np.zeros((2, 3), np.float32)
        wrapper.set_frame(1, ['missing', 'x'], {'x': feature(0), 'missing': None})
        wrapper.match([SimpleNamespace(track_id=8), SimpleNamespace(track_id=9)], [object(), object()], dict(frame_idx=1))
        np.testing.assert_array_equal(wrapper.last_score['valid'], [[False, False], [False, True]])
        np.testing.assert_array_equal(wrapper.last_score['logits'][0], [0, 0, 0])
        self.assertEqual(wrapper.last_score['track_ids'], ['8', '9'])

    def test_frame_error_aborts_allows_retry(self):
        wrapper = self.make()
        wrapper.set_frame(0, ['x'], {'x': feature(0)})
        with self.assertRaises(ValueError):
            wrapper.match([], [object()], dict(frame_idx=1))
        self.seed(wrapper)

    def test_model_error_removes_hook_and_aborts(self):
        wrapper = self.make()
        self.seed(wrapper)
        wrapper.baseline._greedy_assignment = lambda p: (_ for _ in ()).throw(ValueError('controlled failure'))
        with self.assertRaises(ValueError):
            self.query(wrapper)
        self.assertEqual(wrapper.baseline.model.hooks, [])
        self.assertIsNone(wrapper.last_score)
        wrapper.set_frame(1, ['retry'], {'retry': None})
        wrapper.abort()

    def test_commit_validation_retry_and_lifecycle(self):
        wrapper = self.make()
        self.seed(wrapper)
        with self.assertRaises(RuntimeError):
            wrapper.commit({})
        self.query(wrapper)
        with self.assertRaises(RuntimeError):
            wrapper.set_frame(2, [], {})
        with self.assertRaises(ValueError):
            wrapper.commit({'wrong': '9'})
        wrapper.commit({'x': '9'})
        with self.assertRaises(ValueError):
            self.query(wrapper, frame=1)

    def test_no_track_empty_frame_uses_original_early_return(self):
        wrapper = self.make()
        wrapper.set_frame(0, [], {})
        self.assertEqual(wrapper.match([], [], dict(frame_idx=0)), ([], [], [], None))
        wrapper.commit({})
        self.assertIsNone(wrapper.baseline.model.original_output)

    def test_config_roundtrip_and_invalid_choices(self):
        cfg = GeometryConfig('active', 'moge_superflex', metric='spectrum', weight=1)
        self.assertEqual(GeometryConfig(**cfg.to_dict()), cfg)
        for params in [dict(mode='invalid'), dict(mode='diagnostic', weight=1), dict(representation='other'), dict(weight=-1), dict(capacity=0)]:
            with self.assertRaises(ValueError):
                GeometryConfig(**params)


if __name__ == '__main__':
    unittest.main()
