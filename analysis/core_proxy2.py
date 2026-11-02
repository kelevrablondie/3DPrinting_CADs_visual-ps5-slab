import numpy as np, trimesh
from skimage.measure import marching_cubes
d=np.load("core_inner_console.npz"); xf,xd,Y,Z=d["xf"],d["xd"],d["Y"],d["Z"]; res=1.0
X=np.arange(-70,72,res)
G=(X[None,None,:]>xd[:,:,None]+0.5)&(X[None,None,:]<xf[:,:,None]-0.5)
Zg=Z[:,None,None]; Yg=Y[None,:,None]
G&=(Zg>=0)&(Zg<=380)&(np.abs(Yg)<=np.where(Zg<190,255.0,255.0-(Zg-190)/190*15.0)/2)
G=np.pad(G,1); v,f,_,_=marching_cubes(G.astype(np.float32),0.5); v=(v-1)*res
env=trimesh.Trimesh(np.c_[X[0]+v[:,2],Y[0]+v[:,1],Z[0]+v[:,0]],f); env.fix_normals()
print("env watertight", env.is_watertight)
C = 2.2   # core centre x (between glue planes +59.2 / -54.8)
zs = [0, 95, 190, 285, 380]; wf = [40, 47, 55, 65, 75]; wr = [80, 71, 57, 51, 45]; dd = [255, 255, 255, 247.5, 240]
W, CH = 130.0, 25.0
verts, rings = [], []
for z, a, b, d in zip(zs, wf, wr, dd):
    ring = [(C + a/2, d/2), (C + W/2, d/2 - CH), (C + W/2, -d/2 + CH), (C + b/2, -d/2),
            (C - b/2, -d/2), (C - W/2, -d/2 + CH), (C - W/2, d/2 - CH), (C - a/2, d/2)]
    rings.append([(x, y, z) for x, y in ring])
V = np.array([p for r in rings for p in r]); n = 8; F = []
for k in range(len(rings) - 1):
    for i in range(n):
        a, b = k*n + i, k*n + (i+1) % n; c, d2 = a + n, b + n
        F += [[a, b, d2], [a, d2, c]]
cap0 = [[0, i, i+1] for i in range(1, n-1)]; capN = [[(len(rings)-1)*n + 0, (len(rings)-1)*n + i + 1, (len(rings)-1)*n + i] for i in range(1, n-1)]
loft = trimesh.Trimesh(V, F + [f[::-1] for f in cap0] + capN); loft.fix_normals()
print("loft watertight", loft.is_watertight, "volume", round(loft.volume/1e3))
core = trimesh.boolean.intersection([env, loft], engine="manifold")
drive = trimesh.creation.box(bounds=[[C - 53, 127.5 - 150, 2], [C - 20, 127.5, 135]])
drive_v = trimesh.boolean.intersection([drive, trimesh.creation.box(bounds=[[-54.8+3.5, -200, -10], [200, 200, 400]])], engine="manifold")
core = core.simplify_quadric_decimation(face_count=40000); core.export("core_final.stl"); drive_v.export("drive_proxy.stl")
print("core bounds", np.round(core.bounds, 1).tolist(), "drive bounds", np.round(drive_v.bounds, 1).tolist())
