"""Original metric convention checks; IDF1 cases require actual motmetrics."""
from copy import deepcopy
import importlib.util
from pathlib import Path
import tempfile
import unittest

from tracking_evaluation import EvaluationPolicy, OriginalTrackingEvaluator, results_from_rows, evaluate_report
from experiment_runner import ExperimentRunner, Variant
from evaluate_experiments import evaluate_directory
from test_experiment_runner import factory,frames


SOURCE=Path(__file__).resolve().parents[1]/'Whareformer-repo/src'
HAS_MOTMETRICS=importlib.util.find_spec('motmetrics') is not None


def predictions(switch=False):
    return {f'frame_{i:010d}':dict(track_ids=[0 if i==0 or not switch else 1],track_obj_names=['board'],
            track_bboxes=[[0,0,10,10]],track_3d_locs=[[0.,0.,1.]]) for i in [0,60]}


class TrackingEvaluationTests(unittest.TestCase):
    def evaluator(self):return OriginalTrackingEvaluator(SOURCE,EvaluationPolicy(60,60,'diagnostic_prefix'))

    def test_original_pcl_bins_and_supported_mean_are_distinct(self):
        result=self.evaluator().pcl(predictions())
        self.assertEqual(result['supported_timescales'],1)
        self.assertAlmostEqual(result['mpcl_percent'],100/145)
        self.assertEqual(result['mpcl_supported_timescales_percent'],100)

    def test_prefix_horizon_cannot_forward_fill_unprocessed_future(self):
        evaluator=OriginalTrackingEvaluator(SOURCE,EvaluationPolicy(60,120,'diagnostic_prefix'))
        with self.assertRaises(ValueError):evaluator.pcl(predictions())

    def test_source_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'scripts';path.mkdir();(path/'evaluate.py').write_text('modified')
            with self.assertRaises(ValueError):OriginalTrackingEvaluator(folder,EvaluationPolicy(60,60,'diagnostic_prefix'))

    def test_actual_export_order_and_assignment_binding(self):
        row=dict(frame_index=0,detections=2,assignments={'a':'5','b':'2'},evaluation_observations=[
            dict(observation_key='a',track_id='5',obj_name='board',bbox=[0,0,10,10],xyz=[0,0,1]),
            dict(observation_key='b',track_id='2',obj_name='knife',bbox=[10,0,10,10],xyz=[1,0,1])])
        self.assertEqual(results_from_rows([row])['frame_0000000000']['track_ids'],[2,5])
        row['evaluation_observations'][0]['track_id']='7'
        with self.assertRaises(ValueError):results_from_rows([row])

    def test_incomplete_variants_never_scored(self):
        report=dict(expected_frames=10,variants=[dict(config=dict(name='partial'),status='waiting_for_results',counts=dict(frames=1))])
        scored=evaluate_report(report,{},self.evaluator())
        self.assertEqual(scored['variants'][0]['evaluation_status'],'not_scored_incomplete')
        self.assertIsNone(scored['variants'][0]['tracking_metrics'])

    def test_empty_observations_not_successful_zero(self):
        results={'frame_0000000060':dict(track_ids=[],track_obj_names=[],track_bboxes=[],track_3d_locs=[])}
        scored=self.evaluator().score(results,require_idf1=False)
        self.assertIsNone(scored['idf1_percent']);self.assertIsNone(scored['mpcl_percent'])

    @unittest.skipUnless(HAS_MOTMETRICS,'Real motmetrics evaluated in isolated HPC job')
    def test_real_idf1_identity_switch(self):
        evaluator=self.evaluator()
        self.assertAlmostEqual(evaluator.score(predictions())['idf1_percent'],100)
        self.assertAlmostEqual(evaluator.score(predictions(switch=True))['idf1_percent'],50)

    @unittest.skipUnless(HAS_MOTMETRICS,'Real motmetrics evaluated in isolated HPC job')
    def test_common_runner_to_actual_metric_report(self):
        with tempfile.TemporaryDirectory() as folder:
            data=frames(2)
            for frame in data:
                for detection in frame.detections:
                    detection.detection_data.update(obj_name='board',bbox=[0,0,10,10],loc=[0.,0.,1.])
            runner=ExperimentRunner(factory,'V',[Variant('base','W0')],folder)
            report=runner.run(data)
            evaluator=OriginalTrackingEvaluator(SOURCE,EvaluationPolicy(60,1,'diagnostic_prefix'))
            scored=evaluate_report(report,{'base':runner.executions[0].rows},evaluator)
            self.assertEqual(scored['variants'][0]['evaluation_status'],'scored')
            self.assertEqual(scored['variants'][0]['tracking_metrics']['idf1_percent'],100)
            runner.write(Path(folder)/'raw',report)
            disk=evaluate_directory(Path(folder)/'raw',Path(folder)/'scored',SOURCE,EvaluationPolicy(60,1,'diagnostic_prefix'))
            self.assertEqual(disk['variants'][0]['tracking_metrics']['idf1_percent'],100)
            self.assertTrue((Path(folder)/'scored/base_pcl.csv').is_file())
            tampered=deepcopy(runner.executions[0].rows);tampered[0]['evaluation_timestamp']=123.
            self.assertEqual(evaluate_report(report,{'base':tampered},evaluator)['variants'][0]['evaluation_status'],'failed')


if __name__=='__main__':unittest.main()
