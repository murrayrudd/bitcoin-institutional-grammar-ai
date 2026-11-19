import json, hashlib, platform, sys
from pathlib import Path
from copy import deepcopy
from collections import Counter

p=json.loads(Path('packet.json').read_text())
a=json.loads(Path('annotation.json').read_text())
first=json.loads(Path('annotation.first_complete.json').read_text())
checks_first=json.loads(Path('checks.first.json').read_text())
E={e['source_id']:e for e in p['entries']}
U={u['unit_id']:u for u in a['units']}
OBJ='https://github.com/bitcoin/bitcoin/pull/14441'

def ev(k,q=None):
 if not k.startswith('pr14441:'): k='pr14441:'+k
 t=E[k]['text'];q=t if q is None else q;s=t.index(q)
 assert q and t[s:s+len(q)]==q
 return {'source_id':k,'span':{'start':s,'end':s+len(q),'quote':q}}

def uniq(es):
 out=[];seen=set()
 for e in es:
  k=(e['source_id'],e['span']['start'],e['span']['end'])
  if k not in seen:out.append(e);seen.add(k)
 return out

repairs=[]
def change(path,value,reason,evidence,effect,meaning=False):
 node=a
 for key in path[:-1]: node=node[key]
 old=deepcopy(node[path[-1]])
 if old==value:return
 node[path[-1]]=deepcopy(value)
 repairs.append({'change_id':f'R{len(repairs)+1:02d}','stage':'single complete source-based self-review','path':path,'before':old,'after':value,'reason':reason,'evidence':evidence,'diagnosis':'execution_failure_under_existing_rule' if meaning else 'defensible_alternative_representation','effect':effect,'meaning_changes':meaning})

# Narrow the disposition to avoid treating an integrated, partly matching paragraph as verbatim acceptance of every qualification.
s4=U['F02-S04'];idx4=a['units'].index(s4)
change(['units',idx4,'proposition','summary'],
 'ryanofsky recommends documenting the empty-string change in the release notes, tentatively offering wording that describes empty-string label queries for unlabeled transactions as possible with `-deprecatedrpc=accounts` and describes an error without it, with backward compatibility and usefulness/confusion explanations.',
 'Replace potentially permission-sounding summary wording with the source\'s technical capability meaning; the existing force and alternative already excluded institutional permission.',[ev('review_comments:3')],'convention_deviation')

paragraph=ev('patch:0',E['pr14441:patch:0']['text'][E['pr14441:patch:0']['text'].index('+When `-deprecatedrpc'):E['pr14441:patch:0']['text'].index('\n \n Credits')])
comparison=[ev('review_comments:3'),paragraph]
change(['units',idx4,'disposition_events',1,'target'],'broader_proposal',
 'The proposed explicit backward-compatibility rationale is not in the retained paragraph. The merged status should therefore not encode adoption of the entire qualified wording proposition.',comparison,'evidence_basis_error',True)
change(['units',idx4,'disposition_events',1,'rationale'],
 'PR #14441 and the retained head are recorded merged. The patch contains the requested empty-string behavior documentation and usefulness/confusion explanation, but omits the offered explicit backward-compatibility phrase. The merge disposition is therefore scoped to the broader contribution; adoption of every proposed qualification is not established.',
 'Make the rationale agree with the narrowed disposition target and distinguish observed documentation from adoption of the complete suggested formulation.',comparison,'evidence_basis_error',True)
change(['units',idx4,'institution','application_evidence',1,'rationale'],
 'The retained, integrated paragraph demonstrates the focal action of documenting the empty-string change: both setting-dependent behaviors and the usefulness/confusion rationale are present. The offered wording was tentative (Maybe), and this observed-action classification does not claim verbatim implementation, adoption of the omitted explicit backward-compatibility rationale, or institutional recognition of that rationale. The separate unresolved record preserves the limit on the complete wording.',
 'State exactly which focal action is observed rather than compressing partial wording correspondence into an unqualified implementation claim.',comparison,'evidence_basis_error',False)
newapps=deepcopy(s4['institution']['application_evidence'])
newapps.append({'status':'unresolved','target':'this_proposition','evidence':comparison,
 'rationale':'The proposed paragraph explicitly invokes backward compatibility; the retained paragraph does not state that phrase. It is unresolved whether contributors adopted that rationale implicitly or intentionally omitted it. This record concerns the full suggested formulation, while the separately observed application concerns the document-the-change action. No exact implementation of every qualifier is asserted.'})
change(['units',idx4,'institution','application_evidence'],newapps,
 'Keep the uncertainty about the omitted qualification explicit in the application records, rather than relying only on prose surrounding an observed profile.',comparison,'evidence_basis_error',False)

# Tighten the infinitive governing clause without changing any role assignment.
for ci in [0,1,2]:
 change(['units',idx4,'components',ci,'governing_span'],ev('review_comments:3','to document the empty string change'),
  'The focal predicate is the documentation infinitive. Tightening its governing clause makes the distinction from the matrix I think visible.',[ev('review_comments:3','to document the empty string change')],'convention_deviation')

c6=U['F02-C06'];idx6=a['units'].index(c6)
change(['units',idx6,'speech_act'],'asserted',
 'Both are good changes is a declarative positive evaluation, rather than an explicit ACK token or a report of an edit. It remains ordinary assent context.',[ev('review_comments:4')],'convention_deviation')

# Make the abbreviated-SHA inference visible in the exact clause ledger.
o=a['episode_summary']['observed_outcomes'][2]
change(['episode_summary','observed_outcomes',2,'claim'],
 'ryanofsky recorded a later utACK for 89306ab0df93bfdf5630910bc20b1eccb7379172 and identified code simplification and release-note updates since the earlier review. promag recorded a utACK using its matching abbreviated SHA; meshcollider supplied the full revision and qualified the comparison with the original PR.',
 'The source supplies a short hash for promag. Preserve that evidence form rather than presenting the full-revision identity as directly stated by that actor.',[ev('comments:1'),ev('supplement_metadata','"head_sha": "89306ab0df93bfdf5630910bc20b1eccb7379172"')],'evidence_basis_error')
newpart={'text':'promag recorded utACK 89306ab, whose prefix matches the supplied full head SHA; full-revision identity is a bounded contextual inference.','evidence':[ev('comments:1'),ev('supplement_metadata','"head_sha": "89306ab0df93bfdf5630910bc20b1eccb7379172"')]}
change(['episode_summary','observed_outcomes',2,'claim_parts',1],newpart,
 'Attach the supplied full head hash to the short-hash correspondence claim.',newpart['evidence'],'evidence_basis_error')
new_evidence=uniq([e for part in o['claim_parts'] for e in part['evidence']])
change(['episode_summary','observed_outcomes',2,'evidence'],new_evidence,
 'The parent outcome evidence must include every anchor used by the revised claim part.',newpart['evidence'],'convention_deviation')

Path('annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
Path('annotation.final.json').write_bytes(Path('annotation.json').read_bytes())
Path('repair_log.json').write_text(json.dumps({'run_id':'F02_v04_r3','mechanical_repairs':[],'source_review_rounds':1,'changes':repairs,'change_count':len(repairs),'meaning_changing_changes':sum(x['meaning_changes'] for x in repairs),'note':'First-complete structural checks passed. Repairs arise only from the single complete source review; the first-complete output is preserved.'},ensure_ascii=False,indent=2)+'\n')

# A per-occurrence explanation is prepared for every first-check flag. Final flags are linked after the final checker run.
predicate_notes={
 'F02-S01':[
  'Retained contextual A. The source does not name an editor; the later jnewbery update report supports that inferred executor, not an explicit local role or authority.',
  'Retained explicit lexical D Should, with advisory recommendation force under the pragmatic correction reading; no rule authority inferred.',
  'Retained inferred I correct. The surface predicate is be, so the corrective action is visibly marked semantic inference.',
  'Retained inferred Bdir. The desired RPC string is a complement of be, not a literal object of correct; the role is semantic inference and the erroneous original is unavailable.',
  'Retained inferred Cex. The supplied complete name plus with s constrains the reconstructed resulting spelling, without splitting the identifier.'
 ],
 'F02-S02':[
  'Retained local A I under the explicit I would change predicate. The hypothetical proposer is ryanofsky; it is not the I from an unrelated predicate and does not assert an actual implementation.',
  'Retained local I change, explicitly supplied by the proposed edit clause; recommendation force does not make the lexical action inferred.',
  'Retained local explicit Bdir it. Its grammatical role is explicit under change, while its paragraph referent is resolved by the attached preceding-sentence scope note.',
  'Retained Cex proposed replacement. Change it to directly introduces the output wording; both configuration branches and their explanation stay in the same edit proposition.'
 ],
 'F02-S03':[
  'Retained contextual A from the matching later removal report; the imperative does not explicitly name an actor.',
  'Retained explicit local I drop. The prefatory Maybe softens force, while the action remains directly supplied.',
  'Retained inferred Bdir from the preceding technical premise. The new star check is not a local object occurrence under drop and is correctly marked context_reference.',
  'Retained explicit Cex for clarity. It is an action purpose, not a fabricated condition about seeking clarity.'
 ],
 'F02-S04':[
  'Retained contextual A; the source I is the subject of think and cannot be imported as a local actor of document. The governing span was tightened to the infinitive.',
  'Retained explicit I document, now governed by the precise infinitive clause rather than the larger matrix sentence.',
  'Retained explicit Bdir the empty string change under document; the governing span was tightened while its object role remained unchanged.',
  'Retained inferred Cex for the block following Maybe. The adjacent wording specifies the documentation content but is not syntactically introduced by to as in S02. All technical qualifiers remain recoverable.'
 ]}
qual_notes={
 'F02-S01':'The complete RPC name and explicit final s remain in Cex and the qualifier. Actor, corrective predicate, and target-role inferences are disclosed. There is no separate material condition to invent.',
 'F02-S02':'The hypothetical first person, Maybe, same-release rationale, paragraph antecedent, accounts setting and absence, all argument names, transaction directions, and accounts-versus-labels explanation are retained. The technical block does not add another institutional statement.',
 'F02-S03':'Maybe, unless I am missing something, new star-check identity, uncertainty about behavior, and clarity purpose remain explicit. The defeasibility clause can alternatively be Cac; its meaning survives as a scope note.',
 'F02-S04':'The documentation request, tentative proposed wording, backward-compatibility rationale, empty-string value, unlabeled target, both setting branches, and usefulness/confusion explanation remain attached. Technical capability wording was clarified in the summary; the omitted final-patch rationale is preserved as an outcome limit.'}

app_notes={
 'F02-S01':[
  ('retained','The named-reviewer update report and later description of release-note changes support only the broader PR update; no unique local target is claimed.'),
  ('retained','The requested complete identifier is visible in an added release-note heading, and the supplied head and merge SHA match. This supports the requested resulting spelling at integration, not the omitted original typo or review causation.'),
  ('unresolved','The one-word fixed report supplies no unique antecedent. It remains unresolved and does not raise the focal profile.' )],
 'F02-S02':[
  ('retained','The general update report stays at broader-proposal scope.'),
  ('retained','The retained paragraph preserves the two setting-dependent transaction directions and the accounts-versus-labels explanation. The integrated head is identified; formatting differences do not change this edit meaning.')],
 'F02-S03':[
  ('retained','The general update report stays at broader-proposal scope.'),
  ('retained','The matching star-check wording plus I have removed it supports reported application to this suggestion. The record does not claim direct patch verification.'),
  ('unresolved','The final condition is visible but the earlier new check is unavailable. The precise removal remains unresolved as an artifact claim, despite the attributable report.')],
 'F02-S04':[
  ('retained','The general update report stays at broader-proposal scope.'),
  ('corrected','The observed application is explicitly limited to documenting the setting-dependent change. It does not certify the full suggested wording or adoption of backward compatibility as a rationale; a separate unresolved record and broader merge disposition preserve that limit.'),
  ('unresolved','The final paragraph omits the explicit backward-compatibility phrase. Whether its rationale was adopted implicitly or intentionally omitted cannot be resolved from this packet.')]
}

summary_notes=[
 ('retained','All material clauses are attributable participant reports: author update, agreement on behavior, and reported removal. The claim does not represent these as observed intermediate patch changes.'),
 ('retained','The suggestion-to-patch comparisons directly support the complete name, both technical descriptions, and the explicit omission of the backward-compatibility phrase. No inferred network behavior or adoption of a general rationale is added.'),
 ('corrected','The full and abbreviated ACK targets, reviewer update statement, and technical backport qualification are preserved. The short-hash/full-head correspondence is now explicitly identified as inference with its exact supporting head anchor.'),
 ('retained','The canonical URL, merged true, merge time, head SHA, and merge-commit SHA establish only the identified PR\'s recorded integration.'),
 ('retained','The same check-for-star wording and response support a reason-giving sequence and reported removal. The missing earlier diff and independent-conclusion alternative block causal attribution.'),
 ('retained','The explicit since-last-review language, distinct hashes, and author update report support coordination. Packet submission timestamps order the acts at 05:54:07, 07:40:49, and 07:57:22 UTC on 2018-10-10. No reapproval rule or cause of merge is asserted.')]

first_reviews=[];pc=Counter();ac=Counter();sc=0
fu={u['unit_id']:u for u in first['units']}
for i,f in enumerate(checks_first['review_flags']):
 uid=f['unit_id'];code=f['code'];u=U.get(uid);old=fu.get(uid);status='retained';pointer=None
 if code=='qualifier_audit':
  rationale=qual_notes[uid];evidence=uniq([e for q in u['proposition']['qualifiers'] for e in q['evidence']]);pointer=f'/units/{a["units"].index(u)}/proposition/qualifiers'
  if uid=='F02-S04':status='corrected'
 elif code=='predicate_audit':
  j=pc[uid];pc[uid]+=1;c=u['components'][j]
  rationale=predicate_notes[uid][j];evidence=uniq(c['evidence']+[c['governing_span']]);pointer=f'/units/{a["units"].index(u)}/components/{j}'
  if uid=='F02-S04' and j<3:status='corrected'
 elif code=='application_audit':
  j=ac[uid];ac[uid]+=1;event=u['institution']['application_evidence'][j]
  status,rationale=app_notes[uid][j];evidence=event['evidence'];pointer=f'/units/{a["units"].index(u)}/institution/application_evidence/{j}'
 elif code=='summary_audit':
  status,rationale=summary_notes[sc]
  group='observed_outcomes' if sc<4 else 'mechanisms';n=sc if sc<4 else sc-4
  event=a['episode_summary'][group][n];evidence=event['evidence'];pointer=f'/episode_summary/{group}/{n}';sc+=1
 else:raise RuntimeError('Unreviewed flag '+code)
 first_reviews.append({'check_file':'checks.first.json','flag_index_zero_based':i,'flag':f,'target_pointer':pointer,'status':status,'rationale':rationale,'evidence':evidence})

screen_audit=[]
for s in a['entry_screening']:
 e=E[s['source_id']]
 screen_audit.append({'source_id':s['source_id'],'scope':'exhaustive_focal' if s['source_id'] in p['selection_design']['focal_source_ids'] else 'supplemental_context_screening','status':'retained','finding':s['reason'],'evidence':[ev(s['source_id'])] if e['text'] else [],'empty_body_verified':not bool(e['text'])})

review={'run_id':'F02_v04_r3','source_review_rounds':1,'review_scope':'One complete source-based self-review after first-complete freeze and first checker result. Truncated display portions were recovered within this same review; no additional research source was introduced.',
 'first_complete_preserved':True,'checker_interpretation':'A mechanical pass verifies declared structure and offsets only; it does not certify interpretation.',
 'screening_omission_audit':screen_audit,
 'manual_cross_checks':[
  {'area':'authority_and_type','status':'retained','finding':'All four independently executable review suggestions remain institutionally undetermined. None supplies attributed authorization or enforcement, a recurring expectation, a committed personal strategy, or an institutional configuration. The absence of those records in this packet is not evidence that no such arrangements exist elsewhere.','evidence':[ev('review_comments:'+str(i)) for i in range(4)]},
  {'area':'recognition','status':'retained','finding':'Ordinary assent and edit reports do not name an expectation or governing status as a standard. The different-actor technical agreement is not expectation recognition. The ACKs have revision targets and do not show a general rule or repeated independent recognition. Same-episode repetitions are not treated as independent evidence.','evidence':[ev('review_comments:4'),ev('review_comments:6'),ev('reviews:0'),ev('reviews:4'),ev('comments:1'),ev('comments:2')]},
  {'area':'dispositions_and_object_identity','status':'corrected','finding':'Every disposition identifies the same canonical PR using supplied metadata. S01 and S02 have particular final artifact correspondence plus integrated-head evidence. S03 merge remains broader because the intermediate removed check is unavailable. S04 merge was narrowed to broader proposal because not all proposed qualifications are stated in the final paragraph. No referenced PR status or network adoption is inferred.','evidence':[ev('body'),ev('supplement_metadata'),ev('patch:0'),ev('review_comments:3'),ev('review_comments:6')]},
  {'area':'governance_levels','status':'retained','finding':'The four focal actions concern edits to this contribution. Visible suggestions, ACKs, and update reports are operational. No recurring review arrangement, allocation of decision powers, or foundation of legitimate authority is proposed in the supplied focal text. Context statement-target levels remain not applicable.','evidence':[ev('review_comments:'+str(i)) for i in range(4)]+[ev('reviews:4')]},
  {'area':'documentary_time_and_application','status':'retained','finding':'No patch is used as authoritative documentary guidance at the earlier suggestion date. The artifact evidence is application evidence tied to the recorded head and later integration. Retained submission times do not establish complete edit histories.','evidence':[ev('patch:0'),ev('supplement_metadata')]},
  {'area':'challenges_and_sanctions','status':'retained','finding':'Technical criticism of an earlier paragraph or redundant check is the rationale for the extracted recommendations, not an identified challenge to those recommendations. There is no attributed enforcement consequence or executed sanction; software errors in proposed help text remain technical behavior.','evidence':[ev('review_comments:1'),ev('review_comments:2'),ev('review_comments:3'),ev('review_comments:6')]},
  {'area':'relation_direction_and_mechanisms','status':'retained','finding':'Uptake points suggestions to author responses; general uptake remains context-inferred. Review-target update points later review to earlier review and is supported by since-last-review wording. Mechanisms retain alternatives and do not turn order into causation or impose reapproval.','evidence':[ev('comments:0'),ev('review_comments:2'),ev('review_comments:6'),ev('reviews:0'),ev('reviews:4')]},
  {'area':'presentation_and_speech_act','status':'corrected','finding':'The two newly offered replacement blocks remain proposed_wording with mixed presentation, not quotation records. Inline identifiers remain plain presentation. The declarative Both are good changes context is classified asserted; literal proposals and implementation reports retain their appropriate acts.','evidence':[ev('review_comments:1'),ev('review_comments:3'),ev('review_comments:4')]}
 ],
 'first_checker_flag_resolutions':first_reviews,'final_checker_flag_resolutions':[],
 'unresolved_limits':deepcopy(a['episode_summary']['missing_evidence'])+deepcopy(a['episode_summary']['unresolved_questions']),
 'repair_log':'repair_log.json','summary':{'entries_screened':22,'focal_entries_exhaustively_screened':16,'supplemental_entries_context_screened':6,'statement_units':4,'context_units':8,'relations':6,'observed_outcomes':4,'mechanisms':2,'first_flags_reviewed':len(first_reviews)}}
Path('review_notes.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_review_rounds':1,'repairs':len(repairs),'meaning_changing_repairs':sum(x['meaning_changes'] for x in repairs),'first_flags_reviewed':len(first_reviews),'final_path':str(Path('annotation.final.json').resolve())}))
