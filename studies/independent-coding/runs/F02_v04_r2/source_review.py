import json,copy,hashlib,sys,platform
from pathlib import Path
B=Path(__file__).resolve().parent
p=json.loads((B/'packet.json').read_text()); entries={x['source_id']:x for x in p['entries']}
a=json.loads((B/'annotation.json').read_text()); first=copy.deepcopy(a)
U={u['unit_id']:u for u in a['units']}
checks=json.loads((B/'checks.first.json').read_text())

def ev(s,q=None):
 if not s.startswith('pr14441:'):s='pr14441:'+s
 t=entries[s]['text'];q=t if q is None else q;i=t.index(q)
 return {'source_id':s,'span':{'start':i,'end':i+len(q),'quote':q}}
def unique(es):
 out=[]
 for e in es:
  if e not in out:out.append(e)
 return out
repairs=[]
def log(change_id,paths,description,evidence,effect='evidence_basis_error',meaning=False,diagnosis='execution_failure'):
 repairs.append({'change_id':change_id,'phase':'one_source_self_review','paths':paths,'description':description,'evidence':evidence,'diagnosis':diagnosis,'effect':effect,'meaning_changed':meaning,'institutional_conclusion_changed':False})

# Narrow governors to the clause that actually supplies the backport action and its arguments.
for c in U['S01']['components']:c['governing_span']=ev('body','Backport of PR #14411 to v0.17.')
log('R01',['S01.components[0:3].governing_span'],'Narrowed the three governors from the complete body to its first clause. The inference labels and backport meaning are unchanged.',[ev('body','Backport of PR #14411 to v0.17.')])

# Make attachment descriptions match the declared carrying structure.
component_q_paths=[]
for uid in ['S01','S02','S03','S05']:
 for i,q in enumerate(U[uid]['proposition']['qualifiers']):
  if q['attachment']=='component':
   q['rationale']='The named component preserves this qualification; this explicit qualifier record makes it visible to alignment and source review.'
   component_q_paths.append(f'{uid}.proposition.qualifiers[{i}].rationale')
log('R02',component_q_paths,'Replaced a generic scope-note rationale on component-attached qualifiers with an accurate component-attachment explanation.',[ev('body'),ev('review_comments:0'),ev('review_comments:1'),ev('review_comments:3')],effect='convention_deviation')

U['S03']['proposition']['qualifiers'].append({'description':'The conditional I\'d and maybe make the proposed replacement tentative; they do not commit the speaker to perform the edit.','evidence':[ev('review_comments:1',"I'd maybe change it to:")],'attachment':'scope_note','linked_unit_id':None,'rationale':'The source wording already appears in the focal unit and hypothetical-actor interpretation; this note explicitly carries its tentative force.'})
log('R03',['S03.proposition.qualifiers[3]'],'Added an explicit qualifier record for I\'d maybe, already retained in the source span and hypothetical-actor interpretation.',[ev('review_comments:1',"I'd maybe change it to:")],effect='convention_deviation')

q=U['S04']['proposition']['qualifiers'][0];q['attachment']='scope_note';q['rationale']='Cac carries the unless clause, while this scope note additionally preserves Maybe without inventing an explicit deontic modal.'
log('R04',['S04.proposition.qualifiers[0].attachment','S04.proposition.qualifiers[0].rationale'],'Made the hedge\'s attachment a scope note because the Cac component carries the unless clause but no component carries Maybe.',[ev('review_comments:2',"Maybe drop for clarity (unless I'm missing something).")],effect='convention_deviation')

U['S04']['institution']['recognition'][0]['evidence']=[ev('review_comments:6')]
log('R05',['S04.institution.recognition[0].evidence'],'Extended the assent anchor to include the check reference that supports the stated proposition target, rather than relying on uncited surrounding text.',[ev('review_comments:6')])

patch=entries['pr14441:patch:0']['text'];para1=ev('patch:0',patch[patch.index('+When bitcoin'):patch.index('+\n+When `-deprecatedrpc')]);para2=ev('patch:0',patch[patch.index('+When `-deprecatedrpc'):patch.index('\n \n Credits')])
out=a['episode_summary']['observed_outcomes'][1]
out['claim_parts'][3]['evidence']=[para1,para2]+out['claim_parts'][3]['evidence']
out['evidence']=unique([e for part in out['claim_parts'] for e in part['evidence']])
log('R06',['episode_summary.observed_outcomes[1].claim_parts[3].evidence'],'Added the patch-source anchors to the patch/head/merge correspondence part; the source entry\'s supplied revision metadata connects these anchors to the hash evidence.',[para1,para2,ev('supplement_metadata','"head_sha": "89306ab0df93bfdf5630910bc20b1eccb7379172"')])

mech=a['episode_summary']['mechanisms'][1]
mech['claim_parts'][4]['evidence']=[para1,para2]+mech['claim_parts'][4]['evidence']
log('R07',['episode_summary.mechanisms[1].claim_parts[4].evidence'],'Added patch-source anchors to the mechanism\'s integration correspondence part so the part cites both artifact and matching metadata.',[para1,para2,ev('supplement_metadata','"merge_commit_sha": "89306ab0df93bfdf5630910bc20b1eccb7379172"')])

limitation=' The final paragraph omits the explicit for backwards compatibility phrase from the proposed wording. Observed application is limited to the documented flag-dependent behavior and usefulness/confusion rationale, not verbatim adoption of every offered phrase.'
U['S05']['institution']['application_evidence'][0]['rationale']+=limitation
U['S05']['disposition_events'][0]['rationale']+=limitation
U['S05']['uncertainty_reason']+=' The final paragraph does not repeat the explicit backward-compatibility phrase.'
mech['claim_parts'][3]['text']='The retained release-notes patch contains the incoming/outgoing distinction and account/label explanation, plus the empty-string distinction and usefulness/confusion explanation; it omits the proposed explicit backward-compatibility phrase.'
mech['claim_parts'][3]['evidence']=[para1,para2,ev('review_comments:3')]
mech['claim']=' '.join(x['text'] for x in mech['claim_parts'])
mech['evidence']=unique([e for part in mech['claim_parts'] for e in part['evidence']])
log('R08',['S05.institution.application_evidence[0].rationale','S05.disposition_events[0].rationale','S05.uncertainty_reason','episode_summary.mechanisms[1].claim_parts[3]','episode_summary.mechanisms[1].claim','episode_summary.mechanisms[1].evidence'],'Narrowed the implementation description by naming the offered backward-compatibility phrase that the final paragraph omits. The code still describes observed documentation of the behavioral distinction, not verbatim wording adoption.',[ev('review_comments:3'),para2],effect='coverage_or_scope_loss',meaning=True)

# Exhaustive one-pass source review findings and one resolution for every checker audit flag.
predicate_notes={
 'S01':[
  'Backport is a noun in the supplied body. The proposed verb is reconstructed and remains context_inferred/semantic_inference; its governor now contains only the backport clause.',
  'PR #14411 is the object of the nominal backport and acquires Bdir under the proposed-action parse. Its complete identifier is preserved, distinct from current PR #14441.',
  'v0.17 is the backport destination, inferred as Bind from the to phrase; Cex is an explicitly preserved defensible alternative. The governor is narrowed to the same backport clause.'
 ],
 'S02':[
  'Should is the actual modal governing be in the spelling recommendation. Its explicit deontic role survives the pragmatic editing parse; this supplies advisory force, not authority.',
  'Use is not literally present and is correctly labeled a semantic inference from Should be. The alternate technical-description reading remains visible.',
  'The spelling is a predicate complement under literal be and therefore has an inferred Bdir role under use. The complete name and final s survive.'
 ],
 'S03':[
  'I in I\'d is the subject of change, retained as the hypothetical speaker. It is not the actual contribution author, and it does not create a committed personal plan.',
  'Change is supplied directly in the action clause; recommendation force does not make this verb inferred.',
  'It is the local direct object of change; the antecedent paragraph occurs in the preceding sentence and is explicitly explained. It is not borrowed from a different predicate.',
  'The replacement after change it to explicitly constrains the resulting wording. The complete offered paragraph preserves flag conditions and the account/label rationale; these are not activation conditions on the editor.'
 ],
 'S04':[
  'Drop is the explicit action; Maybe is a hedge rather than a lexical D.',
  'The object is elided after drop and recovered from the preceding predicate. Context_reference and context_inferred correctly identify the outside-unit evidence.',
  'For clarity explicitly states the purpose qualifying execution and is Cex; no fabricated if-seeking-clarity activation condition is added.',
  'Unless I\'m missing something qualifies whether to follow the advice and is retained as Cac. An epistemic-scope-note representation is also possible; the condition is not lost.'
 ],
 'S05':[
  'Document is the actual requested action in the subordinate infinitival clause. I belongs to think and is correctly not used as the actor of document.',
  'The empty string change is the direct object of document in that clause; no inferred role is needed.',
  'The Maybe-introduced blockquote specifies proposed documentation content. It does not institute permission to call the RPC or a sanction for an invalid argument.'
 ]}
qual_notes={
 'S01':'The version, referenced PR, partial rather than full reversal of both named objects, and asserted fix all remain attached. The latter is a body claim, not an independently verified outcome. Body creation date is not used to date every sentence.',
 'S02':'The name includes the final s. The requested location is the release-notes source context; the actual prior typo and editor remain unspecified.',
 'S03':'Both settings, both outgoing/incoming versus incoming only, the three argument names, and the past-account/current-label explanation are preserved. The explicit tentative I\'d maybe qualifier was added to the qualifier register.',
 'S04':'Maybe, clarity purpose, the missing-something exception, and the antecedent new check for "*" remain visible. Attachment now correctly distinguishes the hedge scope note from Cac.',
 'S05':'The empty-string/unlabeled link, setting/no-setting contrast, backward-compatibility framing, error behavior, low-usefulness rationale, confusion possibility, and Maybe are retained. Final implementation is explicitly limited because the backward-compatibility phrase is omitted.'}
app_notes={
 'S02':[
  ('retained','Observed means that the resulting name is present in the retained integrated release-notes artifact. It does not verify the earlier typo or uniquely identify the fixed reply.'),
  ('retained','The author\'s update and reviewer\'s description support reported PR-level revision, so broader_proposal is retained rather than a particular repair target.'),
  ('unresolved','Fixed alone does not identify the repaired item. Unresolved target remains appropriate; the separate observed artifact evidence supplies the limited application profile.')],
 'S03':[
  ('retained','The supplied final paragraph materially preserves the requested setting distinction and account/label explanation, with formatting/wording differences. Matching patch revision, head, and merge metadata support the limited observed edit.'),
  ('retained','The reports refer to PR/release-notes updates generally. Their target remains broader_proposal rather than an itemized implementation report.')],
 'S04':[
  ('retained','The author expressly names the same check and reports removal. This supports reported, not observed, application because the exact earlier check and intermediate diff are absent.')],
 'S05':[
  ('corrected','The artifact documents the requested behavioral distinction and usefulness/confusion explanation. The rationale now expressly excludes verbatim adoption of the backward-compatibility phrase, absent from the final paragraph.'),
  ('retained','The author/reviewer reports remain broader-proposal evidence, not precise enumeration of this paragraph edit.')]
}
resolutions=[];pidx={};aidx={};summary_index=0
for i,flag in enumerate(checks['review_flags']):
 uid=flag['unit_id'];code=flag['code'];status='retained';subject=uid or 'episode_summary';evidence=[]
 if code=='qualifier_audit':
  rationale=qual_notes[uid];evidence=unique([e for q in U[uid]['proposition']['qualifiers'] for e in q['evidence']]);status='corrected' if uid in ['S03','S04','S05'] else 'retained'
 elif code=='predicate_audit':
  n=pidx.get(uid,0);pidx[uid]=n+1;c=U[uid]['components'][n];subject=f'{uid}.components[{n}] ({c["symbol"]})';rationale=predicate_notes[uid][n];evidence=unique(c['evidence']+[c['governing_span']]);status='corrected' if uid=='S01' else 'retained'
 elif code=='application_audit':
  n=aidx.get(uid,0);aidx[uid]=n+1;status,rationale=app_notes[uid][n];subject=f'{uid}.institution.application_evidence[{n}]';evidence=U[uid]['institution']['application_evidence'][n]['evidence']
 elif code=='summary_audit':
  n=summary_index;summary_index+=1
  if n<4:
   item=a['episode_summary']['observed_outcomes'][n];subject=f'episode_summary.observed_outcomes[{n}]';status='corrected' if n==1 else 'retained'
   rationale=[
    'PR identity, merged=true, merge timestamp, base, and full matching hashes support each part. The outcome is repository integration only; no referenced-PR outcome or network uptake is inferred.',
    'Each wording/behavior claim is grounded in the retained release-notes patch. The correspondence part now cites artifact sources as well as metadata; the supplied patch-entry revision attribute is the bridge. No claim of runtime correctness is made.',
    'The outcome is explicitly a participant report. The comment supplies both the check reference and removal report; no direct observation of the precise diff is claimed.',
    'The two exact ACK hashes and since-last-review sentence support a review target update and reported change scope. They do not establish changed judgment or required reapproval.'
   ][n]
  else:
   k=n-4;item=a['episode_summary']['mechanisms'][k];subject=f'episode_summary.mechanisms[{k}]';status='corrected' if k==1 else 'retained'
   rationale=[
    'The concern/request, named-check response and removal report, and updated review provide specific correspondence. supported_sequence describes this limited textual sequence, not a causal estimate or sanction.',
    'The requests, attributed author update, updated review, final artifact, and recorded merge each have claim-part anchors. The final wording omission is now explicit; the artifact/head correspondence cites both source types. Causation and exact reply pairing remain limited.'
   ][k]
  evidence=item['evidence']
 else:raise RuntimeError(flag)
 resolutions.append({'checker_file':'checks.first.json','flag_index':i,'flag':flag,'subject':subject,'status':status,'rationale':rationale,'evidence':evidence})

coverage=[]
for screen in a['entry_screening']:
 s=entries[screen['source_id']]
 coverage.append({'source_id':s['source_id'],'focal':s['source_id'] in p['selection_design']['focal_source_ids'],'screening_retained':screen['disposition'],'unit_ids':screen['unit_ids'],'finding':screen['reason'],'evidence':[ev(s['source_id'])] if s['text'] else [],'empty_text_verified':s['text']==''})

crosschecks=[
 {'topic':'type_and_authority','status':'retained','finding':'All five statements remain undetermined: the body is a plausible offered technical contribution and the four review requests are one-off technical/editorial recommendations. No authorization, attributed enforcement provision, explicit committed method, recurring accountability expectation, or institutional status is supplied. ACK counts cannot fill that gap.','evidence':[ev('body'),ev('review_comments:0'),ev('review_comments:1'),ev('review_comments:2'),ev('review_comments:3')]},
 {'topic':'recognition','status':'retained','finding':'ACKs and ordinary author assent remain ordinary_assent/response. None identifies a governing expectation or institutional status as a reason. The same reviewer\'s later ACK is not interpersonal recognition of that reviewer\'s own proposal; all events use the same episode key. Profiles remain none, while uncertain ordinary-assent targets stay explicit.','evidence':[ev('comments:1'),ev('comments:2'),ev('reviews:0'),ev('reviews:4'),ev('review_comments:4'),ev('review_comments:6')]},
 {'topic':'documentary_support','status':'retained','finding':'No institutional policy document supports a governing expectation. Final technical documentation is used as an applied edit artifact, not as documentary authority establishing an earlier review claim. Documentary profiles remain none.','evidence':[para1,para2]},
 {'topic':'dispositions_and_object_identity','status':'retained','finding':'Every event identifies current PR #14441. Its recorded merge is broader for the body and removal request, and limited to observable resulting documentation for the three doc requests. Referenced PR #14411 and #13075/#14023/#14382 do not inherit the containing PR\'s outcome. No rejection, withdrawal, sanction, or closed-unmerged status is invented.','evidence':[ev('body'),ev('supplement_metadata'),ev('review_comments:6'),para1,para2]},
 {'topic':'application_and_implementation_limits','status':'corrected','finding':'The final artifact supports the resulting spelling and substantive documentation distinctions. It does not establish every exact offered phrase, the prior typo, a complete chronology, runtime execution, or the exact intermediate check removal. The missing backward-compatibility phrase is now named.','evidence':[ev('review_comments:3'),para2,ev('review_comments:5'),ev('review_comments:6'),ev('patch:1')]},
 {'topic':'challenges_and_negation','status':'retained','finding':'Technical criticism motivates suggested edits, but no source disputes the chosen edit propositions, their institutional authority, or the backport decision itself. No, you\'re right agrees with the reviewer rather than rejecting the request. No focal dispute is inferred; behavioral error messages are not institutional sanctions.','evidence':[ev('review_comments:1'),ev('review_comments:2'),ev('review_comments:6')]},
 {'topic':'levels_and_scope','status':'retained','finding':'The focal actions are this contribution\'s backport and immediate edits. Both targets and visible review acts are operational and case-specific; discussion of technical evidence and backward compatibility does not constitute epistemic or collective-choice governance. No recurring review arrangement is proposed.','evidence':[ev('body'),ev('review_comments:0'),ev('review_comments:1'),ev('review_comments:2'),ev('review_comments:3')]},
 {'topic':'relations','status':'retained','finding':'Uptake runs from proposal/request to author response. The named-check correspondence supports explicit uptake; other doc-edit links remain context_inferred. Review_target_update points from the later reviewer ACK to the earlier one. Temporal direction relies on supplied timestamps and makes no causal assertion. No invented O, sanction, or logic conjunction is added.','evidence':unique([e for r in a['relations'] for e in r['evidence']])},
 {'topic':'presentation_and_record_roles','status':'retained','finding':'Replacement blockquotes are proposed_wording, not external/repeated quotation. Inline backticks do not make code blocks. ACKs and edit reports are context with reported_action speech acts; empty review bodies remain empty. Nonstatement records contain no grammar components or institutional standing claims.','evidence':[ev('review_comments:1'),ev('review_comments:3'),ev('reviews:4'),ev('review_comments:5')]},
 {'topic':'unresolved_interpretations','status':'unresolved','finding':'The backport body\'s candidate-versus-context reading remains open; the preferred pragmatic candidate is explicitly qualified. Both/fixed reply targets and the exact earlier check remain unresolved. These gaps are not resolved by the mechanical pass.','evidence':[ev('body'),ev('review_comments:4'),ev('review_comments:5'),ev('review_comments:2'),ev('review_comments:6')]}
]

notes={'run_id':'F02_v04_r2','review_count':1,'review_type':'complete_source_based_self_review_after_first_complete_freeze_and_first_checker','first_complete_sha256':hashlib.sha256((B/'annotation.first_complete.json').read_bytes()).hexdigest(),'mechanical_check_is_not_interpretive_certification':True,'reviewed_dimensions':['all_focal_sources_and_context_supplements','screening_omissions','material_qualifications','predicate_roles_and_governors','explicit_vs_inferred_evidence_basis','authority_documentary_recognition_application','dispositions_targets_and_object_identity','governance_levels_and_scope','relations','all_outcome_and_mechanism_claim_parts'],'coverage_review':coverage,'checker_flag_resolutions':resolutions,'crosscutting_source_review':crosschecks,'repair_ids':[r['change_id'] for r in repairs],'remaining_limits':a['episode_summary']['missing_evidence']+a['episode_summary']['unresolved_questions'],'status':'Source review complete; bounded alternatives and source limitations retained.'}

(B/'annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
(B/'annotation.final.json').write_bytes((B/'annotation.json').read_bytes())
(B/'repair_log.json').write_text(json.dumps({'run_id':'F02_v04_r2','mechanical_repairs':[],'source_review_changes':repairs,'first_complete_preserved':True,'changed_institutional_classifications':False},ensure_ascii=False,indent=2)+'\n')
(B/'review_notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_review_passes':1,'changes':len(repairs),'resolved_or_retained_flags':len(resolutions),'remaining_unresolved_flag_items':sum(r['status']=='unresolved' for r in resolutions),'first_complete_preserved':(B/'annotation.first_complete.json').read_bytes()!= (B/'annotation.final.json').read_bytes()}))
