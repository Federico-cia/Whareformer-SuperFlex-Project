"""Griglia di configurazioni della memoria geometrica (opzione A) sul sistema completo.

Per ogni configurazione: tracker Whareformer originale (bundle verificato), GeometryMatcher,
memoria PositionStateMemory tramite MultiHypothesisPipeline, su un prefisso del video fino a
`final_frame`; poi metriche ufficiali (IDF1, mPCL) con il valutatore verificato degli autori.
Esegue anche la baseline W0 (geometria disattivata) come riferimento.

Rappresentazioni: `da_raw_points` (punti osservati accumulati, solo CPU) oppure
`da_raw_superflex` (forme SuperFlex della memoria, worker GPU obbligatorio e descrittori
SuperFlex delle osservazioni forniti con --query-features). Nessun parametro ha valori
predefiniti: tutto viene dal file della griglia. Non sceglie automaticamente nulla se la
regola di selezione non è dichiarata nel file. Cartella di output nuova, mai sovrascritta.

Uso:
  python run_memory_grid.py --bundle BUNDLE --aligned ALLINEATE --grid griglia.json --out NUOVA
         [--variants nome1,nome2] [--superflex-runtime runtime.json] [--query-features q.npz]
"""
import argparse
import copy
import csv
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import sys
import time
import types
import numpy as np

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class AlignedClouds:
    """Nuvole allineate a piena risoluzione (build_aligned_fullres.py), lette su richiesta."""
    def __init__(self, folder):
        folder = Path(folder)
        self.rows = {r['key']: r for r in map(json.loads, (folder / 'per_observation.jsonl').read_text().splitlines())
                     if r.get('status') == 'ok'}
        self.npz = np.load(folder / 'world_clouds_aligned_fullres.npz', allow_pickle=False)
        self.hashes = {n: sha(folder / n) for n in ('per_observation.jsonl', 'summary.json')}

    def camera(self, key):
        r = self.rows[key]
        fx, fy, cx, cy = r['intrinsics']
        return dict(world_to_camera=np.linalg.inv(np.asarray(r['c2w'], float)).tolist(),
                    intrinsics=[fx, fy, cx, cy], image_size=[int(round(2 * cx)), int(round(2 * cy))])

    def points(self, key):
        return self.npz[key.replace('/', '__')].astype(float)


def observed_query_feature(points):
    from scene_geometry import farthest_points
    from shape_tools.geometry import normalize_shape
    from shape_tools.metrics import descriptors
    p = normalize_shape(points[farthest_points(points, 1024)])
    return (p, *descriptors(p))


def load_frames(bundle, final_frame):
    sys.path.insert(0, str(bundle / 'original_src'))
    namespace = types.ModuleType('tracking'); namespace.__path__ = [str(bundle / 'original_src/tracking')]
    sys.modules.setdefault('tracking', namespace)
    from tracking.tracker.detection import Detection
    plan = json.loads((bundle / 'input_manifest.json').read_text())
    with np.load(bundle / 'features.npz', allow_pickle=False) as z:
        app, loc = z['app'].copy(), z['loc'].copy()
    frames = []
    for row in json.loads((bundle / 'frames.json').read_text()):
        idx = row['frame_index']
        if idx > final_frame:
            break
        off = row['offset']
        keys = [f'{plan["video"]}/{row["frame"]}__d{i}' for i in range(len(row['annotations']))]
        dets = [Detection(dict(frame=idx, detection_idx=i, obj_name=a['name'], bbox=a['bounding_box'],
                               app=app[off + i], loc=loc[off + i])) for i, a in enumerate(row['annotations'])]
        frames.append(dict(detections=dets, metadata=dict(frame_name=row['frame'], frame_idx=idx,
                           timestamp=idx / plan['fps']), keys=keys, names=[a['name'] for a in row['annotations']]))
    return plan, frames


def whareformer_factory(bundle, cache, seed, threads):
    import torch, yaml
    from tracking.tracker.tracker import StandardTracker
    plan = json.loads((bundle / 'input_manifest.json').read_text())
    cfg = yaml.safe_load((bundle / 'effective_config.yaml').read_text())
    checkpoint = bundle / 'whareformer.pt'
    state = torch.load(checkpoint, map_location='cpu', weights_only=True)
    cpu = Path(cache) / (sha(checkpoint) + '_cpu.pt')
    if not cpu.exists():
        torch.save(state, cpu)
    torch.set_num_threads(threads)
    params = copy.deepcopy(cfg['tracking']); params.update(model=cfg['model'], device_id=None, app_dim=256)
    params['matcher_params']['model_path'] = str(cpu.resolve())
    def factory():
        torch.manual_seed(seed)
        return StandardTracker(copy.deepcopy(params), plan['fps'])
    return factory


def run_variant(name, spec, grid, frames, aligned, queries, factory, video, out, worker=None, progress=True):
    from frame_coordinator import FrameCoordinator
    from geometry_matcher import GeometryMatcher, GeometryConfig
    from scene_memory import SceneMemoryConfig, SceneObservation
    from position_state_memory import PositionConfig
    from multi_hypothesis_pipeline import MultiHypothesisPipeline
    from cloud_memory import RegistrationConfig
    from tracking_evaluation import export_observations
    tracker = factory()
    baseline = spec is None
    if baseline:
        tracker.matcher = GeometryMatcher(tracker.matcher, video, GeometryConfig('disabled', grid['matcher']['representation']))
        runner = FrameCoordinator(tracker)
    else:
        from registration_verifier import DiagnosticErrorVerifier
        memory = dict(grid['memory'])
        relative = (memory.pop('voxel_fraction'), memory.pop('outlier_fraction'))
        verifier = DiagnosticErrorVerifier(json.loads(Path(grid['verifier']['model']).read_text()))
        memory_config = SceneMemoryConfig(voxel_size=1.0, outlier_radius=1.0,
                                          maximum_predicted_error=grid['verifier']['maximum_predicted_error'], **memory)
        position = PositionConfig(**{**grid['position_fixed'], **{k: v for k, v in spec.items() if k != 'name'},
                                     'selection_provenance': grid['selection_provenance']})
        reconstruction_root = None
        if grid['matcher']['representation'].endswith('_superflex'):
            if worker is None:
                raise ValueError('SuperFlex representation requires --superflex-runtime')
            reconstruction_root = Path(out) / 'superflex_cache' / name
        runner = MultiHypothesisPipeline(tracker, video, GeometryConfig(**grid['matcher']), memory_config, verifier,
                                         registration_config=RegistrationConfig(**grid['registration']),
                                         reconstruction_root=reconstruction_root, position_config=position,
                                         relative_resolution=relative)
    rows, statuses, started = [], Counter(), time.perf_counter()
    path = Path(out) / f'{name}.jsonl'
    with path.open('x', encoding='utf-8') as stream:
        for n, f in enumerate(frames):
            if baseline:
                result = runner.step(f['detections'], f['metadata'], f['keys'])
            else:
                feats = {k: queries.get(k) for k in f['keys']}
                scene = {k: SceneObservation(k, f['metadata']['frame_idx'], f['metadata']['timestamp'],
                                             aligned.points(k), True, 'unknown', '',
                                             provenance=dict(alpha_beta=aligned.rows[k]['alpha_beta_source']),
                                             camera=aligned.camera(k))
                         for k in f['keys'] if k in aligned.rows}
                result = runner.step(f['detections'], f['metadata'], f['keys'], feats, scene)
                pending = runner.snapshot().get('pending_reconstructions', [])
                if pending:
                    for rid in pending:
                        worker(Path(reconstruction_root) / rid)
                    runner.resolve_reconstructions()
                for e in result['updates']:
                    statuses[e.get('diagnostics', {}).get('status', e['status'])] += 1
            row = dict(frame_index=f['metadata']['frame_idx'], assignments=result['assignments'],
                       detections=len(f['keys']),
                       evaluation_observations=export_observations(f['detections'], f['keys'], result['assignments']),
                       evaluation_timestamp=f['metadata']['timestamp'], evaluation_key_order=list(f['keys']))
            stream.write(json.dumps(row) + '\n')
            rows.append(row)
            if progress and n % 500 == 0:
                print(json.dumps(dict(variant=name, frame=n, of=len(frames), s=round(time.perf_counter() - started))), flush=True)
    summary = dict(name=name, baseline=baseline, frames=len(rows), seconds=round(time.perf_counter() - started, 1),
                   memory_statuses=dict(statuses), predictions_sha256=sha(path))
    if not baseline:
        geometry = runner.snapshot()['geometry']
        summary['tracks_with_memory'] = len(geometry)
        summary['states_final'] = sum(len(e['value'].states) for e in geometry.values())
        summary['shape_versions'] = sum(e['value'].shape_version for e in geometry.values())
        summary['withheld_views'] = sum(len(v) for e in geometry.values() for v in e['value'].withheld.values())
    return rows, summary


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bundle', type=Path, required=True)
    ap.add_argument('--aligned', type=Path, required=True)
    ap.add_argument('--grid', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--variants', help='Sottoinsieme di nomi, separati da virgola')
    ap.add_argument('--superflex-runtime', type=Path)
    ap.add_argument('--query-features', type=Path, help='NPZ con descrittori SuperFlex delle osservazioni')
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=False)
    grid = json.loads(a.grid.read_text())
    required = ('video', 'final_frame', 'fps', 'seed', 'torch_threads', 'matcher', 'memory', 'registration',
                'verifier', 'position_fixed', 'variants', 'selection', 'selection_provenance')
    missing = [k for k in required if k not in grid]
    if missing:
        raise ValueError(f'Grid file missing explicit fields: {missing}')
    # Percorsi del file della griglia relativi alla sua cartella.
    grid['verifier']['model'] = str((a.grid.resolve().parent / grid['verifier']['model']).resolve())
    (a.out / 'grid.json').write_text(json.dumps(grid, indent=2))
    plan, frames = load_frames(a.bundle, grid['final_frame'])
    aligned = AlignedClouds(a.aligned)
    names = {}
    for f in frames:
        names.update(zip(f['keys'], f['names']))
    mismatch = [k for k in aligned.rows if k in names and names[k] != aligned.rows[k]['identity']]
    if mismatch:
        raise ValueError(f'Identity mismatch between bundle detections and aligned clouds: {mismatch[:5]}')
    used = [k for k in aligned.rows if k in names]
    queries = {}
    if grid['matcher']['representation'] == 'da_raw_points':
        for k in used:
            queries[k] = observed_query_feature(aligned.points(k))
    else:
        if a.query_features is None:
            raise ValueError('SuperFlex representation requires --query-features')
        with np.load(a.query_features, allow_pickle=False) as z:
            for k in used:
                tag = k.replace('/', '__')
                if tag + '__d2' in z.files:
                    queries[k] = (z[tag + '__points'], z[tag + '__d2'], z[tag + '__spectrum'])
    worker = None
    if a.superflex_runtime:
        from deferred_scene_superflex import validate_request
        from scene_superflex_worker import ProductionBackend, process
        config = json.loads(a.superflex_runtime.read_text())
        runtime = dict(config.get('superflex', config))
        for key in ('checkpoint', 'config'):
            runtime[key] = str((a.superflex_runtime.resolve().parent / runtime[key]).resolve())
        backend = ProductionBackend(runtime)   # modello caricato una sola volta
        def worker(folder):
            r = validate_request(folder)
            return process(Path(folder) / r['input']['path'], r['input']['sha256'], Path(folder) / 'worker',
                           backend=backend)
    cache = a.out / 'assets'; cache.mkdir()
    factory = whareformer_factory(a.bundle, cache, grid['seed'], grid['torch_threads'])
    chosen = set(a.variants.split(',')) if a.variants else None
    variants = [('W0', None)] + [(v['name'], v) for v in grid['variants'] if chosen is None or v['name'] in chosen]
    from tracking_evaluation import EvaluationPolicy, OriginalTrackingEvaluator, results_from_rows
    evaluator = OriginalTrackingEvaluator(a.bundle / 'original_src',
                                          EvaluationPolicy(fps=grid['fps'], final_frame=grid['final_frame'], scope='diagnostic_prefix'))
    report = dict(video=grid['video'], frames=len(frames), final_frame=grid['final_frame'],
                  observations_with_aligned_geometry=len(used), observations_total=len(names),
                  inputs=dict(bundle_manifest=sha(a.bundle / 'input_manifest.json'), aligned=aligned.hashes,
                              grid=sha(a.grid), code={n: sha(HERE / n) for n in
                              ('run_memory_grid.py', 'position_state_memory.py', 'multi_hypothesis_pipeline.py',
                               'frame_coordinator.py', 'geometry_matcher.py', 'tracking_evaluation.py')}),
                  variants=[])
    for name, spec in variants:
        try:
            rows, summary = run_variant(name, spec, grid, frames, aligned, queries, factory, grid['video'], a.out, worker)
            try:
                summary['metrics'] = evaluator.score(results_from_rows(rows))
                summary['metrics'].pop('pcl_rows', None)
                summary['status'] = 'scored'
            except Exception as error:
                summary.update(status='evaluation_failed', error=f'{type(error).__name__}: {error}')
        except Exception as error:
            summary = dict(name=name, status='failed', error=f'{type(error).__name__}: {error}')
        summary['config'] = spec
        report['variants'].append(summary)
        (a.out / 'summary.json').write_text(json.dumps(report, indent=2, default=str))
        print(json.dumps({k: summary.get(k) for k in ('name', 'status', 'seconds', 'error')}), flush=True)
    primary, secondary = grid['selection']['primary'], grid['selection'].get('secondary')
    scored = [v for v in report['variants'] if v.get('status') == 'scored' and v['config'] is not None]
    with (a.out / 'table.csv').open('x', newline='', encoding='utf-8') as stream:
        fields = ['name', 'status', 'minimum_consistency', 'depth_margin', primary] + ([secondary] if secondary else []) + \
                 ['states_final', 'shape_versions', 'withheld_views', 'seconds']
        w = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore'); w.writeheader()
        for v in report['variants']:
            w.writerow({**(v.get('config') or {}), **(v.get('metrics') or {}), **v})
    if scored:
        key = lambda v: tuple(v['metrics'].get(m) if v['metrics'].get(m) is not None else -1e9 for m in (primary, secondary) if m)
        best = max(scored, key=key)
        report['selection'] = dict(rule=grid['selection'], best=best['name'], best_values={m: best['metrics'].get(m) for m in (primary, secondary) if m},
                                   baseline=next((v['metrics'] for v in report['variants'] if v['name'] == 'W0' and v.get('status') == 'scored'), None),
                                   note='Differenze di pochi eventi su uno o due video possono essere rumore; leggere anche il criterio secondario.')
        (a.out / 'summary.json').write_text(json.dumps(report, indent=2, default=str))
    print('FINE', json.dumps(report.get('selection')), flush=True)


if __name__ == '__main__':
    main()
