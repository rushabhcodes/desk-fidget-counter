import { verifiedRouting } from "./routing/replay"
import rp from "./reference/rp2040.json"
import dimensions from "./mechanical/parameters.json"
import fabrication from "./reference/fabrication-rules.json"
import { packageCad } from "./cad"
import { Fragment } from "react"
import { MCU, BootFlash, ClockCrystal, OpticalSensor, FRAM, mcuPins, JlcChip, JlcConnector, JlcButton, JlcResistor, JlcCapacitor, USB } from "./parts"
import type { PartsEngine } from "@tscircuit/props"
const refStyle={"& silkscreentext":{visibility:"hidden" as const}}
const fixedParts: PartsEngine = {findPart:({sourceComponent})=>sourceComponent.type==="source_component"?sourceComponent.supplier_part_numbers??{}:{}}
const resistorMpns: Record<string,string>={"5.1k":"RC0603FR-075K1L","4.42k":"RC0603FR-074K42L","3.09k":"RC0603FR-073K09L","30k":"RC0603FR-0730KL","100k":"RC0603FR-07100KL","10k":"RC0603FR-0710KL","4.7k":"RC0603FR-074K7L","1k":"0603WAF1001T5E","27":"0603WAF270JT5E","1M":"RC0603FR-071ML","470k":"RC0603FR-07470KL","150":"RC0603FR-07150RL","22k":"RC0603FR-0722KL","22":"RC0603FR-0722RL"}
const capacitorMpns: Record<string,string>={"15pF":"0402CG150J500NT","100nF":"GRM188R71C104KA01D","1uF":"GRM188R61A105KA61D","4.7uF":"CL21A475KOFNNNE","10nF":"GRM155R71H103KA88D","2.2uF":"GRM188R61C225KE11D","10uF":"GRM21BR61C106KE15L"}
const R=(p:any)=><JlcResistor cadModel={packageCad("r0603")} manufacturerPartNumber={resistorMpns[p.resistance]} pcbSx={refStyle} schRotation={p.connections?.pin2==="net.V3V3"?90:-90} {...p}/>
const C=({packageSize="0603",...p}:any)=><JlcCapacitor cadModel={packageCad(packageSize==="0805"?"c0805":packageSize==="0402"?"c0402":"c0603")} manufacturerPartNumber={packageSize==="0402"&&p.capacitance==="100nF"?"GRM155R71C104KA88D":capacitorMpns[p.capacitance]} pcbSx={refStyle} schRotation={-90} {...p}/>

const N=(name:string)=>`net.${name}`
const pos=[[-30,15],[30,15],[-30,-15],[30,-15]]
const usbPosition={x:dimensions.usb_center[0],y:dimensions.usb_center[1]}
// A short integral USB tab brings the receptacle to the shell wall. The
// asymmetric outline's own centre is offset; component coordinates stay fixed.
const boardFrontY=Math.max(...dimensions.pcb_outline.usb_tab.points.map(([,y])=>y))
const boardBackY=Math.min(...dimensions.pcb_outline.button_tab.points.map(([,y])=>y))
const boardCenterY=(boardFrontY+boardBackY)/2
const pcbOutline=(()=>{
 let usbInserted=false,buttonInserted=false
 return Array.from({length:144},(_,i)=>({x:Math.max(-34,Math.min(34,36*Math.cos(i*Math.PI/72))),y:Math.max(-34,Math.min(34,36*Math.sin(i*Math.PI/72)))})).flatMap(p=>{
  if(p.y>=dimensions.pcb_outline.usb_tab.replace_above_y){
   if(usbInserted)return [];usbInserted=true
   return dimensions.pcb_outline.usb_tab.points.map(([x,y])=>({x,y}))
  }
  if(p.y<=dimensions.pcb_outline.button_tab.replace_below_y){
   if(buttonInserted)return [];buttonInserted=true
   return dimensions.pcb_outline.button_tab.points.map(([x,y])=>({x,y}))
  }
  return [p]
 }).map(p=>({x:p.x,y:p.y-boardCenterY}))
})()
const rpConnections={
 ...Object.fromEntries(Object.entries(rp.gpio).map(([net,pin])=>[`GPIO${pin}`,N(net)])),
 ...Object.fromEntries(["IOVDD1","IOVDD2","IOVDD3","IOVDD4","IOVDD5","IOVDD6","VREG_IN","ADC_AVDD","USB_VDD"].map(p=>[p,N("V3V3")])),
 DVDD1:N("V1V1"),DVDD2:N("V1V1"),VREG_VOUT:N("V1V1"),GND:N("GND"),TESTEN:N("GND"),
 RUN:N("RUN"),SWDIO:N("SWDIO"),SWCLK:N("SWCLK"),USB_DM:N("USB_DM_MCU"),USB_DP:N("USB_DP_MCU"),
 XIN:N("XIN"),XOUT:N("XOUT"),
 ...Object.fromEntries(["QSPI_SS","QSPI_SCLK","QSPI_SD0","QSPI_SD1","QSPI_SD2","QSPI_SD3"].map(p=>[p,N(p)]))
}
const bypass: [string,string,number,number,number][]=[
 ["C7","IOVDD1",19.9,2.6,180],["C8","IOVDD2",19.9,-1,180],
 ["C9","IOVDD3",25.4,-5.3,-90],["C10","IOVDD4",30.4,-1,0],
 ["C11","IOVDD5",30.4,2.6,0],["C12","IOVDD6",26.4,5.6,90],
 ["C13","ADC_AVDD",32.5,4.6,0],["C17","USB_VDD",25.75,7.5,90],
 ["C18","DVDD2",25.1,5.6,90],["C19","DVDD1",27,-5.3,-90]
]
export default () => <board name="DESK_KNOB_REVF1" title="USB laptop dashboard and scroll ring — Rev F1" width={68} height={boardFrontY-boardBackY} outlineOffsetY={boardCenterY}
 outline={pcbOutline}
 layers={2} thickness={1.6} minTraceWidth={fabrication.minimum_track_width} minBoardEdgeClearance={fabrication.minimum_copper_to_board_edge} minTraceToHoleEdgeClearance={fabrication.minimum_nonplated_hole_to_copper}
 minViaHoleDiameter={fabrication.fine_via_drill_diameter} minViaPadDiameter={fabrication.fine_via_pad_diameter} pcbStyle={{viaHoleDiameter:fabrication.via_drill_diameter,viaPadDiameter:fabrication.via_pad_diameter}}
 minTraceToPadEdgeClearance={fabrication.minimum_track_and_via_copper_clearance} minPadEdgeToPadEdgeClearance={fabrication.minimum_track_and_via_copper_clearance} minViaEdgeToPadEdgeClearance={fabrication.minimum_track_and_via_copper_clearance}
 minViaHoleEdgeToViaHoleEdgeClearance={fabrication.minimum_via_drill_to_drill} minPlatedHoleDrillEdgeToDrillEdgeClearance={fabrication.minimum_component_plated_drill_to_drill}
 partsEngine={fixedParts} schLayout={{layoutMode:"relative"}} autorouter={{algorithmFn:verifiedRouting,traceClearance:.2,allowViaInPad:false}} autorouterVersion="beta_pipeline9" autorouterEffortLevel="2x" >
 <autoroutingphase name="Whole two-layer board" minBoardEdgeClearance={.6} minTraceWidth={.15} minTraceToPadEdgeClearance={.2} minTraceToHoleEdgeClearance={.35} minPadEdgeToPadEdgeClearance={.15} minPlatedHoleDrillEdgeToDrillEdgeClearance={.25} minViaEdgeToPadEdgeClearance={.3} minViaHoleEdgeToViaHoleEdgeClearance={1}/>
 <net name="V1V1" isPowerNet nominalTraceWidth={.2}/>
 <net name="USB_DM_MCU"/><net name="USB_DP_MCU"/>
 <net name="XIN"/><net name="XOUT"/><net name="XTAL_OUT"/>
 <net name="QSPI_SS"/><net name="QSPI_SCLK"/><net name="QSPI_SD0"/>
 <net name="QSPI_SD1"/><net name="QSPI_SD2"/><net name="QSPI_SD3"/>
 <net name="GND" isGroundNet nominalTraceWidth={.15}/><net name="V3V3" isPowerNet nominalTraceWidth={.15}/><net name="VBUS" isPowerNet nominalTraceWidth={.15}/>
 <net name="PERIPH_3V3" isPowerNet nominalTraceWidth={.15}/><net name="PERIPH_EN" nominalTraceWidth={.15}/><net name="RUN" nominalTraceWidth={.15}/><net name="BOOTSEL" nominalTraceWidth={.15}/><net name="MODE_BTN" nominalTraceWidth={.15}/><net name="USB_DM" nominalTraceWidth={.15}/><net name="USB_DP" nominalTraceWidth={.15}/><net name="SWDIO" nominalTraceWidth={.15}/><net name="SWCLK" nominalTraceWidth={.15}/><net name="SCL" nominalTraceWidth={.15}/><net name="SDA" nominalTraceWidth={.15}/><net name="CC1" nominalTraceWidth={.15}/><net name="CC2" nominalTraceWidth={.15}/><net name="IR_A" nominalTraceWidth={.15}/><net name="OPT_A" nominalTraceWidth={.15}/><net name="OPT_B" nominalTraceWidth={.15}/><net name="ENC_A" nominalTraceWidth={.15}/><net name="ENC_B" nominalTraceWidth={.15}/><net name="LCD_RST" nominalTraceWidth={.15}/><net name="LCD_BL" nominalTraceWidth={.15}/><net name="LCD_CS" nominalTraceWidth={.15}/><net name="SPI_SCK" nominalTraceWidth={.15}/><net name="LCD_DC" nominalTraceWidth={.15}/><net name="SPI_MOSI" nominalTraceWidth={.15}/><net name="LCD_SCK" nominalTraceWidth={.15}/><net name="LCD_MOSI" nominalTraceWidth={.15}/>
 <cutout name="LCD_AND_CABLE_POCKET" shape="polygon" points={Array.from({length:4},(_,corner)=>Array.from({length:9},(_,i)=>{const a=(corner*90+i*90/8)*Math.PI/180;const cx=corner===0||corner===3?14.8:-15.8;const cy=corner<2?16.8:-19.8;return {x:cx+2*Math.cos(a),y:cy+2*Math.sin(a)}})).flat()}/>
 {/* Reserve 0.35 mm outside the window on both copper layers. Connector
     housings may span above this space; their pads remain outside it. */}
 <keepout shape="rect" pcbX={-.5} pcbY={-1.5} width={35.3} height={41.3} layers={["top","bottom"]} allowPlacements/>
 {/* Keep a through-via drill out of the ESD signal land; no bottom-side parts. */}
 <keepout shape="rect" pcbX={5.950904} pcbY={34.54996} width={1.5} height={1} layers={["bottom"]} allowPlacements/>
 {/* Copper guards follow the drill centres of the 180-degree USB footprint. */}
 {[-2.999994,2.999994].map(x=><Fragment key={x}><keepout shape="circle" pcbX={usbPosition.x+x} pcbY={usbPosition.y-.7555294} radius={.55} layers={["top","bottom"]} allowPlacements/></Fragment>)}
 {pos.map(([x,y],i)=><Fragment key={i}><hole name={`H${i+1}`} diameter={2.7} pcbX={x} pcbY={y}/></Fragment>)}
 <MCU pcbSx={refStyle} name="U1" pcbX={25.2} pcbY={0} pcbRotation={0} noSchematicRepresentation noConnect={mcuPins.filter(p=>!(p in rpConnections))} connections={rpConnections}/>
 <schematicsheet name="sheet-1" displayName="USB-C interface and ESD protection" sheetIndex={0}>
 <schematictext text="DESK KNOB F1 — USB-C interface and ESD protection" schX={0} schY={8} fontSize={.4}/>
 <schematicsection name="usb" displayName="USB-C / ESD / CC sink resistors"/>
 {/* The receptacle housing overhangs the PCB nose; copper and drills remain on board. */}
 <USB allowOffBoard pcbSx={refStyle} name="J1" schWidth={1.5} pcbX={usbPosition.x} pcbY={usbPosition.y} pcbRotation={180} schX={-7} schY={-2} schSectionName="usb" noConnect={["SBU1","SBU2"]}
 connections={{EH1:N("GND"),EH2:N("GND"),EH3:N("GND"),EH4:N("GND"),GND1:N("GND"),GND2:N("GND"),GND3:N("GND"),GND4:N("GND"),VBUS1:N("VBUS"),VBUS2:N("VBUS"),VBUS3:N("VBUS"),VBUS4:N("VBUS"),DP1:N("USB_DP"),DP2:N("USB_DP"),DN1:N("USB_DM"),DN2:N("USB_DM")}}/>
 <R name="R1" resistance="5.1k" pcbX={8} pcbY={36.5} schX={-2} schY={1} schSectionName="usb" connections={{pin1:N("CC1"),pin2:N("GND")}}/>
 <R name="R2" resistance="5.1k" pcbX={-8} pcbRotation={180} pcbY={36} schX={-2} schY={-2} schSectionName="usb" connections={{pin1:N("CC2"),pin2:N("GND")}}/>
 <trace name="USB_CC1_RD" from=".R1 > .pin1" to=".J1 > .CC1" width={.15}/>
 <trace name="USB_CC2_RD" from=".J1 > .CC2" to=".R2 > .pin1" width={.15}/>
 <JlcChip pcbSx={refStyle} name="U6" cadModel={packageCad("sot23-6")} pinAttributes={{VBUS:{requiresPower:true},GND:{requiresGround:true},DM_IN:{isPassive:true},DM_OUT:{isPassive:true},DP_IN:{isPassive:true},DP_OUT:{isPassive:true}}} manufacturerPartNumber="USBLC6-2SC6" pcbX={7.1} pcbY={33.6} pcbRotation={0} schX={3} schY={-1} schSectionName="usb"
 pinLabels={{pin1:"DM_IN",pin2:"GND",pin3:"DP_IN",pin4:"DP_OUT",pin5:"VBUS",pin6:"DM_OUT"}}
 connections={{DM_IN:N("USB_DM"),GND:N("GND"),DP_IN:N("USB_DP"),DP_OUT:N("USB_DP"),VBUS:N("VBUS"),DM_OUT:N("USB_DM")}}/>
 <C name="C1" capacitance="100nF" pcbX={10.8} pcbY={33.4} pcbRotation={90} schX={7} schY={-1} schSectionName="usb" connections={{pin1:N("VBUS"),pin2:N("GND")}}/>
 <schematictext text="USBLC6-2SC6: USB 2.0 data ESD clamp; VBUS reference = 5V" schX={3} schY={-4} fontSize={.22}/>
 </schematicsheet>
 <schematicsheet name="sheet-2" displayName="USB power and switched peripherals" sheetIndex={1}>
 <schematictext text="DESK KNOB F1 — USB power and switched peripherals" schX={0} schY={8} fontSize={.4}/>
 <schematicsection name="power" displayName="5V USB / 3.3V logic / suspend-controlled display and encoder"/>
 <JlcChip pcbSx={refStyle} name="U4" cadModel={packageCad("sc70-6")} manufacturerPartNumber="TPS22919DCKR" pcbX={5} pcbY={-29} schX={3} schY={1} schSectionName="power" pinLabels={{pin1:"IN",pin2:"GND",pin3:"ON",pin4:"NC",pin5:"QOD",pin6:"VOUT"}} noConnect={["NC"]} pinAttributes={{IN:{requiresPower:true},GND:{requiresGround:true},ON:{isInput:true},VOUT:{providesPower:true},QOD:{isPassive:true},NC:{doNotConnect:true}}} connections={{IN:N("V3V3"),GND:N("GND"),ON:N("PERIPH_EN"),QOD:N("PERIPH_3V3"),VOUT:N("PERIPH_3V3")}}/>
 <C name="C2" capacitance="1uF" pcbX={9} pcbY={-29} schX={-2} schY={-0.5} schSectionName="power" connections={{pin1:N("V3V3"),pin2:N("GND")}}/>
 <C name="C3" capacitance="1uF" pcbX={9} pcbY={-32} schX={6} schY={1} schSectionName="power" connections={{pin1:N("PERIPH_3V3"),pin2:N("GND")}}/>
 <R name="R21" resistance="100k" pcbX={1.5} pcbY={-25} pcbRotation={270} schX={3} schY={-2} schSectionName="power" connections={{pin1:N("PERIPH_EN"),pin2:N("GND")}}/>
 <JlcChip pcbSx={refStyle} name="U5" cadModel={packageCad("sot23-5")} pinAttributes={{IN:{requiresPower:true},GND:{requiresGround:true},OUT:{providesPower:true},EN:{isInput:true},NC:{doNotConnect:true}}} manufacturerPartNumber="TLV75533PDBVR" pcbX={-18} pcbY={-27.5} schX={-5} schY={1} schSectionName="power" noConnect={["NC"]} pinLabels={{pin1:"IN",pin2:"GND",pin3:"EN",pin4:"NC",pin5:"OUT"}} connections={{IN:N("VBUS"),GND:N("GND"),EN:N("VBUS"),OUT:N("V3V3")}}/>
 <C name="C5" capacitance="1uF" pcbX={-14} pcbY={-28} schX={-9} schY={0} schSectionName="power" connections={{pin1:N("VBUS"),pin2:N("GND")}}/>
 <C name="C6" capacitance="4.7uF" packageSize="0805" pcbX={-22.6} pcbY={-25} schX={-2} schY={-1.7} schSectionName="power" connections={{pin1:N("V3V3"),pin2:N("GND")}}/>
 <schematictext text="TLV75533: 5V USB to 3.3V; 500mA rated; C5/C6 ceramic" schX={0} schY={5.2} fontSize={.22}/>
 <schematictext text="TPS22919: 1.5A load switch; GPIO1 low disables LCD and IR" schX={0} schY={4.2} fontSize={.22}/>
 </schematicsheet>
 <schematicsheet name="sheet-3" displayName="RP2040 power, controls and programming" sheetIndex={2}>
 <schematictext text="DESK KNOB F1 — RP2040 power, controls and programming" schX={0} schY={10.8} fontSize={.35}/>
 <schematicsection name="mcu" displayName="RP2040 / local bypassing / 1.1V core regulator / SWD"/>
 <schematicbox name="U1 power" chipRef=".U1" schX={-3} schY={6} width={2.7} height={1.8} schSectionName="mcu"
 pinLabels={{pin1:"IOVDD1",pin10:"IOVDD2",pin22:"IOVDD3",pin33:"IOVDD4",pin42:"IOVDD5",pin49:"IOVDD6",pin48:"USB_VDD",pin43:"ADC_AVDD",pin44:"VREG_IN",pin45:"VREG_VOUT",pin23:"DVDD1",pin50:"DVDD2",pin57:"GND",pin19:"TESTEN"}}
 schPinArrangement={{leftSide:["pin1","pin10","pin22","pin33","pin42","pin49","pin48","pin43"],rightSide:["pin44","pin45","pin23","pin50","pin57","pin19"]}}/>
 {bypass.map(([name,pin,x,y,rotation],i)=><C key={name} name={name} packageSize="0402" capacitance="100nF" maxDecouplingTraceLength={6} pcbX={x} pcbY={y} pcbRotation={rotation} schX={i<8?-7+(i%5)*1.4:3+(i-8)*1.4} schY={i<8?2.5-Math.floor(i/5)*1.5:2.5} schRotation={270} schSectionName="mcu" connections={{pin2:N("GND")}}/>)}
 {bypass.map(([name,pin])=><trace key={name} name={`RP2040_${pin}_BYPASS`} maxLength={6} from={`.U1 > .${pin}`} to={`.${name} > .pin1`} width={.15}/>)}
 <C name="C20" capacitance="1uF" maxDecouplingTraceLength={6} pcbX={30.6} pcbY={5.6} pcbRotation={90} schX={-2.8} schY={1} schRotation={270} schSectionName="mcu" connections={{pin2:N("GND")}}/>
 <C name="C21" capacitance="1uF" maxDecouplingTraceLength={6} pcbX={29} pcbY={5.6} pcbRotation={90} schX={5.8} schY={2.5} schRotation={270} schSectionName="mcu" connections={{pin2:N("GND")}}/>
 <trace name="RP2040_VREG_INPUT" from=".U1 > .VREG_IN" to=".C20 > .pin1" maxLength={7} width={.2}/>
 <trace name="RP2040_VREG_OUTPUT" from=".U1 > .VREG_VOUT" to=".C21 > .pin1" maxLength={7} width={.2}/>
 <schematictext text="3.3V I/O and USB; internal regulator supplies DVDD at 1.1V. TESTEN and exposed pad to GND." schX={0} schY={9.4} fontSize={.22}/>
 <schematicbox name="U1 application" chipRef=".U1" schX={-3} schY={-5} width={2.3} height={1.8} schSectionName="mcu"
 pinLabels={{pin2:"GPIO0",pin3:"GPIO1",pin6:"GPIO4",pin7:"GPIO5",pin31:"GPIO20",pin32:"GPIO21",pin26:"RUN",pin25:"SWDIO",pin24:"SWCLK",pin27:"GPIO16",pin28:"GPIO17",pin29:"GPIO18",pin30:"GPIO19",pin34:"GPIO22",pin35:"GPIO23"}}
 schPinArrangement={{leftSide:["pin2","pin3","pin6","pin7","pin31","pin32","pin26","pin25"],rightSide:["pin24","pin27","pin28","pin29","pin30","pin34","pin35"]}}/>
 <R name="R10" resistance="10k" pcbX={28.6} pcbY={-9.5} pcbRotation={90} schX={-7} schY={-5} schSectionName="mcu" connections={{pin1:N("RUN"),pin2:N("V3V3")}}/>
 <JlcConnector pcbSx={refStyle} name="J4" cadModel={packageCad("jst-ph6")} schWidth={1.575} manufacturerPartNumber="B6B-PH-K-S(LF)(SN)" pcbX={dimensions.programming_connector[0]} pcbY={dimensions.programming_connector[1]} pcbRotation={0} schX={4} schY={-3} schSectionName="mcu" pinLabels={{pin1:"VREF",pin2:"SWDIO",pin3:"SWCLK",pin4:"RUN",pin5:"GND",pin6:"BOOTSEL"}} connections={{pin1:N("V3V3"),pin2:N("SWDIO"),pin3:N("SWCLK"),pin4:N("RUN"),pin5:N("GND"),pin6:N("BOOTSEL")}}/>
 <schematictext text="J4: VREF sense / SWDIO / SWCLK / RUN / GND / BOOTSEL. Ground BOOTSEL during reset for USB UF2." schX={0} schY={-9} fontSize={.22}/>
 </schematicsheet>
 <schematicsheet name="sheet-4" displayName="Optical rotation encoder" sheetIndex={3}>
 <schematictext text="DESK KNOB F1 — Optical rotation encoder" schX={0} schY={8} fontSize={.4}/>
 <schematicsection name="encoder" displayName="48-slot optical ring / common-collector dual sensor / PIO quadrature"/>
 <OpticalSensor pcbSx={refStyle} name="U2" schPinArrangement={{leftSide:["pin1","pin2"],rightSide:["pin4","pin5"],topSide:["pin6"],bottomSide:["pin3"]}} pcbX={-23} pcbY={10} pcbRotation={156.501434} schX={-3} schY={0} schSectionName="encoder" noConnect={["NC"]} connections={{A:N("IR_A"),K:N("GND"),COL:N("PERIPH_3V3"),EA:N("OPT_A"),EB:N("OPT_B")}}/>
 <JlcChip pcbSx={refStyle} name="U7" cadModel={packageCad("sot23-6")} manufacturerPartNumber="SN74LVC2G17DBVR" pcbX={-21} pcbY={19.5} schX={1} schY={0} schSectionName="encoder" pinLabels={{pin1:"A1",pin2:"GND",pin3:"A2",pin4:"Y2",pin5:"VCC",pin6:"Y1"}} pinAttributes={{VCC:{requiresPower:true},GND:{requiresGround:true},A1:{isInput:true},A2:{isInput:true},Y1:{isOutput:true},Y2:{isOutput:true}}} connections={{A1:N("OPT_A"),A2:N("OPT_B"),Y1:N("ENC_A"),Y2:N("ENC_B"),VCC:N("V3V3"),GND:N("GND")}}/>
 <R name="R24" resistance="150" pcbX={-28} pcbY={5.5} schX={-9} schY={2.5} schSectionName="encoder" connections={{pin1:N("PERIPH_3V3"),pin2:N("IR_A")}}/>
 <R name="R25" resistance="22k" pcbX={-25.5} pcbY={18.5} schX={-1} schY={3} schSectionName="encoder" connections={{pin1:N("OPT_A"),pin2:N("GND")}}/>
 <R name="R26" resistance="22k" pcbX={-25.5} pcbY={21.5} schX={2} schY={3} schSectionName="encoder" connections={{pin1:N("OPT_B"),pin2:N("GND")}}/>
 <C name="C14" capacitance="100nF" maxDecouplingTraceLength={6} pcbX={-21} pcbY={17} pcbRotation={180} schX={5} schY={0} schSectionName="encoder"/>
 <trace name="ENCODER_VCC_DECAP" from=".U7 > .VCC" to=".C14 > .pin1" width={.15}/>
 <trace name="ENCODER_GND_DECAP" from=".U7 > .GND" to=".C14 > .pin2" width={.15}/>
 <R name="R12" resistance="4.7k" pcbX={-20.5} pcbY={25.5} pcbRotation={0} schX={-9} schY={-3} schSectionName="encoder" connections={{pin1:N("V3V3"),pin2:N("SDA")}}/>
 <R name="R13" resistance="4.7k" pcbX={-23} pcbY={24} pcbRotation={180} schX={-5} schY={-3} schSectionName="encoder" connections={{pin1:N("V3V3"),pin2:N("SCL")}}/>
 <schematictext text="TCUT1600: dual optical channels; 150R IR drive, nominal 14mA" schX={-3} schY={6} fontSize={.22}/>
 <schematictext text="SN74LVC2G17: 3.3V Schmitt buffers to PIO quadrature" schX={1} schY={-6} fontSize={.22}/>
 </schematicsheet>
 <schematicsheet name="sheet-5" displayName="Persistent turn storage" sheetIndex={4}>
 <schematictext text="DESK KNOB F1 — Persistent turn storage" schX={0} schY={8} fontSize={.4}/>
 <schematicsection name="memory" displayName="32KB FRAM 0x50 / power-fail journal"/>
 <FRAM pcbSx={refStyle} name="U3" pcbX={-15} pcbY={27.5} schX={-2.5} schY={0} schSectionName="memory" connections={{A0:N("GND"),A1:N("GND"),A2:N("GND"),VSS:N("GND"),WP:N("GND"),SDA:N("SDA"),SCL:N("SCL"),VDD:N("V3V3")}}/>
 <C name="C16" capacitance="100nF" pcbX={-9.5} pcbY={31} schX={2.5} schY={0} schSectionName="memory" connections={{pin1:N("V3V3"),pin2:N("GND")}}/>
 <schematictext text="MB85RC256V: 32KB I2C FRAM at 0x50; 2.7-5.5V" schX={0} schY={4} fontSize={.22}/>
 </schematicsheet>
 <schematicsheet name="sheet-6" displayName="User controls and status" sheetIndex={5}>
 <schematictext text="DESK KNOB F1 — User controls and status" schX={0} schY={8} fontSize={.4}/>
 <schematicsection name="controls" displayName="Front side button / Scroll or Count mode / hold 3s to clear turns"/>
 <JlcButton pcbSx={refStyle} allowOffBoard name="SW1" cadModel={packageCad("b3u3000")} manufacturerPartNumber="B3U-3000P" pcbX={0} pcbY={dimensions.front_button.pcb_center[1]} pcbRotation={180} schX={-5} schY={3} schRotation={90} schSectionName="controls" connections={{pin1:N("MODE_BTN"),pin2:N("GND")}}/>
 <schematictext text="GPIO0 internal pull-up; short press selects mode; hold 3s clears turns" schX={0} schY={6} fontSize={.22}/>
 </schematicsheet>
 <schematicsheet name="sheet-7" displayName="Round display and laptop dashboard" sheetIndex={6}>
 <schematictext text="DESK KNOB F1 — Round display and laptop dashboard" schX={0} schY={8} fontSize={.4}/>
 <schematicsection name="display" displayName="Waveshare 19192 / GC9A01 240x240 / fixed 1.28-inch screen"/>
 <JlcConnector pcbSx={refStyle} name="J6" cadModel={packageCad("jst-sh8")} schWidth={1.385} schPinArrangement={{leftSide:["pin1","pin2","pin3","pin4","pin5","pin6","pin7","pin8","pin9","pin10"]}} manufacturerPartNumber="SM08B-SRSS-TB(LF)(SN)" pcbX={dimensions.display_connector[0]} pcbY={dimensions.display_connector[1]} pcbRotation={90} schX={2} schY={0} schSectionName="display" pinLabels={{pin1:"BL",pin2:"RST",pin3:"DC",pin4:"CS",pin5:"CLK",pin6:"DIN",pin7:"GND",pin8:"VCC",pin9:"MP1",pin10:"MP2"}} connections={{pin1:N("LCD_BL"),pin2:N("LCD_RST"),pin3:N("LCD_DC"),pin4:N("LCD_CS"),pin5:N("LCD_SCK"),pin6:N("LCD_MOSI"),pin7:N("GND"),pin8:N("PERIPH_3V3"),pin9:N("GND"),pin10:N("GND")}}/>
 <R name="R27" resistance="22" pcbX={31.1} pcbY={-3.5} pcbRotation={-90} schX={-3} schY={-.1} schRotation={0} schSectionName="display" connections={{pin1:N("SPI_SCK"),pin2:N("LCD_SCK")}}/>
 <R name="R28" resistance="22" pcbX={31.1} pcbY={-6.6} pcbRotation={-90} schX={-6} schY={-.3} schRotation={0} schSectionName="display" connections={{pin1:N("SPI_MOSI"),pin2:N("LCD_MOSI")}}/>
 <C name="C15" capacitance="1uF" pcbX={-28} pcbY={3} schX={6} schY={0} schSectionName="display" connections={{pin1:N("PERIPH_3V3"),pin2:N("GND")}}/>
 <schematictext text="Waveshare 19192: 240x240; 3.3V supply and logic; SPI 12MHz" schX={0} schY={5} fontSize={.22}/>
 <schematictext text="J6: keyed JST-SH 8-pin; H1 crimped SH-to-PH cable; anchors to GND" schX={0} schY={-5} fontSize={.22}/>
 </schematicsheet>
 <schematicsheet name="sheet-8" displayName="RP2040 boot flash, clock and USB termination" sheetIndex={7}>
 <schematictext text="DESK KNOB F1 — RP2040 boot flash, 12MHz clock and USB termination" schX={0} schY={11} fontSize={.35}/>
 <schematicsection name="boot" displayName="2MB Winbond flash / Abracon ABM8 clock / USB series resistors"/>
 <schematicbox name="U1 boot and USB" chipRef=".U1" schX={-5} schY={3} width={2.6} height={1.4} schSectionName="boot"
 pinLabels={{pin20:"XIN",pin21:"XOUT",pin46:"USB_DM",pin47:"USB_DP",pin56:"QSPI_SS",pin52:"QSPI_SCLK",pin53:"QSPI_SD0",pin55:"QSPI_SD1",pin54:"QSPI_SD2",pin51:"QSPI_SD3"}}
 schPinArrangement={{leftSide:["pin20","pin21","pin46","pin47"],rightSide:["pin56","pin52","pin53","pin55","pin54","pin51"]}}/>
 <BootFlash pcbSx={refStyle} name="U8" pcbX={22.5} pcbY={11} pcbRotation={90} schX={3} schY={4} schSectionName="boot"
 connections={{CS:N("QSPI_SS"),SCLK:N("QSPI_SCLK"),SD0:N("QSPI_SD0"),SD1:N("QSPI_SD1"),SD2:N("QSPI_SD2"),SD3:N("QSPI_SD3"),VCC:N("V3V3"),GND:N("GND")}}/>
 <C name="C22" packageSize="0402" capacitance="100nF" maxDecouplingTraceLength={6} pcbX={18.7} pcbY={13.3} pcbRotation={270} schX={7} schY={4} schSectionName="boot" connections={{pin2:N("GND")}}/>
 <trace name="FLASH_BYPASS" from=".U8 > .VCC" to=".C22 > .pin1" maxLength={8} width={.15}/>
 <R name="R6" resistance="1k" pcbX={27.5} pcbY={18.5} pcbRotation={0} schX={3} schY={8} schSectionName="boot" connections={{pin1:N("QSPI_SS"),pin2:N("BOOTSEL")}}/>
 <R name="R7" resistance="10k" pcbX={23.4} pcbY={17.5} pcbRotation={180} schX={7} schY={8} schSectionName="boot" connections={{pin1:N("QSPI_SS"),pin2:N("V3V3")}}/>
 <ClockCrystal pcbSx={refStyle} name="X1" pcbX={20.7} pcbY={-6.5} pcbRotation={180} schX={-8} schY={-5} schSectionName="boot" connections={{X1:N("XIN"),X2:N("XTAL_OUT"),GND1:N("GND"),GND2:N("GND")}}/>
 <R name="R5" resistance="1k" pcbX={24} pcbY={-7.5} pcbRotation={-90} schX={-4.2} schY={-5} schSectionName="boot" connections={{pin1:N("XOUT"),pin2:N("XTAL_OUT")}}/>
 <C name="C23" packageSize="0402" capacitance="15pF" pcbX={23.5} pcbY={-5.1} pcbRotation={90} schX={-11} schY={-7} schSectionName="boot" connections={{pin1:N("XIN"),pin2:N("GND")}}/>
 <C name="C24" packageSize="0402" capacitance="15pF" pcbX={19.4} pcbY={-9.2} pcbRotation={-90} schX={-6} schY={-7} schSectionName="boot" connections={{pin1:N("XTAL_OUT"),pin2:N("GND")}}/>
 <R name="R3" resistance="27" pcbX={27} pcbY={8.4} pcbRotation={90} schX={-10} schY={1} schRotation={90} schSectionName="boot" connections={{pin1:N("USB_DM_MCU"),pin2:N("USB_DM")}}/>
 <R name="R4" resistance="27" pcbX={29} pcbY={8.4} pcbRotation={90} schX={-8} schY={1} schRotation={270} schSectionName="boot" connections={{pin1:N("USB_DP_MCU"),pin2:N("USB_DP")}}/>
 <schematictext text="Winbond W25Q16JVSNIQ: 2MB boot flash; BOOTSEL is isolated from QSPI CS by 1k." schX={0} schY={10} fontSize={.22}/>
 <schematictext text="ABM8-272-T3: 12MHz, CL10pF / 50ohm ESR; 15pF loads and 1k series damping per Raspberry Pi reference." schX={-3} schY={-9} fontSize={.22}/>
 </schematicsheet>
 <copperpour name="GROUND_TOP" layer="top" connectsTo="net.GND" clearance={.25} boardEdgeMargin={.4} cutoutMargin={.31} useThermalReliefs/>
 <copperpour name="GROUND_BOTTOM" layer="bottom" connectsTo="net.GND" clearance={.25} boardEdgeMargin={.4} cutoutMargin={.31} useThermalReliefs/>
 <silkscreentext text="DESK KNOB F1" pcbX={-33} pcbY={0} pcbRotation={90} fontSize={1}/>
 <silkscreentext text="1" pcbX={-5} pcbY={23.5} fontSize={1}/>
 <silkscreentext text="USB-C" pcbX={0} pcbY={32.5} fontSize={1}/>
 <silkscreentext text="USB POWER" pcbX={8} pcbY={-24} fontSize={1}/>
 <silkscreentext text="MODE / CLEAR 3s" pcbX={-4} pcbY={-28.5} fontSize={1}/>
 <silkscreentext text="J6 LCD" pcbX={-28.5} pcbY={-7} fontSize={1}/>
 <silkscreentext text="1" pcbX={-25} pcbY={dimensions.display_connector[1]-3.5} fontSize={1}/>
 <silkscreentext text="8" pcbX={-25} pcbY={dimensions.display_connector[1]+3.5} fontSize={1}/>

</board>
