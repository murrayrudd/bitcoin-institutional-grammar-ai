from pathlib import Path
import json, hashlib

ROOT=Path(__file__).resolve().parent
p=ROOT/'packet.json'
pkt=json.loads(p.read_bytes())
entries={e['source_id']:e for e in pkt['entries']}
T={k:e['text'] for k,e in entries.items()}
def sid(short): return 'pr14441:'+short

def span(source, quote=None, start=None, end=None):
    text=T[source]
    if quote is not None:
        start=text.index(quote,0 if start is None else start)
        end=start+len(quote)
    else:
        start=0 if start is None else start
        end=len(text) if end is None else end
        quote=text[start:end]
    return {'start':start,'end':end,'quote':quote}

def ev(short, quote=None, start=None, end=None):
    source=sid(short)
    return {'source_id':source,'span':span(source,quote,start,end)}

def component(symbol,text,basis,evidence,note='',role='local'):
    return {'symbol':symbol,'text':text,'basis':basis,'evidence':evidence,'inference_note':note,'occurrence_role':role}

def event(kind,target,basis,evidence,rationale):
    return {'kind':kind,'target':target,'basis':basis,'evidence':evidence,'rationale':rationale}

units=[]
def context(uid,short,act,rationale,alt='',uncertainty='',confidence='clear'):
    unit={'unit_id':uid,'source_id':sid(short),'span':span(sid(short)),
      'parent_unit_id':None,'grammar':'not_institutional','speech_act':act,'scope':'case_specific',
      'components':[],
      'institution':{'type':'not_applicable','standing':'not_applicable','dispute_present':False,
          'rationale':rationale,'evidence':[ev(short)],'recognition':[],'authority_evidence':[]},
      'statement_target_level':'not_applicable','observed_action_level':'operational',
      'level_rationale':'The visible act concerns this contribution, review, or reported revision in PR #14441; no recurring governance arrangement or allocation of powers is established.',
      'complexity_flags':['unresolved_reference'] if uncertainty else ['none'],
      'alternative_interpretation':alt,'confidence':confidence,'uncertainty_reason':uncertainty,
      'record_role':'context','parse_mode':'literal','deontic_force':'nondeontic','level_alternatives':[],
      'presentation':{'quotation':'none','markup':'plain','rationale':'Supplied occurrence is ordinary prose, including any inline code or commit reference; no later formatting history is inferred.'},
      'disposition_events':[]}
    units.append(unit)
    return unit

C00=context('C00','body','technical_description',
 'The body identifies the backport, its claimed partial reversions and referenced fix; it does not independently prescribe contributor conduct.',
 'The PR as an act offers a backport for integration, but the body itself is a contribution description rather than a separable conduct prescription.')
C01=context('C01','comments:0','reported_action',
 'The author reports updating the PR with ryanofsky\'s changes. This is implementation reporting about the broader contribution, not recognition of a binding expectation.',
 'The report may cover each of the reviewer\'s suggestions, but it does not individually verify their exact wording.')
C02=context('C02','reviews:0','reported_action',
 'An attributable review endorsement names c8d1f1513fb39d80cebbc32e1b5327209485e085; it is neither an instruction nor a grant of authority.')
C03=context('C03','reviews:4','reported_action',
 'An updated review endorsement names 89306ab0df93bfdf5630910bc20b1eccb7379172 and reports code simplification and release-notes updates since the prior review.',
 'The passage supports a changed review target and a reported change set, not changed judgment, mandatory reapproval, or recognition of an institutional duty.')
C04=context('C04','review_comments:4','reported_action',
 'The author endorses two changes without naming them. This single occurrence is retained without multiplying it into independent endorsements of particular suggestions.',
 'The two substantive release-note paragraphs are plausible referents, but the naming correction is also in the release-note discussion and reliable threading is unavailable.',
 'The referent of Both cannot be uniquely recovered from the supplied text and path.', 'unresolved')
C05=context('C05','review_comments:5','reported_action',
 'The author reports a fix but supplies no textual referent. The report is retained with an unresolved target.',
 'It could respond to the naming correction or another release-note request. Source ordering and the shared file path do not uniquely decide.',
 'The object of fixed is absent and reliable reply threading is not supplied.', 'unresolved')
C06=context('C06','review_comments:6','reported_action',
 'The author agrees about behavioral equivalence with or without the check for "*" and reports removal. The shared distinctive object supports linking this response to the removal suggestion.',
 'The report establishes the author\'s stated edit, not an independently reconstructed intermediate patch or a general obligation to follow review.')
C07=context('C07','comments:1','reported_action',
 'A separate participant endorses the named abbreviated revision 89306ab; no individual review suggestion or institutional expectation is specified.')
C08=context('C08','comments:2','reported_action',
 'The reviewer endorses the fully identified revision and explains this backport\'s code-versus-test differences. These are technical review observations, not a proposed backport procedure.',
 'Mention of other backport PRs could provide comparative practice context, but it does not state a general obligation or authorized exception.')

metadata_merge=[ev('metadata','"merged_at": "2018-11-10T11:46:02+00:00"'), ev('metadata','"merged": true')]
broad_report=[ev('comments:0')]

def statement(uid,short,quote,components,parse='literal',quotation='none',markup='plain',alternative='',uncertainty='',institution_note='',level_note=''):
    e=ev(short,quote)
    u={'unit_id':uid,'source_id':sid(short),'span':e['span'],'parent_unit_id':None,
      'grammar':'regulative','speech_act':'proposed','scope':'case_specific','components':components,
      'institution':{'type':'undetermined','standing':'text_only','dispute_present':False,
        'rationale':institution_note or 'A one-off technical/editorial review recommendation is institutionally relevant as proposed contributor conduct, but the packet supplies no attributed authorization or social expectation sufficient to select rule, norm, or strategy. Technical assent and editing do not establish expectation recognition.',
        'evidence':[e],'recognition':[], 'authority_evidence':[]},
      'statement_target_level':'operational','observed_action_level':'operational',
      'level_rationale':level_note or 'The focal action is an edit to this contribution during review. It concerns operational contribution work, not revision of a recurring governance arrangement.',
      'complexity_flags':['none'],'alternative_interpretation':alternative,'confidence':'plausible',
      'uncertainty_reason':uncertainty,'record_role':'statement','parse_mode':parse,
      'deontic_force':'recommendation','level_alternatives':[],
      'presentation':{'quotation':quotation,'markup':markup,'rationale':
        'An original editorial proposal introduces new replacement/additional wording; the blockquoted technical text is proposed wording, not a repeated original proposition.' if quotation=='proposed_wording' else
        'The proposal is supplied in ordinary prose with inline code; no strike-through or later formatting history is established.'},
      'disposition_events':[]}
    u['institution']['recognition'].append(event('reported_implementation','broader_proposal','context_inferred',broad_report,
        'The PR author thanks ryanofsky and reports incorporating the reviewer\'s changes. Attribution to the set of review suggestions is supported, but individual implementation is not verified by this broad report.'))
    u['institution']['recognition'].append(event('recorded_status','broader_proposal','explicit',metadata_merge,
        'Metadata records integration of PR #14441, not recognition of this recommendation as an expectation or verification of each embedded edit.'))
    u['disposition_events'].append(event('reported_implemented','broader_proposal','context_inferred',broad_report,
        'The broader PR is reported updated with the reviewer\'s changes; the scope remains broader than exact fulfillment of this proposition.'))
    u['disposition_events'].append(event('recorded_merged','broader_proposal','explicit',metadata_merge,
        'The PR is recorded merged on 2018-11-10. No network-adoption or general-governance consequence follows from this metadata.'))
    units.append(u)
    return u

S01=statement('S01','review_comments:0',T[sid('review_comments:0')],[
 component('A','jnewbery, inferred as the PR reviser','context_inferred',[ev('comments:0',"I've updated the PR with your changes.")],
   'No actor is named in the elliptical recommendation. The later statement is attributed to jnewbery in packet metadata and identifies the speaker as the person updating the PR with this reviewer\'s changes; this supports an inferred addressee, not an institutional role.', 'context_reference'),
 component('D','Should','explicit',[ev('review_comments:0','Should')],
   'Advisory should expresses the naming recommendation in this review context; an interpretation as technical correctness remains possible.'),
 component('I','write','context_inferred',[ev('review_comments:0')],
   'The literal predicate is be. Write reconstructs the proposed editorial action rather than labeling be as an institutional definition.','semantic_inference'),
 component('Bdir','`listtransactions`','context_inferred',[ev('review_comments:0','`listtransactions`')],
   'The desired identifier is a literal predicative complement under be; its role as the object to write is reconstructed under the editorial action. The complete identifier is preserved.','semantic_inference'),
 component('Cex','with `s`','explicit',[ev('review_comments:0','with `s`')],
   'The explicit qualifier preserves the plural-s correction rather than merely naming an unspecified spelling edit.')
],parse='pragmatic',alternative='Literally this is a technical correctness assertion about an RPC name. The review location in doc/release-notes.md and advisory should support an elliptical request to correct the spelling; no binding naming rule is established.',
 uncertainty='The exact replaced token and comment line are not supplied. The requested spelling is explicit; the action and reviser are reconstructed.',
 level_note='The focal act is correcting the RPC name in this PR\'s release notes. Its operational target is an editorial change, not the constitution of an RPC or a governance role.')

r1=T[sid('review_comments:1')]
start1=r1.index("I'd maybe change")
newwords1=r1[r1.index('to:',start1):]
S02=statement('S02','review_comments:1',r1[start1:],[
 component('A','I (ryanofsky as the hypothetical editor)','explicit',[ev('review_comments:1','I',start=start1)],
   'The first-person subject belongs to the explicitly supplied hypothetical action I would change. Packet authorship attributes I to ryanofsky. This literal proposal is not treated as a committed personal plan.'),
 component('I','change','explicit',[ev('review_comments:1','change',start=start1)]),
 component('Bdir','it','explicit',[ev('review_comments:1','it',start=r1.index('change',start1)+len('change')),ev('review_comments:1','This paragraph')],
   'It remains the explicit object of change. The antecedent This paragraph lies outside the minimal proposal span and resolves the target to the criticized paragraph, not to the PR as a whole.','context_reference'),
 component('Cex',newwords1,'explicit',[ev('review_comments:1',newwords1)],
   'The full replacement wording constrains the proposed edit: both directions when deprecated accounts are enabled, incoming only without that setting, with the account-versus-label explanation. These are technical content qualifications, not separate institutional permissions.')
],quotation='proposed_wording',markup='mixed',alternative='As an indirect review request, the expected editor could instead be the PR author, contextually inferred from the later update report. The chosen literal parse preserves the reviewer\'s hypothetical I would change without converting it into a commitment. The replacement text itself is technical description.',
 uncertainty='The antecedent paragraph\'s original full text is absent. The source supplies a proposed replacement, but its literal first-person formulation and recipient-oriented review use allow alternative actor parses.',
 level_note='The focal action is changing this release-note paragraph. The recurring RPC behaviors described inside the proposed text are technical content, not recurring contributor-governance arrangements.')

r2=T[sid('review_comments:2')]
proposal2=r2[r2.index('Maybe drop'):]
S03=statement('S03','review_comments:2',proposal2,[
 component('A','jnewbery, inferred as the PR reviser','context_inferred',[ev('review_comments:6',"I've removed it.")],
   'The recommendation omits its actor. The later response, attributed to jnewbery, reports removal of the same distinctive check, supporting this inferred addressee.','context_reference'),
 component('I','drop','explicit',[ev('review_comments:2','drop')]),
 component('Bdir','the new check for "*" here','context_inferred',[ev('review_comments:2','the new check for "*" here')],
   'The object of drop is elided. The preceding clause supplies the new check as subject of changes anything; its object role under drop is reconstructed. This evidence is outside the minimal suggestion span.','semantic_inference'),
 component('Cex','for clarity','explicit',[ev('review_comments:2','for clarity')],
   'An explicitly stated purpose constrains the suggested removal; it is not an if-seeking-clarity activation condition.'),
 component('Cac',"unless I'm missing something",'explicit',[ev('review_comments:2',"unless I'm missing something")],
   'The suggestion is defeasible if the reviewer has overlooked a relevant rationale; this qualification is not silently discarded.')
],alternative='This can be read as a tentative engineering simplification rather than a socially expected practice. Maybe is a hedge, not lexical institutional permission; the omitted object is recoverable from the immediately preceding technical premise.',
 uncertainty='No reliable thread or intermediate patch is supplied, but the distinctive check and explicit author removal report provide strong local correspondence. The reviewer\'s caveat does not identify what missing consideration would defeat the advice.',
 level_note='The focal action is removing the particular new check for "*" in this PR\'s wallet code. Review and reported editing are operational; no general simplification requirement is established.')
S03['institution']['evidence'].append(ev('review_comments:2',r2[:r2.index('Maybe drop')].rstrip()))
S03['institution']['recognition'].insert(0,event('reported_implementation','this_proposition','context_inferred',[ev('review_comments:6')],
 'The author specifically refers to the check for "*", accepts the behavioral-equivalence premise, and says it was removed. This is attributable implementation reporting; the absence of reply threading keeps the linkage contextual and does not establish expectation recognition.'))
S03['disposition_events'].insert(0,event('accepted','this_proposition','context_inferred',[ev('review_comments:6')],
 'Agreement about the same check and the removal report support acceptance of this local technical suggestion, not adoption of an institutional rule.'))
S03['disposition_events'].insert(1,event('reported_implemented','this_proposition','context_inferred',[ev('review_comments:6')],
 'The response identifies the check for "*" and reports its removal. No complete intermediate code history is available for independent verification of the precise removed check.'))

r3=T[sid('review_comments:3')]
newwords3=r3[r3.index('Maybe:'):]
S04=statement('S04','review_comments:3',r3,[
 component('A','jnewbery, inferred as the PR reviser','context_inferred',[ev('comments:0',"I've updated the PR with your changes.")],
   'The reviewer is the subject of I think, not an explicit actor of document. The later author report identifies jnewbery as the PR reviser and supports a contextual addressee for the request.','context_reference'),
 component('I','document','explicit',[ev('review_comments:3','document')]),
 component('Bdir','the empty string change','explicit',[ev('review_comments:3','the empty string change')]),
 component('Cex',newwords3,'explicit',[ev('review_comments:3',newwords3)],
   'The introduced wording proposes the technical content of the documentation: empty-string behavior with deprecated accounts, the error without that setting, and its stated usefulness/confusion rationale. Maybe leaves the exact wording advisory.')
],quotation='proposed_wording',markup='mixed',alternative='The proposed block is a technical capability/error description. Its institutional relevance arises from the explicit request to document that behavior; possible to pass is not permission granted by a governance authority.',
 uncertainty='The author later reports incorporation of the reviewer\'s changes, but that broad report does not establish exact adoption of every proposed word.',
 level_note='The focal action is adding documentation to this contribution\'s release notes. The conditional RPC behavior being described is not itself a contributor-governance rule or a stated institutional sanction.')

# Deterministic order follows packet entries, then span positions.
order={e['source_id']:i for i,e in enumerate(pkt['entries'])}
units.sort(key=lambda u:(order[u['source_id']],u['span']['start'],u['unit_id']))

def rel(a,b,typ,basis,rationale,evidence):
 return {'from_unit_id':a,'to_unit_id':b,'type':typ,'basis':basis,'rationale':rationale,'evidence':evidence,'logic_scope':'not_applicable'}
relations=[]
for s,short in [('S01','review_comments:0'),('S02','review_comments:1'),('S04','review_comments:3')]:
 relations.append(rel(s,'C01','uptake','context_inferred',
  'The later author report explicitly thanks the reviewer and says the PR incorporates the reviewer\'s changes. This is broader-proposal reported uptake, not verified individual fulfillment or expectation recognition.',
  [ev(short),ev('comments:0')]))
relations.append(rel('S03','C06','uptake','context_inferred',
 'The distinctive check for "*" is repeated in the author\'s agreement and removal report, supporting a specific response to the drop suggestion. Reliable reply threading is absent, so the relation remains context-inferred.',[ev('review_comments:2'),ev('review_comments:6')]))
relations.append(rel('C03','C02','review_target_update','context_inferred',
 'The same reviewer names a new commit and refers to changes since the last review. The earlier supplied review names c8d1f1513fb39d80cebbc32e1b5327209485e085; the later names 89306ab0df93bfdf5630910bc20b1eccb7379172. The earlier target is linked by author, chronology, and wording, not by an explicit full quotation; no changed judgment or mandatory reapproval is inferred.',[ev('reviews:0'),ev('reviews:4')]))
relations.append(rel('C01','C03','temporal','context_inferred',
 'Entry timestamps place the author update report at 2018-10-10T07:40:49+00:00 before the later review at 2018-10-10T07:57:22+00:00. This orders supplied occurrences only and does not establish the timing of hidden edits or causation.',[ev('comments:0'),ev('reviews:4')]))

reasons={
 'body':'Focal entry screened exhaustively. Describes the contribution, partial reverts, and referenced fix; no separable conduct prescription or committed method is expressed.',
 'comments:0':'Focal entry screened exhaustively. Reports a PR update and thanks a reviewer; retained as uptake context, not a new prescription.',
 'comments:1':'Focal entry screened exhaustively. Commit-specific review endorsement only; retained as context, without institutional authority or expectation claims.',
 'comments:2':'Focal entry screened exhaustively. Review endorsement plus explanation of code and test backport differences; no proposed recurring backport arrangement.',
 'reviews:0':'Focal entry screened exhaustively. Commit-specific endorsement only; retained as an earlier review-target endpoint.',
 'reviews:1':'Focal empty text. COMMENTED state does not create an unexpressed proposition.',
 'reviews:2':'Focal empty text. COMMENTED state does not create an unexpressed proposition.',
 'reviews:3':'Focal empty text. COMMENTED state does not create an unexpressed proposition.',
 'reviews:4':'Focal entry screened exhaustively. Updated commit endorsement and reported change set; retained as context, without turning technical assent into expectation recognition.',
 'review_comments:0':'Focal entry screened exhaustively. Elliptical naming correction is a plausible editorial recommendation; technical correctness alternative retained.',
 'review_comments:1':'Focal entry screened exhaustively. One proposed paragraph replacement includes its full technical content; initial criticism supplies rationale rather than a second independent request.',
 'review_comments:2':'Focal entry screened exhaustively. One suggested removal preserves its purpose and epistemic exception; the preceding technical premise supplies the elided object.',
 'review_comments:3':'Focal entry screened exhaustively. One documentation request includes suggested wording and all conditional behavior qualifications; embedded capabilities/errors are technical content.',
 'review_comments:4':'Focal entry screened exhaustively. Endorsement of two unnamed changes; retained as one context record with unresolved referents.',
 'review_comments:5':'Focal entry screened exhaustively. Bare implementation report with unresolved target; no new directive.',
 'review_comments:6':'Focal entry screened exhaustively. Agreement and reported removal of the distinctive check; retained as specific uptake context, not an additional prescription.',
 'metadata':'Supplement screened for outcome context. Records PR identity, changed files, merger alias and status; not an exhaustive institutional extraction target. Metadata supplies no independently established contributor authority.',
 'supplement_metadata':'Supplement screened for revision and outcome context. Its merged flag and timestamp corroborate this PR\'s recorded integration and identify the retained head; no assumption about unrelated referenced PRs.',
 'patch:0':'Supplement screened for documentation-outcome context. Retained head supplies the requested name and two behavioral explanations. Context-only scope does not assert absence of all institutional content.',
 'patch:1':'Supplement screened for technical-outcome context. Contains wallet RPC code, argument validation, and help text. Technical must/should wording is not automatically institutional obligation; this is not an exhaustive supplemental extraction target.',
 'patch:2':'Supplement screened for test context. Adds labeled import and transaction assertions at the retained head. Context-only selection is not a claim that the artifact has no institutional relevance.',
 'patch:3':'Supplement screened for test context. Changes watch-only label filtering assertions at the retained head. Context-only selection is not a claim that the artifact has no institutional relevance.'}
screen=[]
for e in pkt['entries']:
 us=[u for u in units if u['source_id']==e['source_id']]
 short=e['source_id'].split(':',1)[1]
 d='candidate' if any(u['record_role']=='statement' for u in us) else 'empty' if not e['text'] else 'context_only'
 screen.append({'source_id':e['source_id'],'disposition':d,'reason':reasons[short],'unit_ids':[u['unit_id'] for u in us]})

summary={
 'observed_outcomes':[
  {'claim':'The author reports incorporating ryanofsky\'s changes into PR #14441. The reviewer subsequently endorses revision 89306ab0df93bfdf5630910bc20b1eccb7379172 and describes only code simplification and release-notes updates since the earlier review of c8d1f1513fb39d80cebbc32e1b5327209485e085. These are attributed reports and endorsements, not proof of recognized obligations.',
   'evidence':[ev('comments:0'),ev('reviews:0'),ev('reviews:4')]},
  {'claim':'The author specifically reports removing the check for "*" after agreeing that behavior would be identical with or without it. The packet does not reconstruct the exact intermediate patch reviewed.',
   'evidence':[ev('review_comments:2'),ev('review_comments:6')]},
  {'claim':'The retained release-notes patch contains the complete name `listtransactions`, distinguishes transactions returned with versus without -deprecatedrpc=accounts, and describes the empty-string case and error without that setting. These contents correspond to the review suggestions, with wording differences; the head snapshot alone does not establish the causal editing history.',
   'evidence':[ev('review_comments:0'),ev('review_comments:1'),ev('review_comments:3'),ev('patch:0')]},
  {'claim':'The supplied metadata records PR #14441 as merged at 2018-11-10T11:46:02+00:00 by the alias laanwj; supplemental metadata identifies the base as 0.17 and head/merge revision as 89306ab0df93bfdf5630910bc20b1eccb7379172. This is repository integration, with no supplied network-adoption outcome.',
   'evidence':metadata_merge+[ev('metadata','"merged_by": "laanwj"'),ev('supplement_metadata','"base": "0.17"'),ev('supplement_metadata','"head_sha": "89306ab0df93bfdf5630910bc20b1eccb7379172"'),ev('supplement_metadata','"merge_commit_sha": "89306ab0df93bfdf5630910bc20b1eccb7379172"')]}
 ],
 'mechanisms':[
  {'category':'reason_giving','claim':'The reviewer questions whether the new check for "*" changes behavior and tentatively suggests dropping it for clarity unless something has been overlooked. The author responds that behavior is identical and reports removal. This specific correspondence supports a local reason-giving-and-edit sequence, without establishing that the review imposed a duty.',
   'evidence':[ev('review_comments:2'),ev('review_comments:6')],
   'unit_ids':['S03','C06'],'alternative_explanation':'The author could have reached the same simplification independently; the supplied response supports uptake but does not identify a causal effect or verify intermediate code.', 'status':'supported_sequence'},
  {'category':'review_coordination','claim':'The naming correction and two documentation suggestions are followed by the author\'s report that the PR was updated with the reviewer\'s changes; the same reviewer then endorses a later revision and reports code simplification and release-notes updates. The retained release-notes patch contains corresponding technical content. This supports a review-and-revision sequence at the broader contribution level, while the targets of Both are good changes and fixed remain unresolved.',
   'evidence':[ev('review_comments:0'),ev('review_comments:1'),ev('review_comments:3'),ev('comments:0'),ev('reviews:0'),ev('reviews:4'),ev('patch:0'),ev('review_comments:4'),ev('review_comments:5')],
   'unit_ids':['S01','S02','S04','C01','C02','C03','C04','C05'],
   'alternative_explanation':'Editorial changes could have been revised independently or together; incomplete threading and edit history prevent assigning every acknowledgment or exact textual change to a single request. The later merged status does not by itself demonstrate a review requirement.',
   'status':'supported_sequence'}
 ],
 'missing_evidence':[
  'Reliable reply threading, comment line positions, and complete edit/revision histories are absent; source indices are not comment IDs.',
  'The complete original paragraph and exact intermediate version of the newly added check are not supplied.',
  'No supplied authority provision, enforcement linkage, or explicit recognition of a contributor expectation supports rule or locally-supported standing for these technical suggestions.',
  'No outcomes for referenced PRs #14411, #13075, #14023, or issue/proposal #14382 are supplied beyond the focal body\'s claims.',
  'No network adoption, release deployment, or higher-level governance allocation outcome is established by repository merge metadata.'
 ],
 'unresolved_questions':[
  'Which two exact changes does Both are good changes endorse, and which specific request does fixed answer?',
  'Should the hypothetical I would change in the paragraph suggestion be parsed literally as the reviewer\'s proposed editing action or pragmatically as a request to the PR reviser? Both preserve the same proposed edit, but actor-role coding differs.',
  'How much of the precise documentation wording was adopted through each review exchange rather than subsequent independent revision?',
  'Do these case-specific suggestions instantiate any broader recognized contributor expectation? The supplied exchange does not decide.'
 ]}
annotation={'schema_version':'0.3','run_id':'F02_v03_r3','episode_id':'F02','packet_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'entry_screening':screen,'units':units,'relations':relations,'episode_summary':summary}
out=json.dumps(annotation,ensure_ascii=False,indent=2)+'\n'
(ROOT/'annotation.json').write_text(out,encoding='utf-8')
first=ROOT/'annotation.first_complete.json'
if first.exists(): raise RuntimeError('First-complete file already exists; it must not be overwritten.')
first.write_text(out,encoding='utf-8')
print(json.dumps({'first_complete_frozen':str(first),'units':len(units),'statements':sum(u['record_role']=='statement' for u in units),'contexts':sum(u['record_role']=='context' for u in units),'relations':len(relations),'screened_entries':len(screen),'packet_sha256':annotation['packet_sha256']},indent=2))
