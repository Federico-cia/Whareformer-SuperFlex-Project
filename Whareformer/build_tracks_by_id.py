"""Reorganize Whareformer P30_05 predictions by track, linking observation IDs.

Run from the Whareformer repository root (in the activated Conda environment):
    python build_tracks_by_id.py

Only unpickle tracking outputs that you generated locally or otherwise trust.
The script never invents matches: it reports unmatched rows separately.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
import pickle


def bbox_iou(a, b):
    ax0, ay0, ax1, ay1 = (float(v) for v in a)
    bx0, by0, bx1, by1 = (float(v) for v in b)
    ix = max(0.0, min(ax1, bx1) - max(ax0, bx0))
    iy = max(0.0, min(ay1, by1) - max(ay0, by0))
    intersection = ix * iy
    area_a = max(0.0, ax1 - ax0) * max(0.0, ay1 - ay0)
    area_b = max(0.0, bx1 - bx0) * max(0.0, by1 - by0)
    denom = area_a + area_b - intersection
    return intersection / denom if denom > 0 else 0.0


def location_to_list(value):
    """Allow NumPy array, Python list, or missing location."""
    if value is None:
        return None
    try:
        vals = [float(x) for x in value]
        if len(vals) != 3:
            return None
        return [v if math.isfinite(v) else None for v in vals]
    except (TypeError, ValueError):
        return None


def main():
    parser = argparse.ArgumentParser(description="Map Whareformer track IDs to per-frame observation IDs")
    parser.add_argument('--video', default='P30_05')
    parser.add_argument('--annotations', type=Path, default=None)
    parser.add_argument('--tracking', type=Path, default=None)
    parser.add_argument('--output', type=Path, default=None)
    parser.add_argument('--min-iou', type=float, default=0.95, help='Minimum IoU for matching a non-identical bounding box (default: 0.95)')
    args = parser.parse_args()
    video = args.video
    annotations_file = args.annotations or Path(f'data/epic_osnom/observations/{video}/object_annotations.json')
    tracking_file = args.tracking or Path(f'outputs/epic/whareformer/{video}/tracking_outputs.pkl')
    output_file = args.output or Path(f'outputs/epic/whareformer/{video}/tracks_by_id.json')
    for p in (annotations_file, tracking_file):
        if not p.is_file():
            parser.error(f'Missing input: {p}')

    with annotations_file.open(encoding='utf-8') as f:
        original = json.load(f)
    annotation_map = {entry['frame_name']: entry['annotations'] for entry in original['video_annotations']}
    # This pickle was produced by Whareformer; do not load unknown/untrusted pickles.
    with tracking_file.open('rb') as f:
        predictions = pickle.load(f)
    if not isinstance(predictions, dict):
        raise TypeError('Expected tracking output to be a dictionary keyed by frame name.')

    tracks = defaultdict(list)
    failures = []
    matched_exact = 0
    matched_approx = 0
    count_preds = 0
    for frame in sorted(predictions):
        pred = predictions[frame]
        if not isinstance(pred, dict):
            raise TypeError(f'{frame}: expected a frame dictionary')
        fields = ('track_ids', 'track_obj_names', 'track_bboxes', 'track_3d_locs')
        if any(field not in pred for field in fields):
            raise KeyError(f'{frame}: missing one of {fields}')
        lists = [pred[k] for k in fields]
        if len({len(lst) for lst in lists}) != 1:
            raise ValueError(f'{frame}: per-frame lists have different lengths.')
        annotations = annotation_map.get(frame, [])
        used = set()
        for row_idx, (track_id, name, box, pos) in enumerate(zip(*lists)):
            count_preds += 1
            # Find the actual source observation; don't assume the two lists share order.
            box_tuple = tuple(int(v) for v in box)
            candidates = [
                (idx, ann) for idx, ann in enumerate(annotations)
                if idx not in used and str(ann['name']) == str(name)
            ]
            exact = [(idx, ann) for idx, ann in candidates if tuple(ann['bounding_box']) == box_tuple]
            quality = None
            if len(exact) == 1:
                idx, annotation = exact[0]
                quality = 'exact'
                matched_exact += 1
            else:
                scored = sorted(
                    [(bbox_iou(box_tuple, ann['bounding_box']), idx, ann) for idx, ann in candidates],
                    reverse=True, key=lambda x: x[0]
                )
                best = scored[0] if scored else None
                # Require one sufficiently good, unambiguous candidate.
                if best is not None and best[0] >= args.min_iou and (
                    len(scored) == 1 or best[0] > scored[1][0]
                ):
                    _, idx, annotation = best
                    quality = 'iou'
                    matched_approx += 1
            if quality is None:
                failures.append({
                    'frame': frame, 'output_index': row_idx,
                    'track_id': str(track_id), 'name': str(name),
                    'bbox': list(box_tuple), 'candidate_count_same_name': len(candidates)
                })
                continue
            used.add(idx)
            tracks[str(track_id)].append({
                'video': video,
                'frame': frame,
                'detection_idx': idx,
                'observation_id': annotation['id'],
                'name': annotation['name'],
                'bbox': annotation['bounding_box'],
                'xyz': location_to_list(pos),
                'matching': quality
            })

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open('w', encoding='utf-8') as f:
        json.dump({'video': video, 'tracks': dict(sorted(tracks.items(), key=lambda kv: (0, int(kv[0])) if kv[0].lstrip('-').isdigit() else (1, kv[0])))}, f, indent=2, ensure_ascii=False)
    report = {
        'video': video,
        'annotation_frames': len(annotation_map),
        'prediction_frames': len(predictions),
        'total_prediction_rows': count_preds,
        'matches_exact': matched_exact,
        'matches_iou': matched_approx,
        'unmatched_rows': len(failures),
        'distinct_tracks_with_matched_observations': len(tracks),
        'unmatched_examples': failures[:30],
        'note': 'Predicted tracks are not ground-truth identities. A track can split or merge physical objects.'
    }
    report_path = output_file.with_name('track_match_report.json')
    with report_path.open('w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(f'Wrote: {output_file}')
    print(f'Wrote: {report_path}')
    if failures:
        print('WARNING: Some predictions did not match a source annotation. Review the report before using them.')


if __name__ == '__main__':
    main()
