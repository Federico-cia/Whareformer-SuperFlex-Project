"""Connection tests; synthetic geometry and controlled tracking, no real claim."""
from copy import deepcopy
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from cloud_memory import radius
from cloud_updater import CloudUpdateConfig, ObservedCloudInput, ObservedCloudUpdater, load_observed_cloud, cloud_hash
from frame_coordinator import FrameCoordinator, UpdateContext
from test_cloud_memory import surface
from test_frame_coordinator import tracker, inputs


def payload(p=None, source='moge', **kwargs):
    values=dict(points=surface() if p is None else p, source=source,
                coordinate_convention='camera optical coordinates', scale_convention='synthetic common units',
                observed_only=True, provenance={'fixture':'synthetic observed surface'})
    values.update(kwargs)
    return ObservedCloudInput(**values)


class CloudUpdaterTests(unittest.TestCase):
    def coordinator(self):
        return FrameCoordinator(tracker(), ObservedCloudUpdater())

    def step(self, c, frame, item):
        args=inputs(frame)
        args['geometry_inputs']={f'V/f{frame}/d0':item}
        return c.step(**args)

    def test_initialize_then_actual_rigid_registration_on_known_transform(self):
        c=self.coordinator();p=surface()
        first=self.step(c,0,payload(p))
        self.assertEqual(first['updates'][0]['diagnostics']['operation'],'initialize')
        self.assertIsNone(first['updates'][0]['diagnostics']['registration'])
        a=.47;r=np.array([[np.cos(a),-np.sin(a),0],[np.sin(a),np.cos(a),0],[0,0,1.]])
        q=p@r+[.3,-.2,.4]
        second=self.step(c,1,payload(q))
        event=second['updates'][0]
        self.assertEqual(event['status'],'accepted',event)
        decision=event['diagnostics']['registration']
        moved=q@np.asarray(decision['rotation'])+decision['translation']
        error=np.sqrt(np.mean(np.sum((moved-p)**2,axis=1)))/radius(p)
        self.assertLess(error,.03)
        state=second['after']['geometry']['40']['value']
        self.assertEqual(state.memory.snapshot()['version'],2)
        self.assertEqual(len(state.memory.cloud()),4096)
        self.assertEqual(len(state.summary()['provenance']),2)

    def test_actual_incompatible_cloud_rejected_preserves_valid_points(self):
        c=self.coordinator();first=self.step(c,0,payload())
        before=first['after']['geometry']['40']['value'].summary()
        other=np.random.default_rng(1).normal(size=(3000,3))*[.3,.3,1.5]
        result=self.step(c,1,payload(other))
        self.assertEqual(result['updates'][0]['status'],'rejected')
        self.assertFalse(result['updates'][0]['diagnostics']['registration']['accepted'])
        self.assertEqual(result['after']['geometry']['40']['value'].summary(),before)
        self.assertEqual(result['after']['geometry']['40']['version'],1)
        # Separate observation shapes can advance even when fusion is refused.
        self.assertEqual(result['after']['shapes']['40']['version'],2)

    def test_sources_pose_conventions_and_completions_not_mixed(self):
        for wrong in [payload(source='da'),payload(observed_only=False),payload(coordinate_convention=''),
                      payload(points=np.zeros((100,3)))]:
            c=self.coordinator()
            result=self.step(c,0,wrong)
            self.assertEqual(result['updates'][0]['status'],'error')
            self.assertEqual(result['after']['geometry'],{})
        c=self.coordinator();self.step(c,0,payload())
        for frame,item in [(1,payload(scale_convention='different units')),
                           (2,payload(coordinate_convention='different axes'))]:
            result=self.step(c,frame,item)
            self.assertEqual(result['updates'][0]['status'],'error')
            self.assertEqual(result['after']['geometry']['40']['version'],1)

    def test_pure_updater_does_not_mutate_prior_or_input(self):
        updater=ObservedCloudUpdater();p=payload()
        ctx=UpdateContext('V','moge_superflex',0,'a','40',p,None)
        first=updater(ctx);prior=dict(version=1,value=first.value)
        before=first.value.summary();input_copy=p.points.copy()
        rejection=dict(accepted=False,reasons=['controlled_rejection'])
        with patch('cloud_updater.register_rigid',return_value=rejection):
            decision=updater(UpdateContext('V','moge_superflex',1,'b','40',p,prior))
        self.assertFalse(decision.accepted)
        self.assertEqual(first.value.summary(),before)
        np.testing.assert_array_equal(p.points,input_copy)

    def test_budget_and_provenance_with_controlled_admission(self):
        c=FrameCoordinator(tracker(),ObservedCloudUpdater(CloudUpdateConfig(views=3,points_per_view=100)))
        admit=dict(accepted=True,reasons=[],rotation=np.eye(3).tolist(),translation=[0,0,0])
        with patch('cloud_updater.register_rigid',return_value=admit):
            for frame in range(6):
                result=self.step(c,frame,payload())
        state=result['after']['geometry']['40']['value']
        self.assertEqual(state.memory.snapshot()['observation_keys'],['V/f0/d0','V/f4/d0','V/f5/d0'])
        self.assertEqual(len(state.memory.cloud()),300)
        self.assertTrue(all(v['provenance']['observed_only'] for v in state.memory.provenance()))

    def test_prior_scope_and_version_mismatch(self):
        updater=ObservedCloudUpdater();item=payload()
        first=updater(UpdateContext('V','moge_points',0,'a','40',item,None))
        for version,tid in [(2,'40'),(1,'other')]:
            with self.assertRaises(ValueError):
                updater(UpdateContext('V','moge_points',1,'b',tid,item,dict(version=version,value=first.value)))

    def test_verified_npz_camera_points_loader_and_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'observed.npz';np.savez_compressed(path,camera_points=surface(100))
            digest=hashlib.sha256(path.read_bytes()).hexdigest()
            item=load_observed_cloud(path,digest,'da','camera','unverified raw depth units')
            self.assertEqual(item.source,'da')
            self.assertEqual(item.provenance['input_sha256'],digest)
            with self.assertRaises(ValueError):load_observed_cloud(path,'wrong','da','camera','units')
        p=surface(100)
        self.assertEqual(cloud_hash(p),cloud_hash(p.astype('>f8')))


if __name__=='__main__':unittest.main()
