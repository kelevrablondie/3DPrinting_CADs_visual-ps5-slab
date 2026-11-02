import sys, numpy as np
def load(p):
    d=open(p,'rb').read(); n=int.from_bytes(d[80:84],'little')
    a=np.frombuffer(d[84:84+n*50],dtype=np.dtype([('n','<f4',3),('v','<f4',(3,3)),('a','<u2')]))
    return a['v'].astype(float)
import build123d as bd
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace, BRepBuilderAPI_Sewing
from OCP.gp import gp_Pnt
for src, dst in zip(sys.argv[1::2], sys.argv[2::2]):
    T = load(src)
    sew = BRepBuilderAPI_Sewing(0.01)
    for tri in T:
        if np.linalg.norm(np.cross(tri[1]-tri[0],tri[2]-tri[0]))<1e-6: continue
        p = BRepBuilderAPI_MakePolygon(*[gp_Pnt(*map(float, v)) for v in tri], True)
        f = BRepBuilderAPI_MakeFace(p.Wire(), True)
        if f.IsDone(): sew.Add(f.Face())
    sew.Perform()
    shape = bd.Shape.cast(sew.SewedShape())
    bd.export_step(shape, dst); print(dst, len(T))
