import trimesh, sys, numpy as np
for f in sys.argv[1:]:
    m = trimesh.load(f)
    print(f, "faces", len(m.faces), "watertight", m.is_watertight)
    print("  bounds", np.round(m.bounds,2).tolist(), "extents", np.round(m.extents,2).tolist())
    print("  volume cm3", round(m.volume/1000,1) if m.is_watertight else "n/a")
    ch = m.split(only_watertight=False)
    print("  bodies", len(ch))
