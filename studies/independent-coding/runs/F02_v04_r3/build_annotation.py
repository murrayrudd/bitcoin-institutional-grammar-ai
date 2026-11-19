import json, hashlib, platform, sys
from pathlib import Path
from copy import deepcopy

P=Path('packet.json')
p=json.loads(P.read_text())
E={x['source_id']:x for x in p['entries']}
OBJ='https://github.com/bitcoin/bitcoin/pull/14441'

def sid(x): return 'pr14441:'+x

def ev(k,q=None,start=None):
    k=k if k.startswith('pr14441:') else sid(k)
    t=E[k]['text']
    if q is None: q=t
    if start is None: start=t.index(q)
    assert t[start:start+len(q)]==q and q
    return {'source_id':k,'span':{'start':start,'end':start+len(q),'quote':q}}

def unique(es):
    out=[]; seen=set()
    for e in es:
        k=(e['source_id'],e['span']['start'],e['span']['end'])
        if k not in seen: out.append(e);seen.add(k)
    return out

IDENT=ev('supplement_metadata','"url": "https://github.com/bitcoin/bitcoin/pull/14441"')
MERGED=[ev('supplement_metadata','"merged": true'),ev('supplement_metadata','"merged_at": "2018-11-10T11:46:02Z"')]
REV=[ev('supplement_metadata','"head_sha": "89306ab0df93bfdf5630910bc20b1eccb7379172"'),ev('supplement_metadata','"merge_commit_sha": "89306ab0df93bfdf5630910bc20b1eccb7379172"')]
HEAD=MERGED+REV+[IDENT]

units=[]
def base(uid,k,q=None,role='statement',speech='proposed',parse='literal',quotation='none',markup='plain'):
    a=ev(k,q)
    statement=role=='statement'
    u={'unit_id':uid,'source_id':a['source_id'],'span':a['span'],'parent_unit_id':None,
       'grammar':'regulative' if statement else 'not_institutional','speech_act':speech,
       'scope':'case_specific','components':[],
       'institution':{'type':'undetermined' if statement else 'not_applicable','dispute_present':False,
         'rationale':'This is a one-off technical or editorial suggestion in review. No supplied authorization, enforcement provision, recurring social expectation, or committed personal strategy selects a more specific institutional type.' if statement else 'Communicative act retained as context; no independently executable prescription or institutional configuration is asserted here.',
         'evidence':[a], 'recognition':[], 'authority_evidence':[],
         'standing_profile':{k:('none' if statement else 'not_applicable') for k in ['documentary','recognition','application']},
         'documentary_support':[],'application_evidence':[],'challenges':[],'type_alternatives':[]},
       'statement_target_level':'operational' if statement else 'not_applicable',
       'observed_action_level':'operational',
       'level_rationale':'The focal action edits the immediate backport contribution. The visible act is ordinary code review, with no proposal to revise a recurring review arrangement or allocate decision authority.' if statement else 'The visible act is review or a contribution-update report within this PR; it makes no higher-level institutional decision.',
       'complexity_flags':['none'],'alternative_interpretation':'','confidence':'plausible' if statement else 'clear','uncertainty_reason':'',
       'record_role':role,'parse_mode':parse,'deontic_force':'recommendation' if statement else 'nondeontic',
       'template_note':'No evidence that this occurrence is a reusable instruction template.',
       'presentation':{'quotation':quotation,'markup':markup,'rationale':'Supplied prose is preserved; inline backticks mark names or literal values, not external quotations.'},
       'disposition_events':[],
       'proposition':{'summary':'','decision_object_id':OBJ,'domain':'Review and editing of the wallet RPC backport in Bitcoin Core PR #14441, including its release notes.','time_scope':f"Retained review wording with recorded submission {E[a['source_id']].get('timestamp')}; complete edit history is unavailable. Later application is separately dated by the recorded revision and merge.",'identity_evidence':[IDENT,a],'qualifiers':[]} if statement else None,
       'target_level_alternatives':[],'observed_level_alternatives':[],
       'level_evidence':{'target_activity':'Editing the immediate proposed contribution.' if statement else 'Not applicable: context record.',
         'observed_activity':'A reviewer proposes a specific edit.' if statement else 'A participant records a review or reports an update.',
         'arrangement':'Ordinary contribution and review within PR #14441; the packet does not supply its governing authorization rules.',
         'evidence':[a,IDENT]}}
    units.append(u)
    return u

def comp(u,sym,text,evidence,basis='explicit',role='local',note='',gov=None):
    if gov is None: gov={'source_id':u['source_id'],'span':deepcopy(u['span'])}
    u['components'].append({'symbol':sym,'text':text,'basis':basis,'evidence':evidence,'inference_note':note,'occurrence_role':role,'governing_span':gov})

def qual(u,desc,evidence,attachment='scope_note',rationale=None,linked=None):
    u['proposition']['qualifiers'].append({'description':desc,'evidence':evidence,'attachment':attachment,'linked_unit_id':linked,'rationale':rationale or 'This qualification remains part of the focal proposition and limits its interpretation.'})

def rec(u,kind,target,evidence,why,basis='context_inferred',mode='ordinary_assent',speaker='different_actor'):
    u['institution']['recognition'].append({'kind':kind,'target':target,'evidence':evidence,'rationale':why,'basis':basis,'mode':mode,'speaker_relation':speaker,'independence_key':OBJ,'object_id':OBJ,'identity_evidence':[IDENT]+evidence[:1]})

def app(u,status,target,evidence,why):
    u['institution']['application_evidence'].append({'status':status,'target':target,'evidence':unique(evidence),'rationale':why})

def disp(u,kind,target,evidence,why,basis='context_inferred'):
    u['disposition_events'].append({'kind':kind,'target':target,'basis':basis,'evidence':unique(evidence),'rationale':why,'object_id':OBJ,'identity_evidence':[IDENT]+evidence[:1]})

# Four independently executable suggestions; technical replacement prose stays attached to the edit it specifies.
s1=base('F02-S01','review_comments:0',parse='pragmatic')
s1['proposition']['summary']='ryanofsky recommends correcting the release-note RPC spelling to `listtransactions`, including its final `s`; the expected editor is inferred as the contributor updating this PR, not an attributed authority.'
s1['alternative_interpretation']='Literally this is an evaluation of the correct technical name ("Should be"), rather than a named actor conducting a change. The preferred pragmatic parse reconstructs a correction request. It does not constitute an institutional definition of the RPC.'
s1['uncertainty_reason']='The source omits the editor and the erroneous occurrence. The path identifies release notes; the author later reports updating the PR, but the single-word "fixed" reply has no reliable supplied thread target.'
comp(s1,'A','the PR editor, contextually jnewbery',[ev('comments:0',"I've updated the PR with your changes.")],basis='context_inferred',role='context_reference',note='The imperative-like review suggestion omits an actor. The later update report by jnewbery supplies the contextual editor; this is not an explicit local A and does not establish any maintainer role.')
comp(s1,'D','Should',[ev('review_comments:0','Should')],note='The lexical modal is explicit; its advisory force is recommendation, not a demonstrated obligation.')
comp(s1,'I','correct',[ev('review_comments:0')],basis='context_inferred',role='semantic_inference',note='The source says "Should be", not "correct". Correction is the reconstructed action of this elliptical edit proposal.')
comp(s1,'Bdir','the RPC spelling in the release notes',[ev('review_comments:0','`listtransactions`')],basis='context_inferred',role='semantic_inference',note='The literal target string is a complement of "be"; its role as the target of a correction is inferred. The supplied path is doc/release-notes.md, and the erroneous spelling is not shown.')
comp(s1,'Cex','to `listtransactions` with `s`',[ev('review_comments:0','`listtransactions` with `s`')],basis='context_inferred',role='semantic_inference',note='Under the reconstructed correction predicate, this source complement supplies the required resulting spelling, including the explicit final s.')
qual(s1,'The requested spelling is the complete identifier `listtransactions`, including the terminal `s`.',[ev('review_comments:0','`listtransactions` with `s`')],attachment='component',rationale='Cex preserves the complete requested output rather than reducing the request to a generic typo fix.')

q2=E[sid('review_comments:1')]['text']
s2=base('F02-S02','review_comments:1',q2[q2.index("I'd maybe"):],quotation='proposed_wording',markup='mixed')
s2['proposition']['summary']='ryanofsky tentatively proposes changing the release-note paragraph to distinguish both outgoing and incoming transactions with `-deprecatedrpc=accounts` from only incoming transactions without that setting, retaining the explanation about spending from accounts versus labels.'
s2['presentation']['rationale']='The unit combines an introductory proposal with newly offered block-quoted replacement wording. The block is not an external or repeated quotation.'
s2['alternative_interpretation']='The literal first-person conditional offers how ryanofsky would edit the paragraph; pragmatically it invites the PR author to make the edit. The explicit actor in this parse is the hypothetical proposer, not a falsely explicit addressee. A tentative offer is not a committed personal plan. The replacement text describes software behavior and is not a separate institutional prescription.'
s2['uncertainty_reason']='The sentence directly supplies the change action, but "I\'d maybe" is a tentative suggestion, not evidence that ryanofsky undertook the edit. Earlier paragraph wording and full reply threads are unavailable.'
g2=ev('review_comments:1',q2[q2.index("I'd maybe"):])
comp(s2,'A','I (ryanofsky, in a hypothetical proposed edit)',[ev('review_comments:1','I',q2.index("I'd maybe"))],note='I is the subject of the explicit conditional change predicate. Author attribution identifies ryanofsky; this is not the actor of the later implementation report.',gov=g2)
comp(s2,'I','change',[ev('review_comments:1','change')],gov=g2)
comp(s2,'Bdir','it (the paragraph)',[ev('review_comments:1','it',q2.index('change it')+len('change '))],note='The pronoun it is the explicit direct object of change. Its antecedent, "This paragraph", is preserved in a scope note outside the focal span.',gov=g2)
replacement2=q2[q2.index('> When'):]
comp(s2,'Cex',replacement2,[ev('review_comments:1',replacement2)],note='The replacement block is explicitly introduced by "to:" as the content the change should produce.',gov=g2)
qual(s2,'Tentative first-person recommendation: "I\'d maybe" does not announce an actual undertaking or impose a duty.',[ev('review_comments:1',"I'd maybe")])
qual(s2,'The target is the preceding paragraph, criticized because both behaviors occur in the same release.',[ev('review_comments:1',q2[:q2.index(" I'd maybe")])],rationale='This antecedent and rationale are outside the smallest edit span but remain explicitly attached; the rationale is not a new activation condition.')
qual(s2,'With `-deprecatedrpc=accounts`, the proposed description returns both outgoing and incoming transactions for a label/account/dummy argument.',[ev('review_comments:1',replacement2[:replacement2.index(' Without')])],attachment='component',rationale='Cex retains the complete setting condition, all three argument names, and both transaction directions.')
qual(s2,'Without `-deprecatedrpc=accounts`, the proposed description returns only incoming transactions; accounts once permitted specific-account spending, whereas labels do not.',[ev('review_comments:1',replacement2[replacement2.index('Without'):])],attachment='component',rationale='Cex retains the negative setting condition and the technical explanation; no permission or institutional authority is inferred from technical possibility.')

q3=E[sid('review_comments:2')]['text']
s3=base('F02-S03','review_comments:2',q3[q3.index('Maybe'):])
s3['proposition']['summary']='ryanofsky tentatively recommends that the contributor drop the new check for "*" in this code for clarity, subject to the possibility that the reviewer is missing something; the preceding premise is that the check appears to change no behavior.'
s3['alternative_interpretation']='The local drop action is explicit, so the parse is literal despite inferred actor and object referent. "Unless I\'m missing something" can be read as an activation exception or as a defeasible epistemic hedge; the preferred representation preserves it as a scope qualification rather than inventing a technical trigger.'
s3['uncertainty_reason']='The target is resolved from the immediately preceding sentence and matching later response. The earlier review diff is absent, preventing independent identification of precisely which newly added star check was removed.'
comp(s3,'A','the PR editor, contextually jnewbery',[ev('review_comments:6',"I've removed it.")],basis='context_inferred',role='context_reference',note='The imperative drop has no expressed actor; the later matching report by jnewbery identifies the contextual actor who removed the check without implying institutional authority.')
comp(s3,'I','drop',[ev('review_comments:2','drop')])
comp(s3,'Bdir','the new check for "*" here',[ev('review_comments:2','the new check for "*" here')],basis='context_inferred',role='context_reference',note='Drop omits its object. The preceding sentence supplies the check as its contextual target, so the Bdir role is inferred rather than an explicit local argument.')
comp(s3,'Cex','for clarity',[ev('review_comments:2','for clarity')],note='This is the explicit purpose qualifying the proposed removal, not an activation condition.')
qual(s3,'The suggestion is tentative and defeasible: "Maybe" and "unless I\'m missing something".',[ev('review_comments:2','Maybe'),ev('review_comments:2',"unless I'm missing something")])
qual(s3,'The target is the new "*" check here, which the reviewer thinks may not change behavior.',[ev('review_comments:2',q3[:q3.index(' Maybe')])],rationale='The scope note retains the exact object antecedent and reviewer uncertainty about its technical effect, without asserting redundancy as independently verified fact.')
qual(s3,'The explicitly supplied purpose is clarity.',[ev('review_comments:2','for clarity')],attachment='component',rationale='Cex carries the purpose; this is not a generalized requirement for clear code.')

q4=E[sid('review_comments:3')]['text']
s4=base('F02-S04','review_comments:3',quotation='proposed_wording',markup='mixed')
s4['proposition']['summary']='ryanofsky recommends documenting the empty-string change in the release notes, tentatively offering wording that permits empty-string label queries for unlabeled transactions with `-deprecatedrpc=accounts` and describes an error without it, with backward compatibility and usefulness/confusion explanations.'
s4['presentation']['rationale']='The sentence proposing documentation and the block-quoted suggested wording are a single edit proposition. The replacement is newly offered wording, not a repeated or external quotation.'
s4['alternative_interpretation']='The prefatory "I think" reports ryanofsky\'s judgment; its I is not the grammatical actor of document. The explicit infinitive provides the edit action while the executor remains contextual. Technical can/possible and error statements inside the draft describe software behavior rather than institutional permission or sanction.'
s4['uncertainty_reason']='The editor is omitted from the documentation infinitive. The target of the nearby "Both are good changes" endorsement cannot be fixed without reliable threading. The substantive replacement, with small phrasing changes, is visible in the retained patch.'
g4=ev('review_comments:3',q4[:q4.index(' Maybe:')])
comp(s4,'A','the PR editor, contextually jnewbery',[ev('comments:0',"I've updated the PR with your changes.")],basis='context_inferred',role='context_reference',note='The source I belongs to think, not to document. The update report by the PR author supplies a contextual editor, without claiming an explicit local actor for the infinitive.',gov=g4)
comp(s4,'I','document',[ev('review_comments:3','document')],gov=g4)
comp(s4,'Bdir','the empty string change',[ev('review_comments:3','the empty string change')],note='This phrase is the explicit object of document in the embedded infinitive, not of think.',gov=g4)
replacement4=q4[q4.index('> Also'):]
comp(s4,'Cex',replacement4,[ev('review_comments:3',replacement4)],basis='context_inferred',role='semantic_inference',note='Maybe introduces concrete wording for the documentation action. Its function as output constraint is inferred from the adjacent proposal; the full block is retained, including all setting conditions and rationales.')
qual(s4,'The proposed wording is tentative ("I think it\'d be good" and "Maybe"), not a binding requirement.',[ev('review_comments:3',"I think it'd be good"),ev('review_comments:3','Maybe')])
qual(s4,'Backward compatibility qualifies empty-string label behavior when `-deprecatedrpc=accounts` is set; the label `""` lists unlabeled transactions.',[ev('review_comments:3',replacement4[:replacement4.index(' Without')])],attachment='component',rationale='The full Cex block retains the setting, empty-string value, backward-compatibility rationale, and unlabeled transaction target.')
qual(s4,'Without `-deprecatedrpc=accounts`, empty-string input is an error; the offered rationale is that unlabeled-only results are not very useful and can confuse.',[ev('review_comments:3',replacement4[replacement4.index('Without'):])],attachment='component',rationale='Cex preserves the negative setting condition, technical result, and offered rationale. The error is technical behavior, not an institutional sanction.')

# Context units preserve distinct observable communicative acts for relation and mechanism endpoints.
context_specs=[
 ('F02-C01','comments:0','reported_action','General author report that the PR was updated with the named reviewer\'s changes; the report does not individually enumerate the edits.'),
 ('F02-C02','comments:1','reported_action','Revision-specific utACK; it does not establish a general expectation, authority, or tested validation. The packet does not define the utACK abbreviation.'),
 ('F02-C03','comments:2','reported_action','Revision-specific utACK plus a technical qualification: the wallet implementation differs significantly from the original PR while tests are basically a clean backport.'),
 ('F02-C04','reviews:0','reported_action','Earlier revision-specific utACK. The supplied review state is APPROVED, without evidence of the reviewer\'s institutional authority.'),
 ('F02-C05','reviews:4','reported_action','Later revision-specific utACK explicitly identifies code simplification and release-note updates since the last review; this is not evidence of a mandated reapproval rule.'),
 ('F02-C06','review_comments:4','reported_action','Positive response to "Both" changes. The exact two antecedents are unresolved without reliable thread reconstruction.'),
 ('F02-C07','review_comments:5','reported_action','Single-word implementation report with an unresolved specific edit target.'),
 ('F02-C08','review_comments:6','reported_action','Author agrees the star check does not change behavior and reports removing it. This is assent and reported implementation, not a recognized institutional standard.')]
for uid,k,speech,why in context_specs:
    u=base(uid,k,role='context',speech=speech)
    u['alternative_interpretation']=why
    if uid in ['F02-C06','F02-C07']:
        u['confidence']='unresolved';u['uncertainty_reason']='Reliable reply threading is absent, so the exact antecedent is not uniquely established.'
    if uid=='F02-C03':
        u['complexity_flags']=['compound'];u['uncertainty_reason']='The technical comparison with the original PR is retained as the participant\'s report; the original PR patch is not supplied.'
    if uid=='F02-C08': u['complexity_flags']=['compound']
    u['level_evidence']['observed_activity']=why

# Evidence support is independent from the candidate type. No supplied guide authorizes these requests.
patch1=ev('patch:0','+`listtransactions` label support')
patch2text=E[sid('patch:0')]['text']
patch2=ev('patch:0',patch2text[patch2text.index('+When bitcoin'):patch2text.index('\n+\n+When `-deprecatedrpc')])
patch4=ev('patch:0',patch2text[patch2text.index('+When `-deprecatedrpc'):patch2text.index('\n \n Credits')])
general_report=ev('comments:0')
review_report=ev('reviews:4')
for u in [s1,s2,s3,s4]:
    rec(u,'reported_implementation','broader_proposal',[general_report],
        'jnewbery explicitly reports updating this PR with ryanofsky\'s changes, but does not enumerate each requested edit. The event is retained at the broader proposal scope and is not recognition of an institutional expectation.',mode='other')
    app(u,'reported','broader_proposal',[general_report,review_report],
        'The author reports incorporating the reviewer\'s changes; the reviewer describes code simplification and release-note updates. These general reports apply to the broader contribution without resolving every local reply antecedent.')
    disp(u,'reported_implemented','broader_proposal',[general_report],
        'The author reports updating PR #14441 with the reviewer\'s changes. This records a reported PR update, not verified implementation of every particular suggestion.',basis='explicit')

# Specific release-note outputs can be compared with the retained patch and its integrated head.
for u,patch,why in [
 (s1,patch1,'The retained added heading contains the complete requested RPC name with terminal s. The same head SHA is recorded as merged. This demonstrates the requested resulting spelling, not the missing intermediate typo or the cause of its correction.'),
 (s2,patch2,'The retained added paragraph distinguishes both transaction directions with the accounts setting from incoming-only results without it and retains the accounts-versus-labels explanation. Typography differs from the suggestion, but the substantive requested documentation is present at the recorded merged head.'),
 (s4,patch4,'The retained added paragraph describes empty-string behavior with and without the accounts setting and the usefulness/confusion rationale. It does not reproduce the explicit words "for backwards compatibility" from the offered wording. The observable application is partial with respect to that rationale; no exact verbatim implementation is claimed.')]:
    app(u,'observed','this_proposition',[{'source_id':u['source_id'],'span':u['span']},patch]+HEAD,why)
    disp(u,'recorded_merged','this_proposition',[patch]+HEAD,why+' The event concerns the particular documented content in PR #14441, not network adoption or adoption of a general rationale.')
    u['institution']['standing_profile']['application']='observed'

# The loose positive and fixed replies are not assigned uniquely on adjacency alone.
rec(s1,'reported_implementation','unresolved',[ev('review_comments:5')],
    '"fixed" is a report in release notes, but the absent reply thread prevents uniquely assigning it to this spelling correction. The PR identity is known; the specific proposition target is unresolved.',basis='unresolved',mode='other')
app(s1,'unresolved','unresolved',[ev('review_comments:5')],
    'A local edit is reported fixed without a uniquely recoverable target. This does not upgrade the focal application profile beyond the independently supported patch observation.')
for u in [s2,s4]:
    rec(u,'endorsement','unresolved',[ev('review_comments:4')],
        '"Both are good changes" provides ordinary assent in the release-note discussion; the likely pairing of wording suggestions cannot be verified without reliable threads. The PR identity is known but the exact targets remain unresolved.',basis='unresolved')

# The star-check response contains specific correspondence; exact intermediate diff remains missing.
rec(s3,'endorsement','this_proposition',[ev('review_comments:6',"No, you're right. It's better without."),ev('review_comments:6','The behaviour would be identical with or without the check for "*".')],
    'jnewbery agrees with dropping the check and the stated technical premise. Matching check-for-star wording supports this target, but the event is ordinary technical assent, not recognition of a governing expectation.')
rec(s3,'reported_implementation','this_proposition',[ev('review_comments:6')],
    'The author specifically reports removing the check after agreeing it would not alter behavior. The response matches the requested object despite unavailable formal threading.',mode='other')
app(s3,'reported','this_proposition',[ev('review_comments:2'),ev('review_comments:6')],
    'The request names the new star check and the response repeats that check, states identical behavior, and says it was removed. This is an attributable report of the requested action, not an independently observed intermediate diff.')
app(s3,'unresolved','this_proposition',[ev('patch:1','+        if (!IsDeprecatedRPCEnabled("accounts") && strAccount.empty()) {')]+HEAD,
    'The retained final patch contains this condition and is integrated, but the earlier proposed check is absent from the packet. The final condition cannot alone identify which newly introduced star check the reviewer meant or demonstrate the claimed removal sequence.')
disp(s3,'accepted','this_proposition',[ev('review_comments:6')],
    'The author agrees the check is unnecessary and reports its removal; matching technical language supports acceptance of this particular suggestion. This is not adoption of a general institutional rule.')
disp(s3,'reported_implemented','this_proposition',[ev('review_comments:6')],
    'The author reports removing the check at issue; the claim remains a participant report, with the earlier diff unavailable.')
disp(s3,'recorded_merged','broader_proposal',HEAD,
    'The containing PR and retained head are recorded merged. The prior version of the redundant check is absent, so this status is limited to the broader contribution.')
s3['institution']['standing_profile']['application']='reported'

# Relations retain limited textual correspondence; no causal or authority edge is inferred from sequence.
relations=[]
def relation(f,t,typ,basis,why,evidence):
    relations.append({'from_unit_id':f,'to_unit_id':t,'type':typ,'basis':basis,'rationale':why,'evidence':unique(evidence),'logic_scope':'not_applicable'})
for u in [s1,s2,s3,s4]:
    relation(u['unit_id'],'F02-C01','uptake','context_inferred',
      'The author names ryanofsky and reports updating the PR with the reviewer\'s changes. This is a grouped response to the set of suggestions, not a unique reply-thread link or proof that every literal clause was implemented.',
      [{'source_id':u['source_id'],'span':u['span']},general_report])
relation('F02-S03','F02-C08','uptake','context_inferred',
    'The response repeats the check-for-star object, agrees it does not alter behavior, and reports removal. This supports specific uptake despite missing formal threading; it does not establish the reviewer caused the edit.',[ev('review_comments:2'),ev('review_comments:6')])
relation('F02-C05','F02-C04','review_target_update','explicit',
    'The same reviewer gives a new revision-specific utACK and explicitly says "since last review", naming the intervening kinds of change. The earlier supplied review names the prior SHA. This records an updated target, not changed judgment or a mandatory reapproval procedure.',[ev('reviews:0'),ev('reviews:4')])

# Summary clauses use exact, inclusive evidence ledgers.
def item(claim,parts,**extra):
    cp=[{'text':t,'evidence':unique(es)} for t,es in parts]
    return {'claim':claim,'evidence':unique([e for part in cp for e in part['evidence']]),'claim_parts':cp,**extra}
outcomes=[
 item('jnewbery reports updating PR #14441 with ryanofsky\'s changes and specifically reports removing the star check after agreeing it would not change behavior.',[
   ('The author reports updating the PR with the named reviewer\'s changes.',[general_report]),
   ('The author agrees the check has identical behavior with or without it and reports removing it.',[ev('review_comments:6')])]),
 item('The retained release-note patch contains the requested complete RPC spelling and the two configuration-dependent behavior descriptions. The empty-string paragraph preserves the behavior and usefulness/confusion explanation, while omitting the suggested explicit backward-compatibility phrase.',[
   ('The requested complete RPC spelling appears in the retained added heading.',[ev('review_comments:0'),patch1]),
   ('The retained paragraph preserves the requested transaction-direction distinction and accounts-versus-labels explanation.',[ev('review_comments:1',replacement2),patch2]),
   ('The empty-string paragraph preserves both setting-dependent behaviors and the usefulness/confusion explanation, but omits the suggested explicit backward-compatibility phrase.',[ev('review_comments:3',replacement4),patch4])]),
 item('ryanofsky recorded a later utACK for 89306ab0df93bfdf5630910bc20b1eccb7379172 and identified code simplification and release-note updates since the earlier review. promag and meshcollider also recorded utACKs for that revision; meshcollider qualified the comparison with the original PR.',[
   ('ryanofsky moved from the earlier named review target to a later utACK and stated the intervening changes.',[ev('reviews:0'),ev('reviews:4')]),
   ('promag recorded utACK 89306ab.',[ev('comments:1')]),
   ('meshcollider recorded a full-revision utACK and described substantial implementation differences but basically cleanly backported tests.',[ev('comments:2')])]),
 item('PR #14441 is recorded merged on 2018-11-10, and its retained head matches the recorded merge commit.',[
   ('The identified PR is recorded merged at 2018-11-10T11:46:02Z.',[IDENT]+MERGED),
   ('The supplied head SHA equals the recorded merge-commit SHA.',REV)])]
mechanisms=[
 item('The star-check exchange supports a bounded reason-giving sequence: ryanofsky questions the check\'s effect and proposes dropping it for clarity, and jnewbery agrees that behavior is identical and reports removal.',[
   ('The reviewer supplies an uncertainty-qualified technical premise and a clarity-based removal proposal.',[ev('review_comments:2')]),
   ('The author agrees with the technical premise and reports removal of the same named check.',[ev('review_comments:6')])],
   category='reason_giving',unit_ids=['F02-S03','F02-C08'],status='supported_sequence',
   alternative_explanation='The author may have independently reached the same technical conclusion. Matching language supports correspondence and a reported sequence, not a causal effect. The intermediate diff needed to observe the precise removal is missing.'),
 item('The review exchange supports a bounded coordination sequence: a revision-specific utACK precedes an author report incorporating the reviewer\'s changes, followed by the same reviewer\'s utACK of a new revision and explicit description of code simplification and release-note updates.',[
   ('The earlier review is a utACK of c8d1f1513fb39d80cebbc32e1b5327209485e085.',[ev('reviews:0')]),
   ('The author reports updating the PR with ryanofsky\'s changes.',[general_report]),
   ('The later review is a utACK of 89306ab0df93bfdf5630910bc20b1eccb7379172 and explicitly names changes since the last review.',[ev('reviews:4')])],
   category='review_coordination',unit_ids=['F02-C04','F02-C01','F02-C05'],status='supported_sequence',
   alternative_explanation='The reviewer may simply be restating technical assent to a revised artifact. Recorded submission times and the explicit "since last review" language support ordering, but the packet does not establish a reapproval requirement or that this sequence caused integration.')]

screen_reasons={
 'body':'Exhaustively screened: describes the submitted backport, partial reverts, and claimed fix using referenced proposal IDs. It does not direct a separate navigation action or independently prescribe institutional conduct. The outcomes of the referenced PRs are not supplied.',
 'comments:0':'Exhaustively screened: author acknowledgment and implementation report, retained as context rather than a new prescription.',
 'comments:1':'Exhaustively screened: revision-specific utACK, retained as assent context rather than an independent norm or permission.',
 'comments:2':'Exhaustively screened: utACK plus material technical comparison with the original PR and tests. The descriptive qualification is retained in the context unit; no independently executable prescription is present.',
 'reviews:0':'Exhaustively screened: revision-specific utACK and supplied APPROVED review state record an act of review; no authority or general rule inferred.',
 'reviews:1':'The supplied review body is empty; the COMMENTED metadata does not supply proposition text.',
 'reviews:2':'The supplied review body is empty; the COMMENTED metadata does not supply proposition text.',
 'reviews:3':'The supplied review body is empty; the COMMENTED metadata does not supply proposition text.',
 'reviews:4':'Exhaustively screened: later utACK explicitly identifies code simplification and release-note updates since the last review. This is a reported review act and update description, not a general requirement to reapprove.',
 'review_comments:0':'Exhaustively screened: one elliptical correction suggestion. Its exact spelling qualifier remains attached; an institutional type is not established.',
 'review_comments:1':'Exhaustively screened: one paragraph-edit suggestion with technical replacement wording and an adjacent same-release rationale. The block describes software behavior and does not add an institutional definition or another independent edit.',
 'review_comments:2':'Exhaustively screened: one check-removal suggestion with a clarity purpose and defeasible missing-information qualification. The preceding sentence supplies the object and technical premise.',
 'review_comments:3':'Exhaustively screened: one request to document the empty-string behavior, with the proposed wording and all setting conditions attached. Software errors and capability language in the block are not institutional sanctions or permissions.',
 'review_comments:4':'Exhaustively screened: ordinary positive assent to two changes with unresolved antecedents, retained as context.',
 'review_comments:5':'Exhaustively screened: a one-word implementation report whose exact target is unresolved, retained as context.',
 'review_comments:6':'Exhaustively screened: technical agreement and a specific removal report. It supplies uptake/application evidence, not a separate prospective prescription.',
 'metadata':'Supplement screened as context under the packet selection design. Recorded status, identifiers, file summaries, and dates support bounded outcome claims; no exhaustive proposition extraction from this supplemental entry is claimed.',
 'supplement_metadata':'Supplement screened as context under the packet selection design. Canonical PR identity, retained head, merge SHA, and status provide object/integration evidence; this is not a claim that all supplemental institutional content has been extracted.',
 'patch:0':'Supplement screened as context under the packet selection design. The retained release-note additions supply direct comparisons for the requested edits. Their technical behavior descriptions are not new focal extraction targets; this does not claim the supplement lacks institutional relevance.',
 'patch:1':'Supplement screened as context under the packet selection design. Retained wallet-code and help-text changes supply limited artifact evidence. The earlier review diff is absent, so the particular redundant star-check removal is not independently verified. No exhaustive supplemental extraction is claimed.',
 'patch:2':'Supplement screened as context under the packet selection design. The patch modifies functional-test labels and assertions, consistent with the reported test backport; the source is not an exhaustive extraction target. No inference of institutional sanction or mandatory testing policy is made.',
 'patch:3':'Supplement screened as context under the packet selection design. The patch modifies watch-only label filtering tests and assertions; no exhaustive supplemental extraction or absence-of-institutions conclusion is claimed.'}
screening=[]
for e in p['entries']:
    ids=[u['unit_id'] for u in units if u['source_id']==e['source_id']]
    statement=any(u['record_role']=='statement' and u['source_id']==e['source_id'] for u in units)
    screening.append({'source_id':e['source_id'],'disposition':'candidate' if statement else ('empty' if not e['text'] else 'context_only'),'reason':screen_reasons[e['source_id'].removeprefix('pr14441:')],'unit_ids':ids})

annotation={'schema_version':'0.4','run_id':'F02_v04_r3','episode_id':'F02','packet_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),
 'entry_screening':screening,'units':units,'relations':relations,
 'episode_summary':{'observed_outcomes':outcomes,'mechanisms':mechanisms,
 'missing_evidence':[
  'No complete comment/edit history or reliable reply threading; fixed and Both lack uniquely established local targets.',
  'No earlier reviewed patch or full revision chronology showing the precise newly added star check before its reported removal.',
  'No attributed authorization, institutional enforcement provision, recurring contribution expectation, or evidence establishing a general rule behind these one-off suggestions.',
  'No evidence of network adoption, actual downstream RPC use, or the disposition of the separately referenced PRs #14411, #13075, #14023, and #14382.',
  'Retained head patches establish artifact content at that revision; they do not alone establish why a contributor accepted a suggestion or when each sentence first appeared.'
 ],
 'unresolved_questions':[
  'Which specific edits are the antecedents of Both are good changes and fixed?',
  'Which exact intermediate star-check expression was removed, and how did it differ from the base and retained head?',
  'Was the explicit backward-compatibility phrase intentionally omitted from the final empty-string paragraph, or was its purpose regarded as implicit?',
  'Are these locally accepted technical suggestions instances of an independently shared review expectation? The supplied evidence does not establish that institutional claim.'
 ]}}
Path('annotation.json').write_text(json.dumps(annotation,ensure_ascii=False,indent=2)+'\n')
# Required pre-check, pre-self-review freeze. Refuse to overwrite the historical first-complete output.
first=Path('annotation.first_complete.json')
if first.exists(): raise RuntimeError('First-complete freeze already exists; do not rerun generator.')
first.write_bytes(Path('annotation.json').read_bytes())
Path('first_complete_record.json').write_text(json.dumps({'run_id':'F02_v04_r3','stage':'first complete before checker or source self-review','packet_sha256':annotation['packet_sha256'],'annotation_sha256':hashlib.sha256(first.read_bytes()).hexdigest(),'entry_count':len(screening),'unit_count':len(units),'statement_count':4,'context_count':8,'source_inputs':['INSTRUCTIONS.txt','protocol/codebook.txt','protocol/annotation_schema.json','packet.json','tools/check_annotation.py'],'calibration_read':False},indent=2)+'\n')
print(json.dumps({'first_complete':str(first.resolve()),'entries':len(screening),'units':len(units),'statements':4,'contexts':8}))
