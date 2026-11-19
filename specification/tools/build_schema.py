"""Build the 0.4 schema from the preserved 0.3 schema; no baseline mutation."""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def obj(properties, required=None):
    return {"type": "object", "properties": properties,
            "required": list(properties) if required is None else required,
            "additionalProperties": False}

def enum(*values):
    return {"enum": list(values)}

def array(item, **kw):
    return {"type": "array", "items": item, **kw}

def build():
    s = json.loads((ROOT / 'baseline_v03/protocol/annotation_schema.json').read_text())
    s['$id'] = 'urn:bitcoin-governance:ig2:0.4'
    s['properties']['schema_version'] = {'const': '0.4'}
    u = s['properties']['units']['items']
    p = u['properties']; inst = p['institution']; ip = inst['properties']
    ev = copy.deepcopy(ip['evidence']['items'])
    evidence = array(ev)
    text = {'type': 'string', 'minLength': 1}
    nullable_text = {'type': ['string', 'null'], 'minLength': 1}
    date = {'type': ['string', 'null'], 'pattern': r'^\d{4}-\d{2}-\d{2}$'}
    target = enum('this_proposition', 'broader_proposal', 'broader_principle', 'unresolved')
    qualifier = obj({'description': text, 'evidence': array(ev, minItems=1),
                     'attachment': enum('component', 'linked_unit', 'scope_note'),
                     'linked_unit_id': nullable_text, 'rationale': text})
    prop = obj({'summary': text, 'decision_object_id': nullable_text,
                'domain': text, 'time_scope': text,
                'identity_evidence': evidence, 'qualifiers': array(qualifier)})
    p['proposition'] = {'oneOf': [prop, {'type': 'null'}]}
    u['required'].append('proposition')
    component = p['components']['items']
    component['properties']['governing_span'] = copy.deepcopy(ev)
    component['required'].append('governing_span')
    del ip['standing']; inst['required'].remove('standing')
    ip['standing_profile'] = obj({
        'documentary': enum('exact', 'partial', 'broader', 'none', 'unresolved', 'not_applicable'),
        'recognition': enum('none', 'same_actor_only', 'interpersonal', 'repeated_interpersonal', 'unresolved', 'not_applicable'),
        'application': enum('none', 'reported', 'observed', 'both', 'unresolved', 'not_applicable')})
    ip['standing_profile']['properties']['recognition']['description'] = 'Focal expectation-recognition projection only. Select kind=expectation_recognition and target=this_proposition. Generic same_actor_restatement responses remain event-level continuity and do not imply same_actor_only. See codebook for precedence and unresolved evidence.'
    ip['recognition']['description'] = 'Events retain responses, assent, personal continuity, and expectation recognition separately. Event presence alone does not establish interpersonal recognition.'
    ip['documentary_support'] = array(obj({
        'coverage': enum('exact', 'partial', 'broader', 'unresolved'),
        'claim_as_of': date, 'source_as_of': date,
        'date_basis': enum('pinned_revision', 'body_history', 'recorded_event', 'unknown'),
        'temporal_fit': enum('established', 'later_only', 'unresolved'),
        'evidence': array(ev, minItems=1), 'rationale': text}))
    ip['application_evidence'] = array(obj({
        'status': enum('reported', 'observed', 'unresolved'),
        'target': target, 'evidence': array(ev, minItems=1), 'rationale': text}))
    ip['challenges'] = array(obj({
        'aspect': enum('content', 'authority', 'application', 'premise', 'unresolved'),
        'target': target, 'evidence': array(ev, minItems=1), 'rationale': text}))
    ip['type_alternatives'] = array(copy.deepcopy(ip['type']), uniqueItems=True)
    for key in ['standing_profile', 'documentary_support', 'application_evidence', 'challenges', 'type_alternatives']:
        inst['required'].append(key)
    recognition = ip['recognition']['items']
    recognition['properties']['target'] = copy.deepcopy(target)
    recognition['properties'].update({
        'mode': enum('ordinary_assent', 'status_recognition', 'expectation_application', 'explicit_expectation', 'same_actor_restatement', 'other', 'unresolved'),
        'speaker_relation': enum('different_actor', 'same_actor', 'unknown', 'not_applicable'),
        'independence_key': nullable_text})
    recognition['required'] += ['mode', 'speaker_relation', 'independence_key']
    for event in [recognition, p['disposition_events']['items']]:
        event['properties'].update({'object_id': nullable_text, 'identity_evidence': evidence})
        event['required'] += ['object_id', 'identity_evidence']
    levels = p.pop('level_alternatives'); u['required'].remove('level_alternatives')
    for k in ['target_level_alternatives', 'observed_level_alternatives']:
        p[k] = copy.deepcopy(levels); u['required'].append(k)
    p['level_evidence'] = obj({'target_activity': text, 'observed_activity': text,
                               'arrangement': text, 'evidence': evidence})
    u['required'].append('level_evidence')
    for group in ['observed_outcomes', 'mechanisms']:
        item = s['properties']['episode_summary']['properties'][group]['items']
        item['properties']['claim_parts'] = array(obj({'text': text, 'evidence': array(ev, minItems=1)}), minItems=1)
        item['required'].append('claim_parts')
    (ROOT/'protocol/annotation_schema.json').write_text(json.dumps(s, indent=2)+'\n')
    return s

if __name__ == '__main__':
    build()
