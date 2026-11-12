"""Local annotation-consistency diagnostic, never global identity ground truth.

Usage: python local_interval_diagnostic.py observations.json distances.csv output.json
Requires optional observation metadata: interpolation and exact category/name.
Pairs are determined solely from metadata before reading saved distances.
"""

import csv
import itertools
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

from shape_tools.comparison import METRICS, file_hash
from shape_tools.pipeline import save_json

observations, distances, output = map(Path, sys.argv[1:])
rows = json.loads(observations.read_text())
selected = {
    tuple(sorted((a["observation_key"], b["observation_key"]))): dict(
        video=a["video"], category=a["category"], interpolation=a["interpolation"]
    )
    for a, b in itertools.combinations(rows, 2)
    if a["video"] == b["video"]
    and a["rgb_frame"] != b["rgb_frame"]
    and a.get("interpolation")
    and a.get("interpolation") == b.get("interpolation")
    and a["category"] == b["category"]
}
selection = dict(
    rule="All different-frame pairs sharing video, interpolation and exact entity name; no negative identities assigned.",
    observations_sha256=file_hash(observations),
    pairs=[dict(left=k[0], right=k[1], **v) for k, v in sorted(selected.items())],
)
save_json(output.with_suffix(".selection.json"), selection)
pair_rows = defaultdict(list)
with distances.open(newline="", encoding="utf-8-sig") as stream:
    for row in csv.DictReader(stream):
        key = tuple(sorted((row["left"], row["right"])))
        if key in selected:
            pair_rows[key].append(row)
names = sorted({r["representation"] for group in pair_rows.values() for r in group})
common = {
    k: group
    for k, group in pair_rows.items()
    if len(group) == len(names)
    and len({r["representation"] for r in group}) == len(names)
    and all(r["status"] == "ready" for r in group)
}
summary = {}
for name in names:
    summary[name] = {}
    for metric in METRICS:
        values = [
            float(r[metric])
            for group in common.values()
            for r in group
            if r["representation"] == name and r[metric] != ""
        ]
        summary[name][metric] = dict(
            n=len(values), median=float(np.median(values)) if values else None
        )
save_json(
    output,
    dict(
        selection=selection,
        distances_sha256=file_hash(distances),
        common_pairs=len(common),
        results=summary,
        limitation="Short local interpolation consistency, dependent pairs and no within-category negatives. Not global identity discrimination or independent GT; never merge these proxies into reviewed identity labels.",
    ),
)
print(json.dumps(summary, indent=2))
