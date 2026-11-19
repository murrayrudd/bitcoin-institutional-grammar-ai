"""Create descriptive source/overlap indexes; human-readable adjudication remains separate."""
from pathlib import Path
import json, csv, sys
P=Path(__file__).resolve().parents[1]
B=json.loads((P/'sources/baseline_annotations.json').read_text())
C=json.loads((P/'sources/baseline_candidate_passages.json').read_text())
S=json.loads((P/'sources/baseline_screening_judgments.json').read_text())
sample=json.loads((P/'protocol/selected_sample.json').read_text())
def overlap(a,b): return max(0,min(a['end'],b['end'])-max(a['start'],b['start']))
def compact(u):
 return {k:u[k] for k in ['unit_id','source_id','record_role','span','grammar','speech_act','scope','parse_mode','deontic_force','statement_target_level','observed_action_level','level_alternatives','alternative_interpretation']} | {
  'components':[{k:c[k] for k in ['symbol','text','basis','occurrence_role','inference_note']} for c in u['components']],
  'institution':u['institution'],'disposition_events':u['disposition_events']}
reviews={g:json.loads((P/'reviewer_outputs'/g/'annotation.json').read_text()) for g in ['A','B','C']}
suffix=''
if '--supplemented' in sys.argv:
 reviews['C']=json.loads((P/'reviewer_outputs/C/supplement/annotation.supplemented.json').read_text())
 suffix='_supplemented'
entries=[];pairs=[]
for x in sample:
 sid=x['source_id'];g=x['reviewer_group'];a=reviews[g]
 baseline=[u for u in B['units'] if u['source_id']==sid and u['record_role']=='statement']
 fresh=[u for u in a['units'] if u['source_id']==sid and u['record_role']=='statement']
 candidates=[c for c in C if c['source_id']==sid]
 screen=next(s for s in a['entry_screening'] if s['source_id']==sid)
 entries.append(x|{'baseline_screen':S[sid],'baseline_candidates':candidates,
   'baseline_statements':[compact(u) for u in baseline],
   'review_screen':screen,'review_statements':[compact(u) for u in fresh],
   'review_nonstatements':[compact(u) for u in a['units'] if u['source_id']==sid and u['record_role']!='statement']})
 for u in baseline:
  hits=[v for v in fresh if overlap(u['span'],v['span'])]
  pairs.append({'baseline_unit_id':u['unit_id'],'source_id':sid,'review_group':g,
    'baseline':compact(u),'overlapping_review_units':[compact(v) for v in hits],
    'warning':'Literal overlap is an index for source review, not semantic agreement.'})
(P/f'analysis/source_comparison_index{suffix}.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
(P/f'analysis/baseline_unit_comparison_index{suffix}.json').write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')
with (P/f'analysis/sample_coverage{suffix}.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['source_id','stratum','review_group','baseline_screen_class','baseline_candidate_passages','baseline_statement_units','fresh_screen_disposition','fresh_statement_units'])
 for e in entries:w.writerow([e['source_id'],e['stratum'],e['reviewer_group'],e['baseline_screen']['screen_class'],len(e['baseline_candidates']),len(e['baseline_statements']),e['review_screen']['disposition'],len(e['review_statements'])])
print(json.dumps({'focal_sources':len(entries),'baseline_statement_units':len(pairs),
 'fresh_focal_statement_units':sum(len(e['review_statements']) for e in entries),
 'fresh_candidate_sources':sum(e['review_screen']['disposition']=='candidate' for e in entries)},indent=2))
