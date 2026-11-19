import json, hashlib, copy
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
packet_bytes = (ROOT/'packet.json').read_bytes()
packet = json.loads(packet_bytes)
entries = {e['source_id']:e for e in packet['entries']}
texts = {k:v['text'] for k,v in entries.items()}
def sid(short): return 'pr14441:'+short
def sp(source, quote=None, start_at=0):
    text = texts[source]
    if quote is None: quote = text
    start = text.index(quote, start_at)
    return {'start':start,'end':start+len(quote),'quote':quote}
def ev(source, quote=None, start_at=0): return {'source_id':source,'span':sp(source,quote,start_at)}
def e(short, quote=None, start_at=0): return ev(sid(short),quote,start_at)
def comp(symbol,text,basis,evidence,role='local',note=''):
    return {'symbol':symbol,'text':text,'basis':basis,'evidence':evidence,'inference_note':note,'occurrence_role':role}
def event(kind,target,basis,evidence,rationale):
    return {'kind':kind,'target':target,'basis':basis,'evidence':evidence,'rationale':rationale}
units=[]
def context(uid,short,speech='reported_action',quote=None,rationale='',alternative='',confidence='clear'):
    u={'unit_id':uid,'source_id':sid(short),'span':sp(sid(short),quote),'parent_unit_id':None,
       'grammar':'not_institutional','speech_act':speech,'scope':'case_specific','components':[],
       'institution':{'type':'not_applicable','standing':'not_applicable','dispute_present':False,
                      'rationale':rationale,'evidence':[e(short,quote)],'recognition':[],'authority_evidence':[]},
       'statement_target_level':'not_applicable','observed_action_level':'operational',
       'level_rationale':'This is a visible contribution/review act in PR #14441, not a new prescription about recurring governance arrangements.',
       'complexity_flags':['none'],'alternative_interpretation':alternative,'confidence':confidence,
       'uncertainty_reason':'' if confidence=='clear' else alternative,'record_role':'context','parse_mode':'literal',
       'deontic_force':'nondeontic','level_alternatives':[],
       'presentation':{'quotation':'none','markup':'plain','rationale':'Retained plain prose; inline code or a URL does not constitute a code block or repeated quotation.'},
       'disposition_events':[]}
    units.append(u);return u

merge_evidence=[e('metadata','"merged_at": "2018-11-10T11:46:02+00:00"'),e('metadata','"merged": true'),e('supplement_metadata','"base": "0.17"'),e('supplement_metadata','"merge_commit_sha": "89306ab0df93bfdf5630910bc20b1eccb7379172"')]
broad_update=[e('comments:0')]
revision_ack=[e('reviews:4')]
def statement(uid,short,quote,parse,components,alternative,uncertainty,presentation=None):
    u={'unit_id':uid,'source_id':sid(short),'span':sp(sid(short),quote),'parent_unit_id':None,
       'grammar':'regulative','speech_act':'proposed','scope':'case_specific','components':components,
       'institution':{'type':'undetermined','standing':'text_only','dispute_present':False,
       'rationale':'The focal proposition is a case-specific review recommendation to edit this contribution. It is institutionally plausible as contribution coordination, but the supplied text does not establish a recurring social expectation, an attributable authorization, a recognized rule-making procedure, or enforcement. A one-off technical/editorial suggestion is therefore undetermined rather than a rule, norm, or personal strategy. Later technical assent and implementation reports are not expectation recognition.',
       'evidence':[e(short,quote)],
       'recognition':[
           event('reported_implementation','broader_proposal','explicit',broad_update,'The PR author jnewbery attributes the PR update to @ryanofsky\'s changes. This is an aggregate participant report, not verification of this individual recommendation or its exact wording.'),
           event('endorsement','broader_proposal','explicit',revision_ack,'ryanofsky utACKs revision 89306ab0df93bfdf5630910bc20b1eccb7379172 and describes the revision as code simplification and release-note updates. The endorsement targets the contribution/revision, not an institutional expectation.'),
           event('recorded_status','broader_proposal','explicit',merge_evidence,'Supplied metadata records the contribution as merged into base 0.17. This does not establish proposition-specific adoption, enforcement, or Bitcoin-network adoption.')],
       'authority_evidence':[]},
       'statement_target_level':'operational','observed_action_level':'operational',
       'level_rationale':'The focal action is an immediate edit to the code or release notes in PR #14441. Reviewing and revising this contribution applies ordinary contribution arrangements; no recurring operational arrangement or allocation of governance powers is being chosen.',
       'complexity_flags':['none'],'alternative_interpretation':alternative,'confidence':'plausible','uncertainty_reason':uncertainty,
       'record_role':'statement','parse_mode':parse,'deontic_force':'recommendation','level_alternatives':[],
       'presentation':presentation or {'quotation':'none','markup':'plain','rationale':'Plain prose recommendation with inline code, not a quotation or a code block.'},
       'disposition_events':[
          event('reported_implemented','broader_proposal','explicit',broad_update,'The author reports incorporating the reviewer\'s changes at PR scope; exact implementation of this proposition is not individually established by that aggregate report.'),
          event('recorded_merged','broader_proposal','explicit',merge_evidence,'The recorded merge is a disposition of PR #14441; it is not a claim that every suggestion was adopted verbatim.')]
       }
    units.append(u);return u

context('F02-C01','body','technical_description',rationale='Describes the submitted backport, partial reverts, and referenced issue. It supplies provenance and purpose, without a separately articulated prescription, permission, recurring strategy, or institutional definition.',alternative='Submitting a PR can pragmatically invite review or integration, but this retained body does not independently articulate such a request; no unstated permission or obligation is extracted.')
context('F02-C02','comments:0',rationale='An attributable report of updating this PR in response to the reviewer; it is response/implementation context, not an independently stated prescription.')
context('F02-C03','comments:1',rationale='An ACK of the supplied abbreviated revision 89306ab. It is contribution endorsement, not a new prescription or evidence of authority.',alternative='The abbreviation matches the prefix of the retained head, but the source token is preserved without silently replacing it with the full hash. No testing claim is inferred from the abbreviation utACK.')
context('F02-C04','comments:2',rationale='An ACK of an explicitly linked revision accompanied by a technical comparison of the backport code and tests. The comparison does not prescribe a general backport procedure.',alternative='The explanation may justify this particular variation from other backports; it does not establish a recurring exception rule or a reviewer\'s authority.')
context('F02-C05','reviews:0',rationale='An ACK of c8d1f1513fb39d80cebbc32e1b5327209485e085 and a visible review act. APPROVED metadata does not itself establish a governing duty, a gate, or an actor\'s authority.')
context('F02-C06','reviews:4',rationale='A later ACK of a different full revision, with a description of changes since the reviewer\'s last review. This is review/update evidence, not a requirement to renew approvals.',alternative='The observed second review could fit many review practices. It does not demonstrate mandatory reapproval, changed judgment, or a rule for integration.')

q0=texts[sid('review_comments:0')]
s0=statement('F02-S01','review_comments:0',q0,'pragmatic',[
    comp('A','PR contributor addressed by the correction (jnewbery inferred)','context_inferred',broad_update,'context_reference','The imperative-like correction supplies no named editing actor. The source attribution of the later report is jnewbery, who reports updating the PR with @ryanofsky\'s changes; this supports, but does not make explicit, the addressee. The outside-unit reference is used only to resolve the contribution participant, not maintainer status.'),
    comp('D','Should','explicit',[e('review_comments:0','Should')],note='Should explicitly expresses the advised corrected form in the elliptical spelling correction; it is advisory rather than a claim of institutional authority.'),
    comp('I','write','context_inferred',[e('review_comments:0')],'semantic_inference','The literal predicate is be. The review context and supplied desired identifier support reconstructing a request to write the identifier correctly; write is not explicitly present.'),
    comp('Bdir','`listtransactions` with `s`','context_inferred',[e('review_comments:0','`listtransactions` with `s`')],'semantic_inference','The literal complement of be becomes the target/output of the reconstructed writing action. Presence of the identifier does not make that transformed Bdir role explicit. The complete identifier and the final-s qualifier are preserved.')
],
'Literal alternative: an assertion about the correct technical spelling of the RPC name, with no independently binding institutional expectation. The canonical analysis retains its pragmatic editorial recommendation. The implicit editing addressee could be any contributor making the correction rather than exclusively the PR author.',
'The editing action and its actor/object roles require pragmatic reconstruction. The file path identifies release notes, but no precise original line or reliable reply threading is supplied.')
s0['level_rationale']='The focal action is correcting an RPC identifier in this PR\'s release notes (source path doc/release-notes.md). It governs an immediate contribution edit, not the definition of an institutional object or a new documentation policy.'

full1=texts[sid('review_comments:1')]
q1=full1[full1.index("I'd maybe"):]
start1=full1.index(q1)
replacement1=full1[full1.index('to:\r\n\r\n>'):]
s1=statement('F02-S02','review_comments:1',q1,'pragmatic',[
    comp('A','PR contributor addressed by the replacement suggestion (jnewbery inferred)','context_inferred',[e('review_comments:1',"I'd maybe change it to:"),*broad_update],'semantic_inference','The explicit I in I\'d belongs to ryanofsky\'s hypothetical formulation, not literally to the contributor being advised. Reading this as an editorial recommendation to the PR contributor transforms the actor role. The later outside-unit update report, attributed to jnewbery, supports the addressee inference without turning it into an explicit actor.'),
    comp('I','change','explicit',[e('review_comments:1','change',start1)],note='Change is explicitly supplied; only the suggested addressee/force is pragmatically reconstructed.'),
    comp('Bdir','it','explicit',[e('review_comments:1','it',full1.index('change it')+len('change '))],note='It is already the direct object of change in the hypothetical source wording and remains the direct object of the same action in the pragmatic recommendation. Its referent is separately resolved from the preceding sentence.'),
    comp('Bdir,p','the paragraph about both behaviors in the same release','context_inferred',[e('review_comments:1',"This paragraph doesn't really make sense when both behaviors are present in the same release.")],'context_reference','The preceding sentence, outside the minimal edit-proposition span, resolves it as this paragraph and supplies the reason for replacing it. Both behaviors in the same release describes the paragraph\'s subject; it is not an activation condition for making the edit.'),
    comp('Cex',replacement1,'explicit',[e('review_comments:1',replacement1)],note='The full to-complement gives proposed replacement wording. Its with/without -deprecatedrpc=accounts distinctions and the account-versus-label rationale are preserved as the content of the edit, not recoded as institutional permissions or activation conditions on contributors.')
],
'A literal reading describes what ryanofsky would perhaps change rather than directing jnewbery; the wording is a tentative editorial suggestion rather than an explicit personal commitment. The replacement itself is technical documentation, not a constitutive definition of institutional roles. I\'d and maybe do not supply an obligatory D.',
'The addressee and recommendation force are inferred; the action and direct-object role are explicit. No old paragraph text or reliable reply threading is supplied. The exact replacement is proposed wording, not evidence of adoption.',
{'quotation':'proposed_wording','markup':'mixed','rationale':'The unit combines a prose edit suggestion with newly offered blockquoted replacement text. The blockquote is drafted wording, not a repeated occurrence or an external authority.'})
s1['complexity_flags']=['nested_component']

full2=texts[sid('review_comments:2')]
q2=full2[full2.index('Maybe drop'):]
s2=statement('F02-S03','review_comments:2',q2,'literal',[
    comp('A','PR contributor addressed by the suggestion (jnewbery inferred)','context_inferred',[e('review_comments:6',"I've removed it.")],'context_reference','The instruction has an implicit addressee. The matching later removal report is attributed to jnewbery; the outside-unit reference supports that addressee while leaving actor role inferred and status unspecified.'),
    comp('I','drop','explicit',[e('review_comments:2','drop')]),
    comp('Bdir','the new check for "*" here','context_inferred',[e('review_comments:2','the new check for "*" here')],'context_reference','Drop omits its object in this clause. The preceding sentence outside the unit supplies the unique local antecedent, the new check for "*" here. The earlier subject is assigned an inferred object role under drop; its words being explicit does not make that role explicit.'),
    comp('Cex','for clarity','explicit',[e('review_comments:2','for clarity')]),
    comp('Cac',"unless I'm missing something",'explicit',[e('review_comments:2',"unless I'm missing something")],note='The reviewer makes the suggestion conditional on not overlooking relevant behavior. This epistemic reservation limits applicability of the recommendation; it is not evidence of higher-level epistemic governance.')
],
'The comment can be read as optional code-quality advice with no institutional expectation. The unless-clause could alternatively be represented as an execution/communicative qualification rather than Cac, provided its reservation is preserved. Maybe expresses tentativeness and does not establish a lexical duty.',
'The object is elliptical and resolved from the preceding sentence; the actor is inferred from the later matching response. No complete revision history verifies the moment of removal.')
s2['institution']['evidence'].append(e('review_comments:2',"I don't see how the new check for \"*\" here changes anything."))
s2['institution']['recognition'][:0]=[
    event('response','this_proposition','context_inferred',[e('review_comments:2'),e('review_comments:6')],'The later answer uniquely repeats the check for "*", agrees that behavior is identical, and reports removing it. Textual correspondence supports the target despite missing reliable reply threading.'),
    event('endorsement','this_proposition','context_inferred',[e('review_comments:2'),e('review_comments:6',"No, you're right. It's better without.")],'The author agrees with this technical simplification. That is technical assent, not recognition of a binding or socially shared expectation.'),
    event('reported_implementation','this_proposition','context_inferred',[e('review_comments:2'),e('review_comments:6')],'The author\'s I\'ve removed it follows an explicit identification of the check for "*". The report specifically corresponds to the removal recommendation; it remains a participant report.')]
s2['disposition_events'][:0]=[
    event('accepted','this_proposition','context_inferred',[e('review_comments:2'),e('review_comments:6')],'The author\'s agreement and matching removal report support acceptance of this particular technical recommendation.'),
    event('reported_implemented','this_proposition','context_inferred',[e('review_comments:2'),e('review_comments:6')],'The named-check correspondence supports a proposition-specific removal report, without claiming an independently reconstructed patch chronology.')]

full3=texts[sid('review_comments:3')]
proposal3=full3[full3.index('Maybe:'):]
s3=statement('F02-S04','review_comments:3',full3,'pragmatic',[
    comp('A','PR contributor addressed by the documentation suggestion (jnewbery inferred)','context_inferred',[e('review_comments:3',"I think it'd be good to document the empty string change."),*broad_update],'semantic_inference','I is the subject of think, not the explicit actor of document. The recommendation reading supplies an editing addressee; the outside-unit report attributed to jnewbery supports that inference without claiming the source explicitly names the documenting actor.'),
    comp('I','document','explicit',[e('review_comments:3','document')],note='The documenting action is explicitly supplied even though the recommendation force is inferred from the appraisal.'),
    comp('Bdir','the empty string change','explicit',[e('review_comments:3','the empty string change')],note='This phrase is the direct object of document in the literal appraisal and remains the direct object of that same verb under the pragmatic recommendation. Its object role has not been transformed.'),
    comp('Cex',proposal3,'explicit',[e('review_comments:3',proposal3)],note='Maybe introduces optional offered wording for documenting the change. The complete draft preserves backwards compatibility, the setting-dependent empty-string behavior, and the usefulness/confusion rationale as edit content; these are not institutional sanctions or authorizations.')
],
'Literal alternative: a positive appraisal of documenting the change, plus a draft technical explanation, rather than a binding directive. The canonical reading is a tentative editorial recommendation. Capability and error statements inside the draft concern software behavior, not permission or sanctions.',
'The addressee and recommendation force are inferred. The supplied draft is one proposed way to document the change; its wording is not required, and aggregate later uptake cannot establish exact adoption.',
{'quotation':'proposed_wording','markup':'mixed','rationale':'The prose recommendation introduces a newly written blockquoted explanation. It is proposed wording rather than an external or repeated quotation.'})
s3['complexity_flags']=['nested_component']

context('F02-C07','review_comments:4',rationale='An endorsement/response stating Both are good changes. This is not an independent prescription. The text and release-notes file path do not identify which two suggestions are endorsed.',alternative='The two substantive documentation proposals are a plausible pair, but the identifier correction is also on this file. Reliable thread links are absent, so no proposition-specific recognition or acceptance is assigned.',confidence='unresolved')
context('F02-C08','review_comments:5',rationale='A terse participant report fixed, not a new prescription. Its target is not named in the supplied text.',alternative='It might report fixing the identifier spelling, the behavior paragraph, or the empty-string documentation. Array adjacency and a shared file path do not resolve the target.',confidence='unresolved')
context('F02-C09','review_comments:6',rationale='An attributable response and report that the check for "*" was removed, with agreement about unchanged behavior. It is implementation/technical context rather than a new directive.',alternative='The report supports the particular removal suggestion by textual correspondence, but no complete edit history independently establishes timing or causal necessity.')

relations=[]
def rel(a,b,typ,basis,evidence,rationale,scope='not_applicable'):
    relations.append({'from_unit_id':a,'to_unit_id':b,'type':typ,'basis':basis,'rationale':rationale,'evidence':evidence,'logic_scope':scope})
for stmt,short in [('F02-S01','review_comments:0'),('F02-S02','review_comments:1'),('F02-S03','review_comments:2'),('F02-S04','review_comments:3')]:
    rel(stmt,'F02-C02','uptake','context_inferred',[e(short),e('comments:0')],
        'The initiating recommendation is by ryanofsky, whom the author thanks by handle while reporting a PR update with your changes. This links the recommendation to an aggregate response; it does not verify this proposition\'s exact implementation or establish an expectation. The relation direction is proposal to response.')
rel('F02-S03','F02-C09','uptake','context_inferred',[e('review_comments:2'),e('review_comments:6')],
    'The request to drop the new check for "*" is followed by a response specifically agreeing about that check and reporting its removal. Missing reliable thread linkage prevents calling the mapping explicit; lexical correspondence supports the attribution.')
rel('F02-C06','F02-C05','review_target_update','context_inferred',[e('reviews:0'),e('reviews:4')],
    'The same reviewer later ACKs 89306ab0df93bfdf5630910bc20b1eccb7379172 and refers to changes since last review; the supplied earlier review ACKs c8d1f1513fb39d80cebbc32e1b5327209485e085. The mapping to that prior review is contextual, not a direct quotation of its identifier. Direction is later review to earlier review; no changed judgment or mandatory reapproval is inferred.')

reasons={
'body':'Focal entry screened exhaustively. Descriptive contribution provenance, partial-revert references, and fix attribution; no separately articulated institutional directive or strategy.',
'comments:0':'Focal entry screened exhaustively. Aggregate participant implementation report and thanks, retained as response context; no separate institutional prescription.',
'comments:1':'Focal entry screened exhaustively. ACK of a supplied abbreviated commit, retained as endorsement context; no duty, permission, or authority claim.',
'comments:2':'Focal entry screened exhaustively. ACK plus explanation of this backport\'s code/test differences. Does not prescribe a recurring backport arrangement.',
'reviews:0':'Focal entry screened exhaustively. Broad revision ACK; approval state is review context and does not establish governing authority.',
'reviews:1':'Empty focal review body; review-state metadata does not supply a proposition.',
'reviews:2':'Empty focal review body; review-state metadata does not supply a proposition.',
'reviews:3':'Empty focal review body; review-state metadata does not supply a proposition.',
'reviews:4':'Focal entry screened exhaustively. Later ACK and comparison to prior review; a reported review act, not a reapproval rule.',
'review_comments:0':'Focal entry screened exhaustively. Elliptical spelling correction is a plausible editorial recommendation; literal technical alternative retained.',
'review_comments:1':'Focal entry screened exhaustively. One recommendation to replace a paragraph, with complete proposed wording retained. The preceding technical rationale and embedded software behaviors do not add independent institutional propositions.',
'review_comments:2':'Focal entry screened exhaustively. One optional removal recommendation preserving object, clarity purpose, and unless reservation; preceding reasoning resolves the omitted object.',
'review_comments:3':'Focal entry screened exhaustively. One request to document empty-string behavior, with optional proposed wording. The software capability/error descriptions are technical edit content, not institutional permissions or sanctions.',
'review_comments:4':'Focal entry screened exhaustively. Technical assent to two unnamed changes; exact targets unresolved, no independently stated expectation.',
'review_comments:5':'Focal entry screened exhaustively. Terse implementation report with unresolved target, not an independent directive.',
'review_comments:6':'Focal entry screened exhaustively. Technical agreement and a specific removal report, retained as an uptake endpoint; no new independent prescription.',
'metadata':'Supplement screened as context per selection design. Recorded PR status and file summary support outcome claims, not exhaustive institutional extraction. No claim that metadata could never bear institutional content.',
'supplement_metadata':'Supplement screened as context per selection design. Provides recorded base/head/merge identity and status, not complete history. Context-only treatment is a scope decision, not a finding of institutional absence.',
'patch:0':'Supplement screened as context per selection design. Retained release-note wording supports bounded content/outcome comparison. Not an exhaustive extraction target or proof of review causation; context-only does not assert institutional absence.',
'patch:1':'Supplement screened as context per selection design. Retained RPC implementation/help changes support technical context. Embedded must/should language concerns software input behavior in this supplied patch; no exhaustive institutional extraction is claimed.',
'patch:2':'Supplement screened as context per selection design. Retained functional-test changes are technical context, not a complete test-execution record or exhaustive institutional extraction target.',
'patch:3':'Supplement screened as context per selection design. Retained label-filtering test changes are technical context; no test-pass claim or exhaustive institutional-absence finding is made.'}
screens=[]
for entry in packet['entries']:
    found=[u for u in units if u['source_id']==entry['source_id']]
    disposition='candidate' if any(u['record_role']=='statement' for u in found) else ('empty' if not entry['text'].strip() else 'context_only')
    screens.append({'source_id':entry['source_id'],'disposition':disposition,'reason':reasons[entry['source_id'].split(':',1)[1]],'unit_ids':[u['unit_id'] for u in found]})

summary={
'observed_outcomes':[
    {'claim':'PR #14441 is recorded as merged on 2018-11-10 at 11:46:02 UTC; the supplied supplement gives base 0.17 and merge_commit_sha 89306ab0df93bfdf5630910bc20b1eccb7379172. This is repository integration of the contribution, not evidence of Bitcoin-network adoption or a governance rule.', 'evidence':merge_evidence},
    {'claim':'jnewbery reports updating the PR with @ryanofsky\'s changes. ryanofsky subsequently utACKs revision 89306ab0df93bfdf5630910bc20b1eccb7379172 and says that only code simplification and release-note updates changed since the last review. These are attributed reports and revision endorsement, not proposition-specific expectation recognition.', 'evidence':[e('comments:0'),e('reviews:4')]},
    {'claim':'After the recommendation to drop the new check for "*" for clarity, subject to the reviewer\'s unless reservation, jnewbery agrees that behavior would be identical and reports removing that check. The matched content supports specific reported uptake; actual edit chronology and causal necessity are not independently reconstructed.', 'evidence':[e('review_comments:2'),e('review_comments:6')]},
    {'claim':'The retained release-notes patch spells listtransactions and describes both the with/without -deprecatedrpc=accounts transaction distinctions and the setting-dependent empty-string behavior raised in review. Its wording is substantively corresponding rather than a verbatim copy of every proposed phrase, and the retained head patch does not establish which review caused an edit.', 'evidence':[e('review_comments:0'),e('review_comments:1'),e('review_comments:3'),e('patch:0')]},
    {'claim':'The author also writes Both are good changes and fixed in release-note comments. The supplied text does not resolve which two changes or which fix these terse responses target; they are not assigned as proposition-specific acceptance.', 'evidence':[e('review_comments:4'),e('review_comments:5')]}
],
'mechanisms':[
    {'category':'reason_giving','claim':'ryanofsky explains that the new check for "*" appears behaviorally redundant and recommends dropping it for clarity unless something is being missed. jnewbery answers that behavior is identical and reports removal. This is a supported request-and-reasoned-response sequence at the operational contribution level; the reported removal is the bounded outcome.',
     'evidence':[e('review_comments:2'),e('review_comments:6')],'unit_ids':['F02-S03','F02-C09'],
     'alternative_explanation':'The author may also have independently noticed the redundant check. The packet lacks complete patch chronology and reliable thread links, so this sequence does not identify a causal effect of review or demonstrate enforcement.','status':'supported_sequence'},
    {'category':'review_coordination','claim':'The reviewer supplies an identifier correction, proposed behavior documentation, a conditional code-simplification suggestion, and an empty-string documentation suggestion. The author reports updating the PR with that reviewer\'s changes; the reviewer then ACKs a later full revision and characterizes the intervening changes as code simplification and release-note updates. This supports contribution-level review coordination and an aggregate reported revision, without resolving every individual response target or demonstrating mandatory reapproval.',
     'evidence':[e('review_comments:0'),e('review_comments:1'),e('review_comments:2'),e('review_comments:3'),e('comments:0'),e('reviews:0'),e('reviews:4')],
     'unit_ids':['F02-S01','F02-S02','F02-S03','F02-S04','F02-C02','F02-C05','F02-C06'],
     'alternative_explanation':'The contribution could have been revised and reviewed through ordinary voluntary practice. The broad report and ACK do not verify all wording, explain the final integration decision, or establish a recognized duty.','status':'supported_sequence'}
],
'missing_evidence':[
'No complete edit history or reliable reply threading; the targets of Both are good changes and fixed remain unresolved.',
'No complete prior revision patches or original release-note paragraph; retained head patches do not identify exact edit timing or causation.',
'No supplied authorization provision, recurring expectation recognition, enforcement claim, or sanction sequence supporting rule or shared-norm classification.',
'No evidence of collective-choice, constitutional, or epistemic governance activity in the focal recommendations; technical documentation conditions do not supply those levels.',
'No outcomes for referenced PRs #13075, #14023, #14382, or #14411 are inferred from their mention; no test-execution or Bitcoin-network adoption evidence is supplied.'
],
'unresolved_questions':[
'Which two documentation changes does Both are good changes endorse, and which edit does fixed report?',
'How precisely did the retained revisions implement each proposed wording change, and what caused the final merge? The aggregate report and retained patches do not resolve that chronology.',
'Do any of these case-specific review practices reflect a broader recognized institutional expectation? This packet provides no sufficient recognition or authority evidence.'
]}
annotation={'schema_version':'0.3','run_id':'F02_v03_r1','episode_id':'F02','packet_sha256':hashlib.sha256(packet_bytes).hexdigest(),'entry_screening':screens,'units':units,'relations':relations,'episode_summary':summary}
encoded=json.dumps(annotation,ensure_ascii=False,indent=2)+'\n'
(ROOT/'annotation.json').write_text(encoded)
(ROOT/'annotation.first_complete.json').write_text(encoded)
(ROOT/'first_complete_freeze.json').write_text(json.dumps({'run_id':'F02_v03_r1','frozen_at_utc':datetime.now(timezone.utc).isoformat(),'annotation_first_complete_sha256':hashlib.sha256(encoded.encode()).hexdigest(),'packet_sha256':annotation['packet_sha256'],'before_checker':True,'before_source_self_review':True},indent=2)+'\n')
print(json.dumps({'screened_entries':len(screens),'units':len(units),'statements':sum(u['record_role']=='statement' for u in units),'relations':len(relations),'first_complete_frozen':True}))
