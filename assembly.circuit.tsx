// SPDX-License-Identifier: MIT
import { assembly } from "tscircuit"
import Board from "./index.circuit"
import parts from "./mechanical/cad/parts.json"
import { version } from "./package.json"

// Immutable release URLs keep the CAD viewer independent of local file servers.
// The same OBJ files are also included in this project for offline inspection.
const assetBase = `https://raw.githubusercontent.com/rushabhcodes/desk-fidget-counter/v${version}/mechanical/cad/`

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
          material="petg" cadModel={cadModel} />
      ) : (
        <assembly.part key={part.name} name={part.name}
          displayName={part.description} cadModel={cadModel} />
      )
    })}
  </assembly.device>
)
