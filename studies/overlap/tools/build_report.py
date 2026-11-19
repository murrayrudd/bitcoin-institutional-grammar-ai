"""Build the readable study report from the reviewed report content."""
from pathlib import Path
import json
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'report/report_content.json').read_text())
doc=Document()
sec=doc.sections[0]
sec.page_width=Inches(8.5);sec.page_height=Inches(11)
sec.top_margin=Inches(.7);sec.bottom_margin=Inches(.7)
sec.left_margin=Inches(.8);sec.right_margin=Inches(.8)
sec.header_distance=Inches(.3);sec.footer_distance=Inches(.3)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3']:
    s=doc.styles[name];s.font.name='Calibri';s.font.color.rgb=RGBColor(0,0,0)
    s.paragraph_format.widow_control=True
    rp=s.element.get_or_add_rPr()
    for e in list(rp):
        if e.tag==qn('w:rFonts'):
            for k in list(e.attrib):
                if k.endswith('Theme'):del e.attrib[k]
    pp=s.element.get_or_add_pPr()
    for e in list(pp):
        if e.tag==qn('w:pBdr'):pp.remove(e)
normal=doc.styles['Normal']
normal.font.size=Pt(11);normal.paragraph_format.line_spacing=1.12
normal.paragraph_format.space_after=Pt(7)
for name,size in [('Title',22),('Heading 1',14),('Heading 2',12),('Heading 3',11)]:
    s=doc.styles[name];s.font.size=Pt(size);s.font.bold=True
    s.paragraph_format.space_before=Pt(12 if name!='Title' else 0)
    s.paragraph_format.space_after=Pt(7)
    s.paragraph_format.keep_with_next=True
doc.styles['Subtitle'].font.size=Pt(10)
doc.styles['Subtitle'].font.italic=False
doc.styles['Subtitle'].paragraph_format.space_after=Pt(12)

footer=sec.footer.paragraphs[0]
footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
r=footer.add_run('Core governance overlap validation  |  ');r.font.size=Pt(9)
f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGE');footer._p.append(f)

def para(text,style=None):
    p=doc.add_paragraph(text,style)
    return p

def table(block):
    if block.get('caption'):
        p=para(block['caption']);p.paragraph_format.keep_with_next=True
        p.runs[0].bold=True
    rows=[block['headers']]+block['rows']
    t=doc.add_table(rows=0,cols=len(rows[0]));t.autofit=False
    widths=block.get('widths',[6.9/len(rows[0])]*len(rows[0]))
    for c,w in zip(t.columns,widths):c.width=Inches(w)
    pr=t._tbl.tblPr
    borders=OxmlElement('w:tblBorders')
    for edge in ['top','left','bottom','right','insideH','insideV']:
        e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');borders.append(e)
    pr.append(borders)
    for i,values in enumerate(rows):
        row=t.add_row()
        trpr=row._tr.get_or_add_trPr()
        no_split=OxmlElement('w:cantSplit');trpr.append(no_split)
        if i==0:
            repeat=OxmlElement('w:tblHeader');trpr.append(repeat)
        for j,(cell,text) in enumerate(zip(row.cells,values)):
            cell.width=Inches(widths[j]);cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            tcpr=cell._tc.get_or_add_tcPr()
            mar=OxmlElement('w:tcMar')
            for side in ['top','bottom','left','right']:
                e=OxmlElement('w:'+side);e.set(qn('w:w'),'100');e.set(qn('w:type'),'dxa');mar.append(e)
            tcpr.append(mar)
            if i==0:
                sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'E5E7EB');tcpr.append(sh)
            p=cell.paragraphs[0];p.paragraph_format.space_after=Pt(0);p.paragraph_format.line_spacing=1.05
            if j in block.get('center_columns',[]):p.alignment=WD_ALIGN_PARAGRAPH.CENTER
            r=p.add_run(str(text));r.font.size=Pt(10);r.bold=(i==0)
    p=para('');p.paragraph_format.space_after=Pt(0);p.paragraph_format.space_before=Pt(0)
    p.paragraph_format.line_spacing=0.3
    p.add_run('').font.size=Pt(2)
    if block.get('note'):
        p=para(block['note'])
        for r in p.runs:r.font.size=Pt(9.5)

para(DATA['title'],'Title');para(DATA['subtitle'],'Subtitle')
for block in DATA['blocks']:
    kind=block['kind']
    if kind=='heading':para(block['text'],'Heading '+str(block.get('level',1)))
    elif kind=='paragraph':para(block['text'])
    elif kind=='table':table(block)
    elif kind=='page_break':doc.add_page_break()
    elif kind=='bullet':para(block['text'],'List Bullet')
    else:raise ValueError(kind)
doc.core_properties.title=DATA['title']
doc.core_properties.subject='Overlapping AI coding validation of Bitcoin Core governance sources'
doc.core_properties.author='AI-assisted research analysis for Murray A. Rudd'
output=ROOT/'report/Core_Knots_Round12_Overlap_Validation_v01.docx'
doc.save(output)
print(output)
