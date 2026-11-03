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
assert npth==Counter({2.7:4,.6:2,1.5:2}),npth
assert len(s.drill_pth.objects)==sum(c['type'] in ['pcb_via','pcb_plated_hole'] for c in cj)
assert len(s.drill_npth.objects)==sum(c['type']=='pcb_hole' for c in cj)
assert sum(abs(o.aperture.diameter-.75)<1e-8 for o in s.drill_pth.objects)==2,'JST drills missing'
outline=s.outline.instance
xs=[v for o in outline.objects for v in (o.x1,o.x2)];ys=[v for o in outline.objects for v in (o.y1,o.y2)]
assert abs(max(xs)-min(xs)-64)<.001 and abs(max(ys)-min(ys)-64)<.001
assert len(outline.objects)==128
with (ROOT/'manufacturing/BOM.csv').open() as f:bom=list(csv.DictReader(f))
with (ROOT/'manufacturing/pick-and-place.csv').open() as f:pnp=list(csv.DictReader(f))
assert len(bom)==57 and len(pnp)==54
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
report={'parser':'gerbonara 1.5.0','graphical_layers':sorted(' '.join(k) for k in s.graphic_layers),'outline_centerline_mm':[64,64],'outline_segments':128,'plated_round_drills':pth['Flash'],'plated_slots':pth['Line'],'npth_diameters_and_counts':dict(npth),'JST_0.75mm_drills':2,'source_vias':sum(c['type']=='pcb_via' for c in cj),'source_plated_holes':sum(c['type']=='pcb_plated_hole' for c in cj),'BOM_rows':len(bom),'populated_placements':len(pnp),'parser_note':'KiCad redundant G90 after header is accepted with a parser syntax warning; no geometry is skipped.'}
(ROOT/'validation/manufacturing-inspection.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
