# SPDX-License-Identifier: MIT
"""JST PH8 static LCD harness: real pitch, housing sizes and bounded wire bends."""
import math,json
from pathlib import Path
import numpy as np,trimesh,manifold3d as m
SIGNALS=['BL','RST','DC','CS','CLK','DIN','GND','VCC']
COLORS=['#ffffff','#b45cce','#ee9b34','#e4d751','#528cdd','#59ac70','#222c38','#e45555']
WIRE_OD=.6096 # Alpha 2840/7: nominal .022in, upper tolerance .024in
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
 parts={};records=[]
 # PHR-8 nominal housing, 17.8 wide x 4.5 cross-section x 6.85 long.
 housing=box((17.8,6.85,4.5),(0,-4.825,2.4))
 for i in range(8):housing-=box((1.4,6.95,2.8),(-7+2*i,-4.825,2.4))
 q=solid(housing);q.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[0,0,1]));q.apply_translation([-19.5,-3.5,4.2]);parts['lcd-cable-board-plug']=q
 housing=box((4.5,17.8,6.85),(8.2,0,12.725))
 for i in range(8):housing-=box((2.8,1.4,6.95),(8.2,-7+2*i,12.725))
 parts['lcd-cable-screen-plug']=solid(housing)
 contacts=[]
 for i,(signal,color) in enumerate(zip(SIGNALS,COLORS)):
  ya=-10.5+2*i;yb=-7+2*i
  t=np.linspace(0,1,100);f=10*t**3-15*t**4+6*t**5
  s=np.column_stack((-11.25+13.25*t,ya+(yb-ya)*f,6.6-3.5*f))
  theta=np.linspace(0,math.pi/2,60);arc=np.column_stack((2+RADIUS*np.sin(theta),np.full_like(theta,yb),9.3-RADIUS*np.cos(theta)))
  path=np.vstack((s,arc[1:]))
  length=float(np.linalg.norm(np.diff(path,axis=0),axis=1).sum())
  q=tube(path,WIRE_OD/2);q.visual=trimesh.visual.ColorVisuals(q,vertex_colors=trimesh.visual.color.hex_to_rgba(color));parts['lcd-wire-'+signal.lower()]=q
  # Metal contact nominal 5.7mm length. Spring/crimp microgeometry omitted.
  contacts.append(box((5.7,.5,.5),(-14.1,ya,6.6)))
  contacts.append(box((.5,.5,5.7),(8.2,yb,12.15)))
  records.append({'pin':i+1,'signal':signal,'color':color,'board_connector':'J6','board_pad_mm':[-19.5,ya,4.2],'board_housing_wire_exit_mm':path[0].tolist(),'screen_housing_wire_exit_mm':path[-1].tolist(),'screen_pin':i+1,'free_wire_centerline_length_mm':round(length,3),'centerline_mm':path.round(5).tolist()})
 parts['lcd-cable-contacts']=solid(m.Manifold.batch_boolean(contacts,m.OpType.Add))
 # Analytical radius of the quintic S-bend; circular segment radius is exact.
 t=np.linspace(0,1,1001);fp=30*t*t-60*t**3+30*t**4;fpp=60*t-180*t*t+120*t**3
 d=np.column_stack((np.full_like(t,13.25),3.5*fp,-3.5*fp));dd=np.column_stack((t*0,3.5*fpp,-3.5*fpp));cross=np.linalg.norm(np.cross(d,dd),axis=1);r=np.divide(np.linalg.norm(d,axis=1)**3,cross,out=t*0+999,where=cross>0)
 report={'housing':'2 x JST PHR-8','contacts':'16 x JST SPH-004T-P0.5S','wire':'Alpha Wire 2840/7, 32AWG stranded PTFE, eight colours','maximum_wire_od_mm':WIRE_OD,'required_bend_radius_mm':WIRE_OD*10,'minimum_modeled_bend_radius_mm':round(min(r.min(),RADIUS),4),'free_wire_length_spec_mm':'24.5 +/- 0.5; between housing wire exits, not including termination allowance','screen_pose':'180deg about Y from official STEP, plus Z17.75mm; tab points -X','connections':records,'scope':'Nominal static routing; termination microgeometry simplified. Verify connector revision, crimp pull strength and service slack on the first physical assembly.'}
 assert report['minimum_modeled_bend_radius_mm']>=report['required_bend_radius_mm']
 return parts,report
if __name__=='__main__':
 parts,report=build();out=Path(__file__).resolve().parent/'harness.json';out.write_text(json.dumps(report,indent=2)+'\n');print(report['connections'][0]['free_wire_centerline_length_mm'],report['minimum_modeled_bend_radius_mm'])
