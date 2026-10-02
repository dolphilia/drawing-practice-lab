"""Supplementary arbitrary-angle comparison; separate from the 24 design cases."""
from pathlib import Path
import copy,json,random
from geometry import *

HERE=Path(__file__).resolve().parent


def main():
    seed=937; rng=random.Random(seed)
    base=json.loads((HERE/'cases.json').read_text())['cases'][0]
    rows=[]
    for i in range(100):
        c=copy.deepcopy(base);c['id']=f'S{i:03}'
        c['angles_deg']=[rng.uniform(-85,85),rng.uniform(-80,80),rng.uniform(-180,180)]
        c['center_camera_mm']=[0,0,120 if i<50 else 240]
        p=camera_vertices(c);ref=ray_world_reference(c)
        q=copy.deepcopy(c);q['angles_deg']=[round(a/5)*5 for a in c['angles_deg']]
        rows.append({'id':c['id'],'angles_deg':c['angles_deg'],'center_camera_mm':c['center_camera_mm'],
                     'angle_5deg':errors(project(camera_vertices(q),q),ref),
                     'circle_rounding':errors(manual_numeric(c)[1],ref)})
    result={'seed':seed,'kind':'synthetic supplemental angles; not human or population evidence',
            'results':rows,'summary':{key:{'max_mm':max(r[key]['max_mm'] for r in rows),
              'within_1mm':sum(r[key]['max_mm']<=1 for r in rows)} for key in ('angle_5deg','circle_rounding')}}
    (HERE/'supplement-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['summary']))


if __name__=='__main__':main()
