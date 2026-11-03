import type { ChipProps } from "@tscircuit/props"

// Pin numbers are physical package numbers, viewed from above. See reference/DATASHEETS.md.
export const mcuPins = ["VBAT","PC13","PC14","PC15","PF0","PF1","NRST","VSSA","VDDA","PA0","PA1","PA2","PA3","PA4","PA5","PA6","PA7","PB0","PB1","PB2","PB10","PB11","VSS1","VDD1","PB12","PB13","PB14","PB15","PA8","PA9","PA10","PA11","PA12","PA13","VSS2","VDDIO2","PA14","PA15","PB3","PB4","PB5","PB6","PB7","BOOT0","PB8","PB9","VSS3","VDD2"] as const
const attributes = (pins: readonly string[], power: string[], ground: string[]) => Object.fromEntries(pins.map(p=>[p, power.includes(p)?{requiresPower:true,mustBeConnected:true}:ground.includes(p)?{requiresGround:true,mustBeConnected:true}:{isBidirectional:true}]))
const labels = (pins: readonly string[]) => Object.fromEntries(pins.map((p,i)=>[`pin${i+1}`,p]))
export const MCU = (props: ChipProps) => <chip {...props} manufacturerPartNumber="STM32F072CBT6" pinLabels={labels(mcuPins)} pinAttributes={attributes(mcuPins,["VBAT","VDDA","VDD1","VDD2","VDDIO2"],["VSSA","VSS1","VSS2","VSS3"])} footprint="lqfp48_w7_h7_p0.5mm" />
export const AngleSensor = (props: ChipProps) => <chip {...props} manufacturerPartNumber="AS5600-ASOM" pinAttributes={{VDD5V:{requiresPower:true},VDD3V3:{requiresPower:true},GND:{requiresGround:true},SDA:{isBidirectional:true},SCL:{isInput:true},DIR:{isInput:true},PGO:{isInput:true},OUT:{isOutput:true}}} pinLabels={labels(["VDD5V","VDD3V3","OUT","GND","PGO","SDA","SCL","DIR"])} footprint="soic8_w3.9mm_p1.27mm" />
export const FRAM = (props: ChipProps) => <chip {...props} manufacturerPartNumber="MB85RC256VPNF-G-AMERE2" pinAttributes={{VDD:{requiresPower:true},VSS:{requiresGround:true},A0:{isInput:true},A1:{isInput:true},A2:{isInput:true},SDA:{isBidirectional:true},SCL:{isInput:true},WP:{isInput:true}}} pinLabels={labels(["A0","A1","A2","VSS","SDA","SCL","WP","VDD"])} footprint="soic8_w3.9mm_p1.27mm" />
export const Charger = (props: ChipProps) => <chip {...props} manufacturerPartNumber="BQ24074RGTR" pinAttributes={{IN:{requiresPower:true},VSS:{requiresGround:true},EP:{requiresGround:true},OUT1:{providesPower:true},OUT2:{providesPower:true},BAT1:{isBidirectional:true},BAT2:{isBidirectional:true}}} pinLabels={labels(["TS","BAT1","BAT2","CE","EN2","EN1","PGOOD","VSS","CHG","OUT1","OUT2","ILIM","IN","TMR","ITERM","ISET","EP"])}
 footprint={<footprint>
  {/* TI RGT0016B land pattern: 0.5 pitch, 0.6 x 0.24 lands, 1.7 square EP. */}
  {Array.from({length:4},(_,i)=><smtpad shape="rect" width={.6} height={.24} pcbX={-1.45} pcbY={.75-i*.5} portHints={[`pin${i+1}`]}/>)}
  {Array.from({length:4},(_,i)=><smtpad shape="rect" width={.24} height={.6} pcbX={-.75+i*.5} pcbY={-1.45} portHints={[`pin${i+5}`]}/>)}
  {Array.from({length:4},(_,i)=><smtpad shape="rect" width={.6} height={.24} pcbX={1.45} pcbY={-.75+i*.5} portHints={[`pin${i+9}`]}/>)}
  {Array.from({length:4},(_,i)=><smtpad shape="rect" width={.24} height={.6} pcbX={.75-i*.5} pcbY={1.45} portHints={[`pin${i+13}`]}/>)}
  <smtpad shape="rect" width={1.7} height={1.7} portHints={["pin17"]}/>
  <silkscreencircle pcbX={-1.8} pcbY={1.8} radius={.15}/>
  <courtyardrect width={4} height={4}/>
 </footprint>} />
