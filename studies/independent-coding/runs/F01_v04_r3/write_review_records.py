import json,hashlib,sys,datetime,collections
from pathlib import Path
p=Path(__file__).resolve().parent
A=json.loads((p/'annotation.final.json').read_text());D={u['unit_id']:u for u in A['units']};PK=json.loads((p/'packet.json').read_text());E={e['source_id']:e for e in PK['entries']};LOG=json.loads((p/'repair_log.json').read_text())
def ev(s,q=None):
 t=E[s]['text'];q=t if q is None else q;i=t.index(q);return {'source_id':s,'span':{'start':i,'end':i+len(q),'quote':q}}
def distinct(es):
 out={}
 for e in es:out[(e['source_id'],e['span']['start'],e['span']['end'])]=e
 return list(out.values())
NOTES={
'B01':'Retain an explicitly pragmatic current-addition proposal. The title supplies v24.0.1 only for the retained snapshot; the body has later-edit uncertainty. Concrete patch application was narrowed to broader_proposal because same-procedure/simplification is not fully observed. Concept NACK is a challenge, not a sanction or final rejection.',
'B02':'One navigation action jointly targets the two complete commit identifiers and version labels. No single canonical decision object is fabricated for the pair. The previous patches show examples, not universal every-release compliance.',
'B03':'Actor we, extend, both file contexts, anymore and the complete negative operator are retained. The primary no_obligation force records denied need, with explicit technical-redundancy alternative and no authority claim.',
'D01':'Navigation has See, the full mutable-link object and information purpose as Cex. The specific requested revision is unresolved; canonical pinned document identity was cleared rather than silently equating master with a snapshot.',
'D02':'The addressed reviewer is inferred from your review, while the reaction, comment target, emoji and inaccurate-listing condition are direct. This is an optional correction method, not a duty; bot template/table is not independent recognition.',
'D03':'Bot is the explicit actor and it the explicit target pronoun, whose referent is retained as ambiguous. Reaction trigger comes from shared context. Next update and unobserved announced consequence are preserved; no executed sanction.',
'C02':'Hold off and a bit are direct; PR progress/integration is the inferred omitted target. The prior post is speculative risk, not an explicit delay instruction. No blocking authority or withdrawal is inferred.',
'C03':'Rebase action is reconstructed from nominal wording; literal subject it becomes an inferred target. The erroneous substring inside bit was replaced with the relevant pronoun. After #26589 is preserved without inventing that PR\'s disposition. Reported rebase supports only the broader contribution.',
'C05':'Every major release is a proposed recurring expected practice, with should as advisory. Accident-prevention domain is attached. Latest-per-feature review conflicts with unconditional inclusion. Operational target and collective-choice observed deliberation retain alternatives, with no adopted rule.',
'C06':'The action adding and qualified version target are literal; should justify is not duty. Original speech is a declarative justification claim. The #25717 and qualified miniscript rationales remain attributed; the latter is challenged by specific test-coverage information.',
'C09':'Preference is asserted, while use and the target role of specific tests are reconstructed. The grep expression identifies examples, not a second command. No personal implementation plan or governing authority is invented.',
'C11':'Keep-open method preserves unspecified dependent-PR endpoint and prior-practice/CI rationale as reports. Until qualifies duration and was corrected to Cex. The later same-actor formulation lacks that endpoint; merger of the broader PR does not prove rejection or implementation of this method.',
'C13':'Remove intermediate releases and at some point remain a tentative available response to a quoted cost concern. Can is not permission; no cutoff criteria, deadline or actual removal is supplied.',
'C15':'Built-copy requirement preserves every single release listed, to-run-at-all purpose and guix-alternative objection. Technical necessity versus institutional obligation remains unresolved; no authority is inferred from have to. The later loop proposal is a prospective workaround, not evidence the current claim is false.',
'C16':'Configure is the inferred editorial action; we remains its explicit causative subject, while the filename becomes an inferred target. Hardcoding replacement, local availability and unchanged all-binary fetch default survive. The conditional discretion statement clarifies rather than demonstrates uptake.',
'C17':'Conditional up-to allocation is retained as a constitutive candidate at ordinary testing level, with technical-behavior and regulative-permission alternatives. It does not allocate authority over collective decisions. The proposed loop and all-binary default explicitly limit the claim.',
'C20':'Passive dropped directly names EOL versions as patient; no human actor is invented. Maybe and the coordinated question make the suggestion tentative. Its replacement counterpart and old-to-modern wallet priority remain attached.',
'C21':'Repository hosts fixtures is directly supplied; it is not a guessed human operator. Instead and the coupled EOL-removal alternative preserve the replacement method. No obligation or performed hosting is established.',
'C23':'If-going-ahead condition, advisory should, update target and 24.0.1 execution constraint are explicit. The author report is distinct from retained patch plus merge. These support the concrete version update, not publication of archives or adoption of the reviewer\'s rationale.',
'C27':'Keep open and occasional rebase remain a coupled method, with separate actions/targets and the correct shared main-clause we. Prior practice is reported; no fixed deadline or dependent-PR condition is added. Broader merge does not prove rejection of the method.',
'C28':'The negative action not rush merging is directly stated, so the parse/action basis was corrected to literal/explicit while recommendation force remains inferred. Original speech asserts a reason. The quoted failure claim retains the smoke-test exception; reported thorough PR checking is not independently verified.',
'C30':'Prune versions in a follow-up is an available option, not formal permission or a promised task. Always marks availability and no specific follow-up object is invented.',
'R01':'Only-latest-per-missing-feature is a proposed review criterion, not authorized rule. The referenced commit gives related txindex/mempool examples, not required wallet exclusion or independent recognition from echoed ACKs. The wallet non-EOL minimum challenges its application here.',
'R02':'The relevant you is the subject of the main need-to-remove clause, not merely the earlier conditional pronoun. Requirement is conditional and disjunctive; remove 23.x is one alternative, with no exclusive ban on doing both and no formal enforcement.',
'R03':'Explain has the complete informational object why 24.x is special. Actor, modal and activation condition are shared-scope inferences from the coordinated clause, not local explicit occurrences. The specialness premise is challenged by the author\'s verification argument.',
'R04':'See is a distinct navigation instruction and the complete commit is the object. The target is not PR #26586, so that PR\'s merge is not assigned as the reference\'s disposition.',
'R05':'Someone remains the explicit actor and that the explicit object of do, resolved to selection cleanup. Reconstructed I was shortened to apply, separating it from the object. Other versions in this file, unrelated and separate pull constrain scope. Cleanup ACK is broader ordinary assent.',
'R06':'Wallet-specific domain, always, at least, recent majors, not-yet-EOL and no-substitution floor all survive. The quote in later assent is narrower, so recognition was reduced to broader_principle and ordinary assent. Patch retention of 23/24 is only broader-proposal application, not evidence of EOL chronology or a generally adopted floor.',
'R07':'The source explicitly supplies I and verify. The summary was corrected so master-created-wallet opening is an example of verifying the no-special-difference assumption, not its entire meaning. Both refers to 23.x and 24.x; no test result is inferred.',
'R09':'Exclude is an inferred action and cleanup an inferred target from a declarative scope judgment; PR boundary is separated as inferred Cex. General cleanup assent remains attached. The guide gives only broader focus language and temporally unresolved applicability, not authority for this exact boundary. Pinned-source checker mismatch remains documented.'}
CTX={
'C01':'Speculative release/wallet-bug claim; no specific instruction. Indirect-delay alternative is visible.',
'C04':'Concept NACK plus reasons is a distinct review act and challenge, not a withdrawal, sanction or rejection outcome.',
'C07':'Technical miniscript-coverage premise used to challenge the wallet rationale.',
'C08':'Qualified dislike and predicted poor efficacy of general tests, used as the original of a repeated quotation.',
'C10':'Attributed low-cost defense, not a duty or empirically independently verified cost estimate.',
'C12':'Conditional future-cost objection remains a question and challenge context; a removal-plan request is only an alternative.',
'C14':'Explicit denial of the low-cost claim with its quoted target.',
'C18':'Predicted unchanged fetching default attaches to the design proposal and discretion, not a new institutional status.',
'C19':'Relative technical testing priorities supply rationale; no independently specified action beyond the linked proposal.',
'C22':'Attributed failure-investigation assertion preserves the exception for recurring smoke failures; no sanctions or verified neglect inferred.',
'C24':'Report of rebase/update preserves temporary archive unavailability; not evidence the archives later appeared.',
'C25':'Ping and uncertainty retain question form. No definite invitation act is added absent reliable request specification.',
'C26':'Exact-head tACK and test report are ordinary review evidence, not recognition of every proposed expectation.',
'C29':'Qualified agreement responds to the quoted retention core; no interpersonal norm recognition is presumed.',
'R08':'ACK on cleanup in general is ordinary assent, qualified by excluding cleanup from this PR.'}
reviews=[]
for u in A['units']:
 uid=u['unit_id'];repair_ids=[x['change_id'] for x in LOG if x['unit_id']==uid]
 if u['record_role']=='statement':
  note=NOTES[uid];es=[{'source_id':u['source_id'],'span':u['span']}]
  es += [e for q in u['proposition']['qualifiers'] for e in q['evidence']]
 elif u['record_role']=='quotation':
  note='Repeated quotation linked to its represented original clause(s). No extra endorsement or institutional standing is counted. Speech act reflects the quoted claim/question; partial quotes do not import missing original scope automatically.'
  es=[e for r in A['relations'] if r['type']=='quotes' and r['from_unit_id']==uid for e in r['evidence']]
 else:note=CTX[uid];es=[{'source_id':u['source_id'],'span':u['span']}]
 reviews.append({'unit_id':uid,'status':'corrected' if repair_ids else 'retained','repair_ids':repair_ids,'review':note,'evidence':distinct(es),'remaining_alternative':u['alternative_interpretation']})
# Every source screened again in this one review pass; supplements are not negative cases.
screen=[]
for sc in A['entry_screening']:
 e=E[sc['source_id']];t=e['text'];es=[]
 if t:
  if e['kind']=='dated_guidance':es=[ev(e['source_id'],'Patchsets should always be focused.'),ev(e['source_id'],'Whether a pull request is merged into Bitcoin Core rests with the project merge\nmaintainers.')]
  else:es=[ev(e['source_id'],t if len(t)<1000 else t[:min(len(t),1000)])]
 screen.append({'source_id':e['source_id'],'status':'retained','focal':e['source_id'] in PK['selection_design']['focal_source_ids'],'disposition':sc['disposition'],'unit_ids':sc['unit_ids'],'review':sc['reason'],'evidence':es,'empty_text_confirmed':not t.strip()})
# One result for every flag occurrence, including repeat checker outputs.
checknames=['checks.first.json','checks.mechanical_01.json','checks.final_attempt_01.json','checks.source_review_01.json','checks.json']
res=[];er=[]
challenge_rel=[r for r in A['relations'] if r['type']=='challenges']
summaries=[('observed_outcomes',i,x) for i,x in enumerate(A['episode_summary']['observed_outcomes'])]+[('mechanisms',i,x) for i,x in enumerate(A['episode_summary']['mechanisms'])]
for name in checknames:
 r=json.loads((p/name).read_text());counters=collections.Counter()
 if 'error' in r:
  er.append({'checker_file':name,'status':'corrected','code':'execution_exception','message':r['error'],'resolution':'The source-review application script failed before writing annotation.final.json because its helper expected a quote. No annotation mutation had been saved. The helper was corrected, final output was created, and the checker was rerun; this original result is preserved.','evidence':[]})
 for error in r.get('errors',[]):
  code=error['code'];uid=error.get('unit_id');status='unresolved' if code=='revision' else 'corrected'
  if code=='revision':
   why='The frozen checker tests only blob_sha or revision_id. The frozen guide source supplies revision and git_blob_sha instead. The annotation correctly retains pinned_revision with unresolved temporal fit. Neither input nor code is modified to force a pass; the compatibility flag is unresolved mechanically, while supplied provenance is visible.'
   es=D['R09']['institution']['documentary_support'][0]['evidence']
  else:
   repairs=[x for x in LOG if x['unit_id']==uid and x['stage']=='mechanical_repair'];why=' '.join(x['reason'] for x in repairs);es=[e for x in repairs for e in x['evidence']]
  er.append({'checker_file':name,'code':code,'unit_id':uid,'status':status,'resolution':why,'evidence':distinct(es)})
 for ix,f in enumerate(r.get('review_flags',[])):
  code=f['code'];uid=f.get('unit_id');j=counters[(code,uid)];counters[(code,uid)]+=1;status='retained';selector=None
  if code=='predicate_audit':
   c=D[uid]['components'][j];selector={'component_index':j,'symbol':c['symbol']};es=c['evidence']+[c['governing_span']]
   if (uid,c['symbol']) in [('C03','Bdir'),('C11','Cex'),('R05','I'),('R09','I'),('R09','Cex'),('C28','I')]:status='corrected'
   why=NOTES[uid]+' Component review: '+(c['inference_note'] or ('The cited expression supplies the '+c['symbol']+' role in its governing clause; no other predicate or merely matching pronoun is substituted.'))
  elif code=='qualifier_audit':
   u=D[uid];es=[{'source_id':u['source_id'],'span':u['span']}]+[e for q in u['proposition']['qualifiers'] for e in q['evidence']];why=NOTES[uid]
   if uid in ['D01','R01','R07']:status='corrected'
  elif code=='application_audit':
   x=D[uid]['institution']['application_evidence'][j];es=x['evidence'];why=x['rationale']+' '+NOTES[uid];selector={'application_index':j};status='corrected' if uid=='B01' else 'retained'
  elif code=='challenge_audit':
   x=D[uid]['institution']['challenges'][j];es=x['evidence']+[{'source_id':D[uid]['source_id'],'span':D[uid]['span']}];why=x['rationale'];selector={'challenge_index':j}
  elif code=='higher_level_audit':
   u=D[uid];es=u['level_evidence']['evidence'];why=u['level_rationale']+' No constitutional or epistemic level is claimed.';status='corrected';selector={'dimension':'observed_action_level','primary':u['observed_action_level'],'alternatives':u['observed_level_alternatives']}
  elif code=='document_scope':
   x=D[uid]['institution']['documentary_support'][j];es=x['evidence'];why=x['rationale']+' The document is not treated as specific authority for the cleanup boundary. Exact historical applicability remains unresolved, and checker field-name incompatibility remains separately recorded.';status='unresolved';selector={'documentary_index':j}
  elif code=='challenge_object':
   x=challenge_rel[j];es=x['evidence'];why=x['rationale'];selector={'relation_from':x['from_unit_id'],'relation_to':x['to_unit_id']}
  elif code=='summary_audit':
   group,k,x=summaries[j];es=x['evidence'];selector={'group':group,'index':k};why='Every material clause is retained as a claim_part with exact evidence. '+('The claim is bounded to reported acts, retained artifacts or the recorded same-PR status; no causality, adopted norm or network deployment is added.' if group=='observed_outcomes' else x['alternative_explanation']+' Status '+x['status']+' is a sequence judgment, not causal identification.')
  else:raise RuntimeError('Unhandled flag '+code)
  res.append({'checker_file':name,'flag_index':ix,'code':code,'unit_id':uid,'selector':selector,'status':status,'resolution':why,'evidence':distinct(es)})
# Additional whole-record review for dimensions not necessarily flagged by the checker.
event_reviews=[]
for u in A['units']:
 for group in ['recognition','authority_evidence']:
  if group=='authority_evidence':continue
  for j,x in enumerate(u['institution'][group]):event_reviews.append({'unit_id':u['unit_id'],'kind':'recognition','index':j,'status':'corrected' if u['unit_id']=='R06' else 'retained','review':x['rationale'],'evidence':x['evidence'],'object_id':x['object_id']})
 for j,x in enumerate(u['disposition_events']):event_reviews.append({'unit_id':u['unit_id'],'kind':'disposition','index':j,'status':'retained','review':x['rationale'],'evidence':x['evidence'],'object_id':x['object_id']})
review={'run_id':'F01_v04_r3','review_round':1,'review_type':'complete source-based self-review after first-complete freeze and mechanical repair','completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_access_boundary':'Only assigned run directory. No new source retrieval, other runs, parent research history or agent outputs.','coverage':{'entries_screened':len(E),'focal_entries_exhaustively_reviewed':len(PK['selection_design']['focal_source_ids']),'units_reviewed':len(D),'statement_units':sum(u['record_role']=='statement' for u in D.values()),'all_outcomes_and_mechanisms_reviewed':True,'review_domains':['screening omissions','material qualifications','predicate and argument roles','literal versus pragmatic basis','authority and type','recognition, attribution and episode independence','reported versus observed application','dispositions and object identity','target and observed governance levels','relations and quotation direction','every outcome/mechanism clause']},'screening_review':screen,'unit_reviews':reviews,'checker_error_resolutions':er,'checker_flag_resolutions':res,'event_reviews':event_reviews,'global_findings':[{'status':'retained','finding':'No focal rule_candidate is justified by a specific authorization or attributed enforcement basis. Guide role language and observed merger are not transferred into authority for every review criterion.','evidence':[ev('pr26586:review_comments:0'),ev('guide:contributing','Whether a pull request is merged into Bitcoin Core rests with the project merge\nmaintainers.')]},{'status':'retained','finding':'Ordinary ACKs, quoted agreement and bot echoes are not counted as independent expectation recognition. No repeated interpersonal standing is established.','evidence':[ev('pr26586:comments:15'),ev('pr26586:review_comments:2','ACK on cleaning up the releases list in general')]},{'status':'retained','finding':'Merge is a broader contribution outcome except the version-update proposition whose specific patch is supplied. No rejection, sanction or network adoption is inferred.','evidence':[ev('pr26586:metadata','"merged": true'),ev('pr26586:patch:0','+            240001,')]}],'remaining_limits':A['episode_summary']['missing_evidence']+A['episode_summary']['unresolved_questions'],'checker_compatibility_limitation':{'status':'unresolved','unit_id':'R09','checker_file':'tools/check_annotation.py','checker_condition':"d['date_basis']=='pinned_revision' and not any(entries[e['source_id']].get('blob_sha') or entries[e['source_id']].get('revision_id') for e in d['evidence'])",'packet_source_id':'guide:contributing','supplied_metadata':{k:E['guide:contributing'][k] for k in ['revision','git_blob_sha','source_as_of','timestamp_kind','object_id']},'resolution':'Retain correct source metadata interpretation and the supplied checker result. No frozen input is changed; no mechanical pass is claimed.'}}
(p/'review_notes.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
# Integrity check is a byte-level operation, not reading calibration for answers.
manifest=json.loads((p/'input_manifest.json').read_text());integrity=[]
for name,expected in manifest['files'].items():
 actual=hashlib.sha256((p/name).read_bytes()).hexdigest();integrity.append({'path':str(p/name),'expected_sha256':expected,'actual_sha256':actual,'unchanged':actual==expected})
(p/'input_integrity_check.json').write_text(json.dumps({'all_unchanged':all(x['unchanged'] for x in integrity),'files':integrity},indent=2)+'\n')
originals=list(manifest['files'])+['input_manifest.json']
created=[str(f.relative_to(p)) for f in p.rglob('*') if f.is_file() and str(f.relative_to(p)) not in originals]
access={'run_id':'F01_v04_r3','configuration':'inherited primary; no override','model_identity':None,'provider_snapshot':None,'seed':None,'sampling_parameters':None,'reasoning_effort':None,'tokens':None,'cost':None,'configuration_basis':'The assignment exposed inherited primary configuration only. No model identity is inferred from protocol, manifest, filenames or historical study instructions.','runtime':{'python_version':sys.version,'execution':'python3 via exec_command; functions orchestration','libraries':['json','hashlib','copy','pathlib','collections','sys','datetime','jsonschema'],'ordinary_library_runtime_access_only_outside_run_directory':True},'research_inputs_accessed':[{'path':str(p/name),'mode':'content read and integrity hash'} for name in ['INSTRUCTIONS.txt','protocol/codebook.txt','protocol/annotation_schema.json','packet.json','tools/check_annotation.py','input_manifest.json']],'calibration_access':[{'path':str(p/name),'mode':'directory name/size and integrity SHA256 only; contents not exposed to coder or used as examples'} for name in manifest['files'] if name.startswith('calibration/')],'own_outputs_accessed_or_written':[str(p/name) for name in sorted(created)]+[str(p/'access_record.json')],'prohibited_accesses':{'other_runs':False,'parent_research_history':False,'Library':False,'web_or_external_sources':False,'other_agent_answers':False,'agents_spawned':0},'coordinator_messages':'Task dispatch and stage-status coordination only; no substantive answer or source supplied by another coder.','execution_incidents':[{'stage':'initial construction','incident':'An initial functions JS syntax error prevented the intended shell call from executing; no file was written by that call.'},{'stage':'self-review application','incident':'A helper missing an optional quote argument failed before saving changes. The checker then found no annotation.final.json. That result is preserved in checks.final_attempt_01.json; helper and file creation were corrected.'}],'all_originals_unchanged':all(x['unchanged'] for x in integrity),'review_rounds':1,'final_checker_status':'fail','remaining_checker_errors':1,'remaining_error_summary':'Pinned revision metadata field-name mismatch, documented in review_notes.json.'}
(p/'access_record.json').write_text(json.dumps(access,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'unit_reviews':len(reviews),'source_reviews':len(screen),'flag_occurrence_resolutions':len(res),'checker_error_resolutions':len(er),'repairs':len(LOG),'all_originals_unchanged':access['all_originals_unchanged']},indent=2))
