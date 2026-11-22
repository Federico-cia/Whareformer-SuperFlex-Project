"""Nuvole DA allineate alla scena a PIENA risoluzione, da nuvole grezze + alpha/beta per frame.

Stessa trasformazione dell'audit 783586 (profondità alpha*z+beta, retroproiezione con gli
intrinseci, c2w EPIC-Fields), senza sottocampionamento. Alpha/beta: audit per il campione,
job 786174 per i blocchi. Legge l'archivio ricevuto in streaming e verifica l'hash di ogni
nuvola grezza contro l'indice. Crea una cartella nuova; non sovrascrive.
Uso: python build_aligned_fullres.py --archive geometry_received.tar.gz --index geometry_index.json
       --audit per_observation.jsonl --alpha-beta-dir out/ --out NUOVA_CARTELLA
"""
import argparse, hashlib, io, json, tarfile, time
from pathlib import Path
import numpy as np


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for k in ('archive', 'index', 'audit', 'alpha_beta_dir', 'out'):
        ap.add_argument('--' + k.replace('_', '-'), type=Path, required=True)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=False)
    index = json.loads(a.index.read_text())['observations']
    audit = {r['key']: r for r in map(json.loads, a.audit.read_text().splitlines())}
    frames = {}
    for f in sorted(a.alpha_beta_dir.glob('block_*.jsonl')):
        for r in map(json.loads, f.read_text().splitlines()):
            if r.get('status') == 'ok' and r.get('align_valid'):
                frames[r['rgb_sha256']] = r
    wanted, skipped = {}, {}
    for o in index:
        key, so = o['observation_key'], o['source_observation']
        art = o['artifacts']['points']
        if key in audit:
            r = audit[key]
            if not r.get('align_valid') or r.get('alpha') is None:
                skipped[key] = 'audit_alignment_invalid'; continue
            ab = dict(alpha=r['alpha'], beta=r['beta'], c2w=r['c2w'], source='audit_783586',
                      mask_source=r.get('mask_source'))
        elif so['rgb_sha256'] in frames:
            r = frames[so['rgb_sha256']]
            ab = dict(alpha=r['alpha'], beta=r['beta'], c2w=r['c2w'], source=f"job_786174_block_{r['block']:04d}",
                      mask_source=r.get('mask_source'))
        else:
            skipped[key] = 'no_alpha_beta_for_frame'; continue
        wanted[art['path']] = (key, so, art['sha256'], ab)
    print(json.dumps(dict(index=len(index), wanted=len(wanted), skipped=len(skipped))), flush=True)
    clouds, rows, started = {}, [], time.time()
    with tarfile.open(a.archive, 'r|gz') as tar:
        for member in tar:
            if member.name not in wanted:
                continue
            key, so, digest, ab = wanted.pop(member.name)
            data = tar.extractfile(member).read()
            row = dict(key=key, frame=so['frame_index'], identity=so['category'], annotation_id=so['annotation_id'],
                       detection_idx=so.get('detection_idx'), intrinsics=so['intrinsics'], raw_points_sha256=digest,
                       alpha=ab['alpha'], beta=ab['beta'], c2w=ab['c2w'], alpha_beta_source=ab['source'],
                       mask_source=ab['mask_source'])
            if hashlib.sha256(data).hexdigest() != digest:
                row.update(status='failed', error='raw cloud hash mismatch'); rows.append(row); continue
            with np.load(io.BytesIO(data), allow_pickle=False) as z:
                cam, pix = z['camera_points'].astype(float), z['pixels_xy']
            fx, fy, cx, cy = so['intrinsics']
            d = ab['alpha'] * cam[:, 2] + ab['beta']
            if not np.isfinite(d).all() or (d <= 0).any():
                row.update(status='failed', error='non-positive aligned depth'); rows.append(row); continue
            p = np.stack([(pix[:, 0] - cx) / fx * d, (pix[:, 1] - cy) / fy * d, d], -1)
            c2w = np.asarray(ab['c2w'], float)
            w = p @ c2w[:3, :3].T + c2w[:3, 3]
            clouds[key.replace('/', '__')] = w.astype(np.float32)
            row.update(status='ok', align_valid=True, points=int(len(w)),
                       radius_al=float(np.sqrt(((w - w.mean(0)) ** 2).sum(1).mean())))
            rows.append(row)
            if len(rows) % 500 == 0:
                print(json.dumps(dict(done=len(rows), s=round(time.time() - started))), flush=True)
    for path, (key, *_rest) in wanted.items():
        rows.append(dict(key=key, status='failed', error='raw cloud not found in archive'))
    rows.sort(key=lambda r: (r.get('frame', -1), r['key']))
    np.savez_compressed(a.out / 'world_clouds_aligned_fullres.npz', **clouds)
    with open(a.out / 'per_observation.jsonl', 'w') as f:
        for r in rows:
            f.write(json.dumps(r) + '\n')
    summary = dict(observations=len(rows), ok=sum(r['status'] == 'ok' for r in rows),
                   failed=sum(r['status'] == 'failed' for r in rows), skipped=len(skipped),
                   skipped_reasons={k: sum(v == k for v in skipped.values()) for k in set(skipped.values())},
                   total_points=int(sum(r.get('points', 0) for r in rows)),
                   identities=len({r.get('identity') for r in rows if r['status'] == 'ok'}),
                   frames=len({r.get('frame') for r in rows if r['status'] == 'ok'}),
                   inputs={str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (a.index, a.audit)},
                   archive=str(a.archive), dtype='float32 world coordinates (EPIC-Fields units, not certified metres)',
                   seconds=round(time.time() - started, 1))
    (a.out / 'summary.json').write_text(json.dumps(summary, indent=2))
    print('FINE', json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
