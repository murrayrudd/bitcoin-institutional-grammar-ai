import json,copy
from pathlib import Path
p=Path('annotation.json');a=json.loads(p.read_text());packet=json.loads(Path('packet.json').read_text());ss={e['source_id']:e for e in packet['entries']};by={u['unit_id']:u for u in a['units']};log=json.loads(Path('repair_log.json').read_text())
def ev(s,q):
 i=ss[s]['text'].index(q);return {'source_id':s,'span':{'start':i,'end':i+len(q),'quote':q}}
def addlog(uid,field,before,after,reason,evidence,kind,meaning):
 log.append({'change_id':'S'+str(sum(x['stage']=='source_self_review' for x in log)+1).zfill(2),'stage':'source_self_review','unit_id':uid,'field':field,'classification':kind,'meaning_changes':meaning,'before':before,'after':after,'reason':reason,'evidence':evidence})
u=by['C11b'];c=next(c for c in u['components'] if c['symbol']=='Bdir');old=copy.deepcopy(c);c['basis']='explicit';c['occurrence_role']='local';c['inference_note']='Some regtest wallets is the explicit direct object of hosts and retains its patient/target role under reconstructed store. Unlike the repo, it is not transformed from subject to destination.'
addlog('C11b','components.Bdir',old,c,'Separate predicate reconstruction from unchanged argument role: wallet objects remain explicitly supplied despite the pragmatic store action.',c['evidence'],'epistemic_component_basis_correction',False)
u=by['C04a'];old=copy.deepcopy(u['institution']);e=ev('commit:d8b705f1caeb3b4a6790cb26e4e5584ca791d965:patch:2','# Add new version after each release:');u['institution']['evidence'].append(e);u['institution']['rationale']+=' A supplied historical code comment states adding a new version after each release; this documents a compatible maintenance expectation, but neither resolves the current dispute nor establishes institutional authorization.'
addlog('C04a','institution',old,u['institution'],'Use the supplied dated code comment as bounded documentary support while retaining disputed standing and abstaining from rule status.',[e],'evidence_completion',False)
u=by['R00a'];old=copy.deepcopy(u['institution']);e=ev('commit:16624e6ff3af4429e571f7a606bbbcac336e067a:metadata','In compatibility tests it makes sense to always use the last release without the new feature, as it is likely more in use than any even older previous release.');u['institution']['evidence'].append(e);u['institution']['rationale']+=' The supplied commit describes a last-release-without-the-new-feature rationale; its accompanying patches concern txindex and mempool tests. Transfer to wallet tests is an argument in the focal review, not an already authorized universal requirement.'
addlog('R00a','institution',old,u['institution'],'Preserve the attributed precedent and its distinct test objects without conflating it with authority over this wallet-test selection dispute.',[e],'evidence_completion',False)
p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n');Path('annotation.final.json').write_bytes(p.read_bytes());Path('repair_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
# Preserve the previous post-review checker result before the final mechanical recheck.
Path('checks.review_draft.json').write_bytes(Path('checks.json').read_bytes())
