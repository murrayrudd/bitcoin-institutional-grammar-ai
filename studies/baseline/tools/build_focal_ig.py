"""Focal IG representations. This is a compact analytical schema, not exhaustive
v0.3 export, IG Script, or a measure of extraction coverage."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
packets={p.stem:json.loads(p.read_text()) for p in (ROOT/'sources/packets').glob('E??.json')}
sources={e['source_id']:e for p in packets.values() for e in p['entries']+p['supplemental_entries']}
units=[]
def unit(eid,suffix,quote,grammar,force,components,institution,standing,target,interpretation,alternatives,claims):
    sid=eid+':'+suffix;start=sources[sid]['text'].index(quote); cs=[]
    for symbol,value,needle,basis in components:
        offset=quote.index(needle)
        cs.append(dict(symbol=symbol,value=value,basis=basis,occurrence_role='local' if basis=='explicit' else 'semantic_inference',evidence={'source_id':sid,'span':{'start':start+offset,'end':start+offset+len(needle),'quote':needle}}))
    units.append(dict(unit_id=eid+'-U'+str(1+sum(u['episode_id']==eid for u in units)),episode_id=eid,source_id=sid,span={'start':start,'end':start+len(quote),'quote':quote},grammar=grammar,deontic_force=force,components=cs,institutional_type=institution,standing=standing,statement_target_level=target,interpretation=interpretation,alternatives_and_limits=alternatives,linked_claim_ids=[eid+'-'+c for c in claims]))

unit('E01','doc_head','Please refrain from creating several pull requests for the same change.','regulative','recommendation',[
('A','contributors','Please refrain','context_inferred'),('I','refrain from','refrain from','explicit'),('Bdir','creating several pull requests for the same change','creating several pull requests for the same change','explicit')],
'norm_candidate','documented','operational','Please expresses politeness. The implied addressee is the contributor addressed by the guide. The same-change qualifier is part of the complete object.','Stronger prohibition is possible in practice, but the imperative alone and this episode do not demonstrate enforcement.',['C1','C4'])
unit('E01','doc_head','If you have problems with squashing (or other workflows with `git`), you can\nalternatively enable "Allow edits from maintainers" in the right GitHub\nsidebar and ask for help in the pull request.','regulative','permission',[
('A','you','you','explicit'),('D','can','can','explicit'),('I','enable','enable','explicit'),('Bdir','Allow edits from maintainers','"Allow edits from maintainers"','explicit'),('Cac','problems with squashing or other Git workflows','If you have problems with squashing (or other workflows with `git`)','explicit'),('Cex','in the right GitHub sidebar','in the right GitHub\nsidebar','explicit')],
'strategy_candidate','documented','operational','This focal projection represents the enabling action. The adjacent asking-for-help action remains in the full source; it is not claimed as a complete compound annotation.','Can could also convey technical possibility. Optional guidance supports permission or offered strategy, not obligation.',['C2','C3'])
unit('E02','doc_head','Trivial pull requests or pull requests that refactor the code with no clear\nbenefits may be immediately closed by the maintainers to reduce unnecessary\nworkload on reviewing.','regulative','permission',[
('A','the maintainers','the maintainers','explicit'),('D','may','may','explicit'),('I','be closed','closed','explicit'),('Bdir','trivial PRs or refactoring PRs with no clear benefits','Trivial pull requests or pull requests that refactor the code with no clear\nbenefits','explicit'),('Cex','immediately','immediately','explicit'),('Cex','to reduce unnecessary review workload','to reduce unnecessary\nworkload on reviewing','explicit')],
'rule_candidate','documented','operational','Passive syntax explicitly identifies the actor and complete eligible PR set. The merged guide attributes this permission to maintainers; head text and merge metadata support documentary authorization.','Authorization in a merged guide is not evidence of application in this episode or uniform practice.',['C1','C4'])
unit('E02','doc_head','Pull requests that refactor the code should not be made by new contributors.','regulative','recommendation',[
('A','new contributors','new contributors','explicit'),('D','should not','should not','explicit'),('I','be made','be made','explicit'),('Bdir','pull requests that refactor the code','Pull requests that refactor the code','explicit')],
'norm_candidate','documented','operational','The lexical negative is preserved. Advisory should not follows the frozen project convention.','A binding prohibition is an alternative requiring evidence beyond the lexical form.',['C2'])
unit('E03','doc_developer_head','Note that when there are no conflicts at all, however, rebasing should be\navoided, as it can be disruptive to reviewers.','regulative','recommendation',[
('A','contributor rebasing the branch','rebasing','context_inferred'),('D','should','should','explicit'),('I','be avoided','avoided','explicit'),('Bdir','rebasing','rebasing','explicit'),('Cac','when there are no conflicts at all','when there are no conflicts at all','explicit')],
'norm_candidate','text_only','operational','The contributor role is inferred from the guide context. Disruption to reviewers supplies rationale, not an independent sanction.','This is unmerged proposed wording. The neighboring within-branch fixup exception remains material to the overall proposal.',['C1','C4'])
unit('E04','doc_before','You are expected to reply to any review comments before your pull request is\nmerged.','regulative','obligation',[
('A','You','You','explicit'),('D','are expected to','are expected to','explicit'),('I','reply','reply','explicit'),('Bdir','any review comments','any review comments','explicit'),('Cex','before your pull request is merged','before your pull request is\nmerged','explicit')],
'rule_candidate','locally_supported','operational','The guide and attributable closure explanation support a candidate rule under v0.3. Bdir denotes the single target of reply under the project convention.','The linked application is attributed to the speaker; the author need not agree with the feedback and can explain disagreement.',['C1','C2','C3'])
unit('E04','doc_before','If there is outstanding feedback and\nyou are not actively working on it, your pull request may be closed.','regulative','permission',[
('A','actor authorized to close the PR','may be closed','context_inferred'),('D','may','may','explicit'),('I','be closed','closed','explicit'),('Bdir','your pull request','your pull request','explicit'),('Cac','outstanding feedback and inactive response','If there is outstanding feedback and\nyou are not actively working on it','explicit')],
'rule_candidate','locally_supported','operational','The actor is omitted locally and is not silently assigned to all reviewers. This permission is linked as a separately represented possible consequence of unmet response requirements.','The conditional is conjunctive. Closure is procedural; punishment and sole causation are not inferred.',['C1','C2','C4'])
unit('E05','comments:1',"Don't forget to include the commit hash after your ACK to specify which version of the PR you are ACK:ing",'regulative','recommendation',[
('A','paymog',"Don't forget",'context_inferred'),('I','include','include','explicit'),('Bdir','the commit hash','the commit hash','explicit'),('Cex','after your ACK','after your ACK','explicit'),('Cex','to specify which version of the PR you are ACKing','to specify which version of the PR you are ACK:ing','explicit')],
'norm_candidate','locally_supported','operational','The addressee comes from the explicit mention immediately before the chosen unit. It is nonlocal, not an explicit A in this span. The response supplies local uptake.','The imperative does not supply a lexical D. This reminder supplies no sanction.',['C1','C2','C3'])
unit('E06','comments:5',"If you agree with the changes, please add the latest hash after your ack, otherwise it's just a concept ack.",'regulative','recommendation',[
('A','you','you','explicit'),('I','add','add','explicit'),('Bdir','the latest hash','the latest hash','explicit'),('Cac','If you agree with the changes','If you agree with the changes','explicit'),('Cex','after your ack','after your ack','explicit')],
'norm_candidate','locally_supported','operational','This projection isolates the requested action; the linked classification is represented separately. The complete conditional sentence preserves the contrast.','It is not enough for a hash to exist somewhere: the review target must correspond to the relevant revision.',['C1','C2','C3'])
unit('E06','comments:5',"otherwise it's just a concept ack.",'constitutive','nondeontic',[
('E','the ACK without the requested hash','it','context_inferred'),('F','is',"'s",'explicit'),('P','just a concept ack','just a concept ack','explicit'),('Cac','otherwise','otherwise','explicit')],
'constitutive_specification','locally_supported','operational','The pronoun and otherwise condition refer to the preceding requested hash addition. This is a local classification claim about an ACK.','Grammatical constitution of an event type does not allocate constitutional powers. Universal bot behavior is not established.',['C1','C2'])
unit('E07','comments:4','(Without a hash, no one can know what the comment is referring to)','not_institutional','nondeontic',[],
'not_applicable','not_applicable','not_applicable','The focal sentence gives an identification rationale. Its local wording alone is not an obligation; the guide and exchange supply the institutional context.','An implied request to add a hash is plausible pragmatically. Missing edit history prevents a causal correction claim.',['C1','C2','C4'])
unit('E08','comments:4','Two utACK or one tested ACK should be sufficient.','undetermined','nondeontic',[
('M','should','should','explicit')],
'undetermined','disputed','operational','The sentence asserts adequacy under the preceding simple-test-PR scope. A constitutive sufficiency condition and a pragmatic permission-to-merge reading are both plausible; full E/F/P or A/D/I decomposition is withheld.','Do not convert predictive or adequacy should into a mandatory minimum. The condition is OR, and the speaker is giving a post-merge explanation.',['C1','C2','C4'])
unit('E09','comments:9',"Please reopen if you're going to work on this again.",'regulative','recommendation',[
('A','the PR author','Please reopen','context_inferred'),('I','reopen','reopen','explicit'),('Bdir','this PR','this','context_inferred'),('Cac','if you are going to work on this again',"if you're going to work on this again",'explicit')],
'strategy_candidate','text_only','operational','The omitted reopening object is inferred from the closure explanation; the token this in the condition is evidence for reference, not an explicit local object of reopen.','No observed reopening is claimed. The invitation is compatible with continued support for the document idea.',['C2','C3','C4'])
unit('E10','review_comments:4','The focus area is something that is entrusted to the maintainer to decide for themselves.','regulative','permission',[
('A','the maintainer','the maintainer','explicit'),('I','decide','decide','explicit'),('Bdir','the focus area','The focus area','context_inferred')],
'undetermined','disputed','operational','The object role is reconstructed from a fronted subject in a paraphrased decision proposition. Entrusted suggests discretion, but no lexical D is supplied.','Descriptive role autonomy or a prescriptive permission are alternatives. The author denies enforced jurisdictions, and the document never merges.',['C1','C2','C4'])
unit('E11','doc_before','there are repository "maintainers" who are responsible for\nmerging pull requests','constitutive','nondeontic',[
('E','repository maintainers','repository "maintainers"','explicit'),('F','are responsible for','are responsible for','explicit'),('P','merging pull requests','merging pull requests','explicit')],
'constitutive_specification','documented','operational','The guide describes an existing role. The nomination episode separately supports local recognition of one occupant; key checks are not counted as identical role endorsements.','Constitutive grammar does not show new constitutional allocation. Access-grant timing and network-level authority remain outside the evidence.',['C1','C2','C4'])
unit('E12','comments:7','I think this can be merged as is','regulative','recommendation',[
('A','actor able to merge the PR','can be merged','context_inferred'),('D','can','can','explicit'),('I','be merged','merged','explicit'),('Bdir','this PR','this','context_inferred'),('Cex','as is','as is','explicit')],
'strategy_candidate','text_only','operational','A proposed workflow separates the key-list intent from fixes to the verification program. The passive actor is inferred and remains unnamed in the local proposition.','Can may express feasibility as well as permission. The statement is a recommendation, not a binding authorization conferred by this speaker.',['C1','C2','C3'])

for u in units:
    if u['unit_id']=='E05-U1':
        c=next(c for c in u['components'] if c['symbol']=='A')
        text=sources[u['source_id']]['text'];start=text.index('@paymog')
        c['evidence']={'source_id':u['source_id'],'span':{'start':start,'end':start+7,'quote':'@paymog'}}
        c['occurrence_role']='context_reference'
out={'schema':'focal_ig_projection_1','codebook_version':'0.3 unchanged','scope':'Sixteen focal projections across twelve episodes. These use v0.3 distinctions but are not exhaustive annotations, schema-complete v0.3 output, or an independent coding run. Missing components are deliberately not filled. Inference explanations retain source versus analyst role assignments.','units':units}
(ROOT/'analysis/focal_ig_records.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'focal_projections':len(units),'components':sum(len(u['components']) for u in units)}))
