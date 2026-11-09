import { packageCad } from "./cad"
import { jlcFootprintPart } from "./jlc-parts"
import type { ChipProps } from "@tscircuit/props"

// Physical package numbers viewed from above; see reference/DATASHEETS.md.
export const mcuPins = ["VBAT","PC13","PC14","PC15","PF0","PF1","NRST","VSSA","VDDA","PA0","PA1","PA2","PA3","PA4","PA5","PA6","PA7","PB0","PB1","PB2","PB10","PB11","VSS1","VDD1","PB12","PB13","PB14","PB15","PA8","PA9","PA10","PA11","PA12","PA13","VSS2","VDDIO2","PA14","PA15","PB3","PB4","PB5","PB6","PB7","BOOT0","PB8","PB9","VSS3","VDD2"] as const
const attributes = (pins: readonly string[], power: string[], ground: string[]) => Object.fromEntries(pins.map(p=>[p, power.includes(p)?{requiresPower:true,mustBeConnected:true}:ground.includes(p)?{requiresGround:true,mustBeConnected:true}:{isBidirectional:true}]))
const labels = (pins: readonly string[]) => Object.fromEntries(pins.map((p,i)=>[`pin${i+1}`,p]))
// Exact imports use different zero angles. Adapt placement, not pad geometry.
// CAD supplied by this project retains the previous verified package axes.
export const libraryAngle: Record<string, number> = {
 "STM32F072CBT6":-90, "MB85RC256VPNF-G-AMERE2":-90,
 "USBLC6-2SC6":-90, "SN74LVC2G17DBVR":-90,
 "TPS22919DCKR":180, "TLV75533PDBVR":180,
 "B6B-PH-K-S(LF)(SN)":180, "2.54-1*8":180,
}
export function JlcChip(props: any) {
 const {manufacturerPartNumber:mpn,pcbRotation=0,cadModel,...rest}=props
 const delta=libraryAngle[mpn]??0
 return jlcFootprintPart(mpn,{...rest,symbol:undefined,pcbRotation:pcbRotation+delta,
  ...(cadModel?{cadModel:{...cadModel,pcbRotationOffset:(cadModel.pcbRotationOffset??0)-delta}}:{})})
}
export const JlcConnector=JlcChip
export const JlcButton=(props:any)=>jlcFootprintPart("B3U-3000P",props)
export const JlcResistor=(props:any)=>jlcFootprintPart(props.manufacturerPartNumber,props)
export const JlcCapacitor=(props:any)=>jlcFootprintPart(props.manufacturerPartNumber,props)
export const MCU = (props: ChipProps) => <JlcChip {...props} cadModel={packageCad("lqfp48")} manufacturerPartNumber="STM32F072CBT6" pinLabels={labels(mcuPins)} pinAttributes={attributes(mcuPins,["VBAT","VDDA","VDD1","VDD2","VDDIO2"],["VSSA","VSS1","VSS2","VSS3"])} />
// Genuine stocked pre-PCN sensor; _A has unchanged fit/form/function per Vishay PCN.
// JLC's pin3 alias C2 means cathode here; use the manufacturer's A/K/C/E functions.
export const OpticalSensor = (props: ChipProps) => <JlcChip {...props} manufacturerPartNumber="TCUT1600X01" cadModel={packageCad("tcut1600")}
 pinLabels={labels(["A","NC","K","EB","EA","COL"])}
 pinAttributes={{A:{isPassive:true},K:{requiresGround:true},COL:{requiresPower:true},EA:{isOutput:true},EB:{isOutput:true},NC:{doNotConnect:true}}}/>
export const FRAM = (props: ChipProps) => <JlcChip {...props} cadModel={packageCad("soic8")} manufacturerPartNumber="MB85RC256VPNF-G-AMERE2" pinAttributes={{VDD:{requiresPower:true},VSS:{requiresGround:true},A0:{isInput:true},A1:{isInput:true},A2:{isInput:true},SDA:{isBidirectional:true},SCL:{isInput:true},WP:{isInput:true}}} pinLabels={labels(["A0","A1","A2","VSS","SDA","SCL","WP","VDD"])} />

// Logical USB aliases adapt the exact supplier pin numbers; copper is unchanged.
// CAD Z uses the lead seating plane (0.09mm in the downloaded model), matching
// the manufacturer's 3.16mm body height. The import itself remains byte-identical.
export const USB = (props:any) => {
 const imported=jlcFootprintPart("TYPEC-309-ACP16L65",{})
 const aliases={...imported.props.pinLabels,pin34:["SBU1","A8"],pin40:["SBU2","B8"]}
 return <connector standard="usb_c" {...imported.props} {...props} pinLabels={aliases}
  cadModel={{...imported.props.cadModel,modelOriginPosition:{...imported.props.cadModel.modelOriginPosition,z:.09}}}
  pinAttributes={Object.fromEntries(Array.from({length:20},(_,i)=>[`pin${i+25}`,i<4?{requiresGround:true}:{isPassive:true}]))}/>
}
