import json,sys,collections
case,mode=sys.argv[1:3];d=json.load(open(case+'_dossier.json'));groups={}
for a in d['annotations']:
 for u in a['units']:
  items=[]
  if mode=='events':
   for k in ['recognition','documentary_support','application_evidence','challenges']:
    items += [(f'institution.{k}[{i}]',v) for i,v in enumerate(u['institution'].get(k,[]))]
   items += [(f'disposition_events[{i}]',v) for i,v in enumerate(u['disposition_events'])]
  elif mode=='notes':
   items=[(k,v) for k,v in u.items() if k in ['alternative_interpretation','level_rationale','uncertainty_reason','level_evidence'] and v]
   items += [('institution.rationale',u['institution']['rationale'])]
   items += [(f'components[{i}].inference_note',c['inference_note']) for i,c in enumerate(u['components']) if c['inference_note']]
  elif mode=='proposition':
   if u.get('proposition'):items=[('proposition',u['proposition'])]
  for path,v in items:
   key=json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
   groups.setdefault(key,[]).append(a['annotation_id']+'/'+u['unit_id']+'/'+path)
items=list(groups.items());lo=int(sys.argv[3]) if len(sys.argv)>3 else 0;hi=int(sys.argv[4]) if len(sys.argv)>4 else 0
print('UNIQUE',len(items))
for i,(v,paths) in enumerate(items[lo:hi],lo):print(i,';'.join(paths),v)
