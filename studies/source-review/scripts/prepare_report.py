from pathlib import Path
import json
P=Path(__file__).resolve().parents[1]
r={e['source_id']:e for e in json.loads((P/'sources/baseline_all_source_registry.json').read_text())}
sources=[]
def source(n,title,*ids):
 v=[f'R{n}',title,[[r[s]['url'],s] for s in ids]];sources.append(v);return v
source(1,'glozow (April 29, 2025) and maflcko (May 14, 2025): review purpose and merit','32359-115','32406-169')
source(2,'aryaethn (May 10, 2025): unspecified majority claim','32359-227')
source(3,'Bitcoin Core moderation guidelines, historical revision of August 14, 2024','D_MOD')
source(4,'willcl-ark (June 7, 2025): topic instruction, warning, and appeal venue','32406-252')
source(5,'PR 32714 (June 10, 2025): achow101’s wording proposal, warning principle, and review response','32714-body','32714-007')
source(6,'bitschmidty (September 22, 2025): undeprecation proposal and reuse of the warning argument','33453-body')
source(7,'maluquices and pinheadmz (June 4, 2025): open-source legitimacy and reply','32406-228','32406-229')
source(8,'Sjors and petertodd (April 28, 2025): suggested code comment and reported completion','32359-038','32359-053')
source(9,'instagibbs and bitschmidty (September 22–24, 2025): maintainer discretion over timing','33453-018','33453-069')
source(10,'ajtowns and polespinasa (May 15, 2025): deprecation meaning and recognition','32406-178','32406-180')
source(11,'hebasto (August 24 and September 1, 2025): translation freeze and later route','33224-010','33224-021')
source(12,'Bitcoin Core contribution guide at the June 9, 2025 merge revision','D_CONTRIB')

def table(headers,rows,widths):return ['table',{'headers':headers,'rows':rows,'widths':widths}]
pages=[
{'title':'Bitcoin Core institutional coding','blocks':[
 ['subtitle','Round 4: source review and reconciliation'],
 ['meta','Governance research projects  |  November 6, 2026  |  Review version 01'],
 ['p','The reviewed sources support carrying the larger governance study forward. The strongest explanation remains that open participation operates through distinct arrangements for review, moderation, integration, and release timing. The review sharpens the evidence for those arrangements and removes one unsupported inference about majority decision authority.'],
 ['p','Three separate AI reviewer contexts examined 24 fixed records across six pull requests. Each received the original sources and frozen coding rules, without Round 3 annotations or conclusions. The resulting comparison supports four substantive corrections to the institutional interpretation.'],
 table(['Issue','Reconciled interpretation'],[
 ['Majority decision authority','The statement that a majority decides the winner does not identify a decision, constituency, or counting procedure. Retain the attributed claim; do not infer a voting rule. [R2]'],
 ['Moderation','The topic and appeal-venue instructions apply supplied written policy. The temporary ban remains an announced consequence. [R3] [R4]'],
 ['Reuse of a warning principle','The September proposer quotes and applies the June principle as a reason for removing deprecation. This supports local recognition beyond textual recurrence. [R5] [R6]'],
 ['Open-source legitimacy','A directly addressed reply challenges the application of the transparency argument. It does not establish rejection of transparency as a value. [R7]']
 ],[1.48,5.52]),
 ['p','The review also adds 16 candidate passages and preserves several reasonable alternative parses. No author decision is needed to apply the corrections. The result is a source-reviewed modeling stage, with separate AI review and explicit reconciliation; independent human validation remains a later publication step.'],
 ['caption','Scope: a bounded review of the existing GitHub corpus. The working paper, book chapter, podcast collection, and broader literature were not revised in this round.']
]},
{'title':'What the reviewed sequences establish','blocks':[
 ['h','Participation and decision authority are distinguishable'],
 ['p','The review-purpose statement rejects a per-user voting-forum interpretation and emphasizes the merit of arguments. A later explanation of the review-summary bot prioritizes technical content over category totals. Together, these sources support local recognition of a merit criterion. They do not supply numeric weights, prove consistent application, or determine what another participant meant by a majority deciding the winner. [R1] [R2]'],
 ['h','Technical uptake and integration are separate outcomes'],
 ['p','A proposed code comment receives the reply “Added comment.” Original GitHub metadata links that reply directly to the suggestion. The containing pull request nevertheless closed without merging. The sequence supports reported implementation of a local suggestion while preserving the distinct repository outcome. It does not independently verify the resulting code. [R8]'],
 ['h','Moderation structures the discussion'],
 ['p','The named intervention directs comments toward the proposed changes, announces a temporary ban for future off-topic contributions, and sends debate about the intervention to the meta repository. The dated moderation guide supplies the corresponding topic and venue provisions. This is evidence that written institutional arrangements shape participation within Core, alongside informal conventions. The supplied record establishes the warning, not an executed ban. [R3] [R4]'],
 ['h','Reasons can persist across unsuccessful proposals'],
 ['p','The June proposal argues against removal warnings where no current removal plan exists. The September proposal explicitly attributes that argument, describes continuing uncertainty for users, and invokes clarity as a reason to remove deprecation. The institutional claim therefore has local recognition in a later proposal, even though the earlier proposal did not merge. This is a traceable path of justification; it does not identify a single cause of the later outcome. [R5] [R6]'],
 ['h','Timing authority remains differentiated'],
 ['p','The maintainer-call statement and the proposer’s later deference preserve a division between expressing a preference and deciding release timing. That interpretation survives the fresh reading. Its scope is the stated timing decision, with no inference that repository maintainers determine network adoption. [R9]'],
 ['caption','The source registry and adjudication ledger preserve exact passages, source identifiers, and the distinction between reported actions, recorded dispositions, and inferred institutional significance.']
]},
{'title':'Corrections without forced agreement','blocks':[
 ['p','The reconciliation evaluates both rounds against the source. A different label can represent the same proposition; matching labels can preserve the same mistake. The following decisions retain useful alternatives while correcting evidence claims that affect the larger explanation.'],
 table(['Passage or issue','Decision and consequence'],[
 ['Majority claim (N14; U02 relation)','Set the majority target to unknown and remove the inferred challenge to merit weighting. Repetition of an argument and an unspecified majority are not necessarily competing decision rules.'],
 ['Moderation (U17–U19)','Use documented standing for topic and venue provisions. Separate the negative venue duty and the announced consequence as the frozen codebook requires. Keep the intervention case specific.'],
 ['Warning expectation (U25)','Use locally supported standing with inferred recognition grounded in the later argument, while retaining uncertainty about generalization beyond these options.'],
 ['Legitimacy claim (N16)','Record the reply’s challenge to application. Retain the epistemic interpretation as one possible framing alongside ordinary accountability and other level interpretations.'],
 ['Deprecation meaning (N04)','Retain local recognition of the embedded status definition. The fresh reading focuses on advice about interpreting the term; that difference does not compel a downgrade. [R10]'],
 ['Translation freeze (U32)','Retain the exact prohibition as expressed. A proposed workaround may implement its purpose or qualify its application; merging alone does not resolve that distinction. [R11]']
 ],[1.82,5.18]),
 ['p','The fresh reviews also omit two status-defining propositions already retained in Round 3: the equivalence between discouragement and deprecation, and the meaning of deprecation as non-recommendation. A fresh moderation parse also generalizes a warning addressed to a named participant. Those readings are not accepted as replacements for the baseline.'],
 ['p','The interpretation of higher governance levels remains a substantive modeling question. The transparency passage can be read as an argument about the foundations of legitimate authority or as an expectation governing ordinary decisions. The paper can examine that argument directly without counting it as proof that an epistemic institution operated in the episode. [R7]'],
 ['caption','Ledger R4-01 through R4-20 distinguishes substantive errors, representation deviations, epistemic coding errors, equivalent meanings, context gaps, and defensible alternatives. The codebook itself remains unchanged.']
]},
{'title':'Extraction coverage and the corrected record','blocks':[
 ['p','Round 3 screened the corpus broadly but fully annotated only selected statements. The fresh reviewers were asked to extract all plausible statements in each focal record. Consequently, 67 fresh focal statement records versus 17 prior full annotations is a difference in task coverage and representation, not 50 demonstrated omissions.'],
 table(['Measure','Result','Interpretation'],[
 ['Fixed focal records','24','12 important cases; 6 retained-candidate samples; 6 exclusions.'],
 ['Prior full statement annotations in the sample','17 in 10 records','The other focal records were screened without full statement coding.'],
 ['Fresh focal statement records','67','Includes alternative segmentation, embedded propositions, and quoted content.'],
 ['Candidate additions','16','5 navigation instructions; 10 additional proposals or procedural claims; 1 defensible rhetorical inclusion.'],
 ['Corrected candidate inventory','500 passages','484 inherited passages plus the 16 additions. These are not counts of institutions.'],
 ['Corrected selective annotation set','64 statements','62 prior statements, one context record converted to a consequence statement, and one separated negative duty.']
 ],[2.33,.93,3.74]),
 ['h','The clearest omissions are narrow'],
 ['p','Five navigation instructions were absent from the candidate inventory, although the frozen codebook requires distinct referrals to be retained. The additional passages also include an explicit technical proposal, moderation classifications and permission, editorial preferences, an objection to extra configuration arguments, advisory reasoning, and a qualified user-protection principle. Indirect and descriptive readings remain marked as alternatives.'],
 ['h','Repeated quotations need corpus context'],
 ['p','Quoted passages in two focal records contain statements whose originals already occur elsewhere in the corpus. Their originals were missing from that reviewer’s packet. The full source registry resolves those occurrences without counting them as new institutional claims. The final sample inventory retains 21 candidate-bearing records and three context records.'],
 ['p','The corrected annotation set is a bounded update, not an automatic union of all fresh parses. Nine existing records change and one negative-duty record is added. Forty-five inherited statements lie outside the focal sample and have not received this separate review. The evidence package preserves the original versions and every accepted correction.']
]},
{'title':'Appendix A. Review design and evidentiary limits','blocks':[
 ['h','Frozen selection and separate reviewer contexts'],
 ['p','The sample was fixed before dispatch. Twelve records were selected for their importance to the existing explanation. For each of six pull requests, one additional candidate-bearing record without a full prior statement annotation and one excluded record were selected by a recorded SHA-256 ranking. Eligible sampled records contained 30–2,400 Unicode characters. The seed, full eligible pools, selection results, codebook, schema, prompts, and input hashes are preserved.'],
 ['p','Each fresh context received eight focal records, supporting source text, six proposal bodies and disposition metadata, selected patch context, and four dated procedural documents. No parent conversation, prior labels, response-chain conclusions, or manuscript narrative was supplied. Context selection was informed by prior work. Reviewers were instructed to use only their own directories; the shared filesystem did not provide a technical access barrier. Their reported access records are retained.'],
 ['h','Context supplements remain visible'],
 ['p','Reviewer B requested original reply metadata before finalizing the reported implementation finding. Reviewer C’s first output was frozen before a uniform audit identified one missing source cited by the baseline focal annotations. C then received that original source, without baseline interpretations, and supplied a separately preserved revision. It changed the standing of the merit criterion to locally supported; it did not resolve the majority claim. Quoted originals located during reconciliation are separately documented as packet-context limitations.'],
 ['h','What the review can establish'],
 ['p','One source-first run was conducted per disjoint subset, with recorded mechanical and self-review repairs before freezing. The three contexts inherited the same parent configuration. Provider snapshot, generation seed, temperature, token use, and cost were not exposed. The evidence supports a documented AI review process and source-based correction, not model independence, repeat-run reliability, a population accuracy estimate, or independent human validation.'],
 ['p','All frozen reviewer annotations, the supplemented annotation, and the corrected selective set pass the supplied structural and exact-span checker. These checks verify representation and source anchoring, not interpretive truth. The package preserves initial attempts, repairs, alternatives, and the final adjudication.'],
 ['h','Implication for the larger paper'],
 ['p','The evidence now supports a stronger methodological demonstration: statement extraction, institutional standing, response, and disposition can be kept distinct in a contested development episode. Core’s internal processes include documented and role-specific arrangements. Broader claims about Bitcoin’s decentralization, network adoption, or causal political influence require evidence beyond this bounded GitHub review. No immediate author adjudication is necessary; a later human review can use the frozen packet and compare independently recorded judgments.']
]},
{'title':'Appendix B. Primary sources and evidence files','blocks':[
 ['p','References below link to the supplied primary records. The analysis uses the frozen source text and historical document revisions, rather than assuming that current repository pages reproduce every earlier edit. Exact offsets and full supporting passages are in the evidence package.'],
 *[['source',s] for s in sources],
 ['h','Evidence package guide'],
 ['caption','analysis/adjudication_ledger.json and .csv: all 20 grouped findings, affected units, decisions, and source evidence.'],
 ['caption','analysis/reconciled_sample_decisions.json and .csv: disposition of every focal record. candidate_additions.json and candidate_inventory_corrected.json: the 16 additions and complete updated inventory.'],
 ['caption','annotations/corrected_baseline.json: bounded correction of the selective annotation set. analysis/correction_log.json identifies every changed field.'],
 ['caption','protocol, reviewer_inputs, reviewer_outputs: frozen selection, instructions, source packets, original outputs, supplements, checks, and repair histories. tools/verify_review.py checks hashes, scope, spans, and annotation structure.'],
 ['caption','The original Round 3 source and annotation files remain under sources/. Structural review flags and their treatment are recorded separately from semantic adjudication.']
]}
]
(P/'report/report_content.json').write_text(json.dumps({'pages':pages,'sources':sources},ensure_ascii=False,indent=2)+'\n')
print('Report content prepared:',len(pages),'pages')
