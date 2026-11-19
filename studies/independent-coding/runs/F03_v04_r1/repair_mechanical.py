import json
from copy import deepcopy
from pathlib import Path
p=Path('.')
a=json.loads((p/'annotation.json').read_text())
packet=json.loads((p/'packet.json').read_text())
texts={e['source_id']:e['text'] for e in packet['entries']}
log=[]
for u in a['units']:
    for i,c in enumerate(u['components']):
        if c['occurrence_role']!='local':continue
        for j,ev in enumerate(c['evidence']):
            q=ev['span']['quote']; source=texts[ev['source_id']]
            if ev['source_id']==u['source_id'] and not(u['span']['start']<=ev['span']['start'] and ev['span']['end']<=u['span']['end']):
                old=deepcopy(ev)
                start=source.index(q,u['span']['start'],u['span']['end'])
                ev['span']={'start':start,'end':start+len(q),'quote':q}
                log.append({'change_id':f'M{len(log)+1:02}','phase':'mechanical_repair','unit_id':u['unit_id'],'path':f'components/{i}/evidence/{j}','before':old,'after':deepcopy(ev),'meaning_changed':False,'evidence_basis_changed':True,'diagnosis':'execution_failure','effect':'evidence_basis_error','reason':'First-occurrence string matching selected a matching token outside the focal predicate. Corrected to the exact local occurrence within the unchanged unit and governing clause.'})
u=next(u for u in a['units'] if u['unit_id']=='U03')
u['institution']['standing_profile']['recognition']='none'
log.append({'change_id':f'M{len(log)+1:02}','phase':'mechanical_repair','unit_id':'U03','path':'institution/standing_profile/recognition','before':'same_actor_only','after':'none','meaning_changed':True,'evidence_basis_changed':True,'diagnosis':'execution_failure','effect':'evidence_basis_error','reason':'The recorded event is a same-author response/restatement, not expectation_recognition. No expectation-recognition profile follows from it. The event and personal-commitment interpretation remain preserved.'})
(p/'annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
(p/'repair_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'changes':len(log),'anchor_changes':len(log)-1}))
