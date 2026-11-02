import numpy as np, trimesh
from scipy import ndimage
from skimage.measure import marching_cubes
P_FLAT, P_DISC = 59.2, 54.8          # glue planes, console frame: flat side +X, disc side -X
CORE_L = 380.0
def depth(z): return np.where(z < 190, 255.0, 255.0 - (z - 190) / 190 * 15.0)
def inner_console(name, side, planeX, sgn_out, P):
    d = np.load(f"{name}_hmap.npz"); lo, hi = d["lo"], d["hi"]; span = hi - lo
    inner = (lo if side == "lo" else hi).copy()
    nz, ny = inner.shape; b = 30
    interior = np.zeros_like(inner, bool); interior[b:-b, b:-b] = True
    clip = ndimage.binary_dilation((np.nan_to_num(span) > np.nanmedian(span) + 1.0) & interior, iterations=4)
    inner[clip] = np.nan
    idx = ndimage.distance_transform_edt(np.isnan(inner), return_distances=False, return_indices=True)
    inner = inner[tuple(idx)]
    # console x of the inner surface
    return (inner - planeX) * 1.0 + (P if sgn_out > 0 else -P)
xf = inner_console("flat", "lo", 374.74, +1, P_FLAT)[::2, ::2]
xd = inner_console("disk", "hi", 184.35, -1, P_DISC)[::2, ::2]
nz, ny = min(xf.shape[0], xd.shape[0]), min(xf.shape[1], xd.shape[1]); xf, xd = xf[:nz, :ny], xd[:nz, :ny]
res = 1.0
Z = np.arange(nz) * res - 4.0          # plate local Z 0 = core z -4 (plates overhang 4 mm each end)
Y = np.arange(ny) * res - 130.75
X = np.arange(-70, 72, res)
G = (X[None, None, :] > xd[:, :, None] + 0.5) & (X[None, None, :] < xf[:, :, None] - 0.5)
Zg = Z[:, None, None]; Yg = Y[None, :, None]
G &= (Zg >= 0) & (Zg <= CORE_L) & (np.abs(Yg) <= depth(Zg) / 2)
G = np.pad(G, 1)
v, f, _, _ = marching_cubes(G.astype(np.float32), 0.5)
v = (v - 1) * res
m = trimesh.Trimesh(np.c_[X[0] + v[:, 2], Y[0] + v[:, 1], Z[0] + v[:, 0]], f)
m = m.simplify_quadric_decimation(face_count=60000); m.fix_normals()
m.export("core_proxy.stl")
print("core proxy bounds", np.round(m.bounds, 1).tolist())
# validation against tape measurements: width of the core across X near the front / rear faces
def face_width(z, front):
    iz = int(round((z - Z[0]) / res)); dz = depth(np.array(z)) / 2
    cols = np.where((np.abs(Y) <= dz) & ((Y > dz - 6) if front else (Y < -dz + 6)))[0]
    w = (xf[iz, cols] - xd[iz, cols] - 1.0)
    return np.nanmax(w)
print("front face width  z=10 (bottom): %.0f  [tape 40 core / 73 with drive]" % face_width(10, True))
print("front face width  z=190 (mid):   %.0f  [tape 55]" % face_width(190, True))
print("front face width  z=370 (top):   %.0f  [tape 75]" % face_width(370, True))
print("rear face width   z=10 (bottom): %.0f  [tape 80]" % face_width(10, False))
print("rear face width   z=190 (mid):   %.0f  [tape 55-60]" % face_width(190, False))
print("rear face width   z=370 (top):   %.0f  [tape 45]" % face_width(370, False))
np.savez("core_inner_console.npz", xf=xf, xd=xd, Y=Y, Z=Z)
