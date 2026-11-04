# Manufacturing / Rev B

Manufacturer: **JLCPCB bare-board fabrication**, followed by supervised manual/reflow assembly. No board or assembly order has been placed. The provided placement file is a coordinate reference; automated assembly requires the assembler to map feeder rotations to the verified pin-1 assembly drawing.

## Stackup and rules

| Parameter | Requirement |
|---|---|
| Outline | Ø64 mm, 128-segment approximation; 4 × Ø2.7 mm NPTH at (±21, ±21) mm |
| Material | FR-4, 1.6 mm nominal, standard Tg ≥135°C |
| Copper | Two layers, 35 µm / 1 oz finished outer copper |
| Finish | ENIG; green solder mask, white silkscreen |
| Trace | Signals/low-current branches ≥0.10 mm; main power paths 0.25 mm |
| Copper clearance | ≥0.15 mm; ground pour clearance 0.25 mm |
| Routing via | Ø0.30 mm finished drill / Ø0.70 mm pad, tented both sides |
| Hole spacing | ≥0.50 mm drill-edge spacing for routed vias, with larger routing allowance |
| Copper to NPTH | ≥0.25 mm; pour cutout allowance 0.30 mm |
| Copper to board edge | ≥0.30 mm; ground pours inset 0.40 mm |
| Solder paste | 100 µm stencil starting point; BQ24074 EP reduced to a 1.36 × 1.36 mm aperture (64% area) |
| Assembly | Top SMT reflow; bottom JST, top JST and toggle hand soldered; J3 wired directly to NTC |

See [JLCPCB's capabilities](https://jlcpcb.com/capabilities/pcb-capabilities/) for current process limits. These project rules are more conservative than the process's minimum trace and hole sizes. No controlled-impedance order is claimed: USB is 12 Mbit/s over short PCB runs; signal integrity must be measured on the prototype.

## Authoritative output

The release's `desk-knob-revb-gerbers.zip` contains the **final KiCad-plotted** copper, solder mask, silk, paste, outline, plated drill and NPTH drill files. Use that bundle for the release; older development outputs are not release fabrication files.

The final source-derived KiCad board and project are included so the fabrication geometry and rules can be independently inspected. `scripts/export-fabrication.py` preserves positions, pads, nets and routes from tscircuit, removes floating copper islands by a normal zone refill, applies the reduced QFN paste aperture, shortens the MCU's corner silkscreen marks by 0.25 mm to clear mask openings, runs DRC without exclusions, and plots Gerber/Excellon files. This finalization is part of the documented source-to-fabrication workflow.

`BOM.csv` includes exact manufacturer part numbers. The off-board cell, NTC, bearing, screen, screws and prints are listed in ASSEMBLY.md. `pick-and-place.csv` uses KiCad's board coordinates, millimetres, board side and rotation. J3 is excluded from population; J4 and J6 are populated. For hand assembly, use the assembly drawing and actual physical pin numbers rather than treating a generic centroid rotation as a feeder setup instruction.

## Reproduce

With Bun, KiCad 10 CLI and its matching Python `pcbnew` module installed:

```sh
bun install --frozen-lockfile
bun run build
bun run check:shorts
bunx tsci export dist/index/circuit.json -f kicad_pcb -o /tmp/desk-knob-raw.kicad_pcb
/usr/bin/python3 scripts/export-fabrication.py /tmp/desk-knob-raw.kicad_pcb
```

The exporter stops on any reported KiCad DRC violation. Packaging and preview scripts then parse and inspect those plotted files and record SHA-256 hashes. The release manifest identifies the exact source revision and manufacturing bundle. The remaining physical tests are listed in [BRINGUP.md](../validation/BRINGUP.md).
