import json, copy, hashlib
from pathlib import Path
from datetime import datetime, timezone

p=json.loads(Path('packet.json').read_text())
a=json.loads(Path('annotation.json').read_text())
entries={e['source_id']:e for e in p['entries']}
us={u['unit_id']:u for u in a['units']}
changes=[]
def ev(s,q=None,start=0):
    t=entries[s]['text'];q=t if q is None else q;i=t.index(q,start)
    return {'source_id':s,'span':{'start':i,'end':i+len(q),'quote':q}}
def record(uid,paths,before,after,reason,evidence,effect='evidence_basis_error',meaning=False,diagnosis='execution_failure_under_existing_rule'):
    changes.append({'change_id':f'R{len(changes)+1:02d}','stage':'single_source_self_review','unit_id':uid,'paths':paths,'before':before,'after':after,'reason':reason,'evidence':evidence,'diagnosis':diagnosis,'effect':effect,'meaning_changed':meaning})

def replace(u,field,value,reason,es,effect='evidence_basis_error',meaning=False,diagnosis='execution_failure_under_existing_rule'):
    before=copy.deepcopy(u[field]);u[field]=value
    record(u.get('unit_id'),[field],before,value,reason,es,effect,meaning,diagnosis)

u=us['F03-U01'];before=copy.deepcopy(u['institution'])
u['institution']['application_evidence'][0]['status']='unresolved'
u['institution']['application_evidence'][0]['rationale']='The retained unmerged head demonstrates a checkbox, checked-state wiring, and a sequence-setting branch in the proposed artifact. It does not verify the complete focal proposition, including placement next to Add Recipient and absence of any GUI replacement path, and supplies no integration evidence. Application of the complete proposed edit is therefore unresolved. The narrower artifact facts remain available as outcome evidence.'
u['institution']['standing_profile']['application']='unresolved'
record(u['unit_id'],['institution.application_evidence[0].status','institution.application_evidence[0].rationale','institution.standing_profile.application'],{'application_evidence':before['application_evidence'],'standing_profile':before['standing_profile']},{'application_evidence':u['institution']['application_evidence'],'standing_profile':u['institution']['standing_profile']},'Partial evidence for an unmerged artifact was too readily summarized as observed application of the entire proposition. The complete placement/function/application claim exceeds the supplied evidence.',u['institution']['application_evidence'][0]['evidence']+[ev('pr7819:metadata','"merged": false')],meaning=True)

u=us['F03-U02']
for i in [0,2]:
    c=u['components'][i];before=copy.deepcopy(c)
    c['basis']='context_inferred';c['occurrence_role']='semantic_inference'
    c['inference_note']=('We is the literal actor of wanting, not an explicitly stated performer of proceed with. Its projected actor role in the reconstructed decision reading is inferred; the group and its decision competence remain unspecified.' if i==0 else 'This is the literal object of want. Its target role under the reconstructed proceed-with action is inferred, although its #7819 referent is unchanged.')
    record(u['unit_id'],[f'components[{i}]'],before,c,'Reconstruction of the action changes the argument-role basis; lexical presence alone does not make the actor or target role explicit.',c['evidence'])

u=us['F03-U06'];before=copy.deepcopy(u['proposition']['qualifiers'])
u['proposition']['qualifiers'].append({'description':'The referent of for it is inferred as the replaceability indication from the immediately following wording concern and the retained confirmation patch.','evidence':[ev('pr7819:comments:1','Also "replaceable" there may have the user thinking that it\'s more replaceable than it is...'),ev('pr7819:patch:1','+        questionString.append(tr("This transaction is replacable (optin-RBF)!"));')],'attachment':'scope_note','linked_unit_id':None,'rationale':'This makes the proposed warning edit’s target explicit without claiming that the unseen screenshots verify it.'})
record(u['unit_id'],['proposition.qualifiers'],before,u['proposition']['qualifiers'],'The edit target was recoverable from context but its contextual attribution needed an attached qualification.',u['proposition']['qualifiers'][-1]['evidence'],effect='coverage_or_scope_loss')

u=us['F03-U08'];s=u['source_id']
# Anchor the modal on the get-red-text predicate, not the matrix should-be predicate.
c=u['components'][0];before=copy.deepcopy(c)
start=entries[s]['text'].index('that should get red text',u['span']['start'])
c['evidence']=[ev(s,'should',start)]
c['governing_span']=ev(s,'the non-replacable case that should get red text',u['span']['start'])
c['inference_note']='The cited should is the modal of get red text in the relative clause. The earlier should governs be and is not used as evidence for this role.'
record(u['unit_id'],['components[0]'],before,c,'The original valid offset cited the wrong should occurrence for the focal formatting predicate.',c['evidence']+[c['governing_span']])
# Avoid using the earlier red-text mention from the different warning predicate.
c=u['components'][3];before=copy.deepcopy(c)
c['evidence']=[ev(s,'red text',u['span']['start'])]
c['governing_span']=ev(s,'the non-replacable case that should get red text',u['span']['start'])
record(u['unit_id'],['components[3]'],before,c,'The semantic-inference anchor had selected the earlier identical red-text phrase outside this proposition. The local occurrence is required even though the intended formatting meaning is unchanged.',c['evidence']+[c['governing_span']])

u=us['F03-U09'];s=u['source_id'];before=copy.deepcopy(u['components'])
newgov=ev(s,'have an "adaptive fee switch" (that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees-- and the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks])',u['span']['start'])
u['components'][2]['evidence']=[ev(s,'have',newgov['span']['start'])]
for c in u['components']:c['governing_span']=copy.deepcopy(newgov)
for i in [0,1]:
    u['components'][i]['occurrence_role']='shared_scope'
    u['components'][i]['inference_note']=('The actor we is stated in the initial alternative and shared by the coordinated have-an-adaptive-fee-switch alternative. It is not a separate local actor occurrence for the second have predicate.' if i==0 else 'Should is stated before the initial have clause and carries the deliberative recommendation across the coordinated switch alternatives. It is shared scope, not a modal locally repeated with the adaptive-fee predicate.')
record(u['unit_id'],['components[0:5].governing_span','components[0].occurrence_role','components[1].occurrence_role','components[2].evidence'],before,u['components'],'The original action anchor selected have a replaceable switch rather than have an adaptive fee switch. The actor and modal are shared across that coordinated alternative, not explicit local occurrences in its governing clause.',[newgov,u['components'][0]['evidence'][0],u['components'][1]['evidence'][0]])

for uid in ['F03-U09','F03-U15']:
    u=us[uid]
    replace(u,'speech_act','question','The wondering-if formulation is an indirect deliberative question in the supplied occurrence; the quoted occurrence preserves that function.',[{'source_id':u['source_id'],'span':u['span']}],effect='convention_deviation',diagnosis='defensible_alternative_representation')

for r in a['relations']:
    if r['from_unit_id']=='F03-U13' and r['to_unit_id']=='F03-U04':
        before=r['rationale'];r['rationale']='The comment’s readiness claim corresponds to and clarifies the intention expressed in the retained body. The body’s incomplete edit history prevents asserting which wording came first.'
        record('F03-U13',['relations[F03-U13 -> F03-U04].rationale'],before,r['rationale'],'The retained body may have later edits, so describing the comment as a later restatement overclaimed textual chronology.',r['evidence'],effect='coverage_or_scope_loss',meaning=True)
    if r['from_unit_id']=='F03-U12' and r['to_unit_id']=='F03-U03':
        before=r['rationale'];r['rationale']='The comment and retained body describe the author’s ongoing replacement-GUI work. This correspondence clarifies the referent without establishing which wording came first or adding independent recognition.'
        record('F03-U12',['relations[F03-U12 -> F03-U03].rationale'],before,r['rationale'],'Correspondence is supported; the retained body does not establish an original-to-repetition chronology.',r['evidence'],effect='coverage_or_scope_loss',meaning=True)

u=us['F03-U04'];before=copy.deepcopy(u['institution']['recognition'][0])
u['institution']['recognition'][0]['rationale']='The same author’s comment expresses a corresponding distinction between replacement development and present review. It demonstrates consistency of personal intent, not interpersonal expectation recognition or a verified order of textual restatement.'
record(u['unit_id'],['institution.recognition[0].rationale'],before,u['institution']['recognition'][0],'The same-actor correspondence is retained without using the body creation date to date its retained sentence.',u['institution']['recognition'][0]['evidence'],effect='coverage_or_scope_loss')

u=us['F03-U17'];before=copy.deepcopy(u['institution']['challenges'])
u['institution']['challenges'][0]['target']='broader_proposal'
u['institution']['challenges'][0]['rationale']='The same author’s fee-only question raises a tentative alternative for the broader replacement-workflow scope. It does not contradict the focal report of having tried additional outputs. The workflow’s canonical proposal identity and any adopted scope decision remain unresolved.'
u['institution']['dispute_present']=False
record(u['unit_id'],['institution.challenges[0].target','institution.challenges[0].rationale','institution.dispute_present'],{'challenges':before,'dispute_present':True},{'challenges':u['institution']['challenges'],'dispute_present':False},'The question about future focus should not be counted as a challenge to the truth or content of the author’s reported earlier attempt.',u['institution']['challenges'][0]['evidence']+[{'source_id':u['source_id'],'span':u['span']}],effect='changed_institutional_meaning',meaning=True)
for r in a['relations']:
    if r['from_unit_id']=='F03-U18' and r['to_unit_id']=='F03-U17':
        before=copy.deepcopy(r);r['type']='clarifies';r['rationale']='The fee-only question qualifies the possible future focus after the report of additional-output experimentation. It does not deny that the attempt occurred or establish that it was withdrawn.'
        record('F03-U18',['relations[F03-U18 -> F03-U17].type','relations[F03-U18 -> F03-U17].rationale'],before,r,'Use a qualification relation instead of a direct focal-proposition challenge because the two utterances concern different temporal/action layers.',r['evidence'],effect='changed_institutional_meaning',meaning=True)

u=us['F03-U19'];before={'scope':u['scope'],'domain':u['proposition']['domain']}
u['scope']='general';u['proposition']['domain']='Implementation of additional-output transaction-replacement workflows, bounded to the technical method discussed in #7819.'
record(u['unit_id'],['scope','proposition.domain'],before,{'scope':u['scope'],'domain':u['proposition']['domain']},'The generic you and confirmation contingency describe the method whenever this additional-output workflow is implemented, even though its discussion is local. Generality remains bounded to this technical workflow, not all project governance.',[ev('pr7819:comments:4')],effect='coverage_or_scope_loss',meaning=True)
u=us['F03-U20'];replace(u,'scope','general','The asserted growth condition concerns repeated uses of the discussed workflow rather than a single observed transaction.',[{'source_id':u['source_id'],'span':u['span']}],effect='coverage_or_scope_loss',meaning=True)

u=us['F03-U21'];c=u['components'][2];before=copy.deepcopy(c)
c['basis']='context_inferred';c['occurrence_role']='semantic_inference';c['inference_note']='Instead of the old word explicitly contrasts the label alternatives. Its execution-constraint role under the reconstructed use action is inferred rather than a local argument of a supplied use predicate.'
record(u['unit_id'],['components[2]'],before,c,'The proposed alternative is explicit, but its role as Cex under an inferred edit action should not be presented as a literal predicate role.',c['evidence'])

u=us['F03-U25'];c=u['components'][1];before=copy.deepcopy(c)
c['evidence'].append(ev('pr7819:supplement_metadata','"url": "https://github.com/bitcoin/bitcoin/pull/7819"'))
c['inference_note']='The object is absent from Needs rebase. The comment is cataloged under #7819, and the supplied canonical-identity metadata anchor resolves the omitted object; neither anchor supplies an explicit local Bdir term.'
record(u['unit_id'],['components[1].evidence','components[1].inference_note'],before,c,'Attach the object-identity evidence directly to the inferred component as well as to its proposition, keeping the nonlocal role visible.',c['evidence'])

Path('annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
Path('annotation.final.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
Path('repair_log.json').write_text(json.dumps({'run_id':'F03_v04_r3','first_complete_preserved':True,'mechanical_repairs':[],'source_review_passes':1,'changes':changes,'change_count':len(changes),'meaning_changed_count':sum(x['meaning_changed'] for x in changes),'notes':'All changes follow the frozen first-complete annotation and first checker result. A mechanical pass did not certify these interpretations.'},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'changes':len(changes),'meaning_changed':sum(c['meaning_changed'] for c in changes)}))
