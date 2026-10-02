import json
import math
from pathlib import Path
import unittest
from measure import position_error,angle_error,ratio_error,align

ROOT=Path(__file__).resolve().parent
F=json.loads((ROOT/'synthetic-cases.json').read_text())
R=F['reference']; CASES=F['cases']; TOL=1e-10


class MeasurementTests(unittest.TestCase):
    def test_raw_positions_independent_expected_values(self):
        for name,p in CASES.items():
            with self.subTest(name=name):
                self.assertAlmostEqual(position_error(R,p,2),F['expected_raw_position'][name],delta=TOL)

    def test_angles_and_directed_reversal(self):
        for name,expected in [('identity',0),('translation_3_4',0),('scale_2',0),('rotation_90',90)]:
            self.assertAlmostEqual(angle_error(R,CASES[name],'a','b'),expected,delta=TOL)
        self.assertAlmostEqual(angle_error(R,{'a':[1,0],'b':[-1,0],'c':[0,1]},'a','b'),180,delta=TOL)

    def test_ratio(self):
        self.assertAlmostEqual(ratio_error(1,2,2,2),math.log(2),delta=TOL)
        self.assertEqual(ratio_error(1,2,1,2),0)
        self.assertAlmostEqual(ratio_error(1,2,2,4),0,delta=TOL)

    def test_translation_alignment_erases_offset(self):
        p,params=align(R,CASES['translation_3_4'])
        self.assertAlmostEqual(position_error(R,p,2),0,delta=TOL)
        self.assertEqual(params['scale'],1)

    def test_rigid_erases_rotation(self):
        p,params=align(R,CASES['rotation_90'],'rigid')
        self.assertAlmostEqual(position_error(R,p,2),0,delta=TOL)
        self.assertAlmostEqual(params['rotation_deg'],-90,delta=TOL)
        # Centroid translation alone must not erase rotation.
        p,_=align(R,CASES['rotation_90'],'translation')
        self.assertGreater(position_error(R,p,2),.4)

    def test_similarity_erases_scale_and_keeps_local_error(self):
        p,params=align(R,CASES['scale_2'],'similarity')
        self.assertAlmostEqual(position_error(R,p,2),0,delta=TOL)
        self.assertAlmostEqual(params['scale'],.5,delta=TOL)
        p,_=align(R,CASES['scale_2'],'rigid')
        self.assertGreater(position_error(R,p,2),.3)
        p,_=align(R,CASES['single_ratio'],'similarity')
        self.assertGreater(position_error(R,p,2),.1)

    def test_reordered_ids_not_positional_pairing(self):
        p={k:R[k] for k in ['c','b','a']}
        self.assertEqual(position_error(R,p,2),0)
        q,_=align(R,p,'rigid')
        self.assertAlmostEqual(position_error(R,q,2),0,delta=TOL)

    def test_missing_non_numeric_and_id_mismatch(self):
        cases=[{}, {'a':None,'b':[1,0],'c':[0,1]}, {'a':[0,'bad'],'b':[1,0],'c':[0,1]},
               {'a':[0,float('nan')],'b':[1,0],'c':[0,1]}, {'a':[0,float('inf')],'b':[1,0],'c':[0,1]},
               {'a':[True,0],'b':[1,0],'c':[0,1]}, {'a':[-1,0],'b':[1,0],'z':[0,1]}]
        for p in cases:
            with self.subTest(p=p),self.assertRaises(ValueError): position_error(R,p,2)

    def test_zero_lengths_and_normalizer(self):
        for n in [0,-1,None,float('nan')]:
            with self.subTest(n=n),self.assertRaises(ValueError): position_error(R,R,n)
        with self.assertRaises(ValueError): angle_error(R,{'a':[1,0],'b':[1,0],'c':[0,1]},'a','b')
        with self.assertRaises(ValueError): angle_error(R,R,'a','missing')
        for values in [(0,2,1,2),(1,0,1,2),(1,2,-1,2),(1,2,1,float('inf'))]:
            with self.subTest(values=values),self.assertRaises(ValueError): ratio_error(*values)

    def test_degenerate_alignment(self):
        with self.assertRaises(ValueError): align(R,dict.fromkeys(R,(0,0)),'rigid')
        with self.assertRaises(ValueError): align(R,R,'affine')

    def test_actual_geometry_id_inputs(self):
        for file in (ROOT/'answers').glob('*.json'):
            data=json.loads(file.read_text())
            p={k:v['pixel'] for k,v in data['landmarks'].items() if v['visible']}
            self.assertGreater(len(p),2)
            self.assertEqual(position_error(p,p,800),0)
            q, _=align(p,p,'similarity')
            self.assertAlmostEqual(position_error(p,q,800),0,delta=TOL)


def report():
    rows=[]
    for name,p in CASES.items():
        row={'case':name,'raw_position':position_error(R,p,2),'axis_deg':angle_error(R,p,'a','b')}
        for mode in ['translation','rigid','similarity']:
            aligned,params=align(R,p,mode)
            row[mode]={'position':position_error(R,aligned,2),'parameters':params}
        rows.append(row)
    (ROOT/'measurement-report.json').write_text(json.dumps({'synthetic':True,'tolerance':TOL,'normalizer':2,'results':rows},indent=2)+'\n')


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(MeasurementTests))
    if not result.wasSuccessful(): raise SystemExit(1)
    report()
