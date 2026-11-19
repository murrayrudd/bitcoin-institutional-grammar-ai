from pathlib import Path
import json
p=json.loads(Path('packet.json').read_text()); ts={e['source_id']:e['text'] for e in p['entries']}
a=json.loads(Path('annotation.json').read_text())
log=[]
for uid,symbol in [('F03-U07','Bdir'),('F03-U11','Bdir')]:
 u=next(x for x in a['units'] if x['unit_id']==uid)
 c=next(x for x in u['components'] if x['symbol']==symbol)
 old=json.loads(json.dumps(c['evidence']))
 q=c['evidence'][0]['span']['quote']; i=ts[u['source_id']].index(q,u['span']['start'])
 c['evidence']=[{'source_id':u['source_id'],'span':{'start':i,'end':i+len(q),'quote':q}}]
 log.append({'change_id':f'M{len(log)+1:02d}','phase':'mechanical_checker','unit_id':uid,'field':'components.'+symbol+'.evidence','trigger':'checks.first.json outside_unit flag','before':old,'after':c['evidence'],'meaning_changes':False,'classification':'evidence_occurrence_error','rationale':'Retargets the same surface words to their occurrence in the focal proposition. The selected actor/action/object interpretation is unchanged, but the former evidence occurrence did not establish this predicate role.'})
Path('annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
Path('repair_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
