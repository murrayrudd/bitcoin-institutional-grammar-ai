from pathlib import Path
import json, hashlib, shutil

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / 'package'
B = ROOT / 'baseline/Core_Knots_Round3_Corpus_Evidence_v01'
SEED = 'CoreKnots_R4_20261106_v01'
def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def rank(sid, tag): return hashlib.sha256((SEED+'|'+tag+'|'+sid).encode()).hexdigest()

R = {e['source_id']:e for e in json.loads((B/'sources/all_source_registry.json').read_text())}
S = json.loads((B/'analysis/screening_judgments.json').read_text())
C = json.loads((B/'analysis/candidate_passages.json').read_text())
A = json.loads((B/'annotations/final.json').read_text())
L = json.loads((B/'analysis/proposition_response_ledger.json').read_text())
candidate_sids = {c['source_id'] for c in C}
coded_sids = {u['source_id'] for u in A['units'] if u['record_role']=='statement'}
prs = [32359,32381,32406,32714,33224,33453]
anchors = ['32359-038','32359-115','32359-227','32381-body','32406-149','32406-178',
           '32406-228','32406-252','32714-body','33224-010','33453-018','33453-body']
plan = {
 'round':4,'date':'2026-11-06','title':'Separate AI source review',
 'baseline_library_file_id':'libfile_a17ea781dfb48191ad0bb568fb794905',
 'baseline_zip_sha256':sha(ROOT/'incoming/Core_Knots_Round3_Corpus_Evidence_v01.zip'),
 'purpose':'Source-first recoding of a fixed subset, then source-based reconciliation against Round 3; not independent human validation.',
 'selection_seed':SEED,'purposive_source_ids':anchors,
 'additional_sampling':'One candidate-bearing source per PR with no baseline full statement annotation, excluding anchors; one nonempty source per PR with no retained candidate and screen class A/C/Q/R. Eligibility is 30 to 2400 Unicode characters. Rank eligible IDs by SHA-256(seed|stratum|source_id); select the minimum. Preserve every eligible ID and hash.',
 'review_assignment':'Three fresh contexts, each four purposive entries, two sampled candidate entries, and two sampled excluded entries; order randomized by a fixed hash. No sample labels, prior annotations, screening decisions, response interpretations, or narrative conclusions supplied.',
 'scope':'All propositions within each complete focal source record, including overlooked prescriptions; supporting sources used for interpretation, recognition, and disposition only.',
 'context_selection':'Preserve the six proposal bodies, metadata, selected final patch contexts, and four dated procedural documents. Add adjacent discussion records and all source records in an existing response chain touching a focal source. Only source text and metadata are supplied, without chain titles, roles, conclusions, or baseline labels. Context selection itself is informed by prior work.',
 'reviewer_access':'Prompt-restricted to its own input directory. Shared filesystem is not a technical sandbox. No parent conversation is inherited. Public author handles, PR IDs, and codebook examples remain visible.',
 'requested_configuration':'Inherited parent configuration; no model override requested. Actual provider snapshot, seed, temperature, and token cost are not exposed.',
 'freeze':'This protocol, selected IDs, source packets, codebook, schema, and prompt hashes are saved before reviewer dispatch. Fresh outputs are frozen before baseline comparison.',
 'comparison':'Compare source coverage, proposition meaning, grammar and components, force, evidence standing, governance levels, and response/disposition links. Count grouped findings and affected records separately. Distinguish substantive errors, epistemic labeling errors, convention deviations, defensible alternatives, and unresolved judgments. A reviewer output is evidence for review, not a gold standard.',
 'coverage_boundary':'Selective full annotation in Round 3 means newly coded propositions are not automatically baseline omissions. An omission in the candidate screen requires absence from the candidate inventory, not merely absence from final.json.',
 'execution_boundary':'One source-first run per disjoint shard. Mechanical repairs may precede final output freeze and must be disclosed. No semantic feedback or baseline disclosure before freeze. No repeated-run reliability or population accuracy estimate.',
 'deliverables':['Review report','Discrepancy ledger with exact evidence','Frozen reviewer packets and outputs','Adjudicated corrections or addendum with prior version preserved','Short list of unresolved questions if any require author judgment']
}
dump(P/'protocol/review_plan.json',plan)
chosen = []
pools = []
for pr in prs:
    for tag in ['candidate','excluded']:
        eligible = [sid for sid in S if R[sid].get('pr')==pr and sid not in anchors
                    and 30<=len(R[sid]['text'])<=2400
                    and (sid in candidate_sids and sid not in coded_sids if tag=='candidate'
                         else sid not in candidate_sids and S[sid]['screen_class'] in ['A','C','Q','R'])]
        eligible.sort(key=lambda sid:rank(sid,tag))
        assert eligible,(pr,tag)
        pools.append({'pr':pr,'stratum':tag,'eligible':[{'source_id':sid,'rank_hash':rank(sid,tag)} for sid in eligible],'selected':eligible[0]})
        chosen.append({'source_id':eligible[0],'stratum':tag,'pr':pr})
focal = [{'source_id':sid,'stratum':'purposive','pr':R[sid]['pr']} for sid in anchors]+chosen
assert len(focal)==24 and len({x['source_id'] for x in focal})==24
dump(P/'protocol/selection_pools.json',pools)
groups = {k:[] for k in ['A','B','C']}
for tag in ['purposive','candidate','excluded']:
    ids = sorted([x['source_id'] for x in focal if x['stratum']==tag],key=lambda sid:rank(sid,'assign_'+tag))
    for i,sid in enumerate(ids): groups[['A','B','C'][i%3]].append(sid)
context_global = {e for e in R if not e[0].isdigit()} | {f'{pr}-body' for pr in prs}
context_global.discard('M33473')
# The backport disposition is available as source context without introducing another discussion thread.
context_global.add('M33473')
for group, ids in groups.items():
    ids.sort(key=lambda sid:rank(sid,'display'))
    context = set(context_global)|set(ids)
    for sid in ids:
        pr,tail=sid.split('-',1)
        if tail.isdigit():
            for n in [int(tail)-1,int(tail)+1]:
                key=f'{pr}-{n:03d}'
                if key in R: context.add(key)
        for chain in L:
            if any(s['source_id']==sid for s in chain['stages']):
                context |= {s['source_id'] for s in chain['stages']}
    packet={'episode_id':'CoreKnots_R4_'+group,'project_codebook_version':'0.3',
            'selection_design':{'focal_source_ids':ids,'scope':'Fully screen and code the complete focal entries. Other entries are supporting context only; their context-only screen disposition means outside focal extraction scope, not an assertion that they contain no institutional statements.'},
            'entries':[R[sid] for sid in sorted(context)]}
    d=ROOT/'reviewer_workspaces'/group
    (d/'protocol').mkdir(parents=True,exist_ok=True);(d/'tools').mkdir(exist_ok=True)
    dump(d/'packet.json',packet)
    for f in ['codebook.txt','annotation_schema.json']: shutil.copy2(B/'protocol'/f,d/'protocol'/f)
    shutil.copy2(B/'tools/check_annotation.py',d/'tools/check_annotation.py')
    prompt=f'''You are a source-first institutional grammar reviewer. This is an explicitly authorized separate AI review. Do not spawn additional agents.

Your only research inputs are inside {d}. Do not inspect parent directories, other reviewer folders, prior analyses, the Library, conversation history, or external sources. This restriction preserves separation from earlier interpretations. You have not been given the earlier annotations. You may use Python and the supplied checker to build and verify your own output. Write your work only in this directory.

Read protocol/codebook.txt and protocol/annotation_schema.json. Apply the frozen project v0.3 coding conventions. The codebook section titled Paired evaluation and references describes a different historical study; do not execute its sampling, model comparison, or delegation instructions. The references and conventions remain available. Do not revise the codebook or checker.

Read packet.json completely, paying particular attention to selection_design.focal_source_ids. There are eight complete focal records. Extract every relevant proposition in those focal records, including technical requests where the codebook treats them as statements. Do not assume every focal record contains a statement. Keep nonstatement exclusions and their reasons. Supporting entries are for context, recognition, authority, and disposition; they need not receive exhaustive component coding. Mark their entry_screening reason as supporting context outside focal extraction scope unless you add necessary relation-endpoint units. Do not treat missing evidence in the supplied packet as proof nothing happened elsewhere. You may ask the coordinator for a specifically identified missing source before finalizing; any addition will be recorded.

Create full schema-compliant annotation.json, with run_id R4_{group}_source_first, the packet's episode_id and SHA-256, complete entry_screening, units, relations, and episode_summary. Distinguish grammatical expression from institutional standing; retained author claims do not establish truth. Preserve exact quotes, force, negation, material conditions, occurrence roles, attribution, and alternatives. Review whether the supplied context establishes specific expectation recognition, broader endorsement, a reply, reported implementation, or recorded disposition. Infer no causal effect from chronology alone. Do not count a merge, an ACK, or implementation as automatic proof of a norm. Check inferred versus explicit component claims carefully. Meaning-preserving alternatives are acceptable and should be explained.

Also write review_notes.json with per-focal-source decisions, any missing context, reasonable alternative analyses, interpretive uncertainties, and a short source-grounded account of any response sequence you can establish. Include exact source IDs and quotes for material claims. Do not report agreement with earlier work because it is unavailable to you. State the file paths you accessed and whether any disallowed material was encountered.

Use tools/check_annotation.py packet.json annotation.json to run the unchanged structural checker. Keep the final checks in checks.json. You may correct mechanical output errors before final submission; save a brief repair_log.json stating what was repaired. Passing the checker is not semantic validation. Before finishing, review your interpretations against the original text once. Preserve your source-first annotation as final for this phase; do not compare it with prior work. Return only a compact completion summary, counts, uncertainties, and paths. The coordinator will freeze and hash your output before any comparison.
'''
    (d/'REVIEW_TASK.txt').write_text(prompt)
    dump(d/'input_manifest.json',{'group':group,'files':[{'path':str(f.relative_to(d)),'sha256':sha(f)} for f in sorted(d.rglob('*')) if f.is_file()]})
    for x in focal:
        if x['source_id'] in ids:x['reviewer_group']=group
    print(group,'focal',ids,'context_sources',len(context),'chars',sum(len(R[sid]['text']) for sid in context))
dump(P/'protocol/selected_sample.json',focal)
for f in ['codebook.txt','annotation_schema.json']: shutil.copy2(B/'protocol'/f,P/'protocol'/f)
shutil.copy2(B/'tools/check_annotation.py',P/'tools/check_annotation.py')
for f in ['all_source_registry.json','annotation_packet.json']:shutil.copy2(B/'sources'/f,P/'sources'/('baseline_'+f))
for f in ['candidate_passages.json','screening_judgments.json','proposition_response_ledger.json']:shutil.copy2(B/'analysis'/f,P/'sources'/('baseline_'+f))
shutil.copy2(B/'annotations/final.json',P/'sources/baseline_annotations.json')
dump(P/'protocol/frozen_inputs.json',{'baseline_zip':sha(ROOT/'incoming/Core_Knots_Round3_Corpus_Evidence_v01.zip'),
 'protocol_files':{str(f.relative_to(P)):sha(f) for f in sorted((P/'protocol').glob('*')) if f.is_file()},
 'reviewer_input_manifests':{g:sha(ROOT/'reviewer_workspaces'/g/'input_manifest.json') for g in groups}})
print('Focal sources with baseline full statements',len(set(x['source_id'] for x in focal)&coded_sids))
print('Baseline full statements in focal sources',sum(u['record_role']=='statement' and u['source_id'] in {x['source_id'] for x in focal} for u in A['units']))
