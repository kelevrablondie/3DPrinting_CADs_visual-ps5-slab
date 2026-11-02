import trimesh, numpy as np, matplotlib, glob
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
cols = plt.cm.tab10.colors
fig = plt.figure(figsize=(16,9))
for i,(name,src,az,pl) in enumerate([("flat","../sources/rhys34512-printables-973426/flat-panel-side.stl",180,374.74),("disk","../sources/rhys34512-printables-973426/disk-panel.stl",0,184.35)]):
    ax = fig.add_subplot(1,2,i+1,projection="3d")
    P = trimesh.load(src).simplify_quadric_decimation(face_count=20000)
    tri=P.vertices[P.faces]; ax.add_collection3d(Poly3DCollection(tri, facecolors=(.6,.6,.6,.12), edgecolor="none"))
    for j,f in enumerate(sorted(glob.glob(f"shelf_{name}_*.stl"))):
        m=trimesh.load(f).simplify_quadric_decimation(face_count=8000)
        n=m.face_normals; L=np.array([-np.cos(np.radians(az)), -0.3, 0.6]); s=0.35+0.65*np.clip(n@(L/np.linalg.norm(L)),0,1)
        c=np.array(cols[j][:3]); ax.add_collection3d(Poly3DCollection(m.vertices[m.faces], facecolors=np.c_[np.outer(s,c), np.ones(len(s))], edgecolor="none"))
        ctr=m.centroid; ax.text(ctr[0],ctr[1],ctr[2]+5,f.split('_')[-1][:-4],fontsize=9)
    b=P.bounds; c=b.mean(0); r=(b[1]-b[0]).max()/2
    ax.set_xlim(c[0]-r,c[0]+r); ax.set_ylim(c[1]-r,c[1]+r); ax.set_zlim(c[2]-r,c[2]+r); ax.set_box_aspect((1,1,1))
    ax.view_init(elev=12, azim=az+25); ax.set_axis_off(); ax.set_title(f"{name} panel: shelves (colour) inside stock plate (ghost), console side")
plt.tight_layout(); plt.savefig("shelves_overview.png", dpi=85)
