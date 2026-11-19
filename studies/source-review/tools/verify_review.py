"""Verify delivered hashes, scope, source anchors, and annotation structure only."""
from pathlib import Path
import json, hashlib
from check_annotation import check
P=Path(__file__).resolve().parents[1]
def read(path):return json.loads((P/path).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
frozen=read('protocol/frozen_inputs.json')
for name,h in frozen['protocol_files'].items():assert sha(P/name)==h,name
if (P/'protocol/baseline_preservation.json').exists():
 for item in read('protocol/baseline_preservation.json')['files']:
  assert sha(P/item['round4_path'])==item['sha256'],item['round4_path']
sample=read('protocol/selected_sample.json')
assert len(sample)==24 and len({x['source_id'] for x in sample})==24
results={}
for g in ['A','B','C']:
 inp=P/'reviewer_inputs'/g;out=P/'reviewer_outputs'/g
 assert sha(inp/'input_manifest.json')==frozen['reviewer_input_manifests'][g]
 for item in json.loads((inp/'input_manifest.json').read_text())['files']:
  assert sha(inp/item['path'])==item['sha256'],(g,item['path'])
 f=json.loads((out/'freeze.json').read_text())
 for item in f['files']:assert sha(out/item['path'])==item['sha256'],(g,item['path'])
 p=inp/f['packet_file'];a=out/'annotation.json'
 assert sha(a)==f['annotation_sha256']
 packet=json.loads(p.read_text());focus=set(packet['selection_design']['focal_source_ids'])
 assert focus=={x['source_id'] for x in sample if x['reviewer_group']==g} and len(focus)==8
 result=check(p,a);assert result['status']=='pass',result
 annotation=json.loads(a.read_text())
 results[g]={k:result[k] for k in ['screened_entries','units','statement_units','exact_anchor_references']}
 results[g]['focal_statement_units']=sum(u['record_role']=='statement' and u['source_id'] in focus for u in annotation['units'])
sf=read('reviewer_outputs/C/supplement/freeze.json')
for name,h in sf['files'].items():assert sha(P/name)==h,name
sp=P/'reviewer_inputs/C/supplement/packet_v2.json'
sa=P/'reviewer_outputs/C/supplement/annotation.supplemented.json'
sr=check(sp,sa);assert sr['status']=='pass',sr
op=read('reviewer_inputs/C/packet.json');np=json.loads(sp.read_text())
assert np['entries'][:-1]==op['entries'] and np['entries'][-1]['source_id']=='32406-169'
assert np['selection_design']['focal_source_ids']==op['selection_design']['focal_source_ids']
results['C_supplement']={k:sr[k] for k in ['screened_entries','units','statement_units','exact_anchor_references']}
registry={e['source_id']:e for e in read('sources/baseline_all_source_registry.json')}
for g in ['A','B','C']:
 f=read(f'reviewer_outputs/{g}/freeze.json')
 for e in read(f'reviewer_inputs/{g}/'+f['packet_file'])['entries']:
  if e['source_id'] in registry:assert registry[e['source_id']]['text']==e['text']
  registry[e['source_id']]=e
def anchors(obj):
 if isinstance(obj,dict):
  if 'source_id' in obj and 'span' in obj:
   t=registry[obj['source_id']]['text'];s=obj['span'];assert 0<=s['start']<s['end']<=len(t) and t[s['start']:s['end']]==s['quote']
  for v in obj.values():anchors(v)
 elif isinstance(obj,list):
  for v in obj:anchors(v)
for file in ['analysis/adjudication_ledger.json','analysis/candidate_additions.json','analysis/reconciled_sample_decisions.json','analysis/candidate_inventory_corrected.json']:
 if (P/file).exists():anchors(read(file))
corrected=P/'annotations/corrected_baseline.json'
if corrected.exists():
 result=check(P/'sources/corrected_annotation_packet.json',corrected);assert result['status']=='pass',result
 results['corrected_baseline']={k:result[k] for k in ['screened_entries','units','statement_units','exact_anchor_references']}
 summary=read('analysis/review_summary.json');decisions=read('analysis/reconciled_sample_decisions.json')
 baseline=read('sources/baseline_annotations.json');focal_ids={x['source_id'] for x in sample}
 focal_units={u['unit_id'] for u in baseline['units'] if u['source_id'] in focal_ids and u['record_role']=='statement'}
 covered={u for f in read('analysis/adjudication_ledger.json') for u in f['baseline_unit_ids']}
 assert len(focal_units)==summary['baseline_fully_annotated_statements_in_sample']==17 and focal_units<=covered
 assert len(decisions)==24 and {x['source_id'] for x in decisions}==focal_ids
 assert sum(d['reconciled_screen']=='candidate' for d in decisions)==summary['reconciled_candidate_records']==21
 assert sum(len(d['reviewer_statement_units']) for d in decisions)==summary['fresh_focal_statement_units']==67
 additions=read('analysis/candidate_additions.json');inventory=read('analysis/candidate_inventory_corrected.json')
 assert len(additions)==summary['candidate_additions']==16
 assert len(inventory)==len({c['candidate_id'] for c in inventory})==summary['corrected_inventory_candidates']==500
 assert result['statement_units']==summary['corrected_projection_statement_units']==64
 assert len(read('analysis/structural_flag_review.json')['flags'])==len(result['review_flags'])
 quality=read('analysis/report_quality_check.json')
 assert sha(P/'report'/quality['document'])==quality['report_sha256']
if (P/'manifest.json').exists():
 for item in read('manifest.json')['files']:
  f=P/item['path'];assert f.is_file() and f.stat().st_size==item['size_bytes'] and sha(f)==item['sha256'],item['path']
print(json.dumps({'status':'pass','focal_records':24,'reviews':results,'semantic_accuracy':'not estimated','human_validation':'not performed'},indent=2))
