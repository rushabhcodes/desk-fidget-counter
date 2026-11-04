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
colors={'base':'#344752','lid':'#6b8797','knob':'#e9bd65','outer-retainer':'#cd9647','inner-retainer':'#95a5ad','button-plunger':'#de744e','bearing':'#b7bec5','magnet':'#46505a','battery':'#acc1c6','fasteners':'#69747e','battery-socket':'#ebe8dd','slide-switch':'#334047','charger-package':'#37393b','usb-esd-package':'#37393b'}
explosion={'base':-18,'battery':-6,'battery-socket':0,'charger-package':0,'usb-esd-package':0,'slide-switch':0,'button-plunger':30,'lid':34,'outer-retainer':42,'bearing':52,'magnet':67,'inner-retainer':65,'fasteners':78,'knob':88}
def add(name,mesh,note):
    mesh=mesh.copy();mesh.visual=trimesh.visual.ColorVisuals(mesh,vertex_colors=trimesh.visual.color.hex_to_rgba(colors[name]))
    mesh.metadata={'name':name,'description':note}
    parts[name]=mesh;description[name]=note
for name,z in [('base',0),('lid',14.2),('outer-retainer',15.8),('inner-retainer',24),('button-plunger',13.6),('knob',0)]:
    mesh=trimesh.load(ROOT/'stl'/f'{name}.stl',force='mesh')
    if name=='knob':
        mesh.apply_transform(trimesh.transformations.rotation_matrix(math.pi,[1,0,0]));mesh.apply_translation([0,0,31])
    else:mesh.apply_translation([0,0,z])
    add(name,mesh,'Exact printable mesh, restored from print orientation to assembly pose')
def solid_mesh(s):
    a=s.to_mesh();return trimesh.Trimesh(np.asarray(a.vert_properties)[:,:3],np.asarray(a.tri_verts),process=True)
def cyl(r,h,z=0,x=0,y=0):return manifold.Manifold.cylinder(h,r,r,96).translate((x,y,z))
def box(size,at):return trimesh.creation.box(size,transform=trimesh.transformations.translation_matrix(at))
b=P['bearing'];bearing=cyl(b['od']/2,b['width'],b['bottom_z'])-cyl(b['id']/2,b['width']+.2,b['bottom_z']-.1)
add('bearing',solid_mesh(bearing),'6805 bearing 25 x 37 x 7 mm; simplified catalog envelope, no internal balls')
m=P['magnet'];add('magnet',solid_mesh(cyl(m['diameter']/2,m['thickness'],m['bottom_z'])),'D42DIA diametric magnet; envelope only')
add('battery',box(P['battery_envelope'],P['battery_center']),'Protected 350 mAh cell allowance; inspect real pouch and wiring before assembly')
add('battery-socket',box((6,4.5,6),(16,-15.55,7)),'J2 bottom-side JST housing envelope; contacts and mating cable omitted')
add('slide-switch',box((4.3,8.6,6.2),(-28,-1,14.7)),'SW1 case envelope; lever detail omitted')
add('charger-package',box((3,3,1),(15,8,12.1)),'U4 package envelope; detailed leads are in PCB fabrication geometry')
add('usb-esd-package',box((1.6,2.9,1.45),(0,18,12.325)),'U6 package envelope; detailed leads are in PCB fabrication geometry')
fasteners=[]
for x,y in P['mount_holes']:fasteners.extend([cyl(1.25,6,5.6,x,y),cyl(2.25,1.3,11.6,x,y)])
for x,y in [(24.4,24.4),(-24.4,-24.4)]:fasteners.extend([cyl(1,6,10.1,x,y),cyl(2,1,16.1,x,y)])
for i in range(3):
    a=2*math.pi*i/3;x,y=9*math.cos(a),9*math.sin(a)
    fasteners.extend([cyl(1,8,17.6,x,y),cyl(1.9,1.6,25.6,x,y)])
    x,y=20.5*math.cos(a),20.5*math.sin(a)
    fasteners.extend([cyl(1,4.8,17,x,y),manifold.Manifold.cylinder(1.2,2.1,1,64).translate((x,y,15.8))])
add('fasteners',trimesh.util.concatenate([solid_mesh(s) for s in fasteners]),'Fastener shanks/heads illustrate assembly access; threads and drive recesses omitted')
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
    scene.metadata={'description':'Desk fidget counter Rev A '+('exploded assembly' if exploded else 'assembled product'),'units':'metres','hardware_model_detail':'Printed parts exact; purchased hardware/package models illustrative. See ASSEMBLY.md.'}
    path=OUT/('exploded.glb' if exploded else 'assembled.glb');scene.export(path)
    reloaded=trimesh.load(path,force='scene');assert len(reloaded.geometry)>=len(parts)
    if not exploded:assert np.allclose(reloaded.extents,[.072,.031,.072],atol=.0001),reloaded.extents
# Per-part OBJ assets use tscircuit's board-centred mm frame. Vertex colours
# survive its OBJ loader. Printed STLs remain in their original print frame.
records=[]
for name,mesh in parts.items():
    asset=mesh.copy();asset.apply_translation([0,0,-BOARD_CENTER])
    asset.export(OUT/f'{name}.obj',include_color=True,include_normals=False,header='SPDX-License-Identifier: MIT; PCB-centred millimetres, +Z up')
    record={'name':name,'printed':name in ['base','lid','knob','outer-retainer','inner-retainer','button-plunger'],'color':colors[name],'asset':f'{name}.obj','bounds_pcb_mm':asset.bounds.round(6).tolist(),'explode_z_mm':explosion[name],'description':description[name]}
    records.append(record)
(OUT/'parts.json').write_text(json.dumps(records,indent=2)+'\n')
# Exploded assembly overview for the guide. Offsets are illustrative movements,
# not claimed disassembly trajectories; assembled dimensions remain authoritative.
fig=plt.figure(figsize=(11,12));ax=fig.add_subplot(111,projection='3d');polys=[];facecolors=[]
for name,mesh in parts.items():
    if name in ['charger-package','usb-esd-package','slide-switch','battery-socket','fasteners']:continue
    display=mesh.copy();display.apply_translation([0,0,explosion[name]])
    polys.extend(display.triangles);facecolors.extend([colors[name]]*len(display.faces))
    x,y,z=display.centroid;ax.text(39,0,z,name,fontsize=8)
for name,mesh in pcb_geometry:
    display=mesh.copy();display.apply_translation([0,0,0]);polys.extend(display.triangles);facecolors.extend(['#246b47']*len(display.faces))
ax.add_collection3d(Poly3DCollection(polys,facecolors=facecolors,edgecolor='none',zsort='average'))
ax.set(xlim=(-38,58),ylim=(-38,38),zlim=(-20,123),xlabel='X / mm',ylabel='Y / mm',zlabel='Z / mm')
ax.set_box_aspect((96,76,143));ax.view_init(18,-60);ax.set_title('Desk knob Rev A — exploded assembly\nIllustrative separation; assembled product is Ø72 × 31 mm')
fig.tight_layout();fig.savefig(ROOT/'exploded.png',dpi=140);plt.close(fig)
report={'assembly_frame':'CAD mm, floor z=0; PCB centre z=10.8','glb_frame':'glTF metres, +Y up; assembled extents [0.072,0.031,0.072] m','part_count':len(parts),'source_board_tsx_sha256':hashlib.sha256((ROOT.parent/'index.circuit.tsx').read_bytes()).hexdigest(),'printed_meshes_restored_from_print_orientation':6,'cad_files':{name:{'bytes':(OUT/name).stat().st_size,'sha256':hashlib.sha256((OUT/name).read_bytes()).hexdigest()} for name in ['assembled.glb','exploded.glb']},'physical_fit':'Unmeasured; envelope models do not replace datasheet/physical fit verification'}
(OUT/'assembly-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
