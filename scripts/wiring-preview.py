#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Draw the removable lead's physical signal map."""
from pathlib import Path
import json,csv
ROOT=Path(__file__).resolve().parents[1]
h=json.loads((ROOT/'mechanical/harness.json').read_text())
rows=sorted(h['connections'],key=lambda r:r['board_pin'])
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1000" viewBox="0 0 1500 1000">','<rect width="1500" height="1000" fill="#f4f7f8"/>','<g font-family="sans-serif" fill="#203943">','<text x="65" y="65" font-size="30">PCB E5 / mechanics E10 — Removable display lead</text>','<text x="65" y="105" font-size="20">Retain both factory ends. Shorten the middle; solder and individually heat-shrink eight joints.</text>','<text x="100" y="175" font-size="22">J6 — fitted 2×4 right-angle header</text>','<text x="960" y="175" font-size="22">Waveshare 19192 — PH2.0</text>']
for i,r in enumerate(rows):
 y=230+i*62;signal=r['signal'];colour=r['color_illustration_only'];colour='#8a9296' if colour=='#ffffff' else colour
 svg += [f'<rect x="128" y="{y-13}" width="32" height="26" fill="#30343a"/>',f'<text x="180" y="{y+7}" font-size="21">{r["board_pin"]}  {signal}</text>',f'<path d="M 350 {y} L 1010 {y}" stroke="{colour}" stroke-width="5"/>',f'<rect x="640" y="{y-8}" width="65" height="16" rx="5" fill="#30343a"/>',f'<text x="1040" y="{y+7}" font-size="21">{r["screen_pin"]}  {signal}</text>']
svg+=['<text x="65" y="795" font-size="20">Header grid: 2.54 mm. Odd pins lower, even pins upper; see physical pad coordinates in WIRING.md.</text>','<text x="65" y="835" font-size="20">VCC = switched 3.3V. Check all eight signals by continuity; factory colours may vary.</text>','<text x="65" y="875" font-size="20">Illustrated free paths: 25.6–27.9 mm. Trial-dress with slack before cutting; these are not cut lengths.</text>','<text x="65" y="915" font-size="20">Nominal female housings and sleeve envelopes; verify actual kit fit before final assembly.</text>','</g></svg>']
(ROOT/'previews/wiring.svg').write_text('\n'.join(svg)+'\n')
with (ROOT/'manufacturing/LCD-harness.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['Assembly','J6 physical pin','PCB hole XY mm','Signal','Original screen pin','Modeled free path mm (not cut length)','Additional consumable'])
 for r in rows:w.writerow(['Included Waveshare lead; both ends retained',r['board_pin'],','.join(f'{v:.2f}' for v in r['board_hole_mm'][:2]),r['signal'],r['screen_pin'],r['modeled_free_wire_path_mm'],'Individual heat-shrink sleeve per inline splice'])
print('Removable-lead wiring drawing and termination schedule exported.')
