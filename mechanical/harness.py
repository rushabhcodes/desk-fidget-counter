# SPDX-License-Identifier: MIT
"""Supplied Waveshare cable, shortened and soldered at J6; original PH plug retained."""
import math,json
from pathlib import Path
import numpy as np,trimesh,manifold3d as m
SIGNALS=['BL','RST','DC','CS','CLK','DIN','GND','VCC']
COLORS=['#b45cce','#ffffff','#ee9b34','#e4d751','#528cdd','#59ac70','#222c38','#e45555']
WIRE_OD=1.0 # Design envelope only; Waveshare does not publish the supplied wire OD.
RADIUS=6.2 # exceeds 10 x maximum insulation OD

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

def build():
 P=json.loads(Path(__file__).with_name('parameters.json').read_text())
 parts={};records=[]
 # Keep the original PH2.0 display plug. Stock wire dimensions are unpublished;
 # the model uses explicit fit envelopes, not a claim about its manufacturer.
 housing=box((4.5,17.8,6.85),(8.2,0,12.725))
 for i in range(8):housing-=box((2.8,1.4,6.95),(8.2,-7+2*i,12.725))
 parts['lcd-cable-screen-plug']=solid(housing)
 contacts=[]
 for i,(signal,color) in enumerate(zip(SIGNALS,COLORS)):
  ya=P['display_connector'][1]-8.89+2.54*i;yb=-7+2*i
  # 2mm dressing bend above the solder joint, then a smooth fan into the window.
  theta=np.linspace(0,math.pi/2,36)
  q=theta/(math.pi/2);side=10*q**3-15*q**4+6*q**5
  lead=np.column_stack((-21.5+2*(1-np.cos(theta)),ya+side,5.2+2*np.sin(theta)))
  t=np.linspace(0,1,130);f=10*t**3-15*t**4+6*t**5
  sweep=np.column_stack((-19.5+21.5*t,ya+1+(yb-ya-1)*f,7.2-4.1*f))
  theta=np.linspace(0,math.pi/2,70)
  arc=np.column_stack((2+RADIUS*np.sin(theta),np.full_like(theta,yb),9.3-RADIUS*np.cos(theta)))
  path=np.vstack((lead,sweep[1:],arc[1:]))
  length=float(np.linalg.norm(np.diff(path,axis=0),axis=1).sum())
  q=tube(path,WIRE_OD/2);q.visual=trimesh.visual.ColorVisuals(q,vertex_colors=trimesh.visual.color.hex_to_rgba(color));parts['lcd-wire-'+signal.lower()]=q
  # Bare conductor/solder geometry is illustrative, inside the actual plated hole.
  contacts.append(m.Manifold.cylinder(3.4,.16,.16,24).translate((-21.5,ya,1.8)))
  contacts.append(box((.5,.5,5.7),(8.2,yb,12.15)))
  records.append({'signal':signal,'color_illustration_only':color,'board_connector':'J6 solder pad','board_pin':8-i,'board_pad_mm':[-21.5,ya,4.2],'insulation_start_mm':path[0].tolist(),'screen_housing_wire_exit_mm':path[-1].tolist(),'screen_pin':i+1,'modeled_insulated_wire_length_mm':round(length,3),'centerline_mm':path.round(5).tolist()})
 parts['lcd-cable-contacts']=solid(m.Manifold.batch_boolean(contacts,m.OpType.Add))
 report={'harness':'Original cable included with Waveshare 19192; shortened at its jumper end','included':True,'custom_harness_required':False,'board_connection':'Direct soldered through J6; optional 2.54mm male header NOT populated','housing':'Original PH2.0 8-pin display plug retained','wire':'Original included wires; no replacement wire or crimp contacts purchased','wire_od_design_envelope_mm':WIRE_OD,'nominal_dressing_bend_radius_mm':2.0,'manufacturer_bend_radius':'Unpublished; fit must be measured; no bend qualification claimed','trim_instruction':'Trial-route supplied lead; target about 35.5mm insulated span from PH housing back, plus 3.4mm stripped board end. Trim each wire to its actual dressed path; solder tails <=0.8mm below PCB. Do not cut the PH plug off.','screen_pose':'180deg about Y from official STEP, plus Z17.75mm; tab points -X','connections':records,'scope':'Cable type and 20cm package length verified on Waveshare product page/photo. Plug is a PH nominal envelope; supplier does not publish wire OD, contact microgeometry or free-wire dimensions. These design-envelope CAD checks do not establish physical fit. Verify actual supplied cable, dressed bends, pull/strain relief, continuity and stock plug revision before fabrication/assembly signoff.'}
 return parts,report
if __name__=='__main__':
 parts,report=build();out=Path(__file__).resolve().parent/'harness.json';out.write_text(json.dumps(report,indent=2)+'\n');print([r['modeled_insulated_wire_length_mm'] for r in report['connections']])
