"""End walls must clear the core at rest and while the plate slides. Run with cadgen from the repo root."""
import build123d as bd
from cadgen import read_step
from cadgen.geometry import closest_points

from slab import CORE, D, L, P_DISC, P_FLAT, R, plate

SLIDE = 25.0      # generous until TODO.md Job 1C measures it
core = read_step(CORE / "core_final.step")
for name, part, zone, move in (
    ("flat wall, drive end", plate(+1)[0], bd.Pos(P_FLAT / 2, 0, (R - 2 - 10) / 2) * bd.Box(P_FLAT - 1, D + 10, R - 2 + 10), 1),
    ("disc wall, fan end", plate(-1)[0], bd.Pos(-P_DISC / 2, 0, (L - R - 2 + L + 5) / 2) * bd.Box(P_DISC - 1, D + 10, R + 7), -1),
):
    wall = part & zone
    assert wall.volume > 0, f"{name}: no wall built"
    box = wall.bounding_box()
    print(f"{name}: x {box.min.X:.1f}..{box.max.X:.1f} z {box.min.Z:.1f}..{box.max.Z:.1f}")
    for dz in (0, 10, SLIDE):
        d = closest_points(bd.Pos(0, 0, move * dz) * wall, core).distance
        print(f"  slid {dz:4.0f} mm: {d:.2f} mm to core")
        assert d > 1.0, f"{name} too close to the core at slide {dz}"
