# SPDX-License-Identifier: MIT
"""Supplied Waveshare cable, shortened and soldered at J6; original PH plug retained."""
import math,json
from pathlib import Path
import numpy as np,trimesh,manifold3d as m
SIGNALS=['BL','RST','DC','CS','CLK','DIN','GND','VCC']
COLORS=['#b45cce','#ffffff','#ee9b34','#e4d751','#528cdd','#59ac70','#222c38','#e45555']
WIRE_OD=1.2 # User-authorized best approximation; clearance is also checked at 1.5mm.
RADIUS=4.7 # Static U bend; engineering estimate, not a cable supplier rating.

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

def build(wire_od=None):
 P=json.loads(Path(__file__).with_name('parameters.json').read_text())
 wire_od=wire_od or P['stock_display_cable']['modeled_wire_od_mm']
 bend=P['stock_display_cable']['dressing_bend_radius_mm']
 start_z=P['pcb_bottom_z']+P['pcb_thickness']+P['stock_display_cable']['insulation_start_above_pcb_mm']
 shift_y=P['stock_display_cable']['lead_y_shift_mm']
 parts={};records=[]
 # Keep the original PH2.0 display plug. Stock wire dimensions are unpublished;
 # the model uses explicit fit envelopes, not a claim about its manufacturer.
 connector=P['display']['cable_mating']
 exit_x=connector['wire_exit_x_mm'];axis_z=connector['axis_z_mm']
 # PHR-8 envelope turned sideways: the long axis of insertion is X, parallel
 # to the screen PCB. The Waveshare STEP models only a solid socket envelope.
 housing=box((6.85,17.8,4.5),(exit_x-6.85/2,0,axis_z))
 for i in range(8):housing-=box((6.95,1.4,2.8),(exit_x-6.85/2,-7+2*i,axis_z))
 parts['lcd-cable-screen-plug']=solid(housing)
 contacts=[]
 for i,(signal,color) in enumerate(zip(SIGNALS,COLORS)):
  ya=P['display_connector'][1]-8.89+2.54*i;yb=-7+2*i
  # Gentler estimated static bend above the solder joint; no flexing in use.
  theta=np.linspace(0,math.pi/2,36)
  q=theta/(math.pi/2);side=10*q**3-15*q**4+6*q**5
  lead=np.column_stack((-21.5+bend*(1-np.cos(theta)),ya+shift_y*side,start_z+bend*np.sin(theta)))
  t=np.linspace(0,1,130);f=10*t**3-15*t**4+6*t**5
  lower_z=axis_z-2*RADIUS
  sweep=np.column_stack((-21.5+bend+(exit_x+21.5-bend)*t,ya+shift_y+(yb-ya-shift_y)*f,start_z+bend-(start_z+bend-lower_z)*f))
  theta=np.linspace(0,math.pi,100)
  arc=np.column_stack((exit_x+RADIUS*np.sin(theta),np.full_like(theta,yb),lower_z+RADIUS*(1-np.cos(theta))))
  path=np.vstack((lead,sweep[1:],arc[1:]))
  length=float(np.linalg.norm(np.diff(path,axis=0),axis=1).sum())
  radii=[]
  for curve in [lead,sweep,arc]:
   velocity=np.gradient(curve,axis=0);acceleration=np.gradient(velocity,axis=0)
   cross=np.linalg.norm(np.cross(velocity,acceleration),axis=1)
   valid=cross>1e-10
   radii.extend((np.linalg.norm(velocity[valid],axis=1)**3/cross[valid]).tolist())
  q=tube(path,wire_od/2);q.visual=trimesh.visual.ColorVisuals(q,vertex_colors=trimesh.visual.color.hex_to_rgba(color));parts['lcd-wire-'+signal.lower()]=q
  # Bare conductor/solder geometry is illustrative, inside the actual plated hole.
  contacts.append(m.Manifold.cylinder(start_z-1.8,.16,.16,24).translate((-21.5,ya,1.8)))
  contacts.append(box((5.7,.5,.5),(exit_x-5.7/2,yb,axis_z)))
  records.append({'signal':signal,'color_illustration_only':color,'board_connector':'J6 solder pad','board_pin':8-i,'board_pad_mm':[-21.5,ya,4.2],'insulation_start_mm':path[0].tolist(),'screen_housing_wire_exit_mm':path[-1].tolist(),'screen_pin':i+1,'modeled_insulated_wire_length_mm':round(length,3),'estimated_minimum_centerline_radius_mm':round(min(radii),3),'centerline_mm':path.round(5).tolist()})
 parts['lcd-cable-contacts']=solid(m.Manifold.batch_boolean(contacts,m.OpType.Add))
 report={'harness':'Original cable included with Waveshare 19192; shortened at its jumper end','included':True,'custom_harness_required':False,'board_connection':'Direct soldered through J6; optional 2.54mm male header NOT populated','housing':'Original PH2.0 8-pin display plug retained; side entry parallel to screen PCB','wire':'Original included wires; no replacement wire or crimp contacts purchased','wire_od_design_envelope_mm':wire_od,'nominal_dressing_bend_radius_mm':bend,'display_U_bend_radius_mm':RADIUS,'manufacturer_bend_radius':'Unpublished; static bends are user-authorized engineering approximations, not supplier ratings','trim_instruction':'Trial-route supplied lead with its plug mated sideways before lowering the screen. Trim each wire to its actual dressed path, leaving assembly slack, plus 2.55mm stripped board end; solder tails <=0.8mm below PCB. Keep the original PH display plug.','screen_pose':'180deg about Y from official STEP, plus Z17.75mm; tab points -X','mating':connector,'connections':records,'scope':'Cable type and 20cm package length verified on Waveshare product page/photo. PHR-8 nominal envelope from JST PH drawing; Waveshare does not specify the exact connector maker or seated plug datum. Mating axis/seating, wire OD and static bends use explicit engineering estimates. The nominal model is 1.2mm OD; larger 1.5mm wire clearance is checked separately.'}
 return parts,report
if __name__=='__main__':
 parts,report=build();out=Path(__file__).resolve().parent/'harness.json';out.write_text(json.dumps(report,indent=2)+'\n');print([r['modeled_insulated_wire_length_mm'] for r in report['connections']])
