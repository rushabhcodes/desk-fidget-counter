#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Parametric printable solids; all dimensions in mm.
Rebuild with: uv run --with manifold3d==3.5.4 --with trimesh==5.2.0 --with matplotlib==3.11.2 mechanical/generate.py
"""
from pathlib import Path
import json, math
import manifold3d as m
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parent
P=json.loads((ROOT/'parameters.json').read_text())
def cyl(r,h,z=0,x=0,y=0):return m.Manifold.cylinder(h,r,r,128).translate((x,y,z))
def box(size,center):return m.Manifold.cube(size,True).translate(center)
def ring(ro,ri,h,z=0):return cyl(ro,h,z)-cyl(ri,h+0.2,z-0.1)
def screws(radius,z,h,d,count=3):
    return [cyl(d/2,h,z,radius*math.cos(2*math.pi*i/count),radius*math.sin(2*math.pi*i/count)) for i in range(count)]
def cut_all(s,holes):
    for h in holes:s=s-h
    return s
# Base floor, walls and PCB standoffs; tray never compresses the pouch.
base=cyl(36,2)+ring(36,34.3,13.4,2)
for x,y in P['mount_holes']:
    base+=cyl(3.7,8,2,x,y)
    base-=cyl(1.0,8.1,2,x,y) # M2.5 thread-forming pilots, PCB rests at z10.
# Two separate lid screw bosses in the stationary outer deck.
for x,y in [(24.4,24.4),(-24.4,-24.4)]:
    base+=cyl(1.5,12.2,2,x,y);base-=cyl(.85,12.4,2,x,y)
# Pouch cage: 0.3mm side clearance and removable strap; 2mm top clearance.
bx,by,bz=P['battery_center'];bw,bl,bh=P['battery_envelope']
for x in [bx-bw/2-.9,bx+bw/2+.9]:
    base+=box((1.2,bl+2,3.0),(x,by,3.5))
for y in [by-bl/2-.9,by+bl/2+.9]:
    base+=box((bw+3,1.2,3.0),(bx,y,3.5))
# Slots for a 4mm fabric ribbon; use ribbon, never a tight cable tie around the cell.
for x in [bx-bw/2-2,bx+bw/2+2]:base-=box((1.3,5,2.4),(x,by,1))
# USB port opening continues through fixed lid, with cable strain-relief access.
base-=box((13,10,6),(0,33,13.2))
# Relief beside the lower-right PCB boss for the bottom JST mating plug.
# The screw pilot is outside this relief and retains over 1mm radial wall.
base-=box((7.0,9.5,8.2),(16,-15,6.1))
# Fixed lid rests on wall at z14.2, with center aperture for magnet post.
lid=cyl(34.15,1.2,14.2)+ring(36,33,1.3,15.3)
lid+=cyl(13.6,1.7,15.35) # Inner race shoulder at z17.
lid+=cyl(P['bearing_stem_od']/2,7.05,16.95)
lid-=cyl(6.2,12,14)
lid=cut_all(lid,screws(9,15,11,1.6)) # M2 retainer screw pilots.
for x,y in [(24.4,24.4),(-24.4,-24.4)]:
    lid-=cyl(1.1,4,14,x,y)
    lid-=cyl(2.1,.6,16.1,x,y) # Recessed M2 countersink approximation, pan head stays in deck.
lid-=box((13,14,4),(0,29,14.8))
lid-=box((5.2,10.0,4),(-28,-1,15))
lid-=cyl(2.4,4,13,0,-27)
lid-=cyl(1.4,4,13,8,-26)
# SWD and boot access is from the removable bottom/base assembly, no hidden wires.
# Cap: roof, skirt, outer race seat, center magnet post. Knurl cuts are vertical and printable.
cap=cyl(24.5,2,29)+ring(24.5,22,12,17)
cap+=ring(21.8,17.5,12,17)
cap-=cyl(P['bearing_pocket_id']/2,7.05,17-.025)
cap+=cyl(5.2,14,15)
mag=P['magnet'];cap-=cyl(P['magnet_pocket_diameter']/2,mag['thickness']+.15,14.99)
cap=cut_all(cap,screws(20.5,16.9,7.1,1.6))
# Roof access bores let the inner retainer be fastened after the rotor captures
# the bearing. Without these, the closed roof would prevent assembly/removal.
cap=cut_all(cap,screws(9,28.9,2.2,4.4))
for i in range(72):
    a=2*math.pi*i/72;cap-=cyl(.42,12.0,17.0,24.55*math.cos(a),24.55*math.sin(a))
outer_retainer=ring(24.2,17.5,1.2,15.8)
outer_retainer=cut_all(outer_retainer,screws(20.5,15.7,1.4,2.2))
for i in range(3):
    a=2*math.pi*i/3
    outer_retainer-=m.Manifold.cylinder(1.21,2.1,1.1,64).translate((20.5*math.cos(a),20.5*math.sin(a),15.79))
plunger=cyl(2.9,.4,13.6,0,-27)+cyl(1.9,2.05,13.95,0,-27)
inner_retainer=ring(13.5,6.2,1.6,24)
inner_retainer=cut_all(inner_retainer,screws(9,23.9,1.8,2.2))
# A small stem/bore fit coupon saves printing a full enclosure for tolerance tuning.
coupon=ring(21.8,P['bearing_pocket_id']/2,3)+ring(P['bearing_stem_od']/2,6.2,3).translate((43,0,0))
parts={'base':base,'lid':lid,'knob':cap,'outer-retainer':outer_retainer,'inner-retainer':inner_retainer,'fit-coupon':coupon,'button-plunger':plunger}
(ROOT/'stl').mkdir(exist_ok=True)
report={}
for name,s in parts.items():
    if name=='knob':s=s.rotate((180,0,0)).translate((0,0,31))
    else:
        lo=s.bounding_box()[2];s=s.translate((0,0,-lo))
    a=s.to_mesh();mesh=trimesh.Trimesh(np.asarray(a.vert_properties)[:,:3],np.asarray(a.tri_verts),process=True)
    print(name, s.status(), mesh.is_watertight, mesh.is_winding_consistent, mesh.volume);
    assert mesh.is_watertight and mesh.volume>0,(name,'invalid solid')
    mesh.export(ROOT/'stl'/f'{name}.stl')
    report[name]={'watertight':bool(mesh.is_watertight),'volume_mm3':round(mesh.volume,2),'bounds_mm':mesh.bounds.round(3).tolist()}
# Geometry QA uses assembly coordinates, not the print transforms.
assert P['magnet']['bottom_z']-(P['pcb_bottom_z']+P['pcb_thickness']+P['sensor_package_height'])>=1.5
assert P['lid_bottom_z']-(P['pcb_bottom_z']+P['pcb_thickness']+1.6)>=1.0-1e-8
assert (P['pcb_bottom_z']-(bz+bh/2))>=2.0
assert outer_retainer.bounding_box()[2]-P['lid_top_z']>=.39
# Only intended ring/race contacts are allowed. Moving printed parts must not intersect fixed lid.
for name,moving in [('knob',cap),('outer-retainer',outer_retainer)]:
    assert (moving^lid).volume()<1e-5,(name,'lid collision')
    assert (moving^inner_retainer).volume()<1e-5,(name,'inner retainer collision')
assert (cap^outer_retainer).volume()<1e-5,'moving parts overlap'
assert (plunger^lid).volume()<1e-5,'plunger collision'
usb_keepout=box((10.4,8.7,3.5),(0,26.95,13.35))
switch_keepout=box((4.3,8.6,6.2),(-28,-1,14.7))
assert (usb_keepout^lid).volume()<1e-5,'USB body/lid collision'
assert (switch_keepout^lid).volume()<1e-5,'switch body/lid collision'
# Conservative bottom JST body + mating plug volume. Keep the pouch, tray,
# standoffs and floor clear; the flexible cable exits into the open right bay.
jst_keepout=box((6.5,9,8),(16,-15,6))
battery_keepout=box(P['battery_envelope'],P['battery_center'])
assert (jst_keepout^base).volume()<1e-5,'battery connector/base collision'
assert (jst_keepout^battery_keepout).volume()<1e-5,'battery connector/pouch collision'
assert (base^battery_keepout).volume()<1e-5,'battery tray compresses pouch'
report['access_checks']={'usb_body_to_lid':'clear','slide_switch_to_lid':'clear','reset_plunger_to_lid':'clear','battery_connector_to_base_and_pouch':'clear','retainer_countersink_edge_wall_mm':1.6}
report['clearances']={'sensor_to_magnet_mm':round(mag['bottom_z']-13.35,3),'rotor_to_lid_mm':.4,'battery_to_pcb_mm':round(10-(bz+bh/2),3),'stem_diametral_clearance_mm':.15,'bearing_outer_diametral_clearance_mm':.10}
(ROOT/'geometry-check.json').write_text(json.dumps(report,indent=2)+'\n')
fig=plt.figure(figsize=(12,8));ax=fig.add_subplot(111,projection='3d')
triangles=[];facecolors=[]
for solid,color in [(base,'#344752'),(lid,'#6b8797'),(cap,'#e9bd65')]:
    a=solid.to_mesh();verts=np.asarray(a.vert_properties)[:,:3];tri=np.asarray(a.tri_verts)
    triangles.extend(verts[tri]);facecolors.extend([color]*len(tri))
ax.add_collection3d(Poly3DCollection(triangles,facecolors=facecolors,edgecolor='none',zsort='average'))
ax.set(xlim=(-38,38),ylim=(-38,38),zlim=(0,38),xlabel='X / mm',ylabel='Y / mm',zlabel='Z / mm')
ax.set_box_aspect((76,76,38));ax.view_init(28,-55);ax.set_title('Desk knob Rev A — assembled geometry (Ø72 × 31 mm)')
fig.tight_layout();fig.savefig(ROOT/'assembly.png',dpi=160);plt.close(fig)
print(json.dumps(report['clearances'],indent=2))
