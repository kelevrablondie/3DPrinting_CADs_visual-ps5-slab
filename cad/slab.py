"""PS5 (original, disc) – level 'slab' side plates, horizontal use.
Console frame (standing): X width (+X flat side, -X disc side), Y depth (+Y front), Z height (0 = bottom end).
Glue planes and clip shelves come from the Rhys34512 scan (CC BY-NC 4.0); core proxy from scan + tape measurements."""
import json
from pathlib import Path
import build123d as bd
from cadgen import model, read_step

HERE = Path(__file__).resolve().parent
CORE = HERE / "core"
# ---- measured / derived ----------------------------------------------------------
P_FLAT, P_DISC = 59.2, 54.8        # glue planes (|x|), 114 mm apart
C = 2.2                            # core centre x
CORE_L = 380.0
WF0, WF1 = 40.0, 75.0              # core front-face width at bottom / top end
WR0, WR1 = 80.0, 45.0              # core rear-face width at bottom / top end
DRIVE_Z = 135.0                    # drive spans z 0..135 on the disc side
# ---- design parameters -----------------------------------------------------------
L, D = 384.0, 255.0                # plate outline: length (z), depth (y); 255 fits the 256 bed with one seam
Z_MID = CORE_L / 2
FLOOR, WALL, R = 2.5, 2.5, 10.0
REVEAL = 4.0                       # gap between straight skirt edge and core face edge
POCKET = 0.8                       # shelf alignment pockets
# end wall edge |x| at rear, front (y = -+D/2), from analysis/end_edges.py; rerun it if the core proxy changes
END_FLAT, END_DISC = (48.5, 35.3), (39.9, 46.3)
COL_PLATE, COL_CORE, COL_DRIVE = "#c6c4be", "#1d1d1f", "#dcdcd8"
COL_SHELF, COL_FOOT = "#8c8c8c", "#3a3a3c"
ACCENT = ["#d8343a", "#e8b923", "#2fa58f", "#3b6fc4"]

POCKETS = json.loads((HERE / "pockets.json").read_text())
GRILLE = json.loads((HERE / "grille.json").read_text())


def outline(x, inset=0.0):
    return bd.Plane.YZ.offset(x) * bd.Pos(0, Z_MID) * bd.RectangleRounded(D - 2 * inset, L - 2 * inset, R - inset)


def edge_line(a0, a1):
    """straight skirt edge |x|(z) through (a0 at z=0) and (a1 at z=CORE_L), extended past both ends"""
    f = lambda z: a0 + (a1 - a0) * z / CORE_L
    return [(0, -10), (f(-10), -10), (f(L), L), (0, L)]


def prism_xz(pts, ydir):
    """polygon given in (x, z) at y=0, extruded across the front (+1) or rear (-1) half"""
    face = bd.Face(bd.Wire.make_polygon([bd.Vector(x, 0, z) for x, z in pts], close=True))
    return bd.extrude(face, amount=D, dir=(0, ydir, 0))


def end_wall_cut(edge, rear, front, z0, z1):
    """everything below the slanted end wall edge; ramps to the skirt edges (rear, front) around the corners"""
    r, f = edge
    at = lambda y: r + (f - r) * (y + D / 2) / D
    ya, yb = -D / 2 + R, D / 2 - R
    pts = [(0, -D / 2 - 1), (rear, -D / 2 - 1), (rear, -D / 2), (at(ya), ya), (at(yb), yb),
           (front, D / 2), (front, D / 2 + 1), (0, D / 2 + 1)]
    face = bd.Face(bd.Wire.make_polygon([bd.Vector(x, y, z0) for x, y in pts], close=True))
    return bd.extrude(face, amount=z1 - z0, dir=(0, 0, 1))


def plate(side):
    """side +1 = flat plate (built at +X); -1 = disc plate (built at +X, mirrored)."""
    P = P_FLAT if side > 0 else P_DISC
    c = C * side                                   # core centre offset seen from this side
    af0, af1 = c + WF0 / 2 + REVEAL, c + WF1 / 2 + REVEAL
    ar0, ar1 = c + WR0 / 2 + REVEAL, c + WR1 / 2 + REVEAL
    x_in = min(af0, af1, ar0, ar1) - 1
    floor = bd.extrude(outline(P), amount=FLOOR)
    floor = bd.fillet(floor.edges().group_by(bd.Axis.X)[-1], 1.5)
    ring = bd.extrude(outline(x_in), amount=P - x_in) - bd.extrude(outline(x_in - 1, WALL), amount=P - x_in + 2)
    rear_cut = prism_xz(edge_line(ar0, ar1), -1)
    front_cut = prism_xz(edge_line(af0, af1), +1)
    # each end is a wedge: the core nearly fills one side (no wall), the other gets a slanted wall
    tan0, tan1 = R - 2, L - R - 2                                    # where the outline's end corners meet its long sides
    ar, af = lambda z: ar0 + (ar1 - ar0) * z / CORE_L, lambda z: af0 + (af1 - af0) * z / CORE_L
    if side > 0:
        w0, w1, z0, z1, edge, tan = -10, tan0, L - R - 3, L + 5, END_FLAT, tan0
    else:
        w0, w1, z0, z1, edge, tan = tan1, L + 5, -10, R + 1, END_DISC, tan1
    wall_zone = bd.Pos(P / 2, 0, (w0 + w1) / 2) * bd.Box(P, D + 10, w1 - w0)
    ring = ring - (rear_cut - wall_zone) - (front_cut - wall_zone)   # skirt cuts would notch the wall
    ring = ring - end_wall_cut(edge, ar(tan), af(tan), w0, w1)
    ring = ring - bd.Pos(P / 2, 0, (z0 + z1) / 2) * bd.Box(P, D + 10, z1 - z0)
    if side < 0:                                                     # drive notch: frame the drive face
        ring = ring - bd.Pos(P / 2, D / 2, DRIVE_Z / 2) * bd.Box(P, 60, DRIVE_Z + 2 * REVEAL + 10)
    body = floor + ring
    name = "flat" if side > 0 else "disk"
    holes = [bd.Pos(P + FLOOR / 2, y, z) * bd.Rot(0, 90, 0) * bd.Cylinder(1.7, FLOOR + 2) for y, z in GRILLE[name]]
    pockets = [bd.extrude(bd.Face(bd.Wire.make_polygon([bd.Vector(P - 0.01, y, z) for y, z in pts], close=True)),
                          amount=POCKET + 0.01, dir=(1, 0, 0)) for pts in POCKETS[name]]
    body = body - bd.Compound(holes) - bd.Compound(pockets)
    extras = []
    if side > 0:                                                     # decorative four-colour inserts
        for k, col in enumerate(ACCENT):
            z = 26 + k * 18
            body = body - bd.Pos(P + FLOOR - 0.3, D / 2 - 14, z) * bd.Box(0.61, 2.6, 14.2)
            ins = bd.Pos(P + FLOOR - 0.3, D / 2 - 14, z) * bd.Box(0.6, 2.5, 14.0)
            ins.color, ins.label = col, f"insert_{k}"
            extras.append(ins)
    else:                                                            # TPU feet
        for y in (-95, 95):
            for z in (35, 345):
                f = bd.Pos(P + FLOOR + 6, y, z) * bd.Rot(0, 90, 0) * bd.Cylinder(10, 12)
                f.color, f.label = COL_FOOT, "foot"
                extras.append(f)
    body.color, body.label = COL_PLATE, f"plate_{name}"
    parts = [body] + extras
    if side < 0:
        parts = [bd.mirror(p, bd.Plane.YZ) for p in parts]
        for p, q in zip(parts, [body] + extras):
            p.color, p.label = q.color, q.label
    return parts


def internals(with_shelves=True):
    core = read_step(CORE / "core_final.step"); core.color, core.label = COL_CORE, "core"
    drive = read_step(CORE / "drive_proxy.step"); drive.color, drive.label = COL_DRIVE, "drive"
    kids = [core, drive]
    if with_shelves:
        for f in sorted(CORE.glob("shelf_*_c.step")):
            s = read_step(f); s.color, s.label = COL_SHELF, f.stem.replace("_c", "")
            kids.append(s)
    return kids


def assembly(lying=True, with_core=True):
    kids = plate(+1) + plate(-1) + (internals() if with_core else [])
    a = bd.Compound(children=kids, label="ps5_slab")
    return bd.Rot(0, -90, 0) * a if lying else a


@model
def slab_horizontal():
    return assembly(lying=True)


@model
def slab_standing():
    return assembly(lying=False)


if __name__ == "__main__":
    slab_standing()
    slab_horizontal()
