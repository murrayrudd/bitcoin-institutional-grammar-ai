"""Reproduce retained computations in a temporary copy; no model or network calls."""
from pathlib import Path
import argparse, hashlib, importlib.metadata, json, os, shutil, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parents[1]

def read(p):
    return json.loads(p.read_text())

def normalized(value, key=None):
    # This historical diagnostic list is built from a set; its ordering is immaterial.
    if isinstance(value, dict):
        return {k: normalized(v, k) for k, v in value.items()}
    if isinstance(value, list):
        items = [normalized(v) for v in value]
        return sorted(items) if key == 'changed_existing_unit_ids' else items
    return value

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', type=Path, help='Write a verification record outside the repository.')
    args = parser.parse_args()
    if args.record and args.record.resolve().is_relative_to(ROOT):
        parser.error('--record must be outside the distributed repository')
    records = []
    compared = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')

    def run(base, command):
        proc = subprocess.run([sys.executable, *command], cwd=base, env=env,
                              text=True, capture_output=True)
        records.append({'directory': base.relative_to(work).as_posix() if base.is_relative_to(work) else '.',
                        'command': ['python', *command], 'returncode': proc.returncode,
                        'output_sha256': hashlib.sha256(proc.stdout.encode()).hexdigest()})
        if proc.returncode:
            raise RuntimeError(' '.join(command) + '\n' + proc.stdout[-6000:] + '\n' + proc.stderr[-6000:])
        print('PASS ' + ' '.join(command), flush=True)

    def compare(relative):
        saved, rebuilt = ROOT / relative, work / relative
        if saved.suffix == '.json':
            equal = normalized(read(saved)) == normalized(read(rebuilt))
        else:
            equal = saved.read_bytes() == rebuilt.read_bytes()
        if not equal:
            raise AssertionError('Regenerated output differs: ' + relative)
        compared.append(relative)

    with tempfile.TemporaryDirectory(prefix='bitcoin-ig2-') as td:
        work = Path(td) / 'repo'
        run(ROOT, ['scripts/verify_package.py'])
        shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns('.git', '.venv', '__pycache__'))

        p = work / 'specification'
        run(p, ['tools/test_specification.py'])
        run(p, ['tools/test_release_correction.py'])
        for f in ['regression_results.json', 'compatibility_results.json']:
            compare('specification/release/' + f)

        p = work / 'studies/baseline'
        for f in ['assemble_sources.py', 'build_analysis.py', 'build_focal_ig.py',
                  'build_diagnostics.py', 'key_gate_experiment.py', 'validate_analysis.py']:
            run(p, ['tools/' + f])
        for f in ['claim_ledger.json', 'claim_index.csv', 'focal_ig_records.json', 'case_mechanisms.json',
                  'narrative_comparison.json', 'evidence_matrix.json', 'case_links.json',
                  'source_integrity.json', 'key_gate_experiment.json', 'timing_checks.json']:
            compare('studies/baseline/analysis/' + f)

        p = work / 'studies/independent-coding'
        for command in [['tools/verify_package.py'], ['tools/verify_final_evaluation.py'],
                        ['tools/evaluate.py', 'verify'], ['tools/metrics.py'],
                        ['tools/supplementary_alpha.py'], ['tools/verify_alpha.py'],
                        ['tools/run_descriptives.py']]:
            run(p, command)
        for f in ['overlap_metrics.json', 'supplementary_alpha.json', 'run_descriptives.json']:
            compare('studies/independent-coding/analysis/' + f)

        masks = read(p / 'analysis/mask_key.json')
        units = {masks[rid]: {u['unit_id']: u for u in read(p / 'runs' / rid / 'annotation.final.json')['units']}
                 for rid in masks}
        groups = {g['group_id']: g for g in read(p / 'reviews/alignment/alignment.json')['groups']}
        metrics = read(p / 'analysis/overlap_metrics.json')
        def value(u, field):
            if field == 'institutional_type': return u['institution']['type']
            if field == 'dispute_present': return u['institution']['dispute_present']
            return u[field]
        totals = {'v03': 0, 'v04': 0}
        denominator = 0
        for case in metrics['cases']:
            denominator += len(case['common_all_six_group_ids'])
            for condition in case['conditions']:
                for gid in case['common_all_six_group_ids']:
                    us = [units[masks[rid]][groups[gid]['members'][masks[rid]][0]] for rid in condition['runs']]
                    totals[condition['condition']] += all(len({json.dumps(value(u, field), sort_keys=True) for u in us}) == 1
                                                         for field in metrics['fields'])
        composite = {'denominator': denominator, 'field_count': len(metrics['fields']),
                     'all_three_all_six_fields': totals}
        assert composite == read(p / 'analysis/common_composite_agreement.json'), composite

        p = work / 'studies/collaborative-review'
        run(p, ['tools/verify_reconciliation.py'])
        run(p, ['tools/build_dataset.py'])
        for directory in ['dataset/adjusted_annotations', 'dataset/reference_only_v03', 'dataset/packets']:
            for f in (ROOT / 'studies/collaborative-review' / directory).glob('*.json'):
                compare(f.relative_to(ROOT).as_posix())
        compare('studies/collaborative-review/analysis/metadata_adapter.json')
        # The builder enumerates directories for its final metadata-only changes.
        # Keep coding changes in sequence; compare final metadata records without
        # their traversal-dependent sequence IDs. Distributed IDs remain unchanged.
        log_path = 'studies/collaborative-review/analysis/change_log.json'
        old, new = read(ROOT / log_path), read(work / log_path)
        assert [x for x in old if x['kind'] == 'coding'] == [x for x in new if x['kind'] == 'coding']
        def metadata_records(rows):
            return sorted(json.dumps({k: v for k, v in x.items() if k != 'change_id'}, sort_keys=True)
                          for x in rows if x['kind'] != 'coding')
        assert metadata_records(old) == metadata_records(new)
        compared.append(log_path)
        rebuilt_checks = read(p / 'analysis/checker_results.json')
        assert len(rebuilt_checks) == 9 and all(x['check']['status'] == 'pass' and not x['check']['errors']
                                              for x in rebuilt_checks)

        p = work / 'studies/source-review'
        run(p, ['tools/verify_review.py'])
        p = work / 'studies/overlap'
        run(p, ['tools/compare_annotations.py'])
        compare('studies/overlap/analysis/overlap_metrics.json')

        p = work / 'studies/core-knots'
        run(p, ['build_analysis.py'])
        for f in (ROOT / 'studies/core-knots/analysis').glob('*.json'):
            if f.name not in ['verification_results.json', 'document_quality_check.json']:
                compare(f.relative_to(ROOT).as_posix())
        run(p, ['verify_model.py'])

        p = work / 'studies/followup'
        run(p, ['build_ledger.py'])
        compare('studies/followup/claim_ledger.json')

        result = {'status': 'pass', 'package_version': '1.0.0', 'python_version': sys.version.split()[0],
                  'jsonschema_version': importlib.metadata.version('jsonschema'),
                  'commands_passed': len(records), 'outputs_compared': len(compared),
                  'common_proposition_agreement': composite, 'commands': records,
                  'compared_outputs': compared,
                  'scope': 'Frozen-file integrity and deterministic reproduction; no new AI coding or full-parent-corpus selection reconstruction.'}
        if args.record:
            args.record.resolve().parent.mkdir(parents=True, exist_ok=True)
            args.record.write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps({k: v for k, v in result.items() if k not in ['commands', 'compared_outputs']}, indent=2))

if __name__ == '__main__':
    main()
