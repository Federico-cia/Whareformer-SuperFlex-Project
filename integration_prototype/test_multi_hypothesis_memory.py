from dataclasses import replace
import tempfile
from pathlib import Path
import json
import unittest
from unittest.mock import patch
import numpy as np
from scipy.spatial import cKDTree
from multi_hypothesis_memory import MultiHypothesisMemory, MultiHypothesisUpdater
from registration_verifier import Verification
from scene_memory import SceneObservation
from test_scene_memory import config


class GeometricTestVerifier:
    def __call__(self, a, b):
        return Verification(float((cKDTree(a).query(b)[0].mean()+cKDTree(b).query(a)[0].mean())/2), 'controlled-test')


class HypothesisTests(unittest.TestCase):
    def setUp(self):
        self.p = np.random.default_rng(4).normal(size=(300, 3)) * [.7, .4, .2]
        self.cfg = config(voxel_size=.005, decay_half_life=100., confirmation_weight=1.5,
                          maximum_predicted_error=.06, minimum_neighbors=1, maximum_pending_states=3,
                          maximum_cells=100000, fuse_after_motion=True)

    def obs(self, i, p=None, t=None, valid=True):
        return SceneObservation(f'k{i}', i, float(i if t is None else t), self.p if p is None else p,
                                valid, 'unknown', '')

    def memory(self, verifier=True):
        return MultiHypothesisMemory('V', '0', self.cfg, GeometricTestVerifier() if verifier else None)

    def test_incompatible_view_is_kept_then_confirmed_after_motion(self):
        m=self.memory()
        a=m.update(self.obs(1)); self.assertEqual(a['status'],'hypothesis_pending')
        b=m.update(self.obs(2)); self.assertTrue(b['shape_changed'])
        before=m.cloud().copy()
        c=m.update(self.obs(3,self.p+[3,0,0]))
        self.assertEqual(len(m.states),2); self.assertFalse(c['shape_changed'])
        np.testing.assert_array_equal(before,m.cloud())
        d=m.update(self.obs(4,self.p+[3,0,0]))
        self.assertTrue(d['promoted']); self.assertTrue(d['shape_changed'])
        self.assertEqual(m.fused_keys,['k1','k2','k3','k4'])
        self.assertTrue(all(s.confirmed for s in m.states.values()))

    def test_weak_and_confirmed_pruning_preserves_shape(self):
        m=self.memory();m.update(self.obs(1));m.update(self.obs(2))
        m.update(self.obs(3,self.p+4)); before=m.cloud().copy()
        e=m.update(self.obs(4,t=2000,valid=False))
        self.assertEqual(len(e['pruned_states']),2)
        self.assertEqual(len(m.states),0);np.testing.assert_array_equal(m.cloud(),before)
        self.assertEqual({r['confirmed'] for r in m.retired_states},{True,False})
        m.update(self.obs(5,self.p+8,t=2001));e=m.update(self.obs(6,self.p+8,t=2002))
        self.assertTrue(e['shape_changed']); self.assertEqual(m.shape_version,2)

    def test_missing_verifier_and_pending_budget(self):
        m=self.memory(False)
        for i in range(1,6):m.update(self.obs(i,self.p+i))
        self.assertEqual(len(m.states),3);self.assertEqual(len(m.cloud()),0)
        self.assertEqual(len(m.retired_states),2)
        self.assertEqual(len(m._views),3)

    def test_confirmed_unregistrable_state_remains_separate(self):
        m=self.memory();m.update(self.obs(1));m.update(self.obs(2)); before=m.cloud().copy()
        m.update(self.obs(3,self.p+3))
        with patch('multi_hypothesis_memory.register_rigid',side_effect=ValueError('no fit')):
            e=m.update(self.obs(4,self.p+3))
        self.assertEqual(e['status'],'confirmed_state_separate')
        self.assertTrue(m.states['k3'].confirmed);self.assertEqual(m.states['k3'].merged_keys,[])
        np.testing.assert_array_equal(m.cloud(),before)
        e=m.update(self.obs(5,self.p+3));self.assertTrue(e['shape_changed'])
        self.assertEqual(m.fused_keys,['k1','k2','k3','k4','k5'])

    def test_causal_failure_atomic_and_state_export(self):
        m=self.memory();m.update(self.obs(1));m.update(self.obs(2));before=m.snapshot()
        with self.assertRaises(ValueError):m.update(self.obs(1))
        self.assertEqual(before,m.snapshot())
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'states.npz';m.export_hypotheses(p)
            with np.load(p,allow_pickle=False) as z:
                self.assertEqual(json.loads(str(z['snapshot_json'])),m.snapshot())
                self.assertTrue(np.isfinite(z['state_0_world_points']).all())

    def test_coordinator_preserves_association_and_old_snapshot(self):
        from frame_coordinator import FrameCoordinator
        from geometry_matcher import GeometryMatcher, GeometryConfig
        from test_frame_coordinator import tracker, inputs
        t=tracker();t.matcher=GeometryMatcher(t.matcher.baseline,'V',GeometryConfig('diagnostic','da_raw_points'))
        c=FrameCoordinator(t,MultiHypothesisUpdater(self.cfg,GeometricTestVerifier()))
        results=[]
        for i in range(2):
            args=inputs(i);key=args['observation_keys'][0]
            args['features']={key:None};args['geometry_inputs']={key:replace(self.obs(i),key=key)}
            results.append(c.step(**args))
        self.assertEqual(results[1]['assignments'],{'V/f1/d0':'40'})
        self.assertEqual(results[0]['after']['geometry']['40']['value'].shape_version,0)
        self.assertEqual(results[1]['after']['geometry']['40']['value'].shape_version,1)

    def test_full_cycle_deferred_fps_publication_and_failure(self):
        from frame_coordinator import FrameCoordinator
        from geometry_matcher import GeometryMatcher,GeometryConfig
        from test_frame_coordinator import tracker,inputs
        from deferred_scene_superflex import DeferredSceneSuperflex,process_request
        from shape_tools.geometry import normalize_shape
        from shape_tools.metrics import descriptors
        with tempfile.TemporaryDirectory() as td:
            t=tracker();t.matcher=GeometryMatcher(t.matcher.baseline,'V',GeometryConfig('active','da_raw_superflex'))
            c=FrameCoordinator(t,MultiHypothesisUpdater(self.cfg,GeometricTestVerifier()),
                              DeferredSceneSuperflex(td,allow_test_results=True))
            def step(i,shift=0):
                args=inputs(i);key=args['observation_keys'][0]
                args['features']={key:None};args['geometry_inputs']={key:replace(self.obs(i,self.p+shift),key=key)}
                return c.step(**args)
            step(0); second=step(1)
            self.assertEqual(second['before']['reconstructions'],{})
            rid=c.snapshot()['pending_reconstructions'][0]
            with self.assertRaises(RuntimeError):step(2)
            with self.assertRaises(FileNotFoundError):c.resolve_reconstructions()
            def controlled(data,folder):
                self.assertEqual(data['normalized'].shape,(4096,3))
                p=normalize_shape(data['normalized'][:1024])
                return p,*descriptors(p)
            process_request(Path(td)/rid,test_backend=controlled)
            c.resolve_reconstructions();old=c.snapshot()['reconstructions']
            self.assertTrue(old)
            third=step(2,4);self.assertEqual(third['before']['reconstructions'],old)
            self.assertEqual(c.snapshot()['pending_reconstructions'],[])
            step(3,4);rid2=c.snapshot()['pending_reconstructions'][0]
            def broken(data,folder):raise RuntimeError('controlled inference failure')
            process_request(Path(td)/rid2,test_backend=broken)
            result=c.resolve_reconstructions()
            self.assertEqual(result[0]['status'],'failed')
            self.assertEqual(c.snapshot()['reconstructions'],old)
            step(4,4)

    def test_legacy_worker_rejected_before_tracker_mutation(self):
        from frame_coordinator import FrameCoordinator
        from geometry_matcher import GeometryMatcher,GeometryConfig
        from test_frame_coordinator import tracker
        t=tracker();t.matcher=GeometryMatcher(t.matcher.baseline,'V',GeometryConfig('active','da_raw_superflex'))
        with self.assertRaisesRegex(ValueError,'FPS'):
            FrameCoordinator(t,MultiHypothesisUpdater(self.cfg,GeometricTestVerifier()),object())
        self.assertEqual(t.tracks,[])

    def test_retry_after_shape_rejection_retains_all_unmerged_views_once(self):
        m=self.memory();m.update(self.obs(1));m.update(self.obs(2))
        original_verify=m._verify
        def deny_shape(a,b):
            if np.linalg.norm(b.mean(0)) < 1e-8:
                return Verification(1.,'controlled-denial'),False
            return original_verify(a,b)
        m._verify=deny_shape
        e=m.update(self.obs(3));self.assertFalse(e['shape_changed'])
        self.assertEqual(m.fused_keys,['k1','k2'])
        # Restore method on the committed instance rather than an older bound copy.
        m.__dict__.pop('_verify')
        e=m.update(self.obs(4));self.assertTrue(e['shape_changed'])
        self.assertEqual(e['fused_observation_keys'],['k3','k4'])
        self.assertEqual(m.fused_keys,['k1','k2','k3','k4'])
        self.assertEqual(m._views,{})

    def test_live_entry_point_publishes_only_after_association(self):
        from multi_hypothesis_pipeline import MultiHypothesisPipeline
        from geometry_matcher import GeometryConfig
        from test_frame_coordinator import tracker,inputs
        pipe=MultiHypothesisPipeline(tracker(),'V',GeometryConfig('diagnostic','da_raw_points'),
                                      self.cfg,GeometricTestVerifier())
        outputs=[]
        for i in range(3):
            args=inputs(i);key=args['observation_keys'][0]
            outputs.append(pipe.step(args['detections'],args['metadata'],[key],{key:None},
                           {key:replace(self.obs(i),key=key)}))
        self.assertEqual(outputs[1]['before']['reconstructions'],{})
        self.assertTrue(outputs[1]['after']['reconstructions'])
        self.assertEqual(outputs[2]['before']['reconstructions'],outputs[1]['after']['reconstructions'])


if __name__=='__main__': unittest.main()
