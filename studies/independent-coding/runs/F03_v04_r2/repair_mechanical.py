import json,copy
from pathlib import Path
R=Path(__file__).resolve().parent
A=json.loads((R/'annotation.json').read_text()); P=json.loads((R/'packet.json').read_text()); texts={x['source_id']:x['text'] for x in P['entries']}
log=[]
for ui,u in enumerate(A['units']):
    for ci,c in enumerate(u['components']):
        if c['occurrence_role']!='local':continue
        for ei,e in enumerate(c['evidence']):
            q=e['span']['quote'];start=u['span']['start'];end=u['span']['end']
            if e['source_id']==u['source_id'] and start<=e['span']['start']<e['span']['end']<=end:continue
            old=copy.deepcopy(e); pos=texts[u['source_id']].index(q,start,end)
            e.update(source_id=u['source_id'],span={'start':pos,'end':pos+len(q),'quote':q})
            log.append({'change_id':f'M{len(log)+1:02d}','phase':'mechanical_repair','unit_id':u['unit_id'],'path':f'/units/{ui}/components/{ci}/evidence/{ei}','before':old,'after':copy.deepcopy(e),'meaning_changed':False,'effect':'evidence_basis_error','diagnosis':'execution_failure','rationale':'Global substring search had selected an earlier matching token. The occurrence is relocated within the focal unit, without changing actor, action, or object interpretation.','evidence':[copy.deepcopy(e)]})
u=next(x for x in A['units'] if x['unit_id']=='F03-U03')
u['institution']['standing_profile']['recognition']='none'
log.append({'change_id':f'M{len(log)+1:02d}','phase':'mechanical_repair','unit_id':'F03-U03','path':'institution/standing_profile/recognition','before':'same_actor_only','after':'none','meaning_changed':True,'effect':'evidence_basis_error','diagnosis':'execution_failure','rationale':'The retained response event is a same-actor restatement of a personal approach, not expectation_recognition. The profile should therefore remain none; the event still documents maintained commitment.','evidence':u['institution']['recognition'][0]['evidence']})
(R/'annotation.json').write_text(json.dumps(A,ensure_ascii=False,indent=2)+'\n')
(R/'repair_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'changes':len(log),'units_fixed':sorted({x['unit_id'] for x in log})}))
