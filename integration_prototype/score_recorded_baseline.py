"""Original IDF1 worker on a semantic reconstruction of the exported predictions.

This does not infer tracks. Ground-truth grouping follows the original worker's
object-name convention; it is not independent physical-identity annotation.
"""
import ast
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np


def main():
    root=Path(__file__).resolve().parent
    for wheel in root.glob('*.whl'):sys.path.insert(0,str(wheel))
    import motmetrics as mm
    assert not (root/'result.json').exists()
    start=time.perf_counter()
    with gzip.open(root/'tracks_by_id.json.gz','rt',encoding='utf-8') as f:source=json.load(f)
    by_frame={}
    for tid,rows in source['tracks'].items():
        for row in rows:by_frame.setdefault(row['frame'],[]).append((int(tid),row))
    results={}
    for frame,rows in sorted(by_frame.items()):
        rows.sort(key=lambda x:x[0])
        results[frame]=dict(track_ids=[tid for tid,r in rows],track_obj_names=[r['name'] for tid,r in rows],
                            track_bboxes=[r['bbox'] for tid,r in rows],track_3d_locs=[r['xyz'] for tid,r in rows])
    tree=ast.parse((root/'original_evaluate.py').read_text())
    worker=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='process_idf1_worker')
    scope={'np':np,'mm':mm};exec(compile(ast.fix_missing_locations(ast.Module(body=[worker],type_ignores=[])),'original_evaluate','exec'),scope)
    updates=scope['process_idf1_worker'](results)
    acc=mm.MOTAccumulator(auto_id=True)
    for update in updates:acc.update(*update)
    metrics=mm.metrics.create().compute(acc,metrics=['idf1','idtp','idfp','idfn'],name='P01_01')
    result=dict(video='P01_01',frames=len(results),metric_frames=len(updates),idf1_percent=float(metrics.loc['P01_01','idf1']*100),
                counts={n:float(metrics.loc['P01_01',n]) for n in ['idtp','idfp','idfn']},motmetrics=mm.__version__,
                seconds=time.perf_counter()-start,evaluator_sha256=hashlib.sha256((root/'original_evaluate.py').read_bytes()).hexdigest(),
                protocol='Original object-name grouping, deduplication and IoU matching in process_idf1_worker; rows reconstructed in original ascending track-ID order.',
                limits=['Scoring of recorded predictions, no inference rerun.', 'Single train video, not held-out accuracy.',
                        'Object-name evaluation convention is not certified persistent physical identity ground truth.'])
    (root/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
