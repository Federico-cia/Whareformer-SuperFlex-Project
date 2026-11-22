"""Portable inputs for learning a geometric correction of frozen Whareformer.

Oracle targets and histories are supervision, never inputs at deployment.
The available geometry index need not cover the whole video.
"""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import sys
import types


def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()
def save(p,obj):
    Path(p).write_text(json.dumps(obj,indent=2,allow_nan=False),encoding='utf-8')
def bounded(root,path):
    root=Path(root).resolve(); p=(root/path).resolve()
    if not p.is_relative_to(root): raise ValueError('Path outside dataset')
    return p


def verify_geometry(root, expected=8126):
    import numpy as np
    root=Path(root); data=read(root/'geometry_index.json'); rows=data['observations']
    if data['video']!='P01_01' or len(rows)!=expected: raise ValueError('Unexpected geometry video/count')
    seen=set(); counts=Counter()
    for row in rows:
        key=row['observation_key']; source=row['source_observation']
        if key in seen or source['observation_key']!=key: raise ValueError('Duplicate/unlinked geometry')
        seen.add(key)
        for asset in row['artifacts'].values():
            if sha(bounded(root,asset['path']))!=asset['sha256']: raise ValueError('Geometry checksum: '+key)
        for field in ('rgb','mask'):
            if sha(bounded(root,source[field]))!=source[field+'_sha256']: raise ValueError('RGB/mask checksum: '+key)
        with np.load(root/row['artifacts']['points']['path'],allow_pickle=False) as z:
            points=z['camera_points']; pixels=z['pixels_xy']; colors=z['colors']
            if points.ndim!=2 or points.shape[1]!=3 or not np.isfinite(points).all() or len(points)<4:
                raise ValueError('Invalid observed cloud')
            if pixels.shape!=(len(points),2) or colors.shape!=(len(points),3): raise ValueError('Invalid pixels/colors')
        counts['observations']+=1
    counts['unique_frames']=len({r['source_observation']['frame_index'] for r in rows})
    return dict(status='passed',**counts)


def load_original(root):
    root=Path(root).resolve(); sys.path.insert(0,str(root/'original_src'))
    # Avoid unrelated video loading imports, as in the verified enrichment builder.
    for name in ('tracking','utils'):
        package=types.ModuleType(name);package.__path__=[str(root/'original_src'/name)]
        sys.modules[name]=package
    from tracking.tracker.tracker import StandardTracker
    from tracking.tracker.detection import Detection
    from utils.manifest_builder import build_feature_manifest_entry
    return StandardTracker,Detection,build_feature_manifest_entry


class Transaction:
    def __init__(self): self.values={}
    def put(self,key,value):
        if key in self.values and self.values[key]!=value: raise ValueError('Feature hash collision')
        self.values[key]=value


def build(root, geometry, output, *, limit_frames=0):
    import numpy as np
    import torch
    root=Path(root).resolve(); geometry=Path(geometry).resolve(); output=Path(output)
    if output.exists(): raise FileExistsError('Preserve existing examples; choose fresh output')
    selected={r['observation_key']:r for r in read(geometry/'geometry_index.json')['observations']}
    frames=read(root/'baseline/frames.json'); cfg=read(root/'baseline/effective_config.json')
    fps=read(root/'baseline/baseline_receipt.json')['fps']
    with np.load(root/'baseline/features.npz',allow_pickle=False) as z: app=z['app'].copy();loc=z['loc'].copy()
    StandardTracker,Detection,manifest_builder=load_original(root)
    params=copy.deepcopy(cfg['tracking']);params.update(matcher_type='oracle',device_id=None,app_dim=256)
    params['matcher_params'].pop('model_path',None)
    tracker=StandardTracker(params,fps);torch.set_num_threads(2)
    histories={}; samples=[]; arrays={}; offset=0; visited=set(); labels=Counter()
    output.mkdir(parents=True)
    for processed,f in enumerate(frames,1):
        if limit_frames and processed>limit_frames: break
        frame=f['frame_index']; anns=f['annotations']
        if f['offset']!=offset or len({a['name'] for a in anns})!=len(anns): raise ValueError('Ambiguous frame/offset')
        ids=[int(t.track_id) for t in tracker.tracks];names=[t.initial_object for t in tracker.tracks]
        ends=[len(histories.get(str(t),[])) for t in ids]
        detections=[Detection(dict(frame=frame,detection_idx=i,obj_name=a['name'],bbox=a['bounding_box'],
                       app=app[offset+i],loc=loc[offset+i])) for i,a in enumerate(anns)]
        training=tracker.update(detections,dict(frame_name=f['frame'],frame_idx=frame,timestamp=frame/fps))
        assignments={int(t.history[-1]['detection_idx']):int(t.track_id) for t in tracker.tracks if t.time_since_update==0}
        if len(assignments)!=len(anns): raise ValueError('Oracle coverage mismatch')
        keys=[f'P01_01/{f["frame"]}__d{i}' for i in range(len(anns))]
        manifests=None; txn=Transaction()
        if any(k in selected for k in keys) and training is not None:
            manifests=manifest_builder(training[1],training[2],training[0],'P01_01',frame,txn,{})
        staged=[]
        for i,(key,ann) in enumerate(zip(keys,anns)):
            if key not in selected: continue
            source=selected[key]['source_observation']
            if (source['annotation_id'],source['category'],list(source['bbox']))!=(ann['id'],ann['name'],ann['bounding_box']):
                raise ValueError('Geometry/official annotation mismatch: '+key)
            target=names.index(ann['name'])+1 if ann['name'] in names else 0
            if target and ids[target-1]!=assignments[i]: raise ValueError('Oracle target disagreement')
            if manifests is None:
                if ids: raise ValueError('Missing original training matrix')
                x=np.concatenate([app[offset+i],loc[offset+i]])[None,:].astype(np.float32)
                y=np.ones(1,dtype=np.int8)
            else:
                m=manifests[i]
                def value(k): return np.frombuffer(txn.values[k.encode()],dtype=np.float32)
                det=np.concatenate([value(m['det_app_key']),value(m['det_loc_key'])])[None,:]
                tracks=np.stack([np.concatenate([value(a),value(l)]) for a,l in zip(m['track_app_keys'],m['track_loc_keys'])])
                x=np.concatenate([det,tracks]);y=m['label']
                da,dl,ta,tl=training[0]
                direct=np.concatenate([np.concatenate([da[i],dl[i]])[None,:],np.concatenate([ta[i],tl[i]],axis=-1)])
                if not np.array_equal(x,direct): raise ValueError('Original input matrix disagreement')
            if x.shape!=(len(ids)+1,259) or int(y.sum())!=1 or int(y.argmax())!=target: raise ValueError('Training contract mismatch')
            array_key=f'sample_{len(samples):06d}';arrays[array_key]=x;arrays[array_key+'_label']=y
            samples.append(dict(observation_key=key,frame_index=frame,detection_idx=i,annotation_id=ann['id'],
                benchmark_identity=ann['name'],oracle_track_id=assignments[i],target_class=target,
                candidate_track_ids=ids,candidate_names=names,candidate_history_ends=ends,
                numerical_input_key=array_key,numerical_label_key=array_key+'_label'))
            labels['new_track' if target==0 else 'existing_track']+=1;visited.add(key);staged.append((assignments[i],key))
        # All detections of this frame saw exactly the same previous geometry.
        for tid,key in staged: histories.setdefault(str(tid),[]).append(dict(observation_key=key,frame_index=frame))
        offset+=len(anns)
        if processed%2500==0: print(json.dumps(dict(frames=processed,samples=len(samples))),flush=True)
    if not limit_frames and (visited!=set(selected) or offset!=len(app) or offset!=len(loc)):
        raise ValueError('Not all selected geometries joined to the full history')
    np.savez_compressed(output/'training_inputs.npz',**arrays)
    save(output/'samples.json',samples);save(output/'geometry_history.json',histories)
    save(output/'summary.json',dict(video='P01_01',samples=len(samples),labels=dict(labels),
        full_history=not limit_frames,replayed_observations=offset,oracle_supervision=True,
        geometry_policy='all strictly earlier views, compact prefix index; no chosen fusion or correction',
        geometry_index_sha256=sha(geometry/'geometry_index.json'),development_only=True))
    return samples


class CorrectionData:
    def __init__(self, root, geometry, examples):
        import numpy as np
        self.root=Path(root);self.geometry=Path(geometry);self.examples=Path(examples)
        self.rows={r['observation_key']:r for r in read(self.examples/'samples.json')}
        self.shapes={r['observation_key']:r for r in read(self.geometry/'geometry_index.json')['observations']}
        self.history=read(self.examples/'geometry_history.json')
        self.arrays=np.load(self.examples/'training_inputs.npz',allow_pickle=False)
    def example(self,key):
        r=self.rows[key]; histories=[]
        for tid,end in zip(r['candidate_track_ids'],r['candidate_history_ends']):
            views=self.history.get(str(tid),[])[:end]
            if any(v['frame_index']>=r['frame_index'] for v in views): raise ValueError('Future/current geometry leaked')
            histories.append([self.shapes[v['observation_key']] for v in views])
        return dict(numerical_input=self.arrays[r['numerical_input_key']].copy(),
            target_class=r['target_class'],label=self.arrays[r['numerical_label_key']].copy(),
            candidate_track_ids=r['candidate_track_ids'],query=self.shapes[key],candidate_views=histories)
    def close(self): self.arrays.close()
    def geometry_features(self,key,kind='surface'):
        """Existing D2/spectrum code; no new candidate-view selection policy."""
        if kind not in ('surface','points'): raise ValueError('Choose surface or points explicitly')
        sys.path.insert(0,str(self.root))
        from shape_tools.comparison import load_features
        asset=self.shapes[key]['artifacts'][kind]
        path=bounded(self.geometry,asset['path'])
        if sha(path)!=asset['sha256']: raise ValueError('Geometry asset changed')
        return load_features(path)


def baseline_logits(root, examples, output):
    import numpy as np
    import torch
    root=Path(root);examples=Path(examples);load_original(root)
    from models import get_model
    cfg=read(root/'baseline/effective_config.json')
    model=get_model('whareformer',**cfg['model']['architecture']).cpu().eval()
    model.load_state_dict(torch.load(root/'baseline/whareformer.pt',map_location='cpu',weights_only=True),strict=True)
    result={};torch.set_num_threads(2)
    with np.load(examples/'training_inputs.npz',allow_pickle=False) as z,torch.inference_mode():
        for r in read(examples/'samples.json'):
            x=torch.from_numpy(z[r['numerical_input_key']].copy()).float()[None,:,:]
            logits=model(x)[0].numpy()
            if not np.isfinite(logits).all(): raise ValueError('Nonfinite baseline logits')
            result[r['numerical_input_key']]=logits
    np.savez_compressed(output,**result)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['verify-geometry','build','logits'])
    p.add_argument('--root',type=Path,default=Path('.'));p.add_argument('--geometry',type=Path,default=Path('data/geometry'))
    p.add_argument('--examples',type=Path,default=Path('data/examples'));p.add_argument('--output',type=Path)
    p.add_argument('--expected',type=int,default=8126);a=p.parse_args()
    if a.command=='verify-geometry': print(json.dumps(verify_geometry(a.geometry,a.expected),indent=2))
    elif a.command=='build': build(a.root,a.geometry,a.examples)
    else: baseline_logits(a.root,a.examples,a.output or a.examples/'baseline_logits.npz')
