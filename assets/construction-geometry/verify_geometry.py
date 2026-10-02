"""Independent bounds, visibility and sampled painter-order checks."""
import json
from pathlib import Path
from generate import mesh,basis,project,triangles,sub,dot,cross,ray_hit,norm

ROOT=Path(__file__).resolve().parent


def depth_at(x,y,screen):
    a,b,c=screen
    den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
    if abs(den)<1e-9: return None
    u=((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(y-c[1]))/den
    v=((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(y-c[1]))/den
    if min(u,v,1-u-v)<1e-7: return None
    return u*a[2]+v*b[2]+(1-u-v)*c[2]


def main():
    config=json.loads((ROOT/'views.json').read_text()); views=config['views']; image=config['image']
    assert len({(v['azimuth_deg'],v['elevation_deg']) for v in views})==6
    assert sum(v['split']=='training' for v in views)==3
    models=json.loads((ROOT/'models.json').read_text())['models']
    count=0; samples=0
    for model in models:
        vertices,faces,lm=mesh(model)
        for view in views:
            data=json.loads((ROOT/'answers'/f'{model["id"]}-{view["id"]}.json').read_text())
            r,u,t=basis(view)
            for axis in [r,u,t]: assert abs(norm(axis)-1)<1e-12
            assert max(abs(dot(r,u)),abs(dot(r,t)),abs(dot(u,t)))<1e-12
            # Every world axis has a nonzero projection at these views.
            for axis in [(1,0,0),(0,1,0),(0,0,1)]: assert dot(axis,r)**2+dot(axis,u)**2>.01
            pp={k:project(p,view,image) for k,p in vertices.items()}
            assert all(30<x<770 and 110<y<690 for x,y,_ in pp.values())
            for box in data['label_boxes']: assert 10<box[0]<box[2]<790 and 100<box[1]<box[3]<700
            order=data['paint_order']; indices={f:i for i,f in enumerate(order)}
            screen_tris=[(f['id'],[pp[k] for k in [f['vertices'][0],f['vertices'][i],f['vertices'][i+1]]])
                         for f in faces if f['id'] in indices for i in range(1,len(f['vertices'])-1)]
            for x in range(120,690,11):
                for y in range(130,681,11):
                    hits=[(fid,d) for fid,tri in screen_tris if (d:=depth_at(x+.137,y+.273,tri)) is not None]
                    if not hits: continue
                    painter=max(hits,key=lambda h:indices[h[0]])
                    near=max(hits,key=lambda h:h[1])
                    assert abs(painter[1]-near[1])<1e-7, (model['id'],view['id'],x,y,painter,near)
                    samples+=1
            count+=1
    # Absolute analytic ray case: origin inside cube, nearest +z face at t=.5.
    simple={'parts':[{'id':'Q','type':'box','size':[1,1,1],'center':[0,0,0],'yaw_deg':0}]}
    v,f,_=mesh(simple)
    hits=[h for _,a,b,c in triangles(v,f) if (h:=ray_hit((0,0,0),(0,0,1),a,b,c)) is not None]
    assert hits and abs(min(hits)-.5)<1e-12
    # The polygonal cylinder touches the box top at y=-.2; does not penetrate.
    cylinder=models[1]['parts'][1]; box=models[1]['parts'][0]
    assert abs(cylinder['center'][1]-cylinder['height']/2-(box['center'][1]+box['size'][1]/2))<1e-12
    for file in (ROOT/'prompts').glob('*-C.md'):
        text=file.read_text(); assert '![' not in text and 'answers/' not in text and '.png' not in text and '"pixel"' not in text
    for file in (ROOT/'prompts').glob('*-B-recall.md'):
        assert '![' not in file.read_text() and 'answers/' not in file.read_text()
    result={'views_checked':count,'painter_samples':samples,'result':'pass','scope':'sampled occlusion, all bounds and labels, split and prompt separation'}
    (ROOT/'geometry-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__': main()
