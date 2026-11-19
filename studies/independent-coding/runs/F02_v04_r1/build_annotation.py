import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
packet_bytes = (ROOT / 'packet.json').read_bytes()
packet = json.loads(packet_bytes)
entries = {e['source_id']: e for e in packet['entries']}
PR = 'https://github.com/bitcoin/bitcoin/pull/14441'
PREFIX = 'pr14441:'

def ev(source, quote=None, start=None):
    source = source if source.startswith(PREFIX) else PREFIX + source
    text = entries[source]['text']
    if quote is None:
        quote = text
    pos = text.index(quote) if start is None else start
    assert text[pos:pos+len(quote)] == quote
    return {'source_id': source, 'span': {'start': pos, 'end': pos+len(quote), 'quote': quote}}

identity = [ev('supplement_metadata', '"url": "https://github.com/bitcoin/bitcoin/pull/14441"')]
merge = [ev('supplement_metadata', '"merged": true'),
         ev('supplement_metadata', '"head_sha": "89306ab0df93bfdf5630910bc20b1eccb7379172"'),
         ev('supplement_metadata', '"merge_commit_sha": "89306ab0df93bfdf5630910bc20b1eccb7379172"'),
         ev('supplement_metadata', '"merged_at": "2018-11-10T11:46:02Z"')]

def unique(es):
    out=[]
    for e in es:
        if e not in out: out.append(e)
    return out

def qualifier(description, evidence, attachment='scope_note', rationale=None):
    return {'description': description, 'evidence': evidence, 'attachment': attachment,
            'linked_unit_id': None, 'rationale': rationale or 'This qualification belongs to the focal edit and is retained explicitly in its proposition scope.'}

def component(symbol, text, evidence, gov, basis='explicit', occurrence='local', note=''):
    return {'symbol': symbol, 'text': text, 'basis': basis, 'evidence': evidence,
            'inference_note': note, 'occurrence_role': occurrence, 'governing_span': gov}

def institution(statement, evidence):
    return {'type': 'undetermined' if statement else 'not_applicable', 'dispute_present': False,
            'rationale': ('This is a case-specific technical edit recommendation. It does not establish a socially expected recurring practice, personal committed method, constituted institutional status, or attributed authorization/enforcement. Technical merit and later uptake do not supply those missing grounds.' if statement else 'Communicative or technical context; not an additional institutional proposition.'),
            'evidence': evidence, 'recognition': [], 'authority_evidence': [],
            'standing_profile': dict.fromkeys(['documentary','recognition','application'], 'none' if statement else 'not_applicable'),
            'documentary_support': [], 'application_evidence': [], 'challenges': [], 'type_alternatives': []}

units=[]
def unit(uid, source, quote=None, statement=False, speech='reported_action', summary='',
         mode='literal', quotation='none', markup='plain', alternative='', uncertainty='', level_activity=''):
    anchor=ev(source,quote)
    u={'unit_id': uid, **anchor, 'parent_unit_id': None,
       'grammar': 'regulative' if statement else 'not_institutional', 'speech_act': speech,
       'scope': 'case_specific', 'components': [], 'institution': institution(statement,[anchor]),
       'statement_target_level': 'operational' if statement else 'not_applicable',
       'observed_action_level': 'operational',
       'level_rationale': ('The focal action changes this contribution under ordinary review; it does not choose a recurring governance arrangement. The observed act is an operational review suggestion.' if statement else 'The visible act concerns this contribution, its review, or a reported edit under ordinary contribution activity. No higher-level decision is evidenced.'),
       'complexity_flags': ['none'], 'alternative_interpretation': alternative,
       'confidence': 'plausible' if statement or uncertainty else 'clear',
       'uncertainty_reason': uncertainty, 'record_role': 'statement' if statement else 'context',
       'parse_mode': mode, 'deontic_force': 'recommendation' if statement else 'nondeontic',
       'presentation': {'quotation': quotation, 'markup': markup,
                        'rationale': ('The passage proposes replacement wording; its blockquote is drafted text, not a repeated endorsement.' if quotation=='proposed_wording' else 'Presentation is retained as supplied; inline code marks do not turn prose into a code block.')},
       'disposition_events': [], 'proposition': None,
       'target_level_alternatives': [], 'observed_level_alternatives': [],
       'level_evidence': {'target_activity': level_activity if statement else 'Not applicable to a context record.',
                          'observed_activity': 'Review recommendation on this contribution.' if statement else level_activity,
                          'arrangement': 'Ordinary Bitcoin Core pull-request contribution and review; no authority beyond the supplied record is inferred.',
                          'evidence': [anchor]}}
    if statement:
        u['proposition']={'summary': summary, 'decision_object_id': PR,
                          'domain': 'Review and editing of PR #14441, the v0.17 backport described in the supplied packet.',
                          'time_scope': 'Advice in the retained review comment submitted on 2018-10-10, limited to this PR. Complete comment edit history is unavailable.',
                          'identity_evidence': identity, 'qualifiers': []}
    units.append(u)
    return u

S1=unit('F02_S01','review_comments:0',statement=True,speech='proposed',mode='pragmatic',
    summary='ryanofsky recommends correcting the release-note RPC name in this PR to `listtransactions`, including the final `s`; the addressed editor is contextually inferred to be jnewbery.',
    alternative='Literal technical reading: the correct RPC identifier is `listtransactions` with an s. The preferred parse reconstructs an editorial action, not an institutional definition or a binding naming rule.',
    uncertainty='The correction action and addressee are elliptical. No inline patch location or reliable reply thread is supplied.',
    level_activity='Correct the RPC identifier in this PR\'s release notes.')
g1=ev('review_comments:0')
S1['components']=[
    component('A','jnewbery (contextually addressed PR editor)',[ev('comments:0',"I've updated the PR with your changes.")],g1,'context_inferred','context_reference','The source does not name an editor. The supplied author attribution of the later update report identifies jnewbery as responding to ryanofsky\'s changes; this supports an inferred addressee, not an explicit local actor.'),
    component('D','Should',[ev('review_comments:0','Should')],g1,'context_inferred','semantic_inference','Should explicitly qualifies the desired spelling under be. Treating it as a recommendation governing an editor\'s correction is a role reconstruction in this pragmatic parse.'),
    component('I','correct',[g1],g1,'context_inferred','semantic_inference','The source predicates should be, not an explicit editing verb. Correct is the reconstructed review request.'),
    component('Bdir','the RPC name in the release notes',[g1],g1,'context_inferred','semantic_inference','The target of correction is inferred from the displayed identifier and the supplied review path doc/release-notes.md; no local grammatical object of correct is expressed.'),
    component('Cex','to `listtransactions` with `s`',[ev('review_comments:0','`listtransactions` with `s`')],g1,'context_inferred','semantic_inference','This is the required result of the inferred edit; in the literal clause it is the complement of be, not an explicit editing constraint.')]
S1['proposition']['qualifiers']=[qualifier('Use the complete identifier `listtransactions`, including its final s, not a shortened or singular identifier.',[ev('review_comments:0','`listtransactions` with `s`')],'component')]

draft2=entries[PREFIX+'review_comments:1']['text'].split('\r\n\r\n',1)[1]
q2="I'd maybe change it to:\r\n\r\n"+draft2
S2=unit('F02_S02','review_comments:1',q2,True,'proposed',
    summary='ryanofsky tentatively recommends that the PR editor replace the release-note paragraph with wording explaining both behaviors in the same release: with `-deprecatedrpc=accounts`, a label/account/dummy argument returns outgoing and incoming transactions; without that setting it returns incoming transactions only, with the stated account-versus-label rationale.',
    mode='pragmatic',quotation='proposed_wording',markup='mixed',
    alternative='A literal hypothetical first-person formulation describes what the reviewer would change. The preferred editorial-request reading infers the PR editor as the advised actor. The embedded RPC behavior is technical description, not a separate institutional permission.',
    uncertainty='The intended edit is explicit, but the actor is pragmatically inferred and the supplied packet lacks reliable reply threading.',
    level_activity='Replace this PR\'s release-note paragraph about the two RPC behaviors.')
g2=ev('review_comments:1',q2)
S2['components']=[
    component('A','jnewbery (contextually addressed PR editor)',[ev('comments:0',"I've updated the PR with your changes.")],g2,'context_inferred','context_reference','The local I names the hypothetical recommending speaker, not the advised editor. The addressee in the preferred request parse is inferred from jnewbery\'s attributed response to ryanofsky\'s changes.'),
    component('I','change',[ev('review_comments:1','change')],g2),
    component('Bdir','it (the release-note paragraph)',[ev('review_comments:1','it',entries[PREFIX+'review_comments:1']['text'].index('change it')+7)],g2,note='Even in the pragmatic recommendation parse, it is explicitly the object of change. Its antecedent is This paragraph in the preceding sentence; the supplied path locates that paragraph in doc/release-notes.md.'),
    component('Cex',draft2,[ev('review_comments:1',draft2)],g2)]
S2['proposition']['qualifiers']=[
    qualifier('The proposed edit is tentative: I\'d maybe change it.',[ev('review_comments:1',"I'd maybe change it to:")]),
    qualifier('The criticism concerns a paragraph describing both behaviors present in the same release; this motivates wording, rather than making the edit conditional on a future release.',[ev('review_comments:1',"This paragraph doesn't really make sense when both behaviors are present in the same release.")]),
    qualifier('The exact drafted replacement preserves the setting-dependent return types and the explanation that spending from specific accounts used to be possible but is no longer possible with labels.',[ev('review_comments:1',draft2)],'component')]

q3="Maybe drop for clarity (unless I'm missing something)."
S3=unit('F02_S03','review_comments:2',q3,True,'proposed',
    summary='ryanofsky tentatively recommends dropping the new check for "*" in this PR\'s wallet RPC code for clarity, unless the reviewer is missing something; jnewbery is the contextually inferred editor.',
    mode='pragmatic',alternative='The preceding sentence can be read as a request to explain the check, but the selected focal clause explicitly supplies a tentative drop recommendation. The uncertainty caveat leaves room to retain a check if its function was missed.',
    uncertainty='The exact reviewed code line and pre-update patch are absent. The check is textually identifiable, but its exact implementation cannot be reconstructed.',
    level_activity='Remove the particular new wallet RPC check if the reviewer has not missed a relevant function.')
g3=ev('review_comments:2',q3)
S3['components']=[
    component('A','jnewbery (contextually addressed PR editor)',[ev('review_comments:6',"I've removed it.")],g3,'context_inferred','context_reference','The imperative omits its actor. jnewbery\'s attributed reply reports removal of the same check; the actor assignment remains contextual.'),
    component('I','drop',[ev('review_comments:2','drop')],g3),
    component('Bdir','the new check for "*" here',[ev('review_comments:2','the new check for "*" here')],g3,'context_inferred','semantic_inference','The antecedent is outside the selected focal clause, where it is the subject of changes. Its receiver role under the elliptical drop is reconstructed, rather than borrowing an explicit object from another predicate.'),
    component('Cex','for clarity',[ev('review_comments:2','for clarity')],g3),
    component('Cac',"unless I'm missing something",[ev('review_comments:2',"unless I'm missing something")],g3)]
S3['proposition']['qualifiers']=[
    qualifier('The recommendation is tentative (Maybe).',[ev('review_comments:2','Maybe')]),
    qualifier('The reviewer does not see how this particular new check changes behavior; that is an attributed rationale, not an independently verified technical fact.',[ev('review_comments:2','I don\'t see how the new check for "*" here changes anything.')]),
    qualifier('Removal is for clarity and is defeasible if the reviewer is missing something.',[ev('review_comments:2',"for clarity (unless I'm missing something)")],'component')]

draft4=entries[PREFIX+'review_comments:3']['text'].split('\r\n\r\n',1)[1]
S4=unit('F02_S04','review_comments:3',statement=True,speech='proposed',mode='literal',quotation='proposed_wording',markup='mixed',
    summary='ryanofsky recommends documenting the empty-string change in this PR\'s release notes and offers tentative wording: for backward compatibility with `-deprecatedrpc=accounts`, an empty string label lists unlabeled transactions; without the setting it is an error, with limited usefulness and possible confusion offered as the rationale.',
    alternative='The opening is phrased as an evaluation of what would be good, but directly supplies document and its object. The subsequent possible-to-pass claim describes technical capability and does not independently authorize conduct.',
    uncertainty='The exact attribution of Both are good changes and fixed to individual release-note suggestions is not established by reply threading.',
    level_activity='Add documentation of the empty-string change to this PR\'s release notes.')
g4=ev('review_comments:3',"I think it'd be good to document the empty string change.")
S4['components']=[
    component('A','jnewbery (contextually addressed PR editor)',[ev('comments:0',"I've updated the PR with your changes.")],g4,'context_inferred','context_reference','The subject of document is omitted. jnewbery\'s attributed update response supplies contextual evidence of the advised editor; I in I think denotes the reviewer and is not assigned this role.'),
    component('I','document',[ev('review_comments:3','document')],g4),
    component('Bdir','the empty string change',[ev('review_comments:3','the empty string change')],g4)]
S4['proposition']['qualifiers']=[
    qualifier('The following paragraph is offered as tentative wording (Maybe), not an independently binding behavioral prescription.',[ev('review_comments:3','Maybe:')]),
    qualifier('The drafted content distinguishes enabled and disabled `-deprecatedrpc=accounts`, preserves backward compatibility and the empty-string label, and includes the attributed usefulness/confusion explanation.',[ev('review_comments:3',draft4)]),
    qualifier('The focal activity is documenting a technical change; possible to pass describes RPC behavior, not institutional permission.',[ev('review_comments:3',draft4)])]

C1=unit('F02_C01','body',speech='technical_description',level_activity='Describe the submitted backport and its stated relationships to earlier numbered contributions.',
    alternative='Submitting a backport may implicitly invite integration, but the body text itself describes this contribution rather than independently prescribing a governance act.',
    uncertainty='Retained body may have later edits; its creation date cannot date every sentence. The packet supplies no outcomes for referenced #14411, #13075, #14023, or #14382.')
C2=unit('F02_C02','comments:0',level_activity='Report updating this PR in response to the named reviewer\'s changes.')
C3=unit('F02_C03','comments:1',level_activity='Acknowledge a specified abbreviated review target.',
    alternative='This is ordinary technical assent to a revision, not evidence of a recognized institutional expectation.')
C4=unit('F02_C04','comments:2',level_activity='Acknowledge a specified revision and describe its code and test relationship to the original backport source.',
    alternative='The backport comparison could suggest a typical workflow, but it does not prescribe that all backports must be clean or identify an enforcement mechanism.')
C5=unit('F02_C05','reviews:0',level_activity='Acknowledge the earlier specified revision of this PR.',
    alternative='The supplied APPROVED review state is assent to the contribution, not proof of rule-making authority or project-wide obligation.')
C6=unit('F02_C06','reviews:4',level_activity='Acknowledge the later revision and report changes since the reviewer\'s last review.',
    alternative='A renewed review does not by itself establish mandatory reapproval or a changed judgment.')
C7=unit('F02_C07','review_comments:4',level_activity='Express ordinary approval of two changes, with the exact pair unresolved.',
    uncertainty='Both does not identify the two suggestions in the text; path and timestamp alone cannot restore missing reply threading.')
C8=unit('F02_C08','review_comments:5',level_activity='Report a fix with an unspecified textual target.',
    uncertainty='The one-word report does not identify which release-note change it refers to.')
C9=unit('F02_C09','review_comments:6',level_activity='Agree with the same-check assessment and report removal.',
    alternative='The author\'s behavior-equivalence claim and removal report are evidence of stated reasoning and reported action, not independent technical verification.')

def recognition(kind,target,evidence,rationale,basis='context_inferred',mode='other',speaker='different_actor'):
    return {'kind':kind,'target':target,'basis':basis,'evidence':evidence,'rationale':rationale,'mode':mode,
            'speaker_relation':speaker,'independence_key':PR,'object_id':PR,'identity_evidence':identity}

def disposition(kind,target,evidence,rationale,basis='context_inferred'):
    return {'kind':kind,'target':target,'basis':basis,'evidence':evidence,'rationale':rationale,'object_id':PR,'identity_evidence':identity}

def application(status,target,evidence,rationale):
    return {'status':status,'target':target,'evidence':evidence,'rationale':rationale}

patch0=entries[PREFIX+'patch:0']['text']
patch_name=ev('patch:0','+`listtransactions` label support')
patch_para=ev('patch:0',patch0[patch0.index('+When bitcoin'):patch0.index('+\n+When `-deprecatedrpc')])
patch_empty=ev('patch:0',patch0[patch0.index('+When `-deprecatedrpc'):patch0.index('\n \n Credits')])

for s, artifact, matching in [(S1,patch_name,'The retained release-note heading contains the exact complete RPC name.'),
                             (S2,patch_para,'The retained release-note paragraph preserves the recommended setting distinction, return categories, and account-versus-label rationale, with minor formatting changes.'),
                             (S4,patch_empty,'The retained release-note paragraph preserves the recommended empty-string behavior with and without the setting and the confusion rationale; wording is not verbatim.')]:
    report=[ev('comments:0'),ev('reviews:4'),{'source_id':s['source_id'],'span':s['span']}]
    s['institution']['recognition'].append(recognition('reported_implementation','this_proposition',report,
        'The author reports incorporating this reviewer\'s changes and the reviewer identifies release-note updates. Mapping that aggregate report to this specific suggestion is contextual; it does not recognize a standing expectation.'))
    s['institution']['application_evidence']=[
        application('reported','this_proposition',report,'The author\'s aggregate update report, corroborated by the reviewer\'s release-note update report, contextually includes this suggestion. Specific reply threading remains unavailable.'),
        application('observed','this_proposition',[artifact]+merge,matching+' The same retained head and merge commit identify integration into this PR\'s repository target. This verifies the resulting edit, not the reason for adoption or network deployment.')]
    s['institution']['standing_profile']['application']='both'
    s['disposition_events']=[
        disposition('reported_implemented','this_proposition',report,'The attributed aggregate update reports contextually include the focal release-note suggestion; they are not treated as exact patch evidence.'),
        disposition('recorded_merged','broader_proposal',merge,'Recorded metadata establishes merging PR #14441. The broader label identifies this PR, not any earlier PR mentioned by its body. Exact edit implementation is separately assessed using the retained artifact.','explicit')]

for s in [S2,S4]:
    s['institution']['recognition'].append(recognition('endorsement','unresolved',[ev('review_comments:4')],
        'The author approves Both changes, but absent reply threading the exact pair cannot be established. This is ordinary assent with an unresolved target; no institutional expectation is recognized.','unresolved','ordinary_assent'))

S1['institution']['recognition'].append(recognition('reported_implementation','unresolved',[ev('review_comments:5')],
    'The release-note fixed report is compatible with this spelling correction, but the text does not identify its target. It is retained without being used to establish this proposition\'s application.','unresolved'))

S3['institution']['recognition']=[
    recognition('endorsement','this_proposition',[ev('review_comments:6')],
        'The response explicitly names the check for "*", says it is better without, and reports removal. This is agreement with the technical edit, not recognition of a general expectation.','context_inferred','ordinary_assent'),
    recognition('reported_implementation','this_proposition',[ev('review_comments:6',"I've removed it."),ev('review_comments:6','The behaviour would be identical with or without the check for "*".')],
        'The same response resolves it to the check for "*" and attributes removal to jnewbery. The link to the recommendation follows exact textual correspondence.','context_inferred')]
S3['institution']['application_evidence']=[application('reported','this_proposition',[ev('review_comments:6')],
    'jnewbery reports removing the same check. The retained final diff is not an earlier-versus-later review diff and cannot independently identify which new check was removed after this suggestion.')]
S3['institution']['standing_profile']['application']='reported'
S3['disposition_events']=[
    disposition('accepted','this_proposition',[ev('review_comments:6',"No, you're right. It's better without."),ev('review_comments:6','The behaviour would be identical with or without the check for "*".')],
        'The response accepts the same-check removal recommendation; the opening No answers the reviewer\'s caveat rather than rejecting the recommendation.'),
    disposition('reported_implemented','this_proposition',[ev('review_comments:6')],
        'The author explicitly reports removal; object linkage to the reviewer\'s check is contextual and strong, while exact code history remains missing.'),
    disposition('recorded_merged','broader_proposal',merge,
        'This merge is the disposition of PR #14441, not independent proof of the exact review-stage code removal.','explicit')]

relations=[]
def relation(f,t,typ,evidence,rationale,basis='context_inferred'):
    relations.append({'from_unit_id':f,'to_unit_id':t,'type':typ,'basis':basis,'rationale':rationale,
                      'evidence':evidence,'logic_scope':'not_applicable'})

for s in [S1,S2,S4]:
    relation(s['unit_id'],'F02_C02','uptake',[{'source_id':s['source_id'],'span':s['span']},ev('comments:0')],
        'The author names ryanofsky and reports incorporating the reviewer\'s changes. The mapping to each specific edit is contextual; the aggregate response does not establish a recurring requirement.')
relation('F02_S03','F02_C09','uptake',[ev('review_comments:2'),ev('review_comments:6')],
    'The reply addresses the same check, agrees it is unnecessary, and reports removal; specific correspondence supports uptake without reconstructing the absent reviewed patch.')
relation('F02_S01','F02_C08','uptake',[ev('review_comments:0'),ev('review_comments:5')],
    'The release-note fix could answer the spelling request, but no textual target or reliable reply threading establishes that connection.','unresolved')
for s in [S2,S4]:
    relation(s['unit_id'],'F02_C07','uptake',[{'source_id':s['source_id'],'span':s['span']},ev('review_comments:4')],
        'Both may refer to the two substantive release-note proposals; this plausible pair remains unresolved because the supplied text does not identify it.','unresolved')
relation('F02_C06','F02_C05','review_target_update',[ev('reviews:4'),ev('reviews:0')],
    'The same reviewer names a new commit and refers to the last review; the earlier supplied review names the older commit. The reference to that particular earlier review is contextually inferred, not a finding of mandatory reapproval.')

def outcome(parts):
    return {'claim':' '.join(p['text'] for p in parts),'evidence':unique([e for p in parts for e in p['evidence']]),'claim_parts':parts}

outcomes=[
    outcome([{'text':'jnewbery reports updating PR #14441 with ryanofsky\'s changes.', 'evidence':[ev('comments:0')]+identity},
             {'text':'ryanofsky subsequently acknowledges revision 89306ab0df93bfdf5630910bc20b1eccb7379172 and describes code simplification and release-note updates as the only changes since the last review.', 'evidence':[ev('reviews:4'),ev('reviews:0')]}]),
    outcome([{'text':'jnewbery says the behavior would be identical with or without the check for "*" and reports removing it.', 'evidence':[ev('review_comments:6')]}]),
    outcome([{'text':'The retained release-note patch uses the complete identifier `listtransactions`.', 'evidence':[patch_name]},
             {'text':'It explains the enabled/disabled `-deprecatedrpc=accounts` return behavior and the account-versus-label rationale.', 'evidence':[patch_para]},
             {'text':'It also explains the empty-string distinction and the limited-usefulness/confusion rationale.', 'evidence':[patch_empty]},
             {'text':'Metadata records PR #14441 merged on 2018-11-10, with the retained head recorded as the merge commit.', 'evidence':identity+merge}])]

mechanisms=[]
m=outcome([{'text':'ryanofsky questions the behavioral contribution of the new check for "*" and tentatively recommends removal for clarity, unless something was missed.', 'evidence':[ev('review_comments:2')]},
           {'text':'jnewbery agrees that behavior would be identical without it and reports removal.', 'evidence':[ev('review_comments:6')]}])
m.update({'category':'reason_giving','unit_ids':['F02_S03','F02_C09'],'alternative_explanation':'The author may have independently reached the same simplification or evaluated other unrecorded information. Exact textual correspondence supports a reason-and-response sequence, not an identified causal effect or independent verification of behavior equivalence.','status':'supported_sequence'})
mechanisms.append(m)
m=outcome([{'text':'ryanofsky recommends a spelling correction, replacement behavior paragraph, removal of a check, and documentation of the empty-string change.', 'evidence':[ev('review_comments:0'),ev('review_comments:1'),ev('review_comments:2'),ev('review_comments:3')]},
           {'text':'jnewbery reports updating the PR with that reviewer\'s changes.', 'evidence':[ev('comments:0')]},
           {'text':'The reviewer names a later revision and reports that only code simplification and release-note updates had changed since the last review.', 'evidence':[ev('reviews:0'),ev('reviews:4')]}])
m.update({'category':'review_coordination','unit_ids':['F02_S01','F02_S02','F02_S03','F02_S04','F02_C02','F02_C05','F02_C06'],
          'alternative_explanation':'The exchange is consistent with ordinary voluntary refinement of a backport. It does not establish a mandatory review cycle, an authorization hierarchy, exact reply pairing for the terse responses, or that these suggestions caused the later merge.',
          'status':'supported_sequence'})
mechanisms.append(m)

reasons={
 'body':'The body describes the submitted backport, partial reversions, and claimed fix. These are technical contribution relationships; no independent prescription beyond an implicit invitation to consider the PR is supplied. Referenced PR outcomes are not inferred.',
 'comments:0':'An attributed report of updating the PR with reviewer changes; response context rather than a new prescription.',
 'comments:1':'Commit-specific utACK is ordinary assent, not an institutional expectation or newly prescribed conduct.',
 'comments:2':'Commit-specific utACK and technical comparison to the original backport; no requirement that all backports follow a specified method.',
 'reviews:0':'Commit-specific review assent. APPROVED metadata does not create an independent institutional proposition or establish the reviewer\'s powers.',
 'reviews:1':'Empty retained review text; metadata alone does not supply a candidate proposition.',
 'reviews:2':'Empty retained review text; metadata alone does not supply a candidate proposition.',
 'reviews:3':'Empty retained review text; metadata alone does not supply a candidate proposition.',
 'reviews:4':'Renewed commit-specific assent and report of intervening edits; no mandatory reapproval instruction.',
 'review_comments:0':'Elliptical recommendation to correct the RPC identifier; coded as one pragmatic regulative edit request with a literal technical alternative.',
 'review_comments:1':'One tentative paragraph-replacement recommendation with its complete proposed text and rationale. Embedded conditions describe the desired text, not new duties or permissions.',
 'review_comments:2':'One tentative removal recommendation with clarity purpose and missing-something caveat. The preceding behavior observation supplies the target and rationale, not another executable instruction.',
 'review_comments:3':'One documentation recommendation and offered wording. Technical possible-to-pass and error behavior are preserved as content qualifications, not institutional permission/prohibition.',
 'review_comments:4':'Ordinary assent to two changes with the exact pair unresolved; no new candidate prescription.',
 'review_comments:5':'A terse fix report with unresolved target; no new candidate prescription.',
 'review_comments:6':'Technical agreement and reported removal, preserved as an uptake endpoint rather than another removal recommendation.',
 'metadata':'Supplement screened as recorded contribution status and file-list context, outside exhaustive focal extraction. It establishes this PR\'s recorded merge only; context-only does not assert the absence of institutional content.',
 'supplement_metadata':'Supplement screened as identity, retained head, and recorded merge context, outside exhaustive focal extraction. Its current archival retrieval does not restore comment or patch history; context-only does not assert absence of institutional content.',
 'patch:0':'Supplement screened as a retained-head release-note artifact and implementation evidence for the focal edits. Technical guidance is contextual under the selection design, not exhaustively extracted; this does not assert absence of institutional content.',
 'patch:1':'Supplement screened as retained-head technical code changes. It supplies no complete review-stage patch chronology and does not alone prove removal of the particular new check identified in review. Context-only is a selection-scope decision, not a claim of no institutional content.',
 'patch:2':'Supplement screened as retained-head test changes concerning labels and transaction assertions. Outside exhaustive extraction; context-only does not claim absence of institutional content.',
 'patch:3':'Supplement screened as retained-head test changes concerning watch-only labels. Outside exhaustive extraction; context-only does not claim absence of institutional content.'}
screening=[]
for entry in packet['entries']:
    sid=entry['source_id']; us=[u for u in units if u['source_id']==sid]
    screening.append({'source_id':sid,'disposition':'candidate' if any(u['record_role']=='statement' for u in us) else ('empty' if not entry['text'].strip() else 'context_only'),
                      'reason':reasons[sid.removeprefix(PREFIX)],'unit_ids':[u['unit_id'] for u in us]})

annotation={'schema_version':'0.4','run_id':'F02_v04_r1','episode_id':'F02','packet_sha256':hashlib.sha256(packet_bytes).hexdigest(),
            'entry_screening':screening,'units':units,'relations':relations,
            'episode_summary':{'observed_outcomes':outcomes,'mechanisms':mechanisms,
                'missing_evidence':['Complete comment/body edit histories and reliable reply threading are unavailable.',
                                    'No pre-update reviewed patch identifies the exact newly added check for "*" that the author reports removing.',
                                    'No supplied institutional authorization, enforcement provision, or recurring socially expected practice supports upgrading these technical edit suggestions to a rule or established norm.',
                                    'No supplied outcome records for referenced #14411, #13075, #14023, or #14382, and no evidence of network adoption.',
                                    'Retained patches demonstrate final artifacts, not which review caused each change or the later merge.'],
                'unresolved_questions':['Which two changes does Both are good changes refer to, and which particular edit does fixed report?',
                                        'Which exact review-stage code check was removed, and is the claimed behavior equivalence independently valid?',
                                        'Do these case-specific technical recommendations express any recurring institutional expectation beyond voluntary local review? The supplied record does not decide.']}}

text=json.dumps(annotation,ensure_ascii=False,indent=2)+'\n'
(ROOT/'annotation.json').write_text(text)
freeze=ROOT/'annotation.first_complete.json'
if freeze.exists():
    raise RuntimeError('First-complete freeze already exists; do not overwrite it.')
freeze.write_text(text)
print(json.dumps({'first_complete_written': True,'entries':len(screening),'units':len(units),'statements':sum(u['record_role']=='statement' for u in units),'packet_sha256':annotation['packet_sha256']}))
