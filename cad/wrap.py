"""PS5 (original, disc) - wrap-around slab plates, PRE-ALPHA DRAFT (fit untested).
Level lips + constant 40 mm black stripe on face, back and both ends (docs/mockups/wrap_views.png).
Console frame (standing) as slab.py: X width (+X flat/north, -X disc/south), Y depth (+Y front), Z length (0 = drive end).
Not designed yet, shown as placeholders: slide-in clip strips (old glued shelves stand in), stepped seam,
port cut-outs (TODO Job 1D), disc guide tunnel behind the lip."""
import build123d as bd
from cadgen import model
from slab import (P_FLAT, P_DISC, C, CORE_L, FLOOR, ACCENT, COL_PLATE, COL_SHELF, COL_FOOT,
                  internals)

BAND = 40.0                                  # constant black stripe, centred on the core
CLR, LIP = 0.5, 2.5                          # lip-to-core clearance, lip wall thickness
YF = 127.5                                   # core face |y| (proxy), plate floor half-depth (255 / 2)
Z0, Z1 = -CLR, CORE_L + CLR                  # floor and face/back lips span
HEX_F, HEX_W = 6.0, 1.2                      # honeycomb: hole across flats, web -> ~69 % open
FAN_Y, FAN_Z, FAN_R = 3.0, 305.0, 55.0       # fan grille (as slab.py)
SLOT_Z, SLOT_X = (22.5, 145.0), (-25.5, -20.5)   # disc slot, from the stock disc-plate scan
COL_LIP = "#bdbbb5"                          # a shade off the plate so the strips read as separate parts


def box(x0, x1, y0, y1, z0, z1):
    return bd.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * bd.Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def hex_prism(axis, length):
    """hexagonal hole along axis 'x', 'y' or 'z'; flats face the pattern's long direction"""
    r = HEX_F / 3 ** 0.5
    import math
    pts2 = [(r * math.cos(math.radians(90 + 60 * k)), r * math.sin(math.radians(90 + 60 * k))) for k in range(6)]
    # (a, b) = (long dir, short dir) of each face; pointy along b
    put = {"y": lambda a, b: bd.Vector(b, -length / 2, a),      # front/back lips: long = z, short = x
           "z": lambda a, b: bd.Vector(b, a, -length / 2),      # end lips: long = y, short = x
           "x": lambda a, b: bd.Vector(-length / 2, b, a)}[axis]  # floor grille: long = z, short = y
    face = bd.Face(bd.Wire.make_polygon([put(a, b) for b, a in pts2], close=True))
    d = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}[axis]
    return bd.extrude(face, amount=length, dir=d)


def hex_grid(a0, a1, b0, b1, inside=lambda a, b: True, inset=2.5):
    """honeycomb centres in the rectangle a0..a1 (long) x b0..b1 (short)"""
    p, r = HEX_F + HEX_W, HEX_F / 3 ** 0.5
    pts, row, b = [], 0, b0 + inset + r
    while b <= b1 - inset - r:
        a = a0 + inset + HEX_F / 2 + (p / 2 if row % 2 else 0)
        while a <= a1 - inset - HEX_F / 2:
            if inside(a, b):
                pts.append((a, b))
            a += p
        b += p * 0.866
        row += 1
    return pts


def holes(axis, length, at, pts):
    """hex holes at (a, b) grid points, centred on 'at' along the hole axis"""
    t = hex_prism(axis, length)
    pos = {"y": lambda a, b: (b, at, a), "z": lambda a, b: (b, a, at), "x": lambda a, b: (at, b, a)}[axis]
    return bd.Compound([bd.Pos(*pos(a, b)) * t for a, b in pts])


def plate_set(side):
    """side +1 = flat plate (north when lying), -1 = disc plate (south, bottom)"""
    name = "flat" if side > 0 else "disk"
    P = P_FLAT if side > 0 else P_DISC
    out, edge = side * (P + FLOOR), C + side * BAND / 2              # outer surface x, stripe edge x
    xs = sorted((edge, out))
    lo, hi = xs                                                        # lip x range
    fl = sorted((side * P, out))
    parts = []

    # floor tray (one part here; the stepped two-tile seam is not drawn yet)
    floor = box(*fl, -YF, YF, Z0, Z1)
    floor = bd.fillet(floor.edges().filter_by(bd.Axis.X), 3)
    fan = [(a, b) for a, b in hex_grid(FAN_Z - FAN_R, FAN_Z + FAN_R, FAN_Y - FAN_R, FAN_Y + FAN_R)
           if (a - FAN_Z) ** 2 + (b - FAN_Y) ** 2 <= (FAN_R - HEX_F / 2) ** 2]
    floor = floor - holes("x", FLOOR + 2, (fl[0] + fl[1]) / 2, fan)
    floor.color, floor.label = COL_PLATE, f"plate_{name}"
    parts.append(floor)

    # face / back lip strips: wall in front of the core face, 0.5 tab up to the floor edge for the weld
    for ys, tag in ((+1, "face"), (-1, "back")):
        y_in, y_out = ys * (YF + CLR), ys * (YF + CLR + LIP)
        wall = box(lo, hi, y_in, y_out, Z0, Z1) + box(*fl, ys * YF, y_in, Z0, Z1)
        if tag == "back":
            vent = hex_grid(Z0, Z1, lo, hi)                                # exhaust: vented end to end
        else:
            vent = hex_grid(CORE_L - 120, Z1, lo, hi)                      # fan end only
            if side < 0:                                                   # disc slot, scan-derived
                wall = wall - box(*SLOT_X, y_in - 1, y_out + 1, *SLOT_Z)
        wall = wall - holes("y", LIP + 2, (y_in + y_out) / 2, vent)
        extras = []
        if tag == "face" and side > 0:                                     # colour inserts, seen from the sofa
            xc = (lo + hi) / 2
            for k, col in enumerate(ACCENT):
                z = 42 - k * 4
                wall = wall - box(xc - 7.1, xc + 7.1, y_out - 0.61, y_out + 0.01, z - 1.3, z + 1.3)
                ins = box(xc - 7, xc + 7, y_out - 0.6, y_out, z - 1.25, z + 1.25)
                ins.color, ins.label = col, f"insert_{k}"
                extras.append(ins)
        wall.color, wall.label = COL_LIP, f"lip_{tag}_{name}"
        parts += [wall] + extras

    # end lip strips: wrap the short ends and the lip corners, fully vented
    yo = YF + CLR + LIP
    for z_in, z_out, tag in ((Z1, Z1 + LIP, "west"), (Z0, Z0 - LIP, "east")):
        zz = sorted((z_in, z_out))
        wall = box(lo, hi, -yo, yo, *zz)
        wall = wall - holes("z", LIP + 2, (z_in + z_out) / 2, hex_grid(-yo, yo, lo, hi))
        wall.color, wall.label = COL_LIP, f"lip_{tag}_{name}"
        parts.append(wall)

    if side < 0:                                                           # TPU feet on the bottom plate
        for y in (-95, 95):
            for z in (35, 345):
                f = bd.Pos(out - 6, y, z) * bd.Rot(0, 90, 0) * bd.Cylinder(10, 12)
                f.color, f.label = COL_FOOT, "foot"
                parts.append(f)
    return parts


def assembly(lying=True):
    kids = plate_set(+1) + plate_set(-1)
    for k in internals():
        if k.label.startswith("shelf_"):
            k.label = "clip_placeholder_" + k.label[6:]                    # slide-in strips not designed yet
            k.color = COL_SHELF
        kids.append(k)
    a = bd.Compound(children=kids, label="ps5_wrap_draft")
    return bd.Rot(0, -90, 0) * a if lying else a


@model
def wrap_horizontal():
    return assembly(lying=True)


if __name__ == "__main__":
    wrap_horizontal()
