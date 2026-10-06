"""Generate an original schematic head, not a copy of a downloaded mesh.

The numeric ratios are teaching examples, not measurements of cgmonkey's model.
No third-party dependencies. Run from any directory with Python 3.
"""

from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parent
LEVELS = [0, .06, .12, .178, .267, .40, .50, .533, .80, .94, 1]
WIDTHS = [.11, .145, .205, .25, .292, .322, 1/3, .33, .302, .225, .075]
FRONTS = [.20, .28, .285, .28, .29, .29, .28, .30, .25, .13, -.01]
BACKS = [-.025, -.07, -.16, -.25, -.34, -.41, -.45, -.45, -.40, -.29, -.15]
COLS = [-1, -.65, -.20, 0, .20, .65, 1]


def vertices(stage):
    points = []
    for row, y in enumerate(LEVELS):
        w, front, back = WIDTHS[row], FRONTS[row], BACKS[row]
        if stage == 0:
            w, front, back = 1/3, .383, -.45
        edge = .05 if stage else front
        for u in COLS:
            z = front if abs(u) <= .65 else edge
            if stage >= 2:
                # Central nose wedge and lateral eye recesses.
                if abs(u) <= .20 and row in (4, 5, 6, 7):
                    z += {4: .093, 5: .064, 6: .032, 7: .005}[row]
                if abs(u) == .65 and row == 6:
                    z -= .075
                if abs(u) == .65 and row == 5:
                    z += .024
            if stage >= 3:
                # Shallow mouth volume and chin. No detailed eyelids or lips.
                if abs(u) <= .65 and row in (1, 2, 3):
                    z += {1: .028, 2: .018, 3: .035}[row]
            points.append([round(u*w, 6), y, round(z, 6)])
        # Continue around the right side, back, and left side of the section.
        side_x = w if stage == 0 else w*.88
        back_width = w if stage == 0 else w*.65
        points.extend([
            [round(side_x, 6), y, round(back*.65, 6)],
            [round(back_width, 6), y, back],
            [0, y, back],
            [round(-back_width, 6), y, back],
            [round(-side_x, 6), y, round(back*.65, 6)],
        ])
    return points


def faces():
    result = []
    n = 12
    for r in range(len(LEVELS)-1):
        for i in range(n):
            j = (i+1) % n
            result.append([r*n+i, r*n+j, (r+1)*n+j, (r+1)*n+i])
    result.append(list(reversed(range(n))))
    result.append(list(range((len(LEVELS)-1)*n, len(LEVELS)*n)))
    return result


def ears():
    points, polys = [], []
    # Separate closed volumes; intentionally not welded to the head.
    for s in (1, -1):
        start = len(points)
        points.extend([
            [s*.305, .29, -.12], [s*.305, .50, -.12],
            [s*.37, .47, -.10], [s*.36, .32, -.10],
            [s*.305, .29, -.21], [s*.305, .50, -.21],
            [s*.37, .47, -.18], [s*.36, .32, -.18],
        ])
        local = [[0,3,2,1], [4,5,6,7], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]]
        if s == -1:
            local = [list(reversed(f)) for f in local]
        polys.extend([[i+start for i in f] for f in local])
    return points, polys


data = {
    "stages": [vertices(i) for i in range(4)],
    "faces": faces(),
    "ears": dict(zip(("vertices", "faces"), ears())),
    "ratios": {"height": 1, "widthWithoutEars": 2/3, "depthIncludingNose": .833},
    "provenance": "Original schematic; not measured from or extracted from cgmonkey's model.",
}
ROOT.joinpath("model-data.json").write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")

v = data["stages"][3]
ep, ef = ears()
obj = ["# Original schematic head for construction practice",
       "# Ratios are illustrative, not measurements of an external model.",
       "o schematic_head"]
obj += ["v " + " ".join(f"{x:.6f}" for x in p) for p in v+ep]
obj += ["f " + " ".join(str(i+1) for i in f) for f in data["faces"]]
obj.append("g ears_separate_volumes")
obj += ["f " + " ".join(str(i+len(v)+1) for i in f) for f in ef]
ROOT.joinpath("schematic-planar-head.obj").write_text("\n".join(obj)+"\n", encoding="utf-8")

# Check the generated geometry, rather than inventing reconstruction accuracy.
for name, points, polys in (("head", v, data["faces"]), ("ears", ep, ef)):
    assert all(math.isfinite(x) for p in points for x in p)
    edges = {}
    for f in polys:
        assert len(set(f)) == len(f)
        for a, b in zip(f, f[1:]+f[:1]):
            assert 0 <= a < len(points) and 0 <= b < len(points)
            key = tuple(sorted((a,b)))
            edges[key] = edges.get(key, 0)+1
    assert all(n == 2 for n in edges.values()), f"Open edge in {name}"
assert len(v) == 132
print(f"Generated {len(v)+len(ep)} vertices; {len(data['faces'])+len(ef)} polygon faces.")
print("Head and separate ear volumes have two incident faces per edge.")
