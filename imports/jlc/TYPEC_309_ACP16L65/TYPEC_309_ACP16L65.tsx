import objPath from "./TYPEC_309_ACP16L65.obj"
import stepPath from "./TYPEC_309_ACP16L65.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin25: ["EH2"],
  pin26: ["EH1"],
  pin27: ["EH3"],
  pin28: ["EH4"],
  pin29: ["GND1","A12"],
  pin30: ["GND2","B1"],
  pin31: ["VBUS1","A9"],
  pin32: ["VBUS2","B4"],
  pin33: ["CC2","B5"],
  pin34: ["SUB1","A8"],
  pin35: ["DP2","B6"],
  pin36: ["DN1","A7"],
  pin37: ["DP1","A6"],
  pin38: ["DN2","B7"],
  pin39: ["CC1","A5"],
  pin40: ["SUB2","B8"],
  pin41: ["VBUS3","B9"],
  pin42: ["VBUS4","A4"],
  pin43: ["GND3","B12"],
  pin44: ["GND4","A1"]
} as const

export const TYPEC_309_ACP16L65 = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C2909598"
  ]
}}
      manufacturerPartNumber="TYPEC-309-ACP16L65"
      footprint={<footprint>
        <hole pcbX="-2.999994mm" pcbY="0.7555294mm" diameter="0.649986mm" />
<hole pcbX="2.999994mm" pcbY="0.7555294mm" diameter="0.649986mm" />
<platedhole  portHints={["pin26"]} pcbX="4.320032mm" pcbY="-2.5449466mm" holeWidth="0.5999988mm" holeHeight="1.5999968mm" outerWidth="0.999998mm" outerHeight="1.999996mm" shape="pill" />
<platedhole  portHints={["pin25"]} pcbX="4.320032mm" pcbY="1.4550454mm" holeWidth="0.5999988mm" holeHeight="1.499997mm" outerWidth="0.999998mm" outerHeight="1.8999962mm" shape="pill" />
<platedhole  portHints={["pin27"]} pcbX="-4.320032mm" pcbY="-2.5449466mm" holeWidth="0.5999988mm" holeHeight="1.5999968mm" outerWidth="0.999998mm" outerHeight="1.999996mm" shape="pill" />
<platedhole  portHints={["pin28"]} pcbX="-4.320032mm" pcbY="1.4550454mm" holeWidth="0.5999988mm" holeHeight="1.499997mm" outerWidth="0.999998mm" outerHeight="1.8999962mm" shape="pill" />
<smtpad portHints={["pin29"]} pcbX="3.350006mm" pcbY="2.0199414mm" width="0.2999994mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin30"]} pcbX="3.050032mm" pcbY="2.0199414mm" width="0.2999994mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin31"]} pcbX="2.549906mm" pcbY="2.0199414mm" width="0.2999994mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin32"]} pcbX="2.249932mm" pcbY="2.0199414mm" width="0.2999994mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin33"]} pcbX="1.75006mm" pcbY="2.0199414mm" width="0.2999994mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin34"]} pcbX="1.249934mm" pcbY="2.0199414mm" width="0.2999994mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin35"]} pcbX="0.750062mm" pcbY="2.0199414mm" width="0.2999994mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin36"]} pcbX="0.249936mm" pcbY="2.0199414mm" width="0.2999994mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin37"]} pcbX="-0.249936mm" pcbY="2.0199414mm" width="0.2999994mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin38"]} pcbX="-0.750062mm" pcbY="2.0199414mm" width="0.2999994mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin39"]} pcbX="-1.249934mm" pcbY="2.0199414mm" width="0.2999994mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin40"]} pcbX="-1.75006mm" pcbY="2.0199414mm" width="0.2999994mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin41"]} pcbX="-2.249932mm" pcbY="2.0199414mm" width="0.2999994mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin42"]} pcbX="-2.549906mm" pcbY="2.0199414mm" width="0.2999994mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin43"]} pcbX="-3.050032mm" pcbY="2.0199414mm" width="0.2999994mm" height="1.1500104mm" shape="rect" />
<smtpad portHints={["pin44"]} pcbX="-3.350006mm" pcbY="2.0199414mm" width="0.2999994mm" height="1.1500104mm" shape="rect" />
<silkscreenpath route={[{"x":-4.469968199999926,"y":-4.645551999999952},{"x":4.470019000000093,"y":-4.645551999999952}]} />
<silkscreenpath route={[{"x":4.470019000000093,"y":-1.3295057999999926},{"x":4.470019000000093,"y":0.28949020000004566}]} />
<silkscreenpath route={[{"x":4.470019000000093,"y":-4.645551999999952},{"x":4.470019000000093,"y":-3.7605905999998868}]} />
<silkscreenpath route={[{"x":-4.469968199999926,"y":-1.3295057999999926},{"x":-4.469968199999926,"y":0.28949020000004566}]} />
<silkscreenpath route={[{"x":-4.469968199999926,"y":-4.645551999999952},{"x":-4.469968199999926,"y":-3.7605905999998868}]} />
<silkscreentext text="{NAME}" pcbX="0.009398mm" pcbY="3.5922034mm" anchorAlignment="center" fontSize="1mm" />
<fabricationnotepath route={[{"x":-3.54998020000005,"y":3.212420599999973},{"x":-2.8499815999999782,"y":3.212420599999973},{"x":-3.1999935999999707,"y":2.7624342000000297},{"x":-3.54998020000005,"y":3.212420599999973}]} strokeWidth="0mm" isFilled hasStroke={false} />
<courtyardoutline outline={[{"x":-5.070031000000085,"y":2.8449465999999575},{"x":5.070030999999972,"y":2.8449465999999575},{"x":5.070030999999972,"y":-4.887500199999977},{"x":-5.070031000000085,"y":-4.887500199999977},{"x":-5.070031000000085,"y":2.8449465999999575}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 0, y: 6.216506999999937, z: -0.01000180000000006 },
      }}
      {...props}
    />
  )
}