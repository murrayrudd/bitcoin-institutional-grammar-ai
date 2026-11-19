# Core and Knots comparative institutional model — Round 11

Version 0.1 · November 6, 2026 · America/Vancouver

The report compares six linked proposals in the 2025 datacarrier dispute. It connects preferences, normative claims, roles, and exercised actions to each disposition. A deterministic replay reconstructs the selected main-branch changes; it does not predict acceptance or simulate operator behavior.

## Main results

- Open participation coexists with distinct controls over proposal form, integration, moderation, and release targeting.
- Three proposals close without merge, through different acts: glozow closes C1; darosior closes the authored C2 proposal; achow101 closes the authored C4 proposal. These events should not all count as maintainer vetoes.
- Achow101 subsequently merges C5 and C6. The comparison attaches roles to particular actions and objects rather than assigning actors permanently to opposing camps.
- The integrated sequence raises the default and changes output budgeting, softens the removal warning, then removes deprecation and the warning. Configuration remains available. C4's proposed alternative never changes the tracked state.
- Twelve explicit links connect inherited institutional statements to actors, decision objects, responses, or events while retaining the original evidential standing.
- Narrow scope does not ensure acceptance; integration does not require agreement on every underlying preference. The selected cases support a process explanation, not an estimate of each factor's causal effect.

## Files and identifiers

| Path | Content |
|---|---|
| `report/` | Six-page comparison report |
| `analysis/comparison_protocol.json` | Dimensions, scope, temporal rules, and inference discipline |
| `analysis/case_comparison.json` | Six comparisons with preferences, claims, controls, responses, outcomes, and limits |
| `analysis/disposition_sources.json` | Refreshed platform records F32359–F33473, including exact author and disposition actor |
| `analysis/disposition_events.json` | Six focal disposition events plus supporting C6B backport |
| `analysis/policy_patch_sources.json` | Four relevant patches from the C3 changed-file retrieval |
| `analysis/state_replay.json` | Initial tracked fields, six focal transitions, final state, and separate backport |
| `analysis/institution_action_links.json` | IL01–IL12, with unit references, related evidence, warrant, and inference boundary |
| `analysis/comparison_tests.json` | Six competing explanations and their standing against the cases |
| `analysis/claim_ledger.json` | Six synthesis claims with sources and limits |
| `analysis/inherited_units_used.json` | 46 unchanged selected IG2 or contextual units |
| `analysis/evidence_anchors_inherited.json` | 77 unchanged exact anchors from Rounds 9 and 10 |
| `analysis/github_sources_used.json` | 76 unchanged inherited source records needed by the comparison |
| `analysis/podcast_passages_used.json` | Unchanged selected passages linked through the six retained podcast statement units |
| `analysis/web_cards_inherited.json` | Four unchanged Round 10 source cards |
| `analysis/proposal_commits_inherited.json` | Identified June and September commits, KJ and KS |
| `analysis/provenance.json` | Input identity, counts, source additions, and review standing |
| `analysis/verification_results.json` | Mechanical checks and report hash |
| `analysis/document_quality_check.json` | Visual inspection record for the supplied DOCX |
| `sources/` | Eleven retrieved GitHub responses: seven pull requests, three closure-actor lookups, and one changed-file list |
| `input/` | Unmodified Round 10 evidence archive, with its nested frozen inputs |
| `build_analysis.py` | Rebuild the comparison, evidence projections, and recorded state transitions |
| `build_report.py` | Regenerate the DOCX with `python-docx` |
| `verify_model.py` | Check lineage, spans, dates, actors, state changes, and references |
| `manifest.json` | SHA-256 and byte size for every other package member |

F identifiers name the new platform metadata projections. F32406_files names the selected changed-file evidence. E, N9, R10E, PE, U, PU, D, X, KJ, KS, and W identifiers retain their inherited meanings. Case numbers are stable labels: C2 closes before C1, and C3 opens while C1 remains active. C6B is a supporting event, not a seventh focal case.

## Scope and interpretation

The six episodes belong to one dispute and are not independent statistical observations. The comparison distinguishes documented responsibility, local recognition, normative assertion, recorded action, and analyst interpretation. Its four dimensions form an analytical projection, not new mutually exclusive IG2 classes.

The state replay uses the old lines in C3's patch for its starting fields and applies only confirmed merged changes to those fields. It does not reconstruct the whole repository history. C5 and C6 preserve the higher default and options; C4 leaves the prior state unchanged. The supporting 30.x integration remains distinct from publication, installation, adoption, or network agreement. An unmerged pull request's prospective merge-hash field never counts as an actual merge.

The June 9 contribution guide supplies a dated documentary basis for C3 and later comparison. It does not independently date its precise wording to April. The moderation guide uses the pinned August 14, 2024 revision. Edited proposal bodies retain their temporal limits; dated quotations and identified commits support narrower claims. The new metadata lookups match the frozen creation, closure, and merge times and head revisions; current body wording is not substituted into the analysis.

No inherited grammar unit or standing changes. The active podcast corpus remains seven recordings and 27 passages: six statement units with `text_only` standing and 21 context units. PU01 remains context. PU03 contains only “Their job is uh to facilitate releases.” P5158, PE25–PE27, and PU08–PU10 remain excluded from active analysis. Historical copies inside frozen archives do not restore them to the corpus. The garbled Murch wording remains outside scope; no recovery task, new transcript, or 2026 fork outcome enters this round.

The matched moderation events do not establish the particular ban reported in Mechanic's interview. The June GitHub exchange does not resolve Guida's reported Twitter exchange. The original working paper remains unchanged. Mechanical checks and internal interpretation do not constitute independent source or coding validation.

## Reproduction

Extract the archive and run from its root with Python 3.9 or later:

```bash
python3 build_analysis.py
python3 verify_model.py
```

These scripts use the standard library and the supplied records. They extract prior frozen archives into `baseline/` as needed. Verification checks the delivered DOCX using its XML and does not require Word. Rebuilding the analysis should reproduce the supplied JSON files exactly.

Optional report regeneration requires `python-docx`:

```bash
python3 build_report.py
python3 verify_model.py
```

Render and inspect every page after regenerating or editing the report. The delivered visual-review record and manifest apply to the supplied bytes. A regenerated DOCX can differ in metadata or pagination and requires a new hash, review record, and manifest.

The archive omits extracted duplicate baselines, render intermediates, and upload utilities. The frozen input retains the full prior evidence trail. New live retrieval should be recorded as a new version rather than silently substituted for these records.
