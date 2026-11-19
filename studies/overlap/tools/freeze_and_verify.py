"""Freeze submitted coding outputs and independently repeat the supplied checker."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    target = ROOT/'protocol/frozen_outputs.json'
    assert not target.exists(), 'Submitted outputs have already been frozen.'
    frozen = json.loads((ROOT/'protocol/frozen_inputs.json').read_text())
    changed = [p for p, h in frozen['files'].items() if digest(ROOT/p) != h]
    assert not changed, ('Frozen inputs changed', changed)
    output = {'frozen_at_utc':datetime.now(timezone.utc).isoformat(),
              'frozen_input_files_verified':len(frozen['files']),
              'input_changes':changed, 'reviewers':{}}
    for label in 'ABC':
        folder = ROOT/'reviewers'/label
        for name in ['annotation.first_complete.json','annotation.json','checks.json',
                     'repair_log.json','review_notes.json']:
            assert (folder/name).is_file(), (label, 'Missing final deliverable', name)
        files = {str(p.relative_to(ROOT)):digest(p) for p in sorted(folder.rglob('*'))
                 if p.is_file() and '__pycache__' not in str(p)}
        run = subprocess.run([sys.executable,str(ROOT/'common_input/tools/check_annotation.py'),
                              str(ROOT/'common_input/packet.json'),str(folder/'annotation.json')],
                              text=True,capture_output=True,cwd=folder)
        try: checks = json.loads(run.stdout)
        except Exception: checks = {'status':'invalid_checker_output','stdout':run.stdout,'stderr':run.stderr}
        (ROOT/f'analysis/checker_repeated_{label}.json').write_text(json.dumps(checks,indent=2)+'\n')
        first = json.loads((folder/'annotation.first_complete.json').read_text())
        final = json.loads((folder/'annotation.json').read_text())
        output['reviewers'][label] = {'files':files,'checker_exit_code':run.returncode,
            'checker_status':checks.get('status'),
            'first_equals_final':first==final,
            'first_complete_sha256':digest(folder/'annotation.first_complete.json'),
            'final_sha256':digest(folder/'annotation.json')}
    target.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:{x:y for x,y in v.items() if x!='files'}
                      for k,v in output['reviewers'].items()},indent=2))

if __name__ == '__main__': main()
