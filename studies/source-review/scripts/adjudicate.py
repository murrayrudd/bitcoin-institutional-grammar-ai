"""Source-based Round 4 reconciliation. Frozen inputs and reviewer outputs stay unchanged."""
from pathlib import Path
import copy, csv, hashlib, json
from collections import Counter

P=Path(__file__).resolve().parents[1]
def read(f): return json.loads((P/f).read_text())
def write(f,x):
 p=P/f; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
registry={e['source_id']:e for e in read('sources/baseline_all_source_registry.json')}
reviews={g:read(f'reviewer_outputs/{g}/annotation.json') for g in 'ABC'}
reviews['C']=read('reviewer_outputs/C/supplement/annotation.supplemented.json')
ru={u['unit_id']:u for a in reviews.values() for u in a['units']}
baseline=read('sources/baseline_annotations.json'); corrected=copy.deepcopy(baseline)
bu={u['unit_id']:u for u in baseline['units']}; cu={u['unit_id']:u for u in corrected['units']}
packet=read('sources/baseline_annotation_packet.json')
ledger=[]
def ev(s,q=None,start=None,end=None):
 t=registry[s]['text']
 if q is None:
  start=0 if start is None else start; end=len(t) if end is None else end; q=t[start:end]
 else:
  start=t.index(q) if start is None else start;end=start+len(q);assert t[start:end]==q
 return {'source_id':s,'span':{'start':start,'end':end,'quote':q}}
def ue(uid):
 u=bu.get(uid,ru.get(uid));return {'source_id':u['source_id'],'span':copy.deepcopy(u['span'])}
def finding(fid,title,category,origin,base,fresh,decision,evidence,effect):
 ledger.append({'finding_id':fid,'title':title,'category':category,'origin':origin,'baseline_unit_ids':base,'reviewer_unit_ids':fresh,'decision':decision,'evidence':evidence,'effect_on_paper':effect})

# 1. Majority language has no specified decision arena or constituency.
u=cu['N14'];u['institution'].update(standing='text_only',dispute_present=False,rationale='A participant attributes winning to a majority, without specifying the decision, constituency, aggregation method, or institutional arena. The merit and bot-purpose comments do not establish a challenge to this particular claim.')
u['statement_target_level']='unknown';u['level_alternatives']=['operational','collective_choice','constitutional']
u['level_rationale']='The winner could concern argumentative success, software adoption, or repository integration. The text does not identify which decision is governed; the observed act remains an operational discussion comment.'
u['alternative_interpretation']='A claim about a collective-choice aggregation principle is possible, but rhetorical victory or aggregate software choice are also possible. Do not turn the statement into a specified majority voting rule.'
u['uncertainty_reason']=u['alternative_interpretation'];u['confidence']='unresolved'
cu['U02']['institution']['dispute_present']=False
corrected['relations']=[r for r in corrected['relations'] if not(r['from_unit_id']=='U02' and r['to_unit_id']=='N14' and r['type']=='challenges')]
finding('R4-01','Unspecified majority and unsupported conflict','substantive_error','baseline',['N14','U02'],['C227_majority','C115_merit'],'Retain the majority claim as attributed text; set target level to unknown, remove the inferred challenge relation and the associated dispute flags. Merit versus repeated posting need not conflict with an unspecified majority claim.',[ue('N14'),ue('U02'),ev('32406-169','The goal is *not* to have everyone "register" their "vote".')],'No evidence of a defined voting rule; avoid using this pair as proof of rival aggregation procedures.')

# 2. Documentary basis for the named moderation intervention.
topic=ev('D_MOD','Comments will be on-topic.')
venue=ev('D_MOD','Comments about moderation decisions or moderation policy are off-topic in Bitcoin Core software projects and will be deleted. If you wish to discuss moderation, please file an issue in [bitcoin-core/meta](https://github.com/bitcoin-core/meta/issues/new), which is the home for project management issues, and nontechnical discussions relating to development of the codebase.')
sanction=ev('D_MOD','If moderation of individual posts fails, moderators will use warnings, timeouts and bans at increasing rates based on prior patterns of behavior. Usually mildly uncivil behavior (such as being off-topic/disruptive or rudeness) will result in a warning or temporary ban (in the order of days).')
u=cu['U17'];u['institution']['standing']='documented';u['institution']['authority_evidence'] += [topic,venue]
u['institution']['evidence'].append(topic)
u['institution']['rationale']='The case-specific topic instruction applies a dated written moderation provision. The accompanying ban announcement is attributable; the speaker\'s actual permissions and execution of a ban are not established.'
u=cu['U19'];u['span']=copy.deepcopy(ru['B19']['span']);u['components'][-1]['text']='on https://github.com/bitcoin-core/meta/'
u['components'][-1]['evidence']=[ev('32406-252','on https://github.com/bitcoin-core/meta/')]
u['deontic_force']='obligation';u['institution'].update(type='rule_candidate',standing='documented',rationale='The positive venue instruction applies the supplied moderation guide, read with the separate negative duty not to debate the intervention in this thread.',evidence=[{'source_id':u['source_id'],'span':copy.deepcopy(u['span'])},venue],authority_evidence=[venue])
u['alternative_interpretation']='The elliptical action can be represented literally as do so or reconstructed as debate; its conditional venue boundary is preserved.';u['uncertainty_reason']=u['alternative_interpretation']
finding('R4-02','Written moderation policy underused','substantive_error','baseline',['U17','U19'],['B15','B19','B20'],'Use documented standing for the on-topic and appeal-venue provisions. Treat the venue instruction as a rule candidate with obligatory force, preserving its case-specific scope.',[ue('U17'),ue('U19'),topic,venue],'The episode applies written institutional arrangements as well as informal expectations; documentation does not verify individual permissions or enforcement.')

# 3. Preserve the already recognized consequence as a statement and split negative duty.
new=copy.deepcopy(ru['B18']);new['unit_id']='U18';new['scope']='case_specific'
new['institution']['standing']='text_only'
new['institution']['rationale']='An attributable case-specific warning announces a temporary ban for future off-topic comments. The dated guide authorizes warnings or temporary bans in this class of case; it does not independently establish this exact future sanction or verify the named speaker\'s office.'
new['confidence']='plausible';new['uncertainty_reason']='The enforcer and affected account are inferred from documentation and the enclosing addressee; no ban event is supplied.'
corrected['units'][corrected['units'].index(cu['U18'])]=new;cu['U18']=new
new=copy.deepcopy(ru['B20']);new['unit_id']='R4_U19_negative'
for c in new['components']:
 if c['symbol']=='Bdir':
  c['basis']='context_inferred';c['inference_note']='The object of the conditional debate clause is inherited by the elliptical negative duty; no local object is repeated.'
new['confidence']='plausible';new['uncertainty_reason']='The omitted actor, action, object, and condition are recovered from the preceding positive clause.'
corrected['units'].append(new);cu[new['unit_id']]=new
corrected['relations'].append({'from_unit_id':'U19','to_unit_id':'R4_U19_negative','type':'AND','basis':'explicit','rationale':'The positive alternative-venue duty and negative current-venue duty share a conditional antecedent and are coordinated by and.','evidence':[ue('U19')],'logic_scope':'propositions'})
finding('R4-03','Separate consequence and negative duty','convention_deviation','baseline',['U18','U19'],['B18','B19','B20'],'Represent the announced sanction as its own statement (U18), keep the existing O link, and split the negative current-thread duty from U19. The original coding already preserved both meanings; this corrects their prescribed representation.',[ue('U18'),ue('U19'),sanction],'No new observed sanction or institutional mechanism is inferred from the representation change.')

# 4. Reason reuse supplies bounded recognition beyond repeated words.
warning_use=ev('33453-body',start=registry['33453-body']['text'].index('This echo'),end=registry['33453-body']['text'].index(' Deprecating the option'))
u=cu['U25'];u['institution'].update(standing='locally_supported',rationale='The September proposer attributes and quotes the warning expectation, then applies the absence of a removal plan and user uncertainty as reasons to remove deprecation. This is local recognition of the expectation in this setting, beyond bare repetition.')
u['institution']['recognition']=[{'kind':'expectation_recognition','target':'this_proposition','basis':'context_inferred','evidence':[warning_use],'rationale':'Attribution and exact quotation are explicit. The inference of recognition rests on the surrounding argument applying the expectation as a reason for the proposed change.'}]
u['alternative_interpretation']='The argument supports the expectation for these options; its scope across every deprecation remains uncertain. Recognition does not adopt the June PR retroactively or establish a unique cause of the September merge.';u['uncertainty_reason']=u['alternative_interpretation']
finding('R4-04','Warning principle receives local recognition','substantive_error','baseline',['U25'],['B26','C32714_warning_expectation'],'Upgrade to locally_supported with context_inferred recognition, using the September argument as well as its quotation.',[ue('U25'),warning_use],'A reason from a proposal that did not merge can become part of the justification for a later proposal; unique causal influence is not identified.')

# 5. The legitimacy claim receives a directly addressed challenge to application.
u=cu['N16'];reply=ev('32406-229');u['institution'].update(standing='disputed',dispute_present=True,rationale='The open-source legitimacy claim is followed by a directly addressed reply disputing its application: the respondent invokes public discussion and historical merit. This is a challenge to using the principle against this process, not a rejection of transparency as a value.')
u['institution']['recognition']=[{'kind':'response','target':'this_proposition','basis':'context_inferred','evidence':[reply],'rationale':'The named reply challenges the application and premise of the open-source criticism. It supplies no endorsement of an established institution.'}]
u['institution']['evidence'].append(reply);u['level_alternatives']=['operational','collective_choice','constitutional']
u['level_rationale']='The baseline focal proposition articulates foundations of legitimate decision authority, making epistemic a plausible target under the project convention. A regulative reading targets ordinary transparent decision conduct. The observed action is operational argument; no higher-level institution or change is established.'
u['alternative_interpretation']='A regulative obligation to make transparent decisions and an ordinary accountability reading are defensible. The epistemic target is an interpretation of the legitimacy framing, not proof that an epistemic institution exists.';u['uncertainty_reason']=u['alternative_interpretation']
finding('R4-05','Challenge to application of the legitimacy claim','substantive_error','baseline',['N16'],['A019'],'Record the reply as a dispute about application. Preserve constitutive and regulative alternatives and the bounded epistemic interpretation; add operational to level alternatives.',[ue('N16'),reply],'The dispute provides evidence of competing legitimacy arguments, not an observed transfer of authority or a demonstrated new governance level.')

# U24 already had the negative response and dispute flag; change the primary standing label only.
cu['U24']['institution']['standing']='disputed'
cu['U24']['institution']['rationale']='A reviewer accepts adding non-recommendation text but explicitly recommends keeping the deprecation warning, challenging the proposed substitution. The body remains a proposed edit; later closure is a separate broader-proposal outcome.'
finding('R4-06','Substitution dispute already preserved','defensible_alternative','both',['U24'],['B22'],'Use disputed as the primary standing label. Round 3 already retained the challenge, dispute flag, and unmerged disposition, so this is label alignment rather than a newly discovered rejection.',[ue('U24'),ev('32714-007',"It's fine to _add_ a non-recommendation text, but we should keep the deprecation warning.")],'The June wording proposal still did not integrate; its embedded reasons remain separately assessable.')

# Candidate inventory additions: do not equate new full parses with screen omissions.
candidates=read('sources/baseline_candidate_passages.json'); additions=[]
def add(s,q,domain,why,reviewids,classification='additional_candidate'):
 e=ev(s,q);idx=sum(x['source_id']==s for x in candidates+additions)+1
 item={'candidate_id':'R4C'+s.replace('-','_')+'_'+str(idx),'source_id':s,'span':e['span'],'domain':domain,'selection_reason':why,'occurrence_role':'original','full_schema_unit_ids':[],'annotation_coverage':'candidate_addendum_with_archived_reviewer_parse','reviewer_unit_ids':reviewids,'review_classification':classification}
 additions.append(item);return e
navigation=[]
for uid in ['A018','C165_referral','B02','B28','B21']:
 u=ru[uid];navigation.append(add(u['source_id'],u['span']['quote'],'navigation','Distinct see/referral instruction required by frozen codebook; the linked material is not thereby supplied or verified.',[uid],'clear_extraction_omission'))
finding('R4-07','Five missed navigation instructions','substantive_error','baseline',[],['A018','C165_referral','B02','B28','B21'],'Add five exact-span navigation candidates, including two from comments previously excluded as technical context.',navigation,'Improves extraction completeness; referrals do not establish shared expectations or authority.')
other=[]
specs=[('A016','technical_request','Direct proposal to lift the technical restriction.'),('A010','review_procedure','Claim that inclusion requires persuasion; obligation versus practical necessity remains open.'),('A001','wording_request','Qualified preference between two documentation formulations.'),('A002','wording_request','Indirect criticism of wording; an editorial recommendation is plausible.'),('C012_no_args','technical_request','Addressed objection to adding node arguments; an evaluative-opinion reading remains possible.'),('C33453_footguns','user_protection','Quoted and favorably characterized principle, then qualified in its application; advisory force is preferred.'),('C33453_remove_deprecation','technical_request','Opening proposal to remove deprecation; descriptive patch-summary reading remains possible.'),('B16','moderation','Classification of comments outside the current thread\'s remit.'),('B17','moderation','Permission to move the broader discussion to meta.')]
for uid,domain,why in specs:
 u=ru[uid];other.append(add(u['source_id'],u['span']['quote'],domain,why,[uid]))
t=registry['32406-178']['text'];q=t[t.index('Here, the reason'):t.index('\r\n\r\nWhether')]
other.append(add('32406-178',q,'user_advice','Attributed reasons for non-use and for the deprecated label. The claim about most developers is the speaker\'s assessment, not a measured preference distribution.',['B08','B09','B29']))
finding('R4-08','Additional proposals and procedural claims','extraction_addendum','baseline',[],[uid for uid,_,_ in specs]+['B08','B09','B29'],'Retain ten additional candidate passages. Direct proposals and permissions are distinguishable from indirect criticisms or descriptions; the latter retain explicit alternatives. None is promoted to a shared institution merely by inclusion.',other,'Broadens source coverage without inflating the number of established norms. Counts are passage additions, not independent institutions.')
rhetorical=add('33453-068','"Expressing disgust" is not a reasonable use case. Why do you think that Bitcoin Core should cater towards emotional outbursts?','use_case_criterion','Retain as a candidate objection to an acceptable-use criterion. A rhetorical/evaluative context reading remains defensible.',['B27'],'defensible_inclusion')
finding('R4-09','Rhetorical question retained as a bounded candidate','defensible_alternative','both',[],['B27'],'Retain the evaluative premise and question together for high-recall screening. Do not infer a binding obligation to answer or a shared project criterion.',[rhetorical],'This changes the candidate inventory, not the institutional standing of the criterion.')

# Source completion resolves quoted-content duplication at the inventory level.
finding('R4-10','Quoted originals already represented','context_completion','review_packet',[],['C018_add_flag','C213_permission','C213_defaults','C213_increase'],'Retain the repeated material as quoted context for corpus-level counting. The complete registry supplies the originals at 33224-016 and 32359-186, both already in the candidate inventory. Their absence from the initial C packet explains fresh external-quotation statement records; those are not newly discovered institutions.',[ev('33224-016','Would it be better to add `-locations none` to the LCONVERT invocation in translate.cmake? (Post branch-off)'),ue('C018_add_flag'),ev('32359-186','As a node runner I should be allowed to configure my mempool and not have it filled with what I consider spam.'),ue('C213_permission')],'Avoid duplicate statement counts and retain the response relation without treating quotation as independent endorsement.')
finding('R4-11','Preserved permissions and allocation of timing authority','substantive_equivalence','both',['N02','U03','U39','U39b'],['A004','C115_no_repost','A013','A014'],'Preserve the permission to defer small edits, absence of an obligation to repost, attributed maintainer timing discretion, and personal commitment not to object. Different spans or resolved pronouns preserve the relevant arrangements.',[ue('N02'),ue('U03'),ue('U39'),ue('U39b')],'The source-supported core explanation survives these comparisons.')
finding('R4-12','Coupled discouragement versus split actions','defensible_alternative','both',['U04'],['C115_unsubstantiated','C115_repetition'],'Retain the coupled baseline representation, with the two separately parsed actions available as an alternative. Both preserve the discouragement and its evaluative rather than overtly mandatory wording.',[ue('U04')],'No claim that repetition is literally prohibited follows from the semantic discouragement alone.')
finding('R4-13','Forum purpose and merit criterion','defensible_alternative','both',['U01','U02'],['C115_forum','C115_merit'],'Preserve U01 as a case-specific constitutive account of this forum with text_only standing. For U02, preserve the baseline constitutive arrangement and locally_supported standing. The reviewer\'s regulative description is a defensible alternative. The source-only supplement supplies attributable recognition of the general merit-over-count criterion; exact counts and applications differ.',[ue('U01'),ue('U02'),ev('32406-169','The technical content of those review comments is what matters, not how many are registered in what category.')],'Do not treat the initial standing difference, caused by missing context, as an independent disagreement on equal evidence.')
meaning_conflict=ev('32406-071',"Deprecation isn't a value judgment but a statement that it will be removed in a future version.")
cu['N04']['institution']['evidence'].append(meaning_conflict)
cu['N04']['institution']['rationale']='The status definition is explicitly quoted and endorsed locally. A separately supplied comment defines deprecation through future removal, documenting competing meanings; no direct reply between those two definitional statements or project-wide agreement is inferred.'
finding('R4-14','Status definition and recognition threshold','defensible_alternative','both',['N04'],['B06','B07'],'Retain local recognition of the embedded status meaning and attach the competing future-removal definition explicitly. The fresh reading focuses on the outer recommendation about how to interpret the term; its stricter endorsement threshold remains a defensible alternative.',[ue('N04'),ev('32406-180'),meaning_conflict],'The paper can analyze contested meanings without treating a proposed definition as project consensus.')
finding('R4-15','Translation freeze and compatible workarounds','defensible_alternative','both',['U32'],['C010_freeze'],'Retain text_only standing for the exact categorical prohibition. A later workaround can qualify its application or comply with its intended constraint; the source does not settle that choice. Literal nominal-action and pragmatic-action parses preserve the prohibition.',[ue('U32'),ev('33224-021')],'The release sequence remains usable; successful integration alone does not validate an absolute freeze rule or prove its violation.')
finding('R4-16','Fresh reviews omit two status definitions','substantive_error','reviewer',['U26a'],['A001','A002','B23'],'Preserve the existing candidate defining discouragement as deprecation and U26a defining deprecation as non-recommendation. Editorial preferences and an embedded recommendation do not exhaust these separate status-defining propositions.',[ev('32714-014','discouragement *is* deprecation'),ue('U26a')],'The fresh outputs are fallible comparison evidence and cannot replace the baseline automatically.')
finding('R4-17','Scope of the named moderation warning','epistemic_coding_error','reviewer',['U17','U18'],['B15','B18'],'Retain case_specific scope for the named addressee and future comments in this thread. General policy supports the intervention but does not make the particular warning a general statement. The exact announced sanction remains text_only, with documented authorization context.',[ue('U17'),ue('U18'),sanction],'Avoid generalizing a single warning into a universal automatic sanction.')
finding('R4-18','Qualified safety principle has advisory force','defensible_alternative','reviewer',[],['C33453_footguns'],'Prefer recommendation for the acknowledged good principle in this qualified discussion; preserve the literal negative-imperative/prohibition alternative. The source immediately limits its applicability to the options at issue.',[ue('C33453_footguns'),ev('33453-body',start=registry['33453-body']['text'].index('“Don’t offer'),end=registry['33453-body']['text'].index(' There already'))],'A normative principle may be recognized and still argued not to control the current case.')
finding('R4-19','Review context parity repaired transparently','process_finding','review_packet',['U02'],['C115_merit'],'The uniform evidence-coverage audit found one missing baseline evidence source in the focal packets: 32406-169. Preserve C\'s frozen first output and a separate source-only supplemented output. No baseline annotation or other reviewer conclusion was disclosed. The supplement changes merit standing but does not resolve the majority claim.',[ev('32406-169','The technical content of those review comments is what matters, not how many are registered in what category.')],'The final comparison uses supplemented C, while the first output remains auditable. Context selection is part of the method.')
finding('R4-20','Exact thread linkage supports reported implementation','substantive_equivalence','both',['N01'],['B14'],'Original reply metadata identifies 32359-053 as a direct reply to 32359-038. Retain reported implementation of the comment suggestion and the separate closed-unmerged PR disposition. The report does not verify the exact resulting code.',[ue('N01'),ev('32359-053','Added comment.')],'Local technical uptake and repository integration remain distinct outcomes.')

# Update dependent synthesis, preserving unreviewed material as inherited.
for m in corrected['episode_summary']['mechanisms']:
 if 'U19' in m['unit_ids']:m['unit_ids'].append('R4_U19_negative')
 if 'U25' in m['unit_ids']:
  m['claim']='The September proposal explicitly quotes and applies the June warning expectation as a reason to remove deprecation. September review accepts undeprecation while retaining broader preferences, and the merged patch removes the warning.'
  m['evidence'].append(warning_use)
corrected['episode_summary']['missing_evidence'][0]='Independent human validation; coding outside the 24-record AI review sample; complete edit/deletion and moderation histories.'
corrected['episode_summary']['unresolved_questions']=[q for q in corrected['episode_summary']['unresolved_questions'] if not q.startswith('When does a repeated quotation')]
corrected['episode_summary']['unresolved_questions'].append('Which decision and constituency does the majority claim refer to? The supplied sources do not resolve this.')
corrected['run_id']='CoreKnots_R4_adjudicated_baseline_v01'
packet['selection_design']=str(packet['selection_design'])+' Round 4 is a correction overlay on this selective annotation projection, not full validation of all inherited units. Reviewer source packets remain separately frozen.'
have={e['source_id'] for e in packet['entries']}
def refs(x):
 if isinstance(x,dict):
  if 'source_id' in x:yield x['source_id']
  for v in x.values():yield from refs(v)
 elif isinstance(x,list):
  for v in x:yield from refs(v)
for sid in sorted(set(refs(corrected))-have):packet['entries'].append(copy.deepcopy(registry[sid]))
units_by_source={e['source_id']:[] for e in packet['entries']}
for u in corrected['units']:units_by_source[u['source_id']].append(u)
corrected['entry_screening']=[{'source_id':sid,'disposition':'candidate' if any(u['record_role']=='statement' for u in us) else ('context_only' if registry[sid]['text'].strip() else 'empty'),'reason':'Selective full-annotation projection with a bounded Round 4 correction overlay; complete candidate inventory is a separate file.','unit_ids':[u['unit_id'] for u in us]} for sid,us in units_by_source.items()]
write('sources/corrected_annotation_packet.json',packet)
corrected['packet_sha256']=sha(P/'sources/corrected_annotation_packet.json')
write('annotations/corrected_baseline.json',corrected)
write('analysis/adjudication_ledger.json',ledger);write('analysis/candidate_additions.json',additions)
inventory=copy.deepcopy(candidates+additions)
for c in inventory:
 linked=[u['unit_id'] for u in corrected['units'] if u['record_role']=='statement' and u['source_id']==c['source_id'] and max(u['span']['start'],c['span']['start'])<min(u['span']['end'],c['span']['end'])]
 c['full_schema_unit_ids']=linked
 if linked:c['annotation_coverage']='overlaps_corrected_selective_projection'
write('analysis/candidate_inventory_corrected.json',inventory)

# Preserve all 24 focal decisions explicitly, without equating passage counts with institutions.
sample=read('protocol/selected_sample.json');screens=read('sources/baseline_screening_judgments.json')
notes={
'32359-038':'Comment suggestion and reported incorporation preserved; direct reply metadata supplied.',
'32359-115':'Merit recognition retained after source completion. Repeated-posting constraint is not a specified majority rule.',
'32359-227':'Unspecified majority claim retained without an assumed decision arena. Polemical descriptions of rival camps remain attributed claims.',
'32381-body':'Add the direct proposal to lift the restriction; retain the mailing-list referral and separate support for PR 32359.',
'32406-149':'Add persuasion threshold claim; retain permission to defer minor edits and local recognition. Practical necessity is an alternative to duty.',
'32406-178':'Add navigation and advisory reasoning; retain the locally recognized status definition and explicit rival meaning.',
'32406-228':'Record challenge to the application of open-source legitimacy; retain level and grammar alternatives.',
'32406-252':'Apply dated policy, keep case scope, represent consequence and negative venue duty separately; add classification, permission, and referral candidates.',
'32714-body':'Retain status definition omitted by fresh review. Upgrade bounded recognition of warning principle. Exploratory bikeshedding can remain context.',
'33224-010':'Preserve categorical prohibition as expressed; workaround and nominal-action alternatives remain unresolved.',
'33453-018':'Maintainer timing discretion and personal non-objection preserved; neither establishes authority over network adoption.',
'33453-body':'Add opening removal proposal and qualified footgun principle; preserve duplicate warning quotation and argument use.',
'32714-014':'Add editorial preferences; preserve the prior definition of discouragement as deprecation omitted by fresh review.',
'32406-148':'Both technical test request and conditional documentation objection are already covered by the candidate passage.',
'33453-004':'Conditional ACK contains a recommendation about the interval before reconsidering deprecation; already retained as a candidate.',
'33224-000':'Add details referral. Bot list instructions are not independent human endorsements; stated bot consequence remains unverified.',
'32359-213':'Only high-default proposal is new at this occurrence; quoted configuration claims have retained originals at 32359-186.',
'32381-012':'Add addressed objection to further arguments, with literal evaluative alternative.',
'32359-066':'Reclassify from context to candidate for two linked PR referrals in a single navigation instruction.',
'32714-013':'Retain as quotation and assent context; no separate new prescription.',
'33453-068':'Retain the use-case criterion and rhetorical question as a bounded candidate; evaluative context is an alternative.',
'32381-018':'Retain context: acknowledgment/prediction does not itself create a distinct institutional prescription.',
'33224-018':'Retain as response context and repeated quotation; original technical request already appears at 33224-016.',
'32406-165':'Reclassify as candidate for issue referral; reported fix and later categorization explanation remain distinct.'}
decisions=[]
for x in sample:
 sid=x['source_id'];fresh=[u for u in reviews[x['reviewer_group']]['units'] if u['source_id']==sid and u['record_role']=='statement'];cs=[c for c in candidates+additions if c['source_id']==sid]
 decisions.append({**x,'baseline_screen_class':screens[sid]['screen_class'],'reviewer_statement_units':[u['unit_id'] for u in fresh],'reconciled_screen':'candidate' if cs else 'context_only','candidate_ids':[c['candidate_id'] for c in cs],'decision':notes[sid],'evidence':[ev(sid)]})
write('analysis/reconciled_sample_decisions.json',decisions)
questions={'blocking_author_questions':[],'optional_later_design_choices':[{'issue':'Interpretive layers for legitimacy claims','recommended_default':'Describe the legitimacy argument in prose and retain alternative level codes; do not use ambiguous level counts as evidence of observed higher-level institutions.'},{'issue':'Human validation for publication','recommended_default':'After the working protocol is stable, give a bounded packet to an institutional analyst who has not seen the adjudicated labels; retain their independent judgments before reconciliation.'}],'interpretation_limits':['The majority constituency is not recoverable from supplied text.','The translation workaround may implement or qualify the stated freeze.','Local recognition does not establish project-wide acceptance.'],'need_user_input_now':False}
write('analysis/author_questions.json',questions)
diffs=[]
for uid,u in cu.items():
 if uid not in bu:diffs.append({'unit_id':uid,'change':'added','fields':['entire_unit']})
 elif bu[uid]!=u:diffs.append({'unit_id':uid,'change':'revised','fields':[k for k in u if u[k]!=bu[uid].get(k)]})
write('analysis/correction_log.json',{'unit_changes':diffs,'removed_relations':[r for r in baseline['relations'] if r not in corrected['relations']],'added_relations':[r for r in corrected['relations'] if r not in baseline['relations']],'scope':'Changes reflect adjudication, not automatic acceptance of a reviewer output. All other baseline units are inherited, not newly validated.'})
counts={'focal_records':24,'purposive':12,'sampled_candidate':6,'sampled_excluded':6,'review_contexts':3,'baseline_fully_annotated_statements_in_sample':17,'baseline_sources_with_full_statement_annotations_in_sample':10,'fresh_focal_statement_units':sum(len(d['reviewer_statement_units']) for d in decisions),'fresh_candidate_records':sum(bool(d['reviewer_statement_units']) for d in decisions),'reconciled_candidate_records':sum(d['reconciled_screen']=='candidate' for d in decisions),'baseline_candidates':len(candidates),'candidate_additions':len(additions),'clear_navigation_omissions':5,'other_candidate_additions':10,'defensible_rhetorical_inclusions':1,'corrected_inventory_candidates':len(candidates+additions),'grouped_findings':len(ledger),'finding_categories':dict(Counter(f['category'] for f in ledger)),'baseline_total_statement_units':sum(u['record_role']=='statement' for u in baseline['units']),'corrected_projection_statement_units':sum(u['record_role']=='statement' for u in corrected['units']),'corrected_projection_total_units':len(corrected['units']),'corrected_projection_sources':len(packet['entries']),'corrected_projection_relations':len(corrected['relations']),'revised_existing_units':sum(d['change']=='revised' for d in diffs),'added_units':sum(d['change']=='added' for d in diffs),'accuracy_estimate':None,'independent_human_validation':False,'author_decision_required':False}
write('analysis/review_summary.json',counts)
for filename,items,fields in [('adjudication_ledger.csv',ledger,['finding_id','title','category','origin','baseline_unit_ids','reviewer_unit_ids','decision','effect_on_paper']),('candidate_additions.csv',additions,['candidate_id','source_id','domain','selection_reason','reviewer_unit_ids','review_classification']),('reconciled_sample_decisions.csv',decisions,['source_id','stratum','reviewer_group','baseline_screen_class','reconciled_screen','decision'])]:
 with (P/'analysis'/filename).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for item in items:w.writerow({k:json.dumps(item[k],ensure_ascii=False) if isinstance(item[k],list) else item[k] for k in fields})
print(json.dumps(counts,indent=2))
