import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["pin1"],
  pin2: ["pin2"],
  pin3: ["pin3"],
  pin4: ["pin4"],
  pin5: ["pin5"],
  pin6: ["pin6"],
  pin7: ["pin7"],
  pin8: ["pin8"]
} as const

export const A_2_54_1_8 = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C5156616"
  ]
}}
      manufacturerPartNumber="2.54-1*8"
      footprint={<footprint>
        <platedhole  portHints={["pin1"]} pcbX="-8.89mm" pcbY="0mm" holeWidth="0.999998mm" holeHeight="0.999998mm" outerWidth="1.499997mm" outerHeight="1.499997mm" rectPad={true} pcbRotation="0deg" shape="pill" />
<platedhole  portHints={["pin2"]} pcbX="-6.35mm" pcbY="0mm" outerDiameter="1.499997mm" holeDiameter="0.999998mm" shape="circle" />
<platedhole  portHints={["pin3"]} pcbX="-3.81mm" pcbY="0mm" outerDiameter="1.499997mm" holeDiameter="0.999998mm" shape="circle" />
<platedhole  portHints={["pin4"]} pcbX="-1.27mm" pcbY="0mm" outerDiameter="1.499997mm" holeDiameter="0.999998mm" shape="circle" />
<platedhole  portHints={["pin5"]} pcbX="1.27mm" pcbY="0mm" outerDiameter="1.499997mm" holeDiameter="0.999998mm" shape="circle" />
<platedhole  portHints={["pin6"]} pcbX="3.81mm" pcbY="0mm" outerDiameter="1.499997mm" holeDiameter="0.999998mm" shape="circle" />
<platedhole  portHints={["pin7"]} pcbX="6.35mm" pcbY="0mm" outerDiameter="1.499997mm" holeDiameter="0.999998mm" shape="circle" />
<platedhole  portHints={["pin8"]} pcbX="8.89mm" pcbY="0mm" outerDiameter="1.499997mm" holeDiameter="0.999998mm" shape="circle" />
<silkscreenpath route={[{"x":10.159974599999941,"y":1.2700000000000955},{"x":10.159974599999941,"y":-1.2699999999999818},{"x":-10.159974600000055,"y":-1.2699999999999818},{"x":-10.159974600000055,"y":1.2700000000000955},{"x":10.159974599999941,"y":1.2700000000000955}]} />
<silkscreenpath route={[{"x":-7.596479600000066,"y":1.2700000000000955},{"x":-7.596479600000066,"y":-1.2699999999999818}]} />
<silkscreentext text="{NAME}" pcbX="-0mm" pcbY="2.27mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-10.50999980000006,"y":1.500010199999906},{"x":10.50997439999992,"y":1.500010199999906},{"x":10.50997439999992,"y":-1.499984799999993},{"x":-10.50999980000006,"y":-1.499984799999993},{"x":-10.50999980000006,"y":1.500010199999906}]} />
      </footprint>}
      cadModel={{
        objUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C5156616.obj?uuid=493a931f43604ecb9f8cc04c531d15ee",
        stepUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C5156616.step?uuid=493a931f43604ecb9f8cc04c531d15ee",
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 7.62001320000007, y: -0.000012700000070253736, z: -0.000005999999999950489 },
      }}
      {...props}
    />
  )
}