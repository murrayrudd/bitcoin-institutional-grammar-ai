"""Coordinator reconciliation; original coding and independent audit stay unchanged."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
R=Path(__file__).resolve().parents[1]
A=json.loads((R/'analysis/independent_source_audit.json').read_text())
P=json.loads((R/'common_input/packet.json').read_text())
T={e['source_id']:e for e in P['entries']}
notes={
'SA02':'Accept the alternatives with a fixed comparison object. For the inherited merit-weighting claim, retain the narrower local-recognition formulation supported by 32406-169. A generalized repeated-support interpretation is possible, but it must not silently replace the exact April utterance or backdate the June documentation.',
'SA05':'Accept as a component/scope-link coverage issue. The premise remains in A227_camps; it is not wholly missing from A. Keep the alignment group unresolved because the focal children do not themselves carry or explicitly link all qualifications.',
'SA07':'Split the resolution. Exact assent to a deprecation definition permits either a bounded institutional-status-recognition reading or ordinary terminology endorsement. In contrast, the retained 33453 body explicitly attributes, quotes, and applies the conditional warning expectation, meeting the project convention for local recognition without a binding-rule requirement. Retain inherited U25 local support, distinguish challenges to its premise from rejection of the conditional principle, and retain the edited-body timing boundary.',
'SA10':'Accept the need to distinguish source words from inferred argument roles. Apply role-label corrections when the chosen action/role is reconstructed. Preserve a reasoned literal nominal-action alternative for translation-source updates and similar compounds; do not count every nominal parse as an established semantic error.',
'SA12':'Accept as a placement/scope-link difference, not wholesale omission. C retains the number in institutional evidence and screening commentary. The one-to-one component comparison still cannot impute that refinement to the focal unit, so the unresolved alignment remains appropriate.',
'SA15':'Accept the source-grounded enforcement-claim candidate while retaining uncertainty about force and authority. Same-speaker reapplication establishes that speaker’s maintained expectation; it cannot establish interpersonal recognition or consensus. For the exact channel claim, text_only is the conservative standing when no separate participant recognition is cited. Do not infer a verified repository sanction or a causal O relation.',
'SA18':'Accept the meaning-preserving split/combined alternative only with the same actor, subjective spam criterion, conditional freedom, and external attribution. Preserve the distinction between an editorial enablement recommendation and the embedded claimed permission; do not count the split units as multiple independent endorsements.',
'SA22':'Accept the alternative layers while preserving hypothetical future deprecation, the advisory preferably qualifier, and the informational purpose. Matching source spans alone cannot make a future-possibility claim identical to a schedule recommendation.',
'SA24':'Accept the codebook’s exact-quotation correspondence convention. Explicit correspondence is not explicit institutional recognition or causal influence. Preserve uncertainty in metadata-based semantic targeting when the available reply link does not verify exact implementation.',
'SA25':'Retain the workflow-status versus technical-description alternative for Reviewed. For the separate absolute freeze prohibition, accept the workaround as a challenge to categorical application, while retaining asserted rather than independently documented authority and no verified waiver.',
'SA26':'Retain epistemic and collective-choice target alternatives. Prefer operational for the visible contribution act unless a separately identified higher-level deliberative act is the analytical target. The reply challenges the application of open-source principles here; it does not reject transparency as a value.'
}
decisions=[]
for f in A['findings']:
    fid=f['finding_id']
    decisions.append({'audit_finding_id':fid,'category':f['category'],
       'disposition':'accepted_with_qualification' if fid in notes else 'accepted',
       'resolution':notes.get(fid,f['resolution_or_alternatives']),
       'affected_units':f['affected_units'],'evidence':f['evidence_spans'],
       'changes_applied_to_coder_outputs':False})

body=T['33453-body']
assert body['updated_at']=='2026-10-15T19:18:50Z'
temporal={'boundary_id':'RB01','source_ids':['33453-body','M33453'],
 'issue':'The retained proposal body attributes the earlier warning principle, but the supplied packet has no body version history establishing when every sentence appeared.',
 'metadata_reference':{'source_id':'33453-body','field':'updated_at','value':body['updated_at']},
 'resolution':'Textual attribution supports a link between the retained proposals. Do not infer from the creation date that the quoted passage existed before the September 30, 2025 merge. The later update timestamp does not prove that this particular sentence changed then either. Preserve the earlier model’s explicit restriction on dating edited sentences and on causal influence.',
 'status':'retained_evidentiary_boundary_not_a_new_historical_finding'}

reports=[
 {'title':'Recognition must attach to a specific proposition',
  'text':'The strongest standing disagreement concerns the conditional advice against removal warnings when no current removal plan exists. The retained 33453 proposal body attributes, quotes, and applies that expectation. This supports the inherited local-recognition judgment even though two fresh coders selected text_only. Local support does not require a binding project-wide rule. Exact assent to a definition of deprecation remains more interpretive: it can recognize an institutional status or simply endorse terminology. The explicit nonblocking-nits reply provides a clearer shared example of local recognition. Sources: 32714-body, 33453-body, 32406-180, and 32406-151.'},
 {'title':'Documentary support depends on scope and date',
  'text':'General guidance on moderation documents a procedure for warnings and bans; it does not independently verify the particular future sanction announced to a named contributor. Similarly, a later contribution guide supports discretionary merit weighting without proving the exact wording or force of an earlier categorical reminder. Broad maintainer release responsibility and deference on one backport decision are related but distinct evidence claims. Several standing differences arise because coders classify these different levels of specificity under one label. Sources: 32359-115, 32406-169, 32406-252, 33453-018, D_CONTRIB, and D_MOD.'},
 {'title':'Matching labels can conceal provenance errors',
  'text':'Within the body of PR 32381, a separate recommendation advocates proceeding with PR 32359. Two coders attach closure metadata for the containing PR to that recommendation. Both PRs closed unmerged, so the status labels match while the evidence targets differ. The correction is to attach the referenced proposal’s metadata or retain the containing proposal’s closure only as episode context. The audit also identified pronouns anchored to the wrong predicate occurrence and incomplete evidence arrays. Exact text matching alone did not detect those semantic targeting problems. Findings SA09, SA14, SA16, SA20, and SA21 preserve the repairs.'},
 {'title':'Higher level claims require bounded alternatives',
  'text':'The statement that a majority decides the winner supplies no electorate, threshold, jurisdiction, or decision procedure. Unknown is the least assumptive target level; constitutional and epistemic readings remain alternatives. The transparency statement more clearly expresses a contested legitimacy expectation, but its target can concern either the foundations of legitimate decisions or recurring decision procedures. The observed exchange does not establish adoption of a new arrangement. A thematic contrast between majority and merit claims also does not prove that they contest the same decision object. Sources: 32359-227, 32359-115, 32406-228, and 32406-229.'},
 {'title':'The absolute freeze claim faces a counterproposal',
  'text':'All three coders identify a categorical prohibition on translation-source updates after the final freeze and flag a dispute in its application. The proposed workaround would permit a source change while limiting translation disruption. It recognizes the reason for a freeze without independently establishing the absolute rule, a formal exception, or actual final translation processing. The inherited U32 annotation should therefore retain its limited evidentiary status while explicitly acknowledging this application challenge. Sources: 33224-010, 33224-015, 33224-019, and D_TRANSLATION.'},
 {'title':'Extraction differences need meaning and scope checks',
  'text':'Some inventory differences preserve meaning through different layers or subdivisions, including a user’s mempool-control claim and the distinction between possible future deprecation and a preferred removal schedule. The two unresolved alignment groups concern where a quoted premise and a tentative 150-byte refinement are stored. The full annotations retain those details in context or evidence, but the focal units do not attach them consistently. These are not established wholesale omissions. A shared convention deviation also survives: all three label a repeated literal bot question with a nonquestion speech act. Findings SA05, SA11, SA12, SA18, SA22, and SA23 retain these distinctions.'},
 {'title':'The central evidentiary boundaries survive',
  'text':'All three distinguish the reported addition of a source comment from verification of its exact wording, an announced moderation consequence from an observed ban, and repository integration from Bitcoin network adoption. They reproduce the supplied sequence of deprecation and warning edits while avoiding a permanent maintenance commitment or a fixed removal timetable. These agreements support the bounded reconstruction. The retained proposal bodies also show explicit attribution across proposals, but absent version histories the analysis cannot date the insertion of every quoted sentence or establish its causal effect on merger.'}
]
out={'reconciliation_id':'R12_coordinator_reconciliation_v01','date_utc':datetime.now(timezone.utc).isoformat(),
 'independent_audit_sha256':hashlib.sha256((R/'analysis/independent_source_audit.json').read_bytes()).hexdigest(),
 'scope':'All 26 independent grouped findings reviewed, plus source and baseline checks by the coordinator. These are revisable analytical resolutions, not a gold standard or accuracy score.',
 'method':'Use exact source support and the frozen specification; do not choose a label by majority vote. Distinguish corrections, alternatives, and unresolved scope. Preserve all submitted coder records and raw agreement statistics.',
 'decisions':decisions,'additional_boundaries':[temporal],'report_findings':reports,
 'raw_agreement_unchanged':True,'applied_to_inherited_files':False,
 'next_specification_clarifications':['Define the proposition and the level of generality before assigning standing.','Distinguish ordinary assent, status recognition, and explicit application of an expectation; record same-speaker repetition separately.','Retain the scope and date of documentary support.','Specify how higher-level claims differ from observed institutional changes.','Require qualifiers and antecedents to remain linked to the focal proposition, including when stored in context.','Check proposition identity in disposition events and the predicate occurrence supporting each component.'],
 'clarifications_status':'Recommendations for a later specification, not post-hoc changes to the frozen coding instructions or reported agreement.'}
(R/'analysis/source_reconciliation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
ar=json.loads((R/'analysis/alignment_review.json').read_text())
ar['source_audit_clarification']='SA05 and SA12 show that the quoted premise and numeric refinement remain in full-annotation context/evidence. The unresolved mapping concerns their attachment to the focal units, not wholesale omission from the complete annotations. The mapping and score denominator remain unchanged.'
(R/'analysis/alignment_review.json').write_text(json.dumps(ar,indent=2)+'\n')
print('Reconciled',len(decisions),'independent findings; preserved raw coding and agreement.')
