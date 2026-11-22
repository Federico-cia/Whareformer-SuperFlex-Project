"""SuperFlex worker for already sampled FPS input; never re-samples model input.

Run on the existing GPU environment. A test double is clearly tagged and cannot
be attached to production training exports by default.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time
import numpy as np
from scene_geometry import farthest_points


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_input(path, expected_sha256):
    if sha(path) != expected_sha256:
        raise ValueError('FPS input checksum mismatch')
    with np.load(path, allow_pickle=False) as z:
        p, indices = z['object_points'].copy(), z['sample_indices'].copy()
        normalized, center, scale = z['normalized_points'].copy(), z['translation'].copy(), float(z['scale'])
        if (str(z['sampling']) != 'deterministic_fps_4096' or not bool(z['observed_only'])
                or normalized.shape != (4096, 3) or indices.shape != (4096,)
                or not np.isfinite(normalized).all() or not np.isfinite(scale) or scale <= 0):
            raise ValueError('Invalid observed FPS input')
        if not np.array_equal(indices, farthest_points(p, 4096)):
            raise ValueError('Input does not match deterministic FPS')
        if (not np.array_equal(z['selected_points'], p[indices])
                or not np.array_equal(normalized, (p[indices] - center) / scale)):
            raise ValueError('FPS normalization/inverse mismatch')
        return dict(normalized=normalized, center=center, scale=scale,
                    shape_version=int(z['shape_version']))


class ProductionBackend:
    def __init__(self, runtime):
        import torch
        from omegaconf import OmegaConf
        from superflex.superflex import SuperFlex
        for name in ('checkpoint', 'config'):
            if sha(runtime[name]) != runtime[name + '_sha256']:
                raise ValueError('Trusted SuperFlex runtime hash mismatch')
        if not torch.cuda.is_available():
            raise RuntimeError('Assigned CUDA GPU required for SuperFlex')
        torch.manual_seed(runtime['seed'])
        self.torch, self.runtime = torch, runtime
        self.provenance = dict(checkpoint_sha256=runtime['checkpoint_sha256'],
                               config_sha256=runtime['config_sha256'], seed=runtime['seed'],
                               torch_version=torch.__version__)
        self.model = SuperFlex(OmegaConf.load(runtime['config']).superflex).cuda().eval()
        self.model.load_state_dict(torch.load(runtime['checkpoint'], map_location='cpu',
            weights_only=False)['model_state_dict'], strict=True)

    def __call__(self, data, folder):
        from superflex.data.dataloader import denormalize_outdict, denormalize_points
        from superflex.utils.predictions_handler import PredictionHandler
        from shape_tools.comparison import load_features
        torch = self.torch
        # Exactly the FPS array; conversion to float32 is the only input change.
        x = torch.from_numpy(data['normalized']).float().unsqueeze(0).cuda()
        with torch.inference_mode():
            result = self.model(x)
        if any(isinstance(v, torch.Tensor) and not torch.isfinite(v).all() for v in result.values()):
            raise ValueError('Nonfinite SuperFlex output')
        result = {k: v.cpu() if isinstance(v, torch.Tensor) else v for k, v in result.items()}
        centers, scales = np.array([data['center']]), np.array([data['scale']])
        result = denormalize_outdict(result, centers, scales, False)
        restored = denormalize_points(x.cpu(), centers, scales, False)
        handler = PredictionHandler.from_outdict(result, restored, ['accumulated_shape'])
        if int((handler.exist > .5).sum()) == 0:
            raise ValueError('No active primitives at authors threshold .5')
        mesh = handler.get_mesh(0, resolution=30)
        if not len(mesh.vertices) or not len(mesh.faces) or not np.isfinite(mesh.vertices).all():
            raise ValueError('Invalid reconstruction mesh')
        mesh.export(folder / 'reconstruction.ply')
        handler.save_npz(str(folder / 'prediction.npz'))
        return load_features(folder / 'reconstruction.ply')


def process(input_path, expected_hash, output, *, backend, test_backend=False):
    # Validate before creating outputs; previous results are never overwritten.
    data = load_input(input_path, expected_hash)
    folder = Path(output)
    folder.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    result = dict(schema='point3-fps-reconstruction-v1', input_sha256=expected_hash,
                  shape_version=data['shape_version'], backend='test-double' if test_backend else 'superflex',
                  sampling='deterministic_fps_4096', random_input_resampling=False,
                  worker_sha256=sha(__file__), runtime_provenance=getattr(backend, 'provenance', None))
    try:
        from shape_tools.metrics import descriptors
        p, d2, spectrum = backend(data, folder)
        if p.shape != (1024, 3) or not np.isfinite(p).all():
            raise ValueError('Expected finite 1024-point reconstruction descriptor surface')
        if not all(np.array_equal(a, b) for a, b in zip((d2, spectrum), descriptors(p))):
            raise ValueError('Inconsistent reconstruction descriptors')
        np.savez_compressed(folder / 'features.npz', points=p, d2=d2, spectrum=spectrum,
                            completed_by_superflex=not test_backend)
        result.update(status='ready', features=dict(path='features.npz', sha256=sha(folder / 'features.npz')))
        if (folder / 'reconstruction.ply').exists():
            result['mesh'] = dict(path='reconstruction.ply', sha256=sha(folder / 'reconstruction.ply'))
    except Exception as error:
        result.update(status='failed', error=f'{type(error).__name__}: {error}')
    result['seconds'] = time.perf_counter() - started
    (folder / 'result.json').write_text(json.dumps(result, indent=2, allow_nan=False))
    return result


def run(export_path, runtime_path, limit=None):
    root, config_path = Path(export_path).resolve(), Path(runtime_path).resolve()
    config = json.loads(config_path.read_text())
    runtime = dict(config.get('superflex', config))
    for name in ('checkpoint', 'config'):
        runtime[name] = str((config_path.parent / runtime[name]).resolve())
    backend = ProductionBackend(runtime)
    versions = json.loads((root / 'versions.json').read_text())
    query_file = root / 'query_requests.json'
    if query_file.exists():
        versions += json.loads(query_file.read_text())
    results, processed = [], 0
    for version in versions:
        name = Path(version['superflex_input']['path']).stem
        out = root / 'reconstructions' / name
        if (out / 'result.json').exists():
            results.append(json.loads((out / 'result.json').read_text()))
            continue
        if limit is not None and processed >= limit:
            break
        path = (root / version['superflex_input']['path']).resolve()
        if not path.is_relative_to(root):
            raise ValueError('Input path outside export')
        result = process(path, version['superflex_input']['sha256'], out, backend=backend)
        result['version_file'] = name
        results.append(result)
        processed += 1
        print(json.dumps(result), flush=True)
    report = dict(processed_now=processed, ready=sum(r['status'] == 'ready' for r in results),
                  failed=sum(r['status'] == 'failed' for r in results),
                  runtime_sha256=sha(config_path), total_shape_versions=len(versions))
    (root / 'reconstruction_summary.json').write_text(json.dumps(report, indent=2))
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--export', required=True)
    p.add_argument('--runtime', required=True)
    p.add_argument('--limit', type=int)
    a = p.parse_args()
    print(json.dumps(run(a.export, a.runtime, a.limit), indent=2))
