"""Research reference and simulated hand constructions; all lengths in mm.

Right-handed camera coordinates: X right, Y up, Z forward. Active rotations
about fixed axes: Ry(yaw), then Rx(pitch), then Rz(roll).
No human use of this module is assumed by the drawing procedures.
"""
import math
from itertools import product, combinations

SIGNS = list(product((-1, 1), repeat=3))
EDGES = [(i, j) for i, a in enumerate(SIGNS) for j, b in enumerate(SIGNS)
         if i < j and sum(x != y for x, y in zip(a, b)) == 1]
FACES = [[i for i, s in enumerate(SIGNS) if s[axis] == side]
         for axis in range(3) for side in (-1, 1)]


def dot(a, b): return sum(x*y for x, y in zip(a, b))
def add(a, b): return [x+y for x, y in zip(a, b)]
def sub(a, b): return [x-y for x, y in zip(a, b)]
def mul(a, k): return [x*k for x in a]
def norm(a): return math.sqrt(dot(a, a))
def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]


def validate(c):
    required = {'id', 'kind', 'unit', 'rotation_order', 'edge_mm',
                'angles_deg', 'center_camera_mm', 'focal_mm', 'paper_scale',
                'paper_half_mm', 'camera_world', 'expected'}
    if set(c) != required: raise ValueError('Missing/unknown input keys')
    if c['unit'] != 'mm' or c['rotation_order'] != 'fixed-Y-X-Z':
        raise ValueError('Unit or rotation convention mismatch')
    numeric = [c['edge_mm'], c['focal_mm'], c['paper_scale'],
               *c['angles_deg'], *c['center_camera_mm'], *c['paper_half_mm'],
               *c['camera_world']['eye'], *sum(c['camera_world']['axes'], [])]
    if not all(isinstance(x, (int, float)) and math.isfinite(x) for x in numeric):
        raise ValueError('Non-finite/non-numeric input')
    if min(c['edge_mm'], c['focal_mm'], c['paper_scale'], *c['paper_half_mm']) <= 0:
        raise ValueError('Non-positive length or output scale')
    if len(c['angles_deg']) != 3 or len(c['center_camera_mm']) != 3:
        raise ValueError('Three angles and center components required')
    axes = c['camera_world']['axes']
    if len(axes) != 3 or any(len(a) != 3 for a in axes): raise ValueError('Frame size')
    if max(abs(dot(a, b)-int(i == j)) for i, a in enumerate(axes)
           for j, b in enumerate(axes)) > 1e-10:
        raise ValueError('Frame is not orthonormal')
    if norm(sub(cross(axes[0], axes[1]), axes[2])) > 1e-10:
        raise ValueError('Frame is not right handed')


def rotate_sequential(p, angles, coefficient_step=None, angle_delta=None, coefficient_delta=None):
    values = []
    for i, angle in enumerate(angles):
        theta = math.radians(angle + (angle_delta[i] if angle_delta else 0))
        cs = [math.cos(theta), math.sin(theta)]
        if coefficient_step:
            cs = [round(v/coefficient_step)*coefficient_step for v in cs]
        if coefficient_delta:
            cs = [v+coefficient_delta[i][j] for j, v in enumerate(cs)]
        values.append(cs)
    (ca, sa), (cb, sb), (cg, sg) = values
    x, y, z = p
    x, z = ca*x+sa*z, -sa*x+ca*z
    y, z = cb*y-sb*z, sb*y+cb*z
    return [cg*x-sg*y, sg*x+cg*y, z]


def axes(c, **kwargs):
    return [rotate_sequential([int(i == j)*c['edge_mm']/2 for i in range(3)],
                              c['angles_deg'], **kwargs) for j in range(3)]


def construction_axes(c, perturb=None):
    # Simulated compass rotation of the endpoint in three auxiliary planes.
    # Polar length+angle construction, not the coefficient multiplication path.
    noise = perturb or (lambda: 0.0)
    result = []
    for axis in range(3):
        p = [int(i == axis)*c['edge_mm']/2 for i in range(3)]
        for i, j, angle in [(0,2,-c['angles_deg'][0]), (1,2,c['angles_deg'][1]),
                            (0,1,c['angles_deg'][2])]:
            radius = math.hypot(p[i], p[j])
            if radius == 0: continue
            theta = math.atan2(p[j], p[i])+math.radians(angle)
            p[i], p[j] = radius*math.cos(theta)+noise(), radius*math.sin(theta)+noise()
        result.append(p)
    return result


def vertices_from_axes(c, h):
    return [[cc+sum(s[j]*h[j][i] for j in range(3))
             for i, cc in enumerate(c['center_camera_mm'])] for s in SIGNS]


def camera_vertices(c, **kwargs):
    half_axes = axes(c, **kwargs)
    return [[center+sum(s[j]*half_axes[j][i] for j in range(3))
             for i, center in enumerate(c['center_camera_mm'])] for s in SIGNS]


def depth_state(points):
    zmin = min(p[2] for p in points)
    if zmin < -1e-9: return 'crosses-eye-plane'
    if zmin <= 1e-9: return 'on-eye-plane'
    return 'finite'


def project(points, c):
    if depth_state(points) != 'finite': raise ValueError('Non-positive depth')
    f = c['focal_mm']*c['paper_scale']
    return [[f*x/z, f*y/z] for x, y, z in points]


def project_reusing_depth(points, c):
    if depth_state(points) != 'finite': raise ValueError('Non-positive depth')
    cache = {}; result = []
    for x,y,z in points:
        if z not in cache: cache[z] = c['focal_mm']*c['paper_scale']/z
        result.append([cache[z]*x, cache[z]*y])
    return result, len(cache)


def status(points, c):
    state = depth_state(points)
    if state != 'finite': return state
    uv = project(points, c)
    return ('outside-paper' if any(abs(p[i]) > c['paper_half_mm'][i]+1e-9
                                  for p in uv for i in range(2)) else 'inside-paper')


def qmul(a, b):
    w, x, y, z = a; t, u, v, s = b
    return [w*t-x*u-y*v-z*s, w*u+x*t+y*s-z*v,
            w*v-x*s+y*t+z*u, w*s+x*v-y*u+z*t]


def world_vertices_independent(c):
    # Independently compose rotations with quaternions, not the axis-table path.
    qs = []
    for angle, axis in zip(c['angles_deg'], (1, 0, 2)):
        q = [math.cos(math.radians(angle)/2), 0, 0, 0]
        q[axis+1] = math.sin(math.radians(angle)/2); qs.append(q)
    q = qmul(qs[2], qmul(qs[1], qs[0])); conjugate = [q[0], -q[1], -q[2], -q[3]]
    frame = c['camera_world']; result = []
    for signs in SIGNS:
        local = [0]+[s*c['edge_mm']/2 for s in signs]
        p = qmul(qmul(q, local), conjugate)[1:]
        p = add(p, c['center_camera_mm'])
        result.append([frame['eye'][i]+sum(frame['axes'][j][i]*p[j] for j in range(3))
                       for i in range(3)])
    return result


def solve(matrix, rhs):
    n = len(rhs); a = [list(row)+[r] for row, r in zip(matrix, rhs)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda i: abs(a[i][col]))
        if abs(a[pivot][col]) < 1e-12: raise ValueError('Parallel or singular')
        a[col], a[pivot] = a[pivot], a[col]
        div = a[col][col]; a[col] = [v/div for v in a[col]]
        for row in range(n):
            if row != col:
                factor = a[row][col]
                a[row] = [v-factor*u for v, u in zip(a[row], a[col])]
    return [a[-1] for a in a]


def ray_world_reference(c):
    # Solve E+t(P-E) = E+f*N+u*R+v*U in world space.
    # Independent vertex rotation and a 3x3 intersection solve are used.
    frame = c['camera_world']; right, up, forward = frame['axes']
    normal = cross(right, up); result = []
    for p in world_vertices_independent(c):
        d = sub(p, frame['eye'])
        if dot(d, normal) <= 1e-9: raise ValueError('Non-positive world ray depth')
        matrix = [[d[i], -right[i], -up[i]] for i in range(3)]
        t, u, v = solve(matrix, mul(normal, c['focal_mm']))
        assert t > 0
        result.append([u*c['paper_scale'], v*c['paper_scale']])
    return result


def intersection(a, b, d, e):
    # Finite straightedge line intersection, independent of projection formula.
    x = sub(b, a); y = sub(e, d)
    t, _ = solve([[x[0], -y[0]], [x[1], -y[1]]], sub(d, a))
    return add(a, mul(x, t))


def helper_scale(points, c):
    # Two sequential helper charts, each inside 160 x 200mm; halve only.
    zspan = max(c['focal_mm'], max(p[2] for p in points))
    transverse = max(abs(p[i]) for p in points for i in (0, 1))
    scale = 1.0
    while scale*zspan > 160 or scale*transverse > 100: scale /= 2
    return scale


def ray_chart(points, c, scale=None, perturb=None):
    if depth_state(points) != 'finite': raise ValueError('Non-positive depth')
    scale = helper_scale(points, c) if scale is None else scale
    noise = perturb or (lambda: 0.0)
    result = []
    # Shared screen line error represents a single mistakenly placed line.
    screen = c['focal_mm']*scale + noise()
    for p in points:
        uv = []
        for component in (0, 1):
            endpoint = [p[2]*scale+noise(), p[component]*scale+noise()]
            if endpoint[0] <= 1e-9: raise ValueError('Perturbed chart crosses eye plane')
            q = intersection([0, 0], endpoint, [screen, -100], [screen, 100])
            # Intersection reading is a separate construction-stage error.
            uv.append((q[1]+noise())/scale*c['paper_scale'])
        result.append(uv)
    return result


def errors(uv, ref):
    distances = [norm(sub(a, b)) for a, b in zip(uv, ref)]
    return {'max_mm': max(distances),
            'rms_mm': math.sqrt(sum(d*d for d in distances)/len(distances))}


def approximate(points, c, method):
    d = c['center_camera_mm'][2]; f = c['focal_mm']*c['paper_scale']
    result = []
    for x, y, z in points:
        t = (z-d)/d
        if method == 'weak': k = f/d
        elif method == 'linear': k = f/d*(1-t)
        elif method == 'quadratic': k = f/d*(1-t+t*t)
        elif method == 'depth-table':
            h = c['edge_mm']/4
            lo = math.floor(z/h)*h; hi = lo+h
            if lo <= 0: raise ValueError('Table requires positive lower knot')
            k = ((hi-z)*(f/lo)+(z-lo)*(f/hi))/h
        else: raise ValueError(method)
        result.append([k*x, k*y])
    return result


def polynomial_bound(points, c, degree):
    d = c['center_camera_mm'][2]
    q = max(abs(p[2]-d) for p in points)/d
    transverse = max(norm(p[:2]) for p in points)
    if q >= 1: return math.inf
    return c['paper_scale']*c['focal_mm']/d*transverse*q**(degree+1)/(1-q)


def line_deviation(uv, ref):
    # Max endpoint distance to reference edge line in the picture; finite VP safe.
    deviations = []
    for i, j in EDGES:
        d = sub(ref[j], ref[i]); length = norm(d)
        if length < 1e-10: continue
        for p in (uv[i], uv[j]):
            v = sub(p, ref[i]); deviations.append(abs(d[0]*v[1]-d[1]*v[0])/length)
    return max(deviations, default=0)


def concurrency_residual(uv):
    # Homogeneous line rank test covers finite and infinite vanishing points.
    # Coordinates divided by 100mm before normalization; dimensionless residual.
    residual = 0.0
    for axis in range(3):
        lines = []
        for i,j in EDGES:
            if SIGNS[i][axis] == SIGNS[j][axis]: continue
            a=[uv[i][0]/100,uv[i][1]/100,1]
            b=[uv[j][0]/100,uv[j][1]/100,1]
            line=cross(a,b);length=norm(line)
            if length > 1e-12: lines.append(mul(line,1/length))
        for a,b,c in combinations(lines,3):residual=max(residual,abs(dot(a,cross(b,c))))
    return residual


def manual_numeric(c):
    # 80mm radius circle, 0.5mm coordinate grid, not a human error distribution.
    half_axes = [[round(v, 3) for v in p] for p in axes(c, coefficient_step=.5/80)]
    points = [[round(center+sum(s[j]*half_axes[j][i] for j in range(3)), 3)
               for i, center in enumerate(c['center_camera_mm'])] for s in SIGNS]
    if depth_state(points) != 'finite': raise ValueError('Rounded non-positive depth')
    uv = []
    for x, y, z in points:
        k = round(c['focal_mm']/z, 6)
        uv.append([round(c['paper_scale']*k*x, 1), round(c['paper_scale']*k*y, 1)])
    return points, uv


def measuring_step(p, screen_p, direction, length, c, perturb=None):
    """Compass measuring point: M=V-sign(ez)*sqrt(f²+|V|²)*w.

    The measuring line lies in the plane through p parallel to the picture.
    Its length is f*length/pz. For paper fit, all four construction points
    undergo the SAME homothety before their straightedge intersections.
    """
    f = c['focal_mm']; noise = perturb or (lambda: 0.0)
    if abs(direction[2]) < 1e-12:
        delta = [f*length/p[2]*direction[i] for i in (0, 1)]
        return add(screen_p, delta), {'parallel': True, 'scale': 1.0}
    v = [f*direction[i]/direction[2] for i in (0, 1)]
    d = sub(v, screen_p)
    if norm(d) < 1e-10:
        return list(screen_p), {'parallel': False, 'collapsed': True, 'scale': 1.0}
    w = [1, 0] if abs(d[1]) >= abs(d[0]) else [0, 1]
    radius = math.copysign(math.sqrt(f*f+dot(v, v)), direction[2])
    m = sub(v, mul(w, radius))
    b = add(screen_p, mul(w, f*length/p[2]))
    points = [screen_p, v, b, m]
    spans = [max(p[i] for p in points)-min(p[i] for p in points) for i in (0, 1)]
    s = 1.0
    while (s*spans[0] > 160 or s*spans[1] > 200
           or s*abs(radius) > 160 or s*f > 160): s /= 2
    pts = [[x*s+noise() for x in pt] for pt in points]
    q = intersection(*pts)
    return mul(q, 1/s), {'parallel': False, 'scale': s,
                          'V': v, 'M': m, 'B': b, 'P': list(screen_p),
                          'span_mm': spans}


def measuring_cube(c, perturb=None):
    points = camera_vertices(c)
    if depth_state(points) != 'finite': raise ValueError('Non-positive depth')
    # One seed by a ray chart; seven tree edges by measuring points.
    seed = ray_chart([points[0]], {**c, 'paper_scale': 1}, perturb=perturb)[0]
    uv = {0: seed}; steps = []
    units = [mul(v, 2/c['edge_mm']) for v in axes(c)]
    for start, end, axis in [(0,4,0), (0,2,1), (0,1,2), (4,6,1),
                             (4,5,2), (2,3,2), (6,7,2)]:
        uv[end], info = measuring_step(points[start], uv[start], units[axis],
                                       c['edge_mm'], c, perturb)
        steps.append({'start': start, 'end': end, 'axis': axis, **info})
    return [mul(uv[i], c['paper_scale']) for i in range(8)], steps
