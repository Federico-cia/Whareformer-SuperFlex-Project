import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from PIL import Image
from frontend_inputs import create_manifest,prepare,artifact,verify_bundle


class FrontendTests(unittest.TestCase):
    def fixture(self,root):
        base=root/'base';ready=root/'rgb';base.mkdir();ready.mkdir()
        ann=dict(id='a',name='board',bounding_box=[1,1,4,4])
        frames=[dict(frame='frame_0000000001',frame_index=1,offset=0,annotations=[ann])]
        np.savez_compressed(base/'features.npz',app=np.ones((1,256)),loc=np.ones((1,3)))
        (base/'frames.json').write_text(json.dumps(frames))
        (base/'input_manifest.json').write_text(json.dumps(dict(video='V',fps=30,prepared_hashes={p.name:artifact(p)['sha256'] for p in base.iterdir()})))
        Image.new('RGB',(10,10)).save(ready/'frame_0000000001.jpg')
        (ready/'camera.json').write_text(json.dumps(dict(camera=dict(width=10,height=10),images={'frame_0000000001.jpg':[1,0,0,0,0,0,0]})))
        (ready/'annotations.json').write_text(json.dumps(dict(video_annotations=[dict(rgb_frame='frame_0000000001.jpg',image=dict(name='V_frame_0000000001.png'),annotations=[dict(id='a',name='board',segments=[[[1,1],[3,1],[3,3],[1,3]]])])])) )
        create_manifest(base,ready,[1],root/'manifest.json')
        return root/'manifest.json'

    def test_generic_video_verified_copy_and_lineage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);manifest=self.fixture(root);result=prepare(manifest,root/'out')
            self.assertEqual(result['history_frames'],1)
            plan,_=verify_bundle(root/'out');self.assertIn('frontend_contract_sha256',plan)
            self.assertEqual((root/'base/features.npz').read_bytes(),(root/'out/features.npz').read_bytes())

    def test_duplicates_mapping_pose_and_resolution_fail_before_copy(self):
        for field,value in [('visor_index',2),('detection_idx',2),('rgb_resolution',[1,1]),('camera_pose',[0]*7),('observation_key','wrong')]:
            with tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);path=self.fixture(root);m=json.loads(path.read_text());m['observations'][0][field]=value;path.write_text(json.dumps(m))
                with self.assertRaises((ValueError,KeyError)):prepare(path,root/'out')
                self.assertFalse((root/'out').exists())

    def test_tampered_cache_and_source_fail(self):
        for target in ['base/features.npz','rgb/frame_0000000001.jpg']:
            with tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);path=self.fixture(root)
                with (root/target).open('ab') as stream:stream.write(b'tamper')
                with self.assertRaises(ValueError):prepare(path,root/'out')


if __name__=='__main__':unittest.main()
