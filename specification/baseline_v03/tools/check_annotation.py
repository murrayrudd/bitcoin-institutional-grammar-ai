"""Version 0.3 structural and occurrence checks. Semantic truth is not certified."""
import json,sys,hashlib,re
from pathlib import Path

def token_fragment(text,start,end):
    q=text[start:end]
    word=lambda c:c.isalnum() or c=='_'
    left=start>0 and word(q[0]) and (word(text[start-1]) or text[start-1]=='-')
    right=end<len(text) and word(q[-1]) and (word(text[end]) or text[end]=='-')
    # Pronoun subjects inside standard contractions are grammatically separable.
    contraction=end<len(text) and text[end] in "'’" and q.lower() in ['i','we','you','they','he','she','it'] and re.match(r"['’](?:m|ve|d|ll|re|s)\b",text[end:],re.I)
    if end<len(text) and text[end] in "'’" and not contraction and word(q[-1]):right=True
    return bool(left or right)

def occurrence_issues(unit,component,texts):
    errors=[];flags=[];role=component['occurrence_role']
    for e in component['evidence']:
        span=e['span'];same=e['source_id']==unit['source_id'];inside=same and unit['span']['start']<=span['start'] and span['end']<=unit['span']['end']
        if role=='local' and not inside:errors.append('local component evidence is outside its unit')
        if not inside:
            if not component['inference_note'].strip():errors.append('outside-unit component lacks a scope/reference explanation')
            flags.append({'kind':'outside_unit','symbol':component['symbol'],'occurrence_role':role,'evidence':e,'note':component['inference_note']})
        if token_fragment(texts[e['source_id']],span['start'],span['end']):
            if not component.get('token_exception','').strip():errors.append('component anchor is a token fragment without an exception')
            flags.append({'kind':'token_fragment','symbol':component['symbol'],'evidence':e,'exception':component.get('token_exception','')})
    if role!='local' and not component['inference_note'].strip():errors.append('nonlocal/inferred occurrence role requires explanation')
    if component['basis']=='context_inferred' and role not in ['semantic_inference','shared_scope','context_reference','unresolved']:errors.append('inferred component must declare its contextual role')
    return errors,flags

def check(packet_path,annotation_path):
    import jsonschema
    root=Path(__file__).resolve().parents[1]
    packet=json.loads(Path(packet_path).read_text());a=json.loads(Path(annotation_path).read_text())
    jsonschema.Draft202012Validator(json.loads((root/'protocol/annotation_schema.json').read_text())).validate(a)
    assert a['episode_id']==packet['episode_id'],'Episode mismatch'
    assert a['packet_sha256']==hashlib.sha256(Path(packet_path).read_bytes()).hexdigest(),'Packet hash mismatch'
    texts={e['source_id']:e['text'] for e in packet['entries']};screens=a['entry_screening'];units={u['unit_id']:u for u in a['units']}
    assert len(units)==len(a['units']),'Duplicate unit IDs'
    assert len(screens)==len(texts) and {x['source_id'] for x in screens}==set(texts),'Screening coverage'
    anchors=0
    def walk(x):
        nonlocal anchors
        if isinstance(x,dict):
            if 'source_id' in x and 'span' in x:
                sp=x['span'];txt=texts[x['source_id']]
                assert 0<=sp['start']<sp['end']<=len(txt) and txt[sp['start']:sp['end']]==sp['quote'],'Invalid quote or offset'
                anchors+=1
            for v in x.values():walk(v)
        elif isinstance(x,list):
            for v in x:walk(v)
    walk(a);errors=[];flags=[]
    for u in a['units']:
        assert u['parent_unit_id'] is None or u['parent_unit_id'] in units,'Missing parent'
        if u['record_role']!='statement':
            assert u['grammar']=='not_institutional' and not u['components'],'Nonstatement grammar/components'
            assert u['institution']['type']=='not_applicable' and u['institution']['standing']=='not_applicable','Nonstatement institution'
            assert u['statement_target_level']=='not_applicable','Nonstatement target level'
        if u['record_role']=='container':assert u['observed_action_level']=='not_applicable','Container action level'
        if u['institution']['standing']=='locally_supported':
            assert any(e['kind']=='expectation_recognition' and e['target']=='this_proposition' and e['evidence'] for e in u['institution']['recognition']),'Local standing lacks proposition-specific expectation recognition'
        for c in u['components']:
            if c['basis']=='explicit':assert c['evidence'],'Explicit component lacks evidence'
            else:assert c['inference_note'].strip(),'Inferred/unresolved component lacks reason'
            ee,ff=occurrence_issues(u,c,texts)
            errors += [{'unit_id':u['unit_id'],'symbol':c['symbol'],'message':e} for e in ee]
            flags += [{'unit_id':u['unit_id'],'source_id':u['source_id'],**f} for f in ff]
    for sc in screens:
        ids={uid for uid,u in units.items() if u['source_id']==sc['source_id']}
        assert set(sc['unit_ids'])==ids,'Screening unit references'
        statement=any(units[i]['record_role']=='statement' for i in ids)
        assert (sc['disposition']=='candidate')==statement,'Candidate screening must match statement records'
        if sc['disposition']=='empty':assert not texts[sc['source_id']].strip() and not ids,'Invalid empty screening'
    for rel in a['relations']:
        assert rel['from_unit_id'] in units and rel['to_unit_id'] in units and rel['from_unit_id']!=rel['to_unit_id'],'Bad relation endpoints'
        if rel['type'] in ['AND','OR','XOR','NOT']:assert rel['logic_scope'] in ['propositions','actions'],'Missing logical scope'
        else:assert rel['logic_scope']=='not_applicable','Spurious logical scope'
        if rel['type']=='quotes':assert units[rel['from_unit_id']]['record_role']=='quotation','quotes must begin at repeated quotation'
        if rel['basis']=='explicit':assert rel['evidence'],'Explicit relation lacks evidence'
    for u in a['units']:
        if u['record_role']=='quotation':assert any(r['type']=='quotes' and r['from_unit_id']==u['unit_id'] for r in a['relations']),'Unlinked quotation'
    for m in a['episode_summary']['mechanisms']:assert set(m['unit_ids'])<=set(units),'Unknown mechanism unit'
    kinds={e['source_id']:e['kind'] for e in packet['entries']}
    for u in a['units']:
        inst=u['institution']
        if inst['type']=='rule_candidate' and not inst['authority_evidence']:
            errors.append({'unit_id':u['unit_id'],'message':'rule_candidate lacks authority_evidence'})
        for c in u['components']:
            if c['occurrence_role']=='semantic_inference' and c['basis']=='explicit':
                errors.append({'unit_id':u['unit_id'],'message':'semantic_inference role cannot have explicit basis'})
            if u['parse_mode']=='pragmatic' and c['symbol'] in ['A','Bdir','Bind'] and c['basis']=='explicit':
                flags.append({'unit_id':u['unit_id'],'kind':'pragmatic_explicit_argument','symbol':c['symbol'],'note':c['inference_note']})
                if not c['inference_note'].strip():errors.append({'unit_id':u['unit_id'],'message':'explicit pragmatic argument requires role-preservation explanation'})
        for event in inst['recognition']+u['disposition_events']:
            if not event['evidence']:errors.append({'unit_id':u['unit_id'],'message':'event lacks evidence'})
            if not event['rationale'].strip():errors.append({'unit_id':u['unit_id'],'message':'event lacks rationale'})
            if event['target']=='unresolved' and event['basis']!='unresolved':errors.append({'unit_id':u['unit_id'],'message':'unresolved target requires unresolved basis'})
            if event['kind'] in ['recorded_status','recorded_merged','recorded_closed_unmerged']:
                if not any(kinds[e['source_id']]=='record_metadata' for e in event['evidence']):errors.append({'unit_id':u['unit_id'],'message':'recorded status requires metadata evidence'})
            if event['kind'] in ['reported_implementation','reported_implemented']:
                if all(kinds[e['source_id']]=='record_metadata' for e in event['evidence']):errors.append({'unit_id':u['unit_id'],'message':'participant implementation report cannot rely only on metadata'})
    for group in ['observed_outcomes','mechanisms']:
        for item in a['episode_summary'][group]:
            if not item['evidence']:errors.append({'message':group+' claim lacks evidence'})
    return {'status':'fail' if errors else 'pass' ,'screened_entries':len(screens),'units':len(units),'statement_units':sum(u['record_role']=='statement' for u in units.values()),'exact_anchor_references':anchors,'errors':errors,'review_flags':flags,'semantic_validity':'Requires source review; not certified by this checker'}

if __name__=='__main__':
    try:r=check(*sys.argv[1:]);print(json.dumps(r,ensure_ascii=False,indent=2));sys.exit(0 if r['status']=='pass' else 1)
    except Exception as e:print(json.dumps({'status':'fail','error':type(e).__name__+': '+str(e)}));sys.exit(1)
