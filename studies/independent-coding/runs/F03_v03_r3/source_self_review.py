from pathlib import Path
import json,copy
p=json.loads(Path('packet.json').read_text());ts={e['source_id']:e['text'] for e in p['entries']}
a=json.loads(Path('annotation.json').read_text());log=json.loads(Path('repair_log.json').read_text());us={u['unit_id']:u for u in a['units']}
def ev(s,q,start=0):
 i=ts[s].index(q,start);return {'source_id':s,'span':{'start':i,'end':i+len(q),'quote':q}}
def ue(n):
 u=us[f'F03-U{n:02d}'];return {'source_id':u['source_id'],'span':copy.deepcopy(u['span'])}
def change(cid,target,field,before,after,meaning,kind,why,evidence):
 log.append({'change_id':cid,'phase':'single_source_self_review','target':target,'field':field,'before':before,'after':after,'meaning_changes':meaning,'classification':kind,'rationale':why,'evidence':evidence})
u=us['F03-U02'];c=next(x for x in u['components'] if x['symbol']=='Cac');before=copy.deepcopy(c)
c.update(basis='context_inferred',occurrence_role='semantic_inference',inference_note='Without explicitly qualifies the author\'s tentative desire. Its role as the activating absence condition for the reconstructed defer-accepting action is inferred, rather than an explicitly stated if-condition.')
change('S01',u['unit_id'],'components.Cac',before,c,False,'epistemic_role_label','The source contains the qualifier, but the activation role depends on the pragmatic action reconstruction.',[ue(2)])
u=us['F03-U06'];c=next(x for x in u['components'] if x['symbol']=='Bdir');before=copy.deepcopy(c)
c['text']='"replaceable" there';c['evidence']=[ev(u['source_id'],c['text'],u['span']['start'])];c['inference_note']='The literal subject plus its locative there becomes the target of the reconstructed revision, so its role is inferred. There preserves the particular interface occurrence, referring back to the confirmation window rather than every use of this word.'
change('S02',u['unit_id'],'components.Bdir',before,c,True,'material_qualification','Retains the local display location in the reconstructed target instead of representing the word alone. The source span had already preserved the qualifier, but the component target was underspecified.',[ue(5),ue(6)])
u=us['F03-U11'];c=next(x for x in u['components'] if x['symbol']=='Bdir');before=copy.deepcopy(c)
c.update(basis='explicit',occurrence_role='local',inference_note='In the literal passive be reviewed, this is explicitly the patient or target of the stated action, so its IG Bdir role is supplied even though its grammatical position is the subject. Resolving this to the current contribution is contextual; no new action is reconstructed.')
change('S03',u['unit_id'],'components.Bdir',before,c,False,'epistemic_role_label','A literal passive directly supplies the review target. This differs from transforming the subject of an evaluative claim into the object of a newly invented action.',[ue(11)])
r=next(r for r in a['relations'] if r['from_unit_id']=='F03-U16' and r['to_unit_id']=='F03-U14');before=copy.deepcopy(r)
r['type']='clarifies';r['rationale']='Specifies technical requirements of the reported additional-output approach. It does not contradict that the author tried it, nor expressly reject the proposal; complexity is not by itself institutional dispute.'
change('S04','F03-U16 -> F03-U14','relation',before,r,True,'relation_overstatement','The first-complete challenges label implied opposition to a proposition that was only a report of an attempted method. The source supports clarification of technical requirements.',[ue(14),ue(16)])
m=a['episode_summary']['mechanisms'][2];before=copy.deepcopy(m['evidence']);m['evidence'].append(ue(22))
change('S05','episode_summary.mechanisms[2]','evidence',before,m['evidence'],False,'claim_evidence_coverage','The claim explicitly mentions the earlier rebase request when limiting causal interpretation; that request must be included in the evidence array.',[ue(22),ue(23)])
Path('annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
Path('annotation.final.json').write_bytes(Path('annotation.json').read_bytes())
Path('repair_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
notes={
 'run_id':'F03_v03_r3','review_type':'one complete source-based self-review after first-complete freeze and mechanical repairs','review_rounds':1,
 'coverage':{'all_entries_screened':19,'focal_entries_exhaustively_reviewed':10,'supplement_entries_context_screened':9,'units_reviewed':23,'statement_units_reviewed':16,'relations_reviewed':13,'outcome_claims_reviewed':3,'mechanism_claims_reviewed':3},
 'checker_flag_resolutions':[
 {'checker_files':['checks.first.json'],'flag_index':0,'unit_id':'F03-U07','kind':'outside_unit','status':'corrected','change_id':'M01','rationale':'The earlier red text occurrence belongs to the remove-emphasis evaluation, not the later get-red-text predicate. The evidence now anchors the occurrence within the non-replacable-case proposition. The inferred apply/Bdir roles remain appropriately inferred.','evidence':[ue(7),next(c for c in us['F03-U07']['components'] if c['symbol']=='Bdir')['evidence'][0]]},
 {'checker_files':['checks.first.json'],'flag_index':1,'unit_id':'F03-U11','kind':'outside_unit','status':'corrected','change_ids':['M02','S03'],'rationale':'The initial this was inside a repeated quotation, not the review predicate. Its evidence now uses this in this can be reviewed already. Self-review also recognizes the explicit patient role of the literal passive. Capability versus institutional permission remains unresolved.','evidence':[ue(11)]},
 {'checker_files':['checks.first.json','checks.mechanical.json','checks.json'],'flag_indices':{'checks.first.json':2,'checks.mechanical.json':0,'checks.json':0},'unit_id':'F03-U04','kind':'pragmatic_explicit_argument','symbol':'Bdir','status':'retained','rationale':'This is directly the object of the explicit verb expose in the source. The pragmatic addition is defer and the recommendation force; neither changes the object\'s existing role. The body resolves the referent to the checkbox. Explicit Bdir is retained as a defensible role assignment, with the nonexplicit negative timing force separately marked.','evidence':[ev('pr7819:comments:0','expose this'),ue(4),ue(1)]}
 ],
 'unit_review':[],
 'screening_review':[],
 'relation_review':[],
 'recognition_and_disposition_review':[
 {'units':['F03-U01'],'status':'retained','finding':'The readiness challenge concerns immediate stand-alone exposure. Closure remains broader-proposal status; reported inclusion in #8182 remains an author implementation report, not verified repository integration. Distinct objects are preserved.','evidence':[ue(1),ue(4),ue(23),ev('pr7819:metadata','"merged": false'),ev('pr8182:supplement_metadata','"merged": false')]},
 {'units':['F03-U04','F03-U08'],'status':'retained','finding':'Quoted-then-agreed responses support this-proposition endorsement, not expectation recognition or locally_supported standing. No accepted disposition is inferred from technical assent.','evidence':[ue(9),ue(10),ue(12),ue(13)]},
 {'units':['F03-U14','F03-U18'],'status':'retained','finding':'Response and favorable-evaluation links remain context-inferred because threading or identity authentication is incomplete; neither event verifies implementation.','evidence':[ue(14),ue(16),ue(19),ue(18),ue(21)]},
 {'units':['F03-U23'],'status':'retained','finding':'The closure report is a context act. Its metadata disposition is broader_proposal recorded_closed_unmerged, without rejection or sanction.','evidence':[ue(23),ev('pr7819:metadata','"closed_at": "2016-06-09T09:21:57+00:00"'),ev('pr7819:metadata','"merged_at": null')]}
 ],
 'authority_application_levels_review':{
   'status':'retained','finding':'No statement is promoted to rule_candidate, constitutive_specification, locally_supported, or repeatedly_supported. No authority, authorization, application-of-rule, or enforcement relation is inferred. All visible contribution actions and focal edit/review activities are operational; there is no evidence of collective-choice procedural revision, constitutional power allocation, or epistemic authority. Technical software properties are not institutions merely because they constrain implementation.',
   'evidence':[ue(1),ue(8),ue(11),ue(16),ue(22),ue(23)]},
 'outcome_and_mechanism_review':[],
 'retained_limitations':a['episode_summary']['missing_evidence'],
 'unresolved_judgments':[
   {'units':['F03-U01','F03-U02','F03-U05','F03-U06','F03-U07','F03-U08','F03-U18','F03-U20','F03-U21'],'status':'unresolved','finding':'Several technical proposals are plausible contribution-governance candidates but lack evidence selecting a rule, norm, or strategy beyond one-off design advice. Their literal technical alternatives are retained.'},
   {'units':['F03-U11','F03-U16'],'status':'unresolved','finding':'Reviewability can and technical need do not establish permission or obligation; the force remains unresolved.'},
   {'units':['F03-U22'],'status':'unresolved','finding':'Rebase request versus technical diagnosis remains unresolved, with a text-only norm-candidate interpretation rather than an authoritative requirement.'}
 ],
 'review_conclusion':'The checker verifies structure and exact text identity, not semantic truth. All checker flags are resolved as corrected or retained with source reasons. Source self-review corrected five items; institutional ambiguities and source limits remain explicit.'
}
unit_findings={
1:'Retained technical edit candidate and disputed timing/application only; no assertion that all checkbox design is rejected. Location, nSequence, and BIP125 RBF are preserved.',
2:'Corrected the activation-condition role to inferred. The tentative negative preference is not elevated into an explicit merge instruction.',
3:'Retained the literal negative intention and personal strategy. The author is the explicit I, while an invitation to reviewers remains an alternative; no reviewer actor is invented.',
4:'Retained pragmatic timing recommendation with explicit object this and complete until-capability qualifier. The modal can inside the condition is technical capability.',
5:'Retained a coupled request to remove red emphasis and the bang in this window. Both display targets remain recoverable; separate coordinated children are a meaning-preserving alternative.',
6:'Corrected the reconstructed object to retain there, bounding the wording concern to this display occurrence. Revise and purpose remain inferred.',
7:'Corrected the red-text evidence occurrence mechanically. The non-replacable case is an inferred receiver of applying red text; should is anchored to the matching get predicate, and fee-update rationale is retained in the unit.',
8:'Retained the complete adaptive-switch alternative with N replacements, future locktimes, multiplicative fees, and the time-indexed fee display. No XOR or implementation outcome is invented.',
9:'Retained a repeated quotation, not another statement or endorsement. The original italic delimiters are absent in this occurrence, which does not imply a new proposition.',
10:'Retained direct agreement as a context act and specific endorsement, without treating it as a recognized rule.',
11:'Retargeted the local patient anchor and corrected it to an explicit role in a literal passive. Can remains unresolved capability versus permission; already is retained.',
12:'Retained exact repeated adaptive-switch text as a quotation endpoint, without independent endorsement.',
13:'Retained tentative possible-solution endorsement, not a completed implementation or settled decision.',
14:'Retained an attributable attempted method, including return to the sendcoins dialog. Its technical-report alternative remains explicit, and the complexity response now clarifies rather than challenges this report.',
15:'Retained a literal question proposing just fee increases; should, maybe, and exclusive focus remain recoverable. No final narrowing of implementation scope is asserted.',
16:'Retained explicit handle/you/object structure and technical-necessity alternative. The original transaction and original-confirms purpose are preserved; additional-output activation is inferred.',
17:'Retained technical repeated-use computational burden as context. Must compute is not a sanction or separately imposed social obligation.',
18:'Retained indirect replacement suggestion with two alternative words, not an obligation to use both. Original replacable and would-as-prediction are preserved.',
19:'Retained positive technical evaluation as a response, not a new adoption claim.',
20:'Retained the option label, delay behavior, amend-within-timeout benefit, and possible abort before initially set. No correction to the source wording or inferred on/off behavior is supplied.',
21:'Retained the incomplete spelling fragment, conditional fallback, and inferred vocative actor role. Jonas and Greg are not assigned unsupplied formal identities or powers.',
22:'Retained a text-only rebase expectation with unresolved technical-diagnosis alternative. Actor is omitted; PR #7819 is the inferred action target. No rebase or sanction is inferred from closure.',
23:'Retained the scoped closure/inclusion report as context. #8182 is the named successor, while supplied metadata establishes each object\'s separate unmerged closure.'}
for i in range(1,24):
 notes['unit_review'].append({'unit_id':f'F03-U{i:02d}','status':'corrected' if i in [2,6,7,11] else 'retained','finding':unit_findings[i],'evidence':[ue(i)]})
for s in a['entry_screening']:
 ent=next(e for e in p['entries'] if e['source_id']==s['source_id'])
 notes['screening_review'].append({'source_id':s['source_id'],'scope':'exhaustive focal' if s['source_id'] in p['selection_design']['focal_source_ids'] else 'supplement context screen','status':'retained','disposition':s['disposition'],'finding':s['reason'],'evidence':[ev(s['source_id'],ent['text'])]})
for i,r in enumerate(a['relations']):
 notes['relation_review'].append({'relation_index':i,'from_unit_id':r['from_unit_id'],'to_unit_id':r['to_unit_id'],'type':r['type'],'status':'corrected' if r['from_unit_id']=='F03-U16' and r['to_unit_id']=='F03-U14' else 'retained','finding':r['rationale'],'evidence':r['evidence']})
for name in ['observed_outcomes','mechanisms']:
 for i,x in enumerate(a['episode_summary'][name]):
  notes['outcome_and_mechanism_review'].append({'target':f'episode_summary.{name}[{i}]','status':'corrected' if name=='mechanisms' and i==2 else 'retained','claim':x['claim'],'finding':'Reviewed every material clause against the cited supplied text and its object/revision context. The claim retains the distinction between technical discussion, author report, recorded PR status, and unverified implementation; no sequence is treated as causal identification.','evidence':x['evidence']})
Path('review_notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'self_review_changes':5,'total_repairs':len(log),'final_units':len(a['units'])}))
