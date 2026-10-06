// Based on ../reml/scripts/books/print-pdf.mjs. Local manual build.
import { createRequire } from "node:module";
import { existsSync, mkdirSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { homedir } from "node:os";
import { pathToFileURL } from "node:url";

const [htmlPath, pdfPath, checkPath] = process.argv.slice(2);
const headerTitle = "新メソッド候補を目的と作図から理解する";
if (!htmlPath || !pdfPath || !checkPath) throw new Error("usage: print-pdf.mjs INPUT.html OUTPUT.pdf CHECKS.json");

const packagePath = process.env.REML_PLAYWRIGHT_PACKAGE ?? join(
  homedir(),
  ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/package.json",
);
const require = createRequire(packagePath);
const { chromium } = require("playwright");

let executable = process.env.REML_CHROMIUM_EXECUTABLE ?? chromium.executablePath();
if (!existsSync(executable) && process.platform === "darwin") {
  const cache = join(homedir(), "Library/Caches/ms-playwright");
  const installs = existsSync(cache)
    ? readdirSync(cache).filter((name) => name.startsWith("chromium-")).sort().reverse()
    : [];
  executable = installs
    .map((name) => join(cache, name, "chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"))
    .find(existsSync) ?? executable;
}
if (!existsSync(executable)) throw new Error("Chromium executable not found");

mkdirSync(dirname(pdfPath), { recursive: true });
const browser = await chromium.launch({
  headless: true,
  timeout: 120_000,
  executablePath: executable,
  args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-gpu"],
});

try {
  const page = await browser.newPage();
  await page.route(/^https?:\/\//, route => route.abort());
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "load", timeout: 120_000 });
  await page.emulateMedia({media:"print"});
  await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(im => im.decode())); });
  await page.evaluate(async () => document.fonts.ready);
  await page.evaluate(() => {
    const identified = [...document.querySelectorAll("[id]")];
    const replacements = new Map(identified.map((element, index) => [element.id, `rpbr-anchor-${index + 1}`]));
    for (const link of document.querySelectorAll('a[href^="#"]')) {
      const target = decodeURIComponent(link.getAttribute("href").slice(1));
      const replacement = replacements.get(target);
      if (replacement) link.setAttribute("href", `#${replacement}`);
    }
    for (const element of identified) element.id = replacements.get(element.id);
  });
  await page.evaluate(() => {
    for (const table of document.querySelectorAll('table')) {
      const n=table.querySelectorAll('thead th').length;
      const head=table.querySelector('thead th')?.textContent.trim();
      let widths=n===2?[28,72]:n===3?[22,39,39]:Array(n).fill(100/n);
      if(head==='今、確かめたいこと')widths=[35,20,45];
      if(head==='候補')widths=[12,40,48];
      table.querySelectorAll('colgroup').forEach(e=>e.remove());
      const cg=document.createElement('colgroup');
      for(const width of widths){const c=document.createElement('col');c.style.width=width+'%';cg.append(c);}
      table.prepend(cg);
    }
  });
  const layout = await page.evaluate(() => {
    const overflows = [...document.querySelectorAll("pre, table, img, svg")]
      .filter((element) => element.scrollWidth > element.clientWidth + 1)
      .map((element) => ({
        tag: element.tagName,
        width: element.clientWidth,
        scrollWidth: element.scrollWidth,
        text: element.textContent?.slice(0, 80) ?? "",
      }));
    const ids=new Set([...document.querySelectorAll('[id]')].map(e=>e.id));
    const missing=[...document.querySelectorAll('a[href^="#"]')].filter(e=>!ids.has(e.getAttribute('href').slice(1))).map(e=>e.getAttribute('href'));
    const images=[...document.images].map(im=>({source:im.src,complete:im.complete,width:im.naturalWidth}));
    return { title: document.title, overflows, missing, images };
  });
  if (layout.overflows.length > 0) throw new Error(`Horizontal overflow: ${JSON.stringify(layout.overflows)}`);
  await page.pdf({
    path: pdfPath,
    format: "A4",
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: `<div style="font-size:7px;color:#687784;width:100%;padding:0 17mm;text-align:right;">${headerTitle}</div>`,
    footerTemplate: '<div style="font-size:7px;color:#687784;width:100%;padding:0 17mm;text-align:center;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    margin: { top: "22mm", right: "17mm", bottom: "22mm", left: "17mm" },
    outline: true,
    tagged: true,
    timeout: 120_000,
  });
  writeFileSync(checkPath, JSON.stringify(layout,null,2)+"\n");
  process.stdout.write(`${JSON.stringify({ ...layout, pdfPath })}\n`);
} finally {
  await browser.close();
}
