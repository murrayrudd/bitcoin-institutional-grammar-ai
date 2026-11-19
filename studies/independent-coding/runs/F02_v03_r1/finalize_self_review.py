import json,copy,hashlib,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
p=json.loads((ROOT/'packet.json').read_text())
texts={e['source_id']:e['text'] for e in p['entries']}
entries={e['source_id']:e for e in p['entries']}
a=json.loads((ROOT/'annotation.json').read_text())
first=json.loads((ROOT/'annotation.first_complete.json').read_text())
assert a==first, 'Self-review must start from preserved first-complete annotation.'
flags=json.loads((ROOT/'checks.first.json').read_text())['review_flags']
def ev(short,q=None):
 s='pr14441:'+short;t=texts[s];q=t if q is None else q;pos=t.index(q)
 return {'source_id':s,'span':{'start':pos,'end':pos+len(q),'quote':q}}
byid={u['unit_id']:u for u in a['units']}
repairs=[]
# The source review found a narrow distinction between a paragraph referent and
# the reviewer's reason for criticizing it; the unseen paragraph is not supplied.
u=byid['F02-S02']; c=next(c for c in u['components'] if c['symbol']=='Bdir,p')
before=copy.deepcopy(c)
c['text']='This paragraph'
c['evidence']=[ev('review_comments:1','This paragraph')]
c['inference_note']='The demonstrative phrase in the preceding sentence, outside the minimal edit-proposition span, resolves it as the paragraph being criticized. The statement about both behaviors being present in the same release is the reviewer\'s reason for the criticism; the absent original paragraph is not asserted to contain any particular wording. That rationale is retained separately as institutional evidence and is not an activation condition on the edit.'
u['institution']['evidence'].append(ev('review_comments:1',"This paragraph doesn't really make sense when both behaviors are present in the same release."))
repairs.append({'change_id':'SR-01','phase':'single_source_self_review','affected_unit_ids':['F02-S02'],
'fields':['components[Bdir,p]','institution.evidence'],
'category':'local_semantic_overstatement','meaning_changes':True,'institutional_interpretation_changes':False,
'before':before,'after':copy.deepcopy(c),
'reason':'The first-complete paraphrase described the paragraph as about both behaviors in the same release. The source supplies that coexistence as a reason for criticism, without reproducing the old paragraph. The final representation narrows the inferred antecedent to This paragraph and retains the full reason separately. Actor, action, object identity, tentative force, complete replacement wording, standing, and governance level remain unchanged.',
'evidence':[ev('review_comments:1')],
'added_evidence':u['institution']['evidence'][-1]})
# Declarative technical assent is not an edit report or an ACK token.
u=byid['F02-C07'];before=u['speech_act'];u['speech_act']='asserted'
repairs.append({'change_id':'SR-02','phase':'single_source_self_review','affected_unit_ids':['F02-C07'],
'fields':['speech_act'],'category':'speech_act_convention','meaning_changes':False,'institutional_interpretation_changes':False,
'before':before,'after':'asserted',
'reason':'Both are good changes is a declarative assessment. It endorses unnamed technical changes but does not itself report an edit. Its context role, unresolved target, nondeontic force, and lack of expectation recognition are retained.',
'evidence':[ev('review_comments:4')]})
encoded=json.dumps(a,ensure_ascii=False,indent=2)+'\n'
(ROOT/'annotation.json').write_text(encoded)
(ROOT/'annotation.final.json').write_text(encoded)
(ROOT/'repair_log.json').write_text(json.dumps({'run_id':'F02_v03_r1','mechanical_repairs':[], 'source_review_passes':1,'changes':repairs,'first_complete_sha256':hashlib.sha256((ROOT/'annotation.first_complete.json').read_bytes()).hexdigest(),'final_sha256':hashlib.sha256(encoded.encode()).hexdigest()},ensure_ascii=False,indent=2)+'\n')

flag_results=[]
for i,f in enumerate(flags):
 u=byid[f['unit_id']]; c=next(c for c in u['components'] if c['symbol']==f['symbol'])
 evidence=copy.deepcopy(c['evidence'])
 if f['kind']=='pragmatic_explicit_argument':
  explanation=('Retained explicit Bdir: it is the object of the explicitly supplied verb change both in the hypothetical formulation and in the request reading. The actor shifts under pragmatic interpretation, but the direct-object role does not. Antecedent resolution is separately inferred.' if u['unit_id']=='F02-S02' else 'Retained explicit Bdir: the empty string change is directly governed by document in both the literal appraisal and the recommendation reading. I is only the subject of think and is not mislabeled as the documenting actor.')
  status='retained'
 elif u['unit_id']=='F02-S02' and c['symbol']=='Bdir,p':
  explanation='Corrected the overdescriptive paraphrase and narrowed the component anchor to This paragraph. The outside-unit antecedent reference remains necessary and is explicitly explained. The full prior sentence is retained as rationale evidence, not as an asserted description of unavailable old wording.'
  status='corrected'
 elif c['symbol']=='A':
  explanation=c['inference_note']+' Source author attribution is part of the supplied entry metadata. This is an inferred participant/addressee assignment, not an inferred occupational role or a claim that compliance proves authority.'
  status='retained'
 else:
  explanation='Retained inferred Bdir with context_reference: the object omitted after drop is resolved from the immediately preceding unique check description. That earlier phrase is a subject of changes; the final coding expressly marks its Bdir assignment context_inferred. Context_reference here records antecedent resolution, while the note makes the role reconstruction explicit. A semantic_inference occurrence label is a defensible alternative with the same epistemic basis and referent.'
  status='retained'
 flag_results.append({'first_checker_flag_index':i,'flag':f,'status':status,'rationale':explanation,'evidence':evidence})

unit_review=[]
notes={
'F02-C01':'Retained context: descriptive backport/revert/fix attribution does not articulate a separate action request. Mentioned PRs remain distinct objects with no imported histories.',
'F02-C02':'Retained aggregate implementation context. The source identifies @ryanofsky and the author reports updating this PR. No exact documentation wording or institutional expectation is thereby verified.',
'F02-C03':'Retained ACK context. Preserve 89306ab as supplied; do not replace the abbreviated source token or claim an unstated test result.',
'F02-C04':'Retained ACK plus technical-comparison context. The full commit URL remains intact. Different code to achieve the same functionality and a largely clean test backport are descriptive claims about this contribution, not a prescribed procedure.',
'F02-C05':'Retained initial ACK context. The review-state APPROVED is attributable metadata about this action, not proof of a governing approval rule or reviewer authority.',
'F02-C06':'Retained later review context and bounded target-update relation. The full hash differs from the earlier one. The explicit since last review statement supports linkage, with contextual mapping to the supplied earlier review; no changed judgment or required reapproval.',
'F02-S01':'Retained pragmatic spelling correction. I=write and Bdir roles are explicitly inferred, D=Should is advisory, and the complete listtransactions plus final-s qualification survives. The inferred addressee is supported by the author\'s attributed update report. A literal technical-correctness alternative remains open; no norm or rule authority is inferred.',
'F02-S02':'Retained one edit proposition beginning at I\'d maybe, with full proposed replacement wording. Explicit change/it roles survive the pragmatic force shift; A is inferred because the literal I refers to the reviewer. Narrowed the antecedent property without losing the separate rationale. Both with/without setting conditions, outgoing/incoming distinctions, and accounts-versus-labels rationale remain inside Cex as edit content. I\'d maybe is not a commitment or obligation.',
'F02-S03':'Retained literal proposed drop action, with inferred omitted object and addressee. New check for "*" here, clarity purpose, and unless I\'m missing something all survive. Cac codes an explicit applicability reservation; Cex is a retained decomposition alternative. Maybe remains tentative. The uniquely matching response supports specific reported acceptance/removal, not enforcement or an independently reconstructed patch transition.',
'F02-S04':'Retained one pragmatic document recommendation with explicit document and its direct object. The source I thinks and is not the literal documenting actor. Complete optional Maybe wording includes backwards compatibility, setting-dependent empty-string results, and the confusion rationale. Possible is technical capability, and error is software behavior; neither becomes an institutional permission or consequence.',
'F02-C07':'Corrected speech_act to asserted for the declarative assessment Both are good changes. Target ambiguity remains: no reliable thread identifies the endorsed pair. No proposition-specific acceptance or expectation recognition is assigned.',
'F02-C08':'Retained reported-action context for fixed. Its source path supports only release-note relevance; it does not identify which particular correction. No precise uptake relation or application relation is manufactured.',
'F02-C09':'Retained response/removal-report context. The explicit check for "*" supplies correspondence to S03, including technical agreement and the author\'s reported edit. The response contains no separate command or recurring expectation.'}
for u in a['units']:
 unit_review.append({'unit_id':u['unit_id'],'status':'corrected' if u['unit_id'] in ['F02-S02','F02-C07'] else 'retained','reviewed_dimensions':['screening_and_boundaries','qualifiers_and_negation','predicate_roles_and_basis','speech_and_presentation','force_and_institutional_standing','recognition_authority_and_application','disposition_target','governance_levels'],'assessment':notes[u['unit_id']],'evidence':[{'source_id':u['source_id'],'span':u['span']}]+(u['institution']['evidence'][-1:] if u['unit_id']=='F02-S02' else [])})

screen_review=[]
for sc in a['entry_screening']:
 ent=entries[sc['source_id']]
 screen_review.append({'source_id':sc['source_id'],'focal_exhaustive':sc['source_id'] in p['selection_design']['focal_source_ids'],'status':'retained','disposition':sc['disposition'],'assessment':sc['reason'],'evidence':[{'source_id':sc['source_id'],'span':{'start':0,'end':len(ent['text']),'quote':ent['text']}}] if ent['text'] else [],'empty_body_verified':not bool(ent['text'])})

relation_review=[]
for i,r in enumerate(a['relations']):
 relation_review.append({'relation_index':i,'from_unit_id':r['from_unit_id'],'to_unit_id':r['to_unit_id'],'type':r['type'],'status':'retained','assessment':r['rationale'],'basis_audit':'context_inferred retained: attributed correspondence supports the mapping, while no exact quoted target or complete thread metadata is supplied. Source timestamps support recorded ordering only; they do not identify causation.','evidence':r['evidence']})
event_review=[]
for u in a['units']:
 for field in ['institution.recognition','disposition_events']:
  events=u['institution']['recognition'] if field=='institution.recognition' else u['disposition_events']
  for i,x in enumerate(events):
   event_review.append({'unit_id':u['unit_id'],'field':field,'event_index':i,'kind':x['kind'],'target':x['target'],'basis':x['basis'],'status':'retained','assessment':x['rationale'],'evidence':x['evidence']})

outcome_reviews=[]
for i,o in enumerate(a['episode_summary']['observed_outcomes']):
 assessment=[
  'The exact merged boolean and merged_at date come from original metadata; base and merge_commit_sha come from the labeled supplement. The source objects agree on PR #14441. No network adoption or authorization is extrapolated.',
  'The two attributed reports support the exact update/ACK claims and full revision identifier. Later ordering uses supplied source timestamps (07:40:49 then 07:57:22 UTC) and remains contextual; complete edit chronology is not claimed.',
  'The initiation evidence includes Maybe, for clarity, and the unless reservation; the response names the same check and reports removal. After refers to recorded comment order, not independent observation of the code edit.',
  'The three review comments and retained release-note patch support the content correspondence. The patch uses label/account/dummy without identical inline-code formatting and revises wording about usefulness/confusion; the claim expressly avoids verbatim-copy or causal attribution.',
  'Both terse responses are quoted directly and their doc/release-notes.md source paths are supplied. Neither contains an explicit antecedent; the missing reliable threading is a source-packet limit. The outcome retains that uncertainty.'
 ][i]
 outcome_reviews.append({'outcome_index':i,'status':'retained','claim':o['claim'],'assessment':assessment,'evidence':o['evidence']})
mechanism_reviews=[]
for i,m in enumerate(a['episode_summary']['mechanisms']):
 mechanism_reviews.append({'mechanism_index':i,'status':'retained','classification':m['status'],'assessment':('Initiation, clarity rationale, epistemic reservation, matching author agreement, and removal report all have exact source support. The sequence is supported by matching content and recorded order; causation and enforcement are not claimed.' if i==0 else 'All four initiation types, aggregate author update, earlier/later revision distinction, and later reviewer characterization are cited. The outcome remains aggregate reported revision and continued review. Every listed unit exists, direction is correct, and no exact implementation of all wording or mandatory approval gate is asserted.'),'alternative_explanation_review':m['alternative_explanation'],'evidence':m['evidence']})

review={
'run_id':'F02_v03_r1','episode_id':'F02','source_self_review_passes':1,'completed_at_utc':datetime.now(timezone.utc).isoformat(),
'method':'After the first-complete freeze and first checker, reread all 22 supplied entry texts with source metadata, the complete focal coding, all relations, every recognition/disposition event, and all summary claims. No new sources or other coder outputs were accessed. Structural checking is not semantic certification.',
'coverage':{'screened_entries':len(a['entry_screening']),'focal_entries':len(p['selection_design']['focal_source_ids']),'supplemental_entries':len(p['entries'])-len(p['selection_design']['focal_source_ids']),'units':len(a['units']),'statement_units':sum(u['record_role']=='statement' for u in a['units']),'relations':len(a['relations']),'recognition_and_disposition_events':len(event_review),'observed_outcomes':len(outcome_reviews),'mechanisms':len(mechanism_reviews)},
'checker_flags':flag_results,
'entry_screening_review':screen_review,
'unit_review':unit_review,
'relation_review':relation_review,
'recognition_and_disposition_review':event_review,
'authority_and_application_review':{'status':'retained','assessment':'None of the four recommendations supplies an authorization provision, an attributed rule-making arrangement, an enforcement claim, or proposition-specific expectation recognition. Technical assent, aggregate implementation, and merge status therefore leave type undetermined and standing text_only. No authorizes, applies, or O relation is justified; technical software error behavior is not an institutional sanction. The packet does not establish an actor\'s maintainer status or power from an ACK, authorship, or merger alias.','evidence':[ev('review_comments:0'),ev('review_comments:1'),ev('review_comments:2'),ev('review_comments:3'),ev('comments:0'),ev('review_comments:6'),ev('metadata','"merged": true')]},
'governance_level_review':{'status':'retained','assessment':'All four focal recommendations concern immediate contribution edits, with operational target and observed levels. The proposed documentation describes software behavior and does not revise a recurring contribution procedure. No evidence supports collective-choice, constitutional, or epistemic governance. Context records have not_applicable target levels; no constitutive grammar or authority claim is inferred from RPC labels or parameter names.','evidence':[ev('review_comments:0'),ev('review_comments:1'),ev('review_comments:2'),ev('review_comments:3')]},
'outcome_review':outcome_reviews,'mechanism_review':mechanism_reviews,
'changes':['SR-01','SR-02'],
'unresolved_limits':a['episode_summary']['missing_evidence'],
'unresolved_source_targets':[
 {'status':'unresolved','claim':'The two changes endorsed by Both are good changes are not individually identified.','evidence':[ev('review_comments:4')]},
 {'status':'unresolved','claim':'The particular edit reported by fixed is not identified.','evidence':[ev('review_comments:5')]}
],
'first_complete_preservation':{'sha256':hashlib.sha256((ROOT/'annotation.first_complete.json').read_bytes()).hexdigest(),'unchanged':hashlib.sha256((ROOT/'annotation.first_complete.json').read_bytes()).hexdigest()==json.loads((ROOT/'first_complete_freeze.json').read_text())['annotation_first_complete_sha256']},
'final_checker':None
}
(ROOT/'review_notes.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'self_review_passes':1,'changes':len(repairs),'meaning_changing_local_repairs':sum(r['meaning_changes'] for r in repairs),'institutional_conclusion_changes':sum(r['institutional_interpretation_changes'] for r in repairs),'checker_flags_resolved':len(flag_results),'recognition_and_disposition_events_reviewed':len(event_review)}))
