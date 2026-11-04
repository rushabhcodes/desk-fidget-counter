# Rev D / v4.0.0 validation record

Reviewed 2026-11-04. This is a **software-checked prototype design**; physical hardware tests remain unperformed. Rev D removes the internal cell and charging network and adds a USB laptop dashboard. The Ø86×22.3 mm assembly retains the side USB-C port, left scroll toggle and fixed Waveshare 19192 screen. Its 68×68 mm clipped PCB has a 34.6×40.6 mm R2 window for the static display harness and independent supports.

| Check | Result |
|---|---|
| TypeScript / netlist / schematic | Passed; seven named functional schematic sheets with chip-function and rating notes |
| Placement | Zero placement/courtyard errors; four reviewed orientation hints and one internal-window connector-access advisory, described below |
| Bare PCB and assembly builds | Both passed with zero circuit errors; 44 PCB components, all mounted on top |
| Design contract | Physical pin maps, USB-only rails, switched LCD/IR supply, USB, encoder, FRAM and both JSTs passed |
| Copper shorts | No shorts detected in the Gerber-derived copper check |
| Independent KiCad 10 DRC | Zero violations, zero unconnected items, no DRC exclusions |
| Gerber / drill inspection | Two closed contours, 128 edge segments; window area 1401.24578 mm²; 178 vias, 23 component plated holes including four USB slots, six NPTHs; 14 JST Ø0.75 mm drills |
| BOM / placement | 44 BOM rows and 44 populated placements, all top side |
| Firmware native tests | Turns/reversals, timer wrap, scroll gating, rejected samples, saturation, CRC/torn writes, 64-bit formatting, LCD scanline bounds and dashboard parsing/calendar/staleness passed |
| Companion tests | Metric encoding, missing laptop battery and application identity checks passed; actual pyserial plus live psutil sample passed through a Linux PTY device simulator |
| ARM image | 61,032 bytes flash, 4,840 bytes data+BSS; vector table and linked CDC+HID descriptors checked; bus-powered 100 mA configuration |
| Printable geometry | Nine product prints plus fit coupon watertight and connected; nominal fixed/moving and full swept optical-track checks passed |
| Purchased parts / harness | All 44 PCB package meshes, the official screen STEP, two mated PH8 plugs and eight individual wire paths checked against prints and the swept rotor; wires also checked against one another |
| Full 3D assembly | 24 named mechanical parts plus native populated PCB; OBJ axes/scale, assembled poses, GLB hashes and identical bare/assembled PCB geometry passed |

## Reviewed placement advisories

The CLI's partial placement check uses straight connection lines and suggests rotating R15, R16, R27 and R28. The completed copper passes native and independent clearance/connectivity checks. J6 points **+X into the routed internal window**, where its mating PH8 housing and cable fit; the CLI's outer-edge heuristic instead requests −X. The correct insertion direction is retained in the source. The actual header, mated plug and wire paths are checked in the assembly geometry.

`check-placement.mjs` accepts only this exact set, requires zero placement/courtyard errors, the passing full routed circuit and the internal-window geometry assertion, and rejects new placement issues. No copper or fabrication DRC is excluded. The switch body courtyard intentionally overhangs the board; its pads and drills still satisfy fabrication edge rules.

## Export and artifact scope

The source contains 117 prescribed routing branches, rendered as 127 PCB traces and 178 manufactured vias. Routed vias are Ø0.6/0.3 mm; three ground stitches are Ø0.7/0.3 mm. An independent USB locating-hole spacing check moved one routed ground via away from the hole, and the left ground stitch was moved to connect the top fragment to the main bottom pour. Near-coincident route vertices were collapsed before export. The final checked geometry is in the source and release artifacts.

The KiCad finalizer starts from a fresh circuit-JSON export, checks its population against the source, assigns distinct priorities to same-net ground-pour fragments, refills/removes isolated ground copper and shortens MCU corner silkscreen strokes. Positions, nets, pads and routed copper otherwise come from tscircuit. Its DRC must pass without exclusions before Gerbers are plotted. See [manufacturing](../manufacturing/README.md).

## Mechanical values and physical limits

The grip begins at z10.8 mm; overall height remains 22.3 mm before feet. Nominal clearances include 0.6 mm bezel/grip radial clearance, 1 mm optical-skirt clearance on each sensor side, 1.65 mm above the specified 6.4 mm USB plug envelope and 0.2 mm front-glass bezel relief. The eight 32AWG wires use a minimum 6.2 mm centreline bend radius at 0.6096 mm worst-case OD. These are CAD values, not measurements.

The screen geometry is a rigid, unscaled transform of Waveshare's official STEP. Package meshes come from the documented KiCad/supplier sources; the sensor, toggle, bearing and crimp details have explicit simplifications. Sources and rights are recorded in [vendor CAD provenance](../mechanical/vendor/README.md). Nominal fastener heads clear all 14 printed countersinks; threads intentionally engage prepared M2 pilots.

**Physical fit, crimp quality, printed tolerances, 950 nm opacity, optical counts, USB signal integrity/inrush/suspend current and real macOS/Windows/Linux USB operation remain untested.** The serial smoke test uses a PTY simulator, not fabricated hardware. The companion must run to provide laptop metrics; stale data disappears after five seconds. USB suspend blanks the screen and turns the optical emitter off, so rotation during host suspend is not counted. No hardware has been ordered or physically tested.

See [bring-up checklist](BRINGUP.md), [logs](logs/), [independent DRC](kicad-drc.json), [fabrication inspection](manufacturing-inspection.json), [assembly geometry](../mechanical/geometry-check.json), [wiring](../manufacturing/WIRING.md) and [assembly guide](../ASSEMBLY.md). Release hashes are recorded in the root manifest.
