"""Archive completed reviewer outputs before comparison or reconciliation."""
from pathlib import Path
import json,hashlib,shutil,sys,datetime
P=Path(__file__).resolve().parents[1];ROOT=P.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
group=sys.argv[1];assert group in ['A','B','C']
d=ROOT/'reviewer_workspaces'/group
dest=P/'reviewer_outputs'/group;inputs=P/'reviewer_inputs'/group
if (dest/'freeze.json').exists():raise SystemExit('Already frozen; do not overwrite a source-first output.')
required=['annotation.json','checks.json','review_notes.json','repair_log.json']
assert all((d/f).is_file() for f in required)
inp=json.loads((d/'input_manifest.json').read_text())
for item in inp['files']:assert sha(d/item['path'])==item['sha256'],item['path']
a=json.loads((d/'annotation.json').read_text())
packet=next(f for f in d.glob('packet*.json') if sha(f)==a['packet_sha256'])
checks=json.loads((d/'checks.json').read_text());assert checks['status']=='pass'
inputs.mkdir(parents=True,exist_ok=True);dest.mkdir(parents=True,exist_ok=True)
for item in inp['files']:
 f=d/item['path'];out=inputs/item['path'];out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,out)
shutil.copy2(d/'input_manifest.json',inputs/'input_manifest.json')
for f in ['packet_v2.json','thread_metadata_supplement.json','supplement_provenance.json']:
 if (d/f).exists():shutil.copy2(d/f,inputs/f)
input_paths={x['path'] for x in inp['files']}|{'input_manifest.json','packet_v2.json','thread_metadata_supplement.json','supplement_provenance.json'}
for f in d.rglob('*'):
 if f.is_file() and '__pycache__' not in f.parts and str(f.relative_to(d)) not in input_paths:
  out=dest/f.relative_to(d);out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,out)
freeze={'review_group':group,'frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'packet_file':packet.name,'annotation_sha256':sha(dest/'annotation.json'),
 'before_comparison':True,'files':[{'path':str(f.relative_to(dest)),'sha256':sha(f)} for f in sorted(dest.rglob('*')) if f.is_file()]}
(dest/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
print(json.dumps({'group':group,'frozen_annotation':str(dest/'annotation.json'),'sha256':freeze['annotation_sha256'],'packet':packet.name,'units':len(a['units']),'statements':sum(u['record_role']=='statement' for u in a['units'])},indent=2))
