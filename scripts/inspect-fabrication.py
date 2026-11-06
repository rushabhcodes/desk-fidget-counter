#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Independently parse the plotted Gerber/Excellon files.
uv run --with gerbonara==1.5.0 --with cairosvg==2.8.2 scripts/inspect-fabrication.py
"""
from pathlib import Path
from collections import Counter
import csv,json
from gerbonara import LayerStack
from gerbonara.utils import Tag
import cairosvg
ROOT=Path(__file__).resolve().parents[1]
s=LayerStack.open(ROOT/'manufacturing/gerbers')
cj=json.loads((ROOT/'dist/index/circuit.json').read_text())
assert set(s.graphic_layers)=={(side,use) for side in ['top','bottom'] for use in ['copper','mask','silk','paste']}|{('mechanical','outline')}
assert s.drill_pth is not None and s.drill_npth is not None
pth=Counter(type(o).__name__ for o in s.drill_pth.objects)
npth=Counter(round(o.aperture.diameter,3) for o in s.drill_npth.objects)
assert pth['Line']==4,'USB must have four routed plated shield slots'
assert npth==Counter({2.7:4,.6:2}),npth
assert len(s.drill_pth.objects)==sum(c['type'] in ['pcb_via','pcb_plated_hole'] for c in cj)
assert len(s.drill_npth.objects)==sum(c['type']=='pcb_hole' for c in cj)
assert sum(abs(o.aperture.diameter-.9000236)<1e-6 for o in s.drill_pth.objects)==6,'Programming JST drills missing'
outline=s.outline.instance
xs=[v for o in outline.objects for v in (o.x1,o.x2)];ys=[v for o in outline.objects for v in (o.y1,o.y2)]
board=next(v for v in cj if v['type']=='pcb_board')
expected_width=max(p['x'] for p in board['outline'])-min(p['x'] for p in board['outline'])
expected_height=max(p['y'] for p in board['outline'])-min(p['y'] for p in board['outline'])
assert abs(max(xs)-min(xs)-expected_width)<.001 and abs(max(ys)-min(ys)-expected_height)<.001
# Both the outer custom profile and the internal routed pocket must be closed.
def key(x,y):return (round(x,5),round(y,5))
adjacency={}
for o in outline.objects:
 a,b=key(o.x1,o.y1),key(o.x2,o.y2)
 adjacency.setdefault(a,[]).append(b);adjacency.setdefault(b,[]).append(a)
assert all(len(v)==2 for v in adjacency.values()),'Open/branched Edge.Cuts contour'
remaining=set(adjacency);contours=[]
while remaining:
 first=next(iter(remaining));loop=[];previous=None;current=first
 while current not in loop:
  loop.append(current);remaining.discard(current)
  nxt=next(n for n in adjacency[current] if n!=previous)
  previous,current=current,nxt
 assert current==first,'Outline did not close'
 contours.append(loop)
assert len(contours)==2,'PCB must have one exterior and one internal window'
area=lambda p:abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(p,p[1:]+p[:1])))/2
areas=sorted(map(area,contours))
cut=next(c for c in cj if c['type']=='pcb_cutout')
assert abs(areas[0]-area([(p['x'],p['y']) for p in cut['points']]))<.01,'Gerbers must preserve exact pocket area'

with (ROOT/'manufacturing/BOM.csv').open() as f:bom=list(csv.DictReader(f))
with (ROOT/'manufacturing/pick-and-place.csv').open() as f:pnp=list(csv.DictReader(f))
assert len(bom)==sum(c['type']=='source_component' for c in cj)
assert len(pnp)==sum(c['type']=='pcb_component' and not c.get('do_not_place') for c in cj)
assert sum(abs(o.aperture.diameter-.999998)<1e-6 for o in s.drill_pth.objects)==8,'Display termination drills missing'
assert all(r['Side']=='top' for r in bom),'All component assembly must be top side'
assert all(r['Side']=='top' for r in pnp),'All placements must be top side'
assert {r['Reference'] for r in bom if r['Populate']=='YES'}=={r['Ref'] for r in pnp}
# Plain copper+drill plots avoid unsupported SVG filter blending in rasterizers.
for side in ['top','bottom']:
 colors={f'{side} copper':'#bb853c','mechanical outline':'#232323','drill pth':'#ffffff','drill npth':'#ffffff'}
 svg=s.to_svg(side_re=f'({side}|mechanical)',margin=1,force_bounds=s.board_bounds(),colors=colors)
 if side=='bottom':
  children=list(svg.children)
  svg.children=[Tag('g',children,transform='translate(200 0) scale(-1 1)')]
 text=str(svg)
 (ROOT/f'previews/gerber-{side}.svg').write_text(text)
 cairosvg.svg2png(bytestring=text.encode(),write_to=str(ROOT/f'previews/gerber-{side}.png'),output_width=1500,output_height=1500,background_color='white')
report={'parser':'gerbonara 1.5.0','graphical_layers':sorted(' '.join(k) for k in s.graphic_layers),'outline_centerline_mm':[round(expected_width,4),round(expected_height,4)],'outline_segments':len(outline.objects),'closed_edge_contours':2,'internal_window_area_mm2':round(areas[0],5),'plated_round_drills':pth['Flash'],'plated_slots':pth['Line'],'npth_diameters_and_counts':dict(npth),'JST_0.90mm_drills':6,'display_1.0mm_drills':8,'source_vias':sum(c['type']=='pcb_via' for c in cj),'source_plated_holes':sum(c['type']=='pcb_plated_hole' for c in cj),'BOM_rows':len(bom),'populated_placements':len(pnp),'parser_note':'KiCad redundant G90 after header is accepted with a parser syntax warning; no geometry is skipped.'}
(ROOT/'validation/manufacturing-inspection.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
