"""Campaign joins and finite search scope; no model/test-set results invented."""
from copy import deepcopy
import io
import unittest

from hpc_campaign import exact_observations,configurations,iter_annotations
from experiment_runner import Variant


class CampaignTests(unittest.TestCase):
    def example(self):
        entry=dict(image=dict(name='P01_01_frame_0000000123.png'),annotations=[
            dict(id='obs',name='pan',segments=[[[1,2],[5,2],[5,8],[1,8]]])])
        baseline={'frame_0000000123':[dict(id='other',name='knife',bounding_box=[0,0,1,1]),
            dict(id='obs',name='pan',bounding_box=[1,2,6,9])]}
        return entry,baseline

    def test_exact_join_uses_detection_index_not_annotation_index(self):
        entry,baseline=self.example()
        rows,excluded=exact_observations(entry,'frame_0000000123.jpg',baseline,['pan'])
        self.assertEqual(excluded,[])
        self.assertEqual((rows[0]['annotation_index'],rows[0]['detection_idx']),(0,1))

    def test_alias_name_bbox_and_missing_id_excluded(self):
        entry,baseline=self.example()
        self.assertEqual(exact_observations(entry,'frame_0000000124.jpg',baseline,['pan'])[1],['temporal_alias'])
        for field,value in [('id','missing'),('name','pan lid')]:
            changed=deepcopy(entry);changed['annotations'][0][field]=value
            self.assertFalse(exact_observations(changed,'frame_0000000123.jpg',baseline,['pan'])[0])
        baseline['frame_0000000123'][1]['bounding_box'][2]=7
        self.assertFalse(exact_observations(entry,'frame_0000000123.jpg',baseline,['pan'])[0])

    def test_finite_configs_are_valid_isolated_and_balanced(self):
        lanes=configurations();all_rows=[r for lane in lanes.values() for r in lane]
        self.assertEqual([len(lanes[x]) for x in ['cpu','gpu']],[19,10])
        self.assertEqual(len({r['name'] for r in all_rows}),29)
        for row in all_rows:Variant(**row)
        for source in ['da','moge']:
            for method in ['S-separata','P-accumulo','S-accumulo']:
                active=[r for r in all_rows if r.get('source')==source and r['method']==method and r.get('weight',0)>0]
                self.assertEqual({(r['weight'],r['neutral_distance']) for r in active},{(.1,0.),(.1,.1),(1.,0.),(1.,.1)})

    def test_streaming_annotations_and_truncated_input(self):
        self.assertEqual(list(iter_annotations(io.StringIO('{"video_annotations":[{"x":1},{"x":2}]}'))),[{'x':1},{'x':2}])
        with self.assertRaises(ValueError):list(iter_annotations(io.StringIO('{"video_annotations":[{"x":')))


if __name__=='__main__':unittest.main()
