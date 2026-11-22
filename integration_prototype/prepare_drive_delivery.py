"""Prepare source-verified assets and one block trial, without Drive credentials or eviction."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

import drive_delivery as delivery


def prepare(project, package):
    project=Path(project).resolve();package=Path(package).resolve();public=package/'public'
    task=project/'p01_full_enrichment_20261121_v1'
    # Use the site's personal quota, not filesystem-wide free space.
    spec=importlib.util.spec_from_file_location('personal_quota',task/'hpc_quota_guard.py')
    quota_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(quota_module)
    try:
        q=subprocess.run(['/userScripts/myquota'],check=True,capture_output=True,text=True).stdout
        quota=quota_module.parse_quota(q)
    except FileNotFoundError:
        q=subprocess.run(['/usr/sbin/beegfs','quota','list-usage'],check=True,capture_output=True,text=True).stdout
        quota=quota_module.parse_native_quota(q,os.getuid())
    if quota['free_bytes']<3.2*1024**3 or quota['free_files']<8000:raise RuntimeError('Insufficient personal reserve for preparation and restore test')
    entries=[]
    def add(source,target,groups,description,expected=None):
        entry=delivery.source_entry(source,target,groups,description)
        if expected and entry['sha256']!=expected:raise ValueError('Pinned source differs: '+target)
        entries.append(entry);print('INDEXED',target,entry['bytes'],flush=True)
        return entry
    # Public administrative files are created locally and copied before this job.
    for p in sorted(public.rglob('*')):
        if p.is_file() and p.name not in ('CATALOG.json','PUBLISH_STATUS.json'):
            rel=p.relative_to(public).as_posix()
            group=['pilot','complete'] if not rel.startswith('06_RESEARCH/') else ['complete','point3']
            add(p,rel,group,'Prepared code, documentation or research fixture')
    data=project/'data_compare200';video=data/'P01_01'
    coverage=delivery.read(task/'coverage.json');cfg=delivery.read(task/'inputs/config.json')
    add(task/'P01_01.tar','03_INPUTS/P01_01/rgb/P01_01.tar',['complete','geometry'],'Official RGB archive',coverage['archive_sha256'])
    add(video/'annotations.zip','03_INPUTS/P01_01/visor/annotations.zip',['complete','geometry'],'Official VISOR polygons',coverage['mask_archive_sha256'])
    for source,target,desc in [(video/'fields.json','03_INPUTS/P01_01/scene/fields.json','Camera intrinsics and EPIC-Fields poses'),
                               (video/'mesh.ply','03_INPUTS/P01_01/scene/mesh.ply','Scene mesh'),
                               (data/'mappings.json','03_INPUTS/mappings.json','VISOR to RGB mapping'),
                               (project/'campaign_20261115_v1/bundle/frames.json','03_INPUTS/P01_01/frames.json','Original ordered frames/detections')]:
        add(source,target,['complete','geometry'],desc)
    model=project/'hf_cache/hub/models--depth-anything--Depth-Anything-V2-Metric-Indoor-Large-hf/snapshots'/cfg['da']['revision']
    for name in ('config.json','preprocessor_config.json','model.safetensors'):
        add(model/name,'02_MODELS/depth_anything/'+cfg['da']['revision']+'/'+name,['complete','geometry'],'Pinned DA model snapshot')
    for name,target,expected in [('checkpoint','02_MODELS/superflex/ckpt.pt',cfg['superflex']['checkpoint_sha256']),
                                 ('config','02_MODELS/superflex/config.yaml',cfg['superflex']['config_sha256'])]:
        add(cfg['superflex'][name],target,['complete','geometry','point3'],'Original SuperFlex robust '+name,expected)
    add(cfg['moge']['checkpoint'],'02_MODELS/moge/'+cfg['moge']['revision']+'/model.pt',['complete','moge_optional'],'Optional MoGE comparison weights',cfg['moge']['checkpoint_sha256'])
    # Prepared tracking bundle contains the numerical features, ordered observations,
    # original tracker code/config/checkpoint and sparse geometry used in existing runs.
    bundle=project/'campaign_20261115_v1/bundle'
    from frontend_inputs import verify_bundle
    bundle_plan,frames=verify_bundle(bundle)
    tracking=public/'04_TRACKING/P01_01/prepared_bundle.tar'
    if not tracking.exists():delivery.pack_directory(bundle,tracking,'prepared_bundle')
    add(tracking,'04_TRACKING/P01_01/prepared_bundle.tar',['complete','tracking'],'Verified original numerical tracking bundle')
    source=task/'geometry/0004';archive=public/'05_OUTPUTS/P01_01/legacy_da_moge/blocks/0004.tar'
    if not archive.exists():delivery.pack_directory(source,archive,'0004',{'0004/source_manifest.json':task/'batches/0004.json'})
    pilot_entry=add(archive,'05_OUTPUTS/P01_01/legacy_da_moge/blocks/0004.tar',['pilot','complete'],'Compact real block: 512 observations, DA/MoGE')
    pilot_entry['role']='pilot_block'
    scratch=package/'scratch';scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='restore_',dir=scratch) as temp:
        target=Path(temp)/'data';roundtrip=delivery.verify_archive(archive,target)
        import geometry_retention
        root=target/'0004';ledger=delivery.read(root/'retention.json');recovered=[]
        for kind in ('input','surface','diagnostic_prediction'):
            entry=next(e for e in ledger['entries'].values() if e['kind']==kind)
            path=geometry_retention.regenerate(root,entry['path'],Path(temp)/(kind+Path(entry['path']).suffix))
            assert delivery.digest(path)==entry['sha256'];recovered.append(dict(kind=kind,sha256=entry['sha256']))
    pilot=dict(status='prepared_verified_locally',block='0004',observations=512,archive=pilot_entry['path'],
               archive_sha256=pilot_entry['sha256'],archive_bytes=pilot_entry['bytes'],roundtrip=roundtrip,
               cpu_regeneration=recovered,cloud_upload_tested=False,sources_evicted=False,
               tracking_bundle=dict(verified=True,frames=len(frames),observations=bundle_plan['coverage']['expected_observations']),
               created_unix=time.time())
    receipt=public/'07_VALIDATION/PILOT_PREPARATION.json';delivery.save(receipt,pilot)
    add(receipt,'07_VALIDATION/PILOT_PREPARATION.json',['pilot','complete'],'Real local archive/restore and CPU regeneration test')
    catalog=dict(schema_version=1,name='Whareformer-SuperFlex',status='prepared_not_uploaded',
                 scope='P01_01 geometry inputs and tracking bundle; point3 research fixture; P01_02 inputs not available',
                 scientific_policy='DA production; MoGE comparison only. Existing legacy outputs preserved.',
                 assets=[{k:v for k,v in e.items() if k!='source'} for e in entries])
    delivery.save(public/'CATALOG.json',catalog)
    add(public/'CATALOG.json','CATALOG.json',['pilot','complete'],'Relative paths, checksums, roles and component inventory')
    delivery.save(package/'private_upload_plan.json',dict(schema_version=1,assets=entries))
    delivery.save(package/'preparation_completed.json',dict(status='passed',assets=len(entries),pilot=pilot,
                 source_bytes=sum(e['bytes'] for e in entries),cloud_authorization_required=True))
    print('DELIVERY_PREPARED',len(entries),sum(e['bytes'] for e in entries),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project',type=Path,required=True);p.add_argument('--package',type=Path,required=True)
    a=p.parse_args();prepare(a.project,a.package)
