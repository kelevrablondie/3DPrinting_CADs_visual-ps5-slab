import trimesh, numpy as np, sys, json
from scipy import ndimage
from skimage.measure import marching_cubes
from shapely.geometry import box as sbox, LineString, Point
from shapely.ops import unary_union

name, src, side = sys.argv[1], sys.argv[2], sys.argv[3]          # side: 'lo' (console at -X) or 'hi'
groups = json.loads(sys.argv[4])                                   # {shelf: [[y,z,'L'|'S'],...]}  local coords
P = trimesh.load(src); (x0,y0,z0),(x1,y1,z1) = P.bounds
d = np.load(f"{name}_hmap.npz"); res=float(d["res"]); lo, hi = d["lo"], d["hi"]
span = hi-lo; inner = (lo if side=="lo" else hi).copy()
sg = 1 if side=="lo" else -1                                       # outboard direction along X
valid = (span>2.3)&(span<3.8)
inner[~valid] = np.nan
idx = ndimage.distance_transform_edt(np.isnan(inner), return_distances=False, return_indices=True)
inner = ndimage.gaussian_filter(inner[tuple(idx)], 2)              # clips/edges removed, smooth
b = int(15/res)
plane = (np.nanmax(inner[b:-b,b:-b]) + 2.9) if sg>0 else (np.nanmin(inner[b:-b,b:-b]) - 2.9)
# voxel slab between inner+0.8 (outboard) and plane
xs = np.arange(min(x0,plane)-1, max(x1,plane)+1, res)
X = xs[None,None,:]
I = inner[:,:,None]
POCKET = 0.8                                                       # shelf back sinks into the plate's alignment pocket (cad/slab.py)
glue = plane + sg*POCKET
slab = ((X-I)*sg > 0.8) & ((glue-X)*sg > 0)                        # shape (nz, ny, nx)
slab = np.pad(slab, 1)
v, f, _, _ = marching_cubes(slab.astype(np.float32), 0.5)
v = (v-1)*res
S = trimesh.Trimesh(np.c_[xs[0]+v[:,2], y0+v[:,1], z0+v[:,0]], f)
S.fix_normals()
report = {"plane_x": float(plane), "outboard": "+X" if sg>0 else "-X"}
T = np.array([[0,0,1,0],[1,0,0,0],[0,1,0,0],[0,0,0,1]],float)    # (u,v,w)->(y,z,x)
xa, xb = (x0-5, glue) if sg>0 else (glue, x1+5)
for shelf, clips in groups.items():
    parts=[]
    for y,z,t in clips:
        hw, hh = (12,21) if t=="L" else (10,16)
        parts.append(sbox(y-hw, z-hh, y+hw, z+hh))
    for (ya,za,_),(yb,zb,_) in zip(clips, clips[1:]):
        parts.append(LineString([(ya,za),(yb,zb)]).buffer(7, cap_style=2))
    fp = unary_union(parts).buffer(2).buffer(-2)
    fp = fp.intersection(sbox(1,1,y1-y0-1,z1-z0-1))
    poly = trimesh.creation.extrude_polygon(fp, height=xb-xa)
    poly.apply_transform(T); 
    poly.apply_translation([xa, y0, z0])
    if sg<0: poly.apply_translation([0,0,0])
    yb_,zb_ = fp.bounds[0], fp.bounds[1]
    crop = trimesh.creation.box(bounds=[[x0-2,y0+fp.bounds[0]-2,z0+fp.bounds[1]-2],[x1+2,y0+fp.bounds[2]+2,z0+fp.bounds[3]+2]])
    Pc = trimesh.boolean.intersection([P, crop], engine="manifold")
    Sc = trimesh.boolean.intersection([S, crop], engine="manifold")
    sh = trimesh.boolean.intersection([trimesh.boolean.union([Pc, Sc], engine="manifold"), poly], engine="manifold")
    sh = max(sh.split(only_watertight=False), key=lambda s: s.volume) if len(sh.split(only_watertight=False))>1 else sh
    out = f"shelf_{name}_{shelf}.stl"; sh.export(out)
    # thickness range (plane to inner surface) under footprint
    report[shelf] = {"file": out, "clips": len(clips), "extents_mm": np.round(sh.extents,1).tolist(),
                     "volume_cm3": round(sh.volume/1000,1), "watertight": bool(sh.is_watertight)}
print(json.dumps(report, indent=1))
