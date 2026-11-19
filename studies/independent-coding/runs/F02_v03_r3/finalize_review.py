from pathlib import Path
import json, hashlib
from collections import Counter
ROOT=Path(__file__).resolve().parent
pkt=json.loads((ROOT/'packet.json').read_bytes())
a=json.loads((ROOT/'annotation.json').read_bytes())
first=json.loads((ROOT/'annotation.first_complete.json').read_bytes())
checks=json.loads((ROOT/'checks.first.json').read_bytes())
entries={e['source_id']:e for e in pkt['entries']}
by={u['unit_id']:u for u in a['units']}

def evidence(source,quote=None):
    t=entries[source]['text']
    start=0 if quote is None else t.index(quote)
    q=t if quote is None else quote
    return {'source_id':source,'span':{'start':start,'end':start+len(q),'quote':q}}
def E(short,quote=None): return evidence('pr14441:'+short,quote)

old=a['episode_summary']['observed_outcomes'][1]['claim']
new='The author agrees that behavior would be identical with or without the check for "*" and reports removing it. The packet does not establish the timing of the edit relative to the author\'s agreement or reconstruct the exact intermediate patch reviewed.'
a['episode_summary']['observed_outcomes'][1]['claim']=new
repairs=[{'change_id':'R01','stage':'single_source_self_review','path':'/episode_summary/observed_outcomes/1/claim',
 'before':old,'after':new,'meaning_changed':True,'institutional_conclusion_changed':False,
 'classification':'substantive_evidence_scope_correction',
 'reason':'The initial after agreeing wording could assert a temporal ordering of private agreement and the edit. One response supplies agreement and a past-tense removal report but does not establish that ordering. The correction preserves the supported report while removing the excess chronology.',
 'evidence':[E('review_comments:6')]}]

unit_notes={
 'C00':'Retained as technical description of a proposed backport. PR submission is operational context, but the body supplies no independently worded instruction or commitment. Do not turn Fixes #14382 into a verified outcome of that external object.',
 'C01':'Retained as a broad author update report. The specific reviewer is named, supporting inferred response attribution. The report verifies neither every requested wording nor an expectation to obey reviewers.',
 'C07':'Retained as an independent participant endorsement of the abbreviated commit. No obligatory force, authority, testing claim, or particular suggestion target is supplied.',
 'C08':'Retained endorsement and technical backport explanation. Comparison with other PRs does not prescribe a recurring backport process. The complete supplied commit URL is preserved.',
 'C02':'Retained earlier review endorsement at the complete named commit. APPROVED metadata and utACK do not by themselves establish reviewer authority or institutional authorization.',
 'C03':'Retained later review endorsement and change report. Same author and phrase last review support the context-inferred review-target-update edge; neither changed judgment nor obligatory re-review is claimed.',
 'S01':'Retained one elliptical correction. The complete desired identifier and with-s qualification survive. Write and the Bdir role are inferred under the edit parse; advisory Should is not promoted to a binding rule. The later broad update supports a possible reviser without making that actor explicit. No additional hidden singular token is invented.',
 'S02':'Retained one paragraph-replacement proposal. The exact action change and pronoun object it are explicit in the literal hypothetical I would change construction; I is the grammatical pronoun within the contraction I\'d, not an unrelated substring. This is a tentative recommendation, not a personal commitment. The entire replacement content preserves both RPC modes, transaction directions, and account/label rationale. An alternate recipient-oriented pragmatic actor parse remains stated.',
 'S03':'Retained one defeasible removal request. Drop is explicit, while the object is inferred from the prior clause and the actor from the specific response. The new-check qualifier, purpose for clarity, and unless-I-am-missing-something condition survive. The author agreement supports local acceptance and a reported edit, not expectation recognition. The technical side effect is not an O sanction.',
 'S04':'Retained one documentation request with its proposed technical wording. The reviewer is subject of think, not an explicit actor of document. Document and the empty string change retain explicit predicate/object roles. The full conditional behavior, empty-string token, backward-compatibility purpose and confusion/usefulness explanation remain in Cex. Possible to pass is technical capability, not authorized discretion.',
 'C04':'Retained one ACK-like endorsement context. Both has no uniquely established pair among the release-note suggestions. Its uncertain target is not replaced with broader_proposal or counted as two separate endorsements.',
 'C05':'Retained one reported-fix context. The absent object and unreliable threading leave its target unresolved. No individual suggestion receives an unsupported disposition based on this word.',
 'C06':'Retained specific agreement/removal-report context. Shared check-for-star wording provides correspondence with S03. This supports reported uptake, not exact reconstruction of an intermediate code edit or a general review-compliance expectation.'}

screen_review=[]
for s in a['entry_screening']:
    source=s['source_id']; ent=entries[source]
    is_focal=source in pkt['selection_design']['focal_source_ids']
    screen_review.append({'source_id':source,'scope':'exhaustive_focal' if is_focal else 'supplemental_context_screen',
      'status':'retained','disposition':s['disposition'],'unit_ids':s['unit_ids'],
      'finding':s['reason'],'evidence':[] if ent['text']=='' else [evidence(source)],
      'empty_text_verified':ent['text']==''})

flag_resolutions=[]
for i,f in enumerate(checks['review_flags']):
    uid=f['unit_id']; sym=f['symbol']; u=by[uid]
    c=next(c for c in u['components'] if c['symbol']==sym)
    explanations={
      ('S01','A'):'Retained outside-unit context reference. The utterance has no actor; the later report is attributed to jnewbery and explicitly concerns the reviewer\'s changes. The component remains context_inferred, and a direct addressee is not claimed as certain.',
      ('S02','Bdir'):'Retained outside-unit antecedent. Within the chosen span, it is the direct object of change at [111,113). This paragraph at [0,14) resolves its reference without changing its explicit grammatical role or enlarging the proposition span.',
      ('S03','A'):'Retained outside-unit context reference. The response attributed to jnewbery mentions the distinctive check and says it was removed. This supports an inferred reviser and remains weaker than an explicitly named request addressee.',
      ('S03','Bdir'):'Retained outside-unit semantic inference. Drop has an elided object. The prior phrase refers to the check, but its role as the receiver of drop is reconstructed; context_inferred and semantic_inference are appropriate.',
      ('S04','A'):'Retained outside-unit context reference. I think identifies the reviewer as evaluator rather than actor of document. The author\'s later broad update report supports a contextual reviser only; the actor is not labeled explicit.'}
    flag_resolutions.append({'flag_index':i,'flag':f,'status':'retained','resolution':explanations[(uid,sym)],
      'evidence':c['evidence']+([E('review_comments:6')] if uid=='S03' and sym=='A' else []),
      'residual_uncertainty':u['uncertainty_reason']})

unit_review=[{'unit_id':u['unit_id'],'status':'retained','finding':unit_notes[u['unit_id']],
             'evidence':[{'source_id':u['source_id'],'span':u['span']}]} for u in a['units']]
recognition_reviews=[]
disposition_reviews=[]
for u in a['units']:
 for i,r in enumerate(u['institution']['recognition']):
  recognition_reviews.append({'unit_id':u['unit_id'],'event_index':i,'status':'retained',
    'kind':r['kind'],'target':r['target'],'basis':r['basis'],
    'finding':r['rationale'],'evidence':r['evidence']})
 for i,r in enumerate(u['disposition_events']):
  disposition_reviews.append({'unit_id':u['unit_id'],'event_index':i,'status':'retained',
    'kind':r['kind'],'target':r['target'],'basis':r['basis'],
    'finding':r['rationale'],'evidence':r['evidence']})

outcome_notes=[
 'Retained as attributed reports and endorsements. Entry authors and timestamps establish the reviewer identity and occurrence order; last review resolves contextually to the supplied earlier review. No general obligation follows.',
 'Corrected by R01. The source joins agreement and a completed-removal report but does not establish when agreement was reached relative to the edit.',
 'Retained. The head release-note patch visibly contains all three correspondences. Exact wording differs, and both the source packet and claim limit inference about causal editing history.',
 'Retained. Merged flag, timestamp, alias, base, head and merge SHA have direct supplied metadata support. No status is transferred to another PR or to network adoption.'
]
mechanism_notes=[
 'Retained supported_sequence for the particular check: the initiation contains the concern, tentative drop action, clarity purpose and proviso; the author response repeats the object and reports removal. The alternative excludes causal identification and mandatory compliance.',
 'Retained supported_sequence only at the broad contribution level. Naming and two documentation proposals, author update report, prior/later review targets and final patch correspondence are all cited. Both and fixed remain uncertain rather than being assigned to specific requests. No exact wording adoption or review requirement is asserted.'
]
notes={
 'run_id':'F02_v03_r3','episode_id':'F02','schema_version':'0.3',
 'review_type':'one_complete_source_based_self_review', 'review_rounds':1,
 'scope':{'entries_reviewed':len(screen_review),'focal_entries_exhaustively_reviewed':len(pkt['selection_design']['focal_source_ids']),
          'units_reviewed':len(unit_review),'relations_reviewed':len(a['relations']),
          'recognition_events_reviewed':len(recognition_reviews),'disposition_events_reviewed':len(disposition_reviews),
          'outcomes_reviewed':len(outcome_notes),'mechanisms_reviewed':len(mechanism_notes)},
 'mechanical_feedback':{'first_status':checks['status'],'errors':checks['errors'],
    'first_review_flag_count':len(checks['review_flags']),'mechanical_pass_is_not_semantic_certification':True},
 'checker_flag_resolutions':flag_resolutions,
 'entry_screening_review':screen_review,
 'unit_review':unit_review,
 'cross_cutting_review':[
   {'topic':'authority_recognition_application','status':'retained',
    'finding':'All four statements remain undetermined/text_only. Broad author implementation reports and repository merge metadata do not establish authority or expectation recognition. ACKs are preserved as attributable context acts; none authorizes behavior, establishes mandatory reapproval, or proves rule application. No authorizes, applies, enforcement, or institutional-sanction relation is warranted.',
    'evidence':[E('comments:0'),E('reviews:0'),E('reviews:4'),E('review_comments:6'),E('metadata','"merged": true')]},
   {'topic':'levels_scope','status':'retained',
    'finding':'All focal conduct concerns operational edits and reviews in this PR. The target of the documentation suggestions is the current edit, even though the proposed technical prose describes recurring RPC behavior. There is no supplied choice of a recurring contributor arrangement, authority allocation, or foundation of legitimate authority.',
    'evidence':[E('review_comments:0'),E('review_comments:1'),E('review_comments:2'),E('review_comments:3')]},
   {'topic':'presentation_and_boundaries','status':'retained',
    'finding':'Four statement units preserve four distinct editorial/code actions. The two blockquotes are new proposed wording and remain qualifications of their edit requests; their technical capabilities and errors are not additional institutional propositions. Technical premises are cited without enlarging units merely to include inferred component anchors.',
    'evidence':[E('review_comments:0'),E('review_comments:1'),E('review_comments:2'),E('review_comments:3')]}
 ],
 'recognition_event_review':recognition_reviews,
 'disposition_event_review':disposition_reviews,
 'relation_review':[{'relation_index':i,'from_unit_id':r['from_unit_id'],'to_unit_id':r['to_unit_id'],
   'type':r['type'],'status':'retained','finding':r['rationale'],'evidence':r['evidence']} for i,r in enumerate(a['relations'])],
 'outcome_review':[{'outcome_index':i,'status':'corrected' if i==1 else 'retained','finding':outcome_notes[i],
    'evidence':o['evidence']} for i,o in enumerate(a['episode_summary']['observed_outcomes'])],
 'mechanism_review':[{'mechanism_index':i,'status':'retained','finding':mechanism_notes[i],
    'evidence':m['evidence']} for i,m in enumerate(a['episode_summary']['mechanisms'])],
 'changes':['R01'],
 'unresolved_limits':a['episode_summary']['missing_evidence']+a['episode_summary']['unresolved_questions'],
 'review_conclusion':'No screening omission requiring a new statement was identified. Five checker flags are reviewed and retained with explicit source support and inferred-role explanations. One outcome wording change removes an unsupported temporal implication; no unit, institution, force, target, level, or event label changes.'
}

def save(name,x): (ROOT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
save('annotation.json',a)
save('annotation.final.json',a)
save('repair_log.json',{'run_id':'F02_v03_r3','first_complete_preserved':True,'mechanical_repairs':[],'changes':repairs})
save('review_notes.json',notes)
print(json.dumps({'final_annotation_saved':True,'changes':len(repairs),'reviewed_checker_flags':len(flag_resolutions),'review_scope':notes['scope']},indent=2))
