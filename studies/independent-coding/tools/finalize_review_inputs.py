"""Attach output formats and lossless-view documentation before review dispatch.

This adds no coding criteria. It refreshes the review-input manifest to include
the lossless dossiers and runtime documentation.
"""
from pathlib import Path
import json,hashlib,datetime,shutil,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
assert (R/'analysis/all_coding_frozen.json').exists()
audit=[]
for name in ['alignment','source_review_a','source_review_b']:
    d=R/'reviews'/name
    shutil.copy2(R/'protocol/review_output_format.json',d/'output_format.json')
    notes='''Execution notes: use only this assigned review directory and normal Python/runtime documentation. Do not inspect parent directories, other agents, other review output, or external sources. The historical evaluation-design sections in supplied guides describe earlier studies; they do not authorize new model calls or override this review assignment.

The three per-case dossier JSON files are lossless views of annotations.json. Each evidence_ref resolves to source_id/span in that case's evidence_pool. A unit's span reference resolves to the span member of that object. You can reconstruct or inspect full annotations as needed. No coded field has been removed from the source-review dossiers. All sources are in F01_packet.json, F02_packet.json, and F03_packet.json. Work case by case and save incremental review records so context compaction does not lose findings. Do not skip annotations or fields merely because another annotation appears similar.

Use output_format.json for the requested output structure. It is a format specification, not a substantive coding key. Cite exact source_id/start/end/quote anchors. Relations have no intrinsic IDs: refer to their zero-based path, such as relations[0], and give endpoints/type in the description. Summary paths should identify the exact outcome or mechanism. Complete all applicable fields and distinguish substantive errors from representation conventions and defensible alternatives. Do not invent a mandatory rule that the assigned guide does not supply.

For source reviews, save review.json with findings and coverage. Each finding should concern a bounded proposition/error issue/case, with all affected annotations listed. Every coverage row must list all checked unit IDs and all packet entry IDs, confirm relations and summary checks, and list units with no identified error. Preserve genuine review limits; do not claim checks you did not perform. For alignment, save alignment.json with all focal statement units assigned exactly once, and explain split/combined/unmatched/unresolved groups. Both tasks must save access_record.json describing files and coverage. Freeze your first complete result before any later correction. Return a concise completion and paths.
'''
    (d/'RUNTIME_NOTES.txt').write_text(notes)
    # Observe possible residual identifiers without modifying frozen research data.
    strings=(d/'annotations.json').read_text()
    patterns={
       'literal_run_ids':r'F0[123]_v0[34]_r[123]',
       'explicit_project_version_mentions':r'(?i)(?:version|specification|codebook)\s+(?:0\.[34]|v0[34])'
    }
    audit.append({'review':name,'possible_identifier_mentions':{k:len(re.findall(p,strings)) for k,p in patterns.items()},'masking':'Partial; structure, component choices, and prose may reveal assigned conventions.'})
    write(d/'input_manifest.json',{'prepared_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':{p.name:sha(p) for p in d.iterdir() if p.is_file() and p.name!='input_manifest.json'}})
write(R/'analysis/review_masking_audit.json',audit)
print(json.dumps(audit))
