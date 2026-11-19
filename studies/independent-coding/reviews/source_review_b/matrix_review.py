import json,sys
case,mode=sys.argv[1:3];d=json.load(open(case+'_dossier.json'));p=json.load(open(case+'_packet.json'));pool=d['evidence_pool'];lo=int(sys.argv[3]) if len(sys.argv)>3 else 0;hi=int(sys.argv[4]) if len(sys.argv)>4 else 999
for e in p['entries'][lo:hi]:
 print('\nSOURCE',e['source_id'])
 for a in d['annotations']:
  for u in a['units']:
   if u['source_id']!=e['source_id']:continue
   z=pool[u['span']['evidence_ref']]['span'];i=u['institution'];print(a['annotation_id'],u['unit_id'],f"{z['start']}:{z['end']}",end=' ')
   if mode=='units':
    vals=[u['record_role'],u['grammar'],u['parse_mode'],u['speech_act'],u['scope'],u['deontic_force'],i['type'],i.get('standing',i.get('standing_profile')),i['dispute_present'],u['statement_target_level'],u['observed_action_level'],u['presentation']]
    print(json.dumps(vals,ensure_ascii=False,separators=(',',':')))
    for c in u['components']:print(' ',c['symbol'],c['text'],c['basis'],c['occurrence_role'],[v['evidence_ref'] for v in c['evidence']],c.get('governing_span',{}).get('evidence_ref'))
    if u.get('proposition'):print(' P',json.dumps(u['proposition'],ensure_ascii=False,separators=(',',':')))
   elif mode=='events':
    print(json.dumps({'institution':i,'dispositions':u['disposition_events']},ensure_ascii=False,separators=(',',':')))
   elif mode=='brief':
    print(json.dumps([u['record_role'],u['grammar'],u['parse_mode'],u['speech_act'],u['scope'],u['deontic_force'],i['type'],i.get('standing',i.get('standing_profile')),i['dispute_present'],u['statement_target_level'],u['observed_action_level']],ensure_ascii=False,separators=(',',':')))
    for c in u['components']:print(' ',c['symbol'],c['text'],c['basis'],c['occurrence_role'],[v['evidence_ref'] for v in c['evidence']],c.get('governing_span',{}).get('evidence_ref'))
   elif mode=='notes':
    print(json.dumps({k:v for k,v in u.items() if k in ['level_rationale','level_evidence','alternative_interpretation','uncertainty_reason','complexity_flags','confidence','target_level_alternatives','observed_level_alternatives','level_alternatives','template_note','parent_unit_id']},ensure_ascii=False,separators=(',',':')))
