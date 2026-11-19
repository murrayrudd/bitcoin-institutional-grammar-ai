import json, hashlib
from pathlib import Path
from copy import deepcopy
P=Path('.')
packet=json.loads((P/'packet.json').read_text())
sources={e['source_id']:e for e in packet['entries']}
texts={k:v['text'] for k,v in sources.items()}
PR='https://github.com/bitcoin/bitcoin/pull/7819'
NEXT='https://github.com/bitcoin/bitcoin/pull/8182'

def a(s,q=None,n=0):
    t=texts[s]
    if q is None: q=t.rstrip('\n')
    st=-1
    for _ in range(n+1): st=t.index(q,st+1)
    return {'source_id':s,'span':{'start':st,'end':st+len(q),'quote':q}}
def uniq(es):
    result=[]
    for e in es:
        if e not in result:result.append(e)
    return result
META='pr7819:supplement_metadata'
ID=[a(META,'"url": "'+PR+'"')]
CLOSED=[a(META,'"state": "closed"'),a(META,'"merged": false'),a(META,'"closed_at": "2016-06-09T09:21:57Z"')]
units=[]
def unit(i,s,q,role='statement',summary=None,typ='undetermined',force='recommendation',speech='proposed',parse='literal',obj=PR,scope='case_specific',rationale=None,alt='',uncert='',parent=None):
    evidence=a(s,q)
    isstmt=role=='statement'
    t=sources[s].get('timestamp')
    obj_ev=deepcopy(ID) if obj==PR else []
    u={
      'unit_id':i,'source_id':s,'span':evidence['span'],'parent_unit_id':parent,
      'record_role':role,'grammar':'regulative' if isstmt else 'not_institutional',
      'speech_act':speech,'scope':scope,'parse_mode':parse,
      'deontic_force':force if isstmt else 'nondeontic','components':[],
      'institution':{'type':typ if isstmt else 'not_applicable','dispute_present':False,
        'rationale':rationale or ('A case-specific technical design or review proposal is institutionally relevant to contribution activity, but supplies neither a governing authorization nor a recurring social expectation or committed method.' if isstmt else 'This record preserves a communicative act or technical context, not a separate institutional proposition.'),
        'evidence':[evidence],'recognition':[],'authority_evidence':[],
        'standing_profile':{'documentary':'none' if isstmt else 'not_applicable','recognition':'none' if isstmt else 'not_applicable','application':'none' if isstmt else 'not_applicable'},
        'documentary_support':[],'application_evidence':[],'challenges':[],'type_alternatives':[]},
      'statement_target_level':'operational' if isstmt else 'not_applicable',
      'observed_action_level':'not_applicable' if role=='container' else 'operational',
      'level_rationale':'The focal action concerns this contribution or its contemplated wallet workflow; the visible act is ordinary proposal/review discourse. No change to recurring governance arrangements or allocation of authority is established.' if isstmt else ('A structural grouping has no independently classified action.' if role=='container' else 'The observed act is ordinary contribution discourse or a reported contribution action; this record does not independently govern an activity.'),
      'complexity_flags':['none'],'alternative_interpretation':alt,
      'confidence':'plausible' if isstmt else 'clear','uncertainty_reason':uncert,
      'presentation':{'quotation':'repeated' if role=='quotation' else 'none','markup':'plain','rationale':'Presentation follows the retained occurrence; no edit history or formatting chronology is inferred.'},
      'disposition_events':[],
      'proposition':{'summary':summary or q,'decision_object_id':obj,'domain':'Bitcoin Core Qt wallet contribution and review','time_scope':('Retained PR body; creation recorded as '+str(t)+', with later update metadata. Exact date of this wording is not established.' if s=='pr7819:body' else 'Retained occurrence recorded at '+str(t)+'; complete edit history unavailable, so the timestamp does not establish the first appearance of every word.'),'identity_evidence':obj_ev,'qualifiers':[]} if isstmt else None,
      'target_level_alternatives':[],'observed_level_alternatives':[],
      'level_evidence':{'target_activity':summary or ('No independently governed activity; '+role+' record'),'observed_activity':speech+' in a PR discussion' if role!='container' else 'Structural grouping only','arrangement':'Case-specific contribution, review, design, or withdrawal activity; no higher-level arrangement is established.','evidence':[evidence]}
    }
    units.append(u)
    return u

def c(u,symbol,text,q=None,basis='explicit',role='local',note='',s=None,gov=None,n=0):
    s=s or u['source_id']
    ev=a(s,q if q is not None else text,n)
    governing=gov if gov else {'source_id':u['source_id'],'span':deepcopy(u['span'])}
    u['components'].append({'symbol':symbol,'text':text,'basis':basis,'evidence':[ev], 'inference_note':note,'occurrence_role':role,'governing_span':governing})
def qual(u,description,es,attachment='scope_note',linked=None,rationale=None):
    u['proposition']['qualifiers'].append({'description':description,'evidence':es,'attachment':attachment,'linked_unit_id':linked,'rationale':rationale or 'This qualification is attached explicitly to the focal proposition and limits its interpretation.'})
def close(u):
    u['disposition_events'].append({'kind':'recorded_closed_unmerged','target':'broader_proposal','basis':'explicit','object_id':PR,'identity_evidence':deepcopy(ID),'evidence':deepcopy(CLOSED),'rationale':'The event concerns PR #7819 as a whole. Its recorded closed state and false merge flag do not establish rejection, implementation, or withdrawal of this particular design/review proposition. They do not supply the disposition of any separate future workflow.'})
def rec(u,ev,kind='endorsement',mode='ordinary_assent',speaker='different_actor',target='this_proposition',obj=PR,rationale='',basis='context_inferred'):
    u['institution']['recognition'].append({'kind':kind,'target':target,'basis':basis,'evidence':ev,'rationale':rationale,'mode':mode,'speaker_relation':speaker,'independence_key':PR,'object_id':obj,'identity_evidence':deepcopy(ID) if obj==PR else []})

s='pr7819:body'
u=unit('U01',s,'Adds a checkbox to the Send-Coins-Pannel (next to "Add Recipient") that allows to set the according nSequence to signal BIP125 RBF.',summary='jonasschnelli offers PR #7819 adding an opt-in BIP125 RBF-signaling checkbox to the Send-Coins-Pannel next to Add Recipient; the PR lacks a GUI transaction-replacement workflow.',speech='technical_description',force='nondeontic',rationale='The PR description can represent an offered edit, but its literal content is an engineering change. Institutional type remains undetermined; the checkbox is not constituted governance authority.',alt='Treat the feature description solely as technical context. The retained candidate represents the contribution proposal, not a permission granted to users.',uncert='The offered-proposal reading comes from the PR context; the sentence itself describes code. No adoption or authority is established.')
c(u,'I','Adds')
c(u,'Bdir','a checkbox')
c(u,'Cex','to the Send-Coins-Pannel (next to "Add Recipient")')
c(u,'Bdir,p','that allows to set the according nSequence to signal BIP125 RBF')
qual(u,'No GUI mechanism for actually replacing a transaction is included.',[a(s,'This PR does not include a way to actually replace a transaction with the GUI.')])
qual(u,'Whether to proceed without a GUI replacement workflow is explicitly uncertain; that larger workflow is reported as in progress.',[a(s,"So not sure if we want this without a GUI based replacement workflow (which I'm working on but it is a bigger chunk).")],attachment='linked_unit',linked='U02')
qual(u,'Two refactoring commits are attributed to #7159; that source PR is not the decision object of this checkbox proposal.',[a(s,'Includes two refactoring commits from https://github.com/bitcoin/bitcoin/pull/7159')])
close(u)
u['institution']['challenges'].append({'aspect':'premise','target':'broader_proposal','evidence':[a('pr7819:comments:0')],'rationale':'The concern questions exposing the current feature before replacement exists. It does not dispute the literal claim that the contribution adds a checkbox, so it is retained as a broader-proposal readiness challenge.'})
u['institution']['application_evidence'].append({'status':'unresolved','target':'this_proposition','evidence':[a('pr7819:patch:0','+      <widget class="QCheckBox" name="optInRBF">'),a('pr7819:patch:0','+        <string>Allow Replace-By-Fee</string>')]+deepcopy(CLOSED),'rationale':'The retained head contains a checkbox artifact, but #7819 was not merged. The packet establishes a prepared feature, not integrated application of the offered proposal; an earlier-to-later implementation sequence is unavailable.'})
u['institution']['standing_profile']['application']='unresolved'

u=unit('U02',s,"So not sure if we want this without a GUI based replacement workflow (which I'm working on but it is a bigger chunk).",role='context',speech='asserted',alt='This could be extracted as a tentative recommendation to defer exposure. Here the uncertainty is preserved as context and a material qualifier to U01; the direct readiness recommendation appears in U04.')

u=unit('U03',s,"But I don't want to hold back review of this PR.",summary='jonasschnelli expresses the intention not to delay review of PR #7819 while the larger replacement workflow remains in progress.',typ='strategy_candidate',force='nondeontic',speech='asserted',parse='pragmatic',rationale='This is an attributable personal intention to let review proceed separately from finishing the larger workflow. It is a strategic commitment rather than a demonstrated rule or shared obligation.',alt='The sentence can remain a personal preference without a committed plan, or pragmatically invite others to review now. Either reading preserves review/exposure separation and the negative preference.',uncert='Intention is expressed as not wanting to hold review back; the degree of commitment is uncertain.')
c(u,'A','I',gov=a(s,"I don't want to hold back review of this PR."),note='Under the reconstructed intention not to delay review, I remains the explicitly expressed actor of the preference.')
c(u,'I','not hold back',q="don't want to hold back",basis='context_inferred',role='semantic_inference',note='The negated preference is reconstructed as a non-delay intention. It is not a deontic prohibition.')
c(u,'Bdir','review of this PR',note='Review is the explicit object of hold back and retains that role in the reconstructed non-delay intention.')
qual(u,'The separate GUI replacement workflow is reported as work in progress and a bigger chunk; review is being separated from that work.',[a(s,"a GUI based replacement workflow (which I'm working on but it is a bigger chunk)")])
u['institution']['type_alternatives']=['undetermined']
rec(u,[a('pr7819:comments:2','but this can be reviewed already.')],kind='response',mode='same_actor_restatement',speaker='same_actor',rationale='The same author restates the possibility of current review while working on the replacement GUI. This is maintained personal commitment, not independent recognition of an expectation.')
u['institution']['standing_profile']['recognition']='same_actor_only'
close(u)

s='pr7819:comments:0'
u=unit('U04',s,texts[s].rstrip('\n'),summary='luke-jr tentatively recommends withholding exposure of the checkbox feature until the wallet actually can do replacement.',parse='pragmatic',speech='asserted',rationale='The evaluation of readiness implies a case-specific recommendation about exposing an incomplete workflow. It does not identify institutional authorization or an established duty; a proposed readiness norm remains a bounded alternative.',alt='Literal technical/product judgment about usefulness, with no instruction. A readiness expectation is also plausible, but the packet does not establish that it is an institutionally governing condition.',uncert='The negative recommendation is inferred from Not sure it makes sense; wallet replacement is not silently narrowed to the GUI wording of the body.')
c(u,'I','withhold exposure',q='Not sure it makes sense to expose',basis='context_inferred',role='semantic_inference',note='Deferral is reconstructed from questioning exposure until a specified capability exists; expose itself is explicit but its deferred/negative role is inferred.')
c(u,'Bdir','this checkbox feature',q='this',basis='context_inferred',role='context_reference',note='This is the explicit object of expose; its feature referent is recovered from U01. Because the annotated object includes that resolution, its basis is contextual.')
c(u,'Bdir,p','the checkbox proposal',q='Adds a checkbox',s='pr7819:body',basis='context_inferred',role='context_reference',note='Outside-unit antecedent identifies this as the currently offered checkbox feature; no separate proposal identity is inferred.')
c(u,'Cac','until the wallet actually _can_ do replacement',note='The explicit until clause supplies the condition terminating the inferred deferral, not an obligation expressed by can.')
u['presentation']['markup']='mixed'
u['presentation']['rationale']='The retained sentence contains emphasis around _can_; the wording is not a quote or struck-through text.'
qual(u,'Tentative negative evaluation, not an explicit categorical prohibition.',[a(s,'Not sure it makes sense')])
qual(u,'The condition is wallet replacement capability; the word can denotes technical capability.',[a(s,'until the wallet actually _can_ do replacement')],attachment='component')
u['institution']['type_alternatives']=['norm_candidate']
rec(u,[a('pr7819:comments:2','Right. I totally agree.'),a('pr7819:comments:2','> Not sure it makes sense to expose this until the wallet actually can do replacement...')],basis='explicit',rationale='The author quotes the readiness judgment and agrees. This is explicit ordinary assent to a technical/product condition, without independently treating an institutional expectation as governing.')
close(u)

s='pr7819:comments:1'
style="I don't think the confirmation window deserves red text and the bang for it."
u=unit('U05',s,style,role='container',speech='other')
u['complexity_flags']=['compound']
u=unit('U06',s,"I don't think the confirmation window deserves red text",parent='U05',summary='gmaxwell suggests removing red emphasis from the confirmation window for the replaceable transaction.',speech='asserted',parse='pragmatic',alt='Literal aesthetic judgment about deserving red text; the edit request is inferred from review context.',uncert='The sentence criticizes styling but does not explicitly command its removal.')
c(u,'I','remove',q="I don't think the confirmation window deserves red text",basis='context_inferred',role='semantic_inference',note='A removal recommendation is inferred from the negative assessment of existing styling.')
c(u,'Bdir','red text emphasis',q='red text',basis='context_inferred',role='semantic_inference',note='Red text is literally the object of deserves; assigning it as the edit target of remove is a reconstructed role.')
c(u,'Cex','in the confirmation window',q='the confirmation window',basis='context_inferred',role='semantic_inference',note='The literal subject of deserves is reconstructed as the location of the proposed edit.')
qual(u,'The criticism concerns the replaceable-transaction confirmation shown in the retained patch, not every red UI element.',[a('pr7819:patch:1','+    if (ui->optInRBF->isChecked())\n+    {\n+        questionString.append("<hr /><span style=\'color:#aa0000;\'>");\n+        questionString.append(tr("This transaction is replacable (optin-RBF)!"));')])
close(u)
u=unit('U07',s,'and the bang for it.',parent='U05',summary='gmaxwell suggests removing the exclamation mark from the replaceable-transaction confirmation.',speech='asserted',parse='pragmatic',alt='The bang is part of a joint aesthetic judgment; this child isolates the separately executable punctuation edit.',uncert='The shared negative assessment is outside this child span and is explicitly attached.')
c(u,'I','remove',q=style,basis='context_inferred',role='shared_scope',note='The preceding negative deserves assessment governs the coordinated bang object; removal is pragmatically reconstructed.',gov=a(s,style))
c(u,'Bdir','the bang',basis='context_inferred',role='semantic_inference',note='The bang is a literal coordinated object of deserves, assigned an inferred edit-target role under remove.')
c(u,'Cex','in the confirmation window',q='the confirmation window',basis='context_inferred',role='shared_scope',note='The confirmation-window scope comes from the shared predicate outside the child, not an unrelated pronoun.',gov=a(s,style))
qual(u,'The shared negative judgment applies to both red text and the bang.',[a(s,style)],attachment='scope_note')
close(u)
u=unit('U08',s,'Also "replaceable" there may have the user thinking that it\'s more replaceable than it is...',role='context',speech='asserted',alt='An indirect request to relabel could be inferred. The wording problem is retained as rationale, with the concrete alternative-label proposal independently extracted in U20.')

q="arguably it should be the non-replacable case that should get red text (because you can't update fees later)."
u=unit('U09',s,q,summary='gmaxwell tentatively suggests applying red text to the non-replacable case because fees cannot be updated later.',parse='pragmatic',speech='asserted',alt='Literal technical/UI proposition that the non-replacable case should get red text; either representation preserves the same target state, advisory force, and stated reason.',uncert='The actor who would change the UI is unexpressed. Arguably makes this an advisory inversion of emphasis.')
c(u,'I','apply',q='should get',basis='context_inferred',role='semantic_inference',note='The requested editing action is reconstructed from a state described as getting red text.')
c(u,'Bdir','red text',basis='context_inferred',role='semantic_inference',note='The source object of get becomes the format applied under the reconstructed edit predicate.')
c(u,'Cex','to the non-replacable case',q='the non-replacable case',basis='context_inferred',role='semantic_inference',note='The literal receiver/subject of get becomes the scope of applying red text.')
qual(u,'Arguably and should make this an advisory suggestion, not a binding prohibition or duty.',[a(s,'arguably it should be'),a(s,'should get red text')])
qual(u,'The reason is the stated inability to update fees later in the non-replacable case.',[a(s,"because you can't update fees later")])
close(u)

q='I\'m wondering if we should even have a "replaceable switch" and not, instead, have an "adaptive fee switch" (that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees-- and the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks])'
u=unit('U10',s,q,summary='gmaxwell tentatively proposes an adaptive fee switch instead of a replaceable switch, computing N future-locktime replacements at multiplicatively higher fees and displaying the corresponding fee schedule.',parse='pragmatic',speech='asserted',rationale='This offered alternative articulates a technical design method, but the focal proposition is a one-off request to substitute the switch, without an attributable commitment to implement it. Institutional type remains undetermined.',alt='A literal deliberation between have-a-replaceable-switch and have-an-adaptive-fee-switch can be decomposed into alternatives. A strategy reading is possible at the embedded design-method layer, rather than the focal substitution request.',uncert='The wording is tentative and syntactically indirect; the inferred substitution preserves rather than strengthens its advisory force.')
c(u,'A','we',basis='context_inferred',role='semantic_inference',note='We is the literal actor of have. Its role as the actor of the reconstructed substitution request is inferred, without assigning named maintainers or a governing electorate.')
c(u,'I','substitute',q='and not, instead, have',basis='context_inferred',role='semantic_inference',note='The rhetorical alternative is reconstructed as substituting the adaptive design for the replaceable switch.')
c(u,'Bdir','a "replaceable switch"',basis='context_inferred',role='semantic_inference',note='The literal object of have is the outgoing target under the reconstructed substitution predicate.')
c(u,'Cex','with an "adaptive fee switch"',q='an "adaptive fee switch"',basis='context_inferred',role='semantic_inference',note='The incoming alternative is an execution specification for substitution, not a separate indirect recipient.')
qual(u,'The adaptive switch computes N replacements with future locktimes and multiplicatively higher fees.',[a(s,'that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees')])
qual(u,'Its fee line changes to the stated x/y/z/q/r fee and 3/4/5/6-block schedule.',[a(s,'the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks]')])
qual(u,'Wondering if marks tentative exploration, not an adopted replacement decision.',[a(s,"I'm wondering if")])
u['complexity_flags']=['compound']
u['institution']['type_alternatives']=['strategy_candidate']
rec(u,[a('pr7819:comments:3','Yes. This might be a solution.'),a('pr7819:comments:3','> '+q)],basis='explicit',rationale='A direct quote precedes tentative agreement that this might be a solution. This is ordinary technical assent, not recognition of an institutional requirement.')
close(u)

s='pr7819:comments:2'
u=unit('U11',s,'> Not sure it makes sense to expose this until the wallet actually can do replacement...',role='quotation',speech='asserted')
u['alternative_interpretation']='Repeated quotation of U04 without its emphasis markup; not another readiness endorsement by the original actor.'
u=unit('U12',s,'Right. I totally agree.',role='context',speech='reported_action')
u['alternative_interpretation']='This is ordinary agreement with the preceding readiness quotation. Expectation recognition is possible only if that technical readiness criterion is independently treated as an institutional standard, which is not established here.'
u=unit('U13',s,'but this can be reviewed already.',summary='jonasschnelli says PR #7819 can already be reviewed while work on the replacement GUI continues.',force='unresolved',speech='asserted',parse='literal',alt='Can may express present review feasibility, permissive encouragement, or a pragmatic review invitation. No institutional grant of permission is established.',uncert='Capability versus permission cannot be resolved from can alone; current review is distinct from exposing the feature.')
c(u,'I','reviewed')
c(u,'Bdir','this',note='In the passive this can be reviewed, this is the explicit patient of reviewed; its #7819 referent is attached separately.')
c(u,'Cex','already')
qual(u,'This refers to the current checkbox PR, whose review the body says should not be held back.',[a('pr7819:body',"But I don't want to hold back review of this PR.")])
qual(u,'Can is unresolved between technical feasibility and permissive encouragement; no authority is supplied.',[a(s,'this can be reviewed already')])
qual(u,'The author says the replacement GUI process is still being worked on and the 0.13 timeline is tough.',[a(s,"I'm working on the replacement GUI process"),a(s,'The timeline to get this into 0.13 is tough.')])
close(u)

s='pr7819:comments:3'
u=unit('U14',s,'> '+q,role='quotation',speech='asserted')
u['alternative_interpretation']='This repeats U10 and does not independently originate or endorse its design.'
u=unit('U15',s,'Yes. This might be a solution.',role='context',speech='reported_action')
u=unit('U16',s,'I somehow was also trying to allow adding additional outputs (edit the transaction back in the sendcoins dialog).',summary='jonasschnelli reports trying a replacement-workflow approach that allows additional outputs by editing the transaction back in the sendcoins dialog.',typ='strategy_candidate',force='nondeontic',speech='reported_action',obj=None,rationale='The author reports an attributable attempted development approach and specifies its method. This is a personal strategy candidate; no expectation that others must adopt it is established.',alt='A report of a past technical attempt can remain context rather than a strategy proposition. Retaining it as a candidate preserves the articulated method without treating it as a shared rule.',uncert='The separate replacement workflow has no established canonical proposal identifier in the packet. The containing #7819 is not automatically the decision object.')
c(u,'A','I')
c(u,'I','allow')
c(u,'Bdir','adding additional outputs')
c(u,'Cex','edit the transaction back in the sendcoins dialog')
qual(u,'The approach was being tried; somehow, also, and was trying do not establish a completed edit or firm commitment.',[a(s,'I somehow was also trying to allow')])
qual(u,'The method concerns the contemplated replacement workflow, not a demonstrated change already included in #7819.',[a('pr7819:body','This PR does not include a way to actually replace a transaction with the GUI.'),a('pr7819:comments:2',"I'm working on the replacement GUI process")])
u['institution']['type_alternatives']=['undetermined']
rec(u,[a('pr7819:comments:5','doing the add output thing would be pretty interesting...')],target='this_proposition',obj=None,rationale='gmaxwell expresses interest in the add-output idea, not an institutional expectation. The underlying replacement-workflow proposal lacks an established ID; the referent is nevertheless identifiable as the method, and object_id is inapplicable to a registered PR.',basis='context_inferred')

u=unit('U17',s,'But maybe we should just focus on increasing the fees?',summary='jonasschnelli tentatively asks whether the replacement-workflow effort should focus only on increasing fees.',speech='question',obj=None,alt='Exploratory design question rather than a directive. The proposed narrower scope can coexist with the adaptive-fee option; it is not evidence of rejecting additional outputs.',uncert='The larger replacement-workflow object has no canonical proposal ID; the question does not establish a decision.')
c(u,'A','we')
c(u,'D','should')
c(u,'I','focus on')
c(u,'Bdir','increasing the fees')
c(u,'Cex','just',note='Just limits the proposed scope to fees; it is not evidence of exclusive technical possibility.')
qual(u,'Maybe and question form preserve tentativeness.',[a(s,'maybe we should just focus on increasing the fees?')])

s='pr7819:comments:4'
q='workflow for additional outputs is more complex because you need to handle also making a child transaction of the original transaction for use in case the original confirms'
u=unit('U18',s,q,summary='gmaxwell says the additional-output workflow requires handling creation of a child of the original transaction for use if the original confirms.',speech='asserted',force='nondeontic',obj=None,rationale='The focal need concerns a technical dependency of the described workflow. It is retained as an institutionally relevant design-method candidate without converting engineering necessity into social obligation.',alt='Pure technical explanatory context. A method/strategy reading is possible, but no personal implementation commitment or institutional duty is asserted.',uncert='Need is best read as technical necessity; its possible prescriptive review force is secondary. The contemplated workflow has no established proposal ID.')
c(u,'A','you',note='Generic you supplies the local actor of handle; no named occupational or governance role is inferred.')
c(u,'I','handle')
c(u,'Bdir','also making a child transaction of the original transaction for use in case the original confirms',note='The complete gerund object preserves what child is created and the condition on its use. The original-confirmation condition applies to using the child, not to beginning development.')
qual(u,'The requirement is specific to the additional-output workflow.',[a(s,'workflow for additional outputs')],attachment='component')
qual(u,'The stated need is a technical dependency and no lexical need/must is treated as institutional authorization.',[a(s,'you need to handle')])
qual(u,'The child is for use if the original confirms, rather than for all replacements unconditionally.',[a(s,'for use in case the original confirms')],attachment='component')
u['institution']['type_alternatives']=['strategy_candidate']
q='and if you do this multiple times there is a bit of exponential blowup in the number of versions you must compute.'
u=unit('U19',s,q,role='context',speech='technical_description',alt='Must compute describes the technical computational consequence of repeated changes. It does not independently establish a duty or sanction.')

s='pr7819:comments:5'
q='Instead of the word "replacable" perhaps the word "updatable" or "amendable" would better express what the it\'ll do?'
u=unit('U20',s,q,summary='gmaxwell suggests substituting updatable or amendable for replacable to better describe the feature.',speech='question',parse='pragmatic',alt='Literal question comparing descriptive adequacy of terms. The editorial recommendation is pragmatic; the two offered substitutes remain alternatives, not simultaneous requirements.',uncert='The proposal is tentative and does not establish adoption of either word.')
c(u,'I','substitute',q='Instead of the word "replacable" perhaps the word "updatable" or "amendable"',basis='context_inferred',role='semantic_inference',note='An edit action is reconstructed from instead-of and the comparative adequacy question.')
c(u,'Bdir','the word "replacable"',basis='context_inferred',role='semantic_inference',note='The phrase is a comparison referent in the literal sentence and becomes the inferred target of substitution.')
c(u,'Cex','with "updatable" or "amendable"',q='the word "updatable" or "amendable"',basis='context_inferred',role='semantic_inference',note='The offered substitutes form a single alternative-valued edit specification; neither is an indirect recipient.')
qual(u,'The goal is better description of what the feature will do, not a stronger claim about replaceability.',[a(s,"would better express what the it'll do?")])
qual(u,'The exact old spelling is replacable; the alternatives are updatable OR amendable.',[a(s,'"replacable"'),a(s,'"updatable" or "amendable"')],attachment='component')
close(u)
u=unit('U21',s,'doing the add output thing would be pretty interesting...',role='context',speech='asserted',alt='This expresses interest in U16, rather than independently prescribing addition of outputs.')
q='though it would be nice to have a [send immediately] option which delays sending it, thus avoids having to do the extra just in case transactions if you amend with in the timeout. (and could also let you abort before it was initially set).'
u=unit('U22',s,q,summary='gmaxwell suggests a [send immediately] option described as delaying sending, avoiding extra just-in-case transactions if amended within the timeout, and potentially allowing abort before initial sending.',obj=None,alt='Exploratory technical feature idea. The apparent tension between the bracketed send immediately label and delayed sending is preserved rather than silently corrected.',uncert='The separate replacement/add-output workflow has no canonical proposal ID, and the exact semantics of the option label are not explained.')
c(u,'I','have')
c(u,'Bdir','a [send immediately] option which delays sending it',note='The full object preserves the supplied option label and its apparently contrary delaying behavior; the wording is not normalized.')
qual(u,'Avoiding extra just-in-case transactions is conditioned on amendment within the timeout.',[a(s,'thus avoids having to do the extra just in case transactions if you amend with in the timeout.')])
qual(u,'Abort is presented as an additional possible capability before it was initially set, not a separate adopted requirement.',[a(s,'(and could also let you abort before it was initially set).')])
qual(u,'The delay option accompanies interest in the add-output workflow.',[a(s,'doing the add output thing would be pretty interesting...')],attachment='linked_unit',linked='U21')

s='pr7819:comments:6'
q=texts[s].rstrip('\n')
u=unit('U23',s,q,summary='kirkalx suggests that Jonas use the spelling beginning replaceab if he does not choose Greg\'s alternative wording.',speech='asserted',parse='pragmatic',alt='Literal assertion about more accepted spelling rather than an explicit edit instruction. The visible replaceab fragment is not expanded to a guessed full replacement.',uncert='Jonas is the supplied addressee, not a verified alias-to-person mapping. Greg\'s suggestion is contextually linked to U20; neither full corrected wording nor adoption is supplied.')
c(u,'A','Jonas (the addressed you)',q='Jonas',basis='context_inferred',role='context_reference',note='The vocative identifies the addressee of the inferred edit request. It does not explicitly occupy the actor position of an edit predicate and is not mapped to an external identity.')
c(u,'I','use',q='is the more accepted spelling',basis='context_inferred',role='semantic_inference',note='Use is reconstructed from the comparative spelling assertion in review context.')
c(u,'Bdir','the supplied spelling fragment "replaceab"...',q='"replaceab"...',basis='context_inferred',role='semantic_inference',note='The quoted spelling fragment is literally the assertion subject; its edit-object role is inferred. The ellipsis is retained without completing the word.')
c(u,'Cac',"if you don't go with Greg's suggestion",note='The explicit if-clause remains the condition on the inferred spelling alternative; you in that conditional is not used as an explicit actor anchor for use.')
qual(u,'The alternative is conditional on not following Greg\'s wording suggestion.',[a(s,"if you don't go with Greg's suggestion")],attachment='component')
qual(u,'Only the spelling fragment replaceab is supplied; the full replacement is unresolved.',[a(s,'"replaceab"...')],attachment='component')
u['institution']['type_alternatives']=['norm_candidate']
close(u)

s='pr7819:comments:7'
u=unit('U24',s,'Needs rebase.',summary='laanwj requests a rebase of the current PR #7819.',parse='pragmatic',speech='asserted',alt='Literal technical state report that the PR needs rebasing. Review context makes the elliptical action request plausible without establishing a binding integration rule.',uncert='The actor expected to rebase is unexpressed; no repository permission or maintainer authority is inferred.')
c(u,'I','rebase',q='rebase',basis='context_inferred',role='semantic_inference',note='The noun rebase in an elliptical needs sentence is reconstructed as the requested action.')
c(u,'Bdir','PR #7819',q='"url": "'+PR+'"',s=META,basis='context_inferred',role='context_reference',note='The omitted target is the current PR, identified by the supplied source association and matching metadata. The metadata is not an explicit local argument.')
close(u)
s='pr7819:comments:8'
u=unit('U25',s,'Closing in favor of #8182 (included there).',role='context',speech='reported_action',alt='The author reports closure and inclusion elsewhere. This does not itself verify the contents or integration of #8182, or rejection of any particular technical recommendation.')

relations=[]
def rel(fr,to,t,es,rationale,basis='context_inferred',logic='not_applicable'):
    relations.append({'from_unit_id':fr,'to_unit_id':to,'type':t,'basis':basis,'rationale':rationale,'evidence':es,'logic_scope':logic})
def ue(i):
    u=next(x for x in units if x['unit_id']==i)
    return {'source_id':u['source_id'],'span':deepcopy(u['span'])}
rel('U02','U01','clarifies',[ue('U02'),ue('U01')],'The author qualifies the checkbox offering by uncertainty about proceeding without the larger GUI workflow.',basis='explicit')
rel('U04','U01','challenges',[ue('U04'),ue('U01')],'The response questions readiness to expose the offered feature before replacement capability, not the factual existence of the proposed checkbox.')
rel('U11','U04','quotes',[ue('U11'),ue('U04')],'The source repeats the readiness sentence, dropping only the original emphasis markup.',basis='explicit')
rel('U04','U12','uptake',[ue('U11'),ue('U12')],'The direct quotation is followed by the author\'s explicit agreement; uptake is assent, not implementation or authority recognition.',basis='explicit')
rel('U13','U04','clarifies',[ue('U13'),ue('U04'),a('pr7819:comments:2',"I'm working on the replacement GUI process but this can be reviewed already.")],'The author distinguishes reviewing now from exposing the incomplete workflow; this is not a contradictory rejection of the readiness concern.')
rel('U13','U03','clarifies',[ue('U13'),ue('U03')],'The same author makes the immediate-review implication of the earlier no-delay intention more explicit; chronology of retained body wording is not inferred.')
rel('U06','U07','AND',[a('pr7819:comments:1',style)],'The red emphasis and bang are coordinated targets of the same negative assessment. Both edits are recoverable as separate actions.',basis='explicit',logic='actions')
rel('U09','U06','clarifies',[ue('U09'),ue('U06')],'The suggested non-replacable red emphasis explains the alternative allocation of warning styling, without implying a universal UI rule.')
rel('U14','U10','quotes',[ue('U14'),ue('U10')],'The adaptive-switch proposal is reproduced as a quote, not independently originated.',basis='explicit')
rel('U10','U15','uptake',[ue('U14'),ue('U15')],'Direct quote followed by tentative acceptance as a possible solution; no implementation is reported.',basis='explicit')
rel('U17','U16','clarifies',[ue('U17'),ue('U16')],'The contrastive question offers fee increases as a narrower contemplated focus than adding outputs, without deciding or rejecting either.')
rel('U18','U16','clarifies',[ue('U18'),ue('U16')],'The response identifies a technical dependency of the discussed additional-output workflow; correspondence supports a response, not a causal effect.')
rel('U19','U18','clarifies',[ue('U19'),ue('U18')],'The coordinated technical explanation adds the computational consequence of repeating the operation.',basis='explicit')
rel('U20','U08','clarifies',[ue('U20'),ue('U08')],'The same speaker later supplies concrete label alternatives corresponding to the earlier concern about overstating replaceability.')
rel('U16','U21','uptake',[ue('U16'),ue('U21')],'The later add-output interest refers to the reported method; this is an evaluative response, not adoption.')
rel('U22','U21','clarifies',[ue('U22'),ue('U21')],'Though links interest in add-output functionality to a delay-option suggestion and its technical rationale.',basis='explicit')
rel('U23','U20','clarifies',[ue('U23'),ue('U20')],'The conditional spelling suggestion applies if the addressee does not choose Greg\'s alternative words. The conversational mapping is inferred rather than external identity verification.')
rel('U24','U25','temporal',[ue('U24'),ue('U25')],'Supplied comment timestamps place the rebase request before the author\'s closure report on 2016-06-09. The text does not attribute closure to the request; no causation or sanction is inferred.')

screen_reasons={
'pr7819:body':'Focal entry exhaustively screened: checkbox offering and personal no-delay review intention retained as candidates. Uncertainty about proceeding without replacement GUI is context and a visible qualifier. Ongoing work, upstream refactoring provenance, and image markup do not independently prescribe conduct; image contents are unavailable.',
'pr7819:comments:0':'Focal entry: tentative readiness recommendation retained with literal technical-assessment alternative. Technical can is not permission.',
'pr7819:comments:1':'Focal entry: red emphasis, bang, alternative warning emphasis, and adaptive-fee switch extracted; descriptive replaceability concern retained as context. Alternative-switch computation and fee-display qualifications remain attached.',
'pr7819:comments:2':'Focal entry: repeated readiness quotation and ordinary agreement separated from the current-review candidate. Ongoing GUI work and version-0.13 timing are direct qualification evidence, not additional obligations.',
'pr7819:comments:3':'Focal entry: repeated switch quotation and tentative assent are distinct from the reported additional-output method and narrower fee-focus question. The larger workflow is not assigned the containing PR identifier without evidence.',
'pr7819:comments:4':'Focal entry: child-transaction dependency retained as a candidate with technical-context alternative. Repeated-operation computational blowup is context; need/must do not establish institutional obligation.',
'pr7819:comments:5':'Focal entry: terminology edit and delay-option suggestion extracted, with interest in additional outputs preserved separately. Timeout and potential-abort qualifications are attached to the option rather than lost or promoted to unconditional duties.',
'pr7819:comments:6':'Focal entry: conditional spelling correction extracted pragmatically, preserving the supplied fragment and the alternative to Greg\'s suggestion.',
'pr7819:comments:7':'Focal entry: elliptical rebase request extracted; actor and authority are not invented.',
'pr7819:comments:8':'Focal entry: reported closure and inclusion in #8182 are outcome context. No independent prescription is asserted, and closure does not imply rejection or sanction.',
'pr7819:metadata':'Supplemental/context entry screened for object identity and recorded outcome. Closed state plus merged false supports closure without integration. Context-only screening is not an assertion of no institutional significance.',
'pr7819:supplement_metadata':'Supplemental/context entry screened for canonical #7819 identity, recorded closure, and retained head provenance. Merge_commit_sha is not treated as integration when merged is false. Not an exhaustive proposition-extraction target.',
'pr8182:supplement_metadata':'Supplemental/context entry screened separately for #8182 identity and closure without merge. Its outcome is not attributed to #7819 or to the specific feature contents. Not an exhaustive proposition-extraction target.',
'pr7819:patch:0':'Supplemental technical artifact screened: checkbox and tooltip at retained head support limited claims about prepared code. Tooltip capability and higher-fee/unconfirmed conditions are technical, not authority; not an exhaustive extraction target.',
'pr7819:patch:1':'Supplemental technical artifact screened: propagation of checkbox state and conditional red replaceable confirmation with bang. Retained head is not a before/after chronology and does not establish review-driven implementation. Not an exhaustive extraction target.',
'pr7819:patch:2':'Supplemental technical artifact screened: optInRBF propagation to CreateTransaction flags. No integration or institutional authorization inferred; context-only is a selection-scope decision, not absence of institutional significance.',
'pr7819:patch:3':'Supplemental technical artifact screened: prepareTransaction signature defaults optInRBF false. Technical API behavior, not authorized discretion; not an exhaustive proposition-extraction target.',
'pr7819:patch:4':'Supplemental technical artifact screened: sign-to-flags refactor, nSequence selection, signing and dummy-signature handling. No governance rule or adoption inferred; not an exhaustive proposition-extraction target.',
'pr7819:patch:5':'Supplemental technical artifact screened: flag enum and CreateTransaction signature. Definitions are technical rather than constituted institutional roles; not an exhaustive proposition-extraction target.'}
screen=[]
for e in packet['entries']:
    us=[u for u in units if u['source_id']==e['source_id']]
    disp='candidate' if any(u['record_role']=='statement' for u in us) else ('empty' if not e['text'].strip() else 'context_only')
    screen.append({'source_id':e['source_id'],'disposition':disp,'reason':screen_reasons[e['source_id']],'unit_ids':[u['unit_id'] for u in us]})

def claim(parts,**extra):
    return {'claim':' '.join(p[0] for p in parts),'evidence':uniq([e for p in parts for e in p[1]]),'claim_parts':[{'text':p[0],'evidence':p[1]} for p in parts],**extra}
outs=[]
outs.append(claim([
 ('jonasschnelli reported closing #7819 in favor of #8182, saying its contents were included there.',[ue('U25')]),
 ('The #7819 metadata records closure on 2016-06-09 with merged false.',deepcopy(ID)+deepcopy(CLOSED)),
 ('The separate #8182 metadata records closure on 2016-12-06 with merged false.',[a('pr8182:supplement_metadata','"url": "'+NEXT+'"'),a('pr8182:supplement_metadata','"state": "closed"'),a('pr8182:supplement_metadata','"merged": false'),a('pr8182:supplement_metadata','"closed_at": "2016-12-06T10:15:00Z"')])]))
outs.append(claim([
 ('The retained #7819 head shows an optInRBF checkbox labeled Allow Replace-By-Fee.',[a('pr7819:patch:0','+      <widget class="QCheckBox" name="optInRBF">'),a('pr7819:patch:0','+        <string>Allow Replace-By-Fee</string>')]),
 ('Its confirmation branch still contains the red color markup and This transaction is replacable (optin-RBF)! wording.',[a('pr7819:patch:1','+    if (ui->optInRBF->isChecked())\n+    {\n+        questionString.append("<hr /><span style=\'color:#aa0000;\'>");\n+        questionString.append(tr("This transaction is replacable (optin-RBF)!"));')])]))
mechs=[]
mechs.append(claim([
 ('luke-jr questioned exposing the feature until wallet replacement was possible.',[ue('U04')]),
 ('The author quoted that concern and explicitly agreed, while saying that the replacement GUI remained in progress and review could proceed already.',[ue('U11'),ue('U12'),a('pr7819:comments:2',"I'm working on the replacement GUI process but this can be reviewed already.")])],category='scope_management',unit_ids=['U04','U11','U12','U13'],alternative_explanation='The exchange may express compatible technical opinions rather than a recognized institutional gate. Agreement and review/exposure separation do not show that a release condition was adopted or enforced.',status='supported_sequence'))
mechs.append(claim([
 ('gmaxwell offered an adaptive-fee switch in place of a replaceable switch.',[ue('U10')]),
 ('The author quoted it, tentatively called it a solution, reported trying additional outputs through transaction editing, and asked whether to focus only on fee increases.',[ue('U14'),ue('U15'),ue('U16'),ue('U17')]),
 ('gmaxwell explained the additional-output child-transaction dependency and repeated-operation computational growth, then expressed interest in adding outputs with a delayed-sending option.',[ue('U18'),ue('U19'),ue('U21'),ue('U22')])],category='reason_giving',unit_ids=['U10','U14','U15','U16','U17','U18','U19','U21','U22'],alternative_explanation='The comments may explore parallel technical possibilities rather than change anyone\'s preferred scope. The packet supplies no completed design choice or verified implementation of these alternatives.',status='supported_sequence'))
annotation={'schema_version':'0.4','run_id':'F03_v04_r1','episode_id':'F03','packet_sha256':hashlib.sha256((P/'packet.json').read_bytes()).hexdigest(),'entry_screening':screen,'units':units,'relations':relations,'episode_summary':{'observed_outcomes':outs,'mechanisms':mechs,'missing_evidence':['No complete body/comment edit history or reliable full reply threading; recorded timestamps do not date every retained sentence.','No rendered image contents; screenshots linked in the body are not independent evidence here.','No full patch chronology showing whether any recommendation caused a code change.','No supplied content or patches for #8182 verifying the author\'s report of inclusion, despite separately supplied outcome metadata.','No institutional authorization, maintainer-permission record, enforcement claim, or recurring governance provision supporting a rule classification.','No canonical decision-object identity for the distinct future replacement/add-output workflow discussed in comments 3–5.','No evidence of repository integration of either supplied PR or Bitcoin network adoption.','No outcome record for referenced refactoring source #7159; its presence in provenance does not establish its disposition.'],'unresolved_questions':['Whether the readiness discussion expressed an institutional expectation or solely a product/engineering recommendation.','Whether current-review can expresses feasibility or permissive encouragement; no authority grant is established.','Whether personal review intention and the reported additional-output attempt warrant strategy status rather than context-only treatment.','How the [send immediately] label is intended to coexist with delayed sending; the supplied wording is retained.','Whether any label, red-style, punctuation, fee-focus, or delayed-send recommendation was later implemented in another contribution.']}}
(P/'annotation.json').write_text(json.dumps(annotation,ensure_ascii=False,indent=2)+'\n')
(P/'annotation.first_complete.json').write_bytes((P/'annotation.json').read_bytes())
print(json.dumps({'units':len(units),'statements':sum(u['record_role']=='statement' for u in units),'screened_entries':len(screen),'relations':len(relations),'packet_sha256':annotation['packet_sha256']}))
