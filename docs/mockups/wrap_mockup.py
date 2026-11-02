"""Preliminary mockup: plates wrap the core with level lips and a constant black stripe all round
(devynPC 'I fixed the PS5 Pro' 1:05 sketch). True scale, mm, from slab.py's numbers.
Usage: python3 -I wrap_mockup.py <out.png>"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, RegularPolygon

PLATE, CORE, DRIVE, VENT, BG = "#c6c4be", "#1d1d1f", "#dcdcd8", "#55555a", "#f4f5f7"
ACCENT = ["#d8343a", "#e8b923", "#2fa58f", "#3b6fc4"]
TOP, BOT = 59.2 + 2.5, -54.8 - 2.5      # outer plate surfaces (x)
C, BAND = 2.2, 40.0                      # stripe centred on the core, = narrowest core face (front, drive end)
B_HI, B_LO = C + BAND / 2, C - BAND / 2  # 22.2, -17.8 -> lips 39.5 mm each
L0, L1 = -2.0, 382.0                     # plate span along the length (core 0..380)
D = 255.0


def honeycomb(ax, u0, u1, x0, x1, flats=6.0, web=1.2, inset=2.5):
    """hex holes for the exhaust: open area = (flats / (flats + web))^2 = 69 % at 6 / 1.2"""
    p = flats + web
    r = flats / 3 ** 0.5                                  # circumradius of a hexagon with these flats
    row, x = 0, x0 + inset + flats / 2
    while x <= x1 - inset - flats / 2:
        u = u0 + inset + r + (p / 2 if row % 2 else 0)
        while u <= u1 - inset - r:
            ax.add_patch(RegularPolygon((u, x), 6, radius=r, orientation=0, color=VENT, lw=0))
            u += p
        x += p * 0.866
        row += 1


def lip(ax, u0, u1, x0, x1):
    ax.add_patch(Rectangle((u0, x0), u1 - u0, x1 - x0, fc=PLATE, ec="#888", lw=0.4))


def frame(ax, title, w):
    ax.set_xlim(-20, w + 20); ax.set_ylim(-75, 78); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, fontsize=10, loc="left")


def face(ax):
    """you looking at the front: W (fan) left, E (drive) right. u = 380 - z"""
    frame(ax, "FACE (working view): E drive end left, W fan end right", 384)
    ax.invert_xaxis()                                                     # trust the scan-based model: drive end on the left
    ax.add_patch(Rectangle((L0, B_LO), L1 - L0, BAND, fc=CORE))
    lip(ax, L0, L1, B_HI, TOP); lip(ax, L0, L1, BOT, B_LO)               # both lips level, end to end
    # drive (z 0..135) sits behind the south lip, like the stock plate; dashed = hidden
    ax.add_patch(Rectangle((380 - 135, -50.8), 135, -17.8 + 50.8, fill=False, ec="#777", lw=0.8, ls="--"))
    # disc slot from the stock disc plate scan: z' 22.5..145, straight disc path x' -25.5..-20.5
    ax.add_patch(Rectangle((380 - 145, -25.5), 145 - 22.5, 5, fc=CORE, ec="#444", lw=0.4))
    honeycomb(ax, L0, 120, B_HI, TOP); honeycomb(ax, L0, 120, BOT, B_LO)
    for i, col in enumerate(ACCENT):                                      # 4 inserts, 2.5 x 14 each
        ax.add_patch(Rectangle((338 + i * 4, C + BAND / 2 + 39.5 / 2 - 7), 2.5, 14, fc=col, lw=0))
    ax.text(312, -40, "drive behind the lip (dashed)", ha="center", fontsize=6.5)
    ax.text(296, -32, "disc slot 122.5 x 5, from stock plate scan", ha="center", fontsize=6.5)
    ax.text(250, 40, "north lip 39.5", fontsize=7); ax.text(150, 0, "black stripe 40, constant", color="w", fontsize=7)
    ax.text(150, -40, "south lip 39.5", fontsize=7)
    ax.text(345, 66, "colour inserts", fontsize=6.5, ha="center")


def back(ax):
    """looking at the back: E left, W right. u = z"""
    frame(ax, "BACK: W left, E right. Lips cover the exhaust, so they are vented end to end", 384)
    ax.invert_xaxis()
    ax.add_patch(Rectangle((L0, B_LO), L1 - L0, BAND, fc=CORE))
    lip(ax, L0, L1, B_HI, TOP); lip(ax, L0, L1, BOT, B_LO)
    honeycomb(ax, L0, L1, B_HI, TOP); honeycomb(ax, L0, L1, BOT, B_LO)
    ax.add_patch(Rectangle((0, -37.8), 100, 80, fill=False, ec="#d8343a", lw=1.2, ls="--"))
    ax.text(50, 66, "ports: positions not measured", color="#d8343a", fontsize=7, ha="center")


def end(ax, title, front_right):
    """looking at a short end. u = depth y (front on the right for W, left for E)"""
    frame(ax, title, D)
    ax.add_patch(Rectangle((0, B_LO), D, BAND, fc=CORE))
    lip(ax, 0, D, B_HI, TOP); lip(ax, 0, D, BOT, B_LO)
    honeycomb(ax, 0, D, B_HI, TOP); honeycomb(ax, 0, D, BOT, B_LO)
    fx = D - 2 if front_right else 2
    ax.text(fx, -70, "front", ha="right" if front_right else "left", fontsize=7)


fig = plt.figure(figsize=(11, 12), facecolor=BG)
gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1])
face(fig.add_subplot(gs[0, :])); back(fig.add_subplot(gs[1, :]))
end(fig.add_subplot(gs[2, 0]), "EAST end (drive)", True); end(fig.add_subplot(gs[2, 1]), "WEST end (fan)", False)
fig.suptitle("Wrap-around plates: level lips, constant black stripe, 6 mm hex honeycomb vents, 69 % open (true scale, mm)", fontsize=12)
fig.savefig(sys.argv[1], dpi=110, facecolor=BG, bbox_inches="tight")
