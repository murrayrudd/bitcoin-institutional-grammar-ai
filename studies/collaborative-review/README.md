# Bitcoin Core IG2 collaborative reconciliation

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
