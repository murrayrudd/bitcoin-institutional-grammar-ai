import json
from pathlib import Path
from copy import deepcopy
p=Path('.')
a=json.loads((p/'annotation.json').read_text())
packet=json.loads((p/'packet.json').read_text())
texts={e['source_id']:e['text'] for e in packet['entries']}
U={u['unit_id']:u for u in a['units']}
log=json.loads((p/'repair_log.json').read_text())

def anchor(s,q,start=0):
 st=texts[s].index(q,start);return {'source_id':s,'span':{'start':st,'end':st+len(q),'quote':q}}
def change(uid,path,before,after,reason,meaning=False,evidence_basis=False,effect='convention_deviation',diagnosis='execution_failure'):
 log.append({'change_id':'S'+str(1+sum(x['phase']=='source_self_review' for x in log)).zfill(2),'phase':'source_self_review','unit_id':uid,'path':path,'before':deepcopy(before),'after':deepcopy(after),'meaning_changed':meaning,'evidence_basis_changed':evidence_basis,'diagnosis':diagnosis,'effect':effect,'reason':reason})
u=U['U09'];c=u['components'][1]
old=deepcopy(c['evidence'])
c['evidence']=[anchor(u['source_id'],'red text',u['span']['start'])]
change('U09','components/1/evidence',old,c['evidence'],'Source review found the semantic-inference anchor pointed to red text in the preceding negative assessment. The chosen apply-red-text predicate concerns the non-replacable case, so the anchor now uses red text in that clause.',evidence_basis=True,effect='evidence_basis_error')
u=U['U04'];c=u['components'][3]
old=deepcopy(c)
c['symbol']='Cex'
c['inference_note']='The explicit until clause bounds the duration of inferred withholding. It is an execution-time constraint, not a trigger to start withholding, and can still means technical capability.'
change('U04','components/3',old,c,'Under the selected withhold-exposure action, until replacement is possible specifies the temporal bound of execution. The readiness condition and force remain unchanged.',diagnosis='defensible_alternative_representation')
for uid in ['U09','U10']:
 u=U[uid];s=u['source_id']
 ev=anchor(s,'should get',u['span']['start']) if uid=='U09' else anchor(s,'should',u['span']['start'])
 if uid=='U09': ev['span']['end']=ev['span']['start']+6;ev['span']['quote']='should'
 c={'symbol':'D','text':'should','basis':'context_inferred','evidence':[ev],'inference_note':'Should is lexically supplied for the described UI state/action. Its role as the recommendation modal of the reconstructed editorial action is inferred; advisory force is unchanged.','occurrence_role':'semantic_inference','governing_span':{'source_id':s,'span':deepcopy(u['span'])}}
 u['components'].append(c)
 change(uid,'components/'+str(len(u['components'])-1),None,c,'Represent the supplied should modal explicitly at the reconstructed editorial layer rather than leaving it only in force/qualification fields. Its changed-predicate role is labeled inferred.',effect='convention_deviation')
u=U['U16'];ev=u['institution']['recognition'][0];old=deepcopy(ev)
ev['target']='unresolved'
ev['rationale']='gmaxwell expresses ordinary interest in the add-output idea. The textual referent is plausible, but the distinct replacement-workflow decision object has no established canonical identifier. object_id is unknown, not inapplicable; target is therefore unresolved. This is not institutional expectation recognition.'
change('U16','institution/recognition/0',old,ev,'An unidentified required decision object must retain unresolved target status, even when the conversational method referent is recognizable.',meaning=True,evidence_basis=True,effect='evidence_basis_error')
u=U['U18'];q=u['proposition']['qualifiers'][0];old=deepcopy(q)
q['attachment']='scope_note'
q['rationale']='The focal clause explicitly specifies the additional-output workflow. That scope is preserved as this visible note; no separate grammar component encodes it.'
change('U18','proposition/qualifiers/0',old,q,'The workflow qualification is supported but was mislabeled as carried by a component. It is now accurately represented as an attached scope note.',effect='convention_deviation')
u=U['U22'];old=u['proposition']['summary']
new='gmaxwell suggests a [send immediately] option described as delaying sending, avoiding extra just-in-case transactions if amended within the timeout, and potentially allowing abort before it was initially set, as worded in the source.'
u['proposition']['summary']=new;u['level_evidence']['target_activity']=new
change('U22','proposition/summary and level_evidence/target_activity',old,new,'The prior summary normalized initially set to initial sending. The supplied wording is now retained because its exact referent cannot be verified.',meaning=True,effect='coverage_or_scope_loss')
old=u['uncertainty_reason'];u['uncertainty_reason']=old+' The phrase initially set is not silently corrected to initially sent; the timing referent remains uncertain.'
change('U22','uncertainty_reason',old,u['uncertainty_reason'],'Attach the ambiguity in initially set to the proposition explicitly.',meaning=False,effect='coverage_or_scope_loss')
o=a['episode_summary']['observed_outcomes'][1]
old=deepcopy(o)
o['claim']=o['claim'].replace('still contains','contains')
o['claim_parts'][1]['text']=o['claim_parts'][1]['text'].replace('still contains','contains')
change(None,'episode_summary/observed_outcomes/1',old,o,'A retained head patch establishes its contents, not persistence through an unobserved revision sequence. Removed still to avoid implying a known before/after chronology.',meaning=True,effect='evidence_basis_error',evidence_basis=True)
(p/'annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
(p/'annotation.final.json').write_bytes((p/'annotation.json').read_bytes())
(p/'repair_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_review_changes':sum(x['phase']=='source_self_review' for x in log),'total_changes':len(log)}))
