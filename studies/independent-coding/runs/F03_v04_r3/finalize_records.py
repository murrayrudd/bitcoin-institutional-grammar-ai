import json, hashlib, sys, platform
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict, Counter
from importlib.metadata import version

ROOT=Path.cwd()
p=json.loads(Path('packet.json').read_text())
a=json.loads(Path('annotation.final.json').read_text())
first=json.loads(Path('annotation.first_complete.json').read_text())
checks0=json.loads(Path('checks.first.json').read_text())
checks1=json.loads(Path('checks.json').read_text())
repairs=json.loads(Path('repair_log.json').read_text())
entries={e['source_id']:e for e in p['entries']}
us={u['unit_id']:u for u in a['units']}
us0={u['unit_id']:u for u in first['units']}
now=datetime.now(timezone.utc).isoformat()

def ev(s,q=None,start=0):
    t=entries[s]['text'];q=t if q is None else q;i=t.index(q,start)
    return {'source_id':s,'span':{'start':i,'end':i+len(q),'quote':q}}
def ue(u):return {'source_id':u['source_id'],'span':u['span']}
def unique(es):
    out=[];seen=set()
    for e in es:
        k=(e['source_id'],e['span']['start'],e['span']['end'])
        if k not in seen:out.append(e);seen.add(k)
    return out

unit_notes={
'F03-U01':'The body offers a specific checkbox change and explicitly excludes GUI replacement. Both qualifiers survive. Its technical report has a contextual-only alternative. The patch proves narrower artifact facts; complete application is unresolved because placement and integration are unverified. The exposure objection challenges sequencing, not whether the submitted artifact contains code.',
'F03-U02':'Not sure remains an unresolved judgment. The reconstructed proceed-with reading is only a candidate; we and this have inferred roles under that action. No integration power or binding prerequisite is assigned. The separate ongoing workflow and the contrary intention not to delay review remain attached.',
'F03-U03':'The relative antecedent identifies the GUI-based replacement workflow; it is not a local Bdir occurrence. The plan is personal, ongoing, and described as larger. No complete patch, completion commitment, or canonical proposal identifier is invented.',
'F03-U04':'The negative intention is retained in the literal predicate rather than changed to a prohibition. Review is the object; no reviewer obligation or authority follows. Correspondence with the comment is supported, but the retained body cannot be backdated sentence by sentence.',
'F03-U05':'The qualified exposure objection supplies a plausible negative recommendation until wallet replacement capability exists. Its literal technical-doubt and local-norm alternatives remain. The author’s quoted agreement is ordinary assent; it does not establish an institutional expectation or a prohibition on review.',
'F03-U06':'Both red text and the bang remain targets of the single formatting recommendation. This can be split without semantic loss. Avoid and its argument roles are inferred from the evaluative deserves clause. The referent of it is visibly attached to the wording concern and retained patch, without relying on screenshots.',
'F03-U08':'Arguably, the non-replacable case, red text, and the inability to update fees later all survive. The should and red-text anchors now belong to the focal get-red-text predicate. Format and its patient/manner roles remain inferred; no warning rule is established.',
'F03-U09':'The complete adaptive-fee alternative survives: N replacements, future locktimes, multiplicatively higher fees, and the fee schedule. Have is anchored to the adaptive alternative. We and should are explicitly supplied but shared across the coordinated alternatives. The wondering-if form is retained as a deliberative question, and no exclusive logical or adoption claim is added.',
'F03-U12':'The author explicitly reports ongoing work on the replacement GUI. This is a personal strategy candidate with a context-only alternative; the object is not silently mapped to #8182. The body/comment correspondence is not a chronology of edited wording.',
'F03-U13':'Reviewed explicitly supplies the action, and this remains its patient in the passive clause even under the pragmatic invitation reading. Already is execution timing. Can is not encoded as an explicit permission. The 0.13 sentence is a difficult timeline, not an implementation promise or evidence of release inclusion.',
'F03-U17':'The reported attempt to allow extra outputs and the sendcoins-dialog method survive, including exploratory/past-progressive wording. The author’s fee-only question concerns possible future scope. It is now a broader-proposal challenge and a clarifying relation, not a dispute about the fact of the prior attempt.',
'F03-U18':'The question retains maybe, should, and just. The proposal concerns fee-only focus, not a final scope decision. We is explicit but unspecified. No claim is made that additional-output work was withdrawn, that its attempt did not occur, or that a recurring governance arrangement changed.',
'F03-U19':'The explicit generic you/handle method is bounded to additional-output workflows. The child transaction is for use if the original confirms; this is not a condition that creation must wait until confirmation. Need is technical necessity, not an institutional deontic. Generality is limited to the stated workflow method; no rule or enforcement is inferred.',
'F03-U21':'The question preserves perhaps and both alternative labels. Use and its object/constraint roles are inferred from the wording comparison. The old word remains the replacement target. The purpose of better expression does not establish a shared naming standard.',
'F03-U23':'The proposal retains the literal [send immediately] label, delaying description, amendment-within-timeout condition, and possible pre-setting abort. The apparent label/behavior conflict and pronoun ambiguity remain unresolved. Technical can/could does not establish authorized discretion.',
'F03-U24':'Jonas is a vocative and therefore an inferred actor of the implied edit, not an explicit argument of a supplied use verb. The source provides only the replaceab... stem. The condition if Greg’s suggestion is not chosen and the I believe attribution remain intact. No unprovided full spelling or contributor role is assumed.',
'F03-U25':'Needs rebase is an elliptical request with a technical-status alternative. The rebase action and omitted #7819 object are inferred, with canonical object evidence attached. The actor remains absent. No maintainer authority, sanction, causal link to closure, or completed rebase is inferred.'}

component_changes={('F03-U02',0):['R02'],('F03-U02',2):['R03'],('F03-U08',0):['R05'],('F03-U08',3):['R06'],('F03-U21',2):['R17'],('F03-U25',1):['R18']}
for i in range(5):component_changes[('F03-U09',i)]=['R07']
qual_changes={'F03-U06':['R04'],'F03-U19':['R15']}
summary_items=[('observed_outcomes',i,x) for i,x in enumerate(a['episode_summary']['observed_outcomes'])]+[('mechanisms',i,x) for i,x in enumerate(a['episode_summary']['mechanisms'])]
summary_notes=[
'The author-reported inclusion is separated from recorded closure. The closed and merged-false anchors both concern #7819. The claim does not infer rejection, merge, or exact implementation in #8182.',
'The URL, closed state, merged-false state, and closure timestamp all concern #8182. Its metadata are never transferred to #7819 or to unknown workflow objects. A merge_commit_sha is not used as integration evidence.',
'The patch anchors directly show the checkbox, conditional confirmation, color code, retained spelling, and exclamation. The head SHA and false merge status limit the claim to the retained unmerged artifact. No review-caused change, exact screenshot placement, or adoption is claimed.',
'The quotation and explicit agreement directly support a response sequence, and the author explicitly distinguishes ongoing GUI work from present review readiness. The mechanism is local coordination; the alternative explains why this is not proof of a recognized procedural rule or subsequent review action.',
'All material clauses are anchored: the complete adaptive method, its quotation and tentative endorsement, the extra-output report, the fee-only question, and the child-transaction/version-growth explanation. The mechanism claims textual reason-giving, not a causal decision or implementation outcome.',
'The author’s closing/inclusion report and #7819’s closed-unmerged record are distinct evidence parts. Consolidation is labeled consistent_with, with the exact transfer and reasons left unknown. No earlier comment is asserted to have caused closure.'
]

def resolve_flags(checks,label):
    comp_ix=defaultdict(int);summary_ix=0;challenge_ix=0;out=[]
    for i,f in enumerate(checks['review_flags']):
        uid=f.get('unit_id');code=f['code'];u=us.get(uid)
        r={'checker_file':label,'flag_index':i,'code':code,'unit_id':uid,'status':'retained','rationale':'','evidence':[],'related_repairs':[]}
        if code=='predicate_audit':
            n=comp_ix[uid];comp_ix[uid]+=1;c=u['components'][n]
            r['component_index']=n;r['symbol']=c['symbol']
            r['evidence']=unique(c['evidence']+[c['governing_span']])
            r['rationale']=('The cited occurrence was checked against its governing predicate. '+(c['inference_note'] if c['inference_note'] else f"The local {c['symbol']} role is supplied in the focal clause and is not borrowed from another predicate.")+' '+unit_notes[uid])
            r['related_repairs']=component_changes.get((uid,n),[])
            if label=='checks.first.json' and r['related_repairs']:r['status']='corrected'
        elif code=='qualifier_audit':
            r['evidence']=unique([ue(u)]+[e for q in u['proposition']['qualifiers'] for e in q['evidence']])
            r['rationale']=unit_notes[uid]
            r['related_repairs']=qual_changes.get(uid,[])
            if label=='checks.first.json' and r['related_repairs']:r['status']='corrected'
        elif code=='application_audit':
            r['status']='corrected' if label=='checks.first.json' else 'unresolved'
            r['related_repairs']=['R01'];r['rationale']=u['institution']['application_evidence'][0]['rationale']
            r['evidence']=unique(u['institution']['application_evidence'][0]['evidence']+[ev('pr7819:metadata','"merged": false'),ue(u)])
            r['remaining_limit']='Complete focal-edit application and integration are not established. The final annotation retains unresolved status rather than forcing an observed conclusion.'
        elif code=='challenge_audit':
            r['evidence']=unique([ue(u)]+[e for c in u['institution']['challenges'] for e in c['evidence']])
            r['rationale']=' '.join(c['rationale'] for c in u['institution']['challenges'])
            if uid=='F03-U17':
                r['related_repairs']=['R13','R14']
                if label=='checks.first.json':r['status']='corrected'
        elif code=='challenge_object':
            challenge_ix+=1
            if challenge_ix==1:
                rel=next(x for x in a['relations'] if x['from_unit_id']=='F03-U05' and x['to_unit_id']=='F03-U01')
                r['evidence']=rel['evidence'];r['rationale']='The reviewer’s this is the checkbox offered by the body in the same PR. The challenge concerns its exposure timing. It does not dispute the existence of the submitted patch or establish a binding release rule.'
                r['relation']='F03-U05 -> F03-U01'
            else:
                rel=next(x for x in a['relations'] if x['from_unit_id']=='F03-U18' and x['to_unit_id']=='F03-U17')
                r['status']='corrected';r['related_repairs']=['R13','R14'];r['evidence']=rel['evidence'];r['rationale']=rel['rationale'];r['relation']='F03-U18 -> F03-U17'
        elif code=='summary_audit':
            group,j,x=summary_items[summary_ix]
            r['item_path']=f'episode_summary.{group}[{j}]';r['rationale']=summary_notes[summary_ix];r['evidence']=x['evidence'];summary_ix+=1
        else:
            raise RuntimeError('Unhandled checker flag '+code)
        out.append(r)
    return out

source_review=[]
for sc in a['entry_screening']:
    s=sc['source_id'];local=[u for u in a['units'] if u['source_id']==s]
    source_review.append({'source_id':s,'scope':'exhaustive_focal_screening' if s in p['selection_design']['focal_source_ids'] else 'supplemental_context_screening','status':'retained','screening_disposition':sc['disposition'],'unit_ids':sc['unit_ids'],'assessment':sc['reason'],'evidence':[ev(s)],'note':'All supplied text and metadata were re-read after the first-complete freeze. Supplemental context screening is not an assertion that no institutional content is present.'})

level_review=[]
for u in a['units']:
    if u['record_role']=='statement':
        level_review.append({'unit_id':u['unit_id'],'status':'retained','statement_target_level':u['statement_target_level'],'observed_action_level':u['observed_action_level'],'assessment':'The focal action concerns the particular offered feature, a bounded technical method, ongoing personal development, or a current review step. No recurring contribution procedure, jurisdiction, decision competence, or foundation of authority is proposed or recognized. General technical scope in U19 does not raise the governance level.','evidence':[ue(u)]})
    else:
        level_review.append({'unit_id':u['unit_id'],'status':'retained','statement_target_level':'not_applicable','observed_action_level':u['observed_action_level'],'assessment':'This contextual or repeated occurrence has no independently coded institutional target. The visible act belongs to ordinary development discussion.','evidence':[ue(u)]})

disposition_review=[]
for u in a['units']:
    for i,d in enumerate(u['disposition_events']):
        disposition_review.append({'unit_id':u['unit_id'],'event_index':i,'status':'retained','assessment':'Both closed state and false merge status refer to #7819. The event is scoped to the broader proposal, never the acceptance/rejection or implementation of this individual proposition. The body’s plain presentation is retained. No #8182 or #7159 status is substituted.','object_id':d['object_id'],'evidence':unique(d['evidence']+d['identity_evidence'])})

recognition_review=[]
for u in a['units']:
    for i,r in enumerate(u['institution']['recognition']):
        recognition_review.append({'unit_id':u['unit_id'],'event_index':i,'status':'retained','assessment':r['rationale']+' The final recognition profile stays none: no supplied event establishes recognition of a governing expectation. Actor identity is taken only from packet attribution; quoted text is not another actor’s endorsement.','evidence':unique(r['evidence']+r['identity_evidence'])})

review={'run_id':'F03_v04_r3','episode_id':'F03','protocol_version':'0.4','review_completed_at_utc':now,'review_passes':1,'review_scope':'One complete source-based self-review after first-complete freeze and first checker. It covers every focal and supplemental entry, all components and qualifiers, institutional evidence, relations, levels, dispositions, and every outcome/mechanism clause.','first_checker_status':checks0['status'],'final_checker_status':checks1['status'],'mechanical_pass_is_not_semantic_certification':True,'source_review':source_review,'unit_interpretation_review':[{'unit_id':uid,'status':'retained_with_bounded_alternatives','assessment':note,'evidence':[ue(us[uid])]+[e for q in us[uid]['proposition']['qualifiers'] for e in q['evidence']]} for uid,note in unit_notes.items()],'flag_resolutions':resolve_flags(checks0,'checks.first.json')+resolve_flags(checks1,'checks.json'),'authority_documentary_review':{'status':'retained','assessment':'No candidate has supplied institutional authorization, a recognized rule-making procedure, or an attributable enforcement claim. No source is treated as an authoritative policy document for these propositions. Institutional type remains undetermined or personal/technical strategy; norm alternatives remain bounded, and all documentary support profiles are none. Technical need, can, and an accepted spelling claim do not fill the authority gap.','evidence':[ev('pr7819:comments:0'),ev('pr7819:comments:2','but this can be reviewed already.'),ev('pr7819:comments:4'),ev('pr7819:comments:6'),ev('pr7819:comments:7')]},'recognition_review':recognition_review,'disposition_review':disposition_review,'level_review':level_review,'relations_review':[{'from_unit_id':r['from_unit_id'],'to_unit_id':r['to_unit_id'],'type':r['type'],'status':'retained','assessment':r['rationale'],'evidence':r['evidence']} for r in a['relations']],'summary_review':[{'item_path':f'episode_summary.{group}[{i}]','status':'retained','assessment':summary_notes[n],'evidence':item['evidence']} for n,(group,i,item) in enumerate(summary_items)],'unresolved_limits':[{'status':'unresolved','limit':'Complete implementation/application of the checkbox proposition, including visual placement and repository integration, is not established.','evidence':[ev('pr7819:body',us['F03-U01']['span']['quote']),ev('pr7819:patch:0'),ev('pr7819:metadata','"merged": false')]},{'status':'unresolved','limit':'The separate replacement-GUI and additional-output plans have no established canonical proposal ID; later reference to #8182 does not identify them retroactively.','evidence':[ev('pr7819:body','a GUI based replacement workflow'),ev('pr7819:comments:2',us['F03-U12']['span']['quote']),ev('pr7819:comments:3',us['F03-U17']['span']['quote']),ev('pr7819:comments:8')]},{'status':'unresolved','limit':'The [send immediately] label and described delaying behavior remain semantically in tension; no unprovided correction is inferred.','evidence':[ev('pr7819:comments:5',us['F03-U23']['span']['quote'])]},{'status':'unresolved','limit':'The source does not establish whether tentative sequencing, wording, and rebase suggestions are shared local expectations rather than individual technical judgments.','evidence':[ev('pr7819:comments:0'),ev('pr7819:comments:6'),ev('pr7819:comments:7')]},{'status':'unresolved','limit':'The exact transferred content in #8182 and adoption of individual suggestions remain unverified; both proposal records are unmerged.','evidence':[ev('pr7819:comments:8'),ev('pr7819:metadata','"merged": false'),ev('pr8182:supplement_metadata','"merged": false')]},{'status':'unresolved','limit':'The retained body’s creation and update dates do not date each sentence or establish the direction of body/comment restatement.','evidence':[ev('pr7819:metadata','"created_at": "2016-04-05T15:15:15+00:00"'),ev('pr7819:metadata','"updated_at": "2021-09-08T11:40:59+00:00"')]}],'repair_log':'repair_log.json','counts':{'first_checker_flags':len(checks0['review_flags']),'final_checker_flags':len(checks1['review_flags']),'resolved_flag_records':len(checks0['review_flags'])+len(checks1['review_flags']),'changes':len(repairs['changes'])}}
Path('review_notes.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')

# Input and output contents are confined to this run. Enumerated names are not treated as read research sources.
read_files=['INSTRUCTIONS.txt','protocol/codebook.txt','protocol/annotation_schema.json','packet.json','tools/check_annotation.py','build_annotation.py','annotation.json','annotation.first_complete.json','checks.first.json','self_review.py','annotation.final.json','checks.json','repair_log.json','finalize_records.py','freeze.first_complete.json','review_notes.json']
written_files=['build_annotation.py','annotation.json','annotation.first_complete.json','freeze.first_complete.json','checks.first.json','self_review.py','annotation.final.json','repair_log.json','checks.json','finalize_records.py','review_notes.json','access_record.json','completion_manifest.json']
access={'run_id':'F03_v04_r3','recorded_at_utc':now,'research_and_write_root':str(ROOT),'configuration':{'mode':'Inherited primary configuration; no override requested or applied.','environment_self_description':'Codex, an agent based on GPT-6. This is an inherited instruction description, not an exact provider model identifier.','model_id':None,'provider_snapshot':None,'seed':None,'sampling':None,'reasoning_effort':None,'token_use':None,'cost':None,'note':'Exact provider snapshot, seed, sampling, token use, and cost were not exposed. None is inferred from protocol, files, or model menu labels.'},'runtime':{'python_version':sys.version,'python_executable':sys.executable,'platform':platform.platform(),'jsonschema_version':version('jsonschema'),'ordinary_libraries_used':['json','hashlib','copy','pathlib','datetime','collections','sys','platform','importlib.metadata','jsonschema'],'ordinary_runtime_access':'Python executable, standard library, jsonschema and its normal dependencies; no runtime documents or research sources outside the assigned directory were consulted.'},'files_accessed':[{'path':str(ROOT/f),'role':'frozen_input' if f in ['INSTRUCTIONS.txt','protocol/codebook.txt','protocol/annotation_schema.json','packet.json','tools/check_annotation.py'] else 'own_run_output','sha256':hashlib.sha256(Path(f).read_bytes()).hexdigest()} for f in read_files],'files_written':[str(ROOT/f) for f in written_files],'self_record_access':{'path':str(ROOT/'access_record.json'),'operation':'Written here and subsequently read to hash the completion manifest; the manifest contains its exact hash.'},'access_record_scope':'Explicit task-file reads and writes; not an operating-system trace of Python dependency loading.','directory_inventory':{'command':'rg --files .','root':str(ROOT),'effect':'Enumerated filenames only. input_manifest.json and calibration file contents were not accessed.'},'calibration_contents_accessed':False,'outside_research_sources_accessed':False,'parent_or_other_run_files_accessed':False,'library_accessed':False,'web_accessed':False,'subagents_spawned':False,'source_packet_sha256':hashlib.sha256(Path('packet.json').read_bytes()).hexdigest(),'originals_modified':False,'limitations':['Runtime model identifier and provider details were not exposed.','The agent inherited task/system context but did not consult any parent research history, other annotation, or external semantic answer.']}
Path('access_record.json').write_text(json.dumps(access,ensure_ascii=False,indent=2)+'\n')

first_hash=hashlib.sha256(Path('annotation.first_complete.json').read_bytes()).hexdigest()
freeze=json.loads(Path('freeze.first_complete.json').read_text())
assert first_hash==freeze['annotation_first_complete_sha256']
assert a['packet_sha256']==hashlib.sha256(Path('packet.json').read_bytes()).hexdigest()
assert Path('annotation.json').read_bytes()==Path('annotation.final.json').read_bytes()
assert len(review['flag_resolutions'])==len(checks0['review_flags'])+len(checks1['review_flags'])
assert all(x['evidence'] and x['rationale'] and x['status'] in ['retained','corrected','unresolved'] for x in review['flag_resolutions'])

# Exact-anchor verification for audit citations, not an additional interpretation pass.
def anchors(x):
    if isinstance(x,dict):
        if 'source_id' in x and 'span' in x:
            s=x['span'];assert entries[x['source_id']]['text'][s['start']:s['end']]==s['quote']
        for y in x.values():anchors(y)
    elif isinstance(x,list):
        for y in x:anchors(y)
anchors(review);anchors(repairs)
manifest={'run_id':'F03_v04_r3','episode_id':'F03','completed_at_utc':now,'status':'complete','counts':{'screened_entries':len(a['entry_screening']),'focal_entries':len(p['selection_design']['focal_source_ids']),'units':len(a['units']),'statement_units':sum(u['record_role']=='statement' for u in a['units']),'context_units':sum(u['record_role']=='context' for u in a['units']),'quotation_units':sum(u['record_role']=='quotation' for u in a['units']),'relations':len(a['relations']),'observed_outcomes':len(a['episode_summary']['observed_outcomes']),'mechanisms':len(a['episode_summary']['mechanisms']),'repairs':len(repairs['changes']),'checker_errors':len(checks1['errors']),'first_review_flags':len(checks0['review_flags']),'final_review_flags':len(checks1['review_flags'])},'final_check_status':checks1['status'],'first_complete_hash_matches_freeze':True,'source_packet_hash_matches':True,'all_checker_flags_have_cited_dispositions':True,'single_source_self_review_complete':True,'files':{f:{'path':str(ROOT/f),'sha256':hashlib.sha256(Path(f).read_bytes()).hexdigest()} for f in ['annotation.first_complete.json','annotation.final.json','annotation.json','checks.first.json','checks.json','repair_log.json','review_notes.json','access_record.json','freeze.first_complete.json']},'unresolved_limits':[x['limit'] for x in review['unresolved_limits']]}
Path('completion_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'complete':True,'counts':manifest['counts'],'first_complete_unchanged':True,'final_check_status':checks1['status'],'audit_anchor_check':'pass'}))
