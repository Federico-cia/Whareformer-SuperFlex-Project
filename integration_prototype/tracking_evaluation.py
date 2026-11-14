"""Original Whareformer evaluation on exported actual assignments.

Object-name grouping and estimated XYZ reproduce the authors' convention;
they are not newly annotated physical identities or independent 3D ground truth.
Only verified original functions are compiled, avoiding Torch/LMDB imports.
"""
import ast
import bisect
from collections import defaultdict
from dataclasses import asdict, dataclass
import hashlib
import math
import json
from pathlib import Path

import numpy as np


EXPECTED={
    'scripts/evaluate.py':'6a82e06e6c4bf5e69d707d1215a31352243da7bb044ea2632b69e2382ceb3f1c',
    'utils/evaluation.py':'b807523636a9a575550dd2593e2ab3748f37565783f6337de28bb34d8af6fc49',
    'tracking/video_instance.py':'dcafdc87c806b001d4d8c5984943cd8bef793ec748e813b0baddd37dd14c7d5e'}


@dataclass(frozen=True)
class EvaluationPolicy:
    fps: int
    final_frame: int
    scope: str
    dense_eval: bool = True
    min_count: int = 3
    distance_threshold: float = 0.3

    def __post_init__(self):
        if (type(self.fps) is not int or self.fps<1 or type(self.final_frame) is not int or self.final_frame<0
                or self.scope not in ('diagnostic_prefix','full_video') or type(self.dense_eval) is not bool
                or type(self.min_count) is not int or self.min_count<1
                or not math.isfinite(self.distance_threshold) or self.distance_threshold<=0):
            raise ValueError('Explicit valid evaluation policy and temporal scope required')


def export_observations(detections,keys,assignments):
    """Keep annotation fields separate from the assigned predicted ID.

    Minimal controlled tracker doubles may lack fields: signal unavailable,
    never fill fake boxes/locations/names just to produce a score.
    """
    if any(not {'obj_name','bbox','loc'}<=set(d.detection_data) for d in detections):return None
    rows=[]
    for key,d in zip(keys,detections):
        data=d.detection_data
        rows.append(dict(observation_key=key,track_id=assignments[key],obj_name=data['obj_name'],
                         bbox=np.asarray(data['bbox']).tolist(),xyz=np.asarray(data['loc']).tolist()))
    return rows


def results_from_rows(rows):
    results={};last=-1
    for row in rows:
        frame=row['frame_index']
        if type(frame) is not int or frame<=last:raise ValueError('Frames must be unique and chronological')
        last=frame
        observations=row.get('evaluation_observations')
        if observations is None:raise ValueError('Missing observed annotation/XYZ fields for evaluation')
        if len(observations)!=row['detections'] or {o['observation_key'] for o in observations}!=set(row['assignments']):
            raise ValueError('Evaluation export must cover all actual assignments')
        for obs in observations:
            if str(obs['track_id'])!=str(row['assignments'][obs['observation_key']]):
                raise ValueError('Prediction/export assignment mismatch')
        # Exact original insertion order: original tracks have increasing integer IDs.
        observations=sorted(observations,key=lambda o:int(o['track_id']))
        results[f'frame_{frame:010d}']=dict(track_ids=[int(o['track_id']) for o in observations],
            track_obj_names=[o['obj_name'] for o in observations],track_bboxes=[o['bbox'] for o in observations],
            track_3d_locs=[o['xyz'] for o in observations])
    return validate_results(results)


def validate_results(results):
    if not results:raise ValueError('No frames to evaluate')
    final={}
    for name,row in sorted(results.items()):
        if name!=f'frame_{int(name.split("_")[1]):010d}':raise ValueError('Canonical frame names required')
        fields=['track_ids','track_obj_names','track_bboxes','track_3d_locs']
        if len({len(row[f]) for f in fields})!=1:raise ValueError('Inconsistent prediction field lengths')
        ids=row['track_ids']
        if any(type(t) is not int or t<0 for t in ids) or len(ids)!=len(set(ids)):
            raise ValueError('Unique nonnegative integer predicted IDs required')
        if any(not isinstance(n,str) or not n for n in row['track_obj_names']):raise ValueError('Observed object names required')
        for box,loc in zip(row['track_bboxes'],row['track_3d_locs']):
            if np.asarray(box).shape!=(4,) or np.asarray(loc).shape!=(3,) or not np.isfinite(box).all() or not np.isfinite(loc).all():
                raise ValueError('Finite original boxes and XYZ required')
        order=sorted(range(len(ids)),key=lambda i:ids[i])
        final[name]={f:[row[f][i] for i in order] for f in fields}
    return final


class OriginalTrackingEvaluator:
    def __init__(self, source_root, policy):
        self.policy=policy
        self.hashes={};sources={}
        for name,expected in EXPECTED.items():
            source=(Path(source_root)/name).read_text(encoding='utf-8')
            actual=hashlib.sha256(source.encode()).hexdigest()
            if actual!=expected:raise ValueError('Original evaluator source hash mismatch: '+name)
            sources[name]=source;self.hashes[name]=actual
        names=['extract_frame_number','euclidean_distance','get_tracking_data','get_last_known_state',
               'get_timescale_accuracy','get_dense_key_frames','get_sparse_key_frames']
        self.helpers=self._compile(sources['utils/evaluation.py'],names,
                                    dict(math=math,bisect=bisect,defaultdict=defaultdict))
        self.idf1_source=sources['scripts/evaluate.py']

    @staticmethod
    def _compile(source,names,scope):
        tree=ast.parse(source)
        nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
        if {n.name for n in nodes}!=set(names):raise ValueError('Missing original functions')
        exec(compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),'verified_original_evaluator','exec'),scope)
        return scope

    def pcl(self, results):
        results=validate_results(results);p=self.policy
        last=max(int(f.split('_')[1]) for f in results)
        if last>p.final_frame:raise ValueError('Predictions exceed evaluation horizon')
        if p.scope=='diagnostic_prefix' and last!=p.final_frame:
            raise ValueError('Prefix horizon must stop at the last processed frame')
        h=self.helpers
        obj_sets,ids,locs,track_locs,lifespans=h['get_tracking_data'](results)
        key_frames=h['get_dense_key_frames'](obj_sets,p.min_count) if p.dense_eval else h['get_sparse_key_frames'](obj_sets,p.fps)
        rows=[]
        for i in range(145):
            accuracy,correct,total=h['get_timescale_accuracy'](key_frames,p.fps*5*i,p.distance_threshold,
                ids,locs,track_locs,lifespans,f'frame_{p.final_frame:010d}',dense_eval=p.dense_eval)
            rows.append(dict(seconds=5*i,pcl_percent=accuracy,correct=correct,total=total))
        supported=[r for r in rows if r['total']>0]
        return dict(mpcl_percent=100*sum(r['correct']/max(r['total'],1) for r in rows)/145 if supported else None,
                    mpcl_supported_timescales_percent=100*sum(r['correct']/r['total'] for r in supported)/len(supported) if supported else None,
                    supported_timescales=len(supported),total_timescales=145,rows=rows)

    def score(self, results, require_idf1=True):
        results=validate_results(results)
        pcl=self.pcl(results)
        output=dict(mpcl_percent=pcl['mpcl_percent'],idf1_percent=None,
                    mpcl_supported_timescales_percent=pcl['mpcl_supported_timescales_percent'],
                    supported_timescales=pcl['supported_timescales'],pcl_rows=pcl['rows'],
                    frames=len(results),observations=sum(len(r['track_ids']) for r in results.values()),
                    duplicate_name_observations=sum(len(r['track_obj_names'])-len(set(r['track_obj_names'])) for r in results.values()),
                    policy=asdict(self.policy),source_sha256=dict(self.hashes),idf1_status='not_requested',
                    limits=['Original object-name grouping/deduplication; not independent persistent physical identity GT.',
                            'Original PCL uses estimated XYZ, track lifespans and last-known-state filling, including original retroactive convention.',
                            'Original 145-bin mPCL assigns zero contribution to unsupported timescales; short prefixes are not comparable to full-video scores.',
                            'Supported-timescale mean is a separately labelled diagnostic, not the original mPCL.'])
        if not output['observations']:
            output['idf1_status']='unavailable_no_observations';return output
        if require_idf1:
            import motmetrics as mm
            fn=self._compile(self.idf1_source,['process_idf1_worker'],dict(np=np,mm=mm))['process_idf1_worker']
            acc=mm.MOTAccumulator(auto_id=True)
            for update in fn(results):acc.update(*update)
            metric=mm.metrics.create().compute(acc,metrics=['idf1','idtp','idfp','idfn'],name='video')
            value=float(metric.loc['video','idf1']*100)
            output.update(idf1_percent=value if math.isfinite(value) else None,idf1_status='scored',motmetrics=mm.__version__,
                          idf1_counts={k:float(metric.loc['video',k]) for k in ['idtp','idfp','idfn']})
        return output


def evaluate_report(report, rows_by_variant, evaluator):
    """Return a new report: completed full-scope variants only, errors explicit."""
    import copy
    report=copy.deepcopy(report)
    report['evaluation_policy']=asdict(evaluator.policy)
    for variant in report['variants']:
        variant['tracking_metrics']=None
        if variant['status']!='completed' or variant['counts']['frames']!=report['expected_frames']:
            variant['evaluation_status']='not_scored_incomplete';continue
        try:
            rows=rows_by_variant[variant['config']['name']]
            if len(rows)!=report['expected_frames']:raise ValueError('Export frame count mismatch')
            scope=hashlib.sha256(json.dumps([(r['frame_index'],r['evaluation_timestamp'],list(r['evaluation_key_order'])) for r in rows],sort_keys=True).encode()).hexdigest()
            if scope!=report['frame_scope_sha256']:raise ValueError('Export frame scope differs from inference report')
            variant['tracking_metrics']=evaluator.score(results_from_rows(rows))
            variant['evaluation_status']='scored' if variant['tracking_metrics']['idf1_status']=='scored' else variant['tracking_metrics']['idf1_status']
        except Exception as error:
            variant['evaluation_status']='failed'
            variant['evaluation_error']=f'{type(error).__name__}: {error}'
    return report
