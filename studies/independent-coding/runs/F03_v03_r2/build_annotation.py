import json, hashlib, copy
from pathlib import Path
ROOT = Path(__file__).resolve().parent
packet = json.loads((ROOT/'packet.json').read_text())
entries = {e['source_id']:e for e in packet['entries']}
BODY='pr7819:body'
C=lambda n:f'pr7819:comments:{n}'
META='pr7819:metadata'
SMETA='pr7819:supplement_metadata'
M8182='pr8182:supplement_metadata'
def span(sid, quote, start=0):
    s=entries[sid]['text'].index(quote,start)
    return {'start':s,'end':s+len(quote),'quote':quote}
def ev(sid,quote,start=0): return {'source_id':sid,'span':span(sid,quote,start)}
def full(sid): return ev(sid,entries[sid]['text'])
def comp(symbol,text,sid,quote,basis='explicit',role='local',note='',start=0,extra=None):
    return {'symbol':symbol,'text':text,'basis':basis,'evidence':[ev(sid,quote,start)]+(extra or []),'inference_note':note,'occurrence_role':role}
units=[]
def unit(uid,sid,quote,role='statement',speech='proposed',parse='literal',force='recommendation',itype='undetermined',standing='text_only',rationale='',components=None,parent=None,alternative='',uncertainty='',confidence='plausible',scope='case_specific',markup='plain',quotation='none',presnote='',levelnote='',flags=None):
    nonstatement=role!='statement'
    u={'unit_id':uid,'source_id':sid,'span':span(sid,quote),'parent_unit_id':parent,
       'grammar':'not_institutional' if nonstatement else 'regulative','speech_act':speech,'scope':scope,'components':components or [],
       'institution':{'type':'not_applicable' if nonstatement else itype,'standing':'not_applicable' if nonstatement else standing,'dispute_present':False,'rationale':rationale,'evidence':[ev(sid,quote)],'recognition':[],'authority_evidence':[]},
       'statement_target_level':'not_applicable' if nonstatement else 'operational',
       'observed_action_level':'not_applicable' if role=='container' else 'operational',
       'level_rationale':levelnote or ('The visible act is ordinary contribution review or technical development; this record adds no governed activity.' if nonstatement else 'The focal action concerns the design, review, or maintenance of this contribution. No recurring decision procedure or allocation of governance authority is proposed.'),
       'complexity_flags':flags or ['none'],'alternative_interpretation':alternative,'confidence':confidence,'uncertainty_reason':uncertainty,
       'record_role':role,'parse_mode':parse,'deontic_force':'nondeontic' if nonstatement else force,'level_alternatives':[],
       'presentation':{'quotation':quotation,'markup':markup,'rationale':presnote or 'Plain supplied prose; no disposition or edit history is inferred from its appearance.'},'disposition_events':[]}
    units.append(u)
    return u

def rec(u,kind,target,evidence,rationale,basis='explicit'):
    u['institution']['recognition'].append({'kind':kind,'target':target,'evidence':evidence,'rationale':rationale,'basis':basis})
def disp(u,kind,target,evidence,rationale,basis='explicit'):
    u['disposition_events'].append({'kind':kind,'target':target,'basis':basis,'evidence':evidence,'rationale':rationale})

q01='Adds a checkbox to the Send-Coins-Pannel (next to "Add Recipient") that allows to set the according nSequence to signal BIP125 RBF.\n\nThis PR does not include a way to actually replace a transaction with the GUI.'
u01=unit('U01',BODY,q01,role='context',speech='technical_description',rationale='The body describes the proposed feature and its missing replacement workflow. It is a technical contribution description, retained as the target of exposure concerns; it does not define institutional permission through technical allows.',confidence='clear',levelnote='Describing the scope of a particular proposed contribution is operational activity. No institutional rule is extracted from the checkbox capability.')
q02="So not sure if we want this without a GUI based replacement workflow (which I'm working on but it is a bigger chunk)."
u02=unit('U02',BODY,q02,speech='asserted',parse='pragmatic',force='unresolved',rationale='A tentative reservation about including the feature before a usable workflow is retained as a candidate constraint on this contribution. The sentence expresses uncertainty, not an authorized integration rule.',components=[
 comp('A','we',BODY,'we','context_inferred','semantic_inference','The source supplies the collective experiencing the preference; its role as decision makers deferring inclusion is inferred, with membership and authority unspecified.'),
 comp('I','consider deferring inclusion',BODY,'not sure if we want this','context_inferred','semantic_inference','The action is reconstructed from an uncertain preference about wanting this feature under the stated condition; it is not a definite refusal.'),
 comp('Bdir','this (the checkbox contribution)',BODY,'this',basis='context_inferred',role='semantic_inference',note='The literal object of want becomes the target of the inferred inclusion decision; U01 supplies the feature antecedent.',start=span(BODY,q02)['start'],extra=[ev(BODY,q01)]),
 comp('Cac','without a GUI based replacement workflow',BODY,'without a GUI based replacement workflow',note='The absence of the workflow qualifies the expressed reservation and the inferred inclusion decision.'),
],alternative='This can remain a literal statement of uncertainty about technical usefulness, with no request to defer. The parenthetical reports ongoing work and its size, not a promised deadline or a separate prescription.',uncertainty='No definitive selection decision, audience authority, or obligation follows from not sure if we want.',levelnote='The focal candidate is a decision about proceeding with this particular contribution without its companion workflow, an operational integration question. It does not propose a recurring integration procedure.')
q03="But I don't want to hold back review of this PR."
u03=unit('U03',BODY,q03,speech='asserted',parse='pragmatic',force='nondeontic',itype='strategy_candidate',rationale='The author expresses a personal approach of not delaying review while the larger GUI workflow remains under development. This supports a tentative case-specific strategy, not an obligation on reviewers.',components=[
 comp('A','I',BODY,'I',note='The first-person subject remains the agent of not holding back; attribution is to the supplied body author, not an inferred maintainer.',start=span(BODY,q03)['start']),
 comp('I','not hold back',BODY,"don't want to hold back",'context_inferred','semantic_inference','Negative desire is normalized to the intended action, preserving the negation. It is weaker than a firm promise that review will proceed.'),
 comp('Bdir','review of this PR',BODY,'review of this PR',note='The explicit object of hold back remains its patient under the inferred negative intention.'),
],alternative='A literal expression of preference need not be an adopted personal strategy. Pragmatically it can invite reviewers to proceed; no reviewer is explicitly directed or compelled.',uncertainty='The sentence states desire, not a completed review, a binding commitment, or authorized permission.',levelnote='The focal activity is the timing of review of this PR, operational contribution coordination; the source does not revise the recurring review process.')
q04=entries[C(0)]['text'].rstrip('\n')
u04=unit('U04',C(0),q04,speech='asserted',parse='pragmatic',rationale='The usefulness reservation plausibly advises delaying exposure of the checkbox until replacement works. It is a technical review recommendation whose institutional type remains undetermined, without rule-making or enforcement evidence.',components=[
 comp('I','defer exposing',C(0),'Not sure it makes sense to expose','context_inferred','semantic_inference','Deferral is inferred from doubt about exposure until a capability exists; the source does not explicitly prohibit exposure.'),
 comp('Bdir','this (the checkbox feature)',C(0),'this',note='This is the explicit patient of expose; the pragmatic deferral keeps the same patient. The feature referent is resolved from the PR body.',extra=[ev(BODY,q01)],role='context_reference'),
 comp('Cex','until the wallet actually _can_ do replacement',C(0),'until the wallet actually _can_ do replacement...',note='The until phrase limits the timing of exposure. Can refers to wallet capability, not institutional authorization.'),
],alternative='A literal technical usefulness assessment without a request is possible. The candidate is advisory, not a categorical prohibition; wallet replacement capability is not necessarily identical to completion of the whole GUI workflow.',uncertainty='Tentative force and the scope of wallet versus GUI capability remain bounded uncertainties.',presnote='Underscore emphasis on can is preserved. Emphasis is neither quotation nor strikethrough; the occurrence is ordinary prose.')

q05="I don't think the confirmation window deserves red text and the bang for it."
u05=unit('U05',C(1),q05,role='container',speech='other',rationale='Structural parent for two independently executable presentation changes sharing a negative evaluative predicate; it is not a third proposition.',confidence='clear',levelnote='This structural grouping has no independently coded target or observed governance activity.',flags=['compound'])
u06=unit('U06',C(1),'red text',speech='asserted',parse='pragmatic',parent='U05',rationale='The negative presentation judgment implies a request to omit red styling for the confirmation. This is a one-off design recommendation, without established institutional expectation.',components=[
 comp('I','omit',C(1),q05,'context_inferred','semantic_inference','The shared negative deserves judgment outside this short child supplies the inferred edit action.'),
 comp('Bdir','red text',C(1),'red text','context_inferred','semantic_inference','The feature evaluated as undeserved is recast as the target of omission; source words alone do not make that transformed role explicit.'),
 comp('Cex','in the confirmation window for this transaction',C(1),'the confirmation window','context_inferred','shared_scope','The enclosing sentence identifies the location of both proposed presentation changes. No new unit span is enlarged to include it.'),
],alternative='The author may be stating a visual preference without requesting an edit. Red styling and the bang could be treated jointly if both remain recoverable.',uncertainty='The edit is pragmatically inferred from the negative assessment.')
u07=unit('U07',C(1),'the bang for it',speech='asserted',parse='pragmatic',parent='U05',rationale='The second object of the shared negative assessment implies omitting the exclamation mark. It is distinct from the color change and supplies no rule authority.',components=[
 comp('I','omit',C(1),q05,'context_inferred','semantic_inference','The enclosing negative deserves assessment supplies the inferred removal request for this second object.'),
 comp('Bdir','the bang for it',C(1),'the bang for it','context_inferred','semantic_inference','The evaluated punctuation feature is recast as the target of omission; bang is kept as supplied rather than silently replacing its source wording.'),
 comp('Cex','in the confirmation window for this transaction',C(1),'the confirmation window','context_inferred','shared_scope','The location is shared with the red-text assessment in the enclosing parent sentence.'),
],alternative='This can be a visual preference rather than an executable request. A coupled presentation edit is equivalent only if it preserves both color and punctuation changes.',uncertainty='The imperative action is inferred, not uttered.')
q08='Also "replaceable" there may have the user thinking that it\'s more replaceable than it is...'
u08=unit('U08',C(1),q08,speech='asserted',parse='pragmatic',rationale='The concern about misleading users is retained as a plausible editorial request to revise or clarify the label. It does not establish a general documentation norm or a permission to replace transactions.',components=[
 comp('I','revise or clarify',C(1),q08,'context_inferred','semantic_inference','An edit request is inferred from the stated risk of misleading the user; no specific replacement wording is provided in this occurrence.'),
 comp('Bdir','"replaceable"',C(1),'"replaceable"','context_inferred','semantic_inference','The literal subject causing a user inference becomes the patient of the inferred edit.'),
 comp('Cex','there (in the confirmation window)',C(1),'there','context_inferred','context_reference','There locates the label at the confirmation window in the preceding sentence.',extra=[ev(C(1),'the confirmation window')]),
],alternative='This may be solely a technical communication-risk rationale for the surrounding design suggestions, rather than a separate request. The risk is stated tentatively with may; actual user confusion is not observed.',uncertainty='The independent request is inferred. Its specific implementation is unresolved.')
q09="arguably it should be the non-replacable case that should get red text (because you can't update fees later)."
u09=unit('U09',C(1),q09,speech='proposed',parse='pragmatic',rationale='The author proposes red styling for the non-replaceable case instead. This is a case-specific UI recommendation; should and the technical fee rationale supply no institutional authority.',components=[
 comp('I','display',C(1),'get red text','context_inferred','semantic_inference','The interface case getting red text is reexpressed as the contributor displaying it; no actor is invented.'),
 comp('D','should',C(1),'should',start=span(C(1),q09)['start']+q09.index('that should'),note='The second should directly governs get red text; it carries advisory force qualified by arguably.'),
 comp('Bdir','red text',C(1),'red text','context_inferred','semantic_inference','Text is the complement of get in the source; it becomes the displayed material in the reconstructed edit.',start=span(C(1),q09)['start']),
 comp('Cac','the non-replacable case',C(1),'the non-replacable case','context_inferred','semantic_inference','The literal cleft subject identifies the case in which the display recommendation would apply, rather than a human actor.'),
],alternative='A literal technical configuration suggestion could keep the case as the subject of get. The because clause supplies the stated reason, not evidence of a sanction or observed inability among particular users.',uncertainty='The reconstructed display action changes argument roles; the recommendation is hedged by arguably.')
q10=entries[C(1)]['text'].split('\n\n')[1].rstrip('\n')
u10=unit('U10',C(1),q10,speech='proposed',parse='literal',rationale='The author offers a detailed alternative feature design. An explicit method is described, but this is a tentative one-off suggestion without the author committing to use it; institutional type therefore remains undetermined.',components=[
 comp('A','we',C(1),'we',start=span(C(1),q10)['start'],note='The collective addressee is explicitly we, with no supplied membership or authority.'),
 comp('D','should',C(1),'should',start=span(C(1),q10)['start'],role='shared_scope',note='Should in the wondering clause scopes the coordinated choice of having the replaceable switch or instead the adaptive-fee switch. It does not denote predictive technical should.'),
 comp('I','have',C(1),'have',start=span(C(1),q10)['start']+q10.index('instead,')),
 comp('Bdir','an "adaptive fee switch" (that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees-- and the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks])',C(1),'an "adaptive fee switch" (that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees-- and the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks])',note='The complete target includes the future locktimes, multiplicative fee progression, and changing fee-line schedule that identify the proposed alternative.'),
 comp('Cex','instead of a "replaceable switch"',C(1),'a "replaceable switch" and not, instead,','context_inferred','semantic_inference','The rhetorical not instead construction is interpreted as replacing the first alternative with the second, not as prohibiting the adaptive option. Both alternatives remain explicit in the quoted span.'),
],alternative='This is an exploratory wondering statement rather than a commitment to build the adaptive switch. The rhetoric asks whether the alternative is preferable; it does not establish mandatory exclusivity or a rejected actual proposal.',uncertainty='The preference remains exploratory and no adoption is supplied.',flags=['compound','nested_component'])

q11=entries[C(2)]['text'].split('\n\n')[0]
u11=unit('U11',C(2),q11,role='quotation',speech='asserted',quotation='repeated',rationale='Repeated occurrence of the exposure reservation coded as U04; omitted underscore formatting does not make it an independent endorsement.',confidence='clear',presnote='The > marker supplies quotation markup; the repeated source omits the original underscore emphasis. Plain denotes prose rather than code or suggestion-fence content.')
q12='Right. I totally agree.'
u12=unit('U12',C(2),q12,role='context',speech='reported_action',rationale='Attributable agreement responding to the immediately quoted concern. It is endorsement of that concern, not proof of an institutionalized expectation or rule.',confidence='clear')
q13="I'm working on the replacement GUI process"
u13=unit('U13',C(2),q13,role='context',speech='reported_action',rationale='The author reports ongoing implementation work. Neither completion nor an institutional expectation is established.',confidence='clear')
q14='this can be reviewed already.'
u14=unit('U14',C(2),q14,speech='asserted',parse='literal',force='unresolved',rationale='In the contrast between ongoing GUI work and review timing, this can be reviewed already plausibly invites review now. Can could express feasibility rather than authorized permission, so force and institutional type remain unresolved.',components=[
 comp('Bdir','this (PR 7819)',C(2),'this',start=span(C(2),q14)['start'],note='This is explicitly the patient of the passive be reviewed; treating it as Bdir preserves that grammatical patient. Context identifies the current PR, not the separate replacement workflow.',role='context_reference',extra=[ev(BODY,'review of this PR')]),
 comp('D','can',C(2),'can',start=span(C(2),q14)['start'],note='Lexical can is retained separately from unresolved capability-versus-permission force.'),
 comp('I','be reviewed',C(2),'be reviewed'),
 comp('Cex','already',C(2),'already'),
],alternative='This can be solely a statement of review feasibility, with no permission or recommendation. Read pragmatically it invites review despite incomplete replacement GUI work. The 0.13 timing concern is rationale, not a deadline imposed on reviewers.',uncertainty='No review authority or completed review is evidenced; capability and permission cannot be resolved from can.',levelnote='The focal action is reviewing this PR now. It is operational review coordination, distinct from exposing the feature or integrating a complete workflow.')

q15=entries[C(3)]['text'].split('\n\n')[0]
u15=unit('U15',C(3),q15,role='quotation',speech='proposed',quotation='repeated',rationale='Repeated occurrence of U10 supplies the precise response target without creating another proposal or endorsement.',confidence='clear',presnote='The > marker identifies a repeated prose quotation. The quote is retained exactly as supplied, including the full proposed fee behavior.')
q16='Yes. This might be a solution.'
u16=unit('U16',C(3),q16,role='context',speech='reported_action',rationale='Tentative endorsement of the immediately quoted adaptive-switch idea; might prevents treating it as an implementation decision.',confidence='clear')
q17='I somehow was also trying to allow adding additional outputs (edit the transaction back in the sendcoins dialog).'
u17=unit('U17',C(3),q17,speech='reported_action',parse='literal',force='nondeontic',itype='strategy_candidate',rationale='An attributable author describes an attempted development approach: enabling additional outputs through editing in the sendcoins dialog. As an explicit personal method it is retained as a strategy candidate, without evidence of success or obligation.',components=[
 comp('A','I',C(3),'I',start=span(C(3),q17)['start']),
 comp('I','trying to allow',C(3),'trying to allow',note='Trying is retained so the action does not become a report of successful implementation.'),
 comp('Bdir','adding additional outputs (edit the transaction back in the sendcoins dialog)',C(3),'adding additional outputs (edit the transaction back in the sendcoins dialog)',note='The parenthetical identifies the proposed editing workflow and remains part of the target design.'),
],alternative='This can instead be context reporting a past technical attempt, not an institutional strategy. Also is additive discourse, not an execution constraint; the parenthetical is an explanatory workflow, not a separate order to an end user.',uncertainty='The source reports an attempt. Neither success nor continuing commitment after the next question is established.')
q18='But maybe we should just focus on increasing the fees?'
u18=unit('U18',C(3),q18,speech='question',parse='literal',rationale='The author tentatively proposes narrowing the development focus to fee increases. It is a review-scope suggestion for this work, not a new recurring contribution arrangement.',components=[
 comp('A','we',C(3),'we',start=span(C(3),q18)['start']),
 comp('D','should',C(3),'should',start=span(C(3),q18)['start'],note='Advisory should is explicitly qualified by maybe; it is not a binding restriction.'),
 comp('I','focus',C(3),'focus',note='Focus is the action; on marks its target, not a separate indirect recipient.'),
 comp('Bdir','increasing the fees',C(3),'increasing the fees'),
 comp('Cex','just',C(3),'just',note='Just narrows the proposed focus to fees rather than the additional-output workflow.'),
],alternative='It is a genuine exploratory question rather than a settled request. It does not by itself withdraw the additional-output idea or reject all future scope expansion.',uncertainty='Maybe and the question form leave the preference provisional.')
q19='you need to handle also making a child transaction of the original transaction for use in case the original confirms...'
u19=unit('U19',C(4),q19,speech='asserted',parse='literal',force='unresolved',rationale='The described need could be read as a development requirement, but its supplied basis is technical behavior of the additional-output workflow. No institutional obligation, authority, or sanction is established.',components=[
 comp('A','you',C(4),'you',note='The generic or conversational developer address is explicit; no named person or role is supplied.'),
 comp('D','need to',C(4),'need to',note='This is lexical necessity. Whether it carries any institutional obligation beyond technical need is unresolved.'),
 comp('I','handle',C(4),'handle'),
 comp('Bdir','making a child transaction of the original transaction',C(4),'making a child transaction of the original transaction'),
 comp('Cac','workflow for additional outputs',C(4),'workflow for additional outputs','context_inferred','shared_scope','The enclosing technical subject bounds when this necessity applies; interpreting it as an activation condition is inferred from the because explanation outside the child span.'),
 comp('Cex','for use in case the original confirms',C(4),'for use in case the original confirms',note='The child transaction is to be available if the original confirms; this is its qualifying use, not a claim that construction begins only after confirmation.'),
],alternative='The whole passage is technical explanation of transaction handling, not a social prescription. It is retained conservatively as a plausible requirement candidate; technical necessity alone cannot make it a rule candidate.',uncertainty='Technical necessity versus interpersonal development expectation is not resolved.',flags=['nested_component'])
q20='and if you do this multiple times there is a bit of exponential blowup in the number of versions you must compute.'
u20=unit('U20',C(4),q20,role='context',speech='technical_description',rationale='Conditional computational growth is a technical consequence and rationale for scope discussion. Must compute states technical workload, not an independently instituted duty or sanction.',alternative='One could parse the embedded compute predicate as another technical-necessity candidate. Here it remains a conditional consequence of repeating the method, not a distinct executable review request.',uncertainty='The source gives qualitative complexity only, without a proof, measurements, or an enforcement claim.',confidence='clear')

q21='Instead of the word "replacable" perhaps the word "updatable" or "amendable" would better express what the it\'ll do?'
u21=unit('U21',C(5),q21,speech='question',parse='pragmatic',quotation='proposed_wording',rationale='A tentative question offers two replacement labels as an editorial recommendation. The object alternatives are preserved in one coupled wording choice, without inventing exclusive-or requirements or accepted terminology.',components=[
 comp('I','use',C(5),q21,'context_inferred','semantic_inference','Use is reconstructed from a comparative question about which wording would express the feature more accurately.'),
 comp('Bdir','the word "updatable" or "amendable"',C(5),'the word "updatable" or "amendable"','context_inferred','semantic_inference','The literal subject of would better express becomes the wording to use; both proposed alternatives remain available.'),
 comp('Cex','Instead of the word "replacable"',C(5),'Instead of the word "replacable"',note='The explicit instead-of phrase identifies what the proposed replacement labels displace.'),
],alternative='This may be a genuine question about semantic adequacy. No particular alternative is selected; it also does not establish a general naming rule.',uncertainty='Perhaps and the question leave the wording tentative.',presnote='The quoted alternatives are newly offered replacement wording; the entire sentence also names the old spelling and is plain prose, not an external quotation.')
q22='doing the add output thing would be pretty interesting...'
u22=unit('U22',C(5),q22,role='context',speech='asserted',rationale='Expression of interest in the previously discussed additional-output design; it is weak technical endorsement, not a commitment, direction to implement, or recognition of an expectation.',confidence='clear')
q23='though it would be nice to have a [send immediately] option which delays sending it, thus avoids having to do the extra just in case transactions if you amend with in the timeout. (and could also let you abort before it was initially set).'
u23=unit('U23',C(5),q23,speech='proposed',parse='literal',rationale='The source offers a delayed-send option as a technical feature suggestion. It describes anticipated benefits without promising implementation, granting end-user institutional permission, or establishing a shared expectation.',components=[
 comp('I','have',C(5),'have',start=span(C(5),q23)['start']),
 comp('Bdir','a [send immediately] option which delays sending it',C(5),'a [send immediately] option which delays sending it',note='The complete supplied label and its counterintuitive delay behavior identify this proposed option; neither is silently corrected.'),
 comp('Bdir,p','thus avoids having to do the extra just in case transactions if you amend with in the timeout',C(5),'thus avoids having to do the extra just in case transactions if you amend with in the timeout',note='This is an anticipated conditional property of the proposed option. It does not assert an observed result or an institutional no-obligation rule.'),
 comp('Bdir,p','(and could also let you abort before it was initially set)',C(5),'(and could also let you abort before it was initially set)',note='Could is a tentative technical capability claim about the same option. The before condition and the source wording set are retained without inferring a corrected technical term.'),
],alternative='It is exploratory engineering speculation rather than a prescription. The parenthetical abort capability can be read as a second optional feature, but it is coupled here as another tentative property of the same delayed-send design.',uncertainty='The [send immediately] label appears alongside delay behavior, and initially set is ambiguous. The packet supplies no clarification or implementation confirmation.',flags=['nested_component','unresolved_reference'])

q24=entries[C(6)]['text'].rstrip('\n')
u24=unit('U24',C(6),q24,speech='asserted',parse='pragmatic',quotation='proposed_wording',rationale='The spelling assertion pragmatically suggests a conditional correction if the earlier alternative-label suggestion is not followed. A claim of accepted spelling is not institutional authorization or demonstrated governance norm.',components=[
 comp('A','Jonas',C(6),'Jonas','context_inferred','semantic_inference','The named addressee becomes the actor of the inferred correction. The source does not state a maintainer role or an explicit correction command.'),
 comp('I','correct',C(6),'is the more accepted spelling','context_inferred','semantic_inference','The editorial action is reconstructed from the assertion about accepted spelling.'),
 comp('Bdir','the spelling',C(6),'spelling','context_inferred','semantic_inference','The predicate description of accepted spelling becomes the target of the inferred correction. The exact current word is recoverable in the preceding suggestion, not silently expanded from the proposed fragment.',extra=[ev(C(5),'the word "replacable"')]),
 comp('Cex','use the supplied "replaceab"... spelling fragment',C(6),'"replaceab"...','context_inferred','semantic_inference','The literal candidate subject is transformed into replacement wording. The ellipsis is preserved; no full corrected identifier is invented.'),
 comp('Cac',"if you don't go with Greg's suggestion",C(6),"if you don't go with Greg's suggestion",note='The negative condition qualifies the fallback correction. Its likely relation to the earlier alternate labels is inferred separately, not treated as a verified person identity.'),
],alternative='The sentence can be merely information about usage, with no requested edit. Greg\'s suggestion most plausibly refers to the immediately preceding alternate labels, but the packet does not supply a real-name mapping or reliable reply thread.',uncertainty='Both the imperative force and exact complete replacement spelling are unexpressed; the antecedent of Greg\'s suggestion is contextual.',presnote='The quoted fragment is newly suggested spelling, not a repeated quotation of an original proposal. No source ellipsis is repaired.',flags=['unresolved_reference'])

q25='Needs rebase.'
u25=unit('U25',C(7),q25,speech='asserted',parse='pragmatic',force='unresolved',itype='norm_candidate',rationale='The brief review comment expresses an expected maintenance action for the current contribution, making it a norm candidate at text-only standing. The supplied text does not distinguish a technical need from a socially obligatory prerequisite, and supplies no rule authorization or enforcement.',components=[
 comp('I','rebase',C(7),'rebase','context_inferred','semantic_inference','The nominal complement of Needs becomes the verb of a reconstructed maintenance request.'),
 comp('D','Needs',C(7),'Needs',note='The lexical need marker is explicit; an obligation versus technical necessity reading is unresolved.'),
 comp('Bdir','PR 7819',C(7),q25,'context_inferred','context_reference','The object omitted from this elliptical comment is inferred to be the current PR from its supplied object_id and body; no named actor is supplied.',extra=[ev(BODY,'This PR')]),
],alternative='It may be only a technical status observation. Even as a request it does not prove a general rebase rule, a maintainer issuing it, or a condition whose breach caused closure.',uncertainty='The actor, timing requirement, binding force, and any response to this request remain unestablished.',levelnote='The focal action is rebasing this particular contribution as ordinary maintenance. It does not change recurring integration procedures or authority.')
q26=entries[C(8)]['text'].rstrip('\n')
u26=unit('U26',C(8),q26,role='context',speech='reported_action',rationale='The PR author announces closure in favor of a distinct PR and reports inclusion there. This is an action and outcome report, not an instruction, sanction, merge event, or proof that all review suggestions were included.',confidence='clear',levelnote='Closing and redirecting a contribution to a different PR is an operational contribution-management act. No authority allocation follows from author attribution alone.')

# Recognition records separate assent, response, and recorded status from expectation recognition.
rec(u04,'endorsement','this_proposition',[ev(C(2),q11),ev(C(2),q12)],'The author quotes the exposure concern and expressly agrees. The agreement supports the concern as a technical position, not recognition of a binding or shared institutional expectation.')
rec(u04,'response','this_proposition',[ev(C(2),q11),ev(C(2),q13),ev(C(2),q14)],'Following the exact quoted concern, the author distinguishes current review from completion of the replacement GUI. The correspondence is explicit, but it does not promise that exposure will be deferred.')
rec(u10,'endorsement','this_proposition',[ev(C(3),q15),ev(C(3),q16)],'The precisely quoted alternative receives a tentative might-be-a-solution response. This is not acceptance of a requirement or a verified implementation.')
rec(u17,'response','this_proposition',[ev(C(3),q17),full(C(4))],'The reply discusses the same additional-output workflow and its complexity. Textual correspondence supports a contextual response target, not reliable reply threading or recognition of an obligation.','context_inferred')
rec(u17,'endorsement','this_proposition',[ev(C(3),q17),ev(C(5),q22)],'The later comment calls the add-output idea interesting; this is qualified interest in the same design rather than a commitment to implement it.','context_inferred')
rec(u08,'response','this_proposition',[ev(C(1),q08),ev(C(5),q21)],'The later wording alternatives plausibly answer the earlier misleading-label concern. The correspondence is contextual, not an explicit reference to that particular earlier sentence.','context_inferred')
rec(u21,'response','this_proposition',[ev(C(5),q21),full(C(6))],'The conditional fallback most plausibly follows the immediately preceding alternate labels and calls it Greg\'s suggestion. This is an inferred response target; neither person-name resolution nor acceptance is established.','context_inferred')
close_ev=[ev(META,'"state": "closed"'),ev(META,'"closed_at": "2016-06-09T09:21:57+00:00"'),ev(META,'"merged_at": null'),ev(META,'"merged": false')]
for u in [u02,u03,u04,u25]:
    disp(u,'recorded_closed_unmerged','broader_proposal',close_ev,'The enclosing PR 7819 is recorded closed without merge. This does not establish rejection, withdrawal, or fulfillment of this individual proposition.')
rec(u02,'recorded_status','broader_proposal',close_ev,'The original contribution closed unmerged; metadata establishes repository status, not a decision about the uncertain inclusion constraint.')

relations=[]
def rel(a,b,t,evidence,rationale,basis='context_inferred',logic='not_applicable'):
    relations.append({'from_unit_id':a,'to_unit_id':b,'type':t,'basis':basis,'rationale':rationale,'evidence':evidence,'logic_scope':logic})
rel('U04','U01','challenges',[ev(C(0),q04),ev(BODY,q01)],'The exposure reservation challenges the readiness or usefulness of the proposed checkbox before replacement capability. It does not reject the feature altogether.')
rel('U04','U02','clarifies',[ev(C(0),q04),ev(BODY,q02)],'Both occurrences question proceeding before replacement exists; the reply names wallet capability, whereas the body names a GUI workflow. This correspondence does not erase the difference in scope.')
rel('U06','U07','AND',[ev(C(1),q05)],'The source joins color and bang under one negative assessment; both independently recoverable presentation changes belong to the same proposed edit set.','explicit','actions')
rel('U11','U04','quotes',[ev(C(2),q11),ev(C(0),q04)],'The > occurrence reproduces the exposure reservation with underscore emphasis omitted; it is quotation rather than another endorsement.','explicit')
rel('U04','U12','uptake',[ev(C(2),q11),ev(C(2),q12)],'Initiating concern to the author\'s explicit agreement with the quoted concern; response uptake does not demonstrate compliance.','explicit')
rel('U04','U14','uptake',[ev(C(2),q11),ev(C(2),q13),ev(C(2),q14)],'The quoted reservation is followed by a contrast separating work in progress from review already being possible. This is response uptake, not implementation of a deferral condition.','explicit')
rel('U14','U03','clarifies',[ev(BODY,q03),ev(C(2),q13),ev(C(2),q14)],'The later can-be-reviewed-now assertion clarifies the author\'s earlier desire not to hold back review. It does not authorize integration.')
rel('U15','U10','quotes',[ev(C(3),q15),ev(C(1),q10)],'The full adaptive-fee proposal is repeated before a response, preserving future locktimes, fee growth, and display details.','explicit')
rel('U10','U16','uptake',[ev(C(3),q15),ev(C(3),q16)],'Initiating design proposal to the author\'s tentative affirmative response. Might be a solution does not show adoption.','explicit')
rel('U18','U17','challenges',[ev(C(3),q17),ev(C(3),q18)],'The fee-only focus question tentatively challenges whether the additional-output scope should be pursued now. It is not evidence that the earlier attempt was withdrawn.')
rel('U17','U19','uptake',[ev(C(3),q17),full(C(4))],'The technical response addresses handling additional outputs and explains a child-transaction need. Topic correspondence supplies the response link; no verified implementation or interpersonal obligation follows.')
rel('U20','U19','clarifies',[full(C(4))],'The conditional workload consequence elaborates the technical complexity of repeating the proposed handling. This is not an institutional O consequence or sanction.')
rel('U17','U22','uptake',[ev(C(3),q17),ev(C(5),q22)],'The later expression of interest responds to the additional-output design, without committing to it.')
rel('U21','U08','clarifies',[ev(C(1),q08),ev(C(5),q21)],'The later alternatives specify ways to address the label\'s meaning. The connection is contextual, not an explicitly attributed reply.')
rel('U21','U24','uptake',[ev(C(5),q21),full(C(6))],'The fallback correction condition plausibly responds to the alternate-label suggestion. The target is contextual and no verified real-name mapping or expectation recognition is inferred.')

screen_reasons={
 BODY:'Focal body fully screened: technical feature description and missing capability are context; tentative inclusion reservation and personal review approach are retained candidates. Ongoing work, refactoring provenance, and unrendered image links supply context rather than extra prescriptions.',
 C(0):'Focal entry fully screened: a tentative exposure-deferral recommendation is retained, with the literal technical-utility alternative and wallet-capability condition.',
 C(1):'Focal entry fully screened: split red-text and bang changes, misleading-label concern, conditional non-replaceable styling, and the complete adaptive-fee alternative are retained. The container is not counted as a proposition.',
 C(2):'Focal entry fully screened: the repeated exposure quote is not a new endorsement; agreement and ongoing work are context, while review-now is a candidate with capability-versus-permission uncertainty. Release timing is contextual rationale.',
 C(3):'Focal entry fully screened: the adaptive-fee quote is repeated content, response is tentative endorsement, additional-output work is a reported strategy candidate, and fee-only focus is a separate question-form suggestion.',
 C(4):'Focal entry fully screened: retain the child-transaction necessity as a plausible development-requirement candidate with a technical alternative. Repeated-workflow computation growth is context, not a separate institutional duty or sanction.',
 C(5):'Focal entry fully screened: alternative labels and the delayed-send option are separate suggestions; interesting add-output comment is context. Delay, timeout qualification, and tentative abort capability are retained within the proposed option.',
 C(6):'Focal entry fully screened: retain conditional spelling correction, its negative condition, exact incomplete proposed fragment, and unresolved reference to Greg\'s suggestion.',
 C(7):'Focal entry fully screened: elliptical rebase request retained with unresolved technical-necessity versus obligation force and no invented actor or authority.',
 C(8):'Focal entry fully screened: author reports closing and inclusion in another PR. This is an operational act/outcome, not an independently proposed prescription or institutional configuration.',
 META:'Supplement screened for status, provenance, and file inventory. Context-only under the assignment; this does not assert that supplemental metadata lacks institutional significance. Closed/unmerged status concerns PR 7819.',
 SMETA:'Supplement screened: PR 7819 current archived status and retained head identity are context. The non-null merge_commit_sha does not override merged:false and merged_at:null. Context-only is the assigned supplemental role.',
 M8182:'Supplement screened: PR 8182 is a distinct object with its own dates and unmerged closure. It does not verify transferred patches or integration. Context-only is the assigned supplemental role, not a claim of no institutional content.'
}
for i in range(6):
    screen_reasons[f'pr7819:patch:{i}']='Supplemental retained-head patch fully screened as technical/context evidence under the assignment, not an exhaustive extraction target. Its code, comments, interface wording, and capability settings are not automatically institutional permissions or constitutive arrangements; no history or causal review-to-change link is supplied.'
screen=[]
for e in packet['entries']:
    us=[u for u in units if u['source_id']==e['source_id']]
    screen.append({'source_id':e['source_id'],'disposition':'candidate' if any(u['record_role']=='statement' for u in us) else ('empty' if not e['text'] else 'context_only'),'reason':screen_reasons[e['source_id']],'unit_ids':[u['unit_id'] for u in us]})

outcomes=[
 {'claim':'The author of PR 7819 announced closing it in favor of #8182 and reported that the contribution was included there. PR 7819 is recorded closed on 2016-06-09 and unmerged. The inclusion claim is a participant report about the broader contribution, not verification of any individual review suggestion.', 'evidence':[ev(C(8),q26)]+close_ev},
 {'claim':'The separate PR 8182 is also recorded closed and unmerged, with closed_at 2016-12-06T10:15:00Z and merged_at null. Its supplied merge_commit_sha is not evidence of integration. The packet does not establish that either PR was merged.', 'evidence':[ev(M8182,'"number": 8182'),ev(M8182,'"state": "closed"'),ev(M8182,'"merged": false'),ev(M8182,'"closed_at": "2016-12-06T10:15:00Z"'),ev(M8182,'"merged_at": null'),ev(M8182,'"merge_commit_sha": "1987a7a11a1a9513f2eca7a54c751178e2ef518c"')]+close_ev},
 {'claim':'The retained PR 7819 patch contains the red #aa0000 styling and the literal message This transaction is replacable (optin-RBF)! at its supplied head. This establishes the retained code occurrence only; without revision chronology it cannot establish whether review caused, failed to cause, or preceded any particular change.', 'evidence':[ev('pr7819:patch:1','+        questionString.append("<hr /><span style=\'color:#aa0000;\'>");\n+        questionString.append(tr("This transaction is replacable (optin-RBF)!"));'),ev(SMETA,'"head_sha": "9c4baa44d6448b3432fe265f5c800af29a6cdaf1"')]}
]
mechanisms=[
 {'category':'review_coordination','claim':'The body questions inclusion without a replacement GUI workflow while expressing a desire not to delay review. A commenter then questions exposure before wallet replacement is possible; the author quotes and agrees with that concern, reports GUI work in progress, and says this can already be reviewed, citing a difficult 0.13 timeline. The supported sequence distinguishes review timing from readiness to expose the feature; it shows no adopted gating rule or completed review.', 'evidence':[ev(BODY,q02),ev(BODY,q03),ev(C(0),q04),full(C(2))],'unit_ids':['U02','U03','U04','U11','U12','U13','U14'],'alternative_explanation':'The exchange may coordinate ordinary technical work by expressing feasibility and shared caution, without any institutional permission or requirement being recognized. The timeline may motivate continued review but does not identify a causal effect on integration.','status':'supported_sequence'},
 {'category':'reason_giving','claim':'An adaptive-fee design is proposed with future-locktime replacements, multiplicatively higher fees, and a changing fee display. The author quotes it, calls it a possible solution, reports attempting additional outputs through the sendcoins dialog, and asks whether to focus only on fee increases. The subsequent reply explains child-transaction handling and conditional growth in computed versions. This supplies specific technical reasons relevant to scope deliberation, but no resolved design selection or verified implementation.', 'evidence':[ev(C(1),q10),full(C(3)),full(C(4))],'unit_ids':['U10','U15','U16','U17','U18','U19','U20'],'alternative_explanation':'These may be exploratory engineering alternatives rather than governance expectations. The complexity explanation need not have changed the author\'s preferred scope, and subsequent implementation is not supplied.','status':'supported_sequence'},
 {'category':'scope_management','claim':'A rebase need is stated, and the later author comment announces closing PR 7819 in favor of #8182 with inclusion reported there. PR 7819 is recorded closed unmerged; the distinct replacement PR 8182 is also recorded closed unmerged later. This is consistent with managing the contribution through supersession, without showing that the rebase request caused the move or that either closure sanctioned noncompliance.', 'evidence':[ev(C(7),q25),ev(C(8),q26)]+close_ev+[ev(M8182,'"number": 8182'),ev(M8182,'"merged": false'),ev(M8182,'"closed_at": "2016-12-06T10:15:00Z"'),ev(M8182,'"merged_at": null')],'unit_ids':['U25','U26'],'alternative_explanation':'The author may have already prepared the other PR independently of the rebase observation. The packet lacks reply threading, a complete patch history, and a stated causal link; reported inclusion does not establish integration.','status':'consistent_with'}
]
summary={'observed_outcomes':outcomes,'mechanisms':mechanisms,'missing_evidence':[
 'No complete edit or revision history, reliable reply threading, or supplied review/test completion records; retained text may reflect later edits.',
 'No rendered images; visual claims are restricted to the supplied prose and retained code patch.',
 'No patch or substantive discussion for PR 8182 and no supplied outcome for PR 7159; inclusion and refactoring links cannot verify per-proposition implementation.',
 'No institutional authorization, rule-making procedure, enforcement linkage, participant role credentials, or repeated recognition evidence is supplied.',
 'No evidence of network adoption or higher-level authority allocation; repository status is a separate object from network behavior.'
], 'unresolved_questions':[
 'Do the exposure reservations and review-now claim express technical feasibility alone, or an interpersonal expectation about how this contribution should proceed?',
 'Does the author\'s personal non-delay preference amount to a development strategy, and does the reported additional-output attempt remain active after the fee-only question?',
 'Which wording or feature suggestions, if any, were implemented in PR 8182 or another contribution? The report of inclusion does not identify individual suggestions.',
 'Does Greg\'s suggestion refer to the preceding alternate-label proposal, and what complete replacement spelling does the quoted replaceab fragment intend?',
 'What exactly does the [send immediately] option mean when it delays sending, and what is meant by initially set in the abort parenthetical?',
 'Did the rebase observation have any role in supersession? The packet establishes no such causal or enforcement relation.'
]}
annotation={'schema_version':'0.3','run_id':'F03_v03_r2','episode_id':'F03','packet_sha256':hashlib.sha256((ROOT/'packet.json').read_bytes()).hexdigest(),'entry_screening':screen,'units':units,'relations':relations,'episode_summary':summary}
(ROOT/'annotation.json').write_text(json.dumps(annotation,ensure_ascii=False,indent=2)+'\n')
# Freeze the first complete annotation before any checker run or source self-review.
freeze=ROOT/'annotation.first_complete.json'
if freeze.exists(): raise RuntimeError('First-complete freeze already exists; do not overwrite')
freeze.write_bytes((ROOT/'annotation.json').read_bytes())
print(json.dumps({'entries':len(screen),'units':len(units),'statements':sum(u['record_role']=='statement' for u in units),'relations':len(relations),'packet_sha256':annotation['packet_sha256']}))
