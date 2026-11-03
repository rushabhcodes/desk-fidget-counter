#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. BOM and pin-1 assembly drawings from the released circuit."""
from pathlib import Path
import csv,json,html,math
ROOT=Path(__file__).resolve().parents[1]
cj=json.loads((ROOT/'dist/index/circuit.json').read_text())
components={c['source_component_id']:c for c in cj if c['type']=='source_component'}
placed={p['source_component_id']:p for p in cj if p['type']=='pcb_component' and p.get('source_component_id') in components}
ports={p['source_port_id']:p for p in cj if p['type']=='source_port'}
dnp={'J3','J4','J5'}
makers={'U1':'STMicroelectronics','U2':'ams OSRAM / Infineon','U3':'RAMXEED','U4':'Texas Instruments','U5':'Texas Instruments','U6':'STMicroelectronics','D1':'Nexperia','J1':'HRO','J2':'JST','J3':'Wurth Elektronik','J4':'Wurth Elektronik','J5':'Wurth Elektronik','SW1':'C&K / Littelfuse','SW2':'XUNPU','LED1':'Lite-On'}
rows=[]
for cid,c in components.items():
    n=c['name'];p=placed[cid]
    value=c.get('display_resistance',c.get('display_capacitance',c.get('manufacturer_part_number','')))
    maker=makers.get(n,'Yageo' if n.startswith('R') else 'Murata')
    note='Unpopulated interface; use wires/pogo contacts/temporary bridge' if n in dnp else 'Top reflow' if p.get('layer')=='top' and n!='SW1' else 'Hand solder'
    rows.append({'Reference':n,'Quantity':1,'Value':value,'Manufacturer':maker,'MPN':c['manufacturer_part_number'],'Side':p['layer'],'Populate':'NO' if n in dnp else 'YES','Assembly notes':note})
rows.sort(key=lambda x:(''.join(c for c in x['Reference'] if not c.isdigit()),int(''.join(c for c in x['Reference'] if c.isdigit()) or 0)))
with (ROOT/'manufacturing/BOM.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# Coordinates in these drawings are the board's native mm frame; bottom is mirrored for assembly.
for side in ['top','bottom']:
    flip=-1 if side=='bottom' else 1
    xy=lambda x,y:(850+flip*x*24,850-y*24)
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1700" height="1760" viewBox="0 0 1700 1760">','<rect width="1700" height="1760" fill="#f8fafb"/>','<circle cx="850" cy="850" r="768" fill="#e4eee7" stroke="#243f32" stroke-width="3"/>',f'<text x="850" y="40" text-anchor="middle" font-family="sans-serif" font-size="28">Desk knob Rev A — {side} assembly</text>']
    for x,y in [(-21,21),(21,21),(-21,-21),(21,-21)]:
        a,b=xy(x,y);svg.append(f'<circle cx="{a}" cy="{b}" r="32.4" fill="white" stroke="#566"/>')
    for cid,p in placed.items():
        if p['layer']!=side:continue
        c=components[cid];n=c['name'];a,b=xy(p['center']['x'],p['center']['y']);w,h=p['width']*24,p['height']*24
        svg.append(f'<rect x="{a-w/2}" y="{b-h/2}" width="{w}" height="{h}" fill="{"#e1e1e1" if n in dnp else "#fff"}" stroke="#334d43" stroke-width="1.5"/>')
        # Every indicator uses the actual physical pin-1 copper port, never a guessed corner.
        pin1=next((q for q in cj if q['type']=='pcb_port' and q.get('pcb_component_id')==p['pcb_component_id'] and ports.get(q.get('source_port_id'),{}).get('pin_number')==1),None)
        if pin1:
            u,v=xy(pin1['x'],pin1['y']);svg.append(f'<circle cx="{u}" cy="{v}" r="5" fill="#be3333"/>')
        svg.append(f'<text x="{a}" y="{b+5}" text-anchor="middle" font-family="monospace" font-weight="bold" font-size="16">{html.escape(n)}</text>')
        if n in dnp:svg.append(f'<text x="{a}" y="{b+h/2+18}" text-anchor="middle" font-family="sans-serif" font-size="13">DNP</text>')
    svg.append('<text x="850" y="1660" text-anchor="middle" font-family="sans-serif" font-size="21">Red dots mark physical pin 1. J3/J4/J5 remain unpopulated.</text>')
    svg.append('<text x="850" y="1695" text-anchor="middle" font-family="sans-serif" font-size="21">Read with BOM.csv and verified package pinouts; USB connector is at +Y.</text></svg>')
    (ROOT/f'previews/assembly-{side}.svg').write_text('\n'.join(svg))
print(f'BOM: {len(rows)} source components, {len(rows)-len(dnp)} populated; assembly views exported.')
