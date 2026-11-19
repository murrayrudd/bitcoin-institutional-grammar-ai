import json,sys
from alignment_helpers import load
EP,AID=sys.argv[1:3]; start=int(sys.argv[3]) if len(sys.argv)>3 else 0; end=int(sys.argv[4]) if len(sys.argv)>4 else 10000
d=load(EP+'_dossier.json');a=next(x for x in d['annotations'] if x['annotation_id']==AID)
print('ANNOTATION',AID,a['note'])
print('component format: symbol | text | basis / occurrence | evidence refs; governing ref | inference note')
for u in a['units'][start:end]:
 e=d['evidence_pool'][u['span']['evidence_ref']];z=e['span'];print('\nUNIT',u['unit_id'],u['source_id'],f"{z['start']}:{z['end']}",repr(z['quote']),'parent',u['parent_unit_id'],'role',u['record_role'],'parse',u['parse_mode'])
 for c in u['components']:
  print(c['symbol'],'|',c['text'],'|',c['basis'],'/',c.get('occurrence_role'),'|',','.join(x['evidence_ref'] for x in c.get('evidence',[])),'gov',c.get('governing_span',{}).get('evidence_ref'),'|',c.get('inference_note',''))
  extra={k:v for k,v in c.items() if k not in ['symbol','text','basis','occurrence_role','evidence','governing_span','inference_note']}
  if extra:print('EXTRA',extra)
 print('ALT',u.get('alternative_interpretation'))
 if 'proposition' in u:
  p=u['proposition'];print('PROP',p['summary']); print('IDENTITY',p['decision_object_id'],'DOMAIN',p['domain'],'TIME',p['time_scope'],'REF',p['identity_evidence'])
  for q in p['qualifiers']:print('QUAL',q['attachment'],q['linked_unit_id'],q['evidence'],q['description'],'RATIONALE',q['rationale'])
 extras={k:v for k,v in u.items() if k not in ['unit_id','source_id','span','parent_unit_id','record_role','parse_mode','components','alternative_interpretation','proposition']}
 if extras: print('EXTRA',extras)
if end>=len(a['units']):
 for i,l in enumerate(a['links']):print('LINK',i,json.dumps(l,ensure_ascii=False,separators=(',',':')))
