#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Reconstruct the product in assembly coordinates.
Run after generate.py and scripts/export-pcb-cad.mjs. OBJ uses PCB-centred mm;
product GLBs use glTF-standard metres/+Y-up, with their floor at the origin.
"""
from pathlib import Path
import json, math, hashlib
import numpy as np
import trimesh
import manifold3d as manifold
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parent
P=json.loads((ROOT/'parameters.json').read_text())
OUT=ROOT/'cad';OUT.mkdir(exist_ok=True)
BOARD_CENTER=P['pcb_bottom_z']+P['pcb_thickness']/2
parts={};description={}
colors={'base':'#344752','lid':'#6b8797','knob':'#e9bd65','outer-retainer':'#24292d','inner-retainer':'#95a5ad','screen-bezel':'#95a5ad','button-plunger':'#de744e','bearing':'#b7bec5','battery':'#acc1c6','fasteners':'#69747e','battery-socket':'#ebe8dd','toggle-switch':'#334047','charger-package':'#37393b','usb-esd-package':'#37393b','programming-socket':'#ebe8dd','display-socket':'#ebe8dd','optical-sensor':'#232127','screen-module':'#2e5846','screen-glass':'#091c24','screen-ui':'#ffffff'}
explosion={'base':-18,'battery':-6,'battery-socket':0,'charger-package':0,'usb-esd-package':0,'toggle-switch':0,'programming-socket':0,'display-socket':0,'optical-sensor':0,'button-plunger':12,'lid':27,'outer-retainer':38,'bearing':48,'inner-retainer':62,'screen-module':81,'screen-glass':81,'screen-ui':81,'screen-bezel':94,'fasteners':106,'knob':130}
for old in OUT.glob('*.obj'):old.unlink()
def add(name,mesh,note,preserve_colors=False):
 mesh=mesh.copy()
 if not preserve_colors:mesh.visual=trimesh.visual.ColorVisuals(mesh,vertex_colors=trimesh.visual.color.hex_to_rgba(colors[name]))
 mesh.metadata={'name':name,'description':note};parts[name]=mesh;description[name]=note
poses=json.loads((ROOT/'print-poses.json').read_text())
printed_names=[name for name in poses if name!='fit-coupon']
for name in printed_names:
 mesh=trimesh.load(ROOT/'stl'/f'{name}.stl',force='mesh');pose=poses[name]
 if pose['inverted']:
  mesh.apply_transform(trimesh.transformations.rotation_matrix(math.pi,[1,0,0]));mesh.apply_translation([0,0,pose['z']])
 else:mesh.apply_translation([0,0,pose['z']])
 add(name,mesh,'Exact printable mesh restored to assembly pose; see print-poses.json')
def solid_mesh(s):
    a=s.to_mesh();return trimesh.Trimesh(np.asarray(a.vert_properties)[:,:3],np.asarray(a.tri_verts),process=True)
def cyl(r,h,z=0,x=0,y=0):return manifold.Manifold.cylinder(h,r,r,96).translate((x,y,z))
def box(size,at):return trimesh.creation.box(size,transform=trimesh.transformations.translation_matrix(at))
b=P['bearing'];bearing=cyl(b['od']/2,b['width'],b['bottom_z'])-cyl(b['id']/2,b['width']+.2,b['bottom_z']-.1)
add('bearing',solid_mesh(bearing),'NSK 6806ZZ bearing 30 x 42 x 7 mm; catalog envelope, internals omitted')
add('battery',box(P['battery_envelope'],P['battery_center']),'Protected 350 mAh cell allowance; inspect real pouch and wiring')
add('battery-socket',box((6,4.5,6),(16,-15.55,7)),'J2 bottom-side JST housing allowance; cable omitted')
tail=P['header_tail_below_pcb_mm'];tail_z=P['pcb_bottom_z']-tail
add('programming-socket',trimesh.util.concatenate([box((13.9,4.5,6),(0,-20.55,14.6))]+[solid_mesh(cyl(.35,tail,tail_z,x,-20)) for x in [-5,-3,-1,1,3,5]]),'J4 JST-PH6 housing and tails trimmed to 0.8mm below PCB; top entry, pin 1 at (-5,-20)')
add('display-socket',trimesh.util.concatenate([box((4.5,17.9,6),(.55,0,14.6))]+[solid_mesh(cyl(.35,tail,tail_z,0,y)) for y in [-7,-5,-3,-1,1,3,5,7]]),'J6 JST-PH8 with 0.8mm trimmed tails; vertical row through the fixed hollow post')
# NKK G12AH dimensioned body/bushing/lever envelope; nominal centre position.
body=box((7,7,4.5),(-22.45,-14,14.2));lever=[]
for radius,length,start in [(2,1.6,-25.95),(.85,3.8,-27.55)]:
 q=solid_mesh(cyl(radius,length));q.apply_transform(trimesh.transformations.rotation_matrix(-math.pi/2,[0,1,0]));q.apply_translation([start,-14,14.2]);lever.append(q)
add('toggle-switch',trimesh.util.concatenate([body]+lever),'NKK G12AH left-facing lever; envelope and neutral pose, not a detailed supplier model')
sensor=[]
for x in [-2.125,2.125]:
 q=box((1.25,4,5.7),(x,0,14.45));q.apply_transform(trimesh.transformations.rotation_matrix(math.radians(P['encoder']['rotation_deg']),[0,0,1]));q.apply_translation([-23,10,0]);sensor.append(q)
add('optical-sensor',trimesh.util.concatenate(sensor),'TCUT1600X01_A envelope; 3mm optical gap, 4.5mm beam height above PCB')
add('charger-package',box((3,3,1),(15,8,12.1)),'U4 package envelope; copper pins in PCB model')
add('usb-esd-package',box((1.6,2.9,1.45),(0,18,12.325)),'U6 package envelope; copper pins in PCB model')
# Waveshare circular PCB with its connector tab pointing +X. A conservative
# rear connector envelope is included; supplied cable and component detail omitted.
lcdboard=cyl(18.75,1,42)+manifold.Manifold.cube((3.95,14.28,1),True).translate((19.675,0,42.5))
add('screen-module',trimesh.util.concatenate([solid_mesh(lcdboard),box((4.5,17.9,8),(11.5,0,38))]),'Waveshare 19192 37.5mm PCB / 40.4mm overall tab envelope; underside housing is an allowance')
add('screen-glass',solid_mesh(cyl(16.8,2.6,43)),'LCD front envelope; active diameter 32.4mm, front z45.6')
# Show an example generated by the actual firmware row renderer, not an invented UI.
from PIL import Image
im=np.array(Image.open(ROOT.parent/'previews/screen-ui.png').resize((240,240),Image.Resampling.NEAREST).convert('RGBA'))
verts=[];faces=[];rgba=[];pitch=32.4/240
for y in range(240):
 x=0
 while x<240:
  if im[y,x,3]==0 or np.array_equal(im[y,x,:3],im[120,0,:3]):x+=1;continue
  start=x;color=im[y,x].copy()
  while x<240 and np.array_equal(im[y,x],color):x+=1
  left=(start-120)*pitch;right=(x-120)*pitch;top=(120-y)*pitch;bottom=top-pitch;n=len(verts)
  verts.extend([(left,bottom,45.61),(right,bottom,45.61),(right,top,45.61),(left,top,45.61)]);faces.extend([(n,n+1,n+2),(n,n+2,n+3)]);rgba.extend([color]*4)
ui=trimesh.Trimesh(verts,faces,vertex_colors=np.array(rgba),process=False)
add('screen-ui',ui,'Illustrative count 12345, 3.92 V, scrolling/USB/charge status from the tested firmware renderer',True)
fasteners=[]
for x,y in P['mount_holes']:fasteners.extend([cyl(1.25,6,5.6,x,y),cyl(2.25,1.3,11.6,x,y)])
for x,y in [(26,26),(-26,-26)]:fasteners.extend([cyl(1,P['lid_screw_length_mm'],20.7-P['lid_screw_length_mm'],x,y),cyl(2,1.2,20.7,x,y)])
for i in range(3):
 a=2*math.pi*i/3;x,y=13*math.cos(a),13*math.sin(a)
 fasteners.extend([cyl(1,8,22.6,x,y),cyl(1.9,1.6,30.6,x,y)])
 x,y=23.2*math.cos(a),23.2*math.sin(a)
 fasteners.extend([cyl(1,4.8,22,x,y),manifold.Manifold.cylinder(1.2,2.1,1.1,64).translate((x,y,20.8))])
for x,y in [(-22.2,0),(0,22.2),(0,-22.2)]:
 fasteners.extend([cyl(1,4.8,41,x,y),manifold.Manifold.cylinder(1.2,1.1,2.1,64).translate((x,y,45.8))])
add('fasteners',trimesh.util.concatenate([solid_mesh(q) for q in fasteners]),'Dimensioned shanks/heads illustrate access; threads and drive recesses omitted')
# Native tscircuit GLB: exported (-X, +Z, +Y). Convert back to PCB +Z-up.
pcb=trimesh.load(OUT/'pcb-source.glb',force='scene')
for mesh in pcb.geometry.values():mesh.merge_vertices()
pcb.export(OUT/'pcb-source.glb')
to_cad=np.array([[-1,0,0,0],[0,0,1,0],[0,1,0,BOARD_CENTER],[0,0,0,1]],float)
pcb_geometry=[]
for node in pcb.graph.nodes_geometry:
    transform,geometry=pcb.graph[node];mesh=pcb.geometry[geometry].copy()
    mesh.apply_transform(to_cad@transform);mesh.merge_vertices();pcb_geometry.append((node,mesh))
assert np.isclose(min(m.bounds[0,2] for _,m in pcb_geometry),P['pcb_bottom_z'],atol=.01)
# Keep every authored part separate and named in both GLBs for hide/select tools.
# Rotate +Z-up CAD to glTF +Y-up and convert mm to metres.
to_gltf=np.array([[.001,0,0,0],[0,0,.001,0],[0,-.001,0,0],[0,0,0,1]],float)
for exploded in [False,True]:
    scene=trimesh.Scene()
    for name,mesh in parts.items():
        transform=to_gltf@trimesh.transformations.translation_matrix([0,0,explosion[name] if exploded else 0])
        scene.add_geometry(mesh,node_name=name,geom_name=name,transform=transform)
    for name,mesh in pcb_geometry:
        transform=to_gltf@trimesh.transformations.translation_matrix([0,0,0])
        scene.add_geometry(mesh,node_name='pcb-'+name,geom_name='pcb-'+name,transform=transform)
    scene.metadata={'description':'Desk fidget counter Rev B '+('exploded assembly' if exploded else 'assembled product'),'units':'metres','hardware_model_detail':'Printed parts exact; purchased hardware/package models illustrative. See ASSEMBLY.md.'}
    path=OUT/('exploded.glb' if exploded else 'assembled.glb');scene.export(path)
    reloaded=trimesh.load(path,force='scene');assert len(reloaded.geometry)>=len(parts)
    if not exploded:assert np.allclose(reloaded.extents,[.080,.047,.080],atol=.0001),reloaded.extents
# Per-part OBJ assets use tscircuit's board-centred mm frame. Vertex colours
# survive its OBJ loader. Printed STLs remain in their original print frame.
records=[]
for name,mesh in parts.items():
    asset=mesh.copy();asset.apply_translation([0,0,-BOARD_CENTER])
    asset.export(OUT/f'{name}.obj',include_color=True,include_normals=False,header='SPDX-License-Identifier: MIT; PCB-centred millimetres, +Z up')
    record={'name':name,'printed':name in printed_names,'color':colors[name],'asset':f'{name}.obj','bounds_pcb_mm':asset.bounds.round(6).tolist(),'explode_z_mm':explosion[name],'description':description[name]}
    records.append(record)
(OUT/'parts.json').write_text(json.dumps(records,indent=2)+'\n')
# Exterior rendering uses the exact assembled meshes and the firmware UI.
fig=plt.figure(figsize=(10,8));ax=fig.add_subplot(111,projection='3d');triangles=[];facecolors=[]
for name in ['base','lid','knob','screen-bezel','toggle-switch','screen-glass']:
 mesh=parts[name];triangles.extend(mesh.triangles);facecolors.extend(mesh.visual.face_colors/255)
ax.computed_zorder=False
ax.add_collection3d(Poly3DCollection(triangles,facecolors=np.asarray(facecolors,dtype=float),edgecolor='none',zsort='average',zorder=1))
# The planar UI is entirely inside the bezel window. Draw it last in this
# painter-style preview; the GLB uses its normal depth-tested physical pose.
ui=parts['screen-ui'];ax.add_collection3d(Poly3DCollection(ui.triangles,facecolors=np.asarray(ui.visual.face_colors,dtype=float)/255,edgecolor='none',zorder=10))
ax.set(xlim=(-42,42),ylim=(-42,42),zlim=(0,50));ax.set_box_aspect((84,84,50));ax.view_init(55,-110);ax.set_axis_off()
ax.set_title('Desk knob Rev B — fixed 1.28-inch display\nRotating grip ring / left toggle / Ø80 × 47 mm',pad=10)
fig.tight_layout();fig.savefig(ROOT/'assembly.png',dpi=160);plt.close(fig)
# Exploded assembly overview for the guide. Offsets are illustrative movements,
# not claimed disassembly trajectories; assembled dimensions remain authoritative.
fig=plt.figure(figsize=(11,12));ax=fig.add_subplot(111,projection='3d');polys=[];facecolors=[]
for name,mesh in parts.items():
    if name in ['charger-package','usb-esd-package','toggle-switch','battery-socket','programming-socket','display-socket','optical-sensor','fasteners','screen-ui','screen-glass']:continue
    display=mesh.copy();display.apply_translation([0,0,explosion[name]])
    polys.extend(display.triangles);facecolors.extend([colors[name]]*len(display.faces))
    x,y,z=display.centroid;ax.text(43,0,z,name,fontsize=8)
for name,mesh in pcb_geometry:
    display=mesh.copy();display.apply_translation([0,0,0]);polys.extend(display.triangles);facecolors.extend(['#246b47']*len(display.faces))
ax.add_collection3d(Poly3DCollection(polys,facecolors=facecolors,edgecolor='none',zsort='average'))
ax.set(xlim=(-42,65),ylim=(-42,42),zlim=(-20,185),xlabel='X / mm',ylabel='Y / mm',zlabel='Z / mm')
ax.set_box_aspect((107,84,205));ax.view_init(18,-60);ax.set_title('Desk knob Rev B — exploded assembly\nIllustrative separation; assembled product is Ø80 × 47 mm')
fig.tight_layout();fig.savefig(ROOT/'exploded.png',dpi=140);plt.close(fig)
report={'assembly_frame':'CAD mm, floor z=0; PCB centre z=10.8','glb_frame':'glTF metres, +Y up; assembled extents [0.080,0.047,0.080] m','part_count':len(parts),'source_board_tsx_sha256':hashlib.sha256((ROOT.parent/'index.circuit.tsx').read_bytes()).hexdigest(),'printed_meshes_restored_from_print_orientation':len(printed_names),'cad_files':{name:{'bytes':(OUT/name).stat().st_size,'sha256':hashlib.sha256((OUT/name).read_bytes()).hexdigest()} for name in ['assembled.glb','exploded.glb']},'physical_fit':'Unmeasured; envelope models do not replace datasheet/physical fit verification'}
(OUT/'assembly-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
