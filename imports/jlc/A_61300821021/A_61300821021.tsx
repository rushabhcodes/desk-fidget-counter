import objPath from "./A_61300821021.obj"
import stepPath from "./A_61300821021.step"
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

export const A_61300821021 = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C5517754"
  ]
}}
      manufacturerPartNumber="61300821021"
      footprint={<footprint>
        <platedhole  portHints={["pin1"]} pcbX="-3.81mm" pcbY="-1.27mm" holeWidth="1.1000232mm" holeHeight="1.1000232mm" outerWidth="1.6999966mm" outerHeight="1.6999966mm" rectPad={true} pcbRotation="0deg" shape="pill" />
<platedhole  portHints={["pin2"]} pcbX="-3.81mm" pcbY="1.27mm" outerDiameter="1.6999966mm" holeDiameter="1.1000232mm" shape="circle" />
<platedhole  portHints={["pin3"]} pcbX="-1.27mm" pcbY="-1.27mm" outerDiameter="1.6999966mm" holeDiameter="1.1000232mm" shape="circle" />
<platedhole  portHints={["pin4"]} pcbX="-1.27mm" pcbY="1.27mm" outerDiameter="1.6999966mm" holeDiameter="1.1000232mm" shape="circle" />
<platedhole  portHints={["pin5"]} pcbX="1.27mm" pcbY="-1.27mm" outerDiameter="1.6999966mm" holeDiameter="1.1000232mm" shape="circle" />
<platedhole  portHints={["pin6"]} pcbX="1.27mm" pcbY="1.27mm" outerDiameter="1.6999966mm" holeDiameter="1.1000232mm" shape="circle" />
<platedhole  portHints={["pin7"]} pcbX="3.81mm" pcbY="-1.27mm" outerDiameter="1.6999966mm" holeDiameter="1.1000232mm" shape="circle" />
<platedhole  portHints={["pin8"]} pcbX="3.81mm" pcbY="1.27mm" outerDiameter="1.6999966mm" holeDiameter="1.1000232mm" shape="circle" />
<silkscreenpath route={[{"x":5.2300123999998505,"y":-5.630011599999989},{"x":5.2300123999998505,"y":-3.130042000000003}]} />
<silkscreenpath route={[{"x":-5.230139400000098,"y":-3.130042000000003},{"x":5.2300123999998505,"y":-3.130042000000003}]} />
<silkscreenpath route={[{"x":-5.230012400000078,"y":-5.629986200000076},{"x":5.2300123999998505,"y":-5.629986200000076}]} />
<silkscreenpath route={[{"x":3.314750799999956,"y":-11.62999960000002},{"x":4.209160999999995,"y":-11.62999960000002},{"x":4.209160999999995,"y":-5.629986200000076}]} />
<silkscreenpath route={[{"x":3.314750799999956,"y":-5.629986200000076},{"x":3.314750799999956,"y":-11.62999960000002}]} />
<silkscreenpath route={[{"x":0.8509507999998505,"y":-11.62999960000002},{"x":1.7453610000000026,"y":-11.62999960000002},{"x":1.7453610000000026,"y":-5.629986200000076}]} />
<silkscreenpath route={[{"x":0.8509507999998505,"y":-5.629986200000076},{"x":0.8509507999998505,"y":-11.62999960000002}]} />
<silkscreenpath route={[{"x":-1.7398492000000942,"y":-11.62999960000002},{"x":-0.8454390000001695,"y":-11.62999960000002},{"x":-0.8454390000001695,"y":-5.629986200000076}]} />
<silkscreenpath route={[{"x":-1.7398492000000942,"y":-5.629986200000076},{"x":-1.7398492000000942,"y":-11.62999960000002}]} />
<silkscreenpath route={[{"x":-4.2544238000000405,"y":-11.629974199999992},{"x":-3.3600136000001157,"y":-11.629974199999992},{"x":-3.3600136000001157,"y":-5.630011599999989}]} />
<silkscreenpath route={[{"x":-4.2544238000000405,"y":-5.630011599999989},{"x":-4.2544238000000405,"y":-11.629974199999992}]} />
<silkscreenpath route={[{"x":-5.230012400000078,"y":-5.630011599999989},{"x":-5.229987000000051,"y":-3.130042000000003}]} />
<silkscreentext text="{NAME}" pcbX="-0mm" pcbY="3.159mm" anchorAlignment="center" fontSize="1mm" />
<fabricationnotepath route={[{"x":3.4729928000000427,"y":-5.6730137999999215},{"x":4.126991999999973,"y":-5.6730137999999215},{"x":4.126991999999973,"y":-11.32700299999999},{"x":3.4729928000000427,"y":-11.32700299999999},{"x":3.4729928000000427,"y":-5.6730137999999215}]} strokeWidth="0mm" isFilled hasStroke={false} />
<fabricationnotepath route={[{"x":0.9329927999999654,"y":-5.6730137999999215},{"x":1.5869920000000093,"y":-5.6730137999999215},{"x":1.5869920000000093,"y":-11.32700299999999},{"x":0.9329927999999654,"y":-11.32700299999999},{"x":0.9329927999999654,"y":-5.6730137999999215}]} strokeWidth="0mm" isFilled hasStroke={false} />
<fabricationnotepath route={[{"x":-1.6070071999999982,"y":-5.6730137999999215},{"x":-0.9530079999999543,"y":-5.6730137999999215},{"x":-0.9530079999999543,"y":-11.32700299999999},{"x":-1.6070071999999982,"y":-11.32700299999999},{"x":-1.6070071999999982,"y":-5.6730137999999215}]} strokeWidth="0mm" isFilled hasStroke={false} />
<fabricationnotepath route={[{"x":-4.147007199999962,"y":-5.6730137999999215},{"x":-3.4930080000000316,"y":-5.6730137999999215},{"x":-3.4930080000000316,"y":-11.32700299999999},{"x":-4.147007199999962,"y":-11.32700299999999},{"x":-4.147007199999962,"y":-5.6730137999999215}]} strokeWidth="0mm" isFilled hasStroke={false} />
<courtyardoutline outline={[{"x":-5.330000000000155,"y":2.36999830000002},{"x":5.329974599999787,"y":2.36999830000002},{"x":5.329974599999787,"y":-11.499990199999957},{"x":-5.330000000000155,"y":-11.499990199999957},{"x":-5.330000000000155,"y":2.36999830000002}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 0.000012700000070253736, y: 4.800003099999913, z: -0.28000599999999976 },
      }}
      {...props}
    />
  )
}