"""DA raw -> scene-aligned observed points; failures never fall back to raw.

Affine least squares on static background, as in Whareformer and the project
audit. Guards (32 pixels, positive slope/depth) are operational, not calibrated.
Scene coordinates are EPIC-Fields units; physical metric accuracy is unverified.
"""
import argparse
from pathlib import Path
import numpy as np
from full_video_enrichment import read, save, sha, settings


def fit_alignment(depth, scene_depth, static):
    valid=static & np.isfinite(depth) & np.isfinite(scene_depth) & (scene_depth>1e-6)
    if valid.sum()<32: raise ValueError('Fewer than 32 static pixels')
    A=np.stack([depth[valid],np.ones(int(valid.sum()))],-1)
    ab,_,rank,_=np.linalg.lstsq(A,scene_depth[valid],rcond=None)
    alpha,beta=map(float,ab)
    if rank<2 or not np.isfinite(ab).all() or alpha<=0: raise ValueError('Invalid affine fit')
    return alpha,beta,int(valid.sum())


def main():
    p=argparse.ArgumentParser(); p.add_argument('--settings',type=Path,required=True)
    p.add_argument('--index',type=int,required=True); a=p.parse_args(); s=settings(a.settings)
    import pyrender, trimesh
    from scene_original import PyrenderScene, colmap_pose_to_c2w
    from PIL import Image
    from shape_tools.pipeline import item_id, digest, artifact
    task=Path(s['task']); raw=task/'geometry'/f'{a.index:04d}'; out=task/'aligned'/f'{a.index:04d}'
    out.mkdir(parents=True,exist_ok=True)
    if (out/'clouds_da_index.json').exists():
        for report in read(out/'clouds_da_index.json').values():
            for asset in report.get('artifacts',{}).values():
                if sha(out/asset['path'])!=asset['sha256']: raise ValueError('Corrupt aligned cache')
        return
    rows=read(read(task/'batches.json')[a.index])['observations']
    allrows=read(task/'inputs/manifest.json')['observations']
    by_rgb={}
    for r in allrows: by_rgb.setdefault(r['rgb_sha256'],[]).append(r)
    upstream=read(raw/'clouds_da_index.json'); indices={}; cache={}; render=None; camera=None
    scene_hash=sha(s['mesh'])
    for row in rows:
        key=item_id(row); info=upstream[key]; folder=out/'clouds_da'/key; folder.mkdir(parents=True,exist_ok=True)
        report=dict(status='failed',artifacts={},error='Alignment not attempted')
        try:
            if info['status']!='ready': raise ValueError('Raw DA cloud unavailable')
            rgbkey=row['rgb_sha256']; intr=np.asarray(row['intrinsics'],float)
            pose=np.asarray(row['camera_pose'],float)
            c2w=colmap_pose_to_c2w(pose[:4],pose[4:],1.0)
            if rgbkey not in cache:
                cache.clear()
                with np.load(raw/'da'/rgbkey[:24]/'prediction.npz',allow_pickle=False) as z: depth=z['depth'].astype(float)
                H,W=depth.shape
                params=[W,H]+intr.tolist()
                if camera!=params:
                    if render is not None: render.renderer.delete()
                    render=PyrenderScene(s['mesh'],params,1.0); camera=params
                scene_depth=render.get_scene_depth(c2w)
                union=np.zeros((H,W),bool)
                for r in by_rgb[rgbkey]:
                    mask=np.asarray(Image.open(r['mask']))>0
                    if mask.shape!=union.shape: raise ValueError('Static mask shape mismatch')
                    union |= mask
                for r in by_rgb[rgbkey]:
                    count=sum(x['frame_index']==r['frame_index'] for x in by_rgb[rgbkey])
                    if count!=r['expected_frame_objects']:
                        raise ValueError('Incomplete object masks for static background')
                alpha,beta,n=fit_alignment(depth,scene_depth,~union)
                cache[rgbkey]=(alpha,beta,n)
            alpha,beta,n=cache[rgbkey]
            asset=info['artifacts']['points']; src=raw/asset['path']
            if sha(src)!=asset['sha256']: raise ValueError('Raw cloud hash mismatch')
            with np.load(src,allow_pickle=False) as z: payload={k:z[k].copy() for k in z.files}
            pix=payload['pixels_xy']; z=alpha*payload['camera_points'][:,2]+beta
            if not np.isfinite(z).all() or (z<=0).any(): raise ValueError('Non-positive/nonfinite aligned object depth')
            fx,fy,cx,cy=intr
            points=np.stack([(pix[:,0]-cx)/fx*z,(pix[:,1]-cy)/fy*z,z],-1)
            payload['camera_points']=points
            # Preserve all observed pixels and colors; no subsampling or fusion.
            np.savez_compressed(folder/'points.npz',**payload)
            np.savez_compressed(folder/'world_points.npz',world_points=points@c2w[:3,:3].T+c2w[:3,3],
                                camera_to_world=c2w,pixels_xy=pix)
            report=dict(status='ready',artifacts={'points':artifact(out,folder/'points.npz'),
                        'world_points':artifact(out,folder/'world_points.npz')},alpha=alpha,beta=beta,
                        static_pixels=n,camera_to_world=c2w.tolist(),mesh_sha256=scene_hash,
                        units='EPIC-Fields scene units; physical metric accuracy unverified')
        except (ValueError,RuntimeError,OSError) as e:
            report.update(error=str(e),error_type=type(e).__name__)
        report['signature']=digest(dict(upstream=info,mesh=scene_hash,report=report,code=sha(__file__)))
        save(folder/'report.json',report); indices[key]=report
    if render is not None: render.renderer.delete()
    save(out/'clouds_da_index.json',indices)


if __name__=='__main__': main()
