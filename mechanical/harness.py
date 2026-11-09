# SPDX-License-Identifier: MIT
"""Supplied Waveshare cable, shortened in its middle; both factory connector ends retained."""
import math,json
from pathlib import Path
import numpy as np,trimesh,manifold3d as m
SIGNALS=['BL','RST','DC','CS','CLK','DIN','GND','VCC']
COLORS=['#b45cce','#ffffff','#ee9b34','#e4d751','#528cdd','#59ac70','#222c38','#e45555']
WIRE_OD=1.2 # User-authorized best approximation; clearance is also checked at 1.5mm.

def solid(q):
 a=q.to_mesh64();return trimesh.Trimesh(np.asarray(a.vert_properties)[:,:3],np.asarray(a.tri_verts),process=True)
def box(s,c):return m.Manifold.cube(s,True).translate(c)
def tube(points,radius):
 pts=np.asarray(points);tangent=np.gradient(pts,axis=0);tangent/=np.linalg.norm(tangent,axis=1)[:,None]
 # Wires progress in X/Z; a fixed Y reference gives continuous round sections.
 a=np.cross(tangent,[0,1,0]);a/=np.linalg.norm(a,axis=1)[:,None];b=np.cross(tangent,a)
 angles=np.arange(12)*2*math.pi/12
 vertices=(pts[:,None,:]+radius*(a[:,None,:]*np.cos(angles)[None,:,None]+b[:,None,:]*np.sin(angles)[None,:,None])).reshape((-1,3)).tolist();faces=[]
 for i in range(len(pts)-1):
  for k in range(12):
   x=i*12+k;y=i*12+(k+1)%12;faces.extend([(x,y,y+12),(x,y+12,x+12)])
 vertices.extend([pts[0],pts[-1]]);lo=len(vertices)-2;hi=lo+1
 for k in range(12):faces.extend([(lo,(k+1)%12,k),(hi,(len(pts)-1)*12+k,(len(pts)-1)*12+(k+1)%12)])
 q=trimesh.Trimesh(vertices,faces,process=True);q.fix_normals();assert q.is_watertight;return q

def fragment(path, start, end):
 pts=np.asarray(path);distance=np.r_[0,np.linalg.norm(np.diff(pts,axis=0),axis=1).cumsum()]
 def at(d):return np.array([np.interp(d,distance,pts[:,k]) for k in range(3)])
 return np.vstack((at(start),pts[(distance>start+1e-8)&(distance<end-1e-8)],at(end)))

def build(wire_od=None):
 P=json.loads(Path(__file__).with_name('parameters.json').read_text())
 wire_od=wire_od or P['stock_display_cable']['modeled_wire_od_mm']
 h=P['display_board_header'];RADIUS=P['stock_display_cable']['display_u_bend_radius_mm']
 connector=P['display']['cable_mating'];exit_x=connector['wire_exit_x_mm'];axis_z=connector['axis_z_mm']
 board_x,board_y=P['display_connector'];entry=board_x-h['body_front_local_y_mm']+h['female_entry_gap_mm']
 wire_start_x=entry+h['female_housing_length_mm'];parts={};records=[]
 housing=box((6.85,17.8,4.5),(exit_x-6.85/2,0,axis_z))
 for i in range(8):housing-=box((6.95,1.4,2.8),(exit_x-6.85/2,-7+2*i,axis_z))
 parts['lcd-cable-screen-plug']=solid(housing)
 board_housings=[];contacts=[];sleeves=[]
 for i,(signal,color) in enumerate(zip(SIGNALS,COLORS)):
  ya=board_y-3.81+2.54*(i//2);yb=-7+2*i
  za=P['pcb_bottom_z']+P['pcb_thickness']+h['pin_axis_above_pcb_mm'][i%2]
  female=box((h['female_housing_length_mm'],h['female_housing_section_mm'],h['female_housing_section_mm']),(entry+h['female_housing_length_mm']/2,ya,za))
  female-=box((6.4,.9,.9),(entry+3.1,ya,za))
  female-=m.Manifold.cylinder(2,.72,.72,32).rotate((0,90,0)).translate((wire_start_x-1.8,ya,za))
  board_housings.append(female)
  t=np.linspace(0,1,210);f=10*t**3-15*t**4+6*t**5
  lower_z=axis_z-2*RADIUS
  # Delaying upper-row descent keeps the two physical header rows separated
  # while the eight leads fan into the screen's single PH row.
  zf=f**1.8 if i%2 else f
  sweep=np.column_stack((wire_start_x+(exit_x-wire_start_x)*t,ya+(yb-ya)*f,za+(lower_z-za)*zf))
  theta=np.linspace(0,math.pi,100)
  arc=np.column_stack((exit_x+RADIUS*np.sin(theta),np.full_like(theta,yb),lower_z+RADIUS*(1-np.cos(theta))))
  path=np.vstack((sweep,arc[1:]));length=float(np.linalg.norm(np.diff(path,axis=0),axis=1).sum())
  centre=7.0 if i%2 else 17.0 if signal=='GND' else 14.0
  assert centre+3.2<length
  jackets=[tube(fragment(path,0,centre-1.25),wire_od/2),tube(fragment(path,centre+1.25,length),wire_od/2)]
  q=trimesh.util.concatenate(jackets);q.visual=trimesh.visual.ColorVisuals(q,vertex_colors=trimesh.visual.color.hex_to_rgba(color));parts['lcd-wire-'+signal.lower()]=q
  joint_path=fragment(path,centre-3,centre+3)
  sleeve_outer=solid_to_manifold(tube(joint_path,1.0));sleeve_inner=solid_to_manifold(tube(joint_path,wire_od/2+.08));sleeves.append(sleeve_outer-sleeve_inner)
  # Both original factory ends remain. Shorten the middle, join the conductors
  # and insulate every joint individually; no additional connector/crimp kit.
  contacts.append(solid_to_manifold(tube(path,.16)))
  contacts.append(box((5.7,.5,.5),(exit_x-5.7/2,yb,axis_z)))
  contacts.append(box((8.8,.34,.34),(entry+10.1,ya,za)))
  contacts.append(box((4.8,.7,.7),(entry+3.5,ya,za))-box((5,.64,.64),(entry+3.5,ya,za)))
  contacts.append(solid_to_manifold(tube(fragment(path,centre-1.25,centre+1.25),.28)))
  velocity=np.gradient(path,axis=0);acceleration=np.gradient(velocity,axis=0);cross=np.linalg.norm(np.cross(velocity,acceleration),axis=1);valid=cross>1e-10
  radii=np.linalg.norm(velocity[valid],axis=1)**3/cross[valid]
  records.append({'signal':signal,'color_illustration_only':color,'board_connector':'J6 removable 2x4 right-angle header','board_pin':i+1,'board_hole_mm':[board_x+(1.27 if i%2==0 else -1.27),ya,4.2],'female_housing_entry_mm':[entry,ya,za],'board_end_wire_exit_mm':path[0].tolist(),'screen_housing_wire_exit_mm':path[-1].tolist(),'screen_pin':i+1,'modeled_free_wire_path_mm':round(length,3),'estimated_minimum_centerline_radius_mm':round(float(min(radii)),3),'splice_center_distance_from_female_housing_mm':centre,'splice_sleeve_length_mm':6,'splice_sleeve_outer_diameter_mm':2,'centerline_mm':path.round(5).tolist()})
 parts['lcd-cable-board-plugs']=solid(m.Manifold.batch_boolean(board_housings,m.OpType.Add))
 parts['lcd-cable-splice-sleeves']=solid(m.Manifold.batch_boolean(sleeves,m.OpType.Add))
 parts['lcd-cable-contacts']=solid(m.Manifold.batch_boolean(contacts,m.OpType.Add))
 report={'harness':'Included Waveshare lead shortened in its middle; both original factory connector ends retained','included':True,'custom_harness_required':False,'board_connection':'Fitted Wurth 61300821021 / C5517754 right-angle 2x4 male header, supplied individual female jumper ends','housing':'Original PH2.0 8-pin display plug and all eight 2.54mm female jumper housings retained','wire':'Original included wires; shorten middle sections and solder eight individually insulated inline joints','wire_od_design_envelope_mm':wire_od,'display_U_bend_radius_mm':RADIUS,'manufacturer_bend_radius':'Unpublished; static bends use explicit engineering approximations','trim_instruction':'Mate both factory connector ends, trial-dress with assembly slack, then remove excess from the middle of each lead. Retain enough tail to solder without heating the housings. Join by signal and insulate every joint with heat-shrink before closure. Model locations are packing estimates, not fixed cut lengths. Check continuity and insulation before USB power. Never cut off the original female jumper ends.','screen_pose':f"180deg about Y from official STEP, plus Z{P['display']['pcb_bottom_z']+.45}mm; tab points -X",'mating':connector,'board_mating':h,'connections':records,'scope':'Original kit ends retained. Female housings use the accepted nominal 2.54x2.54x14.5mm envelope. Modelled wire OD1.2mm, clearance checked OD1.5mm; 2mm finished splice sleeves and 6mm length are conservative assembly envelopes. Exact housing, contact engagement, wire OD, bend limits and free lengths require actual kit fit.'}
 return parts,report

def solid_to_manifold(mesh):
 return m.Manifold(m.Mesh64(np.ascontiguousarray(mesh.vertices,dtype=np.float64),np.ascontiguousarray(mesh.faces,dtype=np.uint64)))

if __name__=='__main__':
 parts,report=build();out=Path(__file__).resolve().parent/'harness.json';out.write_text(json.dumps(report,indent=2)+'\n');print([r['modeled_free_wire_path_mm'] for r in report['connections']])
