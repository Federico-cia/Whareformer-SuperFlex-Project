"""CPU integration check with the real checkpoint and controlled input features.

This is NOT a video tracking run. No original DINO/PCA features are substituted
by fixtures in any reported tracking metric; no tracking metric is produced.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import time

import numpy as np
import torch

from shape_adapter import ShapeLogitAdapter, FusionConfig
from shape_tools.memory import MemoryConfig


def load(path, name):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True);args=parser.parse_args();root=args.root
    expected='5b2e6692461f837ec662d0ac75a5f8c08e4fa9778e5c1b9833598cf90a58ee1d'
    checkpoint=root/'whareformer.pt'
    assert hashlib.sha256(checkpoint.read_bytes()).hexdigest()==expected
    if (root/'result.json').exists():raise FileExistsError('Preserve previous result')
    torch.set_num_threads(2);torch.manual_seed(13)
    model=load(root/'whareformer_model.py','original_model').Whareformer(
        app_dim=256,hidden_dim=64,depth=1,num_heads=32,emb_dropout=.1,enc_dropout=.1).cpu().eval()
    model.load_state_dict(torch.load(checkpoint,map_location='cpu',weights_only=True),strict=True)
    tree=ast.parse((root/'matcher_types.py').read_text())
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='WhareformerMatcher')
    method=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='_greedy_assignment')
    scope={'np':np};exec(compile(ast.fix_missing_locations(ast.Module(body=[method],type_ignores=[])),'original_greedy','exec'),scope)
    assign=lambda x:scope['_greedy_assignment'](None,x)
    rng=np.random.default_rng(13);count=0;max_error=0.;nonzero_changed=0;start=time.perf_counter()
    for detections in (1,2,7,20):
        for ntracks in (1,3,10):
            for _ in range(10):
                ids=[f't{i}' for i in range(ntracks)]
                a=ShapeLogitAdapter('controlled',MemoryConfig('controlled',capacity=2))
                active=ShapeLogitAdapter('controlled',MemoryConfig('controlled',capacity=2),FusionConfig(1.,.2))
                def feat(i):return None,np.array([float(i),float(i)+1.]),np.ones(3)
                init={f'init{i}':feat(i) for i in range(ntracks)}
                for adapter in (a,active):
                    adapter.score(0,list(init),init,[],np.zeros((ntracks,1),dtype=np.float32))
                    adapter.commit(dict(zip(init,ids)))
                inputs=rng.normal(size=(detections,ntracks+1,259)).astype(np.float32)
                norms=np.linalg.norm(inputs[:,:,:256],axis=-1,keepdims=True)
                inputs[:,:,:256]/=norms
                with torch.inference_mode():logits=model(torch.from_numpy(inputs))
                keys=[f'd{i}' for i in range(detections)]
                features={k:None if i%3==2 else feat(i) for i,k in enumerate(keys)}
                original=logits.numpy();after=a.score(1,keys,features,ids,original)['logits']
                positive=active.score(1,keys,features,ids,original)['logits']
                assert np.array_equal(original,after)
                p=torch.softmax(logits,dim=-1)
                q=torch.softmax(torch.from_numpy(after),dim=-1)
                assert torch.equal(p,q)
                assert assign(p.numpy())==assign(q.numpy())
                assert np.array_equal(original[:,0],positive[:,0]) and np.isfinite(positive).all()
                nonzero_changed+=bool(np.any(original!=positive))
                max_error=max(max_error,float(np.max(np.abs(original-after))))
                count+=1
    result=dict(checkpoint_sha256=expected,cases=count,zero_logits_exact=True,zero_torch_softmax_exact=True,
                zero_original_greedy_equal=True,max_logit_difference=max_error,
                active_path_cases_with_changed_logits=nonzero_changed,seconds=time.perf_counter()-start,
                torch=torch.__version__,device='cpu',features='controlled normalized random vectors, NOT original video features',
                limits=['Not a reproduction of P01_01 baseline or its metrics.','No proof of positive tracking effect from active geometry.'],
                code_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.glob('*.py')})
    (root/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
