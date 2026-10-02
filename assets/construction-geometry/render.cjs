// Usage: node render.cjs [sharp-module-path]. Default resolves an installed sharp.
const fs = require('node:fs');
const path = require('node:path');
const sharp = require(process.argv[2] || 'sharp');
async function main() {
  const root = __dirname, dir = path.join(root, 'answers');
  const files = fs.readdirSync(dir).filter(x=>x.endsWith('.svg')).sort();
  for (const file of files) await sharp(path.join(dir,file)).png().toFile(path.join(dir,file.replace('.svg','.png')));
  const tiles = await Promise.all(files.map(async(file,i)=>({
    input:await sharp(path.join(dir,file.replace('.svg','.png'))).resize(400,400).toBuffer(),
    left:(i%4)*400,top:Math.floor(i/4)*400
  })));
  await sharp({create:{width:1600,height:1200,channels:3,background:'#fff'}}).composite(tiles).png().toFile(path.join(root,'contact-sheet.png'));
  console.log('Rendered 12 PNGs and contact sheet.');
}
main().catch(e=>{console.error(e);process.exitCode=1;});
