"""Audit di fattibilità del punto 3 (solo lettura degli input esistenti, nessun training).

Domande: (1) quanto varia la scala di DA grezzo rispetto alla scena e se l'allineamento di
Whareformer la rende coerente fra viste; (2) quante coppie consecutive della stessa identità
hanno un riferimento di posa plausibile dalle camere; (3) cosa restituisce oggi il registratore
rispetto a quel riferimento. Le soglie del registratore non sono usate come etichette.
Convenzioni: punti come righe; camera X destra, Y giù, Z avanti (COLMAP); c2w da Whareformer.
"""
import argparse, ast, csv, glob, hashlib, json, math, os, sys
from pathlib import Path
import numpy as np

SEED = 20261121
SAMPLE = 2048
OVERLAP_TOL = 0.10   # tolleranza DESCRITTIVA (frazione del raggio medio), non una regola di ammissione


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def symbols(path, names, ns):
    tree = ast.parse(Path(path).read_text())
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    assert {n.name for n in nodes} == set(names), (path, names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), ns)


def nn(a, b):
    """Distanza di ogni punto di a dal più vicino di b."""
    try:
        from scipy.spatial import cKDTree
        return cKDTree(b).query(a)[0]
    except ImportError:
        out = np.empty(len(a))
        for i in range(0, len(a), 512):
            d = ((a[i:i+512, None, :] - b[None]) ** 2).sum(-1)
            out[i:i+512] = np.sqrt(d.min(1))
        return out


def radius(p):
    return float(np.sqrt(((p - p.mean(0)) ** 2).sum(1).mean()))


def sample(p, n, seed):
    if len(p) <= n:
        return p
    return p[np.random.default_rng(seed).choice(len(p), n, replace=False)]


def backproject(z, pix, intr):
    fx, fy, cx, cy = intr
    u, v = pix[:, 0].astype(float), pix[:, 1].astype(float)
    return np.stack([(u - cx) / fx * z, (v - cy) / fy * z, z], -1)


def to_world(p_cam, c2w):
    return p_cam @ c2w[:3, :3].T + c2w[:3, 3]


def reference_relative(c2w_a, c2w_b):
    """Trasformazione (riga) che porta camera b su camera a se l'oggetto è fermo: p_a = p_b @ R + t."""
    Ra, ta, Rb, tb = c2w_a[:3, :3], c2w_a[:3, 3], c2w_b[:3, :3], c2w_b[:3, 3]
    return Rb.T @ Ra, (tb - ta) @ Ra


def angle_deg(R1, R2):
    return float(np.degrees(np.arccos(np.clip((np.trace(R1.T @ R2) - 1) / 2, -1, 1))))


def overlap_stats(a, b, scale):
    da, db = nn(a, b) / scale, nn(b, a) / scale
    return dict(frac_a_in_b=float((da < OVERLAP_TOL).mean()), frac_b_in_a=float((db < OVERLAP_TOL).mean()),
                median_nn_a=float(np.median(da)), median_nn_b=float(np.median(db)))


def load_masks_by_frame(batches_dir, task_root):
    by = {}
    for f in sorted(glob.glob(str(Path(batches_dir) / '*.json'))):
        data = json.loads(Path(f).read_text())
        for row in data.get('observations', []):
            rgb, mask = row.get('rgb'), row.get('mask')
            if not rgb or not mask:
                continue
            m = Path(mask)
            if not m.is_absolute():
                for base in (Path(task_root), Path(task_root) / 'inputs'):
                    if (base / m).exists():
                        m = base / m
                        break
            by.setdefault(Path(rgb).name, set()).add(str(m))
    return by


def read_mask(path, shape):
    import cv2
    m = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if m is None:
        raise FileNotFoundError(path)
    if m.ndim == 3:
        m = m[..., 0]
    if m.shape != shape:
        m = cv2.resize((m > 0).astype(np.uint8), (shape[1], shape[0]), interpolation=cv2.INTER_NEAREST)
    return m > 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dataset', type=Path, required=True)       # training_enrichment .../dataset
    ap.add_argument('--batches', type=Path, required=True)       # p01_full_enrichment .../batches
    ap.add_argument('--task-root', type=Path, required=True)     # p01_full_enrichment root
    ap.add_argument('--mesh', type=Path, required=True)
    ap.add_argument('--mesh-sha256', required=True)
    ap.add_argument('--wsrc', type=Path, required=True)          # Whareformer original_src
    ap.add_argument('--registrator', type=Path)                  # dir with cloud_memory.py (optional)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--limit', type=int, default=0)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=False)
    log = open(a.out / 'log.txt', 'w')
    def say(*x):
        s = ' '.join(str(v) for v in x); print(s, flush=True); log.write(s + '\n'); log.flush()

    assert sha(a.mesh) == a.mesh_sha256, 'mesh hash mismatch'
    import pyrender, trimesh
    ns = dict(np=np, pyrender=pyrender, trimesh=trimesh)
    utils = a.wsrc / 'feature_extraction/utils'
    symbols(utils / 'epic_utils.py', ['qvec2rotmat', 'colmap_pose_to_c2w', 'align_metric_and_scene_depth'], ns)
    symbols(utils / 'models.py', ['PyrenderScene'], ns)
    reg = None
    if a.registrator:
        try:
            sys.path.insert(0, str(a.registrator)); from cloud_memory import register_rigid as reg
        except Exception as e:
            say('REGISTRATORE NON DISPONIBILE:', repr(e))

    cat = json.loads((a.dataset / 'geometry_catalogue.json').read_text())
    groot = Path(cat['geometry_root']); iroot = Path(cat['inputs_root'])
    obs = cat['observations']
    samples = json.loads((a.dataset / 'samples.json').read_text())
    z = np.load(a.dataset / 'training_inputs.npz')
    xyz = {s['observation_key']: z[s['numerical_input_key']][0, 256:259].astype(float) for s in samples}
    ident = {s['observation_key']: (s['benchmark_identity'], s['oracle_track_id']) for s in samples}
    masks = load_masks_by_frame(a.batches, a.task_root)
    say('osservazioni catalogo', len(obs), 'frame con maschere complete', len(masks))

    keys = sorted(obs, key=lambda k: (obs[k]['source_observation']['frame_index'], k))
    if a.limit:
        keys = keys[:a.limit]
    scene = None; scene_cache = {}; rows = {}; clouds = {}
    for n, k in enumerate(keys):
        so = obs[k]['source_observation']; g = obs[k]['geometry']
        r = dict(key=k, frame=so['frame_index'], identity=ident.get(k, (None, None))[0], track=ident.get(k, (None, None))[1])
        try:
            intr = [float(v) for v in so['intrinsics']]
            pose = np.asarray(so['camera_pose'], float)
            c2w = ns['colmap_pose_to_c2w'](pose[:4], pose[4:], 1.0)
            pred = groot / 'da' / so['rgb_sha256'][:24] / 'prediction.npz'
            with np.load(pred, allow_pickle=False) as p:
                depth = p['depth'].astype(float)
            H, W = depth.shape
            if scene is None:
                scene = ns['PyrenderScene'](str(a.mesh), [W, H] + intr, 1.0)
            rgbname = Path(so['rgb']).name
            if rgbname not in scene_cache:
                scene_cache.clear(); scene_cache[rgbname] = scene.get_scene_depth(c2w)
            sdepth = scene_cache[rgbname]
            mpaths = masks.get(rgbname)
            r['mask_source'] = 'all_objects' if mpaths else 'catalogue_only'
            if not mpaths:
                mpaths = {str(iroot / obs[o]['source_observation']['mask']) for o in obs
                          if Path(obs[o]['source_observation']['rgb']).name == rgbname}
            union = np.zeros((H, W), bool)
            for mp in mpaths:
                union |= read_mask(mp, (H, W))
            static = (~union) & (sdepth > 1e-6)
            r['static_pixels'] = int(static.sum())
            alpha = beta = None
            if static.sum() >= 32:
                A = np.stack([depth[static], np.ones(static.sum())], -1)
                alpha, beta = (float(v) for v in np.linalg.lstsq(A, sdepth[static], rcond=None)[0])
            r['alpha'], r['beta'] = alpha, beta
            r['align_valid'] = bool(alpha is not None and alpha > 0 and math.isfinite(alpha) and math.isfinite(beta))
            rep = g['representations']['da_points']
            cpath = groot / rep['path']
            assert sha(cpath) == rep['sha256'], 'cloud hash mismatch'
            with np.load(cpath, allow_pickle=False) as c:
                cam_raw = c['camera_points'].astype(float); pix = c['pixels_xy']
            r['depth_cloud_maxdiff'] = float(np.abs(cam_raw[:, 2] - depth[pix[:, 1], pix[:, 0]]).max())
            idx = np.random.default_rng(SEED + n).choice(len(cam_raw), min(SAMPLE, len(cam_raw)), replace=False)
            cam_raw, pix = cam_raw[idx], pix[idx]
            out = dict(cam_raw=cam_raw, w_raw=to_world(cam_raw, c2w))
            if r['align_valid']:
                cam_al = backproject(alpha * cam_raw[:, 2] + beta, pix, intr)
                if (cam_al[:, 2] > 0).all():
                    out.update(cam_al=cam_al, w_al=to_world(cam_al, c2w))
                else:
                    r['align_valid'] = False; r['align_note'] = 'non-positive aligned depth'
            for s in ('raw', 'al'):
                if 'w_' + s in out:
                    r['radius_' + s] = radius(out['w_' + s]); r['centroid_' + s] = out['w_' + s].mean(0).tolist()
            r['c2w'] = c2w.tolist(); r['xyz_official'] = xyz[k].tolist() if k in xyz else None
            r['status'] = 'ok'; clouds[k] = out
        except Exception as e:
            r['status'] = 'failed'; r['error'] = repr(e)[:300]
        rows[k] = r
        if n % 25 == 0:
            say('osservazione', n, k, r['status'], r.get('alpha'))
    with open(a.out / 'per_observation.jsonl', 'w') as f:
        for k in keys:
            f.write(json.dumps(rows[k]) + '\n')

    # coppie consecutive della stessa identità oracle
    by_id = {}
    for k in keys:
        if rows[k]['status'] == 'ok' and rows[k]['identity'] is not None:
            by_id.setdefault((rows[k]['identity'], rows[k]['track']), []).append(k)
    pairs = []
    for (name, tr), ks in by_id.items():
        ks.sort(key=lambda k: rows[k]['frame'])
        for ka, kb in zip(ks, ks[1:]):
            ra, rb = rows[ka], rows[kb]; ca, cb = clouds[ka], clouds[kb]
            p = dict(identity=name, track=tr, key_a=ka, key_b=kb, frame_a=ra['frame'], frame_b=rb['frame'],
                     gap_frames=rb['frame'] - ra['frame'])
            if ra.get('xyz_official') and rb.get('xyz_official'):
                p['xyz_disp'] = float(np.linalg.norm(np.subtract(rb['xyz_official'], ra['xyz_official'])))
            for s in ('raw', 'al'):
                if 'w_' + s in ca and 'w_' + s in cb:
                    R = (rows[ka]['radius_' + s] + rows[kb]['radius_' + s]) / 2
                    p[f'{s}_radius_mean'] = R
                    p[f'{s}_radius_ratio'] = rows[kb]['radius_' + s] / rows[ka]['radius_' + s]
                    p[f'{s}_centroid_dist_R'] = float(np.linalg.norm(cb['w_' + s].mean(0) - ca['w_' + s].mean(0)) / R)
                    for kk, v in overlap_stats(ca['w_' + s], cb['w_' + s], R).items():
                        p[f'{s}_{kk}'] = v
            if 'xyz_disp' in p and 'al_radius_mean' in p:
                p['xyz_disp_R'] = p['xyz_disp'] / p['al_radius_mean']
            if reg is not None:
                Rr, tr_ = reference_relative(np.array(ra['c2w']), np.array(rb['c2w']))
                for s in ('raw', 'al'):
                    if 'cam_' + s in ca and 'cam_' + s in cb:
                        try:
                            res = reg(cb['cam_' + s], ca['cam_' + s])
                            Re, te = np.array(res['rotation']), np.array(res['translation'])
                            b = cb['cam_' + s]; scale = radius(ca['cam_' + s])
                            p[f'reg_{s}_surface_err_R'] = float(np.linalg.norm((b @ Re + te) - (b @ Rr + tr_), axis=1).mean() / scale)
                            p[f'reg_{s}_rot_err_deg'] = angle_deg(Re, Rr)
                            p[f'reg_{s}_accepted'] = bool(res['accepted']); p[f'reg_{s}_reasons'] = '|'.join(res['reasons'])
                            p[f'reg_{s}_n_alternatives'] = len(res['ambiguous_alternatives'])
                            # posa di riferimento valutata con le stesse misure di supporto (descrittivo)
                            moved = b @ Rr + tr_
                            for kk, v in overlap_stats(moved, ca['cam_' + s], scale).items():
                                p[f'ref_{s}_{kk}'] = v
                        except Exception as e:
                            p[f'reg_{s}_error'] = repr(e)[:200]
            pairs.append(p)
    cols = sorted({c for p in pairs for c in p})
    with open(a.out / 'pairs.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); [w.writerow(p) for p in pairs]

    # riepilogo descrittivo
    ok = [rows[k] for k in keys if rows[k]['status'] == 'ok']
    al = [r for r in ok if r['align_valid']]
    alphas = np.array([r['alpha'] for r in al]) if al else np.array([])
    def q(v): v = np.asarray([x for x in v if x is not None and np.isfinite(x)]); return None if not len(v) else {k: float(x) for k, x in zip(['q10', 'q25', 'q50', 'q75', 'q90'], np.quantile(v, [.1, .25, .5, .75, .9]))} | {'n': int(len(v))}
    size_cv = {}
    for s in ('raw', 'al'):
        cvs = []
        for ks in by_id.values():
            v = [rows[k].get('radius_' + s) for k in ks if rows[k].get('radius_' + s)]
            if len(v) >= 3:
                cvs.append(float(np.std(v) / np.mean(v)))
        size_cv[s] = q(cvs)
    summary = dict(
        observations=len(keys), ok=len(ok), failed=len(keys) - len(ok),
        mask_source={m: sum(1 for r in ok if r.get('mask_source') == m) for m in ('all_objects', 'catalogue_only')},
        align_valid=len(al), alpha=q(alphas), alpha_cv=float(alphas.std() / alphas.mean()) if len(alphas) else None,
        depth_cloud_maxdiff=q([r.get('depth_cloud_maxdiff') for r in ok]),
        size_cv_per_identity=size_cv, pairs=len(pairs),
        xyz_disp_R=q([p.get('xyz_disp_R') for p in pairs]),
        overlap_tolerance_descriptive=OVERLAP_TOL,
    )
    for s in ('raw', 'al'):
        summary[f'{s}_radius_ratio'] = q([p.get(f'{s}_radius_ratio') for p in pairs])
        summary[f'{s}_overlap_min'] = q([min(p[f'{s}_frac_a_in_b'], p[f'{s}_frac_b_in_a']) for p in pairs if f'{s}_frac_a_in_b' in p])
        summary[f'reg_{s}_surface_err_R'] = q([p.get(f'reg_{s}_surface_err_R') for p in pairs])
        summary[f'reg_{s}_accepted'] = sum(1 for p in pairs if p.get(f'reg_{s}_accepted'))
    # stratificazione per spostamento ufficiale (terzili, nessuna soglia fissata)
    vals = [p['xyz_disp_R'] for p in pairs if 'xyz_disp_R' in p]
    if len(vals) >= 9:
        cuts = np.quantile(vals, [1/3, 2/3]); strata = {}
        for i, (lo, hi) in enumerate([(-np.inf, cuts[0]), (cuts[0], cuts[1]), (cuts[1], np.inf)]):
            sel = [p for p in pairs if 'xyz_disp_R' in p and lo < p['xyz_disp_R'] <= hi]
            strata[f'terzile_{i+1}'] = dict(range=[float(lo), float(hi)], n=len(sel),
                al_overlap_min=q([min(p['al_frac_a_in_b'], p['al_frac_b_in_a']) for p in sel if 'al_frac_a_in_b' in p]),
                raw_overlap_min=q([min(p['raw_frac_a_in_b'], p['raw_frac_b_in_a']) for p in sel if 'raw_frac_a_in_b' in p]),
                reg_al_surface_err_R=q([p.get('reg_al_surface_err_R') for p in sel]),
                reg_al_accepted=sum(1 for p in sel if p.get('reg_al_accepted')))
        summary['strata_by_official_displacement'] = strata
    (a.out / 'summary.json').write_text(json.dumps(summary, indent=2))
    np.savez_compressed(a.out / 'world_clouds_aligned.npz', **{k.replace('/', '__'): clouds[k]['w_al'] for k in clouds if 'w_al' in clouds[k]})
    say('FINE', json.dumps(dict(ok=len(ok), align_valid=len(al), pairs=len(pairs))))


if __name__ == '__main__':
    main()
