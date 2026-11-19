import json,sys,hashlib
from pathlib import Path
case=sys.argv[1]; mode=sys.argv[2]; d=json.load(open(case+'_dossier.json')); p=json.load(open(case+'_packet.json'))
selected=set(sys.argv[3].split(',')) if len(sys.argv)>3 and sys.argv[3]!='all' else None
lo=int(sys.argv[4]) if len(sys.argv)>4 else 0; hi=int(sys.argv[5]) if len(sys.argv)>5 else 999
pool=d['evidence_pool']; sources={e['source_id']:e['text'] for e in p['entries']}
def short(v):
 if isinstance(v,dict):
  if set(v)=={'evidence_ref'}:
   e=pool[v['evidence_ref']];s=e['span'];return f"{v['evidence_ref']}={e['source_id']}:{s['start']}-{s['end']}"
  return {k:short(x) for k,x in v.items()}
 if isinstance(v,list):return [short(x) for x in v]
 return v
def out(v): print(json.dumps(short(v),ensure_ascii=False,separators=(',',':')))
if mode=='sources':
 for e in p['entries'][lo:hi]:out(e)
elif mode=='evidence':
 for k,v in list(pool.items())[lo:hi]:out({k:v})
else:
 for a in d['annotations']:
  if selected and a['annotation_id'] not in selected:continue
  print('\nANNOTATION',a['annotation_id'],a['assigned_guide'])
  if mode=='core':
   for u in a['units'][lo:hi]:
    x={k:v for k,v in u.items() if k not in ['institution','disposition_events']}
    out(x)
  elif mode=='institution':
   for u in a['units'][lo:hi]:out({'id':u['unit_id'],'quote':pool[u['span']['evidence_ref']]['span']['quote'],'institution':u['institution'],'disposition_events':u['disposition_events']})
  elif mode=='rest':
   out({'entry_screening':a['entry_screening']})
   for i,r in enumerate(a['relations']):out({'relation_path':f'relations[{i}]',**r})
   for k,v in a['episode_summary'].items():
    for i,x in enumerate(v):out({'summary_path':f'episode_summary.{k}[{i}]','value':x})
  elif mode=='roster':
   for u in a['units']:out({'id':u['unit_id'],'span':pool[u['span']['evidence_ref']],'role':u['record_role'],'g':u['grammar'],'f':u['deontic_force'],'t':u['institution']['type'],'standing':u['institution'].get('standing',u['institution'].get('standing_profile')),'level':[u['statement_target_level'],u['observed_action_level']]})
