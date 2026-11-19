"""Summarize frozen run counts and first-to-final changes without judging truth."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
rows=[]
for p in sorted((R/'analysis/run_freezes').glob('*.json')):
    f=read(p);rid=f['run_id'];a=read(R/'runs'/rid/'annotation.final.json');first=read(R/'runs'/rid/'annotation.first_complete.json')
    fu={u['unit_id']:u for u in first['units']};au={u['unit_id']:u for u in a['units']}
    rows.append({'run_id':rid,'case':rid[:3],'condition':rid[4:7],
        'units':len(a['units']),'statements':sum(u['record_role']=='statement' for u in a['units']),
        'relations':len(a['relations']),'screened_entries':len(a['entry_screening']),
        'first_check_status':f['independent_mechanical_checks']['first_complete']['status'],
        'first_errors':len(f['independent_mechanical_checks']['first_complete']['errors']),
        'final_check_status':f['independent_mechanical_checks']['final']['status'],
        'final_errors':len(f['independent_mechanical_checks']['final']['errors']),
        'first_final_added_units':len(au.keys()-fu.keys()),'first_final_removed_units':len(fu.keys()-au.keys()),
        'first_final_changed_existing_units':sum(fu[k]!=au[k] for k in fu.keys()&au.keys()),
        'summary_changed':first.get('episode_summary')!=a.get('episode_summary')})
result={'counts_are_run_incidences':True,'runs':rows,'summary':{v:{
    'annotations':sum(z['condition']==v for z in rows),
    'units':sum(z['units'] for z in rows if z['condition']==v),
    'statements':sum(z['statements'] for z in rows if z['condition']==v),
    'initial_passes':sum(z['first_check_status']=='pass' for z in rows if z['condition']==v),
    'final_passes':sum(z['final_check_status']=='pass' for z in rows if z['condition']==v)} for v in ['v03','v04']}}
(R/'analysis/run_descriptives.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result['summary']))
