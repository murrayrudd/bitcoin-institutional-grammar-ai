import json, copy
from pathlib import Path
ROOT=Path('.')
def ann(run):return json.loads((ROOT/'inputs/runs'/run/'annotation.final.json').read_text())
def unit(run,uid):return next(u for u in ann(run)['units'] if u['unit_id']==uid)
def change(run,uid,path,value,kind='preferred_representation'):
 return {'run_id':run,'unit_id':uid,'path':path,'new_value':value,'recommendation_type':kind}
def src(s,q):return {'source_id':s,'quote':q}
def topic(t,p,a,s,u):return {'topic_id':t,'preferred':p,'alternatives':a,'recommended_changes':[],'source_basis':s,'unresolved':u}
t=[]
t.append(topic('D01',
 'Use null for unidentified follow-up contributions and for a general criterion without a canonical object; #26586 identifies the discussion episode. Sjors gives tentative ordinary assent. In context, his selected quotation can identify the wallet-retention proposal, including the non-substitution implication, without repeating every word. I therefore prefer this_proposition with context-inferred scope, while keeping recognition none under the ordinary-assent interpretation. The quotation identifies what he agrees with; it does not independently show that he treats it as a governing consideration. Correcting object identity is decided; the semantic breadth of assent is less certain.',
 'Broader-principle assent is defensible because the selected quotation omits the wallet-specific framing and explicit non-substitution clause. Tentative expectation recognition also remains possible; neither reading warrants repeated recognition, binding authority, or adoption.',
 [src('pr26586:comments:15','I tend to agree.'),src('pr26586:review_comments:1','in a separate pull'),src('pr26586:review_comments:2','rather than sacrificing one for another?')],
 'Null is inapplicable for the general criterion, unknown for a future contribution. An unidentified future proposal requires an unresolved target only when that proposal itself is the event target; semantically identified general-principle assent need not become unresolved.'))
c=t[-1]['recommended_changes']
for run,uid in [('F01_v04_r3','C30'),('F01_v04_r2','U24'),('F01_v04_r3','R05'),('F01_v04_r3','R06'),('F01_v04_r2','U31')]:
 c.extend([change(run,uid,'proposition.decision_object_id',None,'decided_correction'),change(run,uid,'proposition.identity_evidence',[],'decided_correction')])
for run,uid in [('F01_v04_r3','R05'),('F01_v04_r3','R06'),('F01_v04_r1','S32'),('F01_v04_r2','U31')]:
 c.extend([change(run,uid,'institution.recognition[0].object_id',None,'decided_correction'),change(run,uid,'institution.recognition[0].identity_evidence',[],'decided_correction')])
c.append(change('F01_v04_r3','R05','institution.recognition[0].rationale','Assent concerns general cleanup, whose separate contribution is unidentified; #26586 identifies only the episode.'))
for run,uid in [('F01_v04_r3','R06'),('F01_v04_r1','S32'),('F01_v04_r2','U31')]:
 for path,value in [('kind','endorsement'),('mode','ordinary_assent'),('target','this_proposition'),('basis','context_inferred'),('rationale','Tentative assent contextually identifies the wallet-retention criterion. Broader-principle scope and expectation recognition remain alternatives. A canonical object ID is inapplicable to this general criterion; the episode key is retained.')]:c.append(change(run,uid,'institution.recognition[0].'+path,value))
 c.append(change(run,uid,'institution.standing_profile.recognition','none'))

t.append(topic('D02',
 'The later open-PR proposal repeats a method, not the earlier condition until another PR needs it. Retarget S13 to broader_principle. For the review-now statement, the same author explicitly maintains the distinction between present review and unfinished replacement work. The frozen wording says same-actor events alone give same_actor_only; I prefer that profile for recorded restatements, including the partial open-PR method, with their narrower targets visible. This records maintained commitment, not interpersonal expectation recognition or full repetition of the condition.',
 'None is defensible for the partial-method case if the profile is interpreted as exclusively summarizing recognition of the complete focal proposition. Extending that restriction to the complete review-now restatement is less well supported.',
 [src('pr26586:comments:6',"until there's another PR that needs it"),src('pr26586:comments:15','leave the PR open and occasionally rebase it'),src('pr7819:comments:2','but this can be reviewed already')],
 'The same-actor summary rule does not expressly say whether broader-target events qualify. Preserve that convention ambiguity without silently importing the interpersonal expectation threshold.'))
c=t[-1]['recommended_changes']
c.append(change('F01_v04_r1','S13','institution.recognition[0].target','broader_principle','decided_correction'))
c.append(change('F01_v04_r1','S13','institution.recognition[0].rationale','The same actor repeats leaving the PR open, without repeating the until-another-PR-needs-it condition.'))
for run,uid in [('F01_v04_r1','S13'),('F01_v04_r3','C11'),('F03_v04_r1','U03'),('F03_v04_r2','F03-U03'),('F03_v04_r3','F03-U04')]:c.append(change(run,uid,'institution.standing_profile.recognition','same_actor_only'))

t.append(topic('D03',
 'The integrated release-note artifact directly shows the requested spelling. Observed application, explicitly limited to the resulting spelling, is justified without a new before-and-after requirement. The prior typo, correction chronology, and causal response remain unverified. For the checkbox, the supplied patches directly show a checkbox and connected sequence-setting code. Lack of merge does not negate this prepared artifact. However, placement next to Add Recipient is not shown by the retained patch context, so full-proposition application remains unresolved. Preserve the observed artifact in the existing outcome record rather than inventing a partial-application category.',
 'An artifact-limited observed checkbox event could be defensible if its scope is unmistakable. An unqualified observed profile for the complete proposition would obscure the unverified placement; none also hides an actually examined, relevant artifact.',
 [src('pr14441:patch:0','+`listtransactions` label support'),src('pr7819:patch:0','<widget class="QCheckBox" name="optInRBF">'),src('pr7819:body','next to "Add Recipient"')],
 'The schema lacks a partial application status. This representational limitation remains; integration is a separate disposition, not a universal prerequisite for observing an offered patch.'))
c=t[-1]['recommended_changes']
c.append(change('F02_v04_r1','F02_S01','institution.application_evidence[1].status','observed'))
c.append(change('F02_v04_r1','F02_S01','institution.application_evidence[1].rationale','The integrated artifact shows the requested complete spelling. The earlier typo and historical correction sequence remain unverified.'))
c.append(change('F02_v04_r1','F02_S01','institution.standing_profile.application','both'))
rationale='The retained patch shows the checkbox and connected sequence-setting code. Exact placement next to Add Recipient is not verified; full-proposition application remains unresolved. Unmerged status separately limits integration, not observation of the prepared artifact.'
c.append(change('F03_v04_r1','U01','institution.application_evidence[0].rationale',rationale))
record=copy.deepcopy(unit('F03_v04_r3','F03-U01')['institution']['application_evidence'][0]);record['rationale']=rationale
c.append(change('F03_v04_r2','F03-U01','institution.application_evidence',[record]))
c.append(change('F03_v04_r2','F03-U01','institution.standing_profile.application','unresolved'))

t.append(topic('D04',
 'The author explicitly reports updating the PR with the reviewer’s changes; the reviewer corroborates release-note updates suggested above. This supports context-inferred reported incorporation of the identified suggestions, not merely an unspecified PR update. Prefer this_proposition for that limited report, with independent patch observations kept separate. It does not resolve fixed or Both, verify every tentative phrase, or prove adoption of a rationale. Conversely, rebasing on master establishes only the reported rebase: no text connects it to satisfaction of after #26589. Retain the broad report and a separate unresolved full-condition assessment.',
 'Broader-proposal targeting of aggregate reports remains defensible under a stricter itemization reading. That ambiguity should not erase the positive correspondence between the named reviewer, changes, and corroborated release-note update.',
 [src('pr14441:comments:0',"I've updated the PR with your changes."),src('pr14441:reviews:4','release notes updates suggested above'),src('pr26586:comments:13','Rebased on master')],
 'Exact local reply pairings and the specified dependency event remain unknown. The omitted backward-compatibility phrase cannot be treated as verified verbatim implementation.'))
c=t[-1]['recommended_changes']
for run,uids,idx in [('F02_v04_r3',['F02-S01','F02-S02','F02-S04'],0),('F02_v04_r2',['S02','S03','S05'],1)]:
 for uid in uids:
  c.append(change(run,uid,f'institution.application_evidence[{idx}].target','this_proposition'))
  c.append(change(run,uid,f'institution.application_evidence[{idx}].rationale','The aggregate author report and corroborating reviewer report contextually include this suggestion. Exact reply pairing and every offered phrase remain unverified.'))
  c.append(change(run,uid,'institution.standing_profile.application','both'))
for run,uid in [('F01_v04_r3','C03'),('F01_v04_r1','S09')]:
 a=copy.deepcopy(unit(run,uid)['institution']['application_evidence']);r=copy.deepcopy(a[0]);r.update(status='unresolved',target='this_proposition',rationale='A rebase on master is reported; satisfaction of the after-#26589 condition is unresolved.');a.append(r)
 c.append(change(run,uid,'institution.application_evidence',a));c.append(change(run,uid,'institution.standing_profile.application','unresolved'))
a=copy.deepcopy(unit('F01_v04_r2','U08')['institution']['application_evidence']);r=copy.deepcopy(a[0]);r.update(status='reported',target='broader_proposal',rationale='The author reports rebasing this PR on master, without establishing the #26589 dependency.');a.append(r)
c.append(change('F01_v04_r2','U08','institution.application_evidence',a))

t.append(topic('D05',
 'Prefer undetermined for the terse rebase comments because their supplied context does not distinguish technical necessity from socially expected contribution work. Retain norm_candidate as a serious alternative: a local maintenance request can propose an expectation without repetition or prior acceptance. Recommendation and unresolved force are defensible parses; neither entails obligation. The r1 #7819 rationale should stop treating lack of a recurring expectation as decisive, because v0.4 permits proposed case-specific norms.',
 'Norm_candidate is reasonable when the review utterance itself is interpreted as an expectation directed at the contributor. Nothing supplies authorized merge-gate status, and the word needs cannot furnish that missing evidence.',
 [src('pr7819:comments:7','Needs rebase.'),src('pr26586:comments:2','it needs a rebase after #26589')],
 'The technical-need/social-expectation boundary cannot be made categorical without additional criteria. Preserve existing preferred labels with explicit alternatives rather than declaring either label erroneous.'))
c=t[-1]['recommended_changes']
for run,uid in [('F03_v04_r1','U24'),('F01_v04_r3','C03'),('F01_v04_r1','S09'),('F01_v04_r2','U08')]:c.append(change(run,uid,'institution.type_alternatives',['norm_candidate'],'retain_alternative'))
c.append(change('F03_v04_r1','U24','institution.rationale','The comment permits technical-necessity and local expected-conduct readings; supplied context does not select one. A proposed norm need not already recur or be shared.'))

t.append(topic('D06',
 'Keep operational performance and choosing a recurring arrangement as explicitly linked analytical layers. Adding releases or selecting locally available test versions describes operational conduct; proposing that these become the recurring selection arrangement supports collective-choice analysis. The developer-choice sentence preserves conditional allocation under either constitutive or pragmatic regulative grammar. The selected level must follow the stated focal proposition, not a general rule that all recurring code behavior is governance. Existing rationales mostly identify their layers; do not overwrite their differences with a single level.',
 'Ordinary engineering review remains a supported alternative for the directory-loop exchange. Collective-choice deliberation is stronger for the explicit every-major-release criterion, but still proves neither adoption nor power allocation above testing conduct.',
 [src('pr26586:comments:10',"In that case it's up to the developer"),src('pr26586:comments:4','we should add every major release')],
 'v0.4 allows both editorial/proposal and embedded-conduct layers. Comparisons must state which is focal; no constitutional or network-authority conclusion follows.'))
c=t[-1]['recommended_changes']
for uid in ['S17','S10']:
 c.append(change('F01_v04_r1',uid,'target_level_alternatives',['operational'],'retain_alternative'))
c.append(change('F01_v04_r1','S17','observed_level_alternatives',['operational'],'retain_alternative'))
c.append(change('F01_v04_r1','S17','level_rationale','The focal analysis is the proposal to choose a recurring developer-selection arrangement, conditional on the directory loop. Its embedded act of choosing test versions is operational; ordinary engineering review remains an alternative observed layer.'))

t.append(topic('D07',
 'Q019: for the offered checkbox feature, the exposure objection challenges its readiness premise, so prefer this_proposition and dispute true; it does not deny the artifact. Q038: retaining both versions despite no specialness challenges the explanation requirement’s premise, not merely its wording. Q039: the miniscript objection challenges that attached rationale only; it cannot adjudicate unseen #25717 or every reason to add v24. Q040: a future directory-loop redesign does not falsify the present fixed-list prerequisite; prefer no identified challenge to the present technical claim. Q052: prospective fee-only self-questioning leaves the historical additional-output attempt uncontested. Its broader scope alternative can remain visible.',
 'A literal checkbox-presence report supports broader-proposal targeting and false dispute; make that focal layer explicit. The directory-loop response can alternatively challenge continued application of the prerequisite if the claim is construed as ongoing, rather than current-implementation necessity.',
 [src('pr7819:comments:0','Not sure it makes sense to expose this'),src('pr26586:review_comments:2',"I don't think 24.x is special"),src('pr26586:comments:5',"doesn't test watch-only miniscript support"),src('pr7819:comments:3','But maybe we should just focus on increasing the fees?')],
 'The substantive targets, not Boolean agreement, carry the result. Readiness, a particular technical premise, continued applicability, and future scope are distinct disputes.'))
c=t[-1]['recommended_changes']
for run,uid in [('F03_v04_r1','U01'),('F03_v04_r2','F03-U01')]:
 c.append(change(run,uid,'institution.challenges[0].target','this_proposition'))
 c.append(change(run,uid,'institution.dispute_present',True))
 c.append(change(run,uid,'institution.challenges[0].rationale','The offered feature is questioned on readiness grounds before replacement capability exists; the presence of the checkbox artifact is not disputed.'))
c.append(change('F03_v04_r3','F03-U01','institution.challenges[0].aspect','premise'))
c.append(change('F01_v04_r1','S28','institution.challenges[0].aspect','premise'))
c.append(change('F01_v04_r3','C15','institution.challenges[0].target','unresolved'))
c.append(change('F01_v04_r3','C15','institution.challenges[0].rationale','The future redesign avoids continued fixed-list necessity; it does not contest the present implementation claim. A challenge to continued applicability is an alternative reading.'))
c.append(change('F01_v04_r3','C15','institution.dispute_present',False))

t.append(topic('D08',
 'Reverse the cleanup uptake link: proposal U30 precedes response U33 in the relation’s semantic direction. For the quoted cost-growth concern, prefer clarifies from the pruning response to the concern because the initiating unit remains context and makes no explicit request. For release-withdrawal speculation, prefer temporal linking to the separate pause proposal: the frozen timestamps establish order, while reliable reply threading and an initiating delay request are absent. Preserve the topical connections without implying implementation or causation.',
 'The cost question can pragmatically invite a plan; an uptake link is defensible if that invitation is stated explicitly. Sounds good also supports an implicit-invitation reading, but its exact initiating proposal remains less securely identified.',
 [src('pr26586:review_comments:1','in a separate pull'),src('pr26586:comments:8','We can remove intermediate releases at some point.'),src('pr26586:comments:2','Sounds good to hold off a bit.')],
 'Direction is a decided convention correction. Uptake versus clarifies or temporal remains a contextual interpretation; no formal hold, release withdrawal, or completed pruning is observed.'))
c=t[-1]['recommended_changes']
c.extend([change('F01_v04_r2',None,'relations[24].from_unit_id','U30','decided_correction'),change('F01_v04_r2',None,'relations[24].to_unit_id','U33','decided_correction')])
for run,idx,fr,to in [('F01_v04_r3',11,'C13','C12'),('F01_v04_r1',8,'S14','C07'),('F01_v04_r2',18,'U13','C05')]:
 for path,value in [('type','clarifies'),('from_unit_id',fr),('to_unit_id',to),('rationale','The pruning possibility clarifies the quoted append-only cost concern; an implicit invitation is a retained uptake alternative.')]:c.append(change(run,None,f'relations[{idx}].{path}',value))
c.append(change('F01_v04_r3',None,'relations[1].type','temporal'))
c.append(change('F01_v04_r3',None,'relations[1].rationale','Frozen timestamps place speculation at 2022-11-28T08:12:21+00:00 and the pause proposal at 13:32:40+00:00. Sequence is context-inferred; an initiating request and causal response remain unverified.'))

t.append(topic('D09',
 'Keep the literal object it and qualify its referent. The likely review interpretation is an inference; comment or displayed-listing interpretations remain possible from the text alone. The bot announces a conditional next-update effect after a reaction to this comment. This supplies neither execution nor a uniquely identified internal software object. Correct categorical referent claims wherever they are repeated, including summary, qualifier, institutional rationale, and target-activity description.',
 'The incorrectly listed review is linguistically plausible as the antecedent and may remain the preferred gloss, but no supplied implementation evidence eliminates the comment/listing alternatives.',
 [src('pr26586:comments:0','the bot will ignore it on the next update.')],
 'The underlying software referent is agreed uncertainty. Grammatical Bdir it is explicit even though its referent is unresolved; do not turn referent uncertainty into an inferred-object-role correction.'))
c=t[-1]['recommended_changes'];run='F01_v04_r2';uid='U06'
summary='The bot announces that it will ignore an unresolved review/comment/listing referent on the next update after the requested reaction.'
for path,value in [('proposition.summary',summary),('proposition.qualifiers[0].description','The consequence follows the requested reaction. It likely refers to the mislisted review, but the comment or displayed listing cannot be excluded.'),('institution.rationale','An announced conditional bot procedure with unresolved software referent; authority, use, and interpersonal recognition are not established.'),('level_evidence.target_activity',summary),('uncertainty_reason','The retained text does not distinguish the review, comment, or displayed listing as the software object ignored.')]:c.append(change(run,uid,path,value,'decided_correction'))

t.append(topic('D10',
 'Prefer strategy_candidate for the specific-test preference: it identifies a testing approach and recoverable examples, rather than only an unexplained edit. The coupled EOL-drop/retained-wallet proposal more clearly articulates means for prioritizing old-wallet loading; preserve both halves and their substitution relation. Neither method requires a firm personal commitment under v0.4. Prefer norm_candidate for not rushing new-release merges when read as proposed recurring restraint, with undetermined retained for a case-specific timing rationale. The stated merging action is explicit even though recommendation force is inferred; use literal parse for that action rather than inventing avoid-rushing roles.',
 'Specific-test preference can remain an engineering preference without enough method articulation; undetermined is defensible. The restraint sentence can give a possible reason without asserting expected conduct. None of these type labels demonstrates shared norms or implementation.',
 [src('pr26586:comments:5','I much more prefer specific tests'),src('pr26586:comments:11','the qa-assets repo hosts some regtest wallets instead?'),src('pr26586:comments:15','a reason to not rush merging new releases')],
 'Type thresholds leave bounded interpretation choices; literal action versus inferred recommendation force is separately governed by the existing parsing convention.'))
c=t[-1]['recommended_changes']
for uid in ['C09','C20','C21']:
 c.append(change('F01_v04_r3',uid,'institution.type','strategy_candidate'))
 c.append(change('F01_v04_r3',uid,'institution.type_alternatives',['undetermined'],'retain_alternative'))
 c.append(change('F01_v04_r3',uid,'institution.rationale','An articulated testing method without demonstrated duty; an engineering-preference reading remains possible.'))
c.append(change('F01_v04_r3','C28','institution.type','norm_candidate'))
for run,uid in [('F01_v04_r3','C28'),('F01_v04_r1','S24'),('F01_v04_r2','U23')]:c.append(change(run,uid,'institution.type_alternatives',['undetermined'],'retain_alternative'))
c.append(change('F01_v04_r3','C28','institution.rationale','A proposed restraint on recurring merge timing; a case-specific reason without expected duty remains an alternative.'))
c.append(change('F01_v04_r1','S24','parse_mode','literal','decided_correction'))
c.append(change('F01_v04_r2','U23','parse_mode','literal','decided_correction'))
c.append(change('F01_v04_r2','U23','components',copy.deepcopy(unit('F01_v04_r3','C28')['components']),'decided_correction'))
result={'reviewer':'B','stage':'independent_initial','topics':t}
Path('panel/B_initial.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
texts=[]
for x in t:
 for k in ['preferred','alternatives','unresolved']:texts.append(x[k])
print('Topics:',len(t),'Narrative words:',len(' '.join(texts).split()),'Change objects:',sum(len(x['recommended_changes']) for x in t))
