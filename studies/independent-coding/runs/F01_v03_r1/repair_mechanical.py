import json,datetime
from pathlib import Path
p=Path('annotation.json');a=json.loads(p.read_text()); by={u['unit_id']:u for u in a['units']}; logs=[]
for uid,sym in [('D03','Bdir'),('C02b','Bdir'),('C04a','A'),('C08a','I'),('R02d','Bdir')]:
 u=by[uid]; c=next(x for x in u['components'] if x['symbol']==sym);old=json.loads(json.dumps(c)); q=c['evidence'][0]['span']['quote']; start=u['span']['start']+u['span']['quote'].index(q)
 c['evidence'][0]['span']={'start':start,'end':start+len(q),'quote':q}
 if uid=='R02d': c['token_exception']='That is the pronominal subject before the contracted copula in that\'s; the anchor is the grammatical pronoun, not an arbitrary substring.'
 logs.append({'change_id':'M'+str(len(logs)+1).zfill(2),'stage':'mechanical_repair','unit_id':uid,'field':'components.'+sym+'.evidence','classification':'anchor_alignment_error','meaning_changes':False,'before':old,'after':c,'reason':'Relocated an unintended earlier matching substring or quoted occurrence to the correct predicate-local occurrence. Proposition and role interpretation are unchanged.','evidence':c['evidence']})
p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n');Path('repair_log.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2)+'\n')
Path('annotation.after_mechanical.json').write_bytes(p.read_bytes())
print('Corrected',len(logs),'component anchors.')
