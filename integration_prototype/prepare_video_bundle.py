"""Prepare an entire official feature sequence with exact, verified geometry joins.

Reuses trusted author feature pickles and existing geometric artifacts. This is
not image feature extraction. No predicted track ID is used to select geometry.
The template supplies pinned original code, checkpoint and baseline config.
"""
import argparse
import hashlib
import json
from pathlib import Path
import pickle
import shutil

import numpy as np


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare(inputs, template, tracks, joined, geometry_manifest, geometry_root,
            output, video, fps, max_frame=None):
    from shape_tools.memory import observation_features
    if output.exists():
        raise FileExistsError('Use a new bundle; preserve earlier evidence')
    template_plan=json.loads((template/'input_manifest.json').read_text())
    template_files=[p for name in ['original_src','shape_tools'] for p in (template/name).rglob('*')
                    if p.is_file() and '__pycache__' not in p.parts]
    template_files += [template/'whareformer.pt',template/'effective_config.yaml']
    for path in template_files:
        relative=path.relative_to(template).as_posix()
        if template_plan['prepared_hashes'].get(relative)!=sha(path):
            raise ValueError('Template path/hash mismatch: '+relative)
    acquisition = json.loads((inputs / 'acquisition.json').read_text())
    if acquisition['status'] != 'complete':
        raise ValueError('Incomplete official acquisition')
    for name, info in acquisition['files'].items():
        if sha(inputs / name) != info['sha256']:
            raise ValueError('Official input hash mismatch: ' + name)
    # Only trusted, checksum-verified pickles from the recorded official release.
    with (inputs / '2D_feat_masked_PCA_256d.pkl').open('rb') as stream:
        apps = pickle.load(stream)
    with (inputs / '3D_feat_aligned.pkl').open('rb') as stream:
        locs = pickle.load(stream)
    annotations = {r['frame_name']: r['annotations'] for r in
                   json.loads((inputs / 'object_annotations.json').read_text())['video_annotations']}
    if list(apps) != sorted(apps) or apps.keys() != locs.keys():
        raise ValueError('Feature frame order/key mismatch')
    predicted = {}
    for tid, items in json.loads(tracks.read_text())['tracks'].items():
        for row in items:
            key = row['frame'], row['detection_idx']
            if key in predicted:
                raise ValueError('Duplicate published observation')
            predicted[key] = (int(tid), row)
    full_rows = 0
    for frame, values in apps.items():
        anns, xyz = annotations[frame], np.asarray(locs[frame])
        app = np.asarray(values)
        if app.shape != (len(anns), 256) or xyz.shape != (len(anns), 3):
            raise ValueError('Feature shape mismatch: ' + frame)
        if not np.isfinite(app).all() or not np.isfinite(xyz).all():
            raise ValueError('Nonfinite official feature')
        for i, ann in enumerate(anns):
            row = predicted[frame, i][1]
            if ((row['observation_id'], row['name'], row['bbox']) !=
                    (ann['id'], ann['name'], ann['bounding_box']) or
                    not np.array_equal(np.asarray(row['xyz']), xyz[i].astype(float))):
                raise ValueError('Published order/metadata/XYZ mismatch')
            full_rows += 1
    if full_rows != len(predicted):
        raise ValueError('Published observation count mismatch')
    lookup = {}
    excluded = []
    for row in json.loads(joined.read_text()):
        if row['mapping_status'] != 'exact':
            excluded.append(dict(observation_key=row['observation_key'], reason=row['mapping_status']))
            continue
        key = row['frame_name'], row['annotation_id']
        if key in lookup:
            raise ValueError('Duplicate geometric join')
        lookup[key] = row
    geometries = {r['observation_key']: r for r in json.loads(geometry_manifest.read_text())}
    reps = ['da_raw_points', 'da_raw_superflex', 'moge_points', 'moge_superflex']
    frames, appearance, locations = [], [], []
    shapes, clouds, artifacts, cloud_artifacts = {}, {}, {}, {}
    offset = 0
    for frame in apps:
        idx = int(frame.rsplit('_', 1)[1])
        if max_frame is not None and idx > max_frame:
            break
        anns = annotations[frame]
        feature_ids, cloud_ids = [], []
        for i, ann in enumerate(anns):
            ids, raw_ids = {}, {}
            geo = lookup.get((frame, ann['id']))
            if geo is not None:
                if geo['detection_idx'] != i:
                    raise ValueError('Exact join detection index mismatch')
                original = geometries[geo['observation_key']]
                for rep in reps:
                    feature = observation_features(original, geometry_root, rep)
                    if feature is not None:
                        name = 'f' + str(len(shapes))
                        shapes[name] = feature[1]
                        ids[rep] = name
                        artifacts[geo['observation_key'] + '/' + rep] = original['representations'][rep]['sha256']
                for source, rep in [('da', 'da_raw_points'), ('moge', 'moge_points')]:
                    info = original['representations'][rep]
                    if info['status'] == 'unavailable':
                        continue
                    path = (geometry_root / info['path']).resolve()
                    if not path.is_relative_to(geometry_root.resolve()) or sha(path) != info['sha256']:
                        raise ValueError('Observed point path/hash mismatch')
                    with np.load(path, allow_pickle=False) as z:
                        points = z['camera_points'].copy()
                    name = 'c' + str(len(clouds))
                    clouds[name] = points
                    raw_ids[source] = name
                    cloud_artifacts[name] = dict(input_sha256=info['sha256'],
                        observation_key=geo['observation_key'], source=source)
            feature_ids.append(ids)
            cloud_ids.append(raw_ids)
        frames.append(dict(frame=frame, frame_index=idx, offset=offset, annotations=anns,
            shape_feature_ids=feature_ids, cloud_ids=cloud_ids,
            recorded_baseline_assignments={str(i): predicted[frame, i][0] for i in range(len(anns))}))
        appearance.append(np.asarray(apps[frame]))
        locations.append(np.asarray(locs[frame]))
        offset += len(anns)
    if not frames:
        raise ValueError('Empty frame scope')
    output.mkdir(parents=True)
    for name in ['original_src', 'shape_tools']:
        shutil.copytree(template / name, output / name, ignore=shutil.ignore_patterns('__pycache__'))
    for name in ['whareformer.pt', 'effective_config.yaml']:
        shutil.copyfile(template / name, output / name)
    np.savez_compressed(output / 'features.npz', app=np.concatenate(appearance), loc=np.concatenate(locations))
    np.savez_compressed(output / 'shape_features.npz', **shapes)
    np.savez_compressed(output / 'observed_clouds.npz', **clouds)
    (output / 'frames.json').write_text(json.dumps(frames, indent=2) + '\n')
    coverage = dict(expected_feature_frames=len(apps), expected_observations=full_rows,
        prepared_frames=len(frames), prepared_observations=offset,
        first_frame=frames[0]['frame_index'], final_frame=frames[-1]['frame_index'],
        complete_official_sequence=len(frames) == len(apps),
        geometry_frames=sum(any(row['shape_feature_ids']) for row in frames),
        shape_observations={rep: sum(rep in ids for row in frames for ids in row['shape_feature_ids']) for rep in reps},
        observed_clouds={s: sum(s in ids for row in frames for ids in row['cloud_ids']) for s in ('da','moge')},
        excluded_joins=excluded, metadata_xyz_mismatch_count=0)
    plan = dict(video=video, fps=fps, representations=reps, prefix_frames=len(frames),
        prefix_observations=offset, coverage=coverage,
        input_boundary='Reused official appearance/PCA/scene XYZ and verified sparse observed geometry; no new RGB extraction.',
        source_manifests={str(p.resolve()): sha(p) for p in [inputs/'acquisition.json', tracks, joined, geometry_manifest]},
        shape_artifact_hashes=artifacts, observed_cloud_artifacts=cloud_artifacts,
        cloud_conventions=dict(coordinate_convention='camera_points optical camera coordinates',
            scale_convention='as exported depth units; inter-view scale unverified'), acquisition=acquisition)
    plan['prepared_hashes'] = {p.relative_to(output).as_posix(): sha(p) for p in output.rglob('*') if p.is_file()}
    (output / 'input_manifest.json').write_text(json.dumps(plan, indent=2) + '\n')
    print(json.dumps(coverage, indent=2))
    return coverage


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['inputs','template','tracks','joined','geometry-manifest','geometry-root','output']:
        parser.add_argument('--'+name, type=Path, required=True)
    parser.add_argument('--video', required=True)
    parser.add_argument('--fps', type=int, required=True)
    parser.add_argument('--max-frame', type=int)
    args = parser.parse_args()
    prepare(**vars(args))
