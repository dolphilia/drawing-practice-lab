const fs=require('node:fs'),path=require('node:path');
const sharp=require(process.argv[2] || 'sharp');
(async()=>{
 for(const name of fs.readdirSync(__dirname).filter(x=>x.endsWith('.svg'))) {
  await sharp(path.join(__dirname,name)).png().toFile(path.join(__dirname,name.replace('.svg','.png')));
 }
 console.log('Rendered 2 operation PNGs.');
})().catch(e=>{console.error(e);process.exitCode=1;});
