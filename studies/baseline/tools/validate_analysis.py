"""Deterministic integrity and evidence-identity checks, not semantic validation."""
from pathlib import Path
import json,hashlib,collections,sys
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
sel=read('protocol/selection.json')['cases'];plan=read('protocol/round_plan.json')
assert len(sel)==12 and len({s['number'] for s in sel})==12
assert not ({s['number'] for s in sel}&set(plan['excluded_prs']))
assert hashlib.sha256((ROOT/'protocol/codebook.txt').read_bytes()).hexdigest()==plan['frozen_codebook_sha256']
packets={p.stem:json.loads(p.read_text()) for p in (ROOT/'sources/packets').glob('E??.json')}
sources={e['source_id']:e for p in packets.values() for e in p['entries']+p['supplemental_entries']}
anchor_count=0
def check(a):
 global anchor_count
 s=a['span'];t=sources[a['source_id']]['text'];assert 0<=s['start']<s['end']<=len(t);assert t[s['start']:s['end']]==s['quote'];anchor_count+=1
claims=read('analysis/claim_ledger.json')['claims'];ids={c['claim_id'] for c in claims}
assert len(ids)==len(claims)==48
for c in claims:
 assert c['evidence'];assert c['assessment'] in ['supported','attributed','unresolved','contradicted']
 for a in c['evidence']:check(a)
 assert c['assessment_available_at']==max((sources[a['source_id']]['layer'] for a in c['evidence']),key='DTI'.index)
units=read('analysis/focal_ig_records.json')['units']
for u in units:
 check({'source_id':u['source_id'],'span':u['span']})
 for c in u['components']:
  check(c['evidence']);s=c['evidence']['span']
  if c['occurrence_role']=='local':assert u['span']['start']<=s['start']<s['end']<=u['span']['end']
 assert set(u['linked_claim_ids'])<=ids
for r in read('sources/catalog.json'):
 assert hashlib.sha256(sources[r['source_id']]['text'].encode()).hexdigest()==r['text_sha256']
assert read('analysis/source_integrity.json')['all_git_blobs_match']
assert "doesn't attract anyone willing to review" not in sources['E02:doc_head']['text']
assert 'purpleKarrot' not in sources['E06:merge_message']['text']
assert 'vicjuma:' in sources['E07:merge_message']['text']
gate=read('analysis/key_gate_experiment.json');assert len(gate['runs'])==12 and gate['all_passed']
assert len(read('analysis/case_mechanisms.json'))==12
# Optional exact recheck against the original, unbundled canonical JSONL.
corpus_checks=None
if len(sys.argv)>1:
 corpus=Path(sys.argv[1]);receipt=read('protocol/corpus_receipt.json')
 with corpus.open('rb') as f:
  for r in sel:
   f.seek(r['byte_offset']);line=f.read(r['byte_length']);assert hashlib.sha256(line).hexdigest()==r['line_sha256']
   assert json.loads(line)==read(f"sources/records/{r['episode_id']}_pr{r['number']}.json")
 corpus_checks=12
out={'passed':True,'episodes':12,'frozen_entries':sum(len(p['entries']) for p in packets.values()),'focal_claims':len(claims),'focal_ig_projections':len(units),'exact_anchor_checks':anchor_count,'verified_git_blobs':len(read('analysis/source_integrity.json')['git_blob_checks']),'simulated_gate_checks':12,'original_corpus_line_checks':corpus_checks,'assessment_counts':dict(collections.Counter(c['assessment'] for c in claims)),'limits':'Valid offsets and hashes establish identity and reproducibility, not semantic correctness, institutional truth, coding reliability or model performance.'}
(ROOT/'analysis/validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
