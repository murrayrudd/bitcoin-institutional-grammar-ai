"""Verify frozen inputs/outputs and the completed adjudication without modifying them."""
from pathlib import Path
import json,hashlib,datetime,re,sys
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
errors=[];checks=0

def compare(root,files,label):
 global checks
 for path,want in files.items():
  checks+=1;p=root/path
  if not p.is_file() or sha(p)!=want:errors.append(label+': '+path)

for frozen in ['preselection_freeze.json','dispatch_freeze.json']:
 compare(R,read(R/'protocol'/frozen)['files'],frozen)
allruns=read(R/'analysis/all_coding_frozen.json')
for rid in allruns['runs']:
 d=R/'runs'/rid;f=R/'analysis/run_freezes'/f'{rid}.json'
 checks+=1
 if sha(f)!=allruns['run_freeze_sha256'][rid]:errors.append('Run freeze changed '+rid)
 compare(d,read(d/'input_manifest.json')['files'],'Run input '+rid)
 compare(d,read(f)['files'],'Run output '+rid)
for name,freeze in [('alignment','alignment_freeze.json'),('source_review_a','source_review_a_freeze.json'),('source_review_b','source_review_b_freeze.json')]:
 d=R/'reviews'/name
 compare(d,read(d/'input_manifest.json')['files'],'Review input '+name)
 compare(d,read(R/'analysis'/freeze)['files'],'Review output '+name)

ann={a['annotation_id']:a for a in read(R/'reviews/source_review_a/annotations.json')}
texts={e['source_id']:e['text'] for case in ['F01','F02','F03'] for e in read(R/'sources'/case/'packet.json')['entries']}
rec=read(R/'analysis/reconciliation.json')
fids={f['finding_id'] for name in ['source_review_a','source_review_b'] for f in read(R/'reviews'/name/'review.json')['findings']}
if set(rec['finding_to_groups'])!=fids or not all(rec['finding_to_groups'].values()):errors.append('Incomplete finding mapping')
if len({g['group_id'] for g in rec['groups']})!=len(rec['groups']):errors.append('Duplicate reconciliation group')
for g in rec['groups']:
 for a in g['affected']:
  checks+=1
  if a['annotation_id'] not in ann:errors.append(g['group_id']+' unknown annotation');continue
  known={u['unit_id'] for u in ann[a['annotation_id']]['units']}
  if not set(a['unit_ids'])<=known:errors.append(g['group_id']+' unknown unit')
  for rel in a['relation_ids']:
   m=re.fullmatch(r'relations\[(\d+)\]',rel)
   if not m or int(m[1])>=len(ann[a['annotation_id']]['relations']):errors.append(g['group_id']+' relation path '+rel)
 for e in g['source_evidence']:
  checks+=1;s=e['span'];t=texts[e['source_id']]
  if not 0<=s['start']<s['end']<=len(t) or t[s['start']:s['end']]!=s['quote']:errors.append(g['group_id']+' anchor')
for c in read(R/'analysis/adoptable_case_claims.json')['claims']:
 for e in c['evidence']:
  checks+=1;s=e['span'];t=texts[e['source_id']]
  if t[s['start']:s['end']]!=s['quote']:errors.append(c['id']+' anchor')
primary=[g for g in rec['groups'] if g['category']=='primary_error']
if len(primary)!=5:errors.append('Primary-group count')
if read(R/'analysis/common_composite_agreement.json')['all_three_all_six_fields']!={'v03':24,'v04':21}:errors.append('Composite result')
status=read(R/'analysis/report_status.json')
if not all(status.get(x) for x in ['source_audits_complete','independent_coding_complete','agreement_complete','reconciliation_complete']):errors.append('Final completion status')
result={'status':'fail' if errors else 'pass','checks':checks,'errors':errors,'runs':len(allruns['runs']),'review_findings_mapped':len(fids),'reconciliation_groups':len(rec['groups']),'primary_error_groups':len(primary),'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Integrity, coverage, exact anchors, and result consistency; not a semantic truth certificate.'}
print(json.dumps(result,indent=2));sys.exit(bool(errors))
