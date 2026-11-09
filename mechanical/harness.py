# SPDX-License-Identifier: MIT
"""H1: one made-to-drawing JST-SH8 to JST-PH8 crimped display harness.

Housing boundary dimensions are from JST drawings. Engagement, internal contact
shapes and dressed bends are nominal engineering models, not supplier CAD.
"""
import math,json
from pathlib import Path
import numpy as np,trimesh,manifold3d as m
SIGNALS=['BL','RST','DC','CS','CLK','DIN','GND','VCC']
COLORS=['#b45cce','#ffffff','#ee9b34','#e4d751','#528cdd','#59ac70','#222c38','#e45555']
def solid(q):
 a=q.to_mesh64();return trimesh.Trimesh(np.asarray(a.vert_properties)[:,:3],np.asarray(a.tri_verts),process=True)
def box(s,c):return m.Manifold.cube(s,True).translate(c)
def solid_to_manifold(mesh):
 return m.Manifold(m.Mesh64(np.ascontiguousarray(mesh.vertices,dtype=np.float64),np.ascontiguousarray(mesh.faces,dtype=np.uint64)))
def tube(points,radius):
 pts=np.asarray(points);tangent=np.gradient(pts,axis=0);tangent/=np.linalg.norm(tangent,axis=1)[:,None]
 a=np.cross(tangent,[0,1,0]);a/=np.linalg.norm(a,axis=1)[:,None];b=np.cross(tangent,a)
 angles=np.arange(16)*2*math.pi/16
 vertices=(pts[:,None,:]+radius*(a[:,None,:]*np.cos(angles)[None,:,None]+b[:,None,:]*np.sin(angles)[None,:,None])).reshape((-1,3)).tolist();faces=[]
 for i in range(len(pts)-1):
  for k in range(16):
   x=i*16+k;y=i*16+(k+1)%16;faces.extend([(x,y,y+16),(x,y+16,x+16)])
 vertices.extend([pts[0],pts[-1]]);lo=len(vertices)-2;hi=lo+1
 for k in range(16):faces.extend([(lo,(k+1)%16,k),(hi,(len(pts)-1)*16+k,(len(pts)-1)*16+(k+1)%16)])
 q=trimesh.Trimesh(vertices,faces,process=True);q.fix_normals();assert q.is_watertight;return q

def build(wire_od=None,free_length=None):
 P=json.loads(Path(__file__).with_name('parameters.json').read_text());spec=P['stock_display_cable'];h=P['display_board_header']
 wire_od=wire_od or spec['modeled_wire_od_mm'];free_length=free_length or spec['free_length_mm'];radius=spec['display_u_bend_radius_mm']
 mating=P['display']['cable_mating'];exit_x=mating['wire_exit_x_mm'];axis_z=mating['axis_z_mm']
 board_x,board_y=P['display_connector'];wire_start_x=board_x-h['wire_exit_local_y_mm'];za=P['pcb_bottom_z']+P['pcb_thickness']+h['pin_axis_above_pcb_mm'];parts={};records=[]
 housing=box((6.85,17.8,4.5),(exit_x-6.85/2,0,axis_z))
 for i in range(8):housing-=box((6.95,1.4,2.8),(exit_x-6.85/2,-7+2*i,axis_z))
 parts['lcd-cable-screen-plug']=solid(housing)
 # SHR-08V-S-B boundary 11x5x2.8mm including grip protrusions. The
 # narrower inserted nose is an explicit nominal mating approximation.
 board_housing=box((2,9,2.8),(wire_start_x-1,board_y,za))
 board_housing+=box((1.3,11,2.8),(wire_start_x-.85,board_y,za))
 board_housing+=box((3.05,8,2.05),(wire_start_x-3.475,board_y,za+.025))
 contacts=[]
 for i,(signal,color) in enumerate(zip(SIGNALS,COLORS)):
  ya=board_y-3.5+i;yb=-7+2*i
  board_housing-=box((5.3,.7,1.4),(wire_start_x-2.5,ya,za+.3))
  t=np.linspace(0,1,360);f=10*t**3-15*t**4+6*t**5;lower_z=axis_z-2*radius
  bump=np.where(t<.75,np.sin(np.pi*np.minimum(t,.75)/.75)**2,0)
  theta=np.linspace(0,math.pi,150)
  arc=np.column_stack((exit_x+radius*np.sin(theta),np.full_like(theta,yb),lower_z+radius*(1-np.cos(theta))))
  def dressed(amplitude):
   sweep=np.column_stack((wire_start_x+(exit_x-wire_start_x)*t,ya+(yb-ya)*f,za+(lower_z-za)*f+amplitude*bump))
   return np.vstack((sweep,arc[1:]))
  lo,hi=0,10
  for _ in range(45):
   mid=(lo+hi)/2;path=dressed(mid);length=float(np.linalg.norm(np.diff(path,axis=0),axis=1).sum())
   if length<free_length:lo=mid
   else:hi=mid
  path=dressed((lo+hi)/2);length=float(np.linalg.norm(np.diff(path,axis=0),axis=1).sum());assert abs(length-free_length)<1e-5
  q=tube(path,wire_od/2);q.visual=trimesh.visual.ColorVisuals(q,vertex_colors=trimesh.visual.color.hex_to_rgba(color));parts['lcd-wire-'+signal.lower()]=q
  # Actual named crimp contacts are specified in WIRING.md. These closed
  # surfaces show their connection, not manufacturing geometry for tooling.
  contacts.append(solid_to_manifold(tube(path,.15)))
  contacts.append(box((5.7,.5,.5),(exit_x-5.7/2,yb,axis_z)))
  contacts.append(box((3.8,.5,.7),(wire_start_x-2.7,ya,za+.5))-box((2.5,.32,.42),(wire_start_x-3.45,ya,za+.5)))
  contacts.append(solid_to_manifold(tube(np.array([[wire_start_x+.02,ya,za],[wire_start_x-.65,ya,za],[wire_start_x-1.2,ya,za+.35],[wire_start_x-1.8,ya,za+.5]]),.15)))
  velocity=np.gradient(path,axis=0);acceleration=np.gradient(velocity,axis=0);cross=np.linalg.norm(np.cross(velocity,acceleration),axis=1);valid=cross>1e-9
  radii=np.linalg.norm(velocity[valid],axis=1)**3/cross[valid]
  records.append({'signal':signal,'color_illustration_only':color,'board_connector':'J6 JST SM08B-SRSS-TB(LF)(SN)','board_pin':i+1,'board_pad_mm':[board_x-2.0500086,ya,4.2],'board_end_wire_exit_mm':path[0].tolist(),'screen_housing_wire_exit_mm':path[-1].tolist(),'screen_pin':i+1,'modeled_free_wire_path_mm':round(length,3),'estimated_minimum_centerline_radius_mm':round(float(min(radii)),3),'centerline_mm':path.round(5).tolist()})
 parts['lcd-cable-board-sh-plug']=solid(board_housing)
 parts['lcd-cable-contacts']=solid(m.Manifold.batch_boolean(contacts,m.OpType.Add))
 assert len(parts['lcd-cable-contacts'].split())==8,'H1 must show eight separate continuous conductor/contact assemblies'
 report={'harness':'H1 custom crimped JST-SH8 to JST-PH8 display harness','included':False,'custom_harness_required':True,'board_connection':'J6 JST SM08B-SRSS-TB(LF)(SN) / C160407; mate SHR-08V-S-B with eight SSH-003T-P0.2-H contacts','display_connection':'Waveshare PH2.0 8-pin; mate PHR-8 with eight SPH-004T-P0.5S contacts','wire':spec['wire'],'wire_od_design_envelope_mm':wire_od,'free_length_between_rear_housing_exits_mm':free_length,'free_length_tolerance_mm':spec['free_length_tolerance_mm'],'display_U_bend_radius_mm':radius,'manufacturer_bend_radius':'Not supplied for this installed harness. Static dressed bends are engineering approximations requiring prototype trial-fit.','assembly':'Order one finished eight-conductor crimped harness. Pin1 to pin1 through pin8 to pin8 by connector circuit numbers, not by apparent face orientation. Wire free length 44+/-1mm between rear housing exits; cable maker adds termination allowances. No inline splices. The supplied kit lead is unused. Continuity and isolation check before power.','mating':mating,'board_mating':h,'connections':records,'scope':'Real mating MPNs, pitch and overall housing dimensions specified from JST drawings. Header uses original unscaled supplier STEP. Cable-housing stepped noses, contacts, seating datums, wire dressing and bends are nominal; actual fit and qualified crimps remain prototype checks.'}
 return parts,report
if __name__=='__main__':
 parts,report=build();Path(__file__).with_name('harness.json').write_text(json.dumps(report,indent=2)+'\n');print([(r['modeled_free_wire_path_mm'],r['estimated_minimum_centerline_radius_mm']) for r in report['connections']])
