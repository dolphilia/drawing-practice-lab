"""Check the explanatory booklet's packaging, arithmetic and page boundaries."""
from pathlib import Path
from decimal import Decimal
import hashlib,json,re,logging
from pypdf import PdfReader
import pdfplumber

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
pdf=ROOT/'output/pdf/new-method-candidates-explained.pdf'
src=HERE/'manuscript.md'
body=src.read_text()
for target in re.findall(r'\]\(([^)]+)\)',body):
    if '://' not in target and not target.startswith('#'):
        assert (src.parent/target).exists(),target
browser=json.loads((HERE/'browser-checks.json').read_text())
assert not browser['overflows'] and not browser['missing']
assert len(browser['images'])==8
assert all(i['complete'] and i['width']>0 for i in browser['images'])
assert Decimal(34)/Decimal(40)-Decimal('.75')==Decimal('.10')
assert Decimal(44)*Decimal('.75')==33
model=json.loads((ROOT/'assets/construction-geometry/models.json').read_text())['models'][0]
assert model['id']=='two-boxes'
parts={p['id']:p for p in model['parts']}
assert parts['U']['size']==[1,1,.8] and parts['U']['center']==[.15,.6,0] and parts['U']['yaw_deg']==20
assert parts['L']['size']==[1.3,.7,.65] and parts['L']['center']==[0,-.7,0] and parts['L']['yaw_deg']==-15
r=PdfReader(pdf)
assert len(r.pages)==11,len(r.pages)
assert len(r.outline)>0
counts=[]
warnings=[]
class WarningCapture(logging.Handler):
    def emit(self,record):
        warnings.append(record.getMessage())
logger=logging.getLogger('pdfminer')
logger.addHandler(WarningCapture());logger.propagate=False
with pdfplumber.open(pdf) as document:
    for n,p in enumerate(document.pages,1):
        assert abs(p.width-595.28)<1 and abs(p.height-841.89)<1
        text=p.extract_text() or ''
        counts.append(len(text))
        assert len(text)>300 and '\ufffd' not in text,n
        for c in p.chars:
            assert -1<=c['x0']<=c['x1']<=p.width+1,(n,c['text'],'x')
            assert -1<=c['top']<=c['bottom']<=p.height+1,(n,c['text'],'y')
inputs=[src,HERE/'build.py',HERE/'print.css',HERE/'print-pdf.mjs',ROOT/'assets/new-method-candidates/make_figures.py',ROOT/'assets/construction-geometry/models.json',ROOT/'assets/construction-geometry/generate.py']+sorted((ROOT/'assets/new-method-candidates').glob('*.svg'))
record={'date':'2026-10-03','pdf':str(pdf.relative_to(ROOT)),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pages':len(r.pages),'format':'A4','figures':8,'page_text_lengths':counts,'checks':['local links exist','all 8 images loaded','no browser horizontal overflow','worked M1 arithmetic correct','two-box parameters match existing model','PDF has outlines','all character bounds within pages','no replacement characters','no near-empty pages'],'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'parser_warning_count':len(warnings),'parser_warning_examples':list(dict.fromkeys(warnings))[:3],'scope':'Document packaging and specified arithmetic/model checks only. Visual review is recorded separately; no participant or efficacy validation.'}
(HERE/'quality-checks.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'result':'pass','pages':len(r.pages),'figures':8,'parser_warnings':len(warnings)}))
