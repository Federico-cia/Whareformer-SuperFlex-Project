"""Meaningful contract checks: labels, causal boundaries and identity leakage."""
import unittest

from training_enrichment import GeometryHistory, benchmark_target, validate_sample_rows


class EnrichmentTests(unittest.TestCase):
    def test_new_and_existing_labels_follow_candidate_order(self):
        self.assertEqual(benchmark_target('pan', ['cup', 'pan']), 2)
        self.assertEqual(benchmark_target('knife', ['cup', 'pan']), 0)
        with self.assertRaises(ValueError):
            benchmark_target('pan', ['pan', 'pan'])

    def test_geometry_enters_only_after_the_whole_frame(self):
        history = GeometryHistory()
        self.assertEqual(history.before([7], 10), [[]])
        history.commit(10, [(7, 'view10')])
        with self.assertRaises(ValueError):
            history.before([7], 10)
        self.assertEqual(history.before([7, 2], 11), [['view10'], []])
        with self.assertRaises(ValueError):
            history.commit(10, [])

    def test_audit_rejects_future_or_wrong_identity_history(self):
        sample = dict(observation_key='query', frame_index=20,
            benchmark_identity='pan', candidate_names=['pan'], candidate_track_ids=[0],
            target_class=1, candidate_geometry_keys=[['past']])
        catalogue = {'query': {}, 'past': {'source_observation': dict(frame_index=19, category='pan')}}
        self.assertEqual(validate_sample_rows([sample], catalogue)['samples'], 1)
        catalogue['past']['source_observation']['category'] = 'cup'
        with self.assertRaises(ValueError):
            validate_sample_rows([sample], catalogue)
        catalogue['past']['source_observation'].update(category='pan', frame_index=20)
        with self.assertRaises(ValueError):
            validate_sample_rows([sample], catalogue)


if __name__ == '__main__':
    unittest.main()
