"""Independent checks: full annotation join, causal prefixes, and reference446."""
import argparse
from collections import Counter
from pathlib import Path
import numpy as np
from p01_correction_data import read,save,CorrectionData


def verify(root,geometry,examples):
    root=Path(root);examples=Path(examples)
    frames=read(root/'baseline/frames.json');samples=read(examples/'samples.json')
    lookup={r['observation_key']:r for r in samples}
    source={r['observation_key']:r for r in read(Path(geometry)/'geometry_index.json')['observations']}
    if set(lookup)!=set(source) or len(lookup)!=len(samples): raise ValueError('Coverage/duplicates')
    histories=read(examples/'geometry_history.json'); names=[]; ids=[]; past={}; checked=0
    labels=Counter()
    with np.load(root/'baseline/features.npz',allow_pickle=False) as feature, np.load(examples/'training_inputs.npz',allow_pickle=False) as arrays:
        app=feature['app'].copy();loc=feature['loc'].copy()
        for frame in frames:
            staged=[]
            for i,ann in enumerate(frame['annotations']):
                key=f'P01_01/{frame["frame"]}__d{i}'
                if key in lookup:
                    row=lookup[key]; target=names.index(ann['name'])+1 if ann['name'] in names else 0
                    if row['target_class']!=target or row['candidate_names']!=names or row['candidate_track_ids']!=ids:
                        raise ValueError('Independent target/candidate order mismatch')
                    x=arrays[row['numerical_input_key']];y=arrays[row['numerical_label_key']]
                    offset=frame['offset']+i
                    expected=np.concatenate([app[offset],loc[offset]])
                    if x.shape!=(len(ids)+1,259) or not np.array_equal(x[0],expected) or not np.isfinite(x).all():
                        raise ValueError('Numerical query mismatch')
                    if y.shape!=(len(ids)+1,) or int(y.sum())!=1 or int(y.argmax())!=target: raise ValueError('Label mismatch')
                    for tid,end in zip(ids,row['candidate_history_ends']):
                        actual=histories.get(str(tid),[])[:end]
                        if actual!=past.get(str(tid),[]) or any(r['frame_index']>=frame['frame_index'] for r in actual):
                            raise ValueError('Incomplete/future geometry prefix')
                    checked+=1;labels['new_track' if target==0 else 'existing_track']+=1
                if ann['name'] not in names:
                    # Oracle adds unseen identities after all detections of the frame.
                    staged.append(ann['name'])
            for name in staged:
                if name not in names:names.append(name);ids.append(len(ids))
            for i,ann in enumerate(frame['annotations']):
                key=f'P01_01/{frame["frame"]}__d{i}'
                if key in lookup:
                    tid=names.index(ann['name']);past.setdefault(str(tid),[]).append(dict(observation_key=key,frame_index=frame['frame_index']))
        reference=read(root/'data/reference446/samples.json');ref_count=0
        with np.load(root/'data/reference446/training_inputs.npz',allow_pickle=False) as ref:
            for r in reference:
                if r['observation_key'] not in lookup: continue
                s=lookup[r['observation_key']]
                if not np.array_equal(arrays[s['numerical_input_key']],ref[r['numerical_input_key']]) or not np.array_equal(arrays[s['numerical_label_key']],ref[r['numerical_label_key']]):
                    raise ValueError('Reference446 changed')
                ref_count+=1
    return dict(status='passed',examples=checked,labels=dict(labels),reference446_identical=ref_count,
                full_annotation_join=True,causal_complete_history_prefixes=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path('.'))
    p.add_argument('--geometry',type=Path,default=Path('data/geometry'));p.add_argument('--examples',type=Path,default=Path('data/examples'));a=p.parse_args()
    result=verify(a.root,a.geometry,a.examples);save(a.examples/'verification.json',result);print(result)
