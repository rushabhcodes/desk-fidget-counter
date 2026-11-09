#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Unscaled supplier STEP, transformed only to its exact imported footprint datum."""
from pathlib import Path
import sys,tempfile,subprocess,json
import numpy as np,trimesh
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'mechanical/vendor'
source=ROOT/'imports/jlc/SM08B_SRSS_TB_LF__SN_/SM08B_SRSS_TB_LF__SN_.step'
with tempfile.TemporaryDirectory(prefix='jst-sh8-') as tmp:
 p=Path(tmp)/'header.ply'
 subprocess.run([sys.executable,str(ROOT/'mechanical/step-mesh.py'),str(source),str(p),'--preserve-seams'],check=True)
 mesh=trimesh.load(p,force='mesh',process=False)
mesh.apply_translation(-np.array([3.5,.40673090000004786,-.01]))
assert mesh.is_watertight
mesh.visual=trimesh.visual.ColorVisuals(mesh,vertex_colors=np.tile([211,208,190,255],(len(mesh.vertices),1)))
mesh.export(OUT/'obj/jst-sh8.obj',include_color=True);mesh.export(OUT/'solid/jst-sh8.ply')
p=OUT/'models.json';d=json.loads(p.read_text());d['jst-sh8']={'step':str(source.relative_to(ROOT)),'obj':'mechanical/vendor/obj/jst-sh8.obj','collision_mesh':'mechanical/vendor/solid/jst-sh8.ply','source':'tsci import --jlcpcb --use-exact-footprint --exclude-pin-attributes --download C160407','manufacturer':'JST','MPN':'SM08B-SRSS-TB(LF)(SN)','datasheet':'https://www.jst-mfg.com/product/pdf/eng/eSH.pdf','bounds':mesh.bounds.tolist(),'size':dict(zip('xyz',mesh.extents.tolist())),'datum_note':'Rigid supplier datum subtraction (3.5,0.4067309,-0.01); no scaling, trimming or altered footprint.','derivative_generator':'mechanical/vendor/generate-jst-sh8.py','supplier_model_geometry_unscaled':True};p.write_text(json.dumps(d,indent=2)+'\n');print(mesh.bounds)
