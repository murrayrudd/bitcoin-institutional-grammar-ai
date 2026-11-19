"""Recompute descriptive overlap statistics from frozen annotations and reviewed alignment."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json, hashlib

ROOT = Path(__file__).resolve().parents[1]
LABELS = ['A', 'B', 'C']
FIELDS = ['grammar', 'deontic_force', 'institution.type', 'institution.standing',
          'institution.dispute_present', 'statement_target_level', 'observed_action_level']

def read(p):
    return json.loads(p.read_text())

def field(unit, name):
    value = unit
    for key in name.split('.'):
        value = value[key]
    return value

def summarize_values(values):
    return {'agree': len(set(map(str, values))) == 1, 'values': values}

def main():
    packet = read(ROOT/'common_input/packet.json')
    focal = packet['selection_design']['focal_source_ids']
    annotations = {l: read(ROOT/f'reviewers/{l}/annotation.json') for l in LABELS}
    lookup = {l: {u['unit_id']:u for u in a['units']} for l,a in annotations.items()}
    statements = {l:[u for u in a['units'] if u['record_role']=='statement' and u['source_id'] in focal]
                  for l,a in annotations.items()}
    screen = {l:{s['source_id']:s['disposition'] for s in a['entry_screening']} for l,a in annotations.items()}
    screen_rows = [{'source_id':sid, 'values':{l:screen[l][sid] for l in LABELS},
                    'unanimous':len({screen[l][sid] for l in LABELS})==1} for sid in focal]
    exact = {l:{(u['source_id'],u['span']['start'],u['span']['end']):u for u in us}
             for l,us in statements.items()}
    # Duplicate exact spans cannot be silently collapsed into an agreement score.
    for l in LABELS:
        assert len(exact[l])==len(statements[l]), (l,'duplicate focal statement span')
    out = {'packet_sha256':hashlib.sha256((ROOT/'common_input/packet.json').read_bytes()).hexdigest(),
           'source_records':len(focal), 'focal_statement_counts':{l:len(v) for l,v in statements.items()},
           'unit_role_counts':{l:dict(Counter(u['record_role'] for u in a['units'])) for l,a in annotations.items()},
           'screening':{'rows':screen_rows,'unanimous_count':sum(r['unanimous'] for r in screen_rows),
                        'denominator':len(focal),'pairs':{}},
           'exact_span':{'pairs':{},'three_way_count':len(set(exact['A'])&set(exact['B'])&set(exact['C']))}}
    for a,b in combinations(LABELS,2):
        k=a+b
        out['screening']['pairs'][k]={'agree':sum(screen[a][s]==screen[b][s] for s in focal),'total':len(focal)}
        matched=set(exact[a])&set(exact[b])
        out['exact_span']['pairs'][k]={'matched':len(matched),'unmatched_'+a:len(exact[a])-len(matched),
                                     'unmatched_'+b:len(exact[b])-len(matched),
                                     'fields':{f:{'agree':sum(field(exact[a][x],f)==field(exact[b][x],f) for x in matched),
                                                  'total':len(matched)} for f in FIELDS}}
    alignment_path=ROOT/'analysis/semantic_alignment.json'
    if alignment_path.exists():
        alignment=read(alignment_path)
        groups=alignment['groups'] if isinstance(alignment,dict) else alignment
        used={l:[] for l in LABELS}
        valid=[]
        for g in groups:
            for l in LABELS:
                ids=g['units'].get(l,[])
                for uid in ids:
                    assert uid in lookup[l],(g['group_id'],l,uid)
                    assert lookup[l][uid]['source_id']==g['source_id'],(g['group_id'],l,uid)
                    used[l].append(uid)
            if g['alignment_type']=='one_to_one' and all(len(g['units'].get(l,[]))==1 for l in LABELS):
                us={l:lookup[l][g['units'][l][0]] for l in LABELS}
                if all(u['record_role']=='statement' for u in us.values()): valid.append((g,us))
        for l in LABELS:
            assert len(used[l])==len(set(used[l])),(l,'unit reused across alignment groups')
        missing={l:[u['unit_id'] for u in statements[l] if u['unit_id'] not in used[l]] for l in LABELS}
        rows=[]
        for g,us in valid:
            row={'group_id':g['group_id'],'source_id':g['source_id'],'meaning':g['meaning'],
                 'fields':{f:{'values':{l:field(us[l],f) for l in LABELS},
                              'unanimous':len({str(field(us[l],f)) for l in LABELS})==1} for f in FIELDS}}
            row['all_fields_unanimous']=all(x['unanimous'] for x in row['fields'].values())
            rows.append(row)
        out['semantic_alignment']={'groups':len(groups),'alignment_types':dict(Counter(g['alignment_type'] for g in groups)),
            'unassigned_focal_statements':missing,'one_to_one_triple_denominator':len(valid),
            'all_fields_unanimous':sum(r['all_fields_unanimous'] for r in rows),
            'fields':{f:{'unanimous':sum(r['fields'][f]['unanimous'] for r in rows),'total':len(rows),
                         'pairs':{a+b:{'agree':sum(field(us[a],f)==field(us[b],f) for _,us in valid),'total':len(valid)}
                                  for a,b in combinations(LABELS,2)}} for f in FIELDS},
            'rows':rows}
    (ROOT/'analysis/overlap_metrics.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['screening','exact_span','semantic_alignment']},indent=2))
    print('Screening unanimous',out['screening']['unanimous_count'],'/',len(focal))
    print('Exact triples',out['exact_span']['three_way_count'])
    if 'semantic_alignment' in out:
        sm=out['semantic_alignment']
        print('Semantic one-to-one triples',sm['one_to_one_triple_denominator'])
        print(json.dumps(sm['fields'],indent=2))

if __name__=='__main__':main()
