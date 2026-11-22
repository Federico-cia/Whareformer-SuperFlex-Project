"""Minimal integration contract. It does not select/train a correction model."""
import numpy as np


def apply_correction(baseline_logits,geometry_delta,geometry_available,weight=0.0):
    baseline=np.asarray(baseline_logits)
    delta=np.asarray(geometry_delta)
    available=np.asarray(geometry_available,dtype=bool)
    if baseline.ndim!=1 or delta.shape!=baseline.shape or available.shape!=baseline.shape:
        raise ValueError('Expected one score per class: class 0=new track, classes 1..T=candidates')
    if not np.isfinite(baseline).all() or not np.isfinite(weight): raise ValueError('Nonfinite logits/weight')
    if weight==0: return baseline.copy()
    if not np.isfinite(delta[available]).all(): raise ValueError('Nonfinite available correction')
    result=baseline.copy();result[available]+=weight*delta[available]
    return result
