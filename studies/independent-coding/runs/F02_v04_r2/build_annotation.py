import json, hashlib, copy, sys, platform
from pathlib import Path
BASE = Path(__file__).resolve().parent
packet_path=BASE/'packet.json'
p=json.loads(packet_path.read_text())
entries={s['source_id']:s for s in p['entries']}
OBJ='https://github.com/bitcoin/bitcoin/pull/14441'
PREFIX='pr14441:'

def sid(s): return s if s.startswith(PREFIX) else PREFIX+s

def ev(s,q=None,start=None,end=None):
 s=sid(s); t=entries[s]['text']
 if q is None:
  if start is None:start=0
  if end is None:end=len(t)
  q=t[start:end]
 else:
  if start is None:start=t.index(q)
  assert t[start:start+len(q)]==q,(s,q)
  end=start+len(q)
 return {'source_id':s,'span':{'start':start,'end':end,'quote':q}}

def unique(es):
 out=[]
 for e in es:
  if e not in out:out.append(e)
 return out

identity=[ev('supplement_metadata','"url": "https://github.com/bitcoin/bitcoin/pull/14441"')]
merge_ev=[ev('supplement_metadata','"merged": true'),ev('supplement_metadata','"merged_at": "2018-11-10T11:46:02Z"'),ev('supplement_metadata','"head_sha": "89306ab0df93bfdf5630910bc20b1eccb7379172"'),ev('supplement_metadata','"merge_commit_sha": "89306ab0df93bfdf5630910bc20b1eccb7379172"')]
units=[]

def make(uid,s,q=None,role='statement',parse='literal',speech='proposed',summary='',alternative='',rationale='',scope='case_specific'):
 e=ev(s,q)
 statement=role=='statement'
 u={'unit_id':uid,'source_id':e['source_id'],'span':e['span'],'parent_unit_id':None,
    'grammar':'regulative' if statement else 'not_institutional','speech_act':speech,'scope':scope,'components':[],
    'institution':{'type':'undetermined' if statement else 'not_applicable','dispute_present':False,
      'rationale':rationale if rationale else ('A case-specific technical contribution suggestion; the supplied record does not select a rule, socially expected norm, explicit personal strategy, or constituted institutional status.' if statement else 'This record preserves a communicative act or rationale, not a separate institutional prescription.'),
      'evidence':[e] if statement else [],'recognition':[],'authority_evidence':[],
      'standing_profile':{k:'none' if statement else 'not_applicable' for k in ['documentary','recognition','application']},
      'documentary_support':[],'application_evidence':[],'challenges':[],'type_alternatives':[]},
    'statement_target_level':'operational' if statement else 'not_applicable','observed_action_level':'operational',
    'level_rationale':'The focal action concerns the present contribution or its technical documentation within ordinary PR review; no recurring review arrangement or allocation of decision authority is proposed.' if statement else 'This is an ordinary contribution/review act; it is not itself a statement governing a separate activity.',
    'complexity_flags':['none'],'alternative_interpretation':alternative,'confidence':'plausible' if statement else 'clear',
    'uncertainty_reason':'Institutional type is unestablished; source history and reply threading are incomplete.' if statement else '',
    'record_role':role,'parse_mode':parse,'deontic_force':'recommendation' if statement else 'nondeontic',
    'presentation':{'quotation':'none','markup':'plain','rationale':'The retained occurrence is plain prose, with inline code where supplied; no deletion markup or prior quotation is evidenced.'},
    'disposition_events':[],
    'proposition':{'summary':summary,'decision_object_id':OBJ,'domain':'Bitcoin Core PR #14441: 0.17 wallet RPC backport contribution and review','time_scope':('Retained PR body; creation is recorded as 2018-10-09 but sentence-level history is unavailable.' if s=='body' else 'Retained comment associated with '+str(entries[sid(s)]['timestamp'])+'; full edit history unavailable.'),'identity_evidence':identity,'qualifiers':[]} if statement else None,
    'target_level_alternatives':[],'observed_level_alternatives':[],
    'level_evidence':{'target_activity':summary if statement else 'Not applicable: no separate target prescription.','observed_activity':('Proposal or request in the current contribution review.' if statement else summary or 'Reported contribution/review act.'),'arrangement':'Operational contribution, review, revision, and repository integration for PR #14441.','evidence':[e]}}
 units.append(u);return u

def comp(u,symbol,text,q=None,basis='explicit',role='local',note='',source=None,governing=None):
 evidence=ev(source or u['source_id'],q) if q is not None else {'source_id':u['source_id'],'span':u['span']}
 g=governing or {'source_id':u['source_id'],'span':u['span']}
 c={'symbol':symbol,'text':text,'basis':basis,'evidence':[evidence],'inference_note':note,'occurrence_role':role,'governing_span':g}
 u['components'].append(c);return c

def qual(u,description,evidence,attachment='scope_note',rationale='',linked=None):
 u['proposition']['qualifiers'].append({'description':description,'evidence':evidence,'attachment':attachment,'linked_unit_id':linked,'rationale':rationale or 'This qualification limits the focal proposition and is retained explicitly in this scope note.'})

def disposition(u,kind,target,evidence,rationale,basis='context_inferred'):
 u['disposition_events'].append({'kind':kind,'target':target,'basis':basis,'evidence':evidence,'rationale':rationale,'object_id':OBJ,'identity_evidence':identity})

def recognition(u,kind,target,evidence,rationale,mode='ordinary_assent',speaker='different_actor',basis='context_inferred'):
 u['institution']['recognition'].append({'kind':kind,'target':target,'evidence':evidence,'rationale':rationale,'basis':basis,'mode':mode,'speaker_relation':speaker,'independence_key':OBJ,'object_id':OBJ,'identity_evidence':identity})

def app(u,status,target,evidence,rationale):
 u['institution']['application_evidence'].append({'status':status,'target':target,'evidence':evidence,'rationale':rationale})

# The body is retained as a plausible contribution proposal, with its literal description preserved as an alternative.
s1=make('S01','body',parse='pragmatic',summary='The submitted contribution proposes a backport of PR #14411 to v0.17; its retained description says it partially reverts #13075 and #14023 and fixes #14382.',alternative='The body can be read solely as a technical description of the submitted change, with no separate request to act. The preferred candidate parse treats the offered backport as a proposal, not an instruction to merge or a rule governing future backports.',rationale='The offered backport is a plausible case-specific action proposal in a contribution record. Its technical method alone does not establish a committed personal plan, a social expectation, authority, or a recurring institutional procedure.')
comp(s1,'I','backport','Backport',basis='context_inferred',role='semantic_inference',note='The nominal description of the offered contribution is reconstructed as a proposed action; the source does not explicitly instruct integration.')
comp(s1,'Bdir','PR #14411','PR #14411',basis='context_inferred',role='semantic_inference',note='The object of the nominal backport becomes the direct object in the proposed-action parse. This referenced source PR is distinct from the current decision object #14441.')
comp(s1,'Bind','v0.17','v0.17',basis='context_inferred',role='semantic_inference',note='The version following to is interpreted as the destination of the backport; Cex destination is a defensible alternative.')
qual(s1,'The proposal is a backport to v0.17, not an outcome claim about original PR #14411.',[ev('body','Backport of PR #14411 to v0.17.')],attachment='component')
qual(s1,'Only partial reversion of #13075 and #14023 is claimed.',[ev('body','This change partially reverts #13075 and #14023.')])
qual(s1,'The body claims to fix #14382; the packet does not independently verify that referenced object\'s resolution.',[ev('body','Fixes #14382')])
s1['uncertainty_reason']='The body is a nominal change description; reading it as a proposal is pragmatic. Exact equivalence to PR #14411, the scope of partial reversions, and resolution of #14382 are not independently verifiable in the packet.'
s1['complexity_flags']=['hybrid_candidate']
disposition(s1,'recorded_merged','broader_proposal',merge_ev,'The current PR #14441 is recorded as merged. This does not verify every technical claim in its body, or establish outcomes for referenced PRs.',basis='explicit')
for src in ['reviews:0','reviews:4','comments:1','comments:2']:
 recognition(s1,'endorsement','broader_proposal',[ev(src)],'The ACK endorses the indicated revision of PR #14441. It is ordinary technical assent, not recognition of a backport expectation or proof of every body claim.',speaker='different_actor')

# Distinct communicative acts retained for relation endpoints and mechanism evidence.
c1=make('C01','comments:0',role='context',speech='reported_action',summary='jnewbery thanks ryanofsky and reports updating the PR with the reviewer\'s changes.')
c2=make('C02','comments:1',role='context',speech='reported_action',summary='promag provides utACK for abbreviated revision 89306ab.')
c3=make('C03','comments:2',role='context',speech='reported_action',summary='meshcollider gives utACK for the full revision and qualifies that the wallet implementation differs significantly from the original PR while the tests are basically a clean backport.')
c3['alternative_interpretation']='The comparison explains review scope; it does not propose a general backport standard or reject the contribution.'
c4=make('C04','reviews:0',role='context',speech='reported_action',summary='ryanofsky records utACK for c8d1f1513fb39d80cebbc32e1b5327209485e085.')
c5=make('C05','reviews:4',role='context',speech='reported_action',summary='ryanofsky records utACK for 89306ab0df93bfdf5630910bc20b1eccb7379172 and reports that only code simplification and suggested release-notes updates changed since the prior review.')

s2=make('S02','review_comments:0',parse='pragmatic',summary='ryanofsky recommends using the RPC spelling listtransactions, including the final s, in the release notes.',alternative='Literally this is a predicate about the correct RPC spelling. The preferred editorial-request parse reconstructs use; no general naming rule or institutional definition is asserted.')
comp(s2,'D','Should','Should',note='Should governs the recommended spelling; it is advisory force, not evidence of institutional authority.')
comp(s2,'I','use',basis='context_inferred',role='semantic_inference',note='Use is the reconstructed editing action underlying the elliptical Should be wording.')
comp(s2,'Bdir','the spelling `listtransactions` with `s`','`listtransactions` with `s`',basis='context_inferred',role='semantic_inference',note='The literal predicate complement supplies the proposed spelling; it becomes the object of inferred use. The final s is retained.')
qual(s2,'The requested spelling includes the final s.',[ev('review_comments:0','`listtransactions` with `s`')],attachment='component')
s2['uncertainty_reason']='The editor is implicit. The source file context is doc/release-notes.md; the precise prior misspelled text and reply thread are not supplied.'

rc1=entries[sid('review_comments:1')]['text']
edit_text=rc1[rc1.index("I'd maybe change it to:"):]
s3=make('S03','review_comments:1',edit_text,summary='ryanofsky hypothetically proposes changing the release-notes paragraph to distinguish listtransactions behavior with and without -deprecatedrpc=accounts: both outgoing and incoming transactions with the setting, only incoming transactions without it, with the account-versus-label explanation.',alternative='The conditional I\'d construction is a suggestion to the contribution author, not necessarily a promise by ryanofsky to edit. The explicit hypothetical speaker is retained in A; a pragmatic addressee-as-editor representation is possible. The replacement prose describes software behavior rather than constituting an institutional permission.')
s3['presentation']={'quotation':'proposed_wording','markup':'mixed','rationale':'A plain proposal introduces a blockquoted replacement paragraph. The blockquote is newly proposed wording, not a repeated occurrence or external quotation.'}
proposal_clause=ev('review_comments:1',"I'd maybe change it to:")
comp(s3,'A',"I (ryanofsky, hypothetical editor)","I'd",governing=proposal_clause,note='The I in I\'d is the literal subject of change in a hypothetical recommendation, not an inferred actual editor or a commitment.')
comp(s3,'I','change','change',governing=proposal_clause)
comp(s3,'Bdir','it (the release-notes paragraph)','it',governing=proposal_clause,note='It is explicitly the object of change; the prior sentence supplies paragraph as the antecedent. The unit begins with the action proposal rather than expanding to include that antecedent.')
replacement=rc1[rc1.index('> When'):]
comp(s3,'Cex','Use the proposed replacement paragraph distinguishing the two flag settings and explaining the account/label difference.',replacement,note='The proposed text after to specifies the requested resulting wording. This is an execution constraint on editing, not a condition activating the edit.')
qual(s3,'Both behaviors coexist in the same release, motivating the clarification.',[ev('review_comments:1',"This paragraph doesn't really make sense when both behaviors are present in the same release.")])
qual(s3,'With -deprecatedrpc=accounts, the label/account/dummy argument returns outgoing and incoming transactions; without it, only incoming transactions.',[ev('review_comments:1',replacement)],attachment='component')
qual(s3,'The proposed explanation contrasts past spending from specific accounts with the absence of this feature for labels.',[ev('review_comments:1',replacement)],attachment='component')
s3['complexity_flags']=['nested_component']
s3['uncertainty_reason']='This is a one-off documentation suggestion; the hypothetical speaker is explicit but the actual editor is not prescribed by name. The retained final text is materially similar, not verbatim.'

c10=make('C10','review_comments:1',"This paragraph doesn't really make sense when both behaviors are present in the same release.",role='context',speech='asserted',summary='ryanofsky criticizes the clarity of a paragraph because both behaviors coexist in the same release.')

rc2=entries[sid('review_comments:2')]['text']
request=rc2[rc2.index('Maybe drop'):]
s4=make('S04','review_comments:2',request,summary='ryanofsky tentatively recommends dropping the new check for "*" for clarity, unless the reviewer is missing something.',alternative='The recommendation remains conditional on the reviewer\'s understanding. The preceding claim about unchanged behavior is a technical rationale, not an institutional sanction or proof of redundancy.')
comp(s4,'I','drop','drop')
comp(s4,'Bdir','the new check for "*"','the new check for "*"',source='review_comments:2',basis='context_inferred',role='context_reference',note='The omitted object of drop is recovered from the preceding sentence. That antecedent lies outside the focal action span; no local explicit object is claimed.')
comp(s4,'Cex','for clarity','for clarity')
comp(s4,'Cac',"unless I'm missing something","unless I'm missing something",note='The reviewer explicitly conditions the recommendation on not having overlooked relevant behavior; this is a retained epistemic qualification, not an authority claim.')
qual(s4,'The recommendation is tentative (Maybe) and conditional on the reviewer not missing something.',[ev('review_comments:2',request)],attachment='component')
qual(s4,'The cited rationale is that the reviewer cannot see how the new check for "*" changes anything.',[ev('review_comments:2',rc2[:rc2.index(' Maybe')])])
s4['uncertainty_reason']='The preceding sentence identifies the check at a general level, but no exact earlier revision diff or reliable inline line location identifies its complete implementation. Reported removal can be established; direct observation of that precise removal cannot.'
c9=make('C09','review_comments:2',rc2[:rc2.index(' Maybe')],role='context',speech='asserted',summary='ryanofsky questions whether the new check for "*" changes behavior.')

rc3=entries[sid('review_comments:3')]['text']
s5=make('S05','review_comments:3',summary='ryanofsky recommends documenting the empty-string change: when -deprecatedrpc=accounts is set, an empty string selects unlabeled transactions for backward compatibility; without it, empty string is an error, with the stated usefulness and confusion rationale.',alternative='This is a documentation request rather than a new permission or prohibition imposed on contributors. The embedded possible/error statements describe software capability and behavior. The suggested wording is tentative and need not be reproduced verbatim.')
s5['presentation']={'quotation':'proposed_wording','markup':'mixed','rationale':'A plain request introduces blockquoted replacement/additional wording with Maybe; it is newly drafted text, not a quotation of an already coded institutional proposition.'}
request_clause=ev('review_comments:3',"I think it'd be good to document the empty string change.")
comp(s5,'I','document','document',governing=request_clause)
comp(s5,'Bdir','the empty string change','the empty string change',governing=request_clause)
rep3=rc3[rc3.index('> Also'):]
comp(s5,'Cex','Describe the flag-dependent empty-string behavior and the stated rationale in the proposed wording.',rep3,note='The blockquote specifies the content of the requested documentation, not a permission to execute RPC operations.')
qual(s5,'Backward compatibility when -deprecatedrpc=accounts is set: empty string selects unlabeled transactions.',[ev('review_comments:3',rep3)],attachment='component')
qual(s5,'Without -deprecatedrpc=accounts, empty string is an error; the offered rationale is low usefulness and potential confusion.',[ev('review_comments:3',rep3)],attachment='component')
qual(s5,'Maybe marks the offered wording as tentative.',[ev('review_comments:3','Maybe:')])
s5['complexity_flags']=['nested_component']
s5['uncertainty_reason']='The requested documentation action and its object are explicit; its editor is implicit. The final wording differs slightly while retaining the flag-dependent distinction and rationale.'

c6=make('C06','review_comments:4',role='context',speech='reported_action',summary='jnewbery endorses two unspecified changes with Both are good changes.')
c6['confidence']='unresolved';c6['uncertainty_reason']='The packet lacks reliable reply threading. Both does not uniquely identify which two of the documentation comments it refers to.'
c6['alternative_interpretation']='The two substantive paragraph edits are a plausible referent; a precise pairing is not established by the retained text.'
c7=make('C07','review_comments:5',role='context',speech='reported_action',summary='jnewbery reports fixed without naming the repaired item.')
c7['confidence']='unresolved';c7['uncertainty_reason']='The single word fixed has no reliable reply target in the packet; it cannot alone prove a particular edit.'
c8=make('C08','review_comments:6',role='context',speech='reported_action',summary='jnewbery agrees that behavior is identical with or without the check for "*" and reports removing it.')

patch0=entries[sid('patch:0')]['text']
spell=ev('patch:0','+`listtransactions` label support')
para1=ev('patch:0',patch0[patch0.index('+When bitcoin'):patch0.index('+\n+When `-deprecatedrpc')])
para2=ev('patch:0',patch0[patch0.index('+When `-deprecatedrpc'):patch0.index('\n \n Credits')])
for u,pe,detail in [(s2,spell,'The integrated release-notes artifact uses listtransactions, including the final s. This establishes the resulting spelling, not the exact earlier typo or a particular reply pairing.'),(s3,para1,'The integrated release-notes paragraph makes the requested two-setting distinction and preserves the account/label explanation. It is not a verbatim reproduction of the suggested Markdown.'),(s5,para2,'The integrated release notes document the requested empty-string distinction and the usefulness/confusion rationale, with modest wording changes.')]:
 app(u,'observed','this_proposition',[pe]+merge_ev,detail+' The patch is retained at the head revision that matches the recorded merged commit.')
 app(u,'reported','broader_proposal',[ev('comments:0'),ev('reviews:4')],'The author reports a PR update and the reviewer identifies release-notes updates since the previous review. These reports do not individually itemize this edit.')
 u['institution']['standing_profile']['application']='observed'
 disposition(u,'recorded_merged','this_proposition',[pe]+merge_ev,detail+' The patch and integration record verify this limited resulting edit.',basis='context_inferred')
 disposition(u,'reported_implemented','broader_proposal',[ev('comments:0')],'The report explicitly attributes PR changes to the reviewer, but does not individually enumerate the focal edit.',basis='explicit')
 recognition(u,'response','broader_proposal',[ev('comments:0')],'The author reports taking up reviewer changes at the PR level; this is response to technical review, not interpersonal recognition of an institutional expectation.',mode='other')
 recognition(u,'endorsement','broader_proposal',[ev('reviews:4')],'The reviewer ACKs the updated contribution. The same reviewer proposed this edit; an ACK does not prove institutional expectation recognition.',speaker='same_actor')

# Ambiguous local assent remains visible without being promoted to expectation recognition.
for u in [s3,s5]:
 recognition(u,'endorsement','unresolved',[ev('review_comments:4')],'Both endorses two changes, but absent reliable threading the pair cannot be assigned conclusively. PR identity is known; the exact proposition target remains unresolved.',basis='unresolved')
recognition(s2,'reported_implementation','unresolved',[ev('review_comments:5')],'Fixed could respond to the spelling request, but the packet does not establish that reply target.',mode='other',basis='unresolved')
app(s2,'unresolved','unresolved',[ev('review_comments:5')],'A repair is reported, but the precise repaired item is not recoverable from fixed alone.')

recognition(s4,'endorsement','this_proposition',[ev('review_comments:6',"No, you're right. It's better without.")],'The author agrees with dropping the check. The explicit reference to the check later in the same response identifies the technical proposal; ordinary agreement is not expectation recognition.')
recognition(s4,'reported_implementation','this_proposition',[ev('review_comments:6')],'The author names the same check and reports removal; this is uptake of a technical suggestion, not evidence of a shared conduct norm.',mode='other',basis='explicit')
app(s4,'reported','this_proposition',[ev('review_comments:6')],'The author explicitly reports removing the check after stating identical behavior with or without it. The final head patch is not a before/after diff of that particular review edit.')
s4['institution']['standing_profile']['application']='reported'
disposition(s4,'accepted','this_proposition',[ev('review_comments:6')],'Agreement and removal concern the named check for "*".',basis='explicit')
disposition(s4,'reported_implemented','this_proposition',[ev('review_comments:6')],'The author explicitly reports I\'ve removed it, with the preceding check reference supplying the object.',basis='explicit')
disposition(s4,'recorded_merged','broader_proposal',merge_ev,'PR #14441 is recorded as merged; its retained final patch does not by itself show the precise intermediate check removal.',basis='explicit')

relations=[]
def rel(a,b,kind,evidence,rationale,basis='context_inferred',logic='not_applicable'):
 relations.append({'from_unit_id':a,'to_unit_id':b,'type':kind,'basis':basis,'rationale':rationale,'evidence':evidence,'logic_scope':logic})
rel('S01','C01','uptake',[ev('body'),ev('comments:0')],'The contribution author reports revising the current proposed contribution after review, not completing each referenced technical outcome.')
for u in [s2,s3,s5]:
 rel(u['unit_id'],'C01','uptake',[{'source_id':u['source_id'],'span':u['span']},ev('comments:0'),ev('reviews:4')],'The author attributes the updated PR to ryanofsky\'s changes. Corresponding final release-notes edits support a contextual link, without reliable per-comment threading.')
rel('S04','C08','uptake',[ev('review_comments:2'),ev('review_comments:6')],'The response explicitly identifies the same check for "*", agrees it is behaviorally redundant, and reports removing it.',basis='explicit')
rel('C08','C09','clarifies',[ev('review_comments:2',rc2[:rc2.index(' Maybe')]),ev('review_comments:6')],'The author confirms the technical assessment raised by the reviewer. This is explanatory correspondence, not a new institutional requirement.')
rel('C05','C04','review_target_update',[ev('reviews:0'),ev('reviews:4')],'The same reviewer gives an ACK of a new hash and explicitly describes changes since last review. This records the revision target update without implying a mandatory reapproval process.',basis='explicit')
rel('C01','C05','temporal',[ev('comments:0'),ev('reviews:4')],'The supplied source timestamps place the author\'s update report before the reviewer\'s updated ACK; timing is contextual and is not causal evidence.')

# Exhaustive focal screening. Supplemental disposition means assigned context scope, not absence of institutional content.
screen_reasons={
 'body':'Candidate retained for the offered backport, with literal technical-description alternative and partial-reversion/fix qualifications. References to other PRs are not separate navigation instructions or verified outcomes.',
 'comments:0':'Report of PR revision in response to review; no new independent prescription.',
 'comments:1':'ACK of a revision is ordinary technical assent; no governing expectation is stated.',
 'comments:2':'ACK plus a qualified comparison with the original backport. The comparison supplies technical review context, not a prescription governing future backports.',
 'reviews:0':'ACK of a specific revision; review metadata does not create a separate institutional prescription.',
 'reviews:1':'Empty review body; COMMENTED metadata does not supply a textual proposition.',
 'reviews:2':'Empty review body; COMMENTED metadata does not supply a textual proposition.',
 'reviews:3':'Empty review body; COMMENTED metadata does not supply a textual proposition.',
 'reviews:4':'ACK and account of changes since the last review; no general requirement to repeat approval is expressed.',
 'review_comments:0':'Elliptical spelling recommendation retained as a pragmatic edit candidate, with literal technical alternative.',
 'review_comments:1':'One paragraph-replacement proposal, with its full offered wording and coexisting-behaviors qualification. Introductory criticism supplies rationale, not an additional independently executable request.',
 'review_comments:2':'One conditional drop recommendation, with object resolved from the preceding technical rationale; clarity purpose and uncertainty hedge retained.',
 'review_comments:3':'One request to document empty-string behavior with proposed wording. Embedded capability/error claims are technical documentation content, not contributor permissions or sanctions.',
 'review_comments:4':'Ordinary assent to two changes, with unresolved precise reply targets; no independent prescription.',
 'review_comments:5':'Single-word repair report with unresolved target; no independent prescription.',
 'review_comments:6':'Agreement, technical explanation, and reported removal; no additional independent prescription or rule.',
 'metadata':'Supplement screened for identity and recorded repository outcome, not an exhaustive extraction target; context-only does not imply absence of institutional significance.',
 'supplement_metadata':'Supplement screened for PR identity, recorded merge, and matching head/merge revision; context-only is assignment scope rather than a negative institutional-content finding.',
 'patch:0':'Supplement screened as retained release-notes artifact for resulting spelling and behavioral documentation. Context-only follows assignment scope; it does not claim the artifact lacks all possible institutional content.',
 'patch:1':'Supplement screened as a retained implementation patch; it supports final technical configuration but not complete review-edit chronology. Technical help imperatives/modal terms were not exhaustively extracted under supplemental scope.',
 'patch:2':'Supplement screened as test changes. It supplies technical context, not proof tests were executed or passed; supplemental extraction is not exhaustive.',
 'patch:3':'Supplement screened as test changes. It supplies technical context, not test execution evidence; context-only is not a claim of no institutional content.'
}
screen=[]
for s in p['entries']:
 us=[u for u in units if u['source_id']==s['source_id']]
 disp='candidate' if any(u['record_role']=='statement' for u in us) else 'empty' if s['text']=='' else 'context_only'
 screen.append({'source_id':s['source_id'],'disposition':disp,'reason':screen_reasons[s['source_id'][len(PREFIX):]],'unit_ids':[u['unit_id'] for u in us]})

outcomes=[]
def outcome(parts):
 outcomes.append({'claim':' '.join(t for t,e in parts),'evidence':unique([e for t,es in parts for e in es]),'claim_parts':[{'text':t,'evidence':es} for t,es in parts]})
outcome([
 ('PR #14441 is recorded as merged on 2018-11-10 at 11:46:02Z.',identity+merge_ev[:2]),
 ('Its archived metadata gives base 0.17 and the same 89306ab0df93bfdf5630910bc20b1eccb7379172 value for head and merge commit.',[ev('supplement_metadata','"base": "0.17"')]+merge_ev[2:])])
outcome([
 ('The retained release-notes patch uses listtransactions with the final s.',[spell]),
 ('It distinguishes outgoing-and-incoming results with -deprecatedrpc=accounts from incoming-only results without it, including the account/label explanation.',[para1]),
 ('It also documents unlabeled-transaction selection by empty string with that setting and an error without it, retaining the usefulness/confusion rationale.',[para2]),
 ('The patch revision matches the head and merge commit of the recorded merged contribution.',merge_ev)])
outcome([
 ('jnewbery reports removing the check for "*" and states that behavior is identical with or without it.',[ev('review_comments:6')])])
outcome([
 ('ryanofsky updates the ACK target from c8d1f1513fb39d80cebbc32e1b5327209485e085 to 89306ab0df93bfdf5630910bc20b1eccb7379172.',[ev('reviews:0'),ev('reviews:4')]),
 ('The updated review states that only code simplification and suggested release-notes updates changed since the last review.',[ev('reviews:4')])])

mechanisms=[]
def mechanism(category,parts,ids,alternative,status):
 mechanisms.append({'category':category,'claim':' '.join(t for t,e in parts),'evidence':unique([e for t,es in parts for e in es]),'unit_ids':ids,'alternative_explanation':alternative,'status':status,'claim_parts':[{'text':t,'evidence':es} for t,es in parts]})
mechanism('reason_giving',[
 ('ryanofsky questions the behavioral effect of a new check for "*" and tentatively recommends dropping it for clarity unless something has been missed.',[ev('review_comments:2')]),
 ('jnewbery explicitly agrees that behavior is unchanged and reports removing the check.',[ev('review_comments:6')]),
 ('ryanofsky subsequently ACKs a new revision and describes code simplification among the changes since the last review.',[ev('reviews:0'),ev('reviews:4')])],['C09','S04','C08','C04','C05'],
 'The textual response supports a review-to-removal report, but it does not isolate a causal effect. The author could independently have favored the same simplification; the final patch is not a history of the particular intermediate check.', 'supported_sequence')
mechanism('reason_giving',[
 ('ryanofsky identifies ambiguity from both behaviors appearing in the same release and proposes a paragraph distinguishing the flag settings.',[ev('review_comments:1')]),
 ('The reviewer separately recommends documenting the flag-dependent empty-string behavior with proposed wording.',[ev('review_comments:3')]),
 ('jnewbery reports updating the PR with the reviewer\'s changes; the later reviewer report identifies release-notes updates since the prior review.',[ev('comments:0'),ev('reviews:4')]),
 ('The retained release-notes patch contains both distinctions and their stated explanations, with wording changes.',[para1,para2]),
 ('That retained revision is identified as the head and merge commit of recorded merged PR #14441.',identity+merge_ev)],['C10','S03','S05','C01','C05'],
 'Author attribution and matching final text support a limited sequence of review and revision. Incomplete threading and revision history prevent proving that each exact sentence or acceptance rationale was caused by a particular comment; equivalent edits could also have arisen during ordinary author revision.', 'supported_sequence')

annotation={'schema_version':'0.4','run_id':'F02_v04_r2','episode_id':'F02','packet_sha256':hashlib.sha256(packet_path.read_bytes()).hexdigest(),'entry_screening':screen,'units':units,'relations':relations,'episode_summary':{'observed_outcomes':outcomes,'mechanisms':mechanisms,'missing_evidence':[
 'Complete comment and PR-body edit histories are unavailable; creation/submission timestamps do not date every retained sentence.',
 'Reliable reply threading and exact inline line locations are absent, leaving Both are good changes and fixed without unique proposition targets.',
 'The complete earlier revision and intermediate review diffs are absent; the precise check removed after review cannot be verified from a before/after patch.',
 'Only current PR #14441 has supplied disposition evidence; outcomes for #14411, #13075, #14023, and #14382 cannot be established from the containing PR merge.',
 'No project authorization, enforcement provision, recurring backport procedure, expectation recognition, repository-permission history, or network-adoption evidence is supplied.',
 'Retained code and test patches do not establish executed tests, performance, complete runtime correctness, or downstream network uptake.'
 ],'unresolved_questions':[
 'Should the nominal backport body be treated as a pragmatic contribution proposal or exclusively as technical context? Both readings are retained; it supports no rule or authority claim.',
 'Which exact documentation edits are the two changes endorsed by Both, and which edit is the target of fixed?',
 'Which complete earlier expression is the new check for "*", and how precisely did the final review update alter it?',
 'How far do the supplied one-off edit suggestions bear any broader institutional significance beyond ordinary contribution review? The packet does not select a stronger institutional type.'
 ]}}
(BASE/'annotation.json').write_text(json.dumps(annotation,ensure_ascii=False,indent=2)+'\n')
# Required first-complete freeze precedes any checker call or source self-review.
(BASE/'annotation.first_complete.json').write_bytes((BASE/'annotation.json').read_bytes())
print(json.dumps({'entries':len(screen),'units':len(units),'statements':sum(u['record_role']=='statement' for u in units),'contexts':sum(u['record_role']=='context' for u in units),'relations':len(relations),'packet_sha256':annotation['packet_sha256']}))
