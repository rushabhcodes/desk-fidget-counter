#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Rev E3 nested PCB pocket and printable solids.
All dimensions are millimetres, +Z up. No Z scaling of purchased parts.
"""
from pathlib import Path
import json, math
import manifold3d as m
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parent
P=json.loads((ROOT/'parameters.json').read_text())
TAU=2*math.pi

def cyl(r,h,z=0,x=0,y=0):return m.Manifold.cylinder(h,r,r,128).translate((x,y,z))
def cyl_y(r,start,end,z):return m.Manifold.cylinder(end-start,r,r,96).rotate((-90,0,0)).translate((0,start,z))
def box(size,center):return m.Manifold.cube(size,True).translate(center)
def ring(ro,ri,h,z=0):return cyl(ro,h,z)-cyl(ri,h+.2,z-.1)
def csk_hole(x,y,z,up=False):
 if up:return cyl(2.1,.45,z-.1,x,y)+m.Manifold.cylinder(.9,2.0,1.1,64).translate((x,y,z+.3))
 return cyl(2.1,.45,z-.35,x,y)+m.Manifold.cylinder(.9,1.1,2.0,64).translate((x,y,z-1.2))
def cut_all(s,holes):
 for h in holes:s-=h
 return s
def polar(r,a):return r*math.cos(a),r*math.sin(a)
def located(s,x,y,angle=0):return s.rotate((0,0,angle)).translate((x,y,0))
def radial_holes(s,r,z,h,d,offset=0):
 return cut_all(s,[cyl(d/2,h,z,*polar(r,offset+i*TAU/3)) for i in range(3)])

top=P['pcb_bottom_z']+P['pcb_thickness'];bearing=P['bearing'];bt=bearing['bottom_z'];bh=bearing['width'];grip_z=P['knob_bottom_z'];r=P['encoder']['track_radius']
lid_screws=P['chassis_screw_axes']
outer=P['base_diameter']/2
usb_access=P['usb_access']
base=cyl(outer,2)+ring(outer-.2,outer-2.2,7.2,2)
for x,y in P['mount_holes']:
 # Unplated locator pegs and lid pads capture the board; no tall PCB standoffs.
 base+=cyl(2.3,.6,2,x,y)+cyl(1.25,2.2,2,x,y)
for x,y in lid_screws:
 base+=cyl(2.2,7.2,2,x,y);base-=cyl(.8,7.3,2,x,y)
# Individual solder wells retain 1.2mm floor beneath trimmed through-hole tails.
cj=json.loads((ROOT.parent/'dist/index/circuit.json').read_text())
assert all(c['layer']=='top' for c in cj if c['type']=='pcb_component'),'Every component must assemble from above'
for h in [c for c in cj if c['type']=='pcb_plated_hole']:
 x,y=h.get('x',0),h.get('y',0)
 w=max(h.get('outer_diameter',0),h.get('rect_pad_width',0),h.get('outer_width',0),1.2)+.6
 d=max(h.get('outer_diameter',0),h.get('rect_pad_height',0),h.get('outer_height',0),1.2)+.6
 base-=box((w,d,1.0),(x,y,1.7))
usb=box((usb_access['opening_width_mm'],usb_access['opening_length_mm'],usb_access['opening_top_z']-usb_access['opening_bottom_z']),
 (0,usb_access['opening_center_y'],(usb_access['opening_top_z']+usb_access['opening_bottom_z'])/2))
base-=usb
# The switch sits on an integral front PCB tab. Its own actuator is exposed.
button=P['front_button'];button_z=button['axis_z']
button_opening=box((button['opening_width_mm'],16,button['opening_top_z']-button['opening_bottom_z']),
 (0,-42,(button['opening_top_z']+button['opening_bottom_z'])/2))
base-=button_opening
# Recess only the actual PCB nose, retaining the outer wall wherever there is
# room. The 0.25mm side allowance clears the FR-4 without a large front opening.
board_outline=next(c['outline'] for c in cj if c['type']=='pcb_board')
front_pocket=m.CrossSection([[(q['x'],q['y']) for q in board_outline]]).offset(.25).extrude(1.8).translate((0,0,2.6))
base-=(front_pocket^box((24,16,3),(0,-40,3.5)))
# Open the narrow FR-4 band cleanly instead of retaining sub-nozzle wall slivers.
base-=box((11,12,1.8),(0,-42.5,3.5))
# Support the switch tab directly underneath the solder-free PCB underside.
base+=box((9,6,.6),(0,-38.6,2.3))

lid=ring(outer-.35,27.3,1.2,9.2)
# The large hollow bearing post surrounds, rather than stacks over, the screen.
lid+=ring(31.2,27.3,1.62,10.39)+ring(P['bearing_stem_od']/2,27.3,bh,bt)
for x,y in P['mount_holes']:lid+=cyl(2.0,5.0,top,x,y)
for x in [-6,6]:lid+=cyl(1.3,5.0,top,x,-37)
for x,y in lid_screws:
 lid-=cyl(1.1,2,9,x,y);lid-=csk_hole(x,y,10.4)
# Bearing clamp uses the thick wall of the hollow post; screen supports rise
# independently from the base through the PCB window, inside the encoder skirt.
for i in range(3):
 x,y=polar(28.6,i*TAU/3);lid-=cyl(.8,5.2,14,x,y)
# The flush port keeps the plug body outside the lid; retain its full roof.
lid-=located(box((7.2,5.2,4),(0,0,8.6)),-23,10,P['encoder']['rotation_deg'])


# Outer race captured below, with the optical skirt attached above the fixed
# inner-race support. No moving radial web crosses that stationary support.
cap=ring(42.4,P['bearing_pocket_id']/2,bh,bt)
cap+=ring(42.4,36.2,1.7,19)
cap+=ring(42.4,24.6,1.4,20.7)
for i in range(96):
 x,y=polar(42.45,i*TAU/96);cap-=cyl(.4,12,10.5,x,y)
cap=radial_holes(cap,39.6,11.9,6.1,1.6)
outer_retainer=ring(42.0,36.2,1.2,grip_z)
outer_retainer=radial_holes(outer_retainer,39.6,10.7,1.5,2.2)
for i in range(3):
 x,y=polar(39.6,i*TAU/3)
 outer_retainer-=csk_hole(x,y,10.8,up=True)
encoder_skirt=ring(r+.5,r-.5,12.74,7.9)+ring(P['encoder']['bond_outer_radius'],r-.5,1.2,19.44)
for i in range(48):encoder_skirt-=box((3,1.64,1.8),(r,0,8.6)).rotate((0,0,i*360/48))
bearing_clamp=ring(31.2,27.4,1.2,19)
bearing_clamp=radial_holes(bearing_clamp,28.6,18.9,1.4,2.2)
for i in range(3):
 x,y=polar(28.6,i*TAU/3)
 bearing_clamp-=csk_hole(x,y,20.2)
# Three base-mounted supports lie entirely inside the routed PCB window.
screen_posts=P['screen_posts']
for x,y in screen_posts:
 base+=cyl(1.8,14.1,2,x,y);base-=cyl(.8,10.1,6,x,y)
cradle=ring(24,18.2,1.2,16.1)
for x,y in screen_posts:
 # Short radial ledges reach each pillar without loading rear LCD components.
 a=math.atan2(y,x);rr=math.hypot(x,y)
 cradle+=cyl(2.3,1.2,16.1,x,y)
 cradle-=cyl(1.1,1.4,16,x,y)
 cradle-=csk_hole(x,y,17.3)
cradle-=box((5,16,1.4),(-20,0,16.7))
bezel_screws=[polar(21.1,i*TAU/3) for i in range(3)]
for x,y in bezel_screws:
 cradle+=cyl(1.8,3.6,17.3,x,y);cradle-=cyl(.8,4.9,16.1,x,y)
bezel=ring(24,16.6,1.4,20.9)
# A 0.2mm underside relief prevents the retaining lip from clamping LCD glass.
bezel-=cyl(19,.21,20.89)+box((5,15,.21),(-18.75,0,20.995))
for x,y in bezel_screws:
 bezel-=cyl(1.1,1.6,20.8,x,y)
 bezel-=csk_hole(x,y,22.3)
# Park the rotor at these three windows to reach its underside screws.
for i in range(3):
 x,y=polar(39.6,i*TAU/3)
 base-=cyl(usb_access['driver_window_diameter_mm']/2,11,-.1,x,y);lid-=cyl(usb_access['driver_window_diameter_mm']/2,3,8.9,x,y)
coupon=ring(40,P['bearing_pocket_id']/2,3)+ring(P['bearing_stem_od']/2,27.3,3).translate((74,0,0))
parts={'base':base,'lid':lid,'knob':cap,'outer-retainer':outer_retainer,'inner-retainer':cradle,'screen-bezel':bezel,'bearing-clamp':bearing_clamp,'encoder-skirt':encoder_skirt,'fit-coupon':coupon}
(ROOT/'stl').mkdir(exist_ok=True);report={};poses={}
for name,s in parts.items():
 invert=name in ['knob','outer-retainer','encoder-skirt'];z=s.bounding_box()[5] if invert else s.bounding_box()[2]
 printed=s.rotate((180,0,0)).translate((0,0,z)) if invert else s.translate((0,0,-z))
 a=printed.to_mesh64();mesh=trimesh.Trimesh(np.asarray(a.vert_properties)[:,:3],np.asarray(a.tri_verts),process=True)
 assert mesh.is_watertight and mesh.volume>0,(name,'invalid solid')
 assert len(printed.decompose())==(2 if name=='fit-coupon' else 1),(name,'disconnected print')
 mesh.export(ROOT/'stl'/f'{name}.stl');poses[name]={'inverted':invert,'z':z}
 report[name]={'watertight':True,'volume_mm3':round(mesh.volume,2),'bounds_mm':mesh.bounds.round(3).tolist()}
 print(name,'watertight',round(mesh.volume,1),flush=True)
(ROOT/'print-poses.json').write_text(json.dumps(poses,indent=2)+'\n')
# Use a full solid ring in place of slots to cover every possible rotor angle.
swept_skirt=ring(r+.5,r-.5,12.74,7.9)
moving=[('grip',cap),('retainer',outer_retainer),('swept skirt',swept_skirt),('skirt flange',ring(P['encoder']['bond_outer_radius'],r-.5,1.2,19.44))]
for name,fixed in [('base',base),('lid',lid),('cradle',cradle),('bezel',bezel),('bearing clamp',bearing_clamp)]:
 for mn,mov in moving:assert (mov^fixed).volume()<1e-4,(name,mn,'collision',(mov^fixed).volume())
assert (cap^outer_retainer).volume()<1e-4
# Manufacturer screen STEP transformed rigidly: tab -X, rear connector +X.
def from_mesh(mesh):
 q=m.Manifold(m.Mesh64(np.ascontiguousarray(mesh.vertices,dtype=np.float64),np.ascontiguousarray(mesh.faces,dtype=np.uint64)))
 assert str(q.status()).endswith('NoError'),str(q.status())
 return q
screen_mesh=trimesh.load(ROOT/'vendor/obj/screen19192.obj',force='mesh',process=True)
screen_mesh.apply_transform(np.diag([-1.,1.,-1.,1.]));screen_mesh.apply_translation([0,0,17.75])
lcd=from_mesh(screen_mesh)
from harness import build as build_harness
harness_meshes,harness_report=build_harness()
(ROOT/'harness.json').write_text(json.dumps(harness_report,indent=2)+'\n')
for name,printed in [('base',base),('lid',lid),('cradle',cradle),('bezel',bezel)]:
 assert (printed^lcd).volume()<1e-4,(name,'manufacturer screen collision',(printed^lcd).volume())
# PCB material must not intersect either part nested through its window.
board=next(c for c in cj if c['type']=='pcb_board')
cutout=next(c for c in cj if c['type']=='pcb_cutout')
polygon=lambda points:m.CrossSection([[(v['x'],v['y']) for v in points]])
outline=polygon(board['outline']).extrude(P['pcb_thickness']).translate((0,0,P['pcb_bottom_z']))
window=polygon(cutout['points']).extrude(2).translate((0,0,2.4))
pcb=outline-window
for x,y in P['mount_holes']:pcb-=cyl(1.35,2,2.4,x,y)
assert (base^pcb).volume()<1e-4,'Base must clear actual PCB material and NPTHs'
assert (pcb^lcd).volume()<1e-4
# Direct finger access remains clear even at maximum specified pretravel.
# A 12mm fingertip sphere is tangent to the fully depressed original actuator.
finger_radius=button['finger_check_radius_mm'];pressed_face=button['actuator_front_y']+button['datasheet_pretravel_mm']['max']
finger=m.Manifold.sphere(finger_radius,96).translate((0,pressed_face-finger_radius,button_z))
for label,part in [('base',base),('lid',lid),('PCB',pcb),*moving]:
 assert (finger^part).volume()<1e-4,(label,'direct finger access collision',(finger^part).volume())
actuator_region=box((2.0,.8,1.2),(0,button['actuator_front_y']+.35,button_z))
# Top-side component and mated cable envelopes, including the full sensor arms.
# A continuous approach prism covers the entire maximum plug body from a
# conservative shoulder plane at the socket mouth to beyond every case part.
plug_start=usb_access['plug_shoulder_y'];plug_length=usb_access['plug_check_length_mm']
plug_gauge=box((usb_access['plug_width_mm'],plug_length,usb_access['plug_height_mm']),
 (0,plug_start+plug_length/2,usb_access['axis_z']))
assert plug_start+plug_length>outer+5
for label,part in [('base',base),('lid',lid),('PCB',pcb),('LCD',lcd),*moving]:
 assert (plug_gauge^part).volume()<1e-4,(label,'USB insertion clearance',(plug_gauge^part).volume())
fixed_hardware=[('USB plug approach gauge',plug_gauge),('programming header',box((13.9,4.5,6),(0,19.95,7.2))),('LCD manufacturer model',lcd),('PCB',pcb)]
for name,mesh in harness_meshes.items():fixed_hardware.append((name,from_mesh(mesh)))
for dx in [-2.125,2.125]:
 fixed_hardware.append(('sensor arm',located(box((1.25,4,5.7),(dx,0,7.05)),-23,10,P['encoder']['rotation_deg'])))
for name,fixed in fixed_hardware:
 for mn,mov in moving:assert (mov^fixed).volume()<1e-4,(name,mn,'hardware collision',(mov^fixed).volume())
for name,fixed in fixed_hardware:
 if name in ['PCB']:continue
 assert (lid^fixed).volume()<1e-4,(name,'chassis collision',(lid^fixed).volume())
# Verify actual package-model placements against the fixed and moving prints.
# SMT lead pads and PCB surface contact are intentional; tails fit solder wells.
package_checks=0
for cad in [v for v in cj if v['type']=='cad_component' and v.get('model_obj_url')]:
 url=cad['model_obj_url'];filename=url.split('?')[0].split('/')[-1]
 path=ROOT/'vendor/obj'/filename
 if not path.exists():raise AssertionError(('Missing real package mesh',filename))
 solid_path=ROOT/'vendor/solid'/filename.replace('.obj','.ply')
 # Preserve the button STEP's distinct coincident seam edges.
 mesh=trimesh.load(solid_path if solid_path.exists() else path,force='mesh',process=filename!='b3u3000.obj')
 origin=cad.get('model_origin_position') or {'x':0,'y':0,'z':0}
 mesh.apply_translation([-origin.get(k,0) for k in ['x','y','z']])
 rotation=cad.get('rotation',{})
 mesh.apply_transform(trimesh.transformations.euler_matrix(*[math.radians(rotation.get(k,0)) for k in ['x','y','z']]))
 pos=cad['position'];mesh.apply_translation([pos['x'],pos['y'],pos['z']+P['pcb_bottom_z']+P['pcb_thickness']/2])
 # Supplier meshes can contain independently closed housing/lead solids. Union
 # each closed shell before checking to avoid treating internal faces as voids.
 solids=[]
 for shell in mesh.split(only_watertight=False):
  if not shell.is_watertight:raise AssertionError(('Open vendor shell',filename))
  solids.append(from_mesh(shell))
 physical=m.Manifold.batch_boolean(solids,m.OpType.Add)
 for wn,wire_mesh in harness_meshes.items():
  if wn.startswith('lcd-wire-'):assert (physical^from_mesh(wire_mesh)).volume()<1e-4,(filename,wn,'wire/package collision')
 assert (physical^plug_gauge).volume()<1e-4,(filename,'USB plug approach/package collision')
 if filename=='C165948.obj':
  assert abs(mesh.bounds[1,1]-usb_access['socket_face_y'])<.001,'USB socket must use its real CAD face datum'
  front=mesh.vertices[mesh.vertices[:,1]>mesh.bounds[1,1]-.0001]
  assert abs((front[:,2].min()+front[:,2].max())/2-usb_access['axis_z'])<.001,'Plug gauge must align with the real USB CAD axis'
 for name,printed in [('base',base),('lid',lid),('cradle',cradle),('bezel',bezel)]:
  assert (physical^printed).volume()<1e-4,(filename,name,'package/print collision',(physical^printed).volume())
 for name,mov in moving:
  assert (physical^mov).volume()<1e-4,(filename,name,'package/rotor collision',(physical^mov).volume())
 # Fingers may touch only the original SW1 actuator, never other packages.
 if filename!='b3u3000.obj':assert (physical^finger).volume()<1e-4,(filename,'finger access collision')
 else:
  assert abs(mesh.bounds[0,1]-button['actuator_front_y'])<.001,'Use real actuator datum'
  assert ((physical^finger)-actuator_region).volume()<1e-4,'Finger may contact only the actuator'
 package_checks+=1
wire_solids=[]
for name,mesh in harness_meshes.items():
 if not name.startswith('lcd-wire-'):continue
 wire=from_mesh(mesh)
 for pn,printed in [('base',base),('lid',lid),('cradle',cradle),('bezel',bezel),('PCB',pcb),('LCD module',lcd)]:
  assert (wire^printed).volume()<1e-4,(name,pn,'wire collision',(wire^printed).volume())
 for other_name,other in wire_solids:assert (wire^other).volume()<1e-5,(name,other_name,'wires intersect')
 wire_solids.append((name,wire))
report['purchased_package_models_checked']=package_checks
report['individual_wires_checked']=len(wire_solids)
report['front_button']=P['front_button']
report['direct_finger_access_checked']=True
report['separate_button_plunger']=False
report['button_projection_beyond_wall_mm']=round(-button['actuator_front_y']-(outer-.2),3)
report['pressed_button_projection_beyond_wall_mm']=round(-pressed_face-(outer-.2),3)
report['USB_access']={**usb_access,'outer_case_diameter_mm':P['base_diameter'],
 'socket_recess_from_floor_outer_edge_mm':round(outer-usb_access['socket_face_y'],4),
 'socket_projection_beyond_side_wall_mm':round(usb_access['socket_face_y']-(outer-.2),4),
 'PCB_front_edge_mm':max(q['y'] for q in board['outline']),
 'plug_body_to_PCB_axial_gap_mm':round(plug_start-max(q['y'] for q in board['outline']),4),
 'maximum_plug_approach_sweep_checked':True,'all_package_and_PCB_clearances_checked':True}

report['clearances']={'overall_height_mm':22.3,'previous_height_mm':47,'height_reduction_percent':round((47-22.3)/47*100,1),'grip_lower_edge_mm':10.8,'previous_grip_lower_edge_mm':22,'USB_plug_max_height_mm':usb_access['plug_height_mm'],'USB_plug_to_rotor_vertical_mm':round(grip_z-(usb_access['axis_z']+usb_access['plug_height_mm']/2),3),'bezel_to_grip_radial_mm':.6,'skirt_to_sensor_radial_each_side_mm':1.0,'PCB_bottom_z_mm':2.6,'LCD_connector_in_PCB_window':True,'bearing_id_mm':60,'bearing_od_mm':75,'bearing_width_mm':7,'bearing_stem_diametral_mm':.15,'bearing_outer_diametral_mm':.1,'encoder_slot_count':48,'quadrature_edges_per_turn':192,'all_components_top_side':True,'solder_well_floor_remaining_mm':1.2}
report['scope']='Nominal CAD checks using manufacturer screen geometry and specified static harness. Physical fit, crimp quality, tolerances, 950nm opacity, optical response and grip feel require prototype measurements.'
(ROOT/'geometry-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['clearances'],indent=2))
