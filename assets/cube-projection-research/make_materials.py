"""Original SVG diagrams and worked/blank Markdown sheets from fixed inputs."""
from pathlib import Path
import json, html, math
from geometry import *

HERE=Path(__file__).resolve().parent
FONT='sans-serif'


def svg_start(title,w=1000,h=700):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
            '<rect width="100%" height="100%" fill="#ffffff"/>',
            f'<text x="35" y="40" font-family="{FONT}" font-size="24" fill="#163c50">{html.escape(title)}</text>']


def line(parts,a,b,color='#276b85',width=2,dash=''):
    parts.append(f'<line x1="{a[0]:.5f}" y1="{a[1]:.5f}" x2="{b[0]:.5f}" y2="{b[1]:.5f}" stroke="{color}" stroke-width="{width}" stroke-dasharray="{dash}"/>')


def label(parts,p,text,size=16):
    parts.append(f'<text x="{p[0]:.3f}" y="{p[1]:.3f}" font-family="{FONT}" font-size="{size}" fill="#203d4d">{html.escape(text)}</text>')


def save(parts,name):
    (HERE/name).write_text('\n'.join(parts+['</svg>'])+'\n')


def cube_figure(c,title,name):
    uv=project(camera_vertices(c),c);parts=svg_start(title)
    # All illustrations use 4 pixels per mm, the same origin and no shape fitting.
    pt=lambda p:[500+4*p[0],320-4*p[1]]
    for x in range(-90,91,10):line(parts,pt([x,-65]),pt([x,65]),'#e7edf0',1)
    for y in range(-60,61,10):line(parts,pt([-90,y]),pt([90,y]),'#e7edf0',1)
    line(parts,pt([-90,0]),pt([90,0]),'#9aabb2',1)
    line(parts,pt([0,-65]),pt([0,65]),'#9aabb2',1)
    h=axes(c); visible=[]
    for axis in range(3):
        for side in (-1,1):
            normal=mul(h[axis],side*2/c['edge_mm'])
            center=add(c['center_camera_mm'],mul(h[axis],side))
            if dot(normal,center)<-1e-9:
                visible.append({i for i,s in enumerate(SIGNS) if s[axis]==side})
    for i,j in EDGES:
        shown=any(i in face and j in face for face in visible)
        line(parts,pt(uv[i]),pt(uv[j]),'#1d6079' if shown else '#8e9ca2',3 if shown else 1.5,'' if shown else '7 5')
    boxes=[]
    for i,p in enumerate(uv):
        xy=pt(p);parts.append(f'<circle cx="{xy[0]}" cy="{xy[1]}" r="4" fill="#a54b30"/>')
        # Labels fan away from cube center; two depth layers use opposite offsets.
        dx=8 if SIGNS[i][0]>0 else -28;dy=-10 if SIGNS[i][1]>0 else 22
        for ox,oy in [(dx,dy),(dx,dy-22),(dx,dy+22),(8,-10),(-30,22),(18,35),(-40,-25)]:
            box=(xy[0]+ox,xy[1]+oy-17,xy[0]+ox+26,xy[1]+oy+3)
            if not any(box[0]<b[2]+3 and box[2]>b[0]-3 and box[1]<b[3]+3 and box[3]>b[1]-3 for b in boxes):
                boxes.append(box);label(parts,[xy[0]+ox,xy[1]+oy],f'P{i}');break
    label(parts,[40,635],f"a={c['edge_mm']} mm; angles={c['angles_deg']}; C={c['center_camera_mm']}; f={c['focal_mm']} mm",16)
    label(parts,[40,670],'Original synthetic projection / grid = 10 mm / dashed = hidden edges / not human drawing',14)
    save(parts,name)


def ray_figure(c):
    points=camera_vertices(c);p=points[7];s=helper_scale(points,c)
    parts=svg_start('視線の交点を読む　P7の横位置と縦位置',1000,650)
    for panel,index,title in [(0,0,'横位置 u を求める'),(1,1,'縦位置 v を求める')]:
        ox=60+panel*480;oy=370
        tr=lambda z,t:[ox+z*s*2.4,oy-t*s*2.4]
        label(parts,[ox,95],title,20)
        line(parts,tr(0,0),tr(170/s,0),'#90a6b0',1)
        line(parts,tr(c['focal_mm'],-60/s),tr(c['focal_mm'],80/s),'#d17c41',2)
        line(parts,tr(0,0),tr(p[2],p[index]),'#277b94',3)
        q=c['focal_mm']*p[index]/p[2]
        for xy,txt in [(tr(0,0),'O'),(tr(p[2],p[index]),'P7'),(tr(c['focal_mm'],q),'Q')]:
            parts.append(f'<circle cx="{xy[0]}" cy="{xy[1]}" r="4" fill="#18475b"/>')
            label(parts,[xy[0]-25,xy[1]+22] if txt=='Q' else [xy[0]+8,xy[1]-10],txt)
        label(parts,[ox,555],f"補助図 s={s:g}   読む長さ={s*q:.3f} mm",16)
        label(parts,[ox,583],f"元の紙の値={q:.3f} mm",16)
    label(parts,[40,627],'補助図では Z・X・Y・f をすべて同じ割合で縮める。交点の読みを s で割って戻す。',16)
    save(parts,'ray-charts.svg')


def measuring_figure(c):
    _,steps=measuring_cube(c);step=next(x for x in steps if not x['parallel'])
    points=[step[k] for k in ('P','V','B','M')]
    q=intersection(*points);points.append(q)
    xmin=min(p[0] for p in points);xmax=max(p[0] for p in points)
    ymin=min(p[1] for p in points);ymax=max(p[1] for p in points)
    scale=min(800/max(xmax-xmin,1),400/max(ymax-ymin,1))
    tr=lambda p:[100+(p[0]-xmin)*scale,530-(p[1]-ymin)*scale]
    parts=svg_start('測点を使う　辺1本を延ばす独自構成例')
    p,v,b,m,q=points
    line(parts,tr(q),tr(v));line(parts,tr(q),tr(m),'#b26d33');line(parts,tr(p),tr(b),'#777777',1,'6 4')
    for name,point in zip(('P','V','B','M','Q'),points):
        x,y=tr(point);parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#183f54"/>')
        label(parts,[x+7,y-12],name)
    label(parts,[40,600],'P：始点　V：辺方向の消失点　B：実長を移す点　M：測点　Q：次の頂点',17)
    label(parts,[40,635],'図全体を同じ比率で縮小して表示。原典図の転載・トレースではない。',16)
    label(parts,[40,667],f"Case {c['id']} / P{step['start']} → P{step['end']} / diagram labels are local",14)
    save(parts,'measuring-point.svg')


def main():
    cases={c['id']:c for c in json.loads((HERE/'cases.json').read_text())['cases']}
    selected=[('D1-2-1','正面の面を保った立方体'),('D2-2-1','左右に回した立方体'),('D3-2-0','上面を見せる斜めの立方体')]
    out=['# 立方体作図の記入済み例','',
         '独自の合成計算例。人の作図結果ではない。丸め値は半径80mmの円を0.5mm刻みで読み、半辺を0.001mm、縮尺を小数6桁、最終座標を0.1mmに丸めた計算シミュレーション。', '',
         '[手順書](../../docs/cube-construction-manual.md)の入力・角度・符号表と対応する。理想値と丸め値は別欄。視線法も同じX・Y・Zを使うため、sZとsX、sZとsYの交点をそれぞれ読む。','']
    for cid,title in selected:
        c=cases[cid];p=camera_vertices(c);uv=project(p,c);rounded,ruv=manual_numeric(c)
        cube_figure(c,title,cid+'.svg')
        out += [f'## {title}', '',f"入力：a={c['edge_mm']}mm、角度α・β・γ={c['angles_deg']}度、C={c['center_camera_mm']}mm、f={c['focal_mm']}mm、紙上倍率1。補助図縮尺s={helper_scale(p,c)}。",'',f'![{title}]({cid}.png)','',
                '| 角 | cosに対応する横成分 | sinに対応する縦成分 | 円の読みを丸めた横成分 | 同縦成分 |','| --- | --- | --- | --- | --- |']
        for a in c['angles_deg']:
            co=math.cos(math.radians(a));si=math.sin(math.radians(a))
            out.append(f'| {a}度 | {co:.6f} | {si:.6f} | {round(co*160)/160:.6f} | {round(si*160)/160:.6f} |')
        out += ['', '| 半辺 | X | Y | Z |','| --- | --- | --- | --- |']
        for i,h in enumerate(axes(c),1):out.append('| h%d | %s |'%(i,' | '.join(f'{v:.6f}' for v in h)))
        out += ['', '| 頂点 | 符号 | X | Y | Z | 理想u | 理想v | 丸めu | 丸めv |','| --- | --- | --- | --- | --- | --- | --- | --- | --- |']
        for i,(pp,u,r) in enumerate(zip(p,uv,ruv)):
            out.append(f"| P{i} | {''.join('+' if x>0 else '−' for x in SIGNS[i])} | "+' | '.join(f'{v:.3f}' for v in pp+u+r)+' |')
        # Explicit paper-chart endpoints/readings make both paths traceable.
        s=helper_scale(p,c)
        out += ['', '| 頂点 | sZ | sX | sY | 交点の横読み su | 縦読み sv |','| --- | --- | --- | --- | --- | --- |']
        for i,(pp,u) in enumerate(zip(p,uv)):
            out.append(f'| P{i} | '+' | '.join(f'{v*s:.3f}' for v in [pp[2],pp[0],pp[1],*u])+' |')
        out += ['',f"丸め経路の最大座標差：{errors(ruv,uv)['max_mm']:.4f}mm。ここには実際の点打ち・線引きの誤差を含まない。",'']
    out += ['## 全例で結ぶ辺','',', '.join(f'P{i}–P{j}' for i,j in EDGES)+'。実線・破線は面の向きで分ける。','']
    (HERE/'worked-examples.md').write_text('\n'.join(out))
    ray_figure(cases['D3-2-0']);measuring_figure(cases['D2-2-1'])


if __name__=='__main__':main()
