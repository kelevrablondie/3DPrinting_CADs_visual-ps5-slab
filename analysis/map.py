import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
clips = {
 "flat": [(300.6,310.1,533.3,556.8,"L"),(250.6,257.6,513.3,529.8,"S"),(429.1,439.1,504.3,528.3,"L"),(309.1,316.1,426.8,442.8,"S"),
          (449.6,459.1,419.3,441.8,"L"),(387.1,394.1,382.3,397.8,"S"),(251.6,258.6,377.8,395.3,"S"),(465.6,472.6,331.8,346.8,"S"),
          (363.1,370.1,226.3,242.8,"S"),(466.6,473.6,225.8,241.8,"S"),(252.1,259.1,224.3,241.8,"S")],
 "disk": [(195.6,205.6,532.7,555.7,"L"),(146.1,153.1,512.2,528.7,"S"),(324.6,334.6,503.2,527.7,"L"),(203.6,212.6,418.7,442.2,"L"),
          (146.1,154.6,372.7,394.2,"S"),(281.1,292.1,368.2,397.2,"L"),(146.5,154.0,224.0,242.0,"S")],
}
fig, axs = plt.subplots(1,2, figsize=(15,10))
for ax,name in zip(axs,["disk","flat"]):
    d=np.load(f"{name}_hmap.npz"); hi,lo,res,y0,z0=d["hi"],d["lo"],float(d["res"]),float(d["y0"]),float(d["z0"])
    nz,ny=hi.shape
    ax.imshow(np.isfinite(hi), origin="lower", extent=[0,ny*res,0,nz*res], cmap="Greys", alpha=.25)
    print(f"--- {name} panel: {ny*res:.0f} x {nz*res:.0f} mm (local origin = bottom-left of this view)")
    for i,(a,b,c,e,t) in enumerate(sorted(clips[name], key=lambda r:(-r[2],r[0])),1):
        yc,zc=(a+b)/2-y0,(c+e)/2-z0
        ax.add_patch(plt.Rectangle((a-y0,c-z0),b-a,e-c,fc="tab:red" if t=="L" else "tab:blue",ec="k",alpha=.8))
        ax.annotate(f"{name[0].upper()}{i} ({yc:.0f},{zc:.0f})",(b-y0+2,zc),fontsize=9,va="center")
        print(f"  {name[0].upper()}{i}: {'large spring' if t=='L' else 'small solid'}  centre ({yc:.1f}, {zc:.1f})  footprint {b-a:.1f} x {e-c:.1f}")
    ax.set_title(f"{name} panel — clip map (red = large spring hook, blue = small hook)\nhooks point up (+Z): panel slides up to lock")
    ax.set_xlabel("mm"); ax.set_ylabel("mm"); ax.grid(alpha=.3); ax.set_aspect("equal")
plt.tight_layout(); plt.savefig("clip_map.png", dpi=90)
