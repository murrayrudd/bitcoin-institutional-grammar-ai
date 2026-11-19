import json, hashlib, copy
from pathlib import Path
from collections import Counter
base=Path.cwd()
frozen=['annotation.json','review_notes.json','checks.json','repair_log.json']
before={f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in frozen}
old=json.loads(Path('annotation.json').read_text());a=copy.deepcopy(old)
p=json.loads(Path('packet_v2.json').read_text());p1=json.loads(Path('packet.json').read_text());addition=json.loads(Path('context_completion.json').read_text());prov=json.loads(Path('context_completion_provenance.json').read_text())
assert p['entries'][:-1]==p1['entries'] and p['entries'][-1]==addition
assert p['selection_design']==p1['selection_design']
txt={e['source_id']:e['text'] for e in p['entries']}; us={u['unit_id']:u for u in a['units']}
def ev(s,q,start=0):
 i=txt[s].index(q,start);return {'source_id':s,'span':{'start':i,'end':i+len(q),'quote':q}}
a['run_id']='R4_C_source_first_supplemented';a['packet_sha256']=hashlib.sha256(Path('packet_v2.json').read_bytes()).hexdigest()
qvalue='The technical content of those review comments is what matters, not how many are registered in what category.'
qvote='The goal is *not* to have everyone "register" their "vote".'
qoverview="It is simply a best-effort overview to have a clickable link to every reviewer's most recent review comment."
qclass='When a comment contains both `ack` and `nack` (in uppercase), the bot just picks one.'
qcomplaint='drahtbot has categorized your comment as nack instead of ack'

u=us['C115_merit'];u['institution']['standing']='locally_supported'
u['institution']['evidence'].append(ev('32406-169',qvalue))
u['institution']['recognition'].append({'kind':'expectation_recognition','target':'this_proposition','basis':'context_inferred','evidence':[ev('32406-169',qvalue),ev('32406-169',qvote)],'rationale':'maflcko explicitly states the general expectation that technical content, rather than counts of categorized review signals, matters. This is attributable recognition of the focal content-over-count criterion within the supplied multithread episode, not a direct reply to glozow or proof of actual weighting. The source contrasts category counts whereas the focal sentence contrasts repeated postings; that bounded application difference remains explicit.'})
u['institution']['rationale']='The assertion expresses a general review-evaluation expectation. Added source 32406-169 independently and attributably recognizes technical content over counts of categorized signals, supporting local recognition of the same criterion. This does not verify each actual weighting decision or establish an authorized rule. D_CONTRIB supplies compatible discretionary merit-weighting documentation. Repeatedly-supported standing is not inferred from two PR numbers alone without a separately established cross-episode recognition chain.'
u['confidence']='plausible'
u['uncertainty_reason']='The recognition concerns technical content versus category counts; the focal wording concerns merit versus repeated postings. The shared content-over-count criterion is supported, while exact treatment of repetition, actual decision weights, and a direct response to glozow are not established.'
u['alternative_interpretation']+=' A stricter proposition-identity reading can keep text_only standing and classify the added recognition as broader_proposal because category counts and repeated postings are different quantities. The chosen local-recognition reading treats that as a bounded application difference within the expressed general merit-over-count criterion.'

u=us['C115_forum']
u['institution']['evidence'] += [ev('32406-169',qvote),ev('32406-169',qoverview)]
u['institution']['recognition'].append({'kind':'expectation_recognition','target':'broader_proposal','basis':'context_inferred','evidence':[ev('32406-169',qvote),ev('32406-169',qoverview)],'rationale':'The later source recognizes the broader non-voting review arrangement by explaining the purpose of the bot summary on PR 32406. It does not explicitly characterize this particular PR 32359 forum, so this case-specific statement remains text_only rather than locally_supported.'})
u['institution']['rationale']+=' The source-only supplement recognizes a compatible non-voting purpose for the PR 32406 review summary. Its different immediate referent supplies broader-arrangement support without establishing proposition-specific recognition of this PR 32359 forum.'

u=us['C165_fixed']
u['alternative_interpretation']='The later classification explanation in 32406-169 concerns comments containing both ACK and NACK. The earlier quoted question concerns the bot not updating; the supplied text does not establish that these are the same malfunction or that fixed refers to the classification behavior.'
u['institution']['evidence'] += [ev('32406-164',"Did the NACK/ACK bot break? Doesn't seem to be updating? @DrahtBot"),ev('32406-169',qclass)]
u['uncertainty_reason']+=' Source 32406-169 explains a classification limitation but does not timestamp, verify, or expressly contradict the earlier updating repair report.'

u=us['C227_majority']
u['institution']['evidence'] += [ev('32406-169',qvote),ev('32406-169',qvalue)]
u['institution']['rationale']+=' Added source 32406-169 makes the bot-summary purpose explicitly non-voting and values technical content over category totals. It is not a direct reply to this majority claim and does not resolve whether winner means a merge decision, adoption, or rhetorical success.'
u['alternative_interpretation']+=' If majority refers specifically to a bot tally of ACK/NACK categories, the added explanation is contrary evidence about that tally\'s declared purpose. That conditional contrast does not establish what the original author meant.'

# Necessary context endpoints only: supporting entries remain outside exhaustive extraction.
def context(uid,s,q,role='context',speech='asserted',quotation='none',rationale=''):
 u={'unit_id':uid,**ev(s,q),'parent_unit_id':None,'record_role':role,'grammar':'not_institutional','speech_act':speech,'scope':'case_specific','parse_mode':'literal','deontic_force':'nondeontic','components':[],
 'institution':{'type':'not_applicable','standing':'not_applicable','dispute_present':False,'rationale':rationale,'evidence':[],'recognition':[],'authority_evidence':[]},
 'statement_target_level':'not_applicable','observed_action_level':'operational','level_rationale':'Operational review-tool discussion; this supporting endpoint is not exhaustively component-coded.','level_alternatives':[],'complexity_flags':['none'],'alternative_interpretation':'','confidence':'clear','uncertainty_reason':'','presentation':{'quotation':quotation,'markup':'plain','rationale':'The quotation is repeated from the supplied complaint; the reply span is prose inside the source details block. No edit-history inference.'},'disposition_events':[]}
 a['units'].append(u);return u
context('C166_classification_complaint','32406-166',qcomplaint,rationale='Supporting context outside focal extraction scope; original complaint endpoint for the source added in this supplement. The current source attributes this report to delta1, addressing gmaxwell.')
context('C169_quote','32406-169',qcomplaint,role='quotation',quotation='repeated',rationale='Exact repeated complaint from C166_classification_complaint; it is not a second complaint or endorsement.')
reply=txt['32406-169'].split('\r\n\r\n')[2]
assert reply.startswith(qclass)
context('C169_reply','32406-169',reply,rationale='Supporting context outside focal extraction scope; maflcko explains the categorization behavior and the purpose of the review summary. Technical behavior and institutional-purpose assertions remain attributable claims; neither actual code behavior nor authoritative status is independently established.')
a['relations'] += [
{'from_unit_id':'C169_quote','to_unit_id':'C166_classification_complaint','type':'quotes','basis':'explicit','evidence':[ev('32406-169',qcomplaint),ev('32406-166',qcomplaint)],'rationale':'The added source repeats the supplied categorization complaint exactly, without its addressee prefix.','logic_scope':'not_applicable'},
{'from_unit_id':'C166_classification_complaint','to_unit_id':'C169_reply','type':'uptake','basis':'explicit','evidence':[ev('32406-169',qcomplaint),ev('32406-169',qclass)],'rationale':'The exact quoted complaint receives an explanation of how a comment containing both uppercase categories is classified. The response is not a reported repair or endorsement of voting.','logic_scope':'not_applicable'}]
for sc in a['entry_screening']:
 if sc['source_id']=='32406-166':
  sc['unit_ids']=['C166_classification_complaint'];sc['reason']='Supporting context outside focal extraction scope; necessary original complaint endpoint added for the exact quotation and response in the source-only supplement.'
a['entry_screening'].append({'source_id':'32406-169','disposition':'context_only','reason':'Supporting context outside focal extraction scope; screened for the quoted complaint, explanation of category selection, non-voting summary purpose, content-over-count expectation, and lack of a verified repair. Necessary quotation and reply endpoints retained; the source is not exhaustively component-coded.','unit_ids':['C169_quote','C169_reply']})

summary=a['episode_summary']
summary['observed_outcomes'][0]={'claim':'The bot reply in 32406-165 identifies a known issue, gives an issue-51 referral, and carries an edit reporting fixed after quoting an updating complaint. The added 32406-169 responds to a separate categorization complaint and explains that a comment containing both uppercase ACK and NACK receives one category. It does not verify, date, or expressly contradict the earlier repair report.','evidence':[ev('32406-165',"Did the NACK/ACK bot break? Doesn't seem to be updating? @DrahtBot"),ev('32406-165','This is a known issue. See https://github.com/maflcko/DrahtBot/issues/51. edit: fixed'),ev('32406-169',qcomplaint),ev('32406-169',qclass)]}
summary['mechanisms'][0]['claim']+=' A separate categorization complaint is quoted in the added source and receives a category-selection explanation, followed by clarification that the summary supplies links to recent reviews rather than registering votes. These are two attributable response sequences; the record does not show that the clarification resulted from the earlier repair.'
summary['mechanisms'][0]['evidence'] += [ev('32406-166',qcomplaint),ev('32406-169',qcomplaint),ev('32406-169',qclass),ev('32406-169',qvote),ev('32406-169',qoverview)]
summary['mechanisms'][0]['unit_ids'] += ['C166_classification_complaint','C169_quote','C169_reply']
summary['mechanisms'][0]['alternative_explanation']+=' The updating failure and mixed-category classification may concern distinct behaviors; the word fixed cannot be assigned to both without further evidence.'
summary['mechanisms'][3]['claim']+=' The added reply explains the bot summary as non-voting and explicitly prioritizes technical content over category totals, giving attributable recognition of a compatible general criterion. It does not identify the intended decision domain of aryaethn\'s majority claim.'
summary['mechanisms'][3]['evidence'] += [ev('32406-169',qvote),ev('32406-169',qvalue)]
summary['unresolved_questions'].append('Does the general merit-over-count criterion count as the same proposition when one statement contrasts repeated posts and the other category totals? Local recognition is selected with the stricter broader-proposal alternative recorded.')

# Preserve a complete auditable difference inventory, using only this review's original output.
orig_units={u['unit_id']:u for u in old['units']};now_units={u['unit_id']:u for u in a['units']}
changed={uid:[k for k in now_units[uid] if now_units[uid][k]!=orig_units[uid][k]] for uid in orig_units if now_units[uid]!=orig_units[uid]}
new_ids=[uid for uid in now_units if uid not in orig_units]
assert set(changed)=={'C115_merit','C115_forum','C165_fixed','C227_majority'}
for uid in orig_units:
 for key in ['span','record_role','grammar','speech_act','scope','parse_mode','deontic_force','components','statement_target_level','observed_action_level']:
  assert orig_units[uid][key]==now_units[uid][key],(uid,key)
counts={'screened_entries':len(a['entry_screening']),'focal_records':len(p['selection_design']['focal_source_ids']),'total_units':len(a['units']),'statement_units':sum(u['record_role']=='statement' for u in a['units']),'focal_statement_units':sum(u['record_role']=='statement' and u['source_id'] in p['selection_design']['focal_source_ids'] for u in a['units']),'role_counts':dict(Counter(u['record_role'] for u in a['units'])),'relations':len(a['relations'])}
report={
'run_id':a['run_id'],'episode_id':a['episode_id'],'supplement_source_id':'32406-169','original_packet_sha256':old['packet_sha256'],'supplemented_packet_sha256':a['packet_sha256'],
'scope':'Source-only context completion, restricted to the added original source and focal interpretations it bears on. No baseline annotation, other review, or narrative conclusion was inspected. The eight focal records and their source text are unchanged.',
'packet_integrity':{'original_entries_unchanged':True,'focal_selection_unchanged':True,'one_added_context_entry_matches_completion':True,'provenance_hash_matches':a['packet_sha256']==prov['amended_packet_sha256']},
'counts':counts,'changed_existing_unit_ids':list(changed),'changed_top_level_fields_by_unit':changed,'new_context_or_quotation_unit_ids':new_ids,'new_statement_units':0,
'changes':[
{'unit_id':'C115_merit','decision':'Change standing from text_only to locally_supported, add attributable expectation_recognition targeted at this_proposition, and preserve the bounded alternative. No grammatical component, force, scope, or governance-level change.','rationale':'Both statements explicitly prioritize the substance of review over a numeric tally. The added source names technical content and category counts, while the focal unit names argument merit and repeated postings. This supplies recognition of the general criterion, not verification of actual weights or acceptance of every application. No direct reply to glozow or cross-episode chain is inferred.','evidence':[ev('32359-115','Reviews are weighted by the merit of their arguments, not the number of times they are posted.'),ev('32406-169',qvalue)],'reasonable_alternative':'A strict exact-application reading could retain text_only and use broader_proposal recognition because the quantities compared differ. That alternative is recorded in the supplemented unit.'},
{'unit_id':'C115_forum','decision':'Add broader-arrangement recognition and evidence; retain text_only standing and case-specific operational coding.','rationale':'The added non-voting claim concerns the bot summary in PR 32406. It supports a compatible arrangement, but does not explicitly characterize this PR 32359 forum.','evidence':[ev('32359-115','this is a pull request open for code review, not a per-username voting forum.'),ev('32406-169',qvote),ev('32406-169',qoverview)]},
{'unit_id':'C165_fixed','decision':'Refine the interpretation and add evidence; retain context role, reported_action, and all classification fields.','rationale':'The earlier quoted question asks whether the bot stopped updating; the new reply explains mixed-ACK/NACK categorization. Fixed is not shown to cover both, and the update timestamp remains absent.','evidence':[ev('32406-164',"Did the NACK/ACK bot break? Doesn't seem to be updating? @DrahtBot"),ev('32406-165','edit: fixed'),ev('32406-169',qclass)]},
{'unit_id':'C227_majority','decision':'Add the contrary bot-purpose context and bounded interpretation; retain text_only, unknown target level, and dispute_present=false.','rationale':'The added source is contrary to interpreting bot totals as an intended voting mechanism, but it neither quotes the majority statement nor identifies what winner means. Its different target does not establish a direct challenge to this focal proposition.','evidence':[ev('32359-227','Only the majority decides the winner.'),ev('32406-169',qvote),ev('32406-169',qvalue)]},
{'unit_ids':new_ids,'decision':'Add two supporting context units and one repeated quotation with quotes and uptake relations.','rationale':'The exact repetition establishes the recipient complaint of maflcko\'s added reply. The source\'s broader institutional claims remain available as evidence without exhaustive supporting-entry coding.','evidence':[ev('32406-166',qcomplaint),ev('32406-169',qcomplaint),ev('32406-169',qclass)]}
],
'justified_nonchanges':[
{'unit_ids':['C165_referral','C165_known','C165_quote','C164_question'],'decision':'No change to the issue referral, known-issue statement, repeated updating question, or original question.','rationale':'The added response targets the categorization complaint, not the original navigation instruction or issue-51 contents. The source supplies no new authority, sanction, or verified implementation for those focal units.','evidence':[ev('32406-165','This is a known issue. See https://github.com/maflcko/DrahtBot/issues/51. edit: fixed'),ev('32406-169',qcomplaint)]},
{'unit_ids':['C115_no_repost','C115_unsubstantiated','C115_repetition'],'decision':'No change to standing or deontic interpretation.','rationale':'Content over category totals does not explicitly recognize the conditional no-obligation to repeat a point, a duty to substantiate every ACK, or the full prohibition-like reading of repeated comments.','evidence':[ev('32359-115',"if your point has already been made here or on #28130, you don't need to post it again."),ev('32359-115','There is no reason to leave unsubstantiated or repeat acks/nacks other than to spam the people subscribed to this repo.'),ev('32406-169',qvalue)]},
{'source_ids':['32359-213','33224-018','32381-012','33453-body','33224-010'],'decision':'No changes to their focal statements or interpretations.','rationale':'The added source concerns bot categories and review-summary purpose, not node-configuration proposals, translation tooling or freeze exceptions, extra arguments, or deprecation principles. It supplies no missing original quoted attribution for those focal sources.','evidence':[ev('32406-169',qclass),ev('32406-169',qoverview),ev('32406-169',qvalue)]},
{'decision':'No rule_candidate, repeatedly_supported, sanction, institutional effect, or causal merge finding added.','rationale':'The reply describes an expectation and a summary purpose without establishing rule-making authority, enforcement, a linked cross-episode chain, or an observed effect on integration. The unseen current-master guideline link is not treated as additional documentation.','evidence':[ev('32406-169',qvote),ev('32406-169',qvalue),ev('32406-169','This is also explained in the comment above the table: "See [the guideline](https://github.com/bitcoin/bitcoin/blob/master/CONTRIBUTING.md#code-review) for information on the review process."')]}
],
'response_sequence':{'claim':'The earlier updating complaint receives a known-issue response, referral, and reported fix. A separate categorization complaint is then quoted exactly in the added source and receives an explanation of selection when both categories occur, together with a non-voting review-summary explanation. Exact correspondence establishes the two replies; chronology does not show that the first repair caused the second clarification.','evidence':[ev('32406-164',"Did the NACK/ACK bot break? Doesn't seem to be updating? @DrahtBot"),ev('32406-165','This is a known issue. See https://github.com/maflcko/DrahtBot/issues/51. edit: fixed'),ev('32406-166',qcomplaint),ev('32406-169',qcomplaint),ev('32406-169',qclass),ev('32406-169',qvote),ev('32406-169',qoverview)]},
'unresolved_questions':['Whether category totals and repeated posting counts warrant this-proposition recognition of the general merit criterion or only broader-proposal recognition.','Whether the two bot issues share an underlying cause; what the fixed edit covered and when it was made.','What winner and majority mean in the focal majority claim; the added source does not identify its decision arena.'],
'preserved_first_output_sha256':before,
'accessed_paths':[str(base/f) for f in ['context_completion.json','context_completion_provenance.json','packet_v2.json','packet.json','annotation.json','review_notes.json','checks.json','repair_log.json','build_supplement.py','tools/check_annotation.py','protocol/annotation_schema.json','annotation.supplemented.json','checks.supplemented.json','supplement_review.json']],
'disallowed_material_encountered':False,
'source_review_completed':'Reread the added source and the original bot, forum/merit, and majority texts; reviewed all four changed units, new endpoints, event scopes, and summary changes against their exact evidence. The original extraction and component assignments remain unchanged.'}
Path('annotation.supplemented.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
Path('supplement_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
assert before=={f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in frozen}
print(json.dumps({'counts':counts,'changed':list(changed),'new':new_ids,'first_outputs_unchanged':True},indent=2))
