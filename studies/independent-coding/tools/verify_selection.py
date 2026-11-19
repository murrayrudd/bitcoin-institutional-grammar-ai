"""Recheck fixed selection. Optional argument is the original canonical JSONL.
Does not select new episodes or change any frozen study input.
"""
from pathlib import Path
import json,hashlib,re,sys
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
manifest=read(R/'protocol/selection_manifest.json');inventory=read(R/'protocol/exposure_inventory.json');pools=read(R/'protocol/candidate_ranks.json');errors=[];count=0
for c in manifest['selected']:
 p=sorted(pools[c['stratum']],key=lambda x:x['rank']);count+=3
 if c['number']!=p[0]['number']:errors.append('Not first ranked '+c['episode_id'])
 if c['number'] in inventory['excluded_prs']:errors.append('Exposure '+c['episode_id'])
 if c['rank']!=hashlib.sha256(('IG2_0.4_prospective_overlap_v1|bitcoin/bitcoin#'+str(c['number'])).encode()).hexdigest():errors.append('Rank '+c['episode_id'])
corpus_check='not supplied'
if len(sys.argv)>1:
 h=hashlib.sha256();seen=set();excluded=set(inventory['excluded_prs']);observed={k:[] for k in pools};pattern=re.compile(r'contribut|review|maintain|moder|govern|release|procedure|guideline',re.I)
 with Path(sys.argv[1]).open('rb') as f:
  for raw in f:
   h.update(raw);r=json.loads(raw);n=r['number'];assert n not in seen;seen.add(n)
   chars=len(r.get('body') or '')+sum(len(e.get('body') or '') for g in ['comments','reviews','review_comments'] for e in r.get(g,[]))
   if n in excluded or not 1000<=chars<=12000:continue
   if pattern.search(r['title']):group='procedure_title'
   elif r.get('merged') is True:group='merged'
   elif r.get('merged') is False and r.get('state')=='closed':group='closed_unmerged'
   else:continue
   observed[group].append(n)
 count+=2+len(pools)
 if h.hexdigest()!=manifest['corpus_sha256']:errors.append('Corpus SHA256 mismatch')
 if len(seen)!=manifest['corpus_records']:errors.append('Corpus record count')
 for k,values in observed.items():
  if set(values)!={x['number'] for x in pools[k]}:errors.append('Candidate universe mismatch '+k)
 corpus_check='pass' if not errors else 'fail'
result={'status':'fail' if errors else 'pass','checks':count,'corpus_reconstruction':corpus_check,'errors':errors}
(R/'analysis/selection_verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));sys.exit(bool(errors))
