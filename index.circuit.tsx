import { Fragment } from "react"
import { fp } from "@tscircuit/footprinter"
import { routeBoard } from "./routing"
import { TS_1088_AR02016 } from "./imports/TS_1088_AR02016"
import { MCU, OpticalSensor, FRAM, Charger, mcuPins, phFootprint, toggleFootprint } from "./parts"
import { TYPE_C_31_M_12 } from "./imports/TYPE_C_31_M_12"
import type { PartsEngine } from "@tscircuit/props"
const refStyle={"& silkscreentext":{visibility:"hidden" as const}}
const fixedParts: PartsEngine = {findPart:({sourceComponent})=>sourceComponent.type==="source_component"?sourceComponent.supplier_part_numbers??{}:{}}
const resistorMpns: Record<string,string>={"5.1k":"RC0603FR-075K1L","4.42k":"RC0603FR-074K42L","3.09k":"RC0603FR-073K09L","30k":"RC0603FR-0730KL","100k":"RC0603FR-07100KL","10k":"RC0603FR-0710KL","4.7k":"RC0603FR-074K7L","1k":"RC0603FR-071KL","1M":"RC0603FR-071ML","470k":"RC0603FR-07470KL","150":"RC0603FR-07150RL","22k":"RC0603FR-0722KL","22":"RC0603FR-0722RL"}
const capacitorMpns: Record<string,string>={"100nF":"GRM188R71C104KA01D","1uF":"GRM188R61A105KA61D","4.7uF":"GRM21BR61A475KA73L","10nF":"GRM188R71H103KA01D","2.2uF":"GRM188R61C225KE11D","10uF":"GRM21BR61C106KE15L"}
const R=(p:any)=><resistor manufacturerPartNumber={resistorMpns[p.resistance]} pcbSx={refStyle} footprint="0603" schRotation={p.connections?.pin2==="net.V3V3"?90:-90} {...p}/>
// Preserve the locked 0603 copper/courtyard; omit body ink only at two crowded sites.
const dense0603=fp.string("0603").circuitJson().filter(p=>p.type!=="pcb_silkscreen_path")
const C=(p:any)=><capacitor manufacturerPartNumber={capacitorMpns[p.capacitance]} pcbSx={refStyle} footprint={["C7","C14"].includes(p.name)?dense0603:"0603"} schRotation={-90} {...p}/>

const N=(name:string)=>`net.${name}`
const pos=[[-30,15],[30,15],[-30,-15],[30,-15]]
const used=["VBAT","NRST","VSSA","VDDA","PA0","PA1","PA2","PA3","PA4","PA5","PA6","PA7","PB0","PB1","PB2","VSS1","VDD1","PA11","PA12","PA13","VSS2","VDDIO2","PA14","PB6","PB7","PB4","PB5","PB10","PB11","PA8","PB13","PB14","PB15","BOOT0","VSS3","VDD2"]
export default () => <board name="DESK_KNOB_REVC" title="Low-profile display scroll ring — Rev C" width={68} height={68}
 outline={Array.from({length:144},(_,i)=>({x:Math.max(-34,Math.min(34,36*Math.cos(i*Math.PI/72))),y:Math.max(-34,Math.min(34,36*Math.sin(i*Math.PI/72)))}))}
 layers={2} thickness={1.6} minTraceWidth={.1} minBoardEdgeClearance={.3} minTraceToHoleEdgeClearance={.25}
 minViaHoleDiameter={.3} minViaPadDiameter={.7} pcbStyle={{viaHoleDiameter:.3,viaPadDiameter:.7}}
 minTraceToPadEdgeClearance={.15} minPadEdgeToPadEdgeClearance={.15} minViaEdgeToPadEdgeClearance={.15}
 minViaHoleEdgeToViaHoleEdgeClearance={.55} minPlatedHoleDrillEdgeToDrillEdgeClearance={.25}
 partsEngine={fixedParts} schLayout={{layoutMode:"relative"}} autorouter={{local:true,algorithmFn:routeBoard,traceClearance:.15,allowViaInPad:false}} >
 <net name="GND" isGroundNet nominalTraceWidth={.25}/><net name="V3V3" isPowerNet nominalTraceWidth={.25}/><net name="VBUS" isPowerNet nominalTraceWidth={.25}/><net name="SYS" isPowerNet nominalTraceWidth={.25}/><net name="BAT" isPowerNet nominalTraceWidth={.25}/>
 <net name="NRST"/><net name="BOOT0"/><net name="SCROLL_EN"/><net name="COUNT_RESET"/><net name="CHG_EN1"/><net name="CHG_EN2"/><net name="PGOOD"/><net name="CHG_STAT"/><net name="LED"/><net name="BAT_ADC"/><net name="VBUS_ADC"/><net name="TEMP_ADC"/><net name="CHG_CE"/><net name="USB_DM"/><net name="USB_DP"/><net name="SWDIO"/><net name="SWCLK"/><net name="SCL"/><net name="SDA"/><net name="CC1"/><net name="CC2"/><net name="NTC"/><net name="ILIM"/><net name="TMR"/><net name="ISET"/><net name="LED_A"/><net name="IR_A"/><net name="OPT_A"/><net name="OPT_B"/><net name="ENC_A"/><net name="ENC_B"/><net name="LCD_RST"/><net name="LCD_BL"/><net name="LCD_CS"/><net name="SPI_SCK"/><net name="LCD_DC"/><net name="SPI_MOSI"/><net name="LCD_SCK"/><net name="LCD_MOSI"/>
 <cutout name="BATTERY_AND_LCD_POCKET" shape="polygon" points={Array.from({length:4},(_,corner)=>Array.from({length:9},(_,i)=>{const a=(corner*90+i*90/8)*Math.PI/180;const cx=corner===0||corner===3?14.8:-15.8;const cy=corner<2?16.8:-19.8;return {x:cx+2*Math.cos(a),y:cy+2*Math.sin(a)}})).flat()}/>
 {pos.map(([x,y],i)=><Fragment key={i}><hole name={`H${i+1}`} diameter={2.7} pcbX={x} pcbY={y}/></Fragment>)}
 <MCU pcbSx={refStyle} name="U1" pcbX={25.2} pcbY={0} pcbRotation={90} noSchematicRepresentation noConnect={mcuPins.filter(p=>!used.includes(p))}
 connections={{VBAT:N("V3V3"),VDD1:N("V3V3"),VDD2:N("V3V3"),VDDIO2:N("V3V3"),VDDA:N("V3V3"),VSS1:N("GND"),VSS2:N("GND"),VSS3:N("GND"),VSSA:N("GND"),NRST:N("NRST"),BOOT0:N("BOOT0"),PA0:N("SCROLL_EN"),PA1:N("COUNT_RESET"),PA2:N("CHG_EN1"),PA3:N("CHG_EN2"),PA4:N("PGOOD"),PA5:N("CHG_STAT"),PA6:N("LED"),PA7:N("BAT_ADC"),PB0:N("VBUS_ADC"),PB1:N("TEMP_ADC"),PB2:N("CHG_CE"),PA11:N("USB_DM"),PA12:N("USB_DP"),PA13:N("SWDIO"),PA14:N("SWCLK"),PB6:N("SCL"),PB7:N("SDA"),PB4:N("ENC_A"),PB5:N("ENC_B"),PB10:N("LCD_RST"),PB11:N("LCD_BL"),PA8:N("LCD_CS"),PB13:N("SPI_SCK"),PB14:N("LCD_DC"),PB15:N("SPI_MOSI")}}/>
 <schematicsheet name="sheet-1" displayName="usb" sheetIndex={0}>
 <schematicsection name="usb" displayName="USB-C / ESD / CC sink resistors"/>
 <TYPE_C_31_M_12 pcbSx={refStyle} name="J1" schWidth={1.5} pcbX={0} pcbY={28} pcbRotation={180} schX={-7} schY={-2} schSectionName="usb" noConnect={["SBU1","SBU2"]}
 connections={{EH1:N("GND"),EH2:N("GND"),EH3:N("GND"),EH4:N("GND"),GND1:N("GND"),GND2:N("GND"),VBUS1:N("VBUS"),VBUS2:N("VBUS"),DP1:N("USB_DP"),DP2:N("USB_DP"),DN1:N("USB_DM"),DN2:N("USB_DM")}}/>
 <R name="R1" resistance="5.1k" pcbX={8} pcbY={27} schX={-2} schY={1} schSectionName="usb" connections={{pin1:N("CC1"),pin2:N("GND")}}/>
 <R name="R2" resistance="5.1k" pcbX={-8} pcbRotation={180} pcbY={27} schX={-2} schY={-2} schSectionName="usb" connections={{pin1:N("CC2"),pin2:N("GND")}}/>
 <trace name="USB_CC1_RD" from=".J1 > .CC1" to=".R1 > .pin1" width={.1}/>
 <trace name="USB_CC2_RD" from=".J1 > .CC2" to=".R2 > .pin1" width={.1}/>
 <chip pcbSx={refStyle} name="U6" pinAttributes={{VBUS:{requiresPower:true},GND:{requiresGround:true},DM_IN:{isPassive:true},DM_OUT:{isPassive:true},DP_IN:{isPassive:true},DP_OUT:{isPassive:true}}} manufacturerPartNumber="USBLC6-2SC6" footprint="sot23_6" pcbX={10} pcbY={22} pcbRotation={180} schX={3} schY={-1} schSectionName="usb"
 pinLabels={{pin1:"DM_IN",pin2:"GND",pin3:"DP_IN",pin4:"DP_OUT",pin5:"VBUS",pin6:"DM_OUT"}}
 connections={{DM_IN:N("USB_DM"),GND:N("GND"),DP_IN:N("USB_DP"),DP_OUT:N("USB_DP"),VBUS:N("VBUS"),DM_OUT:N("USB_DM")}}/>
 <C name="C1" capacitance="100nF" pcbX={14} pcbY={21.5} schX={7} schY={-1} schSectionName="usb" connections={{pin1:N("VBUS"),pin2:N("GND")}}/>
 <diode pcbSx={refStyle} name="D1" manufacturerPartNumber="PESD5V0S1BA,115" variant="tvs" schRotation={90} footprint="sod323" pcbX={18.5} pcbY={21.5} schX={7} schY={2} schSectionName="usb" connections={{anode:N("GND"),cathode:N("VBUS")}}/>
 </schematicsheet>
 <schematicsheet name="sheet-2" displayName="power" sheetIndex={1}>
 <schematicsection name="power" displayName="Charging and power"/>
 <Charger pcbSx={refStyle} name="U4" pcbX={5} pcbY={-29} pcbRotation={270} schX={-9} schY={2} schSectionName="power" noConnect={["ITERM"]}
 connections={{TS:N("NTC"),BAT1:N("BAT"),BAT2:N("BAT"),CE:N("CHG_CE"),PGOOD:N("PGOOD"),VSS:N("GND"),CHG:N("CHG_STAT"),OUT1:N("SYS"),OUT2:N("SYS"),ILIM:N("ILIM"),IN:N("VBUS"),TMR:N("TMR"),ISET:N("ISET")}}/>
 <trace name="CHARGER_EP_GROUND" from=".U4 > .EP" to=".U4 > .VSS" width={.1}
 pcbPath={[{x:0,y:0},{x:0.75,y:-0.75},{x:0.75,y:-1.45}]}/>
 <trace name="CHARGER_EN1_PULLDOWN" from=".U4 > .EN1" to=".R6 > .pin1" width={.15} pcbPath={[{x:-.25,y:-2.4}]}/>
 <trace name="CHARGER_EN2_PULLDOWN" from=".U4 > .EN2" to=".R7 > .pin1" width={.15} pcbPath={[{x:-.75,y:-1.9},{x:-4.825,y:-1.9}]}/>
 <R name="R3" resistance="4.42k" pcbX={8.8} pcbY={-26} pcbRotation={270} schX={-6} schY={5} schSectionName="power" connections={{pin1:N("ISET"),pin2:N("GND")}}/>
 <R name="R4" resistance="3.09k" pcbX={8.6} pcbY={-32} pcbRotation={270} schX={-9} schY={8} schSectionName="power" connections={{pin1:N("ILIM"),pin2:N("GND")}}/>
 <R name="R5" resistance="30k" pcbX={9} pcbY={-29} pcbRotation={270} schX={-6} schY={8} schSectionName="power" connections={{pin1:N("TMR"),pin2:N("GND")}}/>
 <R name="R6" resistance="100k" pcbX={1.5} pcbY={-28.75} pcbRotation={180} schX={-13} schY={-4} schSectionName="power" connections={{pin1:N("CHG_EN1"),pin2:N("GND")}}/>
 <R name="R7" resistance="100k" pcbX={1.5} pcbY={-25} pcbRotation={270} schX={-10} schY={-4} schSectionName="power" connections={{pin1:N("CHG_EN2"),pin2:N("GND")}}/>
 <R name="R8" resistance="10k" pcbX={27} pcbY={19.5} pcbRotation={180} schX={-7} schY={-4} schSectionName="power" connections={{pin1:N("V3V3"),pin2:N("PGOOD")}}/>
 <R name="R9" resistance="10k" pcbX={26} pcbY={22} schX={-4} schY={-4} schSectionName="power" connections={{pin1:N("V3V3"),pin2:N("CHG_STAT")}}/>
 <R name="R21" resistance="10k" pcbX={-1.5} pcbY={-25} pcbRotation={270} schX={3} schY={-2} schSectionName="power" connections={{pin1:N("V3V3"),pin2:N("CHG_CE")}}/>
 <R name="R22" resistance="100k" pcbX={-28} pcbY={-7} schX={5} schY={-2} schSectionName="power" connections={{pin1:N("NTC"),pin2:N("TEMP_ADC")}}/>
 <R name="R23" resistance="100k" pcbX={-31} pcbY={-7} schX={8} schY={-2} schSectionName="power" connections={{pin1:N("TEMP_ADC"),pin2:N("GND")}}/>
 <C name="C19" capacitance="10nF" pcbX={-30} pcbY={-4} schX={11} schY={-2} schSectionName="power" connections={{pin1:N("TEMP_ADC"),pin2:N("GND")}}/>
 <C name="C2" capacitance="2.2uF" pcbX={12} pcbY={-31} pcbRotation={270} schX={-1} schY={8} schSectionName="power" connections={{pin1:N("VBUS"),pin2:N("GND")}}/>
 <C name="C3" capacitance="10uF" footprint="0805" pcbX={1.5} pcbY={-32} pcbRotation={270} schX={-1} schY={5} schSectionName="power" connections={{pin1:N("SYS"),pin2:N("GND")}}/>
 <C name="C4" capacitance="10uF" footprint="0805" pcbX={5} pcbY={-24} pcbRotation={270} schX={-1} schY={2} schSectionName="power" connections={{pin1:N("BAT"),pin2:N("GND")}}/>
 <connector pcbSx={refStyle} name="J2" manufacturerPartNumber="S2B-PH-K-S(LF)(SN)" standard="jst_ph" pinCount={2} footprint={phFootprint(2,true)} layer="top" pcbX={18.5} pcbY={-9} pcbRotation={270} schX={5} schY={6} schSectionName="power" pinLabels={{pin1:"BAT_POS",pin2:"GND"}} connections={{BAT_POS:N("BAT"),GND:N("GND")}}/>
 <pinheader pcbSx={refStyle} name="J3" doNotPlace pinCount={2} pitch={2.54} manufacturerPartNumber="61300211121" pcbX={-11} pcbY={-24} schX={5} schY={2} schSectionName="power" pinLabels={["NTC","GND"]} connections={{pin1:N("NTC"),pin2:N("GND")}}/>
 <chip pcbSx={refStyle} name="U5" pinAttributes={{IN:{requiresPower:true},GND:{requiresGround:true},OUT:{providesPower:true},EN:{isInput:true},NC:{doNotConnect:true}}} manufacturerPartNumber="TLV75533PDBVR" footprint="sot23_5" pcbX={-18} pcbY={-28} schX={9} schY={-4} schSectionName="power" noConnect={["NC"]} pinLabels={{pin1:"IN",pin2:"GND",pin3:"EN",pin4:"NC",pin5:"OUT"}} connections={{IN:N("SYS"),GND:N("GND"),EN:N("SYS"),OUT:N("V3V3")}}/>
 <C name="C5" capacitance="1uF" pcbX={-14} pcbY={-28} schX={0.4} schY={5} schSectionName="power" connections={{pin1:N("SYS"),pin2:N("GND")}}/>
 <C name="C6" capacitance="4.7uF" footprint="0805" pcbX={-22} pcbY={-25} schX={13} schY={-5} schSectionName="power" connections={{pin1:N("V3V3"),pin2:N("GND")}}/>
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
  ["C7",22.2,-7,-10.5,1.9],["C8",26.2,-6.4,-9.1,1.9],["C9",32,2.5,-10.5,0.5],["C10",22.7,6.5,-9.1,0.5],["C11",18.7,-2.5,-10.5,-0.9]
 ].map(([n,x,y,sx,sy])=><C key={n} name={n} capacitance="100nF" maxDecouplingTraceLength={4} pcbX={x} pcbY={y} pcbRotation={n==="C8"?180:n==="C9"?-90:n==="C11"?90:0} schX={sx} schY={sy} schSectionName="mcu" connections={undefined}/>)}
 <trace name="MCU_VBAT_DECAP" from=".U1 > .VBAT" to=".C7 > .pin1" width={.15} pcbPath={[{x:-5.2,y:2.75}]}/>
 <trace name="MCU_VBAT_GROUND" from=".C7 > .pin2" to=".C8 > .pin2" width={.1} pcbPath={[{x:2.9,y:0}]}/>
 <trace name="MCU_VDDA_DECAP" from=".U1 > .VDDA" to=".C8 > .pin1" width={.1} pcbPath={[{x:-5.2,y:-1.25}]}/>
 <trace name="MCU_VSSA_DECAP" from=".U1 > .VSSA" to=".C8 > .pin2" width={.15} pcbPath={[{x:-5.2,y:-0.75}]}/>
 <trace name="MCU_VDD1_DECAP" from=".U1 > .VDD1" to=".C9 > .pin1" width={.1} pcbPath={[{x:2.75,y:-5.5}]}/>
 <trace name="MCU_VSS1_DECAP" from=".U1 > .VSS1" to=".C9 > .pin2" width={.15} pcbPath={[{x:2.25,y:-5.5}]}/>
 <trace name="MCU_VDDIO_DECAP" from=".U1 > .VDDIO2" to=".C10 > .pin1" width={.1} pcbPath={[{x:5.2,y:2.75}]}/>
 <trace name="MCU_VSS2_DECAP" from=".U1 > .VSS2" to=".C10 > .pin2" width={.15} pcbPath={[{x:5.2,y:2.25}]}/>
 <trace name="MCU_VDD2_DECAP" from=".U1 > .VDD2" to=".C11 > .pin1" width={.15} pcbPath={[{x:-2.75,y:5.2}]}/>
 <trace name="MCU_VSS3_DECAP" from=".U1 > .VSS3" to=".C11 > .pin2" width={.1} pcbPath={[{x:-2.25,y:5.2}]}/>
 <C name="C12" capacitance="4.7uF" footprint="0805" pcbX={24.2} pcbY={-9} schX={-9.1} schY={-0.9} schSectionName="mcu" connections={{pin1:N("V3V3"),pin2:N("GND")}}/>
 <C name="C13" capacitance="100nF" pcbX={27.5} pcbY={-12} schX={6.5} schY={-3.5} schSectionName="mcu" connections={{pin1:N("NRST"),pin2:N("GND")}}/>
 <R name="R10" resistance="10k" pcbX={21} pcbY={-16} schX={7.5} schY={0.5} schSectionName="mcu" connections={{pin1:N("BOOT0"),pin2:N("GND")}}/>
 <R name="R11" resistance="10k" pcbX={22} pcbY={-13.8} schX={7.5} schY={-1.5} schSectionName="mcu" connections={{pin1:N("NRST"),pin2:N("V3V3")}}/>
 <connector pcbSx={refStyle} name="J4" schWidth={1.575} standard="jst_ph" pinCount={6} footprint={phFootprint(6)} manufacturerPartNumber="B6B-PH-K-S(LF)(SN)" pcbX={0} pcbY={20.5} pcbRotation={0} schX={10.5} schY={-1.5} schSectionName="mcu" pinLabels={{pin1:"VREF",pin2:"SWDIO",pin3:"SWCLK",pin4:"NRST",pin5:"GND",pin6:"BOOT0"}} connections={{pin1:N("V3V3"),pin2:N("SWDIO"),pin3:N("SWCLK"),pin4:N("NRST"),pin5:N("GND"),pin6:N("BOOT0")}}/>
 <schematicbox name="U1 display encoder" chipRef=".U1" schX={2.5} schY={6.5} width={1.96} height={1.0} schSectionName="mcu" pinLabels={{pin1:"PB4",pin2:"PB5",pin3:"PB10",pin4:"PB11",pin5:"PA8",pin6:"PB13",pin7:"PB14",pin8:"PB15"}} schPinArrangement={{leftSide:["pin1","pin2","pin3","pin4"],rightSide:["pin5","pin6","pin7","pin8"]}}/>
 </schematicsheet>
 <schematicsheet name="sheet-4" displayName="encoder" sheetIndex={3}>
 <schematicsection name="encoder" displayName="48-slot optical ring / common-collector dual sensor / TIM3 quadrature"/>
 <OpticalSensor pcbSx={refStyle} name="U2" schPinArrangement={{leftSide:["pin1","pin2"],rightSide:["pin4","pin5"],topSide:["pin6"],bottomSide:["pin3"]}} pcbX={-23} pcbY={10} pcbRotation={156.501434} schX={-3} schY={0} schSectionName="encoder" noConnect={["NC"]} connections={{A:N("IR_A"),K:N("GND"),COL:N("V3V3"),EA:N("OPT_A"),EB:N("OPT_B")}}/>
 <chip pcbSx={refStyle} name="U7" manufacturerPartNumber="SN74LVC2G17DBVR" footprint="sot23_6" pcbX={-21} pcbY={19.5} schX={1} schY={0} schSectionName="encoder" pinLabels={{pin1:"A1",pin2:"GND",pin3:"A2",pin4:"Y2",pin5:"VCC",pin6:"Y1"}} pinAttributes={{VCC:{requiresPower:true},GND:{requiresGround:true},A1:{isInput:true},A2:{isInput:true},Y1:{isOutput:true},Y2:{isOutput:true}}} connections={{A1:N("OPT_A"),A2:N("OPT_B"),Y1:N("ENC_A"),Y2:N("ENC_B"),VCC:N("V3V3"),GND:N("GND")}}/>
 <R name="R24" resistance="150" pcbX={-28} pcbY={5.5} schX={-9} schY={2.5} schSectionName="encoder" connections={{pin1:N("V3V3"),pin2:N("IR_A")}}/>
 <R name="R25" resistance="22k" pcbX={-25.5} pcbY={18.5} schX={-1} schY={3} schSectionName="encoder" connections={{pin1:N("OPT_A"),pin2:N("GND")}}/>
 <R name="R26" resistance="22k" pcbX={-25.5} pcbY={21.5} schX={2} schY={3} schSectionName="encoder" connections={{pin1:N("OPT_B"),pin2:N("GND")}}/>
 <C name="C14" capacitance="100nF" pcbX={-20} pcbY={22} pcbRotation={180} schX={5} schY={0} schSectionName="encoder" connections={{pin1:N("V3V3"),pin2:N("GND")}}/>
 <R name="R12" resistance="4.7k" pcbX={-20} pcbY={24} pcbRotation={180} schX={-9} schY={-3} schSectionName="encoder" connections={{pin1:N("V3V3"),pin2:N("SDA")}}/>
 <R name="R13" resistance="4.7k" pcbX={-23} pcbY={24} pcbRotation={180} schX={-5} schY={-3} schSectionName="encoder" connections={{pin1:N("V3V3"),pin2:N("SCL")}}/>
 </schematicsheet>
 <schematicsheet name="sheet-5" displayName="memory" sheetIndex={4}>
 <schematicsection name="memory" displayName="32KB FRAM 0x50 / power-fail journal"/>
 <FRAM pcbSx={refStyle} name="U3" pcbX={-15} pcbY={28} schX={-2.5} schY={0} schSectionName="memory" connections={{A0:N("GND"),A1:N("GND"),A2:N("GND"),VSS:N("GND"),WP:N("GND"),SDA:N("SDA"),SCL:N("SCL"),VDD:N("V3V3")}}/>
 <C name="C16" capacitance="100nF" pcbX={-10} pcbY={31} schX={2.5} schY={0} schSectionName="memory" connections={{pin1:N("V3V3"),pin2:N("GND")}}/>
 </schematicsheet>
 <schematicsheet name="sheet-6" displayName="controls" sheetIndex={5}>
 <schematicsection name="controls" displayName="Scroll gate / hold 3s to reset count / status / battery sensing"/>
 <switch pcbSx={refStyle} name="SW1" type="spdt" footprint={toggleFootprint} manufacturerPartNumber="G12AH" pcbX={-20} pcbY={-19} pcbRotation={90} schX={-8} schY={3} schSectionName="controls" pinLabels={{pin1:"T4",pin2:"T5",pin3:"T6",pin4:"SUPPORT1",pin5:"SUPPORT3"}} noConnect={["T6","SUPPORT1","SUPPORT3"]} connections={{pin1:N("GND"),pin2:N("SCROLL_EN")}}/>
 <R name="R14" resistance="10k" pcbX={-29} pcbY={-10} schX={-10} schY={3} schSectionName="controls" connections={{pin1:N("SCROLL_EN"),pin2:N("V3V3")}}/>
 <TS_1088_AR02016 pcbSx={refStyle} name="SW2" schRotation={-90} pcbX={-5} pcbY={-30} schX={-2} schY={3} schSectionName="controls" connections={{pin1:N("COUNT_RESET"),pin2:N("GND")}}/>
 <R name="R15" resistance="10k" pcbX={-11} pcbY={-28} schX={0} schY={3} schSectionName="controls" connections={{pin1:N("COUNT_RESET"),pin2:N("V3V3")}}/>
 <led pcbSx={refStyle} name="LED1" footprint="0603" manufacturerPartNumber="LTST-C190KGKT" color="green" schRotation={-90} pcbX={14} pcbY={-28} schX={8} schY={3} schSectionName="controls" connections={{anode:N("LED_A"),cathode:N("GND")}}/>
 <R name="R16" resistance="1k" pcbX={14} pcbY={-25} schX={5} schY={3} schSectionName="controls" connections={{pin1:N("LED"),pin2:N("LED_A")}}/>
 <R name="R17" resistance="1M" pcbX={21} pcbY={-21} pcbRotation={180} schX={0} schY={-3} schSectionName="controls" connections={{pin1:N("BAT"),pin2:N("BAT_ADC")}}/>
 <R name="R18" resistance="1M" pcbX={24} pcbY={-21} schX={0} schY={-6} schSectionName="controls" connections={{pin1:N("BAT_ADC"),pin2:N("GND")}}/>
 <C name="C17" capacitance="100nF" pcbX={24} pcbY={-24} schX={1.5} schY={-6} schSectionName="controls" connections={{pin1:N("BAT_ADC"),pin2:N("GND")}}/>
 <R name="R19" resistance="1M" pcbX={15} pcbY={25} pcbRotation={180} schX={7} schY={-3} schSectionName="controls" connections={{pin1:N("VBUS"),pin2:N("VBUS_ADC")}}/>
 <R name="R20" resistance="470k" pcbX={18} pcbY={25} pcbRotation={180} schX={7} schY={-6} schSectionName="controls" connections={{pin1:N("VBUS_ADC"),pin2:N("GND")}}/>
 <C name="C18" capacitance="100nF" pcbX={15} pcbY={27} schX={8.5} schY={-6} schSectionName="controls" connections={{pin1:N("VBUS_ADC"),pin2:N("GND")}}/>
 </schematicsheet>
 <schematicsheet name="sheet-7" displayName="display" sheetIndex={6}>
 <schematicsection name="display" displayName="Waveshare 19192 / GC9A01 240x240 / fixed 1.28-inch screen"/>
 <connector pcbSx={refStyle} name="J6" schWidth={1.385} schPinArrangement={{leftSide:["pin1","pin2","pin3","pin4","pin5","pin6","pin7","pin8"]}} standard="jst_ph" pinCount={8} footprint={phFootprint(8,true)} manufacturerPartNumber="S8B-PH-K-S(LF)(SN)" pcbX={-19.5} pcbY={-3.5} pcbRotation={90} schX={2} schY={0} schSectionName="display" pinLabels={{pin1:"BL",pin2:"RST",pin3:"DC",pin4:"CS",pin5:"CLK",pin6:"DIN",pin7:"GND",pin8:"VCC"}} connections={{pin1:N("LCD_BL"),pin2:N("LCD_RST"),pin3:N("LCD_DC"),pin4:N("LCD_CS"),pin5:N("LCD_SCK"),pin6:N("LCD_MOSI"),pin7:N("GND"),pin8:N("V3V3")}}/>
 <R name="R27" resistance="22" pcbX={19} pcbY={17} schX={-3} schY={-.1} schRotation={0} schSectionName="display" connections={{pin1:N("SPI_SCK"),pin2:N("LCD_SCK")}}/>
 <R name="R28" resistance="22" pcbX={22} pcbY={17} schX={-6} schY={-.3} schRotation={0} schSectionName="display" connections={{pin1:N("SPI_MOSI"),pin2:N("LCD_MOSI")}}/>
 <C name="C15" capacitance="1uF" pcbX={-28} pcbY={3} schX={6} schY={0} schSectionName="display" connections={{pin1:N("V3V3"),pin2:N("GND")}}/>
 </schematicsheet>
 <via name="GND_USB_L" pcbX={-8} pcbY={22} holeDiameter={.3} outerDiameter={.7} connectsTo="net.GND" tented/>
 <via name="GND_USB_R" pcbX={7.5} pcbY={24} holeDiameter={.3} outerDiameter={.7} connectsTo="net.GND" tented/>
 <via name="GND_CHARGE" pcbX={7} pcbY={-31.5} holeDiameter={.3} outerDiameter={.7} connectsTo="net.GND" tented/>
 <copperpour name="GROUND_TOP" layer="top" connectsTo="net.GND" clearance={.25} boardEdgeMargin={.4} cutoutMargin={.31} useThermalReliefs/>
 <copperpour name="GROUND_BOTTOM" layer="bottom" connectsTo="net.GND" clearance={.25} boardEdgeMargin={.4} cutoutMargin={.31} useThermalReliefs/>
 <silkscreentext text="DESK KNOB C1" pcbX={-33} pcbY={0} pcbRotation={90} fontSize={.9}/>
 <silkscreentext text="USB-C" pcbX={0} pcbY={32.5} fontSize={.8}/>
 <silkscreentext text="BAT+ / GND" pcbX={30} pcbY={-10} fontSize={.8}/>
 <silkscreentext text="RESET 3s" pcbX={-9} pcbY={-32.5} fontSize={.8}/>
</board>
