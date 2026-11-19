import json,hashlib,copy
from pathlib import Path
p0=json.loads(Path('packet.json').read_text());p=json.loads(Path('packet_v2.json').read_text())
assert p['episode_id']==p0['episode_id'] and p['selection_design']==p0['selection_design']
assert p['entries'][:-1]==p0['entries']
assert p['entries'][-1]['source_id']=='T32359_038_053'
a=json.loads(Path('annotation.json').read_text());n=json.loads(Path('review_notes.json').read_text());r=json.loads(Path('repair_log.json').read_text())
txt={s['source_id']:s['text'] for s in p['entries']};us={u['unit_id']:u for u in a['units']}
def ev(sid,q,start=0):
 i=txt[sid].index(q,start);return {'source_id':sid,'span':{'start':i,'end':i+len(q),'quote':q}}
def component(uid,symbol):return next(c for c in us[uid]['components'] if c['symbol']==symbol)
def log(kind,uid,old,new,why):r['repairs'].append({'kind':kind,'unit_id':uid,'before':old,'after':new,'reason':why})
# Exact anchor and explanatory omissions found by the unchanged checker.
c=component('B11','I');old=copy.deepcopy(c)
c['evidence'][1]=ev('32406-178','in',txt['32406-178'].index('leaving the option in')+len('leaving the option '))
log('mechanical_anchor','B11',old,c,'The original search matched in inside leaving. It now anchors the separate particle in after the complete object.')
c=component('B19','Bind');old=copy.deepcopy(c)
c['inference_note']='The explicit destination of do so remains the destination of the recovered debate action; no argument-role transformation is introduced.'
log('mechanical_explanation','B19',old,c,'Added the role-preservation explanation required for an explicit destination in a pragmatic parse.')
for uid in ['B19','B20']:
 c=component(uid,'A');old=copy.deepcopy(c)
 c['evidence']=[ev('32406-252','you',txt['32406-252'].index('If you want to debate this comment'))]
 log('source_review_anchor',uid,old,c,'The initial search found you in the earlier optional-venue clause. The final anchor is the you in the actual debate-condition governing these duties.')
# Preserve the decision criterion without implying a recommendation to remove the option.
u=us['B10'];old=copy.deepcopy(u['components']);q=u['span']['quote'];u['parse_mode']='pragmatic'
u['components']=[
 {'symbol':'I','text':'decide','basis':'context_inferred','evidence':[ev('32406-178',q)],'occurrence_role':'semantic_inference','inference_note':'The focal action of deciding is reconstructed from Whether (or when) ... depends on; the sentence does not itself recommend removal.'},
 {'symbol':'Bdir','text':'Whether (or when) the option should also be removed rather than just deprecated','basis':'context_inferred','evidence':[ev('32406-178','Whether (or when) the option should also be removed rather than just deprecated')],'occurrence_role':'semantic_inference','inference_note':'The clause is the grammatical subject of depends, and becomes the informational object of inferred decide. Its should is internal to the unresolved decision, not an explicit D on decide.'},
 {'symbol':'Cex','text':'weigh user appreciation, maintenance effort, and perhaps harmful network effects','basis':'context_inferred','evidence':[ev('32406-178','depends on the trade-off between how many users continue to appreciate the feature, and how much effort it is to continue to support the code, and, perhaps, whether the presence of the feature is resulting in any harmful network effects.')],'occurrence_role':'semantic_inference','inference_note':'The explicit dependency becomes the inferred decision method/constraint. Perhaps keeps harmful network effects optional; there is no invented activation threshold.'}
]
log('source_review_refinement','B10',old,u['components'],'The action is deciding whether/when, with a trade-off criterion; the first parse risked turning a decision dependency into a recommendation to remove.')
c=component('B13','A');old=copy.deepcopy(c);c['text']='they';c['basis']='explicit';c['inference_note']='They is the grammatically shared subject of patch and use in the coordinated sentence. Users supplies the antecedent; the actor role is explicit under both verbs.'
log('source_review_role','B13',old,c,'Preserved the explicit grammatically shared actor role in the literal coordinated alternatives.')
# Coordinator-approved packet amendment resolves the report target, without proving the exact wording.
a['packet_sha256']=hashlib.sha256(Path('packet_v2.json').read_bytes()).hexdigest()
a['entry_screening'].append({'source_id':'T32359_038_053','disposition':'context_only','reason':'Supporting context outside focal extraction scope; supplied thread metadata establishes the in_reply_to relation for the requested uptake check.','unit_ids':[]})
metaev=ev('T32359_038_053',txt['T32359_038_053'])
u=us['B14'];old=copy.deepcopy({'recognition':u['institution']['recognition'],'disposition':u['disposition_events'],'uncertainty':u['uncertainty_reason']})
u['uncertainty_reason']='The thread metadata identifies Added comment as a reply to this exact snippet in src/test/transaction_tests.cpp. The source change itself is not supplied, so exact inserted wording remains unverified.'
u['confidence']='clear'
for event in u['institution']['recognition']+u['disposition_events']:
 if event['kind'] in ['reported_implementation','reported_implemented']:
  event.update(target='this_proposition',basis='context_inferred',evidence=[ev('32359-053','Added comment.'),metaev],rationale='The added thread metadata gives 32359-053 in_reply_to_id 2063718969, matching 32359-038, in the same src/test/transaction_tests.cpp path. The author specifically reports adding the proposed comment, but exact inserted wording is not verified by a file diff.')
for rel in a['relations']:
 if rel['from_unit_id']=='B14' and rel['to_unit_id']=='C053':
  rel.update(basis='context_inferred',evidence=[ev('32359-038',txt['32359-038']),ev('32359-053','Added comment.'),metaev],rationale='Thread metadata directly links the author\'s Added comment reply to this inline snippet. It supports proposition-specific reported implementation, not verification of exact wording or a causal effect beyond the attributable reply.')
log('authorized_source_amendment','B14',old,{'recognition':u['institution']['recognition'],'disposition':u['disposition_events'],'uncertainty':u['uncertainty_reason']},'The coordinator supplied the specifically requested thread metadata in packet_v2.json before finalization; no prior annotation was disclosed.')
a['episode_summary']['observed_outcomes'][0]={'claim':'Thread metadata links petertodd\'s Added comment reply directly to the focal proposed comment in src/test/transaction_tests.cpp. This supports proposition-specific reported implementation without verifying exact inserted wording. The broader PR 32359 is recorded closed unmerged.','evidence':[ev('32359-038',txt['32359-038']),ev('32359-053','Added comment.'),metaev,ev('M32359',txt['M32359'])]}
a['episode_summary']['mechanisms'].insert(0,{'category':'review_coordination','claim':'Sjors provides proposed source-comment wording, and petertodd replies Added comment in the same identified thread. This is an attributable review-to-reported-edit sequence; the packet does not expose the final source comment.','evidence':[ev('32359-038',txt['32359-038']),ev('32359-053','Added comment.'),metaev],'unit_ids':['B14','C053'],'alternative_explanation':'The author may have implemented an equivalent comment rather than copying the wording exactly; the report cannot distinguish those cases.','status':'supported_sequence'})
a['episode_summary']['missing_evidence'][0]='Thread metadata resolves the 32359-053 reply target as 32359-038. A changed file or commit diff verifying the exact inserted comment remains unavailable.'
a['episode_summary']['unresolved_questions'][-1]='Was the proposed source comment copied exactly or implemented with equivalent wording? The specifically requested thread supplement resolves the reply target.'
# Carry amended decisions into the notes, with explicit access and amendment provenance.
n['packet_sha256']=a['packet_sha256'];n['missing_context']=a['episode_summary']['missing_evidence'];n['unresolved_interpretive_questions']=a['episode_summary']['unresolved_questions'];n['source_grounded_response_sequences']=a['episode_summary']['mechanisms']
for d in n['per_focal_source_decisions']:
 ss=[u for u in a['units'] if u['source_id']==d['source_id']]
 d['alternatives']=[{'unit_id':u['unit_id'],'alternative':u['alternative_interpretation']} for u in ss if u['alternative_interpretation']]
 d['uncertainties']=[{'unit_id':u['unit_id'],'uncertainty':u['uncertainty_reason']} for u in ss if u['uncertainty_reason']]
n['source_amendment']={'request':'Does 32359-053 (Added comment; discussion_r2064478495) have an in_reply_to/thread link to focal 32359-038 (discussion_r2063718969)?','new_source_id':'T32359_038_053','source_quote':txt['T32359_038_053'],'packet_used':'packet_v2.json','original_packet_sha256':hashlib.sha256(Path('packet.json').read_bytes()).hexdigest(),'amended_packet_sha256':a['packet_sha256'],'provenance':json.loads(Path('supplement_provenance.json').read_text()),'effect':'Changed reported implementation and uptake target from unresolved to this_proposition, context_inferred, supported by the explicit reply identifier. Exact wording remains unverified.'}
for f in ['packet_v2.json','thread_metadata_supplement.json','supplement_provenance.json']:n['access_log']['research_inputs_accessed'].append(str(Path.cwd()/f))
for f in ['finalize_annotation.py','final_source_review.txt']:n['access_log']['own_generated_files_accessed'].append(str(Path.cwd()/f))
r['final_packet']='packet_v2.json';r['final_packet_sha256']=a['packet_sha256']
r['note']='The first completed annotation and unchanged-checker feedback remain in annotation_first_complete.json and checks_first.json. The listed edits address checker findings, source reread precision, and the requested bounded metadata amendment.'
Path('annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n');Path('review_notes.json').write_text(json.dumps(n,ensure_ascii=False,indent=2)+'\n');Path('repair_log.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'packet':'packet_v2.json','sha256':a['packet_sha256'],'entries':len(a['entry_screening']),'repairs':len(r['repairs'])},indent=2))
