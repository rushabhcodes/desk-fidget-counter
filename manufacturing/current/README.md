# Desk knob — RP2040 PCB F1 / enclosure E14

Checked 10 November 2026 against the current source. Local circuit, independent fabrication and assembly checks pass for **first-prototype manufacture**. This kit contains RP2040 hardware and firmware 6.0.0, with the recessed curved button inside the Ø89.4×19.5 mm E14 enclosure. Final manufacturer DFM/feeder preview and physical bring-up remain. No supplier upload, purchase or stock allocation was performed.

## Upload files

1. Upload **Gerbers-F1.zip** for PCB fabrication. The outer review ZIP also contains CAD, evidence, firmware and prints; it is not the Gerber upload.
2. For **52-part complete assembly**, upload **BOM-complete.csv + CPL-complete.csv** and confirm a service including the J4 through-hole header.
3. For **51-part SMT assembly**, upload **BOM-smt.csv + CPL-smt.csv**. Fit only J4, JST B6B-PH-K-S(LF)(SN) / C131342, locally. J6 is already fitted.
4. Check every exact MPN, feeder origin, asymmetric rotation and pin 1 against **physical-pin-map.csv** and **assembly/assembly-top.svg** before payment. CPL and Gerbers share their origin, including negative Y; do not mirror, take absolute coordinates or edit rotations independently.

## Board settings

| Item | Specification |
|---|---|
| Material | FR-4, Tg ≥135°C |
| Layers / copper / thickness | 2 layers / 1 oz / 1.6 mm nominal |
| Finish / mask / silk | ENIG / green / white |
| Unit outline | 68×83.5 mm clipped round profile with USB/button tabs |
| Internal window | 34.6×40.6 mm, R2 corners; preserve the Gerber contour |
| Vias | 50 at Ø0.20 drill / Ø0.50 pad; 48 at Ø0.30 / Ø0.60 mm |
| Copper rules | ≥0.10 mm track/gap, ≥0.15 mm component-pad gap, ≥0.30 mm edge clearance |
| USB shield slots | Four plated 0.60×1.50/1.60 mm slots |
| Assembly | 52 top placements / 27 exact MPN BOM lines |

E14 adds a continuous fixed collar to the existing screen carrier. Keep the 0.8 mm rotating seam open; see enclosure/VISUAL-REVIEW.md for the complete visual review. The body remains Ø89.4×19.5 mm with six prints and four screws.

The 98 vias retain ≥0.15 mm annular rings and their drills do not intersect SMT paste. No via-in-pad process is required. Confirm tooling/support for the irregular outline and large internal window; removable panel rails must stay outside the finished outline. USB full-speed signal integrity has not been measured.

## Product assembly and programming

J4 is the only through-hole header. Trim its underside tails/joints to ≤0.8 mm, inspect/deburr and insulate the specified solder wells before enclosure assembly. The Waveshare display, complete 6712ZZ bearing, six printed parts, screws, foam and custom H1 harness are separate from PCBA. H1 is a keyed crimped SH8-to-PH8 lead, 44±1 mm free insulation, straight circuits 1→1 through 8→8; see **WIRING.md** and **LCD-harness.csv**. The display kit's jumper lead is unused.

**enclosure/stl/** contains the six E14 product prints and three fit coupons. Follow the print poses and fit notes, and use **ASSEMBLY.md** for the sequence. Actual printed fits, optical opacity and button force/life require validation.

Use **firmware/desk-knob.uf2** with the RP2040 ROM USB bootloader or **firmware/desk-knob.elf** through J4 SWD. See **firmware/README.md** for the exact procedure. Initialize a fresh FRAM deliberately with a three-second button hold, then perform **BRINGUP.md** checks. Historical STM32 programming procedures and images do not apply.

## Evidence and file integrity

**checks/** includes zero-violation/zero-open KiCad DRC, native-copper/pad/drill preservation, Gerber/Excellon parsing, BOM/CPL and physical pin maps, annuli/paste clearances, local signal paths, firmware image and assembly audit evidence. All 27 exact part identities were publicly purchasable on 10 November 2026; stock is unreserved. Final allocation, purchasing/attrition quantities and feeder/rotation approval require the factory quote/preview. MCU unit pricing does not establish a lower complete PCBA price.

**cad/** contains the finalized source-derived KiCad board/project/rules and exact generated footprints. **manifest.json** binds the kit to the checked source. **SHA256SUMS.txt** covers every kit file except itself. Keep this F1 hardware, BOM/CPL and firmware together.
