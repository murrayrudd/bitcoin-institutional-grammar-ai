from pathlib import Path
import json,hashlib,re,datetime,shutil
R=Path(__file__).resolve().parent
P=R/'package'
for d in ['protocol','sources/records','sources/packets','sources/supplements','analysis','tools','documents']: (P/d).mkdir(parents=True,exist_ok=True)
src=R/'inputs/unpacked/Bitcoin_IG2_Substantive_Pilot_v01'
old=json.loads((src/'protocol/pilot_plan.json').read_text())
excluded=set(old['excluded_prior_cases'])|{x['pr_number'] for x in old['cases']}|{15626}
for n in ['codebook.txt','annotation_schema.json']: shutil.copyfile(src/'protocol'/n,P/'protocol'/n)
plan={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'round':'evidence-expansion-1','research_question':'Under what evidentiary conditions can IG 2.0 reconstruct institutional arrangements from public records of decentralized coordination?','design':'Purposive comparative episode study with evidence availability modeling; not a randomized benchmark or a population estimate.','target_new_episodes':12,'selection_families':['review expectations and guidance','review recognition and technical mediation','role authority and recurring procedures'],'selection_rules':['Exclude all 24 previous focal episodes and bridge 15626.','Screen titles and source lengths first; select historical and outcome variation with manageable full discussions.','Retain thin records and contrary cases; disclose any content-informed selection.','Group linked episodes rather than claiming independent observations.'],'evidence_layers':{'D':'Contemporaneous dated standing guidance only. Proposed documents separately labeled and not treated as standing.','T':'D plus complete available frozen discussion and recorded outcome.','I':'T plus relevant commit-pinned files, patches, and implementation evidence.'},'execution':'One continuing assistant analysis, with deterministic exact-evidence checks and a separate within-session source review. No independent or blind model runs are claimed. Evidence-layer comparisons are source-availability assessments, not performance estimates.','coding_scope':'Focal institutional propositions and case mechanisms, applying v0.3 distinctions. Complete packets retained and read; not exhaustive v0.3 component annotation of every candidate statement.','narrative_comparison':'Within-session structured versus narrative representation on selected contrasts; a diagnostic of information preservation, not a blind efficacy benchmark.','primary_outputs':['Focal claim ledger with source anchors and counterevidence','D/T/I claim support and uncertainty','Mechanism maps and bounded level conclusions','Negative and contrary cases','Readiness assessment for paper'],'frozen_codebook_sha256':hashlib.sha256((P/'protocol/codebook.txt').read_bytes()).hexdigest(),'excluded_prs':sorted(excluded),'known_limits':['Public corpus may omit patch histories, comment edits, thread links, and off-platform activity.','No model accuracy, superiority, cost or scalability estimates.','Recorded merges do not establish recognition of each provision or network adoption.','Source sufficiency remains revisable; richer evidence is not a gold standard.']}
f=P/'protocol/round_plan.json'
assert not f.exists()
f.write_text(json.dumps(plan,indent=2)+'\n')
corpus=R.parent/'pilot_work/frozen/prs_canonical.jsonl'
h=hashlib.sha256(); candidates=[]; count=0
for line in corpus.open('rb'):
 h.update(line); r=json.loads(line); count+=1
 if r['number'] in excluded: continue
 title=r['title']; bodies=[r.get('body') or '']+[x.get('body') or '' for k in ['comments','reviews','review_comments'] for x in r.get(k,[])]
 if re.search(r'contribut|maintain|trusted.key|review.*(guid|polic|ack|process)|ack.*(review|hash)|merge.*(polic|process)|code.of.conduct',title,re.I):
  if 200<=sum(map(len,bodies))<=22000:
   candidates.append({'number':r['number'],'title':title,'year':r['created_at'][:4],'merged':r.get('merged'),'chars':sum(map(len,bodies)),'entries':len(bodies),'files':[x['filename'] for x in r.get('files',[])]})
assert h.hexdigest()==old['corpus_sha256']
(P/'protocol/corpus_receipt.json').write_text(json.dumps({'path':str(corpus),'sha256':h.hexdigest(),'records':count},indent=2)+'\n')
(P/'protocol/title_screen.json').write_text(json.dumps(candidates,indent=2)+'\n')
for r in candidates: print(r['number'],r['year'],r['merged'],r['chars'],r['entries'],r['title'])
