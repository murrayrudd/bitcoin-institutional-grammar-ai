import json,hashlib,sys,platform,copy
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
A=json.loads((ROOT/'annotation.final.json').read_text());P=json.loads((ROOT/'packet.json').read_text());L=json.loads((ROOT/'repair_log.json').read_text());S={e['source_id']:e for e in P['entries']};U={u['unit_id']:u for u in A['units']}
def E(s,q=None,start=None):
 t=S[s]['text'];q=t if q is None else q;start=t.index(q) if start is None else start;assert t[start:start+len(q)]==q;return {'source_id':s,'span':{'start':start,'end':start+len(q),'quote':q}}
def ev(i):u=U[i];return E(u['source_id'],u['span']['quote'],u['span']['start'])
def hashfile(n):return hashlib.sha256((ROOT/n).read_bytes()).hexdigest()
checks=['checks.first.json','checks.mechanical.json','checks.pre_final_missing.json','checks.source_review_stage1.json','checks.json']
corrected_pairs={('u06','Bdir'),('u08','Bdir'),('u09','A'),('u13','I'),('u24','Cex')}
notes=[]
for filename in checks:
 c=json.loads((ROOT/filename).read_text())
 for field in ['errors','review_flags']:
  for k,f in enumerate(c.get(field,[])):
   i=f.get('unit_id');sym=f.get('symbol');unit=U.get(i);cs=[x for x in unit['components'] if x['symbol']==sym] if unit else []
   # Match the present token or phrase where an indexed field has several components.
   oldquote=f.get('evidence',{}).get('span',{}).get('quote')
   target=next((x for x in cs if any(z['span']['quote']==oldquote for z in x['evidence'])),cs[0] if cs else None)
   status='retained';why=''
   if filename=='checks.first.json' and (i,sym) in corrected_pairs:
    status='corrected';why='The first annotation chose an earlier source occurrence or token fragment. The intended complete token now anchors the same role within the focal unit. No token exception was used.'
   elif filename=='checks.first.json' and f.get('message')=='explicit pragmatic argument requires role-preservation explanation':
    status='corrected';why='The required role-preservation explanation was absent. The final pragmatic parse keeps the source actor or object relation and supplies a source-based explanation.'
    sym='A' if i=='u15' else 'Bdir';target=next(x for x in unit['components'] if x['symbol']==sym)
   elif filename=='checks.first.json' and f.get('kind')=='pragmatic_explicit_argument' and not f.get('note'):
    status='corrected';why='The missing role-preservation explanation was added and then checked against the actual causative subject or verb-object relation.'
   elif i=='u27' and sym=='A' and filename in ['checks.first.json','checks.mechanical.json']:
    status='corrected';why='The shared actor is now anchored to the main-clause you will either need to, rather than the earlier conditional you want. The shared subject still governs remove and explain.'
   else:
    why=(target['inference_note'] if target else f.get('note',''))
    if not why:why='The exact unit occurrence and associated relation support the retained interpretation; no mechanical error remains.'
   evidence=([ev(i)] if unit else [])+(copy.deepcopy(target['evidence']) if target else [])
   notes.append({'checker_file':filename,'checker_field':field,'item_index':k,'checker_item':f,'status':status,'resolution':why,'evidence':evidence})

focus=set(P['selection_design']['focal_source_ids'])
entry_reviews=[]
for sc in A['entry_screening']:
 s=sc['source_id'];e=S[s];focal=s in focus
 if not e['text']:evidence=[]
 elif focal:evidence=[E(s)]
 elif s=='guide:contributing':evidence=[E(s,'Whether a pull request is merged into Bitcoin Core rests with the project merge\nmaintainers.'),E(s,'The following applies to code changes to the Bitcoin Core project (and related\nprojects such as libsecp256k1), and is not to be confused with overall Bitcoin\nNetwork Protocol consensus changes.')]
 elif e['kind']=='patch':evidence=[E(s,e['text'][:min(220,len(e['text']))])]
 else:evidence=[E(s)]
 entry_reviews.append({'source_id':s,'review_scope':'exhaustive focal propositions' if focal else 'supplemental context screening, not exhaustive extraction','status':'corrected' if s in ['pr26586:comments:11','pr26586:comments:4'] else 'retained','disposition':sc['disposition'],'unit_ids':sc['unit_ids'],'finding':sc['reason'],'evidence':evidence})

unit_reviews=[]
for u in A['units']:
 changes=[x['change_id'] for x in L if x.get('unit_id')==u['unit_id']]
 comp_notes=[]
 for c in u['components']:
  comp_notes.append({'symbol':c['symbol'],'text':c['text'],'basis':c['basis'],'occurrence_role':c['occurrence_role'],'assessment':c['inference_note'] or 'The exact local source phrase supplies this role in the chosen parse; no actor, duty, or object is added from occupational assumptions.','evidence':c['evidence']})
 unit_reviews.append({'unit_id':u['unit_id'],'status':'corrected' if changes else 'retained','change_ids':changes,'source_evidence':[ev(u['unit_id'])],'boundary_and_qualification_review':'The final span and any explicitly explained shared/contextual evidence preserve the focal action, negation, conditions, object identity, and material qualifications. Repeated quotations do not count as new expectations.' if u['record_role']=='statement' else 'Nonstatement role retained; no grammatical components, institutional type, or target-level claim is attributed to this context/quotation record.','component_review':comp_notes,'force_and_institution_review':u['institution']['rationale'],'level_review':u['level_rationale'],'retained_alternative':u['alternative_interpretation'],'remaining_uncertainty':u['uncertainty_reason']})
relation_reviews=[]
for n,r in enumerate(A['relations']):
 relation_reviews.append({'relation_index':n,'from_unit_id':r['from_unit_id'],'to_unit_id':r['to_unit_id'],'type':r['type'],'status':'retained','finding':r['rationale'],'basis':r['basis'],'evidence':r['evidence']})
event_reviews=[]
for u in A['units']:
 for field,events in [('recognition',u['institution']['recognition']),('disposition_events',u['disposition_events'])]:
  for n,e in enumerate(events):event_reviews.append({'unit_id':u['unit_id'],'field':field,'event_index':n,'status':'retained','kind':e['kind'],'target':e['target'],'basis':e['basis'],'finding':e['rationale'],'evidence':e['evidence']})
claim_reviews=[]
for field in ['observed_outcomes','mechanisms']:
 for n,x in enumerate(A['episode_summary'][field]):
  claim_reviews.append({'field':field,'index':n,'status':'retained','claim':x['claim'],'assessment':'Every material positive clause is covered by the cited report, question, quotation, patch, or recorded status. Reports remain attributed, head patches are snapshots, and sequence is not identified causation. General rule adoption and network adoption are not asserted.','evidence':x['evidence']})
review={
 'run_id':'F01_v03_r3','episode_id':'F01','packet_sha256':A['packet_sha256'],'complete_source_based_self_review_count':1,
 'review_order':['First complete annotation frozen before checks or self-review','First checker output retained','Mechanical occurrence/explanation repair and passing checker output retained','One complete source-based self-review of all focal entries, all supplemental screens, units, relations, events, and summary claims','Source-review repairs and intermediate/final checker outputs retained','All checker flags individually resolved with source evidence'],
 'scope_statement':'All 23 focal entries were exhaustively screened, including 3 empty reviews. All 19 supplements were read and screened as context, without claiming they lack institutional content. No post-dispatch source was obtained.',
 'checker_resolution':notes,
 'workflow_errors':[{'artifact':'checks.pre_final_missing.json','status':'corrected','finding':'A syntax error in the source-review script stopped execution before any annotation write; the following checker invocation encountered a missing annotation.final.json. Its output is preserved. The script syntax was corrected, the intended single source-review changes were applied once, and subsequent final checks passed. This was a workflow error, not a source finding.'}],
 'entry_reviews':entry_reviews,'unit_reviews':unit_reviews,'relation_reviews':relation_reviews,'event_reviews':event_reviews,'summary_claim_reviews':claim_reviews,
 'cross_cutting_findings':[
  {'topic':'predicate roles','status':'corrected','finding':'The first occurrence helper selected five inappropriate token/occurrence anchors; these were corrected without token exceptions. Source review also moved remove/explain actors to the main predicate and retained explicit embedded roles for adding v24 and not rushing integration. The action repeat is separate from its procedure object.','evidence':[ev('u01'),ev('u06'),ev('u08'),ev('u09'),ev('u10'),ev('u13'),ev('u23'),ev('u24'),ev('u26'),ev('u27')]},
  {'topic':'omissions','status':'corrected','finding':'The directional priority of testing ancient-wallet loading in modern versions was added as an uncertain indirect recommendation (u33). The later drop/host alternatives remain separate actions.','evidence':[ev('u33'),ev('u17'),ev('u18')]},
  {'topic':'relation scope','status':'corrected','finding':'The current-PR NACK was not retained as a challenge to historical recurrence. The miniscript objection targets the applicable rationale, not the distinct #25717 claim. The low-cost reply is uptake with concession, and the future-cost challenge and adjacent cost explanation retain inferred basis.','evidence':[ev('c03'),ev('u01'),ev('c04b'),ev('c05a'),ev('c05b'),ev('c06a'),ev('c07'),ev('c09'),ev('u14')]},
  {'topic':'authority and sanctions','status':'retained','finding':'No focal rule_candidate, attributed enforcement action, or authorizes/applies relation is asserted. Dated guidance documents general repository roles but does not supply commenter-specific authority for the release-selection demands. The bot O relation is an announced procedural effect, not an observed sanction.','evidence':[ev('u05'),ev('u06'),ev('u25'),ev('u26'),ev('u27'),E('guide:contributing','Whether a pull request is merged into Bitcoin Core rests with the project merge\nmaintainers.')]},
  {'topic':'specific recognition','status':'retained','finding':'Only u30 receives locally_supported standing: the recurring minimum is quoted and tentatively agreed to. A technical-assent-only alternative is retained. Broad tACK, implementation reports, and metadata status do not establish recognized obligation.','evidence':[ev('u30'),ev('q12'),ev('c15d'),ev('c15a'),ev('c13b')]},
  {'topic':'disposition and outcome scope','status':'retained','finding':'Reported rebase/update are proposition-specific with contextual attribution. Recorded merge is broader_proposal. No optional alternative is marked rejected simply because the PR later merged, and no merge certifies a general rule or network adoption.','evidence':[ev('u08'),ev('c13a'),ev('u19'),ev('c13b'),E('pr26586:metadata','"merged": true'),E('pr26586:metadata','"merged_at": "2023-02-16T14:04:28+00:00"')]},
  {'topic':'levels','status':'retained','finding':'Operational target actions are distinguished from collective-choice deliberation over recurring inclusion criteria. Bounded collective-choice target alternatives remain for those criteria. No constitutional or epistemic focal decision is established.','evidence':[ev('u09'),ev('u25'),ev('u30'),ev('u31')]},
  {'topic':'unresolved references and modalities','status':'unresolved','finding':'The bot ignored object remains ambiguous. Exploratory can may describe capability, recommendation, or permission; these are not resolved by automatic role inference. The exact cleanup action under that remains bounded by the prior criterion and remove-or-explain alternatives.','evidence':[ev('u06'),ev('u12'),ev('u13'),ev('u16'),ev('u24'),ev('u29')]}
 ],
 'remaining_limits':A['episode_summary']['missing_evidence'],'unresolved_questions':A['episode_summary']['unresolved_questions'],
 'conclusion':'Mechanical checks pass. Source review retains explicit uncertainty and defensible alternatives; this is an independently produced annotation, not semantic certification or an external consensus label.'}
(ROOT/'review_notes.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')

frozen=json.loads((ROOT/'first_complete_freeze.json').read_text())
assert hashfile('annotation.first_complete.json')==frozen['sha256']
assert (ROOT/'annotation.json').read_bytes()==(ROOT/'annotation.final.json').read_bytes()
assert json.loads((ROOT/'checks.json').read_text())['status']=='pass'
counts={'entries_screened':len(A['entry_screening']),'focal_entries':len(focus),'supplemental_entries':len(S)-len(focus),'units':len(A['units']),'statement_units':sum(u['record_role']=='statement' for u in A['units']),'context_units':sum(u['record_role']=='context' for u in A['units']),'quotation_units':sum(u['record_role']=='quotation' for u in A['units']),'relations':len(A['relations']),'mechanisms':len(A['episode_summary']['mechanisms']),'outcomes':len(A['episode_summary']['observed_outcomes']),'final_checker_flags':len(json.loads((ROOT/'checks.json').read_text())['review_flags']),'repair_log_entries':len(L)}
written=['build_annotation.py','repair_mechanical.py','source_self_review.py','finish_role_review.py','final_reporting.py','annotation.json','annotation.first_complete.json','annotation.final.json','first_complete_freeze.json','checks.first.json','checks.mechanical.json','checks.pre_final_missing.json','checks.source_review_stage1.json','checks.json','repair_log.json','review_notes.json','access_record.json','completion_summary.json','output_manifest.json']
inputs=['INSTRUCTIONS.txt','protocol/codebook.txt','protocol/annotation_schema.json','packet.json','tools/check_annotation.py']
access={
 'run_id':'F01_v03_r3','sole_research_and_write_directory':str(ROOT),'input_files_accessed':[{'path':str(ROOT/n),'mode':'read_only','sha256':hashfile(n)} for n in inputs],
 'generated_files_accessed':[{'path':str(ROOT/n),'mode':'created/read or executed as locally generated output'} for n in written],
 'source_access':'Only the assigned packet was used as research data. Codebook/schema/checker/instructions were execution materials. No parent directories, other runs, optional calibration files, external research, Library, web, or other agents were accessed.',
 'coordination':'Status-only messages were sent to the parent coordinator. No other coding outputs or semantic keys were received.',
 'runtime':{'python_version':platform.python_version(),'python_implementation':platform.python_implementation(),'python_executable':sys.executable,'standard_modules_used':['json','hashlib','pathlib','copy','sys','platform','datetime'],'checker_runtime_dependency':'jsonschema','library_or_runtime_documentation_read':[]},
 'model_configuration':{'configuration_source':'Inherited primary configuration from the parent run; no model or reasoning override requested or made.','model_identifier':None,'reasoning_effort':None,'provider_snapshot':None,'seed':None,'sampling':None,'temperature':None,'token_use':None,'cost':None,'note':'No effective provider-specific model identifier or sampling configuration was exposed to this coder. Historical model names in protocol files were not used to infer the active configuration.'},
 'frozen_input_integrity':'No original input file was edited. The first-complete hash remains identical to the recorded pre-check freeze.',
 'scope_exception':'All generated artifacts stay inside the specifically authorized run directory; no generic storage destination was accessed.'}
(ROOT/'access_record.json').write_text(json.dumps(access,ensure_ascii=False,indent=2)+'\n')
summary={'run_id':'F01_v03_r3','episode_id':'F01','complete':True,'counts':counts,'checker_status':'pass','complete_source_self_reviews':1,'packet_sha256':A['packet_sha256'],'first_complete_sha256':hashfile('annotation.first_complete.json'),'final_sha256':hashfile('annotation.final.json'),'unresolved_limits':['Bot ignored-object referent; technical capability versus permission; tentative expectation recognition versus technical assent; authority/enforcement; exact contribution causation; general policy adoption.'],'output_directory':str(ROOT),'primary_outputs':['annotation.first_complete.json','annotation.final.json','checks.first.json','checks.json','repair_log.json','review_notes.json','access_record.json']}
(ROOT/'completion_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
manifest={'run_id':'F01_v03_r3','files':[{'path':n,'sha256':hashfile(n),'bytes':(ROOT/n).stat().st_size} for n in written if n!='output_manifest.json'],'original_input_hashes':{n:hashfile(n) for n in inputs}}
(ROOT/'output_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
