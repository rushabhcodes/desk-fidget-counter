import { packageCad } from "./cad"
import { Fragment } from "react"
import type { ChipProps } from "@tscircuit/props"

// Pin numbers are physical package numbers, viewed from above. See reference/DATASHEETS.md.
export const mcuPins = ["VBAT","PC13","PC14","PC15","PF0","PF1","NRST","VSSA","VDDA","PA0","PA1","PA2","PA3","PA4","PA5","PA6","PA7","PB0","PB1","PB2","PB10","PB11","VSS1","VDD1","PB12","PB13","PB14","PB15","PA8","PA9","PA10","PA11","PA12","PA13","VSS2","VDDIO2","PA14","PA15","PB3","PB4","PB5","PB6","PB7","BOOT0","PB8","PB9","VSS3","VDD2"] as const
const attributes = (pins: readonly string[], power: string[], ground: string[]) => Object.fromEntries(pins.map(p=>[p, power.includes(p)?{requiresPower:true,mustBeConnected:true}:ground.includes(p)?{requiresGround:true,mustBeConnected:true}:{isBidirectional:true}]))
const labels = (pins: readonly string[]) => Object.fromEntries(pins.map((p,i)=>[`pin${i+1}`,p]))
export const MCU = (props: ChipProps) => <chip {...props} cadModel={packageCad("lqfp48")} manufacturerPartNumber="STM32F072CBT6" pinLabels={labels(mcuPins)} pinAttributes={attributes(mcuPins,["VBAT","VDDA","VDD1","VDD2","VDDIO2"],["VSSA","VSS1","VSS2","VSS3"])} footprint="lqfp48_w7_h7_p0.5mm" />
// TCUT1600X01_A recommended land pattern (Vishay 84174). Library pin IDs
// follow the top-view perimeter; vendor identifies the leads by A/K/C/E labels.
export const OpticalSensor = (props: ChipProps) => <chip {...props} manufacturerPartNumber="TCUT1600X01_A" cadModel={packageCad("tcut1600")}
 pinLabels={labels(["A","NC","K","EB","EA","COL"])}
 pinAttributes={{A:{isPassive:true},K:{requiresGround:true},COL:{requiresPower:true},EA:{isOutput:true},EB:{isOutput:true},NC:{doNotConnect:true}}}
 footprint={<footprint>
  {[1,2,3].map((n,i)=><Fragment key={n}><smtpad shape="rect" width={1.9} height={n===2?1:.7} pcbX={-2.45} pcbY={1.4-i*1.4} portHints={[`pin${n}`]}/></Fragment>)}
  {[6,5,4].map((n,i)=><Fragment key={n}><smtpad shape="rect" width={1.0} height={.7} pcbX={2.0} pcbY={1.4-i*1.4} portHints={[`pin${n}`]}/></Fragment>)}
  <silkscreenpath route={[{x:-2.75,y:2.1},{x:2.75,y:2.1}]}/>
  <silkscreenpath route={[{x:-2.75,y:-2.1},{x:2.75,y:-2.1}]}/>
  {/* 0.3mm courtyard beyond the full 5.9mm land span and 4mm body. */}
  <courtyardrect width={6.5} height={4.6} pcbX={-.45}/>
 </footprint>}/>
// Exact JST PH land pattern, centred row; +Y is opposite the housing latch.
export const phFootprint = (count: number, sideEntry = false) => <footprint insertionDirection={sideEntry?"from_bottom":"from_above"}>
 {Array.from({length:count},(_,i)=><Fragment key={i}><platedhole shape="circular_hole_with_rect_pad" holeOffsetX={0} holeOffsetY={0} holeDiameter={.75} rectPadWidth={1.2} rectPadHeight={1.75} rectBorderRadius={.25} pcbX={(i-(count-1)/2)*2} portHints={[`pin${i+1}`]}/></Fragment>)}
 {/* Housing/mate overhangs the window; print only the back edge on PCB material. */}
 <silkscreenpath route={[{x:-(count-1)-2.06,y:sideEntry ? .86:1.21},{x:-(count-1)-2.06,y:sideEntry?1.46:1.81},{x:(count-1)+2.06,y:sideEntry?1.46:1.81},{x:(count-1)+2.06,y:sideEntry ? .86:1.21}]}/>
 <silkscreenpath route={[{x:-(count-1),y:sideEntry?1.46:1.81},{x:-(count-1),y:sideEntry?2.26:2.61}]}/>

 <courtyardrect width={(count-1)*2+4.9} height={sideEntry?8.6:5.5} pcbY={sideEntry?-2.45:-.55}/>
 </footprint>
// NKK G12AH: 0.4mm leads on 2.54mm grid; support row 5.08mm
// ahead of electrical row. Lever points +Y before PCB rotation.
export const toggleFootprint = <footprint>
 {[-2.54,0,2.54].map((x,i)=><Fragment key={i}><platedhole shape="circle" holeDiameter={.6} outerDiameter={1.2} pcbX={x} portHints={[`pin${i+1}`]}/></Fragment>)}
 {[-2.54,2.54].map((x,i)=><Fragment key={i}><platedhole shape="circle" holeDiameter={.6} outerDiameter={1.2} pcbX={x} pcbY={5.08} portHints={[`pin${i+4}`]}/></Fragment>)}
 <silkscreenpath route={[{x:-3.5,y:-1.05},{x:3.5,y:-1.05},{x:3.5,y:5.85},{x:-3.5,y:5.85},{x:-3.5,y:-1.05}]}/>
 <courtyardrect width={7.8} height={7.8} pcbY={2.45}/>
 </footprint>
export const FRAM = (props: ChipProps) => <chip {...props} cadModel={packageCad("soic8")} manufacturerPartNumber="MB85RC256VPNF-G-AMERE2" pinAttributes={{VDD:{requiresPower:true},VSS:{requiresGround:true},A0:{isInput:true},A1:{isInput:true},A2:{isInput:true},SDA:{isBidirectional:true},SCL:{isInput:true},WP:{isInput:true}}} pinLabels={labels(["A0","A1","A2","VSS","SDA","SCL","WP","VDD"])} footprint="soic8_w3.9mm_p1.27mm" />
