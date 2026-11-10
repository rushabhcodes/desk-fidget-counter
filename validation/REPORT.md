# Readiness — v6.0.0 / RP2040 PCB F1 / enclosure E14

Local circuit, fabrication and assembly checks pass for **first-prototype manufacture**. Use the matching [F1/E14 fabrication kit](../release/desk-knob-f1-e14-fabrication.zip); the historical STM32 E6 kit is incompatible. Final manufacturer DFM, stock allocation and feeder/rotation preview remain, followed by physical bring-up. No supplier upload or order was performed.

E14 changes the screen carrier by adding a continuous fixed collar beneath the bezel. It retains the F1 PCB, firmware, Ø89.4×19.5 mm body, circular button, six prints and four screws. The collar passes the full rotor/harness tolerance checks; all 144 sampled radial sight lines through its wall are blocked. [The visual review](../mechanical/VISUAL-REVIEW.md) distinguishes the required 0.8 mm radial seam and 0.2 mm top-height step from the larger gap in the supplied screenshot, which was not reproduced in current v6.0.1.

F1 replaces STM32 with RP2040, Winbond W25Q16JVSNIQ 2 MB boot flash, Abracon ABM8-272-T3 12 MHz crystal (15 pF loads, 1 kΩ damping), per-pin bypassing and 27 Ω USB termination. Source and firmware share `reference/rp2040.json`. J4 is VREF/SWDIO/SWCLK/RUN/GND/BOOTSEL; USB recovery grounds BOOTSEL through 1 kΩ to flash CS during reset. The PCB outline, mounting, sensor, USB, display and switch datums are preserved. E14 retains the E13 design: a 14×7 mm curved button recessed 0.20 mm within its Ø89.4×19.5 mm body.

## Circuit and manufacturing checks

| Check | Result |
|---|---|
| Source build, typecheck, netlist, schematic and placement | Pass; no circuit errors or placement warnings |
| Design contract and exact supplier footprints | 52 fitted parts, 222 physical pads; pin maps, values and rails pass |
| Plotted-copper shorts | Zero shorts |
| Independent KiCad 10.0.7 fabrication DRC | Zero violations, zero opens, zero per-violation exclusions |
| Native copper / supplier lands / drills | Preserved in source-derived fabrication export |
| Gerbonara Gerber/Excellon inspection | 98 vias, 10 component plated holes, four plated USB slots; outline/window and 52 placements pass |
| Drill and paste review | Via annuli ≥0.15 mm; no via drill intersects an SMT paste aperture; no via-in-pad process required |
| BOM and CPL | 52 complete or 51 SMT placements; all top; only J4 omitted from SMT option; 27 exact MPN lines |
| Sourcing evidence | All 27 exact identities publicly purchasable on 10 November 2026; unreserved |
| Assembly identity / CAD audit | Identical bare-board copper in full assembly; 52 package models fit; no unexpected solid intersections; six watertight product prints |

The source uses guarded external routing through TSCircuit's documented custom-router interface, with Freerouting 2.5.0 and local power/clock routing. There are 1,277 trace records and 98 vias: 50 at 0.20 mm drill/0.50 mm pad and 48 at 0.30/0.60 mm. Ordinary tracks are ≥0.10 mm, component-pad clearance ≥0.15 mm and copper-to-edge ≥0.30 mm. MCU bypass branches are ≥0.15 mm. Neither library source nor compiled circuit JSON was patched. [Routing details](../routing/README.md).

Measured pad-to-pad bypass paths are 1.36–5.48 mm, meeting the stated engineering budgets; C17 and C21 use two vias each. Crystal nets are 3.74–5.99 mm with no vias, QSPI nets 5.00–19.71 mm, and MCU-to-series USB branches 15.07/15.21 mm. These geometric checks do not establish oscillator margin, USB signal integrity or physical current. Full evidence is in [RP2040 path checks](rp2040-paths.json), [fabrication review](assembly-fabrication-review.json) and [readiness](readiness.json).

## Firmware

Firmware 6.0.0 cross-builds with pinned Pico SDK 2.2.0, TinyUSB 0.21.0 and Arm GNU 14.3.Rel1. The 35,692-byte BIN passes boot2 CRC, vector, linked HID/CDC descriptor, Intel HEX and RP2040 UF2 family/payload checks. Native tests cover counting, button handling, display scanlines, dashboard parsing and the companion. PIO acquires quadrature while LCD/FRAM tasks run; suspend switches off the display/encoder and waits for USB resume. [Programming guide](../firmware/README.md).

## First assembled prototype

Measure 3.3 V/1.1 V stability, current/inrush/temperature, USB enumeration/suspend/resume, cold-start crystal and flash operation, UF2/SWD programming, encoder phase/noise/speed with display activity, FRAM retention and screen orientation. Verify the actual printed bearing fits, opaque optical skirt, crimped H1 routing, button centre/end closure and return, overtravel and foam life. See [bring-up](BRINGUP.md) and [fit checks](../mechanical/FIT.md). The MCU price alone does not establish a lower complete assembly quote because flash, crystal, passives and feeder costs changed.
