from pathlib import Path
import json
p=Path('annotation.json');a=json.loads(p.read_text());u=next(u for u in a['units'] if u['unit_id']=='U08');before=json.loads(json.dumps(u['institution']))
u['institution']['application_evidence'][0]['status']='unresolved'
u['institution']['application_evidence'][0]['target']='this_proposition'
u['institution']['application_evidence'][0]['rationale']='The author reports a rebase on master, but application of the full after-#26589 proposition is unresolved because the specified preceding event is not supplied.'
u['institution']['recognition'][0]['target']='unresolved'
u['institution']['recognition'][0]['basis']='unresolved'
u['institution']['recognition'][0]['rationale']='The report corresponds to a rebase, but recognition of the complete after-#26589 request is unresolved; neither the identified triggering event nor full response linkage is verified.'
log=[{'change_id':'M01','phase':'mechanical_feedback','unit_id':'U08','fields':['institution.application_evidence','institution.recognition'],'meaning_changes':False,'effect':'evidence-basis error','diagnosis':'execution failure under an existing rule','before':before,'after':u['institution'],'rationale':'The first declared application profile was unresolved while its only record was reported with an unresolved target. The revised record explicitly states unresolved application of this proposition and preserves the same evidentiary limit. Recognition target is also bounded consistently.','evidence':u['institution']['application_evidence'][0]['evidence']}]
p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n');Path('annotation.mechanical.json').write_bytes(p.read_bytes());Path('repair_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
