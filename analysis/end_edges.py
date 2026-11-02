"""Straight edge for the end walls: the tightest line |x| = a + b*y that keeps REVEAL off the core
along the plate's slide range. Prints the END_FLAT / END_DISC values used by cad/slab.py.
Run from the repo root after core_proxy*.py."""
import numpy as np
import trimesh
from scipy.optimize import linprog

REVEAL, SLIDE, HALF_D, R, CORE_L = 4.0, 25.0, 127.5, 10.0, 380.0
core = trimesh.load("cad/core/core_final.stl", force="mesh")
ys = np.arange(-HALF_D + R, HALF_D - R + 0.5, 1.0)


def core_top(side, z):
    """outermost |x| of the core per y at height z (nan where the ray misses)"""
    o = np.column_stack([np.full_like(ys, -200.0), ys, np.full_like(ys, z)])
    hit, ray, _ = core.ray.intersects_location(o, np.tile([1.0, 0, 0], (len(ys), 1)))
    top = np.full_like(ys, np.nan)
    for i in range(len(ys)):
        xs = hit[ray == i, 0] * side
        if len(xs):
            top[i] = xs.max()
    return top


def edge(side, zs):
    top = np.nanmax([core_top(side, z) for z in zs], axis=0)
    ok = ~np.isnan(top)
    need = top[ok] + REVEAL
    # the lowest line over every point; a shallower one would cut into the reveal
    a, b = linprog([1, 0], A_ub=np.column_stack([-np.ones(ok.sum()), -ys[ok]]), b_ub=-need, bounds=[(None, None)] * 2).x
    assert np.all(a + b * ys[ok] >= need - 1e-6), "edge cuts into the reveal"
    return a + b * -HALF_D, a + b * HALF_D, (a + b * ys[ok] - top[ok]).min()


for name, side, zs in (("END_FLAT", 1, np.arange(1, SLIDE, 2.0)),                     # flat wall: drive end
                       ("END_DISC", -1, np.arange(CORE_L - SLIDE, CORE_L, 2.0))):     # disc wall: fan end
    r, f, gap = edge(side, zs)
    print(f"{name} = {r:.1f}, {f:.1f}   # rear, front at y=-+{HALF_D}; tightest reveal {gap:.1f}")
