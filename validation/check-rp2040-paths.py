#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Measure actual connected copper, including via metal contacts and pad centroids.
from pathlib import Path
import pcbnew,json,math,heapq,sys,hashlib
from shapely.geometry import Polygon,LineString,Point
b=pcbnew.LoadBoard(sys.argv[1]);assert b,'Load a source-derived KiCad board';parts={f.GetReference():{p.GetNumber():p for p in f.Pads() if p.GetNumber()} for f in b.GetFootprints() if f.GetReference()}
checks=[('1','C7',6),('10','C8',6),('22','C9',6),('33','C10',6),('42','C11',6),('49','C12',6),('43','C13',6),('48','C17',6),('50','C18',6),('23','C19',6),('44','C20',7),('45','C21',7)]
checks=[('U1',pin,cap,'1',budget) for pin,cap,budget in checks]+[('U8','8','C22','1',8),('U7','5','C14','1',6)]
def xy(q):return (q.x/1e6,q.y/1e6)
def poly(p,layer):
 a=p.GetEffectivePolygon(layer);rings=[]
 for i in range(a.OutlineCount()):
  chain=a.Outline(i);rings.append(Polygon([xy(chain.CPoint(j)) for j in range(chain.PointCount())]))
 from shapely.ops import unary_union
 return unary_union(rings)
cache={}
def graph(net):
 if net in cache:return cache[net]
 adj={};segments=[];pads={};vias=[]
 def add(a,c,w,width,via=0):
  adj.setdefault(a,[]).append((c,w,width,via));adj.setdefault(c,[]).append((a,w,width,via))
 for t in b.GetTracks():
  if t.GetNetCode()!=net:continue
  if isinstance(t,pcbnew.PCB_VIA):
   x,y=xy(t.GetPosition());add((0,x,y),(pcbnew.B_Cu,x,y),0,t.GetWidth(pcbnew.F_Cu)/1e6,1);vias.append((x,y,t.GetWidth(pcbnew.F_Cu)/1e6))
  else:
   x,y=xy(t.GetStart());u,v=xy(t.GetEnd());layer=t.GetLayer();a=(layer,x,y);c=(layer,u,v);add(a,c,t.GetLength()/1e6,t.GetWidth()/1e6);segments.append((a,c,t.GetWidth()/1e6,LineString([(x,y),(u,v)])))
 # Via metal can touch a track beside its centre, not just at the centre.
 for x,y,diameter in vias:
  for a,c,width,line in segments:
   pt=Point(x,y)
   if line.distance(pt)<=diameter/2+width/2+.000002:
    q=line.interpolate(line.project(pt));n=(a[0],x,y)
    add(n,a,pt.distance(q)+q.distance(Point(a[1:])),width)
    add(n,c,pt.distance(q)+q.distance(Point(c[1:])),width)
 # Join T-junction endpoints to the middle of existing same-net segments.
 nodes=list(adj)
 for a,c,width,line in segments:
  for n in nodes:
   if n[0]!=a[0] or n in [a,c]:continue
   pt=Point(n[1:])
   if line.distance(pt)<.000002:
    add(a,n,math.dist(a[1:],n[1:]),width);add(c,n,math.dist(c[1:],n[1:]),width)
 for ref,pp in parts.items():
  for number,p in pp.items():
   if p.GetNetCode()!=net:continue
   centre=xy(p.GetPosition());key=('pad',ref,number);pads[(ref,number)]=key;adj.setdefault(key,[])
   for layer in [pcbnew.F_Cu,pcbnew.B_Cu]:
    if not p.IsOnLayer(layer):continue
    shape=poly(p,layer)
    for a,c,width,line in segments:
     if a[0]!=layer or not shape.buffer(width/2+.000002).intersects(line):continue
     closest=line.interpolate(line.project(Point(centre)));q=(closest.x,closest.y)
     add(key,a,math.dist(centre,q)+math.dist(q,a[1:]),width);add(key,c,math.dist(centre,q)+math.dist(q,c[1:]),width)
 cache[net]=(adj,pads);return adj,pads
result=[]
for ref,pin,cap,capPin,budget in checks:
 p=parts[ref][pin];q=parts[cap][capPin];assert p.GetNetCode()==q.GetNetCode()
 adj,pads=graph(p.GetNetCode());start=pads[(ref,pin)];end=pads[(cap,capPin)];queue=[(0,0,start,.99,0)];dist={start:0};answer=None;serial=0
 while queue:
  cost,_,n,width,vias=heapq.heappop(queue)
  if cost>dist.get(n,math.inf):continue
  if n==end:answer=(cost,width,vias);break
  for nxt,delta,w,via in adj[n]:
   new=cost+delta
   if new+1e-9<dist.get(nxt,math.inf):
    dist[nxt]=new;serial+=1;heapq.heappush(queue,(new,serial,nxt,min(width,w),vias+via))
 assert answer is not None,(ref,pin,cap,'unconnected bypass')
 assert answer[0]<=budget,(ref,pin,cap,'bypass path too long',answer,budget)
 assert answer[1]>=.15-1e-6,(ref,pin,cap,'bypass neck-down below 0.15mm',answer)
 assert answer[2]<=(2 if cap in ['C17','C21'] else 0),(ref,pin,cap,'unexpected bypass via count',answer)
 record={'from':ref+'.'+pin,'to':cap+'.'+capPin,'budget_mm':budget,'length_mm':round(answer[0],4) if answer else None,'minimum_track_width_mm':round(answer[1],4) if answer else None,'vias':answer[2] if answer else None};result.append(record);print(record,flush=True)
signals=[]
for name in ['XIN','XOUT','XTAL_OUT','QSPI_SS','QSPI_SCLK','QSPI_SD0','QSPI_SD1','QSPI_SD2','QSPI_SD3','USB_DM_MCU','USB_DP_MCU']:
 ts=[t for t in b.GetTracks() if t.GetNetname()==name]
 length=sum(t.GetLength()/1e6 for t in ts if not isinstance(t,pcbnew.PCB_VIA))
 vias=sum(isinstance(t,pcbnew.PCB_VIA) for t in ts)
 assert length <= (10 if name in ['XIN','XOUT','XTAL_OUT'] else 20 if name.startswith('USB_') else 25),(name,'excess local signal copper',length)
 if name in ['XIN','XOUT','XTAL_OUT']:assert vias==0,(name,'oscillator must remain on top copper')
 signals.append({'net':name,'total_copper_length_mm':round(length,4),'via_count':vias})
 print(name,'track length',round(sum(t.GetLength()/1e6 for t in ts if not isinstance(t,pcbnew.PCB_VIA)),3),'vias',sum(isinstance(t,pcbnew.PCB_VIA) for t in ts),flush=True)
report={'status':'pass','board_sha256':hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest(),'source_circuit_sha256':hashlib.sha256(Path('dist/index/circuit.json').read_bytes()).hexdigest(),'note':'Limits are project engineering budgets; physical bring-up and signal integrity still require a prototype. Lengths are planar routed copper including pad centroids.','bypasses':result,'local_signals':signals}
Path(sys.argv[2]).write_text(json.dumps(report,indent=2)+'\n')
