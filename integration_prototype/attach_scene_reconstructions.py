"""Attach actual completed shapes to causal examples; preserve failed/missing cases."""
import argparse
import hashlib
import json
from pathlib import Path


def attach(export, *, allow_test=False):
    root = Path(export).resolve()
    versions = json.loads((root / 'versions.json').read_text())
    examples = json.loads((root / 'examples.json').read_text())
    ready, failed, missing = {}, 0, 0
    for version in versions:
        key = (version['track_id'], version['shape_version'])
        folder = root / 'reconstructions' / Path(version['superflex_input']['path']).stem
        result_path = folder / 'result.json'
        if not result_path.exists():
            missing += 1
            continue
        r = json.loads(result_path.read_text())
        if (r['input_sha256'] != version['superflex_input']['sha256']
                or r['shape_version'] != version['shape_version']):
            raise ValueError('Reconstruction belongs to another shape')
        if r['backend'] != 'superflex' and not (allow_test and r['backend'] == 'test-double'):
            raise ValueError('Test reconstruction cannot enter production training export')
        if r['status'] != 'ready':
            failed += 1
            continue
        spec = r['features']
        path = (folder / spec['path']).resolve()
        if not path.is_relative_to(root) or hashlib.sha256(path.read_bytes()).hexdigest() != spec['sha256']:
            raise ValueError('Reconstruction feature binding mismatch')
        ready[key] = dict(path=path.relative_to(root).as_posix(), sha256=spec['sha256'],
            backend=r['backend'], shape_version=version['shape_version'],
            last_update_frame=version['last_update_frame'], track_id=version['track_id'])
    attached = 0
    queries = {}
    query_file = root / 'query_requests.json'
    if query_file.exists():
        for request in json.loads(query_file.read_text()):
            folder = root / 'reconstructions' / Path(request['superflex_input']['path']).stem
            result_path = folder / 'result.json'
            if not result_path.exists():
                continue
            result = json.loads(result_path.read_text())
            if result['input_sha256'] != request['superflex_input']['sha256'] or result['shape_version'] != 0:
                raise ValueError('Query reconstruction binding mismatch')
            if result['backend'] != 'superflex' and not (allow_test and result['backend'] == 'test-double'):
                raise ValueError('Unapproved query backend')
            if result['status'] != 'ready':
                continue
            path = (folder / result['features']['path']).resolve()
            if not path.is_relative_to(root) or hashlib.sha256(path.read_bytes()).hexdigest() != result['features']['sha256']:
                raise ValueError('Query features checksum mismatch')
            queries[request['observation_key']] = dict(path=path.relative_to(root).as_posix(),
                sha256=result['features']['sha256'], backend=result['backend'])
    for row in examples:
        row['query_reconstruction'] = queries.get(row['observation_key'])
        for candidate in row['candidates']:
            memory = candidate['memory']
            candidate['reconstruction'] = None
            if memory is None:
                continue
            # A failed later reconstruction retains the most recent past success.
            available = [r for (tid, version), r in ready.items() if tid == memory['track_id']
                         and version <= memory['shape_version'] and r['last_update_frame'] < row['frame_index']]
            if available:
                candidate['reconstruction'] = max(available, key=lambda r: r['shape_version'])
                attached += 1
    out = root / 'examples_with_reconstructions.json'
    with out.open('x', encoding='utf-8') as f:
        json.dump(examples, f, indent=2, allow_nan=False)
    report = dict(ready_versions=len(ready), failed_versions=failed, missing_versions=missing,
                  query_reconstructions_attached=len(queries),
                  candidate_reconstructions_attached=attached, test_results_allowed=allow_test,
                  note='Observed and completed representations remain separate; missing results stay explicit.')
    (root / 'attachment_summary.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report))
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('export')
    attach(p.parse_args().export)
