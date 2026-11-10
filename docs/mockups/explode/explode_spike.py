"""THROWAWAY spike (2026-11-10): exploded views for Mike to react to, not product code.
Run from the repo root: cadgen +0.8.4 run docs/mockups/explode/explode_spike.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "cad"))
import build123d as bd
from cadgen import model
import wrap

GREY, LIP, BLACK, STRIP, TAB, RED = "#c6c4be", "#bdbbb5", "#1d1d1f", "#8c8c8c", "#e8b923", "#d8343a"


def B(x0, x1, y0, y1, z0, z1, col, lab):
    b = wrap.box(x0, x1, y0, y1, z0, z1); b.color, b.label = col, lab
    return b


def arrow(p, d, length, col=RED, lab="arrow"):
    """arrow from point p along unit axis d ('x','y','z' with sign)"""
    ax = {"x": (0, 90, 0), "-x": (0, -90, 0), "y": (-90, 0, 0), "-y": (90, 0, 0), "z": (0, 0, 0), "-z": (180, 0, 0)}[d]
    shaft = bd.Pos(0, 0, length / 2) * bd.Cylinder(1.2, length)
    head = bd.Pos(0, 0, length) * bd.Cone(3, 0, 7)
    a = bd.Pos(*p) * bd.Rot(*ax) * (shaft + head); a.color, a.label = col, lab
    return a


@model
def explode_overall():
    """whole set: north plate up, south plate down, clip strips floating between, core in the middle"""
    kids = []
    for side, dx in ((+1, 190), (-1, -190)):
        for p in wrap.plate_set(side):
            if p.label.startswith("foot"):
                continue
            q = bd.Pos(dx, 0, 0) * p; q.color, q.label = p.color, p.label; kids.append(q)
    for k in wrap.internals():
        if k.label.startswith("shelf_"):                         # clip strips: halfway out
            dx = 95 if ("flat" in k.label) else -45
            q = bd.Pos(dx, 0, 0) * k; q.color, q.label = STRIP, "clip_strip_" + k.label[6:]
        else:
            q = k
        kids.append(q)
    return bd.Rot(0, -90, 0) * bd.Compound(children=kids, label="exploded_overall")


@model
def explode_strip():
    """one clip strip in its channel on a plate offcut (local frame: plate floor in XY, strip slides along X)"""
    L, W, F = 110.0, 40.0, 2.5                    # offcut length, width, floor
    CH, RW, RH = 14.0, 4.0, 4.0                   # channel width, rail width, rail height
    kids = [B(0, L, -W / 2, W / 2, -F, 0, GREY, "plate_offcut")]
    # dovetail rails (overhang 1.5 mm into the channel at the top)
    for s in (-1, 1):
        y_in = s * CH / 2
        pts = [(y_in, 0), (y_in + s * RW, 0), (y_in + s * RW, RH), (y_in - s * 1.5, RH)]
        f = bd.Face(bd.Wire.make_polygon([bd.Vector(0, y, z) for y, z in pts], close=True))
        r = bd.extrude(f, amount=L - 10, dir=(1, 0, 0)); r.color, r.label = GREY, "dovetail_rail"
        kids.append(r)
    kids.append(B(L - 10, L - 4, -CH / 2 - RW, CH / 2 + RW, 0, RH, GREY, "end_stop"))      # closed end
    kids.append(B(6, 9, -CH / 2 + 2, CH / 2 - 2, 0, 1.5, GREY, "latch_ledge"))              # open end
    # strip: exploded up (+Z 30) and back out of the channel (-X 40)
    ox, oz = -40.0, 30.0
    sl = 80.0
    pts = [(-CH / 2 + 0.3, 0), (CH / 2 - 0.3, 0), (CH / 2 - 0.3 + 1.2, RH - 0.2), (-CH / 2 + 0.3 - 1.2, RH - 0.2)]
    f = bd.Face(bd.Wire.make_polygon([bd.Vector(ox + 12, y, oz + z) for y, z in pts], close=True))
    base = bd.extrude(f, amount=sl, dir=(1, 0, 0))
    base += wrap.box(ox + 12, ox + 12 + sl, -CH / 2 + 0.3, CH / 2 - 0.3, oz + RH - 0.2, oz + RH + 3)
    for hx in (ox + 30, ox + 70):                                                # two hooks: shaft + lip
        base += wrap.box(hx, hx + 6, -4, 4, oz + RH + 3, oz + RH + 15)
        base += wrap.box(hx - 4, hx + 6, -4, 4, oz + RH + 12, oz + RH + 15)
    base.color, base.label = STRIP, "clip_strip"
    kids.append(base)
    tab = wrap.box(ox, ox + 12, -4, 4, oz + 1.2, oz + 2.4)                       # flex arm
    tab += wrap.box(ox, ox + 3, -4, 4, oz - 1.0, oz + 1.2)                       # catch under the arm
    tab += wrap.box(ox - 6, ox, -6, 6, oz + 1.2, oz + 4.0)                       # thumb pad
    tab.color, tab.label = TAB, "thumb_latch"
    kids.append(tab)
    kids += [arrow((ox + 50, 0, oz - 4), "-z", 18, lab="1_drop_into_channel"),
             arrow((ox + 95, 0, oz + 8), "x", 22, lab="2_slide_to_end_stop"),
             arrow((ox - 3, 0, oz + 22), "-z", 12, col="#3b6fc4", lab="press_to_release")]
    return bd.Compound(children=kids, label="exploded_strip")


if __name__ == "__main__":
    explode_overall()
    explode_strip()
