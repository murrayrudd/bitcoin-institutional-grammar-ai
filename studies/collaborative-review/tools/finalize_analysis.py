from pathlib import Path
import json,hashlib,datetime,copy
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
agenda=read(R/'agenda.json');groups=read(R/'inputs/analysis/reconciliation.json')['groups'];changes=read(R/'analysis/change_log.json')
finals={a:read(R/f'panel/{a}_final.json') for a in 'ABC'}
records=[
('D01','Corrected identity with retained interpretive disagreement',
 'Future cleanup remains unidentified. The general retention criterion has no applicable numbered decision object; #26586 remains the discussion episode. All reviewers accept these identity distinctions. A and B prefer ordinary tentative assent; C prefers unresolved expectation recognition. Full-proposition and broader-principle targets both remain defensible in context.',
 'Identity fields are corrected. The three existing assent encodings remain, with the alternatives explicit. The final analytical claim is tentative assent to the recurring retention floor, with institutional recognition and exact assent scope unsettled.',
 ['Do not claim an adopted retention policy, binding authority, or repeated independent recognition.','Do not transfer the containing PR merge to future work.']),
('D02','Corrected scope with a retained specification ambiguity',
 'The later open-and-rebase method omits the original until-another-PR-needs-it condition. Same-actor review-now correspondence preserves personal continuity. After inspecting the frozen checker, all reviewers retain response events and recognition none, while exposing the prose/checker tension.',
 'The partial response now targets the broader method. Event records retain same-actor continuity. The checker and codebook remain unchanged; no response is upgraded to expectation_recognition merely to produce same_actor_only.',
 ['The profile none does not mean no personal continuity was expressed.','No interpersonal recognition or verified body-versus-comment wording chronology follows.']),
('D03','Resolved evidence distinction with explicit missing information',
 'The integrated release-note artifact establishes the requested spelling. It does not reconstruct the prior typo or correction history. The checkbox patch is observable even though unmerged, but the supplied fragments do not verify every qualification of the complete checkbox proposition.',
 'F02 r1 now records observed resulting spelling alongside its reported-application record. Complete checkbox application is unresolved in all three views; narrower artifact facts remain in outcomes.',
 ['Do not infer a verified before-and-after correction sequence.','Do not infer complete placement, missing workflow implementation, or repository integration from the checkbox artifact.']),
('D04','Agreed evidence limits with retained report-scope alternatives',
 'All reviewers accept contextual reported incorporation of the identified release-note suggestions as a reasonable preferred reading. They retain broader-proposal targeting as defensible. A rebase on master does not establish fulfillment of the after-#26589 condition.',
 'The original focal versus broader report scopes remain in the adjusted views. All three rebase records preserve the broad action report and explicitly mark complete conditional fulfillment unresolved.',
 ['Do not pair isolated fixed or Both replies to individual changes without evidence.','Do not equate reports with patch verification or verbatim adoption of every offered phrase.']),
('D05','Agreed uncertainty about institutional type',
 'Needs rebase supports a maintenance request but does not select between technical necessity and a proposed social expectation. All reviewers prefer undetermined in the synthesis while retaining norm_candidate as a serious alternative.',
 'Primary type variants remain. Missing alternatives are added, and the rationale that treated recurrence as necessary for a proposed norm is corrected.',
 ['Do not infer an institutional obligation, authorized merge gate, or enforcement from needs.','A proposed norm does not need to be already shared or recurring.']),
('D06','Resolved distinction between analytical layers',
 'Performing release-selection work is operational. Proposing a recurring selection arrangement can target collective choice. Conditional developer discretion can be represented as an allocation or as the resulting conduct, provided the focal layer remains explicit.',
 'Existing primary levels remain where the rationale identifies their layer. Missing operational alternatives are added and the conditional allocation rationale is clarified.',
 ['Constitutive grammar does not establish constitutional authority.','No supplied record establishes a new adopted procedure or authority over Bitcoin network adoption.']),
('D07','Agreed target distinctions with retained scope-dependent projections',
 'The panel converges on a focal readiness-premise challenge when the checkbox statement offers exposure of the feature; an artifact-description layer supports broader targeting. The miniscript criticism reaches only its attached rationale. A proposed directory redesign need not contradict the present implementation prerequisite, and prospective fee-only questioning does not deny a past work report.',
 'Checkbox target variants remain with explicit layer explanations. The specialness challenge uses premise. The current built-copy proposition retains a broader-arrangement challenge and no focal dispute, with the continuing-application alternative visible.',
 ['Do not treat Boolean dispute agreement as complete agreement about meaning.','Do not infer rejection, withdrawal, interpersonal disagreement with oneself, or the contents of unseen #25717.']),
('D08','Corrected direction and selected bounded relation interpretations',
 'Uptake must run from the separate-cleanup proposal to its response. All reviewers prefer clarification for the directly quoted cost concern and temporal order for the less securely attributed release-risk/pause sequence.',
 'The reversed uptake endpoints are repaired. The cost/pruning links use clarifies. The release-risk/pause link uses temporal with recorded creation timestamps and an explicit limitation on reply attribution and causality.',
 ['Context record status alone does not rule out an inferred invitation.','These links establish no completed pruning, formal hold, release withdrawal, or causal influence.']),
('D09','Agreed unresolved software referent',
 'The bot announces a conditional next-update consequence. Its grammatical object it is explicit, but the source does not uniquely identify the software referent. The review is the most plausible linguistic gloss; comment and displayed-listing readings remain possible.',
 'The summary, qualifier, institutional rationale, target activity, and uncertainty description now carry that limit. The explicit grammatical object remains unchanged.',
 ['No observed bot execution, suppression, or sanction follows from the announcement.']),
('D10','Shared type preferences with retained alternatives',
 'The panel prefers strategy candidates for the specific-test and coupled EOL-drop/stored-wallet methods, and a norm candidate for proposed recurring merge restraint. A one-off engineering-preference reading remains defensible. Classification does not itself demonstrate social acceptance.',
 'Primary type variants remain with explicit alternatives and repaired rationales. The adjusted avoid-rushing representation uses the supplied not-rush-merging action. The earlier pragmatic parse remains a defensible alternative, not a newly discovered error.',
 ['Preserve the coupled method, exploratory force, and material conditions.','Do not infer shared norms, authority, or implementation from a candidate label.'])]
decisions=[]
for tid,status,finding,implementation,limits in records:
    item=next(a for a in agenda if a['topic_id']==tid)
    gids=item['group_ids']+(['Q025a'] if tid=='D10' else [])
    anchors=[];seen=set()
    for g in groups:
        if g['group_id'] in gids:
            for e in g['source_evidence']:
                key=json.dumps(e,sort_keys=True)
                if key not in seen:seen.add(key);anchors.append(e)
    decisions.append({'topic_id':tid,'title':item['title'],'status':status,'group_ids':gids,'finding':finding,'implementation':implementation,'limits':limits,'source_evidence':anchors,'panel_final_references':{a:f'panel/{a}_final.json#{tid}' for a in 'ABC'},'change_ids':[c['change_id'] for c in changes if tid in c['decision_ids'] or any(g in c['decision_ids'] for g in gids)]})
write(R/'dataset/decisions.json',decisions)

ledger=[]
for g in groups:
    related=[d['topic_id'] for d in decisions if g['group_id'] in d['group_ids']]
    cg=[c['change_id'] for c in changes if g['group_id'] in c['decision_ids']]
    if related:status='See collaborative decision and retained alternatives'
    elif cg:status='Applied source-reviewed correction to a separate copy'
    elif all(a['condition']=='v03' for a in g['affected']):status='Historical v0.3 convention or alternative retained outside adopted v0.4 views'
    else:status='Retained previously source-reviewed alternative; no new panel adjudication claimed'
    ledger.append({'group_id':g['group_id'],'episode_id':g['episode_id'],'original_category':g['category'],'final_handling':status,'discussion_topics':related,'change_ids':cg,'prior_resolution':g['resolution']})
write(R/'dataset/issue_dispositions.json',ledger)

claims=read(R/'inputs/analysis/adoptable_case_claims.json')['claims']
cases=[]
for case in ['F01','F02','F03']:
    cases.append({'episode_id':case,'case_conclusions':[c for c in claims if c['episode_id']==case],'adjusted_annotation_views':[f'dataset/adjusted_annotations/{case}_v04_r{i}.json' for i in range(1,4)],'source_packet':f'dataset/packets/{case}.json','interpretation':'The views preserve valid unitization and interpretive differences. Consult decisions and limits before aggregating labels. The three views are not independent confirmations of the final adjudication.'})
write(R/'dataset/reconciled_dataset.json',{'dataset_version':'post_evaluation_reconciliation_1','coding_specification':'0.4 unchanged','status':'bounded analytical dataset with explicit alternatives','authoritative_decisions':'dataset/decisions.json','issue_dispositions':'dataset/issue_dispositions.json','cases':cases,'historical_v03_repairs':'dataset/reference_only_v03','original_reliability_unchanged':True,'new_independent_reliability_estimate':None,'scope':'Three retained fresh-evaluation cases; no new source collection, new coding criteria, manuscript editing, or fork extension.'})

write(R/'panel/coordination_log.json',{'design':'Three fresh reviewers, identical instructions and dossiers, initial positions then one peer-response round. No reviewer is represented as an original coder.','initial_access':'Reviewers were instructed not to read peer outputs before their initial submissions. They reported independent initial review. Shared prior audits and coordinator proposals were visible; this is not a blinded validation experiment.','shared_messages':[{'stage':'initial review','message':'Compact dossiers gained omitted qualifier descriptions and resolved relation objects. All reviewers were informed; original sources and annotations were unchanged.'},{'stage':'initial review','message':'Coordinator identified the frozen checker filter for this-proposition expectation_recognition before same_actor_only is projected. B incorporated it before freezing; A and C addressed it as an explicit revision in the peer round.'},{'stage':'peer response','message':'All reviewers received the same digest of the three frozen positions and instructions to respond to peers, retaining source-supported disagreement.'}],'bounded_scope_extension':'D10 peer recommendations also selected a literal representation for U23, already present in the not-rushing dossier. Q025a remains a defensible historical alternative; no new source or criterion was introduced.','rounds_completed':2,'further_round_required':False})

write(R/'analysis/coordinator_disposition.json',{'basis':'Source-supported constraints, explicit peer reasoning, and frozen v0.4 conventions; not a majority-vote truth rule.','selected_representations':['Observed resulting spelling with unverified transformation history','Unresolved complete checkbox application while preserving visible artifact facts','Unresolved after-#26589 fulfillment alongside a broad rebase report','Clarification for the quoted cost concern and temporal order for the weaker response attribution','Literal not-rush-merging representation with the pragmatic alternative retained'], 'preserved_variants':['Ordinary-assent versus unresolved expectation-recognition encoding','Aggregate reports targeted to the focal suggestion versus broader contribution','Technical necessity versus proposed norm','Operational versus collective-choice analytical layer','Offered-feature versus artifact-description challenge scope','Method and restraint candidate types versus undetermined'], 'departures_or_qualifications':['No blanket Q019 target/Boolean replacement was imposed, following the final layer-dependent qualification.','No blanket F02 report-target conversion was imposed; the final dataset retains the explicit alternative scopes.','Type preferences remain in the analytical overlay and alternatives rather than being imposed across every view.','The U23 literal parse is adopted as a preferred representation, not the decided error correction claimed in one initial recommendation. The earlier source review treated its reconstructed avoid-rushing parse as defensible.','Q012 unresolved target also requires unresolved basis under the unchanged checker; its textual correspondence remains in the rationale.']})

readme='''# Bitcoin Core IG2 collaborative reconciliation

Start with `dataset/reconciled_dataset.json`. It links the three cases, eight bounded case conclusions, nine adjusted v0.4 annotation views, and the authoritative decision overlay. Read `dataset/decisions.json` for the ten discussion topics and retained limits. The views deliberately preserve some valid coding alternatives; do not count them as independent confirmations or treat all field differences as unresolved factual contradictions.

## Provenance and interpretation

The original independent coding and reliability results remain unchanged. `inputs/` contains byte-preserved source packets, nine v0.4 annotations, two v0.3 annotations needed for a historical chronology repair, the frozen v0.4 codebook/schema/checker, and prior adjudications. The full independent evaluation remains in the separate parent evidence package identified by SHA256 in `protocol.json`.

Three fresh reviewers produced `panel/A_initial.json`, `B_initial.json`, and `C_initial.json`, then read all initial positions and produced the corresponding `_final.json` peer responses. These are deliberative adjudication records, not fresh independent coding, human validation, or a cross-model comparison. Hash records freeze both rounds. `panel/coordination_log.json` records shared clarifications and the bounded scope extension.

`analysis/change_log.json` records every changed JSON path with before/after values and reasons. `dataset/issue_dispositions.json` maps all 59 prior issue groups. `dataset/reference_only_v03/` repairs unsupported wording chronology in two separate historical copies; these are not adopted v0.4 outputs and do not alter prior v0.3 scores.

## Fixed specification and technical adaptation

The v0.4 codebook, schema, and checker remain unchanged. New packet copies expose revision/blob identifiers already present in retained metadata under the field names expected by the checker. Their source text is identical. `analysis/metadata_adapter.json` records every added alias and packet hash. Adjusted annotation IDs and packet hashes identify post-evaluation copies.

Same-actor response events preserve personal continuity, although the frozen checker projects only this-proposition expectation-recognition events into the recognition summary. The resulting `none` is not evidence that no continuity occurred. The decision overlay exposes this specification ambiguity; no artificial expectation-recognition event has been created to obtain a desired summary.

## Reproduction and verification

Use Python with jsonschema to run `tools/build_dataset.py` against the retained patch plan. This reconstructs the adjusted copies and checker results. `tools/prepare_patch_plan.py` documents the coordinator-selected implementations of panel recommendations; it is not an automatic truth or voting algorithm. `tools/verify_reconciliation.py` verifies frozen inputs, exact source anchors, change-log replay, decisions, and package integrity. The preparation script records how dossiers were assembled from the separate parent package and is not needed to use the reconciled dataset.

No post-discussion alpha or agreement percentage is presented as independent reliability. Consensus, source support, and independent coding reproducibility remain distinct.
'''
(R/'README.md').write_text(readme)
write(R/'analysis/analysis_completion.json',{'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'discussion_topics':len(decisions),'initial_positions':30,'peer_responses':30,'prior_groups_accounted_for':len(ledger),'case_conclusions':len(claims),'codebook_changed':False,'manuscripts_changed':False,'final_artifacts_pending':True})
print('Decision overlay and 59-group dispositions complete')
