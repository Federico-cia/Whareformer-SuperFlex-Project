"""Export per-run comparison tables; no automatic method selection or pooling."""
import argparse
import csv
import json
from pathlib import Path

from experiment_runner import aggregate_reports


def ratio(value,total):
    return 100*value/total if total else None


def write_tables(paths,output):
    groups=aggregate_reports(paths)
    rows=[]
    for i,group in enumerate(groups):
        for run in group['runs']:
            for result in run['variants']:
                cfg=result['config'];counts=result['counts'];statuses=counts['update_statuses']
                metrics=result['tracking_metrics'] or {}
                rows.append(dict(comparison_group=i,video=group['video'],report=run['path'],
                    method=cfg['method'],name=cfg['name'],source=cfg['source'],weight=cfg['weight'],
                    status=result['status'],error=result['error'],controlled_results_allowed=run['controlled'],
                    processed_frames=counts['frames'],detections=counts['detections'],
                    feature_coverage_percent=ratio(counts['features_available'],counts['detections']) if cfg['method']!='W0' else None,
                    detection_comparison_coverage_percent=ratio(counts['detections_with_comparison'],counts['detections']) if cfg['method']!='W0' else None,
                    pair_coverage_percent=ratio(counts['valid_comparison_pairs'],counts['comparison_pairs']),
                    initializations=counts['initializations'],accepted_fusions=counts['accepted_fusions'],
                    rejected_updates=statuses.get('rejected',0),update_errors=statuses.get('error',0),
                    missing_updates=statuses.get('missing',0),worker_failures=counts['worker_statuses'].get('failed',0),
                    pending_requests=len(counts['pending_requests']),unreadable_worker_results=counts['unreadable_worker_results'],
                    attempt_wall_seconds=result['current_attempt_wall_seconds'],
                    attempts_including_replays=result['attempts_including_replays'],
                    replay_costs_linked_to_input_provenance=result['replay_costs_linked_to_input_provenance'],
                    cumulative_setup_run_seconds=result['cumulative_setup_run_seconds'],
                    cumulative_worker_seconds=result['cumulative_worker_seconds'],
                    peak_raw_point_payload_bytes=result['peak_raw_point_payload_bytes'],
                    peak_descriptor_payload_bytes=result['peak_descriptor_payload_bytes'],
                    zero_baseline_exact=result['zero_baseline_exact'],validation_status=result['validation_status'],
                    referenced_peak_gpu_allocated_bytes=result['referenced_peak_gpu_allocated_bytes'],
                    idf1_percent=metrics.get('idf1_percent'),mpcl_percent=metrics.get('mpcl_percent'),
                    evaluation_status=result['evaluation_status']))
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    (output/'groups.json').write_text(json.dumps(groups,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    if rows:
        with (output/'comparison.csv').open('x',encoding='utf-8',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    return rows


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reports',nargs='+',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    rows=write_tables(args.reports,args.output)
    print(f'Exported {len(rows)} variant rows; missing tracking metrics remain empty.')
