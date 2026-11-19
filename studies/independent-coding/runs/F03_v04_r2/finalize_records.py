import json,copy,hashlib,sys,platform,subprocess
from pathlib import Path
import jsonschema
from importlib.metadata import version
R=Path(__file__).resolve().parent
P=json.loads((R/'packet.json').read_text()); A=json.loads((R/'annotation.final.json').read_text()); U={u['unit_id']:u for u in A['units']}; E={e['source_id']:e for e in P['entries']};L=json.loads((R/'repair_log.json').read_text())
def ev(s,q):
 t=E[s]['text'];n=t.index(q);return {'source_id':s,'span':{'start':n,'end':n+len(q),'quote':q}}
def ue(u):return {'source_id':u['source_id'],'span':u['span']}
def dedup(es):
 out=[];seen=set()
 for e in es:
  k=(e['source_id'],e['span']['start'],e['span']['end'])
  if k not in seen:out.append(e);seen.add(k)
 return out
# Final precision edit arising from the same complete source-review pass.
x=A['episode_summary']['observed_outcomes'][1]
before=copy.deepcopy(x)
x['claim_parts'][0]['text']='The retained #7819 patch adds a checkbox labeled Allow Replace-By-Fee; its tooltip describes replacement by a transaction paying higher fees while the original remains unconfirmed.'
x['claim']=' '.join(p['text'] for p in x['claim_parts'])
L.append({'change_id':f'S{1+sum(v["phase"]=="source_self_review" for v in L):02d}','phase':'source_self_review','unit_id':None,'path':'episode_summary/observed_outcomes/1','before':before,'after':copy.deepcopy(x),'meaning_changed':True,'effect':'coverage_or_scope_loss','diagnosis':'execution_failure','rationale':'The source-review precision check retains the higher-fee qualifier as well as the unconfirmed condition when paraphrasing the tooltip. No software efficacy or integration is asserted.','evidence':x['claim_parts'][0]['evidence']})
(R/'checks.post_review_v1.json').write_bytes((R/'checks.json').read_bytes())
for name in ['annotation.json','annotation.final.json']:(R/name).write_text(json.dumps(A,ensure_ascii=False,indent=2)+'\n')
(R/'repair_log.json').write_text(json.dumps(L,ensure_ascii=False,indent=2)+'\n')
result=subprocess.run([sys.executable,'tools/check_annotation.py','packet.json','annotation.final.json'],cwd=R,text=True,capture_output=True)
(R/'checks.json').write_text(result.stdout)
if result.returncode:raise RuntimeError('Final checker failed; see checks.json')
checks={n:json.loads((R/n).read_text()) for n in ['checks.first.json','checks.mechanical.json','checks.post_review_v1.json','checks.json']}
notes={
 'F03-U01':'Retained as a plausible offered edit, with a technical-description-only alternative. Checkbox location, nSequence/BIP125 signaling, and absent GUI replacement remain attached. The capability concern challenges the broader exposure proposal, so dispute_present stays false for the narrow offered edit. Author-directed closure in favor of #8182 supports inferred withdrawal of this submission route; both recorded state and merged false support broader closure only. No accepted edit, authoritative guidance, or implementation application is claimed.',
 'F03-U02':'Uncertainty about wanting this without a GUI workflow is retained as unresolved force. The inferred acceptance action, its object, and now its actor role are marked semantic inference. We has no inferred electorate or power. Ongoing larger work qualifies the question; it is neither a prohibition nor a demonstrated merge gate.',
 'F03-U03':'The negative personal approach is preserved in do not want to hold back, with review as the object. It remains a strategy candidate with preference-only alternative. The later same-actor response shows maintained approach, but does not explicitly recognize an institutional expectation; recognition profile was corrected to none while the restatement event remains visible.',
 'F03-U04':'The source says Not sure and concerns exposure until actual wallet replacement capability. Deferral is inferred, while this remains the explicit receiver of expose. Can is technical capability. The author\'s quoted agreement is ordinary technical assent; recognition evidence now includes the quote. No rule authority, project-wide norm, or review prohibition is inferred.',
 'F03-U05':'Negative evaluation of red text is pragmatically interpreted as removal. The removal action and red-text target role are marked inferred; the focal warning is case-specific. The following bang edit is separately recoverable through the container and action-scoped AND. No parent proposition is double counted.',
 'F03-U06':'The elliptical bang clause receives the shared negative predicate through an explicitly documented enclosing scope. The target is an exclamation mark on the same warning. A coupled representation is a defensible alternative, but both actionable edit targets are preserved. No evidence of acceptance or implementation is supplied.',
 'F03-U07':'Advisory should is anchored to should get red text, not the earlier should be or later adaptive-switch clause. Marking is reconstructed, and the original grammatical subject becomes an inferred edit target. Arguably, the non-replaceable case, and inability to update fees later are retained. Technical reasoning does not establish a rule.',
 'F03-U08':'Source review corrected an in-unit predicate error: the focal action is the second have, governing adaptive fee switch. We and should are shared by the coordinated branch and are explicitly labeled shared_scope. The proposed substitution remains exploratory, with future locktimes, N replacements, multiplicative fees, and block-related display preserved. Object #7819 identifies the contemplated redesign of its switch, not an independently identified future implementation. The quote and might-be-a-solution response supply provisional ordinary assent only.',
 'F03-U09':'The pragmatic invitation is distinguished from the literal capability claim. Reviewed explicitly supplies the action, and this is its passive receiver; neither is borrowed from the preceding working predicate. Governing spans now isolate this can be reviewed already. Ongoing GUI work and 0.13 time pressure remain qualifiers, not evidence of delivery, release, or authority to integrate.',
 'F03-U10':'Was trying marks an attempted personal development approach rather than completed implementation. Additional outputs and editing back in the sendcoins dialog remain recoverable. Specific proposal identity was corrected to null because the original PR lacks GUI replacement and no separate implementation is identified. Later interest is retained with unresolved event object/target, not assigned to #7819 or treated as expectation recognition.',
 'F03-U11':'The literal fee-only question retains maybe, should, and just; focus has increasing fees as its single target. The preceding broader output-editing approach is a linked qualifier. The specific implementation proposal is unknown and now null. This is operational design scope, not a change to recurring governance arrangements.',
 'F03-U12':'The explicit method handles making a child of the original for use if the original confirms. That condition qualifies using the child; it does not postpone making it until confirmation. Need and must in the surrounding explanation express technical necessity, not institutional duty. Generic method scope is general within this workflow, with no identified implementation PR. Exponential workload is technical context, not an O sanction or an independent duty. Strategy-versus-technical-context remains a defensible unresolved interpretation.',
 'F03-U13':'The wording question reconstructs use and converts the literal subject alternatives into an inferred edit object. Updatable or amendable remain alternatives; no XOR is inferred. Instead of replacable identifies the replaced wording. The edit is case-specific and tentative, with no accepted naming norm claimed.',
 'F03-U14':'Have explicitly takes the option with its built-in delay behavior as object. The source\'s send immediately label is not silently repaired. Avoidance of extra contingency transactions is limited to amendments within the timeout, not unconditional. This is an exploratory feature wish without a committed implementer or identified implementation PR.',
 'F03-U15':'The optional abort capability is linked to the same delayed-send option. The inferred action is now add, separated from the capability object. Could indicates technical possibility or a tentative additional request, not institutional permission. Initially set is retained exactly; its meaning remains unresolved. The source does not establish which PR would implement it.',
 'F03-U16':'Jonas is a vocative mapped contextually to the inferred correction actor. The fragment replaceab... is preserved without completing the spelling; its Bdir role is semantic inference. The negative fallback condition if you do not go with Greg\'s suggestion remains explicit. No unsupplied mapping between names and aliases or gendered pronoun remains.',
 'F03-U17':'Needs rebase plausibly expresses a case-specific maintenance expectation, with technical-status alternative. Rebase is reconstructed as action and the omitted PR target is contextually identified. The source supplies no accountable named actor, deadline, maintainer role, authority, or consequence. Later closure neither proves rebase performance nor enforces an inferred sanction.'}
unit_reviews=[]
for u in A['units']:
 uid=u['unit_id'];es=[ue(u)]
 if u['proposition']:
  for q in u['proposition']['qualifiers']:es+=q['evidence']
  for c in u['components']:es+=c['evidence']+[c['governing_span']]
  for r in u['institution']['recognition']+u['disposition_events']:es+=r['evidence']+r['identity_evidence']
  for ch in u['institution']['challenges']:es+=ch['evidence']
  text=notes[uid]
 else:
  text={
  'F03-C01':'The absent GUI replacement claim is technical scope context, not a separate duty. It is used as a material qualification and mechanism endpoint.',
  'F03-K01':'Container only: it groups red text and bang edits, with no components or independent institutional proposition and no action level.',
  'F03-C02':'User-perception concern supplies rationale for terminology evaluation. It does not independently instruct a specific change; the later distinct word suggestion is represented as U13.',
  'F03-Q01':'Repeated concern is linked to U04 by quotes. The difference in inline italics does not make a new proposition or endorsement.',
  'F03-C03':'Agreement is a distinct communicative act after the quote. Its institutional recognition judgment resides on U04; it is not a statement of a new norm.',
  'F03-C04':'The difficult 0.13 timeline is a reported constraint, not proof of release or a deadline obligation.',
  'F03-Q02':'Repeated design wording is linked to U08 by quotes. The quotation alone is not another endorsement.',
  'F03-C05':'Might be a solution is provisional assent, not an adopted method or expectation.',
  'F03-C06':'Conditional computational blowup is a technical effect of repeated output changes. Must compute does not supply a social duty or sanction.',
  'F03-C07':'Interest in additional outputs is ordinary design evaluation. It supplies no proof of feature completion, implementation identity, or governing expectation.',
  'F03-C08':'Closing in favor of #8182 reports an action and inclusion claim. The separate PR identities remain distinct, and inclusion does not prove merged implementation.'}[uid]
 unit_reviews.append({'unit_id':uid,'status':'corrected' if any(x['unit_id']==uid for x in L) else 'retained','assessment':text,'evidence':dedup(es)})
summary_reviews=[]
for group in ['observed_outcomes','mechanisms']:
 for i,item in enumerate(A['episode_summary'][group]):
  if group=='observed_outcomes':
   rationale=[
    'Both quoted readiness concern and agreement are present; the later reviewability and timeline claims have separate exact anchors. This is correspondence among communicative acts, not accepted governance status.',
    'The checkbox, higher-fee replacement condition, unconfirmed condition, red markup, and literal misspelled warning string are each anchored. The final precision edit restored higher fees to the paraphrase. Closed plus merged false limits the observation to the retained proposed patch; no chronological response-to-review or integration inference is made.',
    'The participant report is distinguished from both recorded statuses. #7819 and #8182 identities, closure dates, closed states, and false merge flags are separately cited. No scope of carryover, rejection of individual suggestions, or network adoption is asserted.'
   ][i]
  else:
   rationale=[
    'Initiation, quoted response, ongoing work, review-now distinction, and timeline are supported separately. The body may have later edits; the mechanism does not assert exact historical sentence dating or a causal release gate. Personal review intent predating or independent of the response remains an alternative.',
    'The quote and provisional response, attempted output workflow, fee-only question, child contingency, repeated-version cost, later interest, delayed sending, and optional abort each have evidence. No causal claim runs backward from the complexity explanation to the earlier narrowing question, and no convergent outcome is asserted.',
    'The two source timestamps support order only. Needs rebase and closing in favor of the named alternative are directly evidenced, as is closed-unmerged #7819 status. A planned replacement independent of the rebase comment remains plausible; status is consistent_with rather than supported causal coordination.'
   ][i]
  summary_reviews.append({'group':group,'index':i,'status':'corrected' if group=='observed_outcomes' and i==1 else 'retained','assessment':rationale,'evidence':item['evidence'],'claim_parts_reviewed':len(item['claim_parts'])})
# Every checker flag occurrence is explicitly mapped to a source-based resolution.
resolutions=[]; counters={};summary_index=0
final_flags=checks['checks.json']['review_flags']
for index,f in enumerate(final_flags):
 uid=f.get('unit_id');code=f['code'];components=None
 if code=='summary_audit':
  sr=summary_reviews[summary_index];summary_index+=1;es=sr['evidence'];status=sr['status'];rationale=sr['assessment'];target=f'{sr["group"]}/{sr["index"]}'
 else:
  u=U[uid];target=uid;rationale=notes.get(uid,'Nonstatement record function retained.')
  if code=='predicate_audit':
   ci=counters.get(uid,0);counters[uid]=ci+1;c=u['components'][ci];target+=f'/components/{ci}';es=dedup(c['evidence']+[c['governing_span']]);rationale=f'{c["symbol"]}: {c["text"]}. '+c['inference_note']+' '+notes[uid]
  elif code=='qualifier_audit':es=dedup([ue(u)]+[e for q in u['proposition']['qualifiers'] for e in q['evidence']])
  elif code=='challenge_audit':es=dedup([ue(u)]+[e for ch in u['institution']['challenges'] for e in ch['evidence']])
  else:es=[ue(u)]
  status='corrected' if any(x['unit_id']==uid for x in L) else 'retained'
 occurrences=[]
 for name,ch in checks.items():
  # The ordered flag stream has stable unit/component positions in these four checks.
  if index<len(ch['review_flags']) and ch['review_flags'][index]['code']==code and ch['review_flags'][index].get('unit_id')==uid:
   occurrences.append({'file':name,'flag_index':index})
 resolutions.append({'code':code,'target':target,'occurrences':occurrences,'status':status,'assessment':rationale,'evidence':es})
error_resolutions=[]
for name,ch in checks.items():
 for i,error in enumerate(ch.get('errors',[])):
  changes=[x for x in L if x['unit_id']==error.get('unit_id') and x['phase']=='mechanical_repair']
  error_resolutions.append({'file':name,'error_index':i,'code':error['code'],'unit_id':error.get('unit_id'),'status':'corrected','change_ids':[x['change_id'] for x in changes],'assessment':'The affected local occurrence was relocated to its focal clause, or the recognition summary was aligned with the non-expectation response event. The immutable first-complete output retains the original error; subsequent checker passes report none.','evidence':dedup([e for x in changes for e in x['evidence']])})
review={
 'run_id':'F03_v04_r2','protocol_version':'0.4','review_pass_count':1,
 'review_scope':'One complete source-based self-review of all 19 supplied entries, 10 exhaustive focal entries, 28 units, 14 relations, all support/disposition judgments, and every material clause of 3 outcomes and 3 mechanisms. Subsequent checker executions validate these same review corrections; they are not extra source reviews.',
 'source_screening_review':[{'source_id':s['source_id'],'status':'retained','assessment':s['reason'],'evidence':[ev(s['source_id'],E[s['source_id']]['text'])]} for s in A['entry_screening']],
 'unit_reviews':unit_reviews,'summary_reviews':summary_reviews,
 'checker_error_resolutions':error_resolutions,'checker_flag_resolutions':resolutions,
 'cross_cutting_review':[
  {'topic':'authority_recognition_application','status':'retained','assessment':'No supplied authority attribution or governance document meets rule-candidate documentary requirements. Ordinary agreement and provisional interest do not establish an institutional expectation. No patch-and-integration record verifies implementation of a specific review recommendation; all application profiles remain none. Same-actor review commitment is retained as a response but contributes no expectation-recognition profile.','evidence':[ev('pr7819:comments:2','Right. I totally agree.'),ev('pr7819:comments:3','Yes. This might be a solution.'),ev('pr7819:metadata','"merged": false')]},
  {'topic':'identity_and_disposition','status':'corrected','assessment':'The containing #7819 discussion does not identify the implementation proposal for the broader future GUI work. U10, U11, U12, U14 and U15 therefore use null decision-object identity, and U10\'s interest event retains an unresolved target/object. Only U01 receives the broader #7819 closure and inferred submission withdrawal. #8182 status is independently cited and is also unmerged.','evidence':[ev('pr7819:body','This PR does not include a way to actually replace a transaction with the GUI.'),ev('pr7819:comments:8','Closing in favor of #8182 (included there).'),ev('pr7819:metadata','"merged": false'),ev('pr8182:supplement_metadata','"merged": false')]},
  {'topic':'levels_and_relations','status':'retained','assessment':'The focal activities are contribution review, current UI edits, exploratory technical methods, and ordinary maintenance. No recurring governance procedure, allocation of decision power, or foundation of legitimate authority is established. Thus candidate targets and visible acts remain operational; a technically general method does not become collective-choice governance. Quote links, uptake direction, two action-scoped ANDs, and temporal ordering preserve correspondence without converting it into causation or sanction.','evidence':[ev('pr7819:body','But I don\'t want to hold back review of this PR.'),ev('pr7819:comments:3','But maybe we should just focus on increasing the fees?'),ev('pr7819:comments:7','Needs rebase.')]},
  {'topic':'uncertainty_and_limits','status':'unresolved','assessment':'Candidate-versus-technical-context interpretations, exact proposed-workflow identities, the complete spelling fragment, initially set, historical sentence dates, implementation carryover, participant authority, and causal effects remain unresolved. These limitations are retained rather than repaired with outside evidence.','evidence':[ev('pr7819:comments:6','"replaceab"...'),ev('pr7819:comments:5','before it was initially set'),ev('pr7819:comments:8','Closing in favor of #8182 (included there).')]}
 ],
 'coverage_conclusion':'No additional independently actionable focal proposition was identified during the complete source review. Technical description, repeated quotations, preference, indirect-request, and method alternatives remain explicit. Supplements were screened contextually and are not claimed to lack institutional content.',
 'mechanical_result':{'status':checks['checks.json']['status'],'errors':len(checks['checks.json']['errors']),'review_flags_resolved_in_record':len(resolutions),'all_checker_flag_occurrences_covered':sum(len(x['occurrences']) for x in resolutions)==sum(len(x['review_flags']) for x in checks.values())},
 'semantic_certification':'Not certified by the checker; this is the coder\'s one source-based review, with retained uncertainties and inspectable evidence.'}
(R/'review_notes.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
first_hash=hashlib.sha256((R/'annotation.first_complete.json').read_bytes()).hexdigest()
if first_hash!='139fe48b8b0f04570b026c594381e348f4a5f02b4b2f5d3faa2e97133f36bff6':raise RuntimeError('First-complete freeze changed')
read_files=['INSTRUCTIONS.txt','protocol/codebook.txt','protocol/annotation_schema.json','packet.json','tools/check_annotation.py','build_annotation.py','repair_mechanical.py','apply_source_review.py','finalize_records.py','annotation.json','annotation.first_complete.json','annotation.final.json','checks.first.json','checks.mechanical.json','checks.post_review_v1.json','checks.json','repair_log.json']
written=['build_annotation.py','repair_mechanical.py','apply_source_review.py','finalize_records.py','annotation.json','annotation.first_complete.json','annotation.final.json','checks.first.json','checks.mechanical.json','checks.post_review_v1.json','checks.json','repair_log.json','review_notes.json','access_record.json']
access={'run_id':'F03_v04_r2','authorized_directory':str(R),'source_packet_sha256':hashlib.sha256((R/'packet.json').read_bytes()).hexdigest(),
 'files_accessed':[{'path':str(R/n),'operations':(['read','write'] if n in read_files and n in written else ['read'] if n in read_files else ['write'])} for n in dict.fromkeys(read_files+written)],
 'research_access_limits':{'outside_research_sources_accessed':False,'other_run_directories_accessed':False,'parent_directories_read':False,'library_accessed':False,'web_accessed':False,'calibration_files_accessed':False,'agents_spawned':False,'source_passages_treated_as_data':True,'original_inputs_modified':False},
 'model_configuration':{'selection':'inherited primary configuration','model_override':None,'reasoning_override':None,'provider_model_identity':None,'provider_snapshot':None,'seed':None,'sampling':None,'token_use':None,'cost':None,'note':'No provider-specific runtime model identifier or sampling configuration was exposed. No identity was inferred from protocol or packet text. Primary configuration was inherited without override.'},
 'runtime_configuration':{'python_version':sys.version,'python_executable':sys.executable,'platform':platform.platform(),'jsonschema_version':version('jsonschema'),'ordinary_runtime_modules':['json','hashlib','copy','pathlib','sys','platform','subprocess','importlib.metadata','jsonschema'],'runtime_library_note':'Ordinary interpreter/library imports are outside the research corpus. No external research content or optional calibration was read. The checker invokes the schema in this authorized directory.'},
 'freeze':{'first_complete_path':str(R/'annotation.first_complete.json'),'first_complete_sha256':first_hash,'final_path':str(R/'annotation.final.json'),'final_sha256':hashlib.sha256((R/'annotation.final.json').read_bytes()).hexdigest()},
 'process':{'first_complete_preserved_before_checks':True,'initial_checker_result':'checks.first.json','mechanical_repair_result':'checks.mechanical.json','source_review_initial_result':'checks.post_review_v1.json','final_checker_result':'checks.json','complete_source_self_review_count':1,'repair_log':'repair_log.json','review_notes':'review_notes.json'},
 'counts':{'screened_entries':len(A['entry_screening']),'focal_entries':len(P['selection_design']['focal_source_ids']),'statements':sum(u['record_role']=='statement' for u in A['units']),'contexts':sum(u['record_role']=='context' for u in A['units']),'containers':sum(u['record_role']=='container' for u in A['units']),'quotations':sum(u['record_role']=='quotation' for u in A['units']),'relations':len(A['relations']),'repairs':len(L),'unresolved_decision_object_statements':sum(u['record_role']=='statement' and u['proposition']['decision_object_id'] is None for u in A['units'])}}
(R/'access_record.json').write_text(json.dumps(access,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'complete':True,'counts':access['counts'],'checker_status':checks['checks.json']['status'],'all_flags_accounted_for':review['mechanical_result']['all_checker_flag_occurrences_covered'],'first_complete_sha256':first_hash,'final_sha256':access['freeze']['final_sha256']}))
