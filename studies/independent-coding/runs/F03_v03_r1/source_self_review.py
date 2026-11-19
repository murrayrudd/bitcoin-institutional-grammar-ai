import copy, json
from pathlib import Path
R=Path(__file__).resolve().parent
p=json.loads((R/'packet.json').read_text()); a=json.loads((R/'annotation.json').read_text()); log=json.loads((R/'repair_log.json').read_text()); sources={e['source_id']:e for e in p['entries']}; units={u['unit_id']:u for u in a['units']}
def ev(sid,q,start=0):
 t=sources[sid]['text']; s=t.index(q,start); return {'source_id':sid,'span':{'start':s,'end':s+len(q),'quote':q}}
def eu(uid):
 u=units[uid]; return {'source_id':u['source_id'],'span':copy.deepcopy(u['span'])}
def record(cid,field,before,after,reason,kind='epistemic_labeling_error',meaning=False):
 log['changes'].append({'change_id':cid,'phase':'source_self_review','classification':kind,'meaning_changes':meaning,'affected':[field],'before':before,'after':after,'reason':reason})

u=units['F03-U09']; c=next(c for c in u['components'] if c['symbol']=='D'); before=copy.deepcopy(c)
start=sources[u['source_id']]['text'].index('should get',u['span']['start'])
c.update({'basis':'explicit','occurrence_role':'local','evidence':[ev(u['source_id'],'should',start)],'inference_note':'The second should directly marks the recommended red-text treatment. Reconstructing display does not make this lexical modal inferred; the local anchor distinguishes it from the earlier should be.'})
record('R02','F03-U09.components.D',before,copy.deepcopy(c),'The lexical deontic role survives the pragmatic display reconstruction and must remain explicit. The force remains recommendation.')
u=units['F03-U10']; c=next(c for c in u['components'] if c['symbol']=='I'); before=copy.deepcopy(c)
start=sources[u['source_id']]['text'].index('have an',u['span']['start'])
c.update({'basis':'explicit','occurrence_role':'local','evidence':[ev(u['source_id'],'have',start)],'inference_note':'The second have explicitly supplies the positive alternative action. Tentative recommendation force does not make this action inferred, and the anchor excludes its object article.'})
record('R03','F03-U10.components.I',before,copy.deepcopy(c),'The source directly supplies have in the adaptive-option clause. Replaced the broader have an anchor and corrected explicitness without changing the selected design.')
u=units['F03-U06']; c=next(c for c in u['components'] if c['symbol']=='Bdir'); before=copy.deepcopy(c)
c['text']='red styling'; c['inference_note']='The phrase red text is interpreted as red styling to remove from the warning, not as a requirement to delete the warning words. The literal object of deserves is recast as the inferred edit target.'
record('R04','F03-U06.components.Bdir',before,copy.deepcopy(c),'Clarifies the requested removal as the red treatment, preventing a possible reading that all warning text must be deleted. The source criticizes what visual treatment the confirmation window deserves.',kind='substantive_role_precision',meaning=True)
m=a['episode_summary']['mechanisms'][1]; before={'evidence':copy.deepcopy(m['evidence']),'unit_ids':list(m['unit_ids'])}
m['evidence'].append(eu('F03-U23')); m['unit_ids'].append('F03-U23')
record('R05','episode_summary.mechanisms[1].evidence/unit_ids',before,{'evidence':copy.deepcopy(m['evidence']),'unit_ids':list(m['unit_ids'])},'The alternative explanation mentions later interest in output additions; added that exact source evidence and its context endpoint.',kind='evidence_completeness',meaning=False)
o=a['episode_summary']['observed_outcomes'][2]; before=o['claim']
o['claim']='The supplied retained-head confirmation patch still contains red styling and the text "This transaction is replacable (optin-RBF)!". This is evidence of that snapshot, not a dated response to the comments or a rejection of the proposed style, naming, and spelling changes.'
record('R06','episode_summary.observed_outcomes[2].claim',before,o['claim'],'Delimited the exact UI string clearly; no outcome or causal interpretation changed.',kind='presentation_clarity',meaning=False)

(R/'annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
(R/'annotation.final.json').write_bytes((R/'annotation.json').read_bytes())
(R/'repair_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')

# This is the single complete source-based self-review, following the initial checker and its anchor repair.
unit_notes={
'F03-U01':'Retained technical context. Allows describes functionality, not permission. The missing GUI replacement path is explicit. No image rendering is assumed.',
'F03-U02':'Retained uncertain candidate. Withholding acceptance is a pragmatic reconstruction of wanting this without the workflow. We remains the explicit actor of the deliberation; its membership is unknown. The conditional absence and ongoing larger workflow are preserved, without a binding gate.',
'F03-U03':'Retained personal strategy candidate. The full negative-volitional predicate prevents an erroneous positive hold-back instruction. Preference versus commitment remains an alternative; no reviewer duty is inferred.',
'F03-U04':'Retained tentative deferral reading and explicit this target because it remains the object of expose. The until clause preserves the wallet-capability condition. Exact quoted agreement is endorsement, not obligation recognition.',
'F03-U05':'Retained nonstatement container. It has no components and neither target nor observed level; the children carry both visual-edit actions without double counting.',
'F03-U06':'Corrected object wording to red styling, with inferred target role. The source criticizes the warning treatment, not necessarily the warning content. No actor or obligation is invented.',
'F03-U07':'Retained separate exclamation-removal candidate. The negated evaluation and location are shared outside the child, with explicit inference explanations. The separate removal remains technically executable.',
'F03-U08':'Retained plausible naming-revision request with the pure usability-observation alternative. The source subject becomes an inferred edit target. The claimed user confusion is not treated as an observed outcome.',
'F03-U09':'Corrected the red-text evidence to the local occurrence and should to explicit lexical deontic. The display action and non-replacable trigger remain inferred. The fees-cannot-be-updated reason is a source claim, not a verified engineering fact.',
'F03-U10':'Corrected have to an explicit, object-free action anchor. The adaptive design retains future locktimes, multiplicative fee increases, and the full display schedule. The alternative to the replaceable switch is preserved; no plan commitment or XOR requirement is added.',
'F03-U11':'Retained repeated quotation of U04. Removed emphasis in the quote does not create a fresh proposition or independent endorsement.',
'F03-U12':'Retained explicit agreement as a context act and this-proposition endorsement. Agreement with a technical readiness concern does not itself recognize an institutional expectation.',
'F03-U13':'Retained report of work in progress. No completed GUI process or particular implementation is established.',
'F03-U14':'Retained explicitly supplied passive review action and patient this, with unresolved can force. Already states present reviewability; it does not confer authority or make review mandatory.',
'F03-U15':'Retained scheduling-pressure context. A difficult 0.13 timeline does not establish a deadline rule or eventual release inclusion.',
'F03-U16':'Retained complete repeated adaptive-design quotation, linked to U10 without counting another proposal.',
'F03-U17':'Retained tentative response. Might be a solution limits the assent; it is not acceptance for merge or reported implementation.',
'F03-U18':'Retained personal attempted strategy. Was trying preserves temporal and completion limits. Technical allow is not an institutional permission. Editing back in the sendcoins dialog remains the stated workflow.',
'F03-U19':'Retained literal question recommending possible fee-only scope. Maybe, should, and just remain recoverable. No code or governance arrangement is claimed adopted.',
'F03-U20':'Retained engineering-requirement candidate with unresolved technical-versus-institutional force. The child must relate to the original transaction and be usable if the original confirms. The additional-output workflow is inferred contextual activation, not a universal rule.',
'F03-U21':'Retained technical scaling consequence as context. Must compute does not create a sanction or a separate socially authorized obligation. No O relation is justified.',
'F03-U22':'Retained one conditional naming alternative with disjunctive updatable/amendable replacements and descriptive purpose. The proposed-wording presentation is appropriate; no both-label requirement or selected winner is inferred.',
'F03-U23':'Retained limited expression of interest as context and feature-level favorable response. It is now cited for the mechanism alternative that refers to later interest.',
'F03-U24':'Retained one coupled delayed-send option proposal. The label, delay, timeout-dependent avoidance, and possible abort are preserved together. Could is technical capability; the wording tension is unresolved rather than corrected.',
'F03-U25':'Retained fallback spelling request with inferred actor/target roles. Jonas is only the supplied vocative; no account mapping is invented. The truncated spelling stays truncated. Greg\'s suggestion remains an unresolved referent.',
'F03-U26':'Retained elliptical rebase request with inferred action/target and explicit necessity word. The current PR object is recoverable from source context; no particular person, target revision, compliance, or enforcement is inferred.',
'F03-U27':'Retained closure-and-inclusion report as context. The distinct #8182 identity is preserved. Included there is a participant report, not repository merge or verified preservation of every recommendation.'}

flags=[]
for f in json.loads((R/'checks.first.json').read_text())['review_flags']:
 uid=f['unit_id']; sym=f.get('symbol'); key=(uid,sym)
 if key==('F03-U09','Bdir'):
  status='corrected'; rationale='The red text anchor incorrectly pointed to the earlier visual-style criticism. R01 anchors the same inferred target to the local non-replacable-case clause.'; evidence=[ev('pr7819:comments:1','red text',units[uid]['span']['start']),eu(uid)]
 elif key==('F03-U07','I'):
  status='retained'; rationale='The first clause supplies the negated evaluation that syntactically scopes over and the bang. Removal is inferred, not an explicit command, and the nonlocal role is declared.'; evidence=[eu('F03-U05'),eu(uid)]
 elif key==('F03-U07','Cex'):
  status='retained'; rationale='The shared confirmation-window subject supplies the inferred location of both proposed removals; it is accurately marked semantic inference outside the child.'; evidence=[eu('F03-U05'),ev('pr7819:comments:1','the confirmation window')]
 elif key==('F03-U20','Cac'):
  status='retained'; rationale='The same sentence explicitly identifies the additional-output workflow before the child-transaction predicate. Converting that topical scope into a when-implementing condition remains context-inferred.'; evidence=[ev('pr7819:comments:4','workflow for additional outputs is more complex because'),eu(uid)]
 elif key==('F03-U26','Bdir'):
  status='retained'; rationale='The elliptical target is the PR hosting this comment; both packet entries have object_id https://github.com/bitcoin/bitcoin/pull/7819. The body reference is contextual, not local or explicit evidence of an object in Needs rebase.'; evidence=[eu(uid),ev('pr7819:body','this PR')]
 elif key==('F03-U02','A'):
  status='retained'; rationale='We is directly the subject/actor of the deliberative wanting choice, and stays the actor in the tentative acceptance interpretation. The action and object transformation are separately marked inferred; group membership remains unknown.'; evidence=[eu(uid),ev('pr7819:body','we',units[uid]['span']['start'])]
 elif key==('F03-U04','Bdir'):
  status='retained'; rationale='This is explicitly the object of expose. The inferred deferral wraps that same stated exposure action without changing this from another semantic role into an object; the feature antecedent is supplied in the body.'; evidence=[eu(uid),eu('F03-U01')]
 else:
  raise RuntimeError(f'Unresolved checker flag handler {f}')
 flags.append({'flag':f,'status':status,'rationale':rationale,'evidence':evidence})

review={'run_id':'F03_v03_r1','review_count':1,'review_type':'complete source-based self-review after first-complete freeze and mechanical feedback','source_scope':'All 19 supplied entries reread; exhaustive omission review of all 10 focal entries, context screening for all 9 supplements. No external or post-dispatch source was added.',
'checker_flag_resolutions':flags,
'entry_review':[{'source_id':e['source_id'],'status':'retained','evidence':[ev(e['source_id'],e['text'])] if e['text'] else [],'assessment':next(s['reason'] for s in a['entry_screening'] if s['source_id']==e['source_id'])} for e in p['entries']],
'unit_review':[{'unit_id':uid,'status':'corrected' if uid in ['F03-U06','F03-U09','F03-U10'] else 'retained','evidence':[eu(uid)],'assessment':note} for uid,note in unit_notes.items()],
'relation_review':[{'from_unit_id':r['from_unit_id'],'to_unit_id':r['to_unit_id'],'type':r['type'],'status':'unresolved' if r['basis']=='unresolved' else 'retained','evidence':r['evidence'],'assessment':r['rationale']+' Direction, basis, source identity, and endpoint roles were checked. No causal or obligation claim is inferred beyond the relation.'} for r in a['relations']],
'recognition_review':[{'unit_id':u['unit_id'],'kind':r['kind'],'target':r['target'],'status':'unresolved' if r['target']=='unresolved' else 'retained','evidence':r['evidence'],'assessment':r['rationale']+' None is counted as expectation_recognition, so no locally_supported standing is assigned.'} for u in a['units'] for r in u['institution']['recognition']],
'disposition_review':{'status':'retained','unit_ids':[u['unit_id'] for u in a['units'] if u['disposition_events']],'evidence':a['units'][1]['disposition_events'][0]['evidence'],'assessment':'All 16 disposition events refer only to the broader #7819 contribution and use recorded_closed_unmerged. No per-proposition rejection, implementation, or acceptance is inferred. #8182 closure is confined to its separately identified summary evidence.'},
'authority_and_levels_review':{'status':'retained','evidence':[eu('F03-U03'),eu('F03-U19'),eu('F03-U26'),eu('F03-U27')],'assessment':'No attributable authorization, recognized rule-making procedure, or enforcement chain is supplied. Candidate statements concern operations on this contribution or its design/review. Technical feature choices do not establish collective-choice changes to recurring governance; no constitutional or epistemic activity is supported. Speaker handles are not evidence of maintainer status.'},
'outcome_review':[{'index':i,'status':'corrected' if i==2 else 'retained','claim':o['claim'],'evidence':o['evidence'],'assessment':'Every factual clause is limited to the supplied text or identified object metadata. Participant reports, retained-head state, closure, repository integration, and network adoption are not conflated.'} for i,o in enumerate(a['episode_summary']['observed_outcomes'])],
'mechanism_review':[{'index':i,'status':'corrected' if i==1 else 'retained','claim':m['claim'],'evidence':m['evidence'],'assessment':'Checked initiation, response, available intervening acts, and outcome bounds. Status describes textual correspondence or consistency, not causal identification. The alternative explanation is preserved.'} for i,m in enumerate(a['episode_summary']['mechanisms'])],
'additional_findings':[{'change_id':c['change_id'],'classification':c['classification'],'meaning_changes':c['meaning_changes'],'reason':c['reason']} for c in log['changes']],
'limitations_retained':a['episode_summary']['missing_evidence']+a['episode_summary']['unresolved_questions'],
'conclusion':'The structural checker passes, but source interpretation remains bounded and revisable. No claim of semantic certification or full-corpus validity follows.'}
(R/'review_notes.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'self_reviews':1,'changes':len(log['changes']),'checker_flags_resolved':len(flags),'units_reviewed':len(unit_notes),'sources_reviewed':len(p['entries'])}))
