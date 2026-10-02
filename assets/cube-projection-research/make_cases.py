"""Versioned 24 design + 12 boundary inputs. Expected statuses are explicit."""
from pathlib import Path
import json
from geometry import camera_vertices


def case(name, angles=(0, 0, 0), distance=2, offset=False, kind='design', expected='inside-paper'):
    a = 60; d = distance*a
    return {'id': name, 'kind': kind, 'unit': 'mm', 'rotation_order': 'fixed-Y-X-Z',
            'edge_mm': a, 'angles_deg': list(angles),
            'center_camera_mm': [0.3*d if offset else 0, -0.2*d if offset else 0, d],
            'focal_mm': 100, 'paper_scale': 1, 'paper_half_mm': [90, 125],
            'camera_world': {'eye': [13, -17, 29],
                             'axes': [[0, 1, 0], [-0.8, 0, 0.6], [0.6, 0, 0.8]]},
            'expected': expected}


def main():
    cases = []
    angles = [(0, 0, 0), (30, 0, 0), (45, -20, 0), (65, 35, 15),
              (15, -70, 30), (0, -90, 0)]
    for i, pose in enumerate(angles, 1):
        for distance in (2, 4):
            for offset in (False, True):
                cases.append(case(f'D{i}-{distance}-{int(offset)}', pose, distance, offset))
    specs = [('B01', (0.1, 0, 0)), ('B02', (89.9, 0, 0)),
             ('B03', (0, 90, 0)), ('B04', (30, 20, 90)),
             ('B05', (45, -20, 0)), ('B06', (45, 20, 0)),
             ('B07', (45, 20, 0)), ('B08', (45, 20, 0)),
             ('B09', (45, 20, 0)), ('B10', (45, 20, 0)),
             ('B11', (45, 20, 0)), ('B12', (45, 20, 0))]
    for name, pose in specs:
        c = case(name, pose, kind='boundary')
        if name == 'B05': c['focal_mm'] = 50
        if name == 'B06': c['center_camera_mm'][2] = 1200
        if name in ('B07', 'B08', 'B09', 'B10'):
            c['center_camera_mm'][2] = 0
            reach = -min(p[2] for p in camera_vertices(c))
            near = {'B07': 6, 'B08': .6, 'B09': 0, 'B10': -6}[name]
            c['center_camera_mm'][2] = reach+near
            c['expected'] = {'B07': 'outside-paper', 'B08': 'outside-paper',
                             'B09': 'on-eye-plane', 'B10': 'crosses-eye-plane'}[name]
        if name == 'B11':
            c['center_camera_mm'][0] = 300; c['expected'] = 'outside-paper'
        if name == 'B12': c['center_camera_mm'][2] = 600
        cases.append(c)
    out = {'version': 1, 'date': '2026-10-02', 'primary_selection_mm': 1,
           'secondary_selection_mm': [.5, 2], 'cases': cases}
    Path(__file__).with_name('cases.json').write_text(json.dumps(out, indent=2)+'\n')
    print('Saved 24 design + 12 boundary cases')


if __name__ == '__main__': main()
