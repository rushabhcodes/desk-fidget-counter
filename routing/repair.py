#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Clearance-aware two-layer A* repair of frozen paths.
Uses the reviewed router input and existing copper as obstacles. Run from repo
root with numpy/shapely; independent KiCad DRC and tscircuit checks are required.
"""
import json, math, heapq, sys
from pathlib import Path
import numpy as np
from shapely.geometry import box, Point, LineString
from shapely.ops import unary_union
from shapely import contains_xy
s=json.loads(Path('routing/input.json').read_text())
p=Path('routing/routes.json');saved=json.loads(p.read_text());routes=saved['traces']
STEP=.05;LO=-32;SIZE=1281
pending=set(sys.argv[1:])
xx,yy=np.meshgrid(LO+np.arange(SIZE)*STEP,LO+np.arange(SIZE)*STEP)

def repair(name):
 target=next(r for r in routes if r['pcb_trace_id']==name)
 net=target['connection_name'];width=.25 if net in ['source_net_2','source_net_3','source_net_4'] else .1
 ids={net}
 for _ in range(8):
  for o in s['obstacles']:
   if ids.intersection(o.get('connectedTo',[])):ids.update(o['connectedTo'])
 shapes=[[],[]];via_shapes=[]
 for o in s['obstacles']:
  x,y=o['center']['x'],o['center']['y'];w,h=o['width'],o['height'];g=box(x-w/2,y-h/2,x+w/2,y+h/2)
  is_pad=any(k in o.get('circuitJsonMetadata',{}) for k in ['pcb_smtpad_id','pcb_plated_hole_id'])
  if is_pad:via_shapes.append(g.buffer(.51))
  if ids.intersection(o.get('connectedTo',[])):continue
  for i,l in enumerate(['top','bottom']):
   if l in o['layers']:shapes[i].append(g.buffer(.16+width/2))
  via_shapes.append(g.buffer(.51))
 for r in routes:
  if r is target or r['pcb_trace_id'] in pending:continue
  same=r['connection_name']==net
  for a,b in zip(r['route'],r['route'][1:]):
   if a['route_type']==b['route_type']=='wire' and a['layer']==b['layer'] and not same:
    g=LineString([(a['x'],a['y']),(b['x'],b['y'])]);w=max(a['width'],b['width'])
    shapes[0 if a['layer']=='top' else 1].append(g.buffer(w/2+.16+width/2));via_shapes.append(g.buffer(w/2+.51))
  for a in r['route']:
   if a['route_type']=='via':
    g=Point(a['x'],a['y']);via_shapes.append(g.buffer(.82 if same else .87))
    if not same:
     for i in range(2):shapes[i].append(g.buffer(.35+.16+width/2))
 geoms=[unary_union(v) for v in shapes];blocked=[contains_xy(g,xx,yy) for g in geoms]
 for l in range(2):blocked[l]|=xx*xx+yy*yy>(32-.31-width/2)**2
 vb=contains_xy(unary_union(via_shapes),xx,yy)|(xx*xx+yy*yy>(32-.66)**2)
 def node(pt):return(round((pt['x']-LO)/STEP),round((pt['y']-LO)/STEP),0 if pt['layer']=='top' else 1)
 anchor={'source_net_11_mst1_0':6,'source_net_17_mst0_0':5}.get(name,0)
 prefix=target['route'][:anchor]
 a,b=target['route'][anchor],target['route'][-1];assert a['route_type']==b['route_type']=='wire'
 start,goal=node(a),node(b)
 for label,n in [('start',start),('goal',goal)]:assert not blocked[n[2]][n[1],n[0]],(name,label,'obstructed',n)
 def h(n):return math.hypot(n[0]-goal[0],n[1]-goal[1])+(0 if n[2]==goal[2] else 50)
 q=[(h(start),0,start)];cost={start:0};prev={}
 while q:
  _,c,u=heapq.heappop(q)
  if c!=cost[u]:continue
  if u==goal:break
  x,y,l=u;nbr=[]
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
   nx,ny=x+dx,y+dy
   if not (0<=nx<SIZE and 0<=ny<SIZE) or blocked[l][ny,nx]:continue
   if dx and dy and (blocked[l][y,nx] or blocked[l][ny,x]):continue
   nbr.append(((nx,ny,l),math.hypot(dx,dy)))
  if not vb[y,x] and not blocked[1-l][y,x]:nbr.append(((x,y,1-l),70))
  for v,dc in nbr:
   nc=c+dc
   if nc<cost.get(v,1e100):cost[v]=nc;prev[v]=u;heapq.heappush(q,(nc+h(v),nc,v))
 else:raise RuntimeError((name,'no path',len(cost)))
 path=[goal]
 while path[-1]!=start:path.append(prev[path[-1]])
 path.reverse();pts=[path[0]]
 for a1,b1,c1 in zip(path,path[1:],path[2:]):
  if a1[2]!=b1[2] or b1[2]!=c1[2] or (b1[0]-a1[0],b1[1]-a1[1])!=(c1[0]-b1[0],c1[1]-b1[1]):pts.append(b1)
 pts.append(path[-1]);out=[]
 for i,(x,y,l) in enumerate(pts):
  gx,gy=round(LO+x*STEP,5),round(LO+y*STEP,5)
  if i and pts[i-1][:2]==(x,y) and pts[i-1][2]!=l:
   out.append({'route_type':'via','x':gx,'y':gy,'from_layer':['top','bottom'][pts[i-1][2]],'to_layer':['top','bottom'][l],'via_diameter':.7,'via_hole_diameter':.3})
  out.append({'route_type':'wire','x':gx,'y':gy,'width':width,'layer':['top','bottom'][l]})
 out[0]['x'],out[0]['y']=a['x'],a['y'];out[-1]['x'],out[-1]['y']=b['x'],b['y']
 for a1,b1 in zip(out,out[1:]):
  if a1['route_type']==b1['route_type']=='wire' and a1['layer']==b1['layer']:
   assert not LineString([(a1['x'],a1['y']),(b1['x'],b1['y'])]).intersects(geoms[0 if a1['layer']=='top' else 1]),(name,'clearance at endpoint')
 target['route']=prefix+out
 p.write_text(json.dumps(saved,separators=(',',':'))+'\n')
 print(name,len(out),'points',sum(pt['route_type']=='via' for pt in out),'vias',flush=True)
for name in sys.argv[1:]:
 repair(name);pending.remove(name)
