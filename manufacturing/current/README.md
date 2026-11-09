# Desk knob — PCB E6 fabrication and assembly set

Release 5.11.0. Checked 9 November 2026 against the current workspace, compatible with enclosure E12. Local design, independent DRC, Gerber/drill and assembly-file checks pass for a first prototype. No factory upload, purchase or allocation has been made. Physical electrical operation still needs bring-up testing.

## Upload files

1. Upload **Gerbers-E6.zip** to PCB fabrication. The outer review ZIP also contains source/evidence and is not the Gerber upload.
2. For **39-part complete assembly**, upload **BOM-complete.csv + CPL-complete.csv** and select a service that includes J4 through-hole assembly.
3. For **38-part SMT-only assembly**, upload **BOM-smt.csv + CPL-smt.csv**. Fit only J4, JST B6B-PH-K-S(LF)(SN) / C131342, locally. J6 is already included.
4. Check exact part matches, feeder pickup origin and pin-1/rotation previews against **physical-pin-map.csv** and **assembly/assembly-top.svg** before payment. CPL coordinates intentionally share the plotted Gerber origin, including negative Y; do not mirror, take absolute values or edit rotations independently.

## Board settings

| Item | Specification |
|---|---|
| Material | FR-4, Tg >=135 C |
| Layers / copper | 2 layers / 1 oz outer copper |
| Thickness | 1.6 mm nominal |
| Finish / mask / silk | ENIG / green / white |
| Unit outline | 68 x 83.5 mm, custom clipped round profile with USB/button tabs |
| Inner routed pocket | 34.6 x 40.6 mm, R2 corners; preserve exact Gerber contour |
| Routing vias | 0.30 mm drill / 0.60 mm pad |
| Copper rules | >=0.10 mm track/gap, >=0.15 mm component-pad gap, >=0.30 mm copper to edge; actual tracks >=0.15 mm |
| USB shield slots | Four plated 0.60 x 1.50/1.60 mm slots |
| Component assembly | All populated parts on top; 23 exact MPN BOM lines |

Have the assembler confirm support/tooling for the irregular outline and large inner pocket. Any panel rails must be removable outside the finished unit outline. No controlled-impedance specification is claimed; USB is full-speed and requires prototype signal checks.

## Final product assembly and programming

J4 is the only through-hole header. Before putting the board in the enclosure, trim its underside tails/joints to <=0.8 mm, inspect/deburr and insulate the specified solder wells. Check the six PCB capture pads and E12 button mechanism fit.

The Waveshare display, bearing, six printed enclosure parts, screws, foam and H1 crimped SH8-to-PH8 harness are separate from PCB assembly. The supplied display jumper lead is unused. See **WIRING.md** and **LCD-harness.csv** for the physical pin map and 44+/-1 mm free-insulation length. H1 is not supplied by the PCBA BOM.

Program **firmware/desk-knob.hex** or **firmware/desk-knob.bin** at 0x08000000 using SWD through J4 with USB powering the board. VTref is a voltage-sense input, not programmer power output. Check J4 signal identity against your actual probe, then initialize a fresh FRAM deliberately with the three-second button hold. These are the checked firmware 5.0.0 artifacts; no factory programming is requested by this kit.

## Verification

**checks/** contains the fresh independent KiCad DRC, pad/copper preservation, parsed Gerber/drill, BOM/CPL, annular-ring and dated public-stock reports. DRC found zero violations and zero unconnected items. Public stock is not reserved and does not establish feeder approval, factory loss requirements or minimum buying quantities. Those remain final factory-preview/quote checks.

**cad/** contains the finalized source-derived KiCad PCB/project/rules and its exact generated footprint library. **manifest.json** binds this set to the validated native circuit; **SHA256SUMS.txt** covers every package file except the checksum list itself. Do not mix this set with historical release files.
