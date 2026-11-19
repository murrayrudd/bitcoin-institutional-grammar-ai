"""Apply auditable post-evaluation decisions to copies, never to independent outputs."""
from pathlib import Path
import json, hashlib, copy, subprocess, sys, datetime, re
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def raw(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw(x))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
anns={p.parent.name:read(p) for p in (R/'inputs/runs').glob('*/annotation.final.json')}
originals=copy.deepcopy(anns)
changes=[]
def ptr(parts):return '/'+ '/'.join(str(x).replace('~','~0').replace('/','~1') for x in parts)
def patch(rid,parts,value,decision,reason,kind='coding'):
    x=anns[rid]
    for k in parts[:-1]:x=x[k]
    old=copy.deepcopy(x[parts[-1]])
    if old==value:return
    x[parts[-1]]=copy.deepcopy(value)
    changes.append({'change_id':f'CH{len(changes)+1:03d}','run_id':rid,'path':ptr(parts),'before':old,'after':value,'decision_ids':decision.split(','),'reason':reason,'kind':kind})
def up(rid,uid,tail,value,decision,reason):
    i=next(i for i,u in enumerate(anns[rid]['units']) if u['unit_id']==uid)
    patch(rid,['units',i]+tail,value,decision,reason)
def unit(rid,uid):return next(u for u in anns[rid]['units'] if u['unit_id']==uid)

# Clear execution and representational repairs established before deliberation.
for rid,uid,gid in [('F01_v04_r3','C30','P01'),('F01_v04_r2','U24','P01'),('F01_v04_r3','R05','P02')]:
    up(rid,uid,['proposition','decision_object_id'],None,gid,'The unidentified future contribution is not the containing PR.')
    up(rid,uid,['proposition','identity_evidence'],[],gid,'The containing discussion does not identify future work.')
up('F01_v04_r3','R05',['institution','recognition',0,'object_id'],None,'P02','The general cleanup principle has no applicable numbered decision object; its source episode remains recorded separately.')
up('F01_v04_r3','R05',['institution','recognition',0,'identity_evidence'],[],'P02','No identifier for the general principle is established.')
up('F01_v04_r3','R05',['institution','recognition',0,'rationale'],'ACK supports general cleanup, not every selection criterion or an implemented follow-up. The event concerns a general principle, so a numbered object is inapplicable; the independence key identifies only the discussion episode.','P02','Explain inapplicable object versus unknown future proposal.')
up('F01_v04_r1','S13',['institution','recognition',0,'target'],'broader_principle','P03','The later open-PR method does not repeat the until-another-PR-needs-it condition.')
up('F01_v04_r1','S13',['institution','recognition',0,'rationale'],'Sjors repeats the broader open-PR method with occasional rebasing. The later statement does not restate the condition that another PR needs it, so it cannot establish repetition of the complete conditional proposition. This is same-actor correspondence, not interpersonal recognition.','P03','Preserve the material timing qualification.')
patch('F01_v04_r2',['relations',24,'from_unit_id'],'U30','P04','Uptake runs from the initiating proposal to its response.')
patch('F01_v04_r2',['relations',24,'to_unit_id'],'U33','P04','Uptake runs from the initiating proposal to its response.')
patch('F01_v04_r2',['relations',24,'rationale'],'The separate-cleanup suggestion precedes the author\'s corresponding scope response. This contextual relation does not establish a direct thread, causal influence, or implementation of the follow-up.','P04','Retain the contextual basis and limited response claim.')

literal=[('F02_v04_r1','F02_S03','Q003'),('F03_v04_r3','F03-U13','Q009'),('F03_v04_r2','F03-U09','Q009'),('F03_v04_r2','F03-U01','Q010'),('F03_v04_r3','F03-U05','Q011'),('F01_v04_r1','S11','Q024'),('F01_v04_r2','U10','Q024'),('F01_v04_r1','S24','Q025'),('F01_v04_r1','S31','Q028')]
for rid,uid,gid in literal:up(rid,uid,['parse_mode'],'literal',gid,'The source supplies the selected action; inferred recommendation force or an antecedent does not make that action reconstructed.')
u=unit('F01_v04_r2','U10');i=next(i for i,c in enumerate(u['components']) if c['symbol']=='I')
for k,v in [('basis','explicit'),('occurrence_role','local'),('inference_note','The source explicitly supplies adding. The recommendation force is inferred from the justification claim; the action role is supplied.')]:up('F01_v04_r2','U10',['components',i,k],v,'Q024','Separate explicit action from inferred recommendation force.')
for rid,uid in [('F01_v04_r1','S11'),('F01_v04_r2','U10')]:
    u=unit(rid,uid);i=next(i for i,c in enumerate(u['components']) if c['symbol']=='Bdir')
    up(rid,uid,['components',i,'inference_note'],'The object belongs to the explicitly supplied adding action. The recommendation force is inferred, and the alternative downloadable version remains part of the target.','Q024','Keep explanation consistent with the literal action parse.')
up('F03_v04_r3','F03-U17',['institution','recognition',0,'target'],'unresolved','Q012','The response corresponds to the additional-output method, but the required separate workflow identity remains unknown.')
up('F03_v04_r3','F03-U17',['institution','recognition',0,'basis'],'unresolved','Q012','The frozen checker requires unresolved basis for an unresolved event target; the textual response correspondence remains explained in the rationale.')
up('F03_v04_r3','F03-U17',['institution','recognition',0,'rationale'],'The response addresses the additional-output workflow with a technical complexity explanation. The separate workflow object is unidentified, so the event target remains unresolved. The textual correspondence establishes neither expectation recognition nor success of the attempt.','Q012','Retain textual correspondence while exposing the identity limitation.')
for rid,uid,gid in [('F03_v04_r1','U20','Q008a'),('F03_v04_r2','F03-U13','Q008a'),('F03_v04_r1','U23','Q008b'),('F03_v04_r2','F03-U16','Q008b')]:up(rid,uid,['presentation','quotation'],'proposed_wording',gid,'The source presents new replacement wording, not a quotation of a previously coded proposition.')
u=unit('F01_v04_r1','S15');i=next(i for i,c in enumerate(u['components']) if c['symbol']=='Cac')
up('F01_v04_r1','S15',['components',i,'symbol'],'Cex','Q029','Use the project\'s preferred execution-purpose convention; the activation reading remains semantically defensible.')
for rid in ['F01_v04_r1','F01_v04_r3']:up(rid,'Q02',['speech_act'],'technical_description','Q030a','Retain the original technical-description function in the repeated occurrence.')
up('F01_v04_r1','S26',['speech_act'],'asserted','Q030b','Choose the declarative-claim convention for the source and its quotation; the claim advances a proposed selection criterion.')
up('F01_v04_r1','S26',['alternative_interpretation'],'A methodological preference rather than a social expectation. The declarative assertion also advances a proposed criterion, so proposed remains a defensible speech-act alternative.','Q030b','Harmonization does not settle the assertion-versus-proposal boundary.')
up('F01_v04_r1','Q12',['speech_act'],'proposed','Q030c','The quotation retains the original navigation-request function.')

# These reference-only v0.3 copies are not part of the adopted v0.4 dataset.
for rid in ['F03_v03_r1','F03_v03_r3']:
    patch(rid,['relations',3,'rationale'],'The author\'s reviewability statement clarifies the retained body\'s non-delay intention by distinguishing review from completion of the companion GUI. The record does not establish the relative wording dates of those two passages; this semantic relation makes no earlier/later wording claim.','P05','The retained body lacks sentence-level edit history.')

# Deliberation decisions are separate, inspectable input, not encoded in a truth algorithm.
for p in read(R/'analysis/panel_patch_plan.json'):
    if 'unit_id' in p:up(p['run_id'],p['unit_id'],p['tail'],p['value'],p['decision_ids'],p['reason'])
    else:patch(p['run_id'],p['path'],p['value'],p['decision_ids'],p['reason'])

adapter=[];packetpaths={}
for case in ['F01','F02','F03']:
    old=read(R/f'inputs/sources/{case}/packet.json');packet=copy.deepcopy(old);adds=[]
    for e in packet['entries']:
        for a,b in [('revision','revision_id'),('git_blob_sha','blob_sha')]:
            if e.get(a) and b not in e:e[b]=e[a];adds.append({'source_id':e['source_id'],'from':a,'to':b,'value':e[a]})
        if e['kind']=='commit_metadata' and not e.get('revision_id'):
            s=json.loads(e['text']);v=s['sha'];assert len(v)==40 and e['object_id'].endswith('/'+v) and s['html_url']==e['object_id']
            e['revision_id']=v;adds.append({'source_id':e['source_id'],'from':'sha in retained commit metadata and matching object URL','to':'revision_id','value':v})
    assert [e['text'] for e in old['entries']]==[e['text'] for e in packet['entries']]
    p=R/f'dataset/packets/{case}.json';write(p,packet);packetpaths[case]=p
    adapter.append({'episode_id':case,'original_packet_sha256':sha(R/f'inputs/sources/{case}/packet.json'),'adapted_packet_sha256':sha(p),'added_metadata':adds,'source_text_unchanged':True})
checks=[]
for rid,a in anns.items():
    stage='adjusted_annotations' if '_v04_' in rid else 'reference_only_v03'
    patch(rid,['packet_sha256'],sha(packetpaths[a['episode_id']]),'OP01','Use the metadata-adapted packet with identical source text.','technical_metadata')
    patch(rid,['run_id'],rid+'__reconciled','PROTOCOL','Identify a post-evaluation adjusted view, not an independent coding run.','provenance')
    out=R/f'dataset/{stage}/{rid}.json';write(out,a)
    if '_v04_' in rid:
        cmd=[sys.executable,str(R/'inputs/specifications/v04/tools/check_annotation.py'),str(packetpaths[a['episode_id']]),str(out)]
        result=subprocess.run(cmd,capture_output=True,text=True)
        try:check=json.loads(result.stdout)
        except ValueError:raise RuntimeError(result.stdout+'\n'+result.stderr)
        checks.append({'original_run_id':rid,'adjusted_path':str(out.relative_to(R)),'original_sha256':sha(R/f'inputs/runs/{rid}/annotation.final.json'),'adjusted_sha256':sha(out),'check':check})
write(R/'analysis/change_log.json',changes)
write(R/'analysis/metadata_adapter.json',adapter)
write(R/'analysis/checker_results.json',checks)
for row in read(R/'inputs_manifest.json'):assert sha(R/row['path'])==row['sha256'],row['path']
write(R/'analysis/build_status.json',{'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'adjusted_v04_annotations':len(checks),'coding_field_changes':sum(x['kind']=='coding' for x in changes),'technical_and_provenance_changes':sum(x['kind']!='coding' for x in changes),'original_inputs_unchanged':True,'all_v04_checks_pass':all(x['check']['status']=='pass' for x in checks)})
print(json.dumps({'changes':len(changes),'checks':[(c['original_run_id'],c['check']['status'],len(c['check']['errors'])) for c in checks]},indent=2))
