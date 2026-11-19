"""Compatibility and metadata safety checks, not a prospective coding evaluation."""
from pathlib import Path
import copy, hashlib, importlib.util, json, tempfile, zipfile
from check_annotation import check, profile
from normalize_packet_metadata import normalize, encoded

ROOT=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def unzip(p,out):
    with zipfile.ZipFile(p) as z:
        if any(Path(n).is_absolute() or '..' in Path(n).parts for n in z.namelist()):raise ValueError('Unsafe archive path')
        z.extractall(out)
def without_descriptions(x):
    if isinstance(x,dict):return {k:without_descriptions(v) for k,v in x.items() if k!='description'}
    if isinstance(x,list):return [without_descriptions(v) for v in x]
    return x
def run():
    tests=[];annotations=[]
    def require(value,name):tests.append({'name':name,'pass':bool(value)})
    base={'documentary_support':[],'recognition':[],'application_evidence':[]}
    def event(**kw):
        e={'kind':'expectation_recognition','target':'this_proposition','speaker_relation':'different_actor','mode':'explicit_expectation','basis':'explicit','independence_key':'episode_1'};e.update(kw);return e
    fixtures=[('empty',[],'none'),
        ('generic same-actor response',[event(kind='response',speaker_relation='same_actor',mode='same_actor_restatement')],'none'),
        ('focal same-actor expectation',[event(speaker_relation='same_actor',mode='same_actor_restatement')],'same_actor_only'),
        ('broader expectation',[event(target='broader_principle')],'none'),
        ('ordinary endorsement',[event(kind='endorsement',mode='ordinary_assent')],'none'),
        ('ambiguous focal recognition',[event(basis='unresolved')],'unresolved'),
        ('one qualifying actor',[event()],'interpersonal'),
        ('duplicate episode',[event(),event()],'interpersonal'),
        ('two distinct episodes',[event(),event(independence_key='episode_2')],'repeated_interpersonal'),
        ('interpersonal precedence',[event(speaker_relation='same_actor'),event()],'interpersonal'),
        ('same-actor unresolved basis stays visible',[event(speaker_relation='same_actor',basis='unresolved')],'same_actor_only')]
    for name,events,expected in fixtures:
        inst=copy.deepcopy(base);inst['recognition']=events
        require(profile(inst)['recognition']==expected,'projection '+name)
    require(profile(base,'context')['recognition']=='not_applicable','nonstatement projection')
    with tempfile.TemporaryDirectory() as td:
        td=Path(td);unzip(ROOT/'evidence/specification_v0.4.zip',td/'old')
        old=next((td/'old').rglob('protocol/codebook.txt')).parents[1]
        require(digest(old/'tools/check_annotation.py')==digest(ROOT/'tools/check_annotation.py'),'checker byte-identical to evaluated v0.4')
        require(without_descriptions(json.loads((old/'protocol/annotation_schema.json').read_text()))==without_descriptions(json.loads((ROOT/'protocol/annotation_schema.json').read_text())),'schema constraints unchanged; descriptions only')
        for sub in ['baseline_v03','calibration','sources','development','evaluation']:
            for p in (old/sub).rglob('*'):
                if p.is_file():require(digest(p)==digest(ROOT/p.relative_to(old)),'preserved historical '+str(p.relative_to(old)))
        unzip(ROOT/'evidence/reconciliation_v01.zip',td/'recon')
        recon=next((td/'recon').rglob('dataset/reconciled_dataset.json')).parents[1]
        for case in ['F01','F02','F03']:
            p=recon/f'inputs/sources/{case}/packet.json';original=json.loads(p.read_text());adapted,changes=normalize(original)
            expected=(recon/f'dataset/packets/{case}.json').read_bytes()
            require(encoded(adapted)==expected,'adapter reproduces evaluated '+case+' metadata correction')
            require(normalize(adapted)==(adapted,[]),'adapter idempotent '+case)
            require(all(all(new[k]==v for k,v in oldentry.items()) for oldentry,new in zip(original['entries'],adapted['entries'])),'source fields unchanged '+case)
        for p in sorted((recon/'dataset/adjusted_annotations').glob('*.json')):
            a=json.loads(p.read_text());result=check(recon/f"dataset/packets/{a['episode_id']}.json",p)
            require(result['status']=='pass','retained reconciled view '+p.name)
            annotations.append({'path':p.name,'sha256':digest(p),'status':result['status'],'anchors':result.get('exact_anchor_references')})
        example=json.loads((recon/'inputs/sources/F01/packet.json').read_text())
        bad=copy.deepcopy(example);e=next(e for e in bad['entries'] if e.get('revision'));e['revision_id']='conflict'
        try:normalize(bad);rejected=False
        except ValueError:rejected=True
        require(rejected,'conflicting aliases rejected')
        bad=copy.deepcopy(example);e=next(e for e in bad['entries'] if e.get('kind')=='commit_metadata');e['object_id']='https://example.invalid/wrong'
        try:normalize(bad);rejected=False
        except ValueError:rejected=True
        require(rejected,'commit identity mismatch rejected')
        examples=[]
        for name,uid in [('F01_v04_r1.json','S13'),('F01_v04_r2.json','U25')]:
            a=json.loads((recon/'dataset/adjusted_annotations'/name).read_text());u=next(u for u in a['units'] if u['unit_id']==uid)
            examples.append({'origin':'Post-evaluation reconciled interpretation; not an independent reference answer','run':name,'unit':u})
        current=ROOT/'calibration/recognition_projection_examples.json'
        require(json.loads(current.read_text())['examples']==examples,'worked examples match retained reconciled views')
    result=check(ROOT/'calibration/packet.json',ROOT/'calibration/annotation.json')
    require(result['status']=='pass','original calibration passes unchanged checker')
    summary={'release_version':'0.4.1','schema_version':'0.4','status':'pass' if all(t['pass'] for t in tests) else 'fail','passed':sum(t['pass'] for t in tests),'total':len(tests),'scope':'Retained-case compatibility and mechanical safeguards; no fresh coding, transfer validation, or accuracy estimate.','reconciled_views':annotations,'tests':tests}
    (ROOT/'release/compatibility_results.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ['tests','reconciled_views']},indent=2))
    if summary['status']!='pass':raise SystemExit(1)

if __name__=='__main__':run()
