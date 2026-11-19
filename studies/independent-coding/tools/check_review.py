"""Mechanical coverage and evidence checks for an independent source review.

A passing ledger does not prove the semantic review was correct.
"""
from pathlib import Path
import json,hashlib,sys,datetime
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(name):
    d=R/'reviews'/name
    annotations={a['annotation_id']:a for a in read(d/'annotations.json')}
    packets={eid:read(d/f'{eid}_packet.json') for eid in ['F01','F02','F03']}
    texts={e['source_id']:e['text'] for p in packets.values() for e in p['entries']}
    review=read(d/'review.json');errors=[]
    for filename,h in read(d/'input_manifest.json')['files'].items():
        if sha(d/filename)!=h:errors.append('Input changed: '+filename)
    coverage={c['annotation_id']:c for c in review['coverage']}
    if len(coverage)!=len(review['coverage']) or set(coverage)!=set(annotations):
        errors.append('Coverage must contain each of the 18 annotations exactly once')
    for alias,a in annotations.items():
        c=coverage.get(alias,{})
        expected={u['unit_id'] for u in a['units']}
        actual=c.get('checked_unit_ids',[])
        if set(actual)!=expected or len(actual)!=len(set(actual)):errors.append(alias+' unit coverage')
        entries={e['source_id'] for e in packets[a['episode_id']]['entries']}
        if set(c.get('checked_entry_ids',[]))!=entries:errors.append(alias+' entry coverage')
        if c.get('checked_relations') is not True:errors.append(alias+' relation coverage')
        if c.get('checked_summary') is not True:errors.append(alias+' summary coverage')
        if not set(c.get('no_error_identified_ids',[]))<=expected:errors.append(alias+' invalid no-error units')
    ids=[]
    for f in review['findings']:
        fid=f['finding_id'];ids.append(fid)
        if f['diagnosis'] not in ['criterion_ambiguity','execution_failure','defensible_alternative','unresolved']:errors.append(fid+' diagnosis')
        if f['effect'] not in ['interpretation_changing','evidence_basis','convention_only','coverage_or_scope','unresolved']:errors.append(fid+' effect')
        if not f.get('source_evidence'):errors.append(fid+' missing source evidence')
        for e in f.get('source_evidence',[]):
            t=texts.get(e.get('source_id'));s=e.get('span',{})
            if t is None or not isinstance(s.get('start'),int) or not isinstance(s.get('end'),int) or not 0<=s['start']<s['end']<=len(t) or t[s['start']:s['end']]!=s.get('quote'):
                errors.append(fid+' source anchor')
        for affected in f['affected']:
            alias=affected['annotation_id']
            if alias not in annotations:errors.append(fid+' invalid annotation');continue
            if annotations[alias]['episode_id']!=f['episode_id']:errors.append(fid+' case mismatch')
            us={u['unit_id'] for u in annotations[alias]['units']}
            if not set(affected.get('unit_ids',[]))<=us:errors.append(fid+' invalid units '+alias)
    if len(ids)!=len(set(ids)):errors.append('Duplicate finding IDs')
    result={'review':name,'status':'fail' if errors else 'pass','errors':errors,'annotations':len(coverage),'findings':len(ids),'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'limitation':'Mechanical ledger validation only; not a truth test.'}
    (d/'coverage_check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main(sys.argv[1])
