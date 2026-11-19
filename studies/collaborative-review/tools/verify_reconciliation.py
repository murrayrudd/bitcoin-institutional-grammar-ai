from pathlib import Path
import json,hashlib,copy,datetime
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
passed=[]
def check(condition,label):
    assert condition,label
    passed.append(label)
for row in read(R/'inputs_manifest.json'):check(sha(R/row['path'])==row['sha256'],'frozen input '+row['path'])
for name in ['initial_freeze','final_freeze']:
    for row in read(R/f'panel/{name}.json')['files']:check(sha(R/row['path'])==row['sha256'],name+' '+row['reviewer'])
for row in read(R/'analysis/panel_input_manifest.json')['files']:check(sha(R/row['path'])==row['sha256'],'frozen panel input '+row['path'])
for a in 'ABC':
    for stage in ['initial','final']:
        d=read(R/f'panel/{a}_{stage}.json');check({t['topic_id'] for t in d['topics']}=={f'D{i:02}' for i in range(1,11)},a+' '+stage+' covers ten topics')
    d=read(R/f'panel/{a}_final.json');check(all(t['peer_response'] for t in d['topics']),a+' has explicit peer responses')
old={p.parent.name:read(p) for p in (R/'inputs/runs').glob('*/annotation.final.json')};replayed=copy.deepcopy(old)
def locate(o,path):
    ts=[t.replace('~1','/').replace('~0','~') for t in path.lstrip('/').split('/')]
    for t in ts[:-1]:o=o[int(t)] if isinstance(o,list) else o[t]
    k=int(ts[-1]) if isinstance(o,list) else ts[-1]
    return o,k
changes=read(R/'analysis/change_log.json')
for c in changes:
    o,k=locate(replayed[c['run_id']],c['path']);check(o[k]==c['before'],'change before '+c['change_id']);o[k]=c['after']
for rid,d in replayed.items():
    folder='adjusted_annotations' if '_v04_' in rid else 'reference_only_v03'
    check(d==read(R/f'dataset/{folder}/{rid}.json'),'change replay '+rid)
texts={}
for case in ['F01','F02','F03']:
    p=read(R/f'inputs/sources/{case}/packet.json');q=read(R/f'dataset/packets/{case}.json')
    check([(e['source_id'],e['text']) for e in p['entries']]==[(e['source_id'],e['text']) for e in q['entries']],'source text unchanged '+case)
    texts.update({e['source_id']:e['text'] for e in p['entries']})
anchor_count=0
def anchors(x):
    global anchor_count
    if isinstance(x,dict):
        if 'source_id' in x and isinstance(x.get('span'),dict) and 'quote' in x['span']:
            s=x['span'];check(texts[x['source_id']][s['start']:s['end']]==s['quote'],'anchor '+str(anchor_count));anchor_count+=1
        for v in x.values():anchors(v)
    elif isinstance(x,list):
        for v in x:anchors(v)
anchors(read(R/'dataset/decisions.json'));anchors(read(R/'dataset/reconciled_dataset.json'))
checks=read(R/'analysis/checker_results.json')
check(len(checks)==9 and all(x['check']['status']=='pass' and not x['check']['errors'] for x in checks),'all nine unchanged-checker results pass')
for x in checks:check(sha(R/x['adjusted_path'])==x['adjusted_sha256'],'checked bytes '+x['original_run_id'])
ledger=read(R/'dataset/issue_dispositions.json');original_groups=read(R/'inputs/analysis/reconciliation.json')['groups']
check({g['group_id'] for g in ledger}=={g['group_id'] for g in original_groups} and len(ledger)==59,'all 59 groups accounted for')
dataset=read(R/'dataset/reconciled_dataset.json');check(dataset['new_independent_reliability_estimate'] is None,'no manufactured reliability')
check(sum(len(c['case_conclusions']) for c in dataset['cases'])==8,'eight bounded case conclusions')
manifest=R/'PACKAGE_MANIFEST.json'
if manifest.exists():
    for row in read(manifest)['files']:check(sha(R/row['path'])==row['sha256'],'package '+row['path'])
result={'status':'pass','checks_passed':len(passed),'overlay_exact_anchors_checked':anchor_count,'adjusted_v04_annotations':9,'source_text_unchanged':True,'frozen_inputs_unchanged':True,'initial_positions_unchanged':True,'all_changes_replayed':True,'semantic_validity':'Source-grounded adjudication and explicit alternatives; no mathematical or external certification.'}
print(json.dumps(result,indent=2))
