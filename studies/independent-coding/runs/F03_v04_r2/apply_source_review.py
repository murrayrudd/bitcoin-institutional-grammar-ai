import json,copy
from pathlib import Path
R=Path(__file__).resolve().parent
A=json.loads((R/'annotation.json').read_text());P=json.loads((R/'packet.json').read_text());E={x['source_id']:x for x in P['entries']};U={x['unit_id']:x for x in A['units']};L=json.loads((R/'repair_log.json').read_text())
def ev(s,q,start=0):
 t=E[s]['text'];p=t.index(q,start);return {'source_id':s,'span':{'start':p,'end':p+len(q),'quote':q}}
def change(uid,path,obj,key,value,why,evidence,meaning=False,effect='evidence_basis_error',diagnosis='execution_failure'):
 old=copy.deepcopy(obj[key]);obj[key]=copy.deepcopy(value)
 if old==value:return
 L.append({'change_id':f'S{1+sum(x["phase"]=="source_self_review" for x in L):02d}','phase':'source_self_review','unit_id':uid,'path':path,'before':old,'after':copy.deepcopy(value),'meaning_changed':meaning,'effect':effect,'diagnosis':diagnosis,'rationale':why,'evidence':evidence})
# Predicate-role and local-governor inspection.
u=U['F03-U02'];c=u['components'][0];new=copy.deepcopy(c);new.update(basis='context_inferred',occurrence_role='semantic_inference',inference_note='We is the literal subject of want; assigning the same group as actor of reconstructed consideration/acceptance is a semantic inference. Its membership remains unspecified.')
change(u['unit_id'],'components/0',u['components'],0,new,'The inferred acceptance action should not borrow an explicit actor role from the different predicate want without marking the transfer.',c['evidence'])
u=U['F03-U08'];clause='instead, have an "adaptive fee switch" (that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees-- and the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks])';g=ev(u['source_id'],clause)
new=copy.deepcopy(u['components']);second=ev(u['source_id'],'have',g['span']['start'])
new[2]['evidence']=[second]
for i,c in enumerate(new):
 if i in (0,1):
  c['occurrence_role']='shared_scope';c['governing_span']=g
  c['inference_note']='The '+('actor we' if i==0 else 'advisory should')+' is supplied in the first branch and shared by the coordinated instead-have branch. The rhetorical not instead alternative is not coded as prohibition.'
 else:c['governing_span']=g
new[2]['inference_note']='This is the have governing an adaptive fee switch; the earlier have governs the replaceable switch. Tentative alternative force is preserved in the qualifier.'
change(u['unit_id'],'components',u,'components',new,'Source review found an in-unit but wrong predicate occurrence: the first have governed replaceable switch. The second have and its shared actor/modal are now scoped to the actual adaptive-fee target.',[g,ev(u['source_id'],'we should even have a "replaceable switch" and not, instead, have an "adaptive fee switch"')])
u=U['F03-U09'];g=ev(u['source_id'],'this can be reviewed already.');new=copy.deepcopy(u['components'])
for c in new:c['governing_span']=g
change(u['unit_id'],'components',u,'components',new,'The reviewer invitation belongs to the passive review clause, not the preceding report of working on the GUI.',[g],effect='convention_deviation')
u=U['F03-U15'];new=copy.deepcopy(u['components']);new[0]['text']='add';new[0]['inference_note']='Adding an abort capability is reconstructed from could also let you abort; no explicit implementation verb is supplied.'
change(u['unit_id'],'components/0',u['components'],0,new[0],'Separate the reconstructed action add from its existing object, the abort capability; avoid repeating aborting in both action and object.',new[0]['evidence'],effect='convention_deviation')
u=U['F03-U16'];new=u['proposition']['summary'].replace('if he does not choose','if Jonas does not choose')
change(u['unit_id'],'proposition/summary',u['proposition'],'summary',new,'Remove an unsupported gendered pronoun; the named addressee is supplied and is sufficient.',[ev(u['source_id'],'Jonas'),ev(u['source_id'],"if you don't go with Greg's suggestion")],effect='evidence_basis_error')
# Separate the known discussion venue from unestablished specific proposal identities.
for uid in ['F03-U10','F03-U11','F03-U12','F03-U14','F03-U15']:
 u=U[uid];prop=copy.deepcopy(u['proposition']);prop['decision_object_id']=None;prop['identity_evidence']=[]
 prop['domain']='Exploratory design of a GUI replacement/additional-output workflow discussed within PR #7819; no specific implementation PR for this idea is established.'
 prop['qualifiers'].append({'description':'The discussion occurs in #7819, whose body expressly lacks GUI replacement. No supplied source identifies a separate implementation proposal for this particular workflow or feature; null denotes unresolved decision-object identity, not lack of a known discussion venue.','evidence':[ev('pr7819:body','This PR does not include a way to actually replace a transaction with the GUI.'),ev(u['source_id'],u['span']['quote'])],'attachment':'scope_note','linked_unit_id':None,'rationale':'Containing-discussion metadata cannot establish the identity or disposition of the broader future GUI work.'})
 change(uid,'proposition',u,'proposition',prop,'The initial version assigned the containing PR to work expressly extending beyond its stated scope. The actual implementation proposal is unresolved; no #7819 closure is transferred to these ideas.',prop['qualifiers'][-1]['evidence'],meaning=True,effect='coverage_or_scope_loss')
# Interest is visible, but no implementation proposal can be assigned to this event.
u=U['F03-U10'];r=copy.deepcopy(u['institution']['recognition'][0]);r.update(target='unresolved',basis='unresolved',object_id=None,identity_evidence=[],rationale='The later comment expresses interest in the same additional-output approach, but no particular implementation proposal is identified. Null marks unknown object identity; #7819 identifies only the recognizing discussion episode. This is ordinary technical interest, not recognition of an expectation or evidence of implementation.')
change(u['unit_id'],'institution/recognition/0',u['institution']['recognition'],0,r,'Retain the interest response while leaving the unknown required proposal target unresolved instead of equating it with the containing PR.',r['evidence'],meaning=True,effect='evidence_basis_error')
u=U['F03-U12']
change(u['unit_id'],'scope',u,'scope','general','The method is phrased for generic you and for cases where the original confirms. Its generality is bounded to the additional-output workflow; it is not general project governance.',[ev(u['source_id'],u['span']['quote'])],meaning=True,effect='coverage_or_scope_loss',diagnosis='defensible_alternative_representation')
change(u['unit_id'],'level_rationale',u,'level_rationale','The focal method concerns technical handling of additional-output transactions and confirmation contingencies. It is general within that workflow, while the visible act is ordinary operational technical review. General software behavior does not establish selection of a recurring governance arrangement.',[ev(u['source_id'],u['span']['quote'])],'Clarify why technically general method scope does not make this collective-choice governance.',False,'convention_deviation') if False else None
# Attach the actual repeated question/claim when interpreting a bare assent target.
for uid,qid in [('F03-U04','F03-Q01'),('F03-U08','F03-Q02')]:
 u=U[uid];r=u['institution']['recognition'][0];q=U[qid];ne=[{'source_id':q['source_id'],'span':q['span']}]+r['evidence']
 change(uid,'institution/recognition/0/evidence',r,'evidence',ne,'Include the repeated focal passage as well as the assent, so the exact recognition target is source-auditable. It remains ordinary assent and establishes no institutional standing.',ne)
# Refine explanation without adding an institutional finding.
u=U['F03-U12'];new='The focal method concerns technical handling of additional-output transactions and confirmation contingencies. It is general within that workflow, while the visible act is ordinary operational technical review. General software behavior does not establish selection of a recurring governance arrangement.'
change(u['unit_id'],'level_rationale',u,'level_rationale',new,'Make the technical domain and operational target explicit after changing the method scope to general.',[ev(u['source_id'],u['span']['quote'])],effect='convention_deviation')
# Explicitly retain provisional degree for literal exploratory candidates.
for uid in ['F03-U08','F03-U10','F03-U12','F03-U14']:
 u=U[uid]
 change(uid,'confidence',u,'confidence','plausible','Literal wording is clear, but extracting an institutional candidate from an exploratory technical proposal or method remains interpretive.',[ev(u['source_id'],u['span']['quote'])],effect='convention_deviation')
 change(uid,'uncertainty_reason',u,'uncertainty_reason',u['alternative_interpretation'],'Keep the candidate-versus-technical-context uncertainty visible in its dedicated field.',[ev(u['source_id'],u['span']['quote'])],effect='convention_deviation')
# Record the object limitation at episode level too.
new=A['episode_summary']['missing_evidence']+['No specific implementation proposal is established for the additional-output method, fee-only narrowing, delayed-send option, or abort capability; their decision_object_id values remain null despite a known discussion venue.']
change(None,'episode_summary/missing_evidence',A['episode_summary'],'missing_evidence',new,'Prevent downstream attribution of the future workflow ideas or their dispositions to #7819 solely by discussion location.',[ev('pr7819:body','This PR does not include a way to actually replace a transaction with the GUI.')],meaning=True,effect='coverage_or_scope_loss')
(R/'annotation.json').write_text(json.dumps(A,ensure_ascii=False,indent=2)+'\n')
(R/'annotation.final.json').write_bytes((R/'annotation.json').read_bytes())
(R/'repair_log.json').write_text(json.dumps(L,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_review_changes':sum(x['phase']=='source_self_review' for x in L),'total_changes':len(L),'units':len(A['units'])}))
