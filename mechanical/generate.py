#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Rev B printable solids and swept-volume checks.
Rebuild using the pinned Python packages in mechanical/README.md. Millimetres,
+Z up; PCB bottom at z10. Print transforms are saved alongside every mesh.
"""
from pathlib import Path
import json, math
import manifold3d as m
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parent
P=json.loads((ROOT/'parameters.json').read_text())
def cyl(r,h,z=0,x=0,y=0):return m.Manifold.cylinder(h,r,r,128).translate((x,y,z))
def box(size,center):return m.Manifold.cube(size,True).translate(center)
def ring(ro,ri,h,z=0):return cyl(ro,h,z)-cyl(ri,h+.2,z-.1)
def screws(radius,z,h,d,count=3):
 return [cyl(d/2,h,z,radius*math.cos(2*math.pi*i/count),radius*math.sin(2*math.pi*i/count)) for i in range(count)]
def cut_all(s,holes):
 for h in holes:s-=h
 return s
def located(s,x,y,angle=0):return s.rotate((0,0,angle)).translate((x,y,0))
base=cyl(40,2)+ring(40,38.3,12.2,2)
for x,y in P['mount_holes']:
 base+=cyl(3.7,8,2,x,y);base-=cyl(1,8.1,2,x,y)
lid_screws=[(26,26),(-26,-26)]
for x,y in lid_screws:
 base+=cyl(2.2,12.2,2,x,y);base-=cyl(.85,12.4,2,x,y)
bx,by,bz=P['battery_center'];bw,bl,bh=P['battery_envelope']
for x in [bx-bw/2-.9,bx+bw/2+.9]:base+=box((1.2,bl+2,3),(x,by,3.5))
for y in [by-bl/2-.9,by+bl/2+.9]:base+=box((bw+3,1.2,3),(bx,y,3.5))
for x in [bx-bw/2-2,bx+bw/2+2]:base-=box((1.3,5,2.4),(x,by,1))
base-=box((7,9.5,8.2),(16,-15,6.1))
usb=box((13,22,7),(0,31.5,13.5))
# Open recess gives finger access to the left-facing toggle under the rotor.
toggle_access=box((18,12,10),(-34,-14,16))
base-=usb;base-=toggle_access
lid=cyl(39.85,1.2,14.2)+ring(40,34.5,6.6,15.3)
# Hollow fixed post carries LCD wires through the bearing, never the rotor.
lid+=ring(16.5,11.2,6.65,15.35)
lid+=ring(P['bearing_stem_od']/2,11.2,7.0,22)
lid-=cyl(11.2,18,14)
lid=cut_all(lid,screws(13,15,14.1,1.6))
for x,y in lid_screws:
 lid-=cyl(1.1,8,14,x,y);lid-=cyl(2.1,1.3,20.7,x,y)
lid-=usb;lid-=toggle_access
# A shallow circular recess leaves a continuous 0.6mm lid web. The optical
# skirt clears this recess at every angle; only the sensor needs a full window.
r=P['encoder']['track_radius']
lid-=ring(26.8,23.5,1.0,14.8)
sensor_window=located(box((7.2,5.2,7), (0,0,16)), -23,10,P['encoder']['rotation_deg'])
lid-=sensor_window
# Tall connectors and the right-angle toggle get exact local access windows.
program_window=box((16,6.2,7),(0,-20.5,16))
toggle_body=box((8.2,8.2,6.8),(-22.45,-14,14.7))
lid-=program_window;lid-=toggle_body
lid-=cyl(2.4,5,13,0,-29)
lid-=cyl(1.4,5,13,8,-26)
# Open grip ring; an inward shoulder captures the bearing's outer race.
cap=ring(34,25.6,24.8,22)+ring(26.5,P['bearing_pocket_id']/2,7,22)
cap+=ring(33.8,20,1.2,29)
cap=cut_all(cap,screws(23.2,21.9,7.1,1.6))
for i in range(96):
 a=2*math.pi*i/96;cap-=cyl(.4,24.8,22,34.05*math.cos(a),34.05*math.sin(a))
# Separate black optical ring captures the bearing from below. Slots extend
# from its lower edge, eliminating unsupported bridges when printed inverted.
outer_retainer=ring(26.5,20,1.2,20.8)+ring(r+.5,r-.5,5.6,15.3)
for i in range(48):
 a=360*i/48
 # Tangential 1.64mm apertures, 48 periods on the 25.08mm radius.
 outer_retainer-=box((3,1.64,3.6),(r,0,17)).rotate((0,0,a))
outer_retainer=cut_all(outer_retainer,screws(23.2,20.7,1.4,2.2))
for i in range(3):
 a=2*math.pi*i/3
 outer_retainer-=m.Manifold.cylinder(1.21,2.1,1.1,64).translate((23.2*math.cos(a),23.2*math.sin(a),20.79))
# Fixed inner race clamp and LCD cradle form one removable printed part.
inner_retainer=ring(16.5,11.2,1.6,29)
inner_retainer=cut_all(inner_retainer,screws(13,28.9,1.8,2.2))
for x,y in [(-14,0),(0,14),(0,-14)]:inner_retainer+=box((3,3,9.0),(x,y,35.1))
connector_notch=box((23,24,9),(16.5,0,38))
cradle=ring(25,12,1,38.6)+ring(25,17.8,2.4,39.6)
cradle-=connector_notch
cradle+=ring(25,23.2,3.6,42)
bezel_screws=[(-22.2,0),(0,22.2),(0,-22.2)]
for x,y in bezel_screws:
 cradle+=cyl(2.3,6,39.6,x,y);cradle-=cyl(.8,6.2,39.5,x,y)
inner_retainer+=cradle
bezel=ring(25,16.6,1.4,45.6)
for x,y in bezel_screws:
 bezel-=cyl(1.1,1.6,45.5,x,y)
 bezel-=m.Manifold.cylinder(1.21,1.1,2.1,64).translate((x,y,45.8))
plunger=cyl(2.9,.4,13.6,0,-29)+cyl(1.9,2.05,13.95,0,-29)
coupon=ring(24,P['bearing_pocket_id']/2,3)+ring(P['bearing_stem_od']/2,11.2,3).translate((42,0,0))
parts={'base':base,'lid':lid,'knob':cap,'outer-retainer':outer_retainer,'inner-retainer':inner_retainer,'screen-bezel':bezel,'button-plunger':plunger,'fit-coupon':coupon}
(ROOT/'stl').mkdir(exist_ok=True)
report={};poses={}
for name,s in parts.items():
 # Print the rotor and encoder plate upside down; all other parts bottom down.
 invert=name in ['knob','outer-retainer']
 z=s.bounding_box()[5] if invert else s.bounding_box()[2]
 printed=s.rotate((180,0,0)).translate((0,0,z)) if invert else s.translate((0,0,-z))
 a=printed.to_mesh64();mesh=trimesh.Trimesh(np.asarray(a.vert_properties)[:,:3],np.asarray(a.tri_verts),process=True)
 assert mesh.is_watertight and mesh.volume>0,(name,'invalid solid',s.status(),len(mesh.faces))
 # Each printable part must be one connected object, except the two fit coupons.
 assert len(printed.decompose())==(2 if name=='fit-coupon' else 1),(name,'disconnected print')
 mesh.export(ROOT/'stl'/f'{name}.stl')
 poses[name]={'inverted':invert,'z':z}
 report[name]={'watertight':True,'volume_mm3':round(mesh.volume,2),'bounds_mm':mesh.bounds.round(3).tolist()}
 print(name,'watertight',round(mesh.volume,1))
(ROOT/'print-poses.json').write_text(json.dumps(poses,indent=2)+'\n')
# Swept-volume checks: replace the slotted track by a solid ring to cover every
# possible rotor angle. Fixed windows must clear the sensor/headers, not copper.
swept_skirt=ring(r+.5,r-.5,5.5,15.3)
for name,fixed in [('lid',lid),('cradle',inner_retainer),('bezel',bezel)]:
 for moving_name,moving in [('grip',cap),('encoder plate',outer_retainer),('encoder swept ring',swept_skirt)]:
  assert (moving^fixed).volume()<1e-4,(name,moving_name,'collision')
assert (cap^outer_retainer).volume()<1e-4
assert (plunger^lid).volume()<1e-4
for name,keep in [('USB',box((10.4,8.7,3.5),(0,26.95,13.35))),('programming',box((14,4.8,6),(0,-20.55,14.6))),('toggle',toggle_body),('sensor',sensor_window)]:
 assert (lid^keep).volume()<1e-4,(name,'lid collision')
battery=box(P['battery_envelope'],P['battery_center'])
jst=box((6.5,9,8),(16,-15,6))
assert (base^battery).volume()<1e-4,'pouch compression'
assert (base^jst).volume()<1e-4 and (battery^jst).volume()<1e-4
assert P['pcb_bottom_z']-(bz+bh/2)>=2
assert P['pcb_bottom_z']-P['header_tail_below_pcb_mm']-(bz+bh/2)>=1.0
assert 14.2-(20.7-P['lid_screw_length_mm'])>=3.0 # Lid screws must engage the base bosses
assert (plunger^swept_skirt).volume()<1e-4,'reset plunger catches encoder skirt'
report['clearances']={'screen_bezel_to_grip_radial_mm':.6,'encoder_to_recess_vertical_mm':.5,'encoder_gap_radial_each_side_mm':1.0,'battery_to_pcb_mm':2.0,'trimmed_header_tails_to_battery_mm':round(P['pcb_bottom_z']-P['header_tail_below_pcb_mm']-(bz+bh/2),3),'lid_screw_base_engagement_mm':round(14.2-(20.7-P['lid_screw_length_mm']),2),'stem_diametral_mm':.15,'bearing_outer_diametral_mm':.1,'bearing_head_to_lcd_connector_mm':1.8,'encoder_slot_count':48,'quadrature_edges_per_turn':192}
report['scope']='CAD collision checks only; printed fits, IR opacity, optical contrast and module/cable clearances require prototype measurements.'
(ROOT/'geometry-check.json').write_text(json.dumps(report,indent=2)+'\n')
fig=plt.figure(figsize=(11,8));ax=fig.add_subplot(111,projection='3d');polys=[];colors=[]
for solid,color in [(base,'#344752'),(lid,'#6b8797'),(cap,'#e9bd65'),(bezel,'#95a5ad'),(cyl(16.2,.15,45.65),'#122f38')]:
 a=solid.to_mesh();v=np.asarray(a.vert_properties)[:,:3];t=np.asarray(a.tri_verts);polys.extend(v[t]);colors.extend([color]*len(t))
ax.add_collection3d(Poly3DCollection(polys,facecolors=colors,edgecolor='none',zsort='average'))
ax.set(xlim=(-42,42),ylim=(-42,42),zlim=(0,50),xlabel='X / mm',ylabel='Y / mm',zlabel='Z / mm');ax.set_box_aspect((84,84,50));ax.view_init(40,-135);ax.set_title('Desk knob Rev B — fixed 1.28-inch screen, rotating grip ring\nØ80 × 47 mm / left toggle / rechargeable USB counter')
fig.tight_layout();fig.savefig(ROOT/'assembly.png',dpi=150);plt.close(fig)
print(json.dumps(report['clearances'],indent=2))
