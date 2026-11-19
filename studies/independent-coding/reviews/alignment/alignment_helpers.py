import json, hashlib, pathlib, datetime, collections
ROOT=pathlib.Path(__file__).resolve().parent

def load(name):
    return json.loads((ROOT/name).read_text())

def write_json(name,obj):
    (ROOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def assemble_case(ep,specs,notes):
    d=load(ep+'_dossier.json'); p=load(ep+'_packet.json')
    units={(a['annotation_id'],u['unit_id']):u for a in d['annotations'] for u in a['units']}
    used=[]; groups=[]
    for i,s in enumerate(specs,1):
        g={'group_id':f'{ep}-G{i:03d}','episode_id':ep,**s}
        g['source_evidence']=[d['evidence_pool'][q] for q in g.pop('evidence_refs')]
        ms=[]
        for a,ids in g['members'].items():
            for uid in ids:
                used.append((a,uid));u=units[(a,uid)]
                ms.append({'annotation_id':a,'unit_id':uid,**d['evidence_pool'][u['span']['evidence_ref']]})
        g['selected_spans']=ms
        g['exact_span_result']={'comparison':'source_id/start/end/quote of focal unit span; separate from semantic correspondence', 'all_member_spans_identical':len(ms)>1 and len({(m['source_id'],m['span']['start'],m['span']['end'],m['span']['quote']) for m in ms})==1,'not_applicable':len(ms)==1}
        groups.append(g)
    assert len(used)==len(set(used)), 'Duplicate assignments'
    assert set(used)==set(units),('Missing',set(units)-set(used),'extra',set(used)-set(units))
    src={e['source_id']:e['text'] for e in p['entries']}
    for g in groups:
        for e in g['source_evidence']+g['selected_spans']:
            x=e['span'];assert src[e['source_id']][x['start']:x['end']]==x['quote']
    coverage=[]
    for a in d['annotations']:
        coverage.append({'annotation_id':a['annotation_id'],'checked_unit_ids':[u['unit_id'] for u in a['units']],'assigned_count':len(a['units']),'checked_packet_entry_ids':[e['source_id'] for e in p['entries']],'checked_links_for_alignment':True,'unit_propositions_and_explicit_qualifier_links_checked':True,'limits':['Masked semantic alignment only; no classification-label agreement or source-review correctness rating.']})
    obj={'episode_id':ep,'groups':groups,'coverage':coverage,'notes':notes,'counts':{'groups':len(groups),'units':len(used),'status_counts':dict(collections.Counter(g['status'] for g in groups))},'first_complete_case_saved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    assert not (ROOT/(ep+'_alignment.first_complete.json')).exists()
    write_json(ep+'_alignment.first_complete.json',obj);write_json(ep+'_alignment.json',obj)
    return obj['counts']
