"""PS5 (original, disc) - wrap-around slab plates, PRE-ALPHA DRAFT (fit untested).
Level lips + constant ~48 mm black stripe on face, back and both ends (docs/mockups/wrap_views.png).
Console frame (standing) as slab.py: X width (+X flat/north, -X disc/south), Y depth (+Y front), Z length (0 = drive end).
Not designed yet, shown as placeholders: slide-in clip strips (old glued shelves stand in), stepped seam.
The black stripe is widened on the disc side so rear plugs fit without notches, except on the face: there the south
lip covers the core out to its narrowest face edge (no filler seam), the disc slot is cut through the lip and a
hidden guide welded into it carries the slot back to the drive entry."""
import build123d as bd
from cadgen import model
from slab import (P_FLAT, P_DISC, C, CORE_L, FLOOR, ACCENT, COL_PLATE, COL_SHELF, COL_FOOT, COL_CORE,
                  WF0, WF1, internals)

# black stripe edges (x), same on face, back and both ends. The disc side sits at the disc slot's outer edge, so
# rear plugs need no notches and the slot lies inside the stripe (~48 mm wide; north lip 39.5, south ~32)
STRIPE = (-25.5, C + 20.0)
CLR, LIP = 0.5, 2.5                          # lip-to-core clearance, lip wall thickness
YF = 127.5                                   # core face |y| (proxy), plate floor half-depth (255 / 2)
Z0, Z1 = -CLR, CORE_L + CLR                  # floor and face/back lips span
HEX_F, HEX_W = 6.0, 1.2                      # honeycomb: hole across flats, web -> ~69 % open
FAN_Y, FAN_Z = 3.0, 305.0                     # fan centre (as slab.py)
SLOT_Z, SLOT_X = (22.5, 145.0), (-25.5, -20.5)   # disc slot, from the stock disc-plate scan
SLOT_Y, GUIDE = 111.0, 2.0                   # drive entry depth (stock slot gap), guide floor thickness
COL_LIP = "#bdbbb5"                         # a shade off the plate so the strips read as separate parts
ENGRAVE, GROOVE = 0.4, 1.0                   # engraving depth, panel-line width
# tile seam as a faceted panel line (y, z): clears every clip of BOTH plates by >= 3 mm
SEAM = [(-YF - 3, 164.0), (-70.0, 164.0), (-64.0, 158.0), (YF + 3, 158.0)]
PANEL_H, PANEL_C = 62.0, 14.0                # fan panel: half size, corner chamfer (hides the round fan)
# slide-in clip strips: the scanned hook shelves keep their hooks; their base becomes a dovetail tongue in rails on
# the plate floor. Plates slide off along z (flat +z, disc -z, as slab.py's end-wall check): the end stop takes that pull.
RAIL_W, RAIL_H, DOVE = 4.0, 4.0, 1.5        # rail width, height, dovetail overhang into the channel
FIT = 0.2                                   # strip-to-rail sliding clearance
STOP, LEDGE, PAD = 4.0, 3.0, 4.0            # end stop thickness, latch ledge length, thumb pad length
COL_STRIP = "#8c8c8c"
FONT = "/usr/share/fonts/source-foundry-hack-fonts/Hack-Regular.ttf"
NAME = "[MONOLITH] U-05"
# shortcut: clip footprints (y0, y1, z0, z1) copied from cad/core/shelf_*_c.stl bounds; regenerate when the
# slide-in clip strips are designed
SHELVES = {"flat": [(-116, 118, 17, 50), (-118, -45, 170, 366), (-59, 39, 174, 251), (60, 104, 209, 337),
                    (97, 117, 123, 155)],
           "disk": [(-117, -97, 17, 49), (-118, -45, 167, 365), (-61, 41, 161, 251), (60, 84, 294, 336)]}


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


def panel_pts():
    y0, z0, h, c = FAN_Y, FAN_Z, PANEL_H, PANEL_C
    return [(y0 - h + c, z0 - h), (y0 + h - c, z0 - h), (y0 + h, z0 - h + c), (y0 + h, z0 + h - c),
            (y0 + h - c, z0 + h), (y0 - h + c, z0 + h), (y0 - h, z0 + h - c), (y0 - h, z0 - h + c)]


def top_groove(pts, x_top, closed=False):
    """1 mm panel line, ENGRAVE deep, along (y, z) points on the outer face at x_top (+X side)"""
    pts = pts + pts[:1] if closed else pts
    cut = []
    for (y0, z0), (y1, z1) in zip(pts, pts[1:]):
        dy, dz = y1 - y0, z1 - z0
        n = (dy * dy + dz * dz) ** 0.5
        oy, oz = -dz / n * GROOVE / 2, dy / n * GROOVE / 2
        quad = [(y0 + oy, z0 + oz), (y1 + oy, z1 + oz), (y1 - oy, z1 - oz), (y0 - oy, z0 - oz)]
        face = bd.Face(bd.Wire.make_polygon([bd.Vector(x_top + 0.01, y, z) for y, z in quad], close=True))
        cut.append(bd.extrude(face, amount=ENGRAVE + 0.01, dir=(-1, 0, 0)))
    for y, z in pts:                                                   # round the joints
        cut.append(bd.Pos(x_top, y, z) * bd.Rot(0, 90, 0) * bd.Cylinder(GROOVE / 2, 2 * ENGRAVE))
    return bd.Compound(cut)


def top_text(txt, size, y_base, z_start, x_top):
    """engraved text on the +X outer face, reading +Z (left to right seen from the front), glyph tops toward -Y"""
    pl = bd.Plane(origin=(x_top + 0.01, y_base, z_start), x_dir=(0, 0, 1), z_dir=(1, 0, 0))
    t = pl * bd.Text(txt, font_size=size, font_path=FONT, align=(bd.Align.MIN, bd.Align.MIN))
    solid = bd.extrude(t, amount=ENGRAVE + 0.01, dir=(-1, 0, 0))
    assert solid.volume > 0, txt
    return solid


def filler(y_in):
    """hidden filler behind the south face lip at the drive end, where the core face (tape loft) is narrower than the
    stripe. It is the disc guide: the slot runs through it back to the drive entry. Printed as one with the face lip."""
    x0 = STRIPE[0]
    core_edge = lambda z: C - (WF0 + (WF1 - WF0) * z / CORE_L) / 2         # disc-side core face edge
    z_end = (C - x0) * 2 - WF0                                             # where the face reaches the stripe edge
    z_end = z_end * CORE_L / (WF1 - WF0)
    tri = [(x0, Z0), (core_edge(Z0), Z0), (x0, z_end)]
    face = bd.Face(bd.Wire.make_polygon([bd.Vector(x, SLOT_Y, z) for x, z in tri], close=True))
    f = bd.extrude(face, amount=y_in - SLOT_Y, dir=(0, 1, 0))
    f += box(x0 - GUIDE, x0, SLOT_Y, YF + CLR, *SLOT_Z)                   # slot floor behind the lip
    return f - box(*SLOT_X, SLOT_Y - 1, y_in + 1, *SLOT_Z)


def clip_strip(shelf, side):
    """(plate features, strip) for one scanned hook shelf. Rails, end stop and latch ledge are plate (one with the
    tile); the strip is the shelf minus them, so its base comes out as the matching dovetail tongue."""
    b = shelf.bounding_box()
    y0, y1, z0, z1 = b.min.Y, b.max.Y, b.min.Z, b.max.Z
    x_fl = side * P_FLAT if side > 0 else side * P_DISC                # floor inner face
    xr = lambda d: x_fl - side * d                                     # d mm up from the floor, toward the core
    def rail(y_edge, inward, grow=0.0):                                # dovetail rail profile in (y, x), along z
        w, o = RAIL_W + grow, DOVE + grow
        pts = [(y_edge, 0), (y_edge + inward * w, 0), (y_edge + inward * (w + o), RAIL_H + grow),
               (y_edge, RAIL_H + grow)]
        f = bd.Face(bd.Wire.make_polygon([bd.Vector(xr(d), y, z0 - 1) for y, d in pts], close=True))
        return bd.extrude(f, amount=z1 - z0 + 2, dir=(0, 0, 1))
    # stop at the end the console pulls the strip toward when the plate slides off; latch at the open end
    zs, zo = (z0, z1) if side > 0 else (z1, z0)
    sgn = 1 if zo > zs else -1                                         # stop -> open direction
    stop = box(*sorted((xr(0), xr(RAIL_H))), y0, y1, *sorted((zs, zs - sgn * STOP)))
    ledge = box(*sorted((xr(0), xr(1.5))), y0 + RAIL_W + DOVE, y1 - RAIL_W - DOVE,
                *sorted((zo - sgn * 6, zo - sgn * (6 - LEDGE))))
    plate_bits = rail(y0, +1) + rail(y1, -1) + stop + ledge
    cut = rail(y0, +1, FIT) + rail(y1, -1, FIT) + box(*sorted((xr(-1), xr(1.5 + FIT))),
                                                      y0 + RAIL_W + DOVE, y1 - RAIL_W - DOVE,
                                                      *sorted((zo - sgn * (6 + FIT), zo - sgn * (6 - LEDGE - FIT))))
    cut += box(*sorted((x_fl, x_fl + side * 5)), y0 - 1, y1 + 1, z0 - 1, z1 + 1)   # old 0.8 glue pocket: sit on the floor
    strip = (bd.Solid(shelf) if isinstance(shelf, bd.Shell) else shelf) - cut   # mesh STEP reads as a shell
    assert strip.volume > 0.5 * bd.Solid(shelf).volume, shelf.label
    # shortcut: thumb pad only marks the latch; the flex arm is not modelled. Model it with the hook rebuild
    strip = strip + box(*sorted((xr(1.6), xr(4.0))), y0 + RAIL_W + DOVE, y1 - RAIL_W - DOVE,
                        *sorted((zo, zo + sgn * PAD)))
    strip.color, strip.label = COL_STRIP, "clip_strip_" + shelf.label[6:]
    return plate_bits, strip


def plate_set(side):
    """side +1 = flat plate (north when lying), -1 = disc plate (south, bottom)"""
    name = "flat" if side > 0 else "disk"
    P = P_FLAT if side > 0 else P_DISC
    out, edge = side * (P + FLOOR), STRIPE[side > 0]                   # outer surface x, stripe edge x
    xs = sorted((edge, out))
    lo, hi = xs                                                        # lip x range
    fl = sorted((side * P, out))
    parts = []

    # floor tray (one part here; the stepped two-tile seam is not drawn yet)
    floor = box(*fl, -YF, YF, Z0, Z1)
    floor = bd.fillet(floor.edges().filter_by(bd.Axis.X), 3)
    h, m = PANEL_H - 4, HEX_F / 2 + 2.5                               # hole field inside the panel line
    def keep(z, y):
        dy, dz = abs(y - FAN_Y), abs(z - FAN_Z)
        if dy > h - m or dz > h - m or dy + dz > 2 * PANEL_H - PANEL_C - 6 - m:
            return False
        return not any(y0 - m < y < y1 + m and z0 - m < z < z1 + m for y0, y1, z0, z1 in SHELVES[name])
    fan = hex_grid(FAN_Z - PANEL_H, FAN_Z + PANEL_H, FAN_Y - PANEL_H, FAN_Y + PANEL_H, inside=keep)
    floor = floor - holes("x", FLOOR + 2, (fl[0] + fl[1]) / 2, fan)
    if side > 0:                                                      # north top: panel lines + markings
        x_top = out
        floor = floor - top_groove(SEAM, x_top) - top_groove(panel_pts(), x_top, closed=True)
        floor = floor - top_text(NAME, 5.0, YF - 7, 20, x_top)
        floor = floor - top_text("INTAKE", 3.5, FAN_Y + PANEL_H + 11, FAN_Z - 6, x_top)
        for k in range(8):                                             # tick row left of INTAKE
            z = FAN_Z - 40 + 3 * k
            floor = floor - box(x_top - ENGRAVE, x_top + 0.01, FAN_Y + PANEL_H + 7, FAN_Y + PANEL_H + 11, z - 0.4, z + 0.4)
    strips = [k for k in internals() if k.label.startswith(f"shelf_{name}_")]
    built = [clip_strip(k, side) for k in strips]
    for i, (plate_bits, strip) in enumerate(built):
        for j, (_, other) in enumerate(built):                         # overlapping footprints: neighbours win
            if j != i:
                plate_bits = plate_bits - other
        floor = floor + plate_bits
        parts.append(strip)
    floor.color, floor.label = COL_PLATE, f"plate_{name}"
    parts.append(floor)

    # face / back lip strips: wall in front of the core face, 0.5 tab up to the floor edge for the weld
    for ys, tag in ((+1, "face"), (-1, "back")):
        y_in, y_out = ys * (YF + CLR), ys * (YF + CLR + LIP)
        # south face lip covers the core out to its narrowest face edge, so the black seen there is core only
        hi_w = C - WF0 / 2 if (tag == "face" and side < 0) else hi
        wall = box(lo, hi_w, y_in, y_out, Z0, Z1) + box(*fl, ys * YF, y_in, Z0, Z1)
        if tag == "face" and side < 0:                                     # disc slot through the lip + guide
            wall = wall + filler(y_in) - box(*SLOT_X, y_in - 1, y_out + 1, *SLOT_Z)
            for z0, z1 in ((Z0 - LIP, Z0), (Z1, Z1 + LIP)):               # square corners over the end lips
                wall = wall + box(hi, hi_w, y_in, y_out, z0, z1)
        if tag == "back":
            vent = hex_grid(Z0, Z1, lo, hi)                                # exhaust: vented end to end
        else:
            vent = hex_grid(CORE_L - 120, Z1, lo, hi)                      # fan end only
        wall = wall - holes("y", LIP + 2, (y_in + y_out) / 2, vent)
        zs = SEAM[-1][1] if ys > 0 else SEAM[0][1]                      # lip split line continues the seam
        wall = wall - box(lo, hi_w, y_out - ys * ENGRAVE, y_out + ys * 0.01, zs - GROOVE / 2, zs + GROOVE / 2)
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
    kids += [k for k in internals() if not k.label.startswith("shelf_")]   # shelves now live in the clip strips
    a = bd.Compound(children=kids, label="ps5_wrap_draft")
    return bd.Rot(0, -90, 0) * a if lying else a


@model
def wrap_horizontal():
    return assembly(lying=True)


if __name__ == "__main__":
    wrap_horizontal()
