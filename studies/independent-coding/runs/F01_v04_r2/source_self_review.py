from pathlib import Path
import json,copy
p=json.loads(Path('packet.json').read_text());es={e['source_id']:e for e in p['entries']};a=json.loads(Path('annotation.json').read_text());u={x['unit_id']:x for x in a['units']};log=json.loads(Path('repair_log.json').read_text())
def ev(s,q=None,start=0):
 t=es[s]['text'];q=t if q is None else q;i=t.index(q,start);return {'source_id':s,'span':{'start':i,'end':i+len(q),'quote':q}}
def ref(n):return {'source_id':u[n]['source_id'],'span':u[n]['span']}
def change(n,fields,func,why,evidence,meaning=False,effect='convention deviation'):
 before={k:copy.deepcopy(u[n][k]) for k in fields};func();after={k:copy.deepcopy(u[n][k]) for k in fields}
 if before==after:return
 log.append({'change_id':'S%02d'%(1+sum(x['phase']=='source_self_review' for x in log)),'phase':'source_self_review','unit_id':n,'fields':fields,'meaning_changes':meaning,'effect':effect,'diagnosis':'execution failure under an existing rule' if effect!='unresolved' else 'criterion ambiguity','before':before,'after':after,'rationale':why,'evidence':evidence})
def c(sym,text,e,basis='context_inferred',role='semantic_inference',note='',gov=None):return {'symbol':sym,'text':text,'basis':basis,'evidence':[e],'inference_note':note,'occurrence_role':role,'governing_span':gov or e}
# Do not modify the fixed inputs or the checker to conceal its source-field mismatch.
change('U01',['components'],lambda:u['U01'].update(components=[c('I','repeat',ref('U01'),note='Elliptical nominal description reconstructed as repetition of a method.'),c('Bdir','the release-addition procedure',ev('pr26586:body','The same procedure'),note='The nominal procedure becomes object of reconstructed repeat; its release-addition meaning is supported by the cited predecessors and PR title.',gov=ref('U01'))]),'Separate the reconstructed action from its object without changing the asserted method.',[ref('U01')])
def fix_navigation():
 u['U02']['proposition']['decision_object_id']=None;u['U02']['proposition']['identity_evidence']=[]
 u['U02']['proposition']['domain']='Navigation to the two identified predecessor commits; no single decision object applies.'
 u['U02']['alternative_interpretation']+=' The object ID is null because this navigation has two distinct commit targets, not the containing PR as its decision object.'
change('U02',['proposition','alternative_interpretation'],fix_navigation,'The containing PR was not the actual target of the two-commit navigation. Preserve both complete commit IDs and leave the single decision-object field inapplicable.',[ref('U02')],True,'changed institutional meaning')
def fix_guide_identity():
 u['U04']['alternative_interpretation']+=' The null decision object is inapplicable to a decision proposal; the navigation target is the mutable master guideline, whose exact contemporaneous revision is unknown.'
change('U04',['alternative_interpretation'],fix_guide_identity,'Explain the null object and distinguish the linked mutable guide from the supplied pinned copy.',[ref('U04')])
# Preserve original communicative function as well as inferred force.
for n,sp,why in [('U10','asserted','The literal sentence asserts a sufficiency rationale; the add recommendation remains a pragmatic interpretation.'),('U11','asserted','The literal utterance expresses preference; the inferred use recommendation remains distinct.'),('U19','proposed','This is a direct conditional suggestion to update the PR, so the project speech-act convention favors proposed.')]:
 change(n,['speech_act'],lambda n=n,sp=sp:u[n].update(speech_act=sp),why,[ref(n)])
for n,sp in [('Q01','technical_description'),('Q02','technical_description'),('Q03','technical_description'),('Q04','technical_description'),('Q05','question'),('Q06','technical_description'),('Q07','technical_description'),('Q08','question')]:
 change(n,['speech_act'],lambda n=n,sp=sp:u[n].update(speech_act=sp),'Repeated occurrence retains the original technical claim or question function; quotation does not turn it into a new assertion or endorsement.',[ref(n)])
# Distinguish technical redesign from an institutional choice of recurring arrangements.
for n in ['U11','U13','U15','U16','U17','U18']:
 def setlevel(n=n):
  u[n]['observed_action_level']='operational';u[n]['observed_level_alternatives']=['collective_choice']
  u[n]['level_rationale']='The visible act is an ordinary engineering/review suggestion about test design or possible maintenance. It may contribute to deliberation over a recurring testing arrangement, retained as a collective-choice alternative; technical configurability alone does not establish that higher-level institutional activity.'
 change(n,['observed_action_level','observed_level_alternatives','level_rationale'],setlevel,'The initial primary observed level overread technical suggestions as established deliberation over an institutional arrangement. Retain the higher-level reading as an explicit alternative.',[ref(n)],True,'changed institutional meaning')
def fix_shared():
 s='pr26586:comments:15';g=ev(s,"As we've done before, we could just leave the PR open and occasionally rebase it.")
 e=ev(s,'we',es[s]['text'].index('we could'))
 u['U22']['components'].append(c('A','we',e,'explicit','shared_scope','The explicit main-clause we governs both leave and rebase; it is outside this separately extracted child.',g))
change('U22',['components'],fix_shared,'Recover the explicitly shared actor from the governing coordination instead of relying only on the linked-scope note.',[ref('U21'),ref('U22')],False,'evidence-basis error')
def fix_apply():
 u['U29']['components']=[c('I','apply',ev('pr26586:review_comments:1','The same goes'),note='Apply is reconstructed from the elliptical same-goes extension.',gov=ref('U29')),c('Bdir','the same release-selection criterion',ev('pr26586:review_comments:1','The same'),note='The inherited criterion, explicitly resolved through U25, becomes the object of reconstructed apply.',gov=ref('U29')),c('Bind','the other versions in this file',ev('pr26586:review_comments:1','the other versions in this file'),note='The versions are the distinct targets to which the criterion is applied; this role is inferred under apply.',gov=ref('U29'))]
change('U29',['components'],fix_apply,'Separate apply from the criterion object and retain the other versions as the distinct affected targets.',[ref('U29'),ref('U25')])
def fix_exclude():
 u['U33']['components'][0]['text']='exclude'
 u['U33']['components'].append(c('Cex','from this PR\'s scope',ev('pr26586:review_comments:2','outside of scope for this PR'),note='The exclusion boundary is reconstructed from the literal outside-scope predicate.',gov=ref('U33')))
change('U33',['components'],fix_exclude,'Keep the exclude action separate from its stated PR-scope boundary.',[ref('U33')])
# Same actor's explicit application is maintained commitment, not interpersonal recognition.
def same_actor():
 u['U25']['institution']['recognition'].append({'kind':'expectation_recognition','target':'this_proposition','basis':'context_inferred','evidence':[ref('U29'),ref('U25')],'rationale':'The same actor says the same criterion goes for the other versions in this file, explicitly extending the criterion as the relevant standard. This supports only maintained commitment within one episode.','mode':'same_actor_restatement','speaker_relation':'same_actor','independence_key':p['pr_url'],'object_id':p['pr_url'],'identity_evidence':[ev('pr26586:supplement_metadata',p['pr_url'])]})
 u['U25']['institution']['standing_profile']['recognition']='same_actor_only'
change('U25',['institution'],same_actor,'The same-goes extension is a qualifying same-actor restatement of the criterion, missed in the first recognition inventory. It establishes no interpersonal or project-wide acceptance.',[ref('U25'),ref('U29')],True,'coverage or scope loss')
# Narrow governing predicates where a matrix think or other clause could be confused.
change('U09',['components'],lambda:[x.update(governing_span=ev('pr26586:comments:4','we should add every major release')) for x in u['U09']['components']],'The governing clause for we/should/add/releases is the embedded action clause, not the speaker\'s I think predicate.',[ref('U09')],False,'evidence-basis error')
# Explicit patch comments bind version numerals to their retained version names.
patch=ev('pr26586:patch:0')
def augment(v):
 if isinstance(v,dict):
  if 'evidence' in v and isinstance(v['evidence'],list) and any(isinstance(e,dict) and e.get('source_id')=='pr26586:patch:0' for e in v['evidence']) and patch not in v['evidence']:v['evidence'].append(copy.deepcopy(patch))
  for x in list(v.values()):augment(x)
 elif isinstance(v,list):
  for x in v:augment(x)
before=copy.deepcopy(a);augment(a)
log.append({'change_id':'S%02d'%(1+sum(x['phase']=='source_self_review' for x in log)),'phase':'source_self_review','unit_id':None,'fields':['patch-based application/disposition evidence','episode_summary claim_parts and parent evidence'],'meaning_changes':False,'effect':'evidence-basis error','diagnosis':'execution failure under an existing rule','before':'Numeric test-version anchors plus archive version names.','after':'Existing anchors plus the full retained test patch, including explicit v24.0.1 and v23.0 comment labels.','rationale':'Make every version-name claim inspectable from source labels as well as encoded integers; preserve exact edit/integration scope.','evidence':[patch]})
# Qualifiers and type uncertainty for broader boundary candidates.
for n in ['U01','U11','U12','U17','U18','U21','U22','U30','U32']:
 if 'undetermined' not in u[n]['institution']['type_alternatives']:
  change(n,['institution'],lambda n=n:u[n]['institution']['type_alternatives'].append('undetermined'),'Retain the bounded alternative that the articulated engineering/procedural method lacks sufficient institutional significance, without changing the preferred strategy classification.',[ref(n)],False,'unresolved')
# Domain and time fields of nonlocal hypothetical cleanup remain no-object, while release versions keep their case object.
for n in ['U04','U30']:
 if n=='U30':
  change(n,['proposition'],lambda:u['U30']['proposition'].update(domain='Proposed separate cleanup of other versions in the compatibility-test file; future pull request not identified.'),'Clarify that null is an unknown future proposal identity, not the containing PR.',[ref(n)])
Path('annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n');Path('annotation.final.json').write_bytes(Path('annotation.json').read_bytes());Path('repair_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print('Source review changes:',sum(x['phase']=='source_self_review' for x in log),'with meaning changes:',sum(x['meaning_changes'] for x in log))
