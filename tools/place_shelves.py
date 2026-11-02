"""Move shelves from scan coordinates into the console frame (decimated, for rendering) -> cad/core/shelf_*_c.stl.
Then convert to STEP:  cadgen +0.8.2 run cad/mesh2step.py cad/core/X.stl cad/core/X.step ..."""
import glob, numpy as np, trimesh
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
# name: (scan glue-plane x, console glue-plane x, scan bbox y0, scan bbox z0)
T = {"flat": (374.74, 59.2, 231.12, 196.34), "disk": (184.35, -54.8, 126.61, 196.16)}
for f in sorted(glob.glob(str(ROOT / "analysis/shelf_*.stl"))):
    name = Path(f).stem.split("_")[1]; px, P, y0, z0 = T[name]
    m = trimesh.load(f)
    m.vertices = np.c_[m.vertices[:, 0] - px + P, m.vertices[:, 1] - y0 - 130.75, m.vertices[:, 2] - z0 - 4]
    m.simplify_quadric_decimation(face_count=6000).export(ROOT / "cad/core" / (Path(f).stem + "_c.stl"))
    print("placed", Path(f).name)
