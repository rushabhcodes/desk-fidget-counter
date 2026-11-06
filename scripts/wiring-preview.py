#!/usr/bin/env python3
"""Draw the included lead's verified signal mapping; colours are illustrative."""
from pathlib import Path
import json,csv
ROOT=Path(__file__).resolve().parents[1]
h=json.loads((ROOT/'mechanical/harness.json').read_text())
rows=sorted(h['connections'],key=lambda r:r['board_pin'])
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1000" viewBox="0 0 1500 1000">','<rect width="1500" height="1000" fill="#f4f7f8"/>','<g font-family="sans-serif" fill="#203943">','<text x="65" y="65" font-size="30">PCB E3 / mechanics E4 — Included display lead</text>','<text x="65" y="105" font-size="20">Keep the original PH display plug; shorten and solder the PCB end. No extra harness parts.</text>','<text x="100" y="175" font-size="22">J6 — solder pads (header DNP)</text>','<text x="960" y="175" font-size="22">Waveshare 19192 — PH2.0</text>']
for i,r in enumerate(rows):
 y=230+i*62;signal=r['signal'];colour=r['color_illustration_only']
 if colour=='#ffffff':colour='#8a9296'
 svg += [f'<circle cx="145" cy="{y}" r="12" fill="#dcbf77" stroke="#203943" stroke-width="3"/>',f'<text x="180" y="{y+7}" font-size="21">{r["board_pin"]}  {signal}</text>',f'<path d="M 350 {y} L 1010 {y}" stroke="{colour}" stroke-width="5"/>',f'<text x="1040" y="{y+7}" font-size="21">{r["screen_pin"]}  {signal}</text>']
svg+=['<text x="65" y="795" font-size="20">J6: X=−21.5 mm; pin 1 Y=4.39 mm, continuing toward −Y at 2.54 mm pitch.</text>','<text x="65" y="835" font-size="20">VCC = switched 3.3V. Check continuity against display labels; factory colours may vary.</text>','<text x="65" y="875" font-size="20">Trial-route before trimming; approx. 37 mm insulated span + 2.55 mm stripped PCB end.</text>','<text x="65" y="915" font-size="20">Best approximation: 1.2 mm wire model, 1.5 mm clearance check; static bends, no flexing in use.</text>','</g></svg>']
(ROOT/'previews/wiring.svg').write_text('\n'.join(svg)+'\n')
with (ROOT/'manufacturing/LCD-harness.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Assembly','PCB pad','PCB pad XY mm','Signal','Original screen pin','Modeled insulated span mm','Required purchased parts'])
 for r in rows:w.writerow(['Included Waveshare lead; shorten PCB end',r['board_pin'],','.join(f'{v:.2f}' for v in r['board_pad_mm'][:2]),r['signal'],r['screen_pin'],r['modeled_insulated_wire_length_mm'],'None; retain factory PH display plug'])
print('Wiring drawing and included-lead termination schedule exported.')
