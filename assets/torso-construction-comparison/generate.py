"""Original explanatory geometry, not measured anatomy or experimental data.

Run with Python 3; SVG generation requires only the standard library.
"""
from pathlib import Path
from math import sin, cos, radians
from html import escape

OUT = Path(__file__).resolve().parent
AZ, EL = radians(30), radians(15)
BLUE = ('#e2effa', '#b8d6ed', '#f2f8fc', '#245b82')
AMBER = ('#fff0cd', '#e8c784', '#fff7e5', '#91651b')


def project(p, ox, oy, scale):
    x, y, z = p
    return (ox + scale * (cos(AZ)*x - sin(AZ)*z),
            oy + scale * (sin(EL)*sin(AZ)*x - cos(EL)*y + sin(EL)*cos(AZ)*z))


def points(v):
    return ' '.join(f'{x:.2f},{y:.2f}' for x, y in v)


def text(x, y, s, size=22, color='#243747', weight='400'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(s)}</text>'


def cuboid(w, h, d, y0=0, bottom_w=None, bottom_shift=0):
    # Indices 0..3 bottom, 4..7 top. +z is front; -z is back.
    bw = w if bottom_w is None else bottom_w
    return [(-bw/2,y0,-d/2+bottom_shift),(bw/2,y0,-d/2+bottom_shift),
            (bw/2,y0,d/2+bottom_shift),(-bw/2,y0,d/2+bottom_shift),
            (-w/2,y0+h,-d/2),(w/2,y0+h,-d/2),
            (w/2,y0+h,d/2),(-w/2,y0+h,d/2)]


def box(v, ox, oy, scale, colors):
    p = [project(a, ox, oy, scale) for a in v]
    front, side, top, stroke = colors
    s = []
    # Hidden edges shown explicitly as a construction convention.
    for a, b in [(0,1),(0,3),(0,4)]:
        s.append(f'<polyline points="{points([p[a],p[b]])}" fill="none" stroke="{stroke}" stroke-width="1.6" stroke-dasharray="5 5"/>')
    for face, fill in [([1,2,6,5],side),([3,2,6,7],front),([4,5,6,7],top)]:
        s.append(f'<polygon points="{points([p[i] for i in face])}" fill="{fill}" fill-opacity="0.9" stroke="{stroke}" stroke-width="2.5" stroke-linejoin="round"/>')
    return ''.join(s)


def shell(title, subtitle, body, width=1440, height=800):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>
<rect width="100%" height="100%" fill="#f6f8fa"/>
<g font-family="Hiragino Sans, Noto Sans CJK JP, sans-serif">
{text(44,54,title,32,weight='700')}{text(44,90,subtitle,19)}
{body}</g></svg>'''


def main():
    body = []
    for x in [32,736]:
        body.append(f'<rect x="{x}" y="122" width="672" height="562" rx="16" fill="white" stroke="#dce3e9"/>')
    body += [text(58,163,'洞田式：中立配置の初期ブロック',26,weight='700'),
             text(762,163,'Robo Bean：中立配置の二つの量',26,weight='700')]
    # Both have zero relative rotation; same camera. Sizes are NOT anatomical matches.
    body += [box(cuboid(1,.75,2/3,0),292,561,180,AMBER),
             box(cuboid(1,1,2/3,.75),292,561,180,BLUE),
             box(cuboid(1.1,.60,.55,0),984,561,180,AMBER),
             box(cuboid(1,1,.60,.90),984,561,180,BLUE)]
    body += [text(446,277,'胸郭の基準箱',22,'#245b82'),text(446,310,'高さ H',20),
             text(446,348,'奥行き 2H/3',20),text(446,478,'下へ延ばす補助箱',20,'#91651b'),
             text(446,509,'高さ 3H/4',20),text(446,545,'骨盤そのものではない',17),
             text(1124,268,'胸郭＋肩の一部',20,'#245b82'),text(1124,451,'箱の間に接続部',19),
             text(1124,526,'骨盤＋臀部',20,'#91651b'),
             text(58,616,'胸の面取り等を省き、基準箱と補助箱の関係を示す。',19),
             text(58,649,'この図は完成した洞田式素体を表していない。',19),
             text(762,616,'箱の角を骨の目印に対応させ、面で向きを表す。',19),
             text(762,649,'図の幅・高さ・間隔は説明用。固定比率ではない。',19),
             text(44,727,'共通条件：曲げ・相対的なねじれがない配置を、同じ平行投影で示す。',21,weight='700'),
             text(44,766,'色は説明用。二方法の箱の範囲・角・寸法は同一視できない。出典と省略は README.md を参照。',19)]
    (OUT/'neutral-comparison.svg').write_text(shell('同じ「二つの箱」でも、表しているものが違う',
        '原典をもとにした独自の説明図 ｜ 人体の実測値・採点用の正解画像ではありません', ''.join(body)),encoding='utf-8')

    body = []
    for i,(heading,bw,shift) in enumerate([('1  補助箱を下へ延長',None,0),('2  底面だけ幅を広げる',4/3,0),('3  底面だけ後ろへずらす',4/3,-1/6)]):
        left = 24 + i*472
        body.append(f'<rect x="{left}" y="122" width="448" height="525" rx="16" fill="white" stroke="#dce3e9"/>')
        body.append(text(left+22,165,heading,23,weight='700'))
        body.append(box(cuboid(1,.75,2/3,0,bw,shift),left+220,522,190,AMBER))
        # An unmodified chest box is a size reference, not the final chamfered chest.
        body.append(box(cuboid(1,1,2/3,.75),left+220,522,190,BLUE))
        captions=[['高さは胸の基準箱の 3/4。','下箱は構築の補助。'],['底面を二分し、二つの正方形へ。','上面の幅はそのまま。'],['ずらす量は奥行きの 1/4。','箱全体の平行移動ではない。']][i]
        body.append(text(left+22,586,captions[0],20))
        body.append(text(left+22,619,captions[1],20))
    body += [text(44,700,'抜粋した操作：胸郭の面取り・股関節の球・骨盤の輪郭・くびれの構築は省略。',21,weight='700'),
             text(44,740,'原典第3回の「補助箱4 → 骨盤5 → 骨盤6」に対応。幅と移動を見分けるための独自の段階図。',19),
             text(44,775,'破線は隠れる辺を示す作図用の約束。人体の筋肉や皮膚の線ではありません。',19)]
    (OUT/'toda-base-transforms.svg').write_text(shell('洞田式の補助箱：下側を変える二つの操作',
        '各段階を同じ視点・縮尺で比較 ｜ 上面を保ったまま底面の幅と前後位置を変える', ''.join(body)),encoding='utf-8')

    # Verify the depicted source relationships in 3D, not pixel aspect ratios.
    base = cuboid(1,.75,2/3,0,4/3,-1/6)
    assert abs((base[1][0]-base[0][0])/2 - (base[3][2]-base[0][2])) < 1e-12
    assert abs(base[4][1]-base[0][1]-.75) < 1e-12
    assert abs(base[0][2]-base[4][2]+(2/3)/4) < 1e-12
    assert base[4:] == cuboid(1,.75,2/3)[4:]
    print('Wrote 2 original SVGs. Base width, height, shift, and unchanged top verified.')


if __name__ == '__main__':
    main()
