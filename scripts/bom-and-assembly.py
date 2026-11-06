#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. BOM and pin-1 assembly drawings from the released circuit."""
from pathlib import Path
import csv,json,html,math
ROOT=Path(__file__).resolve().parents[1]
cj=json.loads((ROOT/'dist/index/circuit.json').read_text())
components={c['source_component_id']:c for c in cj if c['type']=='source_component'}
placed={p['source_component_id']:p for p in cj if p['type']=='pcb_component' and p.get('source_component_id') in components}
ports={p['source_port_id']:p for p in cj if p['type']=='source_port'}
dnp={components[cid]['name'] for cid,p in placed.items() if p.get('do_not_place')}
makers={'U1':'STMicroelectronics','U2':'Vishay','U7':'Texas Instruments','U3':'RAMXEED','U4':'Texas Instruments','U5':'Texas Instruments','U6':'STMicroelectronics','J1':'HRO','J4':'JST','J6':'Würth Elektronik','SW1':'Omron',**dict.fromkeys(['C6','C12','C18'],'Samsung Electro-Mechanics')}
rows=[]
for cid,c in components.items():
    n=c['name'];p=placed[cid]
    value=c.get('display_resistance',c.get('display_capacitance',c.get('manufacturer_part_number','')))
    maker=makers.get(n,'Yageo' if n.startswith('R') else 'Murata')
    note='Top reflow' if p.get('layer')=='top' and n not in ['J4','J6'] else 'Hand solder'
    if n=='J6':note='DNP optional header; solder shortened included display lead into these pads'
    rows.append({'Reference':n,'Quantity':1,'Value':value,'Manufacturer':maker,'MPN':c['manufacturer_part_number'],'Side':p['layer'],'Populate':'NO' if n in dnp else 'YES','Assembly notes':note})
rows.sort(key=lambda x:(''.join(c for c in x['Reference'] if not c.isdigit()),int(''.join(c for c in x['Reference'] if c.isdigit()) or 0)))
with (ROOT/'manufacturing/BOM.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# Coordinates in these drawings are the board's native mm frame; bottom is mirrored for assembly.
for side in ['top','bottom']:
    flip=-1 if side=='bottom' else 1
    xy=lambda x,y:(950+flip*x*22,1150-y*22)
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1900" height="2260" viewBox="0 0 1900 2260">','<rect width="1900" height="2260" fill="#f8fafb"/>',f'<text x="950" y="60" text-anchor="middle" font-family="sans-serif" font-size="28">Desk knob Rev E3 — {side} assembly</text>']
    board=next(c for c in cj if c['type']=='pcb_board')
    contours=[board['outline']]+[c['points'] for c in cj if c['type']=='pcb_cutout']
    commands=[]
    for contour in contours:
        commands.append('M '+' L '.join(f'{xy(v["x"],v["y"])[0]:.3f},{xy(v["x"],v["y"])[1]:.3f}' for v in contour)+' Z')
    svg.append('<path d="'+' '.join(commands)+'" fill="#e4eee7" stroke="#243f32" stroke-width="3" fill-rule="evenodd"/>')
    for hole in [c for c in cj if c['type']=='pcb_hole']:
        a,b=xy(hole['x'],hole['y']);radius=hole.get('hole_diameter',hole.get('diameter',2.7))*11
        svg.append(f'<circle cx="{a}" cy="{b}" r="{radius}" fill="white" stroke="#566"/>')
    for cid,p in placed.items():
        if p['layer']!=side:continue
        c=components[cid];n=c['name'];a,b=xy(p['center']['x'],p['center']['y']);w,h=p['width']*22,p['height']*22
        svg.append(f'<rect x="{a-w/2}" y="{b-h/2}" width="{w}" height="{h}" fill="{"#e1e1e1" if n in dnp else "#fff"}" stroke="#334d43" stroke-width="1.5"/>')
        # Every indicator uses the actual physical pin-1 copper port, never a guessed corner.
        pin1=next((q for q in cj if q['type']=='pcb_port' and q.get('pcb_component_id')==p['pcb_component_id'] and ports.get(q.get('source_port_id'),{}).get('pin_number')==1),None)
        if pin1:
            u,v=xy(pin1['x'],pin1['y']);svg.append(f'<circle cx="{u}" cy="{v}" r="5" fill="#be3333"/>')
        svg.append(f'<text x="{a}" y="{b+5}" text-anchor="middle" font-family="monospace" font-weight="bold" font-size="16">{html.escape(n)}</text>')
        if n in dnp:svg.append(f'<text x="{a}" y="{b+h/2+18}" text-anchor="middle" font-family="sans-serif" font-size="13">DNP</text>')
    svg.append('<text x="950" y="2160" text-anchor="middle" font-family="sans-serif" font-size="21">Red dots mark physical pin 1. J4 is JST PH6 SWD; J6 takes the shortened included display lead; header DNP. USB power only.</text>')
    svg.append('<text x="950" y="2195" text-anchor="middle" font-family="sans-serif" font-size="21">All populated components mount on TOP. Read with BOM.csv; USB-C faces +Y.</text></svg>')
    (ROOT/f'previews/assembly-{side}.svg').write_text('\n'.join(svg))
print(f'BOM: {len(rows)} source components, {len(rows)-len(dnp)} populated; assembly views exported.')
