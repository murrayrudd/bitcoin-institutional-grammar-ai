"""Verify evidence lineage and model consistency, not independent scholarly validity."""
from pathlib import Path
from datetime import datetime
from xml.etree import ElementTree as ET
import hashlib, json, re, zipfile
R=Path(__file__).resolve().parent;A=R/'analysis'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def api(n):return json.loads(load(R/'sources'/n)['structuredContent']['content'])
def dt(s):return datetime.fromisoformat(s.replace('Z','+00:00'))
checks=[]
def check(name,ok,detail):
 checks.append({'check':name,'passed':bool(ok),'detail':detail})
 if not ok:raise AssertionError(name+': '+str(detail))
B10=R/'inputs/round10'
B9=R/'inputs/round9'
B5=R/'inputs/round5'
input_files=load(R/'inputs/file_hashes.json')
check('retained_input_file_integrity',all(sha(R/f['path'])==f['sha256'] for f in input_files),len(input_files))
G={x['source_id']:x for x in load(A/'github_sources_used.json')}
oldG={x['source_id']:x for x in load(B5/'baseline/sources/baseline_all_source_registry.json')}
check('inherited_github_records_identical',len(G)==76 and all(g==oldG[k] for k,g in G.items()),len(G))
U={x['unit_id']:x for x in load(A/'inherited_units_used.json')}
oldU={x['unit_id']:x for x in load(B5/'baseline/annotations/corrected_baseline.json')['units']}
oldPU={x['unit_id']:x for x in load(B9/'sources/podcast_annotations_inherited.json')['units']}
check('all_selected_units_identical',len(U)==46 and all(u==(oldU|oldPU)[k] for k,u in U.items()),len(U))
P={x['evidence_id']:x for x in load(A/'podcast_passages_used.json')}
oldP={x['evidence_id']:x for x in load(B9/'sources/podcast_passages.json')}
check('selected_podcast_passages_identical',all(p==oldP[k] for k,p in P.items()),len(P))
E={x['evidence_id']:x for x in load(A/'evidence_anchors_inherited.json')}
oldE={x['evidence_id']:x for path in [B9/'analysis/evidence_anchors.json',B10/'analysis/evidence_anchors.json'] for x in load(path)}
check('inherited_anchors_identical',len(E)==77 and E==oldE,len(E))
for eid,x in E.items():
 s=x['span'];g=G[x['source_id']]
 check('anchor_'+eid,g['text'][s['start']:s['end']]==s['quote'] and g.get('url')==x['url'],x['source_id'])
packet={x['source_id']:x for x in load(B9/'sources/podcast_annotation_packet_inherited.json')['entries']}
for uid,u in U.items():
 text=G[u['source_id']]['text'] if u['source_id'] in G else packet[u['source_id']]['text'];s=u['span']
 check('unit_span_'+uid,text[s['start']:s['end']]==s['quote'],u['source_id'])
check('full_podcast_corpus_counts',len(oldP)==27 and len(load(B9/'sources/podcast_registry.json'))==7 and len(oldPU)==27,{'passages':len(oldP),'units':len(oldPU)})
check('podcast_standing_unchanged',{u['unit_id'] for u in oldPU.values() if u['record_role']=='statement'}=={'PU02','PU03','PU04','PU05','PU06','PU07'} and all(U[f'PU{i:02d}']['institution']['standing']=='text_only' for i in range(2,8)),6)
check('pu01_retains_context',oldPU['PU01']['record_role']=='context','No new parse or standing.')
check('murch_scope_closed',U['PU03']['span']['quote']=='Their job is uh to facilitate releases','Only the accepted clear clause.')
check('excluded_interview_not_active',not {'PE25','PE26','PE27'}&set(oldP) and not {'PU08','PU09','PU10'}&set(U) and all(x['episode_id']!='P5158' for x in P.values()),'Historical copies remain inside frozen inputs only.')
check('inherited_web_cards_identical',load(A/'web_cards_inherited.json')==load(B10/'analysis/web_source_cards.json'),4)
check('inherited_proposal_commits_identical',load(A/'proposal_commits_inherited.json')==load(B10/'analysis/proposal_commits.json'),2)

F={x['source_id']:x for x in load(A/'disposition_sources.json')}
events=load(A/'disposition_events.json');V={x['event_id']:x for x in events}
C={x['case_id']:x for x in load(A/'case_comparison.json')}
oldC={x['case_id']:x for x in load(B9/'analysis/decision_reconstruction.json')}
check('six_focal_cases',set(C)==set(oldC) and all(C[k]['pr']==oldC[k]['pr'] for k in C),sorted(C))
check('seven_dispositions_six_focal',len(V)==len(events)==7 and sum(e['scope']=='focal_case' for e in events)==6,7)
for e in events:
 pr=e['pr'];f=F[f'F{pr}'];raw=api(f'pull_{pr}.json');old=json.loads(G[f'M{pr}']['text'])
 check('frozen_dates_and_head_'+str(pr),all(raw[k]==old[k] for k in ['created_at','closed_at','merged_at','merged']) and raw['head']['sha']==old['head_sha'],e['date_time'])
 check('event_'+str(pr),e['date_time']==(raw['merged_at'] or raw['closed_at']) and e['author']==raw['user']['login'] and e['target_branch']==raw['base']['ref'] and e['action']==('merge' if raw['merged'] else 'close_unmerged'),e['action'])
 actor=raw['merged_by']['login'] if raw['merged'] else api(f'issue_{pr}.json')['closed_by']['login']
 check('actor_'+str(pr),e['actor']==actor==f['disposition_actor'] and e['actor_is_author']==(actor==raw['user']['login']),actor)
 check('actual_merge_sha_'+str(pr),e['actual_merge_sha']==(raw['merge_commit_sha'] if raw['merged'] else None),e['actual_merge_sha'])
 if not raw['merged']:
  issue=api(f'issue_{pr}.json')
  check('closure_source_'+str(pr),issue['closed_at']==raw['closed_at'] and issue['number']==pr and e['actual_merge_sha'] is None,{'raw_prospective_merge_hash':raw['merge_commit_sha'],'recorded_actual_merge':e['actual_merge_sha']})
 check('no_downstream_outcome_'+str(pr),e['publication_observed'] is None and e['adoption_observed'] is None,'Unknown outcomes stay unknown.')
 if e['case_id'] in C:
  c=C[e['case_id']]
  check('case_dates_'+e['case_id'],c['opened_at']==raw['created_at'] and c['disposed_at']==e['date_time'] and c['outcome']==e['action'] and c['disposition_event']==e['event_id'],c['disposed_at'])
check('chronological_event_order',all(dt(a['date_time'])<dt(b['date_time']) for a,b in zip(events,events[1:])),[e['case_id'] for e in events])
check('overlapping_proposals',dt(C['C2']['disposed_at'])<dt(C['C1']['disposed_at']) and dt(C['C3']['opened_at'])<dt(C['C1']['disposed_at']),'Case labels are not event order.')
check('two_author_closures',{e['case_id'] for e in events if e['action']=='close_unmerged' and e['actor_is_author']}=={'C2','C4'},['C2','C4'])
check('actor_roles_vary',V['C4_disposition']['actor']==V['C5_disposition']['actor']==V['C6_disposition']['actor']=='achow101' and V['C4_disposition']['action']!=V['C5_disposition']['action'],'Author closure followed by later merge acts.')

patch=load(A/'policy_patch_sources.json');raw_files=api('pull_32406_files.json');files={x['filename']:x for x in raw_files}
check('selected_patch_text_identical',len(raw_files)==26 and len(patch['files'])==4 and all(p['patch']==files[p['filename']]['patch'] for p in patch['files']),{'retrieved_files':len(raw_files),'retained_patches':len(patch['files'])})
check('c3_init_matches_frozen',files['src/init.cpp']['patch']==G['X32406']['text'],sha(R/'sources/pull_32406_files.json'))
check('initial_single_output_evidenced','-    // only one OP_RETURN txout is permitted' in files['src/policy/policy.cpp']['patch'],'Removed one-output restriction.')
check('budget_change_evidenced','-static const unsigned int MAX_OP_RETURN_RELAY = 83;' in files['src/policy/policy.h']['patch'] and '100,000' in files['doc/release-notes-32406.md']['patch'] and '+    unsigned int datacarrier_bytes_left' in files['src/policy/policy.cpp']['patch'],'Earlier setting, higher default, and aggregate allocation.')
model=load(A/'state_replay.json');states={x['case_id']:x for x in model['events']}
check('only_main_cases_replayed',set(states)==set(C) and model['supporting_backport']==V['C6B_disposition'] and V['C6B_disposition']['target_branch']=='30.x',list(states))
previous=model['initial_state']
for t in model['events']:
 check('state_continuity_'+t['case_id'],t['before']==previous and t['changed_fields']==[k for k in t['after'] if t['after'][k]!=t['before'][k]],t['changed_fields'])
 e=V[t['event_id']]
 check('replay_event_'+t['case_id'],t['date_time']==e['date_time'] and t['action']==e['action'] and t['actor']==e['actor'],e['event_id'])
 if e['action']=='close_unmerged':check('unmerged_state_unchanged_'+t['case_id'],t['after']==t['before'] and not t['changed_fields'],'Proposed changes not applied.')
 previous=t['after']
check('warning_sequence',[states[k]['after']['startup_warning'] for k in ['C3','C4','C5','C6']]==['will_be_removed','will_be_removed','expected_removal',None], 'C4 leaves the earlier warning intact.')
check('c5_only_warning_changes',states['C5']['changed_fields']==['startup_warning'],'Deprecation and policy retained.')
check('c6_only_deprecation_and_warning_change',set(states['C6']['changed_fields'])=={'deprecated','startup_warning'},'Higher default and configuration remain.')
check('options_persist',all(s['after']['options_available'] for s in model['events']),'No selected merge removes configuration.')
check('final_state_matches_last_merge',model['final_state']==previous and model['final_state']['default_policy']=='higher_default_100000_transaction_ceiling' and model['final_state']['deprecated'] is False,'No policy reversal inferred.')
check('downstream_model_scope',set(model['unobserved_outcomes'])=={'publication','operator_adoption','network_acceptance','restored_confidence'},model['unobserved_outcomes'])

IL={x['link_id']:x for x in load(A/'institution_action_links.json')}
W={x['source_id']:x for x in load(A/'web_cards_inherited.json')}
K={x['source_id']:x for x in load(A/'proposal_commits_inherited.json')}
allowed=set(G)|set(U)|set(P)|set(E)|set(F)|set(V)|set(C)|set(IL)|set(W)|set(K)|{'F32406_files'}
check('twelve_links_no_standing_upgrade',len(IL)==12 and all(x['standing_changed'] is False and set(x['unit_ids'])<=set(U) and set(x['case_ids'])<=set(C) for x in IL.values()),len(IL))
def references(node):
 if isinstance(node,list):
  for x in node:yield from references(x)
 elif isinstance(node,dict):
  for k,v in node.items():
   if k in ('references','sources','evidence','unit_ids','case_ids') and isinstance(v,list):
    for value in v:
     if isinstance(value,str):yield value
     else:yield from references(value)
   elif k=='disposition_event':yield v
   else:yield from references(v)
for n in ['case_comparison.json','institution_action_links.json','disposition_events.json','state_replay.json','comparison_tests.json','claim_ledger.json']:
 refs=set(references(load(A/n)));check('references_'+n,refs<=allowed,sorted(refs-allowed))
check('later_interview_not_premerge',P['PE22']['date']>C['C3']['disposed_at'][:10] and 'later interview' in IL['IL10']['boundary'],'The link expressly separates later interpretation from earlier causation.')
check('documentary_snapshot_scope',G['D_CONTRIB']['timestamp']=='2025-06-09' and F['F32406']['actual_merge_sha'] in G['D_CONTRIB']['url'] and G['D_MOD']['timestamp']=='2024-08-14','Pinned documents retain their temporal scope.')

report=R/'report/Core_Knots_Round11_Comparative_Institutional_Model_v01.docx'
with zipfile.ZipFile(report) as z:
 root=ET.fromstring(z.read('word/document.xml'));prose=' '.join(t.text or '' for t in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
 rels=ET.fromstring(z.read('word/_rels/document.xml.rels'))
citations=set()
for bracket in re.findall(r'\[([^\]]+)\]',prose):
 for token in re.split(r'[,;]\s*',bracket):
  m=re.fullmatch(r'(R10E|N9|PE|PU|IL|D|U|E)(\d{2})[–-](\d{2})',token)
  if m:citations|={m[1]+f'{i:02d}' for i in range(int(m[2]),int(m[3])+1)}
  else:citations.add(token)
check('report_citations_resolve',citations<=allowed,{'count':len(citations),'unresolved':sorted(citations-allowed)})
urls={x.get('Target') for x in rels if x.get('Type','').endswith('/hyperlink')}
known={x.get('url') for d in [G,F,E,W,K] for x in d.values()};known|={u.split('#')[0] for u in known if u}
check('report_links_resolve',urls<=known,sorted(urls-known))
check('internal_review_standing_explicit','internal analysis rather than independent validation' in prose and 'adds no IG2 statement' in prose,'No external validation claim.')
check('excluded_passages_not_cited',not {'PE25','PE26','PE27'}&citations,'Historical exclusions remain inactive.')
pr=load(A/'provenance.json')
check('provenance_counts',pr['new_github_reads']==len(list((R/'sources').glob('*.json')))==11 and pr['inherited_units_used']==len(U) and pr['inherited_exact_anchors']==len(E) and pr['github_records_used']==len(G) and pr['institution_action_links']==len(IL),'Counts match supplied records.')
result={'round':11,'status':'passed','check_count':len(checks),'checks':checks,'report_sha256':sha(report),'scope':'Mechanical provenance, exact-span, chronology, citation, and state consistency checks. Internal source interpretation and grammatical standing are not independently validated by these checks.'}
(A/'verification_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
