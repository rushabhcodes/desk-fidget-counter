#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Rev E nested PCB pocket and printable solids.
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
base=cyl(43,2)+ring(42.8,40.8,7.2,2)
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
usb=box((14,25,8.8),(0,32,5.95))
base-=usb
# Front button opposite USB. Open-top guide permits assembly before fitting
# the lid; the lid supplies its keeper. Only the thin nose reaches over PCB.
button_z=P['front_button']['axis_z']
guide=cyl_y(3.3,-40.9,P['front_button']['guide_end_y'],button_z)
guide-=box((8,8,8),(0,-38.5,button_z+4))
base+=guide
base-=cyl_y(2.2,-45,-40.7,button_z)
base-=cyl_y(1.35,-41,-34.8,button_z)
base-=cyl_y(2.85,-40.5,-39.5,button_z)

lid=ring(42.65,27.3,1.2,9.2)
# The large hollow bearing post surrounds, rather than stacks over, the screen.
lid+=ring(31.2,27.3,1.62,10.39)+ring(P['bearing_stem_od']/2,27.3,bh,bt)
for x,y in P['mount_holes']:lid+=cyl(2.0,5.0,top,x,y)
for x,y in lid_screws:
 lid-=cyl(1.1,2,9,x,y);lid-=csk_hole(x,y,10.4)
# Bearing clamp uses the thick wall of the hollow post; screen supports rise
# independently from the base through the PCB window, inside the encoder skirt.
for i in range(3):
 x,y=polar(28.6,i*TAU/3);lid-=cyl(.8,5.2,14,x,y)
lid-=usb
# Keeper closes the open-top plunger guide, with 0.3 mm flange clearance.
lid+=box((6.6,5.7,1.4),(0,-38.05,8.5))
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
plunger=(cyl_y(2,-43,-41.9,button_z)+cyl_y(1.2,-41.9,-35.2,button_z)
 +cyl_y(P['front_button']['tip_radius_mm'],-35.2,P['front_button']['rest_tip_y'],button_z)
 +cyl_y(2.6,-40.5,-39.9,button_z))
# Park the rotor at these three windows to reach its underside screws.
for i in range(3):
 x,y=polar(39.6,i*TAU/3)
 base-=cyl(2.6,11,-.1,x,y);lid-=cyl(2.6,3,8.9,x,y)
coupon=ring(40,P['bearing_pocket_id']/2,3)+ring(P['bearing_stem_od']/2,27.3,3).translate((74,0,0))
parts={'base':base,'lid':lid,'knob':cap,'outer-retainer':outer_retainer,'inner-retainer':cradle,'screen-bezel':bezel,'button-plunger':plunger,'bearing-clamp':bearing_clamp,'encoder-skirt':encoder_skirt,'fit-coupon':coupon}
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
for name,fixed in [('base',base),('lid',lid),('cradle',cradle),('bezel',bezel),('bearing clamp',bearing_clamp),('plunger',plunger)]:
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
# Exact swept solid of the complete linear plunger stroke, including stops.
travel=P['front_button']['plunger_travel_mm']
button_sweep=(cyl_y(2,-43,-41.9+travel,button_z)+cyl_y(1.2,-41.9,-35.2+travel,button_z)
 +cyl_y(P['front_button']['tip_radius_mm'],-35.2,P['front_button']['rest_tip_y']+travel,button_z)
 +cyl_y(2.6,-40.5,-39.9+travel,button_z))
for label,part in [('base',base),('lid',lid),('PCB',pcb),*moving]:
 assert (button_sweep^part).volume()<1e-4,(label,'button stroke collision',(button_sweep^part).volume())
# Top-side component and mated cable envelopes, including the full sensor arms.
fixed_hardware=[('USB plug',box((12.9,18,6.4),(0,42.6,5.95))),('programming header',box((13.9,4.5,6),(0,19.95,7.2))),('display header/mate',box((9.6,17.9,4.85),(-16.05,-3.5,6.625))),('LCD manufacturer model',lcd),('PCB',pcb)]
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
 for name,printed in [('base',base),('lid',lid),('cradle',cradle),('bezel',bezel)]:
  assert (physical^printed).volume()<1e-4,(filename,name,'package/print collision',(physical^printed).volume())
 for name,mov in moving:
  assert (physical^mov).volume()<1e-4,(filename,name,'package/rotor collision',(physical^mov).volume())
 # At rest, the plunger must not preload the real switch or touch any
 # other package. Pressed motion intentionally actuates SW1's moving nose.
 assert (physical^plunger).volume()<1e-4,(filename,'rest plunger collision',(physical^plunger).volume())
 if filename!='b3u3000.obj':assert (physical^button_sweep).volume()<1e-4,(filename,'button sweep collision')
 else:assert (physical^button_sweep).volume()>1e-4,'Plunger stroke must reach the real actuator'
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
report['complete_button_stroke_sweep_checked']=True
# Conservative downward tip play using the front head/aperture and inner
# stem/guide radii. FDM dimensional error is separate and must be measured.
head_axis_y=-42.45;inner_guide_y=P['front_button']['guide_end_y'];tip_y=P['front_button']['rest_tip_y']
tip_drop=.15+(.2+.15)*(tip_y-inner_guide_y)/(inner_guide_y-head_axis_y)
tip_clearance=button_z-P['front_button']['tip_radius_mm']-tip_drop-top
assert tip_clearance>.15,'Allow nominal guide play above the PCB edge'
report['front_button_nominal_play_clearance_mm']=round(tip_clearance,4)
report['clearances']={'overall_height_mm':22.3,'previous_height_mm':47,'height_reduction_percent':round((47-22.3)/47*100,1),'grip_lower_edge_mm':10.8,'previous_grip_lower_edge_mm':22,'USB_plug_max_height_mm':6.4,'USB_plug_to_rotor_vertical_mm':1.65,'bezel_to_grip_radial_mm':.6,'skirt_to_sensor_radial_each_side_mm':1.0,'PCB_bottom_z_mm':2.6,'LCD_connector_in_PCB_window':True,'bearing_id_mm':60,'bearing_od_mm':75,'bearing_width_mm':7,'bearing_stem_diametral_mm':.15,'bearing_outer_diametral_mm':.1,'encoder_slot_count':48,'quadrature_edges_per_turn':192,'all_components_top_side':True,'solder_well_floor_remaining_mm':1.2}
report['scope']='Nominal CAD checks using manufacturer screen geometry and specified static harness. Physical fit, crimp quality, tolerances, 950nm opacity, optical response and grip feel require prototype measurements.'
(ROOT/'geometry-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['clearances'],indent=2))
