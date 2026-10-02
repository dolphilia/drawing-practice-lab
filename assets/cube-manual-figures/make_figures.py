"""Original explanatory vector diagrams; schematic unless marked numerical."""
from pathlib import Path
import math,html,subprocess
HERE=Path(__file__).resolve().parent
INK='#23465a';TEAL='#178178';ORANGE='#bf652e';GRAY='#72858d'
def start(w,h):return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="white"/><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8" fill="{TEAL}"/></marker></defs><g font-family="Hiragino Kaku Gothic ProN, sans-serif" fill="{INK}">']
def line(s,a,b,color=INK,width=2,dash=False,arrow=False):s.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="7 5"' if dash else '')+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
def text(s,x,y,t,size=19,color=INK):s.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{html.escape(t)}</text>')
def dot(s,p,color=ORANGE):s.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="5" fill="{color}"/>')
def save(name,s):
 (HERE/f'{name}.svg').write_text(''.join(s)+'</g></svg>');subprocess.run(['rsvg-convert',str(HERE/f'{name}.svg'),'-o',str(HERE/f'{name}.png')],check=True)
s=start(960,255)
for i,(a,b) in enumerate([('① 入力','位置・向き・大きさ'),('② 半辺','3本の矢印を回す'),('③ 頂点','符号表で8点を作る'),('④ 投影','奥行きZで割る'),('⑤ 描画','紙に点を打ち結ぶ')]):
 x=12+i*191;s.append(f'<rect x="{x}" y="55" width="173" height="110" rx="8" fill="#eef5f5" stroke="#b2d2d1"/>');text(s,x+14,91,a,22);text(s,x+10,132,b,16)
 if i<4:line(s,(x+174,108),(x+189,108),TEAL,2,arrow=True)
text(s,20,217,'立体の座標 (X, Y, Z) を作る                  →                  紙の座標 (u, v) に変える',20)
save('workflow',s)
s=start(960,395)
text(s,20,32,'上から見た断面：左右Xと奥行きZの関係',23)
O=(100,285);T=(780,90);Q=(355,211.875)
line(s,(75,285),(885,285),TEAL,2,arrow=True);text(s,865,321,'前 Z')
line(s,(100,312),(100,66),TEAL,2,arrow=True);text(s,22,68,'右 X')
line(s,(355,75),(355,315),ORANGE,4);text(s,282,60,'画面 Z = f',20,ORANGE)
line(s,O,T,INK,3);line(s,T,(780,285),GRAY,2,dash=True);line(s,Q,(355,285),TEAL,4)
for p in [O,T,Q]:dot(s,p)
text(s,51,351,'視点 O');text(s,672,69,'立体の点 (X, Z)');text(s,369,176,'紙に写る点');text(s,368,254,'u');text(s,793,187,'X')
text(s,195,318,'f');text(s,445,353,'Z：視点から点までの前方向の距離')
text(s,420,382,'同じ視線上なので u / f = X / Z',21)
save('projection-plane',s)
s=start(960,435)
C=(300,235);R=155;P=(C[0]+R*math.cos(math.pi/6),C[1]-R*.5)
s.append(f'<circle cx="{C[0]}" cy="{C[1]}" r="{R}" fill="none" stroke="#a4c5ca" stroke-width="2"/>')
line(s,(95,235),(495,235),TEAL,2,arrow=True);line(s,(300,420),(300,42),TEAL,2,arrow=True)
line(s,C,P,INK,3);line(s,P,(P[0],235),ORANGE,3);line(s,P,(300,P[1]),GRAY,2,dash=True);dot(s,P);dot(s,C)
text(s,496,242,'横');text(s,309,43,'縦');text(s,313,219,'30°',18);text(s,348,272,'横 約69.5mm',18);text(s,443,192,'縦40mm',18)
text(s,535,102,'半径80mmの円',24);text(s,535,151,'横を80で割る → c',22);text(s,535,188,'縦を80で割る → s',22)
text(s,535,245,'c = 69.5 ÷ 80 = 0.86875',19);text(s,535,281,'s = 40 ÷ 80 = 0.5',19)
text(s,535,342,'左・下は負の値として読む。',19);text(s,535,375,'図は模式図。長さは記載値を使う。',17,GRAY)
save('angle-circle',s)
s=start(960,430)
# Axonometric schematic of cube centered on C. Half vectors point to face centres.
C=(265,205);hs=[(95,30),(0,-90),(-65,50)]
def pos(signs):return (C[0]+sum(t*h[0] for t,h in zip(signs,hs)),C[1]+sum(t*h[1] for t,h in zip(signs,hs)))
from itertools import product
signs=list(product([-1,1],repeat=3))
for i,a in enumerate(signs):
 for j,b in enumerate(signs):
  if j>i and sum(x!=y for x,y in zip(a,b))==1:line(s,pos(a),pos(b),'#bdcdd2',2)
for h,label,offset in zip(hs,['h1','h2','h3'],[(5,15),(12,0),(-33,8)]):
 p=(C[0]+h[0],C[1]+h[1]);line(s,C,p,TEAL,4,arrow=True);text(s,p[0]+offset[0],p[1]+offset[1],label,23)
dot(s,C);text(s,C[0]-29,C[1]-12,'C',23)
current=C
for h in hs:
 nxt=(current[0]+h[0],current[1]+h[1]);line(s,current,nxt,ORANGE,3,dash=True);current=nxt
dot(s,current);text(s,current[0]+14,current[1]-7,'P7',23,ORANGE)
text(s,525,70,'半辺は「半分の辺長の矢印」',23);text(s,525,121,'例：一辺60mmなら、各矢印は30mm。',19)
text(s,525,177,'3本とも、出発点は中心C。',20);text(s,525,218,'矢印1本の先は面の中心です。',20)
text(s,525,281,'P7 = C + h1 + h2 + h3',23,ORANGE);text(s,525,323,'矢印を平行移動して順につなぐと、',19);text(s,525,355,'3本ぶん進んだ先が立方体の頂点。',19)
text(s,40,411,'緑：中心からの3本の半辺　／　橙の破線：P7まで足し合わせる経路（模式図）',17)
save('half-edges',s)
s=start(960,390)
for x,y,t in [(45,32,'① 元の2成分を書く'),(345,32,'② 新しい値を両方計算'),(678,32,'③ 両方を置き換える')]:text(s,x,y,t,21)
for x in (35,342,666):s.append(f'<rect x="{x}" y="60" width="264" height="241" rx="8" fill="#f0f6f6"/>')
text(s,55,112,'h1 = (30, 0, 0)',24);text(s,55,163,'元X = 30',23);text(s,55,206,'元Z = 0',23);text(s,55,260,'Y = 0 は変えない',19)
text(s,359,110,'新X = cα × 30 + sα × 0',18);text(s,359,153,'       = 26.0625',20);text(s,359,214,'新Z = −sα × 30 + cα × 0',18);text(s,359,257,'       = −15',20)
text(s,686,118,'h1 ≈',23);text(s,686,161,'(26.062, 0, −15)',22);text(s,686,230,'次のβの回転では',19);text(s,686,263,'この結果を元にする。',19)
line(s,(302,182),(334,182),TEAL,2,arrow=True);line(s,(610,182),(656,182),TEAL,2,arrow=True)
text(s,36,347,'α = 30°、cα = 0.86875、sα = 0.5 の例。途中の26.0625を新Zの式へ入れない。',20)
save('rotation-update',s)
s=start(960,385)
O=(160,112);sx=8;sy=3.3;P=(O[0]+6.7*sx,O[1]+60*sy)
for x in range(64,465,40):line(s,(x,45),(x,342),'#e5edef',1)
for y in range(46,343,33):line(s,(64,y),(464,y),'#e5edef',1)
line(s,(70,112),(470,112),TEAL,2,arrow=True);line(s,(160,341),(160,37),TEAL,2,arrow=True)
line(s,O,(P[0],O[1]),ORANGE,4,arrow=False);line(s,(P[0],O[1]),P,ORANGE,3,dash=True);dot(s,O);dot(s,P)
text(s,120,97,'原点',18);text(s,471,119,'右 u');text(s,171,38,'上 v');text(s,204,96,'6.7mm',18,ORANGE);text(s,227,222,'下へ60.0mm',18,ORANGE);text(s,227,318,'P0',23)
text(s,540,81,'(u, v) = (6.7, −60.0)mm',24);text(s,540,140,'① 原点から右へ6.7mm。',21);text(s,540,190,'② そこから下へ60.0mm。',21);text(s,540,240,'③ 交点にP0と記す。',21)
text(s,540,308,'vが負なら下。Zは紙へ直接写さない。',18);text(s,540,346,'見やすさのため横・縦の縮尺は異なる。',17,GRAY)
save('paper-point',s)
# Enlarge the fixed research examples by cropping empty margins, preserving all vertices.
import xml.etree.ElementTree as ET
research=HERE.parent/'cube-projection-research'
for num,cid,box in [(1,'D1-2-1','460 260 385 350'),(2,'D2-2-1','440 250 350 380'),(3,'D3-2-0','300 175 400 385')]:
 root=ET.fromstring((research/f'{cid}.svg').read_text())
 root.set('viewBox',box);root.set('width',box.split()[2]);root.set('height',box.split()[3])
 for e in root:
  if e.tag.endswith('rect'):
   for k,v in zip(('x','y','width','height'),box.split()):e.set(k,v)
 for e in list(root):
  if e.tag.endswith('text') and float(e.get('y','0')) in (40,635,670):root.remove(e)
 ET.register_namespace('','http://www.w3.org/2000/svg')
 out=HERE/f'example-{num}.svg';ET.ElementTree(root).write(out,encoding='unicode')
 subprocess.run(['rsvg-convert',str(out),'-o',str(out.with_suffix('.png'))],check=True)
s=start(960,430)
text(s,25,32,'P0 = (6, −54, 90)、f = 100、補助縮尺 s = 1/2 の例',22)
for panel,coef,label in [(0,3,'横位置uを求める'),(1,-27,'縦位置vを求める')]:
 ox=65+panel*480;oy=255 if panel==0 else 155;scale=25 if panel==0 else 5
 def pt(z,t):return (ox+z*5,oy-t*scale)
 text(s,ox,79,label,22)
 line(s,pt(0,0),pt(68,0),GRAY,2);text(s,ox+341,oy+6,'Z',19)
 line(s,pt(50,4 if panel==0 else 8),pt(50,-1.3 if panel==0 else -33),ORANGE,3)
 t=pt(45,coef);q=pt(50,coef*50/45)
 line(s,pt(0,0),q,TEAL,3)
 for p,l,dx,dy in [(pt(0,0),'O',-25,20),(t,'端点',-44 if panel==0 else -20,-12 if panel==0 else -35),(q,'交点',10,9)]:dot(s,p);text(s,p[0]+dx,p[1]+dy,l,18)
 text(s,ox+206,oy+37,'45',18);text(s,ox+255,110,'画面50',18,ORANGE)
 reading='3.333…' if panel==0 else '−30'
 result='u ≈ 6.667mm' if panel==0 else 'v = −60mm'
 text(s,ox,357,f'交点の読み {reading} を 1/2 で割る',18);text(s,ox,389,result,22)
text(s,25,423,'説明用の模式図。左右の図の縦方向は別の表示倍率です。実際は各補助図内で全値を同率に縮めます。',16,GRAY)
save('ray-p0',s)
