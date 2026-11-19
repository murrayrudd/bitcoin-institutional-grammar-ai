"""Verify provenance, annotation immutability, alignment coverage, and audit anchors."""
from pathlib import Path
import json, hashlib
from zipfile import ZipFile
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
def read(path): return json.loads(path.read_text())
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    checks=[]
    for name in ['frozen_inputs','analysis_plan_freeze']:
        data=read(ROOT/f'protocol/{name}.json')
        for p,h in data['files'].items():
            assert digest(ROOT/p)==h, (name,p,'file changed')
            checks.append({'kind':'unchanged_file','file':p})
    comparison=read(ROOT/'protocol/comparison_script_freeze.json')
    assert digest(ROOT/comparison['path'])==comparison['sha256'], 'Comparison script changed'
    checks.append({'kind':'unchanged_comparison_script','file':comparison['path']})
    for entry in read(ROOT/'protocol/input_archive_manifest.json'):
        assert digest(ROOT/entry['file'])==entry['sha256'], ('Archive changed',entry['file'])
        checks.append({'kind':'unchanged_prior_archive','file':entry['file']})
    archive=ROOT/'prior_inputs/archives/Core_Knots_Round11_Comparative_Model_Evidence_v01.zip'
    with ZipFile(archive) as z:
        for p in (ROOT/'prior_inputs/round11').glob('*.json'):
            names=[n for n in z.namelist() if n.endswith('/analysis/'+p.name)]
            assert len(names)==1, ('Ambiguous prior archive member',p.name)
            assert p.read_bytes()==z.read(names[0]), ('Copied prior data differ',p.name)
            checks.append({'kind':'prior_copy_matches_archive','file':str(p.relative_to(ROOT))})
    data=read(ROOT/'protocol/frozen_outputs.json')
    for label,info in data['reviewers'].items():
        for p,h in info['files'].items():
            assert digest(ROOT/p)==h, (label,p,'frozen output changed')
            checks.append({'kind':'unchanged_coder_file','file':p})
        assert info['checker_status']=='pass', (label,'mechanical checker did not pass')
    packet=read(ROOT/'common_input/packet.json')
    texts={e['source_id']:e['text'] for e in packet['entries']}
    focal=set(packet['selection_design']['focal_source_ids'])
    stats=read(ROOT/'analysis/overlap_metrics.json')
    assert stats['source_records']==24
    assert not any(stats['semantic_alignment']['unassigned_focal_statements'].values())
    anchors=0
    def walk(obj,path):
        nonlocal anchors
        if isinstance(obj,dict):
            if 'source_id' in obj:
                sp=obj.get('span',obj)
                if all(k in sp for k in ['start','end','quote']):
                    sid=obj['source_id']
                    assert sid in texts, (path,'unknown evidence source',sid)
                    assert 0<=sp['start']<sp['end']<=len(texts[sid]), (path,'invalid offset')
                    assert texts[sid][sp['start']:sp['end']]==sp['quote'], (path,'quote mismatch',sid)
                    anchors+=1
            for k,v in obj.items(): walk(v,path+'/'+k)
        elif isinstance(obj,list):
            for i,v in enumerate(obj): walk(v,path+f'/{i}')
    for name in ['independent_source_audit.json','source_reconciliation.json','baseline_impact.json']:
        path=ROOT/'analysis'/name
        assert path.exists(), ('Missing final analytical record',name)
        walk(read(path),name)
    audit=read(ROOT/'analysis/independent_source_audit.json')
    assert set(audit['reviewed_source_ids'])==focal, 'Audit focal coverage incomplete'
    rec=read(ROOT/'analysis/source_reconciliation.json')
    assert rec['independent_audit_sha256']==digest(ROOT/'analysis/independent_source_audit.json')
    assert {x['audit_finding_id'] for x in rec['decisions']}=={x['finding_id'] for x in audit['findings']}
    assert len(rec['decisions'])==len(audit['findings']), 'Reconciliation coverage differs'
    ar=read(ROOT/'analysis/alignment_review.json')
    assert ar['proposed_sha256']==digest(ROOT/'analysis/semantic_alignment.proposed.json')
    assert ar['final_sha256']==digest(ROOT/'analysis/semantic_alignment.json')
    out={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'status':'pass',
         'unchanged_file_checks':len(checks),'analytical_evidence_anchors':anchors,
         'focal_source_count':len(focal),'alignment_coverage':'all focal statements assigned',
         'limitations':'Mechanical integrity only; source reconciliation remains revisable AI judgment.',
         'checks':checks}
    (ROOT/'analysis/package_verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))

if __name__=='__main__': main()
