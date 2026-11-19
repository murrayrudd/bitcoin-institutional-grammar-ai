from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def p(text,style='Normal'):return dict(text=text,style=style)
def h(text):return p(text,'Heading 1')
def h2(text):return p(text,'Heading 2')
def t(headers,rows,widths):return {'table':dict(headers=headers,rows=rows,widths=widths)}
pages=[]
pages.append([
h('Main result'),
p('The expansion supports a methodological paper on reconstructing institutional arrangements from fragmented public records. Twelve new Bitcoin Core episodes show how documented guidance, participant interpretations and observable technical changes can be linked while preserving differences between proposed wording, recognized expectations and applied procedures.'),
p('The clearest new finding is an explicit attribution of PR closure to contribution requirements. Review episodes also reveal how a hash connects approval to a particular revision, and why final comment snapshots cannot always reconstruct the intervening sequence. Maintainer episodes connect social endorsement with changes to a verification list while leaving broader permissions unobserved.'),
t(['Completed analysis','Scope'],[
['12 new episodes','2015 to 2026; 206 frozen discussion entries'],
['48 focal claims','Supported assertions, attributed explanations and deliberate overreach checks'],
['16 IG projections','Components, force, standing, scope and inference limits'],
['4 narrative comparisons','Same evidence and same analyst; no superiority estimate'],
['12 technical checks','Controlled trusted-key gate tests with simulated GPG output']],[1.65,5.29]),
h2('Meaning for the project'),
p('The case demonstrates an institutionally mixed setting: written guidance, discretionary judgments, tacit understandings made visible in discussion, and technical procedures coexist. It does not establish that Bitcoin Core is wholly decentralized or lacks hierarchy. The relevant methodological challenge is recovering institutional claims and their evidentiary limits across these different records.'),
p('Paper preparation can begin from these results. The project codebook remains at version 0.3. This round is a continuing analyst reconstruction and technical diagnostic, not a new independent coding evaluation. Claims about accuracy, reliability, scalability or advantages over narrative analysis remain outside its results.')])

selection=json.loads((ROOT/'protocol/selection.json').read_text())['cases']
labels=['Duplicate PR guidance','Discretionary closure guidance','Rebasing proposal','Explicit closure explanation','Hash reminder and response','Stale review attribution','Mutable review snapshots','Contested ACK sufficiency','Subsystem roles and codification','Descriptive maintainer table','Role endorsement and key addition','Key removal and verification']
pages.append([
h('Study design and episode selection'),
p('The round uses purposive comparison across guidance, review recognition and role authority. The plan and version 0.3 codebook were fixed before final selection. Screening exposed source content, so this is not a held-out or representative sample. Previously studied focal PRs and bridge PR 15626 were excluded. Eight selected PRs merged and four closed without merging.'),
t(['Case','PR','Year','Outcome','Focal question'],[[s['episode_id'],str(s['number']),s['year'],'Merged' if s['recorded_merged'] else 'Unmerged',label] for s,label in zip(selection,labels)],[.50,.65,.55,.87,4.37]),
p('Complete available frozen discussions were read for every selected episode. Dated repository files, proposals, merge records and technical context were retrieved separately. One public meeting log was added adaptively for the appointment episode. Linked discussions remain part of the same process; twelve PRs do not constitute twelve independent institutional observations.'),
h2('Execution and analytical scope'),
p('One continuing assistant produced the analysis and reviewed its source links within the same session. There were no isolated repeat coders, blinded arms or independent adjudicators. The 48 claims are a deliberately selected ledger, not an exhaustive statement inventory. Sixteen focal grammar projections apply the codebook distinctions in a compact schema; they are not schema-complete version 0.3 annotations or IG Script exports.')])

pages.append([
h('Guidance and procedural application'),
h2('Adoption must be checked at the proposition level'),
p('PR 8771 adds guidance against several PRs for the same change and offers help with Git workflows. The same-change qualifier matters: a broad restriction on simultaneous unrelated contributions would be an incorrect reading. The assistance route is optional. Commit-pinned text provides the integrated wording that the short discussion alone cannot establish. [E01]'),
p('PR 11276 adds advice against newcomer refactoring and permission for maintainers to close trivial PRs or refactoring PRs without clear benefit. Permission is discretionary. A reviewer separately suggests closure when no one volunteers to review, but that sentence is absent from the supplied final guide. A merged thread therefore cannot be treated as adoption of every prescription within it. [E02]'),
p('PR 17940 proposes rebasing guidance in developer-notes.md. The proposal distinguishes conflicts from unnecessary rebasing and preserves within-branch fixups. Qualified support, unresolved nits and disagreement over whether to mention a bot coexist with nonintegration. Closure does not demonstrate unanimous rejection of the proposed arrangement. [E03]'),
h2('An attributable application of contribution requirements'),
p('PR 26399 supplies the strongest new procedural application. Standing guidance expects an author to answer review comments before merge, permits disagreement if explained, and allows closure when feedback remains outstanding and inactive. maflcko identifies alleged failures of preparation and response, then explicitly links closure to the guidelines. The author contests the technical criticism while agreeing to continue discussion in the issue. [E04]'),
t(['Element','Observed evidence in E04'],[
['Provision','Reply before merge; disagreement may be explained'],
['Alleged trigger','Multiple commits, ignored discussions and feedback, limited progress'],
['Actor and consequence','maflcko reports closing the PR; frozen record is unmerged'],
['Limit','Participant attribution does not adjudicate the allegations or isolate a sole cause']],[1.45,5.49]),
p('This supports a bounded enforcement claim because the provision, alleged trigger, consequence and linking explanation are present. A closed PR without that connection would not be equivalent evidence. Technical disagreement remains a concurrent explanation; neither punitive intent nor a counterfactual merge is established.')])

pages.append([
h('Review recognition and incomplete histories'),
p('The review cases distinguish a request, an acknowledgment, a review target and final recorded attribution. In PR 17685, a reminder to include the reviewed hash receives an explicit acknowledgment and a separate hash-specific ACK. This is stronger evidence of local uptake than an unexplained later merge. The guide already describes the convention, so the episode does not demonstrate discovery of an entirely unwritten norm. [E05]'),
p('PR 31904 shows why including a hash is not enough to establish approval of the final version. A bare ACK prompts an explanation of conceptual versus code approval; a later hash-specific review is ultimately classified as stale, and the merge message credits another top-commit reviewer. Stale attribution does not mean the earlier contribution lacked influence or that the reviewer was punished. [E06]'),
h2('A final snapshot cannot supply missing edit history'),
p('PR 36127 contains a quoted earlier bot table, a reminder about hash identification and final review credit. However, the saved review already contains the final hash despite a creation timestamp earlier than the reminder. That timestamp dates the review record, not necessarily its current wording. The final merge establishes recorded credit, while the intervening edit and refresh sequence remains unresolved. [E07]'),
t(['Evidence state','Supported inference','Inference withheld'],[
['Quoted earlier table','A participant reported a classification problem','Exact time and cause of the bot state'],
['Saved review text','The final stored text includes the hash','When the hash entered that text'],
['Merge message','Top-commit credit includes the reviewer','The reminder caused the change']],[1.35,2.65,2.94]),
h2('Sufficiency is scoped and contested'),
p('In PR 11743, a participant challenges review sufficiency after merge. The author replies with a threshold for relatively simple test PRs and explains why the feedback did not block integration. A later proposed follow-up receives acknowledgment. The record supports a contested, scoped rationale; it does not establish an uncontested project-wide minimum, nor verify that the follow-up was completed. [E08]'),
p('Together, these cases make scope, version identity, recognition and chronology central to reconstruction. Treating every ACK as the same event, or every displayed timestamp as a content revision time, would erase material institutional distinctions.')])

pages.append([
h('Role recognition and technical effects'),
p('The unmerged maintainer documents offer useful contrary cases. PR 7005 includes an asserted mining role and explicit recognition by another participant even though the document closes unmerged. PR 25839 debates a descriptive table of focus areas, with the author explicitly denying that the areas are enforced rules. Failed codification therefore does not establish an absence of roles, and a proposed table does not establish binding exclusive jurisdiction. [E09, E10]'),
p('PR 23798 combines explicit wallet-role endorsements, a replacement rationale and key identity checks. The merged tree adds the nominated key. Linked meeting evidence leaves an opportunity for objections and expresses an expectation of at least a week of PR exposure; the observed PR interval is 3.46 days. This discrepancy concerns an expressed expectation, not an established binding minimum. The actual GitHub permission grant and its timing remain unobserved. [E11, M1]'),
p('In PR 27054 the key holder proposes his own removal. Reviewers distinguish that intent from problems with historical signature verification. The merged tree omits the key, but this does not by itself reveal every privilege transition or establish involuntary expulsion. [E12]'),
h2('Controlled test of the verification gate'),
p('The original gpg.sh wrapper was executed with actual before and merged trusted-key files. A stub supplied a simulated valid-signature status for each test key. The test isolates the membership gate; it does not authenticate signatures or reproduce the full verify-commits traversal.'),
t(['Simulated signer','Before change','After merge'],[
['Added key in PR 23798','Rejected','Accepted'],
['Removed key in PR 27054','Accepted','Rejected'],
['Unchanged listed key in each context','Accepted','Accepted'],
['Unlisted control in each context','Rejected','Rejected']],[3.40,1.77,1.77]),
p('All 12 executions matched these expectations: four changed-key conditions and eight control conditions. Head and merged key-list contents matched in both episodes. The result establishes a narrow technical effect that can be linked to social recognition without equating signer acceptance, repository access, expertise and authority over Bitcoin adoption.')])

pages.append([
h('Evidence availability and representation'),
p('The comparison asks which sources permit each conclusion. It does not measure model improvement from adding sources: the same continuing analyst inspected the full evidence and then mapped dependencies retrospectively. The evidence package preserves the complete twelve-case matrix and exact anchors.'),
t(['Layer','Contents','Analytical contribution'],[
['D','Dated standing textual guidance','Identifies documented expectations and role descriptions'],
['T','D plus frozen discussion and outcome metadata','Exposes attributed applications, objections, recognition and local responses'],
['I','T plus dated proposals, commits, technical context and a linked meeting record','Checks exact integrated wording and technical effects; can reveal or retain unresolved gaps']],[.55,2.75,3.64]),
p('More evidence can narrow a claim rather than strengthen it. The final text excludes a reviewer suggestion in E02. The unmerged document in E10 remains a proposal. Additional merge evidence in E07 verifies final attribution but cannot recover missing edit history. These are limits on reconstruction, not extraction failures that should be repaired by plausible inference.'),
h2('Diagnostic comparison with narrative accounts'),
p('Four episodes were represented both as connected narratives and as structured fields using the same evidence. The narrative accounts were written to preserve the relevant limitations. No blinded comparison, scoring panel or accuracy difference was produced.'),
t(['Case','Information preserved by both forms'],[
['E04','Provision, alleged violation, attributed closure and competing explanation'],
['E07','Reported earlier state, final credit and missing edit chronology'],
['E08','Simple-test scope, alternative ACK thresholds and contested standing'],
['E11','Role endorsement, key registration and unobserved permission timing']],[.70,6.24]),
p('IG-informed structure makes actor, force, conditions, institutional standing and consequences explicit and comparable. This round demonstrates that audit function. It does not show that a careful narrative cannot preserve the same evidence or that an IG workflow improves accuracy. An independent comparison would be required for either stronger claim.')])

pages.append([
h('Implications for the methodological paper'),
p('The defensible contribution is a method for reconstructing institutional arrangements from public records while making the inferential steps inspectable. Bitcoin Core supplies cases where prescriptions, interpretations, social recognition and technical procedures are distributed across different sources. The analytical object is a bounded governance arena within the Bitcoin ecosystem.'),
h2('Claims supported by this round'),
p('The results show why grammatical coding needs separate records for institutional standing, local recognition, disposition and observed consequences. They also show why process reconstruction requires source-specific temporal information. The closure episode, mutable review records and opposite key-list changes provide concrete demonstrations of these requirements.'),
p('The strongest mechanism evidence remains operational: applying contribution expectations, coordinating review and maintaining role-related procedures. Proposals to revise recurring guidance support collective-choice analysis even when they are not adopted. Constitutive grammar and technical trust markers do not independently demonstrate constitutional or epistemic authority.'),
h2('Claims that remain outside the evidence'),
p('This round does not demonstrate that Bitcoin Core is wholly decentralized, that its governance is more difficult to study than environmental governance, or that all its relevant expectations are unwritten. The dated guides themselves describe roles and discretion. Comparative difficulty would require a common design across cases, not an assumption based on domain.'),
p('Nor does this analysis estimate full-corpus accuracy, institutional prevalence, extraction coverage or causal effects. Selection was informed by visible content and the episodes are linked. Public model training exposure is unknown, and the continuing analysis was not blind to earlier pilot findings.'),
h2('Starting point for the next writing session'),
p('Begin paper preparation with the case boundary, the reconstruction procedure and three demonstrations: attributed procedural application, review recognition under version change, and role recognition coupled to technical registration. Keep the previous validation evidence separate from this expansion. The literature assessment can then determine which parts of the method are established practice and which constitute a defensible contribution.'),
p('A future performance claim would need a separately frozen evaluation with source-restricted runs, independent review and a strong narrative comparison. A useful methods paper can instead make a narrower demonstration claim, provided its validation limits and evidentiary failures are presented as part of the results.')])

pages.append([
h('Sources and reproducibility'),
p('Each E identifier resolves to a complete frozen PR packet, a source catalog entry and exact claim anchors. Commit-pinned file URLs and Git object identifiers are retained in the package. The primary episode URLs below provide convenient navigation; live pages may differ from the frozen record.'),
* [p(f"{s['episode_id']}  {label}  https://github.com/bitcoin/bitcoin/pull/{s['number']}") for s,label in zip(selection,labels)],
p('M1  Bitcoin Core developer meeting of December 16 2021, especially 19:02 to 19:09 and the subsequent PR opening. https://www.erisian.com.au/bitcoin-core-dev/log-2021-12-16.html'),
h2('Verification completed'),
p('All 179 exact-span checks passed across the claim ledger and focal projections. All 30 retrieved repository-file contents reproduced their supplied Git blob hashes. The twelve selected corpus lines matched their recorded hashes and offsets; the frozen codebook hash was unchanged. All twelve controlled verification-gate executions passed.'),
p('These checks establish text identity and computational reproducibility, not semantic correctness. The source review log records scope corrections, source-target correction, timestamp interpretation and withheld authority claims. The unchanged 25,508-PR corpus is identified by its receipt and is not duplicated in the archive.'),
p('The package includes selected source records, supplements, protocols, claim and grammar records, mechanism maps, narrative diagnostics, experiment outputs and deterministic builders. Builder scripts materialize the analyst’s recorded judgments; they do not rerun a language model. The public meeting source has a limited excerpt and source summary rather than a complete local transcript.')])

out={'title':'Bitcoin Core institutional modeling results','subtitle':'Twelve episode expansion using project codebook version 0 3','date':'31 October 2026','pages':pages}
(ROOT/'analysis/report_content.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
