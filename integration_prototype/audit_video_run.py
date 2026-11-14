"""Audit complete frame coverage, causal geometry and final observed memory.

Run next to the identical production source/runtime. Assertions are evidence
checks, not independent physical-identity or reconstruction-quality validation.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

from cloud_updater import cloud_hash
from deferred_superflex import validate_request, bound_file


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def audit(bundle, inference, cache, output, baseline):
    if output.exists():
        raise FileExistsError('Preserve previous audits')
    summary=json.loads((inference/'summary.json').read_text())
    plan=json.loads((bundle/'input_manifest.json').read_text())
    frames=json.loads((bundle/'frames.json').read_text())
    cloud_ids={f'{plan["video"]}/{row["frame"]}__d{i}':ids
        for row in frames for i,ids in enumerate(row['cloud_ids'])}
    with np.load(bundle/'observed_clouds.npz',allow_pickle=False) as z:
        observed={key:z[key].copy() for key in z.files}
    assert plan['coverage']['complete_official_sequence']
    assert summary['expected_frames']==len(frames)==plan['coverage']['expected_feature_frames']
    opener=gzip.open if baseline.suffix=='.gz' else open
    with opener(baseline,'rt',encoding='utf-8') as stream:
        original=json.load(stream)
    recorded={(row['frame'],row['detection_idx']):str(tid)
        for tid,items in original['tracks'].items() for row in items}
    variants=[]
    for variant in summary['variants']:
        name=variant['config']['name']
        assert variant['status']=='completed' and not variant['counts']['pending_requests']
        predictions=inference/(name+'.jsonl')
        assert sha(predictions)==summary['prediction_export_sha256'][name]
        requests={}
        for folder in sorted((cache/name).iterdir()):
            if not folder.is_dir() or not (folder/'request.json').is_file():
                continue
            req=validate_request(folder)
            result=json.loads((folder/'result.json').read_text())
            assert result['backend']=='superflex' and result['request_id']==req['request_id']
            assert result['request_sha256']==sha(folder/'request.json')
            if result['status']=='ready':
                bound_file(folder,result['features'])
            requests[req['request_id']]=(req,result,folder)
        updates=[];queries=[];differences=[];geometry_frames=[];recon_queries=[];fused_queries=[]
        all_keys=set();per_track=Counter();frame_count=0;observations=0
        with predictions.open() as stream:
            for index,line in enumerate(stream):
                row=json.loads(line);expected=frames[index]
                assert row['frame_index']==expected['frame_index']
                assert row['detections']==len(expected['annotations'])==len(row['assignments'])
                assert row['evaluation_timestamp']==row['frame_index']/plan['fps']
                keys=[f'{plan["video"]}/{expected["frame"]}__d{i}' for i in range(row['detections'])]
                assert row['evaluation_key_order']==keys and set(keys)==set(row['assignments'])
                assert not all_keys.intersection(keys)
                all_keys.update(keys)
                for i,key in enumerate(keys):
                    assigned=row['assignments'][key];per_track[assigned]+=1
                    if assigned!=recorded[expected['frame'],i]:
                        differences.append(dict(frame=row['frame_index'],detection_idx=i,
                            baseline=recorded[expected['frame'],i],active=assigned))
                current=[dict(frame=row['frame_index'],**e) for e in row['updates'] if e['status'] not in ('missing','not_requested')]
                updates.extend(current)
                if row['cloud_inputs_available']:
                    geometry_frames.append(row['frame_index'])
                for query in row['geometric_queries']:
                    q=dict(frame=row['frame_index'],**query)
                    assert abs(q['logit_delta']-variant['config']['weight']*(variant['config']['neutral_distance']-q['distance']))<2e-6
                    for evidence in q['evidence']:
                        if evidence.startswith('reconstruction/'):
                            rid=evidence.split('/',1)[1]
                            req,result,folder=requests[rid]
                            assert result['status']=='ready'
                            assert req['spec']['frame_index']<q['frame']
                            assert req['spec']['track_id']==q['track_id']
                            recon_queries.append(q)
                            if req['spec']['cloud_version']>1:
                                fused_queries.append(q)
                        else:
                            prior=int(evidence.split('/frame_',1)[1].split('__',1)[0])
                            assert prior<q['frame']
                    queries.append(q)
                frame_count+=1;observations+=row['detections']
        assert frame_count==len(frames) and observations==plan['coverage']['expected_observations']
        assert len(updates)==plan['coverage']['observed_clouds'][variant['config']['source']]
        accepted=[e for e in updates if e['status']=='accepted']
        assert len(requests)==len(accepted)
        memory_dir=inference/(name+'_memory')
        memory=json.loads((memory_dir/'manifest.json').read_text())
        rebuild_errors=[]
        assert not memory['pending_reconstructions']
        assert sha(memory_dir/'observed_points.npz')==memory['observed_points_sha256']
        with np.load(memory_dir/'observed_points.npz',allow_pickle=False) as clouds:
            for tid,state in memory['geometry'].items():
                assert cloud_hash(clouds[tid])==state['cloud_sha256']
                matching=[v for v in requests.values() if v[0]['spec']['track_id']==tid]
                req,result,folder=max(matching,key=lambda v:v[0]['spec']['cloud_version'])
                assert req['spec']['cloud_sha256']==state['cloud_sha256']
                with np.load(bound_file(folder,req['input']),allow_pickle=False) as z:
                    assert np.array_equal(clouds[tid],z['object_points'])
                rebuilt=[]
                for entry in state['provenance']:
                    raw=np.asarray(observed[cloud_ids[entry['key']][state['source']]],dtype=np.float64)
                    assert cloud_hash(raw)==entry['provenance']['observed_points_sha256']
                    frame=entry['frame']
                    indices=np.random.default_rng(frame).choice(len(raw),min(state['config']['max_observation_points'],len(raw)),replace=False)
                    limited=raw[indices]
                    moved=limited if entry==state['provenance'][0] else limited@np.asarray(entry['rotation'])+np.asarray(entry['translation'])
                    ids=np.random.default_rng(frame).choice(len(moved),min(state['config']['points_per_view'],len(moved)),replace=False)
                    rebuilt.append(moved[ids])
                reconstructed=np.concatenate(rebuilt)
                # Independent BLAS implementations can round the same 3D rigid
                # transform differently. Bound verification by floating-point
                # arithmetic, never by a fitted geometric registration gate.
                tolerance=32*np.finfo(np.float64).eps*max(1.,float(np.max(np.abs(clouds[tid]))))
                error=float(np.max(np.abs(clouds[tid]-reconstructed)))
                assert np.allclose(clouds[tid],reconstructed,rtol=0,atol=tolerance), 'Observed-memory reconstruction mismatch'
                rebuild_errors.append(error)
        assert any(q['logit_delta']!=0 for q in queries)
        assert recon_queries,'No verified use of an earlier real SuperFlex result'
        detail=dict(name=name,frames=frame_count,observations=observations,first_frame=frames[0]['frame_index'],
            final_observed_frame=frames[-1]['frame_index'],tracks=len(per_track),
            geometry_frames=len(geometry_frames),geometric_queries=len(queries),
            changed_logit_pairs=sum(q['logit_delta']!=0 for q in queries),
            maximum_absolute_logit_delta=max(abs(q['logit_delta']) for q in queries),
            reconstruction_comparison_pairs=len(recon_queries),
            reconstruction_query_frames=len({q['frame'] for q in recon_queries}),
            fused_reconstruction_comparison_pairs=len(fused_queries),
            fused_reconstruction_query_frames=len({q['frame'] for q in fused_queries}),
            updates=dict(Counter(e['status'] for e in updates)),
            initializations=sum(e['diagnostics']['operation']=='initialize' for e in accepted),
            accepted_fusions=sum(e['diagnostics']['operation']=='register_and_accumulate' for e in accepted),
            fusion_events=[dict(frame=e['frame'],track_id=e['track_id'],observation_key=e['observation_key'],
                observation_keys=e['diagnostics']['candidate_memory']['observation_keys'])
                for e in accepted if e['diagnostics']['operation']=='register_and_accumulate'],
            rejection_reasons=dict(Counter(reason for e in updates if e['status']=='rejected' for reason in e['reasons'])),
            reconstructions=dict(Counter(v[1]['status'] for v in requests.values())),
            final_memory_tracks=len(memory['geometry']),
            final_observed_points=sum(v['points'] for v in memory['geometry'].values()),
            maximum_observed_memory_rebuild_error=max(rebuild_errors),
            rebuild_tolerance='32 * float64 epsilon * max(1, abs cloud maximum); no relative tolerance',
            assignment_differences_from_recorded_baseline=len(differences),
            differing_frames=len({v['frame'] for v in differences}),
            assertions_passed=['all official frames/observations in order','geometry logit correction numerically present',
                'all query evidence strictly predates frame','real earlier SuperFlex reconstructions used',
                'one request per accepted update','final observed memory equals latest request cloud',
                'final memory rebuilt from admitted observations/rigid transforms within floating-point roundoff',
                'point/request/result/export hashes valid'],
            limits=['Sparse cached frontend, no raw RGB regeneration or physical identity GT.',
                'Accepted fusion is algorithmic admission, not independently validated physical alignment.'])
        variants.append(detail)
        output.mkdir(parents=True,exist_ok=True)
        for filename,data in [('updates.json',updates),('geometric_queries.json',queries),('assignment_differences.json',differences)]:
            (output/(name+'_'+filename)).write_text(json.dumps(data,indent=2)+'\n')
    result=dict(video=plan['video'],input_manifest_sha256=sha(bundle/'input_manifest.json'),
        inference_summary_sha256=sha(inference/'summary.json'),baseline_sha256=sha(baseline),variants=variants)
    (output/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['bundle','inference','cache','output','baseline']:
        parser.add_argument('--'+name,type=Path,required=True)
    audit(**vars(parser.parse_args()))
