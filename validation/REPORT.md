# Rev C / v3.0.0 validation record

Reviewed 2026-11-04. This is a software-checked prototype; physical hardware tests remain unperformed. Rev C is Ø86×22.3 mm before feet, 52.6% shorter than Rev B. Its clipped PCB has 68×68 mm extents and a 34.6×40.6 mm R2 window for the protected cell, LCD rear connector and independent screen supports.

| Check | Result |
|---|---|
| TypeScript / netlist / schematic | Passed; netlist has zero errors and warnings |
| Placement | Zero native placement DRC errors, warnings or courtyard collisions; eight reviewed orientation suggestions, described below |
| Bare PCB and assembly builds | Both passed with zero circuit errors; 63 PCB components, all assembled from the top |
| Design contract | Physical pin maps, distinct rails, USB, charge controls, encoder and JSTs passed |
| Copper shorts | No shorts detected in the Gerber-derived copper check |
| Independent KiCad 10 DRC | Zero violations, zero unconnected items, no DRC exclusions |
| Gerber / drill inspection | Two closed edge contours, 128 plotted segments; window area 1401.24578 mm²; 222 vias, 27 component plated holes, six NPTHs; four USB plated slots and 16 JST Ø0.75 mm drills |
| BOM / placement | 63 BOM rows, 62 populated placements, all top side; J3 is direct NTC wiring |
| Firmware native tests | Full turns, reversals, wraps, gating, stale/invalid samples, saturation, CRC, 32 torn writes, decimal formatting and LCD scanline/buffer guards passed |
| ARM image | Passed; 59,832 bytes flash, 4,776 bytes data+BSS; CDC+HID descriptors checked |
| Printable geometry | Nine product prints plus fit coupon watertight and connected; fixed/moving and full swept optical-track checks passed |
| PCB nesting | Actual source outline, routed window and NPTHs checked against the base; cell and rear LCD connector clear PCB material |
| Full 3D assembly | 22 named parts; nine printable meshes; OBJ axes/scale, assembled poses, GLB hashes and identical bare/assembled PCB geometry passed |

## Placement suggestions

The CLI's partial placement check uses straight connection lines and exits nonzero for eight centroid-based resistor orientation suggestions: R5, R8, R22, R15, R16, R17, R27 and R28. These were reviewed against the completed routing. They are not placement DRC violations; the actual copper passes both the native checks and independent KiCad clearance/connectivity checks. `check-placement.mjs` accepts only this exact reviewed set, requires zero placement/courtyard DRC errors and a passing full routed circuit, and rejects new placement issues. CI runs the full build first. No copper or fabrication DRC is excluded.

## Mechanical values and physical limits

The grip begins at z10.8 mm, previously z22 mm. The assembly has 0.6 mm bezel/grip radial clearance, 0.5 mm clamp/top-web clearance, 1 mm nominal optical-skirt clearance on each sensor side, 0.85 mm clearance above an 8 mm-high USB plug, and 1.3 mm between the cell and LCD rear connector vertically. These are CAD values, not measurements. The nine prints, 6712ZZ bearing, thin optical-skirt adhesive, screen, connectors and fastener access are described in [ASSEMBLY.md](../ASSEMBLY.md).

Purchased-part models are dimensioned envelopes rather than detailed supplier STEP models. Printed tolerances, cable bends, screen-module fit, bearing retention, adhesive, 950 nm opacity, optical counting, USB signalling, charging temperature and runtime still require [physical bring-up](BRINGUP.md). No hardware has been ordered or physically tested.

See [logs](logs/), [independent DRC](kicad-drc.json), [fabrication inspection](manufacturing-inspection.json), [assembly geometry](../mechanical/geometry-check.json) and [height budget/reference research](../mechanical/LOW_PROFILE.md). Release hashes are recorded in the root manifest.
