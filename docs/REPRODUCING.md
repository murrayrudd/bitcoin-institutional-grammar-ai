# Reproducing the retained analysis

Use Python 3.12.14 and `jsonschema==4.26.0`, the versions used for package verification. From the repository root:

```bash
python -m pip install -r requirements.txt
python scripts/verify_package.py
python scripts/reproduce.py
```

On Windows, `py -3.12` can replace `python`. The baseline's synthetic key-gate experiment uses a POSIX shell; run the complete reproduction command in Linux, macOS, or Windows Subsystem for Linux. Installation needs internet access; the checks and analysis use included files only. No model-provider account is needed.

`verify_package.py` checks the inventory, SHA-256 hashes, and identities of the retained original research files. `.gitattributes` disables line-ending conversion because exact source text and byte identities matter.

`reproduce.py` runs in a temporary copy and leaves the distributed evidence unchanged. It:

1. Runs the specification's regression and release-compatibility checks.
2. Rebuilds the 12-case baseline, 48-claim ledger, grammatical projections, and synthetic key-gate checks.
3. Verifies the 18 frozen coding runs and recalculates field agreement, supplementary nominal alpha, and the 24/42 versus 21/42 common-proposition comparison.
4. Replays the collaborative review's changes into nine adjusted 0.4 views and two separately labeled historical 0.3 copies.
5. Checks the earlier source review and overlapping coding comparison.
6. Rebuilds and checks the six-proposal comparison, selected state changes, and follow-up claim ledger.

Regenerated research outputs are compared with the saved files. Two historical builders use unordered iteration: a diagnostic list of changed unit identifiers, and the final metadata-only change-log entries. Those are compared by content; the latter's traversal-dependent sequence IDs are excluded from comparison. Coding changes retain their sequence, and the distributed change IDs remain unchanged. Recorded preparation timestamps and report-layout checks are not computational findings and are not required to match a new run.

The verification record for this distribution is [VERIFICATION.json](VERIFICATION.json). To save a new record, use an output path outside the repository:

```bash
python scripts/reproduce.py --record ../ig2-verification.json
```

## Source corpus and AI runs

The repository includes the selected canonical records and frozen source packets. The full 25,508-record parent corpus is identified by SHA-256 `b289aa40737d619dea8a673290fae636dbe1a65ccf49331223ab548acb23f7c9` and is not duplicated. Full reconstruction of the population-wide selection requires those exact original `prs_canonical.jsonl` bytes:

```bash
python studies/independent-coding/tools/verify_selection.py /path/to/prs_canonical.jsonl
python studies/baseline/tools/validate_analysis.py /path/to/prs_canonical.jsonl
```

Run those original commands in a copy because they write verification records. The distributed selection records retain the original successful corpus checks.

The scripts recalculate recorded results and apply retained review decisions. They do not rerun the AI coding or establish that another model will reproduce the interpretations. Model instructions, supplied inputs, independent outputs, repair records, and review decisions are available for designing a new evaluation. Original provider snapshot identifiers and sampling telemetry were not exposed in the retained execution records.

## Historical scripts and reports

Study folders preserve their original READMEs, dated status records, and stage reports. Their paths and version references describe those stages. The root commands above are the supported entry points for this distribution. One-time selection, dispatch, masking, freeze, and report-building scripts are historical provenance; do not run them over frozen records. Rebuilding historical DOCX reports additionally requires `python-docx==1.2.0` and, for some authoring scripts, the original authoring environment.

The Core–Knots comparison and follow-up builders have documented path adaptations. No coding judgment or analytical rule was changed for this distribution. See [PROVENANCE.md](PROVENANCE.md).
