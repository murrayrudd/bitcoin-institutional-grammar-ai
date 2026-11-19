import json, hashlib, platform
from pathlib import Path
ROOT=Path(__file__).resolve().parent
P=json.loads((ROOT/'packet.json').read_text())
S={e['source_id']:e for e in P['entries']}
F=set(P['selection_design']['focal_source_ids'])
U=[]; R=[]

def sid(n):
    if isinstance(n,int): return f'pr26586:comments:{n}'
    if n.startswith('r') and n[1:].isdigit(): return 'pr26586:review_comments:'+n[1:]
    if n=='body': return 'pr26586:body'
    return n

def span(s,q=None,start=None):
    s=sid(s); t=S[s]['text']
    if q is None: q=t
    if start is None: start=t.index(q)
    assert t[start:start+len(q)]==q,(s,q)
    return {'start':start,'end':start+len(q),'quote':q}

def E(s,q=None,start=None): return {'source_id':sid(s),'span':span(s,q,start)}
def C(s,symbol,text,q=None,basis='explicit',role='local',note='',source=None,start=None):
    source=sid(source if source is not None else s)
    return {'symbol':symbol,'text':text,'basis':basis,'evidence':[E(source,q if q is not None else text,start)],'inference_note':note,'occurrence_role':role}
def unit(i,s,q=None,**kw):
    s=sid(s); sp=span(s,q)
    x={'unit_id':i,'source_id':s,'span':sp,'parent_unit_id':None,'grammar':'regulative','speech_act':'proposed','scope':'case_specific','components':[],
       'institution':{'type':'undetermined','standing':'text_only','dispute_present':False,'rationale':'Case-specific proposal is institutionally plausible as review coordination, but does not by itself establish a social expectation, attributed authorization, or enforcement.','evidence':[E(s,sp['quote'],sp['start'])],'recognition':[],'authority_evidence':[]},
       'statement_target_level':'operational','observed_action_level':'operational','level_rationale':'The focal action concerns this contribution or its review under existing repository arrangements; no new decision-making power is specified.','complexity_flags':['none'],'alternative_interpretation':'','confidence':'plausible','uncertainty_reason':'The distinction between a technical suggestion and an institutional expectation is not settled by this occurrence.','record_role':'statement','parse_mode':'literal','deontic_force':'recommendation','level_alternatives':[],
       'presentation':{'quotation':'none','markup':'plain','rationale':'Plain occurrence in supplied text; no complete edit history is available.'},'disposition_events':[]}
    x.update(kw); U.append(x); return x

def inst(x,typ='undetermined',standing='text_only',rationale='',dispute=False,evidence=None):
    x['institution'].update(type=typ,standing=standing,dispute_present=dispute,rationale=rationale or x['institution']['rationale'])
    if evidence is not None:x['institution']['evidence']=evidence
    return x

def context(i,s,q=None,speech='technical_description',role='context',**kw):
    x=unit(i,s,q,record_role=role,grammar='not_institutional',speech_act=speech,deontic_force='nondeontic',statement_target_level='not_applicable',components=[],confidence='clear',uncertainty_reason='',level_rationale='Context records an attributable contribution, report, or technical rationale within ordinary review; it does not itself encode a prescription.',**kw)
    inst(x,'not_applicable','not_applicable','Nonstatement record retained for context or a relation endpoint; no independent institution is asserted.')
    return x

def quote(i,s,q,original):
    x=context(i,s,q,speech='other',role='quotation',presentation={'quotation':'repeated','markup':'plain','rationale':'Markdown block quotation repeats a proposition already represented in this packet; it is not an additional endorsement.'})
    rel(i,original,'quotes','explicit','Repeated occurrence reproduces the represented original proposition, with attribution supported by the exact matching text.',[E(s,q),ev(original)])
    return x

def get(i):return next(x for x in U if x['unit_id']==i)
def ev(i):x=get(i);return E(x['source_id'],x['span']['quote'],x['span']['start'])
def rel(a,b,typ,basis,why,evidence=None,scope='not_applicable'):
    R.append({'from_unit_id':a,'to_unit_id':b,'type':typ,'basis':basis,'rationale':why,'evidence':evidence or [ev(a),ev(b)],'logic_scope':scope})
def recognition(i,kind,target,basis,why,evidence):get(i)['institution']['recognition'].append({'kind':kind,'target':target,'basis':basis,'rationale':why,'evidence':evidence})
def disposition(i,kind,target,basis,why,evidence):get(i)['disposition_events'].append({'kind':kind,'target':target,'basis':basis,'rationale':why,'evidence':evidence})

# Body: recurring method, distinct referrals, and the explicitly negated need.
x=unit('u01','body','The same procedure as every release',speech_act='asserted',scope='general',parse_mode='pragmatic',deontic_force='nondeontic',components=[
 C('body','I','repeat the prior release-update procedure','The same procedure as every release',basis='context_inferred',role='semantic_inference',note='The nominal assertion describes recurrence; repeating a release-update method is reconstructed, not a source verb.'),
 C('body','Bdir','previous-release test additions','The same procedure',basis='context_inferred',role='semantic_inference',note='The method is elliptical. The immediately referenced v23.0 and v22.0 commit messages identify previous-release additions; this is not a complete reconstructed workflow.'),
 C('body','Cac','every release','every release')],alternative_interpretation='A retrospective technical analogy introducing this PR, rather than a general institutional strategy or obligation.',level_rationale='The focal method is recurring release-test maintenance, not authority allocation. General recurrence can be described operationally without observing adoption of a new policy.')
inst(x,'strategy_candidate','text_only','The author describes a recurring method by analogy to two pinned previous-release additions. This is an asserted practice, not a rule or demonstrated universal compliance.',evidence=[ev('u01'),E('commit:dba123167236a172d2d33861d58aa94a19729671:metadata','test: previous releases: add v23.0'),E('commit:d8b705f1caeb3b4a6790cb26e4e5584ca791d965:metadata','test: previous releases: add v22.0')])
x=unit('u02','body','see dba123167236a172d2d33861d58aa94a19729671 [v23.0] and d8b705f1caeb3b4a6790cb26e4e5584ca791d965 [v22.0]',components=[
 C('body','I','see'),C('body','Bdir','dba123167236a172d2d33861d58aa94a19729671 [v23.0] and d8b705f1caeb3b4a6790cb26e4e5584ca791d965 [v22.0]')],complexity_flags=['compound'],alternative_interpretation='The parenthetical may function as a citation rather than a request to navigate; both complete commit objects are preserved.')
x=unit('u03','body',"we don't need to extend the tag list in the CI scripts and test/README.md anymore.",speech_act='asserted',scope='general',deontic_force='no_obligation',components=[
 C('body','A','we'),C('body','D',"don't need to"),C('body','I','extend'),C('body','Bdir','the tag list'),C('body','Cex','in the CI scripts and test/README.md'),C('body','Cex','anymore')],alternative_interpretation='The negated need is technical redundancy created by the fetch-script default, not necessarily relief from an institutional duty.',level_rationale='The assertion concerns recurring release-maintenance work in the specified CI scripts and README; automation changes practical work, without evidence of changed governance powers.')
inst(x,rationale='The text expressly denies a need to extend the tag lists, after describing automatic tag selection. The no_obligation label records negated necessity while institutional obligation remains a technical-versus-normative alternative.',evidence=[ev('u03'),E('body',"thanks to #25650, the previous release fetch script defaults to downloading/building the necessary tags")])

# Bot navigation, conditional correction instruction, and separately stated consequence.
x=unit('u04',0,'See [the guideline](https://github.com/bitcoin/bitcoin/blob/master/CONTRIBUTING.md#code-review) for information on the review process.',components=[
 C(0,'I','See'),C(0,'Bdir','[the guideline](https://github.com/bitcoin/bitcoin/blob/master/CONTRIBUTING.md#code-review)'),C(0,'Cex','for information on the review process')],template_note='Apparently reusable bot wording, coded only as the present referral; the mutable master link is not identical to the separately supplied pinned guide revision.')
x=unit('u05',0,'If your review is incorrectly listed, please react with 👎 to this comment',components=[
 C(0,'A','the reviewer whose review is incorrectly listed','your review',basis='context_inferred',role='semantic_inference',note='The possessor in the conditional identifies the intended reacting addressee; no explicit actor noun occurs in the imperative.'),
 C(0,'I','react'),C(0,'Bdir','this comment'),C(0,'Cac','If your review is incorrectly listed'),C(0,'Cex','with 👎')],template_note='Template-like bot correction path applies to this review listing. Please supplies politeness, not lexical D.',alternative_interpretation='A practical bot-use instruction rather than a socially expected correction duty.')
inst(x,'norm_candidate',rationale='The bot proposes how an incorrectly listed reviewer should request correction; only the expressed expectation is established, without evidence that anyone used it.')
x=unit('u06',0,'the bot will ignore it on the next update.',speech_act='asserted',deontic_force='nondeontic',components=[
 C(0,'A','the bot'),C(0,'I','ignore'),C(0,'Bdir','it (review or comment referent unresolved)','it',basis='unresolved',role='unresolved',note='The nearest noun is comment while the preceding condition concerns a review listing. The exact object the bot ignores is not independently specified.'),
 C(0,'Cac','a 👎 reaction when a review is incorrectly listed','If your review is incorrectly listed, please react with 👎 to this comment',basis='context_inferred',role='shared_scope',note='The preceding coordinated instruction supplies the procedural trigger for this stated effect; no actual reaction is observed.'),C(0,'Cex','on the next update')],complexity_flags=['unresolved_reference'],alternative_interpretation='A description of software behavior rather than an institutional consequence; the ignored object may be the review entry or its source comment.',uncertainty_reason='The ignored referent is ambiguous and no bot execution is supplied.')
inst(x,rationale='An announced procedural response by a bot, not an enforcement sanction or observed removal. Future will is predictive, not D.')
rel('u05','u06','O','explicit','The coordinated sentence announces ignoring on the next update following the reaction instruction. This is a stated procedural effect, not evidence that it occurred.',[E(0,'If your review is incorrectly listed, please react with 👎 to this comment and the bot will ignore it on the next update.')])

# Early discussion.
context('c01',1,speech='asserted',alternative_interpretation='The concern could pragmatically invite delay, but the utterance itself wonders about release withdrawal and does not instruct anyone to withdraw it.')
x=unit('u07',2,'Sounds good to hold off a bit.',parse_mode='pragmatic',components=[
 C(2,'I','hold off'),C(2,'Bdir','progressing or integrating this PR','hold off',basis='context_inferred',role='semantic_inference',note='Hold off has an unexpressed target. The PR setting and preceding release-withdrawal concern bound it, but do not distinguish integration from other progress.'),C(2,'Cex','a bit')],alternative_interpretation='Agreement with a perceived pause rather than a new instruction; the exact delayed activity is not specified.',complexity_flags=['unresolved_reference'])
rel('c01','u07','uptake','context_inferred','The subsequent hold-off suggestion plausibly responds to the release-withdrawal concern; no explicit reply threading is available.')
x=unit('u08',2,'Meanwhile it needs a rebase after #26589.',speech_act='asserted',parse_mode='pragmatic',components=[
 C(2,'I','rebase','a rebase',basis='context_inferred',role='semantic_inference',note='The noun rebase is reconstructed as the requested action.'),C(2,'Bdir','this PR','it',basis='context_inferred',role='semantic_inference',note='The grammatical subject it becomes the target of the reconstructed rebase action; the PR setting resolves the likely referent.'),C(2,'Cac','after #26589')],alternative_interpretation='A technical dependency report rather than a contribution-duty claim; after #26589 does not supply its integration date or details.')
context('c03',3,speech='reported_action')
context('c04',4,"@luke-jr one reason for the backwards compatibility tests is to ensure there's no accidental breakage between versions, including wallet upgrades, consensus and p2p bugs.",speech='asserted')
x=unit('u09',4,'So I think we should add every major release.',scope='general',components=[C(4,'A','we'),C(4,'D','should'),C(4,'I','add'),C(4,'Bdir','every major release')],observed_action_level='collective_choice',level_alternatives=['collective_choice'],level_rationale='The focal expectation governs operational addition of every major release to compatibility tests. The visible exchange deliberates a recurring release-selection arrangement, so observed deliberation is collective choice; coding the proposed criterion itself as the target would also be defensible.',alternative_interpretation='A preferred engineering coverage strategy rather than a binding expectation; a proposal to choose a general inclusion policy could instead have collective-choice target level.')
inst(x,'norm_candidate','disputed','A general should expectation is proposed and challenged by narrower feature-specific selection and cost objections. No attributed authorization is supplied.',True)
x=unit('u10',4,'Apart from that, #25717 alone should justify adding v24.0 (or whatever ends up widely available for download).',speech_act='asserted',parse_mode='pragmatic',components=[
 C(4,'I','add','adding',basis='context_inferred',role='semantic_inference',note='The literal predicate is justify; the supported addition is reconstructed as a recommendation.'),C(4,'Bdir','v24.0 (or whatever ends up widely available for download)','v24.0 (or whatever ends up widely available for download)',basis='context_inferred',role='semantic_inference',note='The object is embedded under adding; it becomes the target of the inferred focal recommendation, retaining the availability alternative.')],alternative_interpretation='A reason supporting the existing PR rather than an independently executable new request. Should qualifies the expected justificatory strength of #25717, not lexical duty to add.')
context('c05a',5,"Though, `test/functional/feature_backwards_compatibility.py` doesn't test watch-only miniscript support.")
context('c05b',5,'It is likely so general that it can\'t catch any issues.',speech='asserted')
x=unit('u11',5,'I much more prefer specific tests, like the ones you can find with `git grep -l skip_if_no_prev`',speech_act='asserted',scope='general',parse_mode='pragmatic',components=[
 C(5,'I','use','I much more prefer specific tests',basis='context_inferred',role='semantic_inference',note='The literal preference is interpreted as a recommendation to use specific tests.'),C(5,'Bdir','specific tests, like the ones you can find with `git grep -l skip_if_no_prev`',basis='context_inferred',role='semantic_inference',note='Specific tests is the literal object of prefer, and is assigned an inferred target role under use; the exact search expression is retained as an identifying example.')],alternative_interpretation='An individual engineering preference without a directive or social expectation. The embedded search command illustrates the preferred tests rather than clearly directing a separate navigation action.',level_rationale='The focal recommendation concerns the method of compatibility testing, bounded to this engineering discussion; general technical advice alone does not establish revision of a collective governance rule.')
quote('q01',6,"It is likely so general that it can't catch any issues.",'c05b')
context('c06a',6,"Probably not, but it's a low cost check.",speech='asserted')
quote('q02',6,"doesn't test watch-only miniscript support",'c05a')
x=unit('u12',6,"But we can also keep this PR open until there's another PR that needs it.",components=[
 C(6,'A','we'),C(6,'I','keep'),C(6,'Bdir','this PR'),C(6,'Cex',"open until there's another PR that needs it")],deontic_force='unresolved',alternative_interpretation='Can offers a feasible workflow option, not necessarily authorized discretion. The wording can also be read as a recommendation to defer integration.',level_rationale='Keeping this particular PR open pending a dependent contribution is operational management within the existing contribution workflow.')
inst(x,'strategy_candidate',rationale='A specific conditional management method is articulated. No commitment, duty, or demonstrated authority to impose it is established.')
context('c06b',6,"We've previously piled several major releases this way. Back then it was more work to rebase than it is now. Every time it's rebased, the CI runs the checks again, so it's useful even in an unmerged state.",speech='asserted')
quote('q03',7,"Probably not, but it's a low cost check.",'c06a')
context('c07',7,'Not sure if it will stay low cost forever, if the matrix is append-only with no plan to remove some or all previous releases?',speech='question',alternative_interpretation='The cost question may invite a pruning plan, but it does not itself specify a proposed removal or a duty to make a plan.')
quote('q04',8,"Probably not, but it's a low cost check.",'c06a')
quote('q05',8,'Not sure if it will stay low cost forever, if the matrix is append-only with no plan to remove some or all previous releases?','c07')
x=unit('u13',8,'We can remove intermediate releases at some point.',components=[C(8,'A','We'),C(8,'I','remove'),C(8,'Bdir','intermediate releases'),C(8,'Cex','at some point')],deontic_force='unresolved',scope='general',alternative_interpretation='An available technical option, a suggestion, or a claim of permission; can does not independently demonstrate authorization.',level_rationale='The offered action is future maintenance of the compatibility matrix; no decision allocating removal authority is shown.')
quote('q06',9,"Probably not, but it's a low cost check.",'c06a')
context('c09',9,"It's not low cost.",speech='asserted')
x=unit('u14',9,"To run the test at all, you have to keep a built copy of every single release listed. (And no, guix static binaries aren't a good alternative.)",speech_act='asserted',deontic_force='unresolved',scope='general',components=[
 C(9,'A','you'),C(9,'D','have to'),C(9,'I','keep'),C(9,'Bdir','a built copy of every single release listed'),C(9,'Cex','To run the test at all')],alternative_interpretation='Technical necessity for the described test, rather than institutional obligation. The parenthetical expressly rejects guix static binaries as a good alternative, but supplies no sanction or authority.',level_rationale='The alleged prerequisite concerns running this compatibility test. A technical dependency does not allocate governance power.')
inst(x,rationale='A necessity claim is retained because have to could read as a testing requirement. Its cost argument and rejected binary alternative favor technical necessity; institutional force is unresolved.')

# Alternatives to the test setup and release-selection method.
x=unit('u15',10,'Instead of hardcoding the version numbers in `feature_backwards_compatibility.py` we could have it loop over whatever is available under `releases/v*`.',parse_mode='pragmatic',components=[
 C(10,'A','we'),C(10,'I','configure','could have it loop over',basis='context_inferred',role='semantic_inference',note='The suggestion to have the script loop is reconstructed as a configure action; could is exploratory rather than permission.'),
 C(10,'Bdir','feature_backwards_compatibility.py','`feature_backwards_compatibility.py`',basis='context_inferred',role='semantic_inference',note='The source names a location of hardcoding and then uses it as the script antecedent; its target-of-configuration role is inferred.'),
 C(10,'Cex','loop over whatever is available under `releases/v*` instead of hardcoding version numbers','Instead of hardcoding the version numbers in `feature_backwards_compatibility.py` we could have it loop over whatever is available under `releases/v*`.',basis='context_inferred',role='semantic_inference',note='This reconstructed execution specification preserves both the directory wildcard and substitution for hardcoding.'),
 C(10,'Cex','retain the fetching default of all binaries','The default of `test/get_previous_releases.py` would still to fetch all the binaries.',basis='context_inferred',role='shared_scope',note='The later sentence expressly describes an unchanged default under the same proposed approach; it lies outside this smallest action span.')],alternative_interpretation='A one-off software design suggestion rather than a governance strategy; the stated unchanged fetching default is retained as a qualification.',complexity_flags=['nested_component'])
inst(x,'strategy_candidate',rationale='An explicit alternative testing method is articulated, including replacing hardcoding with discovery while retaining the download default. It is not an attributed rule.')
x=unit('u16',10,"In that case it's up to the developer which previous releases they want to test.",speech_act='asserted',parse_mode='pragmatic',deontic_force='unresolved',scope='general',components=[
 C(10,'A','the developer','the developer',basis='context_inferred',role='semantic_inference',note='The literal up-to construction allocates choice; the role as actor of reconstructed choose is inferred from that allocation.'),
 C(10,'I','choose',"it's up to the developer",basis='context_inferred',role='semantic_inference',note='Choose is not a source verb; it paraphrases up to the developer.'),
 C(10,'Bdir','which previous releases they want to test',basis='context_inferred',role='semantic_inference',note='The interrogative complement specifies the content of a reconstructed choice, rather than an explicit object of choose.'),
 C(10,'Cac','In that case',note='That case refers to the preceding proposed directory-based loop; the condition is expressed locally, while its antecedent is supplied by u15.')],alternative_interpretation='Technical user configurability, not institutionally authorized discretion. A constitutive parse of developer choice could preserve the same conditional allocation.',level_rationale='The possible choice concerns which releases an individual tests under the proposed script. Neither technical configurability nor up-to wording establishes constitutional authority.',complexity_flags=['hybrid_candidate'])
inst(x,rationale='The conditional up-to statement plausibly allocates test-selection discretion, but technical flexibility and institutional permission cannot be distinguished.')
rel('u16','u15','clarifies','explicit','In that case explicitly describes the test-selection consequence of the proposed directory loop, without claiming an observed implementation.')
x=unit('u17',11,'So maybe the EOL versions can be dropped',speech_act='question',scope='general',components=[C(11,'I','be dropped'),C(11,'Bdir','the EOL versions')],alternative_interpretation='An exploratory technical option rather than a binding prohibition on EOL versions; maybe and can weaken force.',level_rationale='The proposal removes EOL versions from compatibility testing, a maintenance choice. Deliberating a recurring retention arrangement admits collective-choice interpretation.',level_alternatives=['collective_choice'])
x=unit('u18',11,'the qa-assets repo hosts some regtest wallets instead?',speech_act='question',scope='general',components=[C(11,'A','the qa-assets repo'),C(11,'I','hosts'),C(11,'Bdir','some regtest wallets'),C(11,'Cex','instead')],alternative_interpretation='Technical storage design instead of running EOL versions; the repository is the literal hosting actor, not an inferred human official.',level_rationale='The focal action is hosting test assets as a substitute method, not allocating governance authority.')
rel('u17','u18','AND','explicit','The question couples dropping EOL versions with hosting regtest wallets instead; both proposed actions are retained.',[E(11,'So maybe the EOL versions can be dropped and the qa-assets repo hosts some regtest wallets instead?')],scope='actions')
context('c11',11,"In any case the test fails intermittently (#24400), so apart from obvious smoke test issues that happen on every iteration, I don't think anyone even looks into failures here.",speech='asserted')
x=unit('u19',12,'Noting that if this is still going ahead, it should be updated to use 24.0.1.',speech_act='asserted',components=[
 C(12,'D','should'),C(12,'I','be updated'),C(12,'Bdir','it (this PR)','it',basis='context_inferred',role='context_reference',note='Passive it remains the update target; this is still going ahead and the PR context supply its referent, not a named version object.'),C(12,'Cac','if this is still going ahead'),C(12,'Cex','to use 24.0.1')],alternative_interpretation='A technical review recommendation contingent on pursuing the PR, not an authority-backed integration condition.')
context('c13a',13,'Rebased on master',speech='reported_action')
context('c13b',13,"updated to v24.0.1 (note that as I'm writing this, the archives on https://bitcoincore.org/bin/ are not available yet for v24.0.1).",speech='reported_action')
rel('u08','c13a','uptake','context_inferred','The author reports the same rebase action later; the text does not explicitly say it responds to Sjors or document the history of #26589.')
rel('u19','c13b','uptake','context_inferred','The later author report specifically names the requested version; temporal and action correspondence support response, not causal identification.')
x=unit('u20',14,'Not sure what to do here. @Sjors?',speech_act='question',parse_mode='pragmatic',components=[
 C(14,'A','Sjors','@Sjors',basis='context_inferred',role='semantic_inference',note='The named addressee is assigned the actor role for the reconstructed invitation to advise.'),C(14,'I','advise','Not sure what to do here. @Sjors?',basis='context_inferred',role='semantic_inference',note='Uncertainty about what to do provides context beyond a bare ping for an invitation to advise.'),C(14,'Bdir','what to do with this PR','what to do here',basis='context_inferred',role='semantic_inference',note='The indirect-question fragment supplies the requested information; here is resolved only to the current PR.')],alternative_interpretation='A ping soliciting attention with no definite request; no invitation to exercise merge authority can be inferred.')

# Final review and management suggestions.
context('c15a',15,'tACK 741908afc1f9ed2040c18667c75665b300c5dfe7\r\n\r\nI checked that it still works on top of current master.',speech='reported_action')
context('c15b',15,"That said, there's no pressing reason to merge this.",speech='asserted',alternative_interpretation='May pragmatically discourage rushing, but the explicit method follows in u21/u22; this clause is its rationale rather than a duplicate negative duty.')
x=unit('u21',15,"As we've done before, we could just leave the PR open",components=[C(15,'A','we',start=S[sid(15)]['text'].index('we could')),C(15,'I','leave'),C(15,'Bdir','the PR'),C(15,'Cex','open')],deontic_force='unresolved',alternative_interpretation='A feasible management option rather than permission or obligation; the claimed precedent is not independently verified.')
inst(x,'strategy_candidate',rationale='The review offers keeping this PR open as part of an explicit keep-open/rebase method. The source reports precedent without supplying separate episodes.')
x=unit('u22',15,'occasionally rebase it.',components=[
 C(15,'A','we','we',basis='explicit',role='shared_scope',note='The subject of the preceding coordinated clause scopes over the rebase action.',start=S[sid(15)]['text'].index('we could')),
 C(15,'I','rebase'),C(15,'Bdir','it (the PR)','it',basis='context_inferred',role='context_reference',note='The explicit object pronoun refers to the PR in the preceding coordinated clause; the grammatical object role is retained but the resolved referent is inferred.',start=S[sid(15)]['text'].index('rebase it.')+7),C(15,'Cex','occasionally')],deontic_force='unresolved',alternative_interpretation='A practical option rather than a requirement to rebase on a schedule. Could in the coordinated clause is exploratory, not permission.')
inst(x,'strategy_candidate',rationale='Periodic rebasing is a separable part of the articulated keep-open method; no actual later rebases are established by this proposal.')
rel('u21','u22','AND','explicit','And coordinates keeping this PR open with occasional rebasing.',[E(15,"As we've done before, we could just leave the PR open and occasionally rebase it.")],scope='actions')
quote('q07',15,"apart from obvious smoke test issues that happen on every iteration, I don't think anyone even looks into failures here",'c11')
x=unit('u23',15,'This can also be a reason to not rush merging new releases.',speech_act='asserted',scope='general',parse_mode='pragmatic',components=[
 C(15,'I','not rush merging','not rush merging',basis='context_inferred',role='semantic_inference',note='The focal recommendation is reconstructed from a reason for not rushing; negation is retained in the action.'),C(15,'Bdir','new releases',basis='context_inferred',role='semantic_inference',note='The embedded merging object becomes the target of the reconstructed recommendation.')],alternative_interpretation='A reason supporting delay rather than an independent prescription. Can predicates justificatory possibility, not permission.',level_rationale='The recommendation concerns pace of release-test contribution integration, with no actor assigned new integration authority.')
context('c15c',15,'This PR itself is where most of the thorough checking happens, at every rebase.',speech='asserted')
x=unit('u24',15,'In any case we can always prune versions in a followup.',components=[C(15,'A','we',start=S[sid(15)]['text'].index('we can always')),C(15,'I','prune'),C(15,'Bdir','versions'),C(15,'Cex','in a followup'),C(15,'Cex','always')],deontic_force='unresolved',alternative_interpretation='Availability of a future technical cleanup, not evidence that it occurred or that a formal removal permission was granted.')
inst(x,'strategy_candidate',rationale='A follow-up cleanup path is articulated. The statement expresses an option, not an implemented pruning decision.')

# Inline selection criterion, alternative obligations, referral, and out-of-scope cleanup.
x=unit('u25','r0','I think it only makes sense to add the latest release for each missing feature.',speech_act='asserted',scope='general',parse_mode='pragmatic',components=[
 C('r0','I','add'),C('r0','Bdir','the latest release'),C('r0','Cex','for each missing feature'),C('r0','Cex','only','only',basis='context_inferred',role='semantic_inference',note='Only literally scopes over makes sense; its restriction is carried into the inferred criterion for addition rather than silently dropped.')],alternative_interpretation='An engineering-selection preference rather than an institutional expectation. Add and its target remain explicitly supplied despite indirect recommendation force.',observed_action_level='collective_choice',level_alternatives=['collective_choice'],level_rationale='The focal recommendation governs additions to the test; the visible exchange deliberates recurring selection criteria. Treating choice of that criterion as the focal target would support collective choice.')
inst(x,'norm_candidate','disputed','A recurring expectation to add only the latest release per missing feature is asserted and directly challenged by the author\'s retain-recent-releases question. No attributed authorization is established.',True)
x=unit('u26','r0','So if you want to add 24.x, you will either need to remove 23.x',speech_act='asserted',deontic_force='obligation',components=[C('r0','A','you'),C('r0','D','need to'),C('r0','I','remove'),C('r0','Bdir','23.x'),C('r0','Cac','if you want to add 24.x')],alternative_interpretation='A strong reviewer recommendation or reasoned technical criterion, rather than an enforceable requirement. Either branch is offered; it is not a claim that both must be completed.')
inst(x,'norm_candidate','disputed','The commenter directly states a conditional need to remove 23.x or explain 24.x. This is an accountability expectation without evidence of rule-making authority; the author challenges sacrificing one recent release for another.',True)
x=unit('u27','r0','explain why 24.x is special',speech_act='asserted',deontic_force='obligation',components=[
 C('r0','A','you','you',basis='explicit',role='shared_scope',note='The explicit subject you in the antecedent and coordinated main clause scopes over this alternative action.'),
 C('r0','D','need to','need to',basis='explicit',role='shared_scope',note='Need to scopes over the remove-or-explain alternatives; future will is not independently treated as D.'),C('r0','I','explain'),C('r0','Bdir','why 24.x is special'),C('r0','Cac','if you want to add 24.x','if you want to add 24.x',basis='explicit',role='shared_scope',note='The introductory conditional activates both alternative actions.')],alternative_interpretation='A demand for technical justification rather than an enforceable obligation. A response denying specialness is not proof the alternative was satisfied to the requester\'s acceptance.')
inst(x,'norm_candidate',rationale='An explicit explanation expectation accompanies the alternative removal condition. No evidence attributes authority to enforce it, and later disagreement with specialness does not automatically make the response a sanction.')
rel('u26','u27','OR','explicit','Either remove 23.x or explain 24.x provides alternatives; the text does not state that performing both is forbidden, so XOR is not imposed.',[E('r0','So if you want to add 24.x, you will either need to remove 23.x or explain why 24.x is special')],scope='actions')
x=unit('u28','r0','see also 16624e6ff3af4429e571f7a606bbbcac336e067a',components=[C('r0','I','see'),C('r0','Bdir','16624e6ff3af4429e571f7a606bbbcac336e067a')],alternative_interpretation='A source citation rather than a navigation request; the complete referenced commit is preserved.')
x=unit('u29','r1','Unrelated: The same goes for the other versions in this file, so someone could do that in a separate pull',components=[
 C('r1','A','someone'),C('r1','I','do'),C('r1','Bdir','that (apply the latest-release-per-missing-feature criterion to the other versions in this file)','that',basis='context_inferred',role='context_reference',note='That and the same goes refer to the preceding inline selection/cleanup discussion; this file is supplied as feature_backwards_compatibility.py in entry metadata, not a new named file in the text.'),C('r1','Cex','in a separate pull')],deontic_force='recommendation',alternative_interpretation='An exploratory cleanup suggestion with no volunteer commitment. Exact retained/removed versions are not enumerated.',complexity_flags=['unresolved_reference'])
inst(x,'strategy_candidate',rationale='The commenter proposes an explicit way to separate cleanup of other versions from the present PR, without imposing a duty on any named contributor.')
quote('q08','r2','I think it only makes sense to add the latest release for each missing feature.','u25')
quote('q09','r2','So if you want to add 24.x, you will either need to remove 23.x','u26')
quote('q10','r2','explain why 24.x is special','u27')
quote('q11','r2','see also [16624e6](https://github.com/bitcoin/bitcoin/commit/16624e6ff3af4429e571f7a606bbbcac336e067a)','u28')
x=unit('u30','r2',"For these wallet backwards compatibility tests, wouldn't it make sense to always keep at least the recent major releases that haven't reached EOL yet as bare minimum rather than sacrificing one for another?",speech_act='question',scope='general',parse_mode='pragmatic',components=[
 C('r2','I','keep'),C('r2','Bdir',"at least the recent major releases that haven't reached EOL yet",note='Although the utterance is an indirect question, the release phrase is explicitly the target of keep in the same predicate; no transformed argument role is introduced.'),C('r2','Cex','For these wallet backwards compatibility tests'),C('r2','Cex','always'),C('r2','Cex','as bare minimum rather than sacrificing one for another')],alternative_interpretation='A technical test-coverage suggestion rather than a shared duty; choosing a recurring minimum-retention arrangement could instead be treated as collective-choice target.',observed_action_level='collective_choice',level_alternatives=['collective_choice'],level_rationale='The focal keep instruction concerns operational coverage of these wallet compatibility tests, retaining the non-EOL minimum and opposition to sacrificing one for another. The exchange is visible deliberation over a recurring selection arrangement.')
inst(x,'norm_candidate','locally_supported','The author proposes an explicit recurring minimum, and Sjors later quotes its core expectation and tentatively agrees. This supports local recognition of the specific expectation, not formal authority, universal adoption, or a binding policy.')
x=unit('u31','r2',"I'd rather verify this assumption (in this case e.g., that wallets created on master can still be opened on both of these versions) rather than potentially miss out on either one of those cases.",speech_act='asserted',deontic_force='nondeontic',components=[
 C('r2','A','I',q='I',start=S[sid('r2')]['text'].index("I'd rather")),C('r2','I','verify'),C('r2','Bdir','this assumption (in this case e.g., that wallets created on master can still be opened on both of these versions)'),C('r2','Cex','rather than potentially miss out on either one of those cases.')],alternative_interpretation='An expression of methodological preference rather than a firm personal plan. Both versions means 24.x and 23.x from the immediately preceding sentence.',level_rationale='The focal method is verifying wallet compatibility on both specified versions, operational testing rather than epistemic governance.')
inst(x,'strategy_candidate',rationale='The author articulates a specific verification method, retaining both versions and the example of wallets created on master. No test execution is claimed in this statement.')
context('c32','r2','ACK on cleaning up the releases list in general',speech='reported_action')
x=unit('u32','r2',"I think that's outside of scope for this PR.",speech_act='asserted',parse_mode='pragmatic',components=[
 C('r2','I','exclude',"outside of scope",basis='context_inferred',role='semantic_inference',note='A scope assertion is interpreted as a recommendation to keep cleanup outside this contribution.'),C('r2','Bdir','cleaning up the releases list in general','cleaning up the releases list in general',source='r2',basis='context_inferred',role='context_reference',note='That resolves to the preceding ACK\'s cleanup object; its action-target role under exclude is inferred, and the evidence lies outside the focal assertion.'),C('r2','Cex','for this PR')],alternative_interpretation='A descriptive assertion about the PR boundary, possibly constitutive of its scope, rather than a new exclusion instruction.')
inst(x,'norm_candidate',rationale='The author asserts a boundary for the present contribution while separately endorsing cleanup generally. This is a scoped review expectation, not evidence of authority over other contributors.')
quote('q12',15,"wouldn't it make sense to always keep at least the recent major releases that haven't reached EOL yet",'u30')
context('c15d',15,'I tend to agree.',speech='asserted')

# Attributable recognition, disputes and links. No general authority is inferred from a merge alias.
rel('c03','u01','challenges','context_inferred','The Concept NACK opposes the broader v24 addition and its necessity, rather than denying the historical existence of prior additions.')
rel('c04','c03','challenges','context_inferred','The addressed response gives a coverage rationale against the stated lack of notable differences; it does not prove the NACK was withdrawn.')
rel('u09','c03','challenges','context_inferred','The general inclusion recommendation responds to the concept objection with a different selection rationale.')
rel('c05a','u10','challenges','context_inferred','The response challenges the miniscript-testing rationale accompanying the proposed addition; it does not prove that no other rationale applies.',[ev('c05a'),ev('u10'),E(4,'On the wallet side this version added watch-only miniscript support (which last time I checked caused problems when downgrading).')])
rel('c06a','c05b','challenges','context_inferred','Probably not appears to concede limited issue detection while low cost supplies a countervailing reason; this does not assert that the test detects such issues.')
rel('c07','c06a','challenges','explicit','The exact quoted low-cost assertion is followed by a question challenging its long-term premise.',[E(7)])
rel('c07','u13','uptake','context_inferred','The pruning possibility follows an exactly repeated cost question and addresses its append-only concern.',[E(8)])
rel('c09','c06a','challenges','explicit','The exact quoted low-cost claim is expressly denied by the same property statement.',[E(9)])
rel('u14','c09','clarifies','explicit','Keeping built copies supplies the immediately stated reason for the not-low-cost claim; it remains a participant claim.',[E(9)])
rel('u25','u09','challenges','context_inferred','The only-latest-per-feature criterion conflicts with adding every major release; these are rival inclusion criteria, not proven rules.')
rel('u30','u25','challenges','context_inferred','After quoting the criterion, the author proposes retaining a minimum of recent non-EOL releases; the full rhetorical relationship is inferred from the contrast.',[E('r2')])
rel('u30','u26','challenges','context_inferred','The author specifically questions sacrificing one recent version for another, challenging the removal branch while preserving the option of testing both.',[ev('u30'),ev('u26')])
rel('u27','u31','uptake','context_inferred','The author responds to the demand for specialness by saying 24.x is not special to 23.x and favoring verification on both. This is a response, not proof of accepted compliance.',[ev('u27'),E('r2',"I don't think 24.x is special to 23.x at all, but I'd rather verify this assumption (in this case e.g., that wallets created on master can still be opened on both of these versions) rather than potentially miss out on either one of those cases.")])
rel('u29','c32','uptake','context_inferred','The general-cleanup ACK is consistent with the prior separate-pull suggestion; it does not endorse a specific version-removal list.')
rel('u32','u29','clarifies','context_inferred','The author endorses general cleanup but states it falls outside this PR, corresponding to the separate-pull suggestion.')
rel('u20','c15a','uptake','context_inferred','The named participant later supplies a tested ACK and management advice. The sequence supports response but lacks reliable formal reply threading.',[ev('u20'),ev('c15a'),ev('u21'),ev('u22')])
rel('u30','c15d','uptake','explicit','The later comment quotes the core keep-recent-non-EOL expectation immediately before I tend to agree; assent is tentative.',[ev('q12'),ev('c15d')])
rel('u24','u32','clarifies','context_inferred','The later follow-up pruning option is compatible with keeping cleanup outside this PR; it does not establish a completed follow-up.')

recognition('u01','endorsement','broader_proposal','explicit','The tested ACK names the final head; it supports this PR, not a universal release-addition obligation.',[ev('c15a')])
recognition('u08','reported_implementation','this_proposition','context_inferred','The author reports rebasing on master; correspondence supports the requested action, while the #26589 dependency is not independently verified.',[ev('c13a'),ev('u08')])
recognition('u19','reported_implementation','this_proposition','context_inferred','The author explicitly reports the exact version update after the request. Its connection to the request is inferred, and archives were unavailable at the stated time.',[ev('c13b'),ev('u19')])
recognition('u20','response','this_proposition','context_inferred','Sjors supplies a tested review and advice after the addressed uncertainty; no invitation to exercise authority is inferred.',[ev('u20'),ev('c15a'),ev('u21'),ev('u22')])
recognition('u25','response','this_proposition','explicit','The author exactly quotes the criterion before offering a competing minimum; the response disputes that criterion rather than recognizing it as binding.',[ev('q08'),ev('u30')])
recognition('u26','response','this_proposition','explicit','The exact remove-or-explain wording is quoted before the challenge to sacrificing one version for another.',[ev('q09'),ev('u30')])
recognition('u27','response','this_proposition','context_inferred','The author responds that 24.x is not special but favors checking both versions; whether the explanation satisfies the request is unestablished.',[E('r2',"I don't think 24.x is special to 23.x at all, but I'd rather verify this assumption (in this case e.g., that wallets created on master can still be opened on both of these versions) rather than potentially miss out on either one of those cases.")])
recognition('u29','endorsement','broader_proposal','context_inferred','The author ACKs cleaning the releases list in general, without endorsing an exact cleanup patch or its version choices.',[ev('c32'),ev('u32')])
recognition('u30','expectation_recognition','this_proposition','explicit','The later quotation preserves the recurring keep-at-least-recent-non-EOL expectation, immediately followed by tentative agreement. This is specific recognition of that expectation, not merely a broad ACK or verified enforcement.',[ev('q12'),ev('c15d')])
merge=[E('pr26586:metadata','"merged_at": "2023-02-16T14:04:28+00:00"'),E('pr26586:metadata','"merged": true')]
for i in ['u01','u19','u30']:
 recognition(i,'recorded_status','broader_proposal','explicit','The PR metadata records integration of the broader contribution; it does not verify adoption of each associated general expectation.',merge)
 disposition(i,'recorded_merged','broader_proposal','explicit','Metadata records the PR as merged. No rule adoption, authority transfer, or network adoption follows from this status.',merge)
disposition('u19','reported_implemented','this_proposition','context_inferred','The author reports updating the contribution to v24.0.1 after the matching request, qualified by unavailable release archives at that time.',[ev('u19'),ev('c13b')])
disposition('u08','reported_implemented','this_proposition','context_inferred','Rebased on master reports the requested rebase action, without independently verifying #26589 ancestry.',[ev('u08'),ev('c13a')])

screen_reason={
 'pr26586:body':'Exhaustive focal screening: recurring release-update method, separate commit referral, and denial of the former tag-list need retained; automatic downloading/building is contextual rationale.',
 sid(0):'Exhaustive focal screening: guideline referral, conditional reaction instruction, and announced bot response retained. Review table, metadata banner, and conflict status are context, not independent endorsements.',
 sid(1):'Exhaustive focal screening: speculative release-withdrawal concern and wallet-bug prediction remain context; no instruction to withdraw a release is supplied.',
 sid(2):'Exhaustive focal screening: pause and rebase are distinct proposals. Appreciation of the smaller commit and fetch-script behavior supplies technical context.',
 sid(3):'Exhaustive focal screening: Concept NACK is a review act with technical reasons; no separate enforceable veto or instruction is inferred.',
 sid(4):'Exhaustive focal screening: general major-release inclusion and a specifically qualified v24 addition are retained; accident-prevention and miniscript claims are supporting rationale.',
 sid(5):'Exhaustive focal screening: specific-test preference retained as an uncertain indirect recommendation; technical limitations preserved as context, and illustrative git grep command is not a separate clear request.',
 sid(6):'Exhaustive focal screening: quoted limitations, low-cost counterreason, conditional keep-open strategy, and claimed rebase utility retained. Descriptions of prior additions are not newly asserted duties.',
 sid(7):'Exhaustive focal screening: repeated quote and cost question remain context; a request to make a removal plan is a bounded alternative, not a specified prescription.',
 sid(8):'Exhaustive focal screening: repeated low-cost/cost-concern quotations are separate from the new intermediate-release removal option.',
 sid(9):'Exhaustive focal screening: cost denial and technical prerequisite retained; no institutional sanction or binary-related prohibition is inferred.',
 sid(10):'Exhaustive focal screening: discovery-based testing method, preserved download default, and conditional developer choice retained, with technical-versus-permission uncertainty.',
 sid(11):'Exhaustive focal screening: dropping EOL versions and hosting substitute regtest wallets are distinct linked proposals. Comparative compatibility priorities and failure-attention claims remain technical context.',
 sid(12):'Exhaustive focal screening: conditional version update recommendation retained with the going-ahead qualifier.',
 sid(13):'Exhaustive focal screening: author reports rebase and version update; archive-unavailability qualification preserved. No new prescription is supplied.',
 sid(14):'Exhaustive focal screening: an uncertain invitation to advise is supported by expressed uncertainty plus the named addressee; a bare ping alternative is retained.',
 sid(15):'Exhaustive focal screening: tested ACK, keep-open and rebase method, not-rushing recommendation, repeated quotes, tentative minimum-coverage recognition, and follow-up pruning option retained; no pressing reason and thorough-checking claims remain rationale.',
 sid('r0'):'Exhaustive focal screening: recurring inclusion criterion, conditional remove-or-explain alternatives, and distinct commit navigation retained.',
 sid('r1'):'Exhaustive focal screening: extension of the cleanup method to other versions is retained with the separate-pull constraint and unresolved exact version list.',
 sid('r2'):'Exhaustive focal screening: original requests are repeated quotations; minimum recent-release retention, verification strategy, cleanup ACK, and present-PR scope boundary are retained separately.'}
for e in P['entries']:
 if not e['text']:screen_reason[e['source_id']]='Empty focal review body screened; COMMENTED metadata is not speech or endorsement.'
 elif e['source_id'] not in F:
  if e['kind']=='dated_guidance':
   why='Supplied dated guidance contains institutional provisions on contribution, review, integration, and roles. Screened as supplemental context, not an exhaustive extraction target. It is not used to impute authority to a particular commenter or prove compliance with a focal proposal.'
  elif e['kind']=='patch':
   why='Supplied patch screened as technical and historical context. Comments and README instructions may contain institutional candidates, but this supplemental entry is not an exhaustive extraction target. Retained head or commit identity does not prove review causation.'
  elif e['kind']=='commit_metadata':
   why='Pinned commit metadata screened as historical context and attributable rationale, not a new exhaustive extraction target or independent authority claim.'
  else:why='Supplied metadata screened as recorded status/object context; not participant speech or independent endorsement.'
  screen_reason[e['source_id']]=why
screen=[]
for e in P['entries']:
 ids=[x['unit_id'] for x in U if x['source_id']==e['source_id']]
 has=any(x['record_role']=='statement' and x['source_id']==e['source_id'] for x in U)
 screen.append({'source_id':e['source_id'],'disposition':'empty' if not e['text'] else 'candidate' if has else 'context_only','reason':screen_reason[e['source_id']],'unit_ids':ids})

summary={
'observed_outcomes':[
 {'claim':'The author reports rebasing on master and updating the PR to v24.0.1, while stating that the release archives were not yet available at the time of the report. The retained head patch adds v24.0.1 test entries and download records.', 'evidence':[E(13),E('pr26586:patch:0'),E('pr26586:patch:1')]},
 {'claim':'Sjors supplies a tested ACK for head 741908afc1f9ed2040c18667c75665b300c5dfe7 and reports checking it on current master. Metadata records the broader PR merged on 2023-02-16; this establishes repository integration, not general policy adoption or network adoption.','evidence':[ev('c15a'),E('pr26586:supplement_metadata','"head_sha": "741908afc1f9ed2040c18667c75665b300c5dfe7"')]+merge},
 {'claim':'The author proposes keeping at least recent major releases that have not reached EOL in these wallet compatibility tests. Sjors later quotes the core expectation and tentatively agrees. The retained patch adds v24.0.1 alongside v23.0; it does not establish acceptance of the criterion as a binding general rule.','evidence':[ev('u30'),ev('q12'),ev('c15d'),E('pr26586:patch:0')]}
],
'mechanisms':[
 {'category':'reason_giving','claim':'A Concept NACK questions the need to add v24. Sjors responds with an accidental-breakage rationale and an every-major-release recommendation. Subsequent cost objections and an only-latest-per-missing-feature criterion contest the expansion; the author answers with a recent-non-EOL minimum and verification on both 23.x and 24.x. Sjors later tentatively agrees with the quoted minimum. This is a supported argumentative sequence, not identification of the cause of the final merge.','evidence':[ev('c03'),ev('c04'),ev('u09'),ev('c07'),ev('c09'),ev('u14'),ev('u25'),ev('u30'),E('r2',"I don't think 24.x is special to 23.x at all, but I'd rather verify this assumption (in this case e.g., that wallets created on master can still be opened on both of these versions) rather than potentially miss out on either one of those cases."),ev('q12'),ev('c15d')],'unit_ids':['c03','c04','u09','c07','c09','u14','u25','u30','u31','c15d'],'alternative_explanation':'The participants may be articulating persistent independent technical preferences; their argument sequence and tentative agreement do not establish that one caused a changed decision or general adoption.','status':'supported_sequence'},
 {'category':'review_coordination','claim':'A reviewer conditionally requests updating the still-pursued PR to 24.0.1, and the author later reports that exact version update with an archive-availability caveat. The retained head patch contains v24.0.1 entries. The correspondence supports a review-to-update sequence, while the patch and eventual merge do not identify a unique cause.','evidence':[ev('u19'),ev('c13b'),E('pr26586:patch:0'),E('pr26586:patch:1')]+merge,'unit_ids':['u19','c13b'],'alternative_explanation':'The author could independently have planned to use the follow-up release; a matching report and later patch do not establish that this particular comment caused the update.','status':'supported_sequence'},
 {'category':'scope_management','claim':'One reviewer suggests handling other-version cleanup in a separate pull request. The author ACKs cleanup generally while placing it outside the current PR; Sjors later offers pruning in a follow-up. The retained patch adds v24.0.1 while retaining v23.0, and the broader PR is recorded merged. This is consistent with separating the addition from cleanup, without evidence that any follow-up cleanup occurred.','evidence':[ev('u29'),ev('c32'),ev('u32'),ev('u24'),E('pr26586:patch:0')]+merge,'unit_ids':['u29','c32','u32','u24'],'alternative_explanation':'The final limited patch may reflect the initial narrow scope independently of these statements. No complete revision history or completed cleanup proposal is supplied.','status':'consistent_with'}
],
'missing_evidence':[
 'No complete body/comment edit history or reliable reply threading; creation timestamps do not date every retained wording or bot table entry.',
 'No full revision chronology or merge decision explanation identifies which review caused which change.',
 'No attributable authorization or enforcement evidence for the disputed release-selection criteria, and no evidence that an ACK or NACK gives its author integration authority.',
 'No observed use of the bot reaction mechanism, and the ignored object remains textually ambiguous.',
 'No supplied outcome for the optional pruning, EOL-wallet substitution, directory-loop approach, or separate cleanup contribution.',
 'The referenced #25650, #26589, #25717, and #24400 are not supplied as full discussions or patches; claims about their effects remain attributed to participants.',
 'The supplied guide is pinned to a dated base revision, not the full historical content of the mutable link when first posted. General documented roles do not establish the authority or status of each named commenter.',
 'No evidence establishes network adoption or a constitutional/epistemic decision in this focal episode.'
],
'unresolved_questions':[
 'Which instructions, if any, participants treated as binding rather than technical recommendations or workflow options?',
 'Does can in keeping the PR open, pruning, and developer choice express mere capability, a proposal, or socially recognized permission?',
 'Did the final patch reflect adoption of a recurring minimum-retention expectation, or only a case-specific addition?',
 'Does the bot ignore the review entry or its source comment after a reaction?',
 'Was the rebase report specifically responsive to #26589, and were the alternative explanation demands considered satisfied?',
 'Are recurring test-selection statements best treated as operational prescriptions deliberated at collective choice, or as proposals directly targeting selection of the recurring arrangement?'
]}
A={'schema_version':'0.3','run_id':'F01_v03_r3','episode_id':'F01','packet_sha256':hashlib.sha256((ROOT/'packet.json').read_bytes()).hexdigest(),'entry_screening':screen,'units':U,'relations':R,'episode_summary':summary}
(ROOT/'annotation.json').write_text(json.dumps(A,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'entries':len(screen),'units':len(U),'statements':sum(u['record_role']=='statement' for u in U),'relations':len(R),'packet_sha256':A['packet_sha256']}))
