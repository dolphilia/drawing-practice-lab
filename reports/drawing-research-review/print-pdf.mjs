// Adapted workflow from ../reml/scripts/books/print-pdf.mjs; local report only.
import { createRequire } from 'node:module';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {existsSync,mkdirSync,readdirSync,writeFileSync} from 'node:fs';
import {dirname,join} from 'node:path';
import {homedir} from 'node:os';
import {pathToFileURL} from 'node:url';
const [htmlPath,pdfPath,checkPath]=process.argv.slice(2);
const require=createRequire(join(homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/package.json'));
const {chromium}=require('playwright');
let executable=process.env.DRAWING_CHROMIUM_EXECUTABLE ?? chromium.executablePath();
if(!existsSync(executable)){
 const cache=join(homedir(),'Library/Caches/ms-playwright');
 executable=readdirSync(cache).filter(n=>n.startsWith('chromium-')).sort().reverse()
 .map(n=>join(cache,n,'chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing')).find(existsSync);
}
if(!executable)throw new Error('Chromium not found');
mkdirSync(dirname(pdfPath),{recursive:true});
const browser=await chromium.launch({headless:true,executablePath:executable,args:['--no-sandbox','--disable-setuid-sandbox','--disable-gpu']});
try{
 const page=await browser.newPage();
 await page.route(/^https?:\/\//,route=>route.abort());
 await page.goto(pathToFileURL(htmlPath).href,{waitUntil:'load'});
 await page.emulateMedia({media:'print'});
 await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(im=>im.decode()));});
 await page.evaluate(()=>{
  for(const table of document.querySelectorAll('table')) {
    const heads=[...table.querySelectorAll('thead th')].map(e=>e.textContent.trim());
    let widths=heads.length===2?[31,69]:heads.length===3?[25,35,40]:[25,25,25,25];
    if(heads[0]==='ID')widths=[7,26,42,25];
    if(heads[0]==='候補'&&heads.length===4)widths=[30,22,33,15];
    if(heads[0]==='作業')widths=[31,39,30];
    if(heads[0]==='作家')widths=[16,43,41];
    if(heads[0]==='研究')widths=[22,38,40];
    if(heads[0]==='読みたいもの')widths=[29,71];
    table.querySelectorAll('colgroup').forEach(e=>e.remove());
    const colgroup=document.createElement('colgroup');
    for(const w of widths){const c=document.createElement('col');c.style.width=w+'%';colgroup.append(c);}
    table.prepend(colgroup);
  }
 });
 const check=await page.evaluate(()=>{
  const overflows=[...document.querySelectorAll('table,pre,img,svg')].filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>({tag:e.tagName,text:e.textContent.slice(0,70)}));
  const ids=new Set([...document.querySelectorAll('[id]')].map(e=>e.id));
  const missing=[...document.querySelectorAll('a[href^="#"]')].map(e=>e.getAttribute('href').slice(1)).filter(id=>!ids.has(decodeURIComponent(id)));
  return {overflows,missing,images:[...document.images].map(im=>({complete:im.complete,width:im.naturalWidth})),title:document.title};
 });
 if(check.overflows.length||check.missing.length)throw new Error(JSON.stringify(check));
 const options={path:pdfPath,format:'A4',printBackground:true,preferCSSPageSize:true,displayHeaderFooter:true,
  headerTemplate:'<div style="font-size:7px;color:#687784;width:100%;padding:0 17mm;text-align:right;">描く力を育てる練習の設計</div>',
  footerTemplate:'<div style="font-size:8px;color:#687784;width:100%;padding:0 17mm;text-align:center;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
  margin:{top:'22mm',right:'17mm',bottom:'22mm',left:'17mm'},outline:true,tagged:true};
 await page.pdf(options);
 const py=process.env.DRAWING_PYTHON ?? join(homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3');
 const script=join(dirname(fileURLToPath(import.meta.url)),'page-map.py');
 const mapPages=()=>{const r=spawnSync(py,[script,pdfPath],{encoding:'utf8'});if(r.status!==0)throw new Error(r.stderr);return JSON.parse(r.stdout);};
 const first=mapPages();
 await page.evaluate(map=>{
   for(const e of document.querySelectorAll('[data-page-for]')) {
     const target=e.dataset.pageFor;
     if(!map[target])throw new Error('Page missing '+target);
     e.textContent=map[target];
   }
 },first.destinations);
 await page.pdf(options);
 const second=mapPages();
 if(JSON.stringify(first)!==JSON.stringify(second))throw new Error('TOC page map changed');
 check.pageMap=second;
 writeFileSync(checkPath,JSON.stringify(check,null,2)+'\n');
 console.log(JSON.stringify({pdfPath,...check}));
}finally{await browser.close();}
