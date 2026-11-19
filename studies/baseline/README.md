# Bitcoin Core IG 2 expansion round

Twelve new, purposively chosen PR episodes extend the substantive pilot using the unchanged project codebook version 0.3. The main deliverable is the results document in `documents/`.

## What was done

One continuing assistant read the complete available frozen discussions and relevant dated supplements, produced 48 focal claims and overreach checks, and prepared 16 IG-informed focal projections. Four same-input narrative comparisons assess information preservation. Twelve controlled script executions test a technical signer-list gate using simulated GPG status output and actual before/merged key lists.

This is a source-grounded modeling round, not an independent, blinded model evaluation. The source-layer matrix is retrospective evidence accounting. The focal schema is deliberately smaller than a complete version 0.3 annotation; do not treat the number of retained propositions as extraction coverage, accuracy, or a population denominator. No statistical inference or IG superiority estimate is made.

## Package contents

- `protocol/`: frozen round plan, unchanged codebook and original schema, selection and corpus receipts. The old schema is a reference, not the schema of this round's compact focal records.
- `sources/records/`: the 12 selected records from the original canonical corpus.
- `sources/packets/`: complete frozen discussion entries plus separately labeled supplements.
- `sources/supplements/`: connector responses for dated primary repository files and commits.
- `sources/catalog.json`: entry identities, layers, URLs and hashes.
- `analysis/claim_ledger.json` and `claim_index.csv`: claims, exact evidence, assessments and limitations.
- `analysis/focal_ig_records.json`: component projections, force, institutional standing and inference limits.
- `analysis/case_mechanisms.json`: linked explanations with alternatives and bounded governance levels.
- `analysis/evidence_matrix.json`, `narrative_comparison.json`, `case_links.json`: comparative diagnostics.
- `analysis/key_gate_experiment.json`: all 12 controlled technical checks.
- `analysis/review_log.json`, `source_integrity.json`, `validation.json`: corrections and checks.
- `tools/`: deterministic builders and checker. These materialize the analyst's judgments; they do not call or evaluate a model.

## Reproduce

Python 3.10 or later and a POSIX shell are sufficient for the analysis builders. Run from any working directory:

```bash
python tools/assemble_sources.py
python tools/build_analysis.py
python tools/build_focal_ig.py
python tools/build_diagnostics.py
python tools/key_gate_experiment.py
python tools/validate_analysis.py
```

Optionally pass the original `prs_canonical.jsonl` path to `validate_analysis.py` to recheck the twelve exact selected corpus lines. The 274 MB corpus is not duplicated in this package. Its SHA256 and selected line offsets are in `protocol/`. The document builder requires python-docx; rendering additionally requires the document renderer and LibreOffice. Page images are internal quality checks and are not included.

Offsets are zero-based Python Unicode code points, end exclusive, within each decoded source entry. Original line endings remain significant. Creation timestamps must not be interpreted as edit timestamps. The linked IRC source is represented by a short excerpt and labeled summary, not a complete locally archived transcript. It was retrieved adaptively after selection and is not a new independent case.

## Interpretation and rights

The codebook separates grammar, utterance force, institutional standing, recognition and consequences. A merged contribution is not evidence that every suggestion was adopted. A signer list is not a GitHub permission ledger or a measure of authority over Bitcoin adoption. Unmerged documents can coexist with recognized roles. No comparative claim about environmental governance difficulty has been tested.

Repository source files retain their original notices. Contributor communications are research evidence, and this package makes no blanket redistribution or publication-rights claim. Review the selected excerpts and any identifiers before public release. The computational checks use synthetic GPG status output; they do not perform cryptographic verification or exercise live repository permissions.
