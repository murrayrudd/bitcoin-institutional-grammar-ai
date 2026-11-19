from pathlib import Path
import json,sys
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
R=Path(__file__).resolve().parents[1]
doc=Document();sec=doc.sections[0]
sec.page_width=Inches(8.5);sec.page_height=Inches(11)
sec.top_margin=sec.bottom_margin=Inches(.65);sec.left_margin=sec.right_margin=Inches(.7)
normal=doc.styles['Normal'];normal.font.name='Calibri';normal.font.size=Pt(11)
normal.paragraph_format.space_after=Pt(7);normal.paragraph_format.line_spacing=1.04
for name,size in [('Title',20),('Subtitle',11),('Heading 1',14),('Heading 2',12)]:
    s=doc.styles[name];s.font.name='Calibri';s.font.size=Pt(size);s.font.color.rgb=RGBColor(0,0,0)
    s.paragraph_format.space_before=Pt(9 if 'Heading' in name else 0);s.paragraph_format.space_after=Pt(6);s.paragraph_format.keep_with_next=True
    for b in list(s._element.iter(qn('w:pBdr'))):b.getparent().remove(b)
sec.footer_distance=Inches(.3);footer=sec.footer.paragraphs[0];footer.alignment=2
run=footer.add_run('Governance research projects  |  ');run.font.size=Pt(9)
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footer._p.append(field)
def p(text):doc.add_paragraph(text)
def h(text):doc.add_paragraph(text,'Heading 1')
def table(headers,rows,widths,size=10.5):
    t=doc.add_table(rows=1,cols=len(headers));t.autofit=False
    borders=OxmlElement('w:tblBorders')
    for edge in ['top','left','bottom','right','insideH','insideV']:
        e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');borders.append(e)
    t._tbl.tblPr.append(borders)
    for i,x in enumerate(headers):t.rows[0].cells[i].text=x
    for row in rows:
        cells=t.add_row().cells
        for i,x in enumerate(row):cells[i].text=x
    repeat=OxmlElement('w:tblHeader');repeat.set(qn('w:val'),'true');t.rows[0]._tr.get_or_add_trPr().append(repeat)
    for ri,row in enumerate(t.rows):
        ns=OxmlElement('w:cantSplit');row._tr.get_or_add_trPr().append(ns)
        for ci,c in enumerate(row.cells):
            c.width=Inches(widths[ci]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            mar=OxmlElement('w:tcMar')
            for side in ['top','left','bottom','right']:
                e=OxmlElement('w:'+side);e.set(qn('w:w'),'90');e.set(qn('w:type'),'dxa');mar.append(e)
            c._tc.get_or_add_tcPr().append(mar)
            if ri==0:
                shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'E9EDF1');c._tc.get_or_add_tcPr().append(shade)
            for pa in c.paragraphs:
                pa.paragraph_format.space_before=Pt(2);pa.paragraph_format.space_after=Pt(2);pa.paragraph_format.line_spacing=1
                for run in pa.runs:run.font.size=Pt(size);run.bold=ri==0
    for i,w in enumerate(widths):t.columns[i].width=Inches(w)
    doc.add_paragraph().paragraph_format.space_after=Pt(1)

doc.add_paragraph('Bitcoin Core IG2 collaborative reconciliation','Title')
doc.add_paragraph('Coding specification 0.4  |  November 7 2026','Subtitle')
p('The reconciliation produces a usable analytical dataset with explicit limits. It corrects proposal identity, partial-support claims, relation direction, and several coding conventions. The discussion also resolves how to describe visible artifacts and reported implementation. Some classification choices remain defensible alternatives. The original independent coding and its agreement results remain unchanged.')
h('Purpose and design')
p('Three fresh reviewing agents examined ten focused topics from the prior source audits. Each recorded an initial position, then read all three positions and responded to the others in one bounded peer round. These reviewers were not the original coders. They shared the same inherited model configuration, source packets, frozen v0.4 materials, and prior adjudications. This is deliberative reconciliation, not a new independent reliability test or a cross-model comparison.')
p('The source material remains the three fresh-evaluation cases. No new sources or coding criteria were introduced. The package contains nine adjusted v0.4 views, a decision overlay, and eight bounded case conclusions. The views retain valid differences in unit boundaries and interpretation; they must not be counted as nine independent confirmations of the final conclusions.')
table(['Case','Retained analytical conclusion'],[
('F01  PR 26586','Competing release-selection criteria, integration of the v24.0.1 addition, and broader cleanup deferred to unidentified future work.'),
('F02  PR 14441','Four bounded edit suggestions, attributed update reports, and integrated release-note content. The prior typo and individual reply pairings remain unverified.'),
('F03  PR 7819','A distinction between reviewing a checkbox proposal and exposing it before a replacement workflow exists. Both identified PRs are recorded closed without merge.')],[1.25,5.85])
h('Corrections and preserved evidence')
p('The four primary v0.4 correction groups now appear in separate adjusted records: unidentified future work no longer inherits PR 26586, the general cleanup assent has a properly scoped object, the repeated open-PR method no longer claims the full original condition, and the cleanup uptake relation points from proposal to response. Two reference-only v0.3 copies also remove unsupported earlier/later wording claims. None of these repairs rewrites the original evaluation.')

doc.add_page_break();h('Discussion decisions')
p('The panel agreed on many evidentiary boundaries while retaining some differences in preferred coding. The decision overlay records those distinctions rather than collapsing them into a post-discussion agreement score.')
table(['Topic','Result and remaining limit'],[
('D01  Assent and identity','Future-work and general-criterion identities are corrected. Ordinary tentative assent and unresolved expectation recognition remain competing readings; adoption is not established.'),
('D02  Same actor','The later method supports only the broader open-PR approach. Personal continuity remains in response events. A codebook/checker ambiguity prevents a clean summary-label resolution.'),
('D03  Artifacts','The resulting spelling is observed. Its correction history is not. A checkbox artifact is visible, but complete placement and workflow qualifications remain unverified.'),
('D04  Reports','Contextual incorporation of the edits is defensible; broader report targeting remains an alternative. Rebasing on master does not verify the after-26589 condition.'),
('D05  Technical need','Undetermined remains the preferred synthesis for terse rebase requests, with a proposed norm retained as an alternative. No authority or institutional obligation follows from needs.'),
('D06  Levels','Operational conduct and choosing a recurring arrangement are distinct analytical layers. Existing primary labels remain when their rationales identify the layer.'),
('D07  Challenges','Readiness can challenge an offered feature while leaving artifact facts intact. Current technical necessity, continued applicability, and future scope require separate targets.'),
('D08  Relations','Uptake direction is repaired. Quoted cost concerns receive clarifying responses; the weaker release-risk/pause link records temporal order. No causal adoption follows.'),
('D09  Bot referent','The conditional announcement remains. The pronoun may refer to the review, comment, or displayed listing; no execution is observed.'),
('D10  Candidate types','The panel prefers methods and proposed restraint as strategy/norm candidates, with technical-preference alternatives retained. A literal action parse is selected without reclassifying the earlier defensible parse as an error.')],[1.35,5.75],10.5)
p('The peer responses contain real revisions. A and C withdrew their proposed same_actor_only profile changes after examining the frozen checker. A moved to temporal linking for the weakly attributed response sequence. C accepted the offered-feature readiness interpretation while retaining the artifact-focused alternative. A and B narrowed recommendations that would have imposed a single report scope or challenge target across all views.')

doc.add_page_break();h('Two distinctions that matter for the paper')
doc.add_paragraph('An artifact can be observed without reconstructing its history','Heading 2')
p('The spelling request specifies listtransactions with a final s. The retained integrated artifact contains that identifier. All three reviewers accept observation of the resulting spelling, while leaving the earlier typo, repair location, and causal sequence unverified. F02 r1 therefore changes from reported application alone to reported and observed application. The other views retain their broader scope for the aggregate report. This is a scoped evidentiary judgment, not a new requirement for every case to include a before-and-after record.')
p('The checkbox case has a different limit. An unmerged patch can demonstrate a prepared artifact, but the retained fragments do not verify every condition in the complete proposition. Its complete application remains unresolved. The distinction prevents both underclaiming visible work and overclaiming implementation.')
doc.add_paragraph('Personal continuity is distinct from shared recognition','Heading 2')
p('The author’s repeated willingness to proceed with review shows a maintained personal approach. The frozen codebook says that same-actor events alone give same_actor_only, but the frozen checker first filters for this-proposition expectation_recognition events. The relevant records are response events. The adjusted views preserve recognition none under that implementation and retain the personal continuity in the event records and decision overlay. The panel did not invent expectation recognition to obtain the preferred summary label. This discrepancy remains a specification-maintenance issue for a later version, outside the present reconciliation.')
h('Implications for the working paper')
p('The paper can describe a two-stage process: independent coding followed by source-based review and documented deliberation. It should report the original agreement results as reproducibility evidence and use the reconciled records for bounded substantive analysis. Negotiated convergence does not replace those original results or establish external validity. Neither this exercise nor the earlier comparison establishes superiority to human coders, cross-model robustness, or reduced time and cost.')
p('The practical contribution is an inspectable path from source passages through competing interpretations to constrained conclusions. Remaining alternatives identify where the evidence or the coding convention cannot select a single answer. They do not require the analysis to choose participants’ values or make the policy decision.')
h('Files and verification')
p('The evidence package starts at dataset/reconciled_dataset.json. It includes all initial and peer-response records, the ten-topic decision overlay, dispositions for all 59 prior issue groups, and a before/after change log. Nine adjusted v0.4 annotations pass the unchanged checker. Metadata aliases expose identifiers already present in the retained packets; source text is unchanged. These checks establish structural integrity and exact anchors, while the source-based decisions remain explicit analytical judgments.')
doc.core_properties.title='Bitcoin Core IG2 collaborative reconciliation'
doc.core_properties.subject='Post-evaluation reconciliation of source interpretation under frozen project coding specification 0.4'
doc.core_properties.author='Governance research projects'
out=Path(sys.argv[1]);doc.save(out);print(out)
