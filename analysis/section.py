import trimesh, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
m = trimesh.load("../sources/rhys34512-printables-973426/flat-panel-side.stl")
# crop around one clip for speed
def crop(m, lo, hi):
    c = m.triangles_center; k = np.all((c>lo)&(c<hi),axis=1)
    return m.submesh([np.where(k)[0]], append=True)
fig, ax = plt.subplots(1,3, figsize=(16,6))
# clip A small (Y 363-370, Z 226-243), clip B large (Y 300.6-310, Z 533-557)
for a,(yc,zr,lab) in zip(ax[:2],[(366.6,(205,260),"small clip Y=366.6"),(305.3,(515,575),"large clip Y=305.3")]):
    s = crop(m, [330, yc-15, zr[0]], [380, yc+15, zr[1]])
    sec = s.section(plane_origin=[0,yc,0], plane_normal=[0,1,0])
    for e in sec.discrete: a.plot(e[:,0], e[:,2], 'k-', lw=1)
    a.set_aspect('equal'); a.grid(alpha=.4); a.set_title(lab+" (section, X vs Z)"); a.set_xlabel("X mm (console is toward -X)"); a.set_ylabel("Z mm")
    a.minorticks_on(); a.grid(which='minor', alpha=.15)
# cross section across small clip at its mid height (plane normal Z)
s = crop(m, [330, 350, 225], [380, 385, 245])
for z,c in [(230,'b'),(236,'r'),(240,'g')]:
    sec = s.section(plane_origin=[0,0,z], plane_normal=[0,0,1])
    if sec is None: continue
    for e in sec.discrete: ax[2].plot(e[:,1], e[:,0], c+'-', lw=1, label=f"Z={z}")
ax[2].set_aspect('equal'); ax[2].grid(alpha=.4); ax[2].set_title("small clip cross-sections (Y vs X)"); ax[2].set_xlabel("Y"); ax[2].set_ylabel("X")
h,l = ax[2].get_legend_handles_labels(); d=dict(zip(l,h)); ax[2].legend(d.values(), d.keys())
plt.tight_layout(); plt.savefig("clip_sections.png", dpi=100)
