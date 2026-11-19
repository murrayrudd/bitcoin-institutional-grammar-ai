import json, hashlib, copy
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=json.loads((ROOT/'packet.json').read_text())
a=json.loads((ROOT/'annotation.json').read_text())
original=copy.deepcopy(a)
texts={e['source_id']:e['text'] for e in p['entries']}
U={u['unit_id']:u for u in a['units']}
changes=[]
def ev(s,q):
    x=texts[s].index(q)
    return {'source_id':s,'span':{'start':x,'end':x+len(q),'quote':q}}
def ue(uid):return {'source_id':U[uid]['source_id'],'span':copy.deepcopy(U[uid]['span'])}
def change(path,value,category,reason,evidence,meaning=True,conclusion=False):
    keys=path.strip('/').split('/')
    obj=a
    for k in keys[:-1]:obj=obj[int(k)] if isinstance(obj,list) else obj[k]
    k=int(keys[-1]) if isinstance(obj,list) else keys[-1]
    before=copy.deepcopy(obj[k]);obj[k]=copy.deepcopy(value)
    if before==value:raise ValueError('Not a change: '+path)
    changes.append({'repair_id':f'R{len(changes)+1:02d}','phase':'source_self_review','path':path,'category':category,'meaning_changed':meaning,'institutional_conclusion_changed':conclusion,'before':before,'after':copy.deepcopy(value),'rationale':reason,'evidence':evidence})

# Correct the target case of color/punctuation changes; the alternative red styling
# is for the non-replaceable case, not a contradiction of an unqualified no-red rule.
for uid in ['U06','U07']:
    ui=next(i for i,u in enumerate(a['units']) if u['unit_id']==uid)
    comps=copy.deepcopy(U[uid]['components'])
    comps[2]['text']='in the confirmation window'
    comps[2]['inference_note']='The enclosing sentence supplies the shared location. The replaceable-case scope is inferred separately from the surrounding label discussion and contrasting non-replacable-case recommendation.'
    comps.append({'symbol':'Cac','text':'for the currently discussed replaceable-case confirmation','basis':'context_inferred','evidence':[ev('pr7819:comments:1','"replaceable" there'),ev('pr7819:comments:1','the non-replacable case')],'inference_note':'The current confirmation is discussed using replaceable, followed by a contrasting suggestion to put red text on the non-replacable case. This limits the omission request to the current replaceable-case presentation, rather than all confirmation windows. Both anchors are outside this child and refer to the same enclosing review comment.','occurrence_role':'context_reference'})
    change(f'/units/{ui}/components',comps,'substantive_qualification','The first complete parse did not explicitly restrict omission to the currently discussed replaceable case. Add that inferred scope and remove the unsupported extra words for this transaction from the location component.',[ue('U05'),ue('U08'),ue('U09')],meaning=True,conclusion=False)

# A quote establishes its reproduced proposition, not every subsequent rhetorical
# statement as an explicit proposition-specific reply.
rec=copy.deepcopy(U['U04']['institution']['recognition'][1])
rec['basis']='context_inferred'
rec['rationale']='The quoted exposure concern and explicit agreement are followed by a contrast between ongoing GUI work and review already being possible. The later review assertion plausibly responds to the concern, but that rhetorical connection is inferred; the quote itself directly establishes only its own target, and no promise of deferral follows.'
change('/units/3/institution/recognition/1',rec,'epistemic_labeling','Limit explicit evidence to the quotation and agreement; the review-now extension is a contextually inferred response.',[ue('U11'),ue('U12'),ue('U13'),ue('U14')],meaning=True,conclusion=False)
r=copy.deepcopy(a['relations'][5]);assert r['from_unit_id']=='U04' and r['to_unit_id']=='U14'
r['basis']='context_inferred'
r['rationale']='The review-now assertion follows a quoted exposure concern and agreement, plausibly distinguishing review from exposure. This rhetorical response link is contextual; exact quotation does not make every following clause an explicit response to the same proposition, nor show implementation of a deferral condition.'
change('/relations/5',r,'epistemic_labeling','Align uptake with the limited evidence supporting the response target.',[ue('U11'),ue('U12'),ue('U13'),ue('U14')],meaning=True,conclusion=False)

# A scope challenge concerns continuation/application of the method, not whether
# the author actually made the reported attempt.
inst=copy.deepcopy(U['U17']['institution'])
inst['dispute_present']=True
inst['rationale']+=' The author\'s next fee-only question tentatively challenges continued application or scope of this method, rather than disputing that the attempt occurred. Text-only standing remains appropriate; this flag records self-questioning of scope, not established interpersonal conflict or a rejected strategy.'
inst['evidence'].append(ue('U18'))
change('/units/16/institution',inst,'interpretive_consistency','Make the bounded application challenge visible in the institution fields as well as the already retained challenges relation; do not upgrade it to a settled dispute or withdrawal.',[ue('U17'),ue('U18')],meaning=True,conclusion=False)
r=copy.deepcopy(a['relations'][9]);assert r['from_unit_id']=='U18' and r['to_unit_id']=='U17'
r['rationale']='The fee-only question tentatively challenges continuation or scope of the additional-output method, not the historical truth of the reported attempt. This is the author\'s self-questioning, not evidence of interpersonal conflict, withdrawal, or a settled decision.'
change('/relations/9',r,'qualification','Specify which aspect of the reported strategy the challenge targets.',[ue('U17'),ue('U18')],meaning=False,conclusion=False)

# Retained body contents cannot be assigned a composition time from creation time.
r=copy.deepcopy(a['relations'][1]);r['rationale']='Both retained occurrences question proceeding before replacement exists; the comment names wallet capability, whereas the body names a GUI workflow. This contextual clarification preserves the difference in scope and does not establish when the retained body wording was composed.'
change('/relations/1',r,'temporal_qualification','Remove reply wording that could imply a verified relationship to an earlier version of the body.',[ue('U04'),ue('U02')],meaning=True,conclusion=False)
r=copy.deepcopy(a['relations'][6]);r['rationale']='The review-now assertion makes more explicit the retained body\'s desire not to hold back review. This is a semantic clarification across the supplied occurrences; body edit history is unavailable, so the direction does not assert which wording was composed first or authorize integration.'
change('/relations/6',r,'temporal_qualification','Remove later-versus-earlier composition claims about retained body wording.',[ue('U03'),ue('U13'),ue('U14')],meaning=True,conclusion=False)
m=copy.deepcopy(a['episode_summary']['mechanisms'][0])
m['claim']='The retained body questions inclusion without a replacement GUI workflow while expressing a desire not to delay review. In the supplied discussion, a commenter questions exposure before wallet replacement is possible; the author quotes and agrees with that concern, reports GUI work in progress, and says this can already be reviewed, citing a difficult 0.13 timeline. The specifically corresponding comment exchange distinguishes review timing from readiness to expose the feature; it shows no adopted gating rule or completed review. The retained body wording has no verified composition date within this exchange.'
change('/episode_summary/mechanisms/0',m,'temporal_qualification','Support the sequence through exact comment quotation and response, without assuming the retained body wording predates those comments.',[ue('U02'),ue('U03'),ue('U04'),ev('pr7819:comments:2',texts['pr7819:comments:2'])],meaning=True,conclusion=False)
m=copy.deepcopy(a['episode_summary']['mechanisms'][1])
m['claim']=m['claim'].replace('The subsequent reply explains child-transaction handling and conditional growth in computed versions.','A later comment addressing the same additional-output workflow explains child-transaction handling and conditional growth in computed versions.')
change('/episode_summary/mechanisms/1',m,'qualification','The technical correspondence supports a response interpretation, but no reliable reply thread is supplied.',[ue('U17'),ue('U18'),ev('pr7819:comments:4',texts['pr7819:comments:4'])],meaning=False,conclusion=False)

(ROOT/'annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
(ROOT/'annotation.final.json').write_bytes((ROOT/'annotation.json').read_bytes())
(ROOT/'repair_log.json').write_text(json.dumps({'run_id':'F03_v03_r2','first_complete_sha256':hashlib.sha256((ROOT/'annotation.first_complete.json').read_bytes()).hexdigest(),'final_sha256':hashlib.sha256((ROOT/'annotation.final.json').read_bytes()).hexdigest(),'mechanical_repairs':[],'source_self_review_passes':1,'changes':changes,'note':'All changes occurred after the first-complete freeze and initial mechanical pass. Each listed before/after value identifies the complete modified field; frozen inputs and the first-complete file were not modified.'},ensure_ascii=False,indent=2)+'\n')

# Review records describe the single complete source-based self-review.
unit_reviews={
'U01':'Retained as a technical feature/scope context endpoint. Technical allows is not institutional permission; missing GUI replacement is explicit.',
'U02':'Retained conservative candidate with unresolved force. Deferral action and its we/Bdir roles are inferred; the absence of GUI workflow activates the reservation. Working on it/bigger chunk are not promises. No adoption or authority is inferred.',
'U03':'Retained tentative personal strategy with literal-desire alternative. Negative desire does not logically guarantee action; the normalization is explicitly inferred. The first-person agent and patient of hold back retain their roles. No duty to perform a review is invented.',
'U04':'Retained advisory exposure candidate with exact until-wallet-capability qualification. The explicit patient survives the inferred deferral action. Agreement is endorsement, not expectation recognition; review-now response basis corrected to contextual.',
'U05':'Retained structural parent only. It carries the common negative evaluation for two children and is never counted as a third proposition.',
'U06':'Retained independently executable color change with inferred omission action and transformed target. Corrected the missing replaceable-case scope; the short child inherits its location/evaluation from the parent and same-comment contrast. Non-replaceable red styling remains possible.',
'U07':'Retained independently executable punctuation change. Inferred action/target, shared confirmation location, and newly explicit inferred replaceable-case scope preserve the intended target without treating the bang as a general forbidden mark.',
'U08':'Retained conservatively as a possible label-revision request, with technical-rationale-only alternative. Source subject becomes inferred object; may is not evidence that users were actually confused.',
'U09':'Retained hedged recommendation for the non-replacable case. Display action, displayed object role, and case trigger are inferred; the second should anchors the correct predicate. Because-fee-update claim is the speaker\'s rationale, not a measured outcome.',
'U10':'Retained one coupled alternative design. We and have are explicit; shared should and rhetorical instead scope are explained. N future-locktime replacements, multiplicative fees, and displayed fee schedule are all preserved. No mandatory XOR, adopted method, or second endorsement is invented.',
'U11':'Retained repeated quotation with exact supplied text. Original underscore emphasis is omitted in the supplied repetition; it points to U04 rather than becoming a new statement.',
'U12':'Retained explicit agreement context. It supports endorsement of the quoted concern, not recognized obligation, compliance, or proven deferral.',
'U13':'Retained report of work in progress. Working is not completion, promise, or a distinct institutional method beyond the surrounding candidates.',
'U14':'Retained capability-versus-permission ambiguity with unresolved force. Passive this remains explicit patient; reviewers are not identified. Already scopes timing, and incomplete GUI work is contrast rather than a condition that review must wait for.',
'U15':'Retained exact repeated adaptive-fee quotation, linked to U10 and not counted as another proposal.',
'U16':'Retained tentative endorsement context; Yes plus might be a solution does not establish selection or implementation.',
'U17':'Retained past attempted personal method as a strategy candidate with context-only alternative. Trying and the sendcoins workflow are preserved. Scope/application self-questioning is now flagged without denying the past attempt or marking it withdrawn.',
'U18':'Retained literal question-form tentative narrowing recommendation. We, should, focus, fee target, and just preserve the proposed scope. Maybe prevents converting it into an adopted prohibition of additional outputs.',
'U19':'Retained plausible technical-necessity requirement with institutional force unresolved. Handle stays separate from its child-transaction target; purpose/confirmation condition qualifies use, not the time construction starts. Additional-output workflow supplies inferred shared activation scope.',
'U20':'Retained technical conditional consequence, not a separate prescription or O sanction. The embedded must compute concerns workload under repeated workflow execution; its alternative extraction is documented.',
'U21':'Retained one wording choice with both updatable/amendable alternatives and displaced replacable spelling intact. Source grammatical subject becomes inferred object of use. Proposed wording presentation and literal question speech are preserved.',
'U22':'Retained weak technical interest as context. It supports qualified endorsement of the design but neither commitment nor expectation recognition.',
'U23':'Retained single delayed-send option with built-in delay, amend-within-timeout condition, and tentative abort-before-initially-set capability. Properties are proposed technical effects, not observed outcomes, permissions, negative duties, or institutional consequences. Counterintuitive label and ambiguous set remain unrepaired.',
'U24':'Retained inferred conditional spelling correction. Jonas is an inferred actor from explicit addressee, not an inferred maintainer. Preserve incomplete replaceab fragment, negative if-not-following condition, and uncertain suggestion reference. No full replacement string or verified real-name mapping is invented.',
'U25':'Retained text-only maintenance norm candidate with unresolved technical need versus obligation. Rebase is a reconstructed verb; no actor, institutional authority, deadline, response, or enforcement is supplied. Broad closure does not reject the specific request.',
'U26':'Retained author closure and inclusion report as context. Distinguish #7819 from #8182 and participant-reported inclusion from verified implementation or repository integration.'
}
review={'run_id':'F03_v03_r2','review_type':'one complete source-based self-review after initial checker','source_self_review_passes':1,'first_checker_status':'pass','mechanical_validity_is_not_semantic_certification':True,'entry_review':[], 'unit_review':[], 'relation_review':[], 'recognition_review':[], 'disposition_review':[], 'outcome_review':[], 'mechanism_review':[], 'checker_flag_resolutions':[], 'cross_cutting_review':[]}
for sc in a['entry_screening']:
    sid=sc['source_id']
    review['entry_review'].append({'source_id':sid,'status':'retained','focal_exhaustive':sid in p['selection_design']['focal_source_ids'],'unit_ids':sc['unit_ids'],'finding':sc['reason'],'evidence':[ev(sid,texts[sid])]})
for u in a['units']:
    review['unit_review'].append({'unit_id':u['unit_id'],'status':'corrected' if u['unit_id'] in ['U04','U06','U07','U17'] else 'retained','finding':unit_reviews[u['unit_id']],'evidence':[ue(u['unit_id'])]})
    for j,r in enumerate(u['institution']['recognition']):
        review['recognition_review'].append({'unit_id':u['unit_id'],'recognition_index':j,'status':'corrected' if u['unit_id']=='U04' and j==1 else 'retained','kind':r['kind'],'target':r['target'],'basis':r['basis'],'finding':r['rationale']+' No locally_supported standing is inferred from this event.','evidence':r['evidence']})
    for j,d in enumerate(u['disposition_events']):
        review['disposition_review'].append({'unit_id':u['unit_id'],'disposition_index':j,'status':'retained','finding':d['rationale'],'evidence':d['evidence']})
for i,r in enumerate(a['relations']):
    review['relation_review'].append({'relation_index':i,'from_unit_id':r['from_unit_id'],'to_unit_id':r['to_unit_id'],'type':r['type'],'status':'corrected' if i in [1,5,6,9] else 'retained','finding':r['rationale'],'evidence':r['evidence']})
for i,o in enumerate(a['episode_summary']['observed_outcomes']):
    review['outcome_review'].append({'outcome_index':i,'status':'retained','claim':o['claim'],'finding':'Each material positive claim is supported by the cited occurrence or object-specific metadata. Negative limitations follow the packet source limits; no causal attribution, transfer of PR status, verified per-suggestion implementation, or network adoption is asserted.','evidence':o['evidence']})
for i,m in enumerate(a['episode_summary']['mechanisms']):
    review['mechanism_review'].append({'mechanism_index':i,'status':'corrected' if i in [0,1] else 'retained','mechanism_status':m['status'],'claim':m['claim'],'finding':'Checked initiation, attributed response, intervening technical discussion or action, recorded outcome, and alternative explanation. The sequence label applies to textual correspondence, not causal identification. Body composition and reply-thread limitations are now explicit.','evidence':m['evidence']})
review['cross_cutting_review']=[
 {'topic':'Authority, recognition, and application','status':'retained','finding':'No rule_candidate, authority_allocation mechanism, expectation_recognition event, locally_supported standing, or sanction is inferred. Need/should/can and technical assent do not independently establish authority. The contribution-method application is tentatively self-questioned in U17-U18; actual review/integration application is not demonstrated.','evidence':[ue('U04'),ue('U12'),ue('U14'),ue('U16'),ue('U17'),ue('U18'),ue('U25')]},
 {'topic':'Levels and scope','status':'retained','finding':'All retained statement targets concern this contribution\'s design, readiness, review, or maintenance and are operational/case_specific. End-user feature reuse is not a general contribution-governance arrangement. The child-transaction and fee mechanisms are technical, not constitutive institutions. There is no supplied constitutional, epistemic, or recurring collective-choice arrangement; nonstatements retain not_applicable target levels and the container has no observed level.','evidence':[ue('U02'),ue('U10'),ue('U14'),ue('U18'),ue('U19'),ue('U23'),ue('U25'),ue('U26')]},
 {'topic':'Object identity and dispositions','status':'retained','finding':'PR 7819 closure is not transferred to any proposed behavior or inferred to be rejection. PR 8182 has separate supplied closed/unmerged metadata; neither merge_commit_sha is a merge. Included there is a report, and PR 7159 remains an unexamined linked provenance reference.','evidence':[ue('U26'),ev('pr7819:metadata','"merged": false'),ev('pr8182:supplement_metadata','"merged": false'),ev('pr7819:body','Includes two refactoring commits from https://github.com/bitcoin/bitcoin/pull/7159')]},
 {'topic':'Omissions and segmentation','status':'retained','finding':'All 10 focal entries were exhaustively screened; all 9 supplements were screened for context. No additional focal candidate was added in self-review. Independent color and punctuation requests are children of one uncounted container; adaptive replacement design and label alternatives remain coupled. Technical side effects and parenthetical capability descriptions are not detached into sanctions or invented duties. Bare review feasibility, desire, and reported technical methods retain explicit noninstitutional alternatives.','evidence':[ue('U05'),ue('U06'),ue('U07'),ue('U10'),ue('U20'),ue('U21'),ue('U23')]},
 {'topic':'Remaining substantive uncertainty','status':'unresolved','finding':'The packet does not settle whether several technical suggestions are institutional expectations, whether review-now is permission, whether personal preferences/past methods are operative strategies, exactly what Greg\'s suggestion and initially set refer to, which edits were included in #8182, or what caused supersession. These limits remain in unit alternatives and episode_summary; no new sources were added.','evidence':[ue('U02'),ue('U03'),ue('U14'),ue('U17'),ue('U19'),ue('U23'),ue('U24'),ue('U25'),ue('U26')]}
]
(ROOT/'review_notes.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_self_review_passes':1,'repair_entries':len(changes),'units':len(a['units']),'statements':sum(u['record_role']=='statement' for u in a['units'])}))
