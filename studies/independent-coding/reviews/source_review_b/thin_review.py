import json,sys
case,ids,mode=sys.argv[1:4];d=json.load(open(case+'_dossier.json'));pool=d['evidence_pool'];lo=int(sys.argv[4]) if len(sys.argv)>4 else 0;hi=int(sys.argv[5]) if len(sys.argv)>5 else 999

def ev(e):
 z=pool[e['evidence_ref']];s=z['span'];return f"{e['evidence_ref']}={z['source_id']}:{s['start']}-{s['end']}"
def slim(x):
 if isinstance(x,dict):
  if set(x)=={'evidence_ref'}:return ev(x)
  return {k:slim(v) for k,v in x.items() if k not in ['rationale','inference_note','identity_evidence']}
 if isinstance(x,list):return [slim(v) for v in x]
 return x
for a in d['annotations']:
 if ids!='all' and a['annotation_id'] not in ids.split(','):continue
 print('ANNOTATION',a['annotation_id'],a['assigned_guide'])
 if mode=='units':
  for u in a['units'][lo:hi]:
   z=pool[u['span']['evidence_ref']];i=u['institution'];out={'id':u['unit_id'],'source':ev(u['span']),'text':z['span']['quote'],'role':u['record_role'],'grammar':u['grammar'],'parse':u['parse_mode'],'speech':u['speech_act'],'scope':u['scope'],'force':u['deontic_force'],'type':i['type'],'standing':i.get('standing',i.get('standing_profile')),'dispute':i['dispute_present'],'levels':[u['statement_target_level'],u['observed_action_level']],'presentation':slim(u['presentation']),'components':slim(u['components'])}
   if u.get('proposition'):out['proposition']=slim(u['proposition'])
   out['alternatives']=u['alternative_interpretation'];print(json.dumps(out,ensure_ascii=False,separators=(',',':')))
 elif mode=='support':
  for u in a['units'][lo:hi]:
   print(json.dumps({'id':u['unit_id'],'institution':slim(u['institution']),'disposition':slim(u['disposition_events'])},ensure_ascii=False,separators=(',',':')))
 elif mode=='notes':
  for u in a['units'][lo:hi]:
   out={'id':u['unit_id'],'level_rationale':u['level_rationale'],'uncertainty':u['uncertainty_reason'],'component_notes':[(c['symbol'],c['inference_note']) for c in u['components']],'institution_rationale':u['institution']['rationale']}
   for k in ['recognition','documentary_support','application_evidence','challenges']:
    out[k]=[v['rationale'] for v in u['institution'].get(k,[])]
   out['disposition_notes']=[v['rationale'] for v in u['disposition_events']];print(json.dumps(out,ensure_ascii=False,separators=(',',':')))
 elif mode=='relations':
  for i,r in enumerate(a['relations'][lo:hi],lo):print(i,json.dumps(r,ensure_ascii=False,separators=(',',':')))
 elif mode=='summary':
  for k,v in a['episode_summary'].items():
   for i,x in enumerate(v):print(k,i,json.dumps(x,ensure_ascii=False,separators=(',',':')))
 elif mode=='screen':
  for e in a['entry_screening']:print(json.dumps(e,ensure_ascii=False,separators=(',',':')))
