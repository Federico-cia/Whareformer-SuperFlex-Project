"""Local deferred protocol/causality tests; NO SuperFlex neural execution."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from cloud_updater import ObservedCloudUpdater
from deferred_superflex import DeferredSuperflex, process_request, validate_request
from frame_coordinator import FrameCoordinator
from geometry_matcher import GeometryConfig, GeometryMatcher
from shape_tools.geometry import normalize_shape
from shape_tools.metrics import descriptors
from test_cloud_memory import surface
from test_cloud_updater import payload
from test_frame_coordinator import tracker, inputs


def feature_tuple(offset=0):
    p=normalize_shape(surface(1024)*[1,1+offset,1])
    return (p,*descriptors(p))


class DeferredTests(unittest.TestCase):
    def coordinator(self, root, allow=True):
        t=tracker();t.matcher=GeometryMatcher(t.matcher.baseline,'V',GeometryConfig('active','moge_superflex'))
        return FrameCoordinator(t,ObservedCloudUpdater(),DeferredSuperflex(root,allow_test_results=allow))

    def frame(self,c,n):
        args=inputs(n);args['features'][f'V/f{n}/d0']=feature_tuple()
        args['geometry_inputs']={f'V/f{n}/d0':payload()}
        return c.step(**args)

    def folder(self,c,root):
        return Path(root)/c.snapshot()['pending_reconstructions'][0]

    def test_export_normalization_pause_publish_and_future_evidence(self):
        with tempfile.TemporaryDirectory() as root:
            c=self.coordinator(root);first=self.frame(c,0)
            self.assertEqual(first['after']['reconstructions'],{})
            with self.assertRaises(RuntimeError):self.frame(c,1)
            with self.assertRaises(FileNotFoundError):c.resolve_reconstructions()
            folder=self.folder(c,root);req=validate_request(folder)
            with np.load(folder/'input.npz',allow_pickle=False) as z:
                np.testing.assert_allclose(z['normalized_points']*z['scale']+z['translation'],z['object_points'][z['sample_indices']])
            process_request(folder,test_backend=lambda r,p:feature_tuple(.5))
            self.assertEqual(c.resolve_reconstructions()[0]['status'],'ready')
            self.assertEqual(first['after']['reconstructions'],{})
            args=inputs(1);args['features']['V/f1/d0']=feature_tuple()
            c.step(**args)
            evidence=c.matcher.last_score['evidence']['V/f1/d0','40']
            self.assertEqual(evidence,('reconstruction/'+req['request_id'],))
            np.testing.assert_array_equal(c.matcher.last_score['logits'],c.matcher.last_logits)

    def test_failed_result_keeps_old_shape_and_observed_points(self):
        with tempfile.TemporaryDirectory() as root:
            c=self.coordinator(root);self.frame(c,0)
            process_request(self.folder(c,root),test_backend=lambda r,p:feature_tuple())
            c.resolve_reconstructions();before=c.snapshot()['reconstructions']
            admit=dict(accepted=True,reasons=[],rotation=np.eye(3).tolist(),translation=[0,0,0])
            with patch('cloud_updater.register_rigid',return_value=admit):self.frame(c,1)
            def fail(r,p):raise RuntimeError('controlled worker failure')
            process_request(self.folder(c,root),test_backend=fail)
            self.assertEqual(c.resolve_reconstructions()[0]['status'],'failed')
            self.assertEqual(c.snapshot()['reconstructions'],before)
            self.assertEqual(c.snapshot()['geometry']['40']['version'],2)

    def test_test_outputs_rejected_by_default(self):
        with tempfile.TemporaryDirectory() as root:
            c=self.coordinator(root,allow=False);self.frame(c,0)
            process_request(self.folder(c,root),test_backend=lambda r,p:feature_tuple())
            with self.assertRaises(ValueError):c.resolve_reconstructions()
            self.assertTrue(c.snapshot()['pending_reconstructions'])
            self.assertEqual(c.snapshot()['reconstructions'],{})

    def test_tampered_input_and_mismatched_result_are_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            c=self.coordinator(root);self.frame(c,0);folder=self.folder(c,root)
            process_request(folder,test_backend=lambda r,p:feature_tuple())
            path=folder/'result.json';result=json.loads(path.read_text());result['request_id']='wrong'
            path.write_text(json.dumps(result))
            with self.assertRaises(ValueError):c.resolve_reconstructions()
            with (folder/'input.npz').open('ab') as stream:stream.write(b'tamper')
            with self.assertRaises(ValueError):validate_request(folder)

    def test_stale_cloud_rejected_and_replay_reuses_exact_request(self):
        with tempfile.TemporaryDirectory() as root:
            c=self.coordinator(root);self.frame(c,0);folder=self.folder(c,root)
            process_request(folder,test_backend=lambda r,p:feature_tuple())
            versions=c.snapshot()['geometry'];versions['40']['version']=2
            with self.assertRaises(ValueError):c.reconstructor.collect([folder.name],0,versions)
            replay=self.coordinator(root);self.frame(replay,0)
            self.assertEqual(self.folder(replay,root),folder)
            replay.resolve_reconstructions()
            self.assertFalse(replay.snapshot()['pending_reconstructions'])

    def test_rejected_update_creates_no_request_and_mesh_not_added_to_cloud(self):
        with tempfile.TemporaryDirectory() as root:
            c=self.coordinator(root);self.frame(c,0)
            before=c.snapshot()['geometry']['40']['value'].memory.cloud()
            process_request(self.folder(c,root),test_backend=lambda r,p:feature_tuple(4))
            c.resolve_reconstructions()
            np.testing.assert_array_equal(before,c.snapshot()['geometry']['40']['value'].memory.cloud())
            with patch('cloud_updater.register_rigid',return_value=dict(accepted=False,reasons=['controlled'])):
                self.frame(c,1)
            self.assertEqual(c.snapshot()['pending_reconstructions'],[])
            self.assertEqual(len(list(Path(root).iterdir())),1)

    def test_multiple_results_published_together_only_after_all_are_available(self):
        with tempfile.TemporaryDirectory() as root:
            c=self.coordinator(root)
            args=inputs(0,2)
            args['features']={k:feature_tuple() for k in args['observation_keys']}
            args['geometry_inputs']={k:payload() for k in args['observation_keys']}
            c.step(**args)
            requests=c.snapshot()['pending_reconstructions']
            process_request(Path(root)/requests[0],test_backend=lambda r,p:feature_tuple())
            with self.assertRaises(FileNotFoundError):c.resolve_reconstructions()
            self.assertEqual(c.snapshot()['reconstructions'],{})
            process_request(Path(root)/requests[1],test_backend=lambda r,p:feature_tuple())
            c.resolve_reconstructions()
            self.assertEqual(set(c.snapshot()['reconstructions']),{'40','41'})

    def test_production_worker_plumbing_with_mocked_gpu_pipeline(self):
        with tempfile.TemporaryDirectory() as root:
            c=self.coordinator(root,allow=False);self.frame(c,0);folder=self.folder(c,root)
            def fake_gpu(data,stage,config):
                from shape_tools.pipeline import item_id
                from shape_tools.comparison import file_hash
                with np.load(stage/'cloud.npz',allow_pickle=False) as z:
                    np.testing.assert_array_equal(z['camera_points'],c.snapshot()['geometry']['40']['value'].memory.cloud())
                (stage/'surface.ply').write_text('controlled placeholder; mesh loader mocked')
                source=config['sources'][0];key=item_id(data['observations'][0])
                record={key:dict(status='ready',artifacts=dict(surface=dict(path='surface.ply',sha256=file_hash(stage/'surface.ply'))))}
                (stage/f'superflex_{source}_index.json').write_text(json.dumps(record))
                (stage/'superflex_backend.json').write_text(json.dumps({'fixture':'mocked GPU pipeline'}))
            cfg=dict(c.reconstructor.config.__dict__,checkpoint='trusted-checkpoint',config='trusted-config')
            with patch('deferred_superflex.pipeline.superflex',side_effect=fake_gpu), patch('deferred_superflex.comparison.load_features',return_value=feature_tuple()):
                result=process_request(folder,runtime=cfg)
            self.assertEqual(result['status'],'ready')
            self.assertEqual(result['production_backend'],{'fixture':'mocked GPU pipeline'})
            c.resolve_reconstructions()


if __name__=='__main__':unittest.main()
