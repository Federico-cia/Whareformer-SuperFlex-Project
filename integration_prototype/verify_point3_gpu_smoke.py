"""Verify downloaded GPU smoke against the local bound input package."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from shape_tools.metrics import descriptors


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify(package, results):
    package, results = Path(package), Path(results)
    requests = json.loads((package / 'versions.json').read_text()) + json.loads((package / 'query_requests.json').read_text())
    verified, failed, missing = 0, 0, 0
    for request in requests:
        folder = results / 'reconstructions' / Path(request['superflex_input']['path']).stem
        path = folder / 'result.json'
        if not path.exists():
            missing += 1; continue
        result = json.loads(path.read_text())
        assert result['input_sha256'] == request['superflex_input']['sha256']
        assert result['shape_version'] == request['shape_version']
        assert result['worker_sha256'] == sha(package / 'code' / 'scene_superflex_worker.py')
        assert result['backend'] == 'superflex' and result['random_input_resampling'] is False
        if result['status'] != 'ready':
            failed += 1; continue
        provenance = result['runtime_provenance']
        assert provenance['checkpoint_sha256'] == '5bd1ba9818dc7322400d4234262d47500b05fb40bad3b0edc1e6b8847833b842'
        assert provenance['config_sha256'] == 'ff468f8baaec1622db6cd26edae26ec32c7c8c828b95a0012811078f51b031bf'
        feature = folder / result['features']['path']
        assert sha(feature) == result['features']['sha256']
        with np.load(feature, allow_pickle=False) as z:
            assert bool(z['completed_by_superflex']) and z['points'].shape == (1024, 3)
            assert all(np.isfinite(z[k]).all() for k in ('points', 'd2', 'spectrum'))
            assert all(np.array_equal(a, b) for a, b in zip((z['d2'], z['spectrum']), descriptors(z['points'])))
        assert sha(folder / result['mesh']['path']) == result['mesh']['sha256']
        verified += 1
    report = dict(requests=len(requests), ready_verified=verified, failed=failed, missing=missing,
                  real_neural_execution_verified=verified > 0, full_smoke_passed=verified == len(requests))
    (results / 'local_verification.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--package', required=True)
    p.add_argument('--results', required=True)
    a = p.parse_args()
    verify(a.package, a.results)
