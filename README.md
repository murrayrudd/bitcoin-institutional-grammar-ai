# AI-assisted institutional analysis of a decentralized protocol

Research materials for **AI-assisted institutional analysis of a decentralized protocol: applying Institutional Grammar 2.0 to Bitcoin Core**, by Murray A. Rudd.

**[Read the working paper on SSRN](https://doi.org/10.2139/ssrn.7710701)** · Repository package **1.0.0** · Coding specification **0.4.1**

The study assesses how AI agents can identify and interpret institutional statements in dispersed software-development records. It applies Institutional Grammar 2.0 and the Institutional Analysis and Development framework to Bitcoin Core, distinguishing documented rules, locally recognized expectations, participants' claims, and observed actions.

## Study and findings

- **12 routine development episodes** support 48 focal institutional claims, with linked source passages and grammatical projections.
- **Six linked Core–Knots proposals** show how control over proposal form, integration, moderation, and release decisions differs within the same controversy.
- **18 independent AI coding runs** compare project specifications 0.3 and 0.4. The more detailed specification did not improve overall agreement: all three coders agreed on all six compared fields for 24 of 42 common propositions under 0.3 and 21 under 0.4.
- **Collaborative AI review** corrected errors, narrowed disagreements, and retained defensible alternatives. Its adjusted annotations remain separate from the original independent results.

The method makes institutional evidence and consequential interpretations available for inspection. Human judgment remains necessary to assess competing purposes, authority claims, and values.

## Find the materials

| Material | Location |
| --- | --- |
| Current codebook, instructions, schema, and checker | [Specification](specification/protocol/) · [Tools](specification/tools/) |
| All 48 focal claims and their evidence | [Claim ledger](studies/baseline/analysis/claim_ledger.json) · [CSV index](studies/baseline/analysis/claim_index.csv) |
| Twelve-case baseline and source packets | [Baseline](studies/baseline/) |
| Six-proposal comparison and recorded state changes | [Core–Knots comparison](studies/core-knots/analysis/) |
| Source review and earlier overlapping coding | [Source review](studies/source-review/) · [Overlap study](studies/overlap/) |
| Frozen instructions, 18 independent runs, and agreement results | [Independent coding](studies/independent-coding/) |
| Review discussions, decisions, and adjusted annotations | [Collaborative review](studies/collaborative-review/) · [Reconciled dataset](studies/collaborative-review/dataset/reconciled_dataset.json) |
| Linked consensus proposals and later project records | [Follow-up evidence](studies/followup/) |
| Data organization, source attribution, and version history | [Data guide](docs/DATA_GUIDE.md) · [Provenance](docs/PROVENANCE.md) |

Files are included directly in the repository. Use **Code → Download ZIP** or clone [this repository](https://github.com/murrayrudd/bitcoin-institutional-grammar-ai).

## Verify and reproduce

Use Python 3.12 and install the checking dependency:

```bash
python -m pip install -r requirements.txt
python scripts/verify_package.py
python scripts/reproduce.py
```

The reproduction command works in a temporary copy. It checks frozen records, recalculates agreement, rebuilds the adjusted annotation views and six-proposal comparison, and compares the results with the distributed files. It does not call an AI service. See [reproduction instructions](docs/REPRODUCING.md) for the scope and original corpus requirements.

## Research basis

**Rudd, M. A. (2026).** *AI-assisted institutional analysis of a decentralized protocol: applying Institutional Grammar 2.0 to Bitcoin Core*. SSRN working paper. **https://doi.org/10.2139/ssrn.7710701**

The paper applies Institutional Grammar 2.0 within the IAD framework. The numbered project specifications are coding instructions developed for this study, not new versions of Institutional Grammar itself. The published working paper is available through the DOI; this repository supplies its research materials. Included stage reports document the analysis as it developed.

## Citation

Please cite the paper and identify **repository package 1.0.0**, the applicable coding specification, and the repository commit used:

```bibtex
@unpublished{Rudd2026InstitutionalGrammarBitcoin,
  author = {Rudd, Murray A.},
  title = {AI-assisted institutional analysis of a decentralized protocol: applying Institutional Grammar 2.0 to Bitcoin Core},
  year = {2026},
  note = {SSRN working paper},
  doi = {10.2139/ssrn.7710701},
  url = {https://doi.org/10.2139/ssrn.7710701}
}
```

[CITATION.cff](CITATION.cff) provides the preferred paper citation through GitHub's **Cite this repository** option. The DOI identifies the paper; this repository package has no separate DOI.

## License

Original project code and associated software documentation are available under the [MIT License](LICENSE.md). See [license scope](LICENSE_SCOPE.md) for the distinction between software, scholarly material, and attributed source evidence. Third-party works retain their source terms.

## Author

**Murray A. Rudd, Ph.D.**  
Futures Insight Research

- ORCID: [0000-0001-9533-5070](https://orcid.org/0000-0001-9533-5070)
- SSRN: [Author profile](https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=5958022)
- Google Scholar: [Profile](https://scholar.google.co.uk/citations?hl=en&user=84qbofEAAAAJ)
