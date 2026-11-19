"""Version 0.4 structural and evidence-scope checks. Not semantic certification."""
import hashlib
import json
import re
import sys
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]

def evidence_key(e):
    return (e['source_id'], e['span']['start'], e['span']['end'])

def inside(a, b):
    return a['source_id'] == b['source_id'] and b['span']['start'] <= a['span']['start'] < a['span']['end'] <= b['span']['end']

def token_fragment(text, start, end):
    q = text[start:end]
    word = lambda c: c.isalnum() or c == '_'
    left = start > 0 and word(q[0]) and (word(text[start-1]) or text[start-1] == '-')
    right = end < len(text) and word(q[-1]) and (word(text[end]) or text[end] == '-')
    contraction = end < len(text) and text[end] in "'’" and q.lower() in ['i','we','you','they','he','she','it'] and re.match(r"['’](?:m|ve|d|ll|re|s)\b", text[end:], re.I)
    if end < len(text) and text[end] in "'’" and not contraction and word(q[-1]):
        right = True
    return bool(left or right)

def profile(inst, role='statement'):
    if role != 'statement':
        return dict.fromkeys(['documentary','recognition','application'], 'not_applicable')
    docs = inst['documentary_support']
    established = [d['coverage'] for d in docs if d['temporal_fit']=='established']
    documentary = next((x for x in ['exact','partial','broader'] if x in established), 'unresolved' if docs else 'none')
    rec = [x for x in inst['recognition'] if x['kind']=='expectation_recognition' and x['target']=='this_proposition']
    inter = [x for x in rec if x['speaker_relation']=='different_actor' and x['mode'] in ['status_recognition','expectation_application','explicit_expectation'] and x['basis']!='unresolved']
    keys = {x['independence_key'] for x in inter if x['independence_key']}
    if len(keys)>=2:
        recognition='repeated_interpersonal'
    elif inter:
        recognition='interpersonal'
    elif any(x['speaker_relation']=='same_actor' for x in rec):
        recognition='same_actor_only'
    elif rec:
        recognition='unresolved'
    else:
        recognition='none'
    applications = {x['status'] for x in inst['application_evidence'] if x['target']=='this_proposition'}
    if {'reported','observed'} <= applications:
        application='both'
    elif 'observed' in applications:
        application='observed'
    elif 'reported' in applications:
        application='reported'
    elif applications:
        application='unresolved'
    else:
        application='none'
    return {'documentary':documentary, 'recognition':recognition, 'application':application}

def check(packet_path, annotation_path):
    packet_path, annotation_path = Path(packet_path), Path(annotation_path)
    packet=json.loads(packet_path.read_text()); a=json.loads(annotation_path.read_text())
    schema=json.loads((ROOT/'protocol/annotation_schema.json').read_text())
    schema_errors=sorted(jsonschema.Draft202012Validator(schema).iter_errors(a), key=lambda e:str(list(e.path)))
    if schema_errors:
        return {'status':'fail','errors':[{'code':'schema','path':list(e.path),'message':e.message} for e in schema_errors], 'review_flags':[]}
    errors=[];flags=[];anchors=0
    def error(code, message, uid=None): errors.append({'code':code,'unit_id':uid,'message':message})
    def flag(code, message, uid=None): flags.append({'code':code,'unit_id':uid,'message':message})
    if a['episode_id']!=packet['episode_id']:error('episode','Episode mismatch')
    if a['packet_sha256']!=hashlib.sha256(packet_path.read_bytes()).hexdigest():error('packet_hash','Packet hash mismatch')
    entries={e['source_id']:e for e in packet['entries']}
    if len(entries)!=len(packet['entries']):error('source_ids','Duplicate packet source IDs')
    if any('object_id' not in e for e in entries.values()):error('object_catalog','Each packet source requires object_id, possibly null')
    texts={k:v['text'] for k,v in entries.items()};units={u['unit_id']:u for u in a['units']}
    if len(units)!=len(a['units']):error('unit_ids','Duplicate unit IDs')
    screens=a['entry_screening']
    if len(screens)!=len(entries) or {s['source_id'] for s in screens}!=set(entries):error('screening','Incomplete or duplicate source screening')
    def walk(x):
        nonlocal anchors
        if isinstance(x,dict):
            if 'source_id' in x and 'span' in x:
                sp=x['span'];txt=texts.get(x['source_id'])
                if txt is None or not (0<=sp['start']<sp['end']<=len(txt)) or txt[sp['start']:sp['end']]!=sp['quote']:
                    error('exact_anchor','Invalid source, quote, or offset')
                anchors+=1
            for v in x.values():walk(v)
        elif isinstance(x,list):
            for v in x:walk(v)
    walk(a)
    if any(e['code']=='exact_anchor' for e in errors):
        return {'status':'fail','errors':errors,'review_flags':flags,'exact_anchor_references':anchors}
    for u in a['units']:
        uid=u['unit_id'];inst=u['institution'];role=u['record_role'];prop=u['proposition']
        if u['parent_unit_id'] is not None and u['parent_unit_id'] not in units:error('parent','Missing parent',uid)
        if role=='statement' and prop is None:error('proposition','Statement lacks bounded proposition',uid)
        if role!='statement':
            if prop is not None or u['grammar']!='not_institutional' or u['components'] or inst['type']!='not_applicable' or u['statement_target_level']!='not_applicable':error('nonstatement','Nonstatement fields imply a focal institutional claim',uid)
            if any(inst[k] for k in ['documentary_support','recognition','application_evidence','challenges','authority_evidence']):error('nonstatement_evidence','Keep evidence judgments on focal statement, not repeated/context record',uid)
        if role=='container' and u['observed_action_level']!='not_applicable':error('container','Container action level must be not_applicable',uid)
        if inst['standing_profile']!=profile(inst,role):error('support_profile','Standing profile does not match declared evidence events',uid)
        expected_dispute=any(x['target']=='this_proposition' and x['aspect']!='unresolved' for x in inst['challenges'])
        if inst['dispute_present']!=expected_dispute:error('challenge_flag','Dispute flag must reflect a scoped, identified challenge',uid)
        if inst['type']=='rule_candidate' and not inst['authority_evidence']:error('authority','rule_candidate lacks authority evidence',uid)
        if inst['type'] in inst['type_alternatives']:error('type_alternative','Primary type repeated as alternative',uid)
        if prop:
            if prop['decision_object_id'] and not prop['identity_evidence']:error('object_identity','Decision-object identity lacks evidence',uid)
            for q in prop['qualifiers']:
                if q['attachment']=='linked_unit' and q['linked_unit_id'] not in units:error('qualifier_link','Missing linked qualifier unit',uid)
                if q['attachment']!='linked_unit' and q['linked_unit_id'] is not None:error('qualifier_link','Unexpected linked qualifier unit',uid)
            flag('qualifier_audit','Check that all material conditions, negation, attribution, and alternatives are listed or encoded',uid)
        for c in u['components']:
            if c['basis']=='explicit' and not c['evidence']:error('component_evidence','Explicit component lacks evidence',uid)
            if c['basis']!='explicit' and not c['inference_note'].strip():error('component_reason','Inferred/unresolved role lacks explanation',uid)
            gov=c['governing_span']
            for e in c['evidence']:
                if c['occurrence_role']=='local' and (not inside(e,u) or not inside(e,gov) or not inside(gov,u)):
                    error('predicate_scope','Local anchor or governing clause lies outside the declared scope',uid)
                if not inside(e,u) and not c['inference_note'].strip():error('outside_unit','Outside-unit component lacks explanation',uid)
                sp=e['span']
                if token_fragment(texts[e['source_id']],sp['start'],sp['end']) and not c.get('token_exception','').strip():error('token_fragment','Component anchor splits a token without justification',uid)
            if c['occurrence_role']!='local' and not c['inference_note'].strip():error('occurrence_reason','Nonlocal/inferred occurrence lacks explanation',uid)
            if c['basis']=='context_inferred' and c['occurrence_role']=='local':error('inferred_role','Inferred component incorrectly labeled local',uid)
            if c['occurrence_role']=='semantic_inference' and c['basis']=='explicit':error('inferred_role','Semantic inference labeled explicit',uid)
            if u['parse_mode']=='pragmatic' and c['symbol'] in ['A','Bdir','Bind'] and c['basis']=='explicit' and not c['inference_note'].strip():error('pragmatic_role','Explicit role in pragmatic parse requires explanation',uid)
            flag('predicate_audit','Verify the cited occurrence performs this role in the declared governing clause',uid)
        for d in inst['documentary_support']:
            if d['temporal_fit']=='established' and (d['date_basis']=='unknown' or d['source_as_of'] is None):error('document_date','Established documentary support lacks dated basis',uid)
            if d['claim_as_of'] and d['source_as_of'] and d['source_as_of']>d['claim_as_of'] and d['temporal_fit']=='established':error('backdating','Later documentary source cannot establish earlier standing',uid)
            if d['date_basis']=='pinned_revision' and not any(entries[e['source_id']].get('blob_sha') or entries[e['source_id']].get('revision_id') for e in d['evidence']):error('revision','Pinned revision claim lacks supplied revision identity',uid)
            flag('document_scope','Verify exact proposition coverage and that the source actually supplies authoritative guidance',uid)
        for application in inst['application_evidence']:
            flag('application_audit','Verify the target and whether the record reports or demonstrates application; an announced consequence is not an executed sanction',uid)
        for challenge in inst['challenges']:
            flag('challenge_audit','Verify the common proposition and the exact content, authority, premise, or application being challenged',uid)
        for ev in inst['recognition']+u['disposition_events']:
            if not ev['evidence'] or not ev['rationale'].strip():error('event_support','Event lacks evidence or rationale',uid)
            if ev['target']=='unresolved' and ev['basis']!='unresolved':error('event_target','Unresolved target requires unresolved basis',uid)
            if ev['object_id'] and not ev['identity_evidence']:error('event_identity','Event object lacks identity evidence',uid)
            if ev['target']=='this_proposition' and prop and prop['decision_object_id'] and ev['object_id']!=prop['decision_object_id']:error('event_identity','Event object differs from focal decision object',uid)
            if ev['kind'] in ['recorded_status','recorded_merged','recorded_closed_unmerged']:
                metadata=[entries[e['source_id']] for e in ev['evidence'] if entries[e['source_id']]['kind']=='record_metadata']
                if not metadata:error('status_metadata','Recorded status lacks metadata evidence',uid)
                if not ev['object_id'] or any(m.get('object_id')!=ev['object_id'] for m in metadata):error('metadata_object','Status metadata belongs to a different or unidentified object',uid)
                if ev['kind']=='recorded_closed_unmerged':
                    joined='\n'.join(e['span']['quote'] for e in ev['evidence'] if entries[e['source_id']]['kind']=='record_metadata')
                    if not re.search(r'"state"\s*:\s*"closed"',joined) or not re.search(r'"merged"\s*:\s*false',joined):error('status_parts','Closed-unmerged event must cite both closed state and false merge status',uid)
            if ev['kind'] in ['reported_implementation','reported_implemented'] and all(entries[e['source_id']]['kind']=='record_metadata' for e in ev['evidence']):error('report_origin','Participant report relies only on metadata',uid)
        for ev in inst['recognition']:
            if ev['kind']=='expectation_recognition':
                if ev['mode'] in ['ordinary_assent','other']:error('recognition_mode','Ordinary assent does not establish expectation recognition',uid)
                if ev['speaker_relation']=='different_actor' and not ev['independence_key']:error('recognition_independence','Interpersonal recognition lacks event identity',uid)
                if ev['mode']=='same_actor_restatement' and ev['speaker_relation']!='same_actor':error('speaker_relation','Same-actor restatement mislabeled interpersonal',uid)
                if ev['speaker_relation']=='different_actor' and prop:
                    actor=entries[u['source_id']].get('author')
                    cited={entries[e['source_id']].get('author') for e in ev['evidence']}
                    if actor and cited and cited=={actor}:error('speaker_identity','All recognition evidence is by the focal speaker',uid)
                    possible_keys={entries[e['source_id']].get('object_id') for e in ev['evidence']
                                   if entries[e['source_id']].get('author') not in [None,actor]}
                    if ev['independence_key'] not in possible_keys:error('recognition_episode','Recognition episode key is not supported by a cited different-actor source',uid)
                flag('recognition_audit','Verify recognition of an expectation, distinct attribution, and independent episode identity',uid)
        for k,alts in [('statement_target_level','target_level_alternatives'),('observed_action_level','observed_level_alternatives')]:
            if u[k] in u[alts]:error('level_alternative','Primary level repeated as alternative',uid)
            if u[k] in ['collective_choice','constitutional','epistemic']:
                if not u['level_evidence']['evidence']:error('higher_level','Higher-level classification lacks evidence',uid)
                flag('higher_level_audit','Verify the governed activity and institutional arrangement independently of the utterance location',uid)
        if '?' in u['span']['quote'] and u['speech_act']!='question':flag('question_audit','Check whether this is a literal question, including repeated quotations',uid)
    for sc in screens:
        ids={i for i,u in units.items() if u['source_id']==sc['source_id']}
        if set(sc['unit_ids'])!=ids or len(sc['unit_ids'])!=len(ids):error('screening_units','Incorrect screening unit references')
        statement=any(units[i]['record_role']=='statement' for i in ids)
        if (sc['disposition']=='candidate')!=statement:error('screening_candidate','Candidate screening does not match statement records')
        if sc['disposition']=='empty' and (texts.get(sc['source_id'],'').strip() or ids):error('screening_empty','Invalid empty screening')
    for rel in a['relations']:
        f,t=rel['from_unit_id'],rel['to_unit_id']
        if f not in units or t not in units or f==t:error('relation_endpoints','Bad relation endpoints');continue
        logical=rel['type'] in ['AND','OR','XOR','NOT']
        if logical != (rel['logic_scope'] in ['propositions','actions']):error('logic_scope','Incorrect relation logic scope')
        if rel['type']=='quotes' and units[f]['record_role']!='quotation':error('quotation','quotes must begin at repeated quotation')
        if rel['basis']=='explicit' and not rel['evidence']:error('relation_evidence','Explicit relation lacks evidence')
        if rel['type']=='challenges':flag('challenge_object','Verify both endpoints concern the same proposition, premise, or application')
    for u in units.values():
        if u['record_role']=='quotation' and not any(r['type']=='quotes' and r['from_unit_id']==u['unit_id'] for r in a['relations']):error('quotation_link','Repeated quotation lacks original link',u['unit_id'])
    for group in ['observed_outcomes','mechanisms']:
        for item in a['episode_summary'][group]:
            if not item['evidence']:error('summary_evidence','Summary claim lacks evidence')
            all_evidence={evidence_key(e) for e in item['evidence']}
            if any(evidence_key(e) not in all_evidence for part in item['claim_parts'] for e in part['evidence']):error('claim_parts','Summary evidence omits a clause evidence anchor')
            if group=='mechanisms' and not set(item['unit_ids'])<=set(units):error('mechanism_unit','Unknown mechanism unit')
            flag('summary_audit','Verify claim_parts cover every material clause; mechanical inclusion does not establish entailment')
    return {'status':'fail' if errors else 'pass','screened_entries':len(screens),'units':len(units),
            'statement_units':sum(u['record_role']=='statement' for u in units.values()),
            'exact_anchor_references':anchors,'errors':errors,'review_flags':flags,
            'semantic_validity':'Not certified; audit flags require recorded source review'}

if __name__=='__main__':
    try:
        r=check(*sys.argv[1:]);print(json.dumps(r,ensure_ascii=False,indent=2));sys.exit(0 if r['status']=='pass' else 1)
    except Exception as e:
        print(json.dumps({'status':'fail','error':type(e).__name__+': '+str(e)}));sys.exit(1)
