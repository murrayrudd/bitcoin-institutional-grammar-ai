"""Build auditable source catalog; preserve frozen discussion text unchanged."""
from pathlib import Path
import json, hashlib, difflib

ROOT = Path(__file__).resolve().parents[1]
def read(p): return json.loads(p.read_text())
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
selection = read(ROOT/'protocol/selection.json')['cases']
catalog=[]; checks=[]
for case in selection:
    eid=case['episode_id']; n=case['number']; packet=read(ROOT/f'sources/packets/{eid}.json')
    for entry in packet['entries']:
        entry['layer']='T'; entry['source_type']='frozen_corpus'; entry['url']=packet['url']
    supplements=[]
    def add(suffix,text,layer,kind,url=None,**kwargs):
        entry=dict(source_id=f'{eid}:{suffix}',text=text,layer=layer,source_type=kind,url=url,**kwargs)
        supplements.append(entry); return entry
    add('outcome',json.dumps({k:packet[k] for k in ['created_at','closed_at','merged_at','recorded_merged','recorded_merger']},sort_keys=True),'T','frozen_metadata',packet['url'])
    for path in sorted((ROOT/'sources/supplements').glob(f'doc_{n}_*.json')):
        s=read(path)['structuredContent']; suffix=path.stem[len(f'doc_{n}_'):]
        raw=s['content'].encode(); observed=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        checks.append({'path':str(path.relative_to(ROOT)),'expected_git_blob_sha':s.get('sha'),'computed_git_blob_sha':observed,'matches':observed==s.get('sha')})
        # D means standing textual guidance, not all dated files.
        layer='D' if suffix in ['before','developer_before'] else 'I'
        add('doc_'+suffix,s['content'],layer,'commit_pinned_file',s.get('display_url'),git_blob_sha=s.get('sha'),raw_file=str(path.relative_to(ROOT)))
    path=ROOT/f'sources/supplements/commit_{n}.json'
    if path.exists():
        s=read(path)['structuredContent']['commit']
        add('merge_message',s['message'],'I','git_commit',s['html_url'],commit_sha=s['sha'])
        add('merge_diff',s.get('diff',''),'I','git_patch',s['html_url'],commit_sha=s['sha'])
    if eid=='E11':
        url='https://www.erisian.com.au/bitcoin-core-dev/log-2021-12-16.html'
        add('irc_decision',"it's not an actual decision in the meeting just an oppertunity to bring up objections",'I','external_primary_excerpt',url,author='laanwj',timestamp='2021-12-16T19:07:56',retrieved_date='2026-10-31')
        add('irc_wait','open for a week at least','I','external_primary_excerpt',url,author='MarcoFalke',timestamp='2021-12-16T19:08:26',retrieved_date='2026-10-31',qualification='Fragment inside an expressed expectation, followed by a question about longer holiday timing; laanwj replied affirmatively at 19:08:50.')
        add('irc_context','At the December 16 meeting, achow101 volunteered for wallet maintenance. Several participants endorsed him. Discussion retained an opportunity for absent participants to comment through a subsequent PR. laanwj explicitly characterized the meeting as an opportunity for objections rather than the final decision. MarcoFalke expressed an expectation of at least a week of PR exposure, possibly longer during holidays; laanwj agreed. achow101 said he would open the PR after the meeting. The log later records its opening.','I','analyst_source_summary',url,source_locators='2021-12-16 19:02 to 19:09; PR opening at 19:54',retrieved_date='2026-10-31',warning='Paraphrase, not a verbatim transcript. Treat as an index to the linked primary log, not independent evidence.')
    packet['supplemental_entries']=supplements
    write(ROOT/f'sources/packets/{eid}.json',packet)
    for e in packet['entries']+supplements:
        catalog.append({k:v for k,v in e.items() if k!='text'}|{'characters':len(e['text']),'text_sha256':hashlib.sha256(e['text'].encode()).hexdigest(),'packet':f'sources/packets/{eid}.json'})
write(ROOT/'sources/catalog.json',catalog)
write(ROOT/'analysis/source_integrity.json',{'git_blob_checks':checks,'all_git_blobs_match':all(c['matches'] for c in checks),'catalog_entries':len(catalog),'offset_convention':'Zero-based Unicode code points, end exclusive, in decoded entry text; CRLF preserved.'})
print(json.dumps({'catalog_entries':len(catalog),'git_files':len(checks),'matches':sum(c['matches'] for c in checks)}))
