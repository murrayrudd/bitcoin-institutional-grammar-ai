"""Supplementary descriptive nominal alpha, added during coding at user request.

Not a prespecified acceptance test. Alignment and selection losses remain separate.
No confidence intervals or population inference from three clustered episodes.
"""
from pathlib import Path
from collections import Counter
import json
from metrics import FIELDS, value

R = Path(__file__).resolve().parents[1]

def read(p):
    return json.loads(p.read_text())

def nominal_alpha(rows):
    rows = [r for r in rows if len(r) >= 2]
    n = sum(map(len, rows))
    if n < 2:
        return {"alpha": None, "reason": "insufficient paired labels", "units": len(rows)}
    counts = Counter(v for r in rows for v in r)
    observed = sum(sum(a != b for a in r for b in r) / (len(r) - 1) for r in rows) / n
    expected = (n*n - sum(c*c for c in counts.values())) / (n*(n-1))
    pair_total = sum(len(r)*(len(r)-1) for r in rows)
    pair_disagree = sum(sum(a != b for a in r for b in r) for r in rows)
    return {
        "alpha": 1-observed/expected if expected else None,
        "reason": None if expected else "undefined: no category variation",
        "units": len(rows), "labels": n, "category_counts": dict(counts),
        "observed_disagreement": observed, "expected_disagreement": expected,
        "pairwise_agreement": 1-pair_disagree/pair_total,
        "all_three_agreement_count": sum(len(set(r)) == 1 for r in rows),
        "all_three_agreement_fraction": sum(len(set(r)) == 1 for r in rows)/len(rows)
    }

def main():
    assert (R/'analysis/all_coding_frozen.json').exists()
    masks = read(R/'analysis/mask_key.json')
    runs = {rid: read(R/'runs'/rid/'annotation.final.json') for rid in masks}
    units = {masks[rid]: {u['unit_id']: u for u in a['units']} for rid,a in runs.items()}
    groups = {g['group_id']:g for g in read(R/'reviews/alignment/alignment.json')['groups']}
    primary = read(R/'analysis/overlap_metrics.json')
    result = {
        "status": "supplementary analysis added during execution following the author's question about human intercoder reliability",
        "acceptance_threshold": None,
        "limitations": [
            "Conditional on the frozen one-to-one semantic alignment; omitted and split propositions are not coded as missing labels.",
            "Nominal metric for each categorical field; no standing-profile-to-scalar crosswalk.",
            "Three source episodes, repeated and dependent propositions: descriptive coefficients only, no confidence intervals or population reliability claim.",
            "Fresh agents per episode; run positions are not persistent individual coders across episodes.",
            "No category variation gives undefined alpha even when raw agreement is perfect.",
            "The coefficients measure consistency, not source accuracy or negotiated agreement."
        ],
        "reference": "Hayes and Krippendorff (2007), DOI 10.1080/19312450709336664",
        "conditions": []
    }
    for version in ['v03','v04']:
        for subset in ['within_condition_matches','common_all_six_matches']:
            pooled = {f:[] for f in FIELDS}
            case_results = []
            for case in primary['cases']:
                condition = next(c for c in case['conditions'] if c['condition']==version)
                aliases = [masks[rid] for rid in condition['runs']]
                gids = condition['semantic_group_ids'] if subset=='within_condition_matches' else case['common_all_six_group_ids']
                data = {f:[] for f in FIELDS}
                for gid in gids:
                    us = [units[a][groups[gid]['members'][a][0]] for a in aliases]
                    for f in FIELDS:
                        labels = [json.dumps(value(u,f),sort_keys=True) for u in us]
                        data[f].append(labels)
                        pooled[f].append(labels)
                case_results.append({'episode_id':case['episode_id'],'group_ids':gids,'fields':{f:nominal_alpha(data[f]) for f in FIELDS}})
            result['conditions'].append({'condition':version,'subset':subset,'cases':case_results,'pooled_fields':{f:nominal_alpha(pooled[f]) for f in FIELDS}})
    p=R/'analysis/supplementary_alpha.json'
    p.write_text(json.dumps(result,indent=2)+'\n')
    print(str(p))

if __name__=='__main__':
    assert nominal_alpha([['a','a'],['b','b']])['alpha'] == 1
    assert abs(nominal_alpha([['a','b'],['a','b']])['alpha'] + 0.5) < 1e-12
    assert nominal_alpha([['a','a','a']])['alpha'] is None
    main()
