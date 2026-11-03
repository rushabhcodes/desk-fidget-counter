// SPDX-License-Identifier: MIT
import saved from "./routing/routes.json"

/** Prescribed, reviewable copper paths. All tscircuit DRC checks still run.
 * The terminal contract prevents stale routes from being reused after an edit.
 * Modify the routes deliberately and re-run all checks when the contract changes.
 */
export async function routeBoard(input: any) {
  const contract = (connections: any[]) => connections.map(c => ({
    name: c.name, pointsToConnect: c.pointsToConnect,
    externallyConnectedPointIds: c.externallyConnectedPointIds,
  }))
  if (JSON.stringify(contract(input.connections)) !== JSON.stringify(contract(saved.connections))) {
    throw new Error("PCB routing terminals changed: regenerate routing/routes.json and validate the new copper")
  }
  const handlers = new Map<string, (event: any) => void>()
  return {
    on(event: string, handler: (event: any) => void) { handlers.set(event, handler) },
    start() { handlers.get("complete")?.({ traces: structuredClone(saved.traces) }) },
    stop() {},
  }
}
