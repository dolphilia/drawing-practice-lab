"""Check final PDF text, links, page size and content inventory; not a layout substitute."""
from pathlib import Path
import hashlib,json,re,unicodedata
from pypdf import PdfReader
import pdfplumber

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
PDF=ROOT/'output/pdf/drawing-practice-research-review.pdf';reader=PdfReader(PDF)
text='\n'.join(unicodedata.normalize('NFKC',p.extract_text()) for p in reader.pages)
compact=re.sub(r'\s+','',text)
assert len(reader.pages)>15
assert all(abs(float(p.mediabox.width)-595)<2 and abs(float(p.mediabox.height)-842)<2 for p in reader.pages)
for word in ['新メソッド','人による確認','310分','54画像回','H1','H8','M1','M4','未実施','刊年未確認']:
    assert word in compact,word
assert 'null' not in compact.lower()
assert '\ufffd' not in text
for i in range(1,68):assert f'R{i:02d}' in compact
for p in reader.pages:assert p.extract_text().strip()
missing=[];external=0;internal=0
for p in reader.pages:
    for ann in p.get('/Annots',[]):
        a=ann.get_object();action=a.get('/A',{})
        if action.get('/S')=='/URI':
            assert str(action['/URI']).startswith(('https://','http://'));external+=1
        dest=a.get('/Dest',action.get('/D'))
        if isinstance(dest,str):
            internal+=1
            if dest not in reader.named_destinations:missing.append(dest)
assert not missing,missing
bounds=[]
with pdfplumber.open(PDF) as doc:
    for i,page in enumerate(doc.pages,1):
        for c in page.chars:
            if c['x0']<-.5 or c['x1']>page.width+.5 or c['top']<-.5 or c['bottom']>page.height+.5:
                bounds.append({'page':i,'text':c['text']})
assert not bounds,bounds[:10]
sources=json.loads((HERE/'sources.json').read_text());assert sources['count']==67
body=(HERE/'manuscript.md').read_text()
assert len(re.findall(r'^\| H[1-8] \|',body,re.M))==8
assert len(re.findall(r'^## M[1-4]　',body,re.M))==4
assert 160+108+40+2==310 and 27*2==54 and 40+27==67
browser=json.loads((HERE/'browser-checks.json').read_text())
assert not browser['overflows'] and not browser['missing']
assert browser['pageMap']['pages']==len(reader.pages)
report={'date':'2026-10-02','pdf':str(PDF.relative_to(ROOT)),'pages':len(reader.pages),'sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),
        'source_notes':67,'body_cited_notes':sources['body_cited_count'],'method_candidates':4,'human_check_items':8,
        'external_links':external,'internal_links':internal,'missing_pdf_destinations':missing,'out_of_page_characters':bounds,
        'text_and_structure':'pass','toc_page_mapping':'pass','browser_layout':browser,
        'visual_review':'Record separately after rendering this exact PDF.'}
visual_path=HERE/'visual-review.json'
if visual_path.exists():
    visual=json.loads(visual_path.read_text())
    if visual.get('sha256')==report['sha256']:report['visual_review']=visual
(HERE/'quality-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='browser_layout'},ensure_ascii=False))
