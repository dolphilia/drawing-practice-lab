"""Markdown -> Pandoc HTML -> Playwright Chromium, following ../reml books.
Source stays in this directory; PDF is published under output/pdf.
"""
from pathlib import Path
import json,re,subprocess,sys,html,os


HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
TMP=ROOT/'tmp/pdfs/drawing-research-review'
OUTPUT=ROOT/'output/pdf/drawing-practice-research-review.pdf'
NODE=os.environ.get('DRAWING_NODE','/Users/dolphilia/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node')

KINDS={'meta-analysis':'メタ分析','review':'レビュー・論評','controlled-study':'条件・群比較','observational-study':'観察研究','methodology':'測定・方法論','practitioner-method':'実践教材','anecdote':'経験談・取材'}
LEVELS={'full-text-sections':'本文の指定節','abstract':'要旨・書誌中心','indexed-excerpts':'検索抽出','official-description':'公式紹介・目次等'}


def main():
    TMP.mkdir(parents=True,exist_ok=True)
    notes=[]
    # Preserve this report's historical scope when later research adds notes.
    manifest=json.loads((HERE/'sources.json').read_text())
    for entry in manifest['references']:
        file=ROOT/entry['path']
        front=file.read_text().split('---',2)[1]
        data={}
        for key in ['title','author','published','source','evidence_kind','verification']:
            match=re.search(r'^'+key+r':\s*(.+)$',front,re.M)
            if match: data[key]=match.group(1).strip().strip('\"\'')
        data['path']=str(file.relative_to(ROOT));data['slug']=file.stem
        notes.append(data)
    notes.sort(key=lambda n:(list(KINDS).index(n['evidence_kind']),n['slug']))
    refs={n['slug']:f'R{i:02d}' for i,n in enumerate(notes,1)}
    original=(HERE/'manuscript.md').read_text()
    cited=set()
    def citation(match):
        slug=match.group(1)
        if slug not in refs:raise ValueError('Unknown citation '+slug)
        cited.add(slug);rid=refs[slug]
        return f'<a class="ref-cite" href="#{rid.lower()}">［{rid}］</a>'
    body=re.sub(r'\[([a-z][a-z0-9-]+)\](?!\()',citation,original)
    bib=[]
    for note in notes:
        rid=refs[note['slug']];e=lambda v:html.escape(str(v))
        source=note.get('source')
        if not isinstance(source,str) or not source.startswith(('https://','http://')):raise ValueError('Bad source '+note['slug'])
        title=note['title'];author=note.get('author','著者は資料ノートを参照');year=note.get('published','刊年未確認')
        if year in {'null','None',''}: year='刊年未確認'
        if author in {'null','None',''}: author='著者は資料ノートを参照'
        bib.append(f'''<div class="reference" id="{rid.lower()}"><p class="ref-title"><strong>{rid}　{e(title)}</strong></p>
<p>{e(author)} ／ {e(year)} · {e(KINDS[note['evidence_kind']])}</p>
<p class="ref-note">確認範囲：{e(LEVELS[note['verification']])}。<a href="{e(source)}">原典・公開先</a></p>
<p class="ref-path">{e(note['path'])}</p></div>''')
    body=body.replace('<!-- REFERENCES -->','\n'.join(bib))
    entries=re.findall(r'^# (.+) \{#([^}]+)\}$',body,re.M)
    toc='<nav id="contents"><h2>目次</h2><p class="intro">最初に結論と候補を読み、必要な箇所から根拠・検証へ戻れる構成です。</p><ul>'
    toc+=''.join(f'<li><a href="#{anchor}"><span>{html.escape(title)}</span><span class="page" data-page-for="{anchor}">—</span></a></li>' for title,anchor in entries)
    toc+='</ul><p class="intro">実用的な結論は第2・6・8章へ。根拠を詳しく読むなら第3～5章、自動検査の意味は第7章、開発の順序は第9章へ進んでください。</p></nav>'
    body=body.replace('<!-- TOC -->',toc)
    # Use absolute local images so the HTML location never changes resolution.
    body=re.sub(r'src="(\.\./[^\"]+)"',lambda m:'src="'+(HERE/m.group(1)).resolve().as_uri()+'"',body)
    md=TMP/'compiled.md';md.write_text(body)
    out=TMP/'report.html'
    subprocess.run([os.environ.get('PANDOC','pandoc'),str(md),'--standalone','--wrap=none','--css',str(HERE/'print.css'),'--output',str(out)],check=True)
    (HERE/'sources.json').write_text(json.dumps({'date':'2026-10-02','count':len(notes),'body_cited_count':len(cited),'references':[{**n,'id':refs[n['slug']]} for n in notes]},ensure_ascii=False,indent=2,default=str)+'\n')
    subprocess.run([NODE,str(HERE/'print-pdf.mjs'),str(out),str(OUTPUT),str(HERE/'browser-checks.json')],check=True)
    print(json.dumps({'pdf':str(OUTPUT),'source_notes':len(notes),'body_cited':len(cited)},ensure_ascii=False))


if __name__=='__main__':main()
