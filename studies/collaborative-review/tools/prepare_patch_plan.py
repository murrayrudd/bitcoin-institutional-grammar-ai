"""Record coordinator-selected implementations of the source-grounded deliberation."""
from pathlib import Path
import json,re,copy
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
A={t['topic_id']:t for t in read(R/'panel/A_initial.json')['topics']}
B={t['topic_id']:t for t in read(R/'panel/B_initial.json')['topics']}
anns={p.parent.name:read(p) for p in (R/'inputs/runs').glob('*v04*/annotation.final.json')}
def u(rid,uid):return next(x for x in anns[rid]['units'] if x['unit_id']==uid)
plan=[]
def add(rid,uid,path,value,ids,reason):
    parts=[int(t) if t.isdigit() else t for t in re.findall(r'[^.\[\]]+',path)]
    q={'run_id':rid,'value':value,'decision_ids':ids,'reason':reason}
    if uid:q.update(unit_id=uid,tail=parts)
    else:q['path']=parts
    plan.append(q)
def import_changes(topic,selected=None):
    for p in A[topic]['recommended_changes']:
        if selected and not selected(p):continue
        add(p['run_id'],p.get('unit_id'),p['path'],p['new_value'],topic,'Source-grounded post-discussion representation; this does not revise independent reliability.')

# D01 correct identity, while retaining explicit alternative readings of assent.
for rid,uid in [('F01_v04_r1','S32'),('F01_v04_r2','U31'),('F01_v04_r3','R06')]:
    for path,value in [('proposition.decision_object_id',None),('proposition.identity_evidence',[]),('institution.recognition[0].object_id',None),('institution.recognition[0].identity_evidence',[])]:
        add(rid,uid,path,value,'D01,Q034','The general retention criterion has no applicable numbered object. The discussion episode remains in independence_key.')
    original=u(rid,uid)
    add(rid,uid,'institution.recognition[0].rationale',original['institution']['recognition'][0]['rationale']+' The numbered object is inapplicable to this general criterion; null does not mean its semantic referent is unknown.','D01,Q034','Separate semantic reference from a numbered proposal identifier.')
    alt=original['alternative_interpretation']
    add(rid,uid,'alternative_interpretation',alt+' Deliberation retained ordinary tentative assent and unresolved expectation-recognition readings. Assent can refer to the complete criterion contextually or to its quoted recurring floor; neither establishes adoption or binding authority.','D01,Q037','Preserve the panel\'s unresolved scope and recognition alternatives.')

# D02 keep the frozen implementation and expose its narrower projection.
for rid,uid in [('F01_v04_r1','S13'),('F01_v04_r3','C11'),('F03_v04_r1','U03'),('F03_v04_r2','F03-U03'),('F03_v04_r3','F03-U04')]:
    old=u(rid,uid)
    add(rid,uid,'uncertainty_reason',old['uncertainty_reason']+' The frozen checker projects only this-proposition expectation_recognition events into the recognition profile. The response event preserves same-actor continuity although the profile is none; the codebook\'s broader same-actor wording remains a documented ambiguity.','D02,Q013,Q041','Do not relabel personal continuity as expectation recognition to satisfy a preferred summary label.')

# D03 resulting artifact is observable, while historical transformation and complete checkbox placement remain unverified.
import_changes('D03')

# D04 retain the two defensible report scopes; implement only the common rebase disposition.
import_changes('D04',lambda p:p['run_id'].startswith('F01'))
for rid,uids in [('F02_v04_r1',['F02_S01','F02_S02','F02_S04']),('F02_v04_r2',['S02','S03','S05']),('F02_v04_r3',['F02-S01','F02-S02','F02-S04'])]:
    for uid in uids:
        extra=(' The aggregate update can instead be targeted to the broader proposal under a stricter itemization reading.' if rid.endswith('r1') else ' The panel preferred contextual reported incorporation of the identified suggestion; this view retains the defensible broader-proposal report target.')
        add(rid,uid,'alternative_interpretation',u(rid,uid)['alternative_interpretation']+extra+' Neither report interpretation resolves isolated fixed/Both replies or verifies every tentative wording choice.','D04,Q006','Retain explicit report-scope alternatives after deliberation.')

# D05 preserve types, repair the mistaken recurrence requirement and retain the other supported type.
for rid,uid in [('F03_v04_r1','U24'),('F03_v04_r2','F03-U17'),('F03_v04_r3','F03-U25'),('F01_v04_r1','S09'),('F01_v04_r2','U08'),('F01_v04_r3','C03')]:
    old=u(rid,uid)['institution'];alt='undetermined' if old['type']=='norm_candidate' else 'norm_candidate'
    add(rid,uid,'institution.type_alternatives',sorted(set(old['type_alternatives']+[alt])-{old['type']}),'D05,Q015,Q036','The supplied evidence permits technical-maintenance and proposed-social-expectation readings.')
add('F03_v04_r1','U24','institution.rationale','The terse maintenance request may express expected contributor conduct or technical necessity. The source does not select between them. A proposed norm need not recur or already be shared; authority and institutional obligation remain unestablished.','D05,Q015','Recurrence and prior sharing are not v0.4 prerequisites for a norm candidate.')

# D06 make linked layers visible without substituting a different focal object.
for uid,field in [('S10','target_level_alternatives'),('S17','target_level_alternatives'),('S17','observed_level_alternatives')]:
    add('F01_v04_r1',uid,field,['operational'],'D06,Q045,Q051','Operational conduct is a supported embedded layer within the proposed recurring arrangement.')
add('F01_v04_r1','S17','level_rationale','The focal analysis is a proposal to choose a recurring developer-selection arrangement, conditional on the availability-based loop. Its embedded act of selecting test versions is operational. The visible exchange can also be read as ordinary engineering review rather than institutional procedure selection.','D06,Q045','State which analytical layer receives the primary label.')

# D07 preserve focal-scope alternatives rather than manufacture Boolean unanimity.
for rid,uid in [('F03_v04_r1','U01'),('F03_v04_r2','F03-U01'),('F03_v04_r3','F03-U01')]:
    add(rid,uid,'alternative_interpretation',u(rid,uid)['alternative_interpretation']+' A readiness objection can target the premise of offering/exposing the feature; when the focal claim is limited to the prepared artifact, the objection concerns the broader proposal. These scope readings change dispute projection without changing the observed checkbox facts.','D07,Q019','Retain the offered-feature and artifact-description alternatives explicitly.')
add('F01_v04_r3','C15','alternative_interpretation',u('F01_v04_r3','C15')['alternative_interpretation']+' A prospective redesign may challenge continued application of the built-copy requirement, but it does not refute the current fixed-list implementation\'s technical prerequisite.','D07,Q040','Distinguish current truth from prospective continued application.')
import_changes('D07',lambda p:p['run_id'].startswith('F01'))

# D08 choose the directly supported clarifying relation for the quoted cost concern.
for rid,idx,fr,to in [('F01_v04_r3',11,'C13','C12'),('F01_v04_r1',8,'S14','C07'),('F01_v04_r2',18,'U13','C05')]:
    rel=anns[rid]['relations'][idx]
    # Confirm endpoints before applying: indices and unit IDs must refer to this specific exchange.
    assert {rel['from_unit_id'],rel['to_unit_id']}=={fr,to}
    for field,val in [('type','clarifies'),('from_unit_id',fr),('to_unit_id',to),('rationale','The pruning option responds to and clarifies the quoted append-only cost concern. Uptake remains a defensible alternative if the question is interpreted as an implicit request for a removal plan; no removal, implementation, or causal effect is established.')]:
        add(rid,None,f'relations[{idx}].{field}',val,'D08,Q042','Prefer textual clarification while preserving the inferred-invitation alternative.')
for field,val in [('type','temporal'),('from_unit_id','C01'),('to_unit_id','C02'),('basis','context_inferred'),('rationale','The frozen source creation timestamps place release-risk speculation at 2022-11-28T08:12:21+00:00 before the separate pause proposal at 2022-11-28T13:32:40+00:00. This ordering does not establish an initiating request, reliable reply attribution, a wording-edit sequence, or causal adoption. An implicit-invitation uptake reading remains an alternative.')]:
    add('F01_v04_r3',None,'relations[1].'+field,val,'D08,Q043','All three final reviewers prefer temporal order for the weakly attributed response relation.')

# D09 remove categorical software identity from all propagated descriptions of this unit.
for p in B['D09']['recommended_changes']:
    add(p['run_id'],p['unit_id'],p['path'],p['new_value'],'D09,Q022','The source supplies a pronoun and condition, but does not identify its internal software referent uniquely.')
add('F01_v04_r2','U06','alternative_interpretation','The incorrectly listed review is the likely linguistic antecedent; the comment or displayed listing remain possible. The bot announces a conditional next-update response, with no observed execution.','D09,Q022','Preserve the plausible preferred referent without claiming certainty.')

# D10 retain primary unitizations/types while adding the panel-supported alternatives.
for gid,desired in [('Q047','strategy_candidate'),('Q048','strategy_candidate'),('Q049','norm_candidate')]:
    g=next(x for x in read(R/'inputs/analysis/reconciliation.json')['groups'] if x['group_id']==gid)
    for item in g['affected']:
        if item['condition']!='v04':continue
        for uid in item['unit_ids']:
            rid=item['run_id'];old=u(rid,uid)['institution'];other='undetermined' if old['type']==desired else desired
            add(rid,uid,'institution.type_alternatives',sorted(set(old['type_alternatives']+[other])-{old['type']}),'D10,'+gid,'Retain the articulated-method or proposed-restraint reading and the one-off technical-advice alternative.')
for uid in ['C09','C20','C21','C28']:
    kind='a proposed restraint on integration' if uid=='C28' else 'an articulated testing method'
    add('F01_v04_r3',uid,'institution.rationale',f'The primary view retains an engineering-preference interpretation. The utterance also supports {kind}, retained as a type alternative. Absence of authority rules out a rule claim but does not itself rule out a strategy or norm candidate; shared acceptance and implementation remain unestablished.','D10','Replace an incomplete authority-based justification with the actual type boundary.')
for p in B['D10']['recommended_changes']:
    if p.get('unit_id')=='U23' and p['path'] in ['parse_mode','components']:
        add(p['run_id'],p['unit_id'],p['path'],p['new_value'],'D10,Q025a','Adopt the panel-preferred literal action representation; the original reconstructed avoid-rushing parse remains a defensible alternative, not a retroactive error.')
add('F01_v04_r2','U23','alternative_interpretation',u('F01_v04_r2','U23')['alternative_interpretation']+' A pragmatic avoid-rushing action with reconstructed roles remains semantically defensible. Deliberation selected the supplied not-rush-merging action for the adjusted view; this is a representation choice, not an error finding against the original parse.','D10,Q025a','Preserve the earlier source-reviewed alternative even after choosing another representation.')

(R/'analysis/panel_patch_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
print('Planned post-discussion field edits',len(plan))
