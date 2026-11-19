"""Post-freeze diagnostic of packet/checker metadata compatibility.
Original workflow failures remain recorded. This is not an original-run pass.
No source text, coding decision, criterion, or original artifact is modified.
"""
from pathlib import Path
import json,hashlib,tempfile,subprocess,sys
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def raw(d):return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 assert (R/'analysis/all_coding_frozen.json').exists(),'Wait for all outputs to freeze'
 results=[]
 for rid in read(R/'analysis/all_coding_frozen.json')['runs']:
  d=R/'runs'/rid;packet=read(d/'packet.json');a=read(d/'annotation.final.json');original_a=sha((d/'annotation.final.json').read_bytes());changes=[]
  for e in packet['entries']:
   for old,new in [('revision','revision_id'),('git_blob_sha','blob_sha')]:
    if e.get(old) and new not in e:
     e[new]=e[old];changes.append({'source_id':e['source_id'],'from':old,'to':new,'value':e[old]})
  pbytes=raw(packet);a['packet_sha256']=sha(pbytes);abytes=raw(a)
  with tempfile.TemporaryDirectory(prefix='ig2_alias_') as tmp:
   pp=Path(tmp)/'packet.json';ap=Path(tmp)/'annotation.json';pp.write_bytes(pbytes);ap.write_bytes(abytes)
   res=subprocess.run([sys.executable,str(d/'tools/check_annotation.py'),str(pp),str(ap)],capture_output=True,text=True)
  try:checked=json.loads(res.stdout)
  except Exception:checked={'status':'invocation_error','stdout':res.stdout,'stderr':res.stderr}
  assert original_a==sha((d/'annotation.final.json').read_bytes())
  results.append({'run_id':rid,'status_label':'post_freeze_metadata_alias_diagnostic','original_annotation_sha256':original_a,'diagnostic_annotation_sha256':sha(abytes),'diagnostic_packet_sha256':sha(pbytes),'metadata_aliases_added':changes,'annotation_change':'Only packet_sha256 points to diagnostic packet; no coding fields changed.','check':checked})
 output={'purpose':'Diagnose OP01 packet field naming, not certify semantic correctness or replace original checks.','results':results}
 p=R/'analysis/metadata_alias_diagnostic.json';p.write_bytes(raw(output));print(json.dumps([{'run':x['run_id'],'status':x['check'].get('status'),'errors':len(x['check'].get('errors',[]))} for x in results],indent=2))
if __name__=='__main__':main()
