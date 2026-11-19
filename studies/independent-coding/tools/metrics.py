"""Descriptive pre-reconciliation agreement. Requires frozen semantic alignment.
No agreement score certifies source validity. Split and unmatched coverage is retained.
"""
from pathlib import Path
from collections import Counter,defaultdict
import json
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def value(u,field):
 if field=='institutional_type':return u['institution']['type']
 if field=='dispute_present':return u['institution']['dispute_present']
 return u[field]
FIELDS=['grammar','deontic_force','institutional_type','statement_target_level','observed_action_level','dispute_present']
def main():
 masks=read(R/'analysis/mask_key.json');reverse={v:k for k,v in masks.items()};runs={rid:read(R/'runs'/rid/'annotation.final.json') for rid in masks};units={masks[rid]:{u['unit_id']:u for u in a['units']} for rid,a in runs.items()}
 groups=read(R/'reviews/alignment/alignment.json')['groups'];seen=Counter();issues=[]
 for g in groups:
  for alias,ids in g['members'].items():
   for uid in ids:
    seen[(alias,uid)]+=1
    if alias not in units or uid not in units[alias] or units[alias][uid]['record_role']!='statement':issues.append('Invalid '+alias+':'+uid)
 expected={(a,u) for a,us in units.items() for u,v in us.items() if v['record_role']=='statement'}
 if set(seen)!=expected or any(v!=1 for v in seen.values()):raise RuntimeError({'missing':sorted(expected-set(seen)),'extra':sorted(set(seen)-expected),'duplicates':[x for x,v in seen.items() if v!=1]})
 if issues:raise RuntimeError(issues)
 output={'interpretation':'Descriptive agreement conditional on one-to-one semantic matches, before source reconciliation. Not accuracy. Repeated units and three episodes are not independent population observations.','masking':'Version/run identities and direct classification labels withheld from aligner; components and explicit proposition summaries can reveal conventions.','fields':FIELDS,'cases':[],'runs':[]}
 for rid,a in runs.items():
  first=read(R/'runs'/rid/'annotation.first_complete.json');old={u['unit_id']:u for u in first['units']};new={u['unit_id']:u for u in a['units']};f=read(R/'analysis/run_freezes'/f'{rid}.json')
  output['runs'].append({'run_id':rid,'statement_units':sum(u['record_role']=='statement' for u in a['units']),'all_units':len(a['units']),'first_units':len(first['units']),'first_check_status':f['independent_mechanical_checks']['first_complete'].get('status'),'final_check_status':f['independent_mechanical_checks']['final'].get('status'),'added_unit_ids':sorted(new.keys()-old.keys()),'removed_unit_ids':sorted(old.keys()-new.keys()),'changed_existing_unit_ids':[u for u in old.keys()&new.keys() if old[u]!=new[u]],'first_final_identical':a==first})
 for eid in ['F01','F02','F03']:
  packet=read(R/'sources'/eid/'packet.json');focal=packet['selection_design']['focal_source_ids'];casegroups=[g for g in groups if g['episode_id']==eid];case={'episode_id':eid,'alignment_groups':len(casegroups),'group_statuses':dict(Counter(g['status'] for g in casegroups)),'conditions':[]}
  common_all_six=[]
  allrids=[rid for rid in runs if rid.startswith(eid+'_')]
  for g in casegroups:
   if g['status'] not in ['unresolved','split_combined'] and all(len(g['members'].get(masks[rid],[]))==1 for rid in allrids):common_all_six.append(g['group_id'])
  case['common_all_six_group_ids']=common_all_six
  for ver in ['v03','v04']:
   ids=sorted(rid for rid in allrids if '_'+ver+'_' in rid);aliases=[masks[rid] for rid in ids]
   screens=[{s['source_id']:s['disposition'] for s in runs[rid]['entry_screening']} for rid in ids]
   screen_agree=sum(len({s[sid] for s in screens})==1 for sid in focal)
   keys=[]
   for rid in ids:
    by=defaultdict(list)
    for u in runs[rid]['units']:
     if u['record_role']=='statement':by[(u['source_id'],u['span']['start'],u['span']['end'])].append(u['unit_id'])
    keys.append(by)
   exact=set(keys[0])&set(keys[1])&set(keys[2]);exact={k for k in exact if all(len(t[k])==1 for t in keys)}
   matched=[];excluded=[]
   for g in casegroups:
    members={a:g['members'].get(a,[]) for a in aliases};touched=any(members.values())
    if g['status']!='unresolved' and all(len(members[a])==1 for a in aliases):
     matched.append((g,[units[a][members[a][0]] for a in aliases]))
    elif touched:excluded.append({'group_id':g['group_id'],'status':g['status'],'member_counts':{a:len(v) for a,v in members.items()}})
   scores={f:sum(len({json.dumps(value(u,f),sort_keys=True) for u in us})==1 for g,us in matched) for f in FIELDS}
   common=[(g,us) for g,us in matched if g['group_id'] in common_all_six]
   common_scores={f:sum(len({json.dumps(value(u,f),sort_keys=True) for u in us})==1 for g,us in common) for f in FIELDS}
   case['conditions'].append({'condition':ver,'runs':ids,'focal_screening_unanimous':screen_agree,'focal_screening_denominator':len(focal),'statement_counts':[sum(u['record_role']=='statement' for u in runs[rid]['units']) for rid in ids],'exact_span_triple_matches':len(exact),'semantic_triple_matches':len(matched),'semantic_group_ids':[g['group_id'] for g,us in matched],'excluded_groups':excluded,'field_unanimous':scores,'field_denominator':len(matched),'all_six_fields_unanimous':sum(all(len({json.dumps(value(u,f),sort_keys=True) for u in us})==1 for f in FIELDS) for g,us in matched),'common_all_six_field_denominator':len(common),'common_all_six_field_unanimous':common_scores})
  output['cases'].append(case)
 write(R/'analysis/overlap_metrics.json',output)
 print(json.dumps(output,indent=2))
if __name__=='__main__':main()
