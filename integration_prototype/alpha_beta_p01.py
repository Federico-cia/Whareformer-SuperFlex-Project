"""Alpha/beta DA->scena per frame dei blocchi P01_01, stessa procedura dell'audit 783586.

Per ogni frame: profondita DA densa del blocco, profondita della mesh renderizzata con la
posa EPIC-Fields (PyrenderScene degli autori), sfondo statico = fuori dall'unione delle
maschere di tutti gli oggetti del frame, minimi quadrati depth_scene ~ alpha*depth_DA + beta.
Le funzioni dell'audit (maschere, simboli Whareformer) sono importate, non riscritte.
Sola lettura dei blocchi; scrive solo nella cartella di output. Nessuna nuvola salvata:
le nuvole allineate a piena risoluzione si ricostruiscono in locale dalle grezze.
Uso: --block N (blocco geometry/N) oppure --check M (riproduce alpha/beta dell'audit
sulle prime M osservazioni del campione con maschere complete e confronta).
"""
import argparse, json, math, sys, time
from pathlib import Path
import numpy as np


def fit(depth, scene_depth, union):
    static = (~union) & (scene_depth > 1e-6)
    n = int(static.sum())
    if n < 32:
        return None, None, n
    A = np.stack([depth[static], np.ones(n)], -1)
    alpha, beta = (float(v) for v in np.linalg.lstsq(A, scene_depth[static], rcond=None)[0])
    return alpha, beta, n


class Renderer:
    def __init__(self, ns, mesh):
        self.ns, self.mesh, self.scene, self.params = ns, mesh, None, None

    def depth(self, intr, shape, c2w):
        H, W = shape
        params = [W, H] + [float(v) for v in intr]
        if params != self.params:
            self.scene = self.ns['PyrenderScene'](str(self.mesh), params, 1.0)
            self.params = params
        return self.scene.get_scene_depth(c2w)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--task-root', type=Path, required=True)
    ap.add_argument('--audit-dir', type=Path, required=True)   # contiene audit_ammissione.py, mesh.ply, files.sha256, out_783586
    ap.add_argument('--mesh-sha256', required=True)
    ap.add_argument('--wsrc', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--block', type=int)
    g.add_argument('--check', type=int)
    ap.add_argument('--dataset', type=Path)                    # solo per --check
    a = ap.parse_args()
    sys.path.insert(0, str(a.audit_dir))
    from audit_ammissione import symbols, load_masks_by_frame, read_mask, sha
    mesh = a.audit_dir / 'mesh.ply'
    if sha(mesh) != a.mesh_sha256:
        raise SystemExit('mesh hash mismatch')
    a.out.mkdir(parents=True, exist_ok=True)
    name = f'block_{a.block:04d}' if a.block is not None else 'check_audit'
    target = a.out / f'{name}.jsonl'
    if target.exists():
        raise SystemExit(f'STOP: {target} gia presente, nessuna sovrascrittura')
    import pyrender, trimesh
    ns = dict(np=np, pyrender=pyrender, trimesh=trimesh)
    utils = a.wsrc / 'feature_extraction/utils'
    symbols(utils / 'epic_utils.py', ['qvec2rotmat', 'colmap_pose_to_c2w'], ns)
    symbols(utils / 'models.py', ['PyrenderScene'], ns)
    render = Renderer(ns, mesh)
    masks = load_masks_by_frame(a.task_root / 'batches', a.task_root)
    started, records = time.time(), []

    def union_for(rgbname, shape, fallback=()):
        paths = masks.get(rgbname)
        source = 'all_objects' if paths else 'catalogue_only'
        paths = paths or set(fallback)
        u = np.zeros(shape, bool)
        for p in paths:
            u |= read_mask(p, shape)
        return u, source, len(paths)

    if a.block is not None:
        rows = json.loads((a.task_root / 'batches' / f'{a.block:04d}.json').read_text())['observations']
        frames = {}
        for r in rows:
            frames.setdefault(r['rgb_sha256'], r)
        geometry = a.task_root / 'geometry' / f'{a.block:04d}'
        for i, (key, r) in enumerate(sorted(frames.items(), key=lambda kv: kv[1]['frame_index'])):
            rec = dict(block=a.block, frame_index=r['frame_index'], rgb_sha256=key, rgb=r.get('rgb'),
                       intrinsics=r['intrinsics'], expected_frame_objects=r.get('expected_frame_objects'))
            try:
                pred = geometry / 'da' / key[:24] / 'prediction.npz'
                if not pred.exists():
                    rec['status'] = 'dense_map_missing'
                    records.append(rec); continue
                with np.load(pred, allow_pickle=False) as z:
                    depth = z['depth'].astype(float)
                pose = np.asarray(r['camera_pose'], float)
                c2w = ns['colmap_pose_to_c2w'](pose[:4], pose[4:], 1.0)
                union, source, nmask = union_for(Path(r['rgb']).name, depth.shape)
                alpha, beta, n = fit(depth, render.depth(r['intrinsics'], depth.shape, c2w), union)
                valid = alpha is not None and alpha > 0 and math.isfinite(alpha) and math.isfinite(beta)
                rec.update(status='ok', alpha=alpha, beta=beta, static_pixels=n, align_valid=bool(valid),
                           mask_source=source, masks_in_union=nmask, depth_shape=list(depth.shape),
                           c2w=np.asarray(c2w).tolist(), prediction_sha256=sha(pred))
            except Exception as e:
                rec.update(status='failed', error=repr(e)[:300])
            records.append(rec)
            if i % 20 == 0:
                print(json.dumps(dict(block=a.block, frame=i, of=len(frames), s=round(time.time() - started))), flush=True)
    else:
        cat = json.loads((a.dataset / 'geometry_catalogue.json').read_text())
        groot, iroot, obs = Path(cat['geometry_root']), Path(cat['inputs_root']), cat['observations']
        audit = {}
        for line in (a.audit_dir / 'out_783586' / 'per_observation.jsonl').read_text().splitlines():
            r = json.loads(line); audit[r['key']] = r
        keys = [k for k in sorted(obs, key=lambda k: (obs[k]['source_observation']['frame_index'], k))
                if audit.get(k, {}).get('mask_source') == 'all_objects' and audit[k].get('alpha') is not None][:a.check]
        for k in keys:
            so = obs[k]['source_observation']
            pose = np.asarray(so['camera_pose'], float)
            c2w = ns['colmap_pose_to_c2w'](pose[:4], pose[4:], 1.0)
            with np.load(groot / 'da' / so['rgb_sha256'][:24] / 'prediction.npz', allow_pickle=False) as z:
                depth = z['depth'].astype(float)
            union, source, nmask = union_for(Path(so['rgb']).name, depth.shape)
            alpha, beta, n = fit(depth, render.depth(so['intrinsics'], depth.shape, c2w), union)
            records.append(dict(key=k, alpha=alpha, beta=beta, static_pixels=n,
                                audit_alpha=audit[k]['alpha'], audit_beta=audit[k]['beta'],
                                audit_static_pixels=audit[k]['static_pixels'],
                                abs_diff_alpha=abs(alpha - audit[k]['alpha']), abs_diff_beta=abs(beta - audit[k]['beta'])))
    with open(target, 'w') as f:
        for r in records:
            f.write(json.dumps(r) + '\n')
    counts = {}
    for r in records:
        s = r.get('status', 'check'); counts[s] = counts.get(s, 0) + 1
    summary = dict(name=name, records=len(records), statuses=counts, seconds=round(time.time() - started, 1),
                   align_valid=sum(bool(r.get('align_valid')) for r in records))
    if a.check is not None and records:
        summary.update(max_abs_diff_alpha=max(r['abs_diff_alpha'] for r in records),
                       max_abs_diff_beta=max(r['abs_diff_beta'] for r in records),
                       static_pixels_equal=all(r['static_pixels'] == r['audit_static_pixels'] for r in records))
    (a.out / f'{name}_summary.json').write_text(json.dumps(summary, indent=2))
    print('FINE', json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
