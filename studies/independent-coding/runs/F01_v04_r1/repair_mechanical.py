from pathlib import Path
import json,copy,datetime
p=json.loads(Path('packet.json').read_text()); txt={e['source_id']:e['text'] for e in p['entries']}
a=json.loads(Path('annotation.json').read_text()); units={u['unit_id']:u for u in a['units']}; logs=[]
def ev(s,q,start=0):
 i=txt[s].index(q,start);return {'source_id':s,'span':{'start':i,'end':i+len(q),'quote':q}}
def change(uid,path,value,reason,effect='convention_deviation',meaning=False):
 d=units[uid]
 for k in path[:-1]:d=d[k]
 old=copy.deepcopy(d[path[-1]]);d[path[-1]]=value
 logs.append({'change_id':'M%02d'%(len(logs)+1),'stage':'checker_repair','unit_id':uid,'path':path,'before':old,'after':value,'reason':reason,'diagnosis':'execution_failure_under_existing_rule','effect':effect,'meaning_changed':meaning})
u=units['S02'];change('S02',['components',0,'governing_span'],{'source_id':u['source_id'],'span':u['span']},'The local see clause must fit inside the first referral unit. The second referral carries shared scope separately.')
for uid in ['S11','S24']:
 for j,c in enumerate(units[uid]['components']):
  if c['symbol']=='Bdir':change(uid,['components',j,'inference_note'],'The source explicitly supplies this object under the stated adding/merging action; the pragmatic interpretation changes recommendation force, not this predicate role.','Explain why the explicit object role survives the pragmatic reading.')
change('S13',['institution','standing_profile','recognition'],'none','A response event that repeats a personal strategy is not an expectation-recognition event. Same-actor restatement remains visible in the event record.','evidence_basis_error',True)
# Select the actual main-clause subject rather than an earlier matching pronoun.
s=units['S22']['source_id']; main=ev(s,'we could just leave the PR open')
change('S22',['components',0,'evidence'],[ev(s,'we',main['span']['start'])],'The subject of leave is the main-clause we, not we in the earlier as-we-have-done predicate.','evidence_basis_error')
# The first alternative has a local governing clause that ends at its own action.
for j,c in enumerate(units['S27']['components']):
 if c['symbol'] in ['A','D','Cac']:change('S27',['components',j,'governing_span'],{'source_id':units['S27']['source_id'],'span':units['S27']['span']},'Local components must be governed by the remove branch itself; the explain branch retains its shared-scope citation.')
# Packet/checker revision-key incompatibilities remain untouched and will be documented.
Path('annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n');Path('annotation.postmechanical.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
Path('repair_log.json').write_text(json.dumps({'run_id':'F01_v04_r1','changes':logs},ensure_ascii=False,indent=2)+'\n')
