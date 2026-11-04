#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Rev C nested PCB pocket and printable solids.
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
def box(size,center):return m.Manifold.cube(size,True).translate(center)
def ring(ro,ri,h,z=0):return cyl(ro,h,z)-cyl(ri,h+.2,z-.1)
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
 base+=cyl(2.2,7.2,2,x,y);base-=cyl(.85,7.3,2,x,y)
bx,by,bz=P['battery_center'];bw,bl,batt_h=P['battery_envelope']
for x in [bx-bw/2-.9,bx+bw/2+.9]:base+=box((1.2,bl+1.2,2.0),(x,by,3.0))
base+=box((bw+3,.6,2),(bx,by-bl/2-.3,3))
base+=box((bw+3,1.2,2),(bx,by+bl/2+.9,3))
for x in [bx-bw/2-2,bx+bw/2+2]:base-=box((1.3,5,2.4),(x,by,1))
# Individual solder wells retain 1.2mm floor beneath trimmed through-hole tails.
cj=json.loads((ROOT.parent/'dist/index/circuit.json').read_text())
assert all(c['layer']=='top' for c in cj if c['type']=='pcb_component'),'Every component must assemble from above'
for h in [c for c in cj if c['type']=='pcb_plated_hole']:
 x,y=h.get('x',0),h.get('y',0)
 w=max(h.get('outer_diameter',0),h.get('rect_pad_width',0),h.get('outer_width',0),1.2)+.6
 d=max(h.get('outer_diameter',0),h.get('rect_pad_height',0),h.get('outer_height',0),1.2)+.6
 base-=box((w,d,1.0),(x,y,1.7))
usb=box((14,25,8.8),(0,32,5.95))
toggle_access=box((17,8,5.9),(-35,-19,7.35))
base-=usb;base-=toggle_access

lid=ring(42.65,27.3,1.2,9.2)
# The large hollow bearing post surrounds, rather than stacks over, the screen.
lid+=ring(31.2,27.3,1.62,10.39)+ring(P['bearing_stem_od']/2,27.3,bh,bt)
for x,y in P['mount_holes']:lid+=cyl(2.0,5.0,top,x,y)
for x,y in lid_screws:
 lid-=cyl(1.1,2,9,x,y);lid-=m.Manifold.cylinder(1.21,1.1,2.1,64).translate((x,y,9.2))
# Bearing clamp uses the thick wall of the hollow post; screen supports rise
# independently from the base through the PCB window, inside the encoder skirt.
for i in range(3):
 x,y=polar(28.6,i*TAU/3);lid-=cyl(.8,5.2,14,x,y)
lid-=usb;lid-=toggle_access
lid-=located(box((7.2,5.2,4),(0,0,8.6)),-23,10,P['encoder']['rotation_deg'])
# Local relief for the side-entry battery connector under the shallow chassis.
lid-=box((11,8,2),(20,-15,9.5))

lid-=cyl(2.4,4,8,-5,-30)

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
 outer_retainer-=m.Manifold.cylinder(1.21,2.1,1.1,64).translate((x,y,10.79))
encoder_skirt=ring(r+.5,r-.5,12.74,7.9)+ring(P['encoder']['bond_outer_radius'],r-.5,1.2,19.44)
for i in range(48):encoder_skirt-=box((3,1.64,1.8),(r,0,8.6)).rotate((0,0,i*360/48))
bearing_clamp=ring(31.2,27.4,1.2,19)
bearing_clamp=radial_holes(bearing_clamp,28.6,18.9,1.4,2.2)
for i in range(3):
 x,y=polar(28.6,i*TAU/3)
 bearing_clamp-=m.Manifold.cylinder(1.21,1.1,2.1,64).translate((x,y,19))
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
 cradle-=m.Manifold.cylinder(1.21,1.1,2.1,64).translate((x,y,16.1))
cradle-=box((5,16,1.4),(20,0,16.7))
bezel_screws=[polar(21.5,math.pi/3+i*TAU/3) for i in range(3)]
for x,y in bezel_screws:
 cradle+=cyl(1.8,3.6,17.3,x,y);cradle-=cyl(.8,4.9,16.1,x,y)
bezel=ring(24,16.6,1.4,20.9)
for x,y in bezel_screws:
 bezel-=cyl(1.1,1.6,20.8,x,y)
 bezel-=m.Manifold.cylinder(1.21,1.1,2.1,64).translate((x,y,21.1))
plunger=cyl(2.9,.4,6.2,-5,-30)+cyl(1.9,3.5,6.55,-5,-30)
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
battery=box(P['battery_envelope'],P['battery_center'])
lcd_rear=box((4.5,17.9,8),(11.5,0,13.3))
assert (base^battery).volume()<1e-4,'pouch compression'
assert (battery^lcd_rear).volume()<1e-4,'LCD connector touches cell'
# PCB material must not intersect either part nested through its window.
board=next(c for c in cj if c['type']=='pcb_board')
cutout=next(c for c in cj if c['type']=='pcb_cutout')
polygon=lambda points:m.CrossSection([[(v['x'],v['y']) for v in points]])
outline=polygon(board['outline']).extrude(P['pcb_thickness']).translate((0,0,P['pcb_bottom_z']))
window=polygon(cutout['points']).extrude(2).translate((0,0,2.4))
pcb=outline-window
for x,y in P['mount_holes']:pcb-=cyl(1.35,2,2.4,x,y)
assert (base^pcb).volume()<1e-4,'Base must clear actual PCB material and NPTHs'
assert (pcb^battery).volume()<1e-4 and (pcb^lcd_rear).volume()<1e-4
# Top-side component and mated cable envelopes, including the full sensor arms.
fixed_hardware=[('USB plug',box((13,18,8),(0,42.6,5.95))),('battery header',box((9.6,5.9,4.8),(15.05,-9,6.6))),('programming header',box((13.9,4.5,6),(0,19.95,7.2))),('display header/mate',box((9.6,17.9,4.8),(-16.05,-3.5,6.6))),('LCD rear',lcd_rear),('cell',battery),('PCB',pcb)]
for dx in [-2.125,2.125]:
 fixed_hardware.append(('sensor arm',located(box((1.25,4,5.7),(dx,0,7.05)),-23,10,P['encoder']['rotation_deg'])))
for name,fixed in fixed_hardware:
 for mn,mov in moving:assert (mov^fixed).volume()<1e-4,(name,mn,'hardware collision',(mov^fixed).volume())
for name,fixed in fixed_hardware:
 if name in ['cell','PCB']:continue
 assert (lid^fixed).volume()<1e-4,(name,'chassis collision',(lid^fixed).volume())
report['clearances']={'overall_height_mm':22.3,'previous_height_mm':47,'height_reduction_percent':round((47-22.3)/47*100,1),'grip_lower_edge_mm':10.8,'previous_grip_lower_edge_mm':22,'USB_plug_max_height_mm':8,'USB_plug_to_rotor_vertical_mm':.85,'bezel_to_grip_radial_mm':.6,'skirt_to_sensor_radial_each_side_mm':1.0,'PCB_bottom_z_mm':2.6,'battery_in_PCB_window':True,'LCD_connector_in_PCB_window':True,'battery_to_LCD_connector_vertical_gap_mm':1.3,'bearing_id_mm':60,'bearing_od_mm':75,'bearing_width_mm':7,'bearing_stem_diametral_mm':.15,'bearing_outer_diametral_mm':.1,'encoder_slot_count':48,'quadrature_edges_per_turn':192,'all_components_top_side':True,'solder_well_floor_remaining_mm':1.2}
report['scope']='Nominal CAD checks. Physical fit, cable bends, race widths, 950nm opacity, optical response and grip feel require prototype measurements.'
(ROOT/'geometry-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['clearances'],indent=2))
