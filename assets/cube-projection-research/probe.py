"""Small synthetic feasibility probe, not a human drawing experiment.

Run with Python 3; standard library only. Output: probe-results.json.
The exact example uses rational rotation coefficients, not measured angles.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def main():
    # A rigid rotation: columns are perpendicular unit edge directions.
    rotation = [[F(4, 5), F(0), F(3, 5)],
                [F(0), F(1), F(0)],
                [-F(3, 5), F(0), F(4, 5)]]
    columns = list(zip(*rotation))
    assert all(dot(a, b) == int(i == j)
               for i, a in enumerate(columns) for j, b in enumerate(columns))
    center = (F(0), F(0), F(600))
    focal = F(200)
    vertices = list(product((-100, 100), repeat=3))
    rows = []
    for vertex in vertices:
        camera = tuple(dot(row, vertex)+c for row, c in zip(rotation, center))
        x, y, z = camera
        assert z > focal
        projected = (focal*x/z, focal*y/z)
        # Independent geometric incidence check: the point on z=f is on OP.
        ray_point = (*projected, focal)
        cross = (ray_point[1]*z-ray_point[2]*y,
                 ray_point[2]*x-ray_point[0]*z,
                 ray_point[0]*y-ray_point[1]*x)
        assert cross == (0, 0, 0)
        rows.append({'vertex': vertex, 'camera_mm': [float(v) for v in camera],
                     'paper_mm': [float(v) for v in projected],
                     'paper_exact': [str(v) for v in projected]})
    # Symmetric pairs: all eight locations are generated from center + 3 axes.
    assert len({tuple(row['camera_mm']) for row in rows}) == 8
    edges = [(i, j) for i, a in enumerate(vertices)
             for j, b in enumerate(vertices) if i < j and
             sum(x != y for x, y in zip(a, b)) == 1]
    assert len(edges) == 12
    for i, j in edges:
        pa = rows[i]['camera_mm']; pb = rows[j]['camera_mm']
        assert sum((a-b)**2 for a, b in zip(pa, pb)) == 200**2
    bounds = []
    for q in [F(1, 10), F(1, 4), F(1, 2)]:
        maximum = [F(0), F(0), F(0)]
        for n in range(-100, 101):
            t = q*F(n, 100)
            exact = 1/(1+t)
            approximations = (F(1), 1-t, 1-t+t*t)
            for order, approximation in enumerate(approximations):
                error = abs(approximation/exact-1)
                assert error == abs(t)**(order+1)
                maximum[order] = max(maximum[order], error)
        bounds.append({'maximum_relative_depth': float(q),
                       'max_relative_scale_error': [float(e) for e in maximum],
                       'samples': 201})
    report = {'date': '2026-10-02', 'kind': 'synthetic algebraic feasibility only',
              'unit': 'mm', 'cube_edge': 200, 'center': [0, 0, 600],
              'focal_distance': 200,
              'rotation': [[str(v) for v in r] for r in rotation],
              'vertices': rows, 'edges_checked': len(edges),
              'reciprocal_approximation': bounds,
              'checks': ['orthonormal edge frame', '12 equal cube edges',
                         '8 finite ray-plane intersections',
                         '603 rational samples of scale-error identity'],
              'not_checked': ['manual operations', 'speed', 'angle reading error',
                              'all camera orientations', 'visual acceptability',
                              'human learning']}
    target = Path(__file__).with_name('probe-results.json')
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'output': str(target), 'vertices': 8, 'edges': 12,
                      'rational_scale_samples': 603, 'status': 'pass'}))


if __name__ == '__main__':
    main()
