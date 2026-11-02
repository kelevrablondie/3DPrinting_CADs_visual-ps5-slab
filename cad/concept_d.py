import build123d as bd
from cadgen import model

# console lying flat (One S style). X = length (console height), Y = depth (Y=0 rear, Y=D front), Z = width
CORE_L, CORE_D = 390.0, 260.0          # PS5 body footprint (Sony spec) - to be measured
CLR, WALL, FLOOR, R = 1.5, 2.5, 2.5, 10.0
L, D = CORE_L + 2 * (CLR + WALL), CORE_D + 2 * (CLR + WALL)
W_TOTAL, GAP = 109.0, 4.0              # total width, shadow line between the plates
RIM = W_TOTAL / 2 - GAP / 2 - FLOOR    # rim depth so the plates nearly meet
FAN_X, FAN_Y, FAN_D = L - (CLR + WALL) - 76, (CLR + WALL) + 131, 124.0   # from X-ray: 76 mm from top end, 131 mm from rear (+-5)
LIGHT, DARK, CORE = "#c4c3be", "#77777b", "#2a2a2c"
ACCENT = ["#d8343a", "#e8b923", "#2fa58f", "#3b6fc4"]


def plate():
    H = FLOOR + RIM
    outer = bd.extrude(bd.RectangleRounded(L, D, R), amount=H)
    outer = bd.fillet(outer.edges().group_by(bd.Axis.Z)[-1], 2.0)
    inner = bd.Pos(0, 0, -0.01) * bd.extrude(bd.RectangleRounded(L - 2 * WALL, D - 2 * WALL, R - WALL), amount=RIM + 0.01)
    p = outer - inner
    cut = []
    # rear: open exhaust window across the rim, framed by 12 mm corners
    cut.append(bd.Pos(0, -D / 2, RIM / 2 - 2) * bd.Box(L - 2 * 24, 3 * WALL, RIM - 6))
    # front: intake slots, 2 mm on 4.5 mm pitch, full length
    n = int((L - 48) // 4.5)
    for i in range(n):
        cut.append(bd.Pos(-L / 2 + 24 + i * 4.5, D / 2, RIM / 2 - 2) * bd.Box(2.0, 3 * WALL, RIM - 8))
    # fan grille: hex field of 3.2 mm holes inside the fan circle
    import math
    pitch, rr = 5.0, FAN_D / 2 - 3
    j = 0
    y = -rr
    while y <= rr:
        off = (j % 2) * pitch / 2
        x = -rr + off
        while x <= rr:
            if math.hypot(x, y) <= rr:
                cut.append(bd.Pos(FAN_X - L / 2 + x, FAN_Y - D / 2 + y, H - 1) * bd.Cylinder(1.6, 6))
            x += pitch
        y += pitch * math.sqrt(3) / 2; j += 1
    p = p - bd.Compound(cut)
    return p


@model
def concept_d_slab():
    top = bd.Pos(L / 2, D / 2, GAP / 2) * plate()
    bot = bd.mirror(top, bd.Plane.XY)
    top.color = bot.color = LIGHT
    top.label, bot.label = "plate_flat", "plate_disc"
    core = bd.Pos(L / 2, D / 2, 0) * bd.Box(CORE_L - 20, CORE_D - 20, W_TOTAL - 2 * FLOOR - 4)
    core.color, core.label = CORE, "core"
    kids = [core, top, bot]
    # subtle four-colour inlay: four 14 x 2 mm bars near the front-left corner of the top plate
    for k, c in enumerate(ACCENT):
        b = bd.Pos(18 + k * 17, D - 12, W_TOTAL / 2 + 0.01) * bd.Box(14, 2, 0.4)
        b.color, b.label = c, f"accent_{k}"
        kids.append(b)
    # TPU feet
    for fx in (40, L - 40):
        for fy in (40, D - 40):
            f = bd.Pos(fx, fy, -W_TOTAL / 2 - 2) * bd.Cylinder(9, 4)
            f.color, f.label = DARK, "foot"
            kids.append(f)
    return bd.Compound(children=kids, label="console")


if __name__ == "__main__":
    concept_d_slab()
