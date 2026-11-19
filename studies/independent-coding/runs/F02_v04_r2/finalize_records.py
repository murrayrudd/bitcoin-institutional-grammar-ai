import json,hashlib,sys
from pathlib import Path
from datetime import datetime,timezone
B=Path(__file__).resolve().parent
r=json.loads((B/'review_notes.json').read_text())
c=json.loads((B/'checks.json').read_text());cf=json.loads((B/'checks.first.json').read_text())
a=json.loads((B/'annotation.final.json').read_text())
assert c['status']=='pass' and not c['errors']
assert c['review_flags']==cf['review_flags']
assert len(r['checker_flag_resolutions'])==len(c['review_flags'])
assert hashlib.sha256((B/'annotation.first_complete.json').read_bytes()).hexdigest()==r['first_complete_sha256']
assert a['packet_sha256']==hashlib.sha256((B/'packet.json').read_bytes()).hexdigest()
assert (B/'annotation.json').read_bytes()==(B/'annotation.final.json').read_bytes()
r['final_checker']={'file':'checks.json','status':c['status'],'error_count':len(c['errors']),'review_flags_identical_to_first_checker':True,'resolution_mapping':'Every checks.json review_flags index maps to the same flag_index in checker_flag_resolutions; the retained/corrected/unresolved source review dispositions apply to both preserved checker results.','review_flag_count':len(c['review_flags']),'exact_anchor_references':c['exact_anchor_references'],'additional_source_review_performed':False}
(B/'review_notes.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')

read_inputs=['INSTRUCTIONS.txt','protocol/codebook.txt','protocol/annotation_schema.json','packet.json','tools/check_annotation.py']
written_files=['build_annotation.py','annotation.json','annotation.first_complete.json','checks.first.json','source_review.py','annotation.final.json','repair_log.json','review_notes.json','checks.json','finalize_records.py','access_record.json','run_log.json']
file_records=[]
for x in read_inputs:
 file_records.append({'path':str(B/x),'access':['read']+(['executed'] if x=='tools/check_annotation.py' else []),'category':'frozen_input','modified':False,'sha256':hashlib.sha256((B/x).read_bytes()).hexdigest()})
for x in written_files:
 modes=['written']
 if x not in ['access_record.json','run_log.json']:modes+=['read']
 if x.endswith('.py'):modes+=['executed']
 file_records.append({'path':str(B/x),'access':modes,'category':'run_output_or_reproducibility_script','modified':True})
access={'run_id':'F02_v04_r2','allowed_research_directory':str(B),'research_inputs':read_inputs,'files_accessed':file_records,'ordinary_runtime_access':{'python_version':sys.version,'python_implementation':sys.implementation.name,'sys_platform':sys.platform,'standard_modules':['json','hashlib','copy','sys','platform','pathlib','datetime'],'checker_runtime_library':'jsonschema','note':'Ordinary Python runtime/library modules loaded for execution; no outside research materials, network, Library, other run, calibration example, or parent-directory research file was accessed.'},'model_runtime_configuration':{'configuration':'inherited primary configuration without override','model_identifier':None,'provider_snapshot':None,'reasoning_effort':None,'seed':None,'sampling':None,'token_use':None,'cost':None,'model_override_used':False,'configuration_provenance':'Only inherited-primary/no-override dispatch is exposed for this coding run. No model identity is inferred from the protocol, file names, or tool registry.'},'independence':{'agents_spawned':False,'outside_sources_used':False,'other_annotations_accessed':False,'messages_to_coordinator':'Progress and completion counts/limits only; no other-coder data received.'},'recorded_at_utc':datetime.now(timezone.utc).isoformat()}
(B/'access_record.json').write_text(json.dumps(access,ensure_ascii=False,indent=2)+'\n')
artifacts=['annotation.first_complete.json','checks.first.json','annotation.json','annotation.final.json','checks.json','repair_log.json','review_notes.json','access_record.json']
log={'run_id':'F02_v04_r2','episode_id':'F02','packet_sha256':a['packet_sha256'],'stages':[{'stage':1,'action':'Read assigned instructions, complete v0.4 codebook/schema, and complete packet within run directory.'},{'stage':2,'action':'Completed all entry screening and first annotation; preserved annotation.first_complete.json before checks or source self-review.'},{'stage':3,'action':'Executed python3 tools/check_annotation.py packet.json annotation.json; preserved checks.first.json.','result':'pass; no mechanical errors; 36 source-review flags'},{'stage':4,'action':'Completed one source-based self-review and recorded eight changes in repair_log.json; preserved first-complete file.','source_review_count':1},{'stage':5,'action':'Saved annotation.final.json and ran the supplied checker on it; preserved checks.json.','result':'pass; no mechanical errors; same 36 review flags, all addressed by indexed resolutions'},{'stage':6,'action':'Saved access/configuration record and final artifact hashes; verified first-complete freeze and packet hash.'}],'counts':{'screened_entries':len(a['entry_screening']),'focal_sources':16,'supplemental_sources':6,'candidate_entries':sum(s['disposition']=='candidate' for s in a['entry_screening']),'context_only_entries':sum(s['disposition']=='context_only' for s in a['entry_screening']),'empty_entries':sum(s['disposition']=='empty' for s in a['entry_screening']),'units':len(a['units']),'statement_units':sum(u['record_role']=='statement' for u in a['units']),'context_units':sum(u['record_role']=='context' for u in a['units']),'relations':len(a['relations']),'observed_outcomes':len(a['episode_summary']['observed_outcomes']),'mechanisms':len(a['episode_summary']['mechanisms']),'source_review_changes':8,'checker_flags':len(c['review_flags']),'checker_errors':0},'artifact_hashes':{x:hashlib.sha256((B/x).read_bytes()).hexdigest() for x in artifacts},'unresolved_limits':a['episode_summary']['unresolved_questions'],'completion_status':'complete_with_explicit_source_limits','finished_at_utc':datetime.now(timezone.utc).isoformat()}
(B/'run_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':log['completion_status'],'counts':log['counts'],'files':artifacts+['run_log.json']}))
