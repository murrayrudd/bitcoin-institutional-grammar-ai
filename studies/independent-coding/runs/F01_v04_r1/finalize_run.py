from pathlib import Path
import json,hashlib,datetime,sys,platform,collections
import jsonschema
root=Path.cwd();a=json.loads(Path('annotation.final.json').read_text());p=json.loads(Path('packet.json').read_text());s=json.loads(Path('protocol/annotation_schema.json').read_text());checks=json.loads(Path('checks.json').read_text());freeze=json.loads(Path('freeze_record.json').read_text());review=json.loads(Path('review_notes.json').read_text());rep=json.loads(Path('repair_log.json').read_text())
jsonschema.Draft202012Validator(s).validate(a)
assert Path('annotation.json').read_bytes()==Path('annotation.final.json').read_bytes()
unchanged={name:hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest for name,digest in freeze['files'].items()}
assert all(unchanged.values())
assert a['packet_sha256']==hashlib.sha256(Path('packet.json').read_bytes()).hexdigest()
assert {e['code'] for e in checks['errors']}=={'revision'} and len(checks['errors'])==3
assert {e['unit_id'] for e in checks['errors']}=={'S09','S26','S34'}
assert len(review['unit_reviews'])==len(a['units'])
assert len(review['screening_reviews'])==len(p['entries'])
# All recorded source anchors in the final annotation, audit notes, and before/after log remain literal packet text.
texts={e['source_id']:e['text'] for e in p['entries']};anchor_count=0
def walk(v):
 global anchor_count
 if isinstance(v,dict):
  if 'source_id' in v and 'span' in v:
   sp=v['span'];t=texts[v['source_id']];assert t[sp['start']:sp['end']]==sp['quote'];anchor_count+=1
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
for d in [a,review,rep]:walk(d)
verification={'run_id':'F01_v04_r1','completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'schema_valid':True,'packet_hash_valid':True,'first_complete_and_frozen_inputs_unchanged':unchanged,'final_working_copy_identical':True,'recorded_source_anchors_verified':anchor_count,'official_checker_status':checks['status'],'remaining_coding_errors':0,'remaining_packet_checker_compatibility_errors':checks['errors'],'checker_feedback_occurrences_documented':{'review_flags':len(review['checker_flag_resolutions']),'errors':len(review['checker_error_resolutions'])},'unit_counts':dict(collections.Counter(u['record_role'] for u in a['units'])),'entry_screening_counts':dict(collections.Counter(e['disposition'] for e in a['entry_screening'])),'one_complete_source_review':True,'source_review_changes':len(rep['changes'])}
Path('verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2)+'\n')
research=['INSTRUCTIONS.txt','protocol/codebook.txt','protocol/annotation_schema.json','packet.json','tools/check_annotation.py']
generated_read=['build_annotation.py','repair_mechanical.py','source_self_review.py','write_review_notes.py','finalize_run.py','annotation.json','annotation.first_complete.json','annotation.postmechanical.json','annotation.selfreview.01.json','annotation.final.json','checks.first.json','checks.postmechanical.json','checks.selfreview.01.json','checks.json','freeze_record.json','repair_log.json','review_notes.json']
written=['build_annotation.py','repair_mechanical.py','source_self_review.py','write_review_notes.py','finalize_run.py','annotation.json','annotation.first_complete.json','annotation.postmechanical.json','annotation.selfreview.01.json','annotation.final.json','checks.first.json','checks.postmechanical.json','checks.selfreview.01.json','checks.json','freeze_record.json','repair_log.json','review_notes.json','verification.json','access_record.json','final_manifest.json','completion_record.json']
access={'run_id':'F01_v04_r1','authorized_directory':str(root),'research_files_accessed':[{'path':str(root/name),'access':'read','sha256':hashlib.sha256(Path(name).read_bytes()).hexdigest()} for name in research],'generated_files_accessed':[{'path':str(root/name),'access':'read_and_written'} for name in generated_read],'files_written':[str(root/name) for name in written],'directory_listing':'rg --files . listed filenames inside the run only. Calibration filenames and input_manifest.json were visible in that listing but their contents were not read.','ordinary_runtime_libraries':'Python standard library and jsonschema (including runtime imports) only; no external research or runtime documentation was consulted.','external_research_sources_accessed':[],'other_runs_or_parent_directories_read':False,'calibration_contents_read':False,'agents_spawned':False,'frozen_inputs_modified':False,'configuration':{'inheritance':'Inherited primary configuration; no model, reasoning, sampling, or provider override applied.','exposed_assistant_role':'Codex','exposed_developer_family_description':'An agent based on GPT-6; this is not a provider snapshot identifier.','model_identifier':None,'provider_snapshot':None,'reasoning_effort':None,'seed':None,'sampling':None,'token_use':None,'cost':None,'configuration_inference_from_files':False},'runtime':{'python_version':sys.version,'python_executable':sys.executable,'platform':platform.platform(),'shell':'bash','timezone_from_task_context':'Etc/UTC'},'limitations':['Filesystem reads by the Python runtime and installed libraries are ordinary execution dependencies, not additional research inputs.','Actual provider model snapshot, seed, sampling parameters, token consumption, and cost were not exposed to this coder.']}
Path('access_record.json').write_text(json.dumps(access,ensure_ascii=False,indent=2)+'\n')
completion={'run_id':'F01_v04_r1','episode_id':'F01','status':'complete_with_documented_packet_checker_compatibility_limit','counts':{'screened_entries':42,'exhaustive_focal_entries':23,'units':60,'statements':34,'context_units':14,'quotation_units':12,'relations':34,'outcomes':3,'mechanisms':3},'final_annotation':str(root/'annotation.final.json'),'first_complete':str(root/'annotation.first_complete.json'),'final_check':str(root/'checks.json'),'source_review':str(root/'review_notes.json'),'repair_log':str(root/'repair_log.json'),'access_record':str(root/'access_record.json'),'unresolved_limits':['Three official-checker revision-key compatibility errors: the packet supplies revision/git_blob_sha while the checker expects revision_id/blob_sha. Frozen source and checker were preserved.','Interpretive uncertainty about technical obligation, bot pronoun reference, tentative expectation recognition, source timing, missing implementation history, and reasons for merger remains explicit.'],'coding_errors_remaining':0}
Path('completion_record.json').write_text(json.dumps(completion,ensure_ascii=False,indent=2)+'\n')
manifest={'run_id':'F01_v04_r1','files':{name:{'sha256':hashlib.sha256(Path(name).read_bytes()).hexdigest(),'bytes':Path(name).stat().st_size} for name in written if name!='final_manifest.json'}}
Path('final_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':completion['status'],'counts':completion['counts'],'anchors_checked':anchor_count,'schema_valid':True,'official_checker_errors':checks['errors']},indent=2))
