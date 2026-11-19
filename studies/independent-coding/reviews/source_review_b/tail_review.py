import json,sys
from collections import defaultdict
from pathlib import Path
c=sys.argv[1];lo=int(sys.argv[2]);hi=int(sys.argv[3]);d=json.load(open(c+'_dossier.json'));out={}
ks=['parent_unit_id','complexity_flags','confidence','presentation','template_note','level_alternatives','target_level_alternatives','observed_level_alternatives']
for a in d['annotations']:
 for u in a['units']:
  for k in ks:
   if k in u:
    v=json.dumps(u[k],ensure_ascii=False,sort_keys=True,separators=(',',':'))
    out.setdefault((k,v),[]).append(a['annotation_id']+'/'+u['unit_id'])
  for k in ['authority_evidence','type_alternatives']:
   v=json.dumps(u['institution'].get(k),ensure_ascii=False,sort_keys=True,separators=(',',':'))
   out.setdefault(('institution.'+k,v),[]).append(a['annotation_id']+'/'+u['unit_id'])
print('UNIQUE',len(out))
for i,((k,v),p) in enumerate(list(out.items())[lo:hi],lo):
 groups={}
 for x in p:
  a,u=x.split('/',1); groups.setdefault(a,[]).append(u)
 refs=','.join(p) if len(p)<=12 else str({a:len(us) for a,us in groups.items()})+' total='+str(len(p))
 print(i,k,refs,v)
Path(c+'_tail_mapping.json').write_text(json.dumps([{'field':k,'value':json.loads(v),'paths':p} for (k,v),p in out.items()],indent=2)+'\n')
