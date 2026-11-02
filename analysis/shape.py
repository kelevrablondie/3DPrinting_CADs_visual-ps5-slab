import trimesh, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(2,2, figsize=(16,12))
for r,(f,name) in enumerate([("../sources/rhys34512-printables-973426/flat-panel-side.stl","flat"),("../sources/rhys34512-printables-973426/disk-panel.stl","disk")]):
    m=trimesh.load(f); (x0,y0,z0),(x1,y1,z1)=m.bounds
    for yl,c in [(20,'r'),(130,'g'),(240,'b')]:
        s=m.section(plane_origin=[0,y0+yl,0],plane_normal=[0,1,0])
        for e in s.discrete: ax[r,0].plot(e[:,0]-x0,e[:,2]-z0,c+'-',lw=.7)
        ax[r,0].plot([],[],c,label=f"Y={yl}")
    for zl,c in [(30,'r'),(195,'g'),(360,'b')]:
        s=m.section(plane_origin=[0,0,z0+zl],plane_normal=[0,0,1])
        for e in s.discrete: ax[r,1].plot(e[:,1]-y0,e[:,0]-x0,c+'-',lw=.7)
        ax[r,1].plot([],[],c,label=f"Z={zl}")
    ax[r,0].set_title(f"{name}: vertical sections (X vs Z)"); ax[r,1].set_title(f"{name}: horizontal sections (Y vs X)")
    for a in ax[r]: a.set_aspect('equal'); a.grid(alpha=.4); a.legend()
plt.tight_layout(); plt.savefig("panel_shape.png",dpi=80)
