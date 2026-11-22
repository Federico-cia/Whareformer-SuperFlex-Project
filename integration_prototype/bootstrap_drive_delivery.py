"""Verify/extract a downloaded delivery and write location-independent P01_01 settings."""
import argparse
import json
from pathlib import Path
import sys
import zipfile

from drive_delivery import digest, read, save, safe_relative, validate_catalog, verify_archive


def configure(root, work, python_da, python_sf, batch_size=512):
    root=Path(root).resolve();work=Path(work).resolve();work.mkdir(parents=True,exist_ok=True)
    check=validate_catalog(root,['geometry'])
    if check['status']!='passed':raise ValueError('Geometry assets missing or corrupt; run verify first')
    archive=root/'01_CODE/pipeline_source_v1.zip';catalog=read(root/'CATALOG.json')
    record=next(x for x in catalog['assets'] if x['path']=='01_CODE/pipeline_source_v1.zip')
    if digest(archive)!=record['sha256']:raise ValueError('Code checksum differs')
    code=work/'code'
    if not code.exists():
        code.mkdir()
        with zipfile.ZipFile(archive) as z:
            for item in z.infolist():
                if item.is_dir():continue
                relative=safe_relative(item.filename);target=code/str(relative)
                target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(item))
    geometry=code/'geometry'
    cfg=read(geometry/'geometry_config.json')
    revision=cfg['da']['revision'];cfg['da']['model']=str(root/'02_MODELS/depth_anything'/revision)
    cfg['sources']=['da'];cfg.pop('moge',None);cfg['clouds'].update(pixel_policy='source',minimum_points=64)
    cfg['superflex']['checkpoint']=str(root/'02_MODELS/superflex/ckpt.pt')
    cfg['superflex']['config']=str(root/'02_MODELS/superflex/config.yaml')
    config=work/'geometry_config.json';save(config,cfg)
    settings=dict(video='P01_01',task=str(work/'P01_01'),frames=str(root/'03_INPUTS/P01_01/frames.json'),
                  fields=str(root/'03_INPUTS/P01_01/scene/fields.json'),mapping=str(root/'03_INPUTS/mappings.json'),
                  annotations=str(root/'03_INPUTS/P01_01/visor/annotations.zip'),rgb_tar=str(root/'03_INPUTS/P01_01/rgb/P01_01.tar'),
                  mesh=str(root/'03_INPUTS/P01_01/scene/mesh.ply'),runtime=str(geometry/'runtime'),superflex_repo=str(geometry/'authors'),
                  geometry_config=str(config),python_da=str(Path(python_da).resolve()),python_sf=str(Path(python_sf).resolve()),
                  batch_size=batch_size,quota_command=[str(Path(python_da).resolve()),str(geometry/'quota_site.py')],
                  reserve_bytes=2147483648,reserve_files=12000)
    save(work/'settings.json',settings)
    return dict(settings=str(work/'settings.json'),driver=str(geometry/'full_video_enrichment.py'),
                note='Configure site modules and quota command before prepare/run. This writes a new task, not a resume of legacy caches.')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True);p.add_argument('--work',type=Path,required=True)
    p.add_argument('--python-da',required=True);p.add_argument('--python-sf',required=True);p.add_argument('--batch-size',type=int,default=512)
    a=p.parse_args();print(json.dumps(configure(a.root,a.work,a.python_da,a.python_sf,a.batch_size),indent=2))


if __name__=='__main__':main()
