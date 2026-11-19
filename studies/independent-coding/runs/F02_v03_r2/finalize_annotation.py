import copy
import datetime
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def read(name):
    return json.loads((ROOT / name).read_text())

def write(name, obj):
    (ROOT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def sha(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()

packet = read('packet.json')
first = read('annotation.first_complete.json')
annotation = read('annotation.json')
first_checks = read('checks.first.json')
assert first == annotation, 'The first-complete snapshot must precede all repairs.'
assert first_checks['status'] == 'pass'
entries = {e['source_id']: e for e in packet['entries']}
unitmap = {u['unit_id']: u for u in annotation['units']}

def evidence(source_id, quote=None):
    text = entries[source_id]['text']
    if quote is None:
        quote = text
    start = text.index(quote)
    return {'source_id': source_id, 'span': {'start': start, 'end': start + len(quote), 'quote': quote}}

def component(uid, symbol):
    return next(c for c in unitmap[uid]['components'] if c['symbol'] == symbol)

repairs = []
cex = component('S04', 'Cex')
before = {k: cex[k] for k in ['basis', 'occurrence_role', 'inference_note']}
cex['basis'] = 'context_inferred'
cex['occurrence_role'] = 'semantic_inference'
cex['inference_note'] = (
    'Maybe introduces optional proposed wording, but the grammatical link making this draft an execution specification of document is elliptical. '
    'Its Cex role is therefore inferred rather than explicit. The source wording and all its material content remain explicit: '
    'the accounts-mode condition, empty string label, unlabeled-transactions result, error without the setting, and usefulness/confusion rationale. '
    'These qualify the suggested documentation content; they are not conditions on whether contributors may document it. '
    'Representing the same draft as an inferred object-content property would preserve the recommendation if its tentativeness and all technical qualifications remain intact.')
repairs.append({
    'change_id': 'R01', 'stage': 'source_self_review', 'unit_id': 'S04',
    'paths': ['components[symbol=Cex].basis', 'components[symbol=Cex].occurrence_role', 'components[symbol=Cex].inference_note'],
    'before': before,
    'after': {k: cex[k] for k in before},
    'category': 'epistemic_labeling_correction',
    'meaning_changed': False, 'evidence_status_changed': True, 'institutional_conclusion_changed': False,
    'rationale': 'The words of the draft are present, but the execution-constraint role under the documentation request is inferred through the elliptical Maybe introduction. This corrects evidence status without changing the recommendation, its qualifications, its scope, or its standing.',
    'evidence': [evidence('pr14441:review_comments:3')]
})

actor = component('S02', 'A')
old_note = actor['inference_note']
actor['inference_note'] = (
    'The explicit I in I\'d maybe belongs to ryanofsky\'s hypothetical phrasing; it is not an explicit name for the actor in the selected recommendation-to-the-contributor parse. '
    'The pragmatic actor is the person updating this PR. jnewbery\'s later attribution of the update to ryanofsky\'s changes supports that addressee only as a contextual inference. '
    'No occupational status, actual commitment by ryanofsky to perform the edit, or duty to comply is inferred. '
    'The literal reviewer-as-hypothetical-actor alternative remains in alternative_interpretation.')
repairs.append({
    'change_id': 'R02', 'stage': 'source_self_review', 'unit_id': 'S02',
    'paths': ['components[symbol=A].inference_note'],
    'before': {'inference_note': old_note}, 'after': {'inference_note': actor['inference_note']},
    'category': 'explanation_clarification',
    'meaning_changed': False, 'evidence_status_changed': False, 'institutional_conclusion_changed': False,
    'rationale': 'Explicitly distinguish the literal first-person hypothetical subject from the inferred addressee of the editing recommendation. The existing inferred actor label and retained alternative are unchanged.',
    'evidence': [evidence('pr14441:review_comments:1', "I'd maybe change it to:"), evidence('pr14441:comments:0')]
})

write('annotation.json', annotation)
write('annotation.final.json', annotation)
check = subprocess.run([sys.executable, str(ROOT / 'tools/check_annotation.py'), str(ROOT / 'packet.json'), str(ROOT / 'annotation.final.json')], capture_output=True, text=True)
(ROOT / 'checks.json').write_text(check.stdout)
if check.stderr:
    (ROOT / 'checks.stderr.txt').write_text(check.stderr)
assert check.returncode == 0, check.stdout + check.stderr
final_checks = read('checks.json')

flag_resolutions = []
for index, flag in enumerate(first_checks['review_flags']):
    uid, symbol = flag['unit_id'], flag['symbol']
    current = component(uid, symbol)
    status = 'retained'
    if flag['kind'] == 'outside_unit' and symbol == 'A':
        rationale = (
            'Retained as an explicitly labeled semantic inference. The source suggestion does not name its addressee; the later author report attributes the PR update to the reviewer. '
            'This supports the likely updater/addressee while leaving exact addressing and any institutional duty unestablished. '
            'The outside-unit span is evidence for actor inference, not a reason to enlarge the unit.')
        if uid == 'S02':
            status = 'corrected'
            rationale += ' R02 clarifies that the literal I is the reviewer\'s hypothetical subject, not an explicit actor in the selected pragmatic request.'
        cited = copy.deepcopy(current['evidence'])
    elif flag['kind'] == 'outside_unit' and symbol == 'Bdir':
        rationale = (
            'Retained. Drop has an omitted object, and the immediately preceding sentence supplies the new check for "*" here. '
            'Its Bdir role is context_inferred with context_reference, not explicit merely because those words occur. '
            'The unit remains the minimal removal request and preserves its purpose and unless caveat.')
        cited = [evidence('pr14441:review_comments:2')]
    elif flag['kind'] == 'pragmatic_explicit_argument' and uid == 'S02':
        rationale = (
            'Retained. In change it to, it is the grammatical object of the explicit verb change in both the literal hypothetical and pragmatic recommendation. '
            'Only its reference to This paragraph requires context. Unlike the desired spelling in S01, no subject or predicate complement is promoted to Bdir.')
        cited = [evidence('pr14441:review_comments:1', "This paragraph doesn't really make sense when both behaviors are present in the same release. I'd maybe change it to:")]
    elif flag['kind'] == 'pragmatic_explicit_argument' and uid == 'S04':
        rationale = (
            'Retained. The empty string change is directly the object of document. Its role survives the inferred recommendation force, so explicit/local Bdir is appropriate. '
            'The elliptical role of the following proposed draft is a separate issue corrected in R01.')
        cited = [evidence('pr14441:review_comments:3', "I think it'd be good to document the empty string change.")]
    else:
        raise AssertionError('Unreviewed checker flag')
    flag_resolutions.append({'flag_id': f'F{index + 1:02}', 'first_check_index': index,
                             'unit_id': uid, 'kind': flag['kind'], 'symbol': symbol,
                             'status': status, 'rationale': rationale, 'evidence': cited,
                             'present_in_final_checker': any(x['kind'] == flag['kind'] and x['unit_id'] == uid and x['symbol'] == symbol for x in final_checks['review_flags'])})
assert len(flag_resolutions) == len(first_checks['review_flags']) == len(final_checks['review_flags'])

screening_reviews = []
for sc in annotation['entry_screening']:
    entry = entries[sc['source_id']]
    focal = sc['source_id'] in packet['selection_design']['focal_source_ids']
    text = entry['text']
    if not text:
        anchors = []
    elif entry['kind'] == 'patch':
        # The complete source was reviewed. A compact locating anchor suffices for this screening ledger.
        anchors = [evidence(sc['source_id'], text.split('\n', 1)[0])]
    elif entry['kind'] == 'record_metadata':
        anchors = [evidence(sc['source_id'], '"number": 14441'), evidence(sc['source_id'], '"merged": true')]
    else:
        anchors = [evidence(sc['source_id'])]
    screening_reviews.append({'source_id': sc['source_id'], 'status': 'retained',
                              'review_scope': 'exhaustive_focal' if focal else 'contextual_supplement',
                              'disposition': sc['disposition'], 'unit_ids': sc['unit_ids'],
                              'rationale': sc['reason'], 'evidence': anchors,
                              'complete_supplied_text_reviewed': True})

unit_reviews = []
for u in annotation['units']:
    notes = []
    if u['unit_id'] == 'S01':
        notes = ['The literal desired-state spelling is retained as a pragmatic correction request. Correct, its target, and the requested spelling-property role are all inferred; Should remains an explicit lexical deontic with recommendation force.',
                 'The complete identifier listtransactions and the explicit s qualification are preserved. The unseen original typo is not reconstructed.']
    elif u['unit_id'] == 'S02':
        notes = ['One edit proposition includes the offered replacement wording; the preceding criticism is its rationale rather than a second request.',
                 'Both -deprecatedrpc=accounts branches, all label/account/dummy names, outgoing versus incoming transactions, and the accounts-versus-labels explanation remain in the Cex text.',
                 'R02 makes the inferred actor versus literal I distinction explicit. Change and its object it retain their source roles.']
    elif u['unit_id'] == 'S03':
        notes = ['Drop is explicitly supplied. Its omitted object is resolved to the immediately preceding new check for "*" here with inferred role and outside-unit evidence.',
                 'For clarity is Cex; unless I\'m missing something is retained as defeasibility/activation qualification with the alternative epistemic reading stated. Maybe is not mislabeled as a duty modal.',
                 'The author\'s No agrees with the recommendation by answering the caveat; it is not a later rejection. Specific removal is reported, not independently reconstructed from final code.']
    elif u['unit_id'] == 'S04':
        notes = ['Document and its complete informational object remain explicit even under pragmatic recommendation force.',
                 'R01 corrects the inferred execution-specification role of the Maybe-introduced draft. The technical branches, empty-string label, output population, error behavior, and rationale are unchanged.',
                 'Technical possible and error statements are not converted into permission or sanction, and the draft is proposed wording rather than a repeated quotation.']
    elif u['unit_id'] in ['C09', 'C10']:
        notes = ['The utterance is retained as a context act. Its exact response target remains unresolved; no arbitrary proposition-specific endorsement or implementation event is attached.']
    else:
        notes = [u['institution']['rationale']]
    unit_reviews.append({'unit_id': u['unit_id'], 'source_id': u['source_id'],
                         'status': 'corrected' if u['unit_id'] in ['S02', 'S04'] else ('unresolved' if u['unit_id'] in ['C09', 'C10'] else 'retained'),
                         'evidence': [{'source_id': u['source_id'], 'span': u['span']}],
                         'notes': notes,
                         'components_reviewed': [{'symbol': c['symbol'], 'basis': c['basis'], 'occurrence_role': c['occurrence_role'], 'evidence': c['evidence'], 'rationale': c['inference_note'] or 'The stated component retains its literal role and local exact anchor.'} for c in u['components']],
                         'level_review': {'statement_target_level': u['statement_target_level'], 'observed_action_level': u['observed_action_level'], 'status': 'retained', 'rationale': u['level_rationale']}})

event_reviews = []
for u in annotation['units']:
    for field, events in [('institution.recognition', u['institution']['recognition']), ('disposition_events', u['disposition_events'])]:
        for i, e in enumerate(events):
            event_reviews.append({'unit_id': u['unit_id'], 'path': f'{field}[{i}]',
                                  'status': 'retained', 'kind': e['kind'], 'target': e['target'], 'basis': e['basis'],
                                  'rationale': e['rationale'], 'evidence': e['evidence']})

review = {
    'run_id': 'F02_v03_r2', 'episode_id': 'F02', 'packet_sha256': sha('packet.json'),
    'review_type': 'one_complete_source_based_self_review_after_first_checker',
    'review_round_count': 1, 'completed': True,
    'scope': {'focal_entries': 16, 'all_entries_screened': 22, 'units_reviewed': 15,
              'statement_units_reviewed': 4, 'components_reviewed': sum(len(u['components']) for u in annotation['units']),
              'relations_reviewed': len(annotation['relations']), 'events_reviewed': len(event_reviews),
              'observed_outcomes_reviewed': len(annotation['episode_summary']['observed_outcomes']),
              'mechanisms_reviewed': len(annotation['episode_summary']['mechanisms'])},
    'first_complete_freeze': {'file': 'annotation.first_complete.json', 'sha256': sha('annotation.first_complete.json'), 'preserved_before_checks_or_self_review': True},
    'checker_review': {'first_check': 'checks.first.json', 'final_check': 'checks.json',
                       'first_status': first_checks['status'], 'final_status': final_checks['status'],
                       'mechanical_errors': [], 'review_flags_resolved': len(flag_resolutions),
                       'semantic_validity': 'The mechanical pass does not certify interpretation. The following source decisions remain revisable.'},
    'flag_resolutions': flag_resolutions,
    'source_findings': [
        {'finding_id': 'R01', 'status': 'corrected', 'category': 'epistemic_labeling', 'unit_ids': ['S04'],
         'claim': 'The optional draft\'s execution-specification role is inferred from Maybe rather than explicitly supplied as a grammatical constraint. Role evidence was relabeled without changing the institutional conclusion.',
         'evidence': [evidence('pr14441:review_comments:3')]},
        {'finding_id': 'R02', 'status': 'corrected', 'category': 'explanation_clarification', 'unit_ids': ['S02'],
         'claim': 'The actor rationale now explicitly distinguishes the literal hypothetical first-person subject from the inferred addressee of the recommendation.',
         'evidence': [evidence('pr14441:review_comments:1', "I'd maybe change it to:"), evidence('pr14441:comments:0')]},
        {'finding_id': 'U01', 'status': 'unresolved', 'category': 'reply_target', 'unit_ids': ['C09', 'C10'],
         'claim': 'Both and fixed remain ambiguous because more than one supplied release-note suggestion could be a target, and reliable threading is absent.',
         'evidence': [evidence('pr14441:review_comments:4'), evidence('pr14441:review_comments:5'), evidence('pr14441:review_comments:0'), evidence('pr14441:review_comments:1'), evidence('pr14441:review_comments:3')]}
    ],
    'screening_reviews': screening_reviews,
    'unit_reviews': unit_reviews,
    'authority_recognition_application_review': {
        'status': 'retained', 'unit_ids': ['S01', 'S02', 'S03', 'S04'],
        'rationale': 'All four are one-off operational edit recommendations with plausible institutional relevance but undetermined type and text-only standing. The packet supplies no rule authorization, enforcement linkage, or recognition of an expectation as such. Broad update reports and revision-specific ACKs establish responses or endorsement, not locally_supported obligation. The specific removal response remains technical acceptance. No authorizes, applies, or O relation is warranted; RPC error text is technical behavior rather than sanction.',
        'evidence': [evidence('pr14441:comments:0'), evidence('pr14441:reviews:4'), evidence('pr14441:review_comments:6')],
        'limitation': 'This is abstention on the supplied evidence, not a claim that authority or expectations are absent from Bitcoin Core generally.'
    },
    'event_reviews': event_reviews,
    'relation_reviews': [{'index': i, 'status': 'retained', **r} for i, r in enumerate(annotation['relations'])],
    'outcome_reviews': [{'index': i, 'status': 'retained', **o,
                        'review_rationale': 'Each positive material claim is scoped to its supplied report, retained patch, or metadata. Exact object/revision identities are retained, and unsupported causation, per-proposition implementation, and network adoption are not asserted.'} for i, o in enumerate(annotation['episode_summary']['observed_outcomes'])],
    'mechanism_reviews': [{'index': i, 'review_status': 'retained', **m,
                          'review_rationale': 'The full initiating proposal, its qualifications, response, and described outcome are included in the cited sources. Supported_sequence means textual correspondence, not causal identification or proof of a recognized rule.'} for i, m in enumerate(annotation['episode_summary']['mechanisms'])],
    'presentation_review': {
        'status': 'retained',
        'rationale': 'S02 and S04 preserve prose plus proposed blockquote wording as proposed_wording/mixed. Inline code in otherwise plain prose does not by itself create an institutional quotation. No supplied occurrence is struck through, and no edit history is inferred. No technical paragraph is double-counted as a new institution.'},
    'remaining_limits': annotation['episode_summary']['missing_evidence'],
    'unresolved_questions': annotation['episode_summary']['unresolved_questions'],
    'review_change_counts': {'logged_changes': len(repairs), 'interpretation_changing_repairs': 0,
                             'epistemic_labeling_corrections': 1, 'explanation_clarifications': 1,
                             'screening_or_unit_count_changes': 0}
}
write('repair_log.json', {'run_id': 'F02_v03_r2', 'first_complete_sha256': sha('annotation.first_complete.json'),
                          'final_sha256': sha('annotation.final.json'), 'mechanical_repairs': [], 'changes': repairs})
write('review_notes.json', review)

frozen = ['INSTRUCTIONS.txt', 'protocol/codebook.txt', 'protocol/annotation_schema.json', 'packet.json', 'tools/check_annotation.py']
generated = ['build_annotation.py', 'annotation.json', 'annotation.first_complete.json', 'checks.first.json', 'finalize_annotation.py', 'annotation.final.json', 'checks.json', 'repair_log.json', 'review_notes.json', 'access_record.json', 'run_manifest.json']
access = {
    'run_id': 'F02_v03_r2', 'episode_id': 'F02', 'recorded_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'allowed_directory': str(ROOT),
    'files_accessed': [{'path': str(ROOT / x), 'relative_path': x, 'role': 'frozen_input',
                        'access': ['read', 'execute'] if x == 'tools/check_annotation.py' else ['read'], 'sha256': sha(x)} for x in frozen]
                    + [{'path': str(ROOT / x), 'relative_path': x, 'role': 'run_output',
                        'access': ['write', 'read', 'execute'] if x.endswith('.py') else ['write', 'read']} for x in generated],
    'research_sources': ['packet.json only'],
    'optional_calibration_files_accessed': [], 'external_research_sources_accessed': [],
    'other_run_files_accessed': [], 'parent_directory_files_accessed': [],
    'web_or_library_access': False, 'subagents_spawned': False,
    'frozen_inputs_modified': False,
    'configuration': {
        'configuration_mode': 'inherited_primary_configuration',
        'description': 'Inherited primary configuration with no model or reasoning override. Historical model names in the protocol were not used to infer this run\'s model identity.',
        'model_override': None, 'exact_model_identifier': None, 'reasoning_effort': None,
        'provider_snapshot': None, 'seed': None, 'sampling_parameters': None,
        'token_use': None, 'cost': None,
        'unknown_fields_note': 'These runtime/provider values were not exposed to the coder and are left null.'
    },
    'runtime': {'python_executable': sys.executable, 'python_version': platform.python_version(),
                'platform': sys.platform,
                'ordinary_library_modules': ['json', 'copy', 'hashlib', 'pathlib', 'datetime', 'platform', 'subprocess', 'sys', 're', 'jsonschema'],
                'library_access_note': 'Only ordinary Python runtime and checker dependency loads occurred outside the assigned research directory; no outside research document was read.'},
    'workflow': ['Read run instructions, complete codebook, complete schema, complete packet, and checker source.',
                 'Created complete annotation and exclusive first-complete snapshot before checker feedback.',
                 'Ran first checker and preserved checks.first.json unchanged; no mechanical repairs were required.',
                 'Conducted one complete source self-review, including every focal entry, all supplements as context, every unit/component, all events/relations, and every outcome/mechanism.',
                 'Logged two source-review changes, saved final JSON, reran checker, and resolved every review flag with source evidence.']
}
write('access_record.json', access)
manifest_names = frozen + [x for x in generated if x != 'run_manifest.json']
manifest = {
    'run_id': 'F02_v03_r2', 'episode_id': 'F02', 'packet_sha256': sha('packet.json'),
    'counts': {'screened_entries': 22, 'candidate_entries': 4, 'context_only_entries': 15, 'empty_entries': 3,
               'units': 15, 'statement_units': 4, 'context_units': 11, 'container_units': 0, 'quotation_units': 0,
               'relations': 7, 'observed_outcomes': 5, 'mechanisms': 2,
               'exact_anchor_references': final_checks['exact_anchor_references'], 'checker_errors': 0, 'review_flags': len(final_checks['review_flags'])},
    'final_check_status': final_checks['status'],
    'artifacts': [{'path': x, 'bytes': (ROOT / x).stat().st_size, 'sha256': sha(x)} for x in manifest_names],
    'freeze_ready': True
}
write('run_manifest.json', manifest)
print(json.dumps({'status': 'complete', 'counts': manifest['counts'], 'final_sha256': sha('annotation.final.json'), 'first_complete_sha256': sha('annotation.first_complete.json')}))
