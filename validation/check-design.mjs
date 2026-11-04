// SPDX-License-Identifier: MIT
import fs from 'node:fs'
import assert from 'node:assert/strict'
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
for(const p of ['VBAT','VDDA','VDD1','VDD2','VDDIO2'])on('U1',p,'V3V3')
for(const p of ['VSSA','VSS1','VSS2','VSS3'])on('U1',p,'GND')
for(const [p,n] of Object.entries({PA0:'SCROLL_EN',PA1:'COUNT_RESET',PA2:'CHG_EN1',PA3:'CHG_EN2',PA4:'PGOOD',PA5:'CHG_STAT',PA6:'LED',PA7:'BAT_ADC',PB0:'VBUS_ADC',PB1:'TEMP_ADC',PB2:'CHG_CE',PA11:'USB_DM',PA12:'USB_DP',PB6:'SCL',PB7:'SDA'}))on('U1',p,n)
for(const [p,n] of Object.entries({COL:'V3V3',K:'GND',A:'IR_A',EA:'OPT_A',EB:'OPT_B'}))on('U2',p,n)
for(const [p,n] of Object.entries({A1:'OPT_A',A2:'OPT_B',Y1:'ENC_A',Y2:'ENC_B',VCC:'V3V3',GND:'GND'}))on('U7',p,n)
for(const p of ['SDA','SCL'])on('U3',p,p)
for(const [p,n] of Object.entries({PB4:'ENC_A',PB5:'ENC_B',PB10:'LCD_RST',PB11:'LCD_BL',PA8:'LCD_CS',PB13:'SPI_SCK',PB14:'LCD_DC',PB15:'SPI_MOSI'}))on('U1',p,n)
for(const [p,n] of Object.entries({BL:'LCD_BL',RST:'LCD_RST',DC:'LCD_DC',CS:'LCD_CS',CLK:'LCD_SCK',DIN:'LCD_MOSI',GND:'GND',VCC:'V3V3'}))on('J6',p,n)
for(const [p,n] of Object.entries({VREF:'V3V3',SWDIO:'SWDIO',SWCLK:'SWCLK',NRST:'NRST',GND:'GND',BOOT0:'BOOT0'}))on('J4',p,n)
on('SW1','T4','GND');on('SW1','T5','SCROLL_EN')
for(const p of ['A0','A1','A2','WP','VSS'])on('U3',p,'GND')
on('U3','VDD','V3V3')
for(const [p,n] of Object.entries({IN:'VBUS',OUT1:'SYS',OUT2:'SYS',BAT1:'BAT',BAT2:'BAT',EP:'GND',VSS:'GND',CE:'CHG_CE',EN1:'CHG_EN1',EN2:'CHG_EN2',TS:'NTC'}))on('U4',p,n)
for(const p of ['VBUS1','VBUS2'])on('J1',p,'VBUS')
for(const p of ['DN1','DN2'])on('J1',p,'USB_DM')
for(const p of ['DP1','DP2'])on('J1',p,'USB_DP')
for(const [c,n] of [['R1','CC1'],['R2','CC2']]){on('J1',n,n);on(c,'pin1',n);on(c,'pin2','GND');assert.equal(components.get(c).resistance,5100)}
for(const n of ['GND','V3V3','VBUS','SYS','BAT','USB_DP','USB_DM','CC1','CC2','CHG_EN1','CHG_EN2'])for(const m of ['GND','V3V3','VBUS','SYS','BAT','USB_DP','USB_DM','CC1','CC2','CHG_EN1','CHG_EN2'])if(m!==n)assert.notEqual(root(nets.get(n)),root(nets.get(m)),`${n} isolated from ${m}`)
pin('U1','PA8',29);pin('U1','PA11',32);pin('U1','PA12',33);pin('U1','VDDIO2',36);pin('U1','PB6',42);pin('U1','PB7',43);pin('U2','COL',6);pin('U2','K',3);pin('U7','Y1',6);pin('U7','Y2',4);pin('U1','PB4',40);pin('U1','PB5',41);pin('U3','VDD',8);pin('U4','IN',13);pin('U4','EP',17)
for(const c of components.values())assert(c.manufacturer_part_number,`${c.name} must have an MPN`)
const errors=cj.filter(x=>x.type.endsWith('_error'));assert.equal(errors.length,0,errors.map(x=>x.message).join('\n'))
// Source-only connections can otherwise conceal an accidentally empty footprint.
for(const p of ports){
 if(!cj.some(t=>t.type==='source_trace'&&t.connected_source_port_ids?.includes(p.source_port_id)))continue
 const physical=cj.filter(q=>q.type==='pcb_port'&&q.source_port_id===p.source_port_id)
 assert.equal(physical.length,1,`${components.get(p.source_component_id)?.name}.${p.name} must have a PCB port`)
 assert(cj.some(q=>['pcb_smtpad','pcb_plated_hole'].includes(q.type)&&q.pcb_port_id===physical[0].pcb_port_id),`${p.source_port_id} needs copper`)
}
for (const [name,count] of [['J2',2],['J4',6],['J6',8]]) {
 const pc=cj.find(x=>x.type==='pcb_component'&&x.source_component_id===components.get(name).source_component_id)
 const holes=cj.filter(x=>x.type==='pcb_plated_hole'&&x.pcb_component_id===pc.pcb_component_id)
 assert.equal(holes.length,count,`${name} JST PH pin count`)
 for(const h of holes)assert.equal(h.hole_diameter,.75,'JST PH finished drill')
}
assert(!components.has('J5'),'BOOT0 must be on six-pin JST J4')
assert(cj.filter(c=>c.type==='pcb_component').every(c=>c.layer==='top'),'Rev C must assemble entirely from the top');
assert.equal(cj.filter(c=>c.type==='pcb_cutout').length,1,'Battery and LCD pocket must be routed from the board');
const mechanics=JSON.parse(fs.readFileSync('mechanical/parameters.json'))
assert.equal(mechanics.encoder.slots*4,192)
assert.equal(mechanics.display.active_diameter,32.4)
// The optical gap must stay on the physical rotational axis, despite the
// asymmetric pad envelope shifting pcb_component.center.
const pp=cj.find(x=>x.type==='pcb_port'&&x.source_port_id===port('U2','A').source_port_id)
const angle=mechanics.encoder.rotation_deg*Math.PI/180
assert(Math.abs(pp.x-(-23-2.45*Math.cos(angle)-1.4*Math.sin(angle)))<1e-5)
assert(Math.abs(pp.y-(10-2.45*Math.sin(angle)+1.4*Math.cos(angle)))<1e-5)
const b=cj.find(x=>x.type==='pcb_board');assert(b);assert.equal(b.thickness,1.6)
console.log(`Design contract passed: ${components.size} components, physical pin maps, power/USB/I2C/controls and distinct rails.`)
