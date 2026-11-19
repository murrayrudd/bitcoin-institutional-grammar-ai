import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
packet = json.loads((ROOT / 'packet.json').read_text())
entries = {e['source_id']: e for e in packet['entries']}

def sid(short):
    return 'pr14441:' + short

def txt(short):
    return entries[sid(short)]['text']

def span(short, quote=None, start=0):
    text = txt(short)
    if quote is None:
        quote = text
    loc = text.index(quote, start)
    return {'start': loc, 'end': loc + len(quote), 'quote': quote}

def ev(short, quote=None, start=0):
    return {'source_id': sid(short), 'span': span(short, quote, start)}

def comp(symbol, text, evidence, basis='explicit', role='local', note=''):
    return {'symbol': symbol, 'text': text, 'basis': basis,
            'evidence': evidence, 'inference_note': note, 'occurrence_role': role}

def event(kind, target, basis, evidence, rationale):
    return {'kind': kind, 'target': target, 'basis': basis,
            'evidence': evidence, 'rationale': rationale}

units = []

def context(uid, short, quote=None, speech='reported_action', rationale='',
            alternative='', uncertainty='', confidence='clear', markup='plain'):
    u = {'unit_id': uid, 'source_id': sid(short), 'span': span(short, quote),
         'parent_unit_id': None, 'grammar': 'not_institutional',
         'speech_act': speech, 'scope': 'case_specific', 'components': [],
         'institution': {'type': 'not_applicable', 'standing': 'not_applicable',
                         'dispute_present': False, 'rationale': rationale,
                         'evidence': [], 'recognition': [], 'authority_evidence': []},
         'statement_target_level': 'not_applicable', 'observed_action_level': 'operational',
         'level_rationale': 'This occurrence is a contribution description, review act, or edit report within PR #14441; it does not itself prescribe a recurring arrangement.',
         'complexity_flags': ['unresolved_reference'] if uncertainty else ['none'],
         'alternative_interpretation': alternative, 'confidence': confidence,
         'uncertainty_reason': uncertainty, 'record_role': 'context',
         'parse_mode': 'literal', 'deontic_force': 'nondeontic',
         'level_alternatives': [], 'template_note': '',
         'presentation': {'quotation': 'none', 'markup': markup,
                          'rationale': 'The supplied occurrence is retained prose; no later edit or formatting history is inferred.'},
         'disposition_events': []}
    units.append(u)
    return u

meta_evidence = [ev('metadata', '"merged_at": "2018-11-10T11:46:02+00:00"'),
                 ev('metadata', '"merged": true')]
update_evidence = [ev('comments:0')]
review_evidence = [ev('reviews:4')]

def statement(uid, short, quote, components, rationale, parse, alternative,
              uncertainty, quotation='none', markup='plain', extra_evidence=None):
    own = ev(short, quote)
    u = {'unit_id': uid, 'source_id': sid(short), 'span': own['span'],
         'parent_unit_id': None, 'grammar': 'regulative', 'speech_act': 'proposed',
         'scope': 'case_specific', 'components': components,
         'institution': {'type': 'undetermined', 'standing': 'text_only',
                         'dispute_present': False, 'rationale': rationale,
                         'evidence': [own] + (extra_evidence or []),
                         'recognition': [
                             event('reported_implementation', 'broader_proposal', 'explicit', update_evidence,
                                   'jnewbery attributes a PR update to ryanofsky\'s changes. The report is broad; it does not individually verify this recommendation or its exact wording.'),
                             event('endorsement', 'broader_proposal', 'explicit', review_evidence,
                                   'ryanofsky gives a revision-specific utACK and describes the intervening changes in aggregate. This endorses the contribution at that revision, not a recognized obligation to follow this request.'),
                             event('recorded_status', 'broader_proposal', 'explicit', meta_evidence,
                                   'The metadata records integration of PR #14441. It does not establish adoption of every suggestion or a governance expectation.')],
                         'authority_evidence': []},
         'statement_target_level': 'operational', 'observed_action_level': 'operational',
         'level_rationale': 'The focal action is an edit to this contribution during review. No recurring review procedure, allocation of decision powers, or foundation of authority is being proposed.',
         'complexity_flags': ['unresolved_reference'],
         'alternative_interpretation': alternative,
         'confidence': 'plausible', 'uncertainty_reason': uncertainty,
         'record_role': 'statement', 'parse_mode': parse, 'deontic_force': 'recommendation',
         'level_alternatives': [], 'template_note': '',
         'presentation': {'quotation': quotation, 'markup': markup,
                          'rationale': ('The reviewer introduces newly drafted replacement wording. Its technical clauses specify the suggested edit; they are not repeated quotations or separate institutional rules.' if quotation == 'proposed_wording' else 'The supplied review suggestion is plain prose, including any inline code; no withdrawal or formatting change is evidenced.')},
         'disposition_events': [
             event('reported_implemented', 'broader_proposal', 'explicit', update_evidence,
                   'The author reports incorporating the reviewer\'s changes into the PR, without individually enumerating this proposition.'),
             event('recorded_merged', 'broader_proposal', 'explicit', meta_evidence,
                   'The recorded merge concerns PR #14441. Its scope is not silently promoted to exact implementation of this recommendation.')]
         }
    units.append(u)
    return u

context('C01', 'body', speech='technical_description',
        rationale='The body describes a backport to v0.17, partial reversions, and an asserted issue fix. It supplies no independently stated instruction, personal prospective strategy, or institutional definition.',
        alternative='Opening a PR can function as an implicit integration proposal, but the supplied body alone does not articulate a separate institutional prescription. The referenced PRs and issue are separate objects, with no supplied outcomes.')
context('C02', 'comments:0',
        rationale='This is an attributable broad report of an update in response to ryanofsky, not a prescription or recognition that review suggestions are obligatory.')
context('C03', 'comments:1',
        rationale='A revision-specific utACK is a review act. It does not state authority or a duty to integrate.')
context('C04', 'comments:2',
        rationale='The utACK and technical comparison with other backports describe this contribution. The comparison does not direct a future backport procedure.',
        alternative='The explanation may justify reviewing a backport on functional rather than textual similarity, but it does not express that as a general expectation.')
context('C05', 'reviews:0',
        rationale='An attributable utACK of c8d1f1513fb39d80cebbc32e1b5327209485e085 is a review act, not a separate permission or obligation.')
context('C06', 'reviews:4',
        rationale='This is a later utACK of 89306ab0df93bfdf5630910bc20b1eccb7379172 plus a report about changes since the last review. No requirement for renewed approval is stated.')

actor_note = ('The review proposes an edit for the person updating this PR. The addressee is not named in the suggestion. '
              'jnewbery\'s later update report supports identifying the PR updater as a likely performer, but neither an occupational role nor a duty is inferred.')
def actor(short, quote):
    return comp('A', 'person updating this PR (jnewbery is the contextually supported likely addressee)',
                [ev(short, quote), ev('comments:0', "I've updated the PR with your changes.")],
                basis='context_inferred', role='semantic_inference', note=actor_note)

q0 = txt('review_comments:0')
s1 = statement('S01', 'review_comments:0', q0,
    [actor('review_comments:0', q0),
     comp('D', 'Should', [ev('review_comments:0', 'Should')]),
     comp('I', 'correct', [ev('review_comments:0', q0)], 'context_inferred', 'semantic_inference',
          'The source states the desired spelling with be; the editing action correct is reconstructed from the inline review. The word be is not mislabeled as an explicit edit verb.'),
     comp('Bdir', 'the RPC spelling in the release notes', [ev('review_comments:0', q0)], 'context_inferred', 'semantic_inference',
          'The target of correction is inferred from the desired spelling and the supplied doc/release-notes.md path. The predicate complement listtransactions is not an explicit direct object of correct.'),
     comp('Bdir,p', '`listtransactions` with `s`', [ev('review_comments:0', '`listtransactions` with `s`')], 'context_inferred', 'semantic_inference',
          'The exact proposed spelling is supplied, but its role as a requested property of the edited name is reconstructed under correct. The trailing s qualification is retained.')],
    'A one-off spelling recommendation in review is institutionally plausible as contribution coordination, but the supplied text does not establish an authorized rule or a socially recognized expectation. Its text-only status survives the later broad update and ACK.',
    'pragmatic',
    'Literally this is an assertion of the correct RPC spelling, with technical rather than institutional force. The selected parse retains its pragmatic editing request, without treating it as a constitutive definition.',
    'The exact original misspelling and comment-thread target are not supplied; the edit action and addressee are inferred.')

reason1 = "This paragraph doesn't really make sense when both behaviors are present in the same release."
context('C07', 'review_comments:1', reason1, speech='technical_description',
        rationale='This evaluative rationale explains why the proposed release-note paragraph is relevant; the following clause already supplies the single edit request. It is not counted again as a separate request.')
q1 = txt('review_comments:1')[txt('review_comments:1').index("I'd maybe"):]
replacement1 = q1[q1.index('to:'):]
s2 = statement('S02', 'review_comments:1', q1,
    [actor('review_comments:1', "I'd maybe change it to:"),
     comp('I', 'change', [ev('review_comments:1', 'change', txt('review_comments:1').index("I'd maybe"))]),
     comp('Bdir', 'it', [ev('review_comments:1', 'it', txt('review_comments:1').index('change it') + len('change '))],
          note='Even in the pragmatic recommendation parse, it remains the explicit object of change. This paragraph in the preceding rationale resolves its referent; it is not transformed from a subject into an object.'),
     comp('Cex', replacement1, [ev('review_comments:1', replacement1)],
          note='The to-complement specifies the proposed replacement. Both configuration branches and the explanation concerning spending from accounts versus labels qualify the edit content. They do not activate an obligation on RPC users.')],
    'The reviewer tentatively offers a replacement paragraph for this PR. This is an editorial recommendation without supplied authorization or recognition of a general duty; an undetermined institutional type preserves that boundary.',
    'pragmatic',
    'The literal I\'d maybe clause can be read as the reviewer\'s hypothetical personal choice. The response context supports a recommendation to the PR updater; it does not establish a committed personal plan. The proposed paragraph itself describes technical behavior.',
    'The intended performer is inferred from the review exchange. The existing paragraph and complete reply threading are unavailable. Maybe makes the wording tentative.',
    quotation='proposed_wording', markup='mixed', extra_evidence=[ev('review_comments:1', reason1)])

reason2 = 'I don\'t see how the new check for "*" here changes anything.'
context('C08', 'review_comments:2', reason2, speech='technical_description',
        rationale='The reviewer states uncertainty about a technical check as the reason for the following tentative removal recommendation. This is not an institutional sanction or a separate requirement.')
q2 = "Maybe drop for clarity (unless I'm missing something)."
s3 = statement('S03', 'review_comments:2', q2,
    [actor('review_comments:2', q2),
     comp('I', 'drop', [ev('review_comments:2', 'drop')]),
     comp('Bdir', 'the new check for "*" here', [ev('review_comments:2', 'the new check for "*" here')],
          'context_inferred', 'context_reference',
          'Drop omits its object. The preceding sentence supplies the new check for "*" here as the antecedent; its role as the object of drop is inferred, although the words are explicit in the rationale. The source path is src/wallet/rpcwallet.cpp.'),
     comp('Cex', 'for clarity', [ev('review_comments:2', 'for clarity')],
          note='This is the stated purpose of removal, not a separate activation condition.'),
     comp('Cac', "unless I'm missing something", [ev('review_comments:2', "unless I'm missing something")],
          note='The reviewer expressly makes the recommendation defeasible if their understanding overlooks a relevant effect. This uncertainty qualification is retained rather than converted into unconditional removal.')],
    'The reviewer tentatively recommends a case-specific code simplification. The author\'s later agreement and removal report support uptake of the edit, not an institutionally recognized obligation. No authority or sanction is supplied.',
    'literal',
    'This may be ordinary technical advice rather than an institutional expectation. The unless clause can alternatively be represented as an epistemic qualification on recommendation force, so long as its defeasibility survives. Maybe is a hedge, not an explicit duty modal.',
    'The original intermediate check and complete patch chronology are absent. Its referent is inferred from the immediately preceding sentence and specifically echoed by the author.',
    extra_evidence=[ev('review_comments:2', reason2)])
reply = ev('review_comments:6')
s3['institution']['recognition'].insert(0, event('response', 'this_proposition', 'context_inferred',
    [ev('review_comments:2'), reply],
    'The author agrees that the check for "*" has no behavioral effect. Shared check identity and matching file path resolve the response to this recommendation despite absent reliable reply threading. Agreement with a technical claim is not expectation recognition.'))
s3['institution']['recognition'].insert(1, event('reported_implementation', 'this_proposition', 'context_inferred',
    [ev('review_comments:2'), reply],
    'The author explicitly reports removal of it immediately after identifying the check for "*". The match to this particular recommendation is contextually inferred; the exact code change is not independently verified.'))
s3['disposition_events'].insert(0, event('accepted', 'this_proposition', 'context_inferred',
    [ev('review_comments:2'), reply],
    'No, you\'re right and It\'s better without accept the technical removal suggestion, with the same check identified. This is agreement on an edit, not recognition of a binding expectation.'))
s3['disposition_events'].insert(1, event('reported_implemented', 'this_proposition', 'context_inferred',
    [ev('review_comments:2'), reply],
    'The author reports I\'ve removed it; the preceding explicit check reference resolves it to the suggested check. Retained-head code alone does not provide the missing intermediate diff.'))

q3 = txt('review_comments:3')
replacement3 = q3[q3.index('Maybe:'):]
s4 = statement('S04', 'review_comments:3', q3,
    [actor('review_comments:3', "I think it'd be good to document the empty string change."),
     comp('I', 'document', [ev('review_comments:3', 'document')]),
     comp('Bdir', 'the empty string change', [ev('review_comments:3', 'the empty string change')],
          note='The empty string change remains the explicit object of document in the pragmatic recommendation. The quoted draft explains what the change concerns; this object role is not reconstructed from a subject or predicate complement.'),
     comp('Cex', replacement3, [ev('review_comments:3', replacement3)],
          note='Maybe introduces optional proposed wording for the documentation. It preserves the accounts-mode condition, the empty string label, the unlabeled-transactions result, the error without the setting, and the usefulness/confusion rationale. Those are technical content of the edit, not conditions on whether contributors may document it.')],
    'This is a tentative recommendation to add explanatory documentation to this contribution. It supplies no rule authority or recognized documentation obligation; a technical editorial request remains undetermined with text-only standing.',
    'pragmatic',
    'The first sentence can literally be an evaluation of desirable documentation rather than a request. The surrounding inline-review exchange supports the recommendation parse. The following draft describes technical capability and error behavior; possible and error do not constitute institutional permission or sanction.',
    'The addressee is inferred, and the proposed wording is tentative. Broad reports and the retained head can support correspondence without establishing a generally shared expectation.',
    quotation='proposed_wording', markup='mixed')

context('C09', 'review_comments:4',
        rationale='The author positively assesses two changes. This is an endorsement act, not an institutional prescription.',
        alternative='Both plausibly refers to two release-note suggestions, but three supplied suggestions concern that file. Source order and timestamps do not establish reliable reply threading.',
        uncertainty='The exact pair denoted by Both is unresolved. It is not allocated as proposition-specific recognition or acceptance of any particular pair.', confidence='unresolved')
context('C10', 'review_comments:5',
        rationale='This is a report of a fix with no stated object; it is not a prescription.',
        alternative='The spelling correction is a plausible target, but the same path contains multiple suggestions and no reliable thread mapping is supplied.',
        uncertainty='The object of fixed is unresolved. This report is not assigned to a particular recommendation or used as exact implementation evidence.', confidence='unresolved')
context('C11', 'review_comments:6',
        rationale='The author agrees about the technical check and reports its removal. The text supports technical uptake, not a duty to comply with reviewers.',
        alternative='The no opening answers the reviewer\'s caveat about missing something. It does not reject the removal recommendation.')

relations = []
def rel(fr, to, typ, evidence, rationale, basis='context_inferred'):
    relations.append({'from_unit_id': fr, 'to_unit_id': to, 'type': typ, 'basis': basis,
                      'rationale': rationale, 'evidence': evidence, 'logic_scope': 'not_applicable'})

rel('C07', 'S02', 'clarifies', [ev('review_comments:1')],
    'The preceding criticism explains why the offered replacement distinguishes both behaviors within the same release. Adjacency and semantic fit establish a contextual rationale, not a separate prescriptive layer.')
rel('C08', 'S03', 'clarifies', [ev('review_comments:2')],
    'The uncertainty about the new check supplies the antecedent and reason for the tentative removal request.')
for uid, short in [('S01', 'review_comments:0'), ('S02', 'review_comments:1'), ('S04', 'review_comments:3')]:
    rel(uid, 'C02', 'uptake', [ev(short), ev('comments:0')],
        'The author reports updating the PR with this reviewer\'s changes. This links the recommendation to a broader response only; it does not verify the individual edit or disambiguate Both or fixed.')
rel('S03', 'C11', 'uptake', [ev('review_comments:2'), ev('review_comments:6')],
    'The shared check for "*" and the author\'s explicit removal report support a proposition-specific response. The source lacks reliable thread IDs, so target correspondence is context_inferred.')
rel('C06', 'C05', 'review_target_update', [ev('reviews:4'), ev('reviews:0')],
    'The same reviewer gives a new revision-specific utACK and refers to the last review. The earlier supplied utACK is the recoverable prior target, with correspondence inferred from authorship, timestamps, and the relative reference. No change in judgment or compulsory reapproval is asserted.')

reasons = {
 'body': 'Exhaustive focal screening: descriptive backport, partial-reversion, and issue-fix claims; no separately expressed prescription or institutional configuration. Referenced PRs retain distinct identities.',
 'comments:0': 'Exhaustive focal screening: broad author update report and thanks, not a new prescription or recognized obligation.',
 'comments:1': 'Exhaustive focal screening: revision-specific utACK review act, without a separate rule or integration instruction.',
 'comments:2': 'Exhaustive focal screening: utACK and technical explanation of this backport; no directive to use a recurring backport procedure.',
 'reviews:0': 'Exhaustive focal screening: attributable utACK; metadata APPROVED does not by itself supply authority or a prescription.',
 'reviews:1': 'Empty supplied review body; COMMENTED metadata is not substituted for a speech statement.',
 'reviews:2': 'Empty supplied review body; COMMENTED metadata is not substituted for a speech statement.',
 'reviews:3': 'Empty supplied review body; COMMENTED metadata is not substituted for a speech statement.',
 'reviews:4': 'Exhaustive focal screening: later revision-specific utACK and report of intervening edits, not a requirement for reapproval.',
 'review_comments:0': 'Exhaustive focal screening: an elliptical spelling correction is retained as a pragmatic edit recommendation; technical-correctness alternative preserved.',
 'review_comments:1': 'Exhaustive focal screening: one paragraph-replacement recommendation with complete tentative wording and a separate rationale context. Technical configuration clauses are content of the proposed edit, not further institutional propositions.',
 'review_comments:2': 'Exhaustive focal screening: one removal recommendation retains its clarity purpose and unless caveat; preceding technical uncertainty is context.',
 'review_comments:3': 'Exhaustive focal screening: one documentation recommendation includes tentative replacement text and all technical qualifications; technical capability/error descriptions are not permissions or sanctions.',
 'review_comments:4': 'Exhaustive focal screening: two-change positive response with unresolved targets; no new prescription and no specific expectation recognition.',
 'review_comments:5': 'Exhaustive focal screening: fixed is an implementation report with unresolved object, not a new prescription.',
 'review_comments:6': 'Exhaustive focal screening: agreement and specific removal report; No addresses the doubt about a missed technical effect, not rejection of the recommendation.',
 'metadata': 'Supplement screened as context under selection_design: status and file-change metadata support outcomes, not speech. Context-only treatment is not a finding that supplemental material cannot have institutional significance.',
 'supplement_metadata': 'Supplement screened as context under selection_design: retained PR base, head, and merge metadata corroborate object/revision identity and integration; no exhaustive institutional extraction is claimed.',
 'patch:0': 'Supplement screened as context under selection_design: retained release-note patch corroborates plural spelling and both documentation topics. This is not a full revision chronology or evidence that review caused the retained text.',
 'patch:1': 'Supplement screened as context under selection_design: retained RPC code/help patch contains technical conditionals, argument guidance, and error text. These are not exhaustively extracted as institutions; their technical must/should wording is not itself authority evidence.',
 'patch:2': 'Supplement screened as context under selection_design: retained functional-test changes describe executable technical checks. No exhaustive institutional extraction of supplemental code is claimed.',
 'patch:3': 'Supplement screened as context under selection_design: retained listtransactions test changes supply technical context. Context-only screening is not a claim of no possible institutional content.'
}
screening = []
for e in packet['entries']:
    found = [u for u in units if u['source_id'] == e['source_id']]
    disposition = 'candidate' if any(u['record_role'] == 'statement' for u in found) else ('empty' if not e['text'].strip() else 'context_only')
    screening.append({'source_id': e['source_id'], 'disposition': disposition,
                      'reason': reasons[e['source_id'].split(':', 1)[1]], 'unit_ids': [u['unit_id'] for u in found]})

patch0 = txt('patch:0')
patch_doc = patch0[patch0.index('+`listtransactions` label support'):patch0.index('\n \n Credits')]
summary = {
 'observed_outcomes': [
   {'claim': 'jnewbery reports updating PR #14441 with ryanofsky\'s changes. This is an attributable broad implementation report, not individual verification of every suggested edit.', 'evidence': [ev('comments:0')]},
   {'claim': 'After the suggestion to drop the new check for "*" for clarity, jnewbery agrees that behavior is identical with or without it and reports removal. The report supports a specific response but does not supply the missing intermediate code diff.', 'evidence': [ev('review_comments:2'), ev('review_comments:6')]},
   {'claim': 'The retained release-note patch contains the plural listtransactions heading and text documenting both deprecated-accounts-mode transaction behavior and the empty-string behavior in each configuration. This establishes the retained documentation, not runtime validation or the causal origin of the wording.', 'evidence': [ev('patch:0', patch_doc)]},
   {'claim': 'ryanofsky records utACKs for c8d1f1513fb39d80cebbc32e1b5327209485e085 and later 89306ab0df93bfdf5630910bc20b1eccb7379172, describing the intervening changes as code simplification and suggested release-note updates. The packet does not establish a duty to repeat review.', 'evidence': [ev('reviews:0'), ev('reviews:4')]},
   {'claim': 'The supplied metadata records PR #14441 merged on 2018-11-10 into the 0.17 base, with retained head and merge commit 89306ab0df93bfdf5630910bc20b1eccb7379172. This is repository integration of this contribution; outcomes for the other referenced PRs and network adoption are not established.',
    'evidence': [ev('supplement_metadata', '"number": 14441'), ev('supplement_metadata', '"merged": true'), ev('supplement_metadata', '"base": "0.17"'), ev('supplement_metadata', '"head_sha": "89306ab0df93bfdf5630910bc20b1eccb7379172"'), ev('supplement_metadata', '"merge_commit_sha": "89306ab0df93bfdf5630910bc20b1eccb7379172"'), ev('supplement_metadata', '"merged_at": "2018-11-10T11:46:02Z"')]}
 ],
 'mechanisms': [
   {'category': 'reason_giving',
    'claim': 'The reviewer questions whether the new check for "*" changes behavior and recommends dropping it for clarity unless something has been missed. The author responds that behavior would be identical and reports removing the check. This is a supported textual sequence of technical reason-giving and a reported edit, without establishing a binding expectation or sanction.',
    'evidence': [ev('review_comments:2'), ev('review_comments:6')],
    'unit_ids': ['C08', 'S03', 'C11'],
    'alternative_explanation': 'The author could independently have recognized redundancy. The supplied report and matching subject support correspondence, but the missing intermediate diff prevents independent reconstruction of the edit and does not establish causal necessity.',
    'status': 'supported_sequence'},
   {'category': 'review_coordination',
    'claim': 'Four supplied review suggestions concern RPC spelling, a configuration-sensitive release-note paragraph, dropping a possibly redundant check, and documenting the empty-string change. The author reports updating the PR with the reviewer\'s changes. The same reviewer subsequently utACKs a new revision and identifies code simplification and release-note changes since the last review. This supports coordination through suggestions, an update report, and revision-specific review; it does not establish mandatory reapproval or exact implementation of all four recommendations.',
    'evidence': [ev('review_comments:0'), ev('review_comments:1'), ev('review_comments:2'), ev('review_comments:3'), ev('comments:0'), ev('reviews:0'), ev('reviews:4')],
    'unit_ids': ['S01', 'S02', 'S03', 'S04', 'C02', 'C05', 'C06'],
    'alternative_explanation': 'These may be voluntary technical exchanges rather than manifestations of a recognized governance expectation. The broad author report and later ACK do not assign exact wording to each response, establish a necessary sequence for integration, or resolve the standalone Both and fixed replies.',
    'status': 'supported_sequence'}
 ],
 'missing_evidence': [
   'No reliable reply threading or complete edit history is supplied. The exact targets of Both are good changes and fixed remain unresolved.',
   'The retained head patches are not the complete revision chronology. The original paragraph, exact original misspelling, and intermediate new check under review are not reconstructed from unseen versions.',
   'No institutional authorization, enforcement provision, obligation-recognition event, or attributed maintainer role is supplied. ACKs and the merged_by field do not fill those gaps.',
   'The packet supplies no cross-episode recognition establishing a recurring arrangement, and no evidence of constitutional or epistemic governance.',
   'The packet does not establish outcomes for PRs #14411, #13075, #14023, or issue #14382, nor runtime results or Bitcoin-network adoption.'
 ],
 'unresolved_questions': [
   'Which two changes does Both refer to, and what exact target is fixed?',
   'What exact intermediate code check was removed, and which revisions first incorporated each individual edit?',
   'Were any of these suggestions recognized as an expectation beyond this voluntary technical exchange?'
 ]
}

annotation = {'schema_version': '0.3', 'run_id': 'F02_v03_r2', 'episode_id': 'F02',
              'packet_sha256': hashlib.sha256((ROOT / 'packet.json').read_bytes()).hexdigest(),
              'entry_screening': screening, 'units': units, 'relations': relations,
              'episode_summary': summary}
encoded = json.dumps(annotation, ensure_ascii=False, indent=2) + '\n'
(ROOT / 'annotation.json').write_text(encoded)
with (ROOT / 'annotation.first_complete.json').open('x') as f:
    f.write(encoded)
print(json.dumps({'units': len(units), 'statements': sum(u['record_role'] == 'statement' for u in units), 'screened': len(screening), 'packet_sha256': annotation['packet_sha256']}))
