"""Fit tests to print before any full plate (TODO.md order). Run: cadgen +0.8.4 run cad/fit_tests.py
Step 1 = deliverables coupons (scanned hooks on the stock plate). Step 2 = this: the smallest disc-plate clip strip
in a plate offcut with its rails, end stop and latch ledge, laid out on the bed as printed."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import build123d as bd
from cadgen import model
import wrap

STRIP, MARGIN, GAP = "clip_strip_disk_bottom", 10.0, 15.0     # test strip, offcut margin round it, gap on the bed
OUT = Path(__file__).resolve().parents[1] / "deliverables" / "fit_tests"


def on_bed(shape, x):
    """lying frame (disc side down) -> print frame: outer face on the bed, min corner at (x, 0, 0)"""
    s = bd.Rot(0, -90, 0) * shape
    b = s.bounding_box()
    return bd.Pos(x - b.min.X, -b.min.Y, -b.min.Z) * s


@model
def fit_strip_offcut():
    parts = wrap.plate_set(-1)
    plate = next(p for p in parts if p.label == "plate_disk")
    strip = next(p for p in parts if p.label == STRIP)
    b = strip.bounding_box()
    cut = wrap.box(b.min.X - 10, b.max.X + 10, b.min.Y - MARGIN, b.max.Y + MARGIN, b.min.Z - MARGIN, b.max.Z + MARGIN)
    offcut = on_bed(plate & cut, 0)
    piece = on_bed(strip, offcut.bounding_box().max.X + GAP)       # upright as installed: hooks up, layers along shafts
    assert offcut.volume > 0 and piece.volume > 0
    offcut.color, offcut.label = wrap.COL_PLATE, "offcut_disk_bottom"
    piece.color, piece.label = wrap.COL_STRIP, STRIP
    return bd.Compound(children=[offcut, piece], label="fit_strip_offcut")


if __name__ == "__main__":
    fit_strip_offcut()
