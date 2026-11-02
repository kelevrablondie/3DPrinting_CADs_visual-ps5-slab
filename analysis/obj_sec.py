import numpy as np, collections, trimesh, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
S=200.0
V=[]; F=collections.defaultdict(list); obj=None; cur=None
for line in open("../sources/obj-visual-model/PS5.obj"):
    if line.startswith("v "): V.append([float(t) for t in line.split()[1:4]])
    elif line.startswith("o "): obj=line.split()[1]
    elif line.startswith("usemtl"): cur=f"{obj}|{line.split()[1]}"
    elif line.startswith("f "):
        p=[int(t.split('/')[0])-1 for t in line.split()[1:]]
        for i in range(1,len(p)-1): F[cur].append([p[0],p[i],p[i+1]])
V=np.array(V)*S
parts={"plates":"Body1:1|Plastic_-_Textured_-_Regular","core":"Console|Plastic_-_Translucent_Glossy_(Gray)",
       "core_matte":"Body3|Plastic_-_Translucent_Matte_(Gray)_1","lightbar":"Lightbar|Plastic_-_Translucent_Glossy_(Blue)",
       "front_glass":"Body4|Glass_-_Heavy_Color","buttons":"Body4:1|Steel_-_Satin"}
M={k:trimesh.Trimesh(V,np.array(F[v]),process=True) for k,v in parts.items()}
for k,m in M.items(): m.remove_unreferenced_vertices(); m.export(f"obj_{k}.stl")
col={"plates":"0.6","core":"k","core_matte":"tab:orange","lightbar":"tab:blue","front_glass":"tab:green","buttons":"tab:red"}
fig,ax=plt.subplots(1,3,figsize=(18,8))
for a,h in zip(ax,[60,200,340]):
    for k,m in M.items():
        s=m.section(plane_origin=[0,h,0],plane_normal=[0,1,0])
        if s is None: continue
        for e in s.discrete: a.plot(e[:,2],e[:,0],color=col[k],lw=1.2 if k!="plates" else 1.8)
        a.plot([],[],color=col[k],label=k)
    a.set_title(f"horizontal section at height {h} mm (front = right)"); a.set_xlabel("depth Z mm"); a.set_ylabel("width X mm"); a.set_aspect("equal"); a.grid(alpha=.3)
ax[0].legend(fontsize=8)
plt.tight_layout(); plt.savefig("obj_sections.png",dpi=80)
for k,m in M.items(): print(k, "bounds mm", np.round(m.bounds,1).tolist())
