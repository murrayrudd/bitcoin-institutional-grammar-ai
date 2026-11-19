"""Lossless evidence interning for manageable source-review dossiers.
Full masked annotations remain available. Re-expansion must equal their originals.
"""
from pathlib import Path
import json,copy,hashlib
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n')
def build(target):
 d=R/'reviews'/target;annotations=read(d/'annotations.json');summary=[]
 for eid in ['F01','F02','F03']:
  selected=[a for a in annotations if a['episode_id']==eid];pool={};reverse={}
  def intern(e):
   key=json.dumps(e,ensure_ascii=False,sort_keys=True,separators=(',',':'))
   if key not in reverse:
    tag=f'Q{len(pool)+1:04d}';reverse[key]=tag;pool[tag]=copy.deepcopy(e)
   return {'evidence_ref':reverse[key]}
  def shrink(x):
   if isinstance(x,list):return [shrink(v) for v in x]
   if isinstance(x,dict):
    if set(x)=={'source_id','span'}:return intern(x)
    if all(k in x for k in ['source_id','span','unit_id']):
     return {k:(intern({'source_id':x['source_id'],'span':v}) if k=='span' else shrink(v)) for k,v in x.items()}
    return {k:shrink(v) for k,v in x.items()}
   return x
  compressed=shrink(selected)
  def expand(x):
   if isinstance(x,list):return [expand(v) for v in x]
   if isinstance(x,dict):
    if set(x)=={'evidence_ref'}:return copy.deepcopy(pool[x['evidence_ref']])
    if all(k in x for k in ['source_id','span','unit_id']):return {k:(expand(v)['span'] if k=='span' else expand(v)) for k,v in x.items()}
    return {k:expand(v) for k,v in x.items()}
   return x
  assert expand(compressed)==selected
  result={'episode_id':eid,'note':'Lossless view. Every evidence_ref resolves to exact source_id/span in evidence_pool. Unit span refs resolve to the span member. Full annotations.json also retained.','evidence_pool':pool,'annotations':compressed}
  p=d/f'{eid}_dossier.json';write(p,result);summary.append({'episode':eid,'annotations':len(selected),'units':sum(len(a['units']) for a in selected),'evidence_anchors':len(pool),'bytes':p.stat().st_size,'lossless_roundtrip':'pass'})
 write(d/'dossier_index.json',summary)
 return summary
if __name__=='__main__':
 for target in ['alignment','source_review_a','source_review_b']:print(target,build(target))
