#!/usr/bin/env python3
"""Import checked PCB copper as a guarded TSCircuit custom-router source asset.

Requires KiCad's matching pcbnew module and Shapely. Never edits compiled JSON.
"""
from pathlib import Path
import argparse,hashlib,json,subprocess
import pcbnew
from shapely.geometry import Point,Polygon
from shapely.ops import unary_union

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('board',type=Path)
parser.add_argument('--source',type=Path,required=True,help='Unrouted source placement circuit JSON')
parser.add_argument('--input',type=Path,required=True,help='Actual TSCircuit routing input SRJ')
parser.add_argument('--drc',type=Path,required=True,help='Fresh independent KiCad JSON DRC')
parser.add_argument('--output',type=Path,default=ROOT/'routing/verified.json')
args=parser.parse_args()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
drc=json.loads(args.drc.read_text())
assert not drc['violations'] and not drc['unconnected_items'],'Only clean copper may be stored'
cj=json.loads(args.source.read_text());b=pcbnew.LoadBoard(str(args.board));assert b
source_ports={p['source_port_id']:p for p in cj if p['type']=='source_port'}
components={c['source_component_id']:c['name'] for c in cj if c['type']=='source_component'}
ports={(components[source_ports[p['source_port_id']]['source_component_id']],str(source_ports[p['source_port_id']]['pin_number'])):p for p in cj if p['type']=='pcb_port'}
nets={n['name']:n['source_net_id'] for n in cj if n['type']=='source_net'}
canonical={}
for name,nid in nets.items():
 candidates=[t for t in cj if t['type']=='source_trace' and nid in t.get('connected_source_net_ids',[])]
 assert candidates,('No source trace representing net',name)
 canonical[name]=min(candidates,key=lambda t:t.get('max_length',float('inf')) if 'max_length' in t else -1)['source_trace_id']
net_for_port={}
parent={}
def root(x):
 parent.setdefault(x,x)
 if parent[x]!=x:parent[x]=root(parent[x])
 return parent[x]
for t in [t for t in cj if t['type']=='source_trace']:
 ids=t.get('connected_source_port_ids',[])+t.get('connected_source_net_ids',[])
 for p in ids[1:]:parent[root(p)]=root(ids[0])
for pid in source_ports:
 names=[name for name,nid in nets.items() if root(pid)==root(nid)]
 assert len(names)<=1,('Source net short',pid,names)
 net_for_port[pid]=names[0] if names else ''
pads=[];checked=set()
for f in b.GetFootprints():
 for p in f.Pads():
  if not p.GetNumber():continue
  key=(f.GetReference(),p.GetNumber());port=ports[key];q=p.GetPosition()
  assert abs(q.x/1e6-100-port['x'])<.0002 and abs(q.y/1e6-100+port['y'])<.0002,('Pad moved',key)
  assert p.GetNetname()==net_for_port[port['source_port_id']],('Pad net differs',key,p.GetNetname())
  checked.add(key)
  for layer in [pcbnew.F_Cu,pcbnew.B_Cu]:
   if not p.IsOnLayer(layer):continue
   shape=p.GetEffectivePolygon(layer);outlines=[]
   for i in range(shape.OutlineCount()):
    ring=shape.Outline(i);outlines.append(Polygon([(ring.CPoint(j).x/1e6,ring.CPoint(j).y/1e6) for j in range(ring.PointCount())]))
   pads.append((p.GetNetname(),layer,port['pcb_port_id'],unary_union(outlines)))
assert checked==set(ports),'Every physical source port must be present'
def xy(q):return {'x':round(q.x/1e6-100,9),'y':round(100-q.y/1e6,9)}
traces=[]
for t in sorted(b.GetTracks(),key=lambda t:(t.GetNetname(),t.GetLayer(),t.GetStart().x,t.GetStart().y,t.GetEnd().x,t.GetEnd().y,type(t).__name__)):
 net=t.GetNetname();assert net in nets
 if isinstance(t,pcbnew.PCB_VIA):
  q=xy(t.GetPosition());route=[{'route_type':'wire',**q,'width':.15,'layer':'top'},
   {'route_type':'via',**q,'from_layer':'top','to_layer':'bottom','via_diameter':t.GetWidth(pcbnew.F_Cu)/1e6,'via_hole_diameter':t.GetDrillValue()/1e6},
   {'route_type':'wire',**q,'width':.15,'layer':'bottom'}];connected=[]
 else:
  if t.GetStart()==t.GetEnd():continue
  width=t.GetWidth()/1e6;layer=t.GetLayer();route=[];connected=[]
  for i,q in enumerate([t.GetStart(),t.GetEnd()]):
   point=Point(q.x/1e6,q.y/1e6);contacts=[pid for n,l,pid,g in pads if n==net and l==layer and g.buffer(width/2+.000002).covers(point)]
   record={'route_type':'wire',**xy(q),'width':width,'layer':'top' if layer==pcbnew.F_Cu else 'bottom'}
   if contacts:record['start_pcb_port_id' if i==0 else 'end_pcb_port_id']=contacts[0]
   route.append(record);connected+=contacts
 traces.append({'type':'pcb_trace','pcb_trace_id':'pcb_trace_external_'+str(len(traces)),'source_trace_id':canonical[net],'connection_name':nets[net],'route':route,'connectsTo':sorted(set(connected))})
signature=subprocess.check_output(['bun',str(ROOT/'routing/input-signature.ts'),str(args.input)],text=True,cwd=ROOT).strip()
metadata={'input_signature':signature,'verification_status':'independent PCB DRC passed; repeat source build, shorts and fabrication export checks','generator':'KiCad 10 / Freerouting 2.5.0 and checked local routing','source_placement_sha256':sha(args.source),'routing_input_sha256':sha(args.input),'verified_board_sha256':sha(args.board),'independent_drc_sha256':sha(args.drc),'physical_pads_verified':len(checked)}
header=json.dumps(metadata,indent=2)[:-1].rstrip()
args.output.write_text(header+',\n  "traces": [\n'+',\n'.join('    '+json.dumps(t,separators=(',',':')) for t in traces)+'\n  ]\n}\n')
print(f'Stored {len(traces)} copper segments/vias with {len(checked)} matching physical ports and input guard {signature}.')
