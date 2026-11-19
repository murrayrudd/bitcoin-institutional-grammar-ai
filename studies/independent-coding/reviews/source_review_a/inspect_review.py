import json,sys,hashlib,pathlib
root=pathlib.Path('.')
def jd(v):return json.dumps(v,ensure_ascii=False,separators=(',',':'))
def load(ep): return json.load(open(ep+'_dossier.json'))
if sys.argv[1]=='prepare':
 for ep in ['F01','F02','F03']:
  d=load(ep);seen={}; out=[]
  def dedup(v,path):
   if isinstance(v,dict): return {k:dedup(x,path+'.'+k) for k,x in v.items()}
   if isinstance(v,list):
    s=jd(v)
    if len(s)>100 and s in seen:return {'same_value_as':seen[s]}
    seen.setdefault(s,path)
    return [dedup(x,path+'['+str(i)+']') for i,x in enumerate(v)]
   if isinstance(v,str) and len(v)>90:
    if v in seen:return {'same_value_as':seen[v]}
    seen[v]=path
   return v
  for a in d['annotations']:
   aid=a['annotation_id'];out.append('\nANNOTATION '+aid+' '+a['assigned_guide'])
   out.append('SCREEN '+jd(dedup(a['entry_screening'],aid+'.entry_screening')))
   for u in a['units']:out.append('UNIT '+jd(dedup(u,aid+'.'+u['unit_id'])))
   for i,r in enumerate(a['relations']):out.append('REL '+str(i)+' '+jd(dedup(r,aid+'.relations['+str(i)+']')))
   for k,v in a['episode_summary'].items():out.append('SUMMARY '+k+' '+jd(dedup(v,aid+'.episode_summary.'+k)))
  root.joinpath(ep+'_inspection.txt').write_text('\n'.join(out))
  print(ep,'inspection chars',sum(map(len,out)),'lines',len(out))
  p=json.load(open(ep+'_packet.json'));src={e['source_id']:e['text'] for e in p['entries']};bad=[]
  for q,e in d['evidence_pool'].items():
   s=e['span']; actual=src[e['source_id']][s['start']:s['end']]
   if actual!=s['quote']:bad.append(q)
  print('anchor mismatches',bad)
if sys.argv[1]=='show':
 ep,aid=sys.argv[2:4];d=load(ep);a=next(a for a in d['annotations'] if a['annotation_id']==aid)
 if sys.argv[4]=='units':
  lo,hi=map(int,sys.argv[5:7]); print('\n'.join(jd(u) for u in a['units'][lo:hi]))
 elif sys.argv[4]=='parts':
  for k in sys.argv[5:]:print(k,jd(a[k]))
 elif sys.argv[4]=='fields':
  for u in a['units']:print(jd({k:u[k] for k in ['unit_id']+sys.argv[5:] if k in u}))
 elif sys.argv[4]=='anchors':
  for q in sys.argv[5:]:print(q,jd(d['evidence_pool'][q]))
