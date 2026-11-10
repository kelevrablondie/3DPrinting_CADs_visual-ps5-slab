import build123d as bd
from cadgen import model

L, D = 388.0, 262.0          # plate outline: length (console height) x depth; Y=0 rear, Y=D front
T_FLOOR, RIM, WALL, R = 2.5, 20.0, 2.5, 14.0
SEAM_X, SEAM_Y = 211.0, 110.0   # tile seams, chosen to miss every clip shelf


def tray_body(color):
    H = T_FLOOR + RIM
    outer = bd.extrude(bd.RectangleRounded(L, D, R), amount=H)
    outer = bd.fillet(outer.edges().group_by(bd.Axis.Z)[-1], 3.0)
    inner = bd.Pos(0, 0, -0.01) * bd.extrude(bd.RectangleRounded(L - 2 * WALL, D - 2 * WALL, R - WALL), amount=RIM + 0.01)
    t = outer - inner
    # vent slots: front rim (intake) and rear rim (exhaust)
    slots = []
    for i in range(int((L - 60) // 5)):
        x = -L / 2 + 30 + i * 5
        for y in (D / 2, -D / 2):
            slots.append(bd.Pos(x, y, 3 + RIM * 0.45) * bd.Box(2.0, 3 * WALL, RIM * 0.6))
    t = t - bd.Compound(slots)
    return bd.Pos(L / 2, D / 2, 0) * t


def core():
    c = bd.Pos(L / 2, D / 2, -36) * bd.extrude(bd.RectangleRounded(L - 8, D - 10, 10), amount=36)
    c = bd.Compound(children=[c, bd.mirror(c, bd.Plane.XY)])
    c.color = "#151515"; c.label = "console_core"
    return c


def place(plate, top_color, bot_color):
    # plate built with floor at Z=0..H facing +Z; put one on top, mirror one below
    top = bd.Pos(0, 0, 54.5 - (T_FLOOR + RIM)) * plate
    bot = bd.mirror(top, bd.Plane.XY)
    top.color, bot.color = top_color, bot_color
    top.label, bot.label = "plate_flat", "plate_disc"
    return bd.Compound(children=[core(), top, bot], label="console")


def groove(x0, y0, x1, y1, z, w=1.2, d=0.8):
    import math
    ln = math.hypot(x1 - x0, y1 - y0)
    b = bd.Box(ln if y0 == y1 else w, w if y0 == y1 else ln, 2 * d)
    return bd.Pos((x0 + x1) / 2, (y0 + y1) / 2, z) * b


@model
def concept_a_monolith():
    """Flush face; tile seams turned into two hairline grooves; vents only in the rims."""
    p = tray_body("#2b2b2e")
    H = T_FLOOR + RIM
    p = p - groove(SEAM_X, 3, SEAM_X, D - 3, H) - groove(3, SEAM_Y, L - 3, SEAM_Y, H)
    return place(p, "#2b2b2e", "#2b2b2e")


@model
def concept_b_heatsink():
    """Fin band along the front (intake) edge, ribs running in the airflow direction."""
    p = tray_body("#3a3d42")
    H = T_FLOOR + RIM
    fins = [bd.Pos(12 + i * 4.0, D - 12 - 35, H + 0.6) * bd.Box(1.6, 70, 1.2) for i in range(int((L - 24) // 4))]
    p = p + bd.Compound(fins)
    p = p - groove(SEAM_X, 3, SEAM_X, D - 82, H)
    return place(p, "#3a3d42", "#3a3d42")


@model
def concept_c_frame_insert():
    """Recessed field with a separate accent insert; border frame hides the tile seams."""
    p = tray_body("#1e1f22")
    H = T_FLOOR + RIM
    B = 16.0
    pocket = bd.Pos(L / 2, D / 2, H - 1.2) * bd.extrude(bd.RectangleRounded(L - 2 * B, D - 2 * B, R - 6), amount=2)
    p = p - pocket
    ins = bd.Pos(L / 2, D / 2, H - 1.2) * bd.extrude(bd.RectangleRounded(L - 2 * B - 0.6, D - 2 * B - 0.6, R - 6.3), amount=1.2)
    a = place(p, "#1e1f22", "#1e1f22")
    insert = bd.Pos(0, 0, 54.5 - (T_FLOOR + RIM)) * ins
    insert.color, insert.label = "#c9a227", "accent_insert"
    return bd.Compound(children=list(a.children) + [insert], label="console")


if __name__ == "__main__":
    concept_a_monolith()
    concept_b_heatsink()
    concept_c_frame_insert()
