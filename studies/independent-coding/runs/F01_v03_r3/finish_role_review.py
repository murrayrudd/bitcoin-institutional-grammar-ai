import json,copy
from pathlib import Path
A=json.loads(Path('annotation.json').read_text());L=json.loads(Path('repair_log.json').read_text())
Path('checks.source_review_stage1.json').write_bytes(Path('checks.json').read_bytes())
for i,action,note in [('u10','adding','The source explicitly supplies adding and the complete v24.0-or-available-release target. Treating that embedded action as the recommended action changes pragmatic force but does not transform its action/object roles; should still qualifies justify, not duty.'),('u23','not rush merging','The source expressly supplies the negated action not rush merging and its target new releases. Interpreting the reason statement as a recommendation does not reconstruct those predicate roles; the negation remains part of the stated action.')]:
 u=next(u for u in A['units'] if u['unit_id']==i)
 for c in u['components']:
  if c['symbol'] not in ['I','Bdir']:continue
  old=copy.deepcopy(c);c.update(basis='explicit',occurrence_role='local',inference_note=note)
  if c['symbol']=='I':c['text']=action
  L.append({'change_id':f'S{1+sum(x["stage"]=="source_self_review" for x in L):02}','stage':'source_self_review','unit_id':i,'field':'components.'+c['symbol'],'meaning_changes':False,'classification':'epistemic_role_correction','reason':'Retained explicit embedded action and object roles; indirect recommendation force alone does not make those roles inferred.','before':old,'after':copy.deepcopy(c),'evidence':c['evidence']})
Path('annotation.json').write_text(json.dumps(A,ensure_ascii=False,indent=2)+'\n');Path('annotation.final.json').write_bytes(Path('annotation.json').read_bytes());Path('repair_log.json').write_text(json.dumps(L,ensure_ascii=False,indent=2)+'\n')
