import { Fragment } from "react"
import { routeBoard } from "./routing"
import { TS_1088_AR02016 } from "./imports/TS_1088_AR02016"
import { MCU, AngleSensor, FRAM, Charger, mcuPins } from "./parts"
import { TYPE_C_31_M_12 } from "./imports/TYPE_C_31_M_12"
import type { PartsEngine } from "@tscircuit/props"
const refStyle={"& silkscreentext":{visibility:"hidden" as const}}
const fixedParts: PartsEngine = {findPart:({sourceComponent})=>sourceComponent.type==="source_component"?sourceComponent.supplier_part_numbers??{}:{}}
const resistorMpns: Record<string,string>={"5.1k":"RC0603FR-075K1L","4.42k":"RC0603FR-074K42L","3.09k":"RC0603FR-073K09L","30k":"RC0603FR-0730KL","100k":"RC0603FR-07100KL","10k":"RC0603FR-0710KL","4.7k":"RC0603FR-074K7L","1k":"RC0603FR-071KL","1M":"RC0603FR-071ML","470k":"RC0603FR-07470KL"}
const capacitorMpns: Record<string,string>={"100nF":"GRM188R71C104KA01D","1uF":"GRM188R61A105KA61D","4.7uF":"GRM21BR61A475KA73L","10nF":"GRM188R71H103KA01D","2.2uF":"GRM188R61C225KE11D","10uF":"GRM21BR61C106KE15L"}
const R=(p:any)=><resistor manufacturerPartNumber={resistorMpns[p.resistance]} pcbSx={refStyle} footprint="0603" schRotation={p.connections?.pin2==="net.V3V3"?90:-90} {...p}/>
const C=(p:any)=><capacitor manufacturerPartNumber={capacitorMpns[p.capacitance]} pcbSx={refStyle} footprint="0603" schRotation={-90} {...p}/>
const N=(name:string)=>`net.${name}`
const pos=[[-21,21],[21,21],[-21,-21],[21,-21]]
const used=["VBAT","NRST","VSSA","VDDA","PA0","PA1","PA2","PA3","PA4","PA5","PA6","PA7","PB0","PB1","PB2","VSS1","VDD1","PA11","PA12","PA13","VSS2","VDDIO2","PA14","PB6","PB7","BOOT0","VSS3","VDD2"]
export default () => <board name="DESK_KNOB_REVA" title="Desk fidget counter / USB scroll knob — Rev A" width={64} height={64}
 outline={Array.from({length:128},(_,i)=>({x:32*Math.cos(i*Math.PI/64),y:32*Math.sin(i*Math.PI/64)}))}
 layers={2} thickness={1.6} minTraceWidth={.1} minBoardEdgeClearance={.3} minTraceToHoleEdgeClearance={.25}
 minViaHoleDiameter={.3} minViaPadDiameter={.7} pcbStyle={{viaHoleDiameter:.3,viaPadDiameter:.7}}
 minTraceToPadEdgeClearance={.15} minPadEdgeToPadEdgeClearance={.15} minViaEdgeToPadEdgeClearance={.15}
 minViaHoleEdgeToViaHoleEdgeClearance={.55} minPlatedHoleDrillEdgeToDrillEdgeClearance={.25}
 partsEngine={fixedParts} schLayout={{layoutMode:"relative"}} autorouter={{local:true,algorithmFn:routeBoard,traceClearance:.15,allowViaInPad:false}} >
 <net name="GND" isGroundNet nominalTraceWidth={.25}/><net name="V3V3" isPowerNet nominalTraceWidth={.25}/><net name="VBUS" isPowerNet nominalTraceWidth={.25}/><net name="SYS" isPowerNet nominalTraceWidth={.25}/><net name="BAT" isPowerNet nominalTraceWidth={.25}/>
 {pos.map(([x,y],i)=><Fragment key={i}><hole name={`H${i+1}`} diameter={2.7} pcbX={x} pcbY={y}/></Fragment>)}
 <MCU pcbSx={refStyle} name="U1" pcbX={-12} pcbY={5} pcbRotation={90} noSchematicRepresentation noConnect={mcuPins.filter(p=>!used.includes(p))}
 connections={{VBAT:N("V3V3"),VDD1:N("V3V3"),VDD2:N("V3V3"),VDDIO2:N("V3V3"),VDDA:N("V3V3"),VSS1:N("GND"),VSS2:N("GND"),VSS3:N("GND"),VSSA:N("GND"),NRST:N("NRST"),BOOT0:N("BOOT0"),PA0:N("SCROLL_EN"),PA1:N("COUNT_RESET"),PA2:N("CHG_EN1"),PA3:N("CHG_EN2"),PA4:N("PGOOD"),PA5:N("CHG_STAT"),PA6:N("LED"),PA7:N("BAT_ADC"),PB0:N("VBUS_ADC"),PB1:N("TEMP_ADC"),PB2:N("CHG_CE"),PA11:N("USB_DM"),PA12:N("USB_DP"),PA13:N("SWDIO"),PA14:N("SWCLK"),PB6:N("SCL"),PB7:N("SDA")}}/>
 <schematicsheet name="sheet-1" displayName="usb" sheetIndex={0}>
 <schematicsection name="usb" displayName="USB-C / ESD / CC sink resistors"/>
 <TYPE_C_31_M_12 pcbSx={refStyle} name="J1" schWidth={1.5} pcbX={0} pcbY={25.7} pcbRotation={180} schX={-7} schY={-2} schSectionName="usb" noConnect={["SBU1","SBU2"]}
 connections={{EH1:N("GND"),EH2:N("GND"),EH3:N("GND"),EH4:N("GND"),GND1:N("GND"),GND2:N("GND"),VBUS1:N("VBUS"),VBUS2:N("VBUS"),DP1:N("USB_DP"),DP2:N("USB_DP"),DN1:N("USB_DM"),DN2:N("USB_DM")}}/>
 <R name="R1" resistance="5.1k" pcbX={6.8} pcbY={23} schX={-2} schY={1} schSectionName="usb" connections={{pin1:N("CC1"),pin2:N("GND")}}/>
 <R name="R2" resistance="5.1k" pcbX={-6.8} pcbRotation={180} pcbY={23} schX={-2} schY={-2} schSectionName="usb" connections={{pin1:N("CC2"),pin2:N("GND")}}/>
 <trace name="USB_CC1_RD" from=".J1 > .CC1" to=".R1 > .pin1" width={.15} pcbPath={[{x:-1.249934,y:3.2},{x:-5.975,y:3.2}]}/>
 <trace name="USB_CC2_RD" from=".J1 > .CC2" to=".R2 > .pin1" width={.15} pcbPath={[{x:1.75006,y:3.2},{x:5.975,y:3.2}]}/>
 <chip pcbSx={refStyle} name="U6" pinAttributes={{VBUS:{requiresPower:true},GND:{requiresGround:true},DM_IN:{isPassive:true},DM_OUT:{isPassive:true},DP_IN:{isPassive:true},DP_OUT:{isPassive:true}}} manufacturerPartNumber="USBLC6-2SC6" footprint="sot23_6" pcbX={0} pcbY={18} pcbRotation={180} schX={3} schY={-1} schSectionName="usb"
 pinLabels={{pin1:"DM_IN",pin2:"GND",pin3:"DP_IN",pin4:"DP_OUT",pin5:"VBUS",pin6:"DM_OUT"}}
 connections={{DM_IN:N("USB_DM"),GND:N("GND"),DP_IN:N("USB_DP"),DP_OUT:N("USB_DP"),VBUS:N("VBUS"),DM_OUT:N("USB_DM")}}/>
 <C name="C1" capacitance="100nF" pcbX={3.8} pcbY={18} schX={7} schY={-1} schSectionName="usb" connections={{pin1:N("VBUS"),pin2:N("GND")}}/>
 <diode pcbSx={refStyle} name="D1" manufacturerPartNumber="PESD5V0S1BA,115" variant="tvs" schRotation={90} footprint="sod323" pcbX={8} pcbY={19} schX={7} schY={2} schSectionName="usb" connections={{anode:N("GND"),cathode:N("VBUS")}}/>
 </schematicsheet>
 <schematicsheet name="sheet-2" displayName="power" sheetIndex={1}>
 <schematicsection name="power" displayName="Charging and power"/>
 <Charger pcbSx={refStyle} name="U4" pcbX={15} pcbY={8} schX={-9} schY={2} schSectionName="power" noConnect={["ITERM"]}
 connections={{TS:N("NTC"),BAT1:N("BAT"),BAT2:N("BAT"),CE:N("CHG_CE"),PGOOD:N("PGOOD"),VSS:N("GND"),CHG:N("CHG_STAT"),OUT1:N("SYS"),OUT2:N("SYS"),ILIM:N("ILIM"),IN:N("VBUS"),TMR:N("TMR"),ISET:N("ISET")}}/>
 <trace name="CHARGER_EP_GROUND" from=".U4 > .EP" to=".U4 > .VSS" width={.1}
 pcbPath={[{x:0,y:0},{x:0.75,y:-0.75},{x:0.75,y:-1.45}]}/>
 <trace name="CHARGER_EN1_PULLDOWN" from=".U4 > .EN1" to=".R6 > .pin1" width={.15} pcbPath={[{x:-.25,y:-2.3},{x:.825,y:-3.375}]}/>
 <trace name="CHARGER_EN2_PULLDOWN" from=".U4 > .EN2" to=".R7 > .pin1" width={.15} pcbPath={[{x:-.75,y:-2.1},{x:-4.825,y:-2.1}]}/>
 <R name="R3" resistance="4.42k" pcbX={12} pcbY={11.8} schX={-6} schY={5} schSectionName="power" connections={{pin1:N("ISET"),pin2:N("GND")}}/>
 <R name="R4" resistance="3.09k" pcbX={19} pcbY={9} schX={-9} schY={8} schSectionName="power" connections={{pin1:N("ILIM"),pin2:N("GND")}}/>
 <R name="R5" resistance="30k" pcbX={15} pcbY={12} schX={-6} schY={8} schSectionName="power" connections={{pin1:N("TMR"),pin2:N("GND")}}/>
 <R name="R6" resistance="100k" pcbX={15} pcbY={4.5} pcbRotation={180} schX={-13} schY={-4} schSectionName="power" connections={{pin1:N("CHG_EN1"),pin2:N("GND")}}/>
 <R name="R7" resistance="100k" pcbX={11} pcbY={4.5} schX={-10} schY={-4} schSectionName="power" connections={{pin1:N("CHG_EN2"),pin2:N("GND")}}/>
 <R name="R8" resistance="10k" pcbX={19} pcbY={4.5} pcbRotation={180} schX={-7} schY={-4} schSectionName="power" connections={{pin1:N("V3V3"),pin2:N("PGOOD")}}/>
 <R name="R9" resistance="10k" pcbX={23} pcbY={4.5} schX={-4} schY={-4} schSectionName="power" connections={{pin1:N("V3V3"),pin2:N("CHG_STAT")}}/>
 <R name="R21" resistance="10k" pcbX={11} pcbY={1.5} schX={3} schY={-2} schSectionName="power" connections={{pin1:N("V3V3"),pin2:N("CHG_CE")}}/>
 <R name="R22" resistance="100k" pcbX={23} pcbY={-3} schX={5} schY={-2} schSectionName="power" connections={{pin1:N("NTC"),pin2:N("TEMP_ADC")}}/>
 <R name="R23" resistance="100k" pcbX={23} pcbY={-6} schX={8} schY={-2} schSectionName="power" connections={{pin1:N("TEMP_ADC"),pin2:N("GND")}}/>
 <C name="C19" capacitance="10nF" pcbX={26} pcbY={-4.5} schX={11} schY={-2} schSectionName="power" connections={{pin1:N("TEMP_ADC"),pin2:N("GND")}}/>
 <C name="C2" capacitance="2.2uF" pcbX={18} pcbY={12} schX={-1} schY={8} schSectionName="power" connections={{pin1:N("VBUS"),pin2:N("GND")}}/>
 <C name="C3" capacitance="10uF" footprint="0805" pcbX={19.5} pcbY={6.8} schX={-1} schY={5} schSectionName="power" connections={{pin1:N("SYS"),pin2:N("GND")}}/>
 <C name="C4" capacitance="10uF" footprint="0805" pcbX={10} pcbY={8} schX={-1} schY={2} schSectionName="power" connections={{pin1:N("BAT"),pin2:N("GND")}}/>
 <connector pcbSx={refStyle} name="J2" manufacturerPartNumber="B2B-PH-K-S(LF)(SN)" standard="jst_ph" pinCount={2} footprint={<footprint insertionDirection="from_below">
  {/* JST B2B-PH-K: 2mm pitch; .75mm drill, 1.2 x 1.75mm lands. */}
  <platedhole shape="circular_hole_with_rect_pad" holeDiameter={.75} rectPadWidth={1.2} rectPadHeight={1.75} rectBorderRadius={.25} pcbX={-1} portHints={["pin1"]}/>
  <platedhole shape="circular_hole_with_rect_pad" holeDiameter={.75} rectPadWidth={1.2} rectPadHeight={1.75} rectBorderRadius={.25} pcbX={1} portHints={["pin2"]}/>
  <silkscreenpath route={[{x:-3.05,y:-2.9},{x:3.05,y:-2.9},{x:3.05,y:1.8},{x:-3.05,y:1.8},{x:-3.05,y:-2.9}]}/>
  <courtyardrect width={6.9} height={5.5} pcbY={-.55}/>
 </footprint>} layer="bottom" pcbX={16} pcbY={-15} schX={5} schY={6} schSectionName="power" pinLabels={{pin1:"BAT_POS",pin2:"GND"}} connections={{BAT_POS:N("BAT"),GND:N("GND")}}/>
 <pinheader pcbSx={refStyle} name="J3" doNotPlace pinCount={2} pitch={2.54} manufacturerPartNumber="61300211121" pcbX={23} pcbY={-10} schX={5} schY={2} schSectionName="power" pinLabels={["NTC","GND"]} connections={{pin1:N("NTC"),pin2:N("GND")}}/>
 <chip pcbSx={refStyle} name="U5" pinAttributes={{IN:{requiresPower:true},GND:{requiresGround:true},OUT:{providesPower:true},EN:{isInput:true},NC:{doNotConnect:true}}} manufacturerPartNumber="TLV75533PDBVR" footprint="sot23_5" pcbX={13} pcbY={-5} schX={9} schY={-4} schSectionName="power" noConnect={["NC"]} pinLabels={{pin1:"IN",pin2:"GND",pin3:"EN",pin4:"NC",pin5:"OUT"}} connections={{IN:N("SYS"),GND:N("GND"),EN:N("SYS"),OUT:N("V3V3")}}/>
 <C name="C5" capacitance="1uF" pcbX={9} pcbY={-5} schX={0.4} schY={5} schSectionName="power" connections={{pin1:N("SYS"),pin2:N("GND")}}/>
 <C name="C6" capacitance="4.7uF" footprint="0805" pcbX={17} pcbY={-5} schX={13} schY={-5} schSectionName="power" connections={{pin1:N("V3V3"),pin2:N("GND")}}/>
 </schematicsheet>
 <schematicsheet name="sheet-3" displayName="mcu" sheetIndex={2}>
 <schematicsection name="mcu" displayName="STM32F072CB / HSI48 crystal-less USB / SWD"/>
 <schematicbox name="U1 power" chipRef=".U1" schX={-5.5} schY={0.5} width={2.15} height={1.2} schSectionName="mcu"
 pinLabels={{pin1:"VDD1",pin2:"VDD2",pin3:"VDDA",pin4:"VDDIO2",pin5:"VBAT",pin6:"VSS1",pin7:"VSS2",pin8:"VSS3",pin9:"VSSA"}}
 schPinArrangement={{leftSide:["pin1","pin2","pin3","pin4","pin5"],rightSide:["pin6","pin7","pin8","pin9"]}}/>
 <schematicbox name="U1 IO" chipRef=".U1" schX={2.5} schY={-1.5} width={1.96} height={2.4} schSectionName="mcu"
 pinLabels={{pin1:"PA0",pin2:"PA1",pin3:"PA2",pin4:"PA3",pin5:"PA4",pin6:"PA5",pin7:"PA6",pin8:"PA7",pin9:"PB0",pin10:"PB6",pin11:"PB7",pin12:"PA11",pin13:"PA12",pin14:"PA13",pin15:"PA14",pin16:"NRST",pin17:"BOOT0",pin18:"PB1",pin19:"PB2"}}
 schPinArrangement={{leftSide:["pin1","pin2","pin3","pin4","pin5","pin6","pin7","pin8","pin9"],rightSide:["pin10","pin11","pin12","pin13","pin14","pin15","pin16","pin17","pin18","pin19"]}}/>

 {[
  ["C7",-15.5,-1.7,-10.5,1.9],["C8",-11,-1.4,-9.1,1.9],["C9",-5.2,7.5,-10.5,0.5],["C10",-14.5,11.5,-9.1,0.5],["C11",-18.5,2.5,-10.5,-0.9]
 ].map(([n,x,y,sx,sy])=><C name={n} capacitance="100nF" maxDecouplingTraceLength={4} pcbX={x} pcbY={y} pcbRotation={n==="C8"?180:n==="C9"?-90:n==="C11"?90:0} schX={sx} schY={sy} schSectionName="mcu" connections={undefined}/>)}
 <trace name="MCU_VBAT_DECAP" from=".U1 > .VBAT" to=".C7 > .pin1" width={.15} pcbPath={[{x:-5.2,y:2.75}]}/>
 <trace name="MCU_VBAT_GROUND" from=".C7 > .pin2" to=".C8 > .pin2" width={.15} pcbPath={[{x:2.9,y:0}]}/>
 <trace name="MCU_VDDA_DECAP" from=".U1 > .VDDA" to=".C8 > .pin1" width={.15} pcbPath={[{x:-5.2,y:-1.25}]}/>
 <trace name="MCU_VSSA_DECAP" from=".U1 > .VSSA" to=".C8 > .pin2" width={.15} pcbPath={[{x:-5.2,y:-0.75}]}/>
 <trace name="MCU_VDD1_DECAP" from=".U1 > .VDD1" to=".C9 > .pin1" width={.15} pcbPath={[{x:2.75,y:-5.5}]}/>
 <trace name="MCU_VSS1_DECAP" from=".U1 > .VSS1" to=".C9 > .pin2" width={.15} pcbPath={[{x:2.25,y:-5.5}]}/>
 <trace name="MCU_VDDIO_DECAP" from=".U1 > .VDDIO2" to=".C10 > .pin1" width={.1} pcbPath={[{x:5.2,y:2.75}]}/>
 <trace name="MCU_VSS2_DECAP" from=".U1 > .VSS2" to=".C10 > .pin2" width={.15} pcbPath={[{x:5.2,y:2.25}]}/>
 <trace name="MCU_VDD2_DECAP" from=".U1 > .VDD2" to=".C11 > .pin1" width={.15} pcbPath={[{x:-2.75,y:5.2}]}/>
 <trace name="MCU_VSS3_DECAP" from=".U1 > .VSS3" to=".C11 > .pin2" width={.1} pcbPath={[{x:-2.25,y:5.2}]}/>
 <C name="C12" capacitance="4.7uF" footprint="0805" pcbX={-13} pcbY={-4} schX={-9.1} schY={-0.9} schSectionName="mcu" connections={{pin1:N("V3V3"),pin2:N("GND")}}/>
 <C name="C13" capacitance="100nF" pcbX={-21} pcbY={-2.5} schX={6.5} schY={-3.5} schSectionName="mcu" connections={{pin1:N("NRST"),pin2:N("GND")}}/>
 <R name="R10" resistance="10k" pcbX={-19} pcbY={5} schX={7.5} schY={0.5} schSectionName="mcu" connections={{pin1:N("BOOT0"),pin2:N("GND")}}/>
 <R name="R11" resistance="10k" pcbX={-22} pcbY={2} schX={7.5} schY={-1.5} schSectionName="mcu" connections={{pin1:N("NRST"),pin2:N("V3V3")}}/>
 <pinheader pcbSx={refStyle} name="J4" doNotPlace schWidth={.675} pinCount={5} pitch={2.54} manufacturerPartNumber="61300511121" pcbX={-14} pcbY={-17} schX={10.5} schY={-1.5} schSectionName="mcu" pinLabels={["VREF","SWDIO","SWCLK","NRST","GND"]} connections={{pin1:N("V3V3"),pin2:N("SWDIO"),pin3:N("SWCLK"),pin4:N("NRST"),pin5:N("GND")}}/>
 <pinheader pcbSx={refStyle} name="J5" doNotPlace pinCount={2} pitch={2.54} manufacturerPartNumber="61300211121" pcbX={-21} pcbY={12} schX={2.5} schY={5.5} schSectionName="mcu" pinLabels={["BOOT0","VREF"]} connections={{pin1:N("BOOT0"),pin2:N("V3V3")}}/>
 </schematicsheet>
 <schematicsheet name="sheet-4" displayName="encoder" sheetIndex={3}>
 <schematicsection name="encoder" displayName="AS5600 0x36 / 3.3V mode / magnet centered on U2"/>
 <AngleSensor pcbSx={refStyle} name="U2" pcbX={0} pcbY={0} schX={-1.7} schY={-2.5} schSectionName="encoder" noConnect={["OUT","PGO"]} connections={{VDD5V:N("V3V3"),VDD3V3:N("V3V3"),GND:N("GND"),DIR:N("GND"),SDA:N("SDA"),SCL:N("SCL")}}/>
 <C name="C14" capacitance="100nF" pcbX={-4.5} pcbY={2.5} pcbRotation={180} schX={3.3} schY={-0.5} schSectionName="encoder" connections={{pin1:N("V3V3"),pin2:N("GND")}}/>
 <C name="C15" capacitance="1uF" pcbX={-4.5} pcbY={-2.5} schX={4.7} schY={-0.5} schSectionName="encoder" connections={{pin1:N("V3V3"),pin2:N("GND")}}/>
 <R name="R12" resistance="4.7k" pcbX={1} pcbY={6} schX={-4.7} schY={2.5} schSectionName="encoder" connections={{pin1:N("V3V3"),pin2:N("SDA")}}/>
 <R name="R13" resistance="4.7k" pcbX={5} pcbY={6} schX={-0.7} schY={2.5} schSectionName="encoder" connections={{pin1:N("V3V3"),pin2:N("SCL")}}/>
 </schematicsheet>
 <schematicsheet name="sheet-5" displayName="memory" sheetIndex={4}>
 <schematicsection name="memory" displayName="32KB FRAM 0x50 / power-fail journal"/>
 <FRAM pcbSx={refStyle} name="U3" pcbX={0} pcbY={-10} schX={-2.5} schY={0} schSectionName="memory" connections={{A0:N("GND"),A1:N("GND"),A2:N("GND"),VSS:N("GND"),WP:N("GND"),SDA:N("SDA"),SCL:N("SCL"),VDD:N("V3V3")}}/>
 <C name="C16" capacitance="100nF" pcbX={4.5} pcbY={-8} schX={2.5} schY={0} schSectionName="memory" connections={{pin1:N("V3V3"),pin2:N("GND")}}/>
 </schematicsheet>
 <schematicsheet name="sheet-6" displayName="controls" sheetIndex={5}>
 <schematicsection name="controls" displayName="Scroll gate / hold 3s to reset count / status / battery sensing"/>
 <switch pcbSx={refStyle} name="SW1" type="spdt" footprint={<footprint>
  {[-2,0,2].map((x,i)=><platedhole shape="circle" holeDiameter={.8} outerDiameter={1.5} pcbX={x} portHints={[`pin${i+1}`]}/>)}
  <hole pcbX={-4.1} diameter={1.5}/><hole pcbX={4.1} diameter={1.5}/>
  <silkscreenpath route={[{x:-4.3,y:2.15},{x:4.3,y:2.15}]}/>
  <silkscreenpath route={[{x:-4.3,y:-2.15},{x:4.3,y:-2.15}]}/>
  {[-4.3,4.3].map(x=><Fragment key={x}><silkscreenpath route={[{x,y:-2.15},{x,y:-1.1}]}/><silkscreenpath route={[{x,y:1.1},{x,y:2.15}]}/></Fragment>)}<courtyardrect width={10.9} height={4.8}/>
 </footprint>} manufacturerPartNumber="OS102011MS2QN1" pcbX={-28} pcbY={-1} pcbRotation={90} schX={-8} schY={3} schSectionName="controls" noConnect={["pin3"]} connections={{pin1:N("GND"),pin2:N("SCROLL_EN")}}/>
 <R name="R14" resistance="10k" pcbX={-21} pcbY={-6} schX={-10} schY={3} schSectionName="controls" connections={{pin1:N("SCROLL_EN"),pin2:N("V3V3")}}/>
 <TS_1088_AR02016 pcbSx={refStyle} name="SW2" schRotation={-90} pcbX={0} pcbY={-27} schX={-2} schY={3} schSectionName="controls" connections={{pin1:N("COUNT_RESET"),pin2:N("GND")}}/>
 <R name="R15" resistance="10k" pcbX={-4} pcbY={-23} schX={0} schY={3} schSectionName="controls" connections={{pin1:N("COUNT_RESET"),pin2:N("V3V3")}}/>
 <led pcbSx={refStyle} name="LED1" footprint="0603" manufacturerPartNumber="LTST-C190KGKT" color="green" schRotation={-90} pcbX={8} pcbY={-26} schX={8} schY={3} schSectionName="controls" connections={{anode:N("LED_A"),cathode:N("GND")}}/>
 <R name="R16" resistance="1k" pcbX={8} pcbY={-23} schX={5} schY={3} schSectionName="controls" connections={{pin1:N("LED"),pin2:N("LED_A")}}/>
 <R name="R17" resistance="1M" pcbX={8} pcbY={-12} pcbRotation={180} schX={0} schY={-3} schSectionName="controls" connections={{pin1:N("BAT"),pin2:N("BAT_ADC")}}/>
 <R name="R18" resistance="1M" pcbX={8} pcbY={-15} schX={0} schY={-6} schSectionName="controls" connections={{pin1:N("BAT_ADC"),pin2:N("GND")}}/>
 <C name="C17" capacitance="100nF" pcbX={8} pcbY={-18} schX={1.5} schY={-6} schSectionName="controls" connections={{pin1:N("BAT_ADC"),pin2:N("GND")}}/>
 <R name="R19" resistance="1M" pcbX={-7} pcbY={16} pcbRotation={180} schX={7} schY={-3} schSectionName="controls" connections={{pin1:N("VBUS"),pin2:N("VBUS_ADC")}}/>
 <R name="R20" resistance="470k" pcbX={-11} pcbY={16} pcbRotation={180} schX={7} schY={-6} schSectionName="controls" connections={{pin1:N("VBUS_ADC"),pin2:N("GND")}}/>
 <C name="C18" capacitance="100nF" pcbX={-15} pcbY={16} schX={8.5} schY={-6} schSectionName="controls" connections={{pin1:N("VBUS_ADC"),pin2:N("GND")}}/>
 </schematicsheet>
 <via name="GND_USB_L" pcbX={-6} pcbY={19.5} holeDiameter={.3} outerDiameter={.7} connectsTo="net.GND" tented/>
 <via name="GND_USB_R" pcbX={6} pcbY={19.5} holeDiameter={.3} outerDiameter={.7} connectsTo="net.GND" tented/>
 <via name="GND_CHARGE" pcbX={17.5} pcbY={10} holeDiameter={.3} outerDiameter={.7} connectsTo="net.GND" tented/>
 <via name="GND_SENSOR" pcbX={4.5} pcbY={-3} holeDiameter={.3} outerDiameter={.7} connectsTo="net.GND" tented/>
 <copperpour name="GROUND_TOP" layer="top" connectsTo="net.GND" clearance={.2} boardEdgeMargin={.4} cutoutMargin={.3} useThermalReliefs/>
 <copperpour name="GROUND_BOTTOM" layer="bottom" connectsTo="net.GND" clearance={.2} boardEdgeMargin={.4} cutoutMargin={.3} useThermalReliefs/>
 <silkscreentext text="DESK KNOB A1" pcbX={0} pcbY={12} fontSize={1.1}/>
 <silkscreentext text="USB-C" pcbX={0} pcbY={21} fontSize={.8}/>
 <silkscreentext text="BAT+ / GND" pcbX={16} pcbY={-19} fontSize={.8} layer="bottom"/>
 <silkscreentext text="RESET 3s" pcbX={0} pcbY={-30.5} fontSize={.8}/>
</board>
