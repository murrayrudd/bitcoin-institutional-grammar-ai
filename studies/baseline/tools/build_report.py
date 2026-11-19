from pathlib import Path
import json,sys,re
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
R=Path(__file__).resolve().parents[1]
def doc(title,subtitle):
 d=Document();s=d.sections[0];s.page_width=Inches(8.5);s.page_height=Inches(11)
 s.top_margin=Inches(.65);s.bottom_margin=Inches(.65);s.left_margin=Inches(.78);s.right_margin=Inches(.78)
 for n,size in [('Normal',11),('Title',23),('Subtitle',12),('Heading 1',16),('Heading 2',12)]:
  st=d.styles[n];st.font.name='Calibri';st.font.size=Pt(size);st.font.color.rgb=RGBColor(0,0,0)
  st.paragraph_format.space_after=Pt(7);st.paragraph_format.line_spacing=1.03;st.paragraph_format.space_before=Pt(0 if n!='Heading 2' else 9)
 d.core_properties.title=title;d.core_properties.subject=subtitle;d.core_properties.author='Murray A. Rudd research project'
 f=s.footer.paragraphs[0];f.alignment=WD_ALIGN_PARAGRAPH.RIGHT;f.add_run('Bitcoin Core   |   Expansion round   |   ').font.size=Pt(9)
 field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');f._p.append(field)
 return d
def clean(d):
 for tree in [d.styles.element,d.element]:
  for b in list(tree.xpath('.//w:pBdr')):b.getparent().remove(b)
def table(d,headers,rows,widths):
 t=d.add_table(rows=1,cols=len(headers));t.autofit=False
 for c,w in zip(t.columns,widths):c.width=Inches(w)
 for c,txt in zip(t.rows[0].cells,headers):c.text=str(txt)
 for row in rows:
  for c,txt in zip(t.add_row().cells,row):c.text=str(txt)
 for i,row in enumerate(t.rows):
  row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
  for j,c in enumerate(row.cells):
   c.width=Inches(widths[j]);pr=c._tc.get_or_add_tcPr()
   mar=OxmlElement('w:tcMar')
   for side in ['top','left','bottom','right']:
    el=OxmlElement('w:'+side);el.set(qn('w:w'),'90');el.set(qn('w:type'),'dxa');mar.append(el)
   pr.append(mar);borders=OxmlElement('w:tcBorders')
   for side in ['top','left','bottom','right']:
    el=OxmlElement('w:'+side);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');borders.append(el)
   pr.append(borders)
   if i==0:
    fill=OxmlElement('w:shd');fill.set(qn('w:fill'),'E8EDF2');pr.append(fill)
   for p in c.paragraphs:
    p.paragraph_format.space_after=Pt(2);p.paragraph_format.line_spacing=1
    for run in p.runs:run.font.size=Pt(10.5);run.bold=(i==0)
   c.vertical_alignment=1
  if i==0:
   rp=row._tr.get_or_add_trPr();repeat=OxmlElement('w:tblHeader');rp.append(repeat)
 d.add_paragraph().paragraph_format.space_after=Pt(1)
 return t
def linkify(d):
 paragraphs=list(d.paragraphs)+[p for t in d.tables for row in t.rows for c in row.cells for p in c.paragraphs]
 for p in paragraphs:
  text=p.text;matches=list(re.finditer(r'https?://[^\s]+',text))
  if not matches:continue
  size=p.runs[0].font.size if p.runs else None
  for child in list(p._p):
   if child.tag!=qn('w:pPr'):p._p.remove(child)
  end=0
  for m in matches:
   url=m.group(0).rstrip('.,;')
   if m.start()>end:
    run=p.add_run(text[end:m.start()]);run.font.size=size
   h=OxmlElement('w:hyperlink');h.set(qn('r:id'),p.part.relate_to(url,RT.HYPERLINK,is_external=True))
   run=OxmlElement('w:r');pr=OxmlElement('w:rPr')
   color=OxmlElement('w:color');color.set(qn('w:val'),'0563C1');pr.append(color)
   underline=OxmlElement('w:u');underline.set(qn('w:val'),'single');pr.append(underline)
   if size is not None:
    sz=OxmlElement('w:sz');sz.set(qn('w:val'),str(round(size.pt*2)));pr.append(sz)
   run.append(pr);t=OxmlElement('w:t');t.text=url;run.append(t);h.append(run);p._p.append(h);end=m.start()+len(url)
  if end<len(text):
   run=p.add_run(text[end:]);run.font.size=size

x=json.loads((R/'analysis/report_content.json').read_text());d=doc(x['title'],x['subtitle'])
for i,page in enumerate(x['pages']):
 if i:d.add_page_break()
 else:d.add_paragraph(x['title'],'Title');d.add_paragraph(x['subtitle'],'Subtitle');d.add_paragraph(x['date'])
 for block in page:
  if 'table' in block:table(d,**block['table'])
  else:d.add_paragraph(block['text'],block.get('style','Normal'))
linkify(d);clean(d);out=R/'documents/Bitcoin_IG2_Expansion_Results_v01.docx';d.save(out);print(out)
