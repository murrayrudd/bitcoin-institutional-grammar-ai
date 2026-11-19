import copy
import datetime
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent
CASES = ['F01', 'F02', 'F03']

def read(name):
    return json.loads((BASE / name).read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(name, value):
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

packets = {c: read(c + '_packet.json') for c in CASES}
dossiers = {c: read(c + '_dossier.json') for c in CASES}
review = copy.deepcopy(read('review_work.json'))
manifest = read('input_manifest.json')
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
input_checks = []
for name, expected in manifest['files'].items():
    actual = sha(BASE / name)
    assert actual == expected, (name, expected, actual)
    input_checks.append({'file': name, 'sha256': actual, 'matches_supplied_manifest': True,
                         'content_review': 'hash verification only; substantive review used lossless per-case dossiers' if name == 'annotations.json' else 'read in full'})

# Add a precise retained metadata anchor to the chronology finding before first completion.
f = next(f for f in review['findings'] if f['finding_id'] == 'B011')
e = next(e for e in packets['F03']['entries'] if e['source_id'] == 'pr7819:metadata')
quote = '"updated_at": "2021-09-08T11:40:59+00:00"'
start = e['text'].index(quote)
f['source_evidence'].append({'source_id': e['source_id'], 'span': {'start': start, 'end': start + len(quote), 'quote': quote}})

ann_index = {a['annotation_id']: (c, a) for c in CASES for a in dossiers[c]['annotations']}
by_annotation = {aid: [] for aid in ann_index}
for f in review['findings']:
    assert f['diagnosis'] in {'criterion_ambiguity', 'execution_failure', 'defensible_alternative', 'unresolved'}
    assert f['effect'] in {'interpretation_changing', 'evidence_basis', 'convention_only', 'coverage_or_scope', 'unresolved'}
    entries = {e['source_id']: e for e in packets[f['episode_id']]['entries']}
    for ev in f['source_evidence']:
        s = ev['span']; text = entries[ev['source_id']]['text']
        assert s['quote'] and text[s['start']:s['end']] == s['quote'], (f['finding_id'], ev)
    for af in f['affected']:
        aid = af['annotation_id']; c, a = ann_index[aid]
        assert c == f['episode_id']
        assert set(af['unit_ids']) <= {u['unit_id'] for u in a['units']}
        for path in af['relation_ids']:
            m = re.fullmatch(r'relations\[(\d+)\]', path)
            assert m and int(m[1]) < len(a['relations']), (f['finding_id'], aid, path)
        assert not af['summary_paths'], 'Unexpected summary path requires explicit validation'
        by_annotation[aid].append((f, af))

review['coverage'] = []
ledger = {
    'reviewer': 'source_review_b',
    'completed_at_utc': now,
    'review_basis': 'Frozen packet texts and each annotation\'s assigned guide; source meaning was compared independently of consensus or agreement scores.',
    'status_convention': 'no_error_identified means no execution failure was identified by this review. Criterion ambiguities and defensible alternatives remain explicit and do not establish correctness. Relation endpoints listed in an execution finding are conservatively excluded from no_error_identified_ids even when the unit text itself is sound.',
    'source_entries': [],
    'annotations': [],
    'review_limits': review['review_limits'] + ['Supplemental documents and patches were read fully as context and evidence; they were not treated as exhaustive institutional-extraction targets contrary to packet selection_design.']
}
counts = Counter()
for c in CASES:
    packet = packets[c]; dossier = dossiers[c]
    entries = {e['source_id']: e for e in packet['entries']}
    pool = dossier['evidence_pool']
    for qid, ev in pool.items():
        s = ev['span']; text = entries[ev['source_id']]['text']
        assert text[s['start']:s['end']] == s['quote'], (c, qid)
    counts['packet_entries'] += len(entries)
    counts['unique_dossier_anchors'] += len(pool)
    focal = set(packet['selection_design']['focal_source_ids'])
    for e in packet['entries']:
        per_annotation = []
        for a in dossier['annotations']:
            screening = [x for x in a['entry_screening'] if x['source_id'] == e['source_id']]
            assert len(screening) == 1, (a['annotation_id'], e['source_id'])
            local_units = [u['unit_id'] for u in a['units'] if u['source_id'] == e['source_id']]
            per_annotation.append({'annotation_id': a['annotation_id'], 'screening_checked': True,
                                   'retained_unit_ids': local_units,
                                   'submitted_screening_unit_ids': screening[0]['unit_ids'],
                                   'submitted_disposition': screening[0]['disposition'],
                                   'omission_review': 'No mandatory substantive omission identified; B002 preserves the bounded nominal-backport candidate alternative.' if c == 'F02' and e['source_id'] == 'pr14441:body' else 'No material omission identified within the assigned extraction scope.'})
        ledger['source_entries'].append({'episode_id': c, 'source_id': e['source_id'], 'kind': e['kind'],
            'assigned_scope': 'focal_exhaustive' if e['source_id'] in focal else 'supplemental_context',
            'source_text_read_in_full': True, 'empty_text': not bool(e['text'].strip()),
            'character_count': len(e['text']), 'text_sha256': hashlib.sha256(e['text'].encode()).hexdigest(),
            'source_metadata_checked': True, 'annotations': per_annotation,
            'related_finding_ids': [f['finding_id'] for f in review['findings'] if f['episode_id'] == c and any(ev['source_id'] == e['source_id'] for ev in f['source_evidence'])]})
    for a in dossier['annotations']:
        aid = a['annotation_id']; unit_ids = [u['unit_id'] for u in a['units']]
        assert len(unit_ids) == len(set(unit_ids))
        assert a['packet_sha256'] == sha(BASE / (c + '_packet.json'))
        relevant = by_annotation[aid]
        execution_units = {u for f, af in relevant if f['diagnosis'] == 'execution_failure' for u in af['unit_ids']}
        execution_relations = {p for f, af in relevant if f['diagnosis'] == 'execution_failure' for p in af['relation_ids']}
        summary_paths = [f'episode_summary.{k}[{i}]' for k, values in a['episode_summary'].items() for i in range(len(values))]
        relation_ids = [f'relations[{i}]' for i in range(len(a['relations']))]
        row = {'annotation_id': aid, 'episode_id': c, 'assigned_guide': a['assigned_guide'],
               'checked_unit_ids': unit_ids, 'checked_relations': True, 'checked_summary': True,
               'checked_entry_ids': list(entries), 'no_error_identified_ids': [u for u in unit_ids if u not in execution_units],
               'limits': list(ledger['review_limits']) + list(packet['source_limits']),
               'checked_relation_ids': relation_ids, 'no_error_identified_relation_ids': [p for p in relation_ids if p not in execution_relations],
               'checked_summary_paths': summary_paths, 'no_error_identified_summary_paths': summary_paths,
               'all_recognition_disposition_documentary_application_authority_and_challenge_records_checked': True,
               'all_component_qualification_rationale_and_alternative_fields_checked': True,
               'finding_ids': [f['finding_id'] for f, af in relevant]}
        review['coverage'].append(row)
        unit_rows = []
        for u in a['units']:
            uid = u['unit_id']; ev = pool[u['span']['evidence_ref']]
            assert ev['source_id'] == u['source_id']
            if u.get('parent_unit_id'):
                assert u['parent_unit_id'] in unit_ids
            fs = [f for f, af in relevant if uid in af['unit_ids']]
            unit_rows.append({'unit_id': uid, 'source_id': u['source_id'], 'span': ev['span'],
                'record_role': u['record_role'], 'checked_fields': list(u),
                'checked_institution_fields': list(u['institution']),
                'checked_component_count': len(u['components']),
                'checked_support_event_counts': {k: len(u['institution'].get(k, [])) for k in ['recognition','documentary_support','application_evidence','authority_evidence','challenges']},
                'checked_disposition_count': len(u['disposition_events']),
                'status': 'execution_failure_identified' if uid in execution_units else 'no_error_identified_with_bounded_alternatives' if fs else 'no_error_identified',
                'finding_ids': [f['finding_id'] for f in fs]})
            counts['units'] += 1
            counts['no_error_identified_units'] += uid not in execution_units
            counts['components'] += len(u['components'])
            counts['disposition_records'] += len(u['disposition_events'])
            for k in ['recognition', 'documentary_support', 'application_evidence', 'authority_evidence', 'challenges']:
                counts[k + '_records'] += len(u['institution'].get(k, []))
        relation_rows = []
        for i, rel in enumerate(a['relations']):
            path = f'relations[{i}]'
            relation_rows.append({'path': path, 'checked_fields': list(rel),
                                 'submitted_relation': rel,
                                 'status': 'execution_failure_identified' if path in execution_relations else 'no_error_identified',
                                 'finding_ids': [f['finding_id'] for f, af in relevant if path in af['relation_ids']]})
        summary_rows = []
        for k, values in a['episode_summary'].items():
            for i, value in enumerate(values):
                row_s = {'path': f'episode_summary.{k}[{i}]', 'status': 'no_error_identified',
                         'checked_fields': list(value) if isinstance(value, dict) else ['text']}
                if isinstance(value, dict):
                    row_s['claim'] = value.get('claim', value.get('text'))
                    row_s['checked_claim_part_paths'] = [f'episode_summary.{k}[{i}].claim_parts[{j}]' for j in range(len(value.get('claim_parts', [])))]
                else:
                    row_s['text'] = value
                summary_rows.append(row_s)
                counts['summary_entries'] += 1
                if k in ['observed_outcomes', 'mechanisms']:
                    counts[k] += 1
                    counts['summary_claim_parts'] += len(value.get('claim_parts', []))
        ledger['annotations'].append({'annotation_id': aid, 'episode_id': c, 'assigned_guide': a['assigned_guide'],
                                     'units': unit_rows, 'relations': relation_rows, 'summary': summary_rows,
                                     'screening_entries_checked': [x['source_id'] for x in a['entry_screening']]})
        counts['annotations'] += 1
        counts['relations'] += len(a['relations'])
        counts['annotation_entry_reviews'] += len(a['entry_screening'])
    review['case_notes'][c]['status'] = 'complete: sources, units, components, qualifications, evidence, support events, relations, summary clauses, alternatives, and screening reviewed'

assert counts['annotations'] == 18 and counts['units'] == 587 and counts['relations'] == 327
assert counts['packet_entries'] == 83 and counts['annotation_entry_reviews'] == 498
assert counts['unique_dossier_anchors'] == 677
assert len(review['coverage']) == len(ann_index)
review['completed_at_utc'] = now
review['first_complete_status'] = 'First complete independent submission; no reconciliation or correction incorporated.'
review['coverage_convention'] = ledger['status_convention']
review['review_counts'] = dict(counts)
review['finding_counts'] = {'total': len(review['findings']), 'diagnosis': dict(Counter(f['diagnosis'] for f in review['findings'])), 'effect': dict(Counter(f['effect'] for f in review['findings']))}
ledger['counts'] = dict(counts)
ledger['finding_counts'] = review['finding_counts']

access = {
    'reviewer': 'source_review_b', 'completed_at_utc': now, 'assigned_directory': str(BASE),
    'research_and_write_scope': 'Only the assigned source_review_b directory; no parent directory, other review, external research source, aggregate metric, or condition-identity file was inspected.',
    'input_files': input_checks,
    'additional_read_inputs': [{'file': 'input_manifest.json', 'sha256': sha(BASE / 'input_manifest.json'), 'purpose': 'Input preservation checks'}],
    'original_annotations_access': 'annotations.json was hashed for preservation. Substantive inspection used all three complete lossless dossiers, as authorized by RUNTIME_NOTES.txt; no claim of a second complete reading of annotations.json is made.',
    'working_records_used': ['review_work.json', 'mechanical_checks.json', 'F01_qualifier_projection.jsonl', 'F02_qualifier_projection.jsonl', 'F03_qualifier_projection.jsonl', 'F01_tail_mapping.json', 'F02_tail_mapping.json', 'F03_tail_mapping.json'],
    'method': ['All three frozen packets, including supplemental patches and metadata, were read fully in bounded source batches.',
               'Every annotation was assessed under its own assigned guide; each retained unit and source entry was compared for meaning and coverage.',
               'All relations and every outcome/mechanism entry and claim part were read and compared with the sources; unanimity was not a correctness criterion.',
               'All institutional evidence, standing/profile fields, recognition/disposition records, documentary assessments, application claims, challenges, rationales, qualifications, alternatives, and remaining metadata fields were inspected.',
               'Exact duplicate field values were displayed once with their complete affected path mapping; all annotation occurrences remained included. Truncated substantive batches were re-read in smaller bounded groups.',
               'Coverage assembly enumerated every unit, source entry, relation, support record, and summary path; enumeration is recorded separately from the substantive judgment.',
               'An interruption occurred after source comparison and most narrative checks. The remaining metadata pass and ledger assembly resumed from preserved working records; completed substantive comparison was not replaced with a spot check.'],
    'boundary_checks': {'other_review_outputs_inspected': False, 'condition_identities_requested_or_inspected': False,
                        'agreement_statistics_inspected': False, 'external_sources_used': False,
                        'new_agents_or_model_calls_initiated': False, 'model_configuration_overridden': False,
                        'inputs_changed': False, 'existing_working_review_overwritten': False},
    'configuration': 'Inherited runtime configuration; no model, reasoning, or service-tier override requested. Runtime model identity is not independently verified by this record.',
    'version_masking_limit': 'Incomplete: assigned guide/schema differences remain visible. No condition identities were sought.',
    'judgment_limit': 'Revisable AI review rather than a reference truth set. Unresolved historical and criterion questions are preserved.',
    'coverage_counts': dict(counts), 'finding_counts': review['finding_counts'],
    'mechanical_validation': {'input_manifest_matches': True, 'all_dossier_source_anchors_exact': True,
                              'finding_source_anchors_exact': True, 'affected_annotation_and_unit_ids_valid': True,
                              'affected_relation_paths_valid': True, 'coverage_complete_for_all_submitted_units_and_packet_entries': True},
    'first_complete_preservation': {'review': 'first_complete_review.json', 'coverage': 'first_complete_coverage_ledger.json',
                                   'access': 'first_complete_access_record.json', 'manifest': 'first_complete_manifest.json',
                                   'later_corrections': 'None at first completion; original first-complete files are preserved separately.'}
}
for name, value in [('review.json', review), ('coverage_ledger.json', ledger), ('access_record.json', access)]:
    assert not (BASE / name).exists(), f'Refusing to overwrite existing completed output: {name}'
    save(name, value)
# Freeze first-complete bytes before allowing a later corrective revision.
frozen = {}
for name in ['review.json', 'coverage_ledger.json', 'access_record.json']:
    dest = BASE / ('first_complete_' + name)
    with dest.open('xb') as out:
        out.write((BASE / name).read_bytes())
    frozen[dest.name] = sha(dest)
save('first_complete_manifest.json', {'frozen_at_utc': now, 'files': frozen, 'inputs_unchanged': True,
                                     'finding_counts': review['finding_counts'], 'coverage_counts': dict(counts)})
print(json.dumps({'outputs': ['review.json', 'coverage_ledger.json', 'access_record.json', 'first_complete_review.json', 'first_complete_coverage_ledger.json', 'first_complete_access_record.json', 'first_complete_manifest.json'], 'counts': dict(counts), 'finding_counts': review['finding_counts']}, indent=2))
