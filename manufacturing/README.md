# Manufacturing source / PCB E5, mechanics E10

This repository contains the design and its verification record. **No new fabrication kit or release archive is prepared.** Export/download the fabrication files yourself from this validated source when you are ready. Project source is published separately to GitHub and TSCircuit; ordering remains yours to perform.

The obsolete v5.4.0 Gerbers, KiCad board, BOM/CPL, order kit and manifest were removed from this working revision because they contain the undersized U3 FRAM footprint and outdated assembly angles. They remain in Git history and the held old release; do not order them or mix them with new exports. Current part identities and exact supplier footprints live in [the catalogue](../reference/jlcpcb-parts.json), [import provenance](../reference/jlcpcb-footprints.json) and `imports/jlc`.

## Board specification

| Parameter | Requirement |
|---|---|
| Outline | Clipped Ø72 mm body with integral USB/button tabs; 68×83.5 mm total; 34.6×40.6 mm R2 window; four Ø2.7 mm NPTH at (±30, ±15) mm |
| Material | FR-4, 1.6 mm nominal, Tg ≥135°C |
| Copper | Two layers, 1 oz outer copper |
| Finish | ENIG; green solder mask, white silkscreen |
| Track | ≥0.10 mm fabrication limit; native phases request 0.15 mm; measured widths in the validation report |
| Clearance | ≥0.10 mm track/via copper; ≥0.15 mm component pad-to-pad; ground pour clearance 0.25 mm |
| Routing via | Ø0.30 mm finished drill / Ø0.60 mm pad; generated entirely by the native autorouter |
| Drill spacing | Via drill-edge ≥0.20 mm; component PTH drill-edge ≥0.45 mm |
| Hole-to-copper | NPTH ≥0.20 mm; via drill ≥0.20 mm; component plated drill ≥0.28 mm |
| Copper to edge | ≥0.30 mm; ground pours inset 0.40 mm |
| Assembly | 39 fitted components, all top; J4 genuine JST PH6 and J6 right-angle 2×4 display header fitted |
| Local assembly | Retain both factory display lead ends; shorten the middle, solder and individually heat-shrink eight splices; trim board tails to ≤0.8 mm |

[Fabrication rules](../reference/fabrication-rules.json) record the checked [JLCPCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities/). Keep 1 oz copper. This is not a controlled-impedance design; USB full-speed signal integrity is a prototype test.

J1 sits at (0,+37.55) mm; its housing overhangs the supported rear tab so its mouth reaches the shell wall. SW1 remains at (0,−40.9) mm. A captive printed cap operates its original actuator; the lid retains the cap without extra screws. No toggle is installed. J6 is a fitted 2×4 right-angle header centred at (−20.35,−3.5) mm and rotated 90°. It faces +X into the window. Pins1–8 are BL/RST/DC/CS/CLK/DIN/GND/VCC, with odd pins lower and even pins upper. The silkscreen labels and physical pin map identify every position. [Wiring and service pin maps](WIRING.md).

## Verification without producing a kit

```sh
bun install --frozen-lockfile
bun run typecheck && bun run test
bun run check:netlist && bun run check:schematic
bun run build
bun run check:placement
bun validation/check-design.mjs
bun run check:footprints && bun run check:shorts && bun run check:assembly
```

For the independent check, install KiCad 10 CLI and its matching Python `pcbnew` module:

```sh
bunx tsci export dist/index/circuit.json -f kicad_pcb -o /tmp/desk-knob-raw.kicad_pcb
/usr/bin/python3 scripts/export-fabrication.py /tmp/desk-knob-raw.kicad_pcb --check-only
```

`--check-only` writes temporary evidence under `/tmp`; it does not produce an order kit. It checks all 177 pad centres and plated drills against source, applies the documented rules, refills ground zones and removes electrically isolated ground fragments. It requires zero DRC violations/unconnected items, no exclusions and an exact match of every native trace and via before/after. It does not route or repair copper. See [validation results](../validation/REPORT.md).

## Standard USB-C connector

J1 is **XUNPU TYPEC-309-ACP16L65 / C2909598**, selected through TSCI's JLCPCB catalogue. Its exact imported footprint has four **0.60×1.50/1.60 mm** plated slots, meeting the published ≥2:1 length/width guidance, and two Ø0.65 mm locating holes with approximately 0.364 mm to adjacent pads. Its drawing agrees with the pad/hole pattern. The housing is 6.5 mm long and 3.16 mm high; the unscaled supplier CAD is aligned to the real SMT seating plane. The socket mouth reaches Y42.1865 mm, within the rear opening; a 13.4×6.9 mm plug approach gauge clears the PCB, packages, shell and grip. The circular product stays 19.5 mm high.

The original C165948 connector and its short slots are removed from the fitted design. No supplier pad or drill geometry was resized. [Selection and drawing evidence](../reference/usb-connector-selection.json) and [measured slot checks](../validation/supplier-review.json).

## When you export later

Use the bare PCB entrypoint [index.circuit.tsx](../index.circuit.tsx) for factory exports. Export all Gerbers, plated/nonplated drills, BOM and placement files from that same freshly built revision. Verify window/outline geometry, exact MPNs, 39 top placements including fitted J4 and J6. Do not reuse the held old CSVs. JLCPCB feeder origins and zero angles still need confirmation against the physical copper and datasheet pin 1 in your final upload preview; a generic 3D model is insufficient.

[JLCPCB guidance](jlcpcb/README.md) records part matching/cost evidence and the remaining supplier steps. The screen, bearing, six prints and final wire/mechanical assembly are separate from PCB assembly. The first prototype still needs [bring-up](../validation/BRINGUP.md) and [fit verification](../mechanical/FIT.md).
