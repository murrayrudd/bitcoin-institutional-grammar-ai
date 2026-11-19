from pathlib import Path
import json, re, shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'package'; OUT=ROOT.parent/'outputs/core_knots_round4';OUT.mkdir(parents=True,exist_ok=True)
content=json.loads((P/'report/report_content.json').read_text());pages=content['pages'];sources=content['sources'];source_urls={k:links[0][0] for k,_,links in sources}
doc=Document();sec=doc.sections[0]
sec.page_width=Inches(8.5);sec.page_height=Inches(11);sec.left_margin=sec.right_margin=Inches(.75)
sec.top_margin=Inches(.67);sec.bottom_margin=Inches(.65);sec.footer_distance=Inches(.3)
styles=doc.styles
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Caption']:
 s=styles[name];s.font.name='Arial';s.font.color.rgb=RGBColor(0,0,0)
 if s.element.rPr is not None:
  for col in s.element.rPr.findall(qn('w:color')):
   for attr in ['themeColor','themeTint','themeShade']:col.attrib.pop(qn('w:'+attr),None)
 if s.element.pPr is not None:
  for b in list(s.element.pPr.findall(qn('w:pBdr'))):s.element.pPr.remove(b)
styles['Normal'].font.size=Pt(11);styles['Normal'].paragraph_format.space_after=Pt(7);styles['Normal'].paragraph_format.line_spacing=1.05
styles['Title'].font.size=Pt(21);styles['Title'].font.bold=True;styles['Title'].paragraph_format.space_after=Pt(5)
styles['Subtitle'].font.size=Pt(13);styles['Subtitle'].paragraph_format.space_after=Pt(5)
styles['Heading 1'].font.size=Pt(15);styles['Heading 1'].font.bold=True;styles['Heading 1'].paragraph_format.space_before=Pt(0);styles['Heading 1'].paragraph_format.space_after=Pt(12)
styles['Heading 2'].font.size=Pt(11.5);styles['Heading 2'].font.bold=True;styles['Heading 2'].paragraph_format.space_before=Pt(8);styles['Heading 2'].paragraph_format.space_after=Pt(5)
styles['Caption'].font.size=Pt(9);styles['Caption'].font.italic=False;styles['Caption'].font.bold=False;styles['Caption'].paragraph_format.space_before=Pt(4);styles['Caption'].paragraph_format.space_after=Pt(6)

def link(p,text,url):
 h=OxmlElement('w:hyperlink');h.set(qn('r:id'),p.part.relate_to(url,RT.HYPERLINK,is_external=True));r=OxmlElement('w:r');rp=OxmlElement('w:rPr');c=OxmlElement('w:color');c.set(qn('w:val'),'1F4E79');rp.append(c);r.append(rp);t=OxmlElement('w:t');t.text=text;r.append(t);h.append(r);p._p.append(h)
def txt(p,t):
 for part in re.split(r'(\[R\d+\])',t):
  if re.fullmatch(r'\[R\d+\]',part):link(p,part,source_urls[part[1:-1]])
  else:p.add_run(part)
def paragraph(t,style=None):
 p=doc.add_paragraph(style=style);txt(p,t);p.paragraph_format.widow_control=True
 if p._p.getprevious() is not None and p._p.getprevious().tag==qn('w:tbl'):p.paragraph_format.space_before=Pt(5)
 return p

def add_table(spec):
 t=doc.add_table(rows=1,cols=len(spec['headers']));t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
 borders=OxmlElement('w:tblBorders')
 for tag in ['top','left','bottom','right','insideH','insideV']:
  e=OxmlElement('w:'+tag);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');borders.append(e)
 t._tbl.tblPr.append(borders);mar=OxmlElement('w:tblCellMar')
 for k,v in [('top',85),('bottom',85),('left',95),('right',95)]:
  e=OxmlElement('w:'+k);e.set(qn('w:w'),str(v));e.set(qn('w:type'),'dxa');mar.append(e)
 t._tbl.tblPr.append(mar)
 for i,w in enumerate(spec['widths']):t.columns[i].width=Inches(w)
 for ri,vals in enumerate([spec['headers']]+spec['rows']):
  row=t.rows[0] if ri==0 else t.add_row();trp=row._tr.get_or_add_trPr();trp.append(OxmlElement('w:cantSplit'))
  if ri==0:trp.append(OxmlElement('w:tblHeader'))
  for j,val in enumerate(vals):
   c=row.cells[j];c.width=Inches(spec['widths'][j]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   p=c.paragraphs[0];txt(p,val);p.paragraph_format.space_after=Pt(0);p.paragraph_format.line_spacing=1.02
   for run in p.runs:run.font.name='Arial';run.font.size=Pt(9.5);run.bold=(ri==0)
   for rp in p._p.xpath('.//w:hyperlink/w:r/w:rPr'):
    sz=OxmlElement('w:sz');sz.set(qn('w:val'),'19');rp.append(sz)
   if ri==0:
    sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'E9E9E9');c._tc.get_or_add_tcPr().append(sh)
 return t

for i,pg in enumerate(pages):
 if i:doc.add_page_break()
 doc.add_paragraph(pg['title'],style='Title' if i==0 else 'Heading 1')
 for typ,val in pg['blocks']:
  if typ=='subtitle':doc.add_paragraph(val,style='Subtitle')
  elif typ=='meta':
   p=doc.add_paragraph(val);p.paragraph_format.space_after=Pt(12)
   for r in p.runs:r.font.size=Pt(9)
  elif typ=='p':paragraph(val)
  elif typ=='h':doc.add_paragraph(val,style='Heading 2')
  elif typ=='quote':
   p=paragraph(val);p.paragraph_format.left_indent=Inches(.15);p.paragraph_format.right_indent=Inches(.1)
   for r in p.runs:r.italic=True;r.font.size=Pt(10.5)
  elif typ=='caption':paragraph(val,'Caption')
  elif typ=='table':add_table(val)
  elif typ=='source':
   k,title,links=val;p=doc.add_paragraph();p.paragraph_format.space_after=Pt(6);p.paragraph_format.line_spacing=1.0
   r=p.add_run(k+'  '+title+'. ');r.bold=True;r.font.size=Pt(9.5)
   for j,(target,label) in enumerate(links):
    if j:p.add_run(' · ')
    link(p,label,target)
   for r in p.runs:r.font.size=Pt(9.5)
   for rp in p._p.xpath('.//w:hyperlink/w:r/w:rPr'):
    sz=OxmlElement('w:sz');sz.set(qn('w:val'),'19');rp.append(sz)
footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=footer.add_run();r.font.name='Arial';r.font.size=Pt(9);field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');r._r.addnext(field)
doc.core_properties.title='Bitcoin Core institutional coding source review'
doc.core_properties.subject='Round 4 separate AI source review and evidence reconciliation'
doc.core_properties.author='Murray A. Rudd'
doc.core_properties.keywords='Bitcoin Core, Knots, Institutional Grammar, IG2, governance, corpus analysis'
path=OUT/'Core_Knots_Round4_Source_Review_v01.docx';doc.save(path)
print(path)
