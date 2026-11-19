from pathlib import Path
import json, hashlib, sys
from datetime import datetime,timezone
from collections import Counter
ROOT=Path(__file__).resolve().parent
load=lambda n:json.loads((ROOT/n).read_bytes())
sha=lambda n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest()
def save(n,x):(ROOT/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
first=load('annotation.first_complete.json'); final=load('annotation.final.json'); checks=load('checks.json'); cfirst=load('checks.first.json')
assert checks['status']=='pass' and not checks['errors']
assert checks['review_flags']==cfirst['review_flags']
assert (ROOT/'annotation.json').read_bytes()==(ROOT/'annotation.final.json').read_bytes()

def diffs(a,b,path=''):
 if type(a)!=type(b): return [path]
 if isinstance(a,dict):
  assert a.keys()==b.keys()
  return [p for k in a for p in diffs(a[k],b[k],path+'/'+k)]
 if isinstance(a,list):
  assert len(a)==len(b)
  return [p for i,(x,y) in enumerate(zip(a,b)) for p in diffs(x,y,path+'/'+str(i))]
 return [] if a==b else [path]
delta=diffs(first,final)
assert delta==['/episode_summary/observed_outcomes/1/claim'],delta
notes=load('review_notes.json')
notes['mechanical_feedback']['final_status']=checks['status']
notes['mechanical_feedback']['final_errors']=checks['errors']
notes['mechanical_feedback']['final_review_flag_count']=len(checks['review_flags'])
notes['mechanical_feedback']['final_flags_match_reviewed_first_flags']=True
notes['integrity']={'first_complete_sha256':sha('annotation.first_complete.json'),'final_sha256':sha('annotation.final.json'),'actual_changed_paths':delta,'all_changes_logged':True}
save('review_notes.json',notes)
counts={'entries':len(final['entry_screening']),'focal_entries':16,'screening':dict(Counter(x['disposition'] for x in final['entry_screening'])),'units':len(final['units']),'record_roles':dict(Counter(u['record_role'] for u in final['units'])),'relations':len(final['relations']),'recognition_events':sum(len(u['institution']['recognition']) for u in final['units']),'disposition_events':sum(len(u['disposition_events']) for u in final['units']),'outcomes':len(final['episode_summary']['observed_outcomes']),'mechanisms':len(final['episode_summary']['mechanisms']),'review_flags':len(checks['review_flags']),'review_flags_addressed':len(notes['checker_flag_resolutions']),'repairs':1}
save('execution_log.json',{
 'run_id':'F02_v03_r3','episode_id':'F02',
 'stages':[
 {'order':1,'action':'Read assigned instructions, complete codebook, complete schema, and complete packet; no calibration or external material accessed.'},
 {'order':2,'action':'Created full annotation and froze first complete output before checker execution or source self-review.','artifacts':['annotation.json','annotation.first_complete.json']},
 {'order':3,'command':'python3 tools/check_annotation.py packet.json annotation.json > checks.first.json','exit_code':0,'status':cfirst['status'],'errors':len(cfirst['errors']),'review_flags':len(cfirst['review_flags'])},
 {'order':4,'action':'Performed one complete source-based self-review. Retained all five flags with source explanations and made one logged temporal-claim correction.','artifacts':['repair_log.json','review_notes.json','annotation.final.json']},
 {'order':5,'command':'python3 tools/check_annotation.py packet.json annotation.json > checks.json','exit_code':0,'status':checks['status'],'errors':len(checks['errors']),'review_flags':len(checks['review_flags'])},
 {'order':6,'action':'Verified final working annotation equals final saved annotation, reviewed flags are unchanged, and first-to-final diff matches the single repair log entry.'}
 ],'counts':counts,'finished_at_utc':datetime.now(timezone.utc).isoformat()})
inputs=[('INSTRUCTIONS.txt',['read']),('protocol/codebook.txt',['read']),('protocol/annotation_schema.json',['read','checker_dependency']),('packet.json',['read','checker_input']),('tools/check_annotation.py',['execute'])]
outputs=[('build_annotation.py',['write','execute']),('finalize_review.py',['write','execute']),('close_run.py',['write','execute']),('annotation.json',['write','read','checker_input']),('annotation.first_complete.json',['write_once_before_checks','read']),('checks.first.json',['write','read']),('annotation.final.json',['write','read']),('checks.json',['write','read']),('repair_log.json',['write']),('review_notes.json',['write','read','update_final_checker_metadata']),('execution_log.json',['write']),('access_record.json',['write']),('output_manifest.json',['write'])]
access={
 'run_id':'F02_v03_r3','episode_id':'F02','authorized_directory':str(ROOT),
 'research_inputs':[{'path':str(ROOT/n),'access_modes':m,'sha256':sha(n)} for n,m in inputs],
 'generated_files':[{'path':str(ROOT/n),'access_modes':m} for n,m in outputs],
 'access_limits':{'all_research_access_within_authorized_directory':True,'parent_directories_read':False,'other_runs_read':False,'library_accessed':False,'web_accessed':False,'outside_research_accessed':False,'calibration_files_read':False,'agents_spawned':False,'post_dispatch_sources_added':False,'frozen_inputs_modified':False},
 'configuration':{'selection':'inherited_primary_configuration','override_requested':False,'model_identity':None,'reasoning_effort':None,'provider_snapshot':None,'seed':None,'sampling_parameters':None,'token_use':None,'cost':None,
 'exposure_note':'The task specifies inherited primary configuration with no override. Actual model identifier and reasoning setting are not independently exposed to this run. No model identity is inferred from historical configurations in the protocol.'},
 'runtime':{'shell':'bash','python_version':sys.version,'python_executable':sys.executable,'ordinary_libraries_used':['json','hashlib','pathlib','collections','datetime','sys'],'runtime_library_source_files_individually_inspected':False},
 'source_integrity':{'packet_sha256':sha('packet.json'),'annotation_packet_sha256_matches':final['packet_sha256']==sha('packet.json'),'first_complete_sha256':sha('annotation.first_complete.json'),'final_sha256':sha('annotation.final.json')},
 'access_log_note':'File accesses include direct reads/writes and execution of local scripts/checker. Standard Python runtime imports are ordinary runtime dependencies, not additional research inputs. Inline Python commands read only the listed assigned or generated files.'}
save('access_record.json',access)
artifact_names=['annotation.first_complete.json','checks.first.json','annotation.json','annotation.final.json','checks.json','repair_log.json','review_notes.json','access_record.json','execution_log.json','build_annotation.py','finalize_review.py','close_run.py']
save('output_manifest.json',{'run_id':'F02_v03_r3','packet_sha256':sha('packet.json'),'counts':counts,'artifacts':[{'path':str(ROOT/n),'bytes':(ROOT/n).stat().st_size,'sha256':sha(n)} for n in artifact_names]})
print(json.dumps({'complete':True,'checker_status':checks['status'],'counts':counts,'final_annotation':str(ROOT/'annotation.final.json'),'review_notes':str(ROOT/'review_notes.json'),'access_record':str(ROOT/'access_record.json'),'manifest':str(ROOT/'output_manifest.json')},indent=2))
