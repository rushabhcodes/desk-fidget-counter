#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
from pathlib import Path
import shutil,subprocess,json,sys
import trimesh,numpy as np
root=Path(__file__).resolve().parents[2];out=root/'mechanical/vendor';lib=Path('/usr/share/kicad/3dmodels')
models={
'header8-ra':'Connector_PinHeader_2.54mm.3dshapes/PinHeader_1x08_P2.54mm_Horizontal.step',
'b3u3000':'Button_Switch_SMD.3dshapes/SW_SPST_B3U-3000P.step',
'lqfp48':'Package_QFP.3dshapes/LQFP-48_7x7mm_P0.5mm.step',
'soic8':'Package_SO.3dshapes/SOIC-8_3.9x4.9mm_P1.27mm.step',
'sot23-5':'Package_TO_SOT_SMD.3dshapes/SOT-23-5.step',
'sot23-6':'Package_TO_SOT_SMD.3dshapes/SOT-23-6.step',
'sc70-6':'Package_TO_SOT_SMD.3dshapes/SOT-363_SC-70-6.step',
'c0402':'Capacitor_SMD.3dshapes/C_0402_1005Metric.step',
'c0603':'Capacitor_SMD.3dshapes/C_0603_1608Metric.step',
'c0805':'Capacitor_SMD.3dshapes/C_0805_2012Metric.step',
'r0603':'Resistor_SMD.3dshapes/R_0603_1608Metric.step',
'sod323':'Diode_SMD.3dshapes/D_SOD-323.step',
'led0603':'LED_SMD.3dshapes/LED_0603_1608Metric.step',
'jst-ph6':'Connector_JST.3dshapes/JST_PH_B6B-PH-K_1x06_P2.00mm_Vertical.step',
'jst-ph8':'Connector_JST.3dshapes/JST_PH_S8B-PH-K_1x08_P2.00mm_Horizontal.step'}
records=json.loads((out/'models.json').read_text()) if (out/'models.json').exists() else {}
for name,relative in models.items():
 if len(sys.argv)>1 and name not in sys.argv[1:]:continue
 src=lib/relative;step=out/'step'/src.name
 if not step.exists():shutil.copyfile(src,step)
 ply=Path('/tmp')/f'desk-vendor-{name}.ply'
 subprocess.run([sys.executable,str(root/'mechanical/step-mesh.py'),str(step),str(ply)],check=True,stdout=subprocess.DEVNULL)
 mesh=trimesh.load(ply,force='mesh');colors=np.tile([50,52,55,255],(len(mesh.vertices),1))
 if name.startswith('jst-'):
  mesh.apply_translation([-5 if name=='jst-ph6' else -7,0,0]);mesh.vertices[:,2]=np.maximum(mesh.vertices[:,2],-2.4)
  mesh.update_faces(mesh.nondegenerate_faces());mesh.merge_vertices()
  colors=np.tile([231,228,212,255],(len(mesh.vertices),1));colors[mesh.vertices[:,2]<0]=[170,176,182,255]
 elif name=='header8-ra':
  mesh.apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2,[0,0,1]));mesh.apply_translation([8.89,0,0])
  mesh.vertices[:,2]=np.maximum(mesh.vertices[:,2],-2.4)
  mesh.update_faces(mesh.nondegenerate_faces());mesh.merge_vertices()
  colors=np.tile([40,42,47,255],(len(mesh.vertices),1));colors[(mesh.vertices[:,1]<-4.04)|(mesh.vertices[:,2]<0)]=[190,171,95,255]
 else:
  # Material colours only; package geometry is unchanged from the upstream STEP.
  span=mesh.extents;coords=mesh.vertices
  if name.startswith(('r','c','led')):
   colors[:]=[169,133,83,255] if name.startswith('c') else [48,52,57,255]
   colors[np.abs(coords[:,0])>span[0]*.33]=[183,190,195,255]
  else:colors[coords[:,2]<.35]=[183,190,195,255]
 mesh.visual=trimesh.visual.ColorVisuals(mesh,vertex_colors=colors)
 obj=out/'obj'/f'{name}.obj';mesh.export(obj,include_color=True,include_normals=False,header='KiCad package model derivative. CC-BY-SA-4.0 with ECAD exception. See ../README.md and source STEP notices.')
 obj.write_text(obj.read_text().rstrip()+'\n')
 records[name]={'step':str(step.relative_to(root)),'obj':str(obj.relative_to(root)),'source':'https://gitlab.com/kicad/libraries/kicad-packages3D/-/blob/master/'+relative,'bounds':mesh.bounds.tolist(),'size':dict(zip('xyz',mesh.extents.tolist())),'pin_tail_trim_mm':.8 if name.startswith('jst') else None}
 if name=='b3u3000':
  solid=out/'solid'/'b3u3000.ply';solid.parent.mkdir(exist_ok=True)
  subprocess.run([sys.executable,str(root/'mechanical/step-mesh.py'),str(step),str(solid),'--preserve-seams'],check=True)
  Path(str(solid)+'.faces.npz').unlink(missing_ok=True)
  records[name]['collision_mesh']=str(solid.relative_to(root))
 print(name,mesh.bounds.round(3).tolist(),flush=True)
(out/'models.json').write_text(json.dumps(records,indent=2)+'\n')

(out/'solid').mkdir(exist_ok=True)
for part in ([] if len(sys.argv)>1 else ['C165948','C720477']):
 subprocess.run([sys.executable,str(root/'mechanical/step-mesh.py'),str(out/'step'/f'{part}.step'),str(out/'solid'/f'{part}.ply')],check=True)
