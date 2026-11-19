import json
from pathlib import Path
A=json.loads(Path('annotation.json').read_text());P=json.loads(Path('packet.json').read_text());S={e['source_id']:e['text'] for e in P['entries']};U={u['unit_id']:u for u in A['units']};changes=[]
def component(k,sym):return next(c for c in U[k]['components'] if c['symbol']==sym)
c=component('need_rebase','Bdir');old=json.loads(json.dumps(c['evidence']));i=S[U['need_rebase']['source_id']].index('it needs',U['need_rebase']['span']['start']);c['evidence']=[{'source_id':U['need_rebase']['source_id'],'span':{'start':i,'end':i+2,'quote':'it'}}]
changes.append({'change_id':'M01','stage':'mechanical','unit_id':'need_rebase','field':'components.Bdir.evidence','before':old,'after':c['evidence'],'meaning_changes':False,'epistemic_correction':True,'reason':'Replace incidental it inside bit with the actual subject it in the rebase clause. The intended referent and inferred role do not change.'})
for k,sym in [('developer_choice','Cac'),('host_regtest','Cex'),('occasionally_rebase','Bdir')]:
 c=component(k,sym);old=c['occurrence_role'];c['occurrence_role']='context_reference';changes.append({'change_id':f'M{len(changes)+1:02d}','stage':'mechanical','unit_id':k,'field':f'components.{sym}.occurrence_role','before':old,'after':c['occurrence_role'],'meaning_changes':False,'epistemic_correction':True,'reason':'The lexical role is supplied locally, but the evidence also resolves an antecedent outside the unit; context_reference accurately declares that evidence scope.'})
Path('annotation.json').write_text(json.dumps(A,ensure_ascii=False,indent=2)+'\n');Path('repair_log.json').write_text(json.dumps({'run_id':'F01_v03_r2','changes':changes},ensure_ascii=False,indent=2)+'\n')
