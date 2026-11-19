from pathlib import Path
import json, hashlib, shutil, datetime, re

BASE=Path('/workspace/scratch/2020b62d57db')
OLD=BASE/'fresh_coding/Bitcoin_Core_IG2_Fresh_Coding_v01'
ROOT=BASE/'reconciled_coding/Bitcoin_Core_IG2_Collaborative_Reconciliation_v01'
def raw(v): return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v): p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw(v))

TOPICS=[
('D01','Assent scope and decision object identity',['P01','P02','Q034','Q037'], 'Distinguish ordinary tentative assent to a recurring criterion from recognition as a governing expectation. Separate the general criterion, the containing discussion, and unidentified future work. Give exact preferred fields and retain justified alternatives.'),
('D02','Same actor repetition and partial support',['P03','Q013','Q041'],'Does later repetition support the entire conditional proposition or only its method? For a same-actor method restatement, determine the recognition profile under the existing codebook; keep interpersonal recognition separate.'),
('D03','Observed artifact and complete application',['Q005','Q014'],'Determine what the final spelling artifact and checkbox patch establish. Distinguish observation of the relevant resulting artifact from evidence of a historical transformation and from full fulfillment of all conditions. Do not add new criteria to v0.4.'),
('D04','Reported implementation and unmet verification conditions',['Q006','Q035'],'Determine the scope of aggregate update reports and rebasing on master. Preserve reports while avoiding verification of unmentioned individual replies, dependencies, or full conditional completion.'),
('D05','Technical necessity and social expectation',['Q015','Q036'],'Apply v0.4 to Needs rebase and needs a rebase after #26589. Technical necessity alone cannot establish obligation, but a proposed norm need not already be shared. Decide whether a preferred type is justified or alternatives must remain.'),
('D06','Focal analytical layer and governance level',['Q045','Q051'],'Separate operational performance from proposing a recurring selection arrangement. Determine whether one level follows from a stated focal proposition, or two legitimate layers should remain explicitly linked. Do not infer constitutional or network authority.'),
('D07','Targets of challenge',['Q019','Q038','Q039','Q040','Q052'],'For each group identify the focal object and whether the challenge concerns that proposition, its premise, a broader proposal, or future alternatives to a past work report. Retain bounded alternative targets where evidence does not settle them.'),
('D08','Response relations and their direction',['P04','Q042','Q043'],'Correct the reversed uptake relation. Decide whether inferred requests in contextual questions or concerns justify uptake, or whether clarifies is preferable; do not infer causal adoption.'),
('D09','Ambiguous bot referent',['Q022'],'Resolve only what the retained bot text establishes about it. Keep the software object unresolved if the evidence does not distinguish the review, comment, or displayed listing. No execution is observed.'),
('D10','Methods and proposed expectations',['Q047','Q048','Q049'],'Assess whether a specific-test preference, the coupled EOL-drop and stored-wallet alternative, and not rushing a merge articulate methods or expected conduct. Retain defensible alternatives; no shared norm follows merely from classification.')
]

ROOT.mkdir(parents=True,exist_ok=True)
for d in ['inputs','dossiers','panel','analysis','dataset','tools']: (ROOT/d).mkdir(exist_ok=True)
copylist=['analysis/reconciliation.json','analysis/adoptable_case_claims.json','analysis/mask_key.json','analysis/overlap_metrics.json','analysis/supplementary_alpha.json','analysis/common_composite_agreement.json']
for e in ['F01','F02','F03']:
    copylist.append(f'sources/{e}/packet.json')
    for i in range(1,4): copylist.append(f'runs/{e}_v04_r{i}/annotation.final.json')
for rid in ['F03_v03_r1','F03_v03_r3']: copylist.append(f'runs/{rid}/annotation.final.json')
for f in ['protocol/codebook.txt','protocol/annotation_schema.json','tools/check_annotation.py']: copylist.append('specifications/v04/'+f)
for rel in copylist:
    p=ROOT/'inputs'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(OLD/rel,p)

groups=read(OLD/'analysis/reconciliation.json')['groups'];byid={g['group_id']:g for g in groups}
entries={e['source_id']:e for case in ['F01','F02','F03'] for e in read(OLD/f'sources/{case}/packet.json')['entries']}
anns={p.parent.name:read(p) for p in (ROOT/'inputs/runs').glob('*/annotation.final.json')}
def compact_event(x): return {k:v for k,v in x.items() if k not in ['evidence','identity_evidence']}
def compact_unit(u,tid):
    out={k:u.get(k) for k in ['unit_id','source_id','span','record_role']}
    out['proposition']={k:v for k,v in (u.get('proposition') or {}).items() if k in ['summary','decision_object_id']}
    out['qualifier_descriptions']=[q['description'] for q in (u.get('proposition') or {}).get('qualifiers',[])]
    inst=u.get('institution',{})
    if tid in ['D01','D02']:
        out['recognition']=[compact_event(x) for x in inst.get('recognition',[])];out['standing_profile']=inst.get('standing_profile')
    if tid in ['D03','D04']:
        out['application']=[compact_event(x) for x in inst.get('application_evidence',[])];out['standing_profile']=inst.get('standing_profile')
    if tid in ['D05','D10']:
        out.update({k:u.get(k) for k in ['grammar','deontic_force']});out['institution']={k:inst.get(k) for k in ['type','rationale','type_alternatives']}
    if tid=='D06':out.update({k:u.get(k) for k in ['grammar','statement_target_level','observed_action_level','target_level_alternatives','observed_level_alternatives','level_rationale']})
    if tid=='D07':out['challenges']=[compact_event(x) for x in inst.get('challenges',[])];out['dispute_present']=inst.get('dispute_present')
    if tid=='D09':out['uncertainty_reason']=u.get('uncertainty_reason')
    return out
agenda=[]
for tid,title,gids,question in TOPICS:
    ds={'topic_id':tid,'title':title,'question':question,'prior_adjudications_are_proposals_not_binding_truth':True,'groups':[],'source_context':[]}
    sids=set()
    for gid in gids:
        g=byid[gid];gc={k:v for k,v in g.items() if k in ['group_id','title','category','coordinator_assessment','resolution','qualification','applicable_rules','source_evidence']};gc['affected_v04']=[]
        for a in g['affected']:
            if a['condition']!='v04':continue
            an=anns[a['run_id']];us=[u for u in an['units'] if u['unit_id'] in a['unit_ids']]
            for u in us:sids.add(u['source_id'])
            rels=[]
            for ri in a['relation_ids']:
                idx=ri if isinstance(ri,int) else int(re.search(r'\[(\d+)\]',ri).group(1))
                rels.append({'index':idx,**an['relations'][idx]})
            gc['affected_v04'].append({'run_id':a['run_id'],'units':[compact_unit(u,tid) for u in us],'relation_refs':a['relation_ids'],'relations':rels,'summary_paths':a['summary_paths']})
        for ev in g['source_evidence']:sids.add(ev['source_id'])
        ds['groups'].append(gc)
    for sid in sorted(sids):
        e=entries[sid];ds['source_context'].append({k:e[k] for k in ['source_id','speaker','actor','created_at','kind','object_id','text'] if k in e})
    write(ROOT/f'dossiers/{tid}.json',ds)
    agenda.append({'topic_id':tid,'title':title,'group_ids':gids,'question':question,'dossier':f'dossiers/{tid}.json'})
write(ROOT/'agenda.json',agenda)
selected={g for _,_,gs,_ in TOPICS for g in gs}
write(ROOT/'analysis/coverage_plan.json',{'discussion_groups':sorted(selected),'other_groups':[{'group_id':g['group_id'],'category':g['category'],'handling':'Apply clear representational corrections where prescribed; otherwise preserve the prior source-reviewed alternative without claiming panel adjudication.'} for g in groups if g['group_id'] not in selected]})
protocol={'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stage':'post_evaluation_collaborative_reconciliation','authorization':'User requests the coding adjustment and collaborative discussions aimed at resolving interpretations.','panel_design':'Three fresh reviewing agents, not the original coders. Same inherited model configuration. Independent initial positions, then one peer-response round. This is deliberative adjudication, not an independent recoding reliability test.','codebook':'inputs/specifications/v04/protocol/codebook.txt','schema':'inputs/specifications/v04/protocol/annotation_schema.json','fixed_constraints':['No new coding criteria or codebook edits','No new sources','No full recoding','Original annotations and independent agreement remain unchanged','No majority vote substitutes for source support','Unresolved alternatives may remain','No manuscript edits or fork extension'],'construction':'Nine v0.4 corrected annotation views retain their distinct unitizations. An authoritative case and decision overlay records resolved conclusions and alternatives. These views are not nine independent confirmations of the final conclusions. No arbitrary single coder is designated the truth.','rounds':[{'round':1,'task':'Read fixed codebook and ten focused dossiers. Record independent preferred interpretation, strongest alternative, exact recommended changes, and source anchors.'},{'round':2,'task':'Read all three frozen initial submissions. Respond explicitly to peers, explaining retained or revised positions. One response per topic; further discussion only for a newly discovered consequential contradiction.'}],'stop_rule':'Every material issue receives an applied correction, agreed interpretation, agreed uncertainty, or explicitly retained disagreement. Unanimity is not required.','original_package_sha256':'a170138fce0a2931ce83406548811268b61b8269b4f47a378e3114a125b2812c'}
write(ROOT/'protocol.json',protocol)
write(ROOT/'inputs_manifest.json',[{'path':str((ROOT/'inputs'/rel).relative_to(ROOT)),'sha256':sha(ROOT/'inputs'/rel),'original_relative_path':rel} for rel in copylist])
shutil.copy2(__file__,ROOT/'tools/prepare_panel.py')
print(json.dumps({'root':str(ROOT),'files':len(copylist),'dossier_bytes':{p.name:p.stat().st_size for p in (ROOT/'dossiers').glob('*.json')}},indent=2))
