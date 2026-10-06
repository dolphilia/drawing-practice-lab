"""Original explanatory diagrams. Hypothetical outputs are never participant data."""
from pathlib import Path
import html,math,json,sys,subprocess
HERE=Path(__file__).resolve().parent
INK='#254b5b';TEAL='#187f7b';RED='#b65d36';GRAY='#77929d';BLUE='#e3f0f5';GOLD='#f8ecd2'
def start(h=450):return [f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{h}" viewBox="0 0 1000 {h}"><rect width="1000" height="{h}" fill="white"/><g font-family="Hiragino Kaku Gothic ProN, sans-serif" fill="{INK}">']
def text(s,x,y,t,size=22,color=INK):s.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{html.escape(t)}</text>')
def line(s,a,b,color=INK,width=3,dash=False):s.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="8 6"' if dash else '')+'/>')
def rect(s,x,y,w,h,fill='none',stroke=INK):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')
def circle(s,x,y,r=6,fill=RED):s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>')
def path(s,d,color=INK,width=3,fill='none',dash=False):s.append(f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="{fill}"'+(' stroke-dasharray="8 6"' if dash else '')+'/>')
def save(n,s):
 p=HERE/f'{n}.svg';p.write_text(''.join(s)+'</g></svg>');subprocess.run(['rsvg-convert',str(p),'-o',str(p.with_suffix('.png'))],check=True)
s=start(460)
for k,(title,split,lower) in enumerate([('① 上の高さを決める',False,False),('② 半分、さらに半分',True,False),('③ 同じ一区間を三つ',True,True)]):
 x=65+335*k;text(s,x-35,34,title,23);rect(s,x,75,140,160,BLUE)
 if split:
  for j in range(1,4):line(s,(x,75+j*40),(x+140,75+j*40),TEAL,2,True)
  for j in range(4):text(s,x+153,102+j*40,str(j+1),20,TEAL)
 if lower:
  rect(s,x,235,140,120,GOLD)
  for j in range(1,3):line(s,(x,235+j*40),(x+140,235+j*40),TEAL,2,True)
  for j in range(3):text(s,x+153,262+j*40,str(j+1),20,TEAL)
 text(s,x-20,401,['上が40mmなら','一区間は40÷4=10mm','下は10×3=30mm'][k],21)
text(s,35,446,'説明用の寸法。描画中に定規で正解を作るのではなく、描いた後に比を確かめる。',20,GRAY)
save('m1-steps',s)
s=start(475)
for k,(title,low,col) in enumerate([('目標',120,INK),('仮の描画',136,RED),('次の絵で試す方向',120,TEAL)]):
 x=100+k*330;text(s,x-35,36,title,23);rect(s,x,74,128,160,BLUE);rect(s,x,234,128,low,GOLD,col)
 text(s,x-36,104,'40',20);text(s,x-36,300,'34' if k==1 else '30',20,col)
 if k==1:line(s,(x-15,354),(x+150,354),TEAL,2,True);text(s,x-62,419,'34÷40=0.85',22,RED)
 else:text(s,x-65,419,'30÷40=0.75' if k==0 else '下を短くする',22,col)
text(s,30,464,'中央は意図的に下を長くした模式図。右は修正の狙いであり、人が上達した結果ではない。',18,GRAY)
save('m1-feedback',s)
s=start(380)
rows=[('A','見ながら描く','手本を表示したまま','見えている形を写せるか'),('B','閉じて同じ図を描く','観察後は手本も前の絵も隠す','見た配置を思い出せるか'),('C','別の向きから描く','寸法は見てよい／完成図は隠す','同じ立体を別視点へ組み立てられるか')]
for k,(a,b,c,d) in enumerate(rows):
 y=30+k*115;rect(s,15,y,970,95,'#f0f6f6','#c5d9df');text(s,35,y+38,a,30,TEAL);text(s,100,y+38,b,24);text(s,100,y+73,c,18,GRAY);text(s,475,y+52,d,22)
save('m2-conditions',s)
# Reuse only the known mesh and projection definitions, creating illustration-only views.
sys.path.insert(0,str(HERE.parent/'construction-geometry'))
from generate import mesh,basis,project,cross,sub,dot
model=json.loads((HERE.parent/'construction-geometry/models.json').read_text())['models'][0]
def boxes(s,ox,oy,az=25,el=15,scale=115,shift_lower=0,wire=False):
 vs,fs,_=mesh(model);view={'azimuth_deg':az,'elevation_deg':el};im={'origin_px':[ox,oy],'scale_px_per_unit':scale}
 ps={k:project(p,view,im) for k,p in vs.items()}
 if shift_lower:ps={k:(v[0]+(shift_lower if k.startswith('L') else 0),v[1],v[2]) for k,v in ps.items()}
 for f in sorted(fs,key=lambda f:sum(ps[k][2] for k in f['vertices'])):
  xyz=[vs[k] for k in f['vertices']]
  if dot(cross(sub(xyz[1],xyz[0]),sub(xyz[2],xyz[0])),basis(view)[2])<=1e-9:continue
  coords=' '.join(f'{ps[k][0]},{ps[k][1]}' for k in f['vertices']);fill='none' if wire else (BLUE if f['part']=='U' else GOLD)
  s.append(f'<polygon points="{coords}" fill="{fill}" stroke="{RED if wire else INK}" stroke-width="{2 if wire else 2.5}"'+(' stroke-dasharray="7 5"' if wire else '')+'/>')
s=start(430)
text(s,65,35,'同じ視点：手本',24);text(s,550,35,'同じ視点：仮の再生と照合',24)
boxes(s,230,205,scale=115);boxes(s,740,205,scale=115);boxes(s,740,205,scale=115,shift_lower=27,wire=True)
text(s,75,388,'上下の箱の「中心のずれ」を見る。',22);text(s,540,388,'赤の破線：下の箱が右へずれた仮の例。',20,RED)
text(s,30,423,'二箱は同じ既知モデル。色は部品の区別。人体の胸郭・骨盤の正解形ではない。',19,GRAY)
save('m2-recall',s)
s=start(470)
text(s,75,35,'見本の向き：方位25°・高さ15°',23);text(s,555,35,'別の向き：方位65°・高さ15°',23)
boxes(s,230,222,scale=126);boxes(s,740,222,az=65,scale=126)
text(s,58,413,'寸法・配置・各箱の向きは同じ。',22);text(s,532,413,'見る方向だけを変えた、照合用の図。',22)
text(s,30,456,'説明専用の投影図。このページを見た角度は、今後の「初めて見る角度」の評価には使わない。',18,GRAY)
save('m2-view-change',s)
s=start(410)
for k,(title,detail) in enumerate([('① 外形の線','画面上で物の外側を区切る'),('② 向きを示す補助線','筒の中心の通り道を決める'),('③ 曲面の回り込みの補助線','途中の断面を考える')]):
 x=35+k*330;text(s,x,32,title,22);cx=x+130
 path(s,f'M {cx-75} 95 C {cx-75} 57 {cx+75} 57 {cx+75} 95 L {cx+75} 295 C {cx+75} 333 {cx-75} 333 {cx-75} 295 Z',INK,3,BLUE)
 path(s,f'M {cx-75} 95 C {cx-75} 133 {cx+75} 133 {cx+75} 95',INK,2)
 if k==1:line(s,(cx,58),(cx,335),TEAL,4,True)
 if k==2:
  path(s,f'M {cx-75} 205 C {cx-75} 243 {cx+75} 243 {cx+75} 205',RED,4)
  path(s,f'M {cx-75} 205 C {cx-75} 167 {cx+75} 167 {cx+75} 205',RED,2,dash=True)
 text(s,x,375,detail,19)
text(s,24,406,'②③は形を考えるための線。完成画で全部を残す必要はない。',19,GRAY)
save('m3-line-roles',s)
def body_arm(s,x,y,raised=False,gap=False,details=False):
 # A schematic toy robot, expressly not an anatomical joint diagram.
 pts=[(x,y),(x+110,y),(x+150,y-35),(x+40,y-35)]
 s.append('<polygon points="'+' '.join(f'{a},{b}' for a,b in pts)+'" fill="#f4f8fa" stroke="'+INK+'" stroke-width="3"/>')
 rect(s,x,y,110,145,BLUE)
 s.append(f'<polygon points="{x+110},{y} {x+150},{y-35} {x+150},{y+110} {x+110},{y+145}" fill="#d0e5eb" stroke="{INK}" stroke-width="3"/>')
 j=(x+133,y+45);root=(j[0]+(35 if gap else 0),j[1]);end=(root[0]+80,root[1]+(-70 if raised else 75))
 line(s,root,end,TEAL,17);line(s,root,end,'#b9ddd6',11);circle(s,*root,10,TEAL)
 circle(s,*j,5,RED)
 if gap:line(s,j,root,RED,2,True)
 if details:
  rect(s,x+22,y-107,67,56,'#f4f8fa');circle(s,x+43,y-80,4,INK);circle(s,x+70,y-80,4,INK)
  line(s,(x+52,y-51),(x+52,y-35),INK,8)
  for dx in (25,84):line(s,(x+dx,y+145),(x+dx,y+205),INK,12)
 return j
s=start(425)
for k,(t,gap) in enumerate([('① 付け根が離れた例',True),('② 付け根を側面に置く例',False)]):
 x=100+k*490;text(s,x-65,34,t,24);body_arm(s,x,123,gap=gap)
 text(s,x-65,342,'ここに隙間がある' if gap else '付け根をこの点へ置く',22,RED if gap else TEAL)
text(s,25,397,'今回の設計は「棒が箱の側面に付く」。赤点は設計上の接続位置。人体の肩関節の位置ではない。',18,GRAY)
save('m3-connection',s)
s=start(465)
text(s,40,34,'部分練習で決めたこと',24);text(s,535,34,'別のポーズの小さな作品で使う',24)
body_arm(s,90,157);body_arm(s,610,167,raised=True,details=True)
text(s,38,398,'「腕の付け根は胴体の側面に置く」',22);text(s,515,398,'腕を上げても、付け根の対応を保つ。',22)
text(s,30,454,'同じ設計の玩具ロボットによる説明。右は練習効果の実測結果ではなく、応用先の目標例。',18,GRAY)
save('m4-transfer',s)
