import io
import json
from pathlib import Path
import tempfile
import sys
import unittest
from unittest.mock import patch
import full_video_enrichment as d


class PortableDriverTests(unittest.TestCase):
    def test_streaming_truncation_and_records(self):
        self.assertEqual(list(d.annotations(io.StringIO('{"video_annotations":[{"x":1},{"x":2}]}'))),[{'x':1},{'x':2}])
        with self.assertRaises(ValueError): list(d.annotations(io.StringIO('{"video_annotations":[{"x":')))

    def test_da_only_config_no_moge_dependency(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t); (p/'ckpt').write_bytes(b'x'); (p/'cfg').write_bytes(b'y')
            cfg={'sources':['da','moge'],'clouds':{'pixel_policy':'common'},'moge':{'checkpoint':'absent'},
                 'superflex':{'checkpoint':'ckpt','config':'cfg','checkpoint_sha256':d.sha(p/'ckpt'),'config_sha256':d.sha(p/'cfg')}}
            d.save(p/'config.json',cfg); actual=d.production_config({'geometry_config':str(p/'config.json')})
            self.assertEqual(actual['sources'],['da']); self.assertNotIn('moge',actual)
            self.assertEqual(actual['clouds']['pixel_policy'],'source')
            (p/'ckpt').write_bytes(b'bad')
            with self.assertRaises(ValueError): d.production_config({'geometry_config':str(p/'config.json')})

    def test_source_stage_environment_and_ninja_path(self):
        s={'python_da':'/env/da/bin/python','python_sf':'/env/sf/bin/python', 'task':'/job',
           'runtime':'/runtime','superflex_repo':'/authors'}
        with patch.object(d.subprocess,'run') as run:
            d.pipeline(s,'da','manifest','out'); d.pipeline(s,'superflex','manifest','out')
        self.assertEqual(run.call_args_list[0].args[0][0],s['python_da'])
        self.assertEqual(run.call_args_list[1].args[0][0],s['python_sf'])
        self.assertTrue(run.call_args.kwargs['env']['PATH'].startswith(str(Path(s['python_sf']).parent)))

    def test_quota_fails_closed(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(ValueError): d.guard({'task':t})
            with patch.object(d.subprocess,'check_output',return_value='{"free_bytes":1,"free_files":99999}'):
                with self.assertRaises(SystemExit) as c: d.guard({'task':t,'quota_command':['quota']})
                self.assertEqual(c.exception.code,75)

    def test_aggregation_retains_missing_and_failures(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t); d.save(p/'batches.json',['a','b']); d.save(p/'coverage.json',{'missing':['x']})
            d.save(p/'completed/0000.json',{'observations':[{'representations':{'da_points':{'status':'unavailable'}},'aligned_representations':{}}]})
            d.aggregate({'task':t,'video':'P01_02'}); result=d.read(p/'final_status.json')
            self.assertFalse(result['all_blocks_exported']); self.assertEqual(result['pending_blocks'],[1])
            self.assertEqual(result['coverage']['missing'],['x']); self.assertEqual(result['representations']['da_points:unavailable'],1)

    def test_affine_alignment_guards(self):
        import numpy as np
        from align_video_scene import fit_alignment
        depth=np.arange(64,dtype=float).reshape(8,8)+1
        a,b,n=fit_alignment(depth,2*depth+3,np.ones_like(depth,bool))
        self.assertAlmostEqual(a,2); self.assertAlmostEqual(b,3); self.assertEqual(n,64)
        for scene,mask in [(100-depth,np.ones_like(depth,bool)),(depth,np.zeros_like(depth,bool)),
                           (depth,np.ones_like(depth,bool))]:
            if scene is depth and mask.all():
                with self.assertRaises(ValueError): fit_alignment(np.ones_like(depth),scene,mask)
            else:
                with self.assertRaises(ValueError): fit_alignment(depth,scene,mask)

    def test_real_cloud_export_without_any_moge_files(self):
        import os
        import numpy as np
        from PIL import Image
        runtime=Path(os.environ.get('SHAPE_RUNTIME',Path(__file__).parent/'runtime'))
        sys.path.insert(0,str(runtime))
        from shape_tools import pipeline
        with tempfile.TemporaryDirectory() as t:
            root=Path(t); out=root/'out'; out.mkdir()
            Image.fromarray(np.full((8,8,3),127,np.uint8)).save(root/'rgb.png')
            Image.fromarray(np.full((8,8),255,np.uint8)).save(root/'mask.png')
            row=dict(observation_key='P01_02/frame_0000000001__d0',video='P01_02',frame_index=1,
                     rgb=str(root/'rgb.png'),mask=str(root/'mask.png'),category='cup',intrinsics=[10,10,4,4])
            data=dict(schema_version=1,observations=[row]); key=pipeline.item_id(row)
            np.savez_compressed(out/'prediction.npz',depth=np.full((8,8),2.0))
            d.save(out/'da_index.json',{key:dict(status='ready',signature='synthetic',
                   artifacts={'prediction':pipeline.artifact(out,out/'prediction.npz')})})
            cfg={'sources':['da'],'clouds':{'pixel_policy':'source','minimum_points':32}}
            pipeline.clouds(data,out,cfg)
            d.save(out/'superflex_da_index.json',{key:dict(status='failed',signature='synthetic',error='No neural inference in this test')})
            rows=pipeline.export(data,out,cfg)
            self.assertEqual(set(rows[0]['representations']),{'da_points','da_superflex'})
            self.assertEqual(rows[0]['representations']['da_points']['status'],'ready')
            self.assertEqual(rows[0]['representations']['da_superflex']['status'],'unavailable')
            with np.load(out/rows[0]['representations']['da_points']['path']) as z:
                self.assertEqual(z['camera_points'].shape,(64,3))
                self.assertTrue(np.allclose(z['camera_points'][:,2],2))


if __name__=='__main__': unittest.main()
