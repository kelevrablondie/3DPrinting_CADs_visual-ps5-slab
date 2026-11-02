import trimesh, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
cfg=[("flat","../sources/rhys34512-printables-973426/flat-panel-side.stl",+1,374.74),("disk","../sources/rhys34512-printables-973426/disk-panel.stl",-1,184.35)]
fig,axs=plt.subplots(2,1,figsize=(14,9))
for ax,(name,src,sg,plane) in zip(axs,cfg):
    m=trimesh.load(src); (x0,y0,z0),(x1,y1,z1)=m.bounds
    v=m.vertices
    # depth inboard from glue plane reached by the plate near each edge (within 6 mm of the outline)
    def prof(axis, at_min, coord_axis, lo_, hi_, n=60):
        a=v[:,axis]; edge=(a<m.bounds[0][axis]+6) if at_min else (a>m.bounds[1][axis]-6)
        c=v[edge,coord_axis]; x=v[edge,0]
        bins=np.linspace(lo_,hi_,n+1); out=[]
        for i in range(n):
            k=(c>=bins[i])&(c<bins[i+1])
            out.append(np.nan if not k.any() else ((plane - x[k].min()) if sg>0 else (x[k].max()-plane)))
        return (bins[:-1]+bins[1:])/2, np.array(out)
    edges={"bottom edge (Z min), along Y":(2,True,1,y0,y1),"top edge (Z max), along Y":(2,False,1,y0,y1),
           "edge Y min, along Z":(1,True,2,z0,z1),"edge Y max, along Z":(1,False,2,z0,z1)}
    print(f"== {name}: max inboard depth of stock plate edge, measured from glue plane (mm)")
    for lab,(axi,mn,ca,a,b) in edges.items():
        t,p=prof(axi,mn,ca,a,b); base=y0 if ca==1 else z0
        ax.plot(t-base,p,label=lab)
        print(f"   {lab:30s} min {np.nanmin(p):5.1f}  median {np.nanmedian(p):5.1f}  max {np.nanmax(p):5.1f}")
    ax.set_title(f"{name}: how deep the stock plate wraps at its edges (from glue plane)"); ax.set_xlabel("position along edge, mm"); ax.set_ylabel("depth mm"); ax.grid(alpha=.4); ax.legend()
plt.tight_layout(); plt.savefig("edge_depth.png",dpi=85)
