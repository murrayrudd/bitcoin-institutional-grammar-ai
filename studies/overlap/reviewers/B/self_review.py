import json,copy,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
P=json.loads((ROOT/'packet.json').read_text());T={e['source_id']:e['text'] for e in P['entries']}
A=json.loads((ROOT/'annotation.first_complete.json').read_text());U={u['unit_id']:u for u in A['units']}
notes=json.loads((ROOT/'review_notes.first_complete.json').read_text());log=[]
def sp(s,q,start=0):
 i=T[s].index(q,start);return {'start':i,'end':i+len(q),'quote':q}
def ev(s,q,start=0):return {'source_id':s,'span':sp(s,q,start)}
def comp(k,sym):return next(c for c in U['B-'+k]['components'] if c['symbol']==sym)
def change(k,reason,meaning,epistemic,fn):
 u=U['B-'+k];old=copy.deepcopy(u);fn(u)
 if old!=u:log.append({'change_id':len(log)+1,'stage':'single_source_self_review','target':u['unit_id'],'reason':reason,'changes_meaning_or_evidential_claim':meaning,'changes_epistemic_basis_or_occurrence':epistemic,'before':old,'after':copy.deepcopy(u)})
def altercomponent(k,sym,changes,reason,meaning=False,epistemic=False):
 def fn(u):next(c for c in u['components'] if c['symbol']==sym).update(changes)
 change(k,reason,meaning,epistemic,fn)
def relationchange(index,reason,new=None):
 old=copy.deepcopy(A['relations'][index]);
 if new is None:A['relations'].pop(index)
 else:A['relations'][index]=new
 log.append({'change_id':len(log)+1,'stage':'single_source_self_review','target':'relation','reason':reason,'changes_meaning_or_evidential_claim':True,'changes_epistemic_basis_or_occurrence':False,'before':old,'after':copy.deepcopy(new)})

# Correct occurrence anchoring, rather than merely matching the same string.
altercomponent('213-nospam','A',{'evidence':[ev('32359-213','I',T['32359-213'].index('As a node runner'))],'occurrence_role':'shared_scope','inference_note':'The coordinated have action shares the I in As a node runner I should be allowed to configure; the I inside what I consider spam is a different predicate occurrence.'},'Anchor the shared subject to the configure/have construction, not to the embedded consider predicate.',epistemic=True)
altercomponent('012-knob','A',{'evidence':[ev('32381-012','we',T['32381-012'].index('we probably should'))]},'Use the actual subject of probably should twiddle rather than the earlier conditional subject in we are twiddling.',epistemic=True)
# Keep action and object roles separate.
altercomponent('038-comment','I',{'text':'add'},'Remove the object phrase from the reconstructed action; the complete proposed comment remains in Bdir.')
altercomponent('012-150','I',{'text':'choose'},'Remove the repeated setting/outcome object from the action; Bdir retains the full numerical specification.')
altercomponent('004-window','I',{'text':'defer'},'Express the reconstructed timing action without embedding its object and duration, which are separately retained.')
altercomponent('004-window','Cex',{'basis':'context_inferred','occurrence_role':'semantic_inference','inference_note':'A long window is a condition of the reported ACK; treating it as the duration of a reconstructed defer action changes its grammatical role and is therefore inferred.'},'Mark the transformed duration role as inferred, while preserving the same conditional-support interpretation.',epistemic=True)
# Minimize independently coded action spans.
for k,q in [('227-capitulate','those who believe the absence of a technically perfect solutions means we should capitulate to spammers'),('213-configure','As a node runner I should be allowed to configure my mempool'),('213-default','A conservative approach would be to let the defaults be as it is')]:
 change(k,'Trim the span before the independently coded coordinated action. The logical relation and full source evidence preserve shared qualifications.',False,False,lambda u,q=q:u.update(span=sp(u['source_id'],q)))
# Make inferred activation and modifier roles explicit as inferences.
altercomponent('178-tradeoff','Cac',{'basis':'context_inferred','occurrence_role':'semantic_inference','inference_note':'The nominal whether/when-removal issue becomes the occasion for the reconstructed weigh action; the role as activation condition is inferred, not a verbatim if clause.'},'Distinguish a source-supplied issue from its reconstructed activation role.',epistemic=True)
altercomponent('227-capitulate','Cac',{'basis':'context_inferred','occurrence_role':'semantic_inference','inference_note':'The quoted absence-of-perfect-solutions premise is treated as activating the attributed recommendation; it could instead be justificatory rationale. The conditional role is not explicitly stated.'},'Do not label the quoted argumentative premise as an explicit activation condition.',epistemic=True)
altercomponent('227-remove','Cac',{'basis':'context_inferred','occurrence_role':'shared_scope','inference_note':'The second camp premise is shared across both attributed actions. Its interpretation as an activating condition rather than a reason is inferred.'},'Carry the same qualified scope to the second action without falsely labeling the condition explicit.',epistemic=True)
altercomponent('228-transparency','Cex',{'basis':'context_inferred','occurrence_role':'semantic_inference','inference_note':'Transparent modifies the source nominal decision-making. Under the reconstructed make decisions action, it and respects diverse input become execution constraints, so the role mapping is inferred.'},'Label the transformed nominal modifiers as inferred execution constraints, despite their explicit wording.',epistemic=True)
altercomponent('149-convince','Cac',{'symbol':'Cex','inference_note':'To include supplies the stated purpose of the persuasion effort. It does not explicitly introduce an if-seeking-inclusion condition.'},'Apply the frozen purpose-as-Cex convention without inventing an activation condition.')
# The majority sentence does not establish a decision arena or legitimate authority.
def majority(u):
 s=u['source_id'];u['grammar']='regulative';u['components']=[{'symbol':sym,'text':q,'basis':'explicit','evidence':[ev(s,q,u['span']['start'])],'inference_note':'','occurrence_role':'local'} for sym,q in [('A','Only the majority'),('I','decides'),('Bdir','the winner')]]
 u['components'].append({'symbol':'Cex','text':'not by argument','basis':'context_inferred','evidence':[ev(s,"It's a debate that no one wins by argument.")],'inference_note':'The immediately preceding assertion supplies the excluded route to winning; treating it as a method constraint on this allocation is inferred.','occurrence_role':'context_reference'})
 u['statement_target_level']='unknown';u['level_alternatives']=['operational','epistemic','constitutional'];u['observed_action_level']='operational'
 u['level_rationale']='The comment does not identify a merge decision, a rulemaking power, an electorate, or a criterion of legitimate authority. The domain of the debate winner is unresolved. An epistemic or constitutional allocation is a bounded alternative, not an established level.'
 u['alternative_interpretation']='A constitutive allocation of exclusive decision authority is possible if the sentence is institutional. It could instead predict a debate or user-choice outcome, with no institutional authority claim. The regulative decomposition preserves the explicit actor, act, object and exclusivity without selecting that stronger reading.'
 u['institution']['rationale']='A plausible exclusive majority decision criterion for the debate, with the preceding rejection of winning by argument preserved. It is not evidence of a defined repository vote, a governing electorate, or network adoption.'
change('227-majority','Avoid establishing a higher governance level from the undefined debate winner; retain the negated argument pathway with an exact outside-unit anchor and preserve the constitutive alternative.',True,True,majority)
# Supplied general moderation documentation does not document every channel-specific clause.
def channel(u):
 u['institution']['standing']='text_only'
 u['institution']['rationale']='The specific mailing-list requirement is expressed and later reiterated by the same author alongside a blocking claim. The supplied moderation guidance supports a general enforcement arrangement, not dated documentation of this exact channel-specific instruction. The enforcement attribution warrants a rule candidate while shared acceptance and the author\'s formal office remain unverified.'
change('32381-channel','Separate documentary support for general moderation authority from evidential standing of the exact channel requirement.',True,False,channel)
# A nominalized prohibition requires a reconstructed action and object.
def freezegrammar(u):
 u['parse_mode']='pragmatic'
 for c in u['components']:
  if c['symbol']=='I':c.update(text='update',basis='context_inferred',evidence=[ev(u['source_id'],'translation source updates',u['span']['start'])],occurrence_role='semantic_inference',inference_note='Reconstructs update from the nominal updates within the existential prohibition; the explicit existential be is not the operational act governed.')
  if c['symbol']=='Bdir':c.update(text='translation sources',basis='context_inferred',evidence=[ev(u['source_id'],'translation source updates',u['span']['start'])],occurrence_role='semantic_inference',inference_note='Translation source is a nominal modifier in the source and becomes the target of reconstructed update; the Bdir role is therefore inferred.')
change('010-freeze','Preserve the must-not force while correcting the explicit-versus-inferred action/object mapping of the nominalized update prohibition.',False,True,freezegrammar)
def freezestanding(u):
 u['institution']['standing']='disputed'
 for r in u['institution']['recognition']:
  if r['kind']=='expectation_recognition':
   r['target']='broader_proposal';r['basis']='context_inferred';r['rationale']='The reply recognizes the existence and rationale of a translation freeze, but does not recognize this exact categorical ban on any update after final freeze. Its proposed safe workaround contests the breadth or application of the ban.'
 u['institution']['rationale']='An emphatic prohibition on any post-final-freeze translation-source update, justified by disruption risk. A later reply recognizes a freeze generally but proposes a workaround, so the exact categorical application is disputed rather than locally supported. No exact formal authority or exception procedure is supplied.'
change('010-freeze','Broad recognition of a freeze is not proposition-specific recognition of an absolute ban; retain the challenge to application and abstain from locally_supported.',True,False,freezestanding)
# Relation review: do not infer a logical alternative or conflate one speaker's qualification with another's claim.
for i in range(len(A['relations'])-1,-1,-1):
 r=A['relations'][i]
 if r['from_unit_id']=='B-148-assert' and r['to_unit_id']=='B-148-nodoc':
  relationchange(i,'Remove an inferred OR that overstates the logic: a request with an existing-test exception and a conditional no-documentation expectation do not explicitly form exhaustive alternative prescriptions.')
 elif r['from_unit_id']=='B-149-stay' and r['to_unit_id']=='B-149-externalpref':
  nr=copy.deepcopy(r);nr.update(from_unit_id='B-149-externalpref',to_unit_id='B-149-stay',type='uptake',rationale='The quoted preference receives a direct So do I conceptual response, qualified by the replying speaker\'s wish not to switch the current PR. It does not revise or clarify gmaxwell\'s own preference.')
  relationchange(i,'Treat the replying speaker\'s qualification as uptake, not clarification of the quoted person\'s position.',nr)
 elif r['from_unit_id']=='B-014-after' and r['to_unit_id']=='B-014-definition':
  nr=copy.deepcopy(r);nr.update(from_unit_id='B-014-definition',to_unit_id='B-014-after',rationale='The asserted equivalence between discouragement and deprecation explains the objection to after a deprecation warning. The definition is the clarifier, not the object being clarified.')
  relationchange(i,'Correct clarifier-to-clarified direction for the semantic reason supporting the wording objection.',nr)
 elif r['from_unit_id']=='B-32714-nack' and r['to_unit_id']=='B-32714-replace':
  nr=copy.deepcopy(r);nr['evidence']=[ev('32714-007',T['32714-007']),{'source_id':'32714-body','span':copy.deepcopy(U['B-32714-replace']['span'])}]
  relationchange(i,'Replace a warning-condition anchor with the exact replacement proposal targeted by the challenge.',nr)
# Provide the negative clause's shared actor explicitly and at the correct occurrence.
def negactor(u):
 u['components'].append({'symbol':'A','text':'you','basis':'explicit','evidence':[ev('32406-252','you',T['32406-252'].index('If you want to debate'))],'inference_note':'The coordinated negative venue clause shares you from the debate-comment conditional; this is not an inferred formal role.','occurrence_role':'shared_scope'})
change('252-not-here','Retain the explicit shared actor for the independently represented negative-duty clause.',False,False,negactor)

# Synchronize review notes and summaries without adding new empirical claims.
for n in notes['per_focal_source']:
 if n['source_id']=='32359-227':n['reasoning']+=' The final representation keeps the exclusive majority actor and prior not-by-argument qualification but leaves the target governance level unknown.'
 if n['source_id']=='32381-body':n['reasoning']+=' Standing of the exact mailing-list direction is text_only; supplied documentation concerns general moderation authority, not that precise clause.'
 if n['source_id']=='33224-010':n['reasoning']+=' Broad recognition of a freeze does not establish acceptance of the absolute post-final-freeze prohibition; its application is disputed.'
 if n['source_id']=='32406-148':n['reasoning']+=' No OR relation is retained because the source does not establish these clauses as a logical alternative set.'
notes['self_review']={'status':'complete','passes_completed':1,'scope':'All 24 focal entries, all 102 units, all initial 35 relations, recognition and disposition events, authority evidence, outcome/mechanism claims, and all 24 checker review flags were reviewed against the permitted packet and codebook. Final relation count is 34.','mechanical_checker_feedback':'First checker passed; changes are from the single source-based self-review, not semantic feedback from another coder.','semantic_feedback_from_others':False,'remaining_flags':'Documented outside-unit evidence and role-preserved explicit arguments remain review flags rather than errors. Semantic alternatives and missing evidence remain in the annotation and notes.'}
notes['recognition_and_disposition_records']=[{'unit_id':u['unit_id'],'source_id':u['source_id'],'recognition':u['institution']['recognition'],'disposition_events':u['disposition_events']} for u in A['units'] if u['institution']['recognition'] or u['disposition_events']]
notes['access_record']['self_authored_files_accessed']=[str(ROOT/f) for f in ['build_annotation.py','annotation.json','annotation.first_complete.json','review_notes.json','review_notes.first_complete.json','checks.first.json','self_review.py']]
notes['access_record']['research_file_hashes']={str(ROOT/f):hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ['TASK.txt','protocol/codebook.txt','protocol/annotation_schema.json','packet.json','tools/check_annotation.py']}
notes['access_record']['prohibited_material_encountered']=False
for sc in A['entry_screening']:
 if sc['source_id'] in {n['source_id'] for n in notes['per_focal_source']}:sc['reason']=next(n['reasoning'] for n in notes['per_focal_source'] if n['source_id']==sc['source_id'])
(ROOT/'annotation.json').write_text(json.dumps(A,ensure_ascii=False,indent=2)+'\n')
(ROOT/'annotation.final.json').write_bytes((ROOT/'annotation.json').read_bytes())
(ROOT/'review_notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
(ROOT/'access_record.json').write_text(json.dumps(notes['access_record'],ensure_ascii=False,indent=2)+'\n')
repair={'run_id':'R12_B','first_complete_sha256':hashlib.sha256((ROOT/'annotation.first_complete.json').read_bytes()).hexdigest(),'final_sha256':hashlib.sha256((ROOT/'annotation.json').read_bytes()).hexdigest(),'first_checker_status':'pass','self_review_passes':1,'external_semantic_feedback':False,'changes':log,'output_metadata_changes':'Review notes, screening reasons, and event indexes were synchronized to these same source-review decisions. Access records and final hashes were added. No additional semantic review or hidden repair pass was conducted.'}
(ROOT/'repair_log.json').write_text(json.dumps(repair,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_review_changes':len(log),'units':len(A['units']),'statement_units':sum(u['record_role']=='statement' for u in A['units']),'relations':len(A['relations']),'changes_to_evidential_claim_or_meaning':sum(c['changes_meaning_or_evidential_claim'] for c in log),'epistemic_or_occurrence_corrections':sum(c['changes_epistemic_basis_or_occurrence'] for c in log)}))
