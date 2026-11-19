"""Verify the distributed file manifest without changing archived records."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'PACKAGE_MANIFEST.json').read_text())
errors=[]
for item in manifest['files']:
    path=ROOT/item['path']
    if not path.is_file():
        errors.append({'path':item['path'],'error':'missing'})
        continue
    content=path.read_bytes()
    if len(content)!=item['bytes'] or hashlib.sha256(content).hexdigest()!=item['sha256']:
        errors.append({'path':item['path'],'error':'size or digest differs'})
print(json.dumps({'status':'fail' if errors else 'pass','checked_files':len(manifest['files']),'errors':errors,'scope':'Byte integrity only, not semantic validation.'},indent=2))
sys.exit(bool(errors))
