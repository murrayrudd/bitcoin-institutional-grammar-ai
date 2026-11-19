# Distribution provenance

Repository package **1.0.0**, prepared November 19, 2026, accompanies SSRN DOI **10.2139/ssrn.7710701**. The published title and citation metadata are recorded in `provenance/paper_metadata.json`, retrieved from the DOI's Crossref record on that date.

The package draws on `Bitcoin_IG2_Complete_Release_v0.4.1.zip` and its preserved research stages. Input archive identities are recorded in `provenance/source_archives.json`. Each copied research file has an original path, byte count, and SHA-256 in `provenance/source_file_map.json`. The root manifest defines this distribution; archived manifests describe their original packages and are not inventories of the new repository.

## Version relationships

| Material | Research version |
| --- | --- |
| Twelve-episode baseline and Core–Knots application | Project coding specification 0.3 |
| Earlier overlapping review | Project coding specification 0.3 |
| Eighteen-run paired evaluation | Project coding specifications 0.3 and 0.4 |
| Collaborative review | Frozen specification 0.4, with separately identified adjusted copies |
| Reusable coding instructions | Release 0.4.1; annotation schema and checker behavior remain 0.4 |
| GitHub distribution | Package 1.0.0 |

## Packaging adaptations

The original coding, source packets, annotations, review decisions, agreement results, and analytical outputs remain byte-preserved. Three working scripts have portability changes:

- `studies/core-knots/build_analysis.py` reads the 11 required inherited files directly from `inputs/round5`, `inputs/round9`, and `inputs/round10`. It previously opened nested archives containing those same files. Its output retains the original archive identity as historical provenance.
- `studies/core-knots/verify_model.py` verifies the retained input files individually instead of reopening the original nested archives. Its evidence-span, actor, chronology, statement, citation, and state-consistency checks remain unchanged.
- `studies/followup/build_ledger.py` resolves its source directory relative to its current location.

The original scripts are retained under `provenance/original-core-knots/` and `provenance/original-followup/`. No analytical output changes arise from these adaptations. Reproduction compares the rebuilt outputs with the preserved research files.

The original overlap archive verifier and manifest are retained under `provenance/original-overlap/`. They refer to complete historical input archives that are not redistributed here. The overlap study's working comparison and retained annotations remain available. The original 0.4.1 release manifest is preserved separately for tracing source-file identities.

## Distribution choices

The repository contains selected source records, complete independent coding runs and review records, needed earlier-stage evidence, reusable instructions, and stage reports. It excludes superseded working-paper drafts, unpublished book chapters, full podcast transcripts, and nested archives whose required inputs are already supplied directly. Two small original specification/reconciliation archives remain under `specification/evidence/` because the unchanged 0.4.1 compatibility test reads them.

The full parent corpus is not bundled; its identity and selected records are retained. Historical scripts that created source packets or dispatched model work may contain old workspace paths. Those paths are provenance, not requirements for the root reproduction commands.

Source material remains attributed to its original repositories, contributors, recordings, and documents. Source URLs and collection records are preserved in the study files. Stage-specific status text and interpretation limits describe the research at that stage; the published paper supplies the integrated account.
