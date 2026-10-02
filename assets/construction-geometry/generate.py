"""Deterministic original geometry. Python 3 standard library only.

SVG faces are sorted by depth. Landmark visibility uses ray/triangle intersections
against the complete mesh, independently of the painter order.
"""
from pathlib import Path
import json
import math
from html import escape

ROOT = Path(__file__).resolve().parent
VERSION = 1
COLORS = {'L': '#dfaf5f', 'U': '#70afd5', 'B': '#70afd5', 'C': '#dfaf5f'}


def add(a, b): return tuple(x+y for x, y in zip(a, b))
def sub(a, b): return tuple(x-y for x, y in zip(a, b))
def mul(a, s): return tuple(x*s for x in a)
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def norm(a): return math.sqrt(dot(a, a))


def rotate(p, yaw):
    a = math.radians(yaw)
    x, y, z = p
    return (math.cos(a)*x+math.sin(a)*z, y, -math.sin(a)*x+math.cos(a)*z)


def mesh(model):
    vertices, faces, landmarks = {}, [], {}
    for part in model['parts']:
        prefix = part['id']
        if part['type'] == 'box':
            w, h, d = part['size']
            v = [(-w/2,-h/2,-d/2),(w/2,-h/2,-d/2),(w/2,-h/2,d/2),(-w/2,-h/2,d/2),
                 (-w/2,h/2,-d/2),(w/2,h/2,-d/2),(w/2,h/2,d/2),(-w/2,h/2,d/2)]
            f = [[0,1,2,3],[4,7,6,5],[0,4,5,1],[3,2,6,7],[0,3,7,4],[1,5,6,2]]
            labels = list(range(8))
        else:
            n, r, h = part['segments'], part['radius'], part['height']
            v = [(r*math.cos(2*math.pi*i/n), y, r*math.sin(2*math.pi*i/n))
                 for y in [-h/2,h/2] for i in range(n)]
            f = [list(range(n)), list(reversed(range(n,2*n)))]
            f += [[i,(i+1)%n,(i+1)%n+n,i+n] for i in range(n)]
            labels = [0,n//4,n//2,3*n//4,n,n+n//4,n+n//2,n+3*n//4]
        for i, p in enumerate(v):
            key = f'{prefix}{i}'
            vertices[key] = add(rotate(p, part['yaw_deg']), part['center'])
            if i in labels: landmarks[key] = vertices[key]
        # Enforce outward winding; input shapes are convex.
        for i, inds in enumerate(f):
            ids = [f'{prefix}{j}' for j in inds]
            pts = [vertices[k] for k in ids]
            c = mul(tuple(map(sum, zip(*pts))), 1/len(pts))
            normal = cross(sub(pts[1],pts[0]), sub(pts[2],pts[0]))
            if dot(normal, sub(c,part['center'])) < 0: ids.reverse()
            faces.append({'id': f'{prefix}-f{i}', 'part': prefix, 'vertices': ids})
    return vertices, faces, landmarks


def basis(view):
    a, e = map(math.radians, [view['azimuth_deg'],view['elevation_deg']])
    return ((math.cos(a),0,-math.sin(a)),
            (-math.sin(e)*math.sin(a), math.cos(e),-math.sin(e)*math.cos(a)),
            (math.cos(e)*math.sin(a),math.sin(e),math.cos(e)*math.cos(a)))


def project(p, view, image):
    right, up, toward = basis(view)
    x0,y0 = image['origin_px']; s = image['scale_px_per_unit']
    return (x0+s*dot(p,right), y0-s*dot(p,up), dot(p,toward))


def ray_hit(p, direction, a, b, c):
    """Return positive ray parameter, or None. No backface exclusion."""
    ab, ac = sub(b,a), sub(c,a)
    h = cross(direction,ac); det = dot(ab,h)
    if abs(det) < 1e-10: return None
    q = sub(p,a); u = dot(q,h)/det
    if u < -1e-9 or u > 1+1e-9: return None
    r = cross(q,ab); v = dot(direction,r)/det
    if v < -1e-9 or u+v > 1+1e-9: return None
    t = dot(ac,r)/det
    return t if t > 1e-8 else None


def triangles(vertices, faces):
    return [(face, vertices[face['vertices'][0]],vertices[face['vertices'][i]],vertices[face['vertices'][i+1]])
            for face in faces for i in range(1,len(face['vertices'])-1)]


def visible(p, toward, tris):
    return not any(ray_hit(p,toward,a,b,c) is not None for _,a,b,c in tris)


def tag(x, y, t, size=18, fill='#263a48'):
    return f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{fill}">{escape(t)}</text>'


def draw(model, view, image):
    vertices, faces, landmarks = mesh(model)
    projected = {k:project(p,view,image) for k,p in vertices.items()}
    toward = basis(view)[2]; tris = triangles(vertices,faces)
    face_order = sorted(faces,key=lambda f:sum(projected[k][2] for k in f['vertices'])/len(f['vertices']))
    painted = []
    for f in face_order:
        p = [vertices[k] for k in f['vertices']]
        if dot(cross(sub(p[1],p[0]),sub(p[2],p[0])),toward) <= 1e-10: continue
        painted.append(f)
    title = f"{model['id']} / {view['id']} / {view['split']}"
    body = [f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800"><title>{escape(title)}</title>',
            '<rect width="800" height="800" fill="#f7f9fb"/>',
            '<g font-family="Arial, sans-serif">',tag(32,42,title,24),
            tag(32,73,f"az {view['azimuth_deg']} deg / el {view['elevation_deg']} deg / orthographic",17)]
    for f in painted:
        coords = ' '.join(f'{projected[k][0]:.4f},{projected[k][1]:.4f}' for k in f['vertices'])
        p = [vertices[k] for k in f['vertices']]
        n = cross(sub(p[1],p[0]),sub(p[2],p[0])); n = mul(n,1/norm(n))
        shade = max(0,dot(n,toward))
        # White overlay changes tone without making rear faces visible.
        body += [f'<polygon points="{coords}" fill="{COLORS[f["part"]]}" stroke="#38546a" stroke-width="1.2"/>',
                 f'<polygon points="{coords}" fill="white" opacity="{.10+.30*shade:.3f}"/>']
    visible_ids, hidden_ids, label_boxes = [], [], []
    for key, p in landmarks.items():
        if not visible(p,toward,tris): hidden_ids.append(key); continue
        visible_ids.append(key)
        x,y,_ = projected[key]
        body.append(f'<circle cx="{x:.4f}" cy="{y:.4f}" r="3.5" fill="#172f42"/>')
        # Allocate non-overlapping labels; leader anchors identify the exact vertex.
        width = 10*len(key)+10
        for dx,dy in [(10,-10),(10,23),(-width-10,-10),(-width-10,23),(15,-30),(-width-15,42)]:
            bx,by = x+dx-3,y+dy-17
            rect = (bx,by,bx+width,by+23)
            if any(not(rect[2]+3<b[0] or b[2]+3<rect[0] or rect[3]+3<b[1] or b[3]+3<rect[1]) for b in label_boxes): continue
            if not(10<rect[0]<rect[2]<790 and 100<rect[1]<rect[3]<700): continue
            label_boxes.append(rect)
            body += [f'<line x1="{x}" y1="{y}" x2="{bx+width/2}" y2="{by+12}" stroke="#38546a" stroke-width=".8"/>',
                     f'<rect x="{bx}" y="{by}" width="{width}" height="23" rx="3" fill="white" opacity=".95"/>',tag(bx+3,by+17,key,16)]
            break
        else: raise ValueError(f'Label collision: {key}')
    body += [tag(32,729,'Labels = visible material landmarks; hidden IDs remain in JSON.',16),
             tag(32,756,'Original synthetic model v1. No anatomy or participant results.',16),'</g></svg>']
    answer = {'version': VERSION,'model_id':model['id'],'view':view,'image':image,
              'landmarks':{k:{'world':p,'pixel':projected[k][:2], 'depth':projected[k][2],
                              'visible':k in visible_ids} for k,p in landmarks.items()},
              'vertices':vertices, 'faces':faces, 'paint_order':[f['id'] for f in painted],
              'hidden_landmarks':hidden_ids, 'label_boxes':label_boxes}
    return ''.join(body),answer


def dump(path, data): path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    models = json.loads((ROOT/'models.json').read_text())['models']
    conf = json.loads((ROOT/'views.json').read_text()); views,image=conf['views'],conf['image']
    assert len({(v['azimuth_deg'],v['elevation_deg']) for v in views}) == len(views)
    answers, prompts = ROOT/'answers', ROOT/'prompts'
    answers.mkdir(exist_ok=True); prompts.mkdir(exist_ok=True)
    manifest=[]
    for m in models:
        for v in views:
            name=f'{m["id"]}-{v["id"]}'
            svg, answer = draw(m,v,image)
            (answers/f'{name}.svg').write_text(svg,encoding='utf-8'); dump(answers/f'{name}.json',answer)
            manifest.append({'model':m['id'],'view':v['id'],'split':v['split'],'answer':f'answers/{name}.json','svg':f'answers/{name}.svg'})
            if v['split']=='training':
                (prompts/f'{name}-A.md').write_text(f'# A：参照あり / {name}\n\n合成モデル。参照を表示したまま、表示されたIDの位置を対応付ける仕様。\n\n![参照](../answers/{name}.png)\n\n測定入力は対応点のIDと画面座標。手描き画像の自動認識は含まない。\n',encoding='utf-8')
                (prompts/f'{name}-B-observe.md').write_text(f'# B：観察 / {name}\n\n![観察参照](../answers/{name}.png)\n\n観察後、この参照を閉じて同名の B-recall ファイルへ進む。時間は未規定。\n',encoding='utf-8')
                (prompts/f'{name}-B-recall.md').write_text(f'# B：再生 / {name}\n\n先ほどの図を同じ向きで再生する。参照・解答は再生後に開いて照合する。\n\n観察段階でIDを含めて覚える条件であり、IDなしの描画記憶とは異なる。\n',encoding='utf-8')
            else:
                # Complete object and camera definition, no target image or 2D answer.
                content=f'# C：未提示角度 / {name}\n\n合成モデル定義と目標カメラから投影を組み立てる仕様。\nモデルは人体の正解ではない。\n\n'
                content+='```json\n'+json.dumps({'model':m,'camera':v,'image':image},ensure_ascii=False,indent=2)+'\n```\n\n'
                content+='座標軸・回転と投影の定義は [仕様](../README.md) を参照。解答フォルダは出題中に開かない。\n'
                (prompts/f'{name}-C.md').write_text(content,encoding='utf-8')
    dump(ROOT/'manifest.json', {'version':VERSION,'synthetic':True,'items':manifest})
    print(f'Generated {len(manifest)} SVGs and answer JSONs; split training/evaluation = 6/6.')


if __name__ == '__main__': main()
