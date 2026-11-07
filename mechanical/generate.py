#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Mechanics E5 simplified assembly and printable solids.
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
outer=P['base_diameter']/2
usb_access=P['usb_access']
base=cyl(outer,2)+ring(outer-.2,outer-2.2,7.2,2)
for x,y in P['mount_holes']:
 # Unplated locator pegs and lid pads capture the board; no tall PCB standoffs.
 base+=cyl(2.3,.6,2,x,y)+cyl(capture['peg_diameter']/2,2.2,2,x,y)
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

lid=ring(outer-.35,27.3,1.2,9.2)
# The large hollow bearing post surrounds, rather than stacks over, the screen.
lid+=ring(mount['inner_contact_od']/2,27.3,bt-10.39,10.39)+ring(P['bearing_stem_od']/2,27.3,bh,bt)
for x,y in P['mount_holes']:lid+=cyl(2.0,P['lid_bottom_z']-capture_z,capture_z,x,y)
for x in [-6,6]:lid+=cyl(1.3,P['lid_bottom_z']-capture_z,capture_z,x,-37)
for x,y in lid_screws:
 lid-=cyl(1.1,2,9,x,y);lid-=csk_hole(x,y,10.4)
# Entry chamfer on the nominal 60mm push-fit post; no separate bearing clamp.
lid-=ring(30.2,29.7,.6,18.4)-m.Manifold.cylinder(.6,30,29.7,128).translate((0,0,18.4))
# The flush port keeps the plug body outside the lid; retain its full roof.
lid-=located(box((7.2,5.2,4),(0,0,8.6)),-23,10,P['encoder']['rotation_deg'])
lid+=button_roof


# The outer race seats against the grip shoulder; the optical skirt joins
# the upper web without crossing the stationary inner-race support.
cap=ring(42.4,P['bearing_pocket_id']/2,19-grip_z,grip_z)
cap+=ring(42.4,mount['outer_contact_id']/2,1.7,19)
cap+=ring(42.4,24.8,1.4,20.7)
for i in range(96):
 x,y=polar(42.45,i*TAU/96);cap-=cyl(.4,12,10.5,x,y)
# The optical track is printed with the grip, removing its adhesive joint.
encoder_skirt=ring(r+half_track,r-half_track,12.9,7.9)+ring(P['encoder']['bond_outer_radius'],r-half_track,1.4,19.44)
for i in range(48):encoder_skirt-=box((3,1.64,1.8),(r,0,8.6)).rotate((0,0,i*360/48))
cap+=encoder_skirt
# Lead-in on the open underside of the 75mm bearing pocket.
cap-=m.Manifold.cylinder(.6,37.8,37.5,128).translate((0,0,grip_z))-cyl(37.4,.8,grip_z-.1)
# Two base posts share the bezel/carrier screws and stay inside the PCB window.
screen_posts=P['screen_posts']
for x,y in screen_posts:
 base+=cyl(2.0,14.1,2,x,y);base-=cyl(.8,5.2,11,x,y)
cradle=ring(24,18.2,1.2,16.1)
for x,y in screen_posts:
 # Short radial ledges reach each pillar without loading rear LCD components.
 a=math.atan2(y,x);rr=math.hypot(x,y)
 cradle+=cyl(2.3,1.2,16.1,x,y)
 cradle-=cyl(1.1,1.4,16,x,y)
cradle-=box((5,16,1.4),(-20,0,16.7))
bezel_screws=P['bezel_screw_axes']
for x,y in bezel_screws:
 cradle+=cyl(2.2,3.6,17.3,x,y);cradle-=cyl(1.1,5,16,x,y)
# Keep both shared support pads inside the 48mm carrier envelope.
cradle=cradle^cyl(24,5,16)
bezel=ring(24,16.6,1.4,20.9)
# The retaining lip clears the active glass even with estimated stack errors.
relief=P['display']['glass_relief_mm']+.01
bezel-=cyl(19,relief,20.89)+box((5,15,relief),(-18.75,0,20.89+relief/2))
for x,y in bezel_screws:
 bezel-=cyl(1.1,1.6,20.8,x,y)
 bezel-=csk_hole(x,y,22.3)
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
 invert=name in ['knob','screen-bezel'];z=s.bounding_box()[5] if invert else s.bounding_box()[2]
 printed=s.rotate((180,0,0)).translate((0,0,z)) if invert else s.translate((0,0,-z))
 a=printed.to_mesh64();mesh=trimesh.Trimesh(np.asarray(a.vert_properties)[:,:3],np.asarray(a.tri_verts),process=True)
 assert mesh.is_watertight and mesh.volume>0,(name,'invalid solid')
 assert len(printed.decompose())==(2 if name.startswith('fit-coupon') else 1),(name,'disconnected print')
 mesh.export(ROOT/'stl'/f'{name}.stl');poses[name]={'inverted':invert,'z':z}
 report[name]={'watertight':True,'volume_mm3':round(mesh.volume,2),'bounds_mm':mesh.bounds.round(3).tolist()}
 print(name,'watertight',round(mesh.volume,1),flush=True)
(ROOT/'print-poses.json').write_text(json.dumps(poses,indent=2)+'\n')
# Use a full solid ring in place of slots to cover every possible rotor angle.
swept_skirt=ring(r+half_track,r-half_track,12.9,7.9)
moving=[('grip with integral optical track',cap),('swept skirt',swept_skirt)]
for name,fixed in [('base',base),('lid',lid),('cradle',cradle),('bezel',bezel)]:
 for mn,mov in moving:assert (mov^fixed).volume()<1e-4,(name,mn,'collision',(mov^fixed).volume())
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
clearance_harness,_=build_harness(wire_od=P['stock_display_cable']['wire_od_check_mm'])
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
# Both posts must clear the window even with PCB registration, print and
# regular routed-contour tolerances. Bearing/SMT errors do not apply here.
f=P['fit_budget'];capture=P['pcb_capture']
pcb_play=(2.7+f['pcb_hole_diameter_error']-(capture['peg_diameter']-f['printed_fit_diameter_error']))/2
post_window_error=pcb_play+f['printed_surface_error']+f['pcb_cutout_edge_error']
for x,y in P['screen_posts']:
 assert (cyl(2.0+post_window_error,2,2.4,x,y)^pcb).volume()<1e-4,'Screen post must clear tolerance-expanded PCB window edge'
report['screen_post_to_window_tolerance_checked_mm']=round(post_window_error,4)

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
 package_bodies.append((filename,physical))
 for wn,wire_mesh in clearance_harness.items():
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
for name,mesh in clearance_harness.items():
 if not name.startswith('lcd-wire-'):continue
 wire=from_mesh(mesh)
 for pn,printed in [('base',base),('lid',lid),('cradle',cradle),('bezel',bezel),('PCB',pcb),('LCD module',lcd)]:
  assert (wire^printed).volume()<1e-4,(name,pn,'wire collision',(wire^printed).volume())
 for other_name,other in wire_solids:assert (wire^other).volume()<1e-5,(name,other_name,'wires intersect')
 wire_solids.append((name,wire))
report['purchased_package_models_checked']=package_checks
report['individual_wires_checked']=len(wire_solids)
from fit import evaluate as evaluate_fit
fit_report=evaluate_fit(P)
(ROOT/'fit-budget.json').write_text(json.dumps(fit_report,indent=2)+'\n')
# Full circular envelopes fill cosmetic grooves and screw holes, so a feature
# cannot hide a collision at another rotor angle. Analytic annular expansion
# gives the same stated radial/axial budget without tessellation-heavy sums.
def tolerance_probes(radius,dz):
 def expanded(ro,ri,height,z):return ring(ro+radius,ri-radius,height+2*dz,z-dz)
 swept_cap=expanded(42.4,P['bearing_pocket_id']/2,19-grip_z,grip_z)+expanded(42.4,mount['outer_contact_id']/2,1.7,19)+expanded(42.4,24.8,1.4,20.7)
 return [('grip',swept_cap),('swept skirt',expanded(r+half_track,r-half_track,12.9,7.9)),('skirt flange',expanded(P['encoder']['bond_outer_radius'],r-half_track,1.4,19.44))]
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

report['clearances']={'overall_height_mm':22.3,'previous_height_mm':47,'height_reduction_percent':round((47-22.3)/47*100,1),'grip_lower_edge_mm':10.8,'previous_grip_lower_edge_mm':22,'USB_plug_max_height_mm':usb_access['plug_height_mm'],'USB_plug_to_rotor_vertical_mm':round(grip_z-(usb_access['axis_z']+usb_access['plug_height_mm']/2),3),'bezel_to_grip_radial_mm':.8,'skirt_to_sensor_radial_each_side_mm':(3-P['encoder']['track_thickness'])/2,'PCB_bottom_z_mm':2.6,'LCD_connector_in_PCB_window':True,'bearing_id_mm':60,'bearing_od_mm':75,'bearing_width_mm':7,'bearing_stem_diametral_mm':round(bearing['id']-P['bearing_stem_od'],3),'bearing_outer_diametral_mm':round(P['bearing_pocket_id']-bearing['od'],3),'encoder_slot_count':48,'quadrature_edges_per_turn':192,'all_components_top_side':True,'solder_well_floor_remaining_mm':1.2}
report['scope']='Manufacturer screen/package models with user-authorized estimated bearing/cable details. Nominal contacts and full-rotation tolerance envelopes checked under fit-budget.json assumptions. Hardware operation and actual print capability are not measured.'
(ROOT/'geometry-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['clearances'],indent=2))
