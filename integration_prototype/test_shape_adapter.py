"""Boundary tests; no pretrained logits or real tracking performance claimed."""
import ast
from pathlib import Path
import unittest

import numpy as np

from shape_adapter import ShapeLogitAdapter, FusionConfig
from shape_tools.memory import MemoryConfig

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'Whareformer-repo/src/tracking/tracker/matcher/matcher_types.py'


def original_assignment():
    """Compile the exact original pure NumPy method, without importing Torch."""
    tree = ast.parse(SOURCE.read_text(encoding='utf-8'))
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'WhareformerMatcher')
    method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == '_greedy_assignment')
    module = ast.Module(body=[method], type_ignores=[])
    env = {'np': np}
    exec(compile(ast.fix_missing_locations(module), str(SOURCE), 'exec'), env)
    return lambda probs: env['_greedy_assignment'](None, probs)


def softmax(logits):
    x = logits - logits.max(axis=1, keepdims=True)
    p = np.exp(x)
    return p / p.sum(axis=1, keepdims=True)


def feature(value):
    return None, np.array([value, value + 1.0]), np.ones(3)


class AdapterTests(unittest.TestCase):
    def adapter(self, weight=0, threshold=0):
        return ShapeLogitAdapter('V', MemoryConfig('diagnostic', capacity=2), FusionConfig(weight, threshold))

    def seed(self, adapter):
        adapter.score(0, ['first'], {'first': feature(0)}, [], np.zeros((1, 1), dtype=np.float32))
        adapter.commit({'first': '9'})

    def test_zero_preserves_logits_and_original_assignment(self):
        assign = original_assignment()
        rng = np.random.default_rng(13)
        for n in (1, 2, 7, 20):
            for tracks in (1, 3, 10):
                for _ in range(10):
                    a = self.adapter()
                    self.seed(a)
                    keys = [f'd{i}' for i in range(n)]
                    ids = ['9'] + [f't{i}' for i in range(tracks - 1)]
                    x = rng.normal(size=(n, tracks + 1)).astype(np.float32)
                    y = a.score(1, keys, {k: feature(i) for i, k in enumerate(keys)}, ids, x)['logits']
                    np.testing.assert_array_equal(x, y)
                    self.assertEqual(assign(softmax(x)), assign(softmax(y)))

    def test_nonzero_changes_existing_competition(self):
        a = self.adapter(2, 0.5); self.seed(a)
        x = np.array([[0, -0.1]], dtype=np.float32)
        result = a.score(1, ['second'], {'second': feature(0)}, ['9'], x)
        self.assertEqual(result['logits'][0, 0], x[0, 0])
        self.assertEqual(np.argmax(result['logits']), 1)
        self.assertNotEqual(softmax(x)[0, 0], softmax(result['logits'])[0, 0])

    def test_missing_shapes_and_empty_track_memory(self):
        a = self.adapter(3, 0.5); self.seed(a)
        x = np.zeros((2, 3), dtype=np.float32)
        r = a.score(1, ['known', 'missing'], {'known': feature(0), 'missing': None}, ['unknown', '9'], x)
        np.testing.assert_array_equal(r['logits'][1], x[1])
        np.testing.assert_array_equal(r['logits'][:, 1], x[:, 1])
        self.assertTrue(r['valid'][0, 1])

    def test_order_and_no_update_before_commit(self):
        a = self.adapter(1, 0.5); self.seed(a)
        before = a.snapshot()
        r = a.score(1, ['b', 'a'], {'a': feature(1), 'b': feature(0)}, ['other', '9'], np.zeros((2, 3)))
        self.assertEqual(r['observation_keys'], ['b', 'a'])
        self.assertEqual(a.snapshot(), before)
        self.assertEqual(r['evidence']['b', '9'], ('first',))
        self.assertEqual(r['evidence']['a', '9'], ('first',))
        a.commit({'b': '9', 'a': 'actual_new_id'})
        self.assertEqual(a.snapshot()['actual_new_id'][0]['observation_key'], 'a')

    def test_future_continuation_does_not_change_past(self):
        outputs = []
        for future in (0, 100):
            a = self.adapter(1, 0.5); self.seed(a)
            r = a.score(1, ['now'], {'now': feature(0.3)}, ['9'], np.zeros((1, 2)))
            a.commit({'now': '9'})
            a.score(2, ['future'], {'future': feature(future)}, ['9'], np.zeros((1, 2)))
            outputs.append(r['logits'])
        np.testing.assert_array_equal(*outputs)

    def test_abort_and_noncausal_frame_rejected(self):
        a = self.adapter(); self.seed(a)
        with self.assertRaises(ValueError):
            a.score(0, [], {}, ['9'], np.zeros((0, 2)))
        a.score(1, ['x'], {'x': feature(0)}, ['9'], np.zeros((1, 2)))
        a.abort()
        a.score(1, ['x'], {'x': feature(0)}, ['9'], np.zeros((1, 2)))
        a.commit({'x': '9'})

    def test_input_errors_do_not_open_transaction(self):
        a = self.adapter()
        with self.assertRaises(ValueError):
            a.score(0, ['x'], {'y': None}, [], np.zeros((1, 1)))
        a.score(0, ['x'], {'x': None}, [], np.zeros((1, 1)))
        a.commit({'x': 'new'})


if __name__ == '__main__':
    unittest.main()
