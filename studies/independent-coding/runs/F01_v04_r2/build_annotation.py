from pathlib import Path
import json, hashlib
P=json.loads(Path('packet.json').read_text())
E={x['source_id']:x for x in P['entries']}
PR=P['pr_url']; COMMIT23='dba123167236a172d2d33861d58aa94a19729671'; COMMIT22='d8b705f1caeb3b4a6790cb26e4e5584ca791d965'; LAST='16624e6ff3af4429e571f7a606bbbcac336e067a'
A={'schema_version':'0.4','run_id':'F01_v04_r2','episode_id':'F01','packet_sha256':hashlib.sha256(Path('packet.json').read_bytes()).hexdigest(),'entry_screening':[],'units':[],'relations':[],'episode_summary':{'observed_outcomes':[],'mechanisms':[],'missing_evidence':[],'unresolved_questions':[]}}
U={}
def ev(s,q=None,start=0):
 t=E[s]['text']; q=t if q is None else q; i=t.index(q,start); return {'source_id':s,'span':{'start':i,'end':i+len(q),'quote':q}}
def ref(u): return {'source_id':u['source_id'],'span':u['span']}
def unit(n,s,q,summary='',typ='undetermined',force='recommendation',speech='proposed',parse='literal',scope='case_specific',target='operational',observed='operational',role='statement',alt='',uncert='',obj='AUTO',level='',parent=None,start=0):
 e=ev(s,q,start); non=role!='statement'; obj=E[s].get('object_id') if obj=='AUTO' else obj
 u={'unit_id':n,'source_id':s,'span':e['span'],'parent_unit_id':parent,'grammar':'not_institutional' if non else 'regulative','speech_act':speech,'scope':scope,'components':[],
 'institution':{'type':'not_applicable' if non else typ,'dispute_present':False,'rationale':summary if not non else 'Contextual or structural record; no independent institutional classification.','evidence':[e],'recognition':[],'authority_evidence':[],'standing_profile':{k:('not_applicable' if non else 'none') for k in ['documentary','recognition','application']},'documentary_support':[],'application_evidence':[],'challenges':[],'type_alternatives':[]},
 'statement_target_level':'not_applicable' if non else target,'observed_action_level':'not_applicable' if role=='container' else observed,
 'level_rationale':level or ('The focal act concerns ordinary contribution, testing, or review in this PR; no allocation of decision powers is established.' if not non else 'Visible review discourse or source quotation in an operational contribution episode; no independent governed activity is coded.'),
 'complexity_flags':['none'],'alternative_interpretation':alt,'confidence':'plausible' if (alt or uncert) else 'clear','uncertainty_reason':uncert,'record_role':role,'parse_mode':parse,'deontic_force':'nondeontic' if non else force,
 'presentation':{'quotation':'repeated' if role=='quotation' else 'none','markup':'plain','rationale':'Supplied plain prose; inline formatting does not alter the communicative act.'},'disposition_events':[],
 'proposition':None if non else {'summary':summary,'decision_object_id':obj,'domain':'Bitcoin Core previous-release compatibility testing and associated PR review','time_scope':('Retained body at supplied snapshot; original creation timestamp does not date every sentence.' if s=='pr26586:body' else 'Retained occurrence associated with '+str(E[s].get('timestamp'))+'; complete edit history is unavailable.'),'identity_evidence':[e] if obj else [],'qualifiers':[]},
 'target_level_alternatives':[],'observed_level_alternatives':[],
 'level_evidence':{'target_activity':'Not applicable to nonstatement record.' if non else summary,'observed_activity':('Structural grouping only.' if role=='container' else speech+' contribution/review discourse'),'arrangement':'Repository contribution, review, and compatibility-test maintenance; no project-wide authority inferred.','evidence':[e]}}
 if non: u['alternative_interpretation']=alt
 A['units'].append(u);U[n]=u;return u
def ctx(n,s,q=None,**kw):
 kw.setdefault('speech','asserted'); return unit(n,s,E[s]['text'] if q is None else q,role='context',force='nondeontic',**kw)
def quote(n,s,q,to,start=0):
 u=unit(n,s,q,role='quotation',speech='asserted',start=start);u['presentation']['rationale']='Block quotation repeating a supplied original; not an additional endorsement.'; rel(n,to,'quotes','explicit','Repeated attributed content corresponds to the supplied original.',[ref(u),ref(U[to])]);return u
def comp(n,sym,text,q=None,basis='explicit',role='local',note='',source=None,gov=None,start=None):
 u=U[n];s=source or u['source_id'];q=text if q is None else q
 st=(u['span']['start'] if s==u['source_id'] else 0) if start is None else start
 e=ev(s,q,st);g=ev(s,gov,0) if gov else ref(u)
 u['components'].append({'symbol':sym,'text':text,'basis':basis,'evidence':[e],'inference_note':note,'occurrence_role':role,'governing_span':g})
def qual(n,desc,es,attachment='scope_note',linked=None,rationale='Material qualification retained explicitly in the proposition scope.'):
 U[n]['proposition']['qualifiers'].append({'description':desc,'evidence':es,'attachment':attachment,'linked_unit_id':linked,'rationale':rationale})
def rel(f,t,typ,basis,why,es,logic='not_applicable'):
 A['relations'].append({'from_unit_id':f,'to_unit_id':t,'type':typ,'basis':basis,'rationale':why,'evidence':es,'logic_scope':logic})
def challenge(n,aspect,target,es,why):
 u=U[n];u['institution']['challenges'].append({'aspect':aspect,'target':target,'evidence':es,'rationale':why})
 if target=='this_proposition':u['institution']['dispute_present']=True
def recog(n,kind,target,mode,speaker,es,why,basis='context_inferred',obj=PR):
 U[n]['institution']['recognition'].append({'kind':kind,'target':target,'basis':basis,'evidence':es,'rationale':why,'mode':mode,'speaker_relation':speaker,'independence_key':PR if speaker!='not_applicable' else None,'object_id':obj,'identity_evidence':[ev('pr26586:supplement_metadata',PR)] if obj==PR else es})
def doc(n,coverage,es,why,source_date,fit='established',claim_date=None):
 U[n]['institution']['documentary_support'].append({'coverage':coverage,'claim_as_of':claim_date,'source_as_of':source_date,'date_basis':'pinned_revision','temporal_fit':fit,'evidence':es,'rationale':why});U[n]['institution']['standing_profile']['documentary']=coverage if fit=='established' else 'unresolved'
def application(n,status,target,es,why):
 U[n]['institution']['application_evidence'].append({'status':status,'target':target,'evidence':es,'rationale':why})
 if target=='this_proposition':
  old=U[n]['institution']['standing_profile']['application']; U[n]['institution']['standing_profile']['application']=status if old in ['none',status] else 'both' if {old,status}=={'reported','observed'} else 'unresolved'
def disp(n,kind,target,es,why,obj=PR,basis='explicit'):
 U[n]['disposition_events'].append({'kind':kind,'target':target,'basis':basis,'evidence':es,'rationale':why,'object_id':obj,'identity_evidence':[ev('pr26586:supplement_metadata',PR)] if obj==PR else es})
def part(text,es):return {'text':text,'evidence':es}
def outcome(parts):
 A['episode_summary']['observed_outcomes'].append({'claim':' '.join(x['text'] for x in parts),'claim_parts':parts,'evidence':sum([x['evidence'] for x in parts],[])})
def mechanism(category,parts,ids,status,alternative):
 A['episode_summary']['mechanisms'].append({'category':category,'claim':' '.join(x['text'] for x in parts),'claim_parts':parts,'evidence':sum([x['evidence'] for x in parts],[]),'unit_ids':ids,'status':status,'alternative_explanation':alternative})
# Body: recurrent method, distinct navigation, and negative task necessity.
s='pr26586:body'
unit('U01',s,'The same procedure as every release',"The author presents the current previous-release addition as repetition of the procedure used for every release.",typ='strategy_candidate',force='nondeontic',speech='asserted',parse='pragmatic',scope='general',alt='An elliptical description of the current patch, rather than an independently prescribed recurring method.',uncert='The omitted action is reconstructed from the PR title and the two cited predecessor patches; the body has no complete revision history.')
comp('U01','I','repeat the release-addition procedure','The same procedure as every release',basis='context_inferred',role='semantic_inference',note='The nominal assertion is reconstructed as repeating a method, not an explicit imperative.')
qual('U01','The current procedure is simpler because the author reports automatic fetching/building of necessary tags, removing manual CI/README tag-list edits.',[ev(s,'only a little simpler now: thanks to #25650, the previous release fetch script defaults to downloading/building the necessary tags, i.e. we don\'t need to extend the tag list in the CI scripts and test/README.md anymore.')])
qual('U01','The current contribution is the retained PR titled add v24.0.1; the title does not date the original wording.',[ev('pr26586:metadata','"title": "test: previous releases: add v24.0.1"')])
unit('U02',s,'see '+COMMIT23+' [v23.0] and '+COMMIT22+' [v22.0]','Readers are referred to the v23.0 and v22.0 predecessor commits.',typ='undetermined',alt='A bibliographic pointer rather than a meaningful institutional prescription. Both targets are preserved as one navigation action.')
comp('U02','I','see');comp('U02','Bdir',COMMIT23+' [v23.0] and '+COMMIT22+' [v22.0]')
unit('U03',s,"we don't need to extend the tag list in the CI scripts and test/README.md anymore.","The author says contributors no longer need to extend the tag list in the CI scripts and test/README.md because the fetch script now defaults to necessary tags.",force='no_obligation',speech='asserted',scope='general',alt='The negated need describes eliminated technical work, not an institutional exemption; nondeontic technical necessity is a defensible reading.')
for sym,txt in [('A','we'),('D',"don't need to"),('I','extend'),('Bdir','the tag list in the CI scripts and test/README.md'),('Cex','anymore')]:comp('U03',sym,txt)
qual('U03','The removal of manual work is attributed to #25650 and the script default, whose own patch and outcome are not supplied.',[ev(s,"thanks to #25650, the previous release fetch script defaults to downloading/building the necessary tags")])
rel('U03','U01','clarifies','explicit','The body expressly explains how the recurring release-addition procedure is now simpler.',[ev(s,"only a little simpler now: thanks to #25650, the previous release fetch script defaults to downloading/building the necessary tags, i.e. we don't need to extend the tag list in the CI scripts and test/README.md anymore.")])
# Bot instructions are instance-specific; the table is an echo, not recognition.
s='pr26586:comments:0'
unit('U04',s,'See [the guideline](https://github.com/bitcoin/bitcoin/blob/master/CONTRIBUTING.md#code-review) for information on the review process.','Readers should consult the linked guideline for information on the review process.',alt='Routine navigation; the link alone does not establish authority for any particular review requirement.',obj=None)
comp('U04','I','See');comp('U04','Bdir','[the guideline](https://github.com/bitcoin/bitcoin/blob/master/CONTRIBUTING.md#code-review)');comp('U04','Cex','for information on the review process')
U['U04']['proposition']['domain']='Review-process information navigation';U['U04']['proposition']['time_scope']='This retained bot-comment instance; mutable master link is not equated with the supplied pinned revision.'
unit('U05',s,'If your review is incorrectly listed, please react with 👎 to this comment','If their review is incorrectly listed, reviewers are asked to react with 👎 to this comment.',typ='strategy_candidate',alt='An automated correction method, not a demonstrated shared norm or binding obligation.')
for sym,txt in [('Cac','If your review is incorrectly listed'),('I','react'),('Cex','with 👎'),('Bdir','this comment')]:comp('U05',sym,txt)
unit('U06',s,'the bot will ignore it on the next update.','The bot is said to ignore the incorrectly listed review on the next update after the requested 👎 reaction.',typ='strategy_candidate',force='nondeontic',speech='asserted',alt='An announced software response, not a sanction or observed application.')
comp('U06','A','the bot');comp('U06','I','ignore');comp('U06','Bdir','it');comp('U06','Cex','on the next update')
qual('U06','The pronoun refers to the mislisted review; the consequence is conditional on the requested reaction.',[ref(U['U05'])],attachment='linked_unit',linked='U05')
for n in ['U04','U05','U06']:U[n]['template_note']='Likely reusable bot wording, coded only for this actual comment instance; the review table is not an independent endorsement.'
rel('U05','U06','O','explicit','The coordinated bot statement announces a procedural consequence of the requested correction reaction; no use or sanction is observed.',[ev(s,'If your review is incorrectly listed, please react with 👎 to this comment and the bot will ignore it on the next update.')])
# Initial delay and contest over release inclusion.
s='pr26586:comments:1';ctx('C01',s,alt='Speculation about wiping a buggy release could motivate waiting, but it is not itself a request to wipe or delay.')
s='pr26586:comments:2'
unit('U07',s,'Sounds good to hold off a bit.','Sjors recommends holding off on the current contribution for a bit.',alt='Assent to a delay, although the preceding comment only supplies a concern and no explicit delay request.')
comp('U07','I','hold off');comp('U07','Cex','a bit');qual('U07','The surrounding concern is a wallet bug and possible removal of the release, not an established integration ban.',[ref(U['C01'])])
unit('U08',s,'Meanwhile it needs a rebase after #26589.','Sjors says this PR needs a rebase after #26589.',speech='asserted',parse='pragmatic',force='unresolved',alt='Technical rebase necessity rather than an institutional duty; the exact event denoted by after #26589 is not supplied.',uncert='Rebase is a noun in the source; acting on the PR is reconstructed. The reference does not establish #26589 integration.')
comp('U08','I','rebase','a rebase',basis='context_inferred',role='semantic_inference',note='Nominal technical need reconstructed as the requested rebase action.')
comp('U08','Bdir','this PR','it',basis='context_inferred',role='semantic_inference',note='Literal subject it becomes the target of reconstructed rebase; source placement resolves it to this PR.')
comp('U08','Cac','after #26589');qual('U08','The rebase is proposed meanwhile, while the inclusion decision remains delayed.',[ev(s,'Meanwhile')])
s='pr26586:comments:3';ctx('C02',s,speech='reported_action' if False else 'asserted')
s='pr26586:comments:4'
unit('U09',s,'So I think we should add every major release.','Sjors proposes that contributors should add every major release to backwards compatibility tests.',typ='norm_candidate',scope='general',observed='collective_choice',level='The focal instruction governs operational release additions. The visible discussion deliberates over a recurring version-selection expectation, so observed action is collective choice; it does not establish adoption.',alt='A technical test-coverage strategy, or a proposal to choose the recurring inclusion procedure (collective-choice target), rather than an already shared norm.')
U['U09']['target_level_alternatives']=['collective_choice'];U['U09']['institution']['type_alternatives']=['strategy_candidate']
for sym,txt in [('A','we'),('D','should'),('I','add'),('Bdir','every major release')]:comp('U09',sym,txt)
qual('U09','The bounded purpose is preventing accidental cross-version breakage including wallet upgrades, consensus and p2p bugs; no claim is made that this particular test covers all those cases.',[ev(s,"one reason for the backwards compatibility tests is to ensure there's no accidental breakage between versions, including wallet upgrades, consensus and p2p bugs.")])
unit('U10',s,'Apart from that, #25717 alone should justify adding v24.0 (or whatever ends up widely available for download).','Sjors advances #25717 as sufficient reason to add v24.0, or whichever version becomes widely downloadable, to the current tests.',parse='pragmatic',alt='A reason supporting the current addition, not a separate recommendation; should governs justify and is not an explicit deontic over adding.')
comp('U10','I','add','adding',basis='context_inferred',role='semantic_inference',note='The recommendation is reconstructed from a claim that a reason justifies adding.')
comp('U10','Bdir','v24.0 (or whatever ends up widely available for download)',basis='explicit',note='The object of adding remains the target of the reconstructed add recommendation; the alternative downloadable version is retained.')
qual('U10','#25717 is the cited reason, not the object whose integration is claimed; the wallet miniscript example is attributed and qualified by last time I checked.',[ev(s,'#25717 alone should justify adding v24.0 (or whatever ends up widely available for download)'),ev(s,'On the wallet side this version added watch-only miniscript support (which last time I checked caused problems when downgrading).')])
# Specific test preference and low-cost rationale.
s='pr26586:comments:5'
ctx('C03',s,'Though, `test/functional/feature_backwards_compatibility.py` doesn\'t test watch-only miniscript support. I don\'t mind, but I am not too much a fan of a "general" compat test. It is likely so general that it can\'t catch any issues.')
unit('U11',s,'I much more prefer specific tests, like the ones you can find with `git grep -l skip_if_no_prev`','maflcko recommends specific compatibility tests, exemplified by those located with git grep -l skip_if_no_prev, in preference to the general test.',typ='strategy_candidate',parse='pragmatic',scope='general',observed='collective_choice',alt='An expression of methodological preference only; the inferred use action is not a stated duty.',level='The proposed method concerns operational testing. The visible comparison of general and specific test arrangements is deliberation over recurring testing choices.')
comp('U11','I','use','prefer',basis='context_inferred',role='semantic_inference',note='Preference is interpreted pragmatically as a recommended test method.')
comp('U11','Bdir','specific tests',basis='context_inferred',role='semantic_inference',note='The object of prefer becomes the object of reconstructed use, so its role is inferred despite exact words.')
qual('U11','The examples can be located with git grep -l skip_if_no_prev; the speaker does not supply an independent imperative to run it.',[ev(s,'like the ones you can find with `git grep -l skip_if_no_prev`')])
s='pr26586:comments:6'
quote('Q01',s,"> It is likely so general that it can't catch any issues.",'C03')
ctx('C04',s,"Probably not, but it's a low cost check.")
quote('Q02',s,"> doesn't test watch-only miniscript support",'C03')
unit('U12',s,"But we can also keep this PR open until there's another PR that needs it.",'Sjors offers keeping this PR open until another PR needs it as an alternative way to proceed.',typ='strategy_candidate',alt='Exploratory feasibility, not institutionally authorized permission; can does not establish a right to keep the PR open.')
for sym,txt in [('A','we'),('I','keep'),('Bdir','this PR'),('Cex',"open until there's another PR that needs it")]:comp('U12',sym,txt)
qual('U12','The offered alternative retains the reported value of rebasing: CI checks run again even while the PR is unmerged. The historical pattern is a participant report.',[ev(s,"We've previously piled several major releases this way. Back then it was more work to rebase than it is now. Every time it's rebased, the CI runs the checks again, so it's useful even in an unmerged state.")])
s='pr26586:comments:7';quote('Q03',s,"> Probably not, but it's a low cost check.",'C04');ctx('C05',s,'Not sure if it will stay low cost forever, if the matrix is append-only with no plan to remove some or all previous releases?',alt='An implied invitation to consider pruning is possible; preferred coding retains a cost challenge and question rather than inventing a request.')
s='pr26586:comments:8';quote('Q04',s,"> > Probably not, but it's a low cost check.",'C04');quote('Q05',s,'> Not sure if it will stay low cost forever, if the matrix is append-only with no plan to remove some or all previous releases?','C05')
unit('U13',s,'We can remove intermediate releases at some point.','Sjors offers removing intermediate releases at some future point.',scope='general',alt='A capability or possible mitigation rather than institutional permission or a committed pruning plan.',observed='collective_choice')
for sym,txt in [('A','We'),('I','remove'),('Bdir','intermediate releases'),('Cex','at some point')]:comp('U13',sym,txt)
s='pr26586:comments:9';quote('Q06',s,">Probably not, but it's a low cost check.",'C04');ctx('C06',s,"It's not low cost.")
unit('U14',s,'To run the test at all, you have to keep a built copy of every single release listed. (And no, guix static binaries aren\'t a good alternative.)','luke-jr says running the test requires keeping a built copy of every listed release, and rejects guix static binaries as a good substitute.',force='unresolved',speech='asserted',scope='general',alt='Literal technical prerequisite, not institutional obligation. The candidate is retained because have to can appear prescriptive; no authority or social expectation is supplied.')
for sym,txt in [('Cex','To run the test at all'),('A','you'),('D','have to'),('I','keep'),('Bdir','a built copy of every single release listed')]:comp('U14',sym,txt)
qual('U14','The rejection of guix static binaries is the speaker\'s qualified alternative assessment, not independently verified.',[ev(s,"(And no, guix static binaries aren't a good alternative.)")])
# Alternative technical arrangements, including bounded developer discretion.
s='pr26586:comments:10'
unit('U15',s,'Instead of hardcoding the version numbers in `feature_backwards_compatibility.py` we could have it loop over whatever is available under `releases/v*`.','Sjors proposes changing feature_backwards_compatibility.py from hardcoded version numbers to looping over whatever is available under releases/v*.',typ='strategy_candidate',parse='pragmatic',scope='general',observed='collective_choice',alt='An exploratory technical redesign, not an established duty or permission; could expresses possibility.')
comp('U15','A','we',basis='explicit',note='The explicit subject of have remains the configuring actor in reconstructed change; no occupational role is inferred.')
comp('U15','I','change','could have it loop over',basis='context_inferred',role='semantic_inference',note='Change is the reconstructed configuration action supplied by the instead-of comparison.')
comp('U15','Bdir','feature_backwards_compatibility.py','`feature_backwards_compatibility.py`',basis='context_inferred',role='semantic_inference',note='The file is originally the location of hardcoding; it becomes the target of the inferred change action.')
qual('U15','The replacement is specifically to loop over whatever is available under releases/v*, instead of hardcoding version numbers.',[ref(U['U15'])])
qual('U15','The default fetch script would still fetch all binaries; this proposal changes test selection rather than that default.',[ev(s,'The default of `test/get_previous_releases.py` would still to fetch all the binaries.')])
unit('U16',s,"In that case it's up to the developer which previous releases they want to test.",'Under the proposed available-directory loop, developers would choose which previous releases to test.',force='unresolved',speech='asserted',parse='pragmatic',scope='general',observed='collective_choice',alt='Technical user choice enabled by a configurable test, rather than institutionally allocated permission; a constitutive allocation-of-discretion parse is possible but lacks an independently established institutional arrangement.')
comp('U16','A','the developer',basis='context_inferred',role='semantic_inference',note='The person to whom the choice is up becomes actor of reconstructed choose.')
comp('U16','I','choose',"it's up to the developer",basis='context_inferred',role='semantic_inference',note='Choice is reconstructed from up to, not directly expressed as a verb.')
comp('U16','Bdir','which previous releases they want to test',basis='context_inferred',role='semantic_inference',note='The informational clause becomes the object of reconstructed choose.')
comp('U16','Cac','In that case');qual('U16','That case is the alternative directory-loop design in U15, and downloading all binaries remains the default.',[ref(U['U15']),ev(s,'The default of `test/get_previous_releases.py` would still to fetch all the binaries.')],attachment='linked_unit',linked='U15')
rel('U16','U15','clarifies','explicit','In that case states the developer-selection consequence of the proposed architecture; it is not independent evidence of authorized discretion.',[ref(U['U16']),ref(U['U15'])])
s='pr26586:comments:11'
unit('U17',s,'So maybe the EOL versions can be dropped','maflcko proposes possibly dropping EOL versions from these tests as part of a replacement using retained regtest wallets.',typ='strategy_candidate',scope='general',speech='question',observed='collective_choice',alt='An exploratory testing method, not an institutional permission or removal decision.')
comp('U17','I','dropped');comp('U17','Bdir','the EOL versions')
unit('U18',s,'and the qa-assets repo hosts some regtest wallets instead?','As the paired alternative to EOL versions, maflcko proposes that the qa-assets repository host some regtest wallets.',typ='strategy_candidate',scope='general',speech='question',observed='collective_choice',alt='Technical storage and test design, not the constitution of a new governance role.')
for sym,txt in [('A','the qa-assets repo'),('I','hosts'),('Bdir','some regtest wallets')]:comp('U18',sym,txt)
for n in ['U17','U18']:qual(n,'The stated priority is loading ancient wallets with modern versions rather than opening modern wallets with ancient EOL software; the proposal is tentative.',[ev(s,"I don't think it is too important that a modern wallet can be opened with an ancient EOL version. It seems more important to be able to load an ancient wallet with a modern version."),ev(s,'So maybe the EOL versions can be dropped and the qa-assets repo hosts some regtest wallets instead?')])
rel('U17','U18','AND','explicit','The source joins two replacement actions; neither is evidence that the other was implemented.',[ev(s,'So maybe the EOL versions can be dropped and the qa-assets repo hosts some regtest wallets instead?')],logic='actions')
ctx('C07',s,"In any case the test fails intermittently (#24400), so apart from obvious smoke test issues that happen on every iteration, I don't think anyone even looks into failures here.")
# Version update request and reports.
s='pr26586:comments:12'
unit('U19',s,'Noting that if this is still going ahead, it should be updated to use 24.0.1.','fanquake recommends updating this PR to use 24.0.1 if it is still proceeding.',speech='asserted',alt='A case-specific technical update recommendation, not a project-wide release-selection rule.')
for sym,txt in [('Cac','if this is still going ahead'),('Bdir','it'),('D','should'),('I','updated'),('Cex','to use 24.0.1')]:comp('U19',sym,txt)
s='pr26586:comments:13';ctx('C08',s,speech='reported_action' if False else 'asserted')
# An invitation has context beyond an isolated name.
s='pr26586:comments:14'
unit('U20',s,'Not sure what to do here. @Sjors?','fanquake invites Sjors to advise on how to proceed with this PR.',parse='pragmatic',speech='question',alt='A pure ping plus expression of uncertainty; the following tested ACK and advice makes a request-for-guidance reading plausible.',uncert='No explicit request verb or reliably reconstructed reply thread.')
comp('U20','A','Sjors','@Sjors',basis='context_inferred',role='semantic_inference',note='The named addressee is inferred as actor of the invitation to advise, not a literal subject of a verb.')
comp('U20','I','advise','Not sure what to do here. @Sjors?',basis='context_inferred',role='semantic_inference',note='The request action is reconstructed from uncertainty plus addressed question.')
comp('U20','Bdir','what to do here',basis='context_inferred',role='semantic_inference',note='The embedded informational clause is the target of reconstructed advice.')
s='pr26586:comments:15'
ctx('C09',s,'tACK 741908afc1f9ed2040c18667c75665b300c5dfe7\r\n\r\nI checked that it still works on top of current master. That said, there\'s no pressing reason to merge this.')
unit('U21',s,"As we've done before, we could just leave the PR open",'Sjors offers leaving this PR open, citing prior practice and absence of a pressing reason to merge.',typ='strategy_candidate',alt='A possible method rather than a promise or institutional authorization; the later merge does not demonstrate rejection of this general option.')
comp('U21','A','we',start=E[s]['text'].index('we could'));comp('U21','I','leave');comp('U21','Bdir','the PR');comp('U21','Cex','open')
qual('U21','The suggestion refers to prior practice and is paired with occasional rebasing, while acknowledging no pressing reason to merge.',[ref(U['C09']),ref(U['U21']),ev(s,'and occasionally rebase it.')])
unit('U22',s,'and occasionally rebase it.','Sjors offers occasionally rebasing the open PR as part of the same continuing method.',typ='strategy_candidate',alt='A possible method, not an obligation or report that all such rebases occurred.')
comp('U22','I','rebase');comp('U22','Bdir','it');comp('U22','Cex','occasionally')
qual('U22','Rebasing is coupled with leaving this PR open under the proposed method, and prior practice is reported.',[ref(U['U21'])],attachment='linked_unit',linked='U21')
rel('U21','U22','AND','explicit','Two independently executable actions are proposed together as an ongoing review method.',[ev(s,"As we've done before, we could just leave the PR open and occasionally rebase it.")],logic='actions')
quote('Q07',s,"> apart from obvious smoke test issues that happen on every iteration, I don't think anyone even looks into failures here",'C07')
unit('U23',s,'This can also be a reason to not rush merging new releases.','Sjors offers the reported weak investigation of intermittent failures as a reason not to rush merging additions of new releases.',typ='norm_candidate',parse='pragmatic',scope='general',observed='collective_choice',alt='A rationale about timing rather than a shared expected restraint; can expresses possible reasoning, not permission.')
comp('U23','I','avoid rushing','not rush merging',basis='context_inferred',role='semantic_inference',note='A restraint recommendation is reconstructed from a claim about a possible reason; negation is retained.')
comp('U23','Bdir','merging new releases',basis='context_inferred',role='semantic_inference',note='The merging act becomes the target of reconstructed avoid rushing.')
qual('U23','This refers to the immediately repeated failure-investigation qualification, not a claim that no failures receive attention.',[ref(U['Q07'])],attachment='linked_unit',linked='Q07')
qual('U23','Sjors attributes thorough checking to the PR at each rebase; this remains a participant report.',[ev(s,'This PR itself is where most of the thorough checking happens, at every rebase.')])
# Q08 is linked after the original inline proposal is represented below.
unit('U24',s,'In any case we can always prune versions in a followup.','Sjors offers pruning versions in a follow-up as an option alongside the present inclusion decision.',alt='Feasible later work rather than authorized discretion or a committed cleanup plan.')
for sym,txt in [('A','we'),('I','prune'),('Bdir','versions'),('Cex','in a followup')]:comp('U24',sym,txt)
qual('U24','Always expresses continued availability of the suggested option; no follow-up object or implementation is identified.',[ev(s,'can always prune versions in a followup')])
# Inline criteria and alternative requirements.
s='pr26586:review_comments:0'
unit('G01',s,E[s]['text'],role='container',speech='other')
unit('U25',s,'I think it only makes sense to add the latest release for each missing feature.','maflcko proposes adding only the latest release for each missing feature.',typ='norm_candidate',scope='general',speech='asserted',observed='collective_choice',parent='G01',alt='An articulated technical selection strategy rather than socially expected conduct; no rule-making authority is attributed.',level='The focal criterion governs operational choice of releases. The visible exchange deliberates over that recurring criterion, supporting collective-choice observed action.')
comp('U25','I','add');comp('U25','Bdir','the latest release');comp('U25','Cex','for each missing feature');qual('U25','Only limits the selection to the latest release for a missing feature; it does not mandate testing every released version.',[ev(s,'only makes sense to add the latest release for each missing feature')])
U['U25']['target_level_alternatives']=['collective_choice'];U['U25']['institution']['type_alternatives']=['strategy_candidate']
unit('U26',s,'So if you want to add 24.x, you will either need to remove 23.x','maflcko tells the contributor who wants to add 24.x to remove 23.x, as one alternative to explaining why 24.x is special.',typ='norm_candidate',force='obligation',speech='asserted',parent='G01',alt='A review recommendation or technical requirement rather than binding duty. Need does not establish institutional authority.',uncert='The force is an attributed conditional review requirement; no enforcement or veto power is supplied.')
for sym,txt in [('Cac','if you want to add 24.x'),('A','you'),('D','need to'),('I','remove'),('Bdir','23.x')]:comp('U26',sym,txt,start=(E[s]['text'].index('you will') if sym=='A' else None))
unit('U27',s,'or explain why 24.x is special','maflcko offers explaining why 24.x is special as the alternative to removing 23.x when adding 24.x.',typ='norm_candidate',force='obligation',speech='asserted',parent='G01',alt='An argumentative request to justify coverage rather than a binding rule; the two routes are not proven mutually exclusive.')
comp('U27','I','explain');comp('U27','Bdir','why 24.x is special')
comp('U27','A','you','you',basis='explicit',role='shared_scope',source=s,gov='So if you want to add 24.x, you will either need to remove 23.x or explain why 24.x is special',start=E[s]['text'].index('you will'),note='The explicit main-clause you is shared by the coordinated remove and explain predicates; it is not local to this child.')
comp('U27','D','need to',basis='explicit',role='shared_scope',source=s,gov='So if you want to add 24.x, you will either need to remove 23.x or explain why 24.x is special',start=0,note='The requirement operator governs both coordinated alternatives.')
comp('U27','Cac','if you want to add 24.x',basis='explicit',role='shared_scope',source=s,gov='So if you want to add 24.x, you will either need to remove 23.x or explain why 24.x is special',start=0,note='The explicit conditional governs both alternatives.')
for n,other in [('U26','U27'),('U27','U26')]:qual(n,'This is one of two alternative routes; either remove 23.x or explain why 24.x is special. Exclusive choice is not established.',[ref(U[other])],attachment='linked_unit',linked=other)
rel('U26','U27','OR','explicit','Either/or supplies alternative discharge routes but does not expressly forbid satisfying both.',[ev(s,'either need to remove 23.x or explain why 24.x is special')],logic='actions')
unit('U28',s,'see also '+LAST,'Readers are referred to the cited last-release compatibility-test commit.',parent='G01',obj='https://github.com/bitcoin/bitcoin/commit/'+LAST,alt='Navigation to a technical precedent does not make that precedent authoritative for this different test.')
comp('U28','I','see');comp('U28','Bdir',LAST)
# Related cleanup and scope.
s='pr26586:review_comments:1'
unit('U29',s,'Unrelated: The same goes for the other versions in this file','maflcko extends the latest-release-per-missing-feature criterion to other versions in this file, marking it unrelated to the immediate addition.',typ='norm_candidate',parse='pragmatic',scope='general',speech='asserted',observed='collective_choice',alt='An elliptical reminder of a technical strategy; the exact criterion is inferred from the preceding inline comment.')
comp('U29','I','apply the same release-selection criterion','The same goes',basis='context_inferred',role='semantic_inference',note='The explicit ellipsis is resolved to the preceding criterion, not a newly stated rule.')
comp('U29','Bdir','the other versions in this file',basis='context_inferred',role='semantic_inference',note='The prepositional scope becomes the target of inferred application.')
qual('U29','The inherited criterion is adding only the latest release for each missing feature.',[ref(U['U25'])],attachment='linked_unit',linked='U25')
qual('U29','Unrelated explicitly separates this extension from the current addition.',[ev(s,'Unrelated:')])
unit('U30',s,'so someone could do that in a separate pull','maflcko suggests that someone perform the corresponding cleanup in a separate pull request.',typ='strategy_candidate',parse='pragmatic',obj=None,alt='A suggested future task, not an identified proposal or obligation; no hypothetical follow-up disposition can be assigned.')
comp('U30','A','someone',basis='explicit',note='Someone is explicitly subject of do and remains actor in the reconstructed cleanup action.')
comp('U30','I','clean up','do',basis='context_inferred',role='semantic_inference',note='The otherwise underspecified do action is reconstructed from this file\'s version-selection criterion.')
comp('U30','Bdir','other-version selection','that',basis='context_inferred',role='semantic_inference',note='That refers to applying the criterion to the other versions; no separate PR identity is supplied.')
comp('U30','Cex','in a separate pull');qual('U30','Cleanup refers to other versions in this file under U29; it is explicitly outside the immediate task.',[ref(U['U29'])],attachment='linked_unit',linked='U29')
s='pr26586:review_comments:2'
quote('Q09',s,E[s]['text'].split('\r\n\r\n')[0],'G01')
unit('U31',s,"For these wallet backwards compatibility tests, wouldn't it make sense to always keep at least the recent major releases that haven't reached EOL yet as bare minimum rather than sacrificing one for another?",'theStack proposes always retaining at least recent major releases that have not reached EOL as a minimum in these wallet backwards compatibility tests, rather than replacing one with another.',typ='norm_candidate',scope='general',speech='question',observed='collective_choice',alt='A methodological test-coverage recommendation, not an established shared rule; question form conveys a proposed standard without an explicit deontic.',level='The proposed minimum governs operational selection of test versions. The visible disagreement deliberates over recurring retention criteria; a collective-choice target is also defensible.')
comp('U31','I','keep');comp('U31','Bdir',"at least the recent major releases that haven't reached EOL yet")
comp('U31','Cex','For these wallet backwards compatibility tests')
qual('U31','The minimum applies always, is a bare minimum, and rejects sacrificing one such release for another.',[ev(s,"always keep at least the recent major releases that haven't reached EOL yet as bare minimum rather than sacrificing one for another")])
qual('U31','The author expressly says 24.x need not be special relative to 23.x; the proposed benefit is verifying both versions rather than assuming equivalence.',[ev(s,"I don't think 24.x is special to 23.x at all, but I'd rather verify this assumption (in this case e.g., that wallets created on master can still be opened on both of these versions) rather than potentially miss out on either one of those cases.")])
U['U31']['target_level_alternatives']=['collective_choice'];U['U31']['institution']['type_alternatives']=['strategy_candidate']
unit('U32',s,"I'd rather verify this assumption (in this case e.g., that wallets created on master can still be opened on both of these versions) rather than potentially miss out on either one of those cases.",'theStack prefers verifying the assumption, for example that wallets created on master can still open on both 23.x and 24.x, rather than potentially missing either case.',typ='strategy_candidate',force='nondeontic',speech='asserted',alt='Rationale for the preceding retention proposal rather than a separate method; no claim that the test has actually verified the assumption is made.')
comp('U32','A','I',"I'd",note='The contracted first-person subject is explicit; the full contraction is anchored.')
comp('U32','I','verify');comp('U32','Bdir','this assumption')
qual('U32','The example assumption is that master-created wallets can still be opened on both versions; the antecedent explicitly compares 24.x with 23.x.',[ev(s,"I don't think 24.x is special to 23.x at all"),ev(s,'(in this case e.g., that wallets created on master can still be opened on both of these versions)')])
qual('U32','The preference is to avoid potentially missing either case, not an assertion of known version-specific incompatibility.',[ev(s,'rather than potentially miss out on either one of those cases.')])
ctx('C10',s,'ACK on cleaning up the releases list in general,')
unit('U33',s,"but I think that's outside of scope for this PR.",'theStack says general release-list cleanup should be outside this PR\'s scope.',typ='norm_candidate',parse='pragmatic',speech='asserted',alt='A constitutive description of proposal scope, or a simple description of intended patch content; preferred parse reconstructs a request to exclude cleanup from this contribution.')
comp('U33','I','exclude from this PR',"outside of scope for this PR",basis='context_inferred',role='semantic_inference',note='The scope assertion is reconstructed as conduct limiting the contribution; the negated inclusion is preserved.')
comp('U33','Bdir','general release-list cleanup',"that's",basis='context_inferred',role='semantic_inference',note='The literal subject that becomes the object of exclude; antecedent is the adjacent cleanup ACK.')
qual('U33','The exclusion concerns cleaning up the releases list in general, which the author endorses separately; it does not reject cleanup itself.',[ref(U['C10'])],attachment='linked_unit',linked='C10')
# Remaining quotation and explicit response in the later comment.
s='pr26586:comments:15';quote('Q08',s,"> wouldn't it make sense to always keep at least the recent major releases that haven't reached EOL yet ",'U31');ctx('C11',s,'I tend to agree.')
# Documentary context, standing, challenges, applications, and bounded dispositions.
for cid,sd in [(COMMIT23,'2022-05-06'),(COMMIT22,'2021-12-16')]:
 doc('U01','partial',[ev('commit:'+cid+':metadata','test: previous releases: add v'+('23.0' if cid==COMMIT23 else '22.0')),ev('commit:'+cid+':patch:2','# Add new version after each release:')], 'The supplied predecessor addition and source comment support repeated additions in two examples, not the claim of every release or continued standing at the retained-body date.',sd,'unresolved')
doc('U09','partial',[ev('commit:'+COMMIT23+':patch:2','# Add new version after each release:')],'The earlier source comment supplies a related addition expectation, but its every release wording and uncertain continuation do not establish this later every-major-release claim.','2022-05-06','unresolved','2022-11-29')
doc('U25','broader',[ev('commit:'+LAST+':metadata','In compatibility tests it makes sense to always use the last release without the new feature, as it is likely more in use than any even older previous release.')],'A contemporaneous pinned commit describes a similar selection rationale in other compatibility tests. It documents the broader principle, not authority or exact application to wallet tests.','2022-12-09','established','2022-12-09')
doc('U33','broader',[ev('guide:contributing','Patchsets should always be focused. For example, a pull request could add a\nfeature, fix a bug, or refactor code; but not a mixture.')],'The pinned guide documents a broader focus principle, not the exact boundary of this PR; its earlier revision does not establish uninterrupted standing at the December 11 claim.','2022-12-10','unresolved','2022-12-11')
challenge('U09','premise','this_proposition',[ref(U['C03']),ref(U['C05']),ref(U['U14'])],'The responses contest general-test value and the cost of continually adding listed releases, directly qualifying the proposed every-major-release expectation.')
challenge('U09','content','this_proposition',[ref(U['U25'])],'The latest-release-per-feature criterion offers a conflicting criterion for retaining releases in this same test discussion.')
challenge('U10','premise','this_proposition',[ref(U['C02']),ref(U['C03'])],'The NACK questions what differs in v24; maflcko specifically says this test does not cover the cited miniscript support. These are challenges to the proposed addition\'s reasons, not proven rejection.')
for n in ['U25','U26','U27']:
 challenge(n,'content' if n=='U25' else 'premise','this_proposition',[ref(U['U31']),ev('pr26586:review_comments:2',"I don't think 24.x is special to 23.x at all")],'The author responds to the quoted criterion by proposing retention of non-EOL majors even without specialness, contesting the requirement\'s application to this wallet test.')
challenge('U31','content','this_proposition',[ref(U['U25']),ref(U['U26']),ref(U['U27'])],'The opposing criterion and its 23.x removal-or-explanation application concern the same release selection; the later author response explicitly quotes and contests them.')
# Broader ACKs remain ordinary assent and cannot establish expectation recognition.
recog('U10','endorsement','broader_proposal','ordinary_assent','same_actor',[ref(U['C09'])],'Sjors later tested-ACKs the identified head, qualifying that there is no pressing merge reason; this does not adopt the specific #25717 rationale.')
recog('U31','endorsement','this_proposition','ordinary_assent','different_actor',[ref(U['Q08']),ref(U['C11'])],'Sjors tentatively agrees with the quoted technical retention proposal. Agreement alone does not establish recognition as an institutional standard.',basis='explicit')
recog('U29','endorsement','broader_principle','ordinary_assent','different_actor',[ref(U['C10']),ref(U['U33'])],'The author agrees with general cleanup while excluding it from this PR; no exact criterion or implementation is endorsed.')
recog('U19','reported_implementation','this_proposition','other','different_actor',[ref(U['C08'])],'The author reports updating to v24.0.1; this responds to the requested edit but is not recognition of an institutional expectation.')
recog('U08','reported_implementation','this_proposition','other','different_actor',[ref(U['C08'])],'The author reports rebasing on master; the specific after-#26589 condition remains unverified. The target is correspondence to the requested rebase, not proof of its full timing.',basis='context_inferred')
application('U08','reported','unresolved',[ref(U['C08'])],'Rebase is reported, but supplied evidence does not verify that it followed the specified #26589 event.')
U['U08']['institution']['standing_profile']['application']='unresolved'
application('U19','reported','this_proposition',[ref(U['C08'])],'The author explicitly reports updating to v24.0.1, while noting archives were not yet available at the time of writing.')
patch24=ev('pr26586:patch:0','+            240001,');patchkeep=ev('pr26586:patch:0','+            240001,\n             230000,\n             220000,')
checksums=ev('pr26586:patch:1',E['pr26586:patch:1']['text'][E['pr26586:patch:1']['text'].index('+    "0b48'):E['pr26586:patch:1']['text'].rindex('\n }')])
merge=[ev('pr26586:metadata','"merged": true'),ev('pr26586:metadata','"merged_at": "2023-02-16T14:04:28+00:00"')]
head=ev('pr26586:supplement_metadata','"head_sha": "741908afc1f9ed2040c18667c75665b300c5dfe7"')
application('U19','observed','this_proposition',[patch24,checksums,head]+merge,'The retained head includes 24.0.1 in the test versions and release archive table, and the PR is recorded merged. This supports the specific version update, not a rationale or general release policy.')
disp('U19','reported_implemented','this_proposition',[ref(U['C08'])],'The author reports the requested version update with the contemporaneous archive-availability caveat.')
disp('U19','recorded_merged','this_proposition',[patch24,checksums,head]+merge,'Patch and integration evidence support the exact requested version update.')
for n in ['U01','U07','U09','U10','U12','U20','U21','U22','U23','U25','U26','U27','U31','U32','U33']:
 disp(n,'recorded_merged','broader_proposal',merge,'The containing PR is recorded merged. This records the contribution\'s disposition and does not show adoption of this reason, general expectation, or alternative procedure.')
application('U31','observed','broader_proposal',[patchkeep,head]+merge,'The merged contribution retains 23.0 while adding 24.0.1, consistent with the case-specific preference. The packet does not establish EOL status, all required recent releases, or adoption of the always/minimum norm.')
# Relations: explicit quotations versus inferred responses remain distinct.
rel('C03','U10','challenges','context_inferred','The specific statement that miniscript is not tested challenges an offered reason for adding v24.',[ref(U['C03']),ref(U['U10'])])
rel('C05','C04','challenges','explicit','The quoted low-cost claim is expressly questioned on append-only growth.',[ref(U['Q03']),ref(U['C05'])])
rel('C06','C04','challenges','explicit','The quoted low-cost claim is expressly denied.',[ref(U['Q06']),ref(U['C06'])])
rel('C05','U13','uptake','context_inferred','Sjors responds to a quoted cost concern with a possible future pruning measure; no implementation is demonstrated.',[ref(U['Q05']),ref(U['U13'])])
rel('U19','C08','uptake','context_inferred','The subsequent author report specifically corresponds to the requested 24.0.1 update; attribution of causation is not established.',[ref(U['U19']),ref(U['C08'])])
rel('U20','C09','uptake','context_inferred','Sjors supplies a tested ACK and process advice after the addressed uncertainty question; full reply-thread linkage is unavailable.',[ref(U['U20']),ref(U['C09'])])
rel('U31','U25','challenges','explicit','The quoted criterion is answered by a different minimum-retention standard for these wallet tests.',[ref(U['Q09']),ref(U['U31'])])
rel('U29','U25','clarifies','context_inferred','The same goes extends the previous criterion to the other versions in this file.',[ref(U['U29']),ref(U['U25'])])
rel('U31','C11','uptake','explicit','The later quote and I tend to agree supply limited assent to the retention proposal.',[ref(U['Q08']),ref(U['C11'])])
rel('U33','U30','uptake','context_inferred','The author\'s scope boundary is consistent with the suggested separate pull for cleanup; no direct thread or causal link is asserted.',[ref(U['U33']),ref(U['U30'])])
# Summary outcomes and mechanisms are decomposed so every material assertion has anchors.
outcome([part('The author reported rebasing on master and updating this PR to v24.0.1, while saying its archives were not yet available when writing.',[ref(U['C08'])]),part('The retained PR head adds 24.0.1 test and archive entries and retains 23.0 in the test version list.',[patchkeep,checksums,head]),part('The PR metadata records a merge on February 16, 2023.',merge)])
outcome([part('Sjors supplied a tested ACK for head 741908afc1f9ed2040c18667c75665b300c5dfe7 and said it worked on current master, while denying a pressing reason to merge.',[ref(U['C09'])]),part('The later tentative agreement followed a quotation of the non-EOL-major-retention proposal.',[ref(U['Q08']),ref(U['C11'])])])
mechanism('reason_giving',[part('A concept NACK questioned the differences warranting v24; Sjors answered with accidental-breakage coverage and every-major-release inclusion.',[ref(U['C02']),ev('pr26586:comments:4',"one reason for the backwards compatibility tests is to ensure there's no accidental breakage between versions, including wallet upgrades, consensus and p2p bugs."),ref(U['U09'])]),part('Subsequent replies questioned general-test coverage and low-cost claims and offered pruning or alternative test arrangements.',[ref(U['C03']),ref(U['C05']),ref(U['U14']),ref(U['U13']),ref(U['U15']),ref(U['U17']),ref(U['U18'])])],['C02','U09','C03','C05','U14','U13','U15','U17','U18'],'supported_sequence','The exchange may reflect parallel technical preferences rather than persuasion; neither the merge nor the surviving patch identifies which argument caused integration.')
mechanism('review_coordination',[part('fanquake conditionally requested the 24.0.1 update; the author then reported that version update and a rebase, with an archive-availability caveat.',[ref(U['U19']),ref(U['C08'])]),part('The retained patch and recorded merge support inclusion of 24.0.1.',[patch24,checksums,head]+merge)],['U19','C08'],'supported_sequence','The author might have planned the update independently; textual correspondence and recorded integration do not identify the causal effect of the request.')
mechanism('scope_management',[part('maflcko proposed a latest-release-per-feature criterion, a remove-23.x-or-explain-24.x requirement, and separate cleanup of other versions.',[ref(U['U25']),ref(U['U26']),ref(U['U27']),ref(U['U29']),ref(U['U30'])]),part('The author quoted that criterion, argued for retaining recent non-EOL majors, and endorsed general cleanup while excluding it from this PR.',[ref(U['Q09']),ref(U['U31']),ref(U['C10']),ref(U['U33'])]),part('The merged contribution adds 24.0.1 while retaining 23.0.',[patchkeep,head]+merge)],['U25','U26','U27','U29','U30','Q09','U31','C10','U33'],'consistent_with','The limited patch scope may reflect the contribution\'s preexisting design; the supplied final head does not show whether review changed it or whether a recurring retention criterion was adopted.')
A['episode_summary']['missing_evidence']=[
 'Complete edit histories and reliable reply threading are absent; body creation does not date every retained sentence.',
 'The packet contains no #25650 or #26589 patches/outcomes, nor independent verification of #25717, #24400, release download availability, EOL status, or claimed wallet behavior.',
 'The final patch is a retained head rather than a full change chronology, so it cannot show which review caused a change.',
 'No evidence establishes a participant\'s authority to impose this release-selection criterion, an executed sanction, or project-wide adoption of either competing criterion.',
 'The supplied guide is pinned to December 10, 2022; continuity of individual provisions at earlier or later comment dates is not established.',
 'Repository merge is not evidence of network adoption; no external sources were consulted.'
]
A['episode_summary']['unresolved_questions']=[
 'Do release-selection suggestions express social expectations or only engineering methods? Norm and strategy alternatives are retained where the text supports both.',
 'Does technical need in the rebase and built-copy comments imply any institutional duty? The preferred records preserve uncertainty rather than create authority.',
 'Was the requested rebase performed after the event denoted by #26589? Only a rebase-on-master report is supplied.',
 'Did anyone implement the bot correction reaction, available-directory loop, pruning, EOL-wallet alternative, or separate cleanup? No supplied record establishes those applications.',
 'Did participants adopt a recurring latest-per-feature or non-EOL-major minimum policy? The merged patch demonstrates one contribution, not that broader conclusion.'
]
# Every entry is screened. Supplements are context scope, not negative institutional judgments.
reasons={
'pr26586:body':'Recurrent-method assertion, separate commit navigation, and negated manual-task necessity are extracted; technical default explanation retained as a qualifier.',
'pr26586:comments:0':'Guideline navigation, conditioned review-list correction, and announced bot consequence are extracted; table and metadata are not independent endorsements.',
'pr26586:comments:1':'Bug/release-withdrawal speculation is context, not a directive or actual withdrawal.',
'pr26586:comments:2':'Delay and rebase requirements are extracted separately; praise of a smaller commit and auto-fetching are technical context.',
'pr26586:comments:3':'Concept NACK plus reasons is a distinct review act and challenge, not an independently prescribed action or sanction.',
'pr26586:comments:4':'Every-major-release expectation and qualified current v24 addition are separate candidates; reasons are attributed and bounded.',
'pr26586:comments:5':'Specific-test method is a candidate with a literal preference alternative; technical criticism is context.',
'pr26586:comments:6':'Keep-open method is a candidate; repeated quotations and low-cost assessment are context. Historical use and CI claims remain attributed rationale.',
'pr26586:comments:7':'Quoted low-cost assertion and conditional cost question are context; an implied pruning invitation is possible but not independently supplied.',
'pr26586:comments:8':'Possible intermediate-version pruning is a candidate; nested repeated quotations add no endorsement.',
'pr26586:comments:9':'Built-copy technical necessity is retained as a boundary candidate; cost denial and quote are context.',
'pr26586:comments:10':'Directory-loop method and conditional developer choice are separate analytical layers; unchanged default fetching is attached to both.',
'pr26586:comments:11':'Dropping EOL versions and hosting regtest wallets are independent replacement actions; comparison rationale and qualified failure observations remain attributed.',
'pr26586:comments:12':'Conditional version-update recommendation is extracted.',
'pr26586:comments:13':'Reported rebase/version update and availability caveat are context and application evidence, not another prescription.',
'pr26586:comments:14':'Request-for-guidance reading supported by uncertainty beyond the name is retained with pure-ping alternative.',
'pr26586:comments:15':'Keep-open, occasional-rebase, non-rushed-merge and follow-up-prune candidates are separate. ACK, tests, quotations, and tentative agreement are bounded context.',
'pr26586:review_comments:0':'Recurring criterion, alternative conditional removal/explanation requests, and distinct commit navigation are extracted under a non-counted container.',
'pr26586:review_comments:1':'Extension of the criterion and separate-PR method are extracted; unidentified future PR is not assigned the current object\'s disposition.',
'pr26586:review_comments:2':'Repeated quotation, non-EOL minimum, verification method, cleanup assent, and immediate scope boundary are distinguished.'}
for e in P['entries']:
 ids=[u['unit_id'] for u in A['units'] if u['source_id']==e['source_id']];statements=[u for u in A['units'] if u['source_id']==e['source_id'] and u['record_role']=='statement']
 if not e['text']:d='empty';reason='Empty review body screened; COMMENTED metadata supplies no textual proposition.'
 elif statements:d='candidate';reason=reasons.get(e['source_id'],'Statement candidate extracted with bounded interpretation.')
 else:
  d='context_only';reason=reasons.get(e['source_id'],'Supplement screened as context under selection_design. It may contain institutional prescriptions or technical methods, but is not an exhaustive extraction target; relevant evidence can be cited directly.')
  if e['kind']=='record_metadata':reason='Supplemental recorded identity/status context; no independent prescription. Integration scope and timestamps are preserved as evidence.'
  elif e['kind']=='patch':reason='Supplemental pinned/retained patch context, including comments and configuration. Not an exhaustive extraction target or a judgment that it lacks institutional content; it supports only exact changes shown.'
  elif e['source_id']=='guide:contributing':reason='Complete pinned guide screened as contextual documentary evidence; it contains many institutional prescriptions but is not a focal extraction target. Its revision date does not establish uninterrupted standing at each comment date.'
  elif e['kind']=='commit_metadata':reason='Pinned predecessor commit and attributed message screened as historical context; any review echoes are not independent endorsements or proof of every rationale.'
 A['entry_screening'].append({'source_id':e['source_id'],'disposition':d,'reason':reason,'unit_ids':ids})
# Make communicative functions and narrower levels explicit where needed.
for n in ['C02','C08','C09','C10','C11']:U[n]['speech_act']='reported_action'
for n in ['C03','C04','C06','C07']:U[n]['speech_act']='technical_description'
U['C05']['speech_act']='question';U['C01']['speech_act']='asserted'
for n in ['U13','U15','U16','U17','U18','U23','U29']:
 U[n]['level_rationale']='The governed act is operational compatibility-test or review practice. The visible exchange considers recurring selection, maintenance, or integration arrangements; observed action is collective choice, with ordinary operational discussion a bounded alternative.'
 U[n]['observed_level_alternatives']=['operational']
for n in ['U15','U16','U17','U18','U29']:U[n]['target_level_alternatives']=['collective_choice']
for n in ['U05','U06']:U[n]['institution']['rationale']+=' This is an articulated procedural method without evidenced social obligation, authority, use, or interpersonal expectation recognition.'
for n in ['U25','U26','U27','U31','U33','U09','U23','U29']:U[n]['institution']['rationale']+=' The candidate reflects expected conduct or an asserted standard; no attributed authorization or enforcement claim meets the rule-candidate threshold.'
Path('annotation.json').write_text(json.dumps(A,ensure_ascii=False,indent=2)+'\n')
print('Written',len(A['units']),'units;',sum(u['record_role']=='statement' for u in A['units']),'statements;',len(A['entry_screening']),'entries')
