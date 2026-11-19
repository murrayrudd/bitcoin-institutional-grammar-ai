from pathlib import Path
import json
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH

R=Path(__file__).resolve().parent;O=R/'report';O.mkdir(parents=True,exist_ok=True)
D=Document();S=D.sections[0];S.page_width=Inches(8.5);S.page_height=Inches(11)
S.top_margin=Inches(.7);S.bottom_margin=Inches(.7);S.left_margin=Inches(.8);S.right_margin=Inches(.8)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2']:
 st=D.styles[name];st.font.name='Calibri';st.font.color.rgb=RGBColor(0,0,0)
for st in D.styles:
 for el in list(st.element.xpath('.//w:pBdr')):el.getparent().remove(el)
D.styles['Normal'].font.size=Pt(11);D.styles['Normal'].paragraph_format.line_spacing=1.08;D.styles['Normal'].paragraph_format.space_after=Pt(8)
for name,size in [('Title',22),('Subtitle',12),('Heading 1',15),('Heading 2',12)]:
 D.styles[name].font.size=Pt(size);D.styles[name].paragraph_format.space_before=Pt(12);D.styles[name].paragraph_format.space_after=Pt(7)
D.styles['Title'].font.bold=True
D.core_properties.title='Institutional control across six Core decisions'
D.core_properties.subject='Round 11 comparative institutional process model'
D.core_properties.author='Murray A. Rudd'
def p(s,style=None):
 pp=D.add_paragraph(s,style)
 prev=pp._p.getprevious()
 if prev is not None and prev.tag==qn('w:tbl'):pp.paragraph_format.space_before=Pt(8)
 return pp
def h(s,new=False):
 pp=D.add_heading(s,1);pp.paragraph_format.page_break_before=new;return pp
def link(pp,label,url):
 rel=pp.part.relate_to(url,'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',is_external=True)
 e=OxmlElement('w:hyperlink');e.set(qn('r:id'),rel);r=OxmlElement('w:r');pr=OxmlElement('w:rPr');c=OxmlElement('w:color');c.set(qn('w:val'),'174F73');pr.append(c);r.append(pr);t=OxmlElement('w:t');t.text=label;r.append(t);e.append(r);pp._p.append(e)
def table(headers,rows,widths):
 t=D.add_table(rows=1,cols=len(headers));t.autofit=False;t.alignment=WD_TABLE_ALIGNMENT.CENTER
 for col,w in zip(t.columns,widths):col.width=Inches(w)
 for c,v,w in zip(t.rows[0].cells,headers,widths):c.text=v;c.width=Inches(w)
 t.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
 for row in rows:
  for c,v,w in zip(t.add_row().cells,row,widths):c.text=v;c.width=Inches(w)
 for i,row in enumerate(t.rows):
  row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
  for cell in row.cells:
   cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER;pr=cell._tc.get_or_add_tcPr()
   mar=OxmlElement('w:tcMar')
   for edge in ['top','left','bottom','right']:
    e=OxmlElement('w:'+edge);e.set(qn('w:w'),'90');e.set(qn('w:type'),'dxa');mar.append(e)
   pr.append(mar);br=OxmlElement('w:tcBorders')
   for edge in ['top','left','bottom','right']:
    e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');br.append(e)
   pr.append(br);sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'DDE8EE' if i==0 else ('F5F7F8' if i%2==0 else 'FFFFFF'));pr.append(sh)
   for pp in cell.paragraphs:
    pp.paragraph_format.space_before=Pt(3);pp.paragraph_format.space_after=Pt(3);pp.paragraph_format.line_spacing=1.03
    for rr in pp.runs:rr.font.size=Pt(10);rr.font.bold=(i==0)
 return t

p('Institutional control across six Core decisions','Title')
p('Round 11 Comparative model of participation and decision making','Subtitle')
p('November 6 2026   Version 0.1')
p('Bitcoin Core’s handling of the datacarrier dispute separates the opportunity to contribute from control over particular decisions. Authors select and revise proposals, reviewers supply reasons, maintainers integrate changes, and release participants address additional constraints. Across six linked proposals, these arrangements allow some questions to reach a recorded disposition while participants continue to contest related policy choices and the grounds for authority. I use the comparison to explain how those distinct controls operate within the dispute. [E23–25, E30–32, F32359, F32381, F32406, F32714, F33224, F33453]')
p('The closure records add an important distinction to the earlier reconstruction. Glozow closed the original proposal and pointed to an alternative that retained configuration; darosior closed the narrower proposal as its author after judging the intended agreement absent; achow101 closed the June warning revision as its author after reviewers disputed its wording and timing. The last account later merged both September revisions. These events show why a model should attach authority to an actor’s role and decision object within each episode, while treating author closure and closure by another participant as different acts. [E01, E04, E14, F32359, F32381, F32714, F33224, F33453]')
table(['Analytical dimension','Question','Evidence required'],[
 ('Preference','What outcome does the actor favor?','An attributed position tied to a specific object'),
 ('Normative claim','What should someone do or recognize?','An existing IG2 unit with its retained evidential standing'),
 ('Role or control','Who can decide which question?','Documented allocation, local recognition, or a scoped role claim'),
 ('Exercised action','What act and immediate result occurred?','An identified event, patch, or attributed action report')
],[1.25,2.1,3.55])
p('These dimensions form an analytical overlay on the existing coding. A statement can express both a preference and a normative claim, while a technical argument may remain contextual evidence. I connect the selected statements to responses and disposition events without converting every argument into an institution or promoting an asserted expectation because a later outcome happens to fit it. The resulting model includes a reproducible account of the selected code changes and twelve explicit links between institutional statements and action records. [IL01–12]')

h('Comparison across the six proposals',True)
p('The six cases belong to one connected dispute. Their alternatives, participants, and reasons overlap: C2 closed before C1, and C3 opened while C1 remained active. I retain the existing identifiers for continuity and compare the decision objects and disposition acts rather than treating the cases as independent trials. The supporting backport remains an additional implementation event within C6. [F32359, F32381, F32406, F33473]')
table(['Case and PR','Decision object','Recorded control and disposition'],[
 ('C1 32359','Remove limits and configuration options','glozow closes May 12; redirects to a proposal retaining options'),
 ('C2 32381','Allow multiple outputs with per-output limits','darosior closes own proposal April 30 after a technical objection and his assessment of contributor disagreement'),
 ('C3 32406','Raise default; retain deprecated options; use an aggregate budget','glozow merges June 9 after presenting a readiness judgment'),
 ('C4 32714','Replace deprecation with non-recommendation','achow101 closes own proposal June 10 after competing reviews'),
 ('C5 33224','Change will be removed to expected to be removed','achow101 merges September 2; translation constraints form part of the discussion'),
 ('C6 33453','Remove deprecation and its startup warning','achow101 merges September 30; fanquake merges supporting PR 33473 into 30.x October 6')
],[1.0,2.45,3.45])
p('C2 provides a direct check on the idea that reducing scope is sufficient for acceptance. Poinsot sought a smaller first step, yet Towns challenged the design because multiple individually limited outputs could bypass the intended constraint and add redundant overhead. The proposer then closed the case after concluding that his intended agreement among regular contributors was absent. C3 subsequently integrated a different design with aggregate budgeting and retained options, so the contrast combines institutional accommodation with technical differences and accumulated review. [E02–04, E07, N902, F32381, F32406]')
p('C4 supplies a different contrast. Towns preferred leaving the choice to users without discouragement while rejecting the proposed distinction between deprecation and non-recommendation; another reviewer objected to reopening a recent decision. Closure therefore did not extinguish every premise in the discussion or establish a common preference for the status quo. The later September proposal removed discouragement without adding June’s substitute wording, making the two proposals analytically distinct. [E12–14, N904, KJ, KS]')

h('A reproducible account of the changes',True)
p('The recorded integrations altered different elements of the software configuration. I track the default setting, the allocation of the data budget across outputs, continued option availability, deprecation status, and the startup warning. The model applies only merged changes and leaves the tracked state unchanged when a proposal closes without merge. It reconstructs the selected main-branch changes; it does not simulate adoption, predict acceptance, or represent a change to Bitcoin’s consensus rules. [F32406_files, X32406, X33224, X33453]')
table(['Recorded state','Default and output budget','Options','Deprecation and warning'],[
 ('Before C3','Earlier setting of 83; one output','Available','No deprecation or removal warning in the tracked fields'),
 ('After C3 June 9','Setting of 100,000; aggregate budget across outputs','Available','Deprecated; warning says will be removed'),
 ('After C5 September 2','Same higher setting and aggregate budget','Available','Deprecated; warning says expected to be removed'),
 ('After C6 September 30','Same higher setting and aggregate budget','Available','Deprecation and startup warning removed')
],[1.25,2.2,.8,2.65])
p('The 83 setting concerns script size, including overhead, and the higher default remains subject to transaction size constraints. Keeping those technical objects distinct prevents removal of deprecation from becoming a claim that Core restored the earlier policy. C4 proposed an intervening formulation but never changed the tracked main-branch state. The October 6 backport confirms integration into a release branch; publication and installation remain separate outcomes. [F32406_files, KJ, F32714, F33473]')
p('This sequence also clarifies the institutional object of the warning dispute. Retaining a usable option did not resolve what developers were signaling about its future, so later proposals addressed the language surrounding continued availability. The normative claim that warnings should correspond to an actual removal plan could therefore recur while the proposed implementation changed. The outcome supports a bounded account of correcting that signal; it does not establish that users revised their expectations or that Core undertook a permanent maintenance obligation. [E09, E12, E18–20, N903, N907]')
p('The same actor can occupy different positions across this sequence. Achow101 proposed the unmerged June revision and later exercised merge control over the September changes. That record weakens an account organized around fixed camps of decision makers and excluded proposers, while leaving the influence of review on each action open to analysis. A role identifies the control relevant to a particular act; an account name alone does not supply its institutional meaning. [F32714, F33224, F33453]')

h('Connecting grammar to institutional action',True)
p('The existing IG2 parses identify the structure of prescriptions and role claims, while the accompanying evidence assessments distinguish documented arrangements, local recognition, disputed claims, and text alone. I preserve those assessments and add explicit links to decision objects, responses, and events. Each link states what connects the records and what inference that connection permits. This makes the movement from a coded statement to a governance explanation visible for source review. [IL01–12]')
table(['Existing unit','Retained standing','What the linked record establishes'],[
 ('D01 Merge responsibility','Documented','Named merge events connect the allocated responsibility to observed integration'),
 ('U25 Warning expectation','Locally supported','Attribution and application connect an earlier proposition to a later, different proposal'),
 ('U39 Backport responsibility','Locally supported','Specific deference accompanies separate decisions over main and release-branch integration'),
 ('U32 Translation freeze','Text only','A participant invokes a restriction; the wording patch does not verify its full force or execution'),
 ('PU06 Community responsiveness','Text only','An interview supplies a scoped normative demand, without a constituency definition or approval threshold')
],[1.7,1.2,4.0])
p('The contribution guide provides a clear example of why the link must preserve its object. It opens peer review, assigns integration to merge maintainers, and distinguishes answering feedback from accepting it. The June Mechanic–Todd exchange demonstrates a reply followed by continued disagreement, while glozow’s readiness account and recorded merge supply a different connection between assessment and exercised control. Todd’s participation does not by itself establish that the proposal author fulfilled every review obligation, and a merge does not independently verify the adequacy of the underlying assessment. [D01–03, D05, D06, E08, R10E01–05, F32406; IL02–04]')
p('C5 prevents a different overstatement. Hebasto’s proposed route addresses a translation constraint, yet the eventual wording change does not prove the operation of every asserted freeze rule or confirm how translators handled the string. U32 and U33 therefore retain their existing standing despite a compatible integration outcome. C6 provides stronger evidence of a specific recognized responsibility because the proposer explicitly defers release timing to maintainers, although even that recognition supplies no authority over network adoption. [E15–17, E24, E25, U32, U33, U39; IL07, IL08]')
p('Moderation remains a parallel control over participation and visibility. The matched April cases identify an offer to reconsider a duplicate classification and an announced block that the participant acknowledged; the June record separately documents substantive replies to an objection. Neither sequence resolves the other, and the April block does not establish enforcement of a June warning directed at someone else. [W04, R10E01–08, E35; IL11]')

h('Explanations supported by the comparison',True)
p('The strongest explanation combines the separation of decision objects with differentiated control and continuing reassessment of reasons. Participants can preserve a disagreement over appropriate data use while accepting a narrower change to configuration or warning language; reviewers and maintainers still evaluate the content and feasibility of that change. The comparison supports this account of the observed process without assigning causal weights to scope, technical judgment, review investment, or release timing. Each factor has identifiable evidence and a limit that the model preserves. [E07, E09, E10, E19, E23–28, R10E13–19]')
table(['Explanation tested','Result across the selected cases'],[
 ('Smaller scope ensures acceptance','C2 contradicts sufficiency; its design also differs technically'),
 ('Every unmerged case is a maintainer veto','C2 and C4 are author closures; C1 has a different closer'),
 ('Integration requires agreement on all preferences','C3 and C6 integrate changes while wider disagreement persists'),
 ('September adopts the identical June proposal','The identified commits and reasons differ'),
 ('Content support determines release execution','Translation and release decisions require separate attention'),
 ('Retained options demonstrate effective influence','Operator adoption and network influence remain unestablished')
],[2.75,4.15])
p('The epistemic issue concerns the authority to assess reasons as well as their technical substance. Participants disagree over what makes an objection reasonable, how contributor experience should count, and which users or community members a decision should answer to. Repository procedures provide a way to reach a disposition despite those competing standards, yet the disposition does not resolve the standards themselves. This gives the paper a concrete connection between epistemic disagreement, institutional arrangements, and exercised control without requiring a verdict on every technical argument. [E32, E37, E38, N15, N16, PE16, PE22]')
p('The central research question can now focus on how Bitcoin Core converts open participation and contested expectations into decisions over software policy and release. The methodological contribution is the explicit connection between grammatical units and decision processes: preserved source spans and evidential standing, actor and object attribution, response sequences, and recorded changes. The substantive contribution concerns the distribution and limits of authority within an open software project. It does not depend on describing Bitcoin as uniformly decentralized at every level. [E23–25, E30–32, IL01–12]')
p('The next paper preparation step is a methods and results draft organized around this comparison. The six cases, the state reconstruction, and the institution–action links provide the analytical core; the existing introduction and background can then be aligned with the narrower claim. Additional general podcast collection would add less than focused review of these explicit links and the retained coding before any claim of independent validation.')

h('Appendix Evidence and reproducibility',True)
p('The comparison retains six focal cases and one supporting backport event. Seven refreshed pull-request records identify authors and merge actors; three issue records identify the actors who closed the unmerged proposals. Their creation, closure, and merge dates and head revisions match the frozen evidence. A further changed-file retrieval confirms the relevant C3 patches. The package contains 77 inherited exact anchors, 46 selected inherited units, 76 inherited GitHub source records, twelve institution–action links, and six explicit comparison tests.')
p('The scripts rebuild the comparison and replay the selected main-branch transitions from the preserved inputs. Only a confirmed merge changes the state; an API merge-hash field on an unmerged proposal does not count as integration. The initial tracked fields come from the old lines of C3’s patch, and the replay does not represent every intervening repository change. Code execution checks internal consistency and provenance, not the truth of participants’ technical claims or the causal adequacy of the governance explanation.')
p('The June 9 contribution guide supplies dated documentary context for C3 and later comparisons; it does not independently establish its exact April wording. The moderation guide uses a pinned August 14, 2024 revision. Edited proposal bodies retain their limits: the analysis does not date every sentence to the opening of a proposal, and the June and September commit records and dated quotations retain their narrower evidential roles.')
p('The podcast corpus remains seven recordings and 27 passages, with six statement units and 21 context units. All six podcast statement units retain text only standing, and PU01 remains context. PU03 retains only the clear release-role clause; the garbled adjacent material remains outside scope. The Hughes and Mechanic exclusion remains in force, and neither that interview nor the unmatched ban and Twitter claims acquire substitute evidence here. This round adds no IG2 statement or changes to existing grammar assignments; the work remains internal analysis rather than independent validation.')
p('References in brackets identify preserved sources, exact anchors, units, or institution–action links in the evidence package. F identifiers denote refreshed platform records; E, N9, R10E, PE, D, U, and PU identifiers retain their inherited meanings. X identifiers denote patch contexts, KJ and KS identify the June and September commits, and W identifiers denote the retained public source cards.')
D.add_heading('Primary source guide',2)
for label,url in [
 ('C1 PR 32359 Closure and alternative','https://github.com/bitcoin/bitcoin/pull/32359#issuecomment-2872995148'),
 ('C2 PR 32381 Author closure','https://github.com/bitcoin/bitcoin/pull/32381#issuecomment-2843023281'),
 ('C3 PR 32406 Readiness account','https://github.com/bitcoin/bitcoin/pull/32406#issuecomment-2955614286'),
 ('C4 PR 32714 Alternative wording','https://github.com/bitcoin/bitcoin/pull/32714'),
 ('C5 PR 33224 Translation route','https://github.com/bitcoin/bitcoin/pull/33224#issuecomment-3241930685'),
 ('C6 PR 33453 Proposal discretion','https://github.com/bitcoin/bitcoin/pull/33453#issuecomment-3338979025'),
 ('Supporting PR 33473 Release branch integration','https://github.com/bitcoin/bitcoin/pull/33473')
]:
 pp=p('');pp.paragraph_format.space_after=Pt(3);link(pp,label,url)
for section in D.sections:
 pp=section.footer.paragraphs[0];pp.alignment=WD_ALIGN_PARAGRAPH.RIGHT
 run=pp.add_run();fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');run._r.addnext(fld)
path=O/'Core_Knots_Round11_Comparative_Institutional_Model_v01.docx'
D.save(path);print(path)

