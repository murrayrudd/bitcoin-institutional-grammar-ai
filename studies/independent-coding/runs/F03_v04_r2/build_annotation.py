import json, hashlib, copy
from pathlib import Path
ROOT=Path(__file__).resolve().parent
packet=json.loads((ROOT/'packet.json').read_text())
sources={e['source_id']:e for e in packet['entries']}
P='https://github.com/bitcoin/bitcoin/pull/7819'
Q='https://github.com/bitcoin/bitcoin/pull/8182'
B='pr7819:body'
def S(i): return f'pr7819:comments:{i}'
def ev(s,q, occurrence=0):
    text=sources[s]['text']; pos=-1
    for _ in range(occurrence+1): pos=text.index(q,pos+1)
    return {'source_id':s,'span':{'start':pos,'end':pos+len(q),'quote':q}}
def whole(s): return ev(s,sources[s]['text'])
def uniq(es):
    seen=set(); out=[]
    for e in es:
        k=(e['source_id'],e['span']['start'],e['span']['end'])
        if k not in seen: out.append(e);seen.add(k)
    return out
identity=[ev('pr7819:supplement_metadata',P)]
identity_q=[ev('pr8182:supplement_metadata',Q)]
units=[]
def unit(id,s,q,summary,role='statement',parse='literal',speech='proposed',force='recommendation',itype='undetermined',alt='',reason='',scope='case_specific',target='operational'):
    a=ev(s,q)
    non=role!='statement'
    u={'unit_id':id,'source_id':s,'span':a['span'],'parent_unit_id':None,
       'grammar':'not_institutional' if non else 'regulative','speech_act':speech,'scope':scope,'components':[],
       'institution':{'type':'not_applicable' if non else itype,'dispute_present':False,
        'rationale':'This record preserves a communicative act or technical context; it is not an additional institutional statement.' if non else reason,
        'evidence':[a],'recognition':[],'authority_evidence':[],
        'standing_profile':{k:'not_applicable' if non else 'none' for k in ('documentary','recognition','application')},
        'documentary_support':[],'application_evidence':[],'challenges':[],'type_alternatives':[]},
       'statement_target_level':'not_applicable' if non else target,
       'observed_action_level':'not_applicable' if role=='container' else 'operational',
       'level_rationale':'The visible act is ordinary contribution, technical review, or maintenance concerning this PR; no recurring governance procedure or decision-power allocation is being chosen.' if role!='container' else 'Structural grouping only.',
       'complexity_flags':['none'],'alternative_interpretation':alt,'confidence':'plausible' if parse=='pragmatic' else 'clear',
       'uncertainty_reason':reason if parse=='pragmatic' else '',
       'record_role':role,'parse_mode':parse,'deontic_force':'nondeontic' if non else force,'template_note':'',
       'presentation':{'quotation':'repeated' if role=='quotation' else 'none','markup':'plain','rationale':'Presentation is the supplied plain-text occurrence; no later formatting history is inferred.'},
       'disposition_events':[],
       'proposition':None if non else {'summary':summary,'decision_object_id':P,'domain':'Development and review of the proposed Bitcoin Core Qt opt-in-RBF interface in PR #7819.','time_scope': 'Retained occurrence associated with '+str(sources[s].get('timestamp'))+'; complete edit history is unavailable, so the timestamp does not independently date every retained word.','identity_evidence':identity,'qualifiers':[]},
       'target_level_alternatives':[],'observed_level_alternatives':[],
       'level_evidence':{'target_activity':summary if not non else 'Not applicable to this nonstatement record.','observed_activity':summary,'arrangement':'Ordinary PR contribution and review; no supplied source establishes a revised governing institution.','evidence':[a]}}
    units.append(u);return u

def comp(u,sym,text,q=None,basis='explicit',role='local',note='',source=None,gov=None,occur=0):
    s=source or u['source_id']; anchor=ev(s,q if q is not None else text,occur)
    g=gov if isinstance(gov,dict) else ev(u['source_id'],gov or u['span']['quote'])
    u['components'].append({'symbol':sym,'text':text,'basis':basis,'evidence':[anchor],'inference_note':note,'occurrence_role':role,'governing_span':g})

def qual(u,desc,s,q,attachment='scope_note',linked=None,why=None):
    u['proposition']['qualifiers'].append({'description':desc,'evidence':[ev(s,q)],'attachment':attachment,'linked_unit_id':linked,'rationale':why or 'This material qualification is carried explicitly in the proposition summary or this scope note.'})

def recognition(u,kind,target,s,q,why,mode='ordinary_assent',speaker='different_actor',basis='explicit',obj=P,ids=None):
    u['institution']['recognition'].append({'kind':kind,'target':target,'basis':basis,'evidence':[ev(s,q)],'rationale':why,'mode':mode,'speaker_relation':speaker,'independence_key':obj,'object_id':obj,'identity_evidence':ids or identity})

def challenge(u,s,q,why,aspect='content',target='this_proposition'):
    u['institution']['challenges'].append({'aspect':aspect,'target':target,'evidence':[ev(s,q)],'rationale':why})
    if target=='this_proposition': u['institution']['dispute_present']=True

def closure(u,obj=P,target='broader_proposal'):
    s='pr7819:metadata' if obj==P else 'pr8182:supplement_metadata'
    u['disposition_events'].append({'kind':'recorded_closed_unmerged','target':target,'basis':'explicit','evidence':[ev(s,'"state": "closed"'),ev(s,'"merged": false')],'rationale':'The supplied state and false merge status concern the identified PR. Closure does not demonstrate rejection of any individual recommendation, its rationale, or network adoption.','object_id':obj,'identity_evidence':identity if obj==P else identity_q})

u01=unit('F03-U01',B,'Adds a checkbox to the Send-Coins-Pannel (next to "Add Recipient") that allows to set the according nSequence to signal BIP125 RBF.',
 'The author offers adding a checkbox next to Add Recipient in the Send-Coins-Pannel to set nSequence for BIP125 RBF signaling.',parse='pragmatic',speech='technical_description',
 alt='The sentence can be retained solely as a technical description of the submitted patch, without an independently prescriptive request.',
 reason='The contribution description plausibly offers this specific edit for review. It neither establishes a social expectation nor supplies authority or a recurring institutional method.')
comp(u01,'I','add','Adds',note='The action verb is supplied; only its offered-edit force is reconstructed.')
comp(u01,'Bdir','a checkbox',note='The checkbox is the explicit object of Adds and remains the target of the offered edit.')
comp(u01,'Bdir,p','to the Send-Coins-Pannel (next to "Add Recipient") that allows to set the according nSequence to signal BIP125 RBF',note='The proposed checkbox retains its location and signaling behavior; these are properties of the same edit target.')
qual(u01,'The feature only signals opt-in-RBF; the PR does not supply a GUI method to replace a transaction.',B,'This PR does not include a way to actually replace a transaction with the GUI.')
qual(u01,'The retained body is associated with PR creation but may contain later edits; no sentence-level historical dating is claimed.',B,u01['span']['quote'])
closure(u01)
u01['disposition_events'].append({'kind':'withdrawn','target':'broader_proposal','basis':'context_inferred','evidence':[whole(S(8))],'rationale':'The PR author reports closing this submission in favor of #8182. This is withdrawal of this PR route, not repudiation of the checkbox idea.','object_id':P,'identity_evidence':identity})

c01=unit('F03-C01',B,'This PR does not include a way to actually replace a transaction with the GUI.', 'The author reports that this PR lacks an actual GUI replacement workflow.',role='context',speech='technical_description')
u02=unit('F03-U02',B,"So not sure if we want this without a GUI based replacement workflow (which I'm working on but it is a bigger chunk).",
 'The author is uncertain whether the group wants this checkbox proposal without a GUI replacement workflow, which the author reports working on as a larger task.',parse='pragmatic',speech='asserted',force='unresolved',
 alt='A statement of uncertainty about product usefulness, rather than a request to defer acceptance; neither acceptance nor a binding prerequisite is asserted.',
 reason='The sentence raises a plausible readiness condition for proceeding with this contribution. Its uncertain force and technical rationale do not establish a norm or rule.')
comp(u02,'A','we',basis='explicit',note='We is the expressed subject of want, retained as the deliberating actor; its membership is not supplied.')
comp(u02,'I','consider accepting','not sure if we want',basis='context_inferred',role='semantic_inference',note='The proposed conduct is reconstructed from uncertainty about wanting the offered PR, not an explicit acceptance verb.')
comp(u02,'Bdir','this checkbox proposal','this',basis='context_inferred',role='semantic_inference',note='This is the explicit object of want; its role as a target of acceptance and its checkbox referent are reconstructed from the adjacent proposal description.')
comp(u02,'Cac','without a GUI based replacement workflow',note='The absence of a workflow is the explicit circumstance under which wanting this proposal is questioned.')
qual(u02,"The author's uncertainty is retained, rather than recoded as an unconditional prohibition.",B,'not sure if we want this')
qual(u02,'The author says the replacement workflow is already being worked on and is a bigger chunk.',B,"which I'm working on but it is a bigger chunk")

u03=unit('F03-U03',B,"But I don't want to hold back review of this PR.",
 'The author expresses a personal strategy not to hold back review of this PR while the larger replacement workflow remains under development.',speech='asserted',force='nondeontic',itype='strategy_candidate',
 alt='This is a personal preference or invitation to review, rather than a committed plan; the timing is not authorization to integrate or expose the feature.',
 reason='The author articulates a case-specific approach to separating current review from the larger implementation task. No duty, authority, or shared norm is established.')
comp(u03,'A','I')
comp(u03,'I',"don't want to hold back",note='The negative preference is preserved in the action phrase; it is not a prohibition imposed on other actors.')
comp(u03,'Bdir','review of this PR')
qual(u03,'The distinction concerns review now, not integration or user exposure before a GUI workflow.',B,'review of this PR',attachment='component')
qual(u03,'Replacement workflow is a larger ongoing task.',B,"which I'm working on but it is a bigger chunk")
recognition(u03,'response','this_proposition',S(2),"I'm working on the replacement GUI process but this can be reviewed already.",'The same attributed author reiterates review now despite unfinished replacement work; this shows maintained commitment, not interpersonal recognition.',mode='same_actor_restatement',speaker='same_actor',basis='context_inferred')
u03['institution']['standing_profile']['recognition']='same_actor_only'

u04=unit('F03-U04',S(0),'Not sure it makes sense to expose this until the wallet actually _can_ do replacement...',
 'luke-jr questions exposing this feature before the wallet can actually perform replacement, plausibly recommending deferral until that capability exists.',parse='pragmatic',speech='asserted',
 alt='A technical usefulness concern with no request or socially expected conduct; the sentence does not expressly prohibit review or integration.',
 reason='A practical readiness recommendation is recoverable, but uncertainty and technical capability language do not establish institutional obligation, authority, or an accepted norm.')
comp(u04,'I','defer exposing','Not sure it makes sense to expose',basis='context_inferred',role='semantic_inference',note='Deferral is inferred from the unfavorable evaluation of exposure until capability exists; expose itself is supplied.')
comp(u04,'Bdir','this feature','this',basis='explicit',note='This is the explicit receiver of expose; body context resolves its referent to the proposed checkbox without changing that grammatical role.')
comp(u04,'Cac','until the wallet actually _can_ do replacement',note='The capability threshold limits the recommendation to defer exposure; can denotes technical ability, not institutional permission.')
qual(u04,'The literal stance is uncertain (Not sure), not an asserted binding prerequisite.',S(0),'Not sure it makes sense')
u04['institution']['type_alternatives']=['norm_candidate']
recognition(u04,'endorsement','this_proposition',S(2),'Right. I totally agree.','The author agrees after quoting the exposure concern. This is ordinary assent to a case-specific technical judgment; no attribution of governing status or binding expectation is explicit.')
challenge(u01,S(0),u04['span']['quote'],'The concern challenges exposing the checkbox without replacement capability, a premise or timing of the broader offered feature rather than every implementation detail.',aspect='premise',target='broader_proposal')

con=unit('F03-K01',S(1),"I don't think the confirmation window deserves red text and the bang for it.",'Grouping of the two independently executable requests to remove warning emphasis.',role='container',speech='other')
con['complexity_flags']=['compound']
u05=unit('F03-U05',S(1),"I don't think the confirmation window deserves red text",'gmaxwell plausibly recommends removing red text from the confirmation warning for this replaceable transaction.',parse='pragmatic',speech='asserted',
 alt='Aesthetic evaluation of warning emphasis rather than an edit request.',reason='A specific UI edit is pragmatically proposed; no supplied authority or accountability expectation selects an institutional type.')
u05['parent_unit_id']='F03-K01'
comp(u05,'I','remove',"don't think the confirmation window deserves",basis='context_inferred',role='semantic_inference',note='Negative evaluation of the current emphasis is reconstructed as removal.')
comp(u05,'Bdir','red text','red text',basis='context_inferred',role='semantic_inference',note='Red text is the object of deserves in the literal evaluation; its target role under remove is inferred.')
qual(u05,'The target is the confirmation-window treatment of the replaceable transaction, not a general ban on red text.',S(1),'the confirmation window deserves red text')

u06=unit('F03-U06',S(1),'and the bang for it.','gmaxwell also plausibly recommends removing the exclamation mark from that confirmation warning.',parse='pragmatic',speech='asserted',
 alt='Elliptical continuation of a single aesthetic evaluation; a coupled warning-emphasis edit would preserve the same action scope.',reason='This is the second edit target in the shared negative evaluation; it does not independently establish a social expectation or rule.')
u06['parent_unit_id']='F03-K01'
comp(u06,'I','remove',"I don't think the confirmation window deserves red text and the bang for it.",basis='context_inferred',role='shared_scope',note='The omitted predicate and negative stance are supplied by the enclosing sentence; the child does not assert an independent explicit remove verb.',gov=con['span']['quote'])
comp(u06,'Bdir','the bang',basis='context_inferred',role='semantic_inference',note='The bang is the conjoined object under deserves; treating it as a removal target changes its predicate role.')
qual(u06,'The bang belongs to the same confirmation-window warning as the red text.',S(1),con['span']['quote'],attachment='linked_unit',linked='F03-U05')

c02=unit('F03-C02',S(1),'Also "replaceable" there may have the user thinking that it\'s more replaceable than it is...', 'The wording may overstate replaceability to users, according to gmaxwell.',role='context',speech='technical_description')
u07=unit('F03-U07',S(1),"arguably it should be the non-replacable case that should get red text (because you can't update fees later).",
 'gmaxwell tentatively recommends red text for the non-replaceable case because fees cannot be updated later.',parse='pragmatic',speech='asserted',
 alt='A comparison explaining why the existing warning is inappropriate, without a firm request to add a different warning.',reason='A tentative case-specific UI recommendation is recoverable; technical fee-update limitations do not establish a governance rule.')
comp(u07,'D','should','should',occur=1,note='The modal governs get red text and carries advisory force; the earlier should be is not used as another duty.')
comp(u07,'I','mark in red','get red text',basis='context_inferred',role='semantic_inference',note='The suggested software behavior is reconstructed as an edit to mark the case; get is not an explicit developer action.')
comp(u07,'Bdir','the non-replacable case',basis='context_inferred',role='semantic_inference',note='The literal subject of should get becomes the target of the reconstructed marking action.')
qual(u07,'Arguably weakens the recommendation.',S(1),'arguably')
qual(u07,'The stated reason is inability to update fees later in the non-replaceable case.',S(1),"because you can't update fees later")

u08=unit('F03-U08',S(1),'I\'m wondering if we should even have a "replaceable switch" and not, instead, have an "adaptive fee switch" (that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees-- and the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks])',
 'gmaxwell tentatively proposes having an adaptive fee switch instead of a replaceable switch: compute N replacements with future locktimes and multiplicatively higher fees, with the fee line showing the stated block-dependent alternatives.',speech='asserted',
 alt='An exploratory design question rather than an asserted requirement; the codebook does not convert should into authority.',reason='A detailed design alternative is proposed once. It is a technical suggestion without a personal implementation commitment or socially enforced expectation.')
comp(u08,'A','we',note='The discussion group or developers are addressed as we; membership is not supplied.')
comp(u08,'D','should')
comp(u08,'I','have','have',occur=1,note='The second have supplies the replacement design action. The instead contrast is preserved in the object and qualifiers.')
comp(u08,'Bdir','an "adaptive fee switch"')
comp(u08,'Bdir,p','that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees-- and the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks]',note='These behaviors identify the suggested switch; they are not activation conditions on making the proposal.')
qual(u08,'The adaptive-fee switch is proposed instead of the replaceable switch; the proposal remains exploratory.',S(1),'I\'m wondering if we should even have a "replaceable switch" and not, instead, have an "adaptive fee switch"')
u08['complexity_flags']=['compound']
recognition(u08,'endorsement','this_proposition',S(3),'Yes. This might be a solution.','The author responds after quoting this design, but might preserves provisional technical assent; it is not expectation recognition.')

q1=unit('F03-Q01',S(2),'> Not sure it makes sense to expose this until the wallet actually can do replacement...', 'Repeated occurrence of the exposure-readiness concern.',role='quotation',speech='asserted')
q1['presentation']['rationale']='The Markdown blockquote repeats the already represented concern, with italic markup removed; it is not an independent endorsement.'
c03=unit('F03-C03',S(2),'Right. I totally agree.','The author agrees with the immediately quoted exposure concern.',role='context',speech='reported_action')
u09=unit('F03-U09',S(2),"I'm working on the replacement GUI process but this can be reviewed already.",
 'The author invites review of this PR now despite ongoing work on the replacement GUI process; the claim is about review timing.',parse='pragmatic',speech='asserted',
 alt='Can may assert practical reviewability rather than permission or a request; the sentence does not authorize integration or exposure.',reason='The source distinguishes current review from unfinished GUI work. A local invitation is plausible, but authority or a recurring norm is not supplied.')
comp(u09,'I','review','reviewed',note='The passive predicate explicitly supplies the review action; its invitation force is inferred.')
comp(u09,'Bdir','this PR','this',note='This is the receiver in the passive clause and remains Bdir under review; the PR referent follows from source identity and body.')
comp(u09,'Cex','already',note='Already makes current review timing material; it is not permission to release.')
qual(u09,'The author is still working on the replacement GUI process.',S(2),"I'm working on the replacement GUI process")
qual(u09,'The continuation states that the timeline for 0.13 is tough, not that 0.13 integration occurred.',S(2),'The timeline to get this into 0.13 is tough.')
c04=unit('F03-C04',S(2),'The timeline to get this into 0.13 is tough.','The author describes difficulty meeting the 0.13 timeline.',role='context',speech='asserted')

q2=unit('F03-Q02',S(3),'> I\'m wondering if we should even have a "replaceable switch" and not, instead, have an "adaptive fee switch" (that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees-- and the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks])', 'Repeated adaptive-fee-switch suggestion.',role='quotation',speech='asserted')
q2['presentation']['rationale']='The supplied Markdown blockquote repeats U08 and does not create an additional statement.'
c05=unit('F03-C05',S(3),'Yes. This might be a solution.','The author provisionally endorses the quoted adaptive-fee design as a possible solution.',role='context',speech='reported_action')
u10=unit('F03-U10',S(3),'I somehow was also trying to allow adding additional outputs (edit the transaction back in the sendcoins dialog).',
 'The author reports an attempted development approach allowing additional outputs by editing the transaction back in the sendcoins dialog.',speech='reported_action',force='nondeontic',itype='strategy_candidate',
 alt='A report of exploratory technical work can remain context rather than an institutional strategy; success or a future commitment is not established.',reason='An attributable personal development approach is explicitly described, without duty or permission. Candidate strategy denotes only that bounded approach.')
comp(u10,'A','I')
comp(u10,'I','was also trying to allow',note='Trying, rather than completed delivery, is retained.')
comp(u10,'Bdir','adding additional outputs')
comp(u10,'Cex','edit the transaction back in the sendcoins dialog',note='The parenthetical states the intended workflow for the output-adding approach.')
qual(u10,'This was an attempt (somehow was also trying), not proof of a completed feature.',S(3),'I somehow was also trying')

u11=unit('F03-U11',S(3),'But maybe we should just focus on increasing the fees?',
 'The author tentatively asks whether the group should focus only on increasing fees rather than the broader additional-output workflow.',speech='question',
 alt='An open design question rather than an adopted scope restriction.',reason='The question proposes narrower scope for current development. It does not choose a recurring governance arrangement or establish an institutional requirement.')
comp(u11,'A','we')
comp(u11,'D','should')
comp(u11,'I','focus')
comp(u11,'Bdir','increasing the fees',note='The sole action target follows focus on; the preposition does not create an indirect object.')
comp(u11,'Cex','just',note='Just bounds the work to fee increases in this alternative.')
qual(u11,'Maybe makes the narrowing tentative.',S(3),'maybe')
qual(u11,'The alternative scope is the preceding attempted additional-output workflow.',S(3),u10['span']['quote'],attachment='linked_unit',linked='F03-U10')

u12=unit('F03-U12',S(4),'you need to handle also making a child transaction of the original transaction for use in case the original confirms',
 'For the additional-output workflow, gmaxwell describes a technical method requiring provision for a child transaction of the original, for use if the original confirms.',speech='technical_description',force='nondeontic',itype='strategy_candidate',
 alt='This can remain technical explanatory context rather than an institutional strategy. Need denotes engineering necessity, not demonstrated duty; the conditional is about using the child, not waiting to create it.',
 reason='The passage supplies an articulated contingency method within the design discussion. Strategy-candidate status is limited to that method; no institutional authorization, obligation, or enforcement is established.')
comp(u12,'A','you',note='The generic designer/operator is expressed as you; no occupational status or named actor is inferred.')
comp(u12,'I','handle')
comp(u12,'Bdir','also making a child transaction of the original transaction for use in case the original confirms',note='The whole contingency task is the object of handle. The use-if-confirmed qualifier remains inside that task, not an activation condition on producing the child.')
qual(u12,'The method is specifically for a workflow that adds additional outputs.',S(4),'workflow for additional outputs is more complex')
qual(u12,'Need to expresses technical necessity in a complexity explanation, with no demonstrated institutional obligation.',S(4),'you need to handle')
qual(u12,'The child is for use if the original confirms; that condition does not assert that the child is only made after confirmation.',S(4),'for use in case the original confirms',attachment='component')
u12['institution']['type_alternatives']=['undetermined']
c06=unit('F03-C06',S(4),'and if you do this multiple times there is a bit of exponential blowup in the number of versions you must compute.',
 'gmaxwell predicts growth in computed versions if the additional-output process is repeated.',role='context',speech='technical_description',alt='Must compute is a technical workload claim, not an institutional obligation or announced sanction.')

u13=unit('F03-U13',S(5),'Instead of the word "replacable" perhaps the word "updatable" or "amendable" would better express what the it\'ll do?',
 'gmaxwell tentatively suggests using updatable or amendable instead of replacable to describe the feature more accurately.',parse='pragmatic',speech='question',
 alt='An informational question about wording adequacy rather than an instruction to edit; either alternative word remains permissible within the suggestion.',
 reason='The interrogative comparative wording plausibly requests a specific editorial change. It does not establish an accepted naming norm or authority.')
comp(u13,'I','use','would better express',basis='context_inferred',role='semantic_inference',note='Use is reconstructed from the evaluation of alternative words, not supplied as an imperative.')
comp(u13,'Bdir','the word "updatable" or "amendable"',basis='context_inferred',role='semantic_inference',note='The literal subject of would better express becomes the object of use under the edit-request parse.')
comp(u13,'Cex','Instead of the word "replacable"',note='The explicitly contrasted old wording identifies replacement scope; it is not a condition on future user behavior.')
qual(u13,'Perhaps and the question form make the recommendation tentative, with two alternative words.',S(5),'perhaps the word "updatable" or "amendable"')

c07=unit('F03-C07',S(5),'doing the add output thing would be pretty interesting...', 'gmaxwell expresses interest in the additional-output design.',role='context',speech='asserted')
recognition(u10,'endorsement','this_proposition',S(5),'doing the add output thing would be pretty interesting...','The later comment expresses interest in the same technical approach, not recognition of a governing expectation or verification that it was implemented.',basis='context_inferred')
u14=unit('F03-U14',S(5),'though it would be nice to have a [send immediately] option which delays sending it, thus avoids having to do the extra just in case transactions if you amend with in the timeout.',
 'gmaxwell suggests a [send immediately] option that delays sending and thereby avoids extra contingency transactions when the transaction is amended within the timeout.',speech='proposed',
 alt='An exploratory feature wish and technical prediction rather than a committed implementation plan; the apparent tension between the label and delayed behavior is left as supplied.',
 reason='A specific technical option is suggested, but no personal commitment, obligation, or socially expected conduct selects a stronger institutional type.')
comp(u14,'I','have')
comp(u14,'Bdir','a [send immediately] option which delays sending it',note='The proposed option includes its stated delay behavior; the bracketed label is retained without correcting it.')
qual(u14,'Avoiding extra contingency transactions is conditional on amendment within the timeout, not a claim that all such transactions are always avoided.',S(5),'thus avoids having to do the extra just in case transactions if you amend with in the timeout.')
qual(u14,'The supplied option label is [send immediately] although its described behavior delays sending.',S(5),'a [send immediately] option which delays sending it',attachment='component')

u15=unit('F03-U15',S(5),'(and could also let you abort before it was initially set).',
 'gmaxwell tentatively proposes that the same delayed-send option could also permit aborting before it was initially set, with the final timing wording unresolved.',parse='pragmatic',speech='proposed',
 alt='Could may describe a possible technical side effect rather than an additional requested feature. The text says set, and is not silently corrected to sent.',
 reason='An additional feature suggestion is recoverable, but capability wording does not establish institutionally authorized discretion or a binding expectation.')
comp(u15,'I','enable aborting','could also let you abort',basis='context_inferred',role='semantic_inference',note='A request to implement abort capability is inferred from exploratory could also let; it is not coded as institutional permission to users.')
comp(u15,'Bdir','the abort capability of the delayed-send option','could also let you abort',basis='context_inferred',role='semantic_inference',note='The implementation target is reconstructed. The shared option antecedent is supplied by the preceding clause, rather than an explicit object of this reconstructed predicate.')
comp(u15,'Cex','before it was initially set',note='The timing limit is retained exactly; the referent and meaning of initially set are not resolved beyond the surrounding transaction context.')
qual(u15,'The additional feature pertains to the preceding delayed-send option.',S(5),'a [send immediately] option which delays sending it',attachment='linked_unit',linked='F03-U14')
qual(u15,'Could also marks a tentative additional capability; the timing phrase initially set remains ambiguous.',S(5),'could also let you abort before it was initially set')
u15['complexity_flags']=['unresolved_reference']

u16=unit('F03-U16',S(6),sources[S(6)]['text'].rstrip('\n'),
 'kirkalx suggests that Jonas use the spelling fragment replaceab... if he does not choose Greg\'s suggestion; the fragment and conditional are retained rather than silently completed.',parse='pragmatic',speech='asserted',
 alt='A claim about accepted spelling rather than an editorial request. Jonas and Greg are textual names; no unsupplied identity mapping or exact intended full spelling is asserted.',
 reason='The addressed spelling observation plausibly requests a correction under a stated fallback condition. A conventional spelling claim is not sufficient evidence of an institutional norm for this project.')
comp(u16,'A','Jonas',basis='context_inferred',role='context_reference',note='Jonas is a vocative addressee. Assigning this addressee as the actor of the reconstructed correction is contextual, not the role of the literal subject I.')
comp(u16,'I','use','is the more accepted spelling',basis='context_inferred',role='semantic_inference',note='Use is inferred from the addressed spelling comparison.')
comp(u16,'Bdir','"replaceab"...','"replaceab"...',basis='context_inferred',role='semantic_inference',note='The truncated quoted spelling is the literal subject of is; its role as object of use is inferred. The full intended spelling is not invented.')
comp(u16,'Cac',"if you don't go with Greg's suggestion",note='The fallback explicitly activates only if the alternative suggestion is not chosen; the negation is retained.')
qual(u16,'The correction is conditional on not choosing Greg\'s suggestion; source context suggests a relation to the prior wording alternatives, but Greg\'s alias is not explicitly established.',S(6),"if you don't go with Greg's suggestion",attachment='component')
qual(u16,'The offered spelling is an ellipsis-bearing fragment, not a fully supplied replacement word.',S(6),'"replaceab"...',attachment='component')
u16['complexity_flags']=['unresolved_reference']

u17=unit('F03-U17',S(7),'Needs rebase.',
 'laanwj requests or expects a rebase of the current PR.',parse='pragmatic',speech='asserted',itype='norm_candidate',
 alt='A report of technical incompatibility rather than a request or accountability expectation; the actor responsible and any merge gate remain unstated.',
 reason='The elliptical maintenance demand expresses expected contribution work in this case. No supplied authority or enforcement basis establishes a rule candidate, and no response demonstrates that a rebase occurred.')
comp(u17,'I','rebase','rebase',basis='context_inferred',role='semantic_inference',note='The noun/complement in Needs rebase is reconstructed as the requested maintenance action.')
comp(u17,'Bdir','PR #7819',P,basis='context_inferred',role='context_reference',source='pr7819:supplement_metadata',note='The object is omitted in the utterance; the containing source identity and metadata identify this PR. Its Bdir role is inferred, not explicit in the local clause.')
u17['institution']['type_alternatives']=['undetermined']
qual(u17,'No actor, deadline, threat, merge condition, or authority attribution is supplied.',S(7),'Needs rebase.')
c08=unit('F03-C08',S(8),'Closing in favor of #8182 (included there).',
 'The PR author reports closing #7819 in favor of #8182 and says the work is included there.',role='context',speech='reported_action',alt='Included there reports cross-PR inclusion, not repository integration or verification that every suggestion was incorporated.')

relations=[]
def rel(a,b,t,es,why,basis='context_inferred',logic='not_applicable'):
    relations.append({'from_unit_id':a['unit_id'],'to_unit_id':b['unit_id'],'type':t,'basis':basis,'rationale':why,'evidence':es,'logic_scope':logic})
rel(u01,u04,'uptake',[ev(B,u01['span']['quote']),whole(S(0))],'The reviewer responds to the offered user-facing feature with a capability-readiness concern; this is a technical response, not demonstrated adoption.')
rel(q1,u04,'quotes',[ev(S(2),q1['span']['quote']),whole(S(0))],'The distinctive exposure concern is repeated as a blockquote; removed italics do not change its proposition.','explicit')
rel(u04,c03,'uptake',[ev(S(2),q1['span']['quote']),ev(S(2),c03['span']['quote'])],'The immediately quoted concern is followed by the author\'s explicit agreement.','explicit')
rel(u09,u03,'clarifies',[ev(B,u03['span']['quote']),ev(S(2),u09['span']['quote'])],'The same author restates that review may proceed during replacement-GUI development; this elaborates review timing without establishing exposure permission.')
rel(u05,u06,'AND',[ev(S(1),con['span']['quote'])],'The conjunction names both warning-emphasis removals under the shared negative evaluation.','explicit',logic='actions')
rel(u07,u05,'clarifies',[ev(S(1),u05['span']['quote']),ev(S(1),u07['span']['quote'])],'The alternative non-replaceable warning explains why red text is considered misplaced for replaceable transactions; it is not evidence that either edit was accepted.')
rel(q2,u08,'quotes',[ev(S(3),q2['span']['quote']),ev(S(1),u08['span']['quote'])],'The adaptive-fee-switch proposal is repeated in a blockquote, without a new independent proposition.','explicit')
rel(u08,c05,'uptake',[ev(S(3),q2['span']['quote']),ev(S(3),c05['span']['quote'])],'The qualified assent follows the repeated proposal and preserves might as provisional.','explicit')
rel(u10,u12,'uptake',[ev(S(3),u10['span']['quote']),whole(S(4))],'The explanation beginning Ah addresses the same additional-output workflow and describes the contingency burden; the response is inferred from the textual correspondence.')
rel(c06,u12,'clarifies',[whole(S(4))],'The conditional growth in computed versions elaborates the technical burden of the child-transaction method; it is not an institutional consequence or sanction.')
rel(u10,c07,'uptake',[ev(S(3),u10['span']['quote']),ev(S(5),c07['span']['quote'])],'The later add-output comment expresses interest in the author\'s proposed workflow, not recognition of an expectation.')
rel(u14,u12,'clarifies',[ev(S(4),u12['span']['quote']),ev(S(5),u14['span']['quote'])],'The delay option addresses the just-in-case transaction burden discussed earlier; an actual adopted workaround is not evidenced.')
rel(u14,u15,'AND',[ev(S(5),u14['span']['quote']),ev(S(5),u15['span']['quote'])],'And could also adds a tentative abort capability to the delay option; conjunction does not create a duty to implement both.','explicit',logic='actions')
rel(u17,c08,'temporal',[whole(S(7)),whole(S(8)),ev('pr7819:metadata','"closed_at": "2016-06-09T09:21:57+00:00"')],'Source timestamps place the rebase comment before the closing report on 2016-06-09. Chronology does not show that the rebase request caused closure.')

screening=[]
reasons={
 B:'Exhaustive focal screening: offered checkbox edit, uncertainty about proceeding without a replacement workflow, and a personal approach to allowing review are extracted. Missing GUI replacement is context. Refactoring inclusion and image links supply technical provenance, not separate prescriptions; images were not rendered.',
 S(0):'Exhaustive focal screening: the exposure-readiness concern is retained as a pragmatic candidate, with technical-evaluation alternative.',
 S(1):'Exhaustive focal screening: red-text removal, exclamation-mark removal, the alternative non-replaceable warning, and the detailed adaptive-fee-switch alternative are represented. Wording-risk explanation is context, not an additional explicit edit.',
 S(2):'Exhaustive focal screening: repeated blockquote and assent are nonstatement records; current reviewability is a pragmatic candidate. Ongoing GUI work and 0.13 time pressure remain qualifications/context, not implementation or integration claims.',
 S(3):'Exhaustive focal screening: quotation and provisional assent are separated from the personal additional-output approach and tentative fee-only focus.',
 S(4):'Exhaustive focal screening: the child-transaction contingency method is retained as a candidate with technical-context alternative. Conditional computational blowup and must compute describe engineering consequences, not a separate institutional duty or sanction.',
 S(5):'Exhaustive focal screening: alternate terminology, delayed sending, and abort capability are distinct candidates; interest in additional outputs is context. Timeout and originally supplied initially set wording are preserved.',
 S(6):'Exhaustive focal screening: conditional spelling correction is retained, including the incomplete spelling fragment, vocative addressee, and unresolved named-reference mapping.',
 S(7):'Exhaustive focal screening: elliptical rebase request is retained with technical-status alternative and no invented actor or authority.',
 S(8):'Exhaustive focal screening: closing and reported inclusion in #8182 are context and outcome evidence. A completed action report does not independently prescribe future conduct.',
 'pr7819:metadata':'Supplement screened as context: identifies #7819 and its closed, unmerged recorded status. File counts do not prove implementation of review recommendations. Supplemental screening is not exhaustive institutional extraction.',
 'pr7819:supplement_metadata':'Supplement screened as context: confirms #7819 identity, current archived status and retained head revision. A merge_commit_sha is not integration when merged is false. Supplemental screening is not a claim that metadata lacks institutional significance.',
 'pr8182:supplement_metadata':'Supplement screened as context: independently identifies #8182 and its later closed, unmerged status. It supplies no patch history or proof of which #7819 proposals were included. Supplemental scope is contextual, not exhaustive extraction.',
 'pr7819:patch:0':'Supplement screened as technical context: retained checkbox and tooltip patch describes opt-in-RBF behavior; the not-confirmed condition is a technical feature qualifier. No claim of exhaustive institutional extraction from supplemental code.',
 'pr7819:patch:1':'Supplement screened as technical context: retained head adds the checked-state path and red confirmation string with replacable and exclamation mark. It cannot establish chronology, acceptance of reviews, or integration.',
 'pr7819:patch:2':'Supplement screened as technical context: option passes from wallet model to transaction creation; no separate institutional interpretation is asserted. Context-only scope does not imply absence of institutional relevance.',
 'pr7819:patch:3':'Supplement screened as technical context: default optInRBF argument is false at the retained head. This technical API default is not automatically an institutional permission.',
 'pr7819:patch:4':'Supplement screened as technical context: transaction flags affect sequence and signing; only a retained head patch is supplied. Code conditionals are not recoded as governance rules.',
 'pr7819:patch:5':'Supplement screened as technical context: enum constants and method signatures define technical interfaces; constitutive institutional status does not follow from software definitions.'}
for entry in packet['entries']:
    us=[u for u in units if u['source_id']==entry['source_id']]
    disposition='candidate' if any(u['record_role']=='statement' for u in us) else 'empty' if not entry['text'].strip() else 'context_only'
    screening.append({'source_id':entry['source_id'],'disposition':disposition,'reason':reasons[entry['source_id']],'unit_ids':[u['unit_id'] for u in us]})

def outcome(parts):
    return {'claim':' '.join(p[0] for p in parts),'evidence':uniq([e for _,es in parts for e in es]),'claim_parts':[{'text':t,'evidence':es} for t,es in parts]}

def mechanism(category,parts,us,status,alternative):
    x=outcome(parts);x.update(category=category,unit_ids=[u['unit_id'] for u in us],status=status,alternative_explanation=alternative);return x

observed=[
 outcome([
  ('The author agreed with the quoted concern about exposing the feature before replacement was possible.',[ev(S(2),q1['span']['quote']),ev(S(2),c03['span']['quote'])]),
  ('The same response said replacement-GUI work was ongoing but the PR could already be reviewed, and described the 0.13 timeline as tough.',[ev(S(2),u09['span']['quote']),ev(S(2),c04['span']['quote'])])]),
 outcome([
  ('The retained #7819 patch adds a checkbox labeled Allow Replace-By-Fee, with a tooltip limiting replacement to an unconfirmed transaction.',[ev('pr7819:patch:0','+      <widget class="QCheckBox" name="optInRBF">'),ev('pr7819:patch:0','+        <string>Allow Replace-By-Fee</string>'),ev('pr7819:patch:0','+        <string>Signals that this transaction can be replaced with a transation paying higher fees (as long as the transaction is NOT confirmed).</string>')]),
  ('Its retained confirmation patch includes the red-color markup and This transaction is replacable (optin-RBF)! string.',[ev('pr7819:patch:1','+        questionString.append("<hr /><span style=\'color:#aa0000;\'>");'),ev('pr7819:patch:1','+        questionString.append(tr("This transaction is replacable (optin-RBF)!"));')]),
  ('The PR is recorded as closed and unmerged, so these retained proposed changes are not evidence of repository integration.',[ev('pr7819:metadata','"state": "closed"'),ev('pr7819:metadata','"merged": false')])]),
 outcome([
  ('The author reported closing #7819 in favor of #8182 and said the work was included there.',[whole(S(8)),ev('pr7819:supplement_metadata',P),ev('pr8182:supplement_metadata',Q)]),
  ('#7819 is recorded closed on 2016-06-09 with merged false.',[ev('pr7819:metadata','"closed_at": "2016-06-09T09:21:57+00:00"'),ev('pr7819:metadata','"state": "closed"'),ev('pr7819:metadata','"merged": false'),ev('pr7819:supplement_metadata',P)]),
  ('The separate #8182 record is also closed and unmerged, with a closure date of 2016-12-06.',[ev('pr8182:supplement_metadata',Q),ev('pr8182:supplement_metadata','"closed_at": "2016-12-06T10:15:00Z"'),ev('pr8182:supplement_metadata','"state": "closed"'),ev('pr8182:supplement_metadata','"merged": false')])])]
mechanisms=[
 mechanism('scope_management',[
  ('The author described a PR lacking a GUI replacement workflow and expressed a desire not to delay its review.',[ev(B,c01['span']['quote']),ev(B,u03['span']['quote'])]),
  ('A reviewer questioned exposing the feature before actual replacement capability; the author quoted that concern and agreed.',[whole(S(0)),ev(S(2),q1['span']['quote']),ev(S(2),c03['span']['quote'])]),
  ('The author nevertheless reiterated current reviewability while reporting ongoing GUI work and a difficult 0.13 timeline.',[ev(S(2),u09['span']['quote']),ev(S(2),c04['span']['quote'])])],
  [c01,u03,u04,q1,c03,u09,c04],'supported_sequence',
  'Review could already have been planned independently, as the body states. The exchange supports a distinction between review and feature exposure, not proof that the concern caused a release gate, integration decision, or new recurring procedure.'),
 mechanism('reason_giving',[
  ('The adaptive-fee-switch alternative specified future locktimes, multiplicatively higher fees, and a changing fee display; the author quoted it and provisionally called it a possible solution.',[ev(S(1),u08['span']['quote']),ev(S(3),q2['span']['quote']),ev(S(3),c05['span']['quote'])]),
  ('The author described trying additional outputs and asked whether to focus only on fees; the response explained a child-transaction contingency and growth in versions under repeated changes.',[ev(S(3),u10['span']['quote']),ev(S(3),u11['span']['quote']),whole(S(4))]),
  ('A later comment expressed interest in additional outputs and suggested delayed sending to avoid contingency transactions when amendments fall within the timeout, with a tentative abort capability.',[ev(S(5),c07['span']['quote']),ev(S(5),u14['span']['quote']),ev(S(5),u15['span']['quote'])])],
  [u08,q2,c05,u10,u11,u12,c06,c07,u14,u15],'supported_sequence',
  'These may be parallel design explorations rather than a convergent decision. In particular the fee-only question precedes the complexity explanation; the packet does not show that explanation caused narrowing or that any discussed alternative was adopted.'),
 mechanism('review_coordination',[
  ('A maintenance comment said Needs rebase.',[whole(S(7))]),
  ('The author subsequently reported closing the PR in favor of #8182 with the work included there; #7819 is recorded closed and unmerged.',[whole(S(8)),ev('pr7819:metadata','"closed_at": "2016-06-09T09:21:57+00:00"'),ev('pr7819:metadata','"state": "closed"'),ev('pr7819:metadata','"merged": false'),ev('pr8182:supplement_metadata',Q)])],
  [u17,c08],'consistent_with',
  'The source timestamps order the comments, but the replacement PR could have been planned independently. No source says the rebase request caused closure, that a rebase was performed, or that closure enforced a sanction.')]

annotation={'schema_version':'0.4','run_id':'F03_v04_r2','episode_id':'F03','packet_sha256':hashlib.sha256((ROOT/'packet.json').read_bytes()).hexdigest(),'entry_screening':screening,'units':units,'relations':relations,
 'episode_summary':{'observed_outcomes':observed,'mechanisms':mechanisms,
 'missing_evidence':[
  'Complete edit histories and reliable reply threading are absent; source timestamps do not establish the historical date of each retained sentence.',
  'No supplied source attributes rule-making authority, maintainer status, or an enforcement procedure to these participants.',
  'No governance document establishing authority, recurring norms, or documentary standing for these suggestions is supplied.',
  'PR #8182 has metadata but no implementation patch or discussion in this packet; reported inclusion does not identify which exact changes carried over.',
  'PR #7159 is mentioned only as the source of two refactoring commits; its implementation and disposition are not supplied.',
  'The linked screenshots were not rendered, and the retained #7819 head patch is not a complete change history.',
  'Neither record shows integration; no source supports network adoption or causal attribution of any code change to a review remark.'
 ],'unresolved_questions':[
  'Which remarks were intended as actionable edit requests rather than technical evaluations or exploratory questions?',
  'Was the exposure-readiness concern a proposed expectation, or only a shared judgment about feature usefulness? The evidence establishes ordinary assent, not governing status.',
  'Does Needs rebase express expected contributor conduct or merely technical status, and who was expected to act?',
  'What exact word was intended by replaceab..., and what precisely did before it was initially set mean?',
  'Which specific proposals, if any, were carried into #8182, and why did either PR close? The packet cannot settle these questions.'
 ]}}
(ROOT/'annotation.json').write_text(json.dumps(annotation,ensure_ascii=False,indent=2)+'\n')
first=ROOT/'annotation.first_complete.json'
if first.exists(): raise RuntimeError('First-complete output already exists; do not overwrite the freeze.')
first.write_bytes((ROOT/'annotation.json').read_bytes())
print(json.dumps({'entries':len(screening),'units':len(units),'statements':sum(u['record_role']=='statement' for u in units),'relations':len(relations),'packet_sha256':annotation['packet_sha256'],'first_complete_sha256':hashlib.sha256(first.read_bytes()).hexdigest()}))
