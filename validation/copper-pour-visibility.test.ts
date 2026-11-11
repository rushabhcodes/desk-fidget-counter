import { describe, expect, test } from "bun:test"
import { readFileSync } from "node:fs"
import fixture from "./fixtures/v603-ground-pour-gap.json"

// Load the installed core's private visibility utility from its compiled bundle.
const bundle = readFileSync(new URL(import.meta.resolve("@tscircuit/core")), "utf8")
const marker = "// lib/components/primitive-components/CopperPour/utils/mark-trace-segments-inside-copper-pour.ts"
const start = bundle.indexOf(marker)
const end = bundle.indexOf("\n// lib/", start + marker.length)
if (start < 0 || end < 0) throw new Error("Could not locate the trace visibility utility in the installed core")
const { markTraceSegmentsInsideCopperPour: mark } = new Function(
  `${bundle.slice(start, end)}; return {markTraceSegmentsInsideCopperPour};`,
)()

const wire = (x: number, y: number, layer = "top") => ({ route_type: "wire", x, y, layer, width: .15 })
const ring = (points: number[][]) => ({ vertices: points.map(([x, y]) => ({ x, y })) })
const square = [[0, 0], [10, 0], [10, 10], [0, 10]]
const pour = (outer = square, holes: number[][][] = []) => ({
  type: "pcb_copper_pour", pcb_copper_pour_id: "pour", source_net_id: "gnd",
  shape: "brep", layer: "top",
  brep_shape: { outer_ring: ring(outer), inner_rings: holes.map(ring) },
})
function annotate(route: any[], copperPour: any = pour(), sourceNet = "gnd") {
  let trace = { type: "pcb_trace", pcb_trace_id: "trace", source_trace_id: sourceNet, route: structuredClone(route) }
  mark({ copperPour, db: {
    source_trace: { list: () => [] },
    pcb_trace: { list: () => [trace], update: (_id: string, update: any) => { trace = { ...trace, ...update } } },
  } })
  return trace.route
}
const hidden = (route: any[], index = 0) =>
  route[index].is_inside_copper_pour === true && route[index + 1].is_inside_copper_pour === true

describe("copper-pour trace visibility", () => {
  test("the exact published 13.0963mm continuation stays visible across its 0.5007mm pour gap", () => {
    const input = fixture.trace.route
    const output = annotate(input, fixture.pour, fixture.pour.source_net_id)
    expect(hidden(output)).toBe(false)
    expect(output).toEqual(input) // No coordinates, layers, widths or connectivity are changed.
  })

  test("a narrow hole between the old five sample locations is not skipped", () => {
    const hole = [[3.1, 4.9], [3.3, 4.9], [3.3, 5.1], [3.1, 5.1]]
    expect(hidden(annotate([wire(1, 5), wire(9, 5)], pour(square, [hole])))).toBe(false)
  })

  test("shared endpoints of covered neighbours do not hide an uncovered middle segment", () => {
    const hole = [[4, 4], [6, 4], [6, 6], [4, 6]]
    const result = annotate([wire(1, 5), wire(3, 5), wire(7, 5), wire(9, 5)], pour(square, [hole]))
    expect(hidden(result, 1)).toBe(false)
  })

  test("a completely covered segment can still be skipped", () => {
    expect(hidden(annotate([wire(1, 5), wire(9, 5)]))).toBe(true)
  })

  test("rectangle containment handles rotation", () => {
    const rect = { ...pour(), shape: "rect", center: { x: 5, y: 5 }, width: 8, height: 1, rotation: 45 }
    expect(hidden(annotate([wire(3, 3), wire(7, 7)], rect))).toBe(true)
    expect(hidden(annotate([wire(3, 7), wire(7, 3)], rect))).toBe(false)
  })

  test("different nets and layers remain visible", () => {
    expect(hidden(annotate([wire(1, 5), wire(9, 5)], pour(), "vbus"))).toBe(false)
    expect(hidden(annotate([wire(1, 5, "bottom"), wire(9, 5, "bottom")]))).toBe(false)
  })

  test("a closed ring's repeated vertex is not an infinite boundary", () => {
    expect(hidden(annotate([wire(11, 5), wire(12, 5)], pour([...square, square[0]])))).toBe(false)
  })

  test("zero-length tracks and layer changes are not classified as covered wires", () => {
    expect(hidden(annotate([wire(1, 5), wire(1, 5)]))).toBe(false)
    expect(hidden(annotate([wire(1, 5), { route_type: "via", x: 1, y: 5, from_layer: "top", to_layer: "bottom" }, wire(1, 5, "bottom")]))).toBe(false)
  })
})
