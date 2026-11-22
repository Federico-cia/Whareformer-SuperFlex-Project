"""Migrate completed numbered blocks only, after a real destructive roundtrip pilot."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
import geometry_retention as retention


def pilot(task):
    from shape_tools import pipeline
    from shape_tools.comparison import load_features
    root = task / 'geometry/0004'
    proof = task / 'retention_tools/cpu_regeneration_verified.json'
    result = retention.compact(root, proof, apply=True, limit=2)
    ledger = retention.read(root / retention.LEDGER)
    recovered = []
    descriptors_match = False
    for kind in ('input', 'surface', 'diagnostic_prediction'):
        entry = next(e for e in ledger['entries'].values() if e['kind'] == kind)
        if kind == 'surface': expected = retention.retained_features(root, entry)
        path = retention.regenerate(root, entry['path'])
        if retention.sha(path) != entry['sha256']: raise ValueError('Roundtrip hash mismatch')
        if kind == 'surface':
            actual = load_features(path)
            for a, b in zip(expected, actual): np.testing.assert_array_equal(a, b)
            descriptors_match = True
        recovered.append(dict(path=entry['path'], sha256=entry['sha256'], byte_identical=True))
    retention.compact(root, proof, apply=True, limit=2)
    retention.install_cache_adapter(pipeline, root)
    resumed = 0
    for source in ('da', 'moge'):
        index = retention.read(root / ('superflex_' + source + '_index.json'))
        for key in sorted(index)[:2]:
            pipeline.cached(root / ('superflex_'+source) / key, index[key]['signature'])
            resumed += 1
    assert resumed == 4 and descriptors_match
    receipt = dict(status='passed', first_compaction=result, restored=recovered,
                   descriptor_arrays_identical=descriptors_match, resumed_records=resumed)
    retention.save(task/'retention_tools/pilot_roundtrip.json', receipt)
    print('PILOT_PASSED', flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--task', type=Path, required=True)
    p.add_argument('--workers', type=int, default=2)
    a = p.parse_args()
    task = a.task.resolve()
    pilot(task)
    blocks = sorted(int(p.stem) for p in (task/'completed').glob('*.json'))
    if not blocks: raise ValueError('No completed blocks')
    logs = task/'retention_tools/migration_logs'
    logs.mkdir(exist_ok=True)
    def process(index):
        root = task/'geometry'/f'{index:04d}'
        with (logs/f'{index:04d}.out').open('wb') as out:
            subprocess.run([sys.executable, '-u', str(Path(__file__).with_name('geometry_retention.py')),
                            'compact', '--root', str(root), '--receipt', str(task/'retention_tools/cpu_regeneration_verified.json'), '--apply'],
                           stdout=out, stderr=subprocess.STDOUT, check=True, env=os.environ.copy())
        print('BLOCK_COMPACTED', index, flush=True)
        return retention.read(root/'retention_result.json')
    with ThreadPoolExecutor(max_workers=a.workers) as executor:
        results = list(executor.map(process, blocks))
    receipt = dict(status='completed', blocks=blocks, results=results,
                   policy='lossless CPU regeneration; original assignments sharded; clouds and dense maps retained')
    retention.save(task/'retention_tools/migration_completed.json', receipt)
    print('MIGRATION_COMPLETED', len(blocks), flush=True)


if __name__ == '__main__': main()
