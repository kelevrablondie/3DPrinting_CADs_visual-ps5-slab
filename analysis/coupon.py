import trimesh, numpy as np
m = trimesh.load("../sources/rhys34512-printables-973426/flat-panel-side.stl")
y0, z0 = m.bounds[0][1], m.bounds[0][2]
xs = (m.bounds[0][0]-1, m.bounds[1][0]+1)
def coupon(yc, zc, wy, wz, name):
    # local coords -> world
    lo = [xs[0], y0+yc-wy/2, z0+zc-wz/2]; hi=[xs[1], y0+yc+wy/2, z0+zc+wz/2]
    lo[1]=max(lo[1],y0-1); lo[2]=max(lo[2],z0-1)
    box = trimesh.creation.box(bounds=[lo,hi])
    c = trimesh.boolean.intersection([m, box], engine="manifold")
    c.export(name); print(name, np.round(c.extents,1), "watertight", c.is_watertight, "faces", len(c.faces))
coupon(24, 32, 50, 64, "coupon_F11_small_corner.stl")     # bottom corner small clip + edge

