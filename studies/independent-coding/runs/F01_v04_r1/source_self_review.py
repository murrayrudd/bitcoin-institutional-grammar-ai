from pathlib import Path
import json,copy
p=json.loads(Path('packet.json').read_text()); text={e['source_id']:e['text'] for e in p['entries']}; a=json.loads(Path('annotation.json').read_text()); by={u['unit_id']:u for u in a['units']}; log=json.loads(Path('repair_log.json').read_text()); changes=log['changes']
def ev(s,q,start=0):
 i=text[s].index(q,start);return {'source_id':s,'span':{'start':i,'end':i+len(q),'quote':q}}
def ee(i,q,start=0):return ev(p['entries'][i]['source_id'],q,start)
def edit(uid,path,value,reason,evidence,effect='evidence_basis_error',meaning=False,diagnosis='execution_failure_under_existing_rule'):
 d=by[uid] if uid else a
 for k in path[:-1]:d=d[k]
 old=copy.deepcopy(d[path[-1]])
 if old==value:return
 d[path[-1]]=value;changes.append({'change_id':'R%02d'%(sum(x['stage']=='source_self_review' for x in changes)+1),'stage':'source_self_review','unit_id':uid,'path':path,'before':old,'after':copy.deepcopy(value),'reason':reason,'evidence':evidence,'diagnosis':diagnosis,'effect':effect,'meaning_changed':meaning})
# Review of predicate-local role evidence: shared actors must come from the action they govern.
main=ee(16,'we could just leave the PR open and occasionally rebase it.')
edit('S23',['components',0,'evidence'],[ee(16,'we',main['span']['start'])],'The shared actor comes from we could leave, not from the separate As we have done before predicate.',[main])
for uid in ['S27','S28']:
 main=ee(20,'you will either need to remove 23.x or explain why 24.x is special')
 edit(uid,['components',0,'evidence'],[ee(20,'you',main['span']['start'])],'The subject governing remove/explain is the second you, not the subject of want in the activation condition.',[main])
# Preserve uncertainty about the bot pronoun rather than force a specific object.
edit('S07',['components',2,'text'],'it (the referent is unresolved between the listed review and this comment)','The local object role is explicit, but the supplied prose does not settle the antecedent.',[ee(1,'If your review is incorrectly listed, please react with 👎 to this comment and the bot will ignore it on the next update.')],meaning=True)
edit('S07',['components',2,'inference_note'],'It is the explicit direct object of ignore. The antecedent could be the incorrectly listed review or this comment; the packet does not independently resolve it.','Separate explicit predicate role from uncertain reference.',[ee(1,'ignore it')])
edit('S07',['proposition','summary'],'The bot says that it will ignore "it" on the next update after the requested 👎 reaction; the ignored object may be the incorrectly listed review or the comment.','Retain both plausible antecedents in the focal proposition.',[ee(1,'If your review is incorrectly listed, please react with 👎 to this comment and the bot will ignore it on the next update.')],effect='changed_institutional_meaning',meaning=True,diagnosis='unresolved')
edit('S07',['complexity_flags'],['unresolved_reference'],'Expose the unsettled object reference.',[ee(1,'ignore it')],effect='convention_deviation')
edit('S07',['confidence'],'unresolved','The consequence is announced, but the target object remains ambiguous.',[ee(1,'ignore it')],meaning=True,diagnosis='unresolved')
edit('S07',['uncertainty_reason'],'The antecedent of it is not uniquely identified; no use of the reaction or later bot correction is observed.','State the limit on downstream consequence claims.',[ee(1,'ignore it on the next update')],effect='coverage_or_scope_loss',meaning=True,diagnosis='unresolved')
# Remove a remote cost premise from the exact add-every-release proposition.
edit('S10',['institution','challenges',1,'target'],'broader_principle','The cost denial challenges continued use of the general compatibility test, not a cost premise stated in the add-every-major-release proposition itself.',[ee(5,'So I think we should add every major release.'),ee(10,"It's not low cost.")],meaning=True)
edit('S10',['institution','challenges',1,'rationale'],'The cost denial concerns the broader low-cost justification for keeping a general compatibility test. The exact add-every-major-release proposition gives accidental-breakage prevention as its reason, so this challenge is not treated as a direct dispute of that stated premise.','Keep the broader challenge visible without conflating its target.',[ee(5,"one reason for the backwards compatibility tests is to ensure there's no accidental breakage between versions"),ee(10,"It's not low cost.")],meaning=True)
# The proposed software method contains nested conduct; reconstruct the configuration action explicitly.
u=by['S16'];s=u['source_id'];g={'source_id':s,'span':u['span']}
def comp(symbol,t,q,basis='explicit',role='local',note=''):
 return {'symbol':symbol,'text':t,'basis':basis,'evidence':[ev(s,q)],'inference_note':note,'occurrence_role':role,'governing_span':g}
new=[comp('A','we','we',note='We remains the explicit actor of have in the source; this same configuring actor is retained under the reconstructed configure action.'),comp('I','configure','have it loop over',basis='context_inferred',role='semantic_inference',note='Configure is reconstructed from having the test script loop over available versions; it does not embed a program object inside I.'),comp('Bdir','it (feature_backwards_compatibility.py)','it',note='It is the explicit target of have in the same clause and remains the target of configure. Its antecedent is the filename in the preceding phrase.'),comp('Cex','to loop over whatever is available under `releases/v*`','loop over whatever is available under `releases/v*`'),comp('Cex','Instead of hardcoding the version numbers','Instead of hardcoding the version numbers')]
edit('S16',['components'],new,'Keep the configuration action separate from the script being configured and the loop behavior required of it.',[ee(11,'we could have it loop over whatever is available under `releases/v*`')],effect='convention_deviation')
edit('S16',['parse_mode'],'pragmatic','Configure is an inferred action that faithfully represents the articulated have-it-loop method.',[ee(11,'we could have it loop over')],effect='evidence_basis_error')
edit('S16',['complexity_flags'],['nested_component'],'The program configuration governs a nested loop behavior.',[ee(11,'we could have it loop over whatever is available under `releases/v*`')],effect='convention_deviation')
# Null IDs are required for proposed future cleanup contributions whose identity is not supplied.
for uid,q in [('S25','In any case we can always prune versions in a followup.'),('S31','so someone could do that in a separate pull')]:
 idx=16 if uid=='S25' else 21; evidence=[ee(idx,q)]
 edit(uid,['proposition','decision_object_id'],None,'This proposal concerns an unidentified future cleanup contribution, not the containing PR as its decision object.',evidence,effect='changed_institutional_meaning',meaning=True)
 edit(uid,['proposition','identity_evidence'],[],'No canonical identity for the future follow-up or separate pull is supplied.',evidence,meaning=True)
 edit(uid,['disposition_events'],[],'The current PR merge cannot establish the disposition of an unidentified future cleanup proposal.',evidence,effect='changed_institutional_meaning',meaning=True)
 newqual={'description':'The follow-up contribution has no supplied canonical object ID or outcome record.','evidence':evidence,'attachment':'scope_note','linked_unit_id':None,'rationale':'Null denotes unresolved proposal identity, not a claim that the containing PR was unmerged.'}
 edit(uid,['proposition','qualifiers'],by[uid]['proposition']['qualifiers']+[newqual],'Make the identity limit explicit and available to alignment.',evidence,effect='coverage_or_scope_loss',meaning=True)
# Reparse the criterion extension without embedding an object in the action label.
u=by['S30'];s=u['source_id'];g={'source_id':s,'span':u['span']}
new=[]
for symbol,t,q,note in [('I','apply','The same goes','Apply is reconstructed from the elliptical extension same goes.'),('Bdir','the previously stated latest-release-per-missing-feature criterion','The same','The demonstrative same supplies the criterion being applied, with the criterion resolved to S26.'),('Bind','the other versions in this file','the other versions in this file','The other versions are the distinct target to which the criterion is applied; this destination role is inferred from the elliptical phrase.')]:
 new.append({'symbol':symbol,'text':t,'basis':'context_inferred','evidence':[ev(s,q)],'inference_note':note,'occurrence_role':'semantic_inference','governing_span':g})
edit('S30',['components'],new,'Separate applying from the criterion and the versions to which it applies. The source interpretation remains the same.',[ee(21,'The same goes for the other versions in this file'),ee(20,'the latest release for each missing feature')],effect='convention_deviation')
# Narrow the verification predicate, preserving the preceding skeptical claim in the unit and qualifier.
g=ee(22,"I'd rather verify this assumption (in this case e.g., that wallets created on master can still be opened on both of these versions) rather than potentially miss out on either one of those cases.")
for j,c in enumerate(by['S33']['components']):edit('S33',['components',j,'governing_span'],g,'Anchor the roles to verify, rather than the separate preceding I do not think predicate.',[g],effect='convention_deviation')
# Local scope recognition is plausible but the wording can equally describe a feasible option.
edit('S34',['institution','recognition',0,'mode'],'unresolved','Can prune in a follow-up does not unambiguously treat the scope boundary as an expectation.',[ee(16,'In any case we can always prune versions in a followup.')],meaning=True,diagnosis='criterion_ambiguity')
edit('S34',['institution','recognition',0,'basis'],'unresolved','The alternative of ordinary technical assent or convenient sequencing remains live.',[ee(16,'In any case we can always prune versions in a followup.')],meaning=True,diagnosis='criterion_ambiguity')
edit('S34',['institution','recognition',0,'rationale'],'Sjors proposes follow-up pruning, which is consistent with the author\'s local scope boundary. It may recognize that boundary as an expectation, but may instead express ordinary agreement with convenient sequencing; the packet does not settle this distinction.','Avoid turning consistency into established interpersonal recognition of an expectation.',[ee(22,"that's outside of scope for this PR."),ee(16,'we can always prune versions in a followup.')],meaning=True,diagnosis='criterion_ambiguity')
edit('S34',['institution','standing_profile','recognition'],'unresolved','The recognition profile follows the retained ambiguity.',[ee(16,'we can always prune versions in a followup.')],meaning=True,diagnosis='criterion_ambiguity')
# Retain bounded alternative governance readings where proposed engineering changes can be operational.
for uid in ['S12','S14','S16','S18','S19','S30']:
 edit(uid,['target_level_alternatives'],['operational'],'Recurring test-design arrangement is the preferred target; a bounded reading treats it as ordinary test maintenance.',[{'source_id':by[uid]['source_id'],'span':by[uid]['span']}],effect='convention_deviation',diagnosis='defensible_alternative_representation')
 edit(uid,['observed_level_alternatives'],['operational'],'The observed deliberation can also be read as ordinary engineering discussion without a decision on a recurring arrangement.',[{'source_id':by[uid]['source_id'],'span':by[uid]['span']}],effect='convention_deviation',diagnosis='defensible_alternative_representation')
edit('S24',['target_level_alternatives'],['collective_choice'],'General advice against rushing release additions could be read as a proposed recurring integration policy, but the focal act supplies no specified new timing procedure.',[ee(16,'This can also be a reason to not rush merging new releases.')],effect='convention_deviation',diagnosis='defensible_alternative_representation')
# Correct linked summary wording after referent and identity review.
for uid in ['S07','S25','S31']:
 edit(uid,['level_evidence','target_activity'],by[uid]['proposition']['summary'],'Keep level evidence aligned with the final bounded proposition.',by[uid]['institution']['evidence'],effect='convention_deviation')
edit('S07',['level_rationale'],'The focal statement announces a bot-list update after a reaction. Its observed act is operational procedural guidance; the ignored object remains unresolved.','Keep the level rationale from retaining the earlier forced antecedent.',[ee(1,'the bot will ignore it on the next update.')],effect='coverage_or_scope_loss',meaning=True)
# Outcome/mechanism clauses: remove unsupported negative outcome claims and evidence every stated concern.
edit(None,['episode_summary','observed_outcomes',0,'claim'],'PR #26586 was recorded merged on February 16, 2023.','Keep the observed outcome wholly factual; limits on policy adoption remain explicit in missing evidence and event rationale.',[ee(24,'"merged": true'),ee(24,'"merged_at": "2023-02-16T14:04:28Z"')],effect='convention_deviation')
mech=copy.deepcopy(a['episode_summary']['mechanisms'][2]);mech['claim']='Participants raised cost and test-value concerns and proposed waiting, pruning versions, using locally available releases, or replacing EOL-version testing with stored wallets.'
newpart={'text':'Test-value concerns included the limited efficacy of a general test and doubt about investigation of intermittent failures, except obvious recurring smoke-test issues.','evidence':[ee(6,"It is likely so general that it can't catch any issues."),ee(12,"In any case the test fails intermittently (#24400), so apart from obvious smoke test issues that happen on every iteration, I don't think anyone even looks into failures here.")]}
mech['claim_parts'].insert(1,newpart);mech['evidence']+=newpart['evidence'];mech['unit_ids']+=['C04','C09']
edit(None,['episode_summary','mechanisms',2],mech,'Cite the test-value concerns explicitly and leave lack of implementation evidence as a limitation rather than an observed negative outcome.',newpart['evidence'],effect='coverage_or_scope_loss')
# Clarify all generic null object cases explicitly in the proposition's scope notes when not already explained.
for uid in ['S04','S10','S12','S14','S15','S16','S17','S18','S19','S24','S26','S30','S32']:
 u=by[uid];q={'description':'No unique canonical proposal ID exists for this general testing criterion or method; the domain is bounded to the compatibility-testing discussion.','evidence':[{'source_id':u['source_id'],'span':u['span']}],'attachment':'scope_note','linked_unit_id':None,'rationale':'The containing PR identifies the discussion episode but is not silently substituted for a general proposition\'s decision object.'}
 edit(uid,['proposition','qualifiers'],u['proposition']['qualifiers']+[q],'Explain null decision-object identity without inventing a new proposal identifier.',q['evidence'],effect='convention_deviation')
# S05 deliberately points to mutable master rather than asserting a version-specific guide object.
edit('S05',['uncertainty_reason'],'The navigational target is mutable master; no exact target revision at the bot occurrence is recoverable. Decision_object_id is therefore null rather than the supplemental pinned revision.','Keep the navigation object identity distinct from documentary comparison material.',[ee(1,'https://github.com/bitcoin/bitcoin/blob/master/CONTRIBUTING.md#code-review')],effect='coverage_or_scope_loss')
Path('annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n');Path('annotation.final.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n');Path('repair_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_review_changes':sum(x['stage']=='source_self_review' for x in changes),'total_change_records':len(changes)},indent=2))
