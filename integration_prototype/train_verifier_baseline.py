"""Train the authorized diagnostic prototype; no claim of real-pair accuracy."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from registration_verifier import DiagnosticErrorVerifier


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def group_mean(values, rows):
    values = np.asarray(values)
    return float(np.mean([values[[r['group'] == g for r in rows]].mean()
                          for g in sorted({r['group'] for r in rows})]))


def predict(model, x):
    return np.maximum(0, np.column_stack([np.ones(len(x)), (x - model.mean) / model.scale]) @ model.weights)


def train(root, output):
    root, out = Path(root), Path(output)
    meta = json.loads((root / 'summary.json').read_text())
    for name, expected in meta['outputs'].items():
        if digest(root / name) != expected:
            raise ValueError('Dataset hash mismatch')
    rows = [json.loads(l) for l in (root / 'samples.jsonl').read_text().splitlines()]
    valid_groups = sorted(meta['groups']['validation'])
    calibration = set(valid_groups[::2])
    evaluation = set(valid_groups[1::2])
    sets = {s: [] for s in ('train', 'calibration', 'evaluation')}
    for row in rows:
        split = 'train' if row['split'] == 'train' else ('calibration' if row['group'] in calibration else 'evaluation')
        sets[split].append(row)
    arrays = {}
    with np.load(root / 'examples.npz', allow_pickle=False) as z:
        for split, rr in sets.items():
            arrays[split] = (np.array([z[r['id'] + '__features'] for r in rr]),
                             np.array([r['error'] for r in rr]))
    x, y = arrays['train']
    xcal, ycal = arrays['calibration']
    trials = []
    models = []
    for ridge in (0., .01, .1, 1., 10., 100.):
        model = DiagnosticErrorVerifier.fit(x, y, training_groups=[r['group'] for r in sets['train']],
             validation_groups=sorted(calibration), ridge=ridge,
             target_provenance=f'{digest(root / "summary.json")}:known-transforms-only')
        mae = group_mean(np.abs(predict(model, xcal) - ycal), sets['calibration'])
        models.append(model)
        trials.append(dict(ridge=ridge, group_macro_mae=mae))
    best = int(np.argmin([r['group_macro_mae'] for r in trials]))
    model = models[best]
    # Prototype definition of a small tolerated pose error. Learned geometric
    # band from the training fixtures only; not a real fusion-utility guarantee.
    small = [r['angle_deg'] <= 5 and r['translation_rms'] <= .03 for r in sets['train']]
    tolerance = float(np.quantile(y[small], .95))
    predicted = predict(model, xcal)
    labels = ycal <= tolerance
    unique = np.unique(predicted)
    thresholds = np.r_[-1e-12, (unique[:-1] + unique[1:]) / 2, unique[-1]]
    trials_threshold = []
    for threshold in thresholds:
        admitted = predicted <= threshold
        # Equal importance of acceptance and rejection, then macro by identity.
        scores = []
        for g in sorted(calibration):
            mask = np.array([r['group'] == g for r in sets['calibration']])
            pos, neg = mask & labels, mask & ~labels
            scores.append(.5 * (admitted[pos].mean() + (~admitted[neg]).mean()))
        trials_threshold.append(float(np.mean(scores)))
    threshold = float(thresholds[int(np.argmax(trials_threshold))])
    # Config class needs nonnegative values: a negative selected threshold means
    # no usable operating point, not permission to silently accept predictions.
    if threshold < 0:
        raise ValueError('No nonnegative operating point selected')
    out.mkdir(parents=True, exist_ok=False)
    model.save(out / 'model.json')
    reports, predictions = {}, []
    for split, rr in sets.items():
        xx, yy = arrays[split]
        pp = predict(model, xx)
        truth, accepted = yy <= tolerance, pp <= threshold
        counts = dict(true_accept=int(np.sum(accepted & truth)), false_accept=int(np.sum(accepted & ~truth)),
                      true_reject=int(np.sum(~accepted & ~truth)), false_reject=int(np.sum(~accepted & truth)))
        reports[split] = dict(samples=len(rr), groups=sorted({r['group'] for r in rr}),
            mae=float(np.abs(pp - yy).mean()), group_macro_mae=group_mean(np.abs(pp - yy), rr),
            constant_training_median_mae=float(np.abs(np.median(y) - yy).mean()),
            confusion=counts, accepted=int(accepted.sum()))
        for r, pred, label in zip(rr, pp, truth):
            predictions.append(dict(id=r['id'], group=r['group'], split=split,
                                    target=r['error'], predicted=float(pred), small_error=bool(label)))
    (out / 'predictions.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in predictions))
    report = dict(schema='point3-trained-diagnostic-prototype-v1', backend='diagnostic-error',
        dataset_summary_sha256=digest(root / 'summary.json'), model_sha256=digest(out / 'model.json'),
        model_id=model.model_id, selected_ridge=trials[best]['ridge'], ridge_trials=trials,
        maximum_predicted_error=threshold, target_error_tolerance=tolerance,
        tolerance_provenance='training 95th percentile of known 0/5-degree, 0/.03-RMS perturbations',
        threshold_provenance='calibration macro-identity balanced accuracy; equal error costs',
        evaluation_used_for_selection=False, metrics=reports,
        limitations=['linear diagnostic baseline, not the planned direct-pair neural model',
                     'simulated targets only; calibration is not physical fusion certification',
                     'two evaluation identities within one development video, no generalization claim'])
    (out / 'report.json').write_text(json.dumps(report, indent=2, allow_nan=False))
    print(json.dumps(report, indent=2))
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', required=True)
    p.add_argument('--out', required=True)
    a = p.parse_args()
    train(a.data, a.out)
