"""Extended post-freeze OP01 diagnostic; preserves the earlier alias-only result.

Also exposes an exact commit SHA already serialized in a commit-metadata source.
No source text or coding judgment changes. This is not an original-run pass.
"""
from pathlib import Path
import json,tempfile,subprocess,sys,datetime
from metadata_alias_diagnostic import R,read,raw,sha

assert (R/'analysis/metadata_alias_diagnostic.json').exists()
results=[]
for rid in read(R/'analysis/all_coding_frozen.json')['runs']:
    d=R/'runs'/rid;packet=read(d/'packet.json');a=read(d/'annotation.final.json')
    original=sha((d/'annotation.final.json').read_bytes());changes=[]
    for e in packet['entries']:
        for old,new in [('revision','revision_id'),('git_blob_sha','blob_sha')]:
            if e.get(old) and new not in e:
                e[new]=e[old];changes.append({'source_id':e['source_id'],'from':old,'to':new,'value':e[old]})
        if e['kind']=='commit_metadata' and not e.get('revision_id'):
            source=json.loads(e['text']);commit_sha=source['sha']
            assert len(commit_sha)==40 and e['object_id'].endswith('/'+commit_sha)
            assert source['html_url']==e['object_id']
            e['revision_id']=commit_sha
            changes.append({'source_id':e['source_id'],'from':'exact serialized source text /sha, checked against object_id and html_url','to':'revision_id','value':commit_sha})
    pb=raw(packet);a['packet_sha256']=sha(pb);ab=raw(a)
    with tempfile.TemporaryDirectory(prefix='ig2_identity_') as tmp:
        pp=Path(tmp)/'packet.json';ap=Path(tmp)/'annotation.json';pp.write_bytes(pb);ap.write_bytes(ab)
        out=subprocess.run([sys.executable,str(d/'tools/check_annotation.py'),str(pp),str(ap)],capture_output=True,text=True)
    checked=json.loads(out.stdout)
    assert original==sha((d/'annotation.final.json').read_bytes())
    results.append({'run_id':rid,'status_label':'post_freeze_metadata_identity_diagnostic','original_annotation_sha256':original,'diagnostic_annotation_sha256':sha(ab),'diagnostic_packet_sha256':sha(pb),'metadata_identity_fields_added':changes,'annotation_change':'Only packet_sha256; source text and coding fields unchanged.','check':checked})
output={'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'purpose':'Extend OP01 diagnostic after alias-only diagnostic left one revision-identity failure. The final commit identity already exists exactly in serialized source metadata. Original tests and earlier diagnostic remain unchanged.','results':results}
(R/'analysis/metadata_identity_diagnostic.json').write_bytes(raw(output))
print(json.dumps([{'run':x['run_id'],'status':x['check']['status'],'errors':len(x['check']['errors'])} for x in results]))
