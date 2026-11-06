import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["IN"],
  pin2: ["GND"],
  pin3: ["ON"],
  pin4: ["NC"],
  pin5: ["QOD"],
  pin6: ["VOUT"]
} as const

const pinAttributes = {
  pin2: {requiresGround: true},
  pin4: {doNotConnect: true}
} as const

export const TPS22919DCKR = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C2149796"
  ]
}}
      manufacturerPartNumber="TPS22919DCKR"
      footprint={<footprint>
        <smtpad portHints={["pin6"]} pcbX="-0.94996mm" pcbY="-0.649986mm" width="0.5999988mm" height="0.419989mm" shape="rect" />
<smtpad portHints={["pin5"]} pcbX="-0.94996mm" pcbY="0mm" width="0.5999988mm" height="0.419989mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="-0.94996mm" pcbY="0.649986mm" width="0.5999988mm" height="0.419989mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="0.94996mm" pcbY="0.649986mm" width="0.5999988mm" height="0.419989mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="0.94996mm" pcbY="0mm" width="0.5999988mm" height="0.419989mm" shape="rect" />
<smtpad portHints={["pin1"]} pcbX="0.94996mm" pcbY="-0.649986mm" width="0.5999988mm" height="0.419989mm" shape="rect" />
<silkscreenpath route={[{"x":-0.6999986000000007,"y":-1.099997799999997},{"x":0.6999986000000149,"y":-1.099997799999997}]} />
<silkscreenpath route={[{"x":-0.6999986000000007,"y":1.099997799999997},{"x":0.6999986000000149,"y":1.099997799999997}]} />
<silkscreenpath route={[{"x":1.0909300000000144,"y":-1.0942066000000068},{"x":0.9672082130372104,"y":-1.2198285560875775},{"x":1.0922000000000054,"y":-1.3441869478927941},{"x":1.2171917869628146,"y":-1.2198285560875775},{"x":1.0934700000000106,"y":-1.0942066000000068}]} />
<silkscreentext text="{NAME}" pcbX="0.101346mm" pcbY="2.1049mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-1.4999594000000087,"y":1.2499979999999908},{"x":1.4999594000000087,"y":1.2499979999999908},{"x":1.4999594000000087,"y":-1.2499980000000193},{"x":-1.4999594000000087,"y":-1.2499980000000193},{"x":-1.4999594000000087,"y":1.2499979999999908}]} />
      </footprint>}
      cadModel={{
        objUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C2149796.obj?uuid=a5d40c04f23243b2af27dc3bf34f18d3",
        stepUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C2149796.step?uuid=a5d40c04f23243b2af27dc3bf34f18d3",
        pcbRotationOffset: 180,
        modelOriginPosition: { x: 0.000012700000013410317, y: 0, z: -0.1 },
      }}
      {...props}
    />
  )
}