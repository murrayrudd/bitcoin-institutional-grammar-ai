import json,copy
from pathlib import Path
p=json.loads(Path('packet_v2.json').read_text());a=json.loads(Path('annotation.json').read_text());n=json.loads(Path('review_notes.json').read_text());r=json.loads(Path('repair_log.json').read_text())
txt={s['source_id']:s['text'] for s in p['entries']};us={u['unit_id']:u for u in a['units']}
def ev(sid,q,start=0):
 i=txt[sid].index(q,start);return {'source_id':sid,'span':{'start':i,'end':i+len(q),'quote':q}}
def log(kind,uid,before,after,reason):r['repairs'].append({'kind':kind,'unit_id':uid,'before':before,'after':after,'reason':reason})
def make_component(symbol,text,sid,q=None,note=''):
 return {'symbol':symbol,'text':text,'basis':'explicit','evidence':[ev(sid,q or text)],'inference_note':note,'occurrence_role':'local'}
# The endorsed concept is conditional on delay; endorsement is not an activation trigger for delay.
c=next(x for x in us['B01']['components'] if x['symbol']=='Cac');old=copy.deepcopy(c)
c.update(symbol='Cex',text='as a condition of the author\'s concept endorsement',inference_note='The source conditions its ACK on a long interval. This qualifies the inferred expectation; it does not state that an endorsement triggers a duty to defer.')
log('source_review_logical_scope','B01',old,c,'Preserved the direction of the conditional endorsement without inventing an activation condition on the requested delay.')
# A literal navigation instruction embedded in technical background is a focal statement.
sid='32406-178';q='see [`gets()`](https://en.cppreference.com/w/c/io/gets) in C, deprecated in 1999, removed from the standard in 2011, but still usable with current compilers and included in [glibc](https://www.man7.org/linux/man-pages/man3/gets.3.html)'
u=copy.deepcopy(us['B02']);u.update(unit_id='B28',source_id=sid,span=ev(sid,q)['span'],template_note='This is a one-off technical-example referral, not a reusable bot occurrence.')
u['components']=[make_component('I','see',sid),make_component('Bdir','[`gets()`](https://en.cppreference.com/w/c/io/gets)',sid),make_component('Bdir,p','in C, deprecated in 1999, removed from the standard in 2011, but still usable with current compilers and included in [glibc](https://www.man7.org/linux/man-pages/man3/gets.3.html)',sid,note='The full descriptive qualification identifies the example as the author presents it. Dates and continued usability are retained author claims, not independently verified technical facts.')]
u['components'][0]['evidence']=[ev(sid,'see',u['span']['start'])]
u['institution'].update(rationale='An explicit navigation request to inspect a named compatibility example; it remains a technical referral with no supplied obligation or institutional authorization.',evidence=[ev(sid,q)])
u['level_rationale']='The referral supports reasoning in this contribution review, an operational discussion act. It does not assign broader epistemic authority.'
u['alternative_interpretation']='The surrounding compatibility description is technical rationale, but the explicit see instruction is separately executable and is retained under the frozen navigation convention.'
a['units'].append(u);us['B28']=u
log('source_review_omission','B28',None,u,'The final reread identified an explicit see referral inside the technical example. It is extracted separately under the codebook\'s navigation convention.')
# Preserve the direct local non-use recommendation separately from speculation about a developer majority.
q='Here, the reason to recommend not using it';u=copy.deepcopy(us['B08']);u.update(unit_id='B29',span=ev(sid,q)['span'],complexity_flags=['unresolved_reference'])
u['components']=[make_component('D','recommend not',sid,q='recommend not'),make_component('I','using',sid),make_component('Bdir','it',sid,note='It is explicitly the object of using. In this paragraph it refers to the option discussed in the PR; the later this option and nondefault-value formulation help resolve the referent.')]
for c in u['components']:c['evidence']=[ev(sid,c['text'],u['span']['start'])]
u['institution'].update(rationale='The author directly supplies reasons for recommending non-use here. This is distinct in attribution from the later conjecture about the vast majority of developers. The technical harm claims are rationale, not verified outcomes.',evidence=[ev(sid,txt[sid][txt[sid].index(q):txt[sid].index('I think the vast majority')])],recognition=[])
u['alternative_interpretation']='This can be grouped with B08 as one advisory proposition if the direct recommendation, the speculative developer-majority attribution, and the later lower-than-default qualification all remain visible. The literal non-use phrase is broader than the lower-value formulation, so their equivalence is not assumed.'
u['uncertainty_reason']='The relation between non-use of the option and the later narrower advice against a lower-than-default setting is not fully explicit.'
u['confidence']='plausible';a['units'].append(u);us['B29']=u
log('source_review_coverage','B29',None,u,'The final reread separated the author\'s direct local non-use recommendation from the differently attributed and qualified developer-majority claim, preventing silent loss of attribution or scope.')
a['relations'].append({'from_unit_id':'B08','to_unit_id':'B29','type':'clarifies','basis':'context_inferred','evidence':[ev(sid,'Here, the reason to recommend not using it'),ev(sid,us['B08']['span']['quote'])],'logic_scope':'not_applicable','rationale':'The later lower-than-default formulation appears to specify the preceding non-use advice, but it is also a conjecture about others\' views. The relation is contextual, and equivalence of scope is not asserted.'})
# The repeated editorial formulation supplies the documentation scope of the first request.
extra='I think that it would be clearer to users to remove the word "deprecated" from the documentation of this option while preserving the non-recommendation.'
u=us['B22'];old=copy.deepcopy(u['institution']['evidence']);u['institution']['evidence'].append(ev('32714-body',extra));u['institution']['rationale']+=' The later restatement explicitly locates the same substitution in the option documentation while preserving non-recommendation; it is cited as clarification of this edit rather than counted as another edit.'
log('source_review_qualification','B22',old,u['institution']['evidence'],'Cited the later explanatory restatement so the documentation scope and preservation constraint are explicitly recoverable without duplicating the edit.')
# Regenerate focal references and annotated exclusion notes.
for screen in a['entry_screening']:
 screen['unit_ids']=[u['unit_id'] for u in a['units'] if u['source_id']==screen['source_id']]
 if screen['source_id']=='32406-178':
  screen['reason']='Candidate: proposed status interpretation and embedded advice, an explicit technical-example referral, direct local non-use advice and separately attributed nondefault-setting advice, deprecation labeling, removal considerations, current retention recommendation, and two bounded technical fallback strategies. Technical harms and compatibility facts are retained as attributed rationale; future might/can does not establish duty or authority.'
for d in n['per_focal_source_decisions']:
 ss=[u for u in a['units'] if u['source_id']==d['source_id']]
 d['statement_unit_ids']=[u['unit_id'] for u in ss if u['record_role']=='statement'];d['nonstatement_unit_ids']=[u['unit_id'] for u in ss if u['record_role']!='statement']
 d['screening']=next(x['reason'] for x in a['entry_screening'] if x['source_id']==d['source_id'])
 d['alternatives']=[{'unit_id':u['unit_id'],'alternative':u['alternative_interpretation']} for u in ss if u['alternative_interpretation']]
 d['uncertainties']=[{'unit_id':u['unit_id'],'uncertainty':u['uncertainty_reason']} for u in ss if u['uncertainty_reason']]
n['unresolved_interpretive_questions'].append('Does the direct non-use recommendation in 32406-178 mean the same as the later lower-than-default restriction, or is its literal scope broader? The two attributions are retained separately.')
a['episode_summary']['unresolved_questions'].append(n['unresolved_interpretive_questions'][-1])
n['access_log']['own_generated_files_accessed'].append(str(Path.cwd()/'source_review_adjustments.py'))
n['final_source_review']={'completed':True,'scope':'Original complete text of all eight focal entries was reread after the first checks, alongside every retained component, force, role, recognition/disposition event, relation, and mechanism claim. The thread supplement was reviewed before target resolution.','result':'Final adjustments preserve the conditional-ACK direction, extract a missed explicit technical referral, preserve direct versus conjecturally attributed advice, and cite the repeated editorial qualification. Remaining alternatives and uncertainties are retained; no comparison to prior work was attempted.'}
Path('annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n');Path('review_notes.json').write_text(json.dumps(n,ensure_ascii=False,indent=2)+'\n');Path('repair_log.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
