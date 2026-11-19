import json,sys
x=json.load(open(sys.argv[1]+'_dossier.json'));a=next(a for a in x['annotations'] if a['annotation_id']==sys.argv[2]);lo,hi=map(int,sys.argv[3:5]);seen={}
def jd(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def compact(v,path):
 s=jd(v)
 if len(s)>90:
  if s in seen:return {'exactly_as':seen[s]}
  seen[s]=path
 if isinstance(v,dict):return {k:compact(w,path+'.'+k) for k,w in v.items()}
 if isinstance(v,list):return [compact(w,path+'['+str(i)+']') for i,w in enumerate(v)]
 return v
for i,u in enumerate(a['units']):
 out=compact(u,a['annotation_id']+'.'+u['unit_id'])
 if lo<=i<hi:print(i,jd(out))
