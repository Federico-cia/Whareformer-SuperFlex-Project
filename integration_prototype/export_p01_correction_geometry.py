"""Read-only geometry export, streamed to stdout. Execute by Marco on the HPC.

No new neural inference, no remote output files, no deletions. Derived PLYs are
reconstructed in RAM using the verified CPU recipe and original SHA-256.
"""
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile


def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def digest(data): return hashlib.sha256(data).hexdigest()


def collect(project):
    project=Path(project); task=project/'p01_full_enrichment_20261121_v1'
    campaign=project/'campaign_20261115_v1'
    roots=[(campaign/'geometry',campaign/'inputs/manifest.json')]
    for i in range(15):
        if not (task/'completed'/f'{i:04d}.json').is_file(): raise ValueError('Unfinished required block '+str(i))
        roots.append((task/'geometry'/f'{i:04d}',task/'batches'/f'{i:04d}.json'))
    seen=set(); records=[]
    for root,manifest in roots:
        sources={r['observation_key']:r for r in read(manifest)['observations']}
        products=read(root/'observations.json')
        if len(products)!=(446 if root==roots[0][0] else 512): raise ValueError('Unexpected block coverage')
        for row in products:
            key=row['observation_key']
            if key in seen or key not in sources or not key.startswith('P01_01/'): raise ValueError('Duplicate/unlinked key '+key)
            seen.add(key); source=sources[key]
            if row['representations']['da_points']['status']!='ready' or row['representations']['da_superflex']['status']!='ready':
                raise ValueError('Required DA representation unavailable '+key)
            records.append((root,manifest.parent,source,row))
    if len(seen)!=8126: raise ValueError('Expected exactly 8126 geometries')
    return records


def stream(project,output):
    project=Path(project).resolve()
    sys.path[:0]=[str(project/'p01_full_enrichment_20261121_v1/retention_tools'),
                  str(project/'campaign_20261115_v1/runtime'),str(project/'SuperFlex-repo')]
    records=collect(project); hashes={}; observations=[]; ledgers={}
    def bytes_for(root,asset):
        path=(root/asset['path']).resolve()
        if not path.is_relative_to(root.resolve()): raise ValueError('Artifact path escape')
        if path.is_file(): data=path.read_bytes()
        else:
            with redirect_stdout(sys.stderr):
                from geometry_retention import cpu_bytes,recipe_provenance
                if root not in ledgers:
                    ledger=read(root/'retention.json')
                    if ledger['provenance']!=recipe_provenance(root): raise ValueError('Changed regeneration environment')
                    ledgers.clear();ledgers[root]=ledger
                entry=ledgers[root]['entries'][asset['path']]
                if entry['kind']!='surface': raise ValueError('Unexpected absent artifact')
                data=cpu_bytes(root,entry)
        if digest(data)!=asset['sha256']: raise ValueError('Artifact checksum mismatch '+asset['path'])
        return data
    with tarfile.open(fileobj=output,mode='w|gz') as tar:
        def add(name,data):
            if name in hashes:
                if hashes[name]!=digest(data): raise ValueError('Archive path collision')
                return
            info=tarfile.TarInfo(name);info.size=len(data);info.mode=0o644;info.mtime=0
            tar.addfile(info,io.BytesIO(data));hashes[name]=digest(data)
        for number,(root,inputs,source,row) in enumerate(records,1):
            key=row['observation_key']; folder='geometry/'+hashlib.sha256(key.encode()).hexdigest()[:24]
            assets={}
            raw=row['representations']['da_points']; sf=row['representations']['da_superflex']
            for kind,asset in [('points',raw),('surface',sf),('parameters',sf['artifacts']['parameters'])]:
                filename={'points':'points.npz','surface':'reconstruction.ply','parameters':'shape_parameters.npz'}[kind]
                name=folder+'/'+filename;data=bytes_for(root,asset);add(name,data)
                assets[kind]=dict(path=name,sha256=digest(data))
            clean={k:v for k,v in source.items() if k not in ('rgb','mask')}
            for kind in ('rgb','mask'):
                path=(inputs/source[kind]).resolve(); data=path.read_bytes()
                if digest(data)!=source[kind+'_sha256']: raise ValueError('Source input hash mismatch '+key)
                name=('inputs/rgb/'+digest(data)+path.suffix.lower()) if kind=='rgb' else ('inputs/masks/'+folder.split('/')[-1]+'.png')
                add(name,data);clean[kind]=name
            clean['detection_idx']=int(key.rsplit('__d',1)[1])
            observations.append(dict(observation_key=key,source_observation=clean,artifacts=assets,
                representation='DA raw observed cloud and SuperFlex surface; no scene alignment certified',
                original_stage_signatures={k:row['representations'][k].get('stage_signature') for k in ('da_points','da_superflex')}))
            if number%128==0: print('EXPORTED',number,'/8126',file=sys.stderr,flush=True)
        add('geometry_index.json',json.dumps(dict(schema_version=1,video='P01_01',observations=observations),indent=2).encode())
        summary=dict(status='complete',observations=len(observations),unique_frames=len({r['source_observation']['frame_index'] for r in observations}),
            new_inferences=0,source='446 previous observations + 15 completed blocks of 512',
            sources=['da'],moGE_not_required_for_production=True,scene_alignment_certified=False)
        add('geometry_receipt.json',json.dumps(summary,indent=2).encode())
        add('SHA256SUMS',(''.join(v+'  '+k+'\n' for k,v in sorted(hashes.items()))).encode())
    print('EXPORT_COMPLETE',json.dumps(summary),file=sys.stderr,flush=True)


if __name__=='__main__': stream(Path.home()/'cv_project',sys.stdout.buffer)
