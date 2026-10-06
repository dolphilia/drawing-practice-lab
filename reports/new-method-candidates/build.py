"""Build the edited manual via Pandoc HTML and Chromium, as in ../reml books."""
from pathlib import Path
import os,re,subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
TMP=ROOT/'tmp/pdfs/new-method-candidates';TMP.mkdir(parents=True,exist_ok=True)
source=HERE/'manuscript.md'
body=source.read_text()
def link(m):
 target=m.group(1)
 if '://' in target or target.startswith('#'):return m.group(0)
 p=(source.parent/target).resolve();assert p.exists(),target
 # Retain vector paths in print; Markdown remains broadly previewable as PNG.
 if p.suffix=='.png' and p.with_suffix('.svg').exists():p=p.with_suffix('.svg')
 return ']('+p.as_uri()+')'
body=re.sub(r'\]\(([^)]+)\)',link,body)
(TMP/'manual.md').write_text(body)
subprocess.run([os.environ.get('PANDOC','pandoc'),str(TMP/'manual.md'),'--standalone','--wrap=none','--metadata','pagetitle=新メソッド候補を、目的と作図から理解する','--css',str(HERE/'print.css'),'--output',str(TMP/'manual.html')],check=True)
node=os.environ.get('DRAWING_NODE',str(Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'))
subprocess.run([node,str(HERE/'print-pdf.mjs'),str(TMP/'manual.html'),str(ROOT/'output/pdf/new-method-candidates-explained.pdf'),str(HERE/'browser-checks.json')],check=True)
