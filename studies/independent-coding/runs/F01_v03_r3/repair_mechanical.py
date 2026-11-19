from pathlib import Path
import json
A=json.loads(Path('annotation.json').read_text()); P=json.loads(Path('packet.json').read_text()); S={e['source_id']:e['text'] for e in P['entries']}; log=[]
def u(i):return next(x for x in A['units'] if x['unit_id']==i)
def fix(i,symbol,quote,which=0):
 x=u(i); cs=[c for c in x['components'] if c['symbol']==symbol];c=cs[which];old=json.loads(json.dumps(c)); start=S[x['source_id']].index(quote,x['span']['start'],x['span']['end']);c['evidence']=[{'source_id':x['source_id'],'span':{'start':start,'end':start+len(quote),'quote':quote}}]
 log.append({'change_id':f'M{len(log)+1:02}','stage':'mechanical','unit_id':i,'field':f'components.{symbol}.evidence','meaning_changes':False,'classification':'anchor_occurrence_error','reason':'Replaced an unintended first source occurrence with the intended complete token inside the focal unit. Intended role and proposition remain unchanged.','before':old,'after':c})
fix('u06','Bdir','it');fix('u08','Bdir','it');fix('u09','A','we');fix('u13','I','remove');fix('u24','Cex','always',1)
for i,symbol,note in [('u15','A','The source explicitly assigns we the causative action have it loop. The reconstructed configure action retains that same causative actor; pragmatic recommendation force does not transform this actor role.'),('u25','Bdir','The latest release is explicitly the object of add in the source. Reconstructing the indirect recommendation leaves that action-object relation intact; only the recommendation force is inferred.')]:
 c=next(c for c in u(i)['components'] if c['symbol']==symbol);old=c['inference_note'];c['inference_note']=note
 log.append({'change_id':f'M{len(log)+1:02}','stage':'mechanical','unit_id':i,'field':f'components.{symbol}.inference_note','meaning_changes':False,'classification':'missing_role_preservation_explanation','reason':'Supplied the required explicit-argument explanation for the pragmatic parse; role basis retained for source self-review.','before':old,'after':note,'evidence':c['evidence']})
Path('annotation.json').write_text(json.dumps(A,ensure_ascii=False,indent=2)+'\n');Path('repair_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
