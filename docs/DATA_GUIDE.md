# Data guide

## Reading the evidence

Start with `studies/baseline/analysis/claim_index.csv` for a compact list of all 48 focal claims. `claim_ledger.json` supplies the evidence and assessments; `focal_ig_records.json` supplies the grammatical projections. The `sources/packets/` files retain each episode's discussion and separately identified supplements.

For the Core–Knots application, start with `studies/core-knots/analysis/case_comparison.json`. `inherited_units_used.json` contains 46 retained units: 40 repository units and six transcript statements. `institution_action_links.json` connects statements to decision objects and actions. `state_replay.json` records selected main-branch changes. `evidence_anchors_inherited.json`, `github_sources_used.json`, and `podcast_passages_used.json` provide the supporting passages.

Independent coding is under `studies/independent-coding/runs/`. Run identifiers combine case, specification, and repetition, such as `F01_v04_r1`. First complete and final independent outputs remain separate from `studies/collaborative-review/dataset/adjusted_annotations/`. The latter are reviewed derivatives, not additional independent observations.

## Identifiers and spans

| Identifier | Meaning |
| --- | --- |
| E01–E12 | Routine development episodes |
| F01–F03 | Cases in the paired coding evaluation |
| C1–C6 | Linked Core–Knots proposals; C6B is a supporting backport |
| U, D, N | Retained statement identifiers within the relevant study |
| PU / PE | Transcript unit / passage identifiers |
| E, N9, R10E | Exact evidence anchors in successive Core–Knots stages |
| IL | Statement-to-action links in the comparative analysis |
| L01–L06 | Follow-up claims concerning linked project records and panel context |

Prefixes are local to their study. Use a study path together with an identifier; do not treat matching labels in different folders as the same record.

Spans use zero-based Unicode character positions, with the end position excluded. Match them against the decoded entry text specified by the record, preserving original line endings. Source packets identify URLs, collection context, and available commit or revision identities. A retrieval date and the date of the event described are different fields.

## Retained decisions

Project specification 0.3 supports the baseline and Core–Knots application. The independent experiment compares 0.3 and 0.4; collaborative review uses frozen 0.4. Specification 0.4.1 clarifies recognition-summary instructions and packet metadata handling without replacing historical coding or scores.

The Core–Knots inputs retain seven recordings and 27 selected passages after source review. The unavailable P5158 interview and PE25–PE27 / PU08–PU10 remain excluded. PU03 uses only the retained clear release-role clause. Follow-up panel passages PE28–PE30 remain separately labeled context. Full podcast transcripts and unpublished book chapters are not distributed.

Agreement measures, source-supported interpretations, and reviewed conclusions answer different questions. The records preserve those distinctions through separate folders, status fields, and change ledgers.
