import json,hashlib,sys,copy
from pathlib import Path
ROOT=Path.cwd()
A=json.loads(Path('annotation.final.json').read_text());P=json.loads(Path('packet.json').read_text());S={e['source_id']:e for e in P['entries']};U={u['unit_id']:u for u in A['units']}
log=json.loads(Path('repair_log.json').read_text())
def ev(s,q,start=0):
 i=S[s]['text'].index(q,start);return {'source_id':s,'span':{'start':i,'end':i+len(q),'quote':q}}
def eu(k):return {'source_id':U[k]['source_id'],'span':copy.deepcopy(U[k]['span'])}
def comp(k,sym):return next(c for c in U[k]['components'] if c['symbol']==sym)
# Every flag from each retained checker execution receives a source-based disposition.
flag_resolutions=[]
for filename in ['checks.first.json','checks.after_mechanical.json','checks.json']:
 check=json.loads(Path(filename).read_text())
 for j,f in enumerate(check.get('review_flags',[])):
  k=f['unit_id'];sym=f['symbol'];c=comp(k,sym);status='retained';evidence=copy.deepcopy(c['evidence']);rationale=''
  if k=='need_rebase':
   status='corrected';rationale='The original it anchor occurred inside bit, outside the rebase clause. M01 replaces it with the actual subject it in Meanwhile it needs a rebase. Its transformed receiver role remains context_inferred/semantic_inference.'
  elif k=='b_method':rationale='The body’s elliptical procedure lacks an explicit release-addition object. The title resolves that target contextually, and the same body’s simpler-now clause qualifies the current procedure. Both reconstructed receiver and recurrence roles are marked inferred; the complete identifiers in the separate referral remain literal.'
  elif k=='bot_ignore':rationale='The preceding if-clause and negative-reaction instruction share procedural scope with and the bot will ignore it. Context-inferred/shared_scope is retained for this announced trigger; actual use and the precise it referent remain unresolved.'
  elif k=='hold_off':rationale='Hold off explicitly states the action but omits its target. The PR context and immediately preceding release concern support advancing this PR as a contextual target; an acknowledgment-only alternative remains. Neither participant role nor an integration authority is inferred.'
  elif k=='developer_choice':
   status='corrected' if f.get('occurrence_role')=='local' else 'retained';rationale='In that case is locally stated, while the preceding loop proposal resolves its reference. Context_reference records that evidence use and retains the explicit conditional role; the redesigned arrangement remains hypothetical.'
  elif k=='drop_eol':rationale='The coordinated clause expressly pairs dropping EOL versions with hosted regtest wallets instead. Shared_scope/context_inferred preserves the replacement qualification rather than coding unconditional deletion.'
  elif k=='host_regtest':
   status='corrected' if f.get('occurrence_role')=='local' else 'retained';rationale='Instead is local but refers back to the EOL-version approach. Context_reference, rather than local, declares the external antecedent evidence. The source’s repository actor is not replaced by an invented person.'
  elif k=='occasionally_rebase' and sym=='A':
   status='corrected' if f['evidence']['span']['start']!=c['evidence'][0]['span']['start'] else 'retained';rationale='The actor shared by leave and rebase is the operative we could clause. The earlier we in as-we-have-done-before expresses historical precedent and was replaced even though the referent likely overlaps.'
  elif k=='occasionally_rebase' and sym=='Bdir':
   status='corrected' if f.get('occurrence_role')=='local' else 'retained';rationale='It has an explicit object role under rebase; the preceding the PR resolves its antecedent. Context_reference correctly covers both evidence locations without changing the literal object role.'
  elif k in ['remove23','explain24'] and sym=='A':
   status='corrected' if f['evidence']['span']['start']!=c['evidence'][0]['span']['start'] else 'retained';rationale='The operative you in you will either need to governs both alternative actions. It replaces the same pronoun from the subordinate if-you-want clause; no actor identity or authority is added.'
  elif k in ['remove23','explain24'] and sym=='D':rationale='Need to is the operator shared by the remove/explain alternatives. The source supplies the requirement explicitly; will is not separately treated as a deontic. No authorized rule or sanction follows from the need wording.'
  elif k in ['remove23','explain24'] and sym=='Cac':rationale='If you want to add 24.x activates the whole either/or requirement and thus both children. Shared_scope preserves this explicit qualification. OR is retained because the text does not prohibit performing both actions.'
  elif k=='separate_cleanup' and sym=='I':rationale='Do that is elliptical. The prior other-version criterion and later general-cleanup ACK justify the reconstructed cleanup action, marked context_inferred/semantic_inference. The later ACK cannot independently establish the exact earlier criterion or authority.'
  elif k=='cleanup_outside':rationale='The adjacent cleanup ACK supplies the antecedent of that. Its new role as receiver of reconstructed keep is inferred, despite the words being present in the source; context_reference and the inference note preserve that distinction.'
  elif k=='loop_available' and f['kind']=='pragmatic_explicit_argument':rationale='We is explicitly the subject of could have it loop. Reconstructing the causative edit as change preserves this actor role, while the file’s target role and behavior constraint are separately inferred. Could remains exploratory rather than permission.'
  elif k=='separate_cleanup' and f['kind']=='pragmatic_explicit_argument':rationale='Someone explicitly performs could do that and remains the actor of reconstructed cleanup. The identity is unknown; the transformation does not invent a responsible maintainer or volunteer.'
  assert rationale,(filename,f)
  flag_resolutions.append({'checker_file':filename,'flag_index':j,'flag':f,'status':status,'evidence':evidence,'rationale':rationale})
error_resolutions=[]
for filename in ['checks.first.json','checks.after_mechanical.json','checks.json']:
 for j,f in enumerate(json.loads(Path(filename).read_text()).get('errors',[])):
  k=f['unit_id'];sym=f['symbol'];c=comp(k,sym)
  error_resolutions.append({'checker_file':filename,'error_index':j,'error':f,'status':'corrected','evidence':copy.deepcopy(c['evidence']),'rationale':('The actual rebase-clause pronoun replaces the incidental substring inside bit; see M01.' if k=='need_rebase' else 'The evidence resolves an outside-unit antecedent. M02–M04 change occurrence_role to context_reference while preserving the explicit local grammatical role. Final checks report no errors.')})
manual={
'b_method':'Corrected recurrent-method qualifications, dispute over application, and inferred recurrence role. This remains a strategy candidate with a technical-description alternative; merger is only broader-proposal status.',
'b_nav':'Both full commit identifiers and version labels are preserved. A single see action takes the paired references as its object; the method is not implemented merely by this referral.',
'b_notags':'Preserves we, the full negative need operator, tag-list locations, and anymore. Technical elimination of a dependency versus no obligation remains unresolved in interpretation.',
'bot_nav':'Purpose is Cex, not an invented activation condition. The mutable link and pinned supplemental revision are distinguished; no authority is imputed to this referral.',
'bot_react':'Incorrect-listing condition, 👎 method, and this-comment target survive. Please is politeness, and the addressee is inferred from your rather than a named role.',
'bot_ignore':'Will predicts the announced bot response rather than imposing a duty. The trigger is shared inferred scope, the next-update timing is explicit, and the exact object ignored remains unresolved.',
'hold_off':'Retains explicit hold-off action and a-bit limit. Target is contextually inferred; no missing author identity, required waiting period, or observed implementation is supplied.',
'need_rebase':'Corrected incidental substring and scoped implementation report to the broader PR: a reported rebase on master does not verify the after-#26589 condition. Technical versus normative need remains unresolved.',
'every_major':'Every major release is an unrestricted recurring inclusion criterion, distinct from minimum recent-non-EOL coverage. Later per-feature selection contests this criterion; no exact adoption or enforcement is demonstrated.',
'add_v24':'Preserves v24.0 or whatever becomes widely available and the separate #25717 rationale. Should qualifies justificatory sufficiency and is not coded lexical D. The wallet-test counterargument now has its own correct endpoint.',
'specific_tests':'Use and its target role are reconstructed from a preference; I is the evaluator, not an assumed executing actor. The full illustrative test-finding command is retained as an object qualifier without inventing another request.',
'keep_open_dependency':'The articulated open-PR method retains its until-another-PR-needs-it limit. Can supplies an option, not institutional permission. Broad merger status does not establish this dependency method was adopted.',
'remove_intermediate':'Intermediate releases and at some point survive. Capability-versus-recommendation remains unresolved; there is no authority or concrete removal event.',
'built_copies':'Preserves the purpose, every single listed release, and rejection of the guix-binary alternative. Have to is lexical need with unresolved technical versus institutional force, not evidence of a rule or sanction.',
'loop_available':'Preserves replacement of hardcoded version numbers by looping over available releases/v*. A remains explicit because source we performs the causative action; I, target role, and reconstructed execution constraint are inferred.',
'developer_choice':'Conditional choice is assigned to individual operational testing, with collective-choice deliberation as the visible proposal. A constitutive allocation of practical discretion is plausible; formal authority and implementation remain unestablished, with a regulative alternative preserved.',
'drop_eol':'A passive target does not require an invented actor. The shared replacement qualification connects removal to hosted test wallets; the tentative question is not an obligation.',
'host_regtest':'Repo is the literal hosting actor and some regtest wallets the object. Instead references the EOL approach; no human operator or adopted system is inferred.',
'update_2401':'Still-going-ahead condition and exact 24.0.1 target are retained. The author specifically reports this version update, while archive availability and actual testing remain qualified.',
'leave_open':'One child of the explicit open-and-rebase method. Could is exploratory; leave-open is not a prohibition on eventual merger.',
'occasionally_rebase':'Corrected shared actor to the operative we-could clause. Frequency and PR antecedent are preserved; this is proposed future maintenance, not a report of new rebases.',
'not_rush':'Negation remains within not rush and the nominal object is merging new releases. Possible reason is an asserted recommendation, not mandatory non-integration.',
'followup_prune':'Keeps versions, always, and in-a-followup without inventing a numbered proposal or deadline. Can remains unresolved capability versus suggestion.',
'latest_per_feature':'Latest release for each missing feature and restrictive only survive. The wallet-test application is disputed; precedent supplied by a commit does not establish institutional authorization.',
'remove23':'Keeps shared need-to operator, full conditional activation, and exact 23.x object. Corrected operative subject and declarative asserted speech-act coding. OR links the justification alternative; no sanction or veto is inferred.',
'explain24':'Keeps exact informational object why 24.x is special and the shared condition. Corrected operative subject, asserted speech act, and request-to-response uptake direction. A reply is not recognized obligation.',
'inline_nav':'Independent see-also action with a complete commit identifier is retained, without importing that commit’s outcome or selection rationale as a binding rule.',
'separate_cleanup':'Someone is the explicit actor of elliptical do-that; action and other-versions target roles are inferred. Separate-pull constraint is explicit. General cleanup endorsement is broader than the exact selection criterion.',
'minimum_recent':'Retains wallet-test scope, always, at least, recent major, not-yet-EOL, and bare-minimum comparison. The exact quoted tentative agreement supports local recognition of this proposed arrangement, not rule authority or general adoption. It is not automatically marked disputed merely because it counters an earlier view.',
'verify_assumption':'The articulated personal verification method preserves the assumption, master-created wallets, and both versions. Preferred testing is not recoded as completed testing. I is anchored to the appropriate contraction, not the earlier evaluator clause.',
'cleanup_outside':'Reconstructs keep cleanup outside this PR; all transformed roles are labeled inferred and the antecedent is exact. Norm candidate reflects the scope expectation without a claimed enforcement power.'
}
unit_review=[]
changed_names=set()
for ch in log['changes']:
 for key in ['unit_id','affected']:
  if ch.get(key):changed_names.add(ch[key].split('.')[0])
for u in A['units']:
 k=u['unit_id'];role=u['record_role']; evidence=[eu(k)]
 for c in u['components']:
  if c['basis']!='explicit' or c['occurrence_role']!='local':evidence+=c['evidence']
 if role=='statement':conclusion=manual[k]
 elif role=='quotation':
  links=[r for r in A['relations'] if r['from_unit_id']==k and r['type']=='quotes'];conclusion='Repeated occurrence checked against its linked original. Original communicative function is retained; no new endorsement, expectation, or proposition is counted. Grammar, components, institution, and statement-target level correctly reflect a nonstatement record.';evidence += [eu(r['to_unit_id']) for r in links]
 elif role=='container':conclusion='Compound boundary and child qualifiers checked. Container contributes no extra statement, components, institutional classification, or observed-action level; action logic is preserved by AND or OR.'
 elif k=='wallet_support_reason':conclusion='New context endpoint isolates the challenged watch-only-miniscript rationale from #25717. The correction challenges relevance to the test rather than the existence of the feature.'
 else:conclusion=u['institution']['rationale']+' The exact source was checked for a distinct directive, recognition overreach, and temporal or outcome claims; context classification is retained.'
 unit_review.append({'unit_id':k,'status':'corrected' if k in changed_names or k=='wallet_support_reason' else 'retained','reviewed_fields':['screening_and_boundary','qualifications_and_negation','predicate_roles_and_evidence','authority_recognition_and_application','disposition_and_target','governance_levels','relations_and_mechanism_use'],'evidence':evidence,'conclusion':conclusion,'remaining_uncertainty':u['uncertainty_reason'] or u['alternative_interpretation']})
source_review=[]
for sc in A['entry_screening']:
 s=sc['source_id'];entry=S[s]
 if not entry['text']:evidence=[]
 elif s=='guide:contributing':
  evidence=[ev(s,'You are expected to reply to any review comments before your pull request is\nmerged. You may update the code or reject the feedback if you do not agree with\nit, but you should express so in a reply.'),ev(s,'Whether a pull request is merged into Bitcoin Core rests with the project merge\nmaintainers.'),ev(s,'The following applies to code changes to the Bitcoin Core project (and related\nprojects such as libsecp256k1), and is not to be confused with overall Bitcoin\nNetwork Protocol consensus changes.')]
 else:evidence=[ev(s,entry['text'])]
 source_review.append({'source_id':s,'scope':'exhaustive_focal' if s in P['selection_design']['focal_source_ids'] else 'supplemental_context_screening','status':'corrected' if s=='pr26586:comments:4' else 'retained','final_disposition':sc['disposition'],'unit_ids':sc['unit_ids'],'evidence':evidence,'conclusion':sc['reason'],'review_limit':('Empty supplied text was inspected; metadata does not supply missing speech.' if not entry['text'] else 'All supplied text reviewed. Context-only supplemental status does not imply absence of institutional content.' if s not in P['selection_design']['focal_source_ids'] else 'Every supplied sentence, question, quote, and negative case was checked; unavailable edit history and threading remain unavailable.')})
relation_review=[]
corrected_edges={('no_miniscript_test','wallet_support_reason'),('explain24','verify_assumption'),('release_concern','hold_off'),('status_ping','tested_ack'),('need_rebase','rebase_update_report'),('b_notags','b_method')}
for i,r in enumerate(A['relations']):
 conclusion=r['rationale']
 if r['type']=='quotes':conclusion+=' Source identity and exact original correspondence checked; repeated text is not independent evidence of recognition.'
 elif r['type'] in ['AND','OR']:conclusion+=' Child action scopes and shared qualifiers checked; no parent is counted as a statement.'
 elif r['type']=='uptake':conclusion+=' Direction checked from initiating statement to response/report, with target specificity and explicit-versus-inferred basis retained.'
 elif r['type']=='temporal':conclusion+=' Entry timestamps are supplied metadata, so ordering remains context_inferred rather than explicit sequence or causation.'
 relation_review.append({'relation_index':i,'from_unit_id':r['from_unit_id'],'to_unit_id':r['to_unit_id'],'type':r['type'],'status':'corrected' if (r['from_unit_id'],r['to_unit_id']) in corrected_edges else 'retained','evidence':r['evidence'],'conclusion':conclusion})
event_review=[]
for u in A['units']:
 for group,events in [('recognition',u['institution']['recognition']),('disposition',u['disposition_events'])]:
  for i,event in enumerate(events):event_review.append({'unit_id':u['unit_id'],'group':group,'event_index':i,'status':'corrected' if u['unit_id']=='need_rebase' else 'retained','kind':event['kind'],'target':event['target'],'basis':event['basis'],'evidence':event['evidence'],'conclusion':event['rationale']})
outcome_notes=[
 'Exact author report supports both named maintenance acts and the unavailable-archives caveat. Neither downloaded binaries nor completed testing is claimed.',
 'Retained patch sources identify wallet and fetch-script files and show v24.0.1 added alongside v23.0. No revision chronology or reviewer causation is claimed.',
 'Full head identifier, current-master check, and the open/rebase alternative are all directly evidenced; the ACK is not generalized to all policies.',
 'Recorded merged boolean, merger timestamp, actor account, and PR number support only repository integration. No participant status is inferred from the merger alias.',
 'Exact quoted baseline plus tentative agreement support local recognition of the proposed recurring arrangement. Binding force, authority, enforcement, and general adoption remain absent.'
]
outcomes_review=[{'outcome_index':i,'status':'retained','claim':o['claim'],'evidence':o['evidence'],'conclusion':outcome_notes[i]} for i,o in enumerate(A['episode_summary']['observed_outcomes'])]
mechanism_notes=[
 'Addressed conceptual response, competing criteria, verification rationale, quote, and tentative agreement each have evidence. Causal prompted wording was removed; supported_sequence describes correspondence only.',
 'Version-update request/report correspond. The rebase report does not establish the after-#26589 condition, now stated explicitly. Initiation, response, intervening reported action, and unverified execution are distinguished.',
 'Separate-pull suggestion, general cleanup ACK, scope judgment, follow-up idea, and retained patch all have support. Their causal connection remains consistent_with, with preexisting patch scope as an alternative.',
 'Bot trigger and announced consequence are supported but no use, implementation, or institutional effect is observed. Status remains unresolved rather than a successful correction or sanction.'
]
mechanisms_review=[{'mechanism_index':i,'status':'corrected' if i<2 else 'retained','claim':m['claim'],'evidence':m['evidence'],'mechanism_status':m['status'],'conclusion':mechanism_notes[i]} for i,m in enumerate(A['episode_summary']['mechanisms'])]
review={'run_id':'F01_v03_r2','episode_id':'F01','review_passes':1,'review_type':'complete source-based self-review after mechanical repair','input_snapshot':'annotation.after_mechanical.json','final_snapshot':'annotation.final.json','checker_error_resolutions':error_resolutions,'checker_flag_resolutions':flag_resolutions,'source_screening_review':source_review,'unit_review':unit_review,'relation_review':relation_review,'recognition_and_disposition_review':event_review,'outcome_review':outcomes_review,'mechanism_review':mechanisms_review,'authority_and_levels_review':{'status':'retained','evidence':[ev('guide:contributing','Whether a pull request is merged into Bitcoin Core rests with the project merge\nmaintainers.'),ev('guide:contributing','You are expected to reply to any review comments before your pull request is\nmerged. You may update the code or reject the feedback if you do not agree with\nit, but you should express so in a reply.'),eu('latest_per_feature'),eu('minimum_recent'),eu('developer_choice')],'conclusion':'The dated guide supports general review and integration context, not a claim that particular inclusion criteria have authorized rule status. No rule_candidate, constitutional, or epistemic focal statement is asserted. Recurring coverage choices are distinguished from operational edits, with bounded operational/collective-choice alternatives. The conditional developer choice concerns individual test execution rather than power to make collective-choice rules. The guide revision timestamp does not date every provision or establish an unchanged earlier mutable-link version.'},'unresolved_limits':A['episode_summary']['missing_evidence']+A['episode_summary']['unresolved_questions'],'review_summary':{'screened_entries':len(A['entry_screening']),'focal_entries':len(P['selection_design']['focal_source_ids']),'units':len(A['units']),'statements':sum(u['record_role']=='statement' for u in A['units']),'relations':len(A['relations']),'outcomes':len(A['episode_summary']['observed_outcomes']),'mechanisms':len(A['episode_summary']['mechanisms']),'final_checker_status':json.loads(Path('checks.json').read_text())['status'],'final_checker_errors':0,'final_checker_flags':len(json.loads(Path('checks.json').read_text())['review_flags']),'all_checker_flags_addressed':True,'semantic_certification':False}}
Path('review_notes.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
inputs=['INSTRUCTIONS.txt','protocol/codebook.txt','protocol/annotation_schema.json','packet.json','tools/check_annotation.py']
outputs=['build_annotation.py','mechanical_repairs.py','self_review.py','finalize_records.py','annotation.json','annotation.first_complete.json','annotation.after_mechanical.json','annotation.final.json','checks.first.json','checks.after_mechanical.json','checks.json','repair_log.json','review_notes.json']
access={'run_id':'F01_v03_r2','authorized_directory':str(ROOT),'input_files_accessed':[{'path':str(ROOT/x),'purpose':('Frozen instructions' if x=='INSTRUCTIONS.txt' else 'Assigned frozen source packet' if x=='packet.json' else 'Frozen coding/validation material'),'sha256':hashlib.sha256(Path(x).read_bytes()).hexdigest()} for x in inputs],'generated_files_accessed':[{'path':str(ROOT/x),'purpose':'Local annotation construction, retained validation, or audit output','sha256':hashlib.sha256(Path(x).read_bytes()).hexdigest()} for x in outputs],'additional_created_files':[str(ROOT/'access_record.json')],'ordinary_runtime_access':['Python standard-library json, pathlib, hashlib, copy, sys and transitive imports','Installed jsonschema and its ordinary runtime dependencies, invoked by the supplied checker'],'configuration':{'execution_mode':'inherited primary configuration; no override requested or applied','model_name':None,'reasoning_effort':None,'provider_snapshot':None,'seed':None,'sampling':None,'temperature':None,'top_p':None,'token_use':None,'cost':None,'configuration_evidence':'Dispatch directed inherited primary configuration. No verified model identifier, snapshot, or sampling configuration was exposed. Model labels in the historical codebook were not used to infer execution identity.'},'runtime':{'python_version':sys.version,'python_executable':sys.executable,'shell':'bash','cwd':str(ROOT)},'research_access':{'outside_sources':False,'network_used':False,'parent_or_other_run_files_read':False,'library_used':False,'additional_agents_used':False,'calibration_files_read':False,'restriction':'Only this directory’s assigned inputs and ordinary Python runtime were accessed.'},'validation_history':[{'command':'python3 tools/check_annotation.py packet.json annotation.json','result':'checks.first.json','status':'fail','error_count':4,'annotation_snapshot':'annotation.first_complete.json'},{'command':'python3 tools/check_annotation.py packet.json annotation.json','result':'checks.after_mechanical.json','status':'pass','error_count':0,'annotation_snapshot':'annotation.after_mechanical.json'},{'command':'python3 tools/check_annotation.py packet.json annotation.final.json','result':'checks.json','status':'pass','error_count':0,'annotation_snapshot':'annotation.final.json'}],'self_review_passes':1,'original_inputs_modified':False,'pre_completion_limitations':'The final mechanical pass checks structure and anchors, not semantic truth; all identified interpretive limits remain in review_notes.json.'}
Path('access_record.json').write_text(json.dumps(access,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(review['review_summary'],indent=2))
print('checker_flag_resolutions',len(flag_resolutions),'checker_error_resolutions',len(error_resolutions))
