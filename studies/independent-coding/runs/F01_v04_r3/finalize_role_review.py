import json,copy
from pathlib import Path
p=Path(__file__).resolve().parent
a=json.loads((p/'annotation.final.json').read_text());d={u['unit_id']:u for u in a['units']};log=json.loads((p/'repair_log.json').read_text())
(p/'checks.source_review_01.json').write_bytes((p/'checks.json').read_bytes())
def record(uid,fields,before,after,reason,es,effect='evidence-basis error'):
 log.append({'change_id':'S'+str(1+sum(x['stage']=='source_self_review' for x in log)).zfill(2),'stage':'source_self_review','unit_id':uid,'fields':fields,'before':before,'after':after,'meaning_changes':False,'effect':effect,'diagnosis':'execution_failure','reason':reason,'evidence':es})
u=d['C28'];before={k:copy.deepcopy(u[k]) for k in ['speech_act','parse_mode','components']};u['speech_act']='asserted';u['parse_mode']='literal';c=next(c for c in u['components'] if c['symbol']=='I');c.update(basis='explicit',occurrence_role='local',inference_note='The action not rush merging is directly supplied. Only the recommendation force is inferred from the stated reason; that does not make the action role inferred.')
record('C28',['speech_act','parse_mode','components.I.basis','components.I.occurrence_role','components.I.inference_note'],before,{k:copy.deepcopy(u[k]) for k in before},'The source explicitly states the negative action within a declarative reason claim. Do not confuse inferred force with inferred action.',[{'source_id':u['source_id'],'span':u['span']}])
for uid in ['C06','C09']:
 u=d[uid];before=u['speech_act'];u['speech_act']='asserted';record(uid,['speech_act'],before,'asserted','Preserve the original declarative claim of justification or preference while retaining its possible directive interpretation.',[{'source_id':u['source_id'],'span':u['span']}],'convention deviation')
for name in ['annotation.json','annotation.final.json']:(p/name).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
(p/'repair_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
