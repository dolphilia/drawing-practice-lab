"""Deterministic synthetic comparisons. No simulated value is human data."""
from pathlib import Path
import json, math, random
from geometry import *

HERE = Path(__file__).resolve().parent
SEED = 20261002


def summarize(values, failures):
    if not values: return {'trials': failures, 'failures': failures}
    ordered = sorted(v['max_mm'] for v in values)
    return {'trials': len(values)+failures, 'failures': failures,
            'maximum_mm': max(ordered), 'median_max_mm': ordered[len(ordered)//2],
            'p95_max_mm': ordered[math.ceil(.95*len(ordered))-1],
            'mean_rms_mm': sum(v['rms_mm'] for v in values)/len(values)}


def perturbed(c, method, amplitude, rng):
    noise = lambda: rng.uniform(-amplitude, amplitude)
    p = camera_vertices(c)
    if method == 'angle-independent':
        return project(camera_vertices(c, angle_delta=[noise() for _ in range(3)]), c)
    if method == 'angle-common':
        delta = noise()
        return project(camera_vertices(c, angle_delta=[delta]*3), c)
    if method == 'circle-components':
        delta = [[noise()/80 for _ in range(2)] for _ in range(3)]
        return project(camera_vertices(c, coefficient_delta=delta), c)
    if method == 'circle-common-scale':
        factor = 1+noise()/80
        delta = [[(factor-1)*f(math.radians(a)) for f in (math.cos, math.sin)]
                 for a in c['angles_deg']]
        return project(camera_vertices(c, coefficient_delta=delta), c)
    if method == 'half-axis-reading':
        h = [[x+noise() for x in v] for v in axes(c)]
        pp = [[cc+sum(s[j]*h[j][i] for j in range(3))
               for i, cc in enumerate(c['center_camera_mm'])] for s in SIGNS]
        return project(pp, c)
    if method == 'rotation-chart':
        return project(vertices_from_axes(c, construction_axes(c, noise)), c)
    if method == 'coordinate-rounding':
        step = 2*amplitude
        pp = [[round(x/step)*step if step else x for x in v] for v in p]
        return project(pp, c)
    if method == 'ray-chart': return ray_chart(p, c, perturb=noise)
    if method == 'measuring-points': return measuring_cube(c, perturb=noise)[0]
    if method == 'final-placement-control':
        return [[x+noise() for x in v] for v in project(p, c)]
    raise ValueError(method)


def main():
    cases = json.loads((HERE/'cases.json').read_text())['cases']
    reference = []; comparison = []; sensitivity = []
    methods = ['angle-independent', 'angle-common', 'circle-components',
               'circle-common-scale', 'half-axis-reading', 'rotation-chart', 'coordinate-rounding',
               'ray-chart', 'measuring-points', 'final-placement-control']
    rng = random.Random(SEED)
    for c in cases:
        validate(c); p = camera_vertices(c); state = status(p, c)
        assert state == c['expected'], (c['id'], state)
        if depth_state(p) != 'finite':
            reference.append({'id': c['id'], 'status': state})
            comparison.append({'id': c['id'], 'status': 'rejected-before-approximation'})
            sensitivity.append({'id': c['id'], 'status': 'rejected-before-perturbation'})
            continue
        uv = project(p, c); world = ray_world_reference(c); chart = ray_chart(p, c)
        assert concurrency_residual(uv) < 1e-10
        measured, steps = measuring_cube(c)
        full_chart = ray_chart(vertices_from_axes(c, construction_axes(c)), c)
        tests = {name: errors(result, uv) for name, result in
                 [('world-ray', world), ('ray-chart', chart), ('full-construction', full_chart), ('measuring', measured)]}
        assert max(e['max_mm'] for e in tests.values()) < 1e-7
        reference.append({'id': c['id'], 'status': state, 'camera_mm': p, 'paper_mm': uv,
                          'half_axes_mm': axes(c), 'checks': tests,
                          'helper_scale': helper_scale(p, c),
                          'measuring_min_scale': min(s['scale'] for s in steps),
                          'projected_size_mm': [max(v[i] for v in uv)-min(v[i] for v in uv)
                                                for i in (0, 1)]})
        variants = {}
        for method in ('weak', 'linear', 'quadratic', 'depth-table'):
            try:
                output = approximate(p, c, method)
                e = errors(output, uv); e['edge_line_deviation_mm'] = line_deviation(output, uv)
                e['concurrency_residual'] = concurrency_residual(output)
                if method != 'depth-table':
                    degree = ('weak', 'linear', 'quadratic').index(method)
                    e['bound_mm'] = polynomial_bound(p, c, degree)
                    assert e['max_mm'] <= e['bound_mm']+1e-8
                variants[method] = e
            except ValueError as exc: variants[method] = {'rejected': str(exc)}
        rounded_angles = {**c, 'angles_deg': [round(a/5)*5 for a in c['angles_deg']]}
        try: variants['angle-5deg'] = errors(project(camera_vertices(rounded_angles), c), uv)
        except ValueError as exc: variants['angle-5deg'] = {'rejected': str(exc)}
        try: variants['circle-and-rounding'] = errors(manual_numeric(c)[1], uv)
        except ValueError as exc: variants['circle-and-rounding'] = {'rejected': str(exc)}
        # Exact reuse: number of distinct depths (numerically merge only equal depths).
        reused, distinct = project_reusing_depth(p, c)
        assert errors(reused, uv)['max_mm'] < 1e-9
        h = c['edge_mm']/4
        low = math.floor(min(v[2] for v in p)/h)
        high = math.floor(max(v[2] for v in p)/h)+1
        comparison.append({'id': c['id'], 'variants': variants,
                           'exact_divisions': distinct, 'baseline_divisions': 8,
                           'table_knot_divisions': high-low+1 if low>0 else None})
        entries = []
        for method in methods:
            amplitudes = [0, .5, 1, 2] if method.startswith('angle-') else [0, .25, .5, 1]
            for amplitude in amplitudes:
                values = []; failures = 0
                for trial in range(40 if amplitude and method != 'coordinate-rounding' else 1):
                    try:
                        result = perturbed(c, method, amplitude, rng)
                        values.append(errors(result, uv))
                    except ValueError: failures += 1
                if amplitude == 0:
                    assert failures == 0 and max(v['max_mm'] for v in values) < 1e-7
                entries.append({'operation': method, 'amplitude': amplitude,
                                'unit': 'degree' if method.startswith('angle-') else 'mm',
                                **summarize(values, failures)})
        sensitivity.append({'id': c['id'], 'status': state, 'operations': entries})
    for name, data in [('reference-results', reference), ('comparison-results', comparison),
                       ('sensitivity-results', sensitivity)]:
        (HERE/(name+'.json')).write_text(json.dumps({'version': 1, 'seed': SEED,
              'kind': 'synthetic; not human measurements', 'results': data}, indent=2)+'\n')
    summary = {'finite_cases': sum('paper_mm' in r for r in reference),
               'rejected_cases': sum('paper_mm' not in r for r in reference),
               'max_reference_disagreement_mm': max(e['max_mm'] for r in reference
                   for e in r.get('checks', {}).values()),
               'sensitivity_trials': sum(e['trials'] for r in sensitivity
                   for e in r.get('operations', [])),
               'design_pass_counts': {}}
    for method in ('weak', 'linear', 'quadratic', 'depth-table', 'circle-and-rounding'):
        summary['design_pass_counts'][method] = {str(t): sum(
            r['variants'][method].get('max_mm', math.inf) <= t
            for r in comparison if r['id'].startswith('D')) for t in (.5, 1, 2)}
    (HERE/'evaluation-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__': main()
