import json,sys
case=sys.argv[1];ids=sys.argv[2].split(',') if len(sys.argv)>2 else None
mode=sys.argv[3] if len(sys.argv)>3 else 'units'
d=json.load(open(case+'_dossier.json'));pool=d['evidence_pool']
def ev(x):
 if isinstance(x,dict) and set(x)=={'evidence_ref'}:
  z=pool[x['evidence_ref']];s=z['span'];return f"{x['evidence_ref']}={z['source_id']}[{s['start']}:{s['end']}]"
 if isinstance(x,dict):return {k:ev(v) for k,v in x.items()}
 if isinstance(x,list):return [ev(v) for v in x]
 return x
def out(x):print(json.dumps(x,ensure_ascii=False,separators=(',',':')))
for a in d['annotations']:
 if ids and a['annotation_id'] not in ids:continue
 print('ANNOTATION',a['annotation_id'],a['assigned_guide'])
 if mode=='units':
  for u in a['units'][int(sys.argv[4]) if len(sys.argv)>4 else 0:int(sys.argv[5]) if len(sys.argv)>5 else 999]:
   r={k:u.get(k) for k in ['unit_id','record_role','grammar','parse_mode','speech_act','scope','deontic_force','statement_target_level','observed_action_level','confidence','uncertainty_reason','alternative_interpretation','level_rationale']}
   r['span']=ev(u['span']);r['quote']=pool[u['span']['evidence_ref']]['span']['quote'];r['proposition']=ev(u.get('proposition'));r['presentation']=u['presentation'];r['components']=[{k:ev(v) for k,v in c.items() if k!='inference_note'} for c in u['components']]
   out(r)
 elif mode=='support':
  for u in a['units'][int(sys.argv[4]) if len(sys.argv)>4 else 0:int(sys.argv[5]) if len(sys.argv)>5 else 999]:
   out({'unit_id':u['unit_id'],'institution':ev(u['institution']),'disposition_events':ev(u['disposition_events']),'component_notes':[(c['symbol'],c.get('inference_note')) for c in u['components']],'level_evidence':ev(u.get('level_evidence')),'remaining':{k:v for k,v in u.items() if k in ['parent_unit_id','complexity_flags','level_alternatives','target_level_alternatives','observed_level_alternatives','template_note']}})
 elif mode=='summary':out(ev(a['episode_summary']))
 elif mode=='relations':
  for i,r in enumerate(a['relations']):out({'path':f'relations[{i}]',**ev(r)})
 elif mode=='screen':out(a['entry_screening'])
