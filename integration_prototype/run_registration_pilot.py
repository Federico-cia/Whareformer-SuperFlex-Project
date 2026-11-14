"""Fixed small diagnostic selection: known-transform control + real-view replay."""
import argparse
import csv
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import time

import numpy as np

from cloud_memory import ObservedCloudMemory, RegistrationConfig, register_rigid, radius, sample

ROOT = Path(__file__).resolve().parents[1]
SELECTION = {
    'P01_01_green_board_A': [2893, 5099, 7508],
    'P03_04_orange_knife_A': [8115, 19311, 20618],
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--selection', type=Path, help='Optional metadata-based diagnostic selection, fixed before scoring')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Choose a new directory to preserve existing evidence')
    args.output.mkdir(parents=True)
    config = RegistrationConfig()
    selection=json.loads(args.selection.read_text(encoding='utf-8')) if args.selection else SELECTION
    save(args.output/'plan.json', dict(selection=selection, config=asdict(config),
         memory_views=4, points_per_view=2048, max_observation_points=12000,
         purpose='diagnostic, associations externally provided; no threshold tuning on these results'))
    start = time.perf_counter()
    reviews = {r['observation_key']:r['physical_identity'] for r in csv.DictReader(
        (ROOT/'outputs/shape_identity_v1/identity_review.csv').open(encoding='utf-8-sig'))
        if r['identity_status']=='visually_verified'}
    observations = json.loads((ROOT/'outputs/geometric_closure_v1/observations.json').read_text(encoding='utf-8'))
    rows = [r for r in observations if reviews.get(r['observation_key']) in selection
            and r['frame_index'] in selection[reviews[r['observation_key']]]]
    assert len(rows)==sum(len(x) for x in selection.values())
    records=[]; exports=[]; inputs={}; controls=[]
    def load(row, source):
        info=row['representations']['da_raw_points' if source=='da' else 'moge_points']
        path=ROOT/'outputs/compare200_749968'/info['path']
        assert digest(path)==info['sha256']
        with np.load(path,allow_pickle=False) as data:p=data['camera_points'].copy()
        inputs[row['observation_key']+'/'+source]=info['sha256']
        return sample(p,12000,row['frame_index'])
    # Check recovery on real point geometry under a known artificial pose.
    first=min(rows,key=lambda r:(r['video'],r['frame_index']))
    for source in ('da','moge'):
        p=load(first,source)
        angle=.6; rot=np.array([[np.cos(angle),0,np.sin(angle)],[0,1.,0],[-np.sin(angle),0,np.cos(angle)]])
        trans=np.array([.2,-.1,.3]); transformed=p@rot+trans
        decision=register_rigid(transformed,p,config)
        aligned=transformed@np.asarray(decision['rotation'])+decision['translation']
        truth_error=float(np.sqrt(np.mean(np.sum((aligned-p)**2,axis=1)))/radius(p))
        controls.append(dict(source=source,decision=decision,known_correspondence_rmse_rms=truth_error))
    for identity, frames in selection.items():
        selected=sorted([r for r in rows if reviews[r['observation_key']]==identity],key=lambda r:r['frame_index'])
        for source in ('da','moge'):
            memory=ObservedCloudMemory(selected[0]['video'],identity,source,views=4,points_per_view=2048)
            for row in selected:
                p=load(row,source); before=memory.cloud()
                decision=register_rigid(p,before,config) if before is not None else None
                outcome=memory.update(row['observation_key'],row['frame_index'],p,registration=decision,
                    provenance={'input_sha256':inputs[row['observation_key']+'/'+source], 'association':'external visual diagnostic label'})
                records.append(dict(identity=identity,source=source,observation_key=row['observation_key'],
                                    frame_index=row['frame_index'],input_points=len(p),registration=decision,**outcome))
                if outcome['accepted']:
                    name=f'{identity}_{source}_v{memory.snapshot()["version"]}.npz'
                    np.savez_compressed(args.output/name,object_points=memory.cloud())
                    item=dict(identity=identity,source=source,frame_index=row['frame_index'],
                              version=memory.snapshot()['version'],path=name,sha256=digest(args.output/name),
                              coordinate_frame='camera of first observation, used as fixed object reference',
                              provenance=memory.provenance())
                    exports.append(item)
                    save(args.output/(name+'.json'),item)
    accepted=[r for r in records if r['registration'] is not None and r['accepted']]
    attempts=2*sum(len(frames)-1 for frames in selection.values())
    summary=dict(selection=selection,real_registration_attempts=attempts,accepted_real_updates=len(accepted),
                 rejected_real_updates=attempts-len(accepted),initializations=2*len(selection),controls=controls,
                 elapsed_seconds=time.perf_counter()-start,
                 input_hashes=inputs,code_sha256={p.name:digest(p) for p in [Path(__file__),Path(__file__).with_name('cloud_memory.py')]},
                 limits=['Acceptance under provisional gates is not proof of physical alignment or identity.',
                         'Rigid only; source scale not corrected, no camera/object pose ground truth.',
                         'Validation query sets are disjoint from fit sets; same observations, not independent views.',
                         'No tracking or neural inference executed by this runner.'])
    save(args.output/'registrations.json',records);save(args.output/'exports.json',exports);save(args.output/'summary.json',summary)
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
