"""CPU-only evaluator verification against existing full-video baseline outputs."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import sys
import unittest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference',type=Path,required=True)
    parser.add_argument('--source-root',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--all-tests',action='store_true')
    args=parser.parse_args()
    for wheel in sorted(args.reference.glob('*.whl')):sys.path.insert(0,str(wheel))
    from tracking_evaluation import EvaluationPolicy,OriginalTrackingEvaluator
    stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.TestLoader().discover(str(Path(__file__).parent),pattern='test_*.py' if args.all_tests else 'test_tracking_evaluation.py'))
    args.output.mkdir(parents=True,exist_ok=False)
    (args.output/'tests.txt').write_text(stream.getvalue())
    print(stream.getvalue(),flush=True)
    if not result.wasSuccessful() or result.skipped:raise RuntimeError('All evaluator tests must actually execute on HPC')
    with gzip.open(args.reference/'tracks_by_id.json.gz','rt') as file:tracks=json.load(file)
    by_frame={}
    for tid,rows in tracks['tracks'].items():
        for row in rows:by_frame.setdefault(row['frame'],[]).append((int(tid),row))
    predictions={}
    for frame,rows in sorted(by_frame.items()):
        rows.sort(key=lambda x:x[0])
        predictions[frame]=dict(track_ids=[t for t,r in rows],track_obj_names=[r['name'] for t,r in rows],
                                track_bboxes=[r['bbox'] for t,r in rows],track_3d_locs=[r['xyz'] for t,r in rows])
    evaluator=OriginalTrackingEvaluator(args.source_root,EvaluationPolicy(60,99135,'full_video'))
    score=evaluator.score(predictions)
    assert abs(score['idf1_percent']-73.2697350574193)<1e-9,score['idf1_percent']
    assert abs(score['mpcl_percent']-70.46550449586455)<1e-9,score['mpcl_percent']
    score.update(validation_tests=result.testsRun,skipped_tests=len(result.skipped),
                 reference='Existing recorded P01_01 train predictions; no new tracking inference.',
                 input_sha256=hashlib.sha256((args.reference/'tracks_by_id.json.gz').read_bytes()).hexdigest())
    (args.output/'result.json').write_text(json.dumps(score,indent=2)+'\n')
    print(json.dumps({k:score[k] for k in ['idf1_percent','mpcl_percent','frames','observations','validation_tests']},indent=2),flush=True)


if __name__=='__main__':main()
