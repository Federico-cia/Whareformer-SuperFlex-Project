"""Final audit of completed migration plus real CLI/reader roundtrip; no inference."""
import argparse
from collections import Counter
import importlib.metadata
import os
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
import geometry_retention as retention
from regenerate_geometry_block import restore


def validate(task):
    from shape_tools import pipeline
    from shape_tools.comparison import load_features
    task = Path(task).resolve()
    tools = task/'retention_tools'
    migration = retention.read(tools/'migration_completed.json')
    assert migration['status'] == 'completed'
    originals = Counter()
    payloads = Counter()
    counts = Counter()
    new_allocated = 0
    for number in migration['blocks']:
        root = task/'geometry'/f'{number:04d}'
        ledger = retention.read(root/retention.LEDGER)
        assert ledger['state'] == 'compacted'
        assert retention.read(root/'run.json')['code'] == pipeline.source_hashes()
        archive = retention.checked(root, ledger['assignment_archive'])
        new_allocated += archive.stat().st_blocks*512 + (root/retention.LEDGER).stat().st_blocks*512
        unique = {}
        for entry in ledger['entries'].values():
            assert not (root/entry['path']).exists(), entry['path']
            originals[entry['kind']] += entry['original_allocated_bytes']
            counts[entry['kind']] += 1
            for kind, info in [('clouds',entry['cloud']),('parameters',entry['parameters'])]:
                unique[info['path']] = (kind, info)
        for kind, info in unique.values(): payloads[kind] += (root/info['path']).stat().st_blocks*512
        for source in ('da','moge'):
            unique_maps = {i['artifacts']['prediction']['path']:i['artifacts']['prediction'] for i in retention.read(root/(source+'_index.json')).values() if i['status']=='ready'}
            for path in unique_maps: payloads['dense_'+source] += (root/path).stat().st_blocks*512
            index = retention.read(root/('superflex_'+source+'_index.json'))
            key = next(k for k,v in index.items() if v['status']=='ready')
            retention.checked(root,index[key]['artifacts']['parameters'])
            cloud = retention.read(root/('clouds_'+source+'_index.json'))[key]['artifacts']['points']
            retention.checked(root,cloud)
        print('AUDITED_BLOCK', number, len(ledger['entries']), flush=True)
    root = task/'geometry/0004'
    destination = tools/'verified_regeneration_smoke'
    result = restore(root, destination, kind='all', source='da', limit=3)
    assert len(result['files']) == 3
    surface = next(x for x in result['files'] if x['original_path'].endswith('reconstruction.ply'))
    info = dict(path=surface['original_path'],sha256=surface['sha256'])
    a = retention.retained_features(root,info)
    b = load_features(surface['path'])
    for first,second in zip(a,b): np.testing.assert_array_equal(first,second)
    # Only our verified smoke payloads are removed; the receipt remains as evidence.
    for item in result['files']:
        path = Path(item['path']).resolve()
        assert path.is_relative_to(destination) and retention.sha(path)==item['sha256']
        path.unlink()
    result['test_payloads_removed_after_verification'] = True
    retention.save(destination/root.name/'regeneration_receipt.json',result)
    # Exercise the actual future CLI path, not just a mock of the cache.
    subprocess.run([sys.executable,'-u',str(tools/'retained_pipeline.py'),'export',
                    '--manifest',str(task/'batches/0004.json'),'--config',str(task/'inputs/config.json'),
                    '--output',str(root)],check=True)
    retention.install_cache_adapter(pipeline,root)
    resumed = 0
    for source in ('da','moge'):
        index = retention.read(root/('superflex_'+source+'_index.json'))
        for key in list(index)[:2]:
            assert pipeline.cached(root/('superflex_'+source)/key,index[key]['signature'])['status']=='ready'
            resumed += 1
    environment = dict(python=sys.version,packages={})
    for name in ('numpy','trimesh','torch','torch-geometric','plyfile','scipy','pandas'):
        try: environment['packages'][name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError: environment['packages'][name] = None
    receipt = dict(status='passed',blocks=migration['blocks'],absent_files=dict(counts),
                   gross_removed_allocated_bytes=dict(originals),new_archive_and_ledger_allocated_bytes=new_allocated,
                   retained_payload_allocated_bytes=dict(payloads),smoke=result,descriptors_identical=True,
                   export_cli_passed=True,resumed_records=resumed,environment=environment,created_unix=time.time())
    retention.save(tools/'final_verification.json',receipt)
    print('FINAL_VERIFICATION_PASSED',sum(counts.values()),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--task',type=Path,required=True)
    validate(p.parse_args().task)
