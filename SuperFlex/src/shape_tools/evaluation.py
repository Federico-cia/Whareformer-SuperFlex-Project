"""Descriptive identity separation on common pairs, grouped by video and category."""

import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import rankdata

from .comparison import METRICS, atomic_output, file_hash


def separation(same, different):
    auc = None
    if same and different:
        n, m = len(same), len(different)
        ranks = rankdata(np.r_[same, different])
        auc = float((ranks[n:].sum() - m * (m + 1) / 2) / (n * m))
    return dict(
        same_pairs=len(same),
        different_pairs=len(different),
        auc=auc,
        median_same=float(np.median(same)) if same else None,
        median_different=float(np.median(different)) if different else None,
    )


def evaluate(distances, review, output):
    with Path(review).open(encoding="utf-8-sig", newline="") as stream:
        labels = list(csv.DictReader(stream))
    keys = [r["observation_key"] for r in labels]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate review keys")
    labels = {
        r["observation_key"]: r
        for r in labels
        if r["identity_status"] == "visually_verified" and r["physical_identity"] and r["evidence"]
    }
    with Path(distances).open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError("Empty distance table")
    names = sorted({r["representation"] for r in rows})
    present = defaultdict(set)
    pairs = defaultdict(list)
    metrics = []
    ready = [r for r in rows if r["status"] == "ready"]
    for metric in METRICS:
        populated = [r.get(metric, "") != "" for r in ready]
        if any(populated) and not all(populated):
            raise ValueError(f"Partially computed metric: {metric}")
        if populated and all(populated):
            metrics.append(metric)
    if not metrics:
        raise ValueError("No computed metrics")
    for row in rows:
        pair = (row["video"], row["left"], row["right"])
        if row["representation"] in present[pair]:
            raise ValueError("Duplicate pair/representation")
        present[pair].add(row["representation"])
        if row["status"] not in ("ready", "unavailable"):
            raise ValueError("Unknown result status")
        for metric in metrics:
            if row["status"] == "ready":
                value = float(row[metric])
                if not np.isfinite(value) or value < 0:
                    raise ValueError("Distances must be finite and nonnegative")
        pairs[pair].append(row)
    if any(sorted(items) != names for items in present.values()):
        raise ValueError("Missing representation rows")
    groups, coverage = {}, dict.fromkeys(names, 0)
    labeled, common = 0, 0
    for (video, left, right), pair_rows in pairs.items():
        if left not in labels or right not in labels:
            continue
        a, b = labels[left], labels[right]
        if a["video"] != video or b["video"] != video or a["rgb_frame"] == b["rgb_frame"]:
            raise ValueError("Review and pair metadata disagree")
        labeled += 1
        for row in pair_rows:
            coverage[row["representation"]] += row["status"] == "ready"
        if any(r["status"] != "ready" for r in pair_rows):
            continue
        common += 1
        if a["category"] != b["category"]:
            continue
        category = a["category"]
        group = groups.setdefault(video, {}).setdefault(category, {})
        for row in pair_rows:
            for metric in metrics:
                bucket = group.setdefault(row["representation"], {}).setdefault(metric, [[], []])
                bucket[a["physical_identity"] != b["physical_identity"]].append(float(row[metric]))
    for categories in groups.values():
        for representations in categories.values():
            for scores in representations.values():
                for metric, (same, different) in scores.items():
                    scores[metric] = separation(same, different)
    result = dict(
        review_sha256=file_hash(review),
        distances_sha256=file_hash(distances),
        labeled_pairs=labeled,
        common_pairs=common,
        coverage=coverage,
        by_video=groups,
        limitation="Dependent pairs and visually reviewed labels; not tracking accuracy.",
    )
    with atomic_output(output) as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
    return result
