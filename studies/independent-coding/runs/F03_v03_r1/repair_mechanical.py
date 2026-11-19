import json
from pathlib import Path
root=Path(__file__).resolve().parent
a=json.loads((root/'annotation.json').read_text()); p=json.loads((root/'packet.json').read_text()); s={e['source_id']:e['text'] for e in p['entries']}
u=next(u for u in a['units'] if u['unit_id']=='F03-U09')
c=next(c for c in u['components'] if c['symbol']=='Bdir')
old=c['evidence'][0]
start=s[u['source_id']].index('red text',u['span']['start'],u['span']['end'])
new={'source_id':u['source_id'],'span':{'start':start,'end':start+len('red text'),'quote':'red text'}}
c['evidence']=[new]
changes=[{'change_id':'R01','phase':'checker_feedback','classification':'evidence_origin_error','meaning_changes':False,'affected':['F03-U09.components.Bdir.evidence'],'before':old,'after':new,'reason':'The first checker flagged the same phrase anchored outside this unit. The local occurrence in the non-replacable-case proposal is the correct evidence. The action target and inference status do not change.'}]
(root/'annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
(root/'repair_log.json').write_text(json.dumps({'run_id':'F03_v03_r1','changes':changes},ensure_ascii=False,indent=2)+'\n')
