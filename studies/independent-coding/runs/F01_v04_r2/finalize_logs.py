from pathlib import Path
import json,hashlib,sys,platform,collections
P=json.loads(Path('packet.json').read_text());E={e['source_id']:e for e in P['entries']};A=json.loads(Path('annotation.final.json').read_text());U={u['unit_id']:u for u in A['units']};F=json.loads(Path('annotation.first_complete.json').read_text());FU={u['unit_id']:u for u in F['units']};LOG=json.loads(Path('repair_log.json').read_text())
def ref(u):return {'source_id':u['source_id'],'span':u['span']}
def uniq(es):
 out=[];keys=set()
 for e in es:
  key=(e['source_id'],e['span']['start'],e['span']['end'])
  if key not in keys:keys.add(key);out.append(e)
 return out
def ev(s,q):
 t=E[s]['text'];i=t.index(q);return {'source_id':s,'span':{'start':i,'end':i+len(q),'quote':q}}
notes={
'U01':'The source supplies an elliptical same-procedure claim. Repeat and its object are inferred; the text does not identify an actor for the procedure. Every release is retained, but only two predecessor examples are documented, so exhaustive recurrence and temporal continuity remain unproved. The body date is not treated as the date of every retained sentence.',
'U02':'One see predicate navigates to two complete commit identifiers and their version labels. This is one coupled navigation action, with null single decision-object identity because there are two commit targets. The containing PR cannot substitute for either target.',
'U03':'The negated operator is preserved as don\'t need to, not permission or prohibition. Extend receives the tag list in both named locations; anymore narrows the claim to the changed script default. Technical elimination of work remains a defensible nondeontic reading, with no source for institutional authority.',
'U04':'See has the guideline as its single direct target and for-information as a purpose/execution constraint. The linked mutable master guide is not silently equated with the supplied pinned revision. The imperative supplies no explicit deontic; recommendation is interpretive force.',
'U05':'The incorrectly-listed condition applies to react with the specified thumbs-down emoji on this comment. Please is politeness, not a deontic. The single target this comment is Bdir. The reusable template is restricted to this occurrence.',
'U06':'The bot is explicit actor of ignore and it is the explicit grammatical object. The antecedent is the mislisted review, and the reaction trigger is attached through U05. Will predicts an automated consequence, not duty, enforcement, or proof of actual bot use.',
'U07':'Hold off supplies the proposed action and a bit supplies its limited duration. The actor and precise integration event are not fabricated. The preceding release-bug speculation is supporting context, not an explicit prior delay request or withdrawal.',
'U08':'Rebase is nominal; reconstruction makes the PR the action target rather than falsely labeling its original subject role explicit. After #26589 is retained without inventing the specified event. A rebase-on-master report does not establish fulfillment of that complete condition; recognition/application remain unresolved.',
'U09':'We/should/add/every-major-release belong to the embedded action clause rather than I think. The proposed expectation is general within backwards compatibility testing. Its accidental-breakage rationale does not prove this test covers all cited cases. The observed debate explicitly concerns a recurring inclusion criterion, while the focal conduct target remains operational.',
'U10':'Should governs justify, not add; no explicit deontic is extracted for the inferred recommendation. The object of adding remains explicit under add and retains the widely-downloadable alternative. #25717 supplies a reason, not the proposal whose merge is claimed. The attributed miniscript example is qualified by last time checked.',
'U11':'The literal function is an asserted preference. Reconstructed use and its object roles are inferred even though specific tests is present. The git-grep string identifies examples rather than a separate imperative. The suggested method is operational engineering discourse with collective-choice deliberation an alternative.',
'U12':'Keep this PR open is the action, with until another PR needs it retained as execution duration. Can is exploratory possibility, not authorization. Historical piling/rebasing and repeat CI checks are participant reports, not independently observed applications of the method.',
'U13':'Remove intermediate releases at some point is a possible mitigation to the explicitly quoted cost question. Can is not coded as lexical permission. The technical suggestion does not prove an adopted recurring pruning arrangement or a completed follow-up.',
'U14':'Have to is retained but force remains unresolved between technical prerequisite and duty-like reading. Keep has every single listed release\'s built copy as object; to-run supplies the purpose. The parenthetical rejects guix static binaries as a good alternative in the speaker\'s assessment, without independent technical verification.',
'U15':'Change and the file\'s role as object are reconstructed from the instead-of comparison. We remains the explicit configuring subject. The loop over available releases/v* and unchanged fetch-all default are attached qualifications. Technical code redesign alone is not proof of a changed institutional arrangement.',
'U16':'Choose, developer-as-actor, and informational-object roles are inferred from up-to wording. In that case limits choice to U15\'s proposed architecture, and the default download remains all binaries. Technical capability versus institutionally allocated discretion is unresolved; no authority is invented.',
'U17':'The passive dropped action has EOL versions as its explicit receiver. Tentativeness is preserved and paired hosting is separately represented. The rationale contrasts old-wallet loading with modern-wallet opening on EOL versions; these are actor judgments, not independently tested priorities.',
'U18':'The repository hosts wallets in the literal technical proposal; no human administrator or institutional role is substituted. Instead and the tentative replacement design are attached through the compound source. The AND links actions and does not prove either occurred.',
'U19':'The if-still-going-ahead condition, should, passive update receiver it, and to-use-24.0.1 constraint are all retained. The report is separate from observed retained-head changes. Patch labels, archive entries, matching head identity, and merge metadata support the version update only; the archive-unavailable caveat applies at the report\'s writing time.',
'U20':'Not sure what to do supplies context beyond a pure name ping. Advise and its actor/object roles are reconstructed. Sjors\'s later advice supports that reading, but reliable threading is unavailable, so pure-ping interpretation remains possible.',
'U21':'The correct we occurrence is the subject of could leave, not the earlier we\'ve done predicate. The proposed method is possible continuation with no pressing merge need, paired with occasional rebase. The merge records the broader PR outcome and does not prove this optional method rejected.',
'U22':'Rebase and it are explicit local action/object; occasionally constrains frequency. The coordinated main-clause we is an explicit shared-scope actor, added in self-review with the full governing coordination. The preceding leave-open action remains attached through U21.',
'U23':'Avoid rushing is a pragmatic restraint reconstructed from the reason-giving assertion. Negation remains in the reconstructed action, and merging new releases is the action target. The referent is the qualified quoted concern about ignored intermittent failures, excluding obvious repeated smoke failures.',
'U24':'Prune versions in a followup preserves action, target, and proposed execution location. Always describes availability of the option; can is not authority and no identifiable follow-up proposal or implementation is supplied.',
'U25':'Add latest for each missing feature retains only as a material scope qualifier. No authorized rule or veto power is supplied. The cited commit documents a broader comparable technical principle in different tests. The same actor\'s same-goes extension is maintained commitment, now recorded as same_actor_only, not interpersonal recognition.',
'U26':'The main-clause you, not the conditional you alone, is actor of remove; need is the attributed review requirement. If adding 24.x activates either remove-23.x or explain-specialness. The OR is inclusive because exclusive satisfaction is not established. The author\'s response contests the premise/application, not an executed sanction.',
'U27':'Explain receives the complete why-24.x-is-special informational object. You, need, and the adding-24.x condition are explicitly shared from the governing coordination, not mislabeled local. The alternative remove route is attached. The source offers no enforcement evidence.',
'U28':'See is a separate navigation action with the full cited commit as Bdir and its own commit identity. Also is additive, not an independent execution condition. The cited change does not establish authority over the current wallet-test inclusion.',
'U29':'The same goes inherits U25\'s criterion. Apply, criterion-as-object, and versions-as-affected-target are inferred roles under the reconstructed action. Unrelated and other versions in this file preserve scope. Its observed use of a recurring criterion supports the collective-choice reading while source action remains ordinary discussion.',
'U30':'Someone is the explicit actor of do; cleanup and its object are reconstructed from that and U29. In a separate pull is retained. Null identity means an unknown future pull request, so the present PR\'s merge is never assigned to it.',
'U31':'The question directly supplies keep and its complete non-EOL recent-major object; recommendation force is inferred without inventing lexical D. At least, always, bare minimum, wallet-test domain, and rather-than-sacrifice are all retained. The author explicitly denies assumed specialness of 24.x. Later tentative agreement is ordinary assent; merged retention of two releases does not establish the full norm.',
'U32':'The complete I\'d contraction anchors the first-person actor; verify and this assumption have explicit action/object roles. The attached example and antecedent identify both 23.x and 24.x and master-created wallets. This is a preferred verification method, not proof of completed verification or known specialness.',
'U33':'The outside-scope assertion is pragmatically parsed as exclude plus a distinct PR boundary. That changes from literal subject to inferred direct object and is resolved to general cleanup, not the current version addition. Separate assent shows cleanup itself is not rejected. The pinned focus guidance is broader and temporally unresolved for the later claim.'}
R={'run_id':'F01_v04_r2','episode_id':'F01','review_protocol_version':'0.4','review_type':'one complete source-based self-review after first-complete freeze and first checker feedback','review_passes':1,'source_scope':'Assigned packet and local protocol/checker only. No post-dispatch new research sources, external comparison, or other coder output.','first_complete_sha256':hashlib.sha256(Path('annotation.first_complete.json').read_bytes()).hexdigest(),'final_sha256':hashlib.sha256(Path('annotation.final.json').read_bytes()).hexdigest(),'counts':{'screened_entries':len(A['entry_screening']),'focal_entries':len(P['selection_design']['focal_source_ids']),'supplemental_entries':len(P['entries'])-len(P['selection_design']['focal_source_ids']),'units':len(A['units']),'unit_roles':dict(collections.Counter(x['record_role'] for x in A['units'])),'relations':len(A['relations']),'outcomes':len(A['episode_summary']['observed_outcomes']),'mechanisms':len(A['episode_summary']['mechanisms'])},'screening_review':[],'unit_source_review':[],'relation_review':[],'summary_review':[],'checker_resolutions':[],'unresolved_limits':A['episode_summary']['missing_evidence']+A['episode_summary']['unresolved_questions']}
for sc in A['entry_screening']:
 e=E[sc['source_id']]
 R['screening_review'].append({'source_id':sc['source_id'],'status':'retained','focal_exhaustive':sc['source_id'] in P['selection_design']['focal_source_ids'],'rationale':sc['reason'],'source_characters':len(e['text']),'unit_ids':sc['unit_ids'],'evidence':[] if not e['text'] else [ev(sc['source_id'],e['text'])]})
for n,x in U.items():
 if x['record_role']=='statement':
  qev=uniq([ref(x)]+sum([q['evidence'] for q in x['proposition']['qualifiers']],[]))
  rr={'unit_id':n,'status':'corrected' if any(z['unit_id']==n for z in LOG) else 'retained','source_based_assessment':notes[n],'qualifications':{'status':'retained','evidence':qev},'predicate_roles':[],'institutional_support':{'type':x['institution']['type'],'alternatives':x['institution']['type_alternatives'],'authority_assessment':'No focal record meets the specific attributed-authority/enforcement threshold for rule_candidate. Strong modal wording and guide titles are insufficient.','standing_profile':x['institution']['standing_profile'],'evidence':uniq(x['institution']['evidence']+sum([z['evidence'] for k in ['documentary_support','recognition','application_evidence','challenges'] for z in x['institution'][k]],[]))},'disposition_review':{'rationale':'Every merge event identifies PR26586 and is restricted to the broader contribution except U19, where the exact version edit has patch and integration evidence. No current-PR outcome is transferred to a referenced PR, predecessor commit, or unidentified cleanup. No rejection, withdrawal, sanction, or network adoption is inferred.','events':x['disposition_events']},'level_review':{'target':x['statement_target_level'],'observed':x['observed_action_level'],'rationale':x['level_rationale'],'target_alternatives':x['target_level_alternatives'],'observed_alternatives':x['observed_level_alternatives'],'evidence':x['level_evidence']['evidence']}}
  for idx,c in enumerate(x['components']):rr['predicate_roles'].append({'component_index':idx,'symbol':c['symbol'],'text':c['text'],'status':'retained','basis':c['basis'],'occurrence_role':c['occurrence_role'],'rationale':c['inference_note'] or 'The cited local occurrence supplies this role for the selected predicate; the exact argument and any qualifier are preserved. '+notes[n],'evidence':uniq(c['evidence']+[c['governing_span']])})
 else:
  rr={'unit_id':n,'status':'corrected' if any(z['unit_id']==n for z in LOG) else 'retained','source_based_assessment':('Repeated occurrence linked to its represented original; original speech function retained; no independent endorsement or expectation recognition.' if x['record_role']=='quotation' else 'Structural grouping without extra proposition or governed activity.' if x['record_role']=='container' else 'Distinct review act, technical rationale, or report retained as context. It is not treated as an independent prescription, status authority, or sanction.'),'evidence':[ref(x)]}
 R['unit_source_review'].append(rr)
for i,r in enumerate(A['relations']):R['relation_review'].append({'relation_index':i,'from_unit_id':r['from_unit_id'],'to_unit_id':r['to_unit_id'],'type':r['type'],'status':'retained','rationale':r['rationale']+' Direction, shared object, attribution, and explicit-versus-inferred basis checked against both endpoints.','evidence':r['evidence']})
for group in ['observed_outcomes','mechanisms']:
 for i,x in enumerate(A['episode_summary'][group]):
  R['summary_review'].append({'group':group,'index':i,'status':'retained','claim':x['claim'],'clause_review':[{'text':p['text'],'status':'retained','evidence':p['evidence'],'rationale':'Anchors support only the attributed utterance, exact retained change, or recorded event stated. They do not establish causal influence, adoption of a rationale, broader norm acceptance, or network adoption.'} for p in x['claim_parts']],'evidence':x['evidence'],'causal_limit':x.get('alternative_explanation','No causal effect is claimed.')})
# Each emitted checker flag gets an individual resolution, including duplicate same-code flags.
for filename,annotation in [('checks.first.json',F),('checks.mechanical.json',json.loads(Path('annotation.mechanical.json').read_text())),('checks.json',A)]:
 cc=json.loads(Path(filename).read_text());uu={x['unit_id']:x for x in annotation['units']};counter=collections.Counter();relation_flags=[r for r in annotation['relations'] if r['type']=='challenges'];summary_items=[(g,i,x) for g in ['observed_outcomes','mechanisms'] for i,x in enumerate(annotation['episode_summary'][g])]
 for i,f in enumerate(cc['review_flags']):
  n=f.get('unit_id');code=f['code'];ord=counter[(n,code)];counter[(n,code)]+=1;status='retained';evidence=[];text='';specific=None
  if n:
   x=U[n];old=uu[n];evidence=[ref(x)];text=notes.get(n,'Repeated question/technical utterance retains its original speech function; no independent institutional evidence is created.')
   if code=='predicate_audit':
    oldc=old['components'][ord];matches=[c for c in x['components'] if c['symbol']==oldc['symbol']]
    selected=next((c for c in matches if c['text']==oldc['text']),matches[0] if matches else None)
    specific={'component_index_in_checked_file':ord,'checked_symbol':oldc['symbol'],'checked_text':oldc['text']}
    if selected:evidence=uniq(selected['evidence']+[selected['governing_span']]);text=(selected['inference_note'] or 'Explicit local role verified against its governing predicate.')+' '+notes[n]
    if filename!='checks.json' and selected!=oldc:status='corrected'
   elif code=='qualifier_audit':evidence=uniq(evidence+sum([q['evidence'] for q in x['proposition']['qualifiers']],[]))
   elif code=='document_scope':
    d=x['institution']['documentary_support'][ord];evidence=d['evidence'];text=d['rationale']+' Documentary coverage does not establish attributed authority. '+notes[n];specific={'documentary_record_index':ord}
    if d['temporal_fit']!='established':status='unresolved'
   elif code=='application_audit':
    e=x['institution']['application_evidence'][ord];evidence=e['evidence'];text=e['rationale'];specific={'application_record_index':ord}
    if e['status']=='unresolved':status='unresolved'
    elif filename!='checks.json' and e!=old['institution']['application_evidence'][ord]:status='corrected'
   elif code=='challenge_audit':
    e=x['institution']['challenges'][ord];evidence=e['evidence'];text=e['rationale'];specific={'challenge_record_index':ord}
   elif code=='recognition_audit':
    e=[e for e in x['institution']['recognition'] if e['kind']=='expectation_recognition'][ord];evidence=e['evidence'];text=e['rationale'];specific={'expectation_recognition_record_index':ord}
   elif code=='higher_level_audit':
    evidence=x['level_evidence']['evidence'];text=x['level_rationale']+' '+notes[n]
    if filename!='checks.json' and x['observed_action_level']!=old['observed_action_level']:status='corrected'
   elif code=='question_audit':text='Corrected repeated question to question speech act; exact block-quoted source is retained.';status='corrected'
  elif code=='challenge_object':
   r=relation_flags[ord];evidence=r['evidence'];text=r['rationale']+' Both endpoints concern the same quoted claim or a directly contested reason for the current version addition, not unrelated themes.';specific={'relation':{'from':r['from_unit_id'],'to':r['to_unit_id']}}
  elif code=='summary_audit':
   g,j,x=summary_items[ord];final=A['episode_summary'][g][j];evidence=final['evidence'];text='Each material clause is represented in claim_parts and covered by its cited exact report, patch, quoted exchange, or metadata. '+('Mechanism status and alternative explanation explicitly limit causal inference: '+final['alternative_explanation'] if g=='mechanisms' else 'Recorded merge and patch facts are distinguished from reports and assent; broader adoption is not claimed.');specific={'summary_group':g,'summary_index':j}
  assert evidence and text,(filename,i,f)
  R['checker_resolutions'].append({'checker_file':filename,'array':'review_flags','index':i,'flag':f,'status':status,'rationale':text,'evidence':evidence,'specific_record':specific})
 # Errors are retained with transparent unresolved mechanical status or explicit correction.
 docs_counter=collections.Counter()
 for i,f in enumerate(cc['errors']):
  n=f.get('unit_id');code=f['code'];x=U[n];record={'checker_file':filename,'array':'errors','index':i,'flag':f,'status':'unresolved','rationale':'','evidence':[ref(x)]}
  if code=='support_profile':
   record.update(status='corrected',rationale='M01 aligns the unresolved full-proposition application record and recognition target with the after-#26589 evidence limit; later checker runs no longer emit this error.',evidence=x['institution']['application_evidence'][0]['evidence'])
  elif code=='revision':
   k=docs_counter[n];docs_counter[n]+=1;d=x['institution']['documentary_support'][k]
   meta=[]
   for e in d['evidence']:
    z=E[e['source_id']];fields={kk:z[kk] for kk in ['revision','git_blob_sha','object_id','url'] if kk in z}
    if z['kind']=='commit_metadata':
     payload=json.loads(z['text']);fields['serialized_commit_sha']=payload.get('sha')
    meta.append({'source_id':z['source_id'],'supplied_metadata':fields})
   record.update(rationale='Unresolved checker/packet field-name incompatibility, not absent source identity: check_annotation.py line 129 accepts only blob_sha or revision_id, while the frozen packet supplies revision/git_blob_sha and commit SHA in serialized metadata. The documentary evidence and temporal limits are retained. Neither frozen input nor checker was changed, and no mechanical pass is claimed.',evidence=d['evidence'],metadata_evidence=meta,checker_code_reference={'path':'tools/check_annotation.py','line':129,'quote':"if d['date_basis']=='pinned_revision' and not any(entries[e['source_id']].get('blob_sha') or entries[e['source_id']].get('revision_id') for e in d['evidence']):error('revision','Pinned revision claim lacks supplied revision identity',uid)"})
  else:raise RuntimeError('Unreviewed error '+str(f))
  R['checker_resolutions'].append(record)
R['checker_limitation']={'status':'unresolved','remaining_error_count':len(json.loads(Path('checks.json').read_text())['errors']),'classification':'checker/packet metadata field incompatibility','explanation':'Five pinned-revision errors remain. Source identities are supplied under other immutable packet fields, documented individually above. All other official schema/offset/reference/consistency checks pass; this is not an overall checker pass or semantic certification.'}
Path('review_notes.json').write_text(json.dumps(R,ensure_ascii=False,indent=2)+'\n')
# Separate integrity assertions verify logs and freeze, without replacing the assigned checker.
manifest=json.loads(Path('first_complete_manifest.json').read_text());assert manifest['annotation_first_complete_sha256']==hashlib.sha256(Path('annotation.first_complete.json').read_bytes()).hexdigest();assert manifest['packet_sha256']==hashlib.sha256(Path('packet.json').read_bytes()).hexdigest()
assert Path('annotation.json').read_bytes()==Path('annotation.final.json').read_bytes()
assert len(R['screening_review'])==len(P['entries'])
for f in ['checks.first.json','checks.mechanical.json','checks.json']:
 c0=json.loads(Path(f).read_text());assert sum(x['checker_file']==f for x in R['checker_resolutions'])==len(c0['errors'])+len(c0['review_flags'])
# Verify all emitted evidence in the review log remains exact.
anchor_count=0
def anchors(v):
 global anchor_count
 if isinstance(v,dict):
  if set(v)=={'source_id','span'}:
   s=v['span'];assert E[v['source_id']]['text'][s['start']:s['end']]==s['quote'];anchor_count+=1
  for y in v.values():anchors(y)
 elif isinstance(v,list):
  for y in v:anchors(y)
anchors(R);anchors(LOG)
summary={'status':'complete_with_documented_checker_incompatibility','run_id':'F01_v04_r2','unit_counts':R['counts'],'first_complete_unchanged':True,'packet_hash_unchanged_since_first_complete':True,'annotation_json_matches_final':True,'review_log_exact_anchors_verified':anchor_count,'all_checker_flags_and_errors_resolved_in_review_notes':True,'official_final_checker_status':'fail','remaining_official_errors':5,'remaining_error_code':'revision','remaining_error_explanation':R['checker_limitation']['explanation'],'source_review_passes':1,'repair_entries':len(LOG),'meaning_changing_repair_entries':sum(x['meaning_changes'] for x in LOG),'packet_sha256':A['packet_sha256'],'first_complete_sha256':R['first_complete_sha256'],'final_sha256':R['final_sha256']}
Path('completion_record.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
# Access record names every task file content read, created, or executed. Directory listing exposed names only for unused calibration/input manifest.
read_originals=['INSTRUCTIONS.txt','protocol/codebook.txt','protocol/annotation_schema.json','packet.json','tools/check_annotation.py']
written=['build_annotation.py','repair_mechanical.py','source_self_review.py','finalize_logs.py','annotation.json','annotation.first_complete.json','first_complete_manifest.json','checks.first.json','annotation.mechanical.json','checks.mechanical.json','repair_log.json','annotation.final.json','checks.json','review_notes.json','completion_record.json','access_record.json']
record={'run_id':'F01_v04_r2','configuration':'inherited primary configuration','configuration_override':False,'model':{'exposed_role_description':'Codex, an agent based on GPT-6','exact_model_identity':None,'provider_snapshot':None,'seed':None,'sampling':None,'reasoning_effort':None,'token_use':None,'cost':None,'note':'No model identity inferred from protocol, packet, or filenames. Exact provider/runtime model controls were not exposed.'},'runtime':{'tool':'functions.exec invoking exec_command','shell':'bash','python_version':sys.version,'python_implementation':platform.python_implementation(),'working_directory':str(Path.cwd()),'libraries':'Python standard library plus checker-owned jsonschema dependency','network_requests':0,'agents_spawned':0},'research_access_boundary':str(Path.cwd()),'original_inputs':[{'path':f,'access':'read only; checker additionally executed for three recorded results' if f.endswith('check_annotation.py') else 'read only','sha256':hashlib.sha256(Path(f).read_bytes()).hexdigest()} for f in read_originals],'output_files':[{'path':f,'access':'created and, where required for checking/review, read or executed'} for f in written],'names_only_observed':['input_manifest.json','calibration/cases.json','calibration/packet.json','calibration/annotation.json'],'not_accessed':'No contents of input_manifest or calibration files, no parent directories, no other runs, no Library, no web, no external research, and no other-agent research output.','generation_notes':['Initial multi-file read was truncated by tool output; the complete protocol, schema, and packet were subsequently read in bounded nontruncated chunks.','One initial construction run failed before writing annotation.json because the local helper duplicated a keyword; the helper was repaired before first-complete output.','First-complete output was copied before any checker execution or source self-review.','One mechanical feedback repair phase and one complete source-based self-review were conducted; all assigned checker results are preserved.']}
Path('access_record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,indent=2))
