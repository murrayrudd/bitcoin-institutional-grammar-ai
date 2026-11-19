Bitcoin Core IG2 fresh coding: completed prospective evaluation
November 7, 2026

STATUS: All 18 independent coding runs, masked proposition alignment, both independent source audits, and coordinator reconciliation are complete. The companion report is Bitcoin_Core_IG2_Fresh_Coding_Results_v01.docx. Start with analysis/report_status.json, analysis/reconciliation.json, and analysis/adoptable_case_claims.json.

Result: The comparison does not demonstrate better overall repeatability or fewer source-supported evidence-basis error groups under project specification 0.4. The common 42-proposition subset has all-three/all-six-field agreement of 24/42 under 0.3 and 21/42 under 0.4. Reconciliation identifies one evidence-basis group under 0.3 and four under 0.4, with disclosed sensitivity to effect classification. These are descriptive judgments, not accuracy rates, population rankings, or human/cross-model comparisons.

Original annotations remain unchanged and contain identified defects. The eight bounded case conclusions and reconciliation ledger identify usable claims and required restrictions. This package contains no negotiated-consensus annotation from the original coders. A final reviewer or coordinator judgment is not a reference truth set.

Contents
  protocol/        Frozen design, selection, exposure inventory, and dispatch hashes.
  specifications/  Original project specifications 0.3 and 0.4, schemas, and checkers.
  sources/         Selected canonical corpus lines and identical source packets.
  source_receipts/ Retrieval receipts for common contextual supplements.
  provenance/      Parent corpus and development-package identities.
  runs/            All 18 first-complete/final outputs, checks, repairs, and access logs.
  reviews/         Frozen masked alignment and both complete independent source audits.
  analysis/        Agreement, supplementary alpha, source reconciliation, bounded claims,
                   operational diagnostics, freeze records, and final report content.
  checkpoints/     Historical interruption material. Its pending-status text describes
                   the interruption only; it does not override the completed status.
  tools/           Analysis, verification, adjudication, and document-building scripts.

Reproduction
Use a copy of the archive: several analysis scripts write their results. The standard-library analysis scripts use paths relative to this root. The original builders tools/prepare.py and tools/assemble.py retain historical workspace assumptions and are provenance, not portable entry points. Do not run evaluate.py mask, finalize_review_inputs.py, or review_views.py over these completed review directories.

  python3 tools/verify_package.py
  python3 tools/verify_final_evaluation.py
  python3 tools/evaluate.py verify
  python3 tools/metrics.py
  python3 tools/supplementary_alpha.py
  python3 tools/verify_alpha.py
  python3 tools/run_descriptives.py

The last scripts regenerate analysis outputs, so their new timestamps can differ from PACKAGE_MANIFEST.json. The manifest verifies the distributed snapshot, not later reanalysis. tools/reconcile_reviews.py reproduces the coordinator's explicitly encoded qualitative adjudications; it does not discover truth automatically. tools/prepare_case_claims.py reproduces bounded conclusions from frozen anchors. tools/prepare_final_report.py and tools/build_report.py reproduce report content and DOCX; python-docx is required for the latter. Assigned coding checkers require jsonschema. Environment versions appear in analysis/environment.json.

Selection
The canonical parent corpus has 25,508 PR records, of which 226 conservatively recorded prior exposures/references were excluded. Only the three selected raw corpus lines are included here. The full parent corpus is not duplicated. Its SHA-256 is b289aa40737d619dea8a673290fae636dbe1a65ccf49331223ab548acb23f7c9. Full selection reconstruction requires those exact parent JSONL bytes:
  python3 tools/verify_selection.py /absolute/path/to/prs_canonical.jsonl
The retained analysis/selection_verification.json records a successful full-corpus reconstruction. Without the optional corpus argument the script checks only the retained selection inputs; it does not reproduce the full population ranking.

Mechanical result
The original final checks pass 15/18 runs. Three F01 version 0.4 runs retain nine metadata-identity failures. Separate post-freeze diagnostic copies expose already-present source identities under the checker's expected keys and pass 18/18. That diagnostic neither replaces the original workflow result nor establishes semantic correctness.

Continuity and historical status fields
The coding and alignment survived a weekly usage interruption. Both existing source-review contexts resumed from their own files. The frozen protocol's original design-stage status fields and the historical recovery report must be read as dated provenance. The final status, report, audits, and reconciliation supersede their pending-work statements without altering them. No original coding or alignment run was repeated.
