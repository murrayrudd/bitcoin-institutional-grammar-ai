from pathlib import Path
import json,copy
p=Path(__file__).resolve().parent
a=json.loads((p/'annotation.json').read_text());d={u['unit_id']:u for u in a['units']};packet=json.loads((p/'packet.json').read_text());texts={e['source_id']:e['text'] for e in packet['entries']}
def ev(s,q,start=None):
 t=texts[s];start=t.index(q) if start is None else start;assert t[start:start+len(q)]==q
 return {'source_id':s,'span':{'start':start,'end':start+len(q),'quote':q}}
log=[]
u=d['D01'];old=copy.deepcopy(u['proposition']);u['proposition']['decision_object_id']=None;u['proposition']['identity_evidence']=[ev('pr26586:comments:0','https://github.com/bitcoin/bitcoin/blob/master/CONTRIBUTING.md#code-review')];u['proposition']['qualifiers'][0]['description']='The requested guide has a mutable master URL. Its original revision is unresolved; the supplied pinned base-revision guide is contextual evidence, not the proven exact navigation target.'
log.append({'change_id':'M01','stage':'mechanical_repair','unit_id':'D01','fields':['proposition.decision_object_id','proposition.identity_evidence','proposition.qualifiers'],'before':old,'after':copy.deepcopy(u['proposition']),'meaning_changes':True,'effect':'evidence-basis error','diagnosis':'execution_failure','reason':'Checker found unsupported identity. Original link names mutable master, while the assigned canonical ID names a specific revision. Clear the exact object rather than invent a revision identity.','evidence':u['proposition']['identity_evidence']})
u=d['C03'];c=next(c for c in u['components'] if c['symbol']=='Bdir');old=copy.deepcopy(c);start=texts[u['source_id']].index('it needs a rebase',u['span']['start']);c['evidence']=[ev(u['source_id'],'it',start)];c['inference_note']='The literal subject it in it needs a rebase becomes the target of reconstructed rebase. The prior occurrence inside bit is unrelated and is not evidence.'
log.append({'change_id':'M02','stage':'mechanical_repair','unit_id':'C03','fields':['components.Bdir.evidence','components.Bdir.inference_note'],'before':old,'after':copy.deepcopy(c),'meaning_changes':False,'effect':'evidence-basis error','diagnosis':'execution_failure','reason':'Substring search hit it inside bit in the prior sentence. Replace with the complete local subject pronoun in the relevant predicate.','evidence':c['evidence']})
(p/'annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n');(p/'repair_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
