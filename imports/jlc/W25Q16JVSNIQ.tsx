import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["N_CS"],
  pin2: ["DO","IO1"],
  pin3: ["N_WP","IO2"],
  pin4: ["GND"],
  pin5: ["DI","IO0"],
  pin6: ["CLK"],
  pin7: ["N_HOLD","N_RESET","IO3"],
  pin8: ["VCC"]
} as const

const pinAttributes = {
  pin4: {requiresGround: true},
  pin8: {requiresPower: true}
} as const

export const W25Q16JVSNIQ = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C2456211"
  ]
}}
      manufacturerPartNumber="W25Q16JVSNIQ"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="-1.905mm" pcbY="-2.682494mm" width="0.6299962mm" height="1.864995mm" radius="0.3149981mm" shape="pill" />
<smtpad portHints={["pin2"]} pcbX="-0.635mm" pcbY="-2.682494mm" width="0.6299962mm" height="1.864995mm" radius="0.3149981mm" shape="pill" />
<smtpad portHints={["pin3"]} pcbX="0.635mm" pcbY="-2.682494mm" width="0.6299962mm" height="1.864995mm" radius="0.3149981mm" shape="pill" />
<smtpad portHints={["pin4"]} pcbX="1.905mm" pcbY="-2.682494mm" width="0.6299962mm" height="1.864995mm" radius="0.3149981mm" shape="pill" />
<smtpad portHints={["pin8"]} pcbX="-1.905mm" pcbY="2.682494mm" width="0.6299962mm" height="1.864995mm" radius="0.3149981mm" shape="pill" />
<smtpad portHints={["pin7"]} pcbX="-0.635mm" pcbY="2.682494mm" width="0.6299962mm" height="1.864995mm" radius="0.3149981mm" shape="pill" />
<smtpad portHints={["pin6"]} pcbX="0.635mm" pcbY="2.682494mm" width="0.6299962mm" height="1.864995mm" radius="0.3149981mm" shape="pill" />
<smtpad portHints={["pin5"]} pcbX="1.905mm" pcbY="2.682494mm" width="0.6299962mm" height="1.864995mm" radius="0.3149981mm" shape="pill" />
<silkscreenpath route={[{"x":-2.576245799999924,"y":-1.5213076},{"x":-2.576245799999924,"y":1.5215361999999004},{"x":2.5761188000000175,"y":1.5215361999999004},{"x":2.5761188000000175,"y":-1.5213076},{"x":-2.576245799999924,"y":-1.5213076}]} />
<silkscreencircle pcbX="-1.9050254mm" pcbY="-0.769112mm" radius="0.150114mm" />
<silkscreencircle pcbX="-2.6723594mm" pcbY="-2.682494mm" radius="0.150114mm" />
<silkscreentext text="{NAME}" pcbX="-0.1242822mm" pcbY="4.2956246mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-2.709989999999948,"y":3.86499149999986},{"x":2.6900002000000995,"y":3.86499149999986},{"x":2.6900002000000995,"y":-3.8649914999999737},{"x":-2.709989999999948,"y":-3.8649914999999737},{"x":-2.709989999999948,"y":3.86499149999986}]} />
      </footprint>}
      cadModel={{
        objUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C2456211.obj?uuid=a8bf75347d3a44d9bc6814f39c22bf07",
        stepUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C2456211.step?uuid=a8bf75347d3a44d9bc6814f39c22bf07",
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 0.0099948999999242, y: -0.06982459999994717, z: -0.8 },
      }}
      {...props}
    />
  )
}