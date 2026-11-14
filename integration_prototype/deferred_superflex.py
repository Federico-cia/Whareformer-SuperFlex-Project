"""Content-bound deferred SuperFlex requests and serial replay results.

The production worker reuses shape_tools.pipeline.superflex, including inverse
normalization and authors' primitive threshold. No completion enters raw memory.
"""
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path

import numpy as np

from cloud_updater import CloudState, cloud_hash
from shape_tools import geometry, metrics, comparison, pipeline


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def save(path, value):
    # Manifest is published last. No replacement of an existing request/result.
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def bound_file(root, info):
    root = Path(root).resolve()
    path = (root / info['path']).resolve()
    if not path.is_relative_to(root) or comparison.file_hash(path) != info['sha256']:
        raise ValueError('Artifact path/hash mismatch')
    return path


def code_hashes():
    hashes = {m.__name__: comparison.file_hash(m.__file__) for m in (geometry, metrics, comparison, pipeline)}
    hashes['deferred_superflex'] = comparison.file_hash(__file__)
    return hashes


@dataclass(frozen=True)
class SuperflexConfig:
    checkpoint_sha256: str = '5bd1ba9818dc7322400d4234262d47500b05fb40bad3b0edc1e6b8847833b842'
    config_sha256: str = 'ff468f8baaec1622db6cd26edae26ec32c7c8c828b95a0012811078f51b031bf'
    seed: int = 42

    def __post_init__(self):
        if type(self.seed) is not int or not 0 <= self.seed < 2**32:
            raise ValueError('Invalid seed')
        for h in (self.checkpoint_sha256, self.config_sha256):
            if len(h) != 64 or any(c not in '0123456789abcdef' for c in h):
                raise ValueError('SHA-256 required')


class DeferredSuperflex:
    def __init__(self, root, config=SuperflexConfig(), allow_test_results=False):
        self.root, self.config = Path(root), config
        self.allow_test_results = allow_test_results

    def prepare(self, frame, versions):
        requests = []
        for tid, version in versions.items():
            state = version['value']
            if not isinstance(state, CloudState) or version['frame_index'] != frame:
                raise ValueError('A cloud accepted in this frame is required')
            meta = state.summary()
            if version['version'] != meta['version'] or tid != meta['track_id']:
                raise ValueError('Cloud version/track mismatch')
            spec = dict(video=meta['video'], track_id=tid, source=meta['source'],
                        frame_index=frame, cloud_version=meta['version'], cloud_sha256=meta['cloud_sha256'],
                        cloud_provenance=meta, superflex=asdict(self.config), code=code_hashes())
            rid = digest(spec)
            folder = self.root / rid
            if not folder.exists():
                folder.mkdir(parents=True)
                p = state.memory.cloud()
                normalized, center, scale, indices = geometry.prepare_superflex_input(p, seed=self.config.seed)
                np.savez_compressed(folder/'input.npz', object_points=p, normalized_points=normalized,
                                    translation=center, scale=scale, sample_indices=indices)
                save(folder/'request.json', dict(request_id=rid, spec=spec,
                     input=dict(path='input.npz', sha256=comparison.file_hash(folder/'input.npz'))))
            request = json.loads((folder/'request.json').read_text(encoding='utf-8'))
            if request['request_id'] != rid or request['spec'] != spec:
                raise ValueError('Cached request mismatch')
            bound_file(folder, request['input'])
            requests.append(rid)
        return requests

    def collect(self, requests, frame, versions):
        ready, events = {}, []
        for rid in requests:
            folder = self.root/rid
            req = validate_request(folder)
            spec = req['spec']
            old = versions[spec['track_id']]
            current = old['value'].summary()
            if (spec['frame_index'] != frame or old['version'] != spec['cloud_version']
                    or old['frame_index'] != frame or current != spec['cloud_provenance']
                    or spec['superflex'] != asdict(self.config)):
                raise ValueError('Result is stale or belongs to another cloud/frame/configuration')
            result = json.loads((folder/'result.json').read_text(encoding='utf-8'))
            if result['request_id'] != rid or result['request_sha256'] != comparison.file_hash(folder/'request.json'):
                raise ValueError('Result/request mismatch')
            if result['backend'] not in ('superflex', 'test-double') or result['backend']=='test-double' and not self.allow_test_results:
                raise ValueError('Unapproved result backend')
            if result['status'] == 'failed':
                events.append(dict(request_id=rid, status='failed', error=result['error']))
                continue
            if result['status'] != 'ready':
                raise ValueError('Invalid result status')
            with np.load(bound_file(folder, result['features']), allow_pickle=False) as z:
                points, d2, spectrum = z['points'].copy(), z['d2'].copy(), z['spectrum'].copy()
            geometry.validate_points(points)
            expected = metrics.descriptors(points)
            if points.shape != (1024,3) or not all(np.array_equal(a,b) for a,b in zip((d2,spectrum),expected)):
                raise ValueError('Inconsistent reconstruction descriptors')
            ready[spec['track_id']] = (rid, (points, d2, spectrum))
            events.append(dict(request_id=rid, status='ready', cloud_version=spec['cloud_version']))
        return ready, events


def validate_request(folder):
    folder = Path(folder)
    req = json.loads((folder/'request.json').read_text(encoding='utf-8'))
    if req['request_id'] != digest(req['spec']) or req['spec']['code'] != code_hashes():
        raise ValueError('Request identity/code mismatch')
    with np.load(bound_file(folder,req['input']),allow_pickle=False) as z:
        p = z['object_points'].copy()
        if cloud_hash(p) != req['spec']['cloud_sha256']:
            raise ValueError('Observed cloud hash mismatch')
        normalized, center, scale, indices = geometry.prepare_superflex_input(p, seed=req['spec']['superflex']['seed'])
        for name, value in [('normalized_points',normalized),('translation',center),('scale',scale),('sample_indices',indices)]:
            if not np.array_equal(z[name], value):
                raise ValueError('Normalization/inverse metadata mismatch')
    return req


def process_request(folder, runtime=None, test_backend=None):
    """Run one request; test_backend(req, folder) returns a controlled feature tuple.

    Real execution requires existing trusted checkpoint/config paths; imports
    Torch and SuperFlex only inside the existing pipeline. Test output is tagged.
    """
    folder = Path(folder)
    req = validate_request(folder)
    if (folder/'result.json').exists():
        raise FileExistsError('Preserve previous result')
    record = dict(request_id=req['request_id'], request_sha256=comparison.file_hash(folder/'request.json'),
                  backend='test-double' if test_backend is not None else 'superflex')
    try:
        if test_backend is not None:
            features = test_backend(req, folder)
        else:
            cfg = dict(runtime)
            for name in ('seed','checkpoint_sha256','config_sha256'):
                if cfg[name] != req['spec']['superflex'][name]:
                    raise ValueError('Worker configuration mismatch')
            stage = folder/'production'
            stage.mkdir(exist_ok=False)
            with np.load(bound_file(folder,req['input']),allow_pickle=False) as z:
                np.savez_compressed(stage/'cloud.npz', camera_points=z['object_points'])
            source = req['spec']['source']
            row = dict(observation_key=req['request_id']);key=pipeline.item_id(row)
            save(stage/f'clouds_{source}_index.json', {key:dict(status='ready',artifacts=dict(points=dict(path='cloud.npz',sha256=comparison.file_hash(stage/'cloud.npz'))))})
            pipeline.superflex(dict(observations=[row]),stage,dict(sources=[source],superflex=cfg))
            info = json.loads((stage/f'superflex_{source}_index.json').read_text())[key]
            if info['status'] != 'ready':
                raise RuntimeError(info.get('error','SuperFlex failed'))
            features = comparison.load_features(bound_file(stage,info['artifacts']['surface']))
            record['production'] = info
            record['production_backend'] = json.loads((stage/'superflex_backend.json').read_text())
        p,d2,spectrum=features
        geometry.validate_points(p)
        if p.shape != (1024,3) or not all(np.array_equal(a,b) for a,b in zip((d2,spectrum),metrics.descriptors(p))):
            raise ValueError('Invalid feature output')
        np.savez_compressed(folder/'features.npz',points=p,d2=d2,spectrum=spectrum)
        record.update(status='ready',features=dict(path='features.npz',sha256=comparison.file_hash(folder/'features.npz')))
    except Exception as error:
        record.update(status='failed',error=f'{type(error).__name__}: {error}')
    save(folder/'result.json',record)
    return record


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request',type=Path,required=True)
    parser.add_argument('--config',type=Path,required=True,help='Existing pipeline JSON with superflex runtime configuration')
    args=parser.parse_args()
    runtime=json.loads(args.config.read_text())['superflex']
    for name in ('checkpoint','config'):
        runtime[name]=str((args.config.resolve().parent/Path(runtime[name])).resolve())
    result=process_request(args.request,runtime)
    print(json.dumps(result,indent=2))
    if result['status']!='ready':raise SystemExit(1)
