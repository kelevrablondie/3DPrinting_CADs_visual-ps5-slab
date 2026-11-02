import trimesh, numpy as np, matplotlib, sys
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig = plt.figure(figsize=(12,6))
for i,f in enumerate(sys.argv[1:],1):
    m = trimesh.load(f).simplify_quadric_decimation(face_count=6000)
    ax = fig.add_subplot(1,2,i,projection="3d")
    tri = m.vertices[m.faces]; n = m.face_normals
    shade = 0.35+0.65*np.clip(n@np.array([0.6,-0.5,0.6]),0,1)
    pc = Poly3DCollection(tri, facecolors=plt.cm.Greys(1-shade*0.8), edgecolor="none"); ax.add_collection3d(pc)
    b=m.bounds; c=b.mean(0); r=(b[1]-b[0]).max()/2
    ax.set_xlim(c[0]-r,c[0]+r); ax.set_ylim(c[1]-r,c[1]+r); ax.set_zlim(c[2]-r,c[2]+r)
    ax.view_init(elev=15, azim=-140); ax.set_title(f.split('/')[-1]); ax.set_box_aspect((1,1,1))
plt.tight_layout(); plt.savefig("coupons.png", dpi=90)
