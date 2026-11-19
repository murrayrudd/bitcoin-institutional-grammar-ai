from pathlib import Path
import json,hashlib,re,shutil,datetime
HERE=Path(__file__).resolve().parent
ROOT=HERE/'Bitcoin_Core_IG2_Fresh_Coding_v01'
BASE=HERE.parent/'ig2_v04/Bitcoin_Core_IG2_Specification_v0.4'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
ROOT.mkdir(exist_ok=True)
assert not (ROOT/'protocol/selection_manifest.json').exists(), 'No silent reselection'
for ver,source in [('v03',BASE/'baseline_v03'),('v04',BASE)]:
 dest=ROOT/'specifications'/ver
 for rel in ['protocol/codebook.txt','protocol/annotation_schema.json','tools/check_annotation.py']:
  (dest/rel).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/rel,dest/rel)
shutil.copytree(BASE/'calibration',ROOT/'specifications/v04/calibration',dirs_exist_ok=True)
for rel in ['evaluation/protocol.json','protocol/coder_instructions.txt','protocol/alignment_instructions.txt','protocol/source_review_instructions.txt']:
 p=ROOT/'protocol'/Path(rel).name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(BASE/rel,p)
# Assemble documented prior exposures and conservative referenced/title-screen exclusions.
reasons={};receipts=[]
def add(n,reason):
 n=int(n)
 if 0<n<100000:reasons.setdefault(n,set()).add(reason)
for p in sorted((HERE/'archives').rglob('*.json')):
 rel=str(p.relative_to(HERE));d=json.loads(p.read_text())
 if p.name in ['selection_manifest.json','selection.json','pilot_plan.json','round_plan.json','source_manifest.json','title_screen.json','content_screen.json']:
  receipts.append({'path':rel,'sha256':sha(p)})
  if p.name=='content_screen.json':
   for x in d:add(x[0],rel+' content screen')
  elif p.name=='title_screen.json':
   for x in d:add(x['number'],rel+' conservative metadata screen')
  else:
   for key in ['development_exclusions','excluded_prs','excluded_prior_cases','original_development_prs']:
    for n in d.get(key,[]):add(n,rel+' '+key)
   for key in ['selected','cases']:
    for x in d.get(key,[]):
     n=x.get('number',x.get('pr_number'))
     if n:add(n,rel+' '+key)
 # Any saved complete record, even if never a focal coded case, is conservatively exposed.
 if isinstance(d,dict) and isinstance(d.get('number'),int) and ('body' in d or 'comments' in d):add(d['number'],rel+' saved source record')
for directory in [HERE/'archives',HERE.parent/'overlap_validation',BASE/'sources']:
 for p in directory.rglob('*'):
  if p.is_file() and p.suffix in ['.json','.txt','.md','.py']:
   txt=p.read_text(errors='replace')
   for n in re.findall(r'https?://(?:api\.)?github\.com/(?:repos/)?bitcoin/bitcoin/(?:pull|pulls|issues)/(\d+)',txt):add(n,'conservative referenced episode in prior retained materials')
inventory={'created_at_utc':now(),'scope':'All retained earlier development, validation, substantive pilot, expansion and Core/Knots packages. Includes title screens and referenced episodes conservatively. Unrecorded historical inspection and model pretraining exposure cannot be ruled out.','sources':receipts,'selection_allowed':True,'excluded_prs':sorted(reasons),'exclusions':[{'number':n,'reasons':sorted(reasons[n])} for n in sorted(reasons)]}
write(ROOT/'protocol/exposure_inventory.json',inventory)
plan={'created_at_utc':now(),'parent_protocol_id':'IG2_0.4_prospective_overlap_v1','canonical_identifier_format':'bitcoin/bitcoin#<decimal PR number>','text_size':'Sum of Python Unicode lengths of complete body plus all comments, reviews, and review_comments bodies, including bot and quoted text, excluding title and serialized metadata. No text normalization.','strata_order':['procedure_title','merged','closed_unmerged'],'procedure_assignment':'Eligible title pattern first regardless of outcome; then remaining merged; then remaining closed with merged false. No year, human-entry, file-size, duration, or claim-content filters.','eligibility':'1000 <= source_text_characters <= 12000 and absent from conservative exposure inventory. Unique corpus record IDs.','supplements':'Complete retained corpus discussion; serialized corpus outcome metadata. Before dispatch, retrieve selected PR outcome metadata and relevant patches, plus directly referenced guidance pinned to an observed revision where available. No new discussion comments from live sources; no invented missing context. Log unavailable sources.','coding_scope':'Every original entry is focal, including empty entries. Supplemental files and metadata supply context and do not require exhaustive extraction, but every entry must be screened.','conditions':['v03','v04'],'schedule':[{'case':f'F{i+1:02d}','order':[f'F{i+1:02d}_{v}_r{r}' for r in range(1,4) for v in (['v03','v04'] if i%2==0 else ['v04','v03'])]} for i in range(3)],'dispatch':'Fresh context for each run; no parent history; inherited primary model and reasoning configuration, no override. Unknown provider snapshot/seed/sampling/tokens/cost null.','masking':'Alignment sees shuffled run aliases, no version labels or institution/level/force classification fields. Source reviewers see run aliases and full records without condition names or aggregate agreement. Schema structure may reveal the condition; masking is limited, not guaranteed blinding.','source_review':'Two fresh contexts review all final runs and source entries. Coordinator reconciles source-supported findings, preserves unresolved alternatives, and never overwrites raw coding.','scoring':'Count distinct source-supported error groups by proposition/error issue/case. A group may affect multiple runs and conditions; report run incidences separately. Primary effects: interpretation-changing, evidence-basis, coverage/scope. Secondary: convention-only, defensible-alternative, unresolved. No accuracy denominators or statistical inference.','agreement':'Pre-reconciliation one-to-one semantic matches within each condition and all three coders. Split/combined and unmatched groups separate. Report each field with explicit denominator. Exact-span comparison also reported. No scalar/profile standing percentage crosswalk.','frozen_criteria':'Use protocol/protocol.json and the frozen specification. A newly discovered criterion problem is reported, not changed during the evaluation.'}
write(ROOT/'protocol/operational_plan.json',plan)
shutil.copy2(__file__,ROOT/'tools/prepare.py') if (ROOT/'tools').exists() else ((ROOT/'tools').mkdir(),shutil.copy2(__file__,ROOT/'tools/prepare.py'))
frozen={str(p.relative_to(ROOT)):sha(p) for p in ROOT.rglob('*') if p.is_file()}
write(ROOT/'protocol/preselection_freeze.json',{'frozen_at_utc':now(),'files':frozen})
corpus=HERE/'corpus/prs_canonical.jsonl'
assert sha(corpus)=='b289aa40737d619dea8a673290fae636dbe1a65ccf49331223ab548acb23f7c9'
pools={k:[] for k in plan['strata_order']};seen=set();offset=0;pattern=re.compile(r'contribut|review|maintain|moder|govern|release|procedure|guideline',re.I)
with corpus.open('rb') as f:
 for line_num,raw in enumerate(f,1):
  r=json.loads(raw);n=r['number'];assert n not in seen;seen.add(n)
  chars=len(r.get('body') or '')+sum(len(e.get('body') or '') for g in ['comments','reviews','review_comments'] for e in r.get(g,[]))
  stratum=None
  if n not in reasons and 1000<=chars<=12000:
   if pattern.search(r['title']):stratum='procedure_title'
   elif r.get('merged') is True:stratum='merged'
   elif r.get('state')=='closed' and r.get('merged') is False:stratum='closed_unmerged'
  if stratum:
   identity=f'bitcoin/bitcoin#{n}';digest=hashlib.sha256(('IG2_0.4_prospective_overlap_v1|'+identity).encode()).hexdigest()
   pools[stratum].append({'number':n,'title':r['title'],'canonical_identifier':identity,'rank':digest,'source_text_characters':chars,'line_number':line_num,'byte_offset':offset,'byte_length':len(raw),'line_sha256':hashlib.sha256(raw).hexdigest()})
  offset+=len(raw)
assert len(seen)==25508
selected=[]
for i,(group,values) in enumerate(pools.items(),1):
 values.sort(key=lambda x:x['rank']);x=values[0];eid=f'F{i:02d}';selected.append({'episode_id':eid,'stratum':group,**x})
 with corpus.open('rb') as f:f.seek(x['byte_offset']);raw=f.read(x['byte_length'])
 p=ROOT/'sources'/eid/'canonical_line.jsonl';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
 write(p.parent/'record.json',json.loads(raw))
write(ROOT/'protocol/selection_manifest.json',{'selected_at_utc':now(),'corpus_sha256':sha(corpus),'corpus_records':len(seen),'exclusion_count':len(reasons),'inventory_sha256':sha(ROOT/'protocol/exposure_inventory.json'),'eligible_counts':{k:len(v) for k,v in pools.items()},'selected':selected})
write(ROOT/'protocol/candidate_ranks.json',pools)
print(json.dumps({'exclusion_count':len(reasons),'eligible_counts':{k:len(v) for k,v in pools.items()},'selected':selected},indent=2))
