import trimesh, numpy as np
a = trimesh.load("../sources/rhys34512-printables-973426/flat-panel-side.stl"); b = trimesh.load("../sources/ps5-cover-standard-edition/Ps5_side_panel.stl")
# align by bounding-box min corner
b2 = b.copy(); b2.apply_translation(a.bounds[0]-b.bounds[0])
pts,_ = trimesh.sample.sample_surface(b2, 200000, seed=0)
from scipy.spatial import cKDTree
apts,_ = trimesh.sample.sample_surface(a, 3000000, seed=0)
d,_ = cKDTree(apts).query(pts)
print("low-poly flat vs Rhys flat: deviation mm  median %.3f  p95 %.3f  p99 %.3f  max %.2f"%(np.median(d),np.percentile(d,95),np.percentile(d,99),d.max()))
for i,s in enumerate(b.split(only_watertight=False)):
    print(" body",i,"faces",len(s.faces),"extents",np.round(s.extents,1),"wt",s.is_watertight)
