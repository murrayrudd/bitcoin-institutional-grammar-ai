"""Build the report from the retained, source-reviewed report_content.json."""
from pathlib import Path
import json,sys
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

R=Path(__file__).resolve().parents[1]
data=json.loads((R/'analysis/report_content.json').read_text())
doc=Document()
sec=doc.sections[0]
sec.page_width=Inches(8.5);sec.page_height=Inches(11)
sec.top_margin=sec.bottom_margin=Inches(.7)
sec.left_margin=sec.right_margin=Inches(.7)
sec.header_distance=sec.footer_distance=Inches(.3)
normal=doc.styles['Normal'];normal.font.name='Calibri';normal.font.size=Pt(11)
normal.paragraph_format.space_after=Pt(6)
normal.paragraph_format.line_spacing=1.05
for name,size in [('Title',20),('Subtitle',11),('Heading 1',14),('Heading 2',12)]:
    s=doc.styles[name];s.font.name='Calibri';s.font.size=Pt(size);s.font.color.rgb=RGBColor(0,0,0)
    s.paragraph_format.space_before=Pt(12 if 'Heading' in name else 0)
    s.paragraph_format.space_after=Pt(6)
    s.paragraph_format.keep_with_next=True
    for border in list(s._element.iter(qn('w:pBdr'))):
        border.getparent().remove(border)
footer=sec.footer.paragraphs[0];footer.alignment=2
run=footer.add_run('Governance research projects  |  ');run.font.size=Pt(9)
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footer._p.append(field)

def add_table(block):
    headers=block['headers'];rows=block['rows'];widths=block.get('widths',[7.1/len(headers)]*len(headers))
    table=doc.add_table(rows=1,cols=len(headers));table.autofit=False
    table.alignment=0
    props=table._tbl.tblPr
    borders=OxmlElement('w:tblBorders')
    for edge in ['top','left','bottom','right','insideH','insideV']:
        element=OxmlElement('w:'+edge);element.set(qn('w:val'),'single');element.set(qn('w:sz'),'4');element.set(qn('w:color'),'B7B7B7');borders.append(element)
    props.append(borders)
    for i,(cell,text) in enumerate(zip(table.rows[0].cells,headers)):
        cell.text=str(text);cell.width=Inches(widths[i])
        shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'EDEDED');cell._tc.get_or_add_tcPr().append(shade)
        for run in cell.paragraphs[0].runs:run.bold=True
    repeat=OxmlElement('w:tblHeader');repeat.set(qn('w:val'),'true');table.rows[0]._tr.get_or_add_trPr().append(repeat)
    for values in rows:
        row=table.add_row()
        for i,(cell,text) in enumerate(zip(row.cells,values)):
            cell.text=str(text);cell.width=Inches(widths[i])
    for row in table.rows:
        cant=OxmlElement('w:cantSplit');row._tr.get_or_add_trPr().append(cant)
        for cell in row.cells:
            for p in cell.paragraphs:
                p.paragraph_format.space_after=Pt(3);p.paragraph_format.space_before=Pt(3)
                for run in p.runs:run.font.name='Calibri';run.font.size=Pt(block.get('font_size',9.5))
    for i,w in enumerate(widths):table.columns[i].width=Inches(w)
    doc.add_paragraph()
    if block.get('note'):
        p=doc.add_paragraph(block['note']);p.paragraph_format.space_after=Pt(8)
        for run in p.runs:run.font.size=Pt(9)

doc.add_paragraph(data['title'],'Title')
doc.add_paragraph(data['subtitle'],'Subtitle')
for block in data['blocks']:
    kind=block['type']
    if kind=='heading':doc.add_paragraph(block['text'],'Heading '+str(block.get('level',1)))
    elif kind=='paragraph':doc.add_paragraph(block['text'])
    elif kind=='table':add_table(block)
    elif kind=='bullet':doc.add_paragraph(block['text'],'List Bullet')
    elif kind=='page_break':doc.add_page_break()
    else:raise ValueError(kind)
doc.core_properties.title=data['title']
doc.core_properties.subject='Prospective comparison of IG2 project coding specifications 0.3 and 0.4'
doc.core_properties.author='Governance research projects'
doc.core_properties.keywords='IG2; institutional analysis; AI-assisted coding; intercoder agreement'
out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True);doc.save(out)
print(out)
