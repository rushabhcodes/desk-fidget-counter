import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["A"],
  pin2: ["NC"],
  pin3: ["C2"],
  pin4: ["E1"],
  pin5: ["E2"],
  pin6: ["C1"]
} as const

const pinAttributes = {
  pin2: {doNotConnect: true}
} as const

export const TCUT1600X01 = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      symbol={
        <symbol>
          <port name="pin4" pinNumber={4} aliases={["E1"]} direction="right" schX={0.6} schY={-0.4} schStemLength={0.2} />
          <port name="pin5" pinNumber={5} aliases={["E2"]} direction="right" schX={0.6} schY={0} schStemLength={0.2} />
          <port name="pin6" pinNumber={6} aliases={["C1"]} direction="right" schX={0.6} schY={0.4} schStemLength={0.2} />
          <port name="pin3" pinNumber={3} aliases={["C2"]} direction="left" schX={-0.8} schY={-0.4} schStemLength={0.2} />
          <port name="pin1" pinNumber={1} aliases={["A"]} direction="left" schX={-0.8} schY={0.4} schStemLength={0.2} />
          <schematicpath points={[{"x":0.2,"y":-0.4},{"x":0.4,"y":-0.4}]} strokeColor="#880000" />
          <schematicpath points={[{"x":0.2,"y":0.4},{"x":0.4,"y":0.4}]} strokeColor="#880000" />
          <schematicpath points={[{"x":0,"y":-0.28},{"x":0.2,"y":-0.4},{"x":0.12,"y":-0.38}]} strokeColor="#880000" />
          <schematicpath points={[{"x":0.2,"y":-0.4},{"x":0.14,"y":-0.34}]} strokeColor="#880000" />
          <schematicpath points={[{"x":0.2,"y":0.06},{"x":0.14,"y":0.12}]} strokeColor="#880000" />
          <schematicpath points={[{"x":0,"y":0.18},{"x":0.2,"y":0.06},{"x":0.12,"y":0.08}]} strokeColor="#880000" />
          <schematicpath points={[{"x":0,"y":-0.16},{"x":0.2,"y":-0.1},{"x":0.32,"y":-0.1},{"x":0.32,"y":0.4}]} strokeColor="#880000" />
          <schematicpath points={[{"x":0,"y":0.28},{"x":0.2,"y":0.4}]} strokeColor="#880000" />
          <schematicpath points={[{"x":0,"y":-0.1},{"x":0,"y":-0.34}]} strokeColor="#880000" />
          <schematicpath points={[{"x":0,"y":0.12},{"x":0,"y":0.36}]} strokeColor="#880000" />
          <schematicpath points={[{"x":0.4,"y":0},{"x":0.2,"y":0},{"x":0.2,"y":0.06}]} strokeColor="#880000" />
          <schematicpath points={[{"x":-0.36,"y":-0.08},{"x":-0.16,"y":-0.08}]} strokeColor="#880000" />
          <schematicpath points={[{"x":-0.36,"y":0.08},{"x":-0.16,"y":0.08},{"x":-0.26,"y":-0.08},{"x":-0.36,"y":0.08}]} strokeColor="#880000" />
          <schematicpath points={[{"x":-0.6,"y":0.4},{"x":-0.26,"y":0.4},{"x":-0.26,"y":-0.4},{"x":-0.6,"y":-0.4}]} strokeColor="#880000" />
          <port name="pin2" pinNumber={2} aliases={["NC"]} direction="left" schX={-0.8} schY={0} schStemLength={0.2} />
          <schematicrect schX={-0.1} schY={0} width={1} height={1.2} strokeWidth={0.02} color="#880000" />
          <schematictext schX={-0.1} schY={0.808} text="{NAME}" fontSize={0.2} anchor="bottom_center" />
        </symbol>
      }
      supplierPartNumbers={{
  "jlcpcb": [
    "C511085"
  ]
}}
      manufacturerPartNumber="TCUT1600X01"
      footprint={<footprint>
        <smtpad portHints={["pin6"]} pcbX="2.449957mm" pcbY="1.400048mm" width="1.8999962mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="-2.449957mm" pcbY="-0mm" width="1.8999962mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="2.449957mm" pcbY="-1.400048mm" width="1.8999962mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="-2.449957mm" pcbY="-1.400048mm" width="1.8999962mm" height="1.1999976mm" shape="rect" />
<smtpad portHints={["pin5"]} pcbX="2.449957mm" pcbY="-0mm" width="1.8999962mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin1"]} pcbX="-2.449957mm" pcbY="1.400048mm" width="1.8999962mm" height="1.1999976mm" shape="rect" />
<silkscreenpath route={[{"x":-1.143000000000029,"y":-1.5240000000001146},{"x":-0.6360922000000073,"y":-1.5240000000001146},{"x":-0.6360922000000073,"y":1.3969999999998208},{"x":-1.1440922000000455,"y":1.3969999999998208}]} />
<silkscreenpath route={[{"x":2.5400508000000173,"y":-2.031949200000099},{"x":2.5400508000000173,"y":-2.2859492000001183},{"x":-2.5399492000000237,"y":-2.2859492000001183},{"x":-2.5399492000000237,"y":-2.2310852000000523}]} />
<silkscreenpath route={[{"x":-2.5399492000000237,"y":2.231186799999932},{"x":-2.5399492000000237,"y":2.2860507999998845},{"x":2.5400508000000173,"y":2.2860507999998845},{"x":2.5400508000000173,"y":2.0320507999998654}]} />
<silkscreentext text="{NAME}" pcbX="0.013843mm" pcbY="3.289048mm" anchorAlignment="center" fontSize="1mm" />
<fabricationnotepath route={[{"x":-1.1393931999999722,"y":-1.615719399999989},{"x":-0.6324853999999505,"y":-1.615719399999989},{"x":-0.5617748633028441,"y":-1.586430136697345},{"x":-0.5324855999999727,"y":-1.515719600000125},{"x":-0.5324855999999727,"y":1.4052803999999242},{"x":-0.5617838420440648,"y":1.475974517523582},{"x":-0.6324853999999505,"y":1.5052547999999888},{"x":-1.140485399999875,"y":1.5052547999999888},{"x":-1.2388915144503017,"y":1.4052677000000813},{"x":-1.140485399999875,"y":1.3052805999999464},{"x":-0.7324852000000419,"y":1.3052805999999464},{"x":-0.7324852000000419,"y":-1.4157452000000603},{"x":-1.1393931999999722,"y":-1.4157452000000603},{"x":-1.237799314450399,"y":-1.5157322999999678},{"x":-1.1393931999999722,"y":-1.615719399999989}]} strokeWidth="0mm" isFilled hasStroke={false} />
<fabricationnotepath route={[{"x":-1.1405108000000155,"y":0.08305799999993724},{"x":-0.12451080000005277,"y":0.08305799999993724},{"x":-0.6325107999999773,"y":-0.4249419999999873},{"x":-1.1405108000000155,"y":0.08305799999993724}]} strokeWidth="0mm" isFilled hasStroke={false} />
<fabricationnotepath route={[{"x":-1.130503200000021,"y":-0.32796480000001793},{"x":-0.1605026000000862,"y":-0.32796480000001793},{"x":-0.1605026000000862,"y":-0.5079746000000114},{"x":-1.130503200000021,"y":-0.5079746000000114},{"x":-1.130503200000021,"y":-0.32796480000001793}]} strokeWidth="0mm" isFilled hasStroke={false} />
<courtyardoutline outline={[{"x":-3.6499551000000565,"y":2.269985800000086},{"x":3.6499551000000565,"y":2.269985800000086},{"x":3.6499551000000565,"y":-2.269985799999972},{"x":-3.6499551000000565,"y":-2.269985799999972},{"x":-3.6499551000000565,"y":2.269985800000086}]} />
      </footprint>}
      cadModel={{
        objUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C511085.obj?uuid=bf879952782a41309bb0937e7ded1595",
        stepUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C511085.step?uuid=bf879952782a41309bb0937e7ded1595",
        pcbRotationOffset: 180,
        modelOriginPosition: { x: 0.004999999999886429, y: 0, z: -0.00005 },
      }}
      {...props}
    />
  )
}