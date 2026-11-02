import numpy as np, sys
from scipy import ndimage
for name in ["disk","flat"]:
    d = np.load(f"{name}_hmap.npz"); hi, lo, res, y0, z0 = d["hi"], d["lo"], float(d["res"]), float(d["y0"]), float(d["z0"])
    span = hi-lo
    base = np.nanmedian(span)
    mask = np.nan_to_num(span) > base + 3.0
    # drop panel border rims: erode from edges
    lab, n = ndimage.label(mask)
    print(f"== {name}: base wall (x-span median) {base:.2f} mm, blobs {n}")
    rows=[]
    for i in range(1, n+1):
        zz, yy = np.where(lab==i)
        if len(zz) < 20: continue
        ymin,ymax = y0+yy.min()*res, y0+(yy.max()+1)*res
        zmin,zmax = z0+zz.min()*res, z0+(zz.max()+1)*res
        if ymax-ymin > 40 or zmax-zmin > 60: 
            print(f"   rim/other blob Y {ymin:.0f}-{ymax:.0f} Z {zmin:.0f}-{zmax:.0f}"); continue
        h = np.nanmax(span[lab==i])
        rows.append((ymin,ymax,zmin,zmax,h))
    rows.sort(key=lambda r:(-r[2], r[0]))
    for r in rows:
        print(f"   clip  Y {r[0]:7.1f}-{r[1]:7.1f} (w {r[1]-r[0]:4.1f})  Z {r[2]:6.1f}-{r[3]:6.1f} (len {r[3]-r[2]:4.1f})  max x-span {r[4]:5.1f}")
