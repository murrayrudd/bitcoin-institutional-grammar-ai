CORE / KNOTS — ROUND 12 OVERLAPPING AI VALIDATION
7 November 2026 | Evidence package version 0.1

Purpose
This package records three fresh AI contexts applying the same frozen project
specification to the same 24 source records, with identical supplied context.
It adds overlapping repeatability evidence to the earlier disjoint source review.
It does not supply a human reference standard, measure population accuracy,
compare distinct model families, or validate the complete institutional model.

Study scope
The sample covers six linked 2025 Bitcoin Core contribution episodes. It reuses
the complete Round 4 sample: 12 purposive records, six deterministically sampled
candidate records, and six deterministically sampled excluded records. It is
known research material, not a novel holdout. The shared packet contains 98
entries, including context, dated documents, and metadata. Context records are
not additional independent test observations. The older paired-version test
described at the end of the codebook is historical; protocol/overlap_protocol.json
defines this study.

Contents
common_input/  Identical source packet, project specification 0.3, schema,
               and supplied mechanical checker.
protocol/      Frozen study protocol, sample provenance, reviewer instructions,
               dispatch details, hashes, and output freeze.
reviewers/     Three separate input copies, first complete annotations, final
               annotations, checker results, repair records, and review notes.
analysis/      Exact and semantic comparisons, source reconciliation, and
               implications for the inherited analysis.
prior_inputs/  Earlier corrected baseline and provenance used only after the
               three new annotations were frozen.
tools/         Reproducible comparison and verification scripts.
report/        Readable report and its preparation materials.

Independence and execution
The three coders received no parent conversation, prior annotation, prior
interpretation, or other coder's output. They used the same inherited model
configuration with no model override. Provider snapshot, sampling parameters,
token usage, and costs were not exposed. The filesystem was shared; access was
restricted by instructions, not a technical sandbox. Access logs are coder
self-reports. No claim of statistical independence or training-data novelty is
made. First complete outputs and subsequent changes are retained.

Reading agreement
Screening is measured over the 24 focal records. Statement counts depend on
segmentation. Exact span matches are reported separately from source-reviewed
semantic matches. Field agreement uses one-to-one, three-coder statement groups;
its denominator excludes split/combined, unmatched, and unresolved groups.
Alignment is a revisable analytical judgment, not an automatic truth criterion.
Source review examines unanimous interpretations as well as disagreements.
Structural and exact-quote checks establish record integrity, not semantic truth.

Reproduction
With Python 3 and jsonschema available, run from the package directory:
    python tools/compare_annotations.py
The frozen supplied checker can be run separately, for example:
    python common_input/tools/check_annotation.py common_input/packet.json reviewers/A/annotation.json
The one-time freeze tool intentionally refuses to overwrite the output freeze.
Source reconciliation and semantic alignment require judgment; their inputs,
decisions, and evidence are retained for inspection rather than represented as
mechanically reproducible ground truth.

Provenance and use
Source texts retain the original supplied content and identifiers. Source URLs,
document provenance, and collection details are in the packet and prior archives.
Repository integration is not Bitcoin network adoption. Announced enforcement
is not proof of executed sanctions. Reported implementation is not independently
verified implementation. Public-source inclusion makes no blanket claim about
redistribution rights over contributor communications.

The manuscript, prior annotations, and later fork history remain outside this
round's modification scope. Any proposed corrections belong to a separate ledger.
