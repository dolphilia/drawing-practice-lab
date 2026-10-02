"""Original operation diagrams, not copies of author illustrations or anatomy."""
from pathlib import Path
import importlib.util
import math
from html import escape
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('geometry',ROOT.parent/'construction-geometry/generate.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
VIEW={'azimuth_deg':30,'elevation_deg':18}


def text(x,y,t,size=21,color='#263a48'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(t)}</text>'
def line(a,b,color='#a34343',dash=False):
    return f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{color}" stroke-width="3"'+(' stroke-dasharray="7 5"' if dash else '')+'/>'
def pp(p,x,y,s=130):return g.project(p,VIEW,{'origin_px':[x,y],'scale_px_per_unit':s})[:2]
def poly(points,fill,stroke='#38546a',dash=False):
    return '<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in points)+f'" fill="{fill}" stroke="{stroke}" stroke-width="2"'+(' stroke-dasharray="6 4"' if dash else '')+'/>'
def model(parts,x,y,s=130):
    verts,faces,_=g.mesh({'parts':parts});toward=g.basis(VIEW)[2]
    faces.sort(key=lambda f:sum(g.dot(verts[k],toward) for k in f['vertices'])/len(f['vertices']))
    out=[]
    for f in faces:
        p=[verts[k] for k in f['vertices']]
        n=g.cross(g.sub(p[1],p[0]),g.sub(p[2],p[0]))
        if g.dot(n,toward)<=0:continue
        color='#c6deee' if f['part']=='U' else '#f1d7a6'
        out.append(poly([pp(a,x,y,s) for a in p],color))
    return ''.join(out)
def shell(title,subtitle,body):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="780" viewBox="0 0 1400 780"><title>'+escape(title)+'</title><rect width="1400" height="780" fill="#f5f8fa"/><g font-family="Hiragino Sans, sans-serif">'+text(36,49,title,32)+text(36,89,subtitle,20)+body+'</g></svg>'
def card(x,title):return f'<rect x="{x}" y="123" width="430" height="542" rx="15" fill="white" stroke="#d5dfe5"/>'+text(x+20,165,title,25)
def box(pid,center,size,yaw=0):return {'id':pid,'type':'box','center':center,'size':size,'yaw_deg':yaw}


def main():
    b=''; cube=box('U',[0,0,0],[1.25,1.7,.9])
    for i,title in enumerate(['1  主要な量を置く','2  面と軸で向きを示す','3  断面で厚みを示す']): b+=card(25+i*460,title)
    b+=model([cube],237,402,125)
    b+=text(48,572,'外側にまとまりを与える。')+text(48,608,'内部の骨・筋はまだ決まらない。',19)
    b+=model([cube],697,402,125)
    for end,label,color in [((.9,0,0),'x','#a34343'),((0,1.12,0),'y','#29806e'),((0,0,.85),'z','#545bb1')]:
        a,z=pp((0,0,0),697,402,125),pp(end,697,402,125);b+=line(a,z,color)+text(z[0]+7,z[1]-8,label,20,color)
    b+=text(508,572,'軸は方向、面は見える側を示す。')+text(508,608,'赤・緑・紫は独自の座標表示。',19)
    cyl={'id':'C','type':'cylinder','radius':.60,'height':1.7,'segments':48,'center':[0,0,0],'yaw_deg':0}
    b+=model([cyl],1157,402,125)
    for yy in [-.35,.35]:
        pts=[pp((.60*math.cos(t*math.pi/24),yy,.60*math.sin(t*math.pi/24)),1157,402,125) for t in range(49)]
        b+='<polyline points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)+'" fill="none" stroke="#a34343" stroke-width="2.5" stroke-dasharray="6 4"/>'
    b+=text(968,572,'赤い輪は説明用の断面。')+text(968,608,'裏側も表示する透視的な約束。',19)
    b+=text(36,707,'同じ情報ではない：量の配置 → 部品の向き → 曲面の回り込み。',24)
    b+=text(36,750,'箱・円柱・寸法・投影は独自設計。リクノ固有理論の再現図、人体の正解像ではありません。',19)
    (ROOT/'mass-axis-section.svg').write_text(shell('描く操作を分ける：量・向き・厚み','概念比較用の独自模式図 ｜ 身体部位への対応と原典の確認範囲は本文を参照',b))
    b=''
    for i,title in enumerate(['1  同じ向きの二つの量','2  下側の向きを変える','3  対応点をつなぐ']): b+=card(25+i*460,title)
    for i,yaw in enumerate([0,35,35]):
        x=237+i*460;y=410;s=120
        upper=box('U',[0,.7,0],[1.15,.65,.75],0)
        lower=box('L',[0,-.65,0],[1.25,.65,.8],yaw)
        b+=model([lower,upper],x,y,s)
        if i==2:
            # Two local front corners. Endpoints belong to different rigid parts.
            top=[(-.575,.375,.375),(.575,.375,.375)]
            bottom=[g.add(g.rotate((xx,.325,.4),yaw),[0,-.65,0]) for xx in [-.625,.625]]
            b+=poly([pp(p,x,y,s) for p in [top[0],top[1],bottom[1],bottom[0]]],'#e4eeed','#29806e')
            for j in range(2):
                for p in [top[j],bottom[j]]:
                    q=pp(p,x,y,s);b+=f'<circle cx="{q[0]}" cy="{q[1]}" r="5" fill="#a34343"/>'
        captions=[['向きがそろっていても、','間の形は自動的に決まらない。'],['この図では y 軸まわりに 35°。','数値は説明用。人体の可動域ではない。'],['赤点は仮の対応点、緑は接続帯。','骨の目印や筋の付着位置ではない。']][i]
        b+=text(48+i*460,572,captions[0],20)+text(48+i*460,608,captions[1],18)
    b+=text(36,707,'回転の指定と、隙間をどうつなぐかは別の判断。',24)
    b+=text(36,750,'接続帯は独自の可視化。皮膚・筋・腹斜筋の形、原典の描線順を表していません。',20)
    (ROOT/'orientation-and-connection.svg').write_text(shell('向きを変えることと、つなぐことを分ける','Bridgman・洞田・Prokoの比較で使う概念を、任意の幾何学形で説明',b))
    print('Generated 2 original operation SVGs.')


if __name__=='__main__':main()
