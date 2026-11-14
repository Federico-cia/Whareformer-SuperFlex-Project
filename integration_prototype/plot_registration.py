"""Project estimated alignments for inspection; includes rejected proposals."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from cloud_memory import sample, radius

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('run',type=Path);args=parser.parse_args()
    records=json.loads((args.run/'registrations.json').read_text())
    observations={r['observation_key']:r for r in json.loads((ROOT/'outputs/geometric_closure_v1/observations.json').read_text())}
    groups={}
    for r in records:groups.setdefault((r['identity'],r['source']),[]).append(r)
    fig,axs=plt.subplots(len(groups),2,figsize=(12,3.2*len(groups)),squeeze=False)
    for row,((identity,source),entries) in enumerate(groups.items()):
        for n,e in enumerate(entries):
            obs=observations[e['observation_key']];rep='da_raw_points' if source=='da' else 'moge_points'
            with np.load(ROOT/'outputs/compare200_749968'/obs['representations'][rep]['path']) as data:p=sample(data['camera_points'],700,e['frame_index'])
            if n==0:center=p.mean(0);scale=radius(p)
            d=e['registration']
            if d:p=p@np.asarray(d['rotation'])+d['translation']
            p=(p-center)/scale
            label=f'{e["frame_index"]}: '+('anchor' if n==0 else 'accepted' if e['accepted'] else 'rejected')
            for col,(i,j) in enumerate([(0,1),(0,2)]):
                ax=axs[row,col];ax.scatter(p[:,i],p[:,j],s=4,alpha=.35,label=label)
                ax.set_aspect('equal',adjustable='datalim');ax.set_xlabel('X / anchor RMS');ax.set_ylabel(('Y' if j==1 else 'Z')+' / anchor RMS')
                ax.set_title(identity+' | '+source.upper());ax.grid(alpha=.15)
        for ax in axs[row]:ax.legend(fontsize=8)
    fig.suptitle('Diagnostic rigid alignment proposals (rejected views are NOT fused)',fontsize=13)
    fig.tight_layout(rect=(0,0,1,.97));fig.savefig(args.run/'alignment_diagnostic.png',dpi=150);plt.close(fig)


if __name__=='__main__':main()
