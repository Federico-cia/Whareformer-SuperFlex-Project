"""Consolidate saved distances; never recompute geometry or assign identities."""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from .comparison import file_hash
from .evaluation import evaluate
from .pipeline import save_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--observations", type=Path, required=True)
    parser.add_argument("--distances", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--plot", action="store_true")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    observations = json.loads(args.observations.read_text(encoding="utf-8-sig"))
    coverage = {}
    for row in observations:
        for name, info in row["representations"].items():
            count = coverage.setdefault(name, Counter())
            count[info["status"]] += 1
    review = list(csv.DictReader(args.review.open(encoding="utf-8-sig")))
    accepted = [
        r
        for r in review
        if r["identity_status"] == "visually_verified" and r["physical_identity"] and r["evidence"]
    ]
    result = evaluate(args.distances, args.review, args.output / "separation.json")
    summary = dict(
        observations=len(observations),
        videos=len({r["video"] for r in observations}),
        reviewed_observations=len(accepted),
        reviewed_identities=len({(r["video"], r["physical_identity"]) for r in accepted}),
        observation_coverage=coverage,
        paired_evaluation=result,
        provenance=dict(observations_sha256=file_hash(args.observations)),
        limitations=[
            "Visual identity labels are not certified persistent ground truth.",
            "Pairs share observations; no independent-pair confidence intervals.",
            "Same-identity distances and AUC are descriptive development evidence, not tracking accuracy.",
            "Common-pair analysis conditions on availability; coverage is reported separately.",
        ],
    )
    save_json(args.output / "summary.json", summary)
    if args.plot:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        groups = [
            (v, c, reps)
            for v, cats in result["by_video"].items()
            for c, reps in cats.items()
            if any(s["d2_wasserstein"]["auc"] is not None for s in reps.values())
        ]
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), constrained_layout=True)
        for video, category, reps in groups:
            names = list(reps)
            axes[0].plot(
                range(len(names)),
                [reps[n]["d2_wasserstein"]["auc"] for n in names],
                marker="o",
                label=f"{video} / {category}",
            )
            axes[1].plot(
                range(len(names)),
                [reps[n]["d2_wasserstein"]["median_same"] for n in names],
                marker="o",
                label=f"{video} / {category}: same",
            )
            axes[1].plot(
                range(len(names)),
                [reps[n]["d2_wasserstein"]["median_different"] for n in names],
                marker="s",
                linestyle="--",
                label=f"{video} / {category}: different",
            )
        if groups:
            for ax in axes:
                ax.set_xticks(range(len(names)), [n.replace("_", "\n") for n in names])
                ax.legend(fontsize=8)
                ax.grid(alpha=0.2)
        axes[0].axhline(0.5, color="gray", linestyle=":")
        axes[0].set_ylim(0, 1)
        axes[0].set_ylabel("D2 AUC (descriptive)")
        axes[1].set_ylabel("Median normalized D2 distance")
        fig.suptitle("Within-category identity evidence — dependent pairs, visual labels")
        fig.savefig(args.output / "identity_signal.png", dpi=180)
        plt.close(fig)


if __name__ == "__main__":
    main()
