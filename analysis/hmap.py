import trimesh, numpy as np, sys, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
f, name, inner = sys.argv[1], sys.argv[2], sys.argv[3]  # inner: 'max' or 'min' x faces console
m = trimesh.load(f)
pts, _ = trimesh.sample.sample_surface(m, 6_000_000, seed=1)
pts = np.vstack([pts, m.vertices])
res = 0.5
y0, z0 = m.bounds[0][1], m.bounds[0][2]
iy = ((pts[:,1]-y0)/res).astype(int); iz = ((pts[:,2]-z0)/res).astype(int)
ny, nz = iy.max()+1, iz.max()+1
idx = iz*ny+iy
x = pts[:,0]
hi = np.full(ny*nz, np.nan); lo = np.full(ny*nz, np.nan)
order = np.argsort(idx)
# max/min per cell
import numpy as np
hi_ = np.full(ny*nz, -np.inf); lo_ = np.full(ny*nz, np.inf)
np.maximum.at(hi_, idx, x); np.minimum.at(lo_, idx, x)
hi_[np.isinf(hi_)] = np.nan; lo_[np.isinf(lo_)] = np.nan
hi = hi_.reshape(nz, ny); lo = lo_.reshape(nz, ny)
np.savez_compressed(f"{name}_hmap.npz", hi=hi, lo=lo, y0=y0, z0=z0, res=res)
inn = hi if inner=="max" else lo
out = lo if inner=="max" else hi
# depth from inner reference plane: distance toward console
ref = np.nanmax(inn) if inner=="max" else np.nanmin(inn)
d = np.abs(ref - inn)
fig, ax = plt.subplots(1,2, figsize=(14,10))
ext = [y0, y0+ny*res, z0, z0+nz*res]
a=ax[0].imshow(d, origin="lower", extent=ext, cmap="viridis"); ax[0].set_title(f"{name}: inner surface, mm back from innermost point"); fig.colorbar(a, ax=ax[0])
t = np.abs(hi-lo)
b=ax[1].imshow(t, origin="lower", extent=ext, cmap="magma", vmax=np.nanpercentile(t,99.5)); ax[1].set_title("x-span per cell (hi-lo), mm"); fig.colorbar(b, ax=ax[1])
for A in ax: A.set_xlabel("Y mm"); A.set_ylabel("Z mm"); A.grid(alpha=.3)
plt.tight_layout(); plt.savefig(f"{name}_inner.png", dpi=90)
