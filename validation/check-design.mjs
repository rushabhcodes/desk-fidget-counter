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
const rp=JSON.parse(fs.readFileSync('reference/rp2040.json','utf8'))
assert.equal(components.get('U1').manufacturer_part_number,'RP2040')
assert.equal(components.get('U8').manufacturer_part_number,'W25Q16JVSNIQ')
assert.equal(components.get('X1').manufacturer_part_number,'ABM8-272-T3')
for(const p of ['IOVDD1','IOVDD2','IOVDD3','IOVDD4','IOVDD5','IOVDD6','VREG_IN','ADC_AVDD','USB_VDD'])on('U1',p,'V3V3')
for(const p of ['DVDD1','DVDD2','VREG_VOUT'])on('U1',p,'V1V1')
for(const p of ['GND','TESTEN'])on('U1',p,'GND')
for(const [net,gpio] of Object.entries(rp.gpio))on('U1',`GPIO${gpio}`,net)
for(const p of ['RUN','SWDIO','SWCLK','XIN','XOUT'])on('U1',p,p)
for(const [p,n] of Object.entries({USB_DM:'USB_DM_MCU',USB_DP:'USB_DP_MCU'}))on('U1',p,n)
for(const [p,n] of Object.entries({IOVDD1:1,GPIO0:2,GPIO1:3,GPIO4:6,GPIO5:7,IOVDD2:10,TESTEN:19,XIN:20,XOUT:21,IOVDD3:22,DVDD1:23,SWCLK:24,SWDIO:25,RUN:26,GPIO16:27,GPIO17:28,GPIO18:29,GPIO19:30,GPIO20:31,GPIO21:32,IOVDD4:33,GPIO22:34,GPIO23:35,IOVDD5:42,ADC_AVDD:43,VREG_IN:44,VREG_VOUT:45,USB_DM:46,USB_DP:47,USB_VDD:48,IOVDD6:49,DVDD2:50,QSPI_SD3:51,QSPI_SCLK:52,QSPI_SD0:53,QSPI_SD2:54,QSPI_SD1:55,QSPI_SS:56,GND:57}))pin('U1',p,n)
for(const [p,n] of Object.entries({CS:'QSPI_SS',SCLK:'QSPI_SCLK',SD0:'QSPI_SD0',SD1:'QSPI_SD1',SD2:'QSPI_SD2',SD3:'QSPI_SD3',VCC:'V3V3',GND:'GND'}))on('U8',p,n)
for(const p of ['SS','SCLK','SD0','SD1','SD2','SD3'])on('U1',`QSPI_${p}`,`QSPI_${p}`)
for(const [p,n] of Object.entries({CS:1,SD1:2,SD2:3,GND:4,SD0:5,SCLK:6,SD3:7,VCC:8}))pin('U8',p,n)
for(const [c,p,n] of [['X1','X1','XIN'],['X1','X2','XTAL_OUT'],['X1','pin2','GND'],['X1','pin4','GND'],['R5','pin1','XOUT'],['R5','pin2','XTAL_OUT'],['R6','pin1','QSPI_SS'],['R6','pin2','BOOTSEL'],['R7','pin1','QSPI_SS'],['R7','pin2','V3V3'],['R10','pin1','RUN'],['R10','pin2','V3V3']])on(c,p,n)
for(const [p,n] of Object.entries({X1:1,pin2:2,X2:3,pin4:4}))pin('X1',p,n)
for(const [c,n] of [['C23','XIN'],['C24','XTAL_OUT']]){on(c,'pin1',n);on(c,'pin2','GND');assert.equal(components.get(c).capacitance,15e-12)}
assert.equal(components.get('R5').resistance,1000);assert.equal(components.get('R6').resistance,1000)
assert.equal(components.get('R7').resistance,10000);assert.equal(components.get('R10').resistance,10000)
for(const [c,n] of [['R3','USB_DM'],['R4','USB_DP']]){on(c,'pin1',`${n}_MCU`);on(c,'pin2',n);assert.equal(components.get(c).resistance,27)}
for(const [c,n] of [['C7','V3V3'],['C8','V3V3'],['C9','V3V3'],['C10','V3V3'],['C11','V3V3'],['C12','V3V3'],['C13','V3V3'],['C17','V3V3'],['C18','V1V1'],['C19','V1V1'],['C20','V3V3'],['C21','V1V1'],['C22','V3V3']]){on(c,'pin1',n);on(c,'pin2','GND');assert.equal(components.get(c).capacitance,['C20','C21'].includes(c)?1e-6:100e-9)}
for(const [p,n] of Object.entries({COL:'PERIPH_3V3',K:'GND',A:'IR_A',EA:'OPT_A',EB:'OPT_B'}))on('U2',p,n)
for(const [p,n] of Object.entries({A1:'OPT_A',A2:'OPT_B',Y1:'ENC_A',Y2:'ENC_B',VCC:'V3V3',GND:'GND'}))on('U7',p,n)
for(const p of ['SDA','SCL'])on('U3',p,p)
for(const [p,n] of Object.entries({BL:'LCD_BL',RST:'LCD_RST',DC:'LCD_DC',CS:'LCD_CS',CLK:'LCD_SCK',DIN:'LCD_MOSI',GND:'GND',VCC:'PERIPH_3V3'}))on('J6',p,n)
for(const [p,n] of Object.entries({VREF:'V3V3',SWDIO:'SWDIO',SWCLK:'SWCLK',RUN:'RUN',GND:'GND',BOOTSEL:'BOOTSEL'}))on('J4',p,n)
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
for(const n of ['GND','V3V3','V1V1','VBUS','PERIPH_3V3','USB_DP','USB_DM','USB_DP_MCU','USB_DM_MCU','CC1','CC2','PERIPH_EN','BOOTSEL','QSPI_SS','XIN','XOUT','XTAL_OUT'])for(const m of ['GND','V3V3','V1V1','VBUS','PERIPH_3V3','USB_DP','USB_DM','USB_DP_MCU','USB_DM_MCU','CC1','CC2','PERIPH_EN','BOOTSEL','QSPI_SS','XIN','XOUT','XTAL_OUT'])if(m!==n)assert.notEqual(root(nets.get(n)),root(nets.get(m)),`${n} isolated from ${m}`)
pin('U2','COL',6);pin('U2','K',3);pin('U7','Y1',6);pin('U7','Y2',4);pin('U3','VDD',8);pin('U4','IN',1);pin('U4','ON',3);pin('U4','VOUT',6)
for(const c of components.values())assert(c.manufacturer_part_number,`${c.name} must have an MPN`)
const errors=cj.filter(x=>x.type.endsWith('_error'));assert.equal(errors.length,0,errors.map(x=>x.message).join('\n'))
// JLCPCB distinguishes component-pad spacing from track/via clearance.
const componentPadErrors=checkPadPadClearance(cj,{minClearance:.15})
assert.equal(componentPadErrors.length,0,componentPadErrors.map(x=>x.message).join('\n'))
for(const t of cj.filter(x=>x.type==='pcb_trace'))for(const p of t.route)if(p.route_type==='wire')assert(p.width>=fabrication.minimum_track_width-1e-6,'All source copper must meet the fabrication minimum')
// Stored copper is associated with complete nets. Check real pad contacts;
// the independent bypass check measures each critical branch's actual path.
const routedPorts=new Set(cj.filter(x=>x.type==='pcb_trace').flatMap(t=>[
 ...(t.connectsTo??[]),...t.route.flatMap(p=>[p.start_pcb_port_id,p.end_pcb_port_id].filter(Boolean))
]))
for (const name of ['RP2040_IOVDD1_BYPASS','RP2040_IOVDD2_BYPASS','RP2040_IOVDD3_BYPASS','RP2040_IOVDD4_BYPASS','RP2040_IOVDD5_BYPASS','RP2040_IOVDD6_BYPASS','RP2040_ADC_AVDD_BYPASS','RP2040_USB_VDD_BYPASS','RP2040_DVDD1_BYPASS','RP2040_DVDD2_BYPASS','RP2040_VREG_INPUT','RP2040_VREG_OUTPUT','FLASH_BYPASS']) {
 const source=cj.find(x=>x.type==='source_trace'&&x.name===name)
 assert(source,`${name} must be explicitly connected`)
 for(const id of source.connected_source_port_ids){
  const physical=cj.find(x=>x.type==='pcb_port'&&x.source_port_id===id)
  assert(physical&&routedPorts.has(physical.pcb_port_id),`${name} endpoint must have source copper`)
 }
}
// Ordinary neck-downs follow the published 0.10mm fabrication minimum.
// MCU supply paths are separately required to retain at least 0.15mm width.
// Source-only connections can otherwise conceal an accidentally empty footprint.
for(const p of ports){
 if(!cj.some(t=>t.type==='source_trace'&&t.connected_source_port_ids?.includes(p.source_port_id)))continue
 const physical=cj.filter(q=>q.type==='pcb_port'&&q.source_port_id===p.source_port_id)
 assert.equal(physical.length,1,`${components.get(p.source_component_id)?.name}.${p.name} must have a PCB port`)
 assert(cj.some(q=>['pcb_smtpad','pcb_plated_hole'].includes(q.type)&&q.pcb_port_id===physical[0].pcb_port_id),`${p.source_port_id} needs copper`)
}
for (const [name,count,drill] of [['J4',6,.9000236]]) {
 const pc=cj.find(x=>x.type==='pcb_component'&&x.source_component_id===components.get(name).source_component_id)
 const holes=cj.filter(x=>x.type==='pcb_plated_hole'&&x.pcb_component_id===pc.pcb_component_id)
 assert.equal(holes.length,count,`${name} JST PH pin count`)
 for(const h of holes)assert(Math.abs((h.hole_diameter??h.hole_width)-drill)<1e-6,`${name} imported finished drill`)
}
assert(!components.has('J2') && !components.has('J3'),'USB-only: no cell or NTC connector')
assert(![...nets.keys()].some(n=>/BAT|CHG|NTC/.test(n)),'No battery or charging rail remains')
on('U5','IN','VBUS');on('U5','EN','VBUS');on('U5','OUT','V3V3')
on('R24','pin1','PERIPH_3V3');on('C15','pin1','PERIPH_3V3')
assert(!components.has('J5'),'BOOTSEL must be on six-pin JST J4')
assert(cj.filter(c=>c.type==='pcb_component').every(c=>c.layer==='top'),'Rev F1 must assemble entirely from the top');
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
assert.equal(components.size,52,'F1 reviewed component count')
assert.equal(components.get('C6').manufacturer_part_number,'CL21A475KOFNNNE')
const expectedRefs=['C1','C2','C3',...Array.from({length:20},(_,i)=>`C${i+5}`),'J1','J4','J6','SW1','X1',...Array.from({length:8},(_,i)=>`U${i+1}`),...['1','2','3','4','5','6','7','10','12','13','21','24','25','26','27','28'].map(i=>`R${i}`)]
assert.deepEqual([...components.keys()].sort(),expectedRefs.sort(),'F1 population is explicit')
assert.equal(cj.filter(x=>['pcb_smtpad','pcb_plated_hole'].includes(x.type)).length,222,'F1 exact physical pad count')

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
const buttonEdge=Math.min(...mechanics.pcb_outline.button_tab.points.map(p=>p[1]))
assert(Math.abs(Math.min(...b.outline.map(p=>p.y))-buttonEdge)<1e-6,'PCB button tab must match the mechanical outline')
assert(Math.abs(b.height-(41.4-buttonEdge))<1e-6)
assert.equal(mechanics.front_button.printed_cap.face_radius_mm,mechanics.base_diameter/2-mechanics.front_button.printed_cap.face_recess_mm)
assert.equal(components.get('J6').manufacturer_part_number,'SM08B-SRSS-TB(LF)(SN)')
assert.equal(mechanics.stock_display_cable.custom_harness_required,true)
const display=cj.find(x=>x.type==='pcb_component'&&x.source_component_id===components.get('J6').source_component_id)
assert(!display.do_not_place,'The removable display socket must be fitted')
assert.equal(cj.filter(x=>x.type==='pcb_smtpad'&&x.pcb_component_id===display.pcb_component_id).length,10)
assert.equal(cj.filter(x=>x.type==='pcb_plated_hole'&&x.pcb_component_id===display.pcb_component_id).length,0)
on('J6','MP1','GND');on('J6','MP2','GND')
assert.deepEqual(mechanics.display_board_header.pin_signals,['BL','RST','DC','CS','CLK','DIN','GND','VCC'])
for (let i=0;i<8;i++) pin('J6',mechanics.display_board_header.pin_signals[i],i+1)
assert.equal(cj.filter(x=>x.type==='pcb_component'&&!x.do_not_place).length,52)
console.log(`Design contract passed: ${components.size} references / 52 populated parts, physical pin maps, power/USB/I2C/controls and distinct rails.`)
