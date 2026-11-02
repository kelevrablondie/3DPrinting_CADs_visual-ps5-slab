"""Shelf alignment-pocket outlines and fan-grille hole list, in the console frame -> cad/pockets.json, cad/grille.json.
Console frame: y = Y_local - 130.75, z = Z_local - 4 (scan local = panel bounding-box min corner)."""
import json, math
from pathlib import Path
from shapely.geometry import box as sbox, LineString, Polygon, Point
from shapely.ops import unary_union
ROOT = Path(__file__).resolve().parents[1]
G = json.load(open(ROOT / "tools/shelf_groups.json"))
EXT = {"flat": (261.49, 388.23), "disk": (260.38, 387.87)}
CLEAR = 0.15                          # pocket clearance around each shelf footprint
FAN_Y, FAN_Z, FAN_R, PITCH, KEEPOUT = 3.0, 305.0, 60.0, 5.0, 2.5
pockets, grille = {}, {}
for name, groups in G.items():
    W, H = EXT[name]; polys = []
    for clips in groups.values():
        parts = [sbox(y-(12 if t=="L" else 10), z-(21 if t=="L" else 16), y+(12 if t=="L" else 10), z+(21 if t=="L" else 16)) for y, z, t in clips]
        parts += [LineString([(a[0], a[1]), (b[0], b[1])]).buffer(7, cap_style=2) for a, b in zip(clips, clips[1:])]
        fp = unary_union(parts).buffer(2).buffer(-2).intersection(sbox(1, 1, W-1, H-1)).buffer(CLEAR)
        polys.append([[round(y-130.75, 2), round(z-4, 2)] for y, z in list(fp.exterior.coords)[:-1]])
    pockets[name] = polys
    keep = unary_union([Polygon(p) for p in polys]).buffer(KEEPOUT)
    holes, j, y = [], 0, -FAN_R
    while y <= FAN_R:
        x = -FAN_R + (j % 2) * PITCH / 2
        while x <= FAN_R:
            if math.hypot(x, y) <= FAN_R and not keep.contains(Point(FAN_Y+x, FAN_Z+y)):
                holes.append([round(FAN_Y+x, 2), round(FAN_Z+y, 2)])
            x += PITCH
        y += PITCH * math.sqrt(3) / 2; j += 1
    grille[name] = holes
json.dump(pockets, open(ROOT / "cad/pockets.json", "w")); json.dump(grille, open(ROOT / "cad/grille.json", "w"))
print({k: len(v) for k, v in grille.items()}, "grille holes")
