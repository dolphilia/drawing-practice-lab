"""Invariant, rejection, independent-reference and general-pose checks."""
import copy, json, math, random, unittest
from pathlib import Path
from geometry import *

HERE = Path(__file__).resolve().parent
CASES = json.loads((HERE/'cases.json').read_text())['cases']


class GeometryTests(unittest.TestCase):
    def test_case_inventory(self):
        self.assertEqual(len(CASES), 36)
        self.assertEqual(sum(c['kind']=='design' for c in CASES), 24)
        self.assertEqual(len({c['id'] for c in CASES}), 36)

    def test_boundary_semantics(self):
        cs={c['id']:c for c in CASES}
        self.assertEqual(cs['B01']['angles_deg'][0],.1)
        self.assertEqual(cs['B02']['angles_deg'][0],89.9)
        self.assertEqual(cs['B03']['angles_deg'],[0,90,0])
        self.assertEqual(cs['B04']['angles_deg'][2],90)
        a,b=cs['D3-2-0'],cs['B05']
        self.assertEqual(a['angles_deg'],b['angles_deg'])
        self.assertEqual(a['center_camera_mm'],b['center_camera_mm'])
        self.assertEqual(b['focal_mm'],a['focal_mm']/2)
        self.assertEqual(cs['B06']['center_camera_mm'][2],20*cs['B06']['edge_mm'])
        for name,near in [('B07',6),('B08',.6),('B09',0),('B10',-6)]:
            self.assertAlmostEqual(min(p[2] for p in camera_vertices(cs[name])),near)
        p=camera_vertices(cs['B12']);s=helper_scale(p,cs['B12'])
        self.assertLessEqual(max(v[2] for v in p)*s,160)
        self.assertLessEqual(max(abs(v[i]) for v in p for i in (0,1))*s,100)

    def test_independent_reference_and_constructions(self):
        for c in CASES:
            with self.subTest(case=c['id']):
                validate(c); p=camera_vertices(c)
                self.assertEqual(status(p,c),c['expected'])
                if depth_state(p)!='finite':
                    for run in (lambda:project(p,c),lambda:ray_world_reference(c),
                                lambda:ray_chart(p,c),lambda:measuring_cube(c)):
                        self.assertRaises(ValueError,run)
                    continue
                ref=ray_world_reference(c)
                for uv in (project(p,c),ray_chart(p,c),measuring_cube(c)[0],
                           ray_chart(vertices_from_axes(c,construction_axes(c)),c)):
                    self.assertLess(errors(uv,ref)['max_mm'],1e-7)
                h=axes(c)
                for i,a in enumerate(h):
                    for j,b in enumerate(h):
                        self.assertAlmostEqual(dot(a,b),(c['edge_mm']/2)**2 if i==j else 0,places=8)
                for i,j in EDGES:self.assertAlmostEqual(norm(sub(p[i],p[j])),c['edge_mm'],places=8)

    def test_known_front_projection(self):
        c=CASES[0];uv=project(camera_vertices(c),c)
        self.assertAlmostEqual(uv[0][0],-100/3)
        self.assertAlmostEqual(uv[0][1],-100/3)
        self.assertAlmostEqual(uv[1][0],-20)
        self.assertAlmostEqual(uv[1][1],-20)

    def test_depth_and_focal_are_different_controls(self):
        c=CASES[0];uv=project(camera_vertices(c),c)
        d=copy.deepcopy(c);d['focal_mm']*=2
        self.assertLess(errors(project(camera_vertices(d),d),[mul(p,2) for p in uv])['max_mm'],1e-9)
        d=copy.deepcopy(c);d['center_camera_mm'][2]*=2
        ratios=[norm(q)/norm(p) for q,p in zip(project(camera_vertices(d),d),uv)]
        self.assertGreater(max(ratios)-min(ratios),.01)

    def test_world_frame_invariance(self):
        c=copy.deepcopy(CASES[8]);a=ray_world_reference(c)
        c['camera_world']={'eye':[0,0,0],'axes':[[1,0,0],[0,1,0],[0,0,1]]}
        self.assertLess(errors(a,ray_world_reference(c))['max_mm'],1e-9)

    def test_reject_malformed_conventions(self):
        mutations=[('unit','cm'),('rotation_order','fixed-X-Y-Z'),('focal_mm',0),
                   ('paper_scale',-1),('edge_mm',float('nan')),('unknown_input',100)]
        for key,value in mutations:
            c=copy.deepcopy(CASES[0]);c[key]=value
            self.assertRaises(ValueError,validate,c)
        c=copy.deepcopy(CASES[0]);c['camera_world']['axes'][0][0]=1
        self.assertRaises(ValueError,validate,c)

    def test_arbitrary_poses_and_bounds(self):
        rng=random.Random(417)
        for _ in range(200):
            c=copy.deepcopy(CASES[0]);c['angles_deg']=[rng.uniform(-180,180) for i in range(3)]
            c['center_camera_mm']=[rng.uniform(-120,120),rng.uniform(-80,80),rng.uniform(90,600)]
            p=camera_vertices(c);ref=ray_world_reference(c)
            for uv in (project(p,c),ray_chart(p,c),measuring_cube(c)[0],
                       ray_chart(vertices_from_axes(c,construction_axes(c)),c)):
                self.assertLess(errors(uv,ref)['max_mm'],1e-7)
            for n,m in enumerate(('weak','linear','quadratic')):
                self.assertLessEqual(errors(approximate(p,c,m),ref)['max_mm'],polynomial_bound(p,c,n)+1e-8)

    def test_helper_homothety_preserves_result(self):
        for c in CASES:
            p=camera_vertices(c)
            if depth_state(p)!='finite':continue
            self.assertLess(errors(ray_chart(p,c,scale=1/32),project(p,c))['max_mm'],1e-7)

    def test_screen_rotation(self):
        c=copy.deepcopy(CASES[0]);c['angles_deg']=[30,20,0]
        first=project(camera_vertices(c),c);c['angles_deg'][2]=90
        self.assertLess(errors(project(camera_vertices(c),c),[[-y,x] for x,y in first])['max_mm'],1e-9)
        c['angles_deg'][2]=0;c['center_camera_mm']=[36,-24,120]
        first=project(camera_vertices(c),c);c['angles_deg'][2]=90
        self.assertGreater(errors(project(camera_vertices(c),c),[[-y,x] for x,y in first])['max_mm'],1)
        c['center_camera_mm']=[24,36,120]
        self.assertLess(errors(project(camera_vertices(c),c),[[-y,x] for x,y in first])['max_mm'],1e-9)

    def test_exact_depth_reuse(self):
        for c in CASES:
            p=camera_vertices(c)
            if depth_state(p)!='finite':continue
            uv,n=project_reusing_depth(p,c)
            self.assertLess(errors(uv,project(p,c))['max_mm'],1e-9)
            self.assertLessEqual(n,8)

    def test_face_diagonals_and_projected_line_midpoints(self):
        c=next(c for c in CASES if c['id']=='D3-2-0')
        p=camera_vertices(c);uv=project(p,c)
        for face in FACES:
            a,b,d,e=face
            hit=intersection(uv[a],uv[e],uv[b],uv[d])
            center=mul(add(p[a],p[e]),.5)
            self.assertLess(norm(sub(hit,project([center],c)[0])),1e-8)
        for i,j in EDGES:
            midpoint=project([mul(add(p[i],p[j]),.5)],c)[0]
            direction=sub(uv[j],uv[i]);offset=sub(midpoint,uv[i])
            self.assertAlmostEqual(direction[0]*offset[1]-direction[1]*offset[0],0,places=8)

    def test_edge_on_viewing_ray(self):
        c=copy.deepcopy(CASES[0]);c['center_camera_mm']=[30,30,300]
        p=camera_vertices(c);uv,steps=measuring_cube(c)
        self.assertLess(errors(uv,ray_world_reference(c))['max_mm'],1e-8)
        self.assertTrue(any(s.get('collapsed') for s in steps))


if __name__=='__main__':unittest.main()
