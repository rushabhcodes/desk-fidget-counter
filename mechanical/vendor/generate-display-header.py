#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Rigid-datum derivative of the exact JLCPCB STEP.

Uses the documented CAD Python environment. Only the through-hole tails are
clipped, to 0.8 mm below a 1.6 mm PCB; copper/drills and original assets are retained.
"""
from pathlib import Path
import subprocess,sys,tempfile
import numpy as np,trimesh,manifold3d as m
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
source=ROOT/'imports/jlc/A_61300821021/A_61300821021.step'
with tempfile.TemporaryDirectory(prefix='display-header-') as tmp:
 mesh_path=Path(tmp)/'header.ply'
 subprocess.run([sys.executable,str(ROOT/'mechanical/step-mesh.py'),str(source),str(mesh_path),'--preserve-seams'],check=True)
 raw=trimesh.load(mesh_path,force='mesh',process=False)
raw.apply_translation(-np.array([.0000127,4.8000031,-.280006]))
header=m.Manifold(m.Mesh64(np.ascontiguousarray(raw.vertices),np.ascontiguousarray(raw.faces,dtype=np.uint64)))
header^=m.Manifold.cube((100,100,50),True).translate((0,0,22.6))
a=header.to_mesh64();mesh=trimesh.Trimesh(np.asarray(a.vert_properties)[:,:3],np.asarray(a.tri_verts),process=False)
c=mesh.triangles_center;body=(c[:,1]>-5.26)&(c[:,1]<-2.74)&(c[:,2]>-.01)
mesh.visual=trimesh.visual.ColorVisuals(mesh,face_colors=np.where(body[:,None],[40,45,48,255],[211,171,78,255]).astype(np.uint8))
assert mesh.is_watertight and np.isclose(mesh.bounds[0,2],-2.4)
mesh.export(OUT/'obj/header2x4-ra.obj',include_color=True)
mesh.export(OUT/'solid/header2x4-ra.ply')
print('Unscaled canonical header bounds (mm):',mesh.bounds.tolist())
