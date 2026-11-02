import trimesh, numpy as np, matplotlib, sys
matplotlib.use("Agg"); import matplotlib.pyplot as plt
m = trimesh.load(sys.argv[1]); out=sys.argv[2]
clips = eval(sys.argv[3])  # list of (yc, zc)
fig, ax = plt.subplots(2, len(clips), figsize=(5*len(clips),10))
for i,(yc,zc) in enumerate(clips):
    sec = m.section(plane_origin=[0,yc,0], plane_normal=[0,1,0])
    a=ax[0,i]
    for e in sec.discrete:
        k = (np.abs(e[:,2]-zc)<22)
        if k.any(): a.plot(e[:,0], e[:,2], 'k-', lw=.8)
    a.set_ylim(zc-20, zc+20); a.set_aspect('equal', adjustable='datalim'); a.minorticks_on(); a.grid(alpha=.4); a.grid(which='minor',alpha=.15)
    a.set_title(f"side section at Y={yc} (X vs Z)")
    b=ax[1,i]
    for z,c in [(zc-6,'b'),(zc,'r'),(zc+6,'g')]:
        sec = m.section(plane_origin=[0,0,z], plane_normal=[0,0,1])
        for e in sec.discrete:
            if (np.abs(e[:,1]-yc)<15).any(): b.plot(e[:,1], e[:,0], c+'-', lw=.8, label=f"Z={z:.0f}")
    b.set_xlim(yc-12, yc+12); b.set_aspect('equal', adjustable='datalim'); b.minorticks_on(); b.grid(alpha=.4); b.grid(which='minor',alpha=.15)
    h,l=b.get_legend_handles_labels(); d=dict(zip(l,h)); b.legend(d.values(), d.keys(), fontsize=8); b.set_title("horizontal sections (Y vs X)")
plt.tight_layout(); plt.savefig(out, dpi=90)
