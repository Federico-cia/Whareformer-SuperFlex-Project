"""Join saved compare200 geometry to Whareformer tracks using verified annotation IDs.

Run from Whareformer repository root, e.g.:
  python link_compare200_tracks.py --video P01_01 --compare-dir ..\compare200

The compare200 ZIP must have been extracted inside --compare-dir such that
--compare-dir/observations_for_tracking.json and --compare-dir/data/compare200/
exist. This script does not regenerate geometry or infer uncertain identities.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path


def read_json(path: Path):
    with path.open('r', encoding='utf-8') as file:
        return json.load(file)


def write_json(path: Path, obj):
    with path.open('w', encoding='utf-8') as file:
        json.dump(obj, file, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Join compare200 observation clouds with Whareformer tracks')
    parser.add_argument('--video', default='P01_01', help='Video ID, default P01_01')
    parser.add_argument('--compare-dir', type=Path, default=Path('../compare200'), help='Directory containing extracted compare200 ZIP')
    parser.add_argument('--tracks', type=Path, default=None, help='Whareformer tracks_by_id.json path')
    parser.add_argument('--output-dir', type=Path, default=None, help='Directory for joined files')
    args = parser.parse_args()

    video = args.video
    compare_dir = args.compare_dir.resolve()
    observations_path = compare_dir / 'observations_for_tracking.json'
    tracks_path = args.tracks or Path('outputs') / 'epic' / 'whareformer' / video / 'tracks_by_id.json'
    output_dir = args.output_dir or Path('outputs') / 'epic' / 'whareformer' / video
    if not observations_path.is_file():
        parser.error(f'Could not find {observations_path}. Confirm ZIP extraction structure.')
    if not tracks_path.is_file():
        parser.error(f'Could not find {tracks_path}. Run build_tracks_by_id.py --video {video} first.')

    observations = read_json(observations_path)
    tracks = read_json(tracks_path)
    if not isinstance(observations, list):
        parser.error('Unexpected observations manifest structure: expected a JSON list.')
    if tracks.get('video') != video or not isinstance(tracks.get('tracks'), dict):
        parser.error('Unexpected Whareformer tracks JSON or mismatched video ID.')

    # Exact, auditable join: (frame stem, observation ID).
    by_key = defaultdict(list)
    frames_present = set()
    predicted_track_counts = Counter()
    for track_id, items in tracks['tracks'].items():
        for item in items:
            if item.get('video') != video:
                continue
            key = (item['frame'], item['observation_id'])
            by_key[key].append((track_id, item))
            frames_present.add(item['frame'])
            predicted_track_counts[str(track_id)] += 1

    joined = []
    statuses = Counter()
    per_track = defaultdict(list)
    duplicate_keys = []
    for obs in observations:
        if obs.get('video') != video:
            continue
        frame = Path(obs['rgb_frame']).stem
        key = (frame, obs.get('annotation_id'))
        candidates = by_key.get(key, [])
        if len(candidates) == 1:
            track_id, t = candidates[0]
            status = 'exact'
        elif len(candidates) > 1:
            status = 'ambiguous_duplicate'
            duplicate_keys.append(key)
            track_id, t = None, None
        elif frame not in frames_present:
            status = 'frame_not_in_whareformer_predictions'
            track_id, t = None, None
        else:
            status = 'annotation_id_not_found_in_frame'
            track_id, t = None, None

        matched_row = dict(obs)
        matched_row['frame_name'] = frame
        matched_row['mapping_status'] = status
        matched_row['track_id'] = int(track_id) if track_id is not None and str(track_id).lstrip('-').isdigit() else track_id
        matched_row['detection_idx'] = t['detection_idx'] if t else None
        matched_row['whareformer_observation_id'] = t['observation_id'] if t else None
        matched_row['whareformer_bbox'] = t['bbox'] if t else None
        matched_row['whareformer_xyz'] = t['xyz'] if t else None
        # Store real paths so downstream scripts know where to load the clouds.
        for field in ('rgb', 'mask', 'camera'):
            path_value = obs.get(field)
            if path_value:
                matched_row[field + '_absolute'] = str((compare_dir / path_value).resolve())
        for source, cloud in obs.get('clouds', {}).items():
            if isinstance(cloud, dict) and cloud.get('path'):
                matched_row['clouds'][source]['path_absolute'] = str((compare_dir / cloud['path']).resolve())
        joined.append(matched_row)
        statuses[status] += 1
        if status == 'exact':
            per_track[str(track_id)].append(matched_row)

    def sort_track(track_id):
        return (-len(per_track[track_id]), int(track_id) if track_id.lstrip('-').isdigit() else track_id)

    report = {
        'video': video,
        'geometry_observations_in_manifest': len(joined),
        'join_statuses': dict(statuses),
        'matched_track_count': len(per_track),
        'matched_observation_count': statuses['exact'],
        'unmatched_observation_count': len(joined) - statuses['exact'],
        'tracks_with_multiple_geometry_observations': sum(len(v) >= 2 for v in per_track.values()),
        'tracks_with_at_least_five_geometry_observations': sum(len(v) >= 5 for v in per_track.values()),
        'top_tracks': [
            {'track_id': track_id, 'num_geometry_observations': len(per_track[track_id]),
             'categories': sorted(set(o.get('category', '') for o in per_track[track_id])),
             'first_frame': min(o['frame_name'] for o in per_track[track_id]),
             'last_frame': max(o['frame_name'] for o in per_track[track_id])}
            for track_id in sorted(per_track, key=sort_track)[:20]
        ],
        'unmatched_examples': [
            {'observation_key': r.get('observation_key'), 'frame_name': r['frame_name'],
             'annotation_id': r.get('annotation_id'), 'category': r.get('category'),
             'reason': r['mapping_status']}
            for r in joined if r['mapping_status'] != 'exact'
        ][:15],
        'important': 'Exact ID matches are not proof that track identities are correct or object shapes are aligned.'
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    joined_file = output_dir / 'compare200_joined_observations.json'
    report_file = output_dir / 'compare200_join_report.json'
    candidates_file = output_dir / 'compare200_track_candidates.csv'
    write_json(joined_file, joined)
    write_json(report_file, report)
    with candidates_file.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['track_id', 'num_geometry_observations', 'categories', 'first_frame', 'last_frame'])
        w.writeheader()
        for row in report['top_tracks']:
            copy = dict(row)
            copy['categories'] = ', '.join(copy['categories'])
            w.writerow(copy)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f'Created: {joined_file}')
    print(f'Created: {report_file}')
    print(f'Created: {candidates_file}')


if __name__ == '__main__':
    main()
