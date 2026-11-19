import json, sys, hashlib
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
p=Path('.')
a=json.loads((p/'annotation.final.json').read_text())
packet=json.loads((p/'packet.json').read_text())
U={u['unit_id']:u for u in a['units']}
texts={e['source_id']:e['text'] for e in packet['entries']}
log=json.loads((p/'repair_log.json').read_text())

def anchor(s,q=None):
 t=texts[s];q=q if q is not None else t.rstrip('\n');st=t.index(q)
 return {'source_id':s,'span':{'start':st,'end':st+len(q),'quote':q}}
def ue(uid):
 u=U[uid];return {'source_id':u['source_id'],'span':deepcopy(u['span'])}
def uniq(es):
 out=[]
 for e in es:
  if e not in out:out.append(e)
 return out
qual_notes={
'U01':'Checkbox location, nSequence/BIP125 purpose, missing GUI replacement, uncertainty about proceeding, larger-work-in-progress scope, and attribution of two refactoring commits to #7159 are visible. No adoption or outcome of #7159 is implied.',
'U03':'Negated personal preference, current-PR review object, and separation from larger GUI work are preserved. Strategy is retained as a plausible personal intention, with preference-only/context and review-invitation alternatives; no shared duty is inferred.',
'U04':'Tentativeness and the actual wallet-replacement condition survive. Until now appears as Cex under withholding because it bounds duration; it is not silently narrowed to the body\'s GUI wording. Can remains capability.',
'U06':'The target is the replaceable-transaction confirmation styling. Negative aesthetic assessment supports an inferred removal suggestion; red styling in every UI context is not prohibited.',
'U07':'The child inherits the negative deserves predicate and confirmation-window scope from the enclosing clause, while preserving the separate bang edit. The shared condition is explicit rather than taken from an unrelated pronoun.',
'U09':'Arguably, advisory should, the non-replacable-case target, and the stated fee-update reason are preserved. A wrong red-text occurrence was corrected to this predicate; the reconstructed modal is now recorded with inferred role.',
'U10':'The contemplated substitution remains tentative. N replacements, future locktimes, multiplicative fees, and the fee-line schedule remain attached. The alternative to replaceable is a coupled design substitution, not an XOR duty. The reconstructed should role is now explicit in the coding record but inferred in basis.',
'U13':'Already, the current PR referent, work still underway on replacement GUI, and tough 0.13 timing are attached. Can remains unresolved between feasibility and encouragement, without an institutional permission claim.',
'U16':'Past/attempted status and transaction editing in the sendcoins dialog are retained. The separate workflow has unknown proposal identity. Its later ordinary-interest event now has unresolved target and basis; no integrated implementation follows from trying.',
'U17':'Maybe, question form, should, and just retain tentative advice to narrow scope to fees. This is neither rejection of additional outputs nor a recurring project-wide governance rule.',
'U18':'Additional-output workflow scope, child-of-original identity, and use-if-original-confirms condition remain visible. The first qualifier is correctly a scope note. Need/must concern engineering dependency and computational consequences, not institutional obligation.',
'U20':'The exact old word replacable and alternative words updatable OR amendable are preserved. Better description supplies the stated goal; no option is treated as adopted.',
'U22':'The [send immediately] label and delay behavior are both preserved, along with amendment-within-timeout and possible abort. Initially set is retained verbatim in meaning rather than normalized to sending; exact interpretation is unresolved.',
'U23':'The addressee is only the supplied Jonas/you. The partial spelling replaceab with ellipsis is not expanded. If the addressee does not follow Greg\'s suggestion remains the activation condition; its mapping to U20 is contextual.',
'U24':'The PR target is contextual and the rebasing actor is unexpressed. Needs is treated as an elliptical review request with a technical-state alternative, not proof of a binding rule or maintainer authority.'}
# Record the one completed source pass, including supplemental screening scope.
source_reviews=[]
for sc in a['entry_screening']:
 s=sc['source_id'];entry=next(x for x in packet['entries'] if x['source_id']==s)
 es=[ue(i) for i in sc['unit_ids']]
 if not es:es=[anchor(s)]
 source_reviews.append({'source_id':s,'scope':'exhaustive_focal' if s in packet['selection_design']['focal_source_ids'] else 'supplemental_context_screen','status':'retained','candidate_count':sum(U[i]['record_role']=='statement' for i in sc['unit_ids']),'unit_ids':sc['unit_ids'],'finding':sc['reason'],'evidence':es})
# Per-component notes show the actual predicate reviewed, including nonlocal roles.
component_reviews=[]
for u in a['units']:
 for i,c in enumerate(u['components']):
  changes=[x['change_id'] for x in log if x['unit_id']==u['unit_id'] and (x['path'].startswith('components/'+str(i)))]
  component_reviews.append({'unit_id':u['unit_id'],'component_index':i,'symbol':c['symbol'],'status':'corrected' if changes else 'retained','basis':c['basis'],'occurrence_role':c['occurrence_role'],'finding':c['inference_note'] or 'The cited exact occurrence supplies this argument/action/constraint in the selected local predicate; no role is borrowed from another clause.','governing_span':c['governing_span'],'evidence':c['evidence'],'repair_ids':changes})
# Mechanism/outcome review is clause-level and intentionally bounded.
summary_reviews=[]
for k in ['observed_outcomes','mechanisms']:
 for i,s in enumerate(a['episode_summary'][k]):
  summary_reviews.append({'section':k,'index':i,'status':'corrected' if k=='observed_outcomes' and i==1 else 'retained','finding':('The author\'s inclusion report is separated from two independently identified metadata outcomes. Both PRs have false merge status. No #8182 content verification, feature acceptance, or network adoption is asserted.' if k=='observed_outcomes' and i==0 else 'The retained head proves the listed checkbox and confirmation text only. Still was removed because no complete chronology establishes persistence or the response to review.' if k=='observed_outcomes' else 'Textual correspondence supports the limited exchange sequence and its stated reasons. Each quoted/asked/reported clause appears in claim_parts; technical exploration and compatible opinions remain alternatives to adopted governance or causally changed decisions.'),'claim_parts':deepcopy(s['claim_parts']),'evidence':deepcopy(s['evidence'])})
# Each distinct checker flag is keyed to its occurrence/component, and every checker occurrence is retained.
checks={name:json.loads((p/name).read_text()) for name in ['checks.first.json','checks.repaired.json','checks.post_review.json','checks.json']}
flag_groups={}
for name,ch in checks.items():
 counters={}
 summary_index=0
 for index,f in enumerate(ch.get('review_flags',[])):
  code=f['code'];uid=f['unit_id'];sub=None
  if code=='predicate_audit':
   sub=counters.get(uid,0);counters[uid]=sub+1
  elif code=='summary_audit':sub=summary_index;summary_index+=1
  key=(code,uid,sub)
  if key not in flag_groups:flag_groups[key]={'code':code,'unit_id':uid,'component_or_summary_index':sub,'occurrences':[]}
  flag_groups[key]['occurrences'].append({'checker_file':name,'flag_index':index})
for (code,uid,sub),r in flag_groups.items():
 if code=='predicate_audit':
  cr=next(x for x in component_reviews if x['unit_id']==uid and x['component_index']==sub)
  r.update({'status':cr['status'],'finding':cr['finding'],'evidence':cr['evidence']+[cr['governing_span']],'repair_ids':cr['repair_ids']})
 elif code=='qualifier_audit':
  u=U[uid];changes=[x['change_id'] for x in log if x['unit_id']==uid and (x['path'].startswith('proposition') or x['path'].startswith('uncertainty'))]
  r.update({'status':'corrected' if changes else 'retained','finding':qual_notes[uid],'evidence':uniq([ue(uid)]+[e for q in u['proposition']['qualifiers'] for e in q['evidence']]),'repair_ids':changes})
 elif code=='application_audit':
  r.update({'status':'unresolved','finding':'The retained checkbox patch is a prepared artifact, while #7819 is closed without merge. There is no verified integrated application of U01. The annotation explicitly leaves application unresolved rather than upgrading the patch into adoption.','evidence':U[uid]['institution']['application_evidence'][0]['evidence'],'repair_ids':[]})
 elif code=='challenge_audit':
  r.update({'status':'retained','finding':'The readiness concern has the same offered checkbox object but questions the broader proposal\'s exposure, not the literal feature-description fact. Target remains broader_proposal and dispute_present remains false.','evidence':[ue('U01'),ue('U04')],'repair_ids':[]})
 elif code=='challenge_object':
  r.update({'status':'retained','finding':'The this in U04 refers to the current checkbox offering in U01. The relation captures a broader readiness challenge to exposing that feature; it does not mark the feature-description proposition itself false or infer institutional rejection.','evidence':[ue('U01'),ue('U04'),anchor('pr7819:body','This PR does not include a way to actually replace a transaction with the GUI.')],'repair_ids':[]})
 elif code=='summary_audit':
  sr=summary_reviews[sub]
  r.update({'status':sr['status'],'finding':sr['finding'],'evidence':sr['evidence'],'repair_ids':['S09'] if sub==1 else []})
 else:
  raise RuntimeError('Unmapped flag '+code)
error_resolutions=[]
for name,ch in checks.items():
 for index,e in enumerate(ch.get('errors',[])):
  uid=e.get('unit_id');code=e['code'];related=[x for x in log if x['unit_id']==uid]
  if code=='support_profile':related=[x for x in related if x['path']=='institution/standing_profile/recognition']
  elif code=='event_target':related=[x for x in related if x['path']=='institution/recognition/0/basis']
  else:related=[x for x in related if x['phase']=='mechanical_repair' and x['path'].startswith('components/')]
  ev=[]
  if code=='support_profile':ev=U[uid]['institution']['recognition'][0]['evidence']
  elif code=='event_target':ev=U[uid]['institution']['recognition'][0]['evidence']+[ue(uid)]
  else:
   for x in related:
    if isinstance(x['after'],dict) and 'source_id' in x['after']:ev.append(x['after'])
  error_resolutions.append({'checker_file':name,'error_index':index,'code':code,'unit_id':uid,'status':'corrected','repair_ids':[x['change_id'] for x in related],'finding':' '.join(x['reason'] for x in related),'evidence':uniq(ev)})
standing_review=[]
for u in a['units']:
 if u['record_role']!='statement':continue
 standing_review.append({'unit_id':u['unit_id'],'status':'unresolved' if u['institution']['standing_profile']['application']=='unresolved' else 'retained','finding':u['institution']['rationale']+' No supplied governing provision or attributable enforcement authority supports rule_candidate. Ordinary assent, own restatement, and unverified implementation are kept separate.','type':u['institution']['type'],'standing_profile':u['institution']['standing_profile'],'authority_evidence_count':len(u['institution']['authority_evidence']),'evidence':uniq(u['institution']['evidence']+[ev for re in u['institution']['recognition'] for ev in re['evidence']]),'recognition_review':[{'kind':x['kind'],'target':x['target'],'basis':x['basis'],'mode':x['mode'],'object_id':x['object_id'],'finding':x['rationale']} for x in u['institution']['recognition']]})
disposition_review={'status':'retained','finding':'Every unit-level disposition concerns the explicitly identified broader #7819 proposal and cites both closed state and false merge status. No #7819 closure is assigned to the distinct future workflow; #8182 has its own outcome record. The author\'s inclusion report is not exact implementation evidence. Closure does not prove rejection, sanctions, or acceptance of a rationale.','unit_ids':[u['unit_id'] for u in a['units'] if u['disposition_events']],'evidence':[anchor('pr7819:supplement_metadata','"url": "https://github.com/bitcoin/bitcoin/pull/7819"'),anchor('pr7819:supplement_metadata','"state": "closed"'),anchor('pr7819:supplement_metadata','"merged": false'),anchor('pr8182:supplement_metadata','"url": "https://github.com/bitcoin/bitcoin/pull/8182"'),anchor('pr8182:supplement_metadata','"state": "closed"'),anchor('pr8182:supplement_metadata','"merged": false'),ue('U25')]}
relation_review=[]
for i,r in enumerate(a['relations']):
 relation_review.append({'relation_index':i,'status':'retained','from_unit_id':r['from_unit_id'],'to_unit_id':r['to_unit_id'],'type':r['type'],'finding':r['rationale'],'evidence':r['evidence']})
notes={'run_id':a['run_id'],'episode_id':a['episode_id'],'packet_sha256':a['packet_sha256'],'review_type':'one_complete_source_based_self_review','source_review_passes':1,'first_complete_preserved_before_checks_and_review':True,'review_sequence':['First-complete annotation frozen','First checker retained','Mechanical anchor/profile repair and repaired check retained','One full pass rereading all 19 packet sources against units, qualifications, roles, support, dispositions, levels, relations, outcomes, and mechanisms','Source-review changes logged','Post-review checker retained; event basis aligned mechanically with unresolved target','Final checker retained'],'source_reviews':source_reviews,'component_reviews':component_reviews,'standing_and_authority_review':standing_review,'disposition_and_object_review':disposition_review,'level_review':{'status':'retained','finding':'All focal candidates concern the concrete contribution, review timing, GUI design, or engineering work. Operational target and observed-action levels are retained. No source chooses recurring governance arrangements, allocates decision powers, or states foundations of legitimate governance. The one container uses not_applicable observed action; all nonstatements have not_applicable target. Future technical workflow is not elevated to collective_choice merely because it could recur.','evidence':[ue(u['unit_id']) for u in a['units'] if u['record_role']=='statement']},'relation_reviews':relation_review,'outcome_and_mechanism_reviews':summary_reviews,'checker_error_resolutions':error_resolutions,'checker_flag_resolutions':list(flag_groups.values()),'coverage_check':{'packet_entries':len(packet['entries']),'screened_entries':len(a['entry_screening']),'focal_sources':len(packet['selection_design']['focal_source_ids']),'all_focal_sources_exhaustively_screened':True,'all_supplements_screened_as_context':True,'flag_occurrences':sum(len(c.get('review_flags',[])) for c in checks.values()),'resolved_or_explicitly_unresolved_flag_occurrences':sum(len(r['occurrences']) for r in flag_groups.values()),'distinct_flag_reviews':len(flag_groups),'checker_error_occurrences':sum(len(c.get('errors',[])) for c in checks.values()),'error_resolutions':len(error_resolutions)},'remaining_limits':a['episode_summary']['missing_evidence']+a['episode_summary']['unresolved_questions'],'semantic_certification':'Mechanical pass does not certify interpretation. The listed candidate/context boundaries, technical-versus-institutional readings, and unknown objects remain bounded alternatives rather than externally adjudicated truth.'}
(p/'review_notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
# This records explicit tool/file access, without inspecting external research or environmental secrets.
read_inputs=['INSTRUCTIONS.txt','protocol/codebook.txt','protocol/annotation_schema.json','packet.json','tools/check_annotation.py']
written=['build_annotation.py','annotation.json','annotation.first_complete.json','checks.first.json','repair_mechanical.py','repair_log.json','checks.repaired.json','self_review.py','annotation.final.json','checks.post_review.json','checks.json','write_review_records.py','review_notes.json','access_record.json','completion_manifest.json']
records=[]
for name in read_inputs:
 records.append({'path':str((p/name).absolute()),'access':'read_only_input','sha256':hashlib.sha256((p/name).read_bytes()).hexdigest()})
for name in written:
 records.append({'path':str((p/name).absolute()),'access':'generated_output_read_write_or_execute','sha256':hashlib.sha256((p/name).read_bytes()).hexdigest() if (p/name).exists() and name not in ['access_record.json','completion_manifest.json'] else None})
access={'run_id':a['run_id'],'research_directory':str(p.absolute()),'access_boundary':'Only this assigned directory was used for research and outputs. No parent directory, other run, Library, network, or outside source was accessed. Standard Python modules and installed jsonschema were used for execution.','files_accessed':records,'model_runtime_configuration':{'selection':'inherited primary configuration','model_override_requested':False,'model_override_applied':False,'model_identifier':None,'provider_snapshot':None,'reasoning_effort':None,'seed':None,'sampling':None,'token_use':None,'cost':None,'configuration_note':'No exact provider model snapshot or sampling/accounting parameters are exposed. Protocol labels are not used to infer model identity.','python_version':sys.version,'shell':'bash','provided_current_date':'2026-11-07','provided_timezone':'Etc/UTC'},'external_sources_accessed':[],'agents_spawned':False,'frozen_inputs_modified':False,'execution_note':'Initial combined input print was truncated; the full codebook, schema, and packet were then read in complete sequential chunks. All first-complete and checker outputs were retained.'}
(p/'access_record.json').write_text(json.dumps(access,ensure_ascii=False,indent=2)+'\n')
manifest={'run_id':a['run_id'],'counts':{'screened_entries':len(a['entry_screening']),'focal_sources':len(packet['selection_design']['focal_source_ids']),'units':len(a['units']),'statement_units':sum(u['record_role']=='statement' for u in a['units']),'context_units':sum(u['record_role']=='context' for u in a['units']),'quotation_units':sum(u['record_role']=='quotation' for u in a['units']),'container_units':sum(u['record_role']=='container' for u in a['units']),'relations':len(a['relations']),'outcomes':len(a['episode_summary']['observed_outcomes']),'mechanisms':len(a['episode_summary']['mechanisms']),'repair_log_changes':len(log)},'checker_status':checks['checks.json']['status'],'review_flag_count':len(checks['checks.json']['review_flags']),'source_self_review_passes':1,'files':{name:{'path':str((p/name).absolute()),'sha256':hashlib.sha256((p/name).read_bytes()).hexdigest()} for name in ['annotation.first_complete.json','annotation.final.json','checks.first.json','checks.repaired.json','checks.post_review.json','checks.json','repair_log.json','review_notes.json','access_record.json']}}
(p/'completion_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checker_status':manifest['checker_status'],'counts':manifest['counts'],'review_coverage':notes['coverage_check']}))
