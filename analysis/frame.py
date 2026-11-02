import trimesh, numpy as np
m = trimesh.load("../sources/rhys34512-printables-973426/flat-panel-side.stl")
(x0,y0,z0),(x1,y1,z1) = m.bounds
W, H = y1-y0, z1-z0
boxes=[]
def B(ya,yb,za,zb):  # local Y/Z ranges
    boxes.append(trimesh.creation.box(bounds=[[x0-1,y0+ya,z0+za],[x1+1,y0+yb,z0+zb]]))
band=12
B(-1,W+1,-1,band); B(-1,W+1,H-band,H+1); B(-1,band,-1,H+1); B(W-band,W+1,-1,H+1)   # perimeter
clips=[(74.2,348.7),(23.0,325.2),(203.0,320.0),(81.5,238.5),(223.2,234.2),(159.5,193.7),(24.0,190.2),(238.0,143.0),(135.5,38.2),(239.0,37.5),(24.5,36.7)]
for y,z in clips: B(y-11,y+11,z-17,z+17)                                            # clip pads
r=5  # half rib width
for z in [37,192,236,335]: B(-1,W+1,z-r,z+r)                                         # horizontal ribs
for y in [24,78,135,160,225]: B(y-r,y+r,-1,H+1)                                      # vertical ribs
keep = trimesh.boolean.union(boxes, engine="manifold")
f = trimesh.boolean.intersection([m, keep], engine="manifold")
f.export("adapter_flat_concept.stl")
print("adapter: extents", np.round(f.extents,1), "volume cm3 %.0f vs panel %.0f"%(f.volume/1000, m.volume/1000), "wt", f.is_watertight)
