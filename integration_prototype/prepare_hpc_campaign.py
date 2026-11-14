"""Package a bounded existing-account HPC campaign, without submitting jobs.

The resulting paths/Slurm scripts are explicit account-specific runtime files.
No credentials or weights are copied. External verified assets are required.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tarfile

from hpc_campaign import configurations,save


def package(output,project,remote_root,target_nouns):
    if output.exists():raise FileExistsError('Use a new campaign directory')
    output.mkdir(parents=True)
    source=Path(__file__).resolve().parent
    repo=source.parent
    shutil.copytree(source,output/'runtime/integration_prototype',ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copyfile(source/'submit_hpc_campaign.py',output/'submit_hpc_campaign_grouped.py')
    shutil.copytree(repo/'SuperFlex/src/shape_tools',output/'runtime/shape_tools',ignore=shutil.ignore_patterns('__pycache__'))
    project=project.rstrip('/')
    spec=dict(schema_version=1,development_only=True,video='P01_01',
        purpose='Expanded regenerated sparse geometry and paired full-history development sweep; no winner or held-out result assumed.',
        assets=dict(project=project,source_data=project+'/data_compare200/P01_01',
            mapping=project+'/data_compare200/mappings.json',geometry_config=project+'/portable_validation_v1/config.json',
            baseline_bundle=project+'/full_video_20261114_v1/bundle',
            baseline_manifest_sha256='1c9bdd82a85c4e78d149af89286bab61d9ddc154acaa05af983358e6ac618bee'),
        source_hashes={'fields.json':'4df5b3fe9b1848e7761e214e78f8f654fb90a82f2972bcce6c598d24b6bdcfce',
            'annotations.zip':'c848514f4586ac451373c0b0ea0af26029b4149a0d3863b27ecd020246ca2d6c',
            'rgb_prefix.bin':'4e1263004ae0f60e93e0b8573a24c1f57d58786a1d75b6ed5b1ad530fdd691db'},
        selection=dict(rule='All exact RGB/VISOR/official observation joins in the existing fixed archive prefix, up to 250 temporal quantiles; category policy inherited, frozen before inference.',
            maximum_frames=250,minimum_frames=120,minimum_observations=300,minimum_mask_pixels=128,
            target_nouns=target_nouns,alias_policy='Exclude all differing VISOR/RGB frame indices; verify ID/name/bbox in the same official frame.'),
        resources=dict(maximum_gpu_concurrency=2,maximum_cpu_array_concurrency=3,
            geometry_gpu_time_limit='02:00:00',gpu_variant_time_limit='00:45:00',
            cpu_variant_time_limit='00:45:00',maximum_gpu_resource_hours=9.5),
        variants=configurations(),
        invariants=['Full official feature history for each independent tracker',
            'All queries before frame updates','Observed points only, no completion feedback into clouds',
            'Frozen models/PCA; unchanged registration and fusion gates',
            'Same RGB masks/common valid pixels and point budgets for DA/MoGE',
            'One real SuperFlex after every admitted geometric update including initialization',
            'No automatic winner selection or held-out claims'])
    save(output/'campaign.json',spec)
    save(output/'policy.json',dict(fps=60,final_frame=99135,scope='full_video',dense_eval=True,min_count=3,distance_threshold=.3))
    common=f'''set -euo pipefail
module load /software/modules/miniconda3
eval "$(conda shell.bash hook)"
export TASK="{remote_root}"
export PROJECT="{project}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 WANDB_MODE=disabled MPLBACKEND=Agg
export HF_HOME="$PROJECT/hf_cache" HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1
export WHAREFORMER_SRC="$PROJECT/full_video_20261114_v1/bundle/original_src"
export PYTHONPATH="$TASK/runtime:$TASK/runtime/integration_prototype"
for wheel in "$PROJECT/recorded_metrics_v2/"*.whl; do export PYTHONPATH="$wheel:$PYTHONPATH"; done
cd "$TASK"
'''
    def job(name,body,minutes=15,gpu=False,mem=16,array=None):
        header=f'''#!/bin/bash
#SBATCH --job-name=cvx_{name}
#SBATCH --partition=stud
#SBATCH --qos=stud
#SBATCH --cpus-per-task=2
#SBATCH --mem={mem}G
#SBATCH --time={minutes//60:02}:{minutes%60:02}:00
#SBATCH --output=logs/{name}_%A_%a.out
#SBATCH --error=logs/{name}_%A_%a.err
'''
        if gpu:header+='#SBATCH --gpus=1\n'
        if array:header+=f'#SBATCH --array={array}\n'
        (output/(name+'.sbatch')).write_text(header+common+body,encoding='utf-8',newline='\n')
    cuda='''module load cuda/12.4
export CUDA_HOME="$(dirname "$(dirname "$(readlink -f "$(command -v nvcc)")")")"
export TORCH_EXTENSIONS_DIR="$PROJECT/torch_extensions" MAX_JOBS=2
'''
    job('preflight','''sha256sum -c files.sha256
conda activate "$HOME/.conda/envs/cv-superflex"
python -m unittest discover -s runtime/integration_prototype -p 'test_*.py' -q > preflight_tests.log 2>&1
conda activate "$HOME/.conda/envs/cv-moge2"
python -u runtime/integration_prototype/hpc_campaign.py select --task "$TASK"
''',minutes=20)
    job('geometry',cuda+'''for stage in da moge clouds superflex export; do
  case "$stage" in
    da) conda activate "$HOME/.conda/envs/cv-epic-depth"; export PYTHONPATH="$TASK/runtime" ;;
    moge) conda activate "$HOME/.conda/envs/cv-moge2"; export PYTHONPATH="$TASK/runtime:$PROJECT/external/rgb_sources/MoGe-07444410f1e33f402353b99d6ccd26bd31e469e8" ;;
    *) conda activate "$HOME/.conda/envs/cv-superflex"; export PYTHONPATH="$TASK/runtime:$PROJECT/SuperFlex-repo" ;;
  esac
  python -u -m shape_tools.pipeline "$stage" --manifest inputs/manifest.json --config inputs/config.json --output geometry
  python -m pip freeze > "geometry/environment_$stage.txt"
  echo "STAGE_COMPLETED $stage"
done
''',minutes=120,gpu=True,mem=24)
    job('build','''conda activate "$HOME/.conda/envs/cv-superflex"
python -u runtime/integration_prototype/hpc_campaign.py build --task "$TASK"
''',minutes=20,mem=24)
    job('cpu','''conda activate "$HOME/.conda/envs/cv-superflex"
python -u runtime/integration_prototype/hpc_campaign.py variant --task "$TASK" --lane cpu --index "$SLURM_ARRAY_TASK_ID"
''',minutes=45,mem=24,array='0-18%3')
    job('gpu',cuda+'''conda activate "$HOME/.conda/envs/cv-superflex"
export PYTHONPATH="$PYTHONPATH:$PROJECT/SuperFlex-repo"
python -u runtime/integration_prototype/hpc_campaign.py variant --task "$TASK" --lane gpu --index "$SLURM_ARRAY_TASK_ID"
''',minutes=45,gpu=True,mem=24,array='0-9%2')
    job('summarize','''conda activate "$HOME/.conda/envs/cv-superflex"
python -u runtime/integration_prototype/hpc_campaign.py summarize --task "$TASK"
''',minutes=20,mem=24)
    (output/'logs').mkdir()
    files=[p for p in output.rglob('*') if p.is_file()]
    (output/'files.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(output).as_posix()+'\n' for p in files),encoding='utf-8',newline='\n')
    archive=output.with_suffix('.tar.gz')
    with tarfile.open(archive,'w:gz') as tar:
        tar.add(output/'logs',arcname='logs',recursive=False)
        for path in output.rglob('*'):
            if path.is_file():tar.add(path,arcname=path.relative_to(output).as_posix())
    print(json.dumps(dict(package=str(output),archive=str(archive),variants={k:len(v) for k,v in spec['variants'].items()},
        maximum_gpu_hours=9.5,assets_copied=False),indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--project',required=True)
    p.add_argument('--remote-root',required=True)
    p.add_argument('--category-reference',type=Path,required=True)
    a=p.parse_args();targets=json.loads(a.category_reference.read_text(encoding='utf-8'))['target_nouns']
    package(a.output,a.project,a.remote_root,targets)
