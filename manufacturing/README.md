# Manufacturing source / PCB RP2040 F1, mechanics E14

**RP2040 F1 passes local first-prototype fabrication and assembly checks.** Use [the F1/E14 kit](../release/desk-knob-f1-e14-fabrication.zip) or the matching files in [manufacturing/current](current/README.md). The population is 52 parts (51 SMT plus the J4 through-hole header), with firmware 6.0.0. Final factory DFM, part/feeder/rotation approval and physical bring-up remain. The historical E6/E13 archive targets STM32 and must not be mixed with F1.

The obsolete v5.4.0 Gerbers, KiCad board, BOM/CPL, order kit and manifest were removed from this working revision because they contain the undersized U3 FRAM footprint and outdated assembly angles. They remain in Git history and the held old release; do not order them or mix them with new exports. Current part identities and exact supplier footprints live in [the catalogue](../reference/jlcpcb-parts.json), [import provenance](../reference/jlcpcb-footprints.json) and `imports/jlc`.

## Board specification

| Parameter | Requirement |
|---|---|
| Outline | Clipped Ø72 mm body with integral USB/button tabs; 68×83.5 mm total; 34.6×40.6 mm R2 window; four Ø2.7 mm NPTH at (±30, ±15) mm |
| Material | FR-4, 1.6 mm nominal, Tg ≥135°C |
| Copper | Two layers, 1 oz outer copper |
| Finish | ENIG; green solder mask, white silkscreen |
| Track | ≥0.10 mm fabrication limit; routing requests 0.15 mm; measured widths in the validation report |
| Clearance | ≥0.10 mm track/via copper; ≥0.15 mm component pad-to-pad; ground pour clearance 0.25 mm |
| Routing via | Ø0.30 mm drill / Ø0.60 mm pad preferred; Ø0.20 mm / Ø0.50 mm for dense fanout; both retain ≥0.15 mm annular ring |
| Drill spacing | Via drill-edge ≥0.20 mm; component PTH drill-edge ≥0.45 mm |
| Hole-to-copper | NPTH ≥0.20 mm; via drill ≥0.20 mm; component plated drill ≥0.28 mm |
| Copper to edge | ≥0.30 mm; ground pours inset 0.40 mm |
| Assembly | 52 fitted components, all top; J4 JST PH6 and J6 keyed JST-SH8 SMT socket fitted |
| Local assembly | Fit crimped replacement H1; continuity/isolation check; trim only J4 tails to ≤0.8mm |

[Fabrication rules](../reference/fabrication-rules.json) record the checked [JLCPCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities/). Keep 1 oz copper. This is not a controlled-impedance design; USB full-speed signal integrity is a prototype test.

J1 remains at (0,+37.55)mm and SW1 at (0,-40.9)mm, operated by the captive printed cap. J6 is JST SM08B-SRSS-TB(LF)(SN)/C160407 at (-21.3,-2)mm,90deg,facing +X. Circuits1–8 are BL/RST/DC/CS/CLK/DIN/GND/VCC; anchors9/10 are GND. Connect the display with the separately purchased crimped H1 harness. [Physical circuit map](WIRING.md).

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

`--check-only` writes temporary evidence under `/tmp`; it does not produce an order kit. It checks all 222 pad centres and plated drills against source, applies the documented rules, refills ground zones and removes electrically isolated ground fragments. It requires zero DRC violations/unconnected items, no exclusions and an exact match of every native trace and via before/after. It does not route or repair copper. See [validation results](../validation/REPORT.md).

## Standard USB-C connector

J1 is **XUNPU TYPEC-309-ACP16L65 / C2909598**, selected through TSCI's JLCPCB catalogue. Its exact imported footprint has four **0.60×1.50/1.60 mm** plated slots, meeting the published ≥2:1 length/width guidance, and two Ø0.65 mm locating holes with approximately 0.364 mm to adjacent pads. Its drawing agrees with the pad/hole pattern. The housing is 6.5 mm long and 3.16 mm high; the unscaled supplier CAD is aligned to the real SMT seating plane. The socket mouth reaches Y42.1865 mm, within the rear opening; a 13.4×6.9 mm plug approach gauge clears the PCB, packages, shell and grip. The circular product stays 19.5 mm high.

The original C165948 connector and its short slots are removed from the fitted design. No supplier pad or drill geometry was resized. [Selection and drawing evidence](../reference/usb-connector-selection.json) and [measured slot checks](../validation/supplier-review.json).

## When you export later

Use the bare PCB entrypoint [index.circuit.tsx](../index.circuit.tsx) for factory exports. Export all Gerbers, plated/nonplated drills, BOM and placement files from that same freshly built revision. Verify window/outline geometry, exact MPNs, 52 top placements including fitted J4 and J6. Do not reuse the held old CSVs. JLCPCB feeder origins and zero angles still need confirmation against the physical copper and datasheet pin 1 in your final upload preview; a generic 3D model is insufficient.

[JLCPCB guidance](jlcpcb/README.md) records part matching/cost evidence and the remaining supplier steps. The screen, bearing, six prints and final wire/mechanical assembly are separate from PCB assembly. The first prototype still needs [bring-up](../validation/BRINGUP.md) and [fit verification](../mechanical/FIT.md).

The independent KiCad check uses 1 nm coordinate resolution. A duplicate zero-length exporter segment may be omitted only when its entire copper disk is already covered by an equal or wider same-net endpoint. The check records each omission and rejects uncovered segments. Native circuit JSON, routed copper geometry, vias and connections remain unchanged.
