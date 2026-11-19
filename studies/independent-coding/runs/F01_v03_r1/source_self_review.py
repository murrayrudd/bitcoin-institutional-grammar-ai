import json,copy
from pathlib import Path
p=Path('annotation.json');a=json.loads(p.read_text());packet=json.loads(Path('packet.json').read_text());sources={e['source_id']:e for e in packet['entries']};by={u['unit_id']:u for u in a['units']};log=json.loads(Path('repair_log.json').read_text())
def ev(s,q):
 t=sources[s]['text'];i=t.index(q);return {'source_id':s,'span':{'start':i,'end':i+len(q),'quote':q}}
def note(uid,field,before,after,reason,meaning=False,classification='convention_deviation',evidence=None):
 log.append({'change_id':'S'+str(sum(x['stage']=='source_self_review' for x in log)+1).zfill(2),'stage':'source_self_review','unit_id':uid,'field':field,'classification':classification,'meaning_changes':meaning,'before':before,'after':after,'reason':reason,'evidence':evidence or [ev(by[uid]['source_id'],by[uid]['span']['quote'])]})
def change(uid,field,value,reason,meaning=False,classification='convention_deviation',evidence=None):
 u=by[uid];old=copy.deepcopy(u[field]);u[field]=value;note(uid,field,old,value,reason,meaning,classification,evidence)
# Original communicative acts remain separate from grammar and role.
for uid,val,reason in [
 ('C03','reported_action','The source reports a Concept NACK; the convention classifies review votes as reported acts, even when their rationale is technical.'),
 ('C13','reported_action','The author reports completed rebase and update actions rather than merely describing technical background.'),
 ('C04b','asserted','The proposition is expressed as a declarative justification claim; its inferred recommendation force is recorded separately.'),
 ('C05c','asserted','A declarative personal preference retains asserted speech act under the pragmatic request reading.'),
 ('C11a','question','Both children fall within the single literal So maybe ... ? question; splitting its actions does not remove question force.')]:
 change(uid,'speech_act',val,reason)
quoteacts={'C06q1':'technical_description','C06q2':'technical_description','C07q':'technical_description','C08q1':'technical_description','C08q2':'question','C09q':'technical_description','C15q1':'technical_description','C15q2':'question'}
for uid,v in quoteacts.items():change(uid,'speech_act',v,'Repeated quotation preserves the original question or technical-description act; record_role already marks repetition.')
change('B03','scope','general','Anymore and the same procedure as every release extend the negated maintenance need to the recurring release-update domain, not only this PR.',True,'substantive_scope_correction',[ev('pr26586:body',sources['pr26586:body']['text'])])
by['B03']['alternative_interpretation']+=' A narrower reading treats the claim as limited to the present update.'
note('B03','alternative_interpretation','Pure technical lack of necessity, not a deontic exemption.',by['B03']['alternative_interpretation'],'Retain the case-specific reading as a bounded alternative after correcting the primary scope.',False,'defensible_alternative')
change('C09b','scope','general','The generic you and to run the test at all describe a recurring prerequisite for this particular test, not only the present PR.',True,'substantive_scope_correction')
change('R02b','deontic_force','nondeontic','An attributed preference to verify is a personal strategy, not a recommendation directed at another actor.',True,'substantive_force_correction')
# The rebase action is reported, but the qualification after #26589 is not verified.
u=by['C02b'];old=copy.deepcopy(u['disposition_events']);u['disposition_events']=[{'kind':'reported_implemented','target':'unresolved','basis':'unresolved','evidence':[ev('pr26586:comments:13','Rebased on master')],'rationale':'A rebase is reported, but whether this fulfills the qualified after-#26589 proposition cannot be established from the supplied sources.'}]
note('C02b','disposition_events',old,u['disposition_events'],'The report individually identifies rebasing but does not verify the material after-#26589 qualifier; the disposition target must remain unresolved.',True,'substantive_evidence_scope_correction',[ev('pr26586:comments:2','Meanwhile it needs a rebase after #26589.'),ev('pr26586:comments:13','Rebased on master')])
# Preserve the unchanged fetch default as direct design context without inventing a duty.
u=by['C10a'];default_ev=ev('pr26586:comments:10','The default of `test/get_previous_releases.py` would still to fetch all the binaries.')
old=copy.deepcopy(u['institution']['evidence']);u['institution']['evidence'].append(default_ev)
note('C10a','institution.evidence',old,u['institution']['evidence'],'The following default-behavior clause materially qualifies how developer selection would work; retain it as technical design context, not an additional prescription.',False,'evidence_completion',[default_ev])
old=u['alternative_interpretation'];u['alternative_interpretation']+=' The source expressly retains fetching all binaries as the default; proposed discretion depends on the available releases, rather than a newly selective fetch default.'
note('C10a','alternative_interpretation',old,u['alternative_interpretation'],'Make the unchanged all-binaries default recoverable alongside the implementation alternative.',False,'evidence_completion',[default_ev])
# The miniscript objection targets a separate technical premise, not the #25717 rationale.
s='pr26586:comments:4';q='On the wallet side this version added watch-only miniscript support (which last time I checked caused problems when downgrading).'
new=copy.deepcopy(by['C05a']);new.update({'unit_id':'C04c','source_id':s,'span':ev(s,q)['span'],'speech_act':'technical_description','alternative_interpretation':'The statement reports past checking; the packet does not independently verify the feature effect or downgrade problem.','uncertainty_reason':'Attributable technical rationale rather than independently measured behavior.','confidence':'plausible'})
new['institution']['rationale']='Version-specific watch-only-miniscript rationale retained as the actual endpoint of the following coverage objection.';new['institution']['evidence']=[ev(s,q)];a['units'].insert(a['units'].index(by['C04b'])+1,new);by['C04c']=new
note('C04c','unit',None,new,'Create the needed context endpoint for the distinct wallet-feature premise; do not silently attach its challenge to #25717.',True,'substantive_relation_target_correction',[ev(s,q)])
r=next(r for r in a['relations'] if r['from_unit_id']=='C05a' and r['type']=='challenges');old=copy.deepcopy(r);r['to_unit_id']='C04c';r['rationale']='The coverage objection limits the relevance of the separate watch-only-miniscript premise, without disputing #25717 or the existence of the feature.'
note('C04c','relation.C05a.challenges',old,r,'Correct the target of the test-coverage objection to the actual technical premise.',True,'substantive_relation_target_correction',r['evidence'])
# A review ACK is uptake of the proposal, not clarification of its contents.
r=next(r for r in a['relations'] if r['from_unit_id']=='C15a' and r['to_unit_id']=='P01');old=copy.deepcopy(r);r['from_unit_id']='P01';r['to_unit_id']='C15a';r['type']='uptake';r['rationale']='The commit-specific test ACK responds to the broader proposal identified by the metadata title and matching recorded head. It does not endorse each intervening recommendation.'
note('C15a','relation.P01.uptake',old,r,'Use initiating proposal to attributable response direction for the broader-patch test ACK.',False,'convention_deviation',r['evidence'])
r=next(r for r in a['relations'] if r['from_unit_id']=='C03' and r['to_unit_id']=='P01');old=copy.deepcopy(r);r['rationale']='Concept NACK challenges the same broader PR at its then-discussed v24 version, citing a bug and doubtful difference. P01 is the retained title with later v24.0.1 wording, not evidence that the earlier NACK targeted the later fixed version.'
note('C03','relation.C03.challenges',old,r,'Clarify version and temporal identity: the initial v24 criticism and the later retained v24.0.1 title concern the same PR at different states.',False,'evidence_scope_clarification',[ev('pr26586:comments:3',sources['pr26586:comments:3']['text']),ev('pr26586:comments:13','updated to v24.0.1'),ev('pr26586:metadata','"title": "test: previous releases: add v24.0.1"')])
# Explicitly mark original compound quotation as mixed communicative functions rather than flattening it.
old=by['R02q']['presentation']['rationale'];by['R02q']['presentation']['rationale']='A repeated block containing an asserted criterion, conditional review demands, and navigation; other preserves their mixed communicative function rather than treating the compound quote as a new endorsement.'
note('R02q','presentation.rationale',old,by['R02q']['presentation']['rationale'],'Explain other speech act for the heterogeneous full-comment quotation; homogeneous repeated questions and descriptions are separately classified.')
# Keep unit inventories consistent after adding the necessary context endpoint.
for item in a['entry_screening']:
 item['unit_ids']=[u['unit_id'] for u in a['units'] if u['source_id']==item['source_id']]
p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n');Path('annotation.final.json').write_bytes(p.read_bytes());Path('repair_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'units':len(a['units']),'statement_units':sum(u['record_role']=='statement' for u in a['units']),'repairs':len(log)}))
