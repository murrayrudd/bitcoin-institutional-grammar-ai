import json, hashlib, copy
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path.cwd()
packet=json.loads(Path('packet.json').read_text())
entries={e['source_id']:e for e in packet['entries']}
PR='https://github.com/bitcoin/bitcoin/pull/7819'
PR2='https://github.com/bitcoin/bitcoin/pull/8182'

def ev(s,q=None,start=0):
    text=entries[s]['text']
    if q is None: q=text
    pos=text.index(q,start)
    return {'source_id':s,'span':{'start':pos,'end':pos+len(q),'quote':q}}

def uniq(es):
    seen=set();out=[]
    for e in es:
        k=(e['source_id'],e['span']['start'],e['span']['end'])
        if k not in seen:out.append(e);seen.add(k)
    return out

id7819=[ev('pr7819:supplement_metadata','"url": "https://github.com/bitcoin/bitcoin/pull/7819"')]
id8182=[ev('pr8182:supplement_metadata','"url": "https://github.com/bitcoin/bitcoin/pull/8182"')]
units=[]

def unit(n,s,q,role='statement',summary='',typ='undetermined',parse='literal',force='recommendation',speech='proposed',scope='case_specific',obj=PR,alt='',rationale='',uncertainty='',quotation='none',markup='plain',target='operational',observed='operational'):
    e=ev(s,q)
    statement=role=='statement'
    inst={
      'type':typ if statement else 'not_applicable','dispute_present':False,
      'rationale':rationale or ('A case-specific contribution proposal; no attributed institutional authorization or binding requirement is supplied.' if statement else 'This record preserves a communicative act or technical context, not an additional institutional proposition.'),
      'evidence':[e],'recognition':[],'authority_evidence':[],
      'standing_profile':dict.fromkeys(['documentary','recognition','application'],'none' if statement else 'not_applicable'),
      'documentary_support':[],'application_evidence':[],'challenges':[],'type_alternatives':[]}
    prop=None
    if statement:
        prop={'summary':summary,'decision_object_id':obj,'domain':'Bitcoin Core Qt wallet development and review in the supplied #7819 discussion','time_scope':('Retained PR body, created 2016-04-05 and subsequently updated; the date of this retained wording is not established.' if s=='pr7819:body' else 'Supplied occurrence recorded at '+entries[s]['timestamp']+'; complete edit history is unavailable.'),'identity_evidence':copy.deepcopy(id7819 if obj==PR else id8182 if obj==PR2 else []),'qualifiers':[]}
    u={'unit_id':f'F03-U{n:02d}','source_id':s,'span':e['span'],'parent_unit_id':None,'grammar':'regulative' if statement else 'not_institutional','speech_act':speech,'scope':scope,'components':[],'institution':inst,'statement_target_level':target if statement else 'not_applicable','observed_action_level':observed,'level_rationale':'The focal activity is a particular contribution, technical design choice, or review step. The observed act is ordinary development discussion, with no supplied change to recurring governance arrangements.' if statement else 'The observed act occurs in ordinary contribution review; this contextual record makes no institutional prescription.','complexity_flags':['none'],'alternative_interpretation':alt,'confidence':'plausible' if statement else 'clear','uncertainty_reason':uncertainty or ('Institutional interpretation is limited to this utterance; authority, adoption, and generality are not established.' if statement else ''),'record_role':role,'parse_mode':parse,'deontic_force':force if statement else 'nondeontic','presentation':{'quotation':quotation,'markup':markup,'rationale':'Presentation records the supplied occurrence; no edit history or unseen image is reconstructed.'},'disposition_events':[],'proposition':prop,'target_level_alternatives':[],'observed_level_alternatives':[],'level_evidence':{'target_activity':summary if statement else 'Not applicable: contextual or repeated occurrence.','observed_activity':('A contributor offers or discusses a specific wallet/review change.' if statement else 'A contributor supplies technical context, repeats earlier wording, endorses an idea, or reports a local action.'),'arrangement':'The supplied PR contribution and review discussion; no allocation of decision power or recurring procedural revision is evidenced.','evidence':[e]}}
    units.append(u);return u

def comp(u,symbol,text,q=None,basis='explicit',role='local',note='',source=None,govern=None):
    s=source or u['source_id']
    e=ev(s,q if q is not None else text,u['span']['start'] if s==u['source_id'] and role=='local' else 0)
    if govern is None: g={'source_id':u['source_id'],'span':copy.deepcopy(u['span'])}
    elif isinstance(govern,dict):g=govern
    else:g=ev(u['source_id'],govern,u['span']['start'])
    c={'symbol':symbol,'text':text,'basis':basis,'evidence':[e],'inference_note':note,'occurrence_role':role,'governing_span':g}
    u['components'].append(c);return c

def qual(u,description,es,attachment='scope_note',linked=None,rationale=None):
    u['proposition']['qualifiers'].append({'description':description,'evidence':es,'attachment':attachment,'linked_unit_id':linked,'rationale':rationale or 'This qualification is part of the bounded proposition and must survive alignment and interpretation.'})

def disp_closed(u):
    u['disposition_events'].append({'kind':'recorded_closed_unmerged','target':'broader_proposal','basis':'explicit','evidence':[ev('pr7819:metadata','"state": "closed"'),ev('pr7819:metadata','"merged": false'),ev('pr7819:metadata','"closed_at": "2016-06-09T09:21:57+00:00"')],'rationale':'These metadata concern #7819 as a whole. They establish closure without merge, not rejection or nonimplementation of every particular suggestion.','object_id':PR,'identity_evidence':copy.deepcopy(id7819)})

def rec(u,kind,target,es,rationale,basis='context_inferred',mode='ordinary_assent',speaker='different_actor',obj=PR):
    u['institution']['recognition'].append({'kind':kind,'target':target,'evidence':es,'rationale':rationale,'basis':basis,'mode':mode,'speaker_relation':speaker,'independence_key':PR if speaker in ['different_actor','same_actor'] else None,'object_id':obj,'identity_evidence':copy.deepcopy(id7819 if obj==PR else id8182 if obj==PR2 else [])})

def challenge(u,aspect,target,es,rationale):
    u['institution']['challenges'].append({'aspect':aspect,'target':target,'evidence':es,'rationale':rationale})
    u['institution']['dispute_present']=any(c['target']=='this_proposition' and c['aspect']!='unresolved' for c in u['institution']['challenges'])

b='pr7819:body'
u01=unit(1,b,'Adds a checkbox to the Send-Coins-Pannel (next to "Add Recipient") that allows to set the according nSequence to signal BIP125 RBF.',summary='The submitted #7819 patch adds a checkbox next to Add Recipient in the Send-Coins-Pannel to set nSequence for BIP125 RBF signaling; it does not supply a GUI transaction-replacement workflow.',speech='reported_action',force='nondeontic',alt='This can be retained solely as a technical report about the offered patch. The candidate parse captures the concrete implementation offered for review, not an institutional permission granted by the checkbox.',rationale='The PR offers a specific implementation. This is a plausible conduct/configuration candidate at the contribution layer, but the feature itself is technical and supplies no demonstrated social duty or authority.')
comp(u01,'I','Adds')
comp(u01,'Bdir','a checkbox')
comp(u01,'Cex','to the Send-Coins-Pannel (next to "Add Recipient")')
comp(u01,'Bdir,p','that allows to set the according nSequence to signal BIP125 RBF')
qual(u01,'The checkbox is beside Add Recipient and signals BIP125 RBF by setting nSequence.',[ev(b,'to the Send-Coins-Pannel (next to "Add Recipient") that allows to set the according nSequence to signal BIP125 RBF')],attachment='component')
qual(u01,'The offered PR does not provide a way to replace a transaction through the GUI.',[ev(b,'This PR does not include a way to actually replace a transaction with the GUI.')])
u01['institution']['application_evidence'].append({'status':'observed','target':'this_proposition','evidence':[ev('pr7819:patch:0','+      <widget class="QCheckBox" name="optInRBF">'),ev('pr7819:patch:0','+        <string>Allow Replace-By-Fee</string>'),ev('pr7819:patch:1','+        prepareStatus = model->prepareTransaction(currentTransaction, CoinControlDialog::coinControl, ui->optInRBF->isChecked());'),ev('pr7819:patch:1','+        prepareStatus = model->prepareTransaction(currentTransaction, NULL, ui->optInRBF->isChecked());'),ev('pr7819:patch:2','+        bool fCreated = wallet->CreateTransaction(vecSend, *newTx, *keyChange, nFeeRequired, nChangePosRet, strFailReason, coinControl, optInRBF ? CREATE_TX_RBF_OPT_IN : CREATE_TX_DEFAULT);'),ev('pr7819:patch:4','+                                              std::numeric_limits<unsigned int>::max() - ((flags & CREATE_TX_RBF_OPT_IN) ? 2 : 1) ));')],'rationale':'The retained unmerged head artifact demonstrates the checkbox, its checked-state wiring, and the sequence-setting branch. This is observed implementation in the proposed artifact only, not repository integration, BIP125 behavioral validation, or proof of the visual placement. The reported location is unverified by the clipped patch.'})
u01['institution']['standing_profile']['application']='observed'
challenge(u01,'content','this_proposition',[ev('pr7819:comments:0','Not sure it makes sense to expose this until the wallet actually _can_ do replacement...')],'The reviewer questions exposing this checkbox before replacement capability. The challenge concerns sequencing of the offered feature, not whether the patch technically contains a checkbox.')
disp_closed(u01)

u02=unit(2,b,"So not sure if we want this without a GUI based replacement workflow",summary='The PR author leaves unresolved whether to proceed with #7819 without a GUI-based replacement workflow.',parse='pragmatic',force='unresolved',speech='asserted',alt='This is an expression of uncertainty rather than a prescription; alternatively it tentatively recommends deferring exposure until a replacement GUI exists. Neither binding deferral nor unconditional approval is stated.',rationale='The utterance raises a candidate condition on proceeding with the proposal, but the author expressly withholds a conclusion. Type and force remain undetermined.')
comp(u02,'A','we',note='The explicitly supplied we is the actor of wanting the proposed feature; the inclusive actor set is unspecified.')
comp(u02,'I','proceed with','want',basis='context_inferred',role='semantic_inference',note='The literal verb is want. Proceeding with or accepting the PR is the bounded pragmatic decision reading; no integration authority is inferred.')
comp(u02,'Bdir','this [#7819]',q='this',note='This is the explicit object of want and remains the target under the proposed proceed-with reading; the containing PR identifies the referent.')
comp(u02,'Cac','without a GUI based replacement workflow')
qual(u02,'The speaker is not sure, so the GUI dependency is a suspended judgment rather than an established requirement.',[ev(b,'So not sure if we want this')])
qual(u02,'The author reports working on the larger GUI replacement workflow.',[ev(b,"which I'm working on but it is a bigger chunk")],attachment='linked_unit',linked='F03-U03')
qual(u02,'The author nevertheless does not want to delay review of this PR.',[ev(b,"But I don't want to hold back review of this PR.")],attachment='linked_unit',linked='F03-U04')
u02['complexity_flags']=['unresolved_reference']
disp_closed(u02)

u03=unit(3,b,"which I'm working on but it is a bigger chunk",summary='The author reports ongoing work on the GUI-based replacement workflow and characterizes that work as a bigger chunk.',typ='strategy_candidate',force='nondeontic',speech='reported_action',obj=None,alt='This can remain a contextual progress report rather than an institutional strategy. No completion commitment or deadline is supplied.',rationale='The attributed first-person work report supplies a personal implementation plan without a duty. Its institutional relevance is limited to explaining review and scope sequencing.',uncertainty='The separate replacement workflow has no established proposal identifier in the supplied passage; it is not automatically #8182.')
comp(u03,'A','I')
comp(u03,'I','working on')
comp(u03,'Bdir','a GUI based replacement workflow',q='a GUI based replacement workflow',basis='context_inferred',role='context_reference',source=b,note='The object of working on is the preceding relative-clause antecedent, not a local noun phrase. The antecedent lies outside this minimal plan span.')
qual(u03,'This is ongoing reported work, described as larger than the checkbox change; the statement supplies no completion date.',[ev(b,"I'm working on but it is a bigger chunk")])
u03['institution']['type_alternatives']=['undetermined']

u04=unit(4,b,"But I don't want to hold back review of this PR.",summary='The author intends not to hold back review of #7819 while the GUI replacement work remains separate.',typ='strategy_candidate',force='nondeontic',speech='asserted',alt='The same sentence can be read as an indirect invitation to reviewers to review now; that would add recommendation force and an inferred reviewer actor. The literal preferred parse retains the author’s stated intention.',rationale='A first-person intention about handling the current contribution is an attributable personal strategy, with no instruction that reviewers are obliged to act.')
comp(u04,'A','I')
comp(u04,'I',"don't want to hold back",note='The negative intention is retained within the action predicate, rather than converted to a lexical deontic.')
comp(u04,'Bdir','review of this PR')
qual(u04,'The negative is an intention not to delay review; it does not authorize integration of the standalone checkbox.',[ev(b,"don't want to hold back review of this PR")],attachment='component')
qual(u04,'The replacement GUI is larger ongoing work, and the author is unsure about proceeding without it.',[ev(b,"So not sure if we want this without a GUI based replacement workflow (which I'm working on but it is a bigger chunk).")])
rec(u04,'response','this_proposition',[ev('pr7819:comments:2','but this can be reviewed already.')],'The same author restates the distinction between replacement development and present review. This is maintained personal intent, not interpersonal expectation recognition.',mode='same_actor_restatement',speaker='same_actor')
u04['institution']['type_alternatives']=['undetermined']
disp_closed(u04)

c='pr7819:comments:0'
u05=unit(5,c,'Not sure it makes sense to expose this until the wallet actually _can_ do replacement...',summary='The reviewer tentatively recommends not exposing the checkbox in #7819 until the wallet can actually perform replacement.',parse='pragmatic',force='recommendation',speech='asserted',alt='A literal reading expresses technical/usability doubt and imposes no prescription. If treated as a conduct expectation, the condition could be a local proposed norm, but no binding release gate is established.',rationale='This is a tentative technical sequencing objection. A local norm reading is plausible, but a one-off feature recommendation without authority or demonstrated accountability is best left undetermined.')
comp(u05,'D','should not yet',q='Not sure it makes sense',basis='context_inferred',role='semantic_inference',note='The negative recommendation is inferred from the qualified objection, not from a lexical prohibition. The hedge is preserved.')
comp(u05,'I','expose')
comp(u05,'Bdir','this [the checkbox proposal]',q='this',note='This is the explicit target of expose even in the pragmatic negative-recommendation reading; the PR body supplies its referent.')
comp(u05,'Cac','until the wallet actually _can_ do replacement')
qual(u05,'The objection is hedged by Not sure; can denotes wallet capability, not institutional permission.',[ev(c,'Not sure it makes sense'),ev(c,'the wallet actually _can_ do replacement')])
qual(u05,'The stated condition is replacement capability; it does not say review must wait.',[ev(c,'to expose this until the wallet actually _can_ do replacement')],attachment='component')
u05['institution']['type_alternatives']=['norm_candidate']
rec(u05,'endorsement','this_proposition',[ev('pr7819:comments:2','> Not sure it makes sense to expose this until the wallet actually can do replacement...'),ev('pr7819:comments:2','Right. I totally agree.')],'The author quotes the objection and explicitly agrees. This establishes ordinary assent to the local technical judgment, not recognition of a governing institutional expectation.',basis='explicit')
disp_closed(u05)

c='pr7819:comments:1'
u06=unit(6,c,"I don't think the confirmation window deserves red text and the bang for it.",summary='The reviewer recommends avoiding red text and the exclamation mark for the replaceability indication in #7819’s confirmation window.',parse='pragmatic',force='recommendation',speech='asserted',alt='Literally this is an evaluation of warning prominence. The inferred edit is to remove both features; splitting the two formatting edits preserves the same proposal if the common target remains explicit.',rationale='This is a local interface-edit recommendation. It does not demonstrate a standing warning-style rule or socially shared requirement.')
comp(u06,'I','avoid',q="don't think the confirmation window deserves",basis='context_inferred',role='semantic_inference',note='Avoiding the styling is an inferred edit action from a negative evaluation, not the literal deserves predicate.')
comp(u06,'Bdir','red text and the bang',basis='context_inferred',role='semantic_inference',note='The literal complements of deserves become the targets of the inferred avoid action. Both styling elements remain recoverable.')
comp(u06,'Cex','in the confirmation window',q='the confirmation window',basis='context_inferred',role='semantic_inference',note='The literal subject becomes the location constraint on the inferred formatting edit.')
qual(u06,'The advice jointly concerns red text and the bang for the replaceability indication.',[ev(c,'red text and the bang for it')],attachment='component')
u06['complexity_flags']=['compound']
disp_closed(u06)

u07=unit(7,c,'Also "replaceable" there may have the user thinking that it\'s more replaceable than it is...',role='context',speech='asserted',alt='The warning about user interpretation can imply changing the label, but this span supplies the rationale rather than a distinct replacement wording. The explicit later naming suggestion is separately represented.')

u08=unit(8,c,"arguably it should be the non-replacable case that should get red text (because you can't update fees later).",summary='The reviewer tentatively recommends red text for the non-replacable case because fees cannot be updated later.',parse='pragmatic',force='recommendation',speech='proposed',alt='The literal clause assigns red text to a UI case; the conduct-layer parse reconstructs an edit. The statement is advisory and hedged, not an enforceable warning requirement.',rationale='The proposed alternative warning treatment is a case-specific technical recommendation with a stated usability rationale.')
comp(u08,'D','should',govern="arguably it should be the non-replacable case that should get red text (because you can't update fees later).")
comp(u08,'I','format',q='get red text',basis='context_inferred',role='semantic_inference',note='Formatting the case is the inferred developer action corresponding to the literal case getting red text.')
comp(u08,'Bdir','the non-replacable case',basis='context_inferred',role='semantic_inference',note='The literal subject of get becomes the target of the reconstructed format action.')
comp(u08,'Cex','red text',basis='context_inferred',role='semantic_inference',note='Red text specifies how the inferred formatting action is performed; it is the complement of get in the literal source.')
qual(u08,'The proposal is qualified by arguably and concerns the non-replacable case, with inability to update fees later supplied as the reason.',[ev(c,"arguably it should be the non-replacable case that should get red text (because you can't update fees later).")])
disp_closed(u08)

q9='I\'m wondering if we should even have a "replaceable switch" and not, instead, have an "adaptive fee switch" (that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees-- and the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks])'
u09=unit(9,c,q9,summary='The reviewer proposes considering an adaptive fee switch instead of a replaceable switch: precompute N replacements with future locktimes and multiplicatively higher fees, and show the fee schedule by block delay.',typ='strategy_candidate',force='recommendation',speech='proposed',alt='This can be classified undetermined as a tentative one-off design suggestion. Strategy_candidate captures the explicitly articulated adaptive-fee method, not an adopted policy or a general obligation.',rationale='The proposal articulates a reusable technical method for this wallet design choice. It lacks an attributed duty, permission, or decision authority.')
comp(u09,'A','we')
comp(u09,'D','should')
comp(u09,'I','have',q='have',govern=q9)
comp(u09,'Bdir','an "adaptive fee switch"')
comp(u09,'Bdir,p','that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees-- and the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks]')
qual(u09,'The adaptive fee switch is offered instead of the replaceable switch, not as a requirement to add both.',[ev(c,'a "replaceable switch" and not, instead, have an "adaptive fee switch"')])
qual(u09,'The method includes N future-locktime replacements, multiplicatively higher fees, and the stated fee-by-block schedule.',[ev(c,'that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees-- and the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks]')],attachment='component')
qual(u09,'I\'m wondering signals a tentative proposal rather than commitment or adoption.',[ev(c,"I'm wondering if")])
u09['complexity_flags']=['compound','nested_component']
u09['institution']['type_alternatives']=['undetermined']
rec(u09,'endorsement','this_proposition',[ev('pr7819:comments:3','> I\'m wondering if we should even have a "replaceable switch" and not, instead, have an "adaptive fee switch" (that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees-- and the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks])'),ev('pr7819:comments:3','Yes. This might be a solution.')],'The author quotes the method and calls it a possible solution. This is qualified ordinary assent, without evidence of institutional expectation recognition or implementation.',basis='explicit')
disp_closed(u09)

c='pr7819:comments:2'
u10=unit(10,c,'> Not sure it makes sense to expose this until the wallet actually can do replacement...',role='quotation',speech='asserted',quotation='repeated',alt='The quotation omits the original emphasis markup around can; it repeats the same qualified exposure objection and supplies no new endorsement by itself.')
u11=unit(11,c,'Right. I totally agree.',role='context',speech='reported_action',alt='The agreement is explicit but its institutional significance remains limited to ordinary assent to the immediately quoted technical sequencing objection.')
u12=unit(12,c,"I'm working on the replacement GUI process",summary='The author reports working on the replacement GUI process.',typ='strategy_candidate',force='nondeontic',speech='reported_action',obj=None,alt='This may be retained as a progress report rather than a strategy statement. It restates the author’s own work, not a separate interpersonal recognition event.',rationale='The attributable first-person work report identifies a personal development plan without an obligation.',uncertainty='The source does not identify a PR for the replacement GUI process. #8182 is not retroactively assigned to this work.')
comp(u12,'A','I')
comp(u12,'I','working on')
comp(u12,'Bdir','the replacement GUI process')
u12['institution']['type_alternatives']=['undetermined']

u13=unit(13,c,'but this can be reviewed already.',summary='The author indicates that #7819 can be reviewed now while the replacement GUI process is still being developed.',parse='pragmatic',force='recommendation',speech='asserted',alt='Can may simply assert technical readiness for review; it does not establish institutional permission. The pragmatic invitation to review now is preferred because it directly answers the exposure concern and repeats the stated intention not to hold back review.',rationale='This is local review coordination. The readiness claim plausibly invites review, but no review duty, authority, or enduring rule is supplied.')
comp(u13,'I','review',q='reviewed',note='The passive explicitly supplies the review action; reconstructed invitation force does not make the review verb inferred.')
comp(u13,'Bdir','this [#7819]',q='this',note='This is the explicit patient of the passive reviewed predicate and remains its target in the pragmatic invitation; the PR is resolved contextually without changing the role.')
comp(u13,'Cex','already')
qual(u13,'Can is readiness/capability wording, not an explicit deontic granting permission.',[ev(c,'can be reviewed already')])
qual(u13,'Review is distinguished from exposing a GUI feature before replacement capability.',[ev(c,'> Not sure it makes sense to expose this until the wallet actually can do replacement...'),ev(c,"I'm working on the replacement GUI process")])
qual(u13,'The author describes the timeline for 0.13 as tough, rather than promising inclusion in that release.',[ev(c,'The timeline to get this into 0.13 is tough.')],attachment='linked_unit',linked='F03-U14')
disp_closed(u13)
u14=unit(14,c,'The timeline to get this into 0.13 is tough.',role='context',speech='asserted',alt='This is scheduling context, not a mandatory deadline or evidence of release inclusion.')

c='pr7819:comments:3'
q15='> I\'m wondering if we should even have a "replaceable switch" and not, instead, have an "adaptive fee switch" (that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees-- and the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks])'
u15=unit(15,c,q15,role='quotation',speech='proposed',quotation='repeated',alt='The repeated adaptive-fee proposal is linked to its original occurrence; it is not a second independent proposal or endorsement.')
u16=unit(16,c,'Yes. This might be a solution.',role='context',speech='reported_action',alt='This is tentative endorsement of the quoted design, not commitment to implement it.')
u17=unit(17,c,'I somehow was also trying to allow adding additional outputs (edit the transaction back in the sendcoins dialog).',summary='The author reports having tried to allow additional outputs by editing the transaction back in the sendcoins dialog.',typ='strategy_candidate',force='nondeontic',speech='reported_action',obj=None,alt='This is an exploratory work report that could remain context. It does not establish that the feature works, was adopted, or must remain in scope.',rationale='The attributable attempt supplies an explicit personal implementation method; no obligatory expectation or authorized rule is evidenced.',uncertainty='The planned replacement workflow has no established proposal identity. The tentative and past-progressive wording does not establish completion.')
comp(u17,'A','I')
comp(u17,'I','trying to allow')
comp(u17,'Bdir','adding additional outputs')
comp(u17,'Cex','edit the transaction back in the sendcoins dialog')
qual(u17,'Somehow was also trying describes an exploratory earlier attempt, with transaction editing in the sendcoins dialog as its method.',[ev(c,'somehow was also trying'),ev(c,'edit the transaction back in the sendcoins dialog')])
u17['institution']['type_alternatives']=['undetermined']
rec(u17,'response','this_proposition',[ev('pr7819:comments:4','Ah. workflow for additional outputs is more complex because you need to handle also making a child transaction of the original transaction for use in case the original confirms...')],'The response addresses the additional-output workflow with a technical complexity explanation; it is neither institutional expectation recognition nor proof that the attempt succeeded.',mode='other',obj=None)

u18=unit(18,c,'But maybe we should just focus on increasing the fees?',summary='The author tentatively proposes limiting the immediate replacement-workflow focus to increasing fees.',force='recommendation',speech='question',obj=None,alt='The question may only invite design discussion, without committing to exclude additional outputs. A strategy reading of narrowed development scope is also plausible.',rationale='This is a hedged scope-prioritization suggestion, with no standing obligation or implemented decision evidenced.',uncertainty='The exact workflow proposal identifier and whether just excludes all additional-output work remain unestablished.')
comp(u18,'A','we')
comp(u18,'D','should')
comp(u18,'I','focus on')
comp(u18,'Bdir','increasing the fees')
comp(u18,'Cex','just')
qual(u18,'Maybe and the question form preserve a tentative suggestion; just restricts the proposed focus to fee increases.',[ev(c,'maybe we should just focus on increasing the fees?')])
u18['institution']['type_alternatives']=['strategy_candidate']

c='pr7819:comments:4'
q19='you need to handle also making a child transaction of the original transaction for use in case the original confirms...'
u19=unit(19,c,q19,summary='For an additional-output workflow, the reviewer says one needs to handle making a child transaction of the original transaction for use if the original confirms.',typ='strategy_candidate',force='nondeontic',speech='technical_description',obj=None,alt='This is technical workflow necessity and may be context only. A local implementation requirement is plausible, but need does not itself establish institutional obligation or enforcement.',rationale='The passage articulates an implementation method and its technical contingency. Strategy_candidate preserves that method without promoting the technical necessity into a rule.',uncertainty='No institutional authority or binding development obligation is supplied. The replacement workflow has no established separate proposal identifier.')
comp(u19,'A','you')
comp(u19,'I','handle')
comp(u19,'Bdir','also making a child transaction of the original transaction')
comp(u19,'Cex','for use in case the original confirms')
qual(u19,'The method specifically concerns the additional-output workflow.',[ev(c,'workflow for additional outputs')])
qual(u19,'Need is technical necessity in this explanation; the child transaction is for use if the original confirms.',[ev(c,'you need to handle'),ev(c,'for use in case the original confirms')])
qual(u19,'Repeating this method is said to cause a bit of exponential growth in versions to compute.',[ev(c,'and if you do this multiple times there is a bit of exponential blowup in the number of versions you must compute.')],attachment='linked_unit',linked='F03-U20')
u19['institution']['type_alternatives']=['undetermined']
u20=unit(20,c,'and if you do this multiple times there is a bit of exponential blowup in the number of versions you must compute.',role='context',speech='technical_description',alt='Must compute describes an asserted engineering consequence, not a sanction or an attributable institutional command. No O relation is warranted.')

c='pr7819:comments:5'
q21='Instead of the word "replacable" perhaps the word "updatable" or "amendable" would better express what the it\'ll do?'
u21=unit(21,c,q21,summary='The reviewer tentatively suggests replacing the label replacable with updatable or amendable to better convey the feature’s behavior.',parse='pragmatic',force='recommendation',speech='question',quotation='proposed_wording',alt='Literally the speaker asks which label better expresses behavior. The implied edit preserves both proposed labels as alternatives, without inferring exclusive choice beyond the single-word label context.',rationale='This is a one-off wording recommendation with a technical communicative purpose; no naming rule or shared institutional norm is established.')
comp(u21,'I','use',q='would better express',basis='context_inferred',role='semantic_inference',note='Use is reconstructed from a comparative question about alternative wording; it is not a verb supplied in this occurrence.')
comp(u21,'Bdir','the word "updatable" or "amendable"',basis='context_inferred',role='semantic_inference',note='These literal subjects of express become objects of the reconstructed use action. Both alternatives are retained.')
comp(u21,'Cex','Instead of the word "replacable"')
qual(u21,'Perhaps and the question form make the wording tentative; updatable and amendable are alternatives.',[ev(c,'perhaps the word "updatable" or "amendable"')])
qual(u21,'The offered purpose is to better express what the feature does; the earlier user-misunderstanding concern is context, not an established general naming standard.',[ev(c,"would better express what the it'll do?"),ev('pr7819:comments:1','Also "replaceable" there may have the user thinking that it\'s more replaceable than it is...')])
u21['complexity_flags']=['compound']
disp_closed(u21)
u22=unit(22,c,'doing the add output thing would be pretty interesting...',role='context',speech='asserted',alt='This expresses qualified interest in the proposed feature; it is not an expectation or an independent implementation commitment.')

q23='though it would be nice to have a [send immediately] option which delays sending it, thus avoids having to do the extra just in case transactions if you amend with in the timeout. (and could also let you abort before it was initially set).'
u23=unit(23,c,q23,summary='The reviewer suggests a [send immediately] option that delays sending, avoids extra contingency transactions if amended within the timeout, and could allow aborting before it was initially set.',force='recommendation',speech='proposed',obj=None,alt='This can be treated as a technical workflow idea rather than an institutional statement, or as a strategy method for delayed sending. The apparently conflicting label and delay are retained exactly without repair.',rationale='This is a tentative feature suggestion with explicit technical purposes. No socially expected conduct or authorized permission is supplied.',uncertainty='The source’s option label says send immediately while its description says it delays sending. The precise intended UI behavior and proposal identity remain unresolved.')
comp(u23,'I','have')
comp(u23,'Bdir','a [send immediately] option which delays sending it')
qual(u23,'The label [send immediately] and its delaying behavior are both retained as supplied.',[ev(c,'a [send immediately] option which delays sending it')],attachment='component')
qual(u23,'Avoiding extra contingency transactions is conditional on amending within the timeout.',[ev(c,'thus avoids having to do the extra just in case transactions if you amend with in the timeout.')])
qual(u23,'Aborting before it was initially set is described as an additional possibility, not an institutional permission.',[ev(c,'(and could also let you abort before it was initially set).')])
u23['complexity_flags']=['compound','unresolved_reference']
u23['institution']['type_alternatives']=['strategy_candidate']

c='pr7819:comments:6'
q24='Hate to be that guy Jonas, but I believe "replaceab"... is the more accepted spelling, if you don\'t go with Greg\'s suggestion.'
u24=unit(24,c,q24,summary='The commenter suggests that Jonas use the more accepted spelling beginning replaceab... if he does not use Greg’s alternative-label suggestion.',parse='pragmatic',force='recommendation',speech='asserted',quotation='proposed_wording',alt='This could be a factual spelling observation rather than an edit request. A localized norm-candidate reading is possible because the commenter invokes accepted usage, but that does not establish a project naming rule.',rationale='A conditional editorial correction is inferred from the addressed spelling comment. Accepted spelling supplies a convention claim, not attributed institutional authority.')
comp(u24,'A','Jonas',basis='context_inferred',role='context_reference',note='Jonas is an explicit vocative, not the grammatical actor of an expressed use predicate. The addressee is inferred as actor of the proposed correction; no occupational role is assumed.')
comp(u24,'I','use',q='is the more accepted spelling',basis='context_inferred',role='semantic_inference',note='Use is the reconstructed editorial action rather than the literal belief/identity assertion.')
comp(u24,'Bdir','the spelling beginning "replaceab"...',q='"replaceab"...',basis='context_inferred',role='semantic_inference',note='The quoted incomplete stem is the subject of the literal spelling claim and becomes the target under use. No absent full spelling is invented.')
comp(u24,'Cac',"if you don't go with Greg's suggestion")
qual(u24,'The correction applies only if Greg’s alternative labels are not chosen.',[ev(c,"if you don't go with Greg's suggestion")],attachment='component')
qual(u24,'The source gives the incomplete spelling "replaceab"... and attributes the assessment to I believe.',[ev(c,'I believe "replaceab"... is the more accepted spelling')])
u24['institution']['type_alternatives']=['norm_candidate']
disp_closed(u24)

c='pr7819:comments:7'
u25=unit(25,c,'Needs rebase.',summary='The reviewer implicitly requests rebasing #7819.',parse='pragmatic',force='recommendation',speech='asserted',alt='This can be a technical status diagnosis rather than a request. Needs could suggest necessity, but neither an institutional obligation nor the actor’s decision authority is established.',rationale='The terse review comment plausibly requests a maintenance action on the current contribution. A local expectation reading is possible, but one-off technical necessity does not by itself select an institutional type.')
comp(u25,'I','rebase',basis='context_inferred',role='semantic_inference',note='Rebase is supplied elliptically after needs; interpreting it as an action requested from a contributor reconstructs the predicate.')
comp(u25,'Bdir','#7819',q='Needs rebase.',basis='context_inferred',role='context_reference',note='The omitted object is inferred from the comment’s containing PR and its canonical identity metadata. No object term is explicitly present in the clause.')
qual(u25,'The actor is omitted and is not reconstructed from the reviewer’s alias; the claimed need may be technical.',[ev(c,'Needs rebase.')])
u25['institution']['type_alternatives']=['norm_candidate']
disp_closed(u25)

c='pr7819:comments:8'
u26=unit(26,c,'Closing in favor of #8182 (included there).',role='context',speech='reported_action',alt='The report establishes author-stated closure and transfer/inclusion, not a rejection of the technical rationale or a merge into the repository. The object of included there is inferred as this PR’s content; the exact transferred patch is unverified.')

relations=[]
def rel(a,b,t,rationale,es,basis='context_inferred',logic='not_applicable'):
    relations.append({'from_unit_id':a['unit_id'],'to_unit_id':b['unit_id'],'type':t,'basis':basis,'rationale':rationale,'evidence':es,'logic_scope':logic})

rel(u05,u01,'challenges','The sequencing objection targets exposing the checkbox described in the PR body, while leaving open review and later development.',[ev('pr7819:comments:0'),ev('pr7819:body',u01['span']['quote'])])
rel(u10,u05,'quotes','The response reproduces the exposure objection, with emphasis markup omitted.',[ev(u10['source_id'],u10['span']['quote']),ev(u05['source_id'],u05['span']['quote'])],basis='explicit')
rel(u05,u11,'uptake','The author expressly agrees after quoting the reviewer’s objection; this response is ordinary assent, not proof of a release rule.',[ev(u10['source_id'],u10['span']['quote']),ev(u11['source_id'],u11['span']['quote'])],basis='explicit')
rel(u13,u05,'clarifies','The author agrees on exposure but distinguishes review now from waiting for replacement functionality.',[ev(u10['source_id'],u10['span']['quote']),ev(u11['source_id'],u11['span']['quote']),ev(u13['source_id'],u13['span']['quote'])])
rel(u13,u04,'clarifies','The later comment restates the author’s intention not to hold back review, now as a review-readiness claim.',[ev(u04['source_id'],u04['span']['quote']),ev(u13['source_id'],u13['span']['quote'])])
rel(u12,u03,'clarifies','The author’s comment repeats ongoing work on the same replacement GUI process; this is not independent support for an expectation.',[ev(u03['source_id'],u03['span']['quote']),ev('pr7819:body','a GUI based replacement workflow'),ev(u12['source_id'],u12['span']['quote'])])
rel(u08,u06,'clarifies','The proposed non-replacable-case warning provides the alternative target for the red-text treatment criticized for replaceability.',[ev(u06['source_id'],u06['span']['quote']),ev(u08['source_id'],u08['span']['quote'])])
rel(u15,u09,'quotes','The comment reproduces the adaptive-fee proposal before responding.',[ev(u15['source_id'],u15['span']['quote']),ev(u09['source_id'],u09['span']['quote'])],basis='explicit')
rel(u09,u16,'uptake','The author calls the quoted design a possible solution, without committing to implement it.',[ev(u15['source_id'],u15['span']['quote']),ev(u16['source_id'],u16['span']['quote'])],basis='explicit')
rel(u18,u17,'challenges','The author questions the scope of his own additional-output attempt by proposing just increasing fees; this is a tentative scope tension, not a withdrawal.',[ev(u17['source_id'],u17['span']['quote']),ev(u18['source_id'],u18['span']['quote'])])
challenge(u17,'content','this_proposition',[ev(u18['source_id'],u18['span']['quote'])],'The same author tentatively questions continuing the additional-output scope by asking whether to focus just on fees. This is a challenge to scope, not evidence that the earlier work did not occur.')
rel(u17,u19,'uptake','The reviewer responds to the additional-output workflow with the child-transaction contingency; shared terminology supports correspondence, not formal reply-thread certainty.',[ev(u17['source_id'],u17['span']['quote']),ev('pr7819:comments:4','Ah. workflow for additional outputs is more complex because '+q19)])
rel(u20,u19,'clarifies','The subsequent technical clause qualifies the proposed contingency method by its asserted growth in computation after repeated use.',[ev(u19['source_id'],u19['span']['quote']),ev(u20['source_id'],u20['span']['quote'])])
rel(u21,u07,'clarifies','The later naming suggestion supplies possible wording that addresses the earlier concern about how replaceability is understood; this link is contextual rather than expressly attributed.',[ev(u21['source_id'],u21['span']['quote']),ev(u07['source_id'],u07['span']['quote'])])
rel(u22,u17,'clarifies','The reviewer’s expressed interest concerns the author’s additional-output idea; it does not demonstrate adoption.',[ev(u22['source_id'],u22['span']['quote']),ev(u17['source_id'],u17['span']['quote'])])
rel(u23,u19,'clarifies','The delayed-send proposal explicitly aims to avoid extra just-in-case transactions when amendment occurs within the timeout, corresponding to the preceding child-transaction explanation.',[ev(u23['source_id'],u23['span']['quote']),ev(u19['source_id'],u19['span']['quote'])])
rel(u24,u21,'clarifies','Greg’s suggestion is contextually resolved to the two earlier labels; the spelling correction is conditional on not choosing that suggestion.',[ev(u24['source_id'],u24['span']['quote']),ev(u21['source_id'],u21['span']['quote'])])
rel(u25,u26,'temporal','The supplied comment timestamps place the rebase diagnosis before the closure report on the same date. Chronology does not show that the diagnosis caused closure.',[ev(u25['source_id'],u25['span']['quote']),ev(u26['source_id'],u26['span']['quote'])])

screens=[]
reasons={
'pr7819:body':'Exhaustively screened. Four candidates retain the offered checkbox, uncertainty about the missing replacement workflow, the author’s ongoing plan, and the intention not to delay review. The inclusion of two #7159 refactoring commits is provenance/technical context without a navigation directive. Image tags are not rendered and provide no additional visual findings.',
'pr7819:comments:0':'Exhaustively screened. The hedged exposure objection is a plausible sequencing prescription, with technical-judgment and local-norm alternatives preserved.',
'pr7819:comments:1':'Exhaustively screened. Three candidates cover warning treatment, the alternative non-replacable warning, and the adaptive-fee method; the concern about misleading replacement language remains distinct rationale. The two elements of the first warning edit and the complete adaptive-fee algorithm are preserved together.',
'pr7819:comments:2':'Exhaustively screened. The repeated objection, explicit agreement, ongoing replacement-GUI plan, current-review invitation, and qualified 0.13 timing are separately retained. Neither the quote nor assent is counted as a new institutional expectation.',
'pr7819:comments:3':'Exhaustively screened. The quotation and tentative endorsement are context; the reported additional-output method and question proposing fee-only focus are candidates.',
'pr7819:comments:4':'Exhaustively screened. The child-transaction method is a plausible strategy candidate with a technical-only alternative; exponential version growth is a technical consequence, not institutional enforcement.',
'pr7819:comments:5':'Exhaustively screened. Candidates retain both proposed alternative labels and the delayed-send method with timeout/abort qualifications. Interest in additional outputs is context; no additional obligation is inferred from capability wording.',
'pr7819:comments:6':'Exhaustively screened. The addressed spelling correction is a conditional pragmatic request. The incomplete proposed stem and the condition concerning Greg’s suggestion are preserved.',
'pr7819:comments:7':'Exhaustively screened. Needs rebase is retained as an elliptical maintenance request with technical-status and force alternatives; no role authority is inferred.',
'pr7819:comments:8':'Exhaustively screened. A closure and reported inclusion act is retained as context, not an independently prescribed method, rejection, or merge.',
'pr7819:metadata':'Supplemental context screened. The record supports #7819’s closed-unmerged outcome and file inventory, not individual suggestion adoption or authority. Context-only screening is not an exhaustive institutional-content claim.',
'pr7819:supplement_metadata':'Supplemental context screened. Canonical identity, head snapshot, and closed-unmerged status are available; a merge_commit_sha does not establish integration. Context-only screening is not a claim that metadata lack institutional relevance.',
'pr8182:supplement_metadata':'Supplemental context screened. This distinct proposal’s identity and closed-unmerged status are used only for its own outcome; it does not identify every earlier planned GUI change. Context-only screening is not an exhaustive institutional-content claim.',
'pr7819:patch:0':'Supplemental context screened. The proposed artifact contains the checkbox and tooltip. Its technical allowance wording is not an institutional authorization. The clipped snapshot does not verify screenshot layout or repository integration.',
'pr7819:patch:1':'Supplemental context screened. The proposed artifact supplies the checkbox wiring and red confirmation text with the retained replacable spelling and exclamation. It does not establish adoption of review suggestions or a causal change history.',
'pr7819:patch:2':'Supplemental context screened. The retained head routes the checkbox selection into transaction flags. This is technical implementation evidence for the offered artifact, not proof of integration or authority.',
'pr7819:patch:3':'Supplemental context screened. The retained head adds the optInRBF parameter and default. No separate institutional proposition is extracted from this context-only supplement.',
'pr7819:patch:4':'Supplemental context screened. The retained head branches sequence values and signing behavior on flags. These technical consequences are not institutional sanctions; no chronology of review-driven changes is established.',
'pr7819:patch:5':'Supplemental context screened. The enum and signature changes are engineering definitions and provenance context. This limited supplement screening is not a claim that no institutional content could be studied in the file.'}
for s,e in entries.items():
    us=[u for u in units if u['source_id']==s]
    screens.append({'source_id':s,'disposition':'candidate' if any(u['record_role']=='statement' for u in us) else 'empty' if not e['text'].strip() else 'context_only','reason':reasons[s],'unit_ids':[u['unit_id'] for u in us]})

def part(text,es):return {'text':text,'evidence':es}
def outcome(claim,parts):return {'claim':claim,'evidence':uniq([e for p in parts for e in p['evidence']]),'claim_parts':parts}
def mech(cat,claim,ids,parts,alt,status='supported_sequence'):
    return {'category':cat,'claim':claim,'unit_ids':[u['unit_id'] for u in ids],'claim_parts':parts,'evidence':uniq([e for p in parts for e in p['evidence']]),'alternative_explanation':alt,'status':status}

outcomes=[
outcome('The author reported closing #7819 in favor of #8182, saying the content was included there; #7819 is recorded closed and unmerged.',[
part('The author reported closing #7819 in favor of #8182 and said it was included there.',[ev('pr7819:comments:8'),*id7819]),
part('#7819 is recorded closed and unmerged, with closure at 2016-06-09T09:21:57+00:00.',[ev('pr7819:metadata','"state": "closed"'),ev('pr7819:metadata','"merged": false'),ev('pr7819:metadata','"closed_at": "2016-06-09T09:21:57+00:00"')])]),
outcome('The distinct follow-up proposal #8182 is also recorded closed and unmerged; its metadata give a closure time of 2016-12-06T10:15:00Z.',[
part('The outcome belongs to #8182, the distinct proposal referenced in the closure report.',[ev('pr7819:comments:8','#8182'),*id8182]),
part('#8182 is recorded closed, merged false, and closed_at 2016-12-06T10:15:00Z.',[ev('pr8182:supplement_metadata','"state": "closed"'),ev('pr8182:supplement_metadata','"merged": false'),ev('pr8182:supplement_metadata','"closed_at": "2016-12-06T10:15:00Z"')])]),
outcome('The retained #7819 head artifact includes an opt-in checkbox and a red replaceability confirmation with the supplied replacable spelling and exclamation mark; this is an unmerged proposal snapshot.',[
part('The retained head artifact adds an optInRBF checkbox labeled Allow Replace-By-Fee.',[ev('pr7819:patch:0','+      <widget class="QCheckBox" name="optInRBF">'),ev('pr7819:patch:0','+        <string>Allow Replace-By-Fee</string>')]),
part('The confirmation code appends red styling and This transaction is replacable (optin-RBF)! when the checkbox is checked.',[ev('pr7819:patch:1','+    if (ui->optInRBF->isChecked())'),ev('pr7819:patch:1','+        questionString.append("<hr /><span style=\'color:#aa0000;\'>");'),ev('pr7819:patch:1','+        questionString.append(tr("This transaction is replacable (optin-RBF)!"));')]),
part('The snapshot is associated with head 9c4baa44d6448b3432fe265f5c800af29a6cdaf1, and #7819 is unmerged.',[ev('pr7819:supplement_metadata','"head_sha": "9c4baa44d6448b3432fe265f5c800af29a6cdaf1"'),ev('pr7819:supplement_metadata','"merged": false')])])]

mechanisms=[
mech('review_coordination','The exposure objection receives quoted assent, followed by the author’s statement that review can proceed already while replacement-GUI work continues. This supports a local distinction between reviewing the patch and exposing the feature.',[u05,u10,u11,u12,u13],[
part('The reviewer questions exposing the feature before replacement capability.',[ev(u05['source_id'],u05['span']['quote'])]),
part('The author repeats that objection and explicitly agrees.',[ev(u10['source_id'],u10['span']['quote']),ev(u11['source_id'],u11['span']['quote'])]),
part('The author says replacement-GUI work is ongoing but this can be reviewed already.',[ev(u12['source_id'],u12['span']['quote']),ev(u13['source_id'],u13['span']['quote'])])],
'The exchange could merely convey technical readiness rather than a recognized procedural standard. It demonstrates textual coordination, not a binding review/exposure rule or the actual occurrence of further review.'),
mech('reason_giving','The adaptive-fee proposal is quoted and called a possible solution; the author reports trying additional outputs and asks whether to focus just on fees. A subsequent explanation ties additional-output complexity to contingency child transactions and growth in transaction versions.',[u09,u15,u16,u17,u18,u19,u20],[
part('The adaptive-fee method includes future-locktime replacements, rising fees, and a displayed fee schedule.',[ev(u09['source_id'],u09['span']['quote'])]),
part('The author quotes that method and calls it a possible solution.',[ev(u15['source_id'],u15['span']['quote']),ev(u16['source_id'],u16['span']['quote'])]),
part('The author reports trying additional outputs and asks whether to focus just on increasing fees.',[ev(u17['source_id'],u17['span']['quote']),ev(u18['source_id'],u18['span']['quote'])]),
part('The reviewer explains additional-output complexity in terms of child transactions if the original confirms and growth in versions when repeated.',[ev('pr7819:comments:4')])],
'These correspondences support technical reason-giving, but the explanation may only elaborate the design space. The packet does not establish a resulting decision, adoption of fee-only scope, or a causal effect on implementation.'),
mech('scope_management','The author reports closing #7819 in favor of #8182 with its content included there, and #7819’s metadata record closure without merge. This is consistent with consolidating work into a separate proposal.',[u26],[
part('The author reports closing in favor of #8182 and says the content was included there.',[ev('pr7819:comments:8')]),
part('#7819 is recorded closed and unmerged.',[ev('pr7819:metadata','"state": "closed"'),ev('pr7819:metadata','"merged": false'),*id7819])],
'The report does not reveal the exact transferred changes or why consolidation was chosen. Neither the earlier rebase comment nor any particular design argument is shown to have caused closure; the separate #8182 record is also unmerged.',status='consistent_with')]

annotation={'schema_version':'0.4','run_id':'F03_v04_r3','episode_id':'F03','packet_sha256':hashlib.sha256(Path('packet.json').read_bytes()).hexdigest(),'entry_screening':screens,'units':units,'relations':relations,'episode_summary':{'observed_outcomes':outcomes,'mechanisms':mechanisms,'missing_evidence':['No complete edit history, reliable reply threading, or exact date for every retained body sentence is available.','Image links are not rendered; visual placement and screenshot appearance are not verified.','The retained patch is a head snapshot, not a chronology; it does not show which review caused changes.','No supplied evidence attributes rule-making authority, enforces a duty, or establishes project-wide expectations for these suggestions.','The exact replacement-GUI and additional-output work objects are not identified; #8182 is not assigned to them merely because it is later referenced.','No #8182 patch or exact transfer comparison is supplied. The inclusion claim remains the author’s report.','No outcome record for #7159 is supplied. Its refactoring-commit inclusion is only the body’s report.','Both supplied proposal outcomes are unmerged; no repository integration, release inclusion, or network adoption is established.'],'unresolved_questions':['Whether the tentative exposure condition should be treated as a local norm or solely as a technical usability judgment.','Whether review can proceed already is an invitation or merely a readiness claim; it is not established authorization.','Whether any suggested warning, naming, adaptive-fee, additional-output, or delayed-send changes were implemented in a different contribution.','What exact behavior was intended by the [send immediately] option described as delaying sending.','Whether the rebase comment and subsequent closure are substantively related; timestamps alone supply no causal link.']}}

text=json.dumps(annotation,ensure_ascii=False,indent=2)+'\n'
Path('annotation.json').write_text(text)
Path('annotation.first_complete.json').write_text(text)
Path('freeze.first_complete.json').write_text(json.dumps({'run_id':'F03_v04_r3','frozen_at_utc':datetime.now(timezone.utc).isoformat(),'packet_sha256':annotation['packet_sha256'],'annotation_first_complete_sha256':hashlib.sha256(text.encode()).hexdigest(),'stage':'First complete annotation, frozen before checker execution and source self-review','counts':{'entries':len(screens),'units':len(units),'statements':sum(u['record_role']=='statement' for u in units),'relations':len(relations)}},indent=2)+'\n')
print(json.dumps({'created':'annotation.first_complete.json','entries':len(screens),'units':len(units),'statements':sum(u['record_role']=='statement' for u in units),'relations':len(relations)}))
