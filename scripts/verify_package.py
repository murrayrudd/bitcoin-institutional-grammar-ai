"""Check the distributed file inventory and unchanged research-file identities."""
from pathlib import Path
import hashlib, json, sys

ROOT = Path(__file__).resolve().parents[1]

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def verify():
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    expected = {r['path']: r for r in manifest['files']}
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
              if p.is_file() and not any(x in p.parts for x in ['.git', '.venv', '__pycache__'])
              and p != ROOT / 'MANIFEST.json'}
    errors = []
    if actual != set(expected):
        errors.append({'inventory_difference': sorted(actual ^ set(expected))})
    for name, row in expected.items():
        p = ROOT / name
        if not p.is_file() or p.stat().st_size != row['bytes'] or digest(p) != row['sha256']:
            errors.append({'file_mismatch': name})
    originals = json.loads((ROOT / 'provenance/source_file_map.json').read_text())
    for row in originals:
        p = ROOT / row['path']
        if not p.is_file() or digest(p) != row['sha256']:
            errors.append({'original_research_file_changed': row['path']})
    result = {'status': 'pass' if not errors else 'fail', 'package_version': manifest['version'],
              'files_checked': len(expected), 'unchanged_source_files': len(originals), 'errors': errors}
    print(json.dumps(result, indent=2))
    return not errors

if __name__ == '__main__':
    sys.exit(0 if verify() else 1)
