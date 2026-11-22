"""Verified lifecycle for derived SuperFlex files; authoritative geometry stays intact.

CPU regeneration: input / surface. Diagnostic replay: original model, CUDA,
separate destination, with explicit numerical comparison (not promised byte-identical).
Scientific pipeline sources and original reports remain immutable.
"""
import argparse
from contextlib import contextmanager
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import time

import numpy as np

VERSION = 1
LEDGER = 'retention.json'
KINDS = {'input': 'input.npz', 'surface': 'reconstruction.ply', 'diagnostic_prediction': 'prediction.npz'}
PARAMETERS = ('scale', 'rotation', 'translation', 'exponents', 'exist', 'tapering', 'bending')


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1048576), b''): h.update(chunk)
    return h.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(json.dumps(value, indent=2, allow_nan=False), encoding='utf-8')
    os.replace(tmp, path)


def bound(root, relative):
    root = Path(root).resolve()
    raw = root / relative
    path = raw.resolve()
    if not path.is_relative_to(root) or raw.is_symlink():
        raise ValueError('Unsafe artifact path: ' + str(relative))
    return path


def checked(root, info):
    path = bound(root, info['path'])
    if sha(path) != info['sha256']: raise ValueError('Artifact checksum mismatch: ' + str(path))
    return path


def arrays(path):
    with np.load(path, allow_pickle=False) as z: return {k: z[k].copy() for k in z.files}


def exact_arrays(expected, actual):
    if set(expected) != set(actual): raise ValueError('Array keys differ')
    for key in expected:
        a, b = expected[key], actual[key]
        if a.dtype != b.dtype or not np.array_equal(a, b):
            raise ValueError('Array differs: ' + key)


def input_arrays(root, entry):
    from shape_tools.geometry import prepare_superflex_input
    cloud = arrays(checked(root, entry['cloud']))['camera_points']
    normalized, center, scale, selected = prepare_superflex_input(cloud, seed=entry['seed'])
    return dict(normalized_points=normalized, sample_indices=selected, translation=center, scale=np.asarray(scale))


def surface_bytes(root, entry):
    from superflex.utils.predictions_handler import PredictionHandler
    params = arrays(checked(root, entry['parameters']))
    # Neither pc nor assignment is read by get_mesh; empty placeholders are deliberate.
    params.update(names=[entry['item_id']], pc=np.empty((1, 0, 3)), assign_matrix=np.empty((1, 0, 0)))
    handler = PredictionHandler(params)
    handler.colors = np.asarray(entry['palette_rgb'], dtype=np.uint8)
    mesh = handler.get_mesh(0, resolution=entry['mesh_resolution'])
    return mesh.export(file_type='ply')


def surface_palette(root, entry):
    """Retain the tiny random visualization palette, not the derived mesh."""
    import colorsys
    from plyfile import PlyData
    with checked(root, entry).open('rb') as stream: ply = PlyData.read(stream)
    element = ply['face']
    if not {'red', 'green', 'blue'}.issubset(element.data.dtype.names): element = ply['vertex']
    colors = np.unique(np.stack([element.data[k] for k in ('red', 'green', 'blue')], axis=-1), axis=0)
    params = arrays(checked(root, entry['parameters']))
    count = params['scale'].shape[1]
    active = np.flatnonzero(params['exist'][0] > 0.5)
    if len(colors) != len(active): raise ValueError('Cannot recover unambiguous original palette')
    palette = np.zeros((count, 3), dtype=np.uint8)
    assigned = set()
    for color in colors:
        hue = colorsys.rgb_to_hls(*(color.astype(float)/255))[0]
        distances = np.abs(active/count - hue)
        distances = np.minimum(distances, 1-distances)
        primitive = int(active[np.argmin(distances)])
        if primitive in assigned: raise ValueError('Ambiguous primitive color')
        assigned.add(primitive)
        palette[primitive] = color
    # This palette is accepted only if the complete regenerated PLY SHA matches.
    return palette.tolist()


def cpu_bytes(root, entry):
    if entry['kind'] == 'surface': return surface_bytes(root, entry)
    if entry['kind'] == 'input':
        # Preserve the original key order used by pipeline.py for byte equivalence.
        data = input_arrays(root, entry)
        buffer = io.BytesIO()
        np.savez_compressed(buffer, **{k: data[k] for k in ('sample_indices', 'normalized_points', 'translation', 'scale')})
        return buffer.getvalue()
    if entry['kind'] == 'diagnostic_prediction':
        import torch
        from superflex.data.dataloader import denormalize_points
        prepared = input_arrays(root, entry)
        pc = denormalize_points(torch.from_numpy(prepared['normalized_points']).float().unsqueeze(0),
                                np.array([prepared['translation']]), np.array([float(prepared['scale'])]), False).numpy()
        if '_assignment_array' in entry: assignment = entry['_assignment_array']
        else:
            archive = checked(root, entry['assignment_archive'])
            with np.load(archive, allow_pickle=False) as z: assignment = z[entry['assignment_key']].copy()
        parameters = arrays(checked(root, entry['parameters']))
        values = dict(names=np.array([entry['item_id']]), pc=pc, assign_matrix=assignment)
        values.update({k: parameters[k] for k in PARAMETERS})
        buffer = io.BytesIO()
        np.savez_compressed(buffer, **values)
        return buffer.getvalue()
    raise ValueError('Unsupported derived artifact kind')


def entry_for(root, source, key, report, cloud_info, seed, kind):
    artifacts = report['artifacts']
    original = artifacts[kind]
    expected_folder = 'superflex_' + source + '/' + key + '/'
    if original['path'] != expected_folder + KINDS[kind] or artifacts['parameters']['path'] != expected_folder + 'shape_parameters.npz':
        raise ValueError('Unexpected removable artifact path')
    if cloud_info['path'] != 'clouds_' + source + '/' + key + '/points.npz': raise ValueError('Unexpected retained cloud path')
    return dict(kind=kind, path=original['path'], sha256=original['sha256'], source=source,
                item_id=key, seed=seed, mesh_resolution=30, parameters=artifacts['parameters'],
                cloud=cloud_info, stage_signature=report['signature'],
                regeneration='cpu_exact' if kind != 'diagnostic_prediction' else 'cpu_exact_from_assignment_shard')


def replay_diagnostics(root, entries, destination):
    """Replay the unchanged original producer into a separate directory, never over originals."""
    import copy
    from shape_tools import pipeline
    root, destination = Path(root).resolve(), Path(destination).resolve()
    if destination == root or destination.is_relative_to(root):
        raise ValueError('Use a separate regeneration destination outside the authoritative block')
    destination.mkdir(parents=True, exist_ok=False)
    run = read(root / 'run.json')
    manifest = run['manifest']
    config = run['config']
    selected = {e['item_id'] for e in entries}
    selected_rows = [r for r in manifest['observations'] if pipeline.item_id(r) in selected]
    for source in sorted({e['source'] for e in entries}):
        wanted = {e['item_id'] for e in entries if e['source'] == source}
        target = destination / source
        target.mkdir()
        index = read(root / ('clouds_' + source + '_index.json'))
        subset = {}
        for key in wanted:
            item = copy.deepcopy(index[key])
            original = item['artifacts']['points']
            item['artifacts']['points']['path'] = str(checked(root, original))
            subset[key] = item
        save(target / ('clouds_' + source + '_index.json'), subset)
        cfg = copy.deepcopy(config)
        cfg['sources'] = [source]
        pipeline.superflex(dict(schema_version=1, observations=[r for r in selected_rows if pipeline.item_id(r) in wanted]), target, cfg)
    return {e['path']: destination / e['source'] / ('superflex_' + e['source']) / e['item_id'] / 'prediction.npz' for e in entries}


def compare_diagnostic(original, replayed):
    a, b = arrays(original), arrays(replayed)
    if set(a) != set(b): raise ValueError('Diagnostic replay keys differ')
    maximum = 0.0
    for key in a:
        if a[key].shape != b[key].shape or a[key].dtype != b[key].dtype: raise ValueError('Replay shape/dtype differs: ' + key)
        if np.issubdtype(a[key].dtype, np.number):
            np.testing.assert_allclose(a[key], b[key], rtol=1e-5, atol=1e-6)
            maximum = max(maximum, float(np.max(np.abs(a[key] - b[key]))) if a[key].size else 0.0)
        elif not np.array_equal(a[key], b[key]): raise ValueError('Replay metadata differs: ' + key)
    return dict(maximum_absolute_difference=maximum, byte_identical=sha(original) == sha(replayed), rtol=1e-5, atol=1e-6)


def recipe_provenance(root):
    from shape_tools import pipeline
    import superflex.utils.predictions_handler as handler
    import superflex.utils.visualizations as visualization
    import trimesh
    run = read(Path(root) / 'run.json')
    return dict(version=VERSION, pipeline_sources=pipeline.source_hashes(),
                handler_sha256=sha(handler.__file__), colors_sha256=sha(visualization.__file__),
                config_sha256=pipeline.digest(run['config']), numpy=np.__version__, trimesh=trimesh.__version__)


def probe(root, receipt, workdir, count=3):
    root = Path(root).resolve()
    run = read(root / 'run.json')
    entries = []
    for source in ('da', 'moge'):
        index = read(root / ('superflex_' + source + '_index.json'))
        clouds = read(root / ('clouds_' + source + '_index.json'))
        keys = sorted(k for k, v in index.items() if v['status'] == 'ready')
        for i in np.linspace(0, len(keys)-1, min(count, len(keys)), dtype=int):
            key = keys[i]
            entries.append(entry_for(root, source, key, index[key], clouds[key]['artifacts']['points'], run['config']['superflex']['seed'], 'diagnostic_prediction'))
    generated = replay_diagnostics(root, entries, workdir)
    results = []
    for entry in entries:
        comparison = compare_diagnostic(checked(root, entry), generated[entry['path']])
        results.append(dict(path=entry['path'], **comparison))
    value = dict(status='passed', scope='stratified CUDA replay sample, not exhaustive replay',
                 root=str(root), provenance=recipe_provenance(root), samples=results, created_unix=time.time())
    save(receipt, value)
    print('GPU_REPLAY_PROBE', json.dumps(value), flush=True)


def probe_cpu(root, receipt, count=3):
    root = Path(root).resolve()
    run = read(root / 'run.json')
    results = []
    for source in ('da', 'moge'):
        index = read(root / ('superflex_' + source + '_index.json'))
        clouds = read(root / ('clouds_' + source + '_index.json'))
        keys = sorted(k for k, v in index.items() if v['status'] == 'ready')
        for i in np.linspace(0, len(keys)-1, min(count, len(keys)), dtype=int):
            key = keys[i]
            for kind in KINDS:
                entry = entry_for(root, source, key, index[key], clouds[key]['artifacts']['points'], run['config']['superflex']['seed'], kind)
                if kind == 'surface': entry['palette_rgb'] = surface_palette(root, entry)
                if kind == 'diagnostic_prediction': entry['_assignment_array'] = arrays(checked(root, entry))['assign_matrix']
                data = cpu_bytes(root, entry)
                if hashlib.sha256(data).hexdigest() != entry['sha256']: raise ValueError('CPU probe failed: ' + entry['path'])
                results.append(dict(path=entry['path'], byte_identical=True))
    value = dict(status='passed', method='cpu_exact_with_assignment_shard', provenance=recipe_provenance(root),
                 samples=results, root=str(root), created_unix=time.time())
    save(receipt, value)
    print('CPU_REGENERATION_PROBE', json.dumps(value), flush=True)


@contextmanager
def locked(root):
    path = Path(root) / '.retention.lock'
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    try: yield
    finally: path.unlink()


def compact(root, receipt, apply=False, limit=None):
    root = Path(root).resolve()
    if root.parent.name != 'geometry' or not root.name.isdigit(): raise ValueError('Only numbered geometry blocks may be compacted')
    if not (root / 'observations.json').is_file(): raise ValueError('Block has not been exported')
    proof = read(receipt)
    if proof['status'] != 'passed' or proof.get('method') != 'cpu_exact_with_assignment_shard' or proof['provenance'] != recipe_provenance(root):
        raise ValueError('CPU proof incompatible with this pipeline/configuration/environment')
    with locked(root):
        ledger_path = root / LEDGER
        ledger = read(ledger_path) if ledger_path.exists() else dict(schema_version=VERSION, state='prepared', entries={}, provenance=proof['provenance'], regeneration_receipt=proof)
        if ledger['provenance'] != proof['provenance']: raise ValueError('Existing ledger incompatible')
        run = read(root / 'run.json')
        archive_path = root / 'retention_assignments.npz'
        if ledger.get('assignment_archive'):
            assignment_values = arrays(checked(root, ledger['assignment_archive']))
            archive_info = ledger['assignment_archive']
            archive_payload = None
        else:
            assignment_values = {}
            for source in ('da', 'moge'):
                for key, info in read(root / ('superflex_' + source + '_index.json')).items():
                    if info['status'] == 'ready':
                        assignment_values[source+'__'+key] = arrays(checked(root, info['artifacts']['diagnostic_prediction']))['assign_matrix']
            buffer = io.BytesIO()
            np.savez_compressed(buffer, **{k: assignment_values[k] for k in sorted(assignment_values)})
            archive_payload = buffer.getvalue()
            archive_info = dict(path=archive_path.name, sha256=hashlib.sha256(archive_payload).hexdigest())
            ledger['assignment_archive'] = archive_info
        removed_bytes = removed_allocated = removed_files = 0
        validated = []
        for source in ('da', 'moge'):
            index = read(root / ('superflex_' + source + '_index.json'))
            clouds = read(root / ('clouds_' + source + '_index.json'))
            keys = sorted(k for k, v in index.items() if v['status'] == 'ready')
            if limit is not None: keys = keys[:limit]
            for key in keys:
                report = index[key]
                params_path = checked(root, report['artifacts']['parameters'])
                params = arrays(params_path)
                for kind in ('input', 'surface', 'diagnostic_prediction'):
                    entry = entry_for(root, source, key, report, clouds[key]['artifacts']['points'], run['config']['superflex']['seed'], kind)
                    if kind == 'diagnostic_prediction':
                        entry.update(assignment_archive=archive_info, assignment_key=source+'__'+key)
                    path = bound(root, entry['path'])
                    if not path.exists():
                        old = ledger['entries'].get(entry['path'])
                        if not old or any(old[k] != entry[k] for k in entry): raise ValueError('Unregistered missing file: ' + str(path))
                        continue
                    checked(root, entry)
                    if kind != 'diagnostic_prediction':
                        if kind == 'surface': entry['palette_rgb'] = surface_palette(root, entry)
                        payload = cpu_bytes(root, entry)
                        if hashlib.sha256(payload).hexdigest() != entry['sha256']:
                            raise ValueError('CPU regeneration is not byte-identical: ' + str(path))
                    else:
                        data = arrays(path)
                        for name in PARAMETERS:
                            if data[name].dtype != params[name].dtype or not np.array_equal(data[name], params[name]):
                                raise ValueError('Diagnostic parameters inconsistent')
                        # Preserve only unique assignment data; GPU replay was not numerically identical.
                        payload = cpu_bytes(root, dict(entry, _assignment_array=assignment_values[entry['assignment_key']]))
                        if hashlib.sha256(payload).hexdigest() != entry['sha256']:
                            raise ValueError('Diagnostic CPU regeneration is not byte-identical: ' + str(path))
                        entry['original_arrays'] = {k: dict(shape=list(v.shape), dtype=str(v.dtype), sha256=hashlib.sha256(v.tobytes()).hexdigest()) for k, v in data.items()}
                    meta = path.stat()
                    entry.update(original_bytes=meta.st_size, original_allocated_bytes=meta.st_blocks*512 if hasattr(meta, 'st_blocks') else meta.st_size)
                    ledger['entries'][entry['path']] = entry
                    validated.append(entry)
                if len(validated) % 192 == 0: print('VERIFIED', root.name, source, len(validated), flush=True)
        ledger['state'] = 'prepared'
        ledger['recipe_version'] = VERSION
        if apply:
            # Ledger durable and complete before the first unlink. Each path is rechecked immediately before unlink.
            if archive_payload is not None:
                if archive_path.exists() and sha(archive_path) != archive_info['sha256']: raise ValueError('Refuse to overwrite different assignment archive')
                tmp = archive_path.with_suffix('.npz.preparing')
                tmp.write_bytes(archive_payload)
                os.replace(tmp, archive_path)
                checked(root, archive_info)
            save(ledger_path, ledger)
            for entry in validated:
                path = checked(root, entry)
                path.unlink()
                removed_bytes += entry['original_bytes']
                removed_allocated += entry['original_allocated_bytes']
                removed_files += 1
            ledger.update(state='compacted', compacted_unix=time.time())
            save(ledger_path, ledger)
            annotate(root, ledger)
        result = dict(root=str(root), apply=apply, verified_files=len(validated), removed_files=removed_files,
                      removed_bytes=removed_bytes, removed_allocated_bytes=removed_allocated,
                      ledger_entries=len(ledger['entries']), assignment_archive_bytes=archive_path.stat().st_size if archive_path.exists() else len(archive_payload or b''),
                      assignment_archive_new=archive_payload is not None)
        if apply: save(root / 'retention_result.json', result)
        print('COMPACTION_RESULT', json.dumps(result), flush=True)
        return result


def annotate(root, ledger=None):
    root = Path(root)
    ledger = ledger or read(root / LEDGER)
    rows = read(root / 'observations.json')
    for row in rows:
        for rep in row['representations'].values():
            if rep['status'] != 'ready': continue
            for info in [rep, *rep.get('artifacts', {}).values()]:
                if info.get('path') in ledger['entries']:
                    info['storage'] = dict(state='regenerable', ledger=LEDGER,
                                           method=ledger['entries'][info['path']]['regeneration'])
    save(root / 'observations.json', rows)


def install_cache_adapter(pipeline, root):
    """Keep original scientific signatures; only registered, reproducible absences are accepted."""
    root = Path(root).resolve()
    if not (root / LEDGER).exists(): return
    ledger = read(root / LEDGER)
    if ledger['provenance'] != recipe_provenance(root): raise ValueError('Retention environment changed')
    verified = set()
    def verify(info):
        identity = (info['path'], info['sha256'])
        if identity not in verified:
            checked(root, info)
            verified.add(identity)
    def cached(folder, signature):
        report_path = folder / 'report.json'
        if not report_path.exists(): return None
        result = read(report_path)
        if result['signature'] != signature: raise ValueError('Incompatible resume: ' + str(folder))
        if result['status'] == 'ready':
            for info in result['artifacts'].values():
                path = bound(root, info['path'])
                if path.exists(): verify(info)
                else:
                    entry = ledger['entries'].get(info['path'])
                    if not entry or entry['sha256'] != info['sha256'] or entry['stage_signature'] != signature:
                        raise ValueError('Unregistered missing/corrupt artifact: ' + str(path))
                    verify(entry['parameters'])
                    verify(entry['cloud'])
                    if entry.get('assignment_archive'): verify(entry['assignment_archive'])
        return result
    pipeline.cached = cached


def regenerate(root, relative, destination=None):
    root = Path(root).resolve()
    ledger = read(root / LEDGER)
    if ledger['provenance'] != recipe_provenance(root): raise ValueError('Pinned regeneration environment changed')
    entry = ledger['entries'][relative]
    if entry['kind'] == 'diagnostic_prediction' and entry['regeneration'] == 'cuda_replay_numerical':
        if destination is None: raise ValueError('CUDA diagnostic replay requires --destination outside this block')
        result = replay_diagnostics(root, [entry], destination)
        path = result[relative]
        replay = arrays(path)
        for key, meta in entry['original_arrays'].items():
            if list(replay[key].shape) != meta['shape'] or str(replay[key].dtype) != meta['dtype']: raise ValueError('Replay array contract differs')
        exact = sha(path) == entry['sha256']
        save(Path(destination) / 'regeneration_receipt.json', dict(original=entry, regenerated_path=str(path), sha256=sha(path),
             byte_identical=exact, numerical_equivalence='sample-validated recipe; original full arrays intentionally not retained'))
        return path
    target = bound(root, relative) if destination is None else Path(destination).resolve()
    if target.exists():
        if sha(target) != entry['sha256']: raise ValueError('Refusing to overwrite different data')
        return target
    data = cpu_bytes(root, entry)
    if hashlib.sha256(data).hexdigest() != entry['sha256']: raise ValueError('Regeneration checksum mismatch')
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_name(target.name + '.regenerating')
    temp.write_bytes(data)
    os.replace(temp, target)
    return target


def resolve_surface(root, info):
    path = bound(root, info['path'])
    if not path.exists(): regenerate(root, info['path'])
    return checked(root, info)


def retained_features(root, info, count=1024, seed=20261109):
    """Use unchanged feature extraction with a temporary CPU-regenerated PLY."""
    from shape_tools.comparison import load_features
    root = Path(root).resolve()
    if bound(root, info['path']).exists(): return load_features(checked(root, info), count=count, seed=seed)
    ledger = read(root / LEDGER)
    if ledger['provenance'] != recipe_provenance(root): raise ValueError('Pinned environment changed')
    entry = ledger['entries'][info['path']]
    if entry['kind'] != 'surface' or entry['sha256'] != info['sha256']: raise ValueError('Invalid retained surface')
    payload = cpu_bytes(root, entry)
    if hashlib.sha256(payload).hexdigest() != info['sha256']: raise ValueError('Regenerated surface differs')
    with tempfile.TemporaryDirectory(prefix='superflex_features_') as directory:
        path = Path(directory) / 'reconstruction.ply'
        path.write_bytes(payload)
        return load_features(path, count=count, seed=seed)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    probe_p = sub.add_parser('probe')
    probe_p.add_argument('--root', type=Path, required=True)
    probe_p.add_argument('--receipt', type=Path, required=True)
    probe_p.add_argument('--workdir', type=Path, required=True)
    probe_p.add_argument('--count', type=int, default=3)
    cpu = sub.add_parser('probe-cpu')
    cpu.add_argument('--root', type=Path, required=True)
    cpu.add_argument('--receipt', type=Path, required=True)
    cpu.add_argument('--count', type=int, default=3)
    c = sub.add_parser('compact')
    c.add_argument('--root', type=Path, required=True)
    c.add_argument('--receipt', type=Path, required=True)
    c.add_argument('--apply', action='store_true')
    c.add_argument('--limit', type=int)
    r = sub.add_parser('regenerate')
    r.add_argument('--root', type=Path, required=True)
    r.add_argument('--path', required=True)
    r.add_argument('--destination', type=Path)
    a = p.parse_args()
    if a.command == 'probe': probe(a.root, a.receipt, a.workdir, a.count)
    elif a.command == 'probe-cpu': probe_cpu(a.root, a.receipt, a.count)
    elif a.command == 'compact': compact(a.root, a.receipt, a.apply, a.limit)
    else: print(regenerate(a.root, a.path, a.destination))


if __name__ == '__main__': main()
