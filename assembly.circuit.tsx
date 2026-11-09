// SPDX-License-Identifier: MIT
import { assembly } from "tscircuit"
import Board from "./index.circuit"
import parts from "./mechanical/cad/parts.json"
// The platform resolves these included assets relative to the project.
const assetBase = "./mechanical/cad/"

export default () => (
  <assembly.device name="DESK_KNOB_ASSEMBLY">
    <Board />
    {parts.map(part => {
      const cadModel = {
        objUrl: `${assetBase}${part.asset}`,
        modelOriginPosition: { x: 0, y: 0, z: 0 },
        modelUnitToMmScale: 1,
      }
      return part.printed ? (
        <assembly.printedpart key={part.name} name={part.name} color={part.color}
          material="pla" cadModel={cadModel} />
      ) : (
        <assembly.part key={part.name} name={part.name}
          displayName={part.description} cadModel={cadModel} />
      )
    })}
  </assembly.device>
)
