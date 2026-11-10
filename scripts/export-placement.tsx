import { Circuit } from "tscircuit"
import { mkdirSync, writeFileSync } from "node:fs"
import Board from "../index.circuit"

const circuit = new Circuit()
circuit.pcbRoutingDisabled = true
circuit.add(<Board />)
await circuit.renderUntilSettled()
const data = circuit.getCircuitJson()
const errors = data.filter(element => element.type.endsWith("_error"))
if (errors.length) throw new Error(JSON.stringify(errors, null, 2))
mkdirSync("dist/placement", { recursive: true })
writeFileSync("dist/placement/circuit.json", JSON.stringify(data, null, 2) + "\n")
console.log("Exported checked, unrouted source placement to dist/placement/circuit.json.")
