import copy
import hashlib
import json
import platform
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
packet=json.loads((ROOT/'packet.json').read_text())
entries={e['source_id']:e for e in packet['entries']}
first=json.loads((ROOT/'annotation.first_complete.json').read_text())
a=json.loads((ROOT/'annotation.json').read_text())
checks=json.loads((ROOT/'checks.first.json').read_text())
units={u['unit_id']:u for u in a['units']}
repairs=[]

def ev(source,quote=None):
    if not source.startswith('pr14441:'): source='pr14441:'+source
    text=entries[source]['text']
    quote=text if quote is None else quote
    start=text.index(quote)
    return {'source_id':source,'span':{'start':start,'end':start+len(quote),'quote':quote}}

def edit(obj,key,new,path,reason,evidence,meaning=False,effect='evidence_basis_error'):
    old=copy.deepcopy(obj[key])
    assert old!=new
    obj[key]=new
    repairs.append({'change_id':f'R{len(repairs)+1:02d}','phase':'single_source_self_review','path':path,
                    'before':old,'after':copy.deepcopy(new),'reason':reason,'evidence':evidence,
                    'meaning_changes':meaning,'diagnosis':'execution_failure_under_existing_rule',
                    'effect':effect})

for i in range(4):
    u=a['units'][i]
    edit(u['institution'],'rationale',
         'This is a case-specific technical edit recommendation. The record supplies no attributed institutional authorization or enforcement claim, socially expected duty or accountability standard, committed personal method, or constituted institutional status. A norm need not be recurring or already shared, but the technical preference expressed here does not by itself select that classification. Later technical assent and implementation do not fill that gap.',
         f'/units/{i}/institution/rationale',
         'The first rationale unnecessarily referred to a socially expected recurring practice. Recurrence is not a norm-candidate requirement. The type remains undetermined on the narrower, source-supported reason that these are technical suggestions without a separately identified social expectation.',
         [ev(u['source_id'])])

s1=units['F02_S01']
app=s1['institution']['application_evidence'][1]
edit(app,'status','unresolved','/units/0/institution/application_evidence/1/status',
     'A retained heading with the requested spelling proves that spelling appears in the integrated artifact. With no inline line and no reviewed preimage, it does not independently locate and verify the particular correction action. Preserve the aggregate participant report but narrow artifact application.',
     [ev('review_comments:0'),ev('patch:0')],True)
edit(app,'rationale',
     'The retained release-note artifact contains the requested complete identifier and its head is the recorded merge commit. However, the supplied review has no line number or pre-update paragraph, so the exact typo occurrence and correction operation cannot be independently matched. This is artifact consistency with the request, while exact observed application remains unresolved; the separate aggregate participant report is retained.',
     '/units/0/institution/application_evidence/1/rationale',
     'Keep observed final spelling separate from proof of the particular requested edit.',[ev('review_comments:0'),ev('patch:0')],True)
edit(s1['institution']['standing_profile'],'application','reported',
     '/units/0/institution/standing_profile/application',
     'Recompute the profile after narrowing observed application to unresolved. A contextually mapped participant report remains.',
     [ev('comments:0'),ev('reviews:4')],True)

s4=units['F02_S04']; app=s4['institution']['application_evidence'][1]
edit(app,'rationale',
     'The retained release-note paragraph supplies the requested documentation of empty-string behavior with and without the setting and the usefulness/confusion explanation. The proposed phrase for backwards compatibility is not reproduced, so this is observed implementation of the focal documentation request, not verbatim adoption of every offered phrase or an independently established compatibility rationale. Matching retained-head and merge-commit metadata supports repository integration; no causal or network-adoption claim follows.',
     '/units/3/institution/application_evidence/1/rationale',
     'The tentative proposed wording included an explicit backward-compatibility rationale that the final paragraph does not repeat. Preserve that difference while retaining observed implementation of the focal request to document the change.',
     [ev('review_comments:3'),ev('patch:0')],False,'coverage_or_scope_loss')

event=units['F02_S03']['disposition_events'][0]
edit(event,'rationale',
     'The complete response says you\'re right and better without and explicitly refers to the check for "*". It supports acceptance of the removal recommendation. The isolated opening No is not coded as rejection; the precise clause it answers is not established.',
     '/units/2/disposition_events/0/rationale',
     'The first rationale over-specified what No answers. The full response establishes acceptance without resolving that discourse detail.',
     [ev('review_comments:6')],False)

out=a['episode_summary']['observed_outcomes'][0]
new=out['claim_parts'][1]['text'].replace('subsequently acknowledges','also acknowledges')
edit(out['claim_parts'][1],'text',new,'/episode_summary/observed_outcomes/0/claim_parts/1/text',
     'Remove unnecessary ordering relative to the author\'s update report. The source explicitly supports acknowledgement and the since-last-review comparison; the packet timestamp can support ordering but the claim does not need it.',
     [ev('reviews:4'),ev('reviews:0')],False,'convention_deviation')
edit(out,'claim',' '.join(p['text'] for p in out['claim_parts']),'/episode_summary/observed_outcomes/0/claim',
     'Keep the parent claim synchronized with the corrected claim part.',out['evidence'],False,'convention_deviation')

m=a['episode_summary']['mechanisms'][0]
edit(m['claim_parts'][0],'text',
     'ryanofsky says the new check for "*" appears not to change behavior and tentatively recommends removal for clarity, unless the reviewer is missing something.',
     '/episode_summary/mechanisms/0/claim_parts/0/text',
     'Describe the declarative doubt directly instead of wording that might be mistaken for a literal question; retain attribution, purpose, and caveat.',
     [ev('review_comments:2')],False,'convention_deviation')
edit(m,'claim',' '.join(p['text'] for p in m['claim_parts']),'/episode_summary/mechanisms/0/claim',
     'Keep the parent mechanism claim synchronized with the corrected part.',m['evidence'],False,'convention_deviation')
m=a['episode_summary']['mechanisms'][1]
edit(m['claim_parts'][0],'text',
     'ryanofsky recommends a spelling correction, a tentative replacement behavior paragraph, dropping the new check for "*" for clarity unless something was missed, and documentation of the empty-string change with tentative wording.',
     '/episode_summary/mechanisms/1/claim_parts/0/text',
     'Carry the removal caveat, clarity purpose, and tentative wording into the aggregate mechanism claim instead of relying solely on its evidence citations.',
     [ev('review_comments:0'),ev('review_comments:1'),ev('review_comments:2'),ev('review_comments:3')],True,'coverage_or_scope_loss')
edit(m,'claim',' '.join(p['text'] for p in m['claim_parts']),'/episode_summary/mechanisms/1/claim',
     'Keep the parent mechanism claim synchronized with the qualified part.',m['evidence'],True,'coverage_or_scope_loss')

# The following records document the one complete source-based review. They do
# not infer semantic validity from the mechanical checker.
predicate_notes={
 'F02_S01':[
   'Retained as inferred. The editor is not a local subject; attribution of the update response supports jnewbery as a contextual addressee without assuming an occupational role.',
   'Retained as inferred in the chosen pragmatic parse. Should is lexical in the be clause; its reconstructed governance of the editing action is not mislabeled as explicit.',
   'Retained as semantic reconstruction. The original says should be and does not contain correct; the alternative literal spelling reading is explicit in the unit.',
   'Retained as inferred. The supplied release-note path and displayed identifier locate the target at document level but not an exact original line; the missing line limits application, not the plausible edit reading.',
   'Retained as inferred execution result. The complete identifier and final s survive; the complement of be is not treated as an explicit object of an absent correct predicate.'],
 'F02_S02':[
   'Retained as inferred. The literal I belongs to the recommending reviewer. The advised PR editor is reconstructed from the attributed update response and is not labeled a local grammatical actor.',
   'Retained explicit: change is supplied by the selected focal predicate. Inferring recommendation force and addressee does not make this expressed action inferred.',
   'Retained explicit object role for it under change. This paragraph supplies the antecedent in the prior sentence, retained in a qualifier; the pragmatic role explanation distinguishes reference from grammatical role.',
   'Retained as an explicit execution specification introduced by change it to. The drafted text is the requested result; its embedded setting conditions constrain technical content rather than activation of the reviewer\'s instruction. A Bdir/property representation could preserve the same meaning.'],
 'F02_S03':[
   'Retained as contextual actor: the imperative omits the editor and the attributed same-check removal report supports jnewbery without making it an explicit local argument.',
   'Retained explicit: drop is the stated action, separated from its omitted object.',
   'Retained inferred object role. The preceding the new check for "*" here was the subject of changes, not the object of drop. Its relocated Bdir role is semantic inference with an outside-unit explanation.',
   'Retained explicit execution purpose for clarity. No invented activation condition is attached to the purpose.',
   'Retained explicit unless caveat as activation/defeasibility. An execution-qualification representation is possible if it preserves that the suggestion is conditional on no missed relevant function; it is not an unconditional command.'],
 'F02_S04':[
   'Retained inferred actor. I in I think is the reviewer, not the omitted subject of document. The author\'s attributed update supports the contextual editor.',
   'Retained explicit document under the introductory evaluation. The action is supplied even though recommendation force is conveyed indirectly.',
   'Retained explicit object the empty string change under document. The offered paragraph remains a scope qualification on that request, rather than a fabricated institutional permission.']}

qualifier_notes={
 'F02_S01':'Complete identifier, final s, actor inference, case-specific release-note scope, and literal technical alternative are retained. Missing exact line is acknowledged and now limits observed application.',
 'F02_S02':'Tentative I\'d maybe, the same-release criticism, both enabled/disabled behaviors, complete setting/argument names, and the no-longer-possible label rationale are carried in the replacement component and scope notes. Embedded technical conditions are not activation conditions for editing.',
 'F02_S03':'Maybe, the particular new check for "*", attributed behavior doubt, clarity purpose, and unless-I-am-missing-something caveat are all retained. The aggregate mechanism was corrected to display the caveat too.',
 'F02_S04':'The focal document action, exact empty-string label, enabled/disabled setting, backward-compatibility language, usefulness/confusion explanation, and tentative proposed wording remain attached. The final artifact\'s omission of the explicit backward-compatibility phrase is now acknowledged in application rationale.'}

flag_reviews=[]
pred_counts=defaultdict(int); app_counts=defaultdict(int); summary_count=0
for i,flag in enumerate(checks['review_flags']):
    uid=flag.get('unit_id'); code=flag['code']; status='retained'
    if code=='qualifier_audit':
        u=units[uid]; explanation=qualifier_notes[uid]
        evidence=[e for q in u['proposition']['qualifiers'] for e in q['evidence']]
    elif code=='predicate_audit':
        j=pred_counts[uid];pred_counts[uid]+=1
        c=units[uid]['components'][j];explanation=predicate_notes[uid][j]
        evidence=c['evidence']+[c['governing_span']]
    elif code=='application_audit':
        j=app_counts[uid];app_counts[uid]+=1
        ap=units[uid]['institution']['application_evidence'][j]
        explanation=ap['rationale'];evidence=ap['evidence']
        if uid=='F02_S01' and j==1: status='corrected'
        if uid=='F02_S04' and j==1: status='corrected'
    elif code=='summary_audit':
        j=summary_count;summary_count+=1
        group='observed_outcomes' if j<3 else 'mechanisms'
        idx=j if j<3 else j-3
        item=a['episode_summary'][group][idx]
        evidence=item['evidence']
        explanation=('Every material clause is mapped to a claim part. Reports remain attributed, final artifact content is distinguished from causation, and the merge belongs only to PR #14441. '
                     +('Unnecessary relative ordering was removed.' if j==0 else 'The check-removal claim is reported only; no observed deletion is inferred.' if j==1 else 'The spelling outcome states only that the retained artifact contains the identifier, not that a precise correction has been located.' if j==2 else 'Declarative doubt, tentative force, clarity purpose, and missing-something caveat are explicit; supported sequence is not a causal estimate.' if j==3 else 'The aggregate recommendation clause was expanded to preserve tentative force and the removal caveat. Subsequent review is correspondence with an update, not mandatory reapproval.'))
        if j in [0,3,4]: status='corrected'
    else:
        raise ValueError('Unreviewed checker flag '+code)
    flag_reviews.append({'flag_index':i,'code':code,'unit_id':uid,'status':status,
                         'explanation':explanation,'evidence':evidence})

screen_reviews=[]
for e in packet['entries']:
    screen=next(s for s in a['entry_screening'] if s['source_id']==e['source_id'])
    screen_reviews.append({'source_id':e['source_id'],'status':'retained','disposition':screen['disposition'],
                          'assessment':screen['reason'],'evidence':[ev(e['source_id'])] if e['text'] else [],
                          'metadata_limit':'The supplied entry author, path, timestamp and review-state fields are considered as metadata; absent reply threading or text is not reconstructed.'})

unit_reviews=[]
for u in a['units']:
    statement=u['record_role']=='statement'
    unit_reviews.append({'unit_id':u['unit_id'],'status':'retained' if u['unit_id'] not in ['F02_S01','F02_S04'] else 'corrected',
        'scope_and_type':u['institution']['rationale'],
        'force_and_presentation':('Recommendation force is technical advice, without lexical permission from can/possible or duty from predictive will. Offered replacement paragraphs are proposed_wording; no repeated-quotation or independent endorsement units are created.' if statement else 'Context status preserves the supplied act without promoting ACKs, reported edits, technical comparisons, or the submitted PR description into new prescriptions.'),
        'authority_recognition_application':('Authority evidence remains absent. Ordinary assent and implementation reports do not establish expectation recognition; documentary support remains none because the release notes are the edit artifact, not an institutional guidance source. Application is separately reported, observed, or unresolved.' if statement else 'All standing dimensions and institutional type remain not_applicable for context.'),
        'dispositions_and_identity':('All status evidence belongs to canonical PR #14441. Recorded merge targets the broader PR, not referenced #14411 or earlier contributions. The removal is accepted and reported; neither No nor the earlier technical criticism is a rejection of this recommendation.' if statement else 'No disposition or recognition events are duplicated on context records.'),
        'levels':u['level_rationale'],
        'evidence':[ev(u['source_id'])]})

relation_reviews=[]
for i,r in enumerate(a['relations']):
    relation_reviews.append({'relation_index':i,'from_unit_id':r['from_unit_id'],'to_unit_id':r['to_unit_id'],
                            'status':'unresolved' if r['basis']=='unresolved' else 'retained',
                            'assessment':r['rationale'],'evidence':r['evidence']})

review={
 'run_id':'F02_v04_r1','review_count':1,'review_type':'complete_source_based_self_review',
 'first_complete_freeze_preceded_checker_and_review':True,
 'checker_result_reviewed':'checks.first.json','initial_mechanical_status':checks['status'],
 'review_scope':['Every source entry, including empty focal entries and context-only supplements','Focal proposition coverage and technical alternatives','Material conditions, negation, actor attribution, time and object identity','Every component role and governing clause','Authority, recognition, documentary support and application','Disposition target, identity and report versus artifact evidence','Target and observed governance levels','Every relation and every outcome/mechanism claim part'],
 'screening_reviews':screen_reviews,'unit_reviews':unit_reviews,'relation_reviews':relation_reviews,
 'flag_resolutions':flag_reviews,
 'flag_accounting':{'first_check_flags':len(checks['review_flags']),'resolved_records':len(flag_reviews),
                    'statuses':dict(Counter(f['status'] for f in flag_reviews))},
 'unresolved_limits':a['episode_summary']['missing_evidence']+a['episode_summary']['unresolved_questions'],
 'interpretive_limits':[{'issue':'Exact spelling-correction application','status':'unresolved','evidence':[ev('review_comments:0'),ev('patch:0')],
                        'assessment':'The correct final spelling is visible, but the particular reviewed occurrence cannot be independently matched. Participant-reported application remains contextual.'},
                       {'issue':'Terse-response pairing','status':'unresolved','evidence':[ev('review_comments:4'),ev('review_comments:5')],
                        'assessment':'Both and fixed do not recover their precise targets without reply threading. The two candidate reply relations remain unresolved.'},
                       {'issue':'Exact removed-check implementation','status':'unresolved','evidence':[ev('review_comments:2'),ev('review_comments:6'),ev('patch:1')],
                        'assessment':'The same-check correspondence supports reported uptake. The final diff does not reconstruct the earlier reviewed check or independently verify behavior equivalence.'}],
 'self_review_conclusion':'All 22 entries were screened; four edit recommendations remain. The principal correction narrows exact observed application of the spelling edit. No authority, institutional expectation recognition, sanction, higher governance level, causal effect, or network adoption is inferred. Mechanical success is not semantic certification.'}

def write(name,value):
    (ROOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

write('annotation.json',a)
write('annotation.final.json',a)
write('repair_log.json',{'run_id':'F02_v04_r1','initial_checker_errors':checks['errors'],
                         'mechanical_repairs':[],'changes':repairs,'change_count':len(repairs),
                         'meaning_change_count':sum(r['meaning_changes'] for r in repairs),
                         'first_complete_sha256':hashlib.sha256((ROOT/'annotation.first_complete.json').read_bytes()).hexdigest()})
write('review_notes.json',review)

access={
 'run_id':'F02_v04_r1','allowed_directory':str(ROOT),'isolation':'Research reads and writes were confined to the assigned run directory. No parent directories, other runs, outside research, calibration answer files, web, Library, or additional agents were accessed.',
 'inherited_primary_configuration':True,'configuration_override':None,
 'model_runtime':{'model_role_description':'Inherited primary Codex configuration; no model or reasoning override requested or selected.',
                  'exact_model_identity':None,'provider_snapshot':None,'seed':None,'sampling':None,'token_use':None,'cost':None,
                  'python_version':platform.python_version(),'python_implementation':platform.python_implementation(),
                  'python_executable':sys.executable,'time_recorded_utc':datetime.now(timezone.utc).isoformat()},
 'files_accessed':[{'path':str(ROOT/f),'access':mode} for f,mode in [
    ('INSTRUCTIONS.txt','read'),('protocol/codebook.txt','read'),('protocol/annotation_schema.json','read'),
    ('packet.json','read'),('tools/check_annotation.py','read_execute'),('build_annotation.py','write_execute'),
    ('annotation.json','write_read_update'),('annotation.first_complete.json','write_then_read; never modified'),
    ('checks.first.json','write_read'),('finalize_review.py','write_execute'),('annotation.final.json','write'),
    ('repair_log.json','write'),('review_notes.json','write'),('access_record.json','write'),('execution_log.json','write')]],
 'runtime_modules':'Ordinary Python standard library plus jsonschema imported by the supplied checker; these are execution dependencies, not research sources.',
 'unknowns_policy':'Unavailable model/provider snapshot, seed, sampling, token use and cost remain null; no identity was inferred from codebook or packet content.'}
write('access_record.json',access)
write('execution_log.json',{'run_id':'F02_v04_r1','steps':[
    {'step':1,'action':'Read assigned instructions, complete codebook and schema, complete packet and supplied checker.'},
    {'step':2,'action':'Construct full-schema annotation with exact Python Unicode offsets; freeze annotation.first_complete.json before any checks or self-review.'},
    {'step':3,'command':'python3 tools/check_annotation.py packet.json annotation.json > checks.first.json','result':'pass','mechanical_errors':0},
    {'step':4,'action':'Conduct one complete source-based self-review; preserve every semantic/rationale change and resolve all initial checker flags in review_notes.json.'},
    {'step':5,'action':'Write final annotation, repair log, review notes and access record; final checker pending.'}],
    'packet_sha256':hashlib.sha256((ROOT/'packet.json').read_bytes()).hexdigest(),
    'first_complete_sha256':hashlib.sha256((ROOT/'annotation.first_complete.json').read_bytes()).hexdigest(),
    'final_annotation_sha256':hashlib.sha256((ROOT/'annotation.final.json').read_bytes()).hexdigest()})
print(json.dumps({'review_complete':True,'changes':len(repairs),'flags_reviewed':len(flag_reviews),
                  'entries':len(a['entry_screening']),'units':len(a['units']),'statements':sum(u['record_role']=='statement' for u in a['units'])}))
