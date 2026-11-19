from pathlib import Path
import json,collections,copy,datetime
p=json.loads(Path('packet.json').read_text()); entries={x['source_id']:x for x in p['entries']};a=json.loads(Path('annotation.final.json').read_text());by={u['unit_id']:u for u in a['units']};rep=json.loads(Path('repair_log.json').read_text())
def ev(s,q):
 i=entries[s]['text'].index(q);return {'source_id':s,'span':{'start':i,'end':i+len(q),'quote':q}}
def base(u):return {'source_id':u['source_id'],'span':u['span']}
notes={
'S01':'The source is an elliptical description of the current contribution as the same procedure used for releases. Follow and its object are inferred roles, not explicit words. Strategy is plausible but undetermined remains an alternative. The retained body is not dated to PR creation sentence by sentence. Simpler procedure and #25650 automation remain scope qualifications; the broad merge is not adoption of a recurring norm.',
'S02':'See is local to the first historical commit referral, with the full SHA and v23.0 label retained. Its governor was narrowed rather than enlarging the unit. The decision object is the referenced commit, not this PR; no disposition of that reference is fabricated.',
'S03':'The second historical commit shares see from the earlier coordinated phrase. The full SHA and v22.0 label are local objects. AND links the two navigation actions, not endorsements of historical procedures.',
'S04':'The negative modal is the full don\'t need to, and the two locations CI scripts and test/README.md remain in the object. Automation is the explicit reason. No-obligation wording is retained while technical redundancy remains the principal alternative; no authority is inferred.',
'S05':'See is navigation, the guideline is its target, and for information on the review process is a purpose constraint rather than an invented activation condition. The mutable master URL is not equated with the supplied pinned revision; null object identity is explained.',
'S06':'The react action explicitly targets this comment, so Bdir is used rather than Bind. The incorrectly-listed-review condition and 👎 execution form remain intact. The actor comes from a possessive addressee cue and is inferred; please is not a lexical deontic. Bot templating is not repeated recognition.',
'S07':'The announced ignore action has an explicit bot actor and local pronoun object. Review could not uniquely resolve it to a review versus this comment, so reference uncertainty is retained. The next-update timing and reaction condition survive. O links an announced procedural consequence, not observed enforcement.',
'S08':'Hold off is an explicit action with a bit as the limited duration. The wallet-bug concern is attached as context. This is a case-specific recommendation, not a rule that new releases must wait. A later merge does not prove rejection of this temporary suggestion.',
'S09':'The literal subject it becomes the object of an inferred rebase request, with both inferred roles labeled. After #26589 remains the activation dependency. The later author report only confirms rebasing generally and cannot verify #26589. The later pinned guide gives broader, temporally insufficient support.',
'S10':'We should add every major release states the action, actor, recommendation, and general coverage criterion. The accidental-breakage purposes remain attached. The latest-feature criterion directly conflicts in the same test domain. The cost dispute was moved to broader_principle because low cost is not the original stated premise. Recurring selection is collective choice, without evidence of authority or adoption.',
'S11':'Adding v24.0 has an explicitly stated object even under the pragmatic recommendation reading. Should belongs to justify and is not a deontic commanding add. Whatever becomes widely downloadable is preserved. The test\'s lack of miniscript coverage challenges a supplied rationale without proving the addition was rejected.',
'S12':'Prefer is reconstructed as a use-method, so I, action, and test object receive inferred-role labels. Specific tests and the complete git command example remain recoverable. This is an articulated method, with social expectation and mere preference as alternatives; operational engineering remains an alternative level.',
'S13':'Keep this PR open is directly supplied and until another PR needs it is retained. Can is an option rather than authorization. The later same-actor repetition is a response and does not earn expectation recognition; the profile was corrected to none. No observed dependency or intentional waiting implementation is claimed.',
'S14':'Remove intermediate releases at some point is an option answering the append-only cost question. Intermediate and the indefinite future time remain explicit. The proposed matrix strategy is distinguished from actual removal; operational cleanup is a valid alternative to collective-choice design.',
'S15':'You have to keep a built copy of every single release listed is exact, including the run-the-test prerequisite. The objection to guix binaries remains a qualification. Technical necessity versus institutional obligation is unresolved; no rule or authorized discretion is inferred.',
'S16':'The source proposes having a script loop over locally available versions. The final parse reconstructs configure, keeps the script as its separate object, and preserves loop-over-available behavior as a constraint. The local it anchor was repaired after the final checker caught an accidental substring match. The unchanged fetch-all default is attached. Operational edit versus recurring selection arrangement remains a level alternative.',
'S17':'Up to the developer conditionally allocates choice of releases under the S16 loop. The preferred constitutive layer concerns operational discretion, not authority to make governance rules. Permission is proposed, not established. The all-binaries download default remains distinct from testing choice.',
'S18':'Drop EOL versions is the first action in a tentative compound question. Passive patient EOL versions is explicit; no actor is invented. It is paired with stored wallets and the priority of modern software opening ancient wallets. Both conditional technical feasibility and ordinary maintenance alternatives survive.',
'S19':'The repository is the explicit grammatical hosting actor and some regtest wallets its object. Instead links to dropping EOL versions. This does not constitute an institutional office or role; it is the storage action in a testing strategy. AND preserves the coupled replacement proposal.',
'S20':'The passive patient it is local to should be updated; no author or maintainer is invented as actor. If still going ahead and use 24.0.1 are retained. The author report and patch plus integration establish both reported and observed implementation of that version update only. The archive-availability qualification remains in the report outcome.',
'S21':'The uncertainty over what to do plus the addressed @Sjors supports a pragmatic advice request more strongly than an isolated ping. All reconstructed roles are inferred. A context-only invitation remains an alternative and the later assessment is only context-inferred uptake because threading is missing.',
'S22':'The actor now comes from the main we could leave predicate, not from As we have done before. Open, the no-pressing-reason rationale, and the linked occasional-rebase action are retained. This is a proposed option, with no claim that elapsed delay proves implementation.',
'S23':'The actor we is shared from the actual leave/rebase clause, and the pronoun it targets the PR. Occasionally remains a constraint. The shared actor was repaired because the same referent in a different predicate is not sufficient explicit grammatical evidence.',
'S24':'Not rush merging retains the complete negation; recommendation does not become prohibition. The new-releases object is explicit even though prescriptive force is inferred. The quoted exception for recurring smoke-test failures is attached. Operational integration advice is preferred, with a recurring timing-policy alternative.',
'S25':'Prune versions in a follow-up is a strategy option. The unidentified future follow-up has null decision_object_id and no merge disposition. The containing PR\'s merge cannot stand for this proposed cleanup. Always expresses continuing feasibility, not duty.',
'S26':'Only the latest release for each missing feature is retained as a personal recurring criterion. The related pinned commit documents a broader last-release rationale and examples in txindex and mempool; it does not impose the wallet criterion. Its echoed utACK is ordinary assent to that contribution, not interpersonal expectation recognition here. The author\'s minimum challenges application of this criterion.',
'S27':'The governing you is the second you in the main need-to predicate, not the antecedent want clause. The remove-23.x action is conditional on choosing to add 24.x. Need-to expresses a norm candidate without authority evidence. OR preserves explain as an alternative, and no exact implementation is inferred from the merge.',
'S28':'Explain has the complete informational object why 24.x is special. Its actor, need-to force, and activation condition are shared from the same coordinated review clause. Those shared roles are justified explicitly. The author questions the need for specialness; this is not rejection by an institutional authority.',
'S29':'See also is a separate navigation instruction to the full pinned commit identifier. The commit is the decision object of the referral, and no containing-PR outcome is attached to it.',
'S30':'The elliptical same goes extends the previous criterion to other versions in this file. The final decomposition separates apply, the criterion, and the versions receiving that criterion; all are inferred roles. Unrelated qualifies the local scope, and operational clarification is a level alternative.',
'S31':'Someone and that are explicit arguments of do, with the cleanup content resolved contextually. Separate pull is material and does not identify a real PR. The final object is null and its formerly misattached current-PR merge event is removed. General ACK does not accept every cleanup criterion or promise implementation.',
'S32':'The complete minimum includes wallet backwards compatibility tests, at least, recent major releases, not reached EOL, always, and avoiding replacement. This is narrower than every historical major release. The reviewer\'s alternative is a same-domain content dispute. Sjors\'s exact quotation plus tentative agreement may recognize an expectation but may be ordinary technical assent; recognition remains unresolved.',
'S33':'The verify predicate is distinct from the preceding I do not think predicate. It retains both versions, wallets created on master, opening on both, and the risk of missing either case. The stance that 24.x is not special remains a qualifier. Personal verification strategy is not an obligation.',
'S34':'The demonstrative subject of the literal scope assertion becomes the inferred excluded object under the pragmatic interpretation. General support for cleanup remains visible. The guide is only broader support with unresolved temporal continuity. Follow-up pruning may recognize a scope expectation or merely convenient sequencing, so interpersonal recognition was downgraded to unresolved. The merge is only a broader contribution status.'}
checks_files=['checks.first.json','checks.postmechanical.json','checks.selfreview.01.json','checks.json']
snapshots={'checks.first.json':'annotation.first_complete.json','checks.postmechanical.json':'annotation.postmechanical.json','checks.selfreview.01.json':'annotation.selfreview.01.json','checks.json':'annotation.final.json'}
checks={f:json.loads(Path(f).read_text()) for f in checks_files}
source_meta={
'S09':[{'source_id':'guide:contributing','field':'revision','value':entries['guide:contributing']['revision']},{'source_id':'guide:contributing','field':'git_blob_sha','value':entries['guide:contributing']['git_blob_sha']},{'source_id':'guide:contributing','field':'source_as_of','value':entries['guide:contributing']['source_as_of']}],
'S34':[{'source_id':'guide:contributing','field':'revision','value':entries['guide:contributing']['revision']},{'source_id':'guide:contributing','field':'git_blob_sha','value':entries['guide:contributing']['git_blob_sha']}],
'S26':[{'source_id':e['source_id'],'field':'revision','value':e.get('revision')} for e in p['entries'][40:42]]}
compat=[]
for uid in ['S09','S26','S34']:
 compat.append({'unit_id':uid,'code':'revision','status':'retained','formal_checker_status':'unresolved','category':'packet_checker_compatibility','reason':'The supplied checker accepts pinned_revision only when an evidence entry exposes blob_sha or revision_id. The frozen packet uses revision and, for the guide, git_blob_sha. These supplied fields identify pinned sources, but the unchanged checker does not recognize their names. The annotation keeps faithful pinned_revision coding; this is separate from the explicitly stated documentary coverage and temporal uncertainty.','source_metadata_evidence':source_meta[uid],'evidence':by[uid]['institution']['documentary_support'][0]['evidence']})
# Resolve each checker occurrence, preserving its checkpoint identity.
flagres=[];errorres=[]
for fname in checks_files:
 check=checks[fname];snap=json.loads(Path(snapshots[fname]).read_text());snapby={u['unit_id']:u for u in snap['units']};ordinals=collections.Counter()
 for k,f in enumerate(check['review_flags']):
  code=f['code'];uid=f['unit_id'];n=ordinals[(code,uid)];ordinals[(code,uid)]+=1
  status='retained';evidence=[];rationale='';target=None;metadata=[]
  if uid:
   u=by[uid];evidence=[base(u)];rationale=notes[uid]
   if code=='predicate_audit':
    finalidx=min(n,len(u['components'])-1);c=u['components'][finalidx];target=['units',uid,'components',finalidx]
    evidence=c['evidence']+[c['governing_span']];rationale+=' Component review: '+c['symbol']+' / '+c['text']+'. '+(c['inference_note'] or 'The cited words directly perform the local role in this predicate.')
    changed=any(x['unit_id']==uid and x['path'] and x['path'][0]=='components' for x in rep['changes'])
    if changed:status='corrected'
    if uid=='S07' and c['symbol']=='Bdir':status='unresolved'
   elif code=='qualifier_audit':
    evidence += [e for q in u['proposition']['qualifiers'] for e in q['evidence']];target=['units',uid,'proposition','qualifiers']
    if any(x['unit_id']==uid and x['path'][:2]==['proposition','qualifiers'] for x in rep['changes']):status='corrected'
    if uid in ['S07','S15','S21']:status='unresolved'
   elif code=='document_scope':
    d=u['institution']['documentary_support'][n];evidence=d['evidence'];rationale=d['rationale']+' '+notes[uid];metadata=source_meta[uid];target=['units',uid,'institution','documentary_support',n]
    status='unresolved' if d['temporal_fit']!='established' else 'retained'
   elif code=='application_audit':
    d=u['institution']['application_evidence'][n];evidence=d['evidence'];rationale=d['rationale']+' '+notes[uid];target=['units',uid,'institution','application_evidence',n]
   elif code=='challenge_audit':
    d=u['institution']['challenges'][n];evidence=d['evidence']+[base(u)];rationale=d['rationale']+' '+notes[uid];target=['units',uid,'institution','challenges',n]
    if uid=='S10' and n==1:status='corrected'
   elif code=='recognition_audit':
    d=[e for e in u['institution']['recognition'] if e['kind']=='expectation_recognition'][n];evidence=d['evidence']+d['identity_evidence'];rationale=d['rationale'];target=['units',uid,'institution','recognition'];status='unresolved' if d['mode']=='unresolved' else 'retained'
   elif code=='higher_level_audit':
    field='statement_target_level' if n==0 else 'observed_action_level';target=['units',uid,field];evidence=u['level_evidence']['evidence'];rationale=u['level_rationale']+' '+notes[uid]
   else:target=['units',uid]
  elif code=='challenge_object':
   r=[r for r in a['relations'] if r['type']=='challenges'][n];target=['relations',r['from_unit_id'],r['to_unit_id'],'challenges'];evidence=r['evidence'];rationale=r['rationale']+' Both endpoints are anchored to the same local release-testing dispute or its stated low-cost premise; no different referenced PR is substituted. The relation does not imply sanction or authority.'
  elif code=='summary_audit':
   items=[('observed_outcomes',i,x) for i,x in enumerate(a['episode_summary']['observed_outcomes'])]+[('mechanisms',i,x) for i,x in enumerate(a['episode_summary']['mechanisms'])]
   group,i,x=items[n];target=['episode_summary',group,i];evidence=x['evidence'];rationale='Every material clause is separated in claim_parts, with the same anchors included in the parent evidence. '+('This is a report or recorded artifact/status claim, not evidence of general norm adoption or network adoption.' if group=='observed_outcomes' else x['alternative_explanation']+' The assigned mechanism status remains '+x['status']+'.')
   if (group=='observed_outcomes' and i==0) or (group=='mechanisms' and i==2):status='corrected'
  flagres.append({'checker_file':fname,'flag_index':k,'code':code,'unit_id':uid,'occurrence_ordinal':n,'target':target,'status':status,'rationale':rationale,'evidence':evidence,**({'source_metadata_evidence':metadata} if metadata else {})})
 for k,e in enumerate(check['errors']):
  uid=e.get('unit_id');code=e['code'];r={'checker_file':fname,'error_index':k,'code':code,'unit_id':uid}
  if code=='revision':
   d=next(x for x in compat if x['unit_id']==uid);r.update({key:value for key,value in d.items() if key not in ['unit_id','code']})
  else:
   matches=[x for x in rep['changes'] if x['unit_id']==uid]
   r.update(status='corrected',category='coding_execution',rationale=notes[uid],change_ids=[x['change_id'] for x in matches],evidence=[base(by[uid])])
  errorres.append(r)
unitreviews=[]
for u in a['units']:
 uid=u['unit_id']
 if u['record_role']=='statement':
  status='unresolved' if uid in ['S07','S15','S21','S32','S34'] else 'corrected' if any(x['unit_id']==uid for x in rep['changes']) else 'retained'
  unitreviews.append({'unit_id':uid,'status':status,'source_review':notes[uid],'evidence':[base(u)]+[e for q in u['proposition']['qualifiers'] for e in q['evidence']],'authority_assessment':'No focal proposition supplies attributed institutional authorization or enforcement sufficient for rule_candidate. Norm and strategy labels are candidates, not findings of adoption.','standing_profile_review':u['institution']['standing_profile'],'disposition_review':[{'kind':d['kind'],'target':d['target'],'object_id':d['object_id'],'evidence':d['evidence'],'identity_evidence':d['identity_evidence'],'assessment':d['rationale']} for d in u['disposition_events']],'predicate_roles_reviewed':[{'symbol':c['symbol'],'text':c['text'],'basis':c['basis'],'occurrence_role':c['occurrence_role'],'evidence':c['evidence'],'governing_span':c['governing_span'],'assessment':c['inference_note'] or 'Explicit argument, predicate, or constraint in the declared local clause.'} for c in u['components']]})
 else:
  unitreviews.append({'unit_id':uid,'status':'retained','source_review':'The record is '+u['record_role']+'. It has no institutional grammar/components/support profile. '+('Its repeated text is linked to the original occurrence by quotes and is not counted as independent recognition.' if u['record_role']=='quotation' else 'It preserves a distinct review act, rationale, question, or attributed report used as a relation endpoint or in the mechanism narrative.'),'evidence':[base(u)]})
screens=[]
for sc in a['entry_screening']:
 e=entries[sc['source_id']];q=e['text'][:500]
 screens.append({'source_id':sc['source_id'],'status':'retained','disposition':sc['disposition'],'scope':'exhaustive_focal' if sc['source_id'] in p['selection_design']['focal_source_ids'] else 'supplemental_context','review':sc['reason'],'unit_ids':sc['unit_ids'],'evidence':[ev(sc['source_id'],q)] if q else [],'empty_source_metadata':{'review_state':e.get('review_state'),'author':e.get('author'),'timestamp':e.get('timestamp')} if not q else None})
relationreviews=[]
for i,r in enumerate(a['relations']):
 relationreviews.append({'relation_index':i,'from_unit_id':r['from_unit_id'],'to_unit_id':r['to_unit_id'],'type':r['type'],'status':'retained','review':r['rationale']+' '+('Direction follows the literal quotation/repeated-original mapping.' if r['type']=='quotes' else 'The assigned basis remains '+r['basis']+'; no causal, enforcement, or adoption conclusion is added.'),'evidence':r['evidence']})
review={'run_id':'F01_v04_r1','review_type':'one_complete_source_based_self_review','source_review_passes':1,'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':{'entries_reviewed':42,'exhaustive_focal_entries':23,'supplemental_context_entries':19,'units':60,'statements':34,'contexts':14,'quotations':12,'relations':34,'observed_outcomes':3,'mechanisms':3},'sequence':['Complete assigned sources and codebook/schema read.','First complete annotation frozen before checker and source self-review.','Initial checker result preserved; mechanical repairs recorded.','One full source-based review covered screening, qualification, predicate roles, object/time identity, evidence basis, recognition/application, dispositions, levels, all relations and all outcome/mechanism clauses.','An accidental token anchor introduced during the review was repaired from the final checker result and the pre-repair snapshot and result were preserved.','Final unchanged checker reports only three packet/checker revision-key compatibility errors.'],'unit_reviews':unitreviews,'screening_reviews':screens,'relation_reviews':relationreviews,'checker_error_resolutions':errorres,'checker_flag_resolutions':flagres,'compatibility_limits':compat,'interpretive_limits':a['episode_summary']['missing_evidence']+a['episode_summary']['unresolved_questions']+['The ignored object in the bot consequence remains ambiguous.','A complete source review and mechanical checks do not certify that all institutional interpretations are uniquely correct.'],'summary_review':[{'group':g,'index':i,'status':'retained','claim':x['claim'],'claim_parts':x['claim_parts'],'review':'All positive material clauses have corresponding supplied text or patch/status evidence. Repository integration, particular edits, participant reports, and norm adoption remain distinct. Alternative explanations are retained for mechanisms.'} for g in ['observed_outcomes','mechanisms'] for i,x in enumerate(a['episode_summary'][g])],'change_summary':{'total_records':len(rep['changes']),'meaning_change_records':sum(x['meaning_changed'] for x in rep['changes']),'effects':dict(collections.Counter(x['effect'] for x in rep['changes']))},'formal_checker_status':checks['checks.json']['status'],'coding_errors_remaining':0,'packet_checker_compatibility_errors_remaining':3}
Path('review_notes.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
# Coverage of every feedback occurrence is independently countable.
assert len(flagres)==sum(len(x['review_flags']) for x in checks.values())
assert len(errorres)==sum(len(x['errors']) for x in checks.values())
print(json.dumps({'review_flags_resolved':len(flagres),'checker_error_occurrences_resolved':len(errorres),'unit_reviews':len(unitreviews),'source_reviews':len(screens),'changes':len(rep['changes'])},indent=2))
