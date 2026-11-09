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
HEIGHT=P['display']['bezel_top_z'];SCREEN_OFFSET=P['display']['pcb_bottom_z']+.45;SCREEN_UI_Z=P['display']['front_z']+.01
OUT=ROOT/'cad';OUT.mkdir(exist_ok=True)
BOARD_CENTER=P['pcb_bottom_z']+P['pcb_thickness']/2
parts={};description={}
colors={'base':'#344752','lid':'#6b8797','knob':'#e9bd65','screen-carrier':'#95a5ad','screen-bezel':'#95a5ad','button-cap':'#26343d','bearing':'#b7bec5','fasteners':'#69747e','screen-module':'#2e5846','screen-ui':'#ffffff'}
explosion={'base':-18,'lid':27,'bearing':48,'screen-carrier':62,'screen-module':81,'screen-ui':81,'screen-bezel':94,'button-cap':-4,'fasteners':106,'knob':130}
for old in OUT.glob('*.obj'):old.unlink()
def add(name,mesh,note,preserve_colors=False):
 mesh=mesh.copy()
 if not preserve_colors:mesh.visual=trimesh.visual.ColorVisuals(mesh,vertex_colors=trimesh.visual.color.hex_to_rgba(colors[name]))
 mesh.metadata={'name':name,'description':note};parts[name]=mesh;description[name]=note
poses=json.loads((ROOT/'print-poses.json').read_text())
printed_names=[name for name in poses if not name.startswith('fit-coupon')]
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
from bearing import build as build_bearing
bearing_meshes,_,bearing_report=build_bearing(P)
(ROOT/'bearing-model.json').write_text(json.dumps(bearing_report,indent=2)+'\n')
# One purchased bearing has one selectable/visible assembly object. Keep every
# internal surface and its colour while combining the six constituent meshes.
bearing_pieces=[]
for name,mesh in bearing_meshes.items():
 color='#c8ced3' if name.endswith('balls') else '#687780' if name.endswith('cage') else '#929da5' if 'shield' in name else '#b7bec5'
 piece=mesh.copy()
 piece.visual=trimesh.visual.ColorVisuals(piece,vertex_colors=trimesh.visual.color.hex_to_rgba(color))
 bearing_pieces.append(piece)
add('bearing',trimesh.util.concatenate(bearing_pieces),
 'Complete 6712ZZ bearing, including both races, both shields, balls and cage; verified 60x75x7 envelope, accepted approximate internals',True)
assert len(parts['bearing'].faces)==sum(len(mesh.faces) for mesh in bearing_meshes.values())
assert np.allclose(parts['bearing'].bounds,[np.min([m.bounds[0] for m in bearing_meshes.values()],axis=0),np.max([m.bounds[1] for m in bearing_meshes.values()],axis=0)])
# Six compliant pads avoid clamping a variable-thickness PCB between hard faces.
capture=P['pcb_capture'];top=P['pcb_bottom_z']+P['pcb_thickness'];pads=[];adhesive=[]
for x,y,radius in [*( (x,y,2.0) for x,y in P['mount_holes']),*((x,y,1.3) for x,y in capture['front_pad_centers'])]:
 pads.append(cyl(radius,capture['compressed_pad_height']-capture['adhesive_thickness'],top,x,y))
 adhesive.append(cyl(radius,capture['adhesive_thickness'],top+capture['compressed_pad_height']-capture['adhesive_thickness'],x,y))
for name,solids,color in [('pcb-capture-pads',pads,'#24292d'),('pcb-pad-adhesive',adhesive,'#bbc4c9')]:
 colors[name]=color;explosion[name]=27
 add(name,trimesh.util.concatenate([solid_mesh(q) for q in solids]),'PORON 4701-30-20062-04 pads, 1.57mm free thickness; drawn compressed under lid, with 0.05mm 467MP adhesive')
# Exact rigid manufacturer STEP geometry, tessellated without axis scaling.
screen=trimesh.load(ROOT/'vendor/obj/screen19192.obj',force='mesh',process=True)
screen.apply_transform(np.diag([-1.,1.,-1.,1.]));screen.apply_translation([0,0,SCREEN_OFFSET])
add('screen-module',screen,'Waveshare 19192 official STEP 0508, rigid 180deg Y rotation, tab -X; 40.4531 x 37.5 x 9.2mm',True)
from harness import build as build_harness
harness_meshes,harness_report=build_harness()
(ROOT/'harness.json').write_text(json.dumps(harness_report,indent=2)+'\n')
for name,mesh in harness_meshes.items():
 colors[name]='#20262c' if name=='lcd-cable-board-plugs' else '#b9b9ac' if 'plug' in name else '#adb6bf' if 'contacts' in name else '#30343a' if 'sleeves' in name else '#ffffff'
 explosion[name]=40
 add(name,mesh,'Included Waveshare display lead, both factory ends retained, shortened in its middle with insulated splices; nominal plug/wire envelopes, see harness.json',name.startswith('lcd-wire-'))
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
  verts.extend([(left,bottom,SCREEN_UI_Z),(right,bottom,SCREEN_UI_Z),(right,top,SCREEN_UI_Z),(left,top,SCREEN_UI_Z)]);faces.extend([(n,n+1,n+2),(n,n+2,n+3)]);rgba.extend([color]*4)
ui=trimesh.Trimesh(verts,faces,vertex_colors=np.array(rgba),process=False)
add('screen-ui',ui,'Illustrative laptop clock, CPU, RAM, laptop battery and turns from the tested firmware renderer',True)
fasteners=[]
def csk(x,y,z,up=False,length=6):
 # DIN965 M2 nominal: dk3.8, k1.2, 90deg cone plus 0.3mm rim.
 if up:solids=[cyl(1,length-1.2,z+1.2,x,y),cyl(1.9,.3,z,x,y),manifold.Manifold.cylinder(.9,1.9,1,64).translate((x,y,z+.3))]
 else:solids=[cyl(1,length-1.2,z-length,x,y),cyl(1.9,.3,z-.3,x,y),manifold.Manifold.cylinder(.9,1,1.9,64).translate((x,y,z-1.2))]
 body=manifold.Manifold.batch_boolean(solids,manifold.OpType.Add)
 # Cross recess is a visual approximation; outside head/shank dimensions stay
 # nominal. Select a driver to match the actual purchased DIN965 screw.
 level=z+.15 if up else z-.15
 recess=manifold.Manifold.cube((1.7,.45,.5),True).translate((x,y,level))+manifold.Manifold.cube((.45,1.7,.5),True).translate((x,y,level))
 return [body-recess]
for x,y in P['chassis_screw_axes']:fasteners.extend(csk(x,y,P['lid_top_z']))
for x,y in P['bezel_screw_axes']:fasteners.extend(csk(x,y,HEIGHT,length=10))
assert len(fasteners)==4
add('fasteners',trimesh.util.concatenate([solid_mesh(q) for q in fasteners]),'Four screws: two DIN965 M2x6 chassis screws and two M2x10 shared bezel/carrier screws; nominal dimensions, fine threads omitted')
# Native tscircuit GLB: exported (-X, +Z, +Y). Convert back to PCB +Z-up.
pcb=trimesh.load(OUT/'pcb-source.glb',force='scene')
for mesh in pcb.geometry.values():mesh.merge_vertices()
to_cad=np.array([[-1,0,0,0],[0,0,1,0],[0,1,0,BOARD_CENTER],[0,0,0,1]],float)
pcb_geometry=[]
for node in pcb.graph.nodes_geometry:
    transform,geometry=pcb.graph[node];mesh=pcb.geometry[geometry].copy()
    mesh.apply_transform(to_cad@transform);mesh.merge_vertices();pcb_geometry.append((node,mesh))
assert np.isclose(min(m.bounds[0,2] for name,m in pcb_geometry if name.startswith('Box')),P['pcb_bottom_z'],atol=.01)
assert min(m.bounds[0,2] for _,m in pcb_geometry)>=P['pcb_bottom_z']-P['header_tail_below_pcb_mm']-.01
# Keep every assembly part named in both GLBs for hide/select tools. The complete
# bearing is one object; its internals are never separate visibility entries.
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
    scene.metadata={'description':'Desk fidget counter Mechanics E10 '+('exploded assembly' if exploded else 'assembled product'),'units':'metres','hardware_model_detail':'Printed parts exact; official screen STEP and KiCad package models; bearing and cable internals use authorized best approximations. See mechanical/vendor/README.md.'}
    path=OUT/('exploded.glb' if exploded else 'assembled.glb');scene.export(path)
    reloaded=trimesh.load(path,force='scene');assert len(reloaded.geometry)>=len(parts)
    assert [n for n in reloaded.graph.nodes_geometry if n=='bearing' or n.startswith('bearing-')]==['bearing']
    if not exploded:
        assert abs(reloaded.extents[0]-P['base_diameter']*.001)<.0001 and abs(reloaded.extents[1]-HEIGHT*.001)<.0001
        expected_depth=(P['base_diameter']/2-P['front_button']['printed_cap']['face_front_y'])*.001
        assert abs(reloaded.extents[2]-expected_depth)<.0001, reloaded.extents
        assembled_size_mm=(reloaded.extents*1000).round(3).tolist()
# Per-part OBJ assets use tscircuit's board-centred mm frame. Vertex colours
# survive its OBJ loader. Printed STLs remain in their original print frame.
records=[]
for name,mesh in parts.items():
    asset=mesh.copy();asset.apply_translation([0,0,-BOARD_CENTER])
    if name.startswith('bearing-'):asset.visual=trimesh.visual.ColorVisuals(asset,vertex_colors=trimesh.visual.color.hex_to_rgba(colors[name]))
    asset.export(OUT/f'{name}.obj',include_color=True,include_normals=False,header='PCB-centred millimetres, +Z up. Vendor models retain upstream rights; see mechanical/vendor/README.md. Other geometry MIT.')
    obj_path=OUT/f'{name}.obj'
    obj_path.write_text(obj_path.read_text().rstrip()+'\n')
    record={'name':name,'printed':name in printed_names,'color':colors[name],'asset':f'{name}.obj','bounds_pcb_mm':asset.bounds.round(6).tolist(),'explode_z_mm':explosion[name],'description':description[name]}
    records.append(record)
(OUT/'parts.json').write_text(json.dumps(records,indent=2)+'\n')
# Exterior rendering uses the exact assembled meshes and the firmware UI.
fig=plt.figure(figsize=(10,8));ax=fig.add_subplot(111,projection='3d');triangles=[];facecolors=[]
for name in ['base','lid','knob','screen-bezel','screen-module','button-cap']:
 mesh=parts[name];triangles.extend(mesh.triangles);facecolors.extend(mesh.visual.face_colors/255)
ax.computed_zorder=False
ax.add_collection3d(Poly3DCollection(triangles,facecolors=np.asarray(facecolors,dtype=float),edgecolor='none',zsort='average',zorder=1))
# The planar UI is entirely inside the bezel window. Draw it last in this
# painter-style preview; the GLB uses its normal depth-tested physical pose.
ui=parts['screen-ui'];ax.add_collection3d(Poly3DCollection(ui.triangles,facecolors=np.asarray(ui.visual.face_colors,dtype=float)/255,edgecolor='none',zorder=10))
ax.set(xlim=(-45,45),ylim=(-45,45),zlim=(0,26));ax.set_box_aspect((90,90,26));ax.view_init(55,-110);ax.set_axis_off()
ax.set_title(f'Desk knob Mechanics E10 — fixed 1.28-inch display\nRotating grip ring / front printed mode button / Ø84.8 body × {HEIGHT:g} mm high',pad=10)
fig.tight_layout();fig.savefig(ROOT/'assembly.png',dpi=160);plt.close(fig)
# Exploded assembly overview for the guide. Offsets are illustrative movements,
# not claimed disassembly trajectories; assembled dimensions remain authoritative.
fig=plt.figure(figsize=(11,12));ax=fig.add_subplot(111,projection='3d');polys=[];facecolors=[]
for name,mesh in parts.items():
    if name=='screen-ui':continue
    display=mesh.copy();display.apply_translation([0,0,explosion[name]])
    polys.extend(display.triangles);facecolors.extend([colors[name]]*len(display.faces))
    x,y,z=display.centroid
    if name.startswith('lcd-'):
        if name=='lcd-cable-screen-plug':ax.text(43,0,z,'H1 LCD harness (8 wires)',fontsize=8)
    elif name=='pcb-pad-adhesive':
        pass  # Label the six foam/adhesive pairs together for a readable guide.
    else:
        label_z=z+5 if name=='screen-carrier' else z
        ax.text(43,0,label_z,'fasteners: 2 x M2x6 + 2 x M2x10' if name=='fasteners' else 'PCB capture: 6 foam/adhesive pairs' if name=='pcb-capture-pads' else name,fontsize=8)
for name,mesh in pcb_geometry:
    display=mesh.copy();display.apply_translation([0,0,0]);polys.extend(display.triangles);facecolors.extend(['#246b47']*len(display.faces))
ax.add_collection3d(Poly3DCollection(polys,facecolors=facecolors,edgecolor='none',zsort='average'))
ax.set(xlim=(-42,65),ylim=(-42,42),zlim=(-20,185),xlabel='X / mm',ylabel='Y / mm',zlabel='Z / mm')
ax.set_box_aspect((107,84,205));ax.view_init(18,-60);ax.set_title(f'Desk knob Mechanics E10 — six prints / four screws\nIllustrative separation; assembled product is Ø84.8 × {HEIGHT:g} mm')
fig.tight_layout();fig.savefig(ROOT/'exploded.png',dpi=140);plt.close(fig)
report={'assembly_frame':f'CAD mm, floor z=0; PCB centre z={BOARD_CENTER}','glb_frame':f'glTF metres, +Y up; 84.8mm body, {HEIGHT:g}mm height; front printed cap gives 86.6mm overall depth','assembled_size_gltf_xyz_mm':assembled_size_mm,'part_count':len(parts),'fastener_count':4,'product_print_count':len(printed_names),'source_parameters_sha256':hashlib.sha256((ROOT/'parameters.json').read_bytes()).hexdigest(),'source_board_tsx_sha256':hashlib.sha256((ROOT.parent/'index.circuit.tsx').read_bytes()).hexdigest(),'printed_meshes_restored_from_print_orientation':len(printed_names),'cad_files':{name:{'bytes':(OUT/name).stat().st_size,'sha256':hashlib.sha256((OUT/name).read_bytes()).hexdigest()} for name in ['assembled.glb','exploded.glb']},'physical_fit':'Unmeasured; nominal supplier/library models do not replace physical tolerance and prototype verification'}
(OUT/'assembly-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
