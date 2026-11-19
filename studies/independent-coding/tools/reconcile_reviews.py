"""Assemble the coordinator's explicit adjudications; never change coder/reviewer outputs.

The decisions below are qualitative judgments, not an automatic truth classifier.
Counts describe distinct proposition/error/case groups, not accuracy rates.
"""
from pathlib import Path
import json,hashlib,datetime,collections
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def write(p,j):p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
reviews={k:read(R/'reviews'/n/'review.json') for k,n in [('A','source_review_a'),('B','source_review_b')]}
findings={f['finding_id']:f for j in reviews.values() for f in j['findings']}
annotations={a['annotation_id']:a for a in read(R/'reviews/source_review_a/annotations.json')}
key={v:k for k,v in read(R/'analysis/mask_key.json').items()}
merged={'A001':['B002'],'A002':['B003'],'A005':['B001'],'A012':['B010'],'A031':['B004'],'A033':['B007'],'A035':['B005'],'A037':['B008'],'A041':['B006']}
groups=[]
def add(gid,refs,category,diagnosis,effect,note='',resolution=None,selection=None,title=None,qualification=None):
    fs=[findings[x] for x in refs];case=fs[0]['episode_id'];assert all(f['episode_id']==case for f in fs)
    aff={};ev={}
    for f in fs:
        for x in f['affected']:
            aid=x['annotation_id']
            if selection is not None and aid not in selection:continue
            units=x.get('unit_ids',[])
            if selection is not None:units=[u for u in units if u in selection[aid]]
            if selection is not None and not units:continue
            a=aff.setdefault(aid,{'annotation_id':aid,'run_id':key[aid],'condition':key[aid].split('_')[1],'unit_ids':set(),'relation_ids':set(),'summary_paths':set()})
            a['unit_ids'].update(units);a['relation_ids'].update(x.get('relation_ids',[]));a['summary_paths'].update(x.get('summary_paths',[]))
        for e in f['source_evidence']:ev[json.dumps(e,sort_keys=True)]=e
    for a in aff.values():
        for k in ['unit_ids','relation_ids','summary_paths']:a[k]=sorted(a[k])
    groups.append({'group_id':gid,'episode_id':case,'title':title or fs[0]['description'].split('. ')[0]+'.','review_finding_refs':refs,'category':category,'diagnosis':diagnosis,'effect':effect,'coordinator_assessment':note or 'Accepted within the bounded scope of the independent finding after comparison with the supplied source and assigned guide; no stronger institutional conclusion follows.','resolution':resolution or fs[0]['resolution'],'qualification':qualification,'affected':list(aff.values()),'source_evidence':list(ev.values()),'applicable_rules':[f['applicable_rule'] for f in fs]})

# Primary groups: five distinct focal proposition/relationship issues.
add('P01',['A033','B007'],'primary_error','execution_failure','evidence_basis',
 'The follow-up pruning option explicitly concerns unidentified later work. The current discussion identifier cannot identify that future contribution, even though the prose correctly disclaims implementation.',
 'Use a null decision_object_id for the unidentified follow-up. Preserve #26586 solely as the discussion episode and do not transfer its merge outcome.',
 {'R03':['C30'],'R10':['U24']},'Unidentified pruning follow-up assigned the containing PR ID')
add('P02',['A033','B007'],'primary_error','execution_failure','evidence_basis',
 'Applying the selection criterion to other versions in a separate pull is a second, differently qualified proposition. R03 assigns #26586 to it and its general-cleanup endorsement. The source expressly separates that work from the current PR.',
 'Leave the separate cleanup object unidentified. Preserve general-cleanup assent without treating the episode identifier as a known future proposal.',
 {'R03':['R05']},'Separate cleanup proposal assigned the containing PR ID')
add('P03',['A041','B006'],'primary_error','execution_failure','evidence_basis',
 'The later open-and-rebase suggestion does not reproduce the dependent-PR stopping condition. The same-actor-restatement event therefore overstates full-proposition correspondence. R04 itself notes the different timing qualification; this supports narrowing the event, not any claim of interpersonal recognition.',
 'Retain a same-actor response about the broader open-PR method. Do not claim repetition of the full until-another-PR-needs-it condition.',
 {'R04':['S13']},'Partial method repetition targeted at the complete conditional proposition',
 'Reviewer A emphasizes criterion ambiguity; reviewer B treats the target scope as an execution error. The coordinator counts only the unsupported full-proposition restatement, leaving the profile convention in Q041.')
add('P04',['A031','B004'],'primary_error','execution_failure','evidence_basis',
 'The stored uptake direction reverses initiating proposal and response under the assigned relation definition. The prose preserves their scope correspondence, so this changes evidence linkage rather than the broad institutional conclusion.',
 'For uptake, reverse endpoints to R10 U30 -> U33 and retain contextual basis. Alternatively use clarifies U33 -> U30 with a bounded rationale.',
 {'R10':['U30','U33']},'Uptake relation reverses the proposal-response direction',
 'Reviewer A calls this convention-only; reviewer B calls it evidence-basis. The coordinator uses evidence-basis because a consumer of the directed relation receives the wrong initiating/response order. Sensitivity counts also show the convention-only treatment.')
add('P05',['B011'],'primary_error','execution_failure','evidence_basis',
 'The packet dates PR creation and supplies a later record updated_at, but supplies no sentence-level edit history. R02/R07 describe the body wording as earlier than the comment. Preserve the supported semantic relation while withholding that specific wording chronology. The later updated_at does not prove that this body sentence changed.',
 'Remove earlier/later wording claims between the retained body sentence and comment; retain semantic clarification and independently dated comment events.',
 {'R02':['F03-U03','F03-U14'],'R07':['F03-U03','F03-U11']},'Wording chronology inferred without sentence-level history',
 'Accepted with correction to reviewer B’s description: a later PR-record update is not proof of a body-text edit. The error is unsupported certainty about wording order, not proof that the opposite order occurred.')

# Remaining review issues. Split distinct propositions even when the reviewer combined them.
skip={'A008','A030','A031','A033','A041'}
for fid in sorted(k for k in findings if k.startswith('A')):
    if fid in skip:continue
    f=findings[fid];refs=[fid]+merged.get(fid,[])
    cat={'execution_failure':'convention_deviation','criterion_ambiguity':'criterion_ambiguity','defensible_alternative':'defensible_alternative','unresolved':'unresolved'}[f['diagnosis']]
    diagnosis=f['diagnosis'];effect=f['effect'];note='';qual=None;selection=None
    if cat=='convention_deviation':effect='convention_only'
    if fid=='A002':
        note='The two actor parses preserve the same tentative edit. The difference in parse_mode when only the performer changes remains a codebook convention ambiguity; no forced actor choice follows.'
    if fid=='A005':
        note='The guide permits observation of an act or artifact. The resulting spelling is visible, while a historically located typo-correction operation is not. This supports two bounded observation objects, not a proven false implementation claim.'
    if fid=='A007':
        note='The older guide permits explained explicit roles in pragmatic parses and does not contain the later governing-span test. Keep the inferred-acceptance-role preference and explicit-deliberative-agent alternative; do not retrospectively import the newer rule.'
    if fid=='A012':
        note='The record explicitly leaves the workflow object unknown and makes no implementation or expectation-recognition claim. Its semantically identifiable response nevertheless violates the guide’s unresolved-target convention. This is a convention correction, not an invented object or authority claim.'
        qual='Reviewer A assigns evidence-basis; reviewer B assigns convention-only. The coordinator retains the latter bounded effect.'
    if fid=='A022':
        note='The review/listing antecedent is plausible, but the exact ignored software object is not uniquely supplied. Keep the inference and the comment/listing alternative; do not count a demonstrated semantic error or observed bot execution.'
    if fid=='A024':
        note='The supplied adding action does not disappear when recommendation force is inferred. Use the literal action under the preferred convention. R10 understates its lexical basis but does not invent an action or stronger evidentiary support. It remains a convention-level finding here; a stricter basis-error treatment is included in sensitivity results.'
    if fid=='A025':
        selection={'R04':['S24'],'R09':['u23']}
        note='R04 and R09 retain an explicit supplied predicate while choosing pragmatic mode; that is a convention mismatch. R10 actually reconstructs an avoid-rushing predicate and marks its roles inferred, so its meaning-preserving alternative is separated below.'
        qual='Qualified relative to reviewer A: do not require a literal rewrite of R10 solely to impose the preferred surface form.'
    if fid=='A029':
        note='The guide prefers Cex for purpose wording. Cac preserves the same technical prerequisite here, so this is a nonpreferred convention and not a lost condition or false institutional duty. The preference does not establish one uniquely valid grammar.'
    if fid=='A032':
        note='The initiating endpoint is a technical assessment, not an extracted request/proposal. The reply direction and actual concession survive in the rationale. Correct the defined uptake label as a convention; do not turn this bounded response into acceptance of a governance prescription.'
    if fid=='A035':
        cat='criterion_ambiguity';diagnosis='criterion_ambiguity';effect='unresolved'
        note='Both reviewers preserve the reported rebase and the unverified #26589 condition. A report can correspond to the action without verifying the complete qualified request. The target convention is unresolved; an unqualified fulfillment claim is not adopted.'
    add('Q'+fid[1:],refs,cat,diagnosis,effect,note,selection=selection,qualification=qual)

add('Q008a',['A008'],'convention_deviation','execution_failure','convention_only',selection={'R13':['U20'],'R16':['F03-U13']},title='Replacement-word proposal presentation')
add('Q008b',['A008'],'convention_deviation','execution_failure','convention_only',selection={'R13':['U23'],'R16':['F03-U16']},title='Conditional spelling proposal presentation')
add('Q025a',['A025'],'defensible_alternative','defensible_alternative','convention_only',
 'R10 chooses a synonymous reconstructed restraint predicate and consistently marks its action/object roles inferred. The negative recommendation, tentative reason, and release-test scope survive. A preferred literal representation does not make this alternative a source error.',
 'Preserve the reconstructed alternative or adopt the simpler literal form without treating either as a different institutional conclusion.',
 {'R10':['U23']},'Reconstructed avoid-rushing alternative')
add('Q030a',['A030'],'convention_deviation','execution_failure','convention_only',selection={'R03':['Q02'],'R04':['Q02']},title='Repeated technical-description speech-act consistency')
add('Q030b',['A030'],'convention_deviation','execution_failure','convention_only',
 'R04 assigns different speech-act categories to the original criterion and its repeat. Treat this as a cross-occurrence consistency issue. The original record is not automatically the correct one: the source uses an assertion to advance a recommendation.',
 'Harmonize the original and quoted occurrence under the chosen source-based speech-act convention, retaining the asserted-versus-proposed boundary if unresolved. Do not infer a new endorsement from quotation.',
 {'R04':['Q09']},'Repeated selection-criterion speech-act consistency',
 'Repair may concern the original S26 as well as the repeated Q09; do not mechanically copy a potentially debatable original label.')
add('Q030c',['A030'],'convention_deviation','execution_failure','convention_only',selection={'R04':['Q12']},title='Repeated navigation-proposal speech-act consistency')
add('Q041',['A041'],'criterion_ambiguity','criterion_ambiguity','unresolved',
 'Whether same_actor_only summarizes any maintained personal method or only an expectation-related event remains unclear. This profile ambiguity is distinct from P03’s overly narrow full-proposition restatement target.',
 'Record the same-actor method response explicitly, retain the none/same_actor_only profile alternative as needed, and do not infer interpersonal support.',title='Same-actor profile convention for partial method repetition')
add('Q051',['B009'],'defensible_alternative','defensible_alternative','convention_only',
 'An operational instruction and a proposal to select a recurring testing arrangement occupy different analytical layers. Retain the layer and uncertainty about adoption; the label difference alone does not reverse the historical account.',title='Operational versus collective-choice focal layer')
add('Q052',['B012'],'defensible_alternative','defensible_alternative','unresolved',
 'The fee-only question can challenge continuation of a design without contradicting the past attempt. Preserve that prospective alternative and the uncontested historical report, without inferring withdrawal or adoption.',title='Prospective self-questioning versus dispute of a historical work report')

mapping={fid:[g['group_id'] for g in groups if fid in g['review_finding_refs']] for fid in findings}
assert all(mapping.values()) and len(groups)==59
for g in groups:
    for a in g['affected']:
        us={u['unit_id'] for u in annotations[a['annotation_id']]['units']}
        assert set(a['unit_ids'])<=us
bycase={}
for case in ['F01','F02','F03']:
    bycase[case]={}
    for condition in ['v03','v04']:
        primary=[g for g in groups if g['episode_id']==case and g['category']=='primary_error' and any(a['condition']==condition for a in g['affected'])]
        bycase[case][condition]={'primary_error_groups':len(primary),'interpretation_changing':sum(g['effect']=='interpretation_changing' for g in primary),'evidence_basis':sum(g['effect']=='evidence_basis' for g in primary),'coverage_or_scope':sum(g['effect']=='coverage_or_scope' for g in primary),'group_ids':[g['group_id'] for g in primary],'run_group_incidences':sum(sum(a['condition']==condition for a in g['affected']) for g in primary),'affected_runs':sorted({a['run_id'] for g in primary for a in g['affected'] if a['condition']==condition})}
status={'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'independent_reviews':['source_review_a','source_review_b'],'review_counts':{'A':50,'B':12},'grouping_rule':'Distinct focal proposition or relationship / error issue / case. Repeated runs do not create new error groups. Findings can map to multiple groups when they combine distinct propositions or effects.','scope':'Coordinator reconciliation after frozen independent submissions, not original-coder deliberation; no annotation changed.','coordinator_access':'Coordinator read all focal source entries, the assigned-rule passages, all 62 review findings, and targeted full records/projections for primary and convention findings. Reviewers supplied the complete all-record audits; coordinator did not claim a third blind full-corpus coding pass.','reconciliation_is_reference_truth':False,'groups':groups,'finding_to_groups':mapping,'category_counts':dict(collections.Counter(g['category'] for g in groups)),'primary_by_case_and_condition':bycase,'sensitivity':{'base':{'v03_evidence_groups':1,'v04_evidence_groups':4},'classify_P03_and_P04_as_convention_instead':{'v03_evidence_groups':1,'v04_evidence_groups':2},'add_Q024_R10_action_basis_as_evidence_error':{'v03_evidence_groups':1,'v04_evidence_groups':5},'interpretation':'These reasonable effect-boundary alternatives do not yield evidence of fewer evidence-basis groups under 0.4 in this sample. They do not justify a population ranking or accuracy rate.'},'limits':['All judgments remain revisable and share an AI provider context.','Different schemas create different opportunities to expose or commit errors; this is a whole-workflow comparison.','No identified interpretation-changing error or material extraction/qualifier omission is not proof that none exists.','No raw annotation, alignment, agreement score, or tested criterion was repaired or redefined through reconciliation.']}
write(R/'analysis/reconciliation.json',status)
print(json.dumps({'groups':len(groups),'categories':status['category_counts'],'primary':bycase},indent=2))
