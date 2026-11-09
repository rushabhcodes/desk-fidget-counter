// SPDX-License-Identifier: MIT
import fs from 'node:fs'
import assert from 'node:assert/strict'
import { checkPadPadClearance } from '@tscircuit/checks'
const fabrication=JSON.parse(fs.readFileSync('reference/fabrication-rules.json','utf8'))
const cj=JSON.parse(fs.readFileSync(process.argv[2]??'dist/index/circuit.json','utf8'))
const components=new Map(cj.filter(x=>x.type==='source_component').map(x=>[x.name,x]))
const ports=cj.filter(x=>x.type==='source_port')
const nets=new Map(cj.filter(x=>x.type==='source_net').map(x=>[x.name,x.source_net_id]))
const parent=new Map()
function root(x){if(!parent.has(x))parent.set(x,x);if(parent.get(x)!==x)parent.set(x,root(parent.get(x)));return parent.get(x)}
function join(a,b){parent.set(root(a),root(b))}
for(const t of cj.filter(x=>x.type==='source_trace')){
 const ids=[...(t.connected_source_port_ids??[]),...(t.connected_source_net_ids??[])]
 ids.slice(1).forEach(x=>join(ids[0],x))
}
function port(c,p){const component=components.get(c);assert(component,`component ${c}`);const found=ports.filter(x=>x.source_component_id===component.source_component_id&&x.port_hints?.includes(p));assert.equal(found.length,1,`${c}.${p} uniquely resolves`);return found[0]}
function on(c,p,n){assert.equal(root(port(c,p).source_port_id),root(nets.get(n)),`${c}.${p} must be ${n}`)}
function pin(c,p,n){assert.equal(port(c,p).pin_number,n,`${c}.${p} physical pin`)}
for(const p of ['VDDA','VDD1','VDD2','VDDIO2'])on('U1',p,'V3V3')
on('U1','VBAT','V3V3');on('C7','pin1','V3V3')
for(const p of ['VSSA','VSS1','VSS2','VSS3'])on('U1',p,'GND')
for(const [p,n] of Object.entries({PA0:'MODE_BTN',PB2:'PERIPH_EN',PA11:'USB_DM',PA12:'USB_DP',PB6:'SCL',PB7:'SDA'}))on('U1',p,n)
for(const [p,n] of Object.entries({COL:'PERIPH_3V3',K:'GND',A:'IR_A',EA:'OPT_A',EB:'OPT_B'}))on('U2',p,n)
for(const [p,n] of Object.entries({A1:'OPT_A',A2:'OPT_B',Y1:'ENC_A',Y2:'ENC_B',VCC:'V3V3',GND:'GND'}))on('U7',p,n)
for(const p of ['SDA','SCL'])on('U3',p,p)
for(const [p,n] of Object.entries({PB4:'ENC_A',PB5:'ENC_B',PB10:'LCD_RST',PB11:'LCD_BL',PA8:'LCD_CS',PB13:'SPI_SCK',PB14:'LCD_DC',PB15:'SPI_MOSI'}))on('U1',p,n)
for(const [p,n] of Object.entries({BL:'LCD_BL',RST:'LCD_RST',DC:'LCD_DC',CS:'LCD_CS',CLK:'LCD_SCK',DIN:'LCD_MOSI',GND:'GND',VCC:'PERIPH_3V3'}))on('J6',p,n)
for(const [p,n] of Object.entries({VREF:'V3V3',SWDIO:'SWDIO',SWCLK:'SWCLK',NRST:'NRST',GND:'GND',BOOT0:'BOOT0'}))on('J4',p,n)
on('SW1','pin1','MODE_BTN');on('SW1','pin2','GND');assert.equal(components.get('SW1').manufacturer_part_number,'B3U-3000P')
for(const p of ['A0','A1','A2','WP','VSS'])on('U3',p,'GND')
on('U3','VDD','V3V3')
for(const [p,n] of Object.entries({IN:'V3V3',GND:'GND',ON:'PERIPH_EN',VOUT:'PERIPH_3V3',QOD:'PERIPH_3V3'}))on('U4',p,n)
for(const p of ['VBUS1','VBUS2','VBUS3','VBUS4'])on('J1',p,'VBUS')
for(const p of ['GND1','GND2','GND3','GND4','EH1','EH2','EH3','EH4'])on('J1',p,'GND')
assert.equal(components.get('J1').manufacturer_part_number,'TYPEC-309-ACP16L65')
// Manufacturer drawing: physical library numbers map to the real USB contacts.
for(const [p,n] of Object.entries({CC2:33,SBU1:34,DP2:35,DN1:36,DP1:37,DN2:38,CC1:39,SBU2:40}))pin('J1',p,n)
for(const p of ['DN1','DN2'])on('J1',p,'USB_DM')
for(const p of ['DP1','DP2'])on('J1',p,'USB_DP')
for(const [c,n] of [['R1','CC1'],['R2','CC2']]){on('J1',n,n);on(c,'pin1',n);on(c,'pin2','GND');assert.equal(components.get(c).resistance,5100)}
for(const n of ['GND','V3V3','VBUS','PERIPH_3V3','USB_DP','USB_DM','CC1','CC2','PERIPH_EN'])for(const m of ['GND','V3V3','VBUS','PERIPH_3V3','USB_DP','USB_DM','CC1','CC2','PERIPH_EN'])if(m!==n)assert.notEqual(root(nets.get(n)),root(nets.get(m)),`${n} isolated from ${m}`)
pin('U1','PA8',29);pin('U1','PA11',32);pin('U1','PA12',33);pin('U1','VDDIO2',36);pin('U1','PB6',42);pin('U1','PB7',43);pin('U2','COL',6);pin('U2','K',3);pin('U7','Y1',6);pin('U7','Y2',4);pin('U1','PB4',40);pin('U1','PB5',41);pin('U3','VDD',8);pin('U4','IN',1);pin('U4','ON',3);pin('U4','VOUT',6)
for(const c of components.values())assert(c.manufacturer_part_number,`${c.name} must have an MPN`)
const errors=cj.filter(x=>x.type.endsWith('_error'));assert.equal(errors.length,0,errors.map(x=>x.message).join('\n'))
// JLCPCB distinguishes component-pad spacing from track/via clearance.
const componentPadErrors=checkPadPadClearance(cj,{minClearance:.15})
assert.equal(componentPadErrors.length,0,componentPadErrors.map(x=>x.message).join('\n'))
for(const t of cj.filter(x=>x.type==='pcb_trace'))for(const p of t.route)if(p.route_type==='wire')assert(p.width>=fabrication.minimum_track_width-1e-6,'All native copper must meet the fabrication minimum')
for (const name of ['MCU_VSSA_DECAP','MCU_VSS1_DECAP','MCU_VSS2_DECAP','MCU_VDD2_DECAP']) {
 const source=cj.find(x=>x.type==='source_trace'&&x.name===name)
 const routes=cj.filter(x=>x.type==='pcb_trace'&&x.source_trace_id===source.source_trace_id)
 assert(routes.length>0,`${name} must have native copper`)
 for(const route of routes)for(const p of route.route)if(p.route_type==='wire')
  assert(p.width>=.15-1e-6,`${name} must meet its requested 0.15mm width`)
}
// Source-only connections can otherwise conceal an accidentally empty footprint.
for(const p of ports){
 if(!cj.some(t=>t.type==='source_trace'&&t.connected_source_port_ids?.includes(p.source_port_id)))continue
 const physical=cj.filter(q=>q.type==='pcb_port'&&q.source_port_id===p.source_port_id)
 assert.equal(physical.length,1,`${components.get(p.source_component_id)?.name}.${p.name} must have a PCB port`)
 assert(cj.some(q=>['pcb_smtpad','pcb_plated_hole'].includes(q.type)&&q.pcb_port_id===physical[0].pcb_port_id),`${p.source_port_id} needs copper`)
}
for (const [name,count,drill] of [['J4',6,.9000236],['J6',8,1.1000232]]) {
 const pc=cj.find(x=>x.type==='pcb_component'&&x.source_component_id===components.get(name).source_component_id)
 const holes=cj.filter(x=>x.type==='pcb_plated_hole'&&x.pcb_component_id===pc.pcb_component_id)
 assert.equal(holes.length,count,`${name} JST PH pin count`)
 for(const h of holes)assert(Math.abs((h.hole_diameter??h.hole_width)-drill)<1e-6,`${name} imported finished drill`)
}
assert(!components.has('J2') && !components.has('J3'),'USB-only: no cell or NTC connector')
assert(![...nets.keys()].some(n=>/BAT|CHG|NTC/.test(n)),'No battery or charging rail remains')
on('U5','IN','VBUS');on('U5','EN','VBUS');on('U5','OUT','V3V3')
on('R24','pin1','PERIPH_3V3');on('C15','pin1','PERIPH_3V3')
assert(!components.has('J5'),'BOOT0 must be on six-pin JST J4')
assert(cj.filter(c=>c.type==='pcb_component').every(c=>c.layer==='top'),'Rev E must assemble entirely from the top');
assert.equal(cj.filter(c=>c.type==='pcb_cutout').length,1,'LCD and cable pocket must be routed from the board');
const mechanics=JSON.parse(fs.readFileSync('mechanical/parameters.json'))
assert.equal(mechanics.encoder.slots*4,192)
assert.equal(mechanics.display.active_diameter,32.4)
// The optical gap must stay on the physical rotational axis, despite the
// asymmetric pad envelope shifting pcb_component.center.
const pp=cj.find(x=>x.type==='pcb_port'&&x.source_port_id===port('U2','A').source_port_id)
const angle=mechanics.encoder.rotation_deg*Math.PI/180
assert(Math.abs(pp.x-(-23-2.45*Math.cos(angle)-1.4*Math.sin(angle)))<.0002)
assert(Math.abs(pp.y-(10-2.45*Math.sin(angle)+1.4*Math.cos(angle)))<.0002)
const b=cj.find(x=>x.type==='pcb_board');assert(b);assert.equal(b.thickness,1.6);assert.equal(b.num_layers,2,'The PCB must retain two copper layers')

for(const n of ['D1','LED1','R11','R14','R15','R16','R29','SW2'])assert(!components.has(n),`Redundant component ${n} must remain removed`)
assert.equal(components.size,39,'Rev E reviewed component count')
assert.equal(components.get('C8').capacitance,10e-9);assert.equal(components.get('C17').capacitance,1e-6);assert.equal(components.get('C18').capacitance,4.7e-6)
for(const ref of ['C6','C12','C18'])assert.equal(components.get(ref).manufacturer_part_number,'CL21A475KOFNNNE','Use the current 16V Samsung bulk capacitor, not the obsolete Murata part')
const audit=JSON.parse(fs.readFileSync('reference/component-audit.json','utf8'));assert.equal(audit.baseline_components.length,45);assert.deepEqual([...components.keys()].sort(),[...audit.baseline_components.filter(x=>x.decision!=='remove'),...audit.added_components].map(x=>x.reference).sort())

const usb=cj.find(x=>x.type==='pcb_component'&&x.source_component_id===components.get('J1').source_component_id)
const usbSlots=cj.filter(x=>x.type==='pcb_plated_hole'&&x.pcb_component_id===usb.pcb_component_id)
assert.equal(usbSlots.length,4)
for(const slot of usbSlots){
 const width=Math.min(slot.hole_width,slot.hole_height)
 const length=Math.max(slot.hole_width,slot.hole_height)
 assert(width>=.5-1e-6,'JLCPCB standard plated slot width')
 assert(length/width>=fabrication.minimum_standard_plated_slot_length_width_ratio-1e-6,'JLCPCB standard plated slot length/width')
}
assert.equal(usb.is_allowed_to_be_off_board,true,'USB housing intentionally overhangs the PCB nose')
const button=cj.find(x=>x.type==='pcb_component'&&x.source_component_id===components.get('SW1').source_component_id)
assert.equal(button.is_allowed_to_be_off_board,true,'Original switch actuator intentionally overhangs the PCB nose')
assert(cj.filter(x=>x.type==='pcb_component'&&![usb.pcb_component_id,button.pcb_component_id].includes(x.pcb_component_id)).every(x=>!x.is_allowed_to_be_off_board),'Only USB and the direct button may overhang')
assert.deepEqual(button.footprint_origin,{x:0,y:mechanics.front_button.pcb_center[1]})
assert.equal(mechanics.front_button.direct_actuation,false)
assert.equal(mechanics.front_button.printed_cap.part,'button-cap')
assert(fs.existsSync('mechanical/stl/button-cap.stl'),'The user-facing printed cap must be included')
assert(!fs.existsSync('mechanical/stl/button-plunger.stl'),'No separate printed button plunger')
assert.equal(usb.footprint_origin.x,mechanics.usb_center[0]);assert.equal(usb.footprint_origin.y,mechanics.usb_center[1])
assert(Math.abs(Math.max(...b.outline.map(p=>p.y))-41.4)<1e-6,'Integral USB tab must reach its specified front edge')
assert(Math.abs(Math.min(...b.outline.map(p=>p.y))+42.1)<1e-6)
assert(Math.abs(b.height-83.5)<1e-6)
assert.equal(components.get('J6').manufacturer_part_number,'61300821021')
assert.equal(mechanics.stock_display_cable.custom_harness_required,false)
const display=cj.find(x=>x.type==='pcb_component'&&x.source_component_id===components.get('J6').source_component_id)
assert(!display.do_not_place,'The removable display header must be fitted')
assert.deepEqual(mechanics.display_board_header.pin_signals,['BL','RST','DC','CS','CLK','DIN','GND','VCC'])
for (let i=0;i<8;i++) pin('J6',mechanics.display_board_header.pin_signals[i],i+1)
assert.equal(cj.filter(x=>x.type==='pcb_component'&&!x.do_not_place).length,39)
console.log(`Design contract passed: ${components.size} references / 39 populated parts, physical pin maps, power/USB/I2C/controls and distinct rails.`)
