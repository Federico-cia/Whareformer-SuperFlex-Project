"""Causal FPS reconstruction bridge for the multi-hypothesis coordinator."""
import hashlib
import json
from pathlib import Path
import numpy as np
from multi_hypothesis_memory import MultiHypothesisMemory
from scene_superflex_worker import process, sha, ProductionBackend


def identity(spec):
    return hashlib.sha256(json.dumps(spec, sort_keys=True, allow_nan=False).encode()).hexdigest()


class DeferredSceneSuperflex:
    reconstruction_contract = 'scene-fps-v1'

    def __init__(self, root, *, allow_test_results=False):
        self.root = Path(root)
        self.allow_test_results = allow_test_results
        self.prepared_versions = {}

    def prepare(self, frame, versions):
        requests = []
        for tid, version in versions.items():
            memory = version['value']
            if (not isinstance(memory, MultiHypothesisMemory) or str(tid) != memory.track_id
                    or version['version'] != memory.version or version['frame_index'] != frame):
                raise ValueError('Multi-hypothesis version/frame mismatch')
            if memory.shape_version == 0 or self.prepared_versions.get(tid) == memory.shape_version:
                continue
            spec = dict(video=memory.video, track_id=tid, frame=frame,
                        geometry_version=memory.version, shape_version=memory.shape_version,
                        cloud_sha256=memory.snapshot()['cloud_sha256'],
                        policy=memory.policy, worker_sha256=sha(Path(__file__).with_name('scene_superflex_worker.py')))
            rid = identity(spec); folder = self.root / rid
            if not folder.exists():
                folder.mkdir(parents=True)
                memory.export_superflex(folder / 'input.npz')
                request = dict(request_id=rid, spec=spec, input=dict(path='input.npz', sha256=sha(folder / 'input.npz')))
                (folder / 'request.json').write_text(json.dumps(request, indent=2))
            request = validate_request(folder)
            if request['spec'] != spec:
                raise ValueError('Existing request belongs to another memory')
            self.prepared_versions[tid] = memory.shape_version
            requests.append(rid)
        return requests

    def collect(self, requests, frame, versions):
        from shape_tools.metrics import descriptors
        ready, events = {}, []
        for rid in requests:
            folder = self.root / rid
            request = validate_request(folder); spec = request['spec']
            v = versions[spec['track_id']]; memory = v['value']
            if (v['frame_index'] != frame or frame != spec['frame'] or v['version'] != spec['geometry_version']
                    or memory.video != spec['video'] or memory.shape_version != spec['shape_version']
                    or memory.snapshot()['cloud_sha256'] != spec['cloud_sha256']):
                raise ValueError('Stale reconstruction result')
            result = json.loads((folder / 'worker' / 'result.json').read_text())
            if (result['input_sha256'] != request['input']['sha256']
                    or result['shape_version'] != spec['shape_version'] or result['worker_sha256'] != spec['worker_sha256']):
                raise ValueError('Result/input/code mismatch')
            if result['backend'] != 'superflex' and not (self.allow_test_results and result['backend'] == 'test-double'):
                raise ValueError('Test-double reconstruction forbidden')
            if result['status'] == 'failed':
                events.append(dict(request_id=rid,status='failed',error=result['error']));continue
            if result['status'] != 'ready':
                raise ValueError('Invalid reconstruction status')
            path = (folder / 'worker' / result['features']['path']).resolve()
            if not path.is_relative_to((folder / 'worker').resolve()) or sha(path) != result['features']['sha256']:
                raise ValueError('Reconstruction feature path/hash mismatch')
            with np.load(path,allow_pickle=False) as z:
                points,d2,spectrum=(z[k].copy() for k in ('points','d2','spectrum'))
            if points.shape != (1024,3) or not np.isfinite(points).all() or not all(
                    np.array_equal(a,b) for a,b in zip((d2,spectrum),descriptors(points))):
                raise ValueError('Reconstruction feature mismatch')
            ready[spec['track_id']] = (rid,(points,d2,spectrum))
            events.append(dict(request_id=rid,status='ready',shape_version=spec['shape_version']))
        return ready,events


def validate_request(folder):
    folder = Path(folder).resolve()
    r = json.loads((folder / 'request.json').read_text())
    p = (folder / r['input']['path']).resolve()
    if r['request_id'] != identity(r['spec']) or not p.is_relative_to(folder) or sha(p) != r['input']['sha256']:
        raise ValueError('Request identity/path/hash mismatch')
    if sha(Path(__file__).with_name('scene_superflex_worker.py')) != r['spec']['worker_sha256']:
        raise ValueError('Worker changed after request generation')
    return r


def process_request(folder, runtime=None, test_backend=None):
    folder=Path(folder);r=validate_request(folder)
    backend=ProductionBackend(runtime) if test_backend is None else test_backend
    return process(folder/r['input']['path'],r['input']['sha256'],folder/'worker',
                   backend=backend,test_backend=test_backend is not None)


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--request',required=True);p.add_argument('--runtime',required=True)
    a=p.parse_args();cfgpath=Path(a.runtime).resolve();cfg=json.loads(cfgpath.read_text())
    cfg=dict(cfg.get('superflex',cfg))
    for k in ('checkpoint','config'):cfg[k]=str((cfgpath.parent/cfg[k]).resolve())
    result=process_request(a.request,cfg)
    print(json.dumps(result,indent=2))
    if result['status']!='ready':raise SystemExit(1)
