"""Prepare a cautious operating policy using calibration identities only.

Risk budget is an explicit prototype engineering choice, not a certified bound.
The original model and balanced policy remain unchanged.
"""
import argparse
import json
from pathlib import Path
import shutil
import numpy as np


def select(source, output, risk_budget):
    root, out = Path(source), Path(output)
    report = json.loads((root / 'report.json').read_text())
    rows = [json.loads(l) for l in (root / 'predictions.jsonl').read_text().splitlines()]
    cal = [r for r in rows if r['split'] == 'calibration']
    groups = sorted({r['group'] for r in cal})
    thresholds = sorted({r['predicted'] for r in cal})
    feasible = []
    for threshold in thresholds:
        rates = []
        for group in groups:
            pos = [r for r in cal if r['group'] == group and r['small_error']]
            neg = [r for r in cal if r['group'] == group and not r['small_error']]
            if not pos or not neg:
                raise ValueError('Both target classes required per calibration identity')
            rates.append((sum(r['predicted'] <= threshold for r in neg) / len(neg),
                          sum(r['predicted'] <= threshold for r in pos) / len(pos)))
        if max(r[0] for r in rates) <= risk_budget:
            feasible.append((float(np.mean([r[1] for r in rates])), threshold, rates))
    if not feasible:
        raise ValueError('No operating point satisfies the requested empirical calibration budget')
    _, threshold, rates = max(feasible, key=lambda r: (r[0], -r[1]))
    out.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(root / 'model.json', out / 'model.json')
    shutil.copyfile(root / 'predictions.jsonl', out / 'predictions.jsonl')
    report['previous_balanced_threshold'] = report['maximum_predicted_error']
    report['maximum_predicted_error'] = threshold
    report['operating_policy'] = 'conservative-calibration-v1'
    report['empirical_risk_budget_per_calibration_identity'] = risk_budget
    report['threshold_provenance'] = 'maximize macro true-accept rate subject to per-identity calibration false-accept budget'
    report['risk_limit_is_not_a_statistical_guarantee'] = True
    for split, metrics in report['metrics'].items():
        rr = [r for r in rows if r['split'] == split]
        counts = dict(true_accept=0, false_accept=0, true_reject=0, false_reject=0)
        for r in rr:
            accepted, truth = r['predicted'] <= threshold, r['small_error']
            counts[('true_' if accepted == truth else 'false_') + ('accept' if accepted else 'reject')] += 1
        metrics['confusion'] = counts
        metrics['accepted'] = counts['true_accept'] + counts['false_accept']
    (out / 'report.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(dict(threshold=threshold, calibration_rates=rates,
                         evaluation=report['metrics']['evaluation']), indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--risk-budget', type=float, required=True)
    a = p.parse_args()
    if not 0 < a.risk_budget < 1:
        p.error('Risk budget must be between zero and one')
    select(a.model, a.out, a.risk_budget)
