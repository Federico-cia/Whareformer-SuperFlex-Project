"""Common serial variant runner and descriptive telemetry, independent of Torch.

Tracking metrics require an explicit evaluator; no predicted IDs are used as GT.
Input frames/features must be prepared with verified provenance by the caller.
"""
from collections import Counter
from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
import time
import hashlib
import uuid

import numpy as np

from cloud_updater import ObservedCloudUpdater, CloudUpdateConfig, cloud_hash
from deferred_superflex import DeferredSuperflex, SuperflexConfig
from frame_coordinator import FrameCoordinator
from geometry_matcher import GeometryMatcher, GeometryConfig
from shape_tools.geometry import normalize_shape
from shape_tools.metrics import descriptors
from tracking_evaluation import export_observations


VARIANTS=('W0','G0','S-separata','S-accumulo','P-accumulo')


@dataclass(frozen=True)
class Variant:
    name: str
    method: str
    source: str = 'da'
    weight: float = 0.0
    neutral_distance: float = 0.0
    metric: str = 'd2'
    capacity: int = 2

    def __post_init__(self):
        if (not self.name or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in self.name)
                or self.method not in VARIANTS or self.source not in ('da','moge')):
            raise ValueError('Invalid variant name/method/source')
        if self.method in ('W0','G0') and self.weight != 0:
            raise ValueError('Baseline/diagnostic variant cannot influence matching')
        self.matcher_config()

    @property
    def accumulate(self):
        return self.method in ('G0','S-accumulo','P-accumulo')

    @property
    def representation(self):
        suffix='superflex' if self.method in ('S-separata','S-accumulo') else 'points'
        return ('da_raw_' if self.source=='da' else 'moge_')+suffix

    def matcher_config(self):
        mode='disabled' if self.method=='W0' else 'diagnostic' if self.method=='G0' else 'active'
        return GeometryConfig(mode,self.representation,capacity=self.capacity,metric=self.metric,
                              weight=self.weight,neutral_distance=self.neutral_distance)


@dataclass
class FrameData:
    detections: list
    metadata: dict
    keys: list
    features: dict
    cloud_inputs: dict = field(default_factory=dict)


class ResultsPending(RuntimeError):
    """Replay is incomplete; request files are ready, tracking must not continue."""


def accumulated_point_features(state):
    # Same numeric-point sampling, normalization and descriptor policy as the
    # existing comparison.load_features NPZ branch; no generated points.
    p=state.memory.cloud()
    ids=np.random.default_rng(20261109).choice(len(p),1024,replace=len(p)<1024)
    normalized=normalize_shape(p[ids])
    return normalized,*descriptors(normalized)


class VariantExecution:
    def __init__(self, tracker, video, variant, cache, cloud_config, superflex_config,
                 worker=None, allow_test_results=False):
        self.variant=variant
        tracker.matcher=GeometryMatcher(tracker.matcher,video,variant.matcher_config())
        self.geometry_seconds=0.0
        updater=ObservedCloudUpdater(cloud_config)
        def timed_update(context):
            started=time.perf_counter()
            try:return updater(context)
            finally:self.geometry_seconds+=time.perf_counter()-started
        reconstructor=DeferredSuperflex(Path(cache)/variant.name,superflex_config,allow_test_results) if variant.method=='S-accumulo' else None
        self.coordinator=FrameCoordinator(tracker,timed_update if variant.accumulate else None,reconstructor)
        self.worker=worker
        self.rows=[]
        self.started=None
        self.elapsed_seconds=None
        self.failed_frame=None
        self.status='created'
        self.error=None
        self.worker_events=[]
        self.descriptor_size=0

    def step(self, frame):
        variant=self.variant
        available=frame.features.get(variant.representation,{})
        features={key:available.get(key) for key in frame.keys} if variant.method!='W0' else None
        for feature in (features or {}).values():
            if feature is not None:self.descriptor_size=len(feature[1 if variant.metric=='d2' else 2])
        clouds=frame.cloud_inputs.get(variant.source,{}) if variant.accumulate else {}
        before_geometry=self.geometry_seconds
        started=time.perf_counter()
        transaction=self.coordinator.step(frame.detections,frame.metadata,frame.keys,features,clouds)
        coordinator_seconds=time.perf_counter()-started
        matcher=self.coordinator.matcher
        score=matcher.last_score
        valid=score['valid'] if variant.method!='W0' else np.zeros((len(frame.keys),0),bool)
        point_errors=[]
        point_seconds=0.0
        if variant.method=='P-accumulo':
            start=time.perf_counter();published={}
            for event in transaction['updates']:
                if event['status']!='accepted':continue
                tid=event['track_id'];entry=transaction['after']['geometry'][tid]
                try:
                    feature=accumulated_point_features(entry['value'])
                    published[tid]=(f"{entry['version']}_{cloud_hash(entry['value'].memory.cloud())}",feature)
                except Exception as error:
                    point_errors.append(dict(track_id=tid,error=f'{type(error).__name__}: {error}'))
            matcher.geometry.publish_accumulated_points(frame.metadata['frame_idx'],published)
            point_seconds=time.perf_counter()-start
        row=dict(frame_index=frame.metadata['frame_idx'],assignments=transaction['assignments'],
                 detections=len(frame.keys),features_available=sum(v is not None for v in (features or {}).values()),
                 cloud_inputs_available=sum(v is not None for v in clouds.values()),
                 comparison_pairs=int(valid.size),valid_comparison_pairs=int(valid.sum()),
                 detections_with_comparison=int(valid.any(axis=1).sum()),updates=transaction['updates'],
                 point_descriptor_errors=point_errors,point_descriptor_seconds=point_seconds,
                 coordinator_seconds=coordinator_seconds,registration_accumulation_seconds=self.geometry_seconds-before_geometry,
                 resolution_seconds=0.0,worker_seconds=0.0,reconstruction_events=[])
        row['evaluation_observations']=export_observations(frame.detections,frame.keys,transaction['assignments'])
        row['evaluation_timestamp']=frame.metadata['timestamp']
        row['evaluation_key_order']=list(frame.keys)
        self.rows.append(row)
        self.status='running'
        self._payload_metrics(row)
        requests=self.coordinator.snapshot()['pending_reconstructions']
        row['request_ids']=list(requests)
        if requests:
            self.status='waiting_for_results'
            start=time.perf_counter()
            try:
                if self.worker is not None:
                    service=self.coordinator.reconstructor
                    for rid in requests:
                        folder=service.root/rid
                        if not (folder/'result.json').exists():
                            begin=time.perf_counter();outcome=self.worker(folder)
                            seconds=time.perf_counter()-begin
                            self.worker_events.append(dict(request_id=rid,seconds=seconds,status=outcome['status']))
                            row['worker_seconds']+=seconds
                row['reconstruction_events']=self.coordinator.resolve_reconstructions()
            except FileNotFoundError as error:
                raise ResultsPending(f'{variant.name}: process {requests} then replay from the start using the same cache') from error
            finally:
                row['resolution_seconds']=time.perf_counter()-start
            self.status='running'
        self._payload_metrics(row)
        return row

    def _payload_metrics(self, row):
        snapshot=self.coordinator.snapshot()
        raw_bytes=sum(e['value'].memory.snapshot()['points']*3*8 for e in snapshot['geometry'].values())
        base_entries=sum(len(v) for v in snapshot['separate_shape_memory'].values())
        published_entries=sum(len(v) for v in snapshot['reconstructions'].values())
        descriptor_bytes=base_entries*self.descriptor_size*8+published_entries*(16384 if self.variant.metric=='d2' else 3)*8
        row.update(raw_observed_point_bytes=raw_bytes,descriptor_payload_bytes=descriptor_bytes,
                   published_track_features=snapshot['reconstructions'])

    def summary(self):
        updates=[e for row in self.rows for e in row['updates']]
        workers=[];unreadable_workers=[]
        if self.coordinator.reconstructor is not None:
            for rid in {rid for row in self.rows for rid in row.get('request_ids',[])}:
                result_path=self.coordinator.reconstructor.root/rid/'result.json'
                if result_path.exists():
                    try:
                        record=json.loads(result_path.read_text())
                        if not isinstance(record,dict) or record.get('status') not in ('ready','failed'):
                            raise ValueError('Invalid worker manifest')
                        workers.append(record)
                    except (OSError,ValueError,TypeError) as error:
                        unreadable_workers.append(dict(request_id=rid,error=f'{type(error).__name__}: {error}'))
        phases={name:sum(row[name] for row in self.rows) for name in ['coordinator_seconds','registration_accumulation_seconds','point_descriptor_seconds','resolution_seconds','worker_seconds']}
        counts=dict(frames=len(self.rows),detections=sum(r['detections'] for r in self.rows),
                    features_available=sum(r['features_available'] for r in self.rows),
                    cloud_inputs_available=sum(r['cloud_inputs_available'] for r in self.rows),
                    valid_comparison_pairs=sum(r['valid_comparison_pairs'] for r in self.rows),
                    comparison_pairs=sum(r['comparison_pairs'] for r in self.rows),
                    detections_with_comparison=sum(r['detections_with_comparison'] for r in self.rows),
                    update_statuses=dict(Counter(e['status'] for e in updates)),
                    initializations=sum(e['status']=='accepted' and e.get('diagnostics',{}).get('operation')=='initialize' for e in updates),
                    accepted_fusions=sum(e['status']=='accepted' and e.get('diagnostics',{}).get('operation')=='register_and_accumulate' for e in updates),
                    point_descriptor_failures=sum(len(r['point_descriptor_errors']) for r in self.rows),
                    worker_statuses=dict(Counter(w['status'] for w in workers)),
                    pending_requests=self.coordinator.snapshot()['pending_reconstructions'],
                    unreadable_worker_results=len(unreadable_workers))
        forwards=[];gpu_peaks=[]
        for record in workers:
            detail=record.get('production')
            if not isinstance(detail,dict):continue
            for name,target in [('forward_seconds',forwards),('peak_allocated_bytes',gpu_peaks)]:
                value=detail.get(name)
                if type(value) in (int,float) and np.isfinite(value) and value>=0:target.append(value)
        forward=sum(forwards) if forwards else None
        return dict(config=asdict(self.variant),status=self.status,error=self.error,counts=counts,timings=phases,
                    current_attempt_wall_seconds=self.elapsed_seconds if self.elapsed_seconds is not None else 0.0,
                    failed_frame_index=self.failed_frame,unreadable_worker_details=unreadable_workers,
                    referenced_cached_forward_seconds=forward,
                    referenced_peak_gpu_allocated_bytes=max(gpu_peaks) if gpu_peaks else None,
                    peak_raw_point_payload_bytes=max((r.get('raw_observed_point_bytes',0) for r in self.rows),default=0),
                    peak_descriptor_payload_bytes=max((r.get('descriptor_payload_bytes',0) for r in self.rows),default=0),
                    tracking_metrics=None,evaluation_status='not_scored',
                    limits=['Timings are nested: registration inside coordinator, worker inside resolution; do not sum phases.',
                            'Payload bytes exclude Python overhead, tracker weights, meshes, caches and process/GPU RSS.',
                            'Cached forward cost is referenced provenance, not newly incurred time.',
                            'No predicted track IDs treated as ground truth.'])


class ExperimentRunner:
    def __init__(self, tracker_factory, video, variants, cache,
                 cloud_config=CloudUpdateConfig(),superflex_config=SuperflexConfig(),
                 worker=None,allow_test_results=False,provenance=None):
        variants=list(variants)
        if len({v.name for v in variants})!=len(variants):raise ValueError('Unique variant names required')
        if not variants:raise ValueError('At least one variant required')
        self.provenance=dict(provenance or {})
        self.cache=Path(cache)
        self._ran=False
        self.executions=[]
        trackers=[];models=[]
        for variant in variants:
            setup_started=time.perf_counter()
            tracker=tracker_factory()
            if isinstance(tracker.matcher,GeometryMatcher):raise TypeError('Factory must return a fresh original tracker')
            if any(tracker is t for t in trackers) or any(tracker.matcher.model is m for m in models):
                raise ValueError('Trackers and models must not be shared between variants')
            trackers.append(tracker);models.append(tracker.matcher.model)
            execution=VariantExecution(tracker,video,variant,cache,cloud_config,superflex_config,worker,allow_test_results)
            execution.setup_seconds=time.perf_counter()-setup_started
            self.executions.append(execution)
        self.video=video
        self.cloud_config=cloud_config
        self.superflex_config=superflex_config
        self.allow_test_results=allow_test_results

    def run(self, frames):
        if self._ran:raise RuntimeError('Create fresh runner/trackers to replay an attempt')
        self._ran=True
        frames=list(frames)
        if not frames:raise ValueError('At least one input frame required')
        frame_scope=hashlib.sha256(json.dumps([(f.metadata['frame_idx'],f.metadata['timestamp'],f.keys) for f in frames],sort_keys=True).encode()).hexdigest()
        input_bound=bool(self.provenance.get('input_manifest_sha256'))
        unverified_attempt=uuid.uuid4().hex
        for execution in self.executions:
            execution.started=time.perf_counter()
            try:
                for frame in frames:execution.step(frame)
                execution.status='completed'
            except ResultsPending as error:
                execution.error=str(error)
            except Exception as error:
                execution.status='failed';execution.failed_frame=frame.metadata['frame_idx'];execution.error=f'{type(error).__name__}: {error}'
            execution.elapsed_seconds=time.perf_counter()-execution.started
        baseline=next((e for e in self.executions if e.variant.method=='W0' and e.status=='completed'),None)
        summaries=[]
        for execution in self.executions:
            summary=execution.summary()
            summary['zero_baseline_exact']=None
            if baseline is not None and execution.status=='completed' and execution.variant.weight==0:
                summary['zero_baseline_exact']=[r['assignments'] for r in baseline.rows]==[r['assignments'] for r in execution.rows]
            summary['validation_status']='failed_zero' if summary['zero_baseline_exact'] is False else 'passed_zero' if summary['zero_baseline_exact'] is True else 'not_checked'
            signature=hashlib.sha256(json.dumps(dict(video=self.video,variant=asdict(execution.variant),
                cloud=asdict(self.cloud_config),superflex=asdict(self.superflex_config),provenance=self.provenance,
                controlled=self.allow_test_results,frame_scope=frame_scope,
                unverified_attempt=None if input_bound else unverified_attempt),sort_keys=True).encode()).hexdigest()
            ledger=self.cache/execution.variant.name/'attempts.jsonl'
            ledger.parent.mkdir(parents=True,exist_ok=True)
            attempt=dict(attempt_id=uuid.uuid4().hex,signature=signature,status=execution.status,
                         setup_seconds=execution.setup_seconds,run_seconds=execution.elapsed_seconds,
                         worker_seconds=summary['timings']['worker_seconds'])
            with ledger.open('a',encoding='utf-8') as stream:stream.write(json.dumps(attempt)+'\n')
            attempts=[json.loads(line) for line in ledger.read_text().splitlines() if line]
            matching=[r for r in attempts if r['signature']==signature]
            summary['replay_costs_linked_to_input_provenance']=input_bound
            summary['attempts_including_replays']=len(matching)
            summary['cumulative_setup_run_seconds']=sum(r['setup_seconds']+r['run_seconds'] for r in matching)
            summary['cumulative_worker_seconds']=sum(r['worker_seconds'] for r in matching)
            summary['attempt_id']=attempt['attempt_id']
            summary['setup_seconds']=execution.setup_seconds
            summaries.append(summary)
        return dict(schema_version=1,video=self.video,expected_frames=len(frames),frame_scope_sha256=frame_scope,provenance=self.provenance,
                    cloud_config=asdict(self.cloud_config),superflex_config=asdict(self.superflex_config),
                    controlled_results_allowed=self.allow_test_results,variants=summaries)

    def write(self, output, report):
        output=Path(output);output.mkdir(parents=True,exist_ok=False)
        for execution in self.executions:
            with (output/(execution.variant.name+'.jsonl')).open('x',encoding='utf-8') as stream:
                for row in execution.rows:stream.write(json.dumps(row,allow_nan=False)+'\n')
        saved_report=dict(report)
        saved_report['prediction_export_sha256']={e.variant.name:hashlib.sha256((output/(e.variant.name+'.jsonl')).read_bytes()).hexdigest() for e in self.executions}
        (output/'summary.json').write_text(json.dumps(saved_report,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def aggregate_reports(paths):
    """Preserve per-run denominators/status; never turn missing metrics into zero."""
    groups={}
    for path in paths:
        report=json.loads(Path(path).read_text())
        signature=json.dumps(dict(video=report['video'],expected_frames=report['expected_frames'],frame_scope=report.get('frame_scope_sha256'),
                                  cloud_config=report['cloud_config'],superflex_config=report['superflex_config'],
                                  provenance=report.get('provenance',{}),controlled=report['controlled_results_allowed'],evaluation_policy=report.get('evaluation_policy')),sort_keys=True)
        if not report.get('provenance',{}).get('input_manifest_sha256'):signature+=':unverified:'+str(path)
        group=groups.setdefault(signature,dict(video=report['video'],runs=[]))
        group['runs'].append(dict(path=str(path),controlled=report['controlled_results_allowed'],variants=report['variants']))
    return list(groups.values())
