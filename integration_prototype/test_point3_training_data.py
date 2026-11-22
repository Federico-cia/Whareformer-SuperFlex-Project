import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from attach_scene_reconstructions import attach
from point3_training_data import AccumulatedTrainingData


class TrainingExportTests(unittest.TestCase):
    def fixture(self, root):
        np.savez_compressed(root / 'training_inputs.npz', input=np.arange(3), label=np.array([0, 1]))
        np.savez_compressed(root / 'observed.npz', points=np.zeros((1024, 3)), d2=np.zeros(16384),
                            spectrum=np.zeros(3), completed_by_superflex=False)
        digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
        spec = dict(path='observed.npz', sha256=digest(root / 'observed.npz'))
        version = dict(track_id='1', shape_version=1, last_update_frame=10,
                       points=spec, superflex_input=dict(path='shapes/memory.npz', sha256='a' * 64))
        row = dict(observation_key='V/q', frame_index=20, target_class=1, query=spec,
                   numerical_input_key='input', numerical_label_key='label', candidate_track_ids=[1],
                   candidates=[dict(track_id=1, memory=version)])
        (root / 'versions.json').write_text(json.dumps([version]))
        (root / 'examples.json').write_text(json.dumps([row]))
        return row, version

    def test_missing_geometry_is_masked_and_labels_unchanged(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            row, version = self.fixture(root)
            data = AccumulatedTrainingData(root).example('V/q')
            np.testing.assert_array_equal(data['original_label'], [0, 1])
            self.assertTrue(data['geometry_available'][0])
            row['query'] = None
            (root / 'examples.json').write_text(json.dumps([row]))
            self.assertFalse(AccumulatedTrainingData(root).example('V/q')['geometry_available'][0])

    def test_current_frame_memory_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            row, version = self.fixture(root)
            version['last_update_frame'] = row['frame_index']
            (root / 'examples.json').write_text(json.dumps([row]))
            with self.assertRaisesRegex(ValueError, 'Current/future'):
                AccumulatedTrainingData(root).example('V/q')

    def test_attachment_excludes_test_doubles_and_preserves_missing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            row, version = self.fixture(root)
            folder = root / 'reconstructions' / 'memory'
            folder.mkdir(parents=True)
            result = dict(input_sha256='a' * 64, shape_version=1, backend='test-double', status='ready',
                          features=dict(path='features.npz', sha256='b' * 64))
            (folder / 'result.json').write_text(json.dumps(result))
            with self.assertRaisesRegex(ValueError, 'Test reconstruction'):
                attach(root)
            result['backend'] = 'superflex'; result['status'] = 'failed'
            (folder / 'result.json').write_text(json.dumps(result))
            report = attach(root)
            self.assertEqual(report['failed_versions'], 1)
            self.assertEqual(report['candidate_reconstructions_attached'], 0)
            rows = json.loads((root / 'examples_with_reconstructions.json').read_text())
            self.assertIsNone(rows[0]['candidates'][0]['reconstruction'])
            self.assertEqual(rows[0]['candidates'][0]['memory'], version)


if __name__ == '__main__':
    unittest.main()
