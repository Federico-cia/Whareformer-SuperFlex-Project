# Shape tools

Utilities for camera-frame point clouds and paired comparison of saved DA/MoGE geometry.
The authors' networks, weights and the Whareformer matcher are not included.

```bash
pip install -e ./SuperFlex
shape-tools compare observations.json --root /path/to/geometry --output distances.csv
shape-tools evaluate distances.csv identity_review.csv --output evaluation.json
python -m unittest discover -s SuperFlex/tests
```

`compare` computes D2 and covariance-spectrum distances. Add `--registration` for
24-start, bidirectional ICP/Chamfer on 512 points. Input geometry is loaded once;
comparisons use 1024 centered, RMS-normalized points, 16384 D2 samples and seed
20261109. Absolute size and position are discarded.

The manifest is a JSON list. Each observation contains `observation_key`, `video`,
`rgb_frame`, `category`, and `representations`. Each representation contains `status`
(`ready` or `unavailable`), a `.npz`/`.ply` `path` relative to `--root`, and optionally
`sha256`. NPZ clouds contain `camera_points[N,3]`. Only different frames in the same
video are paired. Missing predictions remain explicit; outputs are not overwritten.

`evaluate` accepts a CSV with `observation_key`, `video`, `rgb_frame`, `category`,
`physical_identity`, `identity_status`, and `evidence`. Only `visually_verified`
identities with evidence are used. Representations are compared on common successful
pairs, grouped by video and category. Dependent pairs are not independent samples.

`shape_tools.geometry` exposes `backproject`, `paired_clouds`, and
`prepare_superflex_input`. Camera axes: X right, Y down, Z forward. Backprojection
requires perspective Z depth and intrinsics at the same resolution. SuperFlex input
uses 4096 samples and mean/max-extent normalization, distinct from comparison RMS
normalization. Neither normalization corrects orientation sensitivity.
