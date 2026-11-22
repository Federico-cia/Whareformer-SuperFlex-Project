"""Restore selected derived files from one compact block into a separate directory.

No GPU. Exact original SHA required for every output; authoritative data are read-only.
The assignment shard is verified/loaded once when restoring many diagnostics.
"""
import argparse
import hashlib
from pathlib import Path
import time

import geometry_retention as retention


def restore(root, destination, kind='surface', source=None, limit=None):
    root, destination = Path(root).resolve(), Path(destination).resolve()
    if destination == root or destination.is_relative_to(root):
        raise ValueError('Use a destination outside the authoritative geometry block')
    with retention.locked(root):
        ledger = retention.read(root / retention.LEDGER)
        if ledger['provenance'] != retention.recipe_provenance(root): raise ValueError('Pinned regeneration environment changed')
        entries = [e for _, e in sorted(ledger['entries'].items())
                   if (kind == 'all' or e['kind'] == kind) and (source is None or e['source'] == source)]
        if limit is not None: entries = entries[:limit]
        shards, results = {}, []
        started = time.perf_counter()
        for entry in entries:
            file_started = time.perf_counter()
            output = retention.bound(destination / root.name, entry['path'])
            if output.exists():
                if retention.sha(output) != entry['sha256']: raise ValueError('Refuse overwrite: ' + str(output))
            else:
                working = dict(entry)
                if entry['kind'] == 'diagnostic_prediction':
                    info = entry['assignment_archive']
                    identity = (info['path'], info['sha256'])
                    if identity not in shards: shards[identity] = retention.arrays(retention.checked(root, info))
                    working['_assignment_array'] = shards[identity][entry['assignment_key']]
                data = retention.cpu_bytes(root, working)
                if hashlib.sha256(data).hexdigest() != entry['sha256']: raise ValueError('Regeneration checksum mismatch')
                output.parent.mkdir(parents=True, exist_ok=True)
                temporary = output.with_name(output.name + '.regenerating')
                temporary.write_bytes(data)
                temporary.replace(output)
            results.append(dict(original_path=entry['path'], path=str(output), sha256=entry['sha256'], bytes=output.stat().st_size,
                                elapsed_seconds=time.perf_counter()-file_started))
            print('REGENERATED', entry['path'], flush=True)
        result = dict(status='passed', root=str(root), files=results, elapsed_seconds=time.perf_counter()-started, byte_identical=True)
        retention.save(destination / root.name / 'regeneration_receipt.json', result)
        return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--destination', type=Path, required=True)
    p.add_argument('--kind', choices=['surface', 'input', 'diagnostic_prediction', 'all'], default='surface')
    p.add_argument('--source', choices=['da', 'moge'])
    p.add_argument('--limit', type=int)
    a = p.parse_args()
    result = restore(a.root, a.destination, a.kind, a.source, a.limit)
    print('RESTORED_FILES', len(result['files']), 'SECONDS', round(result['elapsed_seconds'], 3), flush=True)


if __name__ == '__main__': main()
