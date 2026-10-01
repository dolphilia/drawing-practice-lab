// Synthetic fixtures only. No browser automation or participant observations.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const base=__dirname+'/';
const {measureRatio}=require(base+'measurement.js');
let v=measureRatio([[320,100],[480,100],[320,300],[480,300],[320,450],[480,450]]);
assert.equal(v.ratio,.75);assert.equal(v.absolute_error,0);
assert.equal(measureRatio([[0,0],[1,0],[0,100],[1,100],[0,180],[1,180]]).absolute_error,Math.abs(.8-.75));
assert.throws(()=>measureRatio([]));assert.throws(()=>measureRatio(Array(6).fill([0,0])));
assert.throws(()=>measureRatio([[0,NaN],...Array(5).fill([0,1])]));
let records=JSON.parse(fs.readFileSync(base+'stimuli.json'));
assert.equal(records.length,12);
for(let r of records){assert.equal(r.lower_height/r.upper_height,.75);assert(r.x>=0&&r.x+r.width<=800&&r.y>=0&&r.y+r.upper_height+r.lower_height<=600);let svg=fs.readFileSync(base+r.id+'.svg','utf8');assert(svg.includes(`M${r.x} ${r.y}`));assert(svg.includes(`V${r.y+r.upper_height+r.lower_height}`));}
function harness(file){let els={},downloads=[],alerts=[],blobs=[],timer,now=0;
function el(id){return els[id]??=( {value:({trial:'fixture-01',target:'standard',round:'1',missing:'',note:''})[id]??'',disabled:false,listeners:{},addEventListener(k,f){this.listeners[k]=f},getBoundingClientRect(){return {left:0,top:0,width:800,height:600}},setPointerCapture(){},getContext(){return {fillRect(){},stroke(){},moveTo(){},lineTo(){},beginPath(){},clearRect(){},drawImage(){},arc(){},fill(){},fillText(){}}},toDataURL(){return 'data:image/png;fixture'}} );}
let c={document:{getElementById:el,createElement(){let a={click(){downloads.push({name:a.download,href:a.href})}};return a}},URL:{createObjectURL(b){blobs.push(b);return 'fixture:'+blobs.length},revokeObjectURL(){}},Blob,Image:class{set src(x){this.naturalWidth=800;this.naturalHeight=600;this.onload()}},Date:{now:()=>now},setInterval(f){timer=f},setTimeout(f){f()},alert(t){alerts.push(t)},confirm:()=>true,measureRatio};
vm.createContext(c);let html=fs.readFileSync(base+file,'utf8');for(let m of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g))new vm.Script(m[1]).runInContext(c);
return {els,downloads,alerts,blobs,tick(n){now=n;timer()},el};}
let d=harness('draw.html');d.el('start').onclick();assert(d.el('clear').disabled);d.el('save').onclick();assert.equal(d.downloads.length,0);d.tick(240001);assert(!d.el('clear').disabled);d.el('save').onclick();assert.equal(d.downloads[0].name,'fixture-01.png');d.el('clear').onclick();assert(!d.el('start').disabled);
let s=harness('score.html');s.el('file').onchange({target:{files:[{name:'fixture.png'}]}});for(let [x,y] of [[320,100],[480,100],[320,300],[480,300],[320,450],[480,450]])s.el('image').onclick({clientX:x,clientY:y});s.el('export').onclick();assert.equal(s.downloads[0].name,'fixture-rating1.csv');
(async()=>{let csv=await s.blobs[1].text();assert(csv.includes('"0.75"'));assert(csv.split('\n').length===3);s.el('missing').value='missing-edge';s.el('export').onclick();let miss=await s.blobs[2].text();assert(miss.includes('"missing-edge"'));s.el('file').onchange({target:{files:[{name:'fixture2.png'}]}});assert.equal(s.el('missing').value,'');console.log('PASS: 12 SVGs, ratio/boundary/error cases, timer/save state, endpoint CSV and missing/reset (synthetic DOM only)');})().catch(e=>{console.error(e);process.exit(1)});
