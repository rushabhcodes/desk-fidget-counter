# Rev B / v2.0.0 validation record

Reviewed 2026-11-04. This release implements the fixed 1.28-inch screen, optical rotating ring, left toggle and populated JST programming connector. It is a **software-checked prototype design**; no physical board has been assembled or measured.

| Check | Result |
|---|---|
| TypeScript | Passed with the pinned dependency lockfile |
| Netlist / schematic placement / PCB placement | Passed; no actionable placement errors or warnings |
| Bare-board and native assembly builds | Passed; zero circuit error/warning records |
| Physical pin/net contract | 63 components; MCU, optical common collector, Schmitt outputs, PA8 screen CS, USB/power and JST pin maps checked |
| Gerber-derived copper shorts | No shorts detected on either layer |
| Independent KiCad 10 DRC | **0 violations, 0 unconnected items**, no exclusions |
| Gerber/Excellon parser | 9 graphical layers; Ø64 mm / 128 segments; 193 round plated drills, 4 plated slots, 6 NPTH; source drill counts agree |
| JST drills | 16 finished Ø0.75 mm holes across PH2 / PH6 / PH8 |
| BOM / placements | 63 source components, 62 populated; J3 is direct NTC wiring, no header |
| Native firmware tests | Full turns both directions, 16-bit wrap, partial reversal, slow edges, scroll gating, stale/invalid/jump samples, saturation, CRC/torn writes and 64-bit formatting passed |
| LCD renderer tests | All 240 scanlines, 20-digit count/fault states and buffer guards passed; example UI rendered and visually inspected |
| ARM image | 59,832 bytes flash; 4,776 bytes data+BSS in 16 KB RAM; valid stack/reset/USB IRQ vectors |
| Linked USB descriptors | CDC + relative HID wheel; 3 interfaces / 4 endpoints; 500 mA configuration |
| Printable solids | Seven product pieces plus fit coupon watertight and connected as intended; moving/fixed and swept-skirt checks passed |
| Native 3D assembly | 20 named models, seven exact print meshes; OBJ axes/scale/bounds, GLB hashes and every PCB record checked against the bare board |
| Complete product GLBs | Self-contained assembled/exploded models, metres/+Y-up; Ø80×47 mm assembled envelope |

Logs are in [logs](logs). Detailed physical tests remain in [BRINGUP.md](BRINGUP.md).

## Source-to-fabrication handling

The final board is exported from tscircuit with its source pads, nets and prescribed copper. The KiCad finalizer applies the declared 0.10 mm minimum track / 0.15 mm copper clearance rules, normal ground refill/island removal, a 64% QFN exposed-pad paste aperture and shorter QFP corner silkscreen marks. Any entire isolated ground fragment is removed only when KiCad identifies it as isolated, with an audit in [pour-cleanup.json](pour-cleanup.json). Final DRC is strict; no check or reported violation is excluded. The Gerber bundle is plotted from that final board and parsed independently.

The native CLI may print a ground-path cache serialization notice for prejoined terminals. Released paths are prescribed in `routing/routes.json`; this cache notice does not bypass connectivity checks. Both native builds return success and independent KiCad reports zero unconnected items.

## Mechanical and display scope

Nominal checked clearances are 0.6 mm bezel-to-grip radially, 0.5 mm skirt-to-lid axially, 1.0 mm on each side of the optical skirt, 2.0 mm cell-envelope-to-PCB and 1.2 mm to header tails trimmed to 0.8 mm. The lid uses M2×10 screws with 3.5 mm base engagement. These values are model inputs/results, not measurements of printed parts.

The 48-slot skirt and 0.8 mm optical channel spacing give approximately 87.7° quadrature at the 25.0799 mm radius. Firmware expects 192 edges/revolution. IR opacity, actual contrast, alignment, dust/ambient-light response, speed accuracy and bearing feel require a physical prototype. The timer-running and LCD-transport status flags do not prove optical contrast or display presence.

The screen and its cable remain fixed through the hollow bearing post. The row renderer uses a 480-byte buffer rather than a full framebuffer. Purchased-part CAD is dimensioned envelope geometry, including a conservative LCD rear-connector allowance; flexible wiring and detailed vendor internals are omitted. Follow the assembly guide and inspect the real module before tightening.

The [release manifest](../release-manifest.json) binds source and output hashes to Git tag `v2.0.0`. Physical USB operation, charging/NTC/thermal behaviour, power handover, runtime, persistence under real power cuts, lead insulation and printed fit remain unperformed. TinyUSB development VID/PID must be replaced with authorized identifiers for commercial distribution.
