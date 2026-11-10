import { packageCad } from "./cad"
import { jlcFootprintPart } from "./jlc-parts"
import type { ChipProps } from "@tscircuit/props"

// Physical package numbers viewed from above; see reference/DATASHEETS.md.
export const mcuPins = ["IOVDD1", "GPIO0", "GPIO1", "GPIO2", "GPIO3", "GPIO4", "GPIO5", "GPIO6", "GPIO7", "IOVDD2", "GPIO8", "GPIO9", "GPIO10", "GPIO11", "GPIO12", "GPIO13", "GPIO14", "GPIO15", "TESTEN", "XIN", "XOUT", "IOVDD3", "DVDD1", "SWCLK", "SWDIO", "RUN", "GPIO16", "GPIO17", "GPIO18", "GPIO19", "GPIO20", "GPIO21", "IOVDD4", "GPIO22", "GPIO23", "GPIO24", "GPIO25", "GPIO26", "GPIO27", "GPIO28", "GPIO29", "IOVDD5", "ADC_AVDD", "VREG_IN", "VREG_VOUT", "USB_DM", "USB_DP", "USB_VDD", "IOVDD6", "DVDD2", "QSPI_SD3", "QSPI_SCLK", "QSPI_SD0", "QSPI_SD2", "QSPI_SD1", "QSPI_SS", "GND"] as const
const attributes = (pins: readonly string[], power: string[], ground: string[]) => Object.fromEntries(pins.map(p=>[p, power.includes(p)?{requiresPower:true,mustBeConnected:true}:ground.includes(p)?{requiresGround:true,mustBeConnected:true}:{isBidirectional:true}]))
const labels = (pins: readonly string[]) => Object.fromEntries(pins.map((p,i)=>[`pin${i+1}`,p]))
// Exact imports use different zero angles. Adapt placement, not pad geometry.
// CAD supplied by this project retains the previous verified package axes.
export const libraryAngle: Record<string, number> = {
 "W25Q16JVSNIQ":-90, "STM32F072CBT6":-90, "MB85RC256VPNF-G-AMERE2":-90,
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
export const MCU = (props: ChipProps) => <JlcChip {...props} cadModel={packageCad("rp2040")} manufacturerPartNumber="RP2040" pinLabels={labels(mcuPins)} pinAttributes={{...attributes(mcuPins,["IOVDD1","IOVDD2","IOVDD3","IOVDD4","IOVDD5","IOVDD6","DVDD1","DVDD2","ADC_AVDD","USB_VDD","VREG_IN"],["GND","TESTEN"]),VREG_VOUT:{providesPower:true,mustBeConnected:true}}} />
export const BootFlash = (props: ChipProps) => <JlcChip {...props} cadModel={packageCad("soic8")} manufacturerPartNumber="W25Q16JVSNIQ" pinLabels={labels(["CS","SD1","SD2","GND","SD0","SCLK","SD3","VCC"])} pinAttributes={{CS:{isInput:true},SD0:{isBidirectional:true},SD1:{isBidirectional:true},SD2:{isBidirectional:true},SD3:{isBidirectional:true},SCLK:{isInput:true},VCC:{requiresPower:true},GND:{requiresGround:true}}}/>
export const ClockCrystal = ({connections,...props}: any) => <JlcChip {...props} loadCapacitance="10pF" maxTraceLength={10} connections={{pin1:connections.X1,pin2:connections.GND1,pin3:connections.X2,pin4:connections.GND2}} cadModel={packageCad("abm8")} manufacturerPartNumber="ABM8-272-T3" pinLabels={labels(["X1","GND1","X2","GND2"])} pinAttributes={{X1:{isPassive:true},X2:{isPassive:true},GND1:{requiresGround:true},GND2:{requiresGround:true}}}/>
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
