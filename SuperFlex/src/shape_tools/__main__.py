import argparse

from .comparison import compare
from .evaluation import evaluate


def main():
    parser = argparse.ArgumentParser(description="Paired shape comparison from saved geometry.")
    commands = parser.add_subparsers(dest="command", required=True)
    comparison = commands.add_parser("compare")
    comparison.add_argument("manifest")
    comparison.add_argument("--root", required=True)
    comparison.add_argument("--output", required=True)
    comparison.add_argument("--registration", action="store_true")
    evaluation = commands.add_parser("evaluate")
    evaluation.add_argument("distances")
    evaluation.add_argument("review")
    evaluation.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.command == "compare":
        count = compare(args.manifest, args.root, args.output, args.registration)
        print(f"Compared {count} pairs")
    else:
        result = evaluate(args.distances, args.review, args.output)
        print(f"Evaluated {result['common_pairs']} common labeled pairs")


if __name__ == "__main__":
    main()
