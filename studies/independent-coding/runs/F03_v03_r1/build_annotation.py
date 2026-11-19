import json, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
packet_path = ROOT / 'packet.json'
p = json.loads(packet_path.read_text())
S = {x['source_id']: x for x in p['entries']}
units = []
relations = []

def sp(sid, q, start_at=0):
    text = S[sid]['text']
    start = text.index(q, start_at)
    return {'start': start, 'end': start + len(q), 'quote': q}

def ev(sid, q, start_at=0):
    return {'source_id': sid, 'span': sp(sid,q,start_at)}

def evu(u):
    return {'source_id':u['source_id'], 'span':dict(u['span'])}

def unit(n, sid, q, role='statement', speech='proposed', parse='literal', force='recommendation', itype='undetermined', rationale='', alt='', uncertainty='', confidence='plausible', parent=None, quotation='none', markup='plain', scope='case_specific'):
    isstmt=role=='statement'
    u={'unit_id':f'F03-U{n:02d}', 'source_id':sid, 'span':sp(sid,q), 'parent_unit_id':parent,
       'grammar':'regulative' if isstmt else 'not_institutional', 'speech_act':speech,'scope':scope,'components':[],
       'institution':{'type':itype if isstmt else 'not_applicable','standing':'text_only' if isstmt else 'not_applicable','dispute_present':False,'rationale':rationale if rationale else ('One-off contribution proposal; no attributed rule-making authority or recognized obligation is supplied.' if isstmt else 'Record preserves a communicative act or technical context, not an additional institutional proposition.'),'evidence':[ev(sid,q)],'recognition':[],'authority_evidence':[]},
       'statement_target_level':'operational' if isstmt else 'not_applicable',
       'observed_action_level':'not_applicable' if role=='container' else 'operational',
       'level_rationale':('The focal action concerns this contribution or its review within the existing repository process. The technical feature does not itself revise recurring governance arrangements.' if isstmt else ('Structural grouping only; no separate governed or observed action is counted.' if role=='container' else 'The visible act belongs to contribution discussion or disposition. This context record has no statement target.')),
       'complexity_flags':['none'], 'alternative_interpretation':alt,'confidence':confidence,'uncertainty_reason':uncertainty,
       'record_role':role,'parse_mode':parse,'deontic_force':force if isstmt else 'nondeontic','level_alternatives':[],
       'presentation':{'quotation':quotation,'markup':markup,'rationale':'Presentation is the supplied occurrence; no edit history or later formatting state is inferred.'},'disposition_events':[]}
    units.append(u)
    return u

def comp(u,sym,text,anchor=None,basis='explicit',role='local',note='',source=None):
    sid = source or u['source_id']
    anchor = text if anchor is None else anchor
    if isinstance(anchor,list):
        evidence=anchor
    else:
        begin=u['span']['start'] if sid==u['source_id'] and role=='local' else 0
        evidence=[ev(sid,anchor,begin)]
    u['components'].append({'symbol':sym,'text':text,'basis':basis,'evidence':evidence,'inference_note':note,'occurrence_role':role})

def recognition(u,kind,target,evidence,rationale,basis='context_inferred'):
    u['institution']['recognition'].append({'kind':kind,'target':target,'basis':basis,'evidence':evidence,'rationale':rationale})

def relation(a,b,typ,evidence,rationale,basis='context_inferred',logic='not_applicable'):
    relations.append({'from_unit_id':a['unit_id'],'to_unit_id':b['unit_id'],'type':typ,'basis':basis,'rationale':rationale,'evidence':evidence,'logic_scope':logic})

body='pr7819:body'; c=lambda n:f'pr7819:comments:{n}'
u1=unit(1,body,'Adds a checkbox to the Send-Coins-Pannel (next to "Add Recipient") that allows to set the according nSequence to signal BIP125 RBF.\n\nThis PR does not include a way to actually replace a transaction with the GUI.',role='context',speech='technical_description',confidence='clear',alt='Describes the submitted feature and its missing companion workflow; capability language is not an institutional permission.')
u2=unit(2,body,"So not sure if we want this without a GUI based replacement workflow (which I'm working on but it is a bigger chunk).",speech='asserted',parse='pragmatic',force='unresolved',rationale='The author raises a possible readiness condition for accepting the partial feature. The wording expresses doubt rather than a definite requirement; no authority or shared expectation is established.',alt='May be uncertainty about product usefulness rather than a recommendation to defer acceptance. The accompanying workflow is reported as work in progress, not completed.',uncertainty='The pragmatic acceptance/defer action is inferred from wanting this without its companion workflow; the group denoted by we is unspecified.')
comp(u2,'A','we',note='The source directly attributes the deliberative choice to we. The pragmatic interpretation preserves that actor role without identifying its members.')
comp(u2,'I','withhold accepting','not sure if we want',basis='context_inferred',role='semantic_inference',note='Reconstructs a tentative deferral concern from doubt about wanting the partial feature; no categorical prohibition is asserted.')
comp(u2,'Bdir','this','this',basis='context_inferred',role='semantic_inference',note='The literal object of want becomes the target of inferred acceptance; the feature is described in the preceding sentences.')
comp(u2,'Cac','without a GUI based replacement workflow',note='The absence of the companion workflow explicitly qualifies the acceptance concern.')
u3=unit(3,body,"But I don't want to hold back review of this PR.",speech='asserted',force='nondeontic',itype='strategy_candidate',rationale='The author states a personal approach to proceeding with review while companion work remains incomplete. This supports a personal strategy candidate, not an obligation imposed on reviewers.',alt='The sentence may express a preference or invitation rather than a committed plan. It does not require anyone to review.',uncertainty='The intended review sequencing is expressed, but implementation and other participants\' responsibilities are not established.')
comp(u3,'A','I')
comp(u3,'I',"don't want to hold back",note='Retains the full negative volitional predicate; neither want nor its negation is converted into an institutional deontic.')
comp(u3,'Bdir','review of this PR')
u3['level_rationale']='The focal strategy concerns initiating review of this PR before a companion feature is complete, an operational contribution decision.'

u4=unit(4,c(0),'Not sure it makes sense to expose this until the wallet actually _can_ do replacement...',speech='asserted',parse='pragmatic',rationale='A tentative readiness objection plausibly recommends delaying exposure of this feature. An attributed author agrees with it, but neither technical assent nor this reply establishes a recognized obligation.',alt='May be only a question of technical usefulness. The emphasized can concerns wallet capability, not authorized discretion; the inferred recommendation is not a binding integration rule.',uncertainty='Deferring exposure is a pragmatic reconstruction; expose could concern user-facing availability rather than merging the code.')
comp(u4,'I','defer exposing','Not sure it makes sense to expose',basis='context_inferred',role='semantic_inference',note='The hesitant evaluative assertion is interpreted as advice to wait, with its tentative force retained.')
comp(u4,'Bdir','this',note='This remains the explicit object of expose in the reconstructed deferral request. Its referent is the checkbox feature described in the body; no actor is invented.')
comp(u4,'Cex','until the wallet actually _can_ do replacement',note='The explicit until clause bounds how long exposure would be deferred; emphasis denotes technical capability.')

q5="I don't think the confirmation window deserves red text and the bang for it."
u5=unit(5,c(1),q5,role='container',speech='other',confidence='clear',alt='Groups two independently executable changes to the same warning treatment; only the children are counted as statements.')
u5['complexity_flags']=['compound']
u6=unit(6,c(1),"I don't think the confirmation window deserves red text",speech='asserted',parse='pragmatic',parent=u5['unit_id'],alt='Literally an assessment of the warning presentation; pragmatically a request to remove its red styling.',uncertainty='The edit action and implementation actor are not directly commanded; no implementer is identified.')
comp(u6,'I','remove',u6['span']['quote'],basis='context_inferred',role='semantic_inference',note='Reconstructs the edit implied by saying the window does not deserve this treatment.')
comp(u6,'Bdir','red text','red text',basis='context_inferred',role='semantic_inference',note='The literal object of deserves is recast as the target of removing the styling.')
comp(u6,'Cex','from the confirmation window','the confirmation window',basis='context_inferred',role='semantic_inference',note='The literal subject is transformed into the location of the inferred edit.')
u7=unit(7,c(1),'and the bang for it.',speech='asserted',parse='pragmatic',parent=u5['unit_id'],alt='The bang is part of the same criticized warning treatment; it could be grouped with red styling without altering the proposed removal of both.',uncertainty='The action and location are inherited from the preceding clause; bang is interpreted as the exclamation mark without extending the request to unrelated punctuation.')
comp(u7,'I','remove',[ev(c(1),"I don't think the confirmation window deserves"),evu(u7)],basis='context_inferred',role='semantic_inference',note='The negated evaluative predicate scopes over the coordinated bang. It supports a separate inferred removal action; the first anchor is outside the child span.')
comp(u7,'Bdir','the bang','the bang',basis='context_inferred',role='semantic_inference',note='The coordinated object of deserves becomes the target of the inferred edit.')
comp(u7,'Cex','from the confirmation window','the confirmation window',basis='context_inferred',role='semantic_inference',note='The location is inherited from the shared subject outside this child span; it is a transformed role rather than an explicit location.')
relation(u6,u7,'AND',[ev(c(1),'red text and the bang')],'The conjunction joins the two criticized visual features; the inferred removal requests concern both.',basis='explicit',logic='actions')
u8=unit(8,c(1),'Also "replaceable" there may have the user thinking that it\'s more replaceable than it is...',speech='asserted',parse='pragmatic',rationale='The reviewer raises a usability objection that plausibly asks for clearer naming. The technical reading remains viable and does not establish a general naming norm.',alt='Could be only a prediction of user misunderstanding, with no independent edit request beyond the later naming proposal.',uncertainty='The action revise and its purpose are inferred; the source does not specify replacement wording in this clause.')
comp(u8,'I','revise',u8['span']['quote'],basis='context_inferred',role='semantic_inference',note='Infers an editorial request from the claimed misleading effect of the label.')
comp(u8,'Bdir','the "replaceable" wording','"replaceable" there',basis='context_inferred',role='semantic_inference',note='The literal subject causing misunderstanding becomes the target of the inferred revision.')
comp(u8,'Cex','to avoid overstating the transaction\'s replaceability',"may have the user thinking that it's more replaceable than it is",basis='context_inferred',role='semantic_inference',note='Reconstructs the purpose from the explicitly stated misunderstanding rather than asserting verified user behavior.')
u9=unit(9,c(1),"arguably it should be the non-replacable case that should get red text (because you can't update fees later).",speech='proposed',parse='pragmatic',alt='May be rhetorical criticism of the current warning rather than a settled design request. The inability to update fees is the reviewer\'s stated rationale, not an independently verified technical fact.',uncertainty='The display action and trigger are reconstructed from a technical object getting a treatment; arguably keeps the recommendation tentative.')
comp(u9,'I','display','get',basis='context_inferred',role='semantic_inference',note='Recasts the case receiving red text as an edit to display red text; no technical case is coded as a human actor.')
comp(u9,'D','should','should get',basis='context_inferred',role='semantic_inference',note='The second should scopes over getting red text and supports advisory force in the reconstructed display request; the anchor includes the predicate to disambiguate the two should occurrences.')
comp(u9,'Bdir','red text','red text',basis='context_inferred',role='semantic_inference',note='Retains the requested treatment while acknowledging the receiving-case to display-action reconstruction.')
comp(u9,'Cac','in the non-replacable case','the non-replacable case',basis='context_inferred',role='semantic_inference',note='The literal subject/receiving case becomes the condition for the display action.')
u10=unit(10,c(1),'I\'m wondering if we should even have a "replaceable switch" and not, instead, have an "adaptive fee switch" (that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees-- and the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks])',speech='proposed',alt='An exploratory design question rather than a committed implementation plan. The quoted response later calls it a possible solution, which does not establish implementation or institutional obligation.',uncertainty='The recommendation selects an alternative design tentatively; the membership of we and actual implementation remain unspecified.')
comp(u10,'A','we')
comp(u10,'D','should',note='The modal scopes over the coordinated design alternatives; it is advisory in this exploratory formulation.')
comp(u10,'I','have','have an',basis='context_inferred',role='semantic_inference',note='Uses the second have, identified by its following article, as the action of choosing the adaptive option; the field normalizes the scoped selection rather than treating the first have as the positive proposal.')
comp(u10,'Bdir','an "adaptive fee switch"')
comp(u10,'Bdir,p','(that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees-- and the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks])',note='Preserves the entire proposed technical behavior, including locktimes, multiplicative fees, and the displayed fee schedule.')
comp(u10,'Cex','instead of a "replaceable switch"','a "replaceable switch" and not, instead, have',basis='context_inferred',role='semantic_inference',note='Retains the rejected design alternative and the comparative selection without changing should into a binding prohibition.')
u10['complexity_flags']=['nested_component']

u11=unit(11,c(2),'> Not sure it makes sense to expose this until the wallet actually can do replacement...',role='quotation',speech='asserted',quotation='repeated',confidence='clear',alt='Repeats the earlier readiness objection, omitting the earlier emphasis markup; it is not a new endorsement by itself.')
u12=unit(12,c(2),'Right. I totally agree.',role='context',speech='reported_action',confidence='clear',alt='Agreement with the quoted readiness concern does not itself recognize a binding expectation.')
u13=unit(13,c(2),"I'm working on the replacement GUI process",role='context',speech='reported_action',confidence='clear',alt='Reports ongoing work, without supplying its completion or a patch for the full replacement process.')
u14=unit(14,c(2),'this can be reviewed already.',speech='asserted',force='unresolved',rationale='The author distinguishes current reviewability from the missing replacement GUI. The statement plausibly invites review, but technical can does not establish authorized discretion.',alt='A literal claim of practical reviewability rather than a normative permission or request. An invitation to review now is the pragmatic alternative.',uncertainty='The source supports a review action and timing, but whether can carries a recommendation, permission, or merely capability is unresolved.')
comp(u14,'I','reviewed',note='Retains the explicitly supplied passive review predicate.')
comp(u14,'Bdir','this',note='The passive subject is explicitly the patient of reviewed, so its action-target role is directly supplied. It refers to the current PR, not the unfinished GUI process.')
comp(u14,'Cex','already',note='The explicit timing adverb allows review at the present incomplete-feature stage. No authorization is inferred from can.')
u15=unit(15,c(2),'The timeline to get this into 0.13 is tough.',role='context',speech='asserted',confidence='clear',alt='States perceived scheduling pressure; it is not evidence of a release deadline rule or eventual inclusion in 0.13.')
relation(u11,u4,'quotes',[evu(u11),evu(u4)],'The supplied blockquote repeats the earlier comment\'s proposition, with emphasis markup removed.',basis='explicit')
relation(u4,u12,'uptake',[evu(u11),evu(u12)],'The author explicitly agrees immediately after quoting the readiness objection. This is assent to the specific concern, not verification of a governance duty.',basis='explicit')
recognition(u4,'endorsement','this_proposition',[evu(u11),evu(u12)],'The quotation identifies the concern that the author says they totally agree with; this remains technical/readiness assent, not expectation recognition.',basis='explicit')
relation(u14,u3,'clarifies',[evu(u3),evu(u13),evu(u14)],'The later statement by the same author makes the earlier non-delay preference more concrete: review can occur while the GUI process is being worked on.')

u16=unit(16,c(3),'> I\'m wondering if we should even have a "replaceable switch" and not, instead, have an "adaptive fee switch" (that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees-- and the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks])',role='quotation',speech='proposed',quotation='repeated',confidence='clear',alt='Repeats the adaptive-switch proposal without independently re-proposing it.')
u17=unit(17,c(3),'Yes. This might be a solution.',role='context',speech='reported_action',confidence='clear',alt='A tentative positive response to the quoted design, not a firm commitment or verification of a working solution.')
u18=unit(18,c(3),'I somehow was also trying to allow adding additional outputs (edit the transaction back in the sendcoins dialog).',speech='reported_action',force='nondeontic',itype='strategy_candidate',rationale='The author reports a personal implementation approach they had been trying. It supports an attributable strategy candidate without obligation or technical permission being inferred.',alt='Could be retained only as a historical engineering-work report rather than an ongoing strategy; the wording does not establish success.',uncertainty='Trying denotes an attempted approach, not completed behavior or institutional approval.')
comp(u18,'A','I')
comp(u18,'I','was also trying to allow',note='Preserves attempt status; allow refers to building technical functionality, not granting an institutional permission.')
comp(u18,'Bdir','adding additional outputs')
comp(u18,'Cex','(edit the transaction back in the sendcoins dialog)',note='The parenthetical directly specifies the intended workflow for adding outputs.')
u19=unit(19,c(3),'But maybe we should just focus on increasing the fees?',speech='question',alt='An open question about design scope rather than a settled instruction. It could concern the companion workflow more broadly, but it remains part of this feature discussion.',uncertainty='Maybe and the question form leave commitment unsettled; no implemented restriction is shown.')
comp(u19,'A','we')
comp(u19,'D','should')
comp(u19,'I','focus on',note='Keeps the essential preposition with focus; the action does not include its target.')
comp(u19,'Bdir','increasing the fees')
comp(u19,'Cex','just',note='Preserves the explicit restriction to fee increases rather than the broader additional-output functionality.')
relation(u16,u10,'quotes',[evu(u16),evu(u10)],'The supplied blockquote repeats the whole adaptive-fee alternative.',basis='explicit')
relation(u10,u17,'uptake',[evu(u16),evu(u17)],'The author responds to the exactly quoted adaptive-switch proposal by calling it a possible solution; this is tentative assent, not implementation.',basis='explicit')
recognition(u10,'endorsement','this_proposition',[evu(u16),evu(u17)],'The exact quote identifies the proposal; might be a solution makes the endorsement provisional and does not recognize an institutional expectation.',basis='explicit')

u20=unit(20,c(4),'you need to handle also making a child transaction of the original transaction for use in case the original confirms...',speech='asserted',force='unresolved',rationale='The engineering necessity can pragmatically guide how an additional-output implementation must be built. The record does not establish an institutional requirement, authorized rule, or enforcement claim.',alt='A pure technical dependency rather than a prescription. Need to refers to claimed algorithmic/workflow necessity, and may therefore be nondeontic.',uncertainty='The comment does not resolve technical necessity versus an instruction to implement; the general you is not identified as a particular contributor.')
comp(u20,'A','you',note='Preserves the explicit generic addressee, without identifying a contributor or maintainer.')
comp(u20,'D','need to',note='Lexical necessity is present, but institutional deontic force remains unresolved.')
comp(u20,'I','handle')
comp(u20,'Bdir','also making a child transaction of the original transaction for use in case the original confirms',note='Keeps the child transaction\'s original-transaction identity and intended confirmation contingency in the target rather than treating it as an institutional consequence.')
comp(u20,'Cac','when implementing the additional-output workflow','workflow for additional outputs',basis='context_inferred',role='semantic_inference',note='The preceding explanatory clause outside this unit supplies the technical workflow to which the handling requirement applies; the conditional formulation is inferred.')
u20['complexity_flags']=['nested_component']
u21=unit(21,c(4),'and if you do this multiple times there is a bit of exponential blowup in the number of versions you must compute.',role='context',speech='technical_description',confidence='clear',alt='Must compute concerns the described technical growth in transaction versions, not an independently established institutional obligation or sanction.')
relation(u18,u20,'uptake',[evu(u18),ev(c(4),'workflow for additional outputs is more complex because'),evu(u20)],'The additional-output workflow named in the reply corresponds to the author\'s attempted feature; the response describes a technical complication, not acceptance or enforcement.')
recognition(u18,'response','this_proposition',[evu(u18),ev(c(4),'workflow for additional outputs is more complex because'),evu(u20),evu(u21)],'The reply addresses the additional-output strategy through its confirmation contingency and scaling cost. It does not establish completion or recognized obligation.')

u22=unit(22,c(5),'Instead of the word "replacable" perhaps the word "updatable" or "amendable" would better express what the it\'ll do?',speech='question',parse='pragmatic',quotation='proposed_wording',alt='Could be read as a question about terminology, but it offers two specific replacement labels. The alternatives are disjunctive, not a demand to use both.',uncertainty='The edit action is inferred from comparative wording and perhaps; no final label choice or implementation is shown.')
comp(u22,'I','replace',u22['span']['quote'],basis='context_inferred',role='semantic_inference',note='The comparative wording offers an edit, but no literal replace imperative occurs.')
comp(u22,'Bdir','the word "replacable"','the word "replacable"',basis='context_inferred',role='semantic_inference',note='The instead-of phrase identifies the existing label; it becomes the target of the reconstructed replacement action.')
comp(u22,'Cex','with "updatable" or "amendable"','the word "updatable" or "amendable"',basis='context_inferred',role='semantic_inference',note='The literal candidate-label subject becomes the disjunctive replacement specification; no XOR or joint requirement is inferred.')
comp(u22,'Cex','to better express what it will do',"would better express what the it'll do",basis='context_inferred',role='semantic_inference',note='Preserves the stated descriptive purpose, including its tentative comparative character; the source typo is left intact in evidence.')
u22['presentation']['rationale']='The statement includes newly offered replacement labels in inline quotation marks; the original label is also quoted, but no earlier full proposition is being repeated.'
u23=unit(23,c(5),'doing the add output thing would be pretty interesting...',role='context',speech='asserted',confidence='clear',alt='Expresses interest in the additional-output feature, without a commitment to implement it.')
u24=unit(24,c(5),'though it would be nice to have a [send immediately] option which delays sending it, thus avoids having to do the extra just in case transactions if you amend with in the timeout. (and could also let you abort before it was initially set).',speech='proposed',rationale='A tentative technical design recommendation proposes an optional sending delay and associated capabilities. It is not an institutional permission for users or a committed implementation plan.',alt='May be exploratory product design rather than an actionable contribution prescription. The label send immediately and the stated delay are preserved together without resolving their apparent tension.',uncertainty='The precise option behavior, timing, and abort semantics remain underspecified; capability effects are predictions, not observed outcomes.')
comp(u24,'I','have')
comp(u24,'Bdir','a [send immediately] option which delays sending it',note='Keeps the supplied option label and its delaying behavior together, without silently correcting either.')
comp(u24,'Bdir,p','thus avoids having to do the extra just in case transactions if you amend with in the timeout. (and could also let you abort before it was initially set).',note='Retains the stated timeout-dependent benefit and possible pre-initial-send abort as properties of the offered option. Could is capability, not permission; the text\'s wording is not repaired.')
u24['complexity_flags']=['nested_component']
relation(u18,u23,'uptake',[evu(u18),evu(u23)],'The later expression of interest names the additional-output feature discussed earlier; it supplies technical interest rather than recognition of a duty.')
recognition(u18,'endorsement','this_proposition',[evu(u18),evu(u23)],'The feature is called interesting, a limited favorable response that does not demonstrate implementation or recognized obligation.')

u25=unit(25,c(6),'Hate to be that guy Jonas, but I believe "replaceab"... is the more accepted spelling, if you don\'t go with Greg\'s suggestion.',speech='asserted',parse='pragmatic',quotation='proposed_wording',alt='A spelling observation rather than an imperative. The likely relation to the preceding naming suggestion is plausible, but the packet does not explicitly identify Greg as the author of a particular supplied comment.',uncertainty='Only the prefix replaceab is supplied; the missing ending is not invented. Greg\'s referent and the exact final word remain unresolved.')
comp(u25,'A','Jonas','Jonas',basis='context_inferred',role='semantic_inference',note='The explicit vocative is interpreted as the addressee who would make the suggested edit; no alias-to-person mapping is assumed.')
comp(u25,'I','use',u25['span']['quote'],basis='context_inferred',role='semantic_inference',note='Reconstructs the editorial request from the assertion about accepted spelling.')
comp(u25,'Bdir','"replaceab"...','"replaceab"...',basis='context_inferred',role='semantic_inference',note='The literal subject of the spelling claim becomes the target form of the inferred use action. The visibly incomplete form is not expanded.')
comp(u25,'Cac',"if you don't go with Greg's suggestion",note='The fallback edit is expressly conditional on not choosing the other suggestion; its referent remains unresolved.')
u25['complexity_flags']=['unresolved_reference']
u25['presentation']['rationale']='The supplied occurrence offers a quoted spelling fragment as possible replacement wording. The ellipsis does not license completing the word.'
recognition(u22,'response','unresolved',[evu(u22),evu(u25)],'The conditional mention of Greg\'s suggestion may respond to these preceding alternatives, but neither the name mapping nor that referent is explicit in the packet.',basis='unresolved')
relation(u22,u25,'uptake',[evu(u22),evu(u25)],'A likely naming-discussion response is retained as unresolved: Greg\'s suggestion is not explicitly matched to this comment by supplied identity evidence.',basis='unresolved')

u26=unit(26,c(7),'Needs rebase.',speech='asserted',parse='pragmatic',rationale='An elliptical maintenance request plausibly asks for rebasing the current contribution. No supplied authority, enforcement claim, or recognized standing makes it a rule.',alt='May merely diagnose a technical prerequisite. The packet neither identifies the required target revision nor verifies a subsequent rebase.',uncertainty='The action is nominalized and the object omitted; the current PR is inferred from the source object association and body, without assigning an implementer.')
comp(u26,'I','rebase','rebase',basis='context_inferred',role='semantic_inference',note='Reconstructs the action from the nominalized rebase following Needs.')
comp(u26,'D','Needs',note='The explicit necessity wording supports the request reading, but the recommended action is not promoted to an authorized obligation.')
comp(u26,'Bdir','this PR','this PR',basis='context_inferred',role='context_reference',source=body,note='The omitted target is resolved to the PR that contains this comment. The outside-unit body anchor supplies its own this PR reference; source object metadata identifies #7819. This does not establish who must act.')
u27=unit(27,c(8),'Closing in favor of #8182 (included there).',role='context',speech='reported_action',confidence='clear',alt='Reports replacing this PR as the vehicle for the work and claims inclusion in #8182. It does not report integration into the repository or prove preservation of each suggestion.')
relation(u26,u27,'temporal',[evu(u26),evu(u27)],'The supplied source timestamps place the rebase comment before the closure report on 2016-06-09. Ordering alone does not show that the rebase request caused closure or that a rebase occurred.')

close_evidence=[ev('pr7819:metadata','"state": "closed"'),ev('pr7819:metadata','"closed_at": "2016-06-09T09:21:57+00:00"'),ev('pr7819:metadata','"merged_at": null'),ev('pr7819:metadata','"merged": false')]
for u in units:
    if u['record_role']=='statement':
        u['disposition_events'].append({'kind':'recorded_closed_unmerged','target':'broader_proposal','basis':'explicit','evidence':close_evidence,'rationale':'The supplied metadata records closure without merge of PR #7819, the broader contribution hosting this proposition. This does not establish rejection, withdrawal, implementation, or acceptance of the particular proposition, or the outcome of a successor.'})

reasons={
 body:'Exhaustively screened. The feature description and image URLs provide technical context; the readiness concern and stated non-delay review strategy are plausible institutional candidates. The reference to #7159 reports included refactoring commits, not a separate navigation imperative.',
 c(0):'Exhaustively screened. A tentative exposure-readiness objection can pragmatically guide whether the contribution should be exposed. The technical capability interpretation is retained.',
 c(1):'Exhaustively screened. Extracted independent red-style and exclamation-removal requests, the potentially misleading-label concern, a warning-treatment alternative, and the fully qualified adaptive-fee alternative. The visual-treatment parent is not double counted.',
 c(2):'Exhaustively screened. The repeated quote is not counted as a fresh statement; agreement, ongoing GUI work, and scheduling pressure are context. Current reviewability is an institutional candidate with unresolved capability/request force.',
 c(3):'Exhaustively screened. The repeated design quote and tentative assent are context/quotation. The author\'s attempted additional-output method and separate fee-only scope question are candidates.',
 c(4):'Exhaustively screened. The child-transaction necessity is retained as a candidate with a pure engineering alternative. The repeated-use scaling consequence, including must compute, is technical context, not an independent institutional sanction or duty.',
 c(5):'Exhaustively screened. Alternative terminology and the delayed-send option are separate candidates. Interest in additional outputs is a contextual response. Timeout avoidance and possible abort are properties/capabilities of the same option, not independent permissions.',
 c(6):'Exhaustively screened. The conditional spelling correction is an inferred editorial request. The supplied incomplete spelling and uncertain Greg reference remain unresolved.',
 c(7):'Exhaustively screened. The elliptical rebase diagnostic plausibly requests maintenance of the current PR; no authority or completed rebase is inferred.',
 c(8):'Exhaustively screened. A reported closure and inclusion claim supplies disposition context rather than a new prescription; it does not establish repository integration.',
 'pr7819:metadata':'Supplement screened for context under the selection design. Records #7819 closed without merge and its file list; context-only is not a claim that metadata can never bear institutional relevance.',
 'pr7819:supplement_metadata':'Supplement screened for context under the selection design. Confirms #7819 identity, retained head, and closed/unmerged status. Its merge_commit_sha is not integration evidence.',
 'pr8182:supplement_metadata':'Supplement screened for context under the selection design. The distinct successor #8182 is also recorded closed/unmerged; no patch or discussion proving inclusion or disposition of individual #7819 recommendations is supplied.',
 'pr7819:patch:0':'Supplement screened for context under the selection design, not exhaustive extraction. The retained UI label and unconfirmed-transaction tooltip provide technical feature evidence; Allow is a UI capability label, not established institutional authorization.',
 'pr7819:patch:1':'Supplement screened for context under the selection design, not exhaustive extraction. The retained confirmation code contains red styling and the original replacable text with an exclamation mark; the snapshot alone does not date changes or establish rejection of feedback.',
 'pr7819:patch:2':'Supplement screened for context under the selection design, not exhaustive extraction. Technical propagation of the optInRBF argument and flag is relevant implementation context, not evidence of authority or review uptake.',
 'pr7819:patch:3':'Supplement screened for context under the selection design, not exhaustive extraction. A defaulted optInRBF parameter documents retained technical code; ordinary method comments are not treated as governance instructions.',
 'pr7819:patch:4':'Supplement screened for context under the selection design, not exhaustive extraction. Transaction flags, sequence selection, and signing behavior are technical patch content; no rule recognition or integration follows from the diff.',
 'pr7819:patch:5':'Supplement screened for context under the selection design, not exhaustive extraction. Enumerated flags and a method signature define code objects, not institutional roles or constitutional authority.'}
screen=[]
for entry in p['entries']:
    us=[u for u in units if u['source_id']==entry['source_id']]
    screen.append({'source_id':entry['source_id'],'disposition':'candidate' if any(u['record_role']=='statement' for u in us) else ('empty' if not entry['text'] else 'context_only'),'reason':reasons[entry['source_id']],'unit_ids':[u['unit_id'] for u in us]})

outcomes=[
 {'claim':'The author reported closing PR #7819 in favor of #8182 and said the work was included there. The supplied #7819 metadata records closure on June 9, 2016 without a merge; the inclusion statement does not verify the content of #8182 or integration of either PR.','evidence':[evu(u27)]+close_evidence},
 {'claim':'The separately identified PR #8182 is also recorded closed without merge, with a closure date of December 6, 2016. Its non-null merge_commit_sha does not establish repository integration.','evidence':[ev('pr8182:supplement_metadata','"url": "https://github.com/bitcoin/bitcoin/pull/8182"'),ev('pr8182:supplement_metadata','"state": "closed"'),ev('pr8182:supplement_metadata','"merged": false'),ev('pr8182:supplement_metadata','"closed_at": "2016-12-06T10:15:00Z"'),ev('pr8182:supplement_metadata','"merged_at": null'),ev('pr8182:supplement_metadata','"merge_commit_sha": "1987a7a11a1a9513f2eca7a54c751178e2ef518c"')]},
 {'claim':'The supplied retained-head confirmation patch still contains red styling and the text This transaction is replacable (optin-RBF)! . This is evidence of that snapshot, not a dated response to the comments or a rejection of the proposed style, naming, and spelling changes.','evidence':[ev('pr7819:patch:1',"questionString.append(\"<hr /><span style='color:#aa0000;'>\");"),ev('pr7819:patch:1','questionString.append(tr("This transaction is replacable (optin-RBF)!"));'),evu(u6),evu(u7),evu(u22),evu(u25)]},
 {'claim':'The author explicitly agreed with the quoted exposure-readiness concern while reporting ongoing replacement-GUI work and saying the current PR could already be reviewed. The packet establishes that distinction in discussion, not a binding integration condition or completed replacement workflow.','evidence':[evu(u11),evu(u12),evu(u13),evu(u14)]}
]
mechanisms=[
 {'category':'review_coordination','claim':'The body states that the feature lacks an actual GUI replacement path and expresses a wish not to delay review. A participant questions exposure before replacement is available; the author quotes and agrees with that concern, then distinguishes ongoing GUI work from current reviewability and cites pressure around 0.13. This supports a discussion-level separation of review timing from feature readiness, without establishing a binding gate or eventual release inclusion.','evidence':[evu(u1),evu(u3),evu(u4),evu(u11),evu(u12),evu(u13),evu(u14),evu(u15)],'unit_ids':[u['unit_id'] for u in [u1,u3,u4,u11,u12,u13,u14,u15]],'alternative_explanation':'The exchange could be an informal technical usefulness discussion and scheduling preference, rather than application of a shared governance expectation.','status':'supported_sequence'},
 {'category':'reason_giving','claim':'The adaptive-fee switch proposal receives a quoted, tentative positive response. The author also reports trying additional-output editing and asks whether to focus only on fee increases. The next technical response describes the original-confirmation contingency and growth in versions required by repeated output additions. These correspondences support reason giving about design scope, but do not show that the fee-only question was accepted or implemented.','evidence':[evu(u10),evu(u16),evu(u17),evu(u18),evu(u19),ev(c(4),'workflow for additional outputs is more complex because'),evu(u20),evu(u21)],'unit_ids':[u['unit_id'] for u in [u10,u16,u17,u18,u19,u20,u21]],'alternative_explanation':'The scaling discussion may merely explain a technical cost while leaving both feature directions open; later interest in output additions is consistent with continued exploration.','status':'supported_sequence'},
 {'category':'scope_management','claim':'A rebase request is followed in the recorded source timestamps by the author\'s report of closing #7819 in favor of #8182, with a claim that the work is included there. The metadata confirms #7819 closed unmerged. This is consistent with moving work to a different PR, but does not verify a rebase or show that the request caused the closure.','evidence':[evu(u26),evu(u27)]+close_evidence,'unit_ids':[u26['unit_id'],u27['unit_id']],'alternative_explanation':'The author may already have planned the successor independently of the rebase comment; the supplied successor metadata does not verify the content transfer.','status':'consistent_with'}
]
annotation={'schema_version':'0.3','run_id':'F03_v03_r1','episode_id':'F03','packet_sha256':hashlib.sha256(packet_path.read_bytes()).hexdigest(),'entry_screening':screen,'units':units,'relations':relations,'episode_summary':{'observed_outcomes':outcomes,'mechanisms':mechanisms,'missing_evidence':[
'No full comment/body edit history or reliable reply threading is supplied; source timestamps cannot date every retained wording state.',
'Images referenced by the body are not rendered in the packet. Visual claims are limited to supplied prose and retained patches.',
'The retained #7819 patch is a head snapshot, not a sequence of revisions demonstrating responses to review.',
'No #8182 patch or discussion verifies the claimed inclusion, adoption of individual recommendations, or eventual integration elsewhere.',
'No supplied institutional authorization, enforcement chain, recognized obligation, or allocation of collective-choice powers supports a rule, sanction, constitutional, or epistemic claim.',
'The source does not explicitly map Greg to a particular supplied participant, complete the replaceab spelling fragment, or verify the requested rebase.',
'No repository integration is recorded for #7819 or #8182; network adoption is outside the supplied evidence.'
],'unresolved_questions':[
'Do readiness and reviewability statements express only technical judgments, or also case-specific expectations guiding contribution timing?',
'Is the child-transaction claim purely technical necessity or an indirect implementation requirement? The packet does not decide.',
'Did any recommendation affect another revision, the successor PR, or later work? Snapshot evidence does not resolve causal uptake or exact implementation.',
'Does Greg\'s suggestion refer to the preceding naming alternatives, and what exact spelling was intended beyond the supplied fragment?',
'Was moving to #8182 related to the rebase request, or did it reflect a separately planned continuation?'
]}}
(ROOT/'annotation.json').write_text(json.dumps(annotation,ensure_ascii=False,indent=2)+'\n')
(ROOT/'annotation.first_complete.json').write_bytes((ROOT/'annotation.json').read_bytes())
print(json.dumps({'entries':len(screen),'units':len(units),'statements':sum(u['record_role']=='statement' for u in units),'relations':len(relations),'packet_sha256':annotation['packet_sha256']}))
