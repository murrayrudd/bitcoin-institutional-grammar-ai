import json,hashlib,datetime,re
from pathlib import Path
P=Path('.');now=datetime.datetime.now(datetime.timezone.utc).isoformat()
cases={ep:json.loads(P.joinpath(ep+'_review.json').read_text()) for ep in ['F01','F02','F03']}
review={'reviewer':'source_review_a','status':'complete','completed_at_utc':now,'findings':sorted([f for c in cases.values() for f in c['findings']],key=lambda x:x['finding_id']),'coverage':sorted([x for c in cases.values() for x in c['coverage']],key=lambda x:x['annotation_id']),'checked_claims_with_no_identified_error':{ep:c['checked_claims_with_no_identified_error'] for ep,c in cases.items()},'new_criterion_candidates':{ep:c.get('new_criterion_candidates',[]) for ep,c in cases.items()},'limits':['This independent review is revisable AI judgment, not a reference truth set. Findings count bounded issues, not independent observations or a quality score.','All findings use each annotation\'s assigned guide. Version masking is incomplete because guides and schemas differ. No condition identities, agreement statistics, other review content or external research were accessed.','The frozen source packets bound factual conclusions. Missing edit/reply histories, exact intermediate changes, referenced-PR outcomes and unobserved actions remain missing; no external facts were supplied.','All 18 annotations, 587 retained units, 327 relations and 83 distinct packet entries were semantically inspected. Exact-anchor validation is separate from that semantic review.','No confirmed interpretation-changing execution failure was identified. Evidence-basis errors, convention deviations, criterion ambiguities, defensible alternatives and unresolved findings are kept distinct.'], 'coverage_totals':{'annotations':18,'retained_units':587,'relations':327,'distinct_packet_entries':83},'case_first_complete_files':{ep:ep+'_review.first_complete.json' for ep in cases},'prior_case_corrections':'corrections_record.json'}
raw=json.dumps(review,ensure_ascii=False,indent=2)+'\n';P.joinpath('review.json').write_text(raw)
if not P.joinpath('review.first_complete.json').exists():P.joinpath('review.first_complete.json').write_text(raw)
packets={ep:json.loads(P.joinpath(ep+'_packet.json').read_text()) for ep in cases}
dossiers={ep:json.loads(P.joinpath(ep+'_dossier.json').read_text()) for ep in cases}
ledger={'status':'complete','reviewer':'source_review_a','coverage':review['coverage'],'case_source_entries':{ep:[{'source_id':e['source_id'],'checked_in_full':True,'scope':'Focal entries checked for every material candidate and contextual claim; supplemental metadata, guidance and patches checked as contextual evidence and for relevant omissions without inventing a new exhaustive extraction target.'} for e in p['entries']] for ep,p in packets.items()},'case_totals':{ep:{'annotations':len(dossiers[ep]['annotations']),'retained_units':sum(len(a['units']) for a in dossiers[ep]['annotations']),'relations':sum(len(a['relations']) for a in dossiers[ep]['annotations']),'packet_entries':len(packets[ep]['entries'])} for ep in cases},'method':'Sequential semantic reading in bounded case/annotation/unit/field batches; repeated values only compressed through exact earlier-occurrence references. Full sources and assigned guides read. Incremental case and annotation checkpoints preserved. Unanimous-looking claims checked directly against sources, without voting.','limits':review['limits']}
P.joinpath('coverage_ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
if not P.joinpath('coverage_ledger.first_complete.json').exists():P.joinpath('coverage_ledger.first_complete.json').write_text(P.joinpath('coverage_ledger.json').read_text())
# Mechanical validation follows preservation of the first complete submission.
errors=[];annotations={a['annotation_id']:(ep,a) for ep,d in dossiers.items() for a in d['annotations']}
def getpath(o,path):
 for key,num in re.findall(r'([A-Za-z_][A-Za-z_0-9]*)|\[(\d+)\]',path):o=o[key] if key else o[int(num)]
 return o
for f in review['findings']:
 ep=f['episode_id'];src={e['source_id']:e['text'] for e in packets[ep]['entries']}
 for e in f['source_evidence']:
  s=e['span']
  if e['source_id'] not in src or src[e['source_id']][s['start']:s['end']]!=s['quote']:errors.append([f['finding_id'],'anchor mismatch',e['source_id']])
 for af in f['affected']:
  ae,a=annotations[af['annotation_id']]
  if ae!=ep:errors.append([f['finding_id'],'case mismatch',af['annotation_id']])
  for uid in af['unit_ids']:
   if uid not in {u['unit_id'] for u in a['units']}:errors.append([f['finding_id'],'unknown unit',af['annotation_id'],uid])
  for path in af['relation_ids']+af['summary_paths']:
   try:getpath(a,path)
   except Exception:errors.append([f['finding_id'],'unknown path',af['annotation_id'],path])
for c in review['coverage']:
 ep,a=annotations[c['annotation_id']]
 if c['checked_unit_ids']!=[u['unit_id'] for u in a['units']]:errors.append(['coverage units',c['annotation_id']])
 if c['checked_entry_ids']!=[e['source_id'] for e in packets[ep]['entries']]:errors.append(['coverage entries',c['annotation_id']])
 if c['checked_relation_ids']!=[f'relations[{i}]' for i in range(len(a['relations']))]:errors.append(['coverage relations',c['annotation_id']])
 if not set(c['no_error_identified_ids'])<=set(c['checked_unit_ids']):errors.append(['no-error membership',c['annotation_id']])
anchor_total=0
for ep,d in dossiers.items():
 src={e['source_id']:e['text'] for e in packets[ep]['entries']}
 for q,e in d['evidence_pool'].items():
  anchor_total+=1;s=e['span']
  if src[e['source_id']][s['start']:s['end']]!=s['quote']:errors.append([ep,'pool anchor mismatch',q])
validation={'validated_at_utc':now,'errors':errors,'evidence_pool_anchors_checked':anchor_total,'findings':len(review['findings']),'coverage_rows':len(review['coverage']),'role':'Mechanical checks after semantic review; not a replacement for reading.'}
P.joinpath('validation_record.json').write_text(json.dumps(validation,indent=2)+'\n')
print(json.dumps(validation,indent=2))
