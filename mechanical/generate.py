#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Mechanics E10 reduced-height PLA assembly.
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

def cyl(r,h,z=0,x=0,y=0):return m.Manifold.cylinder(h,r,r,192).translate((x,y,z))
def cyl_y(r,start,end,z):return m.Manifold.cylinder(end-start,r,r,96).rotate((-90,0,0)).translate((0,start,z))
def box(size,center):return m.Manifold.cube(size,True).translate(center)
def from_mesh(mesh):
 q=m.Manifold(m.Mesh64(np.ascontiguousarray(mesh.vertices,dtype=np.float64),np.ascontiguousarray(mesh.faces,dtype=np.uint64)))
 assert str(q.status()).endswith('NoError'),str(q.status())
 return q
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

top=P['pcb_bottom_z']+P['pcb_thickness'];bearing=P['bearing'];bt=bearing['bottom_z'];bh=bearing['width'];grip_z=P['knob_bottom_z'];r=P['encoder']['track_radius'];half_track=P['encoder']['track_thickness']/2
mount=P['bearing_mount'];capture=P['pcb_capture'];capture_z=top+capture['compressed_pad_height']
lid_screws=P['chassis_screw_axes']
outer=P['base_diameter']/2;lid_bottom=P['lid_bottom_z'];lid_top=P['lid_top_z']
bearing_top=bt+bh;skirt_bottom=P['encoder']['skirt_bottom_z'];skirt_height=bearing_top+1.8-skirt_bottom
screen_offset=P['display']['pcb_bottom_z']+.45;screen_front=P['display']['front_z'];overall_height=P['display']['bezel_top_z']
usb_access=P['usb_access']
# Use the actual supplier PCB outline to clear rear components omitted by the
# simplified STEP, including the non-circular tab and its rounded shoulders.
screen_mesh=trimesh.load(ROOT/'vendor/obj/screen19192.obj',force='mesh',process=True)
screen_mesh.apply_transform(np.diag([-1.,1.,-1.,1.]));screen_mesh.apply_translation([0,0,screen_offset])
lcd=from_mesh(screen_mesh)
screen_pcb_profile=lcd.slice(P['display']['pcb_bottom_z']+.1)
base=cyl(outer,2)+ring(outer-.2,outer-2.2,lid_bottom-2,2)
for x,y in P['mount_holes']:
 # Unplated locator pegs and lid pads capture the board; no tall PCB standoffs.
 base+=cyl(2.3,.6,2,x,y)+cyl(capture['peg_diameter']/2,2.2,2,x,y)
for x,y in lid_screws:
 base+=cyl(2.2,lid_bottom-2,2,x,y);base-=cyl(.8,lid_bottom-1.9,2,x,y)
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
# The switch sits on an integral front PCB tab behind a captive printed cap.
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
from button import build as build_button
button_surround,button_roof,button_cap=build_button(P)
base+=button_surround-front_pocket
assert (button_surround-cyl(outer-.2,20)).volume()<1e-4,'Button guides must remain inside the circular wall'

lid=ring(outer-.35,27.3,lid_top-lid_bottom,lid_bottom)
# The large hollow bearing post surrounds, rather than stacks over, the screen.
lid+=ring(mount['inner_contact_od']/2,27.3,bt-lid_top+.01,lid_top-.01)+ring(P['bearing_stem_od']/2,27.3,bh,bt)
for x,y in P['mount_holes']:lid+=cyl(2.0,P['lid_bottom_z']-capture_z,capture_z,x,y)
for x,y in capture['front_pad_centers']:lid+=cyl(1.3,P['lid_bottom_z']-capture_z,capture_z,x,y)
for x,y in lid_screws:
 lid-=cyl(1.1,2,lid_bottom-.2,x,y);lid-=csk_hole(x,y,lid_top)
# Entry chamfer on the nominal 60mm push-fit post; no separate bearing clamp.
lid-=ring(30.2,29.7,.6,bearing_top-.6)-m.Manifold.cylinder(.6,30,29.7,128).translate((0,0,bearing_top-.6))
# The flush port keeps the plug body outside the lid; retain its full roof.
lid-=located(box((7.2,5.2,4),(0,0,8.6)),-23,10,P['encoder']['rotation_deg'])
# Keep the existing fork clearance as the main lid plate moves down.
lid-=box((14,4,1),(0,-38.3,7.1))
# Recess only the real USB package envelope, with 0.2mm assembly allowance.
cad_usb=next(c for c in cj if c['type']=='cad_component' and usb_access['model_filename'] in c.get('model_obj_url',''))
usb_mesh=trimesh.load(ROOT/'vendor/solid'/usb_access['solid_filename'],force='mesh')
origin=cad_usb.get('model_origin_position') or {};usb_mesh.apply_translation([-origin.get(k,0) for k in ['x','y','z']])
rotation=cad_usb.get('rotation',{});usb_mesh.apply_transform(trimesh.transformations.euler_matrix(*[math.radians(rotation.get(k,0)) for k in ['x','y','z']]))
pos=cad_usb['position'];usb_mesh.apply_translation([pos['x'],pos['y'],pos['z']+P['pcb_bottom_z']+P['pcb_thickness']/2])
lid-=box(usb_mesh.extents+.4,usb_mesh.bounds.mean(axis=0))
lid+=button_roof
# A raised outer rim stiffens the recessed lid without raising the bearing.
# Driver wells keep both countersunk chassis screws accessible from above.
rim_top=grip_z-.8
lid+=ring(outer-.35,40.0,rim_top-lid_top,lid_top)
for x,y in lid_screws:lid-=cyl(2.2,rim_top-lid_top+.2,lid_top,x,y)
assert (button_roof-cyl(outer-.35,20)).volume()<1e-4,'Button roof must remain inside the circular wall'
assert (base^lid).volume()<1e-4,'Base guides must clear the lid and capture pads'


# The outer race seats against the grip shoulder; the optical skirt joins
# the upper web without crossing the stationary inner-race support.
cap=ring(42.4,P['bearing_pocket_id']/2,bearing_top-grip_z,grip_z)
cap+=ring(42.4,mount['outer_contact_id']/2,1.7,bearing_top)
cap+=ring(42.4,24.8,1.4,bearing_top+1.7)
for i in range(96):
 x,y=polar(42.45,i*TAU/96);cap-=cyl(.4,P['knob_top_z']-grip_z+.6,grip_z-.3,x,y)
# The optical track is printed with the grip, removing its adhesive joint.
encoder_skirt=ring(r+half_track,r-half_track,skirt_height,skirt_bottom)+ring(P['encoder']['bond_outer_radius'],r-half_track,1.4,bearing_top+.44)
for i in range(48):encoder_skirt-=box((3,1.64,1.8),(r,0,8.6)).rotate((0,0,i*360/48))
cap+=encoder_skirt
# Lead-in on the open underside of the 75mm bearing pocket.
cap-=m.Manifold.cylinder(.6,37.8,37.5,128).translate((0,0,grip_z))-cyl(37.4,.8,grip_z-.1)
# Broad PLA end walls support the four actual screen bosses, with splayed
# roots. The screw axes are braced along their entire height rather than
# standing on isolated slender columns through the PCB window.
screen_posts=P['screen_posts']
support=P['screen_support']
wall_height=support['seat_z']-2
for y in support['wall_centers_y_mm']:
 base+=box((support['wall_span_x_mm'],support['wall_thickness_mm'],wall_height),(0,y,2+wall_height/2))
 half=support['wall_thickness_mm']/2;foot=support['foot_thickness_mm']/2
 root=m.CrossSection([[(y-foot,1.9),(y+foot,1.9),
                        (y+half-.1,support['gusset_top_z']),(y-half+.1,support['gusset_top_z'])]])
 base+=root.extrude(support['wall_span_x_mm']).transform([[0,0,1,-support['wall_span_x_mm']/2],[1,0,0,0],[0,1,0,0]])
for x,y in screen_posts:
 near_x=-9.3 if x<0 else 9.3;near_y=13.35 if y>0 else -13.35
 web=m.CrossSection.circle(2,192).translate((x,y))+m.CrossSection.circle(2,192).translate((near_x,near_y))
 base+=web.hull().extrude(wall_height).translate((0,0,2))
 base+=cyl(2.0,support['carrier_bottom_z']-2,2,x,y);base-=cyl(.8,5.2,support['carrier_bottom_z']-5.1,x,y)
for pin in support['locator_pins']:
 base+=cyl(pin['diameter_mm']/2,support['locator_height_mm']+.1,support['seat_z']-.1,*pin['center_mm'])
carrier_z=support['carrier_bottom_z'];carrier_top=carrier_z+1.2
assert abs(P['display']['pcb_bottom_z']-carrier_top-support['carrier_rim_to_PCB_gap_mm'])<1e-6
cradle=ring(24,18.2,1.2,carrier_z)
for x,y in screen_posts:
 # Short radial ledges reach each pillar without loading rear LCD components.
 a=math.atan2(y,x);rr=math.hypot(x,y)
 cradle+=cyl(2.3,1.2,carrier_z,x,y)
 cradle-=cyl(1.1,1.4,carrier_z-.1,x,y)
cradle-=box((5,16,1.4),(-20,0,carrier_z+.6))
bezel_screws=P['bezel_screw_axes']
for x,y in bezel_screws:
 cradle+=cyl(2.2,screen_front-carrier_top,carrier_top,x,y)
 # A through bore must pass the entire boss. A fixed 5mm cut left a 0.1mm
 # membrane at Z18.0..18.1, intersecting each installed M2 screw.
 cradle-=cyl(1.1,screen_front-carrier_z+.2,carrier_z-.1,x,y)
# Keep both shared support pads inside the 48mm carrier envelope.
cradle=cradle^cyl(24,5.2,carrier_z-.1)
# The four real rear bosses sit on the base walls; this rim need not support
# the PCB underside. Clear its full outline, with 0.4mm lateral allowance.
cradle-=screen_pcb_profile.offset(support['carrier_rear_profile_clearance_mm']).extrude(1.6).translate((0,0,carrier_z-.1))
bezel=ring(24,16.6,1.4,screen_front)
# The retaining lip clears the active glass even with estimated stack errors.
relief=P['display']['glass_relief_mm']+.01
bezel-=cyl(19,relief,screen_front-.01)+box((5,15,relief),(-18.75,0,screen_front-.01+relief/2))
for x,y in bezel_screws:
 bezel-=cyl(1.1,1.6,screen_front-.1,x,y)
 bezel-=csk_hole(x,y,overall_height)
# Remove sub-micron Boolean seams before float32 STL export/vertex welding.
# This changes no surface by more than 0.0001mm; it is not a mesh repair.
base=base.as_original().simplify(.0001)
assert (base^lid).volume()<1e-4,'Braced screen supports must clear the stationary lid'
parts={'base':base,'lid':lid,'knob':cap,'screen-carrier':cradle,'screen-bezel':bezel,'button-cap':button_cap}
for obsolete in ['outer-retainer','inner-retainer','bearing-clamp','encoder-skirt']:
 (ROOT/'stl'/f'{obsolete}.stl').unlink(missing_ok=True)
# Print alternatives individually on a small bed. These are calibration samples,
# never assembled product parts and never a substitute for measured race faces.
coupons={}
for name,pocket_delta,stem_delta in [('fit-coupon-tight',-.1,.1),('fit-coupon',0,0),('fit-coupon-loose',.2,-.2)]:
 pocket=P['bearing_pocket_id']+pocket_delta;stem=P['bearing_stem_od']+stem_delta
 parts[name]=ring(40,pocket/2,7)+ring(stem/2,27.3,7).translate((74,0,0))
 coupons[name]={'pocket_id_mm':round(pocket,3),'stem_od_mm':round(stem,3),'height_mm':7,'pocket_center_mm':[0,0],'stem_center_mm':[74,0]}
(ROOT/'fit-coupons.json').write_text(json.dumps(coupons,indent=2)+'\n')
(ROOT/'stl').mkdir(exist_ok=True);report={};poses={}
for name,s in parts.items():
 invert=name in ['knob','screen-bezel','button-cap'];z=s.bounding_box()[5] if invert else s.bounding_box()[2]
 printed=s.rotate((180,0,0)).translate((0,0,z)) if invert else s.translate((0,0,-z))
 a=printed.to_mesh64();mesh=trimesh.Trimesh(np.asarray(a.vert_properties)[:,:3],np.asarray(a.tri_verts),process=True)
 assert mesh.is_watertight and mesh.volume>0,(name,'invalid solid')
 assert len(printed.decompose())==(2 if name.startswith('fit-coupon') else 1),(name,'disconnected print')
 # Binary STL stores float32 coordinates. Round before export and discard only
 # triangles collapsed to zero area by that representation; never fill holes.
 vertices=mesh.vertices.astype(np.float32).astype(np.float64)
 assert np.max(np.abs(vertices-mesh.vertices))<.00001
 mesh=trimesh.Trimesh(vertices,mesh.faces,process=True)
 degenerate=~mesh.nondegenerate_faces(height=1e-8)
 removed=int(degenerate.sum());mesh.update_faces(~degenerate);mesh.remove_unreferenced_vertices()
 assert mesh.is_watertight,(name,'STL quantization opened the mesh')
 path=ROOT/'stl'/f'{name}.stl';mesh.export(path);poses[name]={'inverted':invert,'z':z}
 reloaded=trimesh.load(path,force='mesh',process=True)
 assert reloaded.is_watertight and len(reloaded.split())==(2 if name.startswith('fit-coupon') else 1),(name,'exported STL invalid')
 report[name]={'watertight':True,'stl_roundtrip_watertight':True,'zero_area_triangles_collapsed_by_float32':removed,'volume_mm3':round(mesh.volume,2),'bounds_mm':mesh.bounds.round(3).tolist()}
 print(name,'watertight',round(mesh.volume,1),flush=True)
(ROOT/'print-poses.json').write_text(json.dumps(poses,indent=2)+'\n')
# Use a full solid ring in place of slots to cover every possible rotor angle.
swept_skirt=ring(r+half_track,r-half_track,skirt_height,skirt_bottom)
moving=[('grip with integral optical track',cap),('swept skirt',swept_skirt)]
for name,fixed in [('base',base),('lid',lid),('cradle',cradle),('bezel',bezel)]:
 for mn,mov in moving:assert (mov^fixed).volume()<1e-4,(name,mn,'collision',(mov^fixed).volume())
# Manufacturer screen STEP is rigidly placed above: tab -X, connector +X.
from screen import audit as audit_screen
screen_report=audit_screen(P)
from harness import build as build_harness
harness_meshes,harness_report=build_harness()
(ROOT/'harness.json').write_text(json.dumps(harness_report,indent=2)+'\n')
clearance_harness,_=build_harness(wire_od=P['stock_display_cable']['wire_od_check_mm'])
# The supplier socket is a simplified solid, with no mating cavity. Permit
# plug engagement only inside that socket envelope, never through the PCB/glass.
socket_envelope=box((6,20,5.6),(8.2,0,P['display']['cable_mating']['axis_z_mm']))
plug=from_mesh(harness_meshes['lcd-cable-screen-plug'])
assert (plug^(lcd-socket_envelope)).volume()<1e-4,'Display plug must engage only the real rear socket envelope'
for label,printed in [('base',base),('lid',lid),('cradle',cradle),('bezel',bezel)]:
 assert (plug^printed).volume()<1e-4,(label,'side-entry display plug collision')
report['screen_fit']=screen_report
for name,printed in [('base',base),('lid',lid),('cradle',cradle),('bezel',bezel)]:
 assert (printed^lcd).volume()<1e-4,(name,'manufacturer screen collision',(printed^lcd).volume())
# Verify real rear boss contact, rather than only a free-space collision check.
for x,y in P['display']['mounting_hole_centers_mm']:
 contact=base.translate((0,0,.01))^lcd^cyl(2,.04,support['seat_z']-.01,x,y)
 assert contact.volume()>.01,('Screen boss not supported',x,y)
assert (lcd.translate((0,0,.5))^bezel).volume()>.01,'Bezel must capture screen before its locating pins disengage'
report['screen_fit']['rear_boss_contacts_checked']=4
report['screen_fit']['bezel_captures_before_locator_disengagement']=True
# Conservative space reservation, not fabricated supplier component geometry.
rear_depth=P['display']['rear_component_clearance_depth_mm']
rear_space=screen_pcb_profile.extrude(rear_depth).translate((0,0,P['display']['pcb_bottom_z']-rear_depth))
for x,y in P['display']['mounting_hole_centers_mm']:
 rear_space-=cyl(2.05,rear_depth+2,P['display']['pcb_bottom_z']-rear_depth-1,x,y)
# Existing socket, boss and estimated mated housing footprints are already
# occupied by their own checked geometry; components cannot occupy them too.
rear_space-=box((10.6,20.6,rear_depth+2),(10.2,0,P['display']['pcb_bottom_z']-rear_depth/2))
for name,printed in [('base',base),('lid',lid),('carrier',cradle),('bezel',bezel)]:
 assert (rear_space^printed).volume()<1e-4,(name,'screen rear-component space obstructed')
for name,mesh in clearance_harness.items():
 if name.startswith('lcd-wire-') or name in ['lcd-cable-board-plugs','lcd-cable-splice-sleeves']:assert (rear_space^from_mesh(mesh)).volume()<1e-4,(name,'screen rear-component space obstructed')
report['screen_fit']['rear_component_reservation']={'depth_mm':rear_depth,'carrier_profile_lateral_clearance_mm':support['carrier_rear_profile_clearance_mm'],'outline':'Cross-section of the original supplier PCB, including its tab','exclusions':'Existing four rear bosses, socket and estimated mated plug footprint','status':'Conservative engineering allowance; actual component heights and kit fit remain unmeasured'}
(ROOT/'screen-fit.json').write_text(json.dumps(screen_report,indent=2)+'\n')
# PCB material must not intersect either part nested through its window.
board=next(c for c in cj if c['type']=='pcb_board')
cutout=next(c for c in cj if c['type']=='pcb_cutout')
polygon=lambda points:m.CrossSection([[(v['x'],v['y']) for v in points]])
outline=polygon(board['outline']).extrude(P['pcb_thickness']).translate((0,0,P['pcb_bottom_z']))
window=polygon(cutout['points']).extrude(2).translate((0,0,2.4))
pcb=outline-window
for x,y in P['mount_holes']:pcb-=cyl(1.35,2,2.4,x,y)
assert (base^pcb).volume()<1e-4,'Base must clear actual PCB material and NPTHs'
# Both posts must clear the window even with PCB registration, print and
# regular routed-contour tolerances. Bearing/SMT errors do not apply here.
f=P['fit_budget'];capture=P['pcb_capture']
pcb_play=(2.7+f['pcb_hole_diameter_error']-(capture['peg_diameter']-f['printed_fit_diameter_error']))/2
post_window_error=pcb_play+f['printed_surface_error']+f['pcb_cutout_edge_error']
for x,y in P['screen_posts']:
 assert (cyl(2.0+post_window_error,2,2.4,x,y)^pcb).volume()<1e-4,'Screen post must clear tolerance-expanded PCB window edge'
report['screen_post_to_window_tolerance_checked_mm']=round(post_window_error,4)
# Expand the entire wall footprint at PCB height, including every gusset/web,
# to cover board registration, printed profile and routed-window uncertainty.
support_slice=base.slice(3.4)^m.CrossSection.square((40,48),True)
support_expanded=support_slice.offset(post_window_error).extrude(P['pcb_thickness']).translate((0,0,P['pcb_bottom_z']))
assert (support_expanded^pcb).volume()<1e-4,'Braced screen walls must clear the tolerance-expanded PCB window'
report['screen_support']=support

assert (pcb^lcd).volume()<1e-4
# A 12mm fingertip can depress the broad cap all the way to its nominal stop.
button_design=button['printed_cap']
finger_radius=button['finger_check_radius_mm'];pressed_face=button_design['face_front_y']+button_design['nominal_max_travel_mm']
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
fixed_hardware=[('USB plug approach gauge',plug_gauge),('programming header',box((13.9,4.5,6),(P['programming_connector'][0],P['programming_connector'][1]-.55,7.2))),('LCD manufacturer model',lcd),('PCB',pcb)]
for name,mesh in clearance_harness.items():fixed_hardware.append((name,from_mesh(mesh)))
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
package_bodies=[]
for cad in [v for v in cj if v['type']=='cad_component' and v.get('model_obj_url')]:
 url=cad['model_obj_url'];filename=url.split('?')[0].split('/')[-1]
 path=ROOT/'vendor/obj'/filename
 if not path.exists():raise AssertionError(('Missing real package mesh',filename))
 solid_path=ROOT/'vendor/solid'/filename.replace('.obj','.ply')
 # Preserve the button STEP's distinct coincident seam edges.
 mesh=trimesh.load(solid_path if solid_path.exists() else path,force='mesh',process=filename not in ['b3u3000.obj','header2x4-ra.obj'])
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
 package_bodies.append((filename,physical))
 for wn,wire_mesh in clearance_harness.items():
  if wn.startswith('lcd-wire-') or wn in ['lcd-cable-board-plugs','lcd-cable-splice-sleeves']:assert (physical^from_mesh(wire_mesh)).volume()<1e-4,(filename,wn,'wire/package collision')
 assert (physical^plug_gauge).volume()<1e-4,(filename,'USB plug approach/package collision')
 if filename==usb_access['model_filename']:
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
for name,mesh in clearance_harness.items():
 if not (name.startswith('lcd-wire-') or name in ['lcd-cable-board-plugs','lcd-cable-splice-sleeves']):continue
 wire=from_mesh(mesh)
 for pn,printed in [('base',base),('lid',lid),('cradle',cradle),('bezel',bezel),('PCB',pcb),('LCD module',lcd)]:
  assert (wire^printed).volume()<1e-4,(name,pn,'wire collision',(wire^printed).volume())
 for other_name,other in wire_solids:assert (wire^other).volume()<1e-5,(name,other_name,'wires intersect')
 wire_solids.append((name,wire))
report['purchased_package_models_checked']=package_checks
report['individual_wires_checked']=8
report['removable_harness_nonmetal_groups_checked']=len(wire_solids)
from fit import evaluate as evaluate_fit
fit_report=evaluate_fit(P)
(ROOT/'fit-budget.json').write_text(json.dumps(fit_report,indent=2)+'\n')
# Full circular envelopes fill cosmetic grooves and screw holes, so a feature
# cannot hide a collision at another rotor angle. Analytic annular expansion
# gives the same stated radial/axial budget without tessellation-heavy sums.
def tolerance_probes(radius,dz):
 def expanded(ro,ri,height,z):return ring(ro+radius,ri-radius,height+2*dz,z-dz)
 swept_cap=expanded(42.4,P['bearing_pocket_id']/2,bearing_top-grip_z,grip_z)+expanded(42.4,mount['outer_contact_id']/2,1.7,bearing_top)+expanded(42.4,24.8,1.4,bearing_top+1.7)
 return [('grip',swept_cap),('swept skirt',expanded(r+half_track,r-half_track,skirt_height,skirt_bottom)),('skirt flange',expanded(P['encoder']['bond_outer_radius'],r-half_track,1.4,bearing_top+.44))]
print_probes=tolerance_probes(P['fit_budget']['moving_xy_print_check'],P['fit_budget']['moving_z_print_check'])
pcb_probes=tolerance_probes(P['fit_budget']['moving_xy_pcb_check'],P['fit_budget']['moving_z_hardware_check'])
for name,fixed in [('base',base),('lid',lid),('cradle',cradle),('bezel',bezel)]:
 for mn,mov in print_probes:assert (mov^fixed).volume()<1e-4,(name,mn,'tolerance-envelope collision',(mov^fixed).volume())
for name,fixed in fixed_hardware+package_bodies:
 for mn,mov in pcb_probes:assert (mov^fixed).volume()<1e-4,(name,mn,'hardware tolerance-envelope collision',(mov^fixed).volume())
from bearing import build as build_bearing
_,bearing_solids,bearing_report=build_bearing(P)
for name,s in bearing_solids.items():
 for pn,printed in [('base',base),('lid',lid),('cradle',cradle),('bezel',bezel),*moving]:
  assert (s^printed).volume()<1e-4,(name,pn,'bearing/printed-part collision',(s^printed).volume())
# Two axial shoulders and two radial push-fit interfaces contact their own race.
contacts=[('inner lower',lid.translate((0,0,.01)),'bearing-inner-race'),
 ('outer upper',cap.translate((0,0,-.01)),'bearing-outer-race'),
 ('inner bore',lid.scale((1.0004,1.0004,1)),'bearing-inner-race'),
 ('outer pocket',cap.scale((.9998,.9998,1)),'bearing-outer-race')]
for label,contact,race in contacts:
 assert (contact^bearing_solids[race]).volume()>.1,(label,'bearing contact missing')
 for name,solid in bearing_solids.items():
  if name!=race:assert (contact^solid).volume()<1e-4,(label,'contacts incorrect bearing part',name)
report['tolerance_envelopes_checked']={'print_xy_mm':P['fit_budget']['moving_xy_print_check'],'hardware_xy_mm':P['fit_budget']['moving_xy_pcb_check'],'print_z_mm':P['fit_budget']['moving_z_print_check'],'hardware_z_mm':P['fit_budget']['moving_z_hardware_check'],'wire_od_mm':P['stock_display_cable']['wire_od_check_mm'],'full_rotor_sweep':True}
report['bearing_contacts_checked']=4
report['assembly_simplification']=P['assembly_simplification']
for x,y in lid_screws:
 assert (lid^cyl(2.0,12,lid_top+.01,x,y)).volume()<1e-4,'A 4mm driver gauge must reach each chassis screw'
report['recessed_lid']={'plate_top_z_mm':lid_top,'outer_rim_top_z_mm':rim_top,'rim_to_grip_nominal_gap_mm':round(grip_z-rim_top,3),'chassis_driver_diameter_checked_mm':4.0}
# Check a fingertip at full pretravel with PCB play/height and case-profile error.
# PCB and original switch housing move together; only its actuator may touch.
xy=fit_report['results']['PCB_maximum_in_plane_play_mm']
dz=P['fit_budget']['pcb_thickness_error']+P['fit_budget']['relative_print_z_error']
button_tolerance_checks=0
for dx in [-xy,xy]:
 for zshift in [-dz,dz]:
  shift=(dx,xy+P['fit_budget']['printed_surface_error'],zshift)
  f=finger.translate(shift)
  for name,s in [('base',base),('lid',lid),('PCB',pcb.translate(shift)),*print_probes]:
   assert (f^s).volume()<1e-4,(name,'button access at tolerance limit',(f^s).volume())
  for name,s in package_bodies:
   if name!='b3u3000.obj':assert (f^s.translate(shift)).volume()<1e-4,(name,'finger/package tolerance collision')
  button_tolerance_checks+=1
report['button_tolerance_access_checks']=button_tolerance_checks
button_checks=0
for travel in np.linspace(0,button_design['nominal_max_travel_mm'],13):
 pressed=button_cap.translate((0,float(travel),0))
 for name,fixed in [('base',base),('lid',lid),('PCB',pcb),('LCD',lcd),*moving]:
  assert (pressed^fixed).volume()<1e-4,(name,'printed cap travel collision',travel,(pressed^fixed).volume())
 for name,physical in package_bodies:
  # Omron drawing: housing front is 1.25mm from the footprint datum.
  # Only the projecting actuator moves; never exclude the fixed housing.
  if name=='b3u3000.obj':
   actuator=box((2,1.0,1.4),(0,-42.66,button_z))
   physical-=actuator
  assert (pressed^physical).volume()<1e-4,(name,'cap/fixed package collision',travel)
 button_checks+=1
available=button_design['rest_tip_y']+button_design['nominal_max_travel_mm']-button['actuator_front_y']
assert abs(available-button['datasheet_pretravel_mm']['max'])<1e-6
assert (button_cap.translate((0,button_design['nominal_max_travel_mm']+.05,0))^base).volume()>.01,'The side ears must meet the physical stop'
report['printed_button']={**button_design,'checked_travel_poses':button_checks,'nominal_switch_travel_at_stop_mm':round(available,3),'checks':'Nominal cap sweep, fixed housing clearance, stop engagement and fingertip access. Friction, switch tolerance and safe overtravel require a printed prototype; no actuation force or cycle life is certified.'}
report['printed_button']['fixed_guide_within_circular_wall']=True
report['printed_button']['fixed_guide_max_radius_mm']=outer-.2
report['front_button']=P['front_button']
report['direct_finger_access_checked']=True
report['separate_button_plunger']=True
report['button_projection_beyond_wall_mm']=round(-button_design['face_front_y']-(outer-.2),3)
report['pressed_button_projection_beyond_wall_mm']=round(-pressed_face-(outer-.2),3)
report['USB_access']={**usb_access,'outer_case_diameter_mm':P['base_diameter'],
 'socket_recess_from_floor_outer_edge_mm':round(outer-usb_access['socket_face_y'],4),
 'socket_projection_beyond_side_wall_mm':round(usb_access['socket_face_y']-(outer-.2),4),
 'PCB_front_edge_mm':max(q['y'] for q in board['outline']),
 'plug_body_to_PCB_axial_gap_mm':round(plug_start-max(q['y'] for q in board['outline']),4),
 'maximum_plug_approach_sweep_checked':True,'all_package_and_PCB_clearances_checked':True}

report['clearances']={'overall_height_mm':overall_height,'previous_height_mm':47,'height_reduction_percent':round((47-overall_height)/47*100,1),'grip_lower_edge_mm':grip_z,'previous_grip_lower_edge_mm':22,'USB_plug_max_height_mm':usb_access['plug_height_mm'],'USB_plug_to_rotor_vertical_mm':round(grip_z-(usb_access['axis_z']+usb_access['plug_height_mm']/2),3),'bezel_to_grip_radial_mm':.8,'skirt_to_sensor_radial_each_side_mm':(3-P['encoder']['track_thickness'])/2,'PCB_bottom_z_mm':2.6,'LCD_connector_in_PCB_window':True,'bearing_id_mm':60,'bearing_od_mm':75,'bearing_width_mm':7,'bearing_stem_diametral_mm':round(bearing['id']-P['bearing_stem_od'],3),'bearing_outer_diametral_mm':round(P['bearing_pocket_id']-bearing['od'],3),'encoder_slot_count':48,'quadrature_edges_per_turn':192,'all_components_top_side':True,'solder_well_floor_remaining_mm':1.2}
report['scope']='Manufacturer screen/package models with user-authorized estimated bearing/cable details. Nominal contacts and full-rotation tolerance envelopes checked under fit-budget.json assumptions. Hardware operation and actual print capability are not measured.'
(ROOT/'geometry-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['clearances'],indent=2))
