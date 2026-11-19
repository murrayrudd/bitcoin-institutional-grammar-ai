import json,copy,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
p=json.loads((R/'packet.json').read_text());t={e['source_id']:e['text'] for e in p['entries']}
a=json.loads((R/'annotation.json').read_text());u={v['unit_id']:v for v in a['units']};n=json.loads((R/'review_notes.json').read_text());log=[]
def ev(s,q,start=None):
 if start is None:start=t[s].index(q)
 assert t[s][start:start+len(q)]==q
 return {'source_id':s,'span':{'start':start,'end':start+len(q),'quote':q}}
def change(id,reason,meaning,fn,category='source_self_review'):
 before=copy.deepcopy(u[id]);fn(u[id]);after=copy.deepcopy(u[id]);log.append({'change_id':f'R{len(log)+1:03}','phase':category,'unit_ids':[id],'description':reason,'changes_meaning':meaning,'before':before,'after':after})
def cmp(id,sym,idx=0):return [c for c in u[id]['components'] if c['symbol']==sym][idx]
def anch(id,sym,q,start=None,note=None):
 c=cmp(id,sym);c['evidence']=[ev(u[id]['source_id'],q,start)]
 if note:c['inference_note']=note
# First mechanical feedback repairs: no exceptions are used to hide an unrelated substring.
fixes=[('A115_forum','F','is',t['32359-115'].index('is a pull'),'Anchor the copula is rather than the substring in this.'),('A115_repeat','A','you',t['32359-115'].index(", you don't")+2,'Anchor the subject you rather than the substring in your.'),('A178_keep','Cex','in',t['32406-178'].index('the option in seems')+len('the option '),'Anchor the particle in following option rather than a substring in maintaining.'),('A252_debate','Bdir','so',t['32406-252'].index('do so on')+3,'Anchor the anaphoric so rather than the substring in also.'),('A714_equivalence','F','is',t['32714-014'].index('*is*')+1,'Anchor the emphasized copula rather than the substring in discouragement.'),('A018_call','E',"that's",None,'Use the full contraction as evidence for its demonstrative subject; preserve the decomposition in an explicit note.')]
for id,sym,q,start,reason in fixes:
 change(id,reason,False,lambda x,id=id,sym=sym,q=q,start=start:anch(id,sym,q,start,note='The demonstrative that is the subject in the contraction that\'s; the full contraction is anchored without a token-fragment exception.' if id=='A018_call' else None),'checker_mechanical')

# One source-based review, covering every focal record, all units and claims.
change('A115_spam','Keep the spam rationale in institutional interpretation rather than misreading other than as an exception/constraint on the inferred avoid action.',True,lambda x:(x.update(components=[c for c in x['components'] if c['symbol']!='Cex']),x['institution'].update(rationale=x['institution']['rationale']+' The claimed spam effect is the rationale for discouragement, not an exception permitting the conduct.')))
change('A115_forum','Anchor the separate-episode recognition to the explicit no-vote/forum-function statement, not solely the technical-content clause.',False,lambda x:x['institution']['recognition'][0].update(evidence=[ev('32406-169','The goal is *not* to have everyone "register" their "vote". It is simply a best-effort overview to have a clickable link to every reviewer\'s most recent review comment.')]))
change('A227_majority','Do not automatically classify the challenger as disputed merely because it conflicts with an earlier position. No supplied reply challenges this majority claim itself.',True,lambda x:x['institution'].update(standing='text_only',dispute_present=False,rationale='The author assigns decisive standing to a majority and denies that argument decides this debate. This is an expressed competing conception; no reply challenging this particular proposition, defined electorate, or formal decision procedure is supplied.'))
change('A115_merit','Keep supported merit weighting separate from the later competing majority criterion; mark an inferred challenge to its application without removing its independent support.',True,lambda x:x['institution'].update(dispute_present=True))
# Wrong antecedent would change the informational object.
change('A148_document','Remove the over-specific docstring antecedent: it more plausibly denotes the property to be tested/documented, and the parent inline context is absent.',True,lambda x:(x.update(components=[c for c in x['components'] if c['symbol']!='Bdir,p'],uncertainty_reason='The referent of it is not fully resolved; it likely denotes the asserted size/test property rather than the docstring itself.'),anch('A148_document','Bdir','it',t['32406-148'].index(', it probably')+2)))
change('A149_stay','Use the I in the actual preference predicate I\'d rather not switch back, matching the existing role explanation.',False,lambda x:anch('A149_stay','A','I',t['32406-149'].index("I'd rather")))
change('A178_definition','Retain personal epistemic stance in the source/rationale, not as an execution constraint on the definition.',False,lambda x:(x.update(components=[c for c in x['components'] if c['symbol']!='Cex']),x['institution'].update(rationale=x['institution']['rationale']+' Personally, I think marks the offered interpretation as the speaker\'s view.')))
change('A178_low','Narrow the advice unit to its own clause and retain the attributed-majority qualification as epistemic stance, not an execution constraint; marking deprecated remains a separate proposition.',False,lambda x:(x.update(span=ev('32406-178','I think the vast majority of developers contributing to core would recommend not setting this option to a lower value than the default')['span'],components=[c for c in x['components'] if not(c['symbol']=='Cex' and c['text'].startswith('I think'))]),x['institution'].update(evidence=[ev('32406-178','I think the vast majority of developers contributing to core would recommend not setting this option to a lower value than the default')])) )
# Focal action here is selecting a decision, not prescribing removal unconditionally.
def tradeoff(x):
 x['parse_mode']='pragmatic';x['components']=[]
 for sym,txt,q in [('I','decide','Whether (or when) the option should also be removed rather than just deprecated depends'),('Bdir','whether or when to remove the option rather than merely deprecate it','Whether (or when) the option should also be removed rather than just deprecated'),('Cex','by weighing user appreciation, support effort, and perhaps harmful network effects','the trade-off between how many users continue to appreciate the feature, and how much effort it is to continue to support the code, and, perhaps, whether the presence of the feature is resulting in any harmful network effects')]:
  x['components'].append({'symbol':sym,'text':txt,'basis':'context_inferred','evidence':[ev(x['source_id'],q)],'inference_note':'The depends-on construction is reconstructed as a decision criterion. The embedded should does not impose removal; its complete whether/when object and tentative third criterion are preserved.','occurrence_role':'semantic_inference'})
 x['alternative_interpretation']+=' The literal grammar states a dependency; the selected regulative parse reconstructs an instruction to decide using these criteria.'
change('A178_tradeoff','Reconstruct the decision-criterion action explicitly and remove the misleading positive should-remove parse. Preserve whether, when, rather-than, and perhaps.',True,tradeoff)
change('A004_window','Remove the isolated assuming component; it introduces the endorsement condition and is not itself a complete activation condition for a reconstructed delay recommendation.',False,lambda x:(x.update(components=[c for c in x['components'] if c['symbol']!='Cac']),x['institution'].update(rationale=x['institution']['rationale']+' The long window is expressly a condition of this speaker\'s ACK.')))
change('A067_retain','Represent the relative clause as a property of the options, not an execution constraint on retaining them; mark the transformed target relation as inferred.',False,lambda x:[c.update(symbol='Bdir,p',basis='context_inferred',occurrence_role='semantic_inference',inference_note='The relative clause identifies the usefulness claimed for these options; it modifies the reconstructed retention target, not the manner of retention.') for c in x['components'] if c['symbol']=='Cex'])
change('A252_debate','Trim the positive routing unit before the separately represented negative-duty clause; the existing AND relation retains their full coordination.',False,lambda x:x.update(span=ev('32406-252','If you want to debate this comment please also do so on https://github.com/bitcoin-core/meta/')['span']))

# Avoid concealing independent alternative actions in execution constraints.
def new_from(id,newid,q,parent=None):
 x=copy.deepcopy(u[id]);x['unit_id']=newid;x['span']=ev(x['source_id'],q)['span'];x['parent_unit_id']=parent;x['components']=[];x['institution']['evidence']=[ev(x['source_id'],q)];x['institution']['recognition']=[];x['disposition_events']=[];a['units'].append(x);u[newid]=x;return x
def c(id,sym,txt,q=None,basis='explicit',role='local',note='',start=None):
 x=u[id];q=q or txt
 if start is None:
  z=t[x['source_id']].find(q,x['span']['start'],x['span']['end']);start=z if z>=0 else None
 x['components'].append({'symbol':sym,'text':txt,'basis':basis,'evidence':[ev(x['source_id'],q,start)],'inference_note':note,'occurrence_role':role})
def container(id):
 x=u[id];x.update(record_role='container',grammar='not_institutional',components=[],speech_act='other',parse_mode='literal',deontic_force='nondeontic',statement_target_level='not_applicable',observed_action_level='not_applicable');x['institution'].update(type='not_applicable',standing='not_applicable',dispute_present=False,recognition=[],authority_evidence=[],rationale='Structural container preserves the coupled/alternative framework without adding another proposition.')
def relation(fr,to,typ,s,q,scope='actions',rationale=''):
 a['relations'].append({'from_unit_id':fr,'to_unit_id':to,'type':typ,'basis':'explicit','evidence':[ev(s,q)],'rationale':rationale,'logic_scope':scope})
def group_log(before,ids,why,meaning):
 log.append({'change_id':f'R{len(log)+1:03}','phase':'source_self_review','unit_ids':ids,'description':why,'changes_meaning':meaning,'before':before,'after':[copy.deepcopy(u[i]) for i in ids]})

before=copy.deepcopy(u['A213_defaults'])
new_from('A213_defaults','A213_keep_defaults','let the defaults be as it is','A213_defaults');c('A213_keep_defaults','I','let');c('A213_keep_defaults','Bdir','the defaults');c('A213_keep_defaults','Cex','be as it is')
new_from('A213_defaults','A213_allow_increase','allow it to be increased for those who chose to increase it','A213_defaults');c('A213_allow_increase','I','allow');c('A213_allow_increase','Bdir','it to be increased');c('A213_allow_increase','Bind','those who chose to increase it')
u['A213_allow_increase']['deontic_force']='permission';u['A213_allow_increase']['institution']['rationale']='The articulated method proposes permission for willing users to increase the setting; it is not evidence that a standing rule already grants this discretion.'
container('A213_defaults');relation('A213_keep_defaults','A213_allow_increase','AND','32359-213','let the defaults be as it is and allow it to be increased for those who chose to increase it',rationale='The proposed conservative method combines unchanged defaults with optional user increases; users are not required to increase anything.')
group_log(before,['A213_defaults','A213_keep_defaults','A213_allow_increase'],'Separate unchanged defaults from permission to increase the setting; preserve the same coupled method and its OR alternative.',False)

before=copy.deepcopy(u['A178_patch'])
new_from('A178_patch','A178_patch_back','patch it back in','A178_patch');c('A178_patch_back','I','patch');c('A178_patch_back','Bdir','it');c('A178_patch_back','Cex','back in')
new_from('A178_patch','A178_derivative','use a derivative that does that for them','A178_patch');c('A178_derivative','I','use');c('A178_derivative','Bdir','a derivative that does that for them')
for id in ['A178_patch_back','A178_derivative']:
 c(id,'A','they',role='shared_scope',note='The explicit subject they scopes both alternative actions; users is the local antecedent.');c(id,'Cac','even if it does get removed from core, if users actually want it',role='shared_scope',note='Both conditions are shared by the coordinated capability alternatives; no institutional permission is inferred from can.')
container('A178_patch');relation('A178_patch_back','A178_derivative','OR','32406-178','patch it back in or use a derivative that does that for them',rationale='The source offers alternative user capabilities, not obligations to do both.')
group_log(before,['A178_patch','A178_patch_back','A178_derivative'],'Separate the two alternative user actions so use a derivative is not mislabeled as an execution constraint of patching. Preserve capability-versus-permission uncertainty.',False)

# Supporting original alternatives need unambiguous action recoverability.
for old,specs in [('A711_a',[('A711_a_recommend','recommend the option not be used','recommend','the option not be used',None),('A711_a_mark','mark it deprecated','mark','it','deprecated')]),('A711_b',[('A711_b_notmark','not mark it deprecated','not mark','it','deprecated'),('A711_b_user','leave it up to the user to decide whether to use the option, without making any particular recommendation','leave','it','up to the user to decide whether to use the option, without making any particular recommendation')])]:
 before=copy.deepcopy(u[old]);kids=[]
 for newid,q,act,obj,constraint in specs:
  new_from(old,newid,q,old);kids.append(newid);c(newid,'A','we',role='shared_scope',note='Explicit we in the enclosing either/or proposal scopes this branch.');c(newid,'D','should',role='shared_scope',note='Advisory should scopes the offered branch rather than both alternatives.');c(newid,'I',act);c(newid,'Bdir',obj)
  if constraint:c(newid,'Cex',constraint)
  u[newid]['institution']['recognition']=copy.deepcopy(before['institution']['recognition'])
 container(old);relation(kids[0],kids[1],'AND','32714-011',before['span']['quote'],rationale='These coordinated actions form one alternative bundle; the separate OR relation links the two bundles.')
 group_log(before,[old]+kids,'Split the independent actions inside this quoted framework while retaining their coupled branch and broader endorsement scope.',False)
change('A711_c','Preserve advisory should from shared scope and put local negation with not try, rather than treating not alone as the complete deontic.',False,lambda x:x.update(components=[c for c in x['components'] if c['symbol'] not in ['D','I']]))
c('A711_c','D','should',role='shared_scope',note='Should in the enclosing recommendation scopes the coordinated negative alternative.');c('A711_c','I','not try')
log[-1]['after']=copy.deepcopy(u['A711_c'])

# Screened quoted camp claims remain uncertain, rather than quietly excluding plausible prescriptions.
before=copy.deepcopy(u['A227_camps'])
base=copy.deepcopy(u['A213_configure'])
def camp(id,q,act,obj=None,constraint=None):
 x=copy.deepcopy(base);x.update(unit_id=id,source_id='32359-227',span=ev('32359-227',q)['span'],parent_unit_id=None,scope='general',speech_act='asserted',parse_mode='literal',deontic_force='recommendation',components=[],confidence='unresolved',complexity_flags=['none'],alternative_interpretation='This is the external quotation\'s characterization of a camp, possibly a rhetorical caricature, not an independently verified proposal or endorsement by this commenter.',uncertainty_reason='The original source and camp members are not supplied; the distinction between reporting a belief and advancing a prescription is unresolved.')
 x['institution'].update(type='undetermined',standing='text_only',dispute_present=False,rationale='A reported normative stance in an external quotation is retained as a plausible candidate only. Its expression is evidenced; neither authenticity of the characterization, adoption, nor the current commenter\'s endorsement of this camp is established.',evidence=[ev('32359-227',q)],recognition=[],authority_evidence=[])
 x['disposition_events']=[];a['units'].append(x);u[id]=x
 c(id,'A','we');c(id,'D','should');c(id,'I',act)
 if obj:c(id,'Bdir',obj)
 if constraint:c(id,'Cex',constraint)
camp('A227_proactive','we should remain proactive towards spam filtration, despite the lack of a 100% effective solution','remain proactive','spam filtration','despite the lack of a 100% effective solution')
camp('A227_capitulate','we should capitulate to spammers, and remove all efforts to slow down / reduce spam','capitulate','spammers')
u['A227_capitulate']['complexity_flags']=['compound'];c('A227_capitulate','I','remove');c('A227_capitulate','Bdir','all efforts to slow down / reduce spam');u['A227_capitulate']['alternative_interpretation']+=' The two explicit action components preserve the quoted coupling; this is not a new author recommendation to capitulate.'
group_log(before,['A227_camps','A227_proactive','A227_capitulate'],'Retain two externally reported camp stances as unresolved candidates, with explicit warnings that the quotation may be an adversarial characterization rather than actual prescriptions. No endorsement/adoption is inferred.',True)

# Per-focal notes and access/repair trail are part of the same review pass.
nt={z['source_id']:z for z in n['per_focal_source']}
nt['32359-227']['reasoning']='A majority-decision claim is distinct from two externally reported camp stances retained as unresolved candidate prescriptions. The latter are attributed characterizations, not independent proof of what either camp proposes or what the commenter endorses. The majority claim challenges merit weighting but is not itself marked disputed without a supplied reply.'
nt['32359-227']['consequential_alternative_interpretations']+=' The quoted camp stances may be rhetorical reports rather than institutional propositions; they remain explicit unresolved candidates rather than suppressed alternatives.'
nt['32359-213']['reasoning']='The external quotation includes an entitlement claim and a conservative method with separate unchanged-default and optional-increase actions; the author supplies a high-default alternative. The why-removed question remains informational context.'
nt['32406-178']['reasoning']='Definition, navigation, attributed advice, marking deprecated, future decision criteria, current retention, and two alternative user capabilities are separated. The decision criterion is explicitly pragmatic; should in its embedded whether-question does not require removal.'
nt['32406-148']['missing_context']+=' The referent of it in the documentation question is not resolved to a docstring; it may mean the tested property.'
nt['32714-013']['reasoning']='No new statement: qualified Concept ACK and agreement with a repeated supplied original. Its original framework has separate actions within two alternative bundles, without treating branch agreement as selection or recognized obligation.'
for sc in a['entry_screening']:
 ids=[x['unit_id'] for x in a['units'] if x['source_id']==sc['source_id']];sc['unit_ids']=ids
 sc['disposition']='candidate' if any(u[i]['record_role']=='statement' for i in ids) else ('empty' if not t[sc['source_id']].strip() else 'context_only')
 if sc['source_id'] in nt:sc['reason']=nt[sc['source_id']]['reasoning']
# Record all self-authored and evidence files read during review. No unassigned source is accessed.
more=['annotation.first_complete.json','annotation.json','checks.first_complete.json','review_notes.json','self_review.py']
for f in more:n['research_access_record'].append({'path':str(R/f),'purpose':'Preserved/self-authored annotation, first checker feedback, or single self-review helper','access':'read'+('/execute' if f.endswith('.py') else ''),'sha256':hashlib.sha256((R/f).read_bytes()).hexdigest()})
n['self_review']={'completed':True,'passes':1,'scope':'All 24 focal records and all retained units, component roles/anchors, relations, recognition/disposition events, outcomes and mechanisms checked against the same frozen packet. No outside semantic feedback.','semantic_feedback_from_others':False,'remaining_alternatives':a['episode_summary']['unresolved_questions'],'checker_flags_reviewed':'All outside-unit references have explicit scope/antecedent notes. Six initial token-fragment errors were corrected by selecting the grammatical occurrence; none was waived.'}
repair={'run_id':'R12_A','first_complete_sha256':hashlib.sha256((R/'annotation.first_complete.json').read_bytes()).hexdigest(),'changes':log,'meaning_changing_changes':sum(z['changes_meaning'] for z in log),'mechanical_or_meaning_preserving_changes':sum(not z['changes_meaning'] for z in log),'self_review_passes':1,'outside_semantic_feedback':False}
(R/'annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n');(R/'review_notes.json').write_text(json.dumps(n,ensure_ascii=False,indent=2)+'\n');(R/'repair_log.json').write_text(json.dumps(repair,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'changes':len(log),'meaning_changing':repair['meaning_changing_changes'],'units':len(a['units']),'statements':sum(x['record_role']=='statement' for x in a['units'])},indent=2))
