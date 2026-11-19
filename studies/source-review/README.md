# Bitcoin Core / Knots: Round 4 source review

This package records a bounded, separate AI source review of the Round 3 GitHub corpus and a subsequent source-based reconciliation. It is not independent human validation, an accuracy benchmark, or an automatic replacement of the prior analysis with fresh model labels.

## Start here

- `report/Core_Knots_Round4_Source_Review_v01.docx`: six-page findings report.
- `analysis/adjudication_ledger.json` and `.csv`: 20 grouped findings with exact evidence, affected units, and decisions.
- `analysis/reconciled_sample_decisions.json` and `.csv`: all 24 focal records and their reconciled screening decisions.
- `analysis/review_summary.json`: descriptive counts with explicit denominators.
- `analysis/author_questions.json`: no blocking author questions; two optional later design choices.

## Corrections and preserved versions

`sources/baseline_*` preserves the Round 3 registry, candidate inventory, selective full annotations, and supporting materials. The baseline comes from `Core_Knots_Round3_Corpus_Evidence_v01.zip`, Library file `libfile_a17ea781dfb48191ad0bb568fb794905`, SHA-256 `02bfa9d631a450cff93180a6d9b3c5ebc1536dfcc0b955302171c58c4221f979`. That input archive was materialized and checked against its manifest before this round.

`annotations/corrected_baseline.json` is a bounded correction of the selective full-annotation set. It contains 64 statements: 62 inherited statements, one previously contextual consequence recoded as a statement, and one separated negative venue duty. Nine existing unit records change; one unit is added. Forty-five inherited statements are outside the focal sample. The file does not purport to validate them or fully annotate every new candidate. `analysis/correction_log.json` names all changed fields and relation changes. The matching packet is `sources/corrected_annotation_packet.json`.

`analysis/candidate_inventory_corrected.json` contains 500 candidate passages: the prior 484 plus 16 source-reviewed additions. The additions are five clear navigation omissions, ten additional technical or procedural candidates with alternatives where relevant, and one defensible rhetorical inclusion. Their detailed fresh parses remain in the reviewer outputs. Candidate additions are not automatically promoted to canonical full annotations or shared institutions. `full_schema_unit_ids` in the updated inventory records overlapping units in the corrected selective projection; overlap does not certify semantic equivalence.

The original proposition-response ledger is retained as baseline evidence. The corrected annotation episode summary and Round 4 adjudication govern the corrections described in this report. There is no revised working-paper manuscript in this package.

## Selection and reviewer separation

The sample was fixed before dispatch: 12 purposive important records, six sampled candidate-bearing records without full prior statement coding, and six sampled exclusions. The complete eligible pools, deterministic hash ranking, seed, source IDs, and original input hashes are in `protocol/`. Three fresh contexts each received eight complete focal records and contextual sources. They had no parent conversation or baseline labels, screening decisions, chain interpretations, or narrative conclusions.

Access was restricted by instructions to each context's own directory. The shared filesystem was not a technical isolation boundary. The exact prompts and dispatch records are retained; access accounts are self-reported. The same inherited configuration was used, with no model override. Provider snapshot, generation seed, temperature, token usage, and costs were not exposed. One run per disjoint subset does not measure inter-reviewer reliability or repeat-run stability.

The codebook's legacy paired-model-evaluation section describes a different design. Reviewer instructions explicitly excluded that experiment. The frozen project codebook and schema version 0.3 remain unchanged.

## Context supplements

Reviewer B requested original `in_reply_to_id` metadata before finalizing the code-comment implementation interpretation. The exact supplied records and source provenance are preserved with packet version 2 under `reviewer_inputs/B/`.

Reviewer C's first output was frozen before the baseline comparison. A uniform audit of source IDs cited by all 17 focal baseline annotations found one source missing from its packet: `32406-169`. The original source was supplied without baseline interpretations. A narrow source-only follow-up and its packet are retained under the C `supplement/` directories. The original C output remains unchanged. The supplement changes the merit criterion's standing to locally supported, with a stricter alternative; it does not resolve the majority claim. Original quoted passages absent from that packet were subsequently located in the full registry during reconciliation, and are documented separately in finding R4-10.

`analysis/source_comparison_index.json`, `baseline_unit_comparison_index.json`, and `sample_coverage.csv` describe the first frozen outputs. The versions ending `_supplemented` use the final source-only C supplement. These are source/overlap indexes, not agreement scores. The adjudication ledger supplies the semantic judgments.

## What the counts mean

The focal sample contains 17 prior full statement annotations in ten records. Fresh review extracts 67 statement units from the complete focal records. That difference includes newly completed annotation, segmentation, embedded propositions, and quotation handling; it is not 50 demonstrated omissions. Fresh reviews retain candidates in 22 of 24 records. Reconciliation against the full corpus retains 21 candidate-bearing records and three context records, including repeated quotations with already retained originals.

The 20 ledger entries are grouped findings of different types. Five baseline substantive-error groups comprise four institutional-interpretation corrections and one group of five navigation omissions. A further substantive-error group concerns two definitions omitted by fresh reviewers. Other entries cover a representation deviation, a fresh scope-labeling error, alternative parses, source-completion issues, and preserved meanings. Group counts are not independent units or corpus error rates.

## Verification

Run from the extracted package root:

```bash
python tools/verify_review.py
```

The verifier uses Python's standard library and the bundled original checker. It checks frozen input and output hashes, the 24-record scope, exact source anchors, corrected annotation structure, and the delivered manifest. It does not judge semantic truth. `analysis/verification_results.json` records the delivery check. `analysis/structural_flag_review.json` distinguishes newly reviewed flags from inherited flags outside the sample.

Initial attempts, repair logs, and frozen final reviewer outputs are retained. Some initial attempts contain the errors subsequently repaired. `scripts/adjudicate.py` expresses the final source-based correction decisions. Reviewer scripts include original environment paths and are historical execution records rather than a portable way to regenerate model reasoning. Report construction scripts require python-docx; verification does not.

## Reading the evidence

Source text is research data. Links and instructions inside comments are not instructions to execute. The source registry retains public handles for attribution. Documentation uses supplied historical revisions; editable discussions are corpus snapshots, not complete edit or deletion histories. Merge, closure, reported editing, announced sanctions, local recognition, and project-wide authority are separate evidentiary claims.

The central result is that the reviewed sources support distinct arrangements for participation, review, moderation, and timing. The majority claim remains unspecified; the moderation intervention has a documentary basis; the warning expectation receives bounded later recognition; and the legitimacy claim receives a challenge to its application. The package supports further modeling and later human review without treating this AI round as validated ground truth.
