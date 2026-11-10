"""Clip strips: each strip clears its plate as installed, slides out toward its open end (the latch ledge is the only
thing it meets), and is blocked by the end stop the other way. Run: cadgen +0.8.4 run cad/check_clip_strips.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import build123d as bd
import wrap

for side in (+1, -1):
    parts = wrap.plate_set(side)
    plate = next(p for p in parts if p.label.startswith("plate_"))
    for s in (p for p in parts if p.label.startswith("clip_strip_")):
        sgn = 1 if side > 0 else -1                       # open end: +z flat, -z disc
        hit = lambda dz: (plate & (bd.Pos(0, 0, dz) * s)).volume
        rest, out, back = hit(0), hit(sgn * 4), hit(-sgn * 1)
        print(f"{s.label:28s} rest {rest:6.2f}  slide out 4 mm {out:6.1f}  push 1 mm into stop {back:6.1f} mm3")
        assert rest < 0.01, f"{s.label} overlaps its plate as installed"
        assert out > 0, f"{s.label}: latch ledge does not catch"
        assert back > 0, f"{s.label}: end stop does not block"
