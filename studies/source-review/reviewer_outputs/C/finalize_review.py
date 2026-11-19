import json
from pathlib import Path
from collections import Counter
base=Path.cwd()
p=json.loads(Path('packet.json').read_text()); txt={e['source_id']:e['text'] for e in p['entries']};a=json.loads(Path('annotation.json').read_text());us={u['unit_id']:u for u in a['units']}
def ev(s,q,start=0):
 i=txt[s].index(q,start);return {'source_id':s,'span':{'start':i,'end':i+len(q),'quote':q}}
repairs=[]
def anchor(uid,sym,s,q,start):
 c=next(c for c in us[uid]['components'] if c['symbol']==sym);old=c['evidence'];c['evidence']=[ev(s,q,start)];repairs.append({'unit_id':uid,'field':'components.'+sym+'.evidence','kind':'mechanical_occurrence_repair','before':old,'after':c['evidence']})
anchor('C115_forum','F','32359-115','is',txt['32359-115'].index('this is')+5)
anchor('C115_no_repost','A','32359-115','you',txt['32359-115'].index(', you')+2)
anchor('C227_remove_efforts','A','32359-227','we',txt['32359-227'].index('we should capitulate'))
anchor('C227_remove_efforts','D','32359-227','should',txt['32359-227'].index('we should capitulate')+3)
repairs.append({'unit_id':'C227_remove_efforts','kind':'semantic_occurrence_review','explanation':'The exact same we and should strings originally anchored the first quoted camp. Re-anchored to the second camp governing capitulate and remove. This corrects attribution/scope evidence without changing the preserved actor text or proposed actions.'})
us['C227_majority']['institution']['dispute_present']=False
us['C227_majority']['institution']['rationale']+=' No explicit response challenges this majority claim. The unresolved relation to the earlier forum claim records a possible conflict, not a demonstrated dispute directed at this counterclaim.'
repairs.append({'unit_id':'C227_majority','kind':'source_review_refinement','field':'institution.dispute_present','before':True,'after':False,'reason':'The earlier forum claim supplies potential contrary context, not an explicit challenge to the later majority counterclaim. The unresolved relation and uncertainty remain.'})
us['C33453_footguns']['institution']['evidence'].append(ev('33453-body','“Don’t offer users footguns” is also a good principle'))
repairs.append({'unit_id':'C33453_footguns','kind':'evidence_completion','reason':'Added exact evidence for the author calling the quoted maxim a good principle.'})
us['C213_defaults']['institution']['recognition'].append({'kind':'response','target':'this_proposition','basis':'context_inferred','evidence':[ev('32359-213','Or setting a default high limit, so that a node runner can set to a lowest value.')],'rationale':'nick1981 offers a higher-default alternative to the quoted conservative approach. This response does not recognize a duty or establish the original speaker\'s identity.'})
repairs.append({'unit_id':'C213_defaults','kind':'evidence_completion','reason':'Recorded the focal author\'s attributable alternative as a response, without upgrading institutional standing.'})
Path('annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
Path('repair_log.json').write_text(json.dumps({'initial_output':'annotation.initial.json','initial_checks':'checks.initial.json','repairs':repairs,'codebook_or_checker_modified':False,'final_source_review':'Every focal source was reread in full alongside the complete extracted units and component anchors before finalization. Semantic alternatives remain explicit; checker pass is not semantic certification.'},ensure_ascii=False,indent=2)+'\n')

def exclusion(s,q,why):return {'evidence':ev(s,q),'reason':why}
exclusions={
'32359-213':[
exclusion('32359-213','I can understand removing the limits as a default config in core (although i would prefer it not to be this way)','A qualified acknowledgment and preference, not a distinct executable proposal beyond the later conservative-default alternative; not treated as permission or endorsement of the PR.'),
exclusion('32359-213','why is the ability to configure it being removed all together?','Bare explanatory question inside an external quote; no supplied original exchange establishes an independent request to act or give reasons.'),
exclusion('32359-213','This can make running a node very RAM expensive.','Technical burden rationale; no deontic force or independent verified causal finding.')],
'33224-018':[
exclusion('33224-018','Is this context info useful?','Informational question in an external quote; no separately established invitation beyond the retained add-flag proposal.'),
exclusion('33224-018','Line numbers will change whenever some previous function in the file gets a non-trivial edit...','Technical prediction supporting the quoted suggestion; will is not a duty.'),
exclusion('33224-018',"The actual source location of the string can change and the ids in the `.xlf` won't change.",'Technical capability/stability claim retained in the diagnosis context, not a permission.'),
exclusion('33224-018',"It's unclear to me why the sort order would change.",'An explicit uncertainty, not a direction to a named actor or an institutional statement.')],
'32359-115':[
exclusion('32359-115','Reminder that','Metadiscursive introduction to the retained forum statement, not a separate instruction.'),
exclusion('32359-115','Please rest assured that','Reassurance framing; the relevant embedded no-obligation proposition is coded.'),
exclusion('32359-115','other than to spam the people subscribed to this repo.','The asserted impact explains the two discouragements; it is not a separately stated sanction, intended reward, or observed enforcement event.')],
'32406-165':[
exclusion('32406-165',"Did the NACK/ACK bot break? Doesn't seem to be updating? @DrahtBot",'Repeated question linked to the supplied original; not another independent statement or endorsement.'),
exclusion('32406-165','This is a known issue.','A response diagnosis, not a governing instruction.'),
exclusion('32406-165','edit: fixed','Reported repair context, with neither exact edit time nor independent verification. No institutional adoption is inferred.')],
'32359-227':[
exclusion('32359-227','I agree.','Assent to the quoted framing; not independent endorsement of both rhetorically opposed expectations.'),
exclusion('32359-227',"It's a debate that no one wins by argument.",'Context for the majority claim; absent a specified institutional process, retained as an assessment of persuasive limits rather than another rule.'),
exclusion('32359-227','those who believe','Attribution framing is preserved in the container, institution rationales, and uncertainties; it is not itself a separate prescription.')],
'32381-012':[
exclusion('32381-012','~0','Unelaborated stance marker; no independently interpretable prescription.'),
exclusion('32381-012','Anything that results in 150 bytes or beyond?','Included as a tentative numeric elaboration of the setting recommendation, not counted as a second instruction or asserted minimum requirement.'),
exclusion('32381-012','while I understand your main point','Limited acknowledgment does not accept the proposed extra argument; the following disagreement is retained.')],
'33453-body':[
exclusion('33453-body','Many current Bitcoin Core users want to continue using this option','Author-attributed preference claim, explicitly based on public postings rather than a formal survey; no prevalence or consensus finding follows.'),
exclusion('33453-body','for now there seem to be a bunch of users who like the option','External observational quotation attributed to AJ Towns; not an institutional statement or separately verified survey.'),
exclusion('33453-body','IMO we should not have removal warnings if there is no current plan to actually remove them.','Not excluded from the record: coded as a repeated quotation with the original supplied proposition at C32714_warning_expectation, avoiding double counting.'),
exclusion('33453-body','there is even less likelihood of a near term plan to remove these options.','An author prediction, not independent evidence of the actual absence of future plans.'),
exclusion('33453-body','the option could be removed in the next version or perhaps never.','A claim of planning uncertainty, not permission or a definite removal schedule.'),
exclusion('33453-body','There is non-zero maintenance cost to keeping this code around (although leaving the options deprecated for a long time has the same effect).','Technical/economic rationale, not a sanction or separate obligation.'),
exclusion('33453-body','there seems to be only small impacts that can quickly be remedied by changing the option value by Bitcoin Core users.','Qualified impact claim used to argue the principle\'s application; not an instruction that users must change the value or independently verified impact estimate.'),
exclusion('33453-body','There already exist in Bitcoin Core more potentially-user-harmful options/values than what datacarrier might cause.','Comparative author claim; no comparative risk evidence is supplied.')],
'33224-010':[
exclusion('33224-010','cc @hebasto; given this would change translations after translation string freeze.','Exact repeated concern linked to its original; not another expectation-recognition event.'),
exclusion('33224-010','The translation workflow on Transifex includes marking translated strings as "Reviewed", which locks them from further changes.','Technical workflow description, not automatically an institutional constitutive status or role.'),
exclusion('33224-010','Not every translation team uses this feature, but those who do rely on it.','Qualified background claim; prevents treating the described review feature as universal.'),
exclusion('33224-010','it is not guaranteed that updating the translation source file (as in https://github.com/bitcoin/bitcoin/pull/33193) won’t reset the "Reviewed" status for other strings.','Stated technical uncertainty supporting the prohibition; not verified effects or an institutional sanction.')]
}
foc=[]
for sid in p['selection_design']['focal_source_ids']:
 su=[u for u in a['units'] if u['source_id']==sid]
 foc.append({'source_id':sid,'author':next(e['author'] for e in p['entries'] if e['source_id']==sid),'full_source_reviewed':True,'screening':next(e for e in a['entry_screening'] if e['source_id']==sid),'statement_count':sum(u['record_role']=='statement' for u in su),'decisions':[{'unit_id':u['unit_id'],'record_role':u['record_role'],'evidence':{'source_id':sid,'span':u['span']},'rationale':u['institution']['rationale'],'alternative':u['alternative_interpretation'],'uncertainty':u['uncertainty_reason']} for u in su],'nonstatement_or_duplicate_decisions':exclusions[sid]})
notes={
'run_id':a['run_id'],'episode_id':a['episode_id'],'packet_sha256':a['packet_sha256'],'review_basis':'Source-first review of the eight complete focal records under frozen project v0.3. No earlier annotation or narrative was available for comparison. Claims and rhetoric are retained as attributed source content, not adopted as factual conclusions.',
'counts':{'screened_entries':len(a['entry_screening']),'focal_records':len(foc),'candidate_focal_records':sum(x['screening']['disposition']=='candidate' for x in foc),'focal_statement_units':sum(x['statement_count'] for x in foc),'supporting_statement_units':sum(u['record_role']=='statement' and u['source_id'] not in p['selection_design']['focal_source_ids'] for u in a['units']),'total_units':len(a['units']),'role_counts':dict(Counter(u['record_role'] for u in a['units'])),'relations':len(a['relations'])},
'per_focal_source':foc,
'context_and_attribution_decisions':[
{'claim':'External quotations whose originals are absent are retained as new attributed statement candidates; the current comment author is not substituted for the missing original speaker. The opposed spam positions are rhetorical descriptions, not verified camps.','evidence':[ev('32359-213','As a node runner I should be allowed to configure my mempool and not have it filled with what I consider spam.'),ev('33224-018','Would it be better to add `-locations none` to the LCONVERT invocation in translate.cmake?'),ev('32359-227','those who believe we should remain proactive towards spam filtration'),ev('32359-227','those who believe the absence of a technically perfect solutions means we should capitulate to spammers')]},
{'claim':'The supplied contribution guide assigns merges to project merge maintainers and permits merit weighting. These statements contextualize the forum/majority contrast; they do not prove the role of any named commenter or resolve whether majority concerns repository integration.','evidence':[ev('D_CONTRIB','Whether a pull request is merged into Bitcoin Core rests with the project merge\nmaintainers.'),ev('D_CONTRIB','Project maintainers reserve the right to weigh the opinions of peer reviewers\nusing common sense judgement and may also weigh based on merit.'),ev('32359-227','Only the majority decides the winner.')]},
{'claim':'The moderation document supports attributable moderation of repeated or unconstructive comments, with an exception for constructive reframing. No focal sanction is inferred, and its qualified provision is not silently substituted for the focal discouragement.','evidence':[ev('D_MOD','Moderators may remove comments that do not either contribute new information or constructively reframe existing information.'),ev('32359-115','There is no reason to leave unsubstantiated or repeat acks/nacks other than to spam the people subscribed to this repo.')]},
{'claim':'The provided release and translation documents supply release-workflow context, but no supplied text specifies the exact final freeze prohibition or assigns hebasto authority to create it. The norm-candidate classification abstains from a rule claim.','evidence':[ev('D_RELEASE','Update translations see [translation_process.md](/doc/translation_process.md#synchronising-translations).'),ev('D_TRANSLATION','For general PRs, you shouldn’t include any updates to the translation source files.'),ev('33224-010','there must not be any translation source updates after the final translation string freeze.')]}
],
'response_sequences':a['episode_summary']['mechanisms'],
'recorded_outcomes':a['episode_summary']['observed_outcomes'],
'missing_context':a['episode_summary']['missing_evidence'],'interpretive_questions':a['episode_summary']['unresolved_questions'],
'additional_source_requests':[],'source_additions':[],
'final_semantic_review':{'completed':True,'method':'Reread all eight full focal texts alongside each unit and component anchor, then revisited response, standing, chronology, and disposition claims. All three repeated quotations link to supplied originals. Every outside-unit component has an explicit scope explanation. No rule candidate was inferred solely from a modal, document title, merge, ACK, or chronology.','limitations':'Structural pass establishes schema and exact anchors only. The retained alternatives, unidentified quoted speakers, uncertain decision domain, and incomplete histories remain substantive limitations.'},
'access_audit':{'research_input_paths':[str(base/x) for x in ['REVIEW_TASK.txt','protocol/codebook.txt','protocol/annotation_schema.json','packet.json','tools/check_annotation.py']],'own_output_or_script_paths_accessed':[str(base/x) for x in ['build_annotation.py','annotation.json','annotation.initial.json','checks.initial.json','finalize_review.py','repair_log.json','review_notes.json','checks.json']],'disallowed_material_encountered':False,'statement':'No parent directory, other review, prior project analysis, Library material, external source, or conversation-history research material was inspected. All research access and output stayed in this C directory.'}
}
Path('review_notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(notes['counts'],indent=2))
