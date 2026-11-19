from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parent;P=R/'package'
CASES=[(8771,'guidance','Limits on simultaneous contributions'),(11276,'guidance','Reducing unnecessary review workload'),(17940,'guidance','Competing rebase guidance proposal'),(26399,'guidance','Explicit attribution of closure to contribution requirements'),(17685,'recognition','Reminder to identify the reviewed commit'),(31904,'recognition','Distinguishing concept approval from code review'),(36127,'recognition','Reported omission from automated review counting'),(11743,'recognition','Contested review sufficiency after merge'),(7005,'authority','Unmerged subsystem responsibility file'),(25839,'authority','Unmerged minimal maintainer document'),(23798,'authority','Trusted key addition and appointment evidence'),(27054,'authority','Trusted key removal and departure evidence')]
plan=json.load(open(P/'protocol/round_plan.json'));exclude=set(plan['excluded_prs']);assert not exclude.intersection(n for n,_,_ in CASES)
records={};offset=0
for line_no,line in enumerate((R.parent/'pilot_work/frozen/prs_canonical.jsonl').open('rb'),1):
 r=json.loads(line)
 if r['number'] in [n for n,_,_ in CASES]:records[r['number']]=(r,{'line_number':line_no,'byte_offset':offset,'byte_length':len(line),'line_sha256':hashlib.sha256(line).hexdigest()})
 offset+=len(line)
manifest=[]
for i,(n,family,reason) in enumerate(CASES,1):
 eid=f'E{i:02}';r,loc=records[n];(P/f'sources/records/{eid}_pr{n}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 entries=[{'source_id':f'{eid}:body','kind':'body','author':r.get('author'),'timestamp':r.get('created_at'),'text':r.get('body') or ''}]
 for kind in ['comments','reviews','review_comments']:
  for j,x in enumerate(r.get(kind,[])):
   entries.append({'source_id':f'{eid}:{kind}:{j}','kind':kind,'author':x.get('author'),'timestamp':x.get('created_at',x.get('submitted_at')),'path':x.get('path'),'text':x.get('body') or ''})
 packet={'episode_id':eid,'pr_number':n,'url':f'https://github.com/bitcoin/bitcoin/pull/{n}','title':r['title'],'created_at':r['created_at'],'closed_at':r.get('closed_at'),'merged_at':r.get('merged_at'),'recorded_merged':r.get('merged'),'recorded_merger':r.get('merged_by'),'entries':entries,'supplemental_entries':[],'limits':plan['known_limits']}
 (P/f'sources/packets/{eid}.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
 (P/f'sources/packets/{eid}_discussion.txt').write_text('\n\n'.join(f"[{e['source_id']}] {e['author']} {e['timestamp']}\n{e['text']}" for e in entries))
 manifest.append({'episode_id':eid,'number':n,'family':family,'selection_reason':reason,'title':r['title'],'year':r['created_at'][:4],'recorded_merged':r.get('merged'),'entries':len(entries),'chars':sum(len(e['text']) for e in entries),**loc})
 (P/f'analysis/{eid}').mkdir(exist_ok=True)
selection={'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selection':'Purposive; titles screened first, recognition cases identified by phrase searches; screening text was visible before selection. Not held out or representative.','cases':manifest}
(P/'protocol/selection.json').write_text(json.dumps(selection,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
