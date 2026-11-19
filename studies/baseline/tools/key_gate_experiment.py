"""Test the original gpg.sh allowlist gate using simulated GPG status output.

This does not verify signatures, keys, repository access, or full commit history.
"""
from pathlib import Path
import json, tempfile, os, subprocess, hashlib

ROOT=Path(__file__).resolve().parents[1]
def content(name): return json.loads((ROOT/'sources/supplements'/name).read_text())['structuredContent']['content']
rows=[]
with tempfile.TemporaryDirectory(prefix='ig2_gate_') as temp:
    p=Path(temp); (p/'bin').mkdir(); (p/'contrib/verify-commits').mkdir(parents=True)
    gpg=p/'bin/gpg'; gpg.write_text('#!/bin/sh\nprintf "[GNUPG:] VALIDSIG %s 2021-12-16 1639684431 0 4 0 1 10 00 %s\\n" "$IG2_TEST_KEY" "$IG2_TEST_KEY"\n'); gpg.chmod(0o700)
    for n in [23798,27054]:
        before=content(f'doc_{n}_keys_base_sha.json'); after=content(f'doc_{n}_keys_merged.json')
        assert after==content(f'doc_{n}_keys_head_sha.json')
        b=set(before.split()); a=set(after.split()); assert len(a^b)==1
        changed=next(iter(a^b)); same=sorted(a&b)[0]
        script=content(f'doc_{n}_verify_gpg.json'); (p/'gpg.sh').write_text(script)
        for state,keys in [('before',before),('merged',after)]:
            (p/'contrib/verify-commits/trusted-keys').write_text(keys)
            for condition,key in [('changed_key',changed),('unchanged_key',same),('unlisted_key','0'*40)]:
                env=dict(os.environ,PATH=str(p/'bin')+os.pathsep+os.environ['PATH'],BITCOIN_VERIFY_COMMITS_ALLOW_SHA1='1',IG2_TEST_KEY=key)
                env.pop('BITCOIN_VERIFY_COMMITS_ALLOW_REVSIG',None)
                result=subprocess.run(['/bin/sh',str(p/'gpg.sh')],cwd=p,env=env,input='simulated signature payload\n',capture_output=True,text=True,timeout=5)
                expected=0 if key in keys.split() else 1
                rows.append(dict(pr=n,state=state,condition=condition,key=key,exit_status=result.returncode,expected_exit_status=expected,passed=result.returncode==expected,script_sha256=hashlib.sha256(script.encode()).hexdigest()))
out={'design':'Controlled execution of original gpg.sh with stubbed GPG VALIDSIG output and real before/merged trusted-key files. SHA1 option selects a simpler code path; it is not a security recommendation. No revoked/expired-key branches tested.','inference':'For the simulated valid signature status, changing membership changes this script gate. This neither proves signature authenticity nor reveals GitHub access permissions or institutional legitimacy.','runs':rows,'all_passed':all(r['passed'] for r in rows)}
(ROOT/'analysis/key_gate_experiment.json').write_text(json.dumps(out,indent=2)+'\n')
assert out['all_passed']; print(json.dumps({'runs':len(rows),'all_passed':out['all_passed']}))
