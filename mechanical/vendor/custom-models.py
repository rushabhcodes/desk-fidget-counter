#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Nominal datasheet-derived package geometry. See README.md for omissions."""
from pathlib import Path
import json,math
import numpy as np,trimesh,manifold3d as m
ROOT=Path(__file__).resolve().parent
j=json.loads((ROOT/'models.json').read_text())
def box(s,c):return m.Manifold.cube(s,True).translate(c)
def mesh(s):
 a=s.to_mesh64();return trimesh.Trimesh(np.asarray(a.vert_properties)[:,:3],np.asarray(a.tri_verts),process=True)
def export(name,body,leads,source):
 meshes=[]
 for solid,color in [(body,[40,42,47,255]),(leads,[176,183,188,255])]:
  q=mesh(solid);q.visual=trimesh.visual.ColorVisuals(q,vertex_colors=color);meshes.append(q)
 q=trimesh.util.concatenate(meshes);p=ROOT/'obj'/f'{name}.obj';q.export(p,include_color=True,include_normals=False,header='SPDX-License-Identifier: MIT. Datasheet-derived nominal geometry; see ../README.md.')
 p.write_text(p.read_text().rstrip()+'\n');j[name]={'obj':str(p.relative_to(ROOT.parents[1])),'source':source,'bounds':q.bounds.tolist(),'size':dict(zip('xyz',q.extents.tolist()))}
# Vishay p.6: 5.5 x 4 x 5.7 body, radial 3mm gap, beam at z4.5.
body=box((5.5,4,.8),(0,0,.4))
for x in [-2.125,2.125]:body+=box((1.25,4,4.9),(x,0,3.25))
leads=m.Manifold()
for x,width in [(-2.45,1.9),(2,1.0)]:
 for y in [-1.4,0,1.4]:leads+=box((width,.45,.15),(x,y,.075))
export('tcut1600',body,leads,'https://www.vishay.com/docs/84174/tcut1600x01.pdf')
# NKK G12AH right-angle pin 5/common is the origin. Moulding details omitted.
body=box((7,7,4.5),(0,2.45,2.65))
bush=m.Manifold.cylinder(1.6,2,2,64).rotate((-90,0,0)).translate((0,5.95,2.6));body+=bush
lever=m.Manifold.cylinder(3.8,.85,.85,48).rotate((-90,0,0)).rotate((28,0,0)).translate((0,7.55,2.6));body+=lever
leads=m.Manifold()
for x,y in [(-2.54,0),(0,0),(2.54,0),(-2.54,5.08),(2.54,5.08)]:
 leads+=box((.4,.4,2.8),(x,y,-1.0))
export('g12ah',body,leads,'https://www.nkkswitches.com/pdf/Gtoggles.pdf')
(ROOT/'models.json').write_text(json.dumps(j,indent=2)+'\n')
