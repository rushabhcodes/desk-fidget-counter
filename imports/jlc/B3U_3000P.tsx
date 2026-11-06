import type { PushButtonProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["pin1"],
  pin2: ["pin2"]
} as const

export const B3U_3000P = (props: PushButtonProps<typeof pinLabels>) => {
  const { name = "SW1", ...restProps } = props

  return (
    <pushbutton
      name={name}
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C963349"
  ]
}}
      manufacturerPartNumber="B3U-3000P"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="-1.700022mm" pcbY="0mm" width="0.7999984mm" height="1.6999966mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="1.700022mm" pcbY="0mm" width="0.7999984mm" height="1.6999966mm" shape="rect" />
<silkscreenpath route={[{"x":0.4500117999998565,"y":1.949983399999951},{"x":-0.4499864000000571,"y":1.949983399999951},{"x":-0.8499855999999681,"y":1.5459963999999218},{"x":-0.8499855999999681,"y":1.3800074000000677}]} />
<silkscreenpath route={[{"x":0.449579999999969,"y":1.950719999999933},{"x":0.8510015999999041,"y":1.5459963999999218},{"x":0.8508999999999105,"y":1.379220000000032}]} />
<silkscreenpath route={[{"x":-1.4999970000000076,"y":-1.2500356000001602},{"x":1.4999970000000076,"y":-1.2500102000000197}]} />
<silkscreenpath route={[{"x":-1.4999970000000076,"y":1.2499594000000798},{"x":1.4999970000000076,"y":1.2499594000000798}]} />
<silkscreenpath route={[{"x":1.4999970000000076,"y":1.081125600000064},{"x":1.4999970000000076,"y":1.2499594000000798}]} />
<silkscreenpath route={[{"x":-1.4999970000000076,"y":1.2499594000000798},{"x":-1.4999970000000076,"y":1.081125600000064}]} />
<silkscreenpath route={[{"x":-1.4999970000000076,"y":-1.081150999999977},{"x":-1.4999970000000076,"y":-1.2500102000000197}]} />
<silkscreenpath route={[{"x":1.4999970000000076,"y":-1.2500102000000197},{"x":1.4999970000000076,"y":-1.081150999999977}]} />
<silkscreentext text="{NAME}" pcbX="-0.0127mm" pcbY="2.9558mm" anchorAlignment="center" fontSize="1mm" />
<fabricationnotepath route={[{"x":-0.8499856000000818,"y":1.4999970000000076},{"x":0,"y":1.949983399999951},{"x":0.8500110000001087,"y":1.4999970000000076},{"x":-0.8499856000000818,"y":1.4999970000000076}]} strokeWidth="0mm" isFilled hasStroke={false} />
<courtyardoutline outline={[{"x":-2.3500212000000147,"y":2.1959955999999465},{"x":2.3500212000000147,"y":2.1959955999999465},{"x":2.3500212000000147,"y":-1.5039980000000241},{"x":-2.3500212000000147,"y":-1.5039980000000241},{"x":-2.3500212000000147,"y":2.1959955999999465}]} />
      </footprint>}
      cadModel={{
        objUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C963349.obj?uuid=d1ba1a65d84b4871ac1456490a2ad18b",
        stepUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C963349.step?uuid=d1ba1a65d84b4871ac1456490a2ad18b",
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 0, y: -0.3459987999999612, z: -0.01 },
      }}
      {...restProps}
    />
  )
}