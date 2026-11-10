import math
from pathlib import Path
import build123d as bd
from cadgen import model, read_step

HERE = Path(__file__).resolve().parent
# OBJ reference frame (mm): X = width (flat side -X, disc side +X), Y = height 0..390, Z = depth (front +Z)
H, Z0, Z1 = 390.0, -122.0, 122.0          # plate outline flush with core (core Z -121.1..121.8)
FLOOR, WALL, RC = 2.5, 2.5, 8.0
X_FB_END = 32.0                            # front/rear walls stop here -> ~6 mm reveal to the core front face
X_TB_END = 47.0                            # top/bottom walls stop just outside the core's matte sides
FAN_Y, FAN_Z, FAN_D = 314.0, 8.0, 124.0    # X-ray: 76 mm below top, ~132 mm from rear
PLATE, CORE, MATTE, LIGHT, BTN = "#c4c3be", "#232326", "#161618", "#4f86e0", "#8d8d90"


def plate(side, P):
    """side -1 = flat side, +1 = disc side; P = |X| of the glue plane (inner face of the floor)."""
    xo = P + FLOOR
    prof = bd.Plane.YZ.offset(0) * bd.Pos(H / 2, (Z0 + Z1) / 2) * bd.RectangleRounded(H, Z1 - Z0, RC)
    def slab(x_from, x_to, inset=0.0):
        sk = bd.Plane.YZ.offset(x_from) * bd.Pos(H / 2, (Z0 + Z1) / 2) * bd.RectangleRounded(H - 2 * inset, Z1 - Z0 - 2 * inset, RC - inset if RC > inset else 0.5)
        return bd.extrude(sk, amount=x_to - x_from)
    body = slab(X_FB_END, xo)
    body = body - slab(X_FB_END - 1, P, inset=WALL)                       # hollow: floor + walls
    if xo > X_TB_END:                                                      # top/bottom walls stop at X_TB_END
        for y in (WALL / 2 - 0.5,):          # bottom only: the stand area is wide; top stays closed
            body = body - bd.Pos((X_FB_END + X_TB_END) / 2 - 0.5, y, 0) * bd.Box(X_TB_END - X_FB_END + 1, WALL + 1.2, Z1 - Z0 - 2 * WALL)
    else:
        body = body - bd.Pos((X_FB_END + xo) / 2, H / 2, 0) * bd.Box(xo - X_FB_END + 2, H + 2, 0) if False else body
    body = bd.fillet(body.edges().filter_by(bd.Axis.X, reverse=True).group_by(bd.Axis.X)[-1], 1.5)
    holes = []
    pitch, rr, j, y = 5.0, FAN_D / 2, 0, -FAN_D / 2
    while y <= rr:
        x = -rr + (j % 2) * pitch / 2
        while x <= rr:
            if math.hypot(x, y) <= rr - 2:
                holes.append(bd.Pos(xo - 1.5, FAN_Y + y, FAN_Z + x) * bd.Rot(0, 90, 0) * bd.Cylinder(1.6, 6))
            x += pitch
        y += pitch * math.sqrt(3) / 2; j += 1
    body = body - bd.Compound(holes)
    if side < 0:
        body = bd.mirror(body, bd.Plane.YZ)
    body.color = PLATE
    body.label = "plate_disc" if side > 0 else "plate_flat"
    return body


def core():
    kids = []
    for f, c, lab in [("core.step", CORE, "core_gloss"), ("core_matte.step", MATTE, "core_matte"),
                      ("lightbar.step", LIGHT, "lightbar"), ("front_glass.step", MATTE, "front_io"), ("buttons.step", BTN, "buttons")]:
        s = read_step(HERE / "core" / f); s.color = c; s.label = lab; kids.append(s)
    return kids


def console(p_flat, p_disc, lying=False):
    kids = core() + [plate(-1, p_flat), plate(+1, p_disc)]
    c = bd.Compound(children=kids, label="console")
    if lying:                             # One S style: disc-side plate down as the base
        return bd.Rot(0, 90, 0) * c
    return bd.Rot(90, 0, 0) * c           # standing: OBJ Y (height) -> world Z


@model
def concept_e_level():
    """Each plate as close to the core as the stock geometry allows (disc side carries the drive bulge)."""
    return console(44.1, 68.8)


@model
def concept_e_symmetric():
    """Both plates at the drive-bulge level: core strip centred."""
    return console(68.8, 68.8)


@model
def concept_e_lying():
    """Level version lying flat, thick disc-side plate as the base."""
    return console(44.1, 68.8, lying=True)


if __name__ == "__main__":
    concept_e_lying()
    concept_e_level()
    concept_e_symmetric()
