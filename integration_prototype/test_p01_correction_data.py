import tempfile
import unittest
from pathlib import Path
import numpy as np
from p01_correction_hook import apply_correction
from p01_correction_data import CorrectionData,bounded,save,sha,verify_geometry


class CorrectionDeliveryTests(unittest.TestCase):
    def test_zero_weight_and_unavailable_are_neutral(self):
        x=np.array([1.0,2.0,3.0],dtype=np.float32)
        self.assertTrue(np.array_equal(apply_correction(x,[np.nan]*3,[False]*3,0),x))
        self.assertTrue(np.array_equal(apply_correction(x,[0,4,np.nan],[False,True,False],.5),[1,4,3]))
        with self.assertRaises(ValueError):apply_correction(x,[0,np.nan,2],[True]*3,1)
        with self.assertRaises(ValueError):apply_correction(x,[1,2],[True,True],0)

    def test_paths_cannot_escape(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(ValueError):bounded(t,'../outside.npz')

    def test_reader_preserves_order_and_rejects_future(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);key='P01_01/frame_2__d0';past='P01_01/frame_1__d0'
            save(p/'geometry_index.json',{'observations':[{'observation_key':key},{'observation_key':past}]})
            save(p/'samples.json',[dict(observation_key=key,frame_index=2,candidate_track_ids=[7,3],
                 candidate_history_ends=[1,0],numerical_input_key='x',numerical_label_key='y',target_class=1)])
            save(p/'geometry_history.json',{'7':[dict(observation_key=past,frame_index=1)]})
            np.savez_compressed(p/'training_inputs.npz',x=np.zeros((3,259)),y=np.array([0,1,0]))
            data=CorrectionData(p,p,p);example=data.example(key)
            self.assertEqual(example['candidate_track_ids'],[7,3]);self.assertEqual(len(example['candidate_views'][0]),1)
            self.assertEqual(example['candidate_views'][1],[])
            data.history['7'][0]['frame_index']=2
            with self.assertRaises(ValueError):data.example(key)
            data.close()

    def test_geometry_integrity_and_counts(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);np.savez_compressed(p/'points.npz',camera_points=np.ones((8,3)),pixels_xy=np.zeros((8,2)),colors=np.zeros((8,3)))
            (p/'rgb').write_bytes(b'rgb');(p/'mask').write_bytes(b'mask');(p/'params').write_bytes(b'params');(p/'ply').write_bytes(b'ply')
            key='P01_01/frame_1__d0';row=dict(observation_key=key,source_observation=dict(observation_key=key,frame_index=1,
                rgb='rgb',mask='mask',rgb_sha256=sha(p/'rgb'),mask_sha256=sha(p/'mask')),
                artifacts={k:dict(path=n,sha256=sha(p/n)) for k,n in [('points','points.npz'),('surface','ply'),('parameters','params')]})
            save(p/'geometry_index.json',dict(video='P01_01',observations=[row]))
            self.assertEqual(verify_geometry(p,1)['observations'],1)
            with self.assertRaises(ValueError):verify_geometry(p,8126)
            (p/'params').write_bytes(b'corrupted')
            with self.assertRaises(ValueError):verify_geometry(p,1)


if __name__=='__main__':unittest.main()
