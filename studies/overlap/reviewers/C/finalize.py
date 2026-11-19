import json,hashlib,copy
from pathlib import Path
R=Path('/workspace/scratch/2020b62d57db/overlap_validation/Core_Knots_Round12_Overlap_Validation_Evidence_v01/reviewers/C')
a=json.loads((R/'annotation.json').read_text());p=json.loads((R/'packet.json').read_text());t={e['source_id']:e['text'] for e in p['entries']};u=next(u for u in a['units'] if u['unit_id']=='C178_lower');c=next(c for c in u['components'] if c['symbol']=='D');before=copy.deepcopy(c['evidence']);q='recommend not';start=t[u['source_id']].index(q,u['span']['start'],u['span']['end']);c['evidence']=[{'source_id':u['source_id'],'span':{'start':start,'end':start+len(q),'quote':q}}]
(R/'checks.after_self_review.json').write_bytes((R/'checks.json').read_bytes())
(R/'annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
log=json.loads((R/'repair_log.json').read_text());changes=log['changes']
changes.append({'change_id':f'C-repair-{len(changes)+1:02d}','unit_id':'C178_lower','field':'components.D.evidence','category':'mechanical','changes_meaning':False,'rationale':'The checker identified the earlier occurrence of recommend not elsewhere in the same source. Use the identical lexical phrase within this unit. No semantic judgment changed.','before':before,'after':copy.deepcopy(c['evidence'])})
newrel=next(r for r in a['relations'] if r['from_unit_id']=='C453_schedule')
changes.append({'change_id':f'C-repair-{len(changes)+1:02d}','unit_id':'C453_schedule','field':'relations','category':'segmentation_bookkeeping','changes_meaning':False,'rationale':'Explicitly retain the relation created during the one source-review pass when separating the schedule preference.','before':None,'after':newrel})
changes.append({'change_id':f'C-repair-{len(changes)+1:02d}','unit_id':'C453_schedule','field':'entry_screening.33453-body.unit_ids','category':'segmentation_bookkeeping','changes_meaning':False,'rationale':'Add the separated embedded unit to its source screening references.','before':None,'after':'C453_schedule'})
log['counts']={'logged_changes':len(changes),'changes_marked_meaning_changing':sum(c['changes_meaning'] for c in changes)}
log['execution_notes']=['The source-review helper initially failed in memory on a missing explanation argument before writing any annotation changes; fixing the helper did not constitute an additional source-review pass.','A post-review checker found one ambiguous same-source lexical occurrence. That mechanical anchor correction is logged and its checker output preserved in checks.after_self_review.json.']
(R/'repair_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
notes=json.loads((R/'review_notes.json').read_text());notes['self_review']['mechanical_followup']='One checker-directed, within-unit occurrence correction followed the source review; no second semantic review was conducted.'
for x in notes['per_focal_source']:
 x['self_review_findings']=[{'change_id':z['change_id'],'unit_id':z['unit_id'],'rationale':z['rationale'],'changes_meaning':z['changes_meaning']} for z in changes if z['unit_id'] in x['unit_ids']]
access=notes['access_record']
access['own_generated_files_accessed']=list(dict.fromkeys(access['own_generated_files_accessed']+[str(R/f) for f in ['annotation.json','annotation.first_complete.json','checks.first.json','checks.after_self_review.json','checks.json','review_notes.json','repair_log.json','finalize.py']]))
access['research_file_hashes_sha256']={f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in access['research_files_accessed']}
access['generated_artifact_paths']=[str(R/f) for f in ['annotation.first_complete.json','annotation.json','checks.first.json','checks.after_self_review.json','checks.json','repair_log.json','review_notes.json','access_record.json','freeze_manifest.json','build_annotation.py','self_review.py','finalize.py']]
notes['access_record']=access
(R/'review_notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
(R/'access_record.json').write_text(json.dumps(access,ensure_ascii=False,indent=2)+'\n')
print(log['counts'])
