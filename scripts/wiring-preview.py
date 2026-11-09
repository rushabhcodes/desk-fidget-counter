#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. H1 connector-to-connector physical signal map."""
from pathlib import Path
import json,csv
ROOT=Path(__file__).resolve().parents[1];h=json.loads((ROOT/'mechanical/harness.json').read_text());rows=sorted(h['connections'],key=lambda r:r['board_pin'])
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1000" viewBox="0 0 1500 1000">','<rect width="1500" height="1000" fill="#f4f7f8"/>','<g font-family="sans-serif" fill="#203943">','<text x="65" y="65" font-size="30">PCB E6 / mechanics E11 — H1 keyed crimped display harness</text>','<text x="65" y="105" font-size="20">One replacement cable. JST-SH at J6; JST-PH at the display. No inline joints.</text>','<text x="65" y="165" font-size="22">SHR-08V-S-B / J6 1.0 mm pitch</text>','<text x="930" y="165" font-size="22">PHR-8 / screen 2.0 mm pitch</text>','<rect x="112" y="200" width="60" height="493" rx="5" fill="#d7d5c2"/>','<rect x="1010" y="200" width="60" height="493" rx="5" fill="#d7d5c2"/>']
for i,r in enumerate(rows):
 y=230+i*62;signal=r['signal'];colour=r['color_illustration_only'];colour='#8a9296' if colour=='#ffffff' else colour
 svg += [f'<text x="190" y="{y+7}" font-size="21">{r["board_pin"]}  {signal}</text>',f'<path d="M 350 {y} L 1010 {y}" stroke="{colour}" stroke-width="5"/>',f'<text x="1090" y="{y+7}" font-size="21">{r["screen_pin"]}  {signal}</text>']
svg+=['<text x="65" y="755" font-size="20">Match circuit numbers, not apparent left/right in connector-face views. Verify every wire by continuity.</text>','<text x="65" y="795" font-size="20">Free insulation length 44 ± 1 mm between rear housing exits; cable maker adds termination allowances.</text>','<text x="65" y="835" font-size="20">8× SSH-003T-P0.2-H + 8× SPH-004T-P0.5S; TE 55A0111-30-9, 30 AWG, OD 0.61 mm nominal.</text>','<text x="65" y="875" font-size="20">VCC = switched 3.3 V. Colours illustrative; both keyed ends removable. Supplied kit lead unused.</text>','<text x="65" y="915" font-size="20">Order H1 as a crimped harness; nominal seating and dressed bends require prototype fit.</text>','</g></svg>'];(ROOT/'previews/wiring.svg').write_text('\n'.join(svg)+'\n')
# Use the built supplier pad positions, including its original conversion residue.
cj=json.loads((ROOT/'dist/index/circuit.json').read_text())
j6=next(x for x in cj if x['type']=='source_component' and x['name']=='J6')
ports={x['source_port_id']:x for x in cj if x['type']=='source_port' and x['source_component_id']==j6['source_component_id']}
pad_xy={ports[x['source_port_id']]['pin_number']:[x['x'],x['y']] for x in cj if x['type']=='pcb_port' and x.get('source_port_id') in ports}
with (ROOT/'manufacturing/LCD-harness.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['Assembly','J6 physical pin','PCB pad XY mm','Signal','PHR-8 display circuit','Free insulation length mm','Board contact','Display contact','Wire'])
 for r in rows:w.writerow(['H1 SHR-08V-S-B to PHR-8',r['board_pin'],','.join(f'{v:.5f}' for v in pad_xy[r['board_pin']]),r['signal'],r['screen_pin'],'44 +/- 1; between rear housing exits','SSH-003T-P0.2-H','SPH-004T-P0.5S','TE 55A0111-30-9,30AWG'])
print('H1 crimped-harness signal drawing and termination schedule exported.')
