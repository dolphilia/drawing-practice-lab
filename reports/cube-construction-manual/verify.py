"""Verify document packaging and that copied worked-example values remain correct."""
from pathlib import Path
import hashlib,json,re,sys
from pypdf import PdfReader
import pdfplumber
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'assets/cube-projection-research'))
from geometry import manual_numeric
pdf=ROOT/'output/pdf/cube-construction-manual.pdf';src=ROOT/'docs/cube-construction-manual.md'
text=src.read_text();cases=json.loads((ROOT/'assets/cube-projection-research/cases.json').read_text())['cases']
for num,cid in enumerate(['D1-2-1','D2-2-1','D3-2-0'],1):
 section=re.search(r'^## .*作例'+str(num)+r'：.*?\n(.*?)(?=^## |\Z)',text,re.S|re.M).group(1)
 rows=re.findall(r'^\| P([0-7]) \| (-?[\d.]+) \| (-?[\d.]+) \|$',section,re.M)
 assert len(rows)==8,(num,rows)
 c=next(c for c in cases if c['id']==cid);_,expected=manual_numeric(c)
 for i,x,y in rows:assert [float(x),float(y)]==expected[int(i)],(cid,i)
for t in re.findall(r'\]\(([^)]+)\)',text):
 if '://' not in t and not t.startswith('#'):assert (src.parent/t).exists(),t
browser=json.loads((HERE/'browser-checks.json').read_text())
assert not browser['overflows'] and not browser['missing']
assert len(browser['images'])==10 and all(i['complete'] and i['width']>0 for i in browser['images'])
r=PdfReader(pdf);assert len(r.pages)==15
assert len(r.outline)>0
with pdfplumber.open(pdf) as p:
 counts=[]
 for i,page in enumerate(p.pages,1):
  assert abs(page.width-595.28)<1 and abs(page.height-841.89)<1
  content=page.extract_text() or '';counts.append(len(content));assert len(content)>300,i
  assert '\ufffd' not in content,i
  for c in page.chars:
   assert -1<=c['x0']<=c['x1']<=page.width+1,(i,c['text'],'x')
   assert -1<=c['top']<=c['bottom']<=page.height+1,(i,c['text'],'y')
inputs=[src,HERE/'build.py',HERE/'print.css',HERE/'print-pdf.mjs',ROOT/'assets/cube-manual-figures/make_figures.py']+sorted((ROOT/'assets/cube-manual-figures').glob('*.svg'))
record={'date':'2026-10-02','pdf':str(pdf.relative_to(ROOT)),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pages':len(r.pages),'format':'A4','images':10,'worked_vertices_checked':24,'page_text_lengths':counts,'checks':['local links exist','all images loaded','no browser horizontal overflow','24 paper coordinate pairs match existing manual_numeric','PDF has outlines','all characters within page','no replacement characters','no near-empty pages'], 'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'visual_review':'Recorded separately for this PDF hash.'}
(HERE/'quality-checks.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'pages':15,'worked_vertices_checked':24,'images':10,'result':'pass'}))
