"""Freeze run artifacts, prepare masked review inputs, and audit exact identities.
No semantic correction or model calls occur in this script.
"""
from pathlib import Path
import json,hashlib,datetime,sys,shutil,subprocess,re
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def freeze_run(rid):
 d=R/'runs'/rid;inp=read(d/'input_manifest.json');bad=[p for p,h in inp['files'].items() if sha(d/p)!=h]
 required=['annotation.first_complete.json','annotation.final.json','checks.first.json','checks.json','repair_log.json','review_notes.json','access_record.json']
 missing=[f for f in required if not (d/f).exists()]
 if bad or missing:raise RuntimeError({'run':rid,'changed_inputs':bad,'missing':missing})
 checks={}
 for stage in ['first_complete','final']:
  p=subprocess.run([sys.executable,str(d/'tools/check_annotation.py'),str(d/'packet.json'),str(d/f'annotation.{stage}.json')],capture_output=True,text=True)
  try:checks[stage]=json.loads(p.stdout)
  except Exception:checks[stage]={'status':'failed_invocation','stdout':p.stdout,'stderr':p.stderr,'returncode':p.returncode}
 receipt={'run_id':rid,'frozen_at_utc':now(),'input_integrity':'pass','files':{f:sha(d/f) for f in required},'independent_mechanical_checks':checks}
 p=R/'analysis/run_freezes'/f'{rid}.json'
 if p.exists():
  old=read(p)
  assert old['files']==receipt['files'],'Frozen output changed'
 else:write(p,receipt)
 return {'run':rid,'units':len(read(d/'annotation.final.json')['units']),'status':checks['final'].get('status')}
def prepare_masked():
 schedule=read(R/'protocol/operational_plan.json')['schedule'];ids=[rid for s in schedule for rid in s['order']]
 for rid in ids:freeze_run(rid)
 ordered=sorted(ids,key=lambda rid:hashlib.sha256(('IG2_mask_v1|'+rid).encode()).hexdigest())
 aliases={rid:f'R{i+1:02d}' for i,rid in enumerate(ordered)}
 write(R/'analysis/mask_key.json',aliases)
 for i,ver in enumerate(['v04','v03']):
  text=(R/'specifications'/ver/'protocol/codebook.txt').read_text()
  text=re.sub(r'0\.[234]', '[specification identifier omitted]',text)
  for target in ['source_review_a','source_review_b']:
   p=R/'reviews'/target/f'guide_{i+1}.txt';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
 full=[];aligned=[]
 for rid in ordered:
  a=read(R/'runs'/rid/'annotation.final.json');alias=aliases[rid];eid=a['episode_id'];g='guide_1.txt' if '_v04_' in rid else 'guide_2.txt'
  masked={k:v for k,v in a.items() if k not in ['schema_version','run_id']};masked['annotation_id']=alias;masked['assigned_guide']=g
  full.append(masked)
  fields=['unit_id','source_id','span','parent_unit_id','record_role','parse_mode','components','alternative_interpretation','proposition']
  aligned.append({'annotation_id':alias,'episode_id':eid,'units':[{k:u[k] for k in fields if k in u} for u in a['units'] if u['record_role']=='statement'],'links':[rel for rel in a['relations'] if rel['type'] in ['AND','OR','XOR','NOT','quotes']],'note':'Classification labels withheld; components and proposition text can partly reveal coding conventions.'})
 for target in ['source_review_a','source_review_b','alignment']:
  p=R/'reviews'/target;p.mkdir(parents=True,exist_ok=True)
  for source in (R/'sources').glob('*/packet.json'):shutil.copy2(source,p/(source.parent.name+'_packet.json'))
  write(p/'annotations.json',aligned if target=='alignment' else full)
  instruction='alignment_instructions.txt' if target=='alignment' else 'source_review_instructions.txt'
  shutil.copy2(R/'protocol'/instruction,p/'INSTRUCTIONS.txt')
  write(p/'input_manifest.json',{'prepared_at_utc':now(),'files':{q.name:sha(q) for q in p.iterdir() if q.is_file() and q.name!='input_manifest.json'}})
 write(R/'analysis/all_coding_frozen.json',{'frozen_at_utc':now(),'runs':ids,'run_freeze_sha256':{rid:sha(R/'analysis/run_freezes'/f'{rid}.json') for rid in ids}})
 print('Prepared masked inputs for',len(ids),'frozen runs')
def verify_sources():
 errors=[];checks=0
 for fname in ['preselection_freeze.json','dispatch_freeze.json']:
  f=read(R/'protocol'/fname)
  for p,h in f['files'].items():
   checks+=1
   if sha(R/p)!=h:errors.append(f'{fname}: {p}')
 for case in read(R/'protocol/selection_manifest.json')['selected']:
  d=R/'sources'/case['episode_id'];raw=(d/'canonical_line.jsonl').read_bytes();r=json.loads(raw);p=read(d/'packet.json');focal=[e for e in p['entries'] if e['source_id'] in p['selection_design']['focal_source_ids']]
  expected=[r.get('body') or '']+[e.get('body') or '' for g in ['comments','reviews','review_comments'] for e in r.get(g,[])]
  checks+=4
  if sha(d/'canonical_line.jsonl')!=case['line_sha256']:errors.append(case['episode_id']+' corpus line')
  if [e['text'] for e in focal]!=expected:errors.append(case['episode_id']+' discussion text')
  if sum(map(len,expected))!=case['source_text_characters']:errors.append(case['episode_id']+' text count')
  if case['number'] in read(R/'protocol/exposure_inventory.json')['excluded_prs']:errors.append(case['episode_id']+' exposure')
 result={'status':'fail' if errors else 'pass','checks':checks,'errors':errors,'checked_at_utc':now()};write(R/'analysis/source_integrity.json',result);print(json.dumps(result))
if __name__=='__main__':
 if sys.argv[1]=='freeze':print(json.dumps(freeze_run(sys.argv[2])))
 elif sys.argv[1]=='mask':prepare_masked()
 elif sys.argv[1]=='verify':verify_sources()
