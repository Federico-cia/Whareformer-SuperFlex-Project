"""Common runner, point-control and telemetry tests using controlled tracking."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from experiment_runner import ExperimentRunner, Variant, FrameData, aggregate_reports
from deferred_superflex import process_request
from test_deferred_superflex import feature_tuple
from test_cloud_updater import payload
from test_frame_coordinator import tracker, inputs
from summarize_experiments import write_tables


def factory():
    t=tracker();t.matcher=t.matcher.baseline
    return t


def frames(n=2):
    result=[]
    for frame in range(n):
        args=inputs(frame)
        keys=args['observation_keys']
        representations={rep:{k:feature_tuple() for k in keys} for rep in ['da_raw_points','da_raw_superflex','moge_points','moge_superflex']}
        clouds={source:{k:payload(source=source) for k in keys} for source in ['da','moge']}
        result.append(FrameData(args['detections'],args['metadata'],keys,representations,clouds))
    return result


def worker(folder):
    return process_request(folder,test_backend=lambda req,out:feature_tuple(.3))


class ExperimentTests(unittest.TestCase):
    def test_all_five_modes_isolated_zero_exact_and_same_cloud_budget(self):
        variants=[Variant(method,method,'moge') for method in ['W0','G0','S-separata','S-accumulo','P-accumulo']]
        with tempfile.TemporaryDirectory() as root:
            runner=ExperimentRunner(factory,'V',variants,root,worker=worker,allow_test_results=True)
            admit=dict(accepted=True,reasons=[],rotation=np.eye(3).tolist(),translation=[0,0,0])
            with patch('cloud_updater.register_rigid',return_value=admit):report=runner.run(frames())
            for item in report['variants']:
                self.assertEqual(item['status'],'completed',item)
                self.assertTrue(item['zero_baseline_exact'])
                self.assertIsNone(item['tracking_metrics'])
                self.assertEqual(item['counts']['detections'],2)
            shapes=[]
            for execution in runner.executions:
                if execution.variant.accumulate:
                    state=execution.coordinator.snapshot()['geometry']['40']['value']
                    shapes.append(state.summary()['cloud_sha256'])
                    self.assertEqual(execution.summary()['counts']['accepted_fusions'],1)
            self.assertEqual(len(set(shapes)),1)
            point=runner.executions[-1]
            self.assertTrue(point.coordinator.matcher.last_score['evidence']['V/f1/d0','40'][0].startswith('accumulated_points/'))
            self.assertGreater(point.rows[-1]['raw_observed_point_bytes'],0)
            self.assertGreater(point.rows[-1]['descriptor_payload_bytes'],0)
            self.assertEqual(len({id(e.coordinator.tracker) for e in runner.executions}),5)
            runner.write(Path(root)/'all_variant_reports',report)
            write_tables([Path(root)/'all_variant_reports/summary.json'],Path(root)/'all_variant_table')
            with self.assertRaises(RuntimeError):runner.run(frames())

    def test_missing_shapes_clouds_and_partial_results_have_denominators(self):
        with tempfile.TemporaryDirectory() as root:
            data=frames(1);data[0].features={};data[0].cloud_inputs={}
            runner=ExperimentRunner(factory,'V',[Variant('points','P-accumulo','moge')],root)
            report=runner.run(data)['variants'][0]
            self.assertEqual(report['counts']['detections'],1)
            self.assertEqual(report['counts']['features_available'],0)
            self.assertEqual(report['counts']['update_statuses'],{'missing':1})
            self.assertIsNone(report['zero_baseline_exact'])
            self.assertIsNone(report['tracking_metrics'])

    def test_failed_variant_does_not_hide_or_stop_others(self):
        with tempfile.TemporaryDirectory() as root:
            data=frames(1);data[0].features['moge_superflex']['V/f0/d0']=(None,np.array([-1.]),None)
            variants=[Variant('bad','S-separata','moge'),Variant('baseline','W0')]
            report=ExperimentRunner(factory,'V',variants,root).run(data)
            self.assertEqual([v['status'] for v in report['variants']],['failed','completed'])
            self.assertEqual(report['variants'][0]['failed_frame_index'],0)

    def test_pending_replay_costs_and_report_export(self):
        with tempfile.TemporaryDirectory() as root:
            root=Path(root);cache=root/'cache';variant=Variant('S','S-accumulo','moge')
            first=ExperimentRunner(factory,'V',[variant],cache,allow_test_results=True,provenance={'input_manifest_sha256':'0'*64})
            report=first.run(frames(1));summary=report['variants'][0]
            self.assertEqual(summary['status'],'waiting_for_results')
            self.assertEqual(len(summary['counts']['pending_requests']),1)
            self.assertGreater(summary['peak_raw_point_payload_bytes'],0)
            first.write(root/'partial',report)
            second=ExperimentRunner(factory,'V',[variant],cache,worker=worker,allow_test_results=True,provenance={'input_manifest_sha256':'0'*64})
            complete=second.run(frames(1));summary=complete['variants'][0]
            self.assertEqual(summary['status'],'completed')
            self.assertEqual(summary['attempts_including_replays'],2)
            self.assertGreaterEqual(summary['cumulative_setup_run_seconds'],summary['current_attempt_wall_seconds'])
            second.write(root/'complete',complete)
            self.assertEqual(json.loads((root/'complete/summary.json').read_text())['expected_frames'],1)
            with self.assertRaises(FileExistsError):second.write(root/'complete',complete)

    def test_factory_model_sharing_and_invalid_configs_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            shared=factory();model=shared.matcher.model
            def reused_model():
                t=factory();t.matcher.model=model;return t
            with self.assertRaises(ValueError):ExperimentRunner(reused_model,'V',[Variant('a','W0'),Variant('b','W0')],root)
            for kwargs in [dict(name='../bad',method='W0'),dict(name='a',method='G0',weight=1),dict(name='a',method='unknown')]:
                with self.assertRaises(ValueError):Variant(**kwargs)

    def test_aggregate_separates_provenance_controls_and_unverified_reports(self):
        with tempfile.TemporaryDirectory() as root:
            root=Path(root);paths=[]
            for i,provenance in enumerate([{}, {}, {'input_manifest_sha256':'a'}, {'input_manifest_sha256':'b'}]):
                runner=ExperimentRunner(factory,'V',[Variant('base','W0')],root/f'cache{i}',provenance=provenance)
                report=runner.run(frames(1));runner.write(root/f'out{i}',report)
                paths.append(root/f'out{i}/summary.json')
            self.assertEqual(len(aggregate_reports(paths)),4)

    def test_table_keeps_unscored_metrics_blank_and_zero_denominators_missing(self):
        import csv
        with tempfile.TemporaryDirectory() as root:
            root=Path(root)
            runner=ExperimentRunner(factory,'V',[Variant('baseline','W0')],root/'cache')
            report=runner.run(frames(1));runner.write(root/'run',report)
            write_tables([root/'run/summary.json'],root/'table')
            with (root/'table/comparison.csv').open() as stream:row=next(csv.DictReader(stream))
            self.assertEqual(row['idf1_percent'],'')
            self.assertEqual(row['pair_coverage_percent'],'')
            self.assertEqual(row['feature_coverage_percent'],'')
            self.assertEqual(row['detections'],'1')

    def test_corrupt_worker_result_is_reported_without_hiding_other_variants(self):
        with tempfile.TemporaryDirectory() as root:
            def broken_worker(folder):
                (folder/'result.json').write_text('{broken')
                return {'status':'failed'}
            runner=ExperimentRunner(factory,'V',[Variant('S','S-accumulo','moge'),Variant('base','W0')],root,worker=broken_worker)
            report=runner.run(frames(1))
            self.assertEqual(report['variants'][0]['status'],'failed')
            self.assertEqual(report['variants'][0]['counts']['unreadable_worker_results'],1)
            self.assertEqual(report['variants'][1]['status'],'completed')


if __name__=='__main__':unittest.main()
