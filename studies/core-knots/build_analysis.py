"""Reproduce the six-case comparison and a bounded replay of recorded changes."""
from pathlib import Path
from datetime import datetime
import copy, hashlib, json, zipfile

R=Path(__file__).resolve().parent; A=R/'analysis'; A.mkdir(exist_ok=True)
B10=R/'inputs/round10'
B9=R/'inputs/round9'
B5=R/'inputs/round5'
def load(p):return json.loads(p.read_text())
def save(n,d):(A/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def api(n):return json.loads(load(R/'sources'/n)['structuredContent']['content'])
def dt(s):return datetime.fromisoformat(s.replace('Z','+00:00'))
G={x['source_id']:x for x in load(B5/'baseline/sources/baseline_all_source_registry.json')}
E={x['evidence_id']:x for n in [B9/'analysis/evidence_anchors.json', B10/'analysis/evidence_anchors.json'] for x in load(n)}
U={x['unit_id']:x for x in load(B5/'baseline/annotations/corrected_baseline.json')['units']}
PU={x['unit_id']:x for x in load(B9/'sources/podcast_annotations_inherited.json')['units']}
P={x['evidence_id']:x for x in load(B9/'sources/podcast_passages.json')}
cases=load(B9/'analysis/decision_reconstruction.json')

# A platform event is distinct from its normative interpretation and from adoption.
events=[]; refreshed=[]
for c in cases+[{'case_id':'C6B','pr':33473,'metadata_source_id':'M33473'}]:
 pr=c['pr'];raw=api(f'pull_{pr}.json');old=json.loads(G[c['metadata_source_id']]['text'])
 assert all(raw[k]==old[k] for k in ['created_at','closed_at','merged_at','merged']),pr
 assert raw['head']['sha']==old['head_sha'],pr
 actor=raw['merged_by']['login'] if raw['merged'] else api(f'issue_{pr}.json')['closed_by']['login']
 if not raw['merged']:assert api(f'issue_{pr}.json')['closed_at']==raw['closed_at']
 item={'source_id':f'F{pr}','pr':pr,'url':raw['html_url'],'api_url':f'https://api.github.com/repos/bitcoin/bitcoin/pulls/{pr}','author':raw['user']['login'],'base':raw['base']['ref'],'head_sha':raw['head']['sha'],'merged':raw['merged'],'created_at':raw['created_at'],'closed_at':raw['closed_at'],'merged_at':raw['merged_at'],'disposition_actor':actor,'actual_merge_sha':raw['merge_commit_sha'] if raw['merged'] else None,'retrieved_user_date':'2026-11-06','role':'Fresh platform metadata matched to frozen disposition dates and head SHA. Current body wording is not used.'}
 refreshed.append(item)
 events.append({'event_id':c['case_id']+'_disposition','case_id':c['case_id'],'pr':pr,'action':'merge' if raw['merged'] else 'close_unmerged','actor':actor,'author':raw['user']['login'],'actor_is_author':actor==raw['user']['login'],'date_time':raw['merged_at'] or raw['closed_at'],'target_branch':raw['base']['ref'],'actual_merge_sha':item['actual_merge_sha'],'sources':[f'F{pr}',c['metadata_source_id']],'scope':'supporting_backport' if pr==33473 else 'focal_case','publication_observed':None,'adoption_observed':None})
events.sort(key=lambda x:dt(x['date_time']))
save('disposition_sources.json',refreshed);save('disposition_events.json',events)

protocol={
 'unit_of_comparison':'Six linked proposal episodes within one dispute; not six independent observations.',
 'event_order':'Case numbers retain prior identifiers. C2 closes before C1, and C3 opens before C1 closes.',
 'dimensions':[
  {'dimension':'preference','question':'What outcome does this participant favor?','coding_rule':'Record actor, object, and qualification. An expressed preference may coexist with support for another feasible choice.'},
  {'dimension':'normative_claim','question':'What ought an actor to do, or what is an object said to count as?','coding_rule':'Link the existing IG2 unit and retain its standing. Prescriptive wording alone does not establish a shared or enforced norm.'},
  {'dimension':'role_or_control','question':'Who is said to be able or entitled to decide this object?','coding_rule':'Separate documentary allocation, local recognition, an attributed role claim, and observed control. Keep proposal form, integration, moderation, and release targeting distinct.'},
  {'dimension':'exercised_action','question':'What act and immediate result does the record show?','coding_rule':'Use event metadata, identified patch content, or an attributed action report. Do not infer a mandate, persuasion, or downstream adoption from integration.'}
 ],
 'classification_note':'These dimensions are analytical projections, not new mutually exclusive IG2 classes. A statement may express both a preference and a normative claim; a technical reason may be context only.',
 'link_record':'Each connection names source units, the decision object, related evidence or event, warrant, and an inference boundary.',
 'historical_document_scope':'D_CONTRIB is a June 9, 2025 snapshot. It supplies documented context for C3 and later comparisons, not independent proof of its wording in April. D_MOD is a pinned August 14, 2024 revision.',
 'body_version_scope':'Edited proposal bodies identify retained content and attributed links. Do not assign every sentence to the opening timestamp. Round 10 dated comments and identified commits retain their narrower timing role.',
 'causal_scope':'The comparison tests proposed explanations against contrasting outcomes. It does not estimate causal effects, score decentralization, or predict which proposal should merge.',
 'grammar_policy':'Preserve all inherited units and standing. Add zero IG2 statements and perform no new independent validation.'}
save('comparison_protocol.json',protocol)

rows=[
 {'case_id':'C1','pr':32359,'object':'Remove limits and configuration options','preference':'The proposal removes both; the closure account favors retaining configuration through another proposal.','normative_claim':'Review weight depends on arguments rather than repeated ACKs or NACKs.','role_or_control':'petertodd proposes; glozow closes and redirects.','exercised_action':'A nonauthor closes the proposal without merge; local edits had already occurred.','response':'Reported edit uptake precedes a closure over the remaining configuration question.','residual_disagreement':'Future option removal and the replacement proposal remain open.','references':['E01','E05','E06','N901','F32359'],'unit_ids':['U01','U02','U03','U06'],'comparison_limit':'The closure comment follows the event by one second. It explains the disposition; it does not predetermine C3 or prove April wording of the June contribution guide.'},
 {'case_id':'C2','pr':32381,'object':'Allow multiple outputs while retaining per-output limits','preference':'Poinsot seeks a narrower first step and then favors pursuing the earlier alternative after concluding agreement is absent.','normative_claim':'Address the concerns of the identified contributors before pursuing that alternative.','role_or_control':'darosior proposes and closes; ajtowns supplies a technical NACK.','exercised_action':'The author closes his own proposal without merge.','response':'A specific technical objection challenges the narrow design; the author judges his intended regular-contributor agreement absent.','residual_disagreement':'The broader policy and an aggregate-budget design remain available.','references':['E02','E03','E04','N902','F32381'],'unit_ids':['U08','U09a','U09b'],'comparison_limit':'A technical NACK followed by author closure is not evidence that the reviewer exercised a formal veto.'},
 {'case_id':'C3','pr':32406,'object':'Raise the default and allow aggregate budgeting while retaining deprecated options','preference':'The accepted package retains configuration while the merger reports continuing preferences for removal; Mechanic continues to oppose the default change.','normative_claim':'The merger invokes postponement of removal; public claims contest whose reasons and consent should govern.','role_or_control':'instagibbs proposes; reviewers exchange arguments; glozow supplies the readiness account and merges.','exercised_action':'Main-branch integration follows the readiness account and a matched June objection sequence.','response':'Reply and counterreply establish engagement with the selected objection without acceptance of its conclusion.','residual_disagreement':'Future removal, appropriate data use, and wider legitimacy remain disputed.','references':['E07','E08','E09','E10','E11','E30','E31','E32','E37','E38','R10E01','R10E02','R10E03','R10E04','R10E05','F32406','X32406','PE16'],'unit_ids':['D01','D02','D03','D05','D06','U20a','U21e','U22','N15','N16','PU06'],'comparison_limit':'Integration neither proves universal objection resolution nor supplies a network mandate. The selected response by Todd does not independently establish the proposal author’s fulfillment of every review duty.'},
 {'case_id':'C4','pr':32714,'object':'Replace deprecation with non-recommendation','preference':'The author proposes revised discouragement. Towns prefers user choice without discouragement while rejecting the proposed intermediate distinction; other reviewers oppose immediate reconsideration.','normative_claim':'The retained proposal states that removal warnings should correspond to an actual removal plan.','role_or_control':'achow101 proposes and closes; reviewers offer both support and objections.','exercised_action':'The author closes the proposal without merge after the exchange.','response':'The discussion preserves disagreement over wording, timing, and review churn.','residual_disagreement':'The warning principle and the alternative of removing discouragement remain available.','references':['E12','E13','E14','N904','R10E11','R10E12','KJ','F32714'],'unit_ids':['U24','U25','U27','U28a','U28b','U29','U30'],'comparison_limit':'Closure does not reject every premise. Hashpower thresholds remain one participant’s proposals, not operating rules; complete body edit history remains unrecovered.'},
 {'case_id':'C5','pr':33224,'object':'Replace categorical removal wording with an expectation','preference':'Participants support more qualified warning language while raising translation costs during release preparation.','normative_claim':'Hebasto asserts a freeze restriction and proposes acceptance with translation deferred to v31.','role_or_control':'l0rinc proposes; hebasto addresses translation constraints; achow101 merges.','exercised_action':'Integration changes the warning while retaining deprecation and the higher default.','response':'A reported experiment and conditional acceptance identify an implementation route.','residual_disagreement':'Options remain deprecated; actual translation handling and users’ interpretation are not observed.','references':['E15','E16','E17','F33224','X33224'],'unit_ids':['D01','U32','U33','U34'],'comparison_limit':'The patch establishes changed wording, not successful execution of every translation proposal or a general exception to the freeze.'},
 {'case_id':'C6','pr':33453,'object':'Remove deprecation and warning while retaining the higher default','preference':'Poinsot supports undeprecation while favoring fewer options; Mechanic recognizes improvement while demanding broader reversal.','normative_claim':'Warning accuracy recurs; participants recognize a maintainer’s release decision and preserve author choice over proposal form.','role_or_control':'bitschmidty proposes; achow101 merges main; fanquake authors and merges the supporting 30.x backport.','exercised_action':'September 30 main integration and October 6 backport integration are distinct events.','response':'Support for a limited correction coexists with disagreement over wording, release urgency, and wider policy.','residual_disagreement':'The default remains higher; no permanent maintenance commitment, adoption outcome, or agreement on legitimacy follows.','references':['E18','E19','E20','E21','E22','E23','E24','E25','E26','E27','E28','E29','N905','N907','R10E13','R10E14','R10E16','R10E17','R10E18','R10E19','KS','F33453','F33473','X33453'],'unit_ids':['D01','U25','U36','U39','U39b','U41a','U41b','U41c'],'comparison_limit':'Recognition of improvement is not Mechanic’s endorsement. Author discretion over form is not merge authority. The supporting backport is not a seventh focal case.'}
]
for row in rows:
 c=next(c for c in cases if c['case_id']==row['case_id']);e=next(e for e in events if e['case_id']==row['case_id'])
 row['opened_at']=c['created_at'];row['disposed_at']=e['date_time'];row['disposition_event']=e['event_id'];row['outcome']=e['action']
save('case_comparison.json',rows)

links=[]
def link(i,units,cases_,relation,evidence,warrant,boundary):
 links.append({'link_id':f'IL{i:02d}','unit_ids':units,'case_ids':cases_,'relation':relation,'evidence':evidence,'warrant':warrant,'boundary':boundary,'standing_changed':False})
link(1,['U02'],['C1','C3'],'Review weighting',['E32','32359-115','32406-169'],'Local recognition of argument weight plus a later documented allocation of discretion.','No numerical voting or merit weights; the June document is not proof of its exact April wording.')
link(2,['D01'],['C3','C5','C6'],'Integration authority',['E30','F32406','F33224','F33453'],'Documented merge responsibility connected to named platform merge events.','A repository permission and its exercise do not confer authority over the Bitcoin network.')
link(3,['D03'],['C3'],'Judgment before integration',['E32','E08','32406-264','C3_disposition'],'The recorded merger describes weighing reasons and later executes the integration.','The record does not independently verify the adequacy of the judgment or all objections.')
link(4,['D02','D05','D06'],['C3'],'Participation and nonacceptance',['E31','R10E01','R10E02','R10E03','R10E04','R10E05'],'The guidance distinguishes review access, response, and rejection of feedback; the selected sequence illustrates reply without persuasion.','Todd’s reply is not proof that the proposal author fulfilled every review duty. This is a comparison, not a compliance verdict.')
link(5,['U20a','U21e'],['C3','C6'],'Postponed disagreement',['E09','E10','X32406','X33453'],'A stated postponement accompanies retained options and later removal of the warning.','No new standing or permanent maintenance promise; the complete future-removal condition is not tested.')
link(6,['U25'],['C4','C6'],'Reason survives unmerged proposal',['E12','E18','R10E11','KJ','KS','C4_disposition','C6_disposition'],'Retained attribution links the warning expectation across different proposals; outcomes differ.','Compatible later action does not isolate the reason’s causal effect or date every sentence in edited bodies.')
link(7,['U32','U33'],['C5'],'Release constraint and proposed route',['E15','E16','E17','X33224','C5_disposition'],'Participants address a freeze problem and propose deferred translation; the patch changes wording.','The exact freeze prohibition and the route retain text_only standing; actual translation processing is unobserved.')
link(8,['U39'],['C6'],'Recognized release responsibility',['E24','E25','R10E19','C6_disposition','C6B_disposition'],'A specific attribution and deference accompany separate integration events.','Release incorporation is distinct from publication, installation, or a universal rule about all release decisions.')
link(9,['U41a','U41b','U41c'],['C6'],'Author choice over proposal form',['E23','F33453'],'A maintainer explicitly leaves revision, retention, or replacement of the proposal to its author.','The permission concerns proposal form, not authority to integrate it.')
link(10,['N15','N16','PU06','PU07'],['C3'],'Competing legitimacy criteria',['E37','E38','PE16','PE22'],'Claims differ over reasonableness, responsiveness, and the relevant constituency.','No operative community voting threshold is supplied. The later interview does not cause the earlier merge; source-specific standing remains unchanged.')
link(11,['D07','D08','U14','U16b','U18','U19','R4_U19_negative'],['C1','C3'],'Moderation and substantive review',['E33','E34','E35','W04','R10E06','R10E07','R10E08'],'Documented venue rules and specific attributed acts identify controls separate from replying to technical objections.','The April block is not enforcement of the June warning to another actor, nor a match for Mechanic’s interview ban claim. No general fairness finding.')
link(12,['PU02','PU03','PU04','PU05'],['C3','C5','C6'],'Interview context and institutional scope',['PE07','PE10','PE13','PE14'],'Retained claims contextualize review, release work, relay discretion, and enforcement consistency.','All six podcast statement units remain text_only. These accounts add no new event, role appointment, compliance finding, or network mandate.')
save('institution_action_links.json',links)

# Replay only the selected main-branch changes; no transition predicts acceptance.
full=api('pull_32406_files.json');files={f['filename']:f for f in full}
assert files['src/init.cpp']['patch']==G['X32406']['text']
patches={32406:G['X32406']['text'],33224:G['X33224']['text'],33453:G['X33453']['text']}
save('policy_patch_sources.json',{'source_id':'F32406_files','url':'https://github.com/bitcoin/bitcoin/pull/32406/files','head_sha':next(x for x in refreshed if x['pr']==32406)['head_sha'],'files':[{'filename':n,'patch':files[n]['patch']} for n in ['doc/release-notes-32406.md','src/policy/policy.h','src/policy/policy.cpp','src/init.cpp']],'scope':'Four relevant changed-file patches from the retrieved 26-file list. No whole-program behavior test.'})
def changed_lines(patch,sign):return [l[1:] for l in patch.splitlines() if l.startswith(sign) and not l.startswith(sign*3)]
def warning(lines):
 line=next((l for l in lines if 'InitWarning' in l and "Options '-datacarrier'" in l),None)
 if line is None:return None
 return 'expected_removal' if 'expected to be removed' in line else 'will_be_removed'
state={'default_policy':'earlier_83_byte_limit','output_budget':'single_output','options_available':True,'deprecated':False,'startup_warning':None}
initial=copy.deepcopy(state);timeline=[]
for event in events:
 if event['scope']!='focal_case':continue
 before=copy.deepcopy(state);pr=event['pr']
 if event['action']=='merge':
  patch=patches[pr];added=changed_lines(patch,'+');removed=changed_lines(patch,'-')
  if any('(DEPRECATED)' in l for l in added):state['deprecated']=True
  elif any('(DEPRECATED)' in l for l in removed):state['deprecated']=False
  if any('InitWarning' in l and "Options '-datacarrier'" in l for l in added+removed):
   assert warning(removed)==state['startup_warning'],pr
   state['startup_warning']=warning(added)
  if pr==32406:
   assert '-static const unsigned int MAX_OP_RETURN_RELAY = 83;' in files['src/policy/policy.h']['patch']
   assert '100,000' in files['doc/release-notes-32406.md']['patch']
   assert '+    unsigned int datacarrier_bytes_left' in files['src/policy/policy.cpp']['patch']
   state['default_policy']='higher_default_100000_transaction_ceiling';state['output_budget']='aggregate_across_multiple_outputs'
 timeline.append({'event_id':event['event_id'],'case_id':event['case_id'],'date_time':event['date_time'],'action':event['action'],'actor':event['actor'],'before':before,'after':copy.deepcopy(state),'changed_fields':[k for k in state if before[k]!=state[k]],'evidence':[f'F{pr}']+([f'X{pr}'] if event['action']=='merge' else [])})
save('state_replay.json',{'scope':'A projection of selected main-branch changes, not a full repository history, an adoption model, or a model of Bitcoin consensus rules. The old lines in C3 establish the tracked starting fields. Unmerged proposals do not apply their proposed changes.','initial_state':initial,'events':timeline,'final_state':state,'supporting_backport':next(e for e in events if e['scope']=='supporting_backport'),'unobserved_outcomes':['publication','operator_adoption','network_acceptance','restored_confidence']})

comparisons=[
 {'id':'CT1','cases':['C1','C2','C3'],'explanation_tested':'Smaller scope is sufficient for acceptance','observed_contrast':'C2 offered a smaller step and closed; C3 integrated a larger package with a different technical design and retained configuration.','assessment':'Contradicted as a sufficient explanation; scope reduction remains one possible contributor.','sources':['E01','E02','E03','E04','E07','E09','F32381','F32406']},
 {'id':'CT2','cases':['C1','C2','C4'],'explanation_tested':'Every nonintegration records a maintainer veto','observed_contrast':'glozow closes C1; darosior and achow101 close their own C2 and C4 proposals.','assessment':'Contradicted as a single action category. Author withdrawal may respond to review without constituting a reviewer’s formal veto.','sources':['F32359','F32381','F32714','E01','E04','E14']},
 {'id':'CT3','cases':['C3','C6'],'explanation_tested':'Integration requires convergence on all underlying preferences','observed_contrast':'C3 defers removal disagreement; C6 leaves opposed preferences and wider reversal demands intact.','assessment':'Inconsistent with the observed coexistence of integration and expressed disagreement.','sources':['E09','E10','E19','R10E17','R10E18','F32406','F33453']},
 {'id':'CT4','cases':['C4','C6'],'explanation_tested':'September simply adopted the identical rejected June proposal','observed_contrast':'The commits differ; recurring reasons accompany revised technical judgments and a different release context.','assessment':'Contradicted by identified content and timing. The normative proposition can persist without identity of the proposal.','sources':['KJ','KS','R10E09','R10E10','R10E11','R10E13','R10E14','R10E19']},
 {'id':'CT5','cases':['C5','C6'],'explanation_tested':'Support for wording automatically determines release execution','observed_contrast':'C5 includes translation constraints; C6 separates main integration and 30.x backport and contains conflicting views about release delay.','assessment':'The record requires a separate release decision. It does not identify every implementation step or publication.','sources':['E15','E17','E24','E25','E27','E28','F33453','F33473']},
 {'id':'CT6','cases':['C3','C6'],'explanation_tested':'Retained local options establish effective network influence or restored confidence','observed_contrast':'Options remain while participants disagree about defaults and legitimacy; the bounded operator search identifies no focal effect.','assessment':'Not established. The model preserves downstream outcomes as unknown.','sources':['N903','N907','R10E18','W01','W02','W03']}
]
save('comparison_tests.json',comparisons)
claims=[
 {'id':'K11_1','claim':'The six episodes show differentiated control over proposal form, integration, moderation, and release targeting.','sources':['E23','E24','E25','E30','E31','E32','W04','F32406','F33453','F33473'],'standing':'supported within the selected dispute','boundary':'No overall decentralization score or network mandate.'},
 {'id':'K11_2','claim':'Nonintegration comprises different acts, including closure by another participant and author closure.','sources':['F32359','F32381','F32714'],'standing':'direct platform-event comparison','boundary':'Review may influence withdrawal; formal reviewer veto is not inferred.'},
 {'id':'K11_3','claim':'The integrated sequence changes policy, then warning strength, then deprecation while preserving configuration.','sources':['F32406_files','X32406','X33224','X33453','F32406','F33224','F33453'],'standing':'bounded reproducible state reconstruction','boundary':'Selected main-branch fields only; not a behavioral or adoption simulation.'},
 {'id':'K11_4','claim':'A common institutional proposition can connect proposals with different contents and outcomes.','sources':['E12','E18','KJ','KS','F32714','F33453'],'standing':'supported linkage with inherited local recognition','boundary':'No isolated causal effect of the warning principle.'},
 {'id':'K11_5','claim':'Grammar units become explanatory through explicit links to actors, decision objects, responses, and disposition events.','sources':['IL02','IL03','IL04','IL06','IL07','IL08','IL10'],'standing':'methodological construction demonstrated in this comparison','boundary':'The overlay is not new IG2 coding or independent validation.'},
 {'id':'K11_6','claim':'The governance problem includes disagreement about who may judge reasons and which constituency should matter.','sources':['N15','N16','PE16','PE22','E32','E37','E38'],'standing':'supported comparison of contested claims','boundary':'No operational community approval procedure or finding that a technical argument is true.'}
]
save('claim_ledger.json',claims)

# Retain all inherited exact anchors, and the source/grammar records needed by the overlay.
unit_ids=sorted({u for row in rows for u in row['unit_ids']}|{u for x in links for u in x['unit_ids']})
units=[copy.deepcopy((U if u in U else PU)[u]) for u in unit_ids]
save('inherited_units_used.json',units)
save('evidence_anchors_inherited.json',list(E.values()))
source_ids={x['source_id'] for x in E.values()}|{u['source_id'] for u in units if u['source_id'] in G}
def collect_sources(node):
 if isinstance(node,list):
  for x in node:yield from collect_sources(x)
 elif isinstance(node,dict):
  for k,v in node.items():
   if k=='source_id' and isinstance(v,str):yield v
   else:yield from collect_sources(v)
source_ids|={s for s in collect_sources(units) if s in G}
for sid in ['32359-body','32381-body','32406-body','M32359','M32381','M32406','M32714','M33224','M33453','M33473','X32406','X33224','X33453','32359-115','32406-169']:source_ids.add(sid)
save('github_sources_used.json',[G[k] for k in sorted(source_ids)])
save('podcast_passages_used.json',[P[s] for s in sorted({u['source_id'] for u in units if u['source_id'] in P})])
save('web_cards_inherited.json',load(B10/'analysis/web_source_cards.json'))
save('proposal_commits_inherited.json',load(B10/'analysis/proposal_commits.json'))
save('provenance.json',{'round':11,'version':'0.1','user_facing_date':'2026-11-06','user_timezone':'America/Vancouver','input_file':'Core_Knots_Round10_Decision_Evidence_Package_v01.zip','input_sha256':'a9b7c248350cfdc25d333fdad1592597bad2650687a5b0ceba86ac6a1bc557f5','input_library_file_id':'libfile_fde3_f-09f7e72800bc8191986ad2353f4b04cf_88c23e15eda48191b8db6b4f3889fb68','input_library_version':0,'focal_cases':6,'supporting_backport_events':1,'new_github_reads':11,'refreshed_pull_records':7,'closure_actor_lookups':3,'policy_patch_lookup':1,'new_ig2_statements':0,'inherited_units_used':len(units),'inherited_exact_anchors':len(E),'github_records_used':len(source_ids),'institution_action_links':len(links),'independent_validation':False,'podcast_corpus_unchanged':{'recordings':7,'passages':27,'statement_units':6,'context_units':21},'interpretive_status':'Internal comparative process model. Historical coding unchanged. Deterministic replay describes recorded changes; it does not predict decisions.','exclusions':'P5158 and PE25–PE27 remain outside active evidence; PU03 retains only the clear release-role clause. No recovery task or 2026 fork outcome.'})
print(json.dumps(load(A/'provenance.json'),indent=2))
