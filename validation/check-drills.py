#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Check annuli and keep via drills out of SMT paste."""
from pathlib import Path
import argparse,hashlib,json,math
import pcbnew
from shapely.geometry import Point,Polygon
from shapely.ops import unary_union

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('board',type=Path)
parser.add_argument('output',type=Path)
args=parser.parse_args();b=pcbnew.LoadBoard(str(args.board));assert b
component=[];paste=[]
for f in b.GetFootprints():
 for p in f.Pads():
  drill=p.GetDrillSize()
  if p.GetNumber() and drill.x:
   size=p.GetSize();ring=min(size.x-drill.x,size.y-drill.y)/2e6
   assert ring>=.18-1e-6,(f.GetReference(),p.GetNumber(),ring)
   component.append({'reference':f.GetReference(),'pin':p.GetNumber(),'minimum_annulus_mm':ring})
  if p.GetAttribute()!=pcbnew.PAD_ATTRIB_SMD:continue
  for layer in [pcbnew.F_Paste,pcbnew.B_Paste]:
   if not p.IsOnLayer(layer):continue
   shape=p.GetEffectivePolygon(layer);out=[]
   for i in range(shape.OutlineCount()):
    ring=shape.Outline(i);out.append(Polygon([(ring.CPoint(j).x/1e6,ring.CPoint(j).y/1e6) for j in range(ring.PointCount())]))
   if out:paste.append((f.GetReference()+'.'+p.GetNumber(),unary_union(out)))
assert len(paste)>=212,('Missing SMT paste geometry',len(paste))
vias=[];minimum=math.inf
for t in b.GetTracks():
 if not isinstance(t,pcbnew.PCB_VIA):continue
 diameter=t.GetWidth(pcbnew.F_Cu)/1e6;drill=t.GetDrillValue()/1e6
 assert any(abs(diameter-d)<1e-6 and abs(drill-h)<1e-6 for d,h in [(.6,.3),(.5,.2)]),(diameter,drill)
 ring=(diameter-drill)/2;assert ring>=.15-1e-6
 q=t.GetPosition();point=Point(q.x/1e6,q.y/1e6)
 clearance=min(point.distance(g)-drill/2 for _,g in paste)
 assert clearance>=.001,('Via drill intersects SMT solder paste',point,clearance)
 minimum=min(minimum,clearance);vias.append({'x_mm':q.x/1e6,'y_mm':q.y/1e6,'diameter_mm':diameter,'drill_mm':drill,'annulus_mm':ring})
assert len(component)==10
report={'status':'pass','board_sha256':hashlib.sha256(args.board.read_bytes()).hexdigest(),'component_plated_pads':component,'SMT_paste_apertures_checked':len(paste),'routing_vias':vias,'minimum_via_annulus_mm':min(v['annulus_mm'] for v in vias),'minimum_via_drill_to_SMT_paste_clearance_mm':minimum,'via_in_pad_process_required':False}
args.output.write_text(json.dumps(report,indent=2)+'\n')
print(f'Drills passed: {len(component)} component holes, {len(vias)} vias, ≥0.15mm via annuli, no via drills in SMT paste.')
