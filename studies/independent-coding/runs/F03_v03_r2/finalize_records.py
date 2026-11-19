import json, hashlib, sys
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
ROOT=Path(__file__).resolve().parent
read=lambda name:json.loads((ROOT/name).read_text())
a=read('annotation.final.json');first=read('checks.first.json');last=read('checks.json');notes=read('review_notes.json');repairs=read('repair_log.json');manifest=read('input_manifest.json')
U={u['unit_id']:u for u in a['units']}
def ue(uid): return {'source_id':U[uid]['source_id'],'span':U[uid]['span']}
assert first['status']=='pass' and last['status']=='pass'
assert (ROOT/'annotation.json').read_bytes()==(ROOT/'annotation.final.json').read_bytes()
assert hashlib.sha256((ROOT/'annotation.first_complete.json').read_bytes()).hexdigest()==repairs['first_complete_sha256']
integrity=[]
for name,h in manifest['files'].items():
    found=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    integrity.append({'file':name,'expected_sha256':h,'actual_sha256':found,'unchanged':found==h})
assert all(x['unchanged'] for x in integrity)

reason={
('U02','outside_unit','Bdir'):'Retain the external antecedent evidence. This in the reservation points to the body\'s checkbox proposal and missing replacement capability. Bdir under inferred deferral is context_inferred/semantic_inference; no grammatical role is promoted to explicit merely by finding the word.',
('U04','outside_unit','Bdir'):'Retain the body as contextual antecedent for this. The local source already makes this the patient of expose; deferring exposure preserves that object role, while resolving the actual feature referent requires context. Explicit role and contextual referent are distinguished.',
('U06','outside_unit','I'):'Retain the enclosing negative deserves judgment as the inference basis for omit. The child quotes the independently actionable color object; parent U05 carries common predicate scope and the AND relation retains the second action without double counting the parent.',
('U06','outside_unit','Cex'):'The external confirmation-window phrase correctly provides shared location. The component was corrected to remove for this transaction and to state replaceable-case scope separately; the nonlocal location anchor remains justified.',
('U06','outside_unit','Cac'):'Retain this new inferred contextual limitation. The same comment calls the current label replaceable and contrasts the non-replacable case as the proposed recipient of red text. Those exact occurrences prevent interpreting the color omission as applying to every confirmation case.',
('U07','outside_unit','I'):'Retain the same enclosing negative deserves judgment for the independent punctuation edit. The shared source does not become a second statement and omission remains explicitly inferred.',
('U07','outside_unit','Cex'):'The enclosing confirmation-window phrase supplies location. The unsupported for this transaction wording was removed, while the current replaceable-case target is now stated separately with contextual evidence.',
('U07','outside_unit','Cac'):'Retain the same-comment replaceable/non-replacable contrast as inferred scope for the punctuation request coupled with the color assessment. This is a bounded reading of the current presentation, not an explicit universal punctuation rule.',
('U08','outside_unit','Cex'):'Retain the preceding confirmation window as the antecedent of there. Both occur in one comment; the local there is present, and the normalized location is correctly context_inferred rather than explicit.',
('U14','outside_unit','Bdir'):'Retain review of this PR as the antecedent for this in can be reviewed already. The local passive patient is explicit even though the identity resolution is contextual. It does not refer to completed GUI replacement work or assign a reviewer actor.',
('U19','outside_unit','Cac'):'Retain shared activation scope from the enclosing workflow-for-additional-outputs subject. Its conditional role is explicitly inferred, and the note distinguishes this scope from the child transaction\'s later use if the original confirms.',
('U24','outside_unit','Bdir'):'Retain the immediately preceding replacable wording as contextual identification of the spelling target. The target role remains inferred from the literal accepted-spelling assertion; neither a full corrected word nor a verified Greg-to-handle mapping is supplied.',
('U25','outside_unit','Bdir'):'Retain the body\'s This PR reference together with the local needs-rebase occurrence and source object identity. PR 7819 is the inferred omitted patient; an actor or maintainer role is not invented.',
('U03','pragmatic_explicit_argument','A'):'Retain explicit A. I is the subject controlling hold back in the supplied negative-desire construction. The pragmatic normalization changes the action interpretation, not the identity or grammatical agent role; the weak desire-versus-plan alternative remains.',
('U03','pragmatic_explicit_argument','Bdir'):'Retain explicit Bdir. Review of this PR is already the direct patient of hold back. Interpreting a negative intention preserves that role rather than turning an original subject into an object.',
('U04','pragmatic_explicit_argument','Bdir'):'Retain explicit object role. This is already the patient of expose; inferred deferral changes the stance toward that action, not its patient. Contextual reference evidence resolves which feature this denotes, without claiming its referent was lexically named in the comment.'
}
def key(f):
    e=f.get('evidence')
    return (f['unit_id'],f['kind'],f['symbol'],json.dumps(e,sort_keys=True,ensure_ascii=False) if e else '')
allflags={}
for name,check in [('checks.first.json',first),('checks.json',last)]:
    for i,f in enumerate(check['review_flags']):
        k=key(f)
        if k not in allflags:allflags[k]={'flag':f,'occurrences':[]}
        allflags[k]['occurrences'].append({'checker_file':name,'flag_index':i})
res=[]
for n,row in enumerate(allflags.values(),1):
    f=row['flag'];base=(f['unit_id'],f['kind'],f['symbol']);uid=f['unit_id']
    assert base in reason,base
    evidence=[ue(uid)]
    if f.get('evidence'):evidence.append(f['evidence'])
    else:
        c=next(c for c in U[uid]['components'] if c['symbol']==f['symbol'])
        evidence.extend(c['evidence'])
    if uid in ['U06','U07']:evidence.extend([ue('U05'),ue('U08'),ue('U09')])
    if uid in ['U02','U04']:evidence.append(ue('U01'))
    status='corrected' if base in [('U06','outside_unit','Cex'),('U07','outside_unit','Cex')] else 'retained'
    res.append({'resolution_id':f'F{n:02d}','flag_kind':f['kind'],'unit_id':uid,'symbol':f['symbol'],'checker_occurrences':row['occurrences'],'status':status,'finding':reason[base],'evidence':evidence})
notes['checker_flag_resolutions']=res
notes['checker_review_summary']={'first_checker_flags':len(first['review_flags']),'final_checker_flags':len(last['review_flags']),'distinct_flag_occurrences_resolved':len(res),'first_errors':len(first['errors']),'final_errors':len(last['errors']),'all_first_and_final_flags_addressed':True,'retained_flags_are_review_prompts_not_errors':True,'no_mechanical_pass_claim_of_semantic_certainty':True}
notes['input_integrity']=integrity
(ROOT/'review_notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')

now=datetime.now(timezone.utc).isoformat()
files_accessed=[
 {'path':'INSTRUCTIONS.txt','access':['read','integrity_hash'],'purpose':'Run boundary and required workflow'},
 {'path':'protocol/codebook.txt','access':['read_complete','integrity_hash'],'purpose':'Assigned version 0.3 interpretation conventions'},
 {'path':'protocol/annotation_schema.json','access':['read_complete','checker_read','integrity_hash'],'purpose':'Full annotation structure'},
 {'path':'packet.json','access':['read_complete','programmatic_read','integrity_hash'],'purpose':'Sole research source packet and exact Unicode anchors'},
 {'path':'tools/check_annotation.py','access':['read_complete','execute','integrity_hash'],'purpose':'Provided mechanical validation only'},
 {'path':'input_manifest.json','access':['read_complete'],'purpose':'Input integrity and exposed inherited-configuration record'},
 {'path':'build_annotation.py','access':['write','execute'],'purpose':'Generate first complete annotation and preserve freeze before checks'},
 {'path':'annotation.json','access':['write','read','checker_read','revise'],'purpose':'Working full-schema annotation; final content equals annotation.final.json'},
 {'path':'annotation.first_complete.json','access':['write_once','read','integrity_hash'],'purpose':'First complete freeze, never revised'},
 {'path':'checks.first.json','access':['write','read'],'purpose':'Preserved first checker result'},
 {'path':'self_review_finalize.py','access':['write','execute'],'purpose':'Apply single source-self-review corrections and record exact before/after changes'},
 {'path':'annotation.final.json','access':['write','read','checker_read','integrity_hash'],'purpose':'Final full-schema annotation'},
 {'path':'checks.json','access':['write','read'],'purpose':'Final checker result'},
 {'path':'repair_log.json','access':['write','read'],'purpose':'Every annotation change after first-complete freeze'},
 {'path':'review_notes.json','access':['write','read','complete_flag_resolutions'],'purpose':'Full source review plus disposition of every checker flag'},
 {'path':'finalize_records.py','access':['write','execute','integrity_hash'],'purpose':'Resolve flagged anchors, verify input integrity, and write provenance logs'},
 {'path':'access_record.json','access':['write','integrity_hash'],'purpose':'This access and exposed-runtime record'},
 {'path':'execution_log.json','access':['write','integrity_hash'],'purpose':'Ordered required workflow and validation outcomes'},
 {'path':'output_manifest.json','access':['write'],'purpose':'Output hashes and unit counts; own hash omitted to avoid recursive self-hashing'}
]
access={'run_id':'F03_v03_r2','recorded_at_utc':now,'working_directory':str(ROOT),'scope':'All research, reads, and outputs remained within this assigned run directory; ordinary Python runtime imports are listed separately. No parent-directory, other-run, Library, web, or external research inputs were read.','files_accessed':files_accessed,'directory_inventory_access':{'directory':str(ROOT),'recursive':True,'purpose':'Enumerate assigned inputs only; no traversal outside this directory'},'ordinary_runtime_access':{'python_executable':sys.executable,'python_version':sys.version,'runtime_modules':['json','hashlib','copy','pathlib','sys','re','datetime','collections','jsonschema (through provided checker)'],'source_note':'Python imports used ordinary installed runtime/library code; no external research content was retrieved.'},'exposed_configuration':{'configuration':'inherited primary; no override','configuration_source':'Dispatch and input_manifest.json','model_identity':None,'reasoning_effort':None,'provider_snapshot':None,'seed':None,'sampling_parameters':None,'tokens':None,'cost':None,'note':'No independently exposed model selector, provider snapshot, sampling, usage, or cost telemetry was available. No model identity or reasoning setting was inferred from the historical protocol text.'},'outside_sources_used':False,'network_calls':0,'subagents_spawned':0,'frozen_input_integrity':integrity,'limitations':'Conversation/tool-output token and cost telemetry, exact provider configuration, and a provider-side execution snapshot are not exposed.'}
(ROOT/'access_record.json').write_text(json.dumps(access,ensure_ascii=False,indent=2)+'\n')
counts={'screened_entries':len(a['entry_screening']),'focal_entries':len(read('packet.json')['selection_design']['focal_source_ids']),'screening_dispositions':dict(Counter(x['disposition'] for x in a['entry_screening'])),'unit_roles':dict(Counter(u['record_role'] for u in a['units'])),'total_units':len(a['units']),'relations':len(a['relations']),'recognition_events':sum(len(u['institution']['recognition']) for u in a['units']),'disposition_events':sum(len(u['disposition_events']) for u in a['units']),'outcome_claims':len(a['episode_summary']['observed_outcomes']),'mechanisms':len(a['episode_summary']['mechanisms']),'self_review_passes':1,'repair_entries':len(repairs['changes']),'final_exact_anchor_references':last['exact_anchor_references'],'final_checker_flags':len(last['review_flags'])}
log={'run_id':'F03_v03_r2','finalized_at_utc':now,'phases':[
 {'order':1,'action':'Read complete instructions, codebook, schema, and packet; enumerate assigned directory','external_sources':False},
 {'order':2,'action':'Screen all entries and generate complete annotation','artifacts':['annotation.json']},
 {'order':3,'action':'Preserve first-complete annotation before validation or self-review','artifacts':['annotation.first_complete.json'],'sha256':repairs['first_complete_sha256']},
 {'order':4,'action':'Run provided checker','command':'python3 tools/check_annotation.py packet.json annotation.json > checks.first.json','exit_code':0,'status':first['status'],'errors':len(first['errors']),'review_flags':len(first['review_flags'])},
 {'order':5,'action':'Conduct one complete source-based self-review and record corrections','artifacts':['repair_log.json','review_notes.json','annotation.final.json'],'source_self_review_passes':1,'new_sources':False,'mechanical_repairs':0,'repair_entries':len(repairs['changes'])},
 {'order':6,'action':'Run final provided checker','command':'python3 tools/check_annotation.py packet.json annotation.final.json > checks.json','exit_code':0,'status':last['status'],'errors':len(last['errors']),'review_flags':len(last['review_flags'])},
 {'order':7,'action':'Resolve every first/final checker flag, verify unchanged inputs and freeze, and complete access/output records','all_flags_reviewed':True,'all_frozen_inputs_unchanged':True}
],'counts':counts,'first_complete_sha256':repairs['first_complete_sha256'],'final_annotation_sha256':repairs['final_sha256'],'unresolved_limits':a['episode_summary']['missing_evidence']+a['episode_summary']['unresolved_questions']}
(ROOT/'execution_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
outputs=['annotation.json','annotation.first_complete.json','annotation.final.json','checks.first.json','checks.json','repair_log.json','review_notes.json','access_record.json','execution_log.json','build_annotation.py','self_review_finalize.py','finalize_records.py']
output_manifest={'run_id':'F03_v03_r2','packet_sha256':a['packet_sha256'],'counts':counts,'outputs':{name:{'sha256':hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),'bytes':(ROOT/name).stat().st_size} for name in outputs},'checks':'Both provided checker runs pass; all 14 first-check and 18 final-check flags have cited dispositions in review_notes.json. Semantic uncertainty remains explicit.','inputs_unchanged':True}
(ROOT/'output_manifest.json').write_text(json.dumps(output_manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'counts':counts,'checker_status':last['status'],'resolved_distinct_flags':len(res),'inputs_unchanged':True,'output_directory':str(ROOT)},ensure_ascii=False))
