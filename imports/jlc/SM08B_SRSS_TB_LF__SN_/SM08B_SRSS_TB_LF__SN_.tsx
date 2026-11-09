import objPath from "./SM08B_SRSS_TB_LF__SN_.obj"
import stepPath from "./SM08B_SRSS_TB_LF__SN_.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["pin1"],
  pin2: ["pin2"],
  pin3: ["pin3"],
  pin4: ["pin4"],
  pin5: ["pin5"],
  pin6: ["pin6"],
  pin7: ["pin7"],
  pin8: ["pin8"],
  pin9: ["pin9"],
  pin10: ["pin10"]
} as const

export const SM08B_SRSS_TB_LF__SN_ = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C160407"
  ]
}}
      manufacturerPartNumber="SM08B-SRSS-TB(LF)(SN)"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="-3.499866mm" pcbY="2.0500086mm" width="0.5999988mm" height="1.5500096mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="-2.5019mm" pcbY="2.0499832mm" width="0.5999988mm" height="1.5500096mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="-1.501902mm" pcbY="2.0499832mm" width="0.5999988mm" height="1.5500096mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="-0.501904mm" pcbY="2.0499832mm" width="0.5999988mm" height="1.5500096mm" shape="rect" />
<smtpad portHints={["pin5"]} pcbX="0.500126mm" pcbY="2.0500086mm" width="0.5999988mm" height="1.5500096mm" shape="rect" />
<smtpad portHints={["pin6"]} pcbX="1.498092mm" pcbY="2.0499832mm" width="0.5999988mm" height="1.5500096mm" shape="rect" />
<smtpad portHints={["pin7"]} pcbX="2.49809mm" pcbY="2.0499832mm" width="0.5999988mm" height="1.5500096mm" shape="rect" />
<smtpad portHints={["pin8"]} pcbX="3.499866mm" pcbY="2.0500086mm" width="0.5999988mm" height="1.5500096mm" shape="rect" />
<smtpad portHints={["pin9"]} pcbX="4.800092mm" pcbY="-1.8250154mm" width="1.499997mm" height="1.999996mm" shape="rect" />
<smtpad portHints={["pin10"]} pcbX="-4.800092mm" pcbY="-1.8250154mm" width="1.499997mm" height="1.999996mm" shape="rect" />
<silkscreenpath route={[{"x":-3.8800023999999667,"y":-2.7467306000000917},{"x":3.799992399999951,"y":-2.7467306000000917}]} />
<silkscreenpath route={[{"x":-4.059986800000047,"y":1.9732497999999623},{"x":-5.2599844000000076,"y":1.9732497999999623},{"x":-5.2599844000000076,"y":-0.566750200000115}]} />
<silkscreenpath route={[{"x":3.9800021999999444,"y":1.9332448000000113},{"x":5.219979400000057,"y":1.9332448000000113},{"x":5.219979400000057,"y":-0.6067298000000392}]} />
<silkscreentext text="{NAME}" pcbX="-0.0127mm" pcbY="3.8374086mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-5.800090500000124,"y":3.075013399999989},{"x":5.80009050000001,"y":3.075013399999989},{"x":5.80009050000001,"y":-3.075013399999989},{"x":-5.800090500000124,"y":-3.075013399999989},{"x":-5.800090500000124,"y":3.075013399999989}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 3.5, y: 0.40673090000004786, z: -0.01 },
      }}
      {...props}
    />
  )
}