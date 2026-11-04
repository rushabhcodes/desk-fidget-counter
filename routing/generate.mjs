// SPDX-License-Identifier: MIT
// Node 26.12.1; the worker runtime is supplied by the locked autorouter package.
// Generates a candidate, never silently replaces the reviewed copper.
import fs from 'node:fs'
import { AutoroutingPipelineSolver9_PreloadedTraceGraph } from '@tscircuit/capacity-autorouter'
import { createAutorouterSolverRuntime } from '@tscircuit/capacity-autorouter/runtime/node'

const original = JSON.parse(fs.readFileSync('routing/input.json', 'utf8'))
const srj = structuredClone(original)
const cutoutStripe = o => !o.circuitJsonMetadata && o.layers?.length === 2 &&
  Math.abs(o.center.x + .5) < .01 && o.width > 30 && o.height < .61 &&
  o.center.y > -22 && o.center.y < 19
const stripes = srj.obstacles.filter(cutoutStripe).length
if (stripes !== 68) throw new Error('Window decomposition changed: review the conservative routing envelope')
srj.obstacles = srj.obstacles.filter(o => !cutoutStripe(o))
srj.obstacles.push({ type: 'rect', layers: ['top', 'bottom'],
  center: { x: -.5, y: -1.5 }, width: 35, height: 41, connectedTo: [] })

const solver = new AutoroutingPipelineSolver9_PreloadedTraceGraph(srj, { effort: .1 })
const runtime = createAutorouterSolverRuntime({ workerCount: 4, requireWorker: true })
const timer = setInterval(() => console.log(solver.getCurrentPhase(), solver.progress), 30000)
try {
  await solver.solveAsync(runtime)
  if (solver.failed) throw new Error(solver.error)
  const traces = solver.getOutputSimplifiedPcbTraces()
  fs.writeFileSync('routing/candidate.json', JSON.stringify({ connections: original.connections, traces }) + '\n')
  console.log(`Generated ${traces.length} candidate branches. Rebuild and validate before replacing routes.json.`)
} finally {
  clearInterval(timer)
  await runtime.dispose()
}
