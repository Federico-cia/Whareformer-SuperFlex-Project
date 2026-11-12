# Whareformer – Tracking and Geometry Integration

## Objective
Connect Whareformer object tracks to the 3D point clouds produced by the SuperFlex geometry pipeline, enabling future multi-view point-cloud accumulation and reconstruction.

## Completed work
1. Ran pretrained Whareformer inference on EPIC-KITCHENS video `P01_01`.
2. Implemented `build_tracks_by_id.py` to associate predictions with original observation IDs.
3. Implemented `link_compare200_tracks.py` to link Whareformer observations to the DA/MoGE point clouds in the compare200 dataset.
4. Visually inspected track 9 (red pan), a promising candidate for multi-view reconstruction.

## Verified results – P01_01
- 110,590 / 110,590 tracking observations matched to original annotations.
- 52 predicted tracks.
- 71 / 73 compare200 geometry observations linked successfully.
- 18 tracks with available geometry; 9 with multiple observations.
- Track 9: 18 observations of a pan, visually consistent with the same manipulated object.

## Reproduction
Run these scripts from the root of the original Whareformer repository, with the pretrained model, extracted EPIC features and compare200 package available:

```bash
python build_tracks_by_id.py --video P01_01
python link_compare200_tracks.py --video P01_01 --compare-dir ../compare200
```

## Next steps
- Validate geometric consistency across observations.
- Register and progressively accumulate DA/MoGE point clouds belonging to the same object.
- Feed accumulated clouds into SuperFlex and compare reconstruction quality against single-observation baselines.

## Limitations
Track identities are predictions, not ground truth. The 18 selected observations are temporally sparse, and their point clouds are not yet aligned. No reconstruction improvement has been demonstrated yet.
