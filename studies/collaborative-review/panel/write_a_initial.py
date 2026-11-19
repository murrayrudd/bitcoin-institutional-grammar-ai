import json
from pathlib import Path
ROOT=Path('/workspace/scratch/2020b62d57db/reconciled_coding/Bitcoin_Core_IG2_Collaborative_Reconciliation_v01')
cache={}
def unit(run,uid):
 if run not in cache: cache[run]=json.loads((ROOT/'inputs/runs'/run/'annotation.final.json').read_text())
 return next(u for u in cache[run]['units'] if u['unit_id']==uid)
def change(run,uid,path,value): return dict(run_id=run,unit_id=uid,path=path,new_value=value)
def topic(i,preferred,alternatives,unresolved,sources):
 return dict(topic_id=i,preferred=preferred,alternatives=alternatives,recommended_changes=[],source_basis=[dict(source_id=s,quote=q) for s,q in sources],unresolved=unresolved)
T=[]
t=topic('D01',
 'Decided representation: unidentified follow-up work must have a null object ID; the discussion episode remains #26586. The recurring retention criterion likewise needs no numbered proposal ID. A null inapplicable identifier does not make its semantically identified assent target unknowable. I prefer ordinary, tentative assent to this proposition: the quotation preserves the recurring non-EOL floor, while the surrounding exchange supplies the wallet-testing domain and the floor entails retaining qualifying releases rather than substituting them. The omission of words from a quotation alone does not prove narrower assent.',
 'The strongest alternative is recognition of the proposed minimum as a governing consideration, with an unresolved recognition profile. A broader-principle target is also defensible if the omitted no-substitution formulation is treated as independently material. Neither reading establishes adoption, repeated recognition, or binding authority.',
 'The force of the tentative assent remains interpretive under v0.4. Future-work identity is unknown; criterion identity is semantically recoverable although a canonical numbered ID is inapplicable. These are different uncertainties.',
 [('pr26586:comments:15','I tend to agree.'),('pr26586:review_comments:2','as bare minimum rather than sacrificing one for another?'),('pr26586:review_comments:1','in a separate pull'),('pr26586:comments:15','In any case we can always prune versions in a followup.')])
for run,uid in [('F01_v04_r3','C30'),('F01_v04_r2','U24'),('F01_v04_r3','R05'),('F01_v04_r3','R06'),('F01_v04_r2','U31')]:
 t['recommended_changes'] += [change(run,uid,'proposition.decision_object_id',None),change(run,uid,'proposition.identity_evidence',[])]
for run,uid in [('F01_v04_r3','R05'),('F01_v04_r3','R06'),('F01_v04_r1','S32'),('F01_v04_r2','U31')]:
 t['recommended_changes'] += [change(run,uid,'institution.recognition[0].object_id',None),change(run,uid,'institution.recognition[0].identity_evidence',[])]
for run,uid in [('F01_v04_r3','R06'),('F01_v04_r1','S32'),('F01_v04_r2','U31')]:
 for p,v in [('kind','endorsement'),('mode','ordinary_assent'),('target','this_proposition'),('basis','context_inferred')]: t['recommended_changes'].append(change(run,uid,'institution.recognition[0].'+p,v))
 t['recommended_changes'].append(change(run,uid,'institution.recognition[0].rationale','Tentative assent identifies the recurring retention floor in its wallet-testing context. A canonical numbered criterion ID is inapplicable; #26586 identifies the episode only. Expectation recognition and narrower principle-level assent remain alternatives.'))
 t['recommended_changes'].append(change(run,uid,'institution.standing_profile.recognition','none'))
T.append(t)
t=topic('D02',
 'The later open-and-rebase suggestion maintains the method but does not repeat the earlier stopping condition. Narrow S13 recognition to broader_principle. Prefer same_actor_only wherever an attributable same_actor_restatement is retained, including the review-now strategy: the codebook expressly assigns same-actor events that profile, and does not make interpersonal recognition or established obligation prerequisites. This summary records maintained personal commitment, not recognition by another participant. The existing S13-to-S22 uptake direction can remain, with its limited response rationale.',
 'The strongest profile alternative is none for the partial open-PR event, if the summary is restricted to full-proposition recognition. That restriction is less clearly stated for recognition than for application. The review-now restatement is materially closer to its complete focal intention and therefore supplies a stronger case for same_actor_only.',
 'No uncertainty permits reinstating the omitted dependent-PR stopping condition or treating either repetition as interpersonal support. The scope of the profile for broader-target same-actor events remains a convention ambiguity.',
 [('pr26586:comments:6',"until there's another PR that needs it"),('pr26586:comments:15','leave the PR open and occasionally rebase it'),('pr7819:comments:2',"I'm working on the replacement GUI process but this can be reviewed already.")])
t['recommended_changes'].append(change('F01_v04_r1','S13','institution.recognition[0].target','broader_principle'))
t['recommended_changes'].append(change('F01_v04_r1','S13','institution.recognition[0].rationale','The same actor maintains the open-PR method; the later suggestion does not repeat the until-another-PR-needs-it condition.'))
for run,uid in [('F01_v04_r1','S13'),('F01_v04_r3','C11'),('F03_v04_r1','U03'),('F03_v04_r2','F03-U03'),('F03_v04_r3','F03-U04')]: t['recommended_changes'].append(change(run,uid,'institution.standing_profile.recognition','same_actor_only'))
T.append(t)
t=topic('D03',
 'Prefer observed application of the requested resulting spelling. The added release-note heading and matching integrated revision establish that artifact without reconstructing the earlier typo or attributing causation. The checkbox evidence is different: it establishes a prepared checkbox artifact but not every placement and functional qualification of the complete proposition. Prefer unresolved complete application, while preserving the narrower artifact observations already recorded in outcomes. An unmerged patch can still be observed; lack of integration alone is not a reason to deny observation of a proposed artifact.',
 'A transformation-specific spelling interpretation can retain unresolved application of the historical correction operation. It should not displace the separately observable resulting identifier. For the checkbox, none is a defensible no-positive-application summary, but unresolved communicates the partial evidence and outstanding qualifications more accurately.',
 'The spelling history and exact checkbox placement remain unverified. No new partial-application category or before-and-after requirement should be added to v0.4.',
 [('pr14441:review_comments:0','Should be `listtransactions` with `s`.'),('pr14441:patch:0','+`listtransactions` label support'),('pr14441:supplement_metadata','"merged": true'),('pr7819:patch:0','<widget class="QCheckBox" name="optInRBF">'),('pr7819:body','next to "Add Recipient"')])
t['recommended_changes'] += [change('F02_v04_r1','F02_S01','institution.application_evidence[1].status','observed'),change('F02_v04_r1','F02_S01','institution.application_evidence[1].rationale','The integrated artifact contains the requested complete identifier. Observation concerns resulting spelling, not the unidentified earlier typo, transformation chronology, or causal response.'),change('F02_v04_r1','F02_S01','institution.standing_profile.application','both')]
checkbox='The retained proposed artifact establishes a checkbox, but complete application, including the specified placement, remains unresolved. The unmerged status limits integration claims; it does not negate observation of the prepared artifact.'
t['recommended_changes'].append(change('F03_v04_r1','U01','institution.application_evidence[0].rationale',checkbox))
a=json.loads(json.dumps(unit('F03_v04_r1','U01')['institution']['application_evidence'][0]));a['rationale']=checkbox
t['recommended_changes'] += [change('F03_v04_r2','F03-U01','institution.application_evidence',[a]),change('F03_v04_r2','F03-U01','institution.standing_profile.application','unresolved')]
T.append(t)
t=topic('D04',
 'Prefer context-inferred reported application for the three release-note suggestions. The author attributes the update to the reviewer’s changes, and the reviewer identifies the suggested release-note updates. This is an intelligible collective report about those suggestions; reporting need not individually enumerate every item. It does not resolve the isolated fixed or Both replies, verify verbatim implementation, or prove adoption of every rationale. By contrast, rebasing on master neither names nor establishes the after-#26589 condition. Retain that broader rebase report and mark complete conditional application unresolved.',
 'A broader_proposal target for the aggregate report is defensible where collective reference is considered insufficient to identify individual suggestions. This is a genuine scope interpretation, not necessarily a substantive error. Its cautiousness alone does not make it preferable.',
 'The individual reply antecedents, the omitted compatibility rationale, and the dependency chronology remain unverified. Reported and observed application must retain their distinct evidentiary meanings.',
 [('pr14441:comments:0',"I've updated the PR with your changes."),('pr14441:reviews:4','release notes updates suggested above'),('pr26586:comments:13','Rebased on master'),('pr26586:comments:2','needs a rebase after #26589')])
for run,ids in [('F02_v04_r2',['S02','S03','S05']),('F02_v04_r3',['F02-S01','F02-S02','F02-S04'])]:
 for uid in ids:
  u=unit(run,uid)
  for i,a in enumerate(u['institution']['application_evidence']):
   if a['status']=='reported':
    t['recommended_changes'].append(change(run,uid,f'institution.application_evidence[{i}].target','this_proposition'))
    t['recommended_changes'].append(change(run,uid,f'institution.application_evidence[{i}].rationale','The attributed aggregate report contextually includes this release-note suggestion; no individual reply pairing or exact completion of every offered phrase is verified.'))
  t['recommended_changes'].append(change(run,uid,'institution.standing_profile.application','both'))
for run,uid in [('F01_v04_r1','S09'),('F01_v04_r3','C03')]:
 a=json.loads(json.dumps(unit(run,uid)['institution']['application_evidence']))
 b=json.loads(json.dumps(unit('F01_v04_r2','U08')['institution']['application_evidence'][0])); a.append(b)
 t['recommended_changes'] += [change(run,uid,'institution.application_evidence',a),change(run,uid,'institution.standing_profile.application','unresolved')]
a=json.loads(json.dumps(unit('F01_v04_r2','U08')['institution']['application_evidence']));a.append(json.loads(json.dumps(unit('F01_v04_r1','S09')['institution']['application_evidence'][0])))
t['recommended_changes'].append(change('F01_v04_r2','U08','institution.application_evidence',a))
T.append(t)
t=topic('D05',
 'Prefer undetermined institutional type with norm_candidate retained for both rebase formulations. A pragmatic maintenance request is supported, but these words alone do not discriminate a social expectation from a technical condition for maintaining the contribution. Recommendation is a reasonable pragmatic force; unresolved force remains appropriate when the literal technical-necessity reading is focal. The absence of authority defeats a rule-candidate inference, but cannot itself decide between a proposed norm and an ordinary engineering request.',
 'The strongest alternative is norm_candidate: an elliptical reviewer demand can express locally expected contributor conduct even without repetition or wider assent. Requiring a recurring or already shared expectation would add a criterion that v0.4 explicitly does not require.',
 'Retain the type ambiguity rather than treating either interpretation as established by needs. No executed rebase, institutional obligation, or authority follows merely from the phrasing.',
 [('pr7819:comments:7','Needs rebase.'),('pr26586:comments:2','Meanwhile it needs a rebase after #26589.')])
for run,uid in [('F03_v04_r1','U24'),('F03_v04_r2','F03-U17'),('F03_v04_r3','F03-U25'),('F01_v04_r1','S09'),('F01_v04_r2','U08'),('F01_v04_r3','C03')]:
 t['recommended_changes'] += [change(run,uid,'institution.type','undetermined'),change(run,uid,'institution.type_alternatives',['norm_candidate'])]
t['recommended_changes'].append(change('F03_v04_r1','U24','institution.rationale','The technical maintenance request permits a proposed social-expectation reading, but does not distinguish that reading from one-off engineering necessity; recurrence or prior sharing is not required for norm_candidate.'))
T.append(t)
t=topic('D06',
 'Two analytical layers should remain explicitly linked. For the embedded add-every-release instruction and script-edit action, I prefer operational targets with collective-choice observed deliberation. For the constitutive up-to-the-developer allocation, I prefer a collective-choice target: it proposes who will select releases under a recurring arrangement. A pragmatic developer-chooses representation can instead target the resulting operational conduct. These differences should be explained through the selected proposition rather than labeled as disagreement about authority.',
 'Treating the whole design proposal as choosing a recurring testing arrangement supports collective_choice for both target and observation. Conversely, ordinary engineering deliberation remains an operational observation alternative. The source does not uniquely settle whether every technical selection arrangement is institutional at that layer.',
 'Constitutive parsing does not imply constitutional power. No statement allocates control over Bitcoin network adoption. Both layers are supportable within v0.4; linked explanations are preferable to uniform labels imposed without changing focal meaning.',
 [('pr26586:comments:4','we should add every major release'),('pr26586:comments:10',"In that case it's up to the developer which previous releases they want to test.")])
for uid in ['S10','S16']:
 t['recommended_changes'] += [change('F01_v04_r1',uid,'statement_target_level','operational'),change('F01_v04_r1',uid,'target_level_alternatives',['collective_choice'])]
t['recommended_changes'] += [change('F01_v04_r3','C17','statement_target_level','collective_choice'),change('F01_v04_r3','C17','target_level_alternatives',['operational']),change('F01_v04_r1','S17','target_level_alternatives',['operational'])]
for uid in ['U15','U16']:
 t['recommended_changes'] += [change('F01_v04_r2',uid,'observed_action_level','collective_choice'),change('F01_v04_r2',uid,'observed_level_alternatives',['operational'])]
for run,uid in [('F01_v04_r1','S10'),('F01_v04_r1','S16'),('F01_v04_r3','C17'),('F01_v04_r1','S17'),('F01_v04_r2','U15'),('F01_v04_r2','U16')]:
 t['recommended_changes'].append(change(run,uid,'level_rationale','The embedded contribution or testing action is operational; proposing its recurring selection arrangement is collective choice. The constitutive developer-discretion reading targets that arrangement, while a pragmatic choose-action reading targets operational conduct. The visible exchange deliberates the arrangement, with ordinary engineering review retained as an alternative.'))
T.append(t)
t=topic('D07',
 'Q019: for an offered checkbox proposal, the exposure objection challenges its readiness premise, so prefer this_proposition and dispute_present true. A challenge need not deny the physical checkbox to contest offering it under the stated conditions. Q038: retain focal dispute over the specialness justification, preferably premise. Q039: retain the challenge to the explicitly attached miniscript rationale, without inferring #25717 contents. Q040: a proposed redesign addresses the burden of the current requirement but does not refute its current technical truth; prefer a broader-proposal application challenge and no focal dispute. Q052: the fee-only alternative does not dispute the historical attempt.',
 'For Q019, a strictly artifact-descriptive focal proposition supports broader_proposal and false. For Q040, a prospective challenge to continued application can support true if that prospective layer is explicit. These are bounded focal-object alternatives, not opposing facts.',
 'The unobserved future workflow and proposed redesign remain unadopted possibilities. No disagreement with past work or actual implementation should be inferred from an alternative future method.',
 [('pr7819:comments:0','Not sure it makes sense to expose this until the wallet actually _can_ do replacement...'),('pr26586:review_comments:2',"I don't think 24.x is special to 23.x at all"),('pr26586:comments:5',"doesn't test watch-only miniscript support"),('pr26586:comments:10','Instead of hardcoding the version numbers'),('pr7819:comments:3','But maybe we should just focus on increasing the fees?')])
for run,uid in [('F03_v04_r1','U01'),('F03_v04_r2','F03-U01'),('F03_v04_r3','F03-U01')]:
 t['recommended_changes'] += [change(run,uid,'institution.challenges[0].aspect','premise'),change(run,uid,'institution.challenges[0].target','this_proposition'),change(run,uid,'institution.dispute_present',True),change(run,uid,'institution.challenges[0].rationale','The objection questions the readiness premise of offering this checkbox without replacement capability; it does not deny the artifact description.')]
t['recommended_changes'].append(change('F01_v04_r1','S28','institution.challenges[0].aspect','premise'))
t['recommended_changes'] += [change('F01_v04_r3','C15','institution.challenges[0].target','broader_proposal'),change('F01_v04_r3','C15','institution.dispute_present',False),change('F01_v04_r3','C15','institution.challenges[0].rationale','The prospective redesign addresses the burden of the broader test arrangement; it does not contest the stated requirement under the current fixed-list design.')]
T.append(t)
t=topic('D08',
 'Reverse the separate-cleanup uptake relation to initiating proposal U30 followed by response U33. For the quoted cost-growth question, prefer clarifies from the pruning option to the concern: the reply directly addresses an append-only premise without requiring an inferred request. For release-risk speculation followed by hold-off assent, prefer a contextual clarifying response about intended handling, with the weak thread evidence stated. No relation establishes that a delay or pruning occurred.',
 'Uptake remains defensible when the cost question is reconstructed as a request for a removal plan, or the release concern as an implicit delay proposal. That reconstruction must be explicit. Context record status alone does not prove that no pragmatic request occurred, but neither does a responsive utterance automatically establish one.',
 'The direction of P04 is decided by v0.4. The other relation types remain interpretive; quotation establishes response correspondence more strongly in Q042 than the unthreaded sequence establishes it in Q043.',
 [('pr26586:review_comments:1','so someone could do that in a separate pull'),('pr26586:review_comments:2',"but I think that's outside of scope for this PR."),('pr26586:comments:8','We can remove intermediate releases at some point.'),('pr26586:comments:2','Sounds good to hold off a bit.')])
t['recommended_changes'] += [change('F01_v04_r2',None,'relations[24].from_unit_id','U30'),change('F01_v04_r2',None,'relations[24].to_unit_id','U33')]
for run,idx,fr,to in [('F01_v04_r3',11,'C13','C12'),('F01_v04_r1',8,'S14','C07'),('F01_v04_r2',18,'U13','C05'),('F01_v04_r3',1,'C02','C01')]:
 for p,v in [('type','clarifies'),('from_unit_id',fr),('to_unit_id',to),('basis','context_inferred')]:t['recommended_changes'].append(change(run,None,f'relations[{idx}].'+p,v))
 t['recommended_changes'].append(change(run,None,f'relations[{idx}].rationale','The later statement clarifies a possible response to the concern. An inferred initiating request would instead support uptake; no adoption, implementation, or causal effect is established.'))
T.append(t)
t=topic('D09',
 'Retain the bot’s announced reaction-to-next-update consequence, but leave the software object unresolved. The pronoun it is an explicit grammatical object; its referent is not therefore explicit. Review is a plausible antecedent, while comment or displayed listing cannot be excluded from this retained wording. The known PR discussion ID does not resolve which software object the bot would ignore.',
 'The incorrectly listed review is the strongest ordinary-language reading, and can be recorded as an alternative rather than asserted categorically. A specific implementation interpretation would require evidence absent from the packet.',
 'No reaction, update, suppression, executed sanction, or implemented governance consequence is observed. Preserve that limit alongside the conditional statement.',
 [('pr26586:comments:0','If your review is incorrectly listed, please react with 👎 to this comment'),('pr26586:comments:0','the bot will ignore it on the next update.')])
t['recommended_changes'] += [change('F01_v04_r2','U06','proposition.summary','After the requested 👎 reaction, the bot is said to ignore an unresolved referent on its next update.'),change('F01_v04_r2','U06','proposition.qualifiers[0].description','The announced consequence is conditional on the requested reaction; it may refer to the review, comment, or displayed listing.'),change('F01_v04_r2','U06','uncertainty_reason','The grammatical object it is explicit, but the retained text does not uniquely resolve its software referent.'),change('F01_v04_r2','U06','alternative_interpretation','The incorrectly listed review is the strongest linguistic antecedent; comment or displayed listing remain alternatives. The announced software response is not an observed action or sanction.')]
T.append(t)
t=topic('D10',
 'Prefer strategy_candidate for the specific-test preference: it articulates a testing method and examples, although no personal implementation commitment follows. Prefer strategy_candidate for the coupled EOL-drop and stored-wallet alternative, whose components jointly specify a replacement testing method. Splitting the clauses must preserve that coupling. Prefer norm_candidate for not rushing merges: it offers a reason for expected restraint in recurring integration conduct. None of these classifications establishes shared acceptance, authority, or implementation.',
 'Undetermined remains strongest for a mere evaluative preference or tentative one-off suggestion. The not-rushing sentence can likewise be read as optional practical advice rather than expected conduct. These alternatives remain stronger than inferring a rule from modal force or reducing every technical method to an institutional norm.',
 'V0.4 leaves a judgment boundary between articulated method, technical suggestion, and proposed social expectation. Preserve the preferred types and explicit alternatives without turning classifications into evidence of collective recognition.',
 [('pr26586:comments:5','I much more prefer specific tests'),('pr26586:comments:11','So maybe the EOL versions can be dropped and the qa-assets repo hosts some regtest wallets instead?'),('pr26586:comments:15','This can also be a reason to not rush merging new releases.')])
for uid in ['C09','C20','C21']:
 t['recommended_changes'] += [change('F01_v04_r3',uid,'institution.type','strategy_candidate'),change('F01_v04_r3',uid,'institution.type_alternatives',['undetermined']),change('F01_v04_r3',uid,'institution.rationale','The utterance articulates a preferred or tentative testing method; no expected duty, authorization, or implementation is established.')]
t['recommended_changes'] += [change('F01_v04_r3','C28','institution.type','norm_candidate'),change('F01_v04_r3','C28','institution.rationale','The speaker offers a reason for proposed restraint in recurring integration conduct; this candidate classification does not establish sharing or authority.')]
for run,uid in [('F01_v04_r3','C28'),('F01_v04_r1','S24'),('F01_v04_r2','U23')]: t['recommended_changes'].append(change(run,uid,'institution.type_alternatives',['undetermined']))
T.append(t)
out={'reviewer':'A','stage':'independent_initial','topics':T}
p=ROOT/'panel/A_initial.json'; p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
words=sum(len(t[k].split()) for t in T for k in ['preferred','alternatives','unresolved'])
print(str(p));print('Narrative words:',words);print('Topics:',len(T),'recommended field changes:',sum(len(t['recommended_changes']) for t in T))
