"""Storage adapter around the unchanged scientific shape_tools.pipeline."""
from pathlib import Path
import sys
from shape_tools import pipeline
from geometry_retention import install_cache_adapter, compact


def main():
    args = sys.argv[1:]
    output = Path(args[args.index('--output') + 1]).resolve()
    if args[0] in ('superflex', 'export'):
        install_cache_adapter(pipeline, output)
    pipeline.main()
    if args[0] == 'export':
        task = output.parent.parent
        compact(output, task / 'retention_tools/cpu_regeneration_verified.json', apply=True)


if __name__ == '__main__': main()
