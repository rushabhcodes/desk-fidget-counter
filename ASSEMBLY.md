# Assembly / Rev A

The printable design is defined by `mechanical/parameters.json` and `mechanical/generate.py`. Print files are in `mechanical/stl`. All STL dimensions are millimetres. Generated parts are checked for watertightness and positive volume; the assembly model checks moving parts against the fixed lid and retainer.

## Mechanical bill of materials

| Qty | Part |
|---|---|
| 1 each | Printed base, lid, knob, outer retainer, inner retainer, button plunger |
| 1 | 6805 / SKF 61805-2RS1 bearing, 25 × 37 × 7 mm |
| 1 | K&J D42DIA diametric N42 magnet, Ø6.35 × 3.175 mm; same-size N52 variant only after checking sensor field status |
| 1 | Adafruit 2750 protected 350 mAh LiPo, within 21 × 37 × 5.8 mm envelope |
| 1 | Semitec 103AT-2 NTC on insulated flexible wires |
| 4 | M2.5 × 6 mm thread-forming PCB screws, low-profile head |
| 2 | M2 × 6 mm lid screws |
| 3 | M2 × 8 mm pan-head inner-race retainer screws |
| 3 | M2 × 6 mm **countersunk** outer-race retainer screws |
| 1 | 4 mm fabric ribbon for cell retention; insulating foam/tape; nonconductive magnet adhesive |
| 3–4 | Rubber feet, 1 mm nominal, outside the ribbon slots |

Use PETG, 0.2 mm layers, four perimeters and solid layers around fasteners. Print the fit coupon before the full parts. The supplied knob STL is inverted for printing with its roof against the bed; no large unsupported roof is required. Leave bearing fits and the magnet bore free of support material. Hole sizes and 0.15/0.10 mm diametral bearing clearances are starting values requiring a printer-specific fit trial. Retainers provide axial capture; do not depend on an aggressive press fit.

## PCB and electrical assembly

1. Fabricate the specified bare board; inspect copper, drill registration and polarity. Reflow the top-side SMT parts. BQ24074 EP is ground and must be soldered; use the reduced paste aperture and an appropriate reflow profile. Hand-assemble the slide switch and bottom-side JST battery connector afterward.
2. J3, J4 and J5 are intentionally unpopulated copper interfaces. Solder the two insulated NTC wires directly into J3. Use pogo contacts on J4 for programming. J5 is a temporary BOOT0 recovery bridge. Permanent tall headers prevent the lid fitting.
3. Trim all top-side through-hole leads to **1 mm or less below the board**, deburr and clean. Battery-to-PCB clearance is 2.0 mm; untrimmed header tails can hit the pouch. Insulate the battery-facing board underside with a thin PET/Kapton sheet, leaving the JST mating opening accessible.
4. Run the electrical bring-up tests with current-limited power before connecting the LiPo. Verify J2 pin 1 is BAT+ and pin 2 GND; check the actual cable with a meter. Never assume a third-party JST cable has the same polarity.
5. Bond the NTC bead to the broad pouch face using insulating tape. Do not solder to or puncture the cell. Place the battery in the tray over a thin insulating foam pad. Route its cable and NTC wires beside the tray. The fabric ribbon passes through the two base slots and holds the cell gently; it must not compress the pouch.
6. Fit the PCB at z=10 mm with the four M2.5 screws. Recheck clearances at the connector, trimmed leads and ribbon. The USB opening faces +Y. Program the MCU and deliberately initialize FRAM with a three-second reset.

## Bearing, rotor and cover

1. Fit the button plunger from below the lid: its wide flange remains below the lid, with its stem through the RESET opening. The tactile switch supplies its return force. Verify free travel before tightening the lid.
2. Screw the lid to the base. The stationary collar locates the bearing's inner race; its shoulder is at z=17 mm. The PCB and sensor remain stationary. The USB port, scroll lever, reset plunger and LED opening stay accessible on the fixed part.
3. On the bench, turn the knob upside down. Put the inner retainer into the roof cavity, with its three holes aligned to the three Ø4.4 mm roof access bores. Fit the bearing into the outer-race seat. Attach the outer retainer with three M2 × 6 **countersunk** screws. Their heads must be flush with its underside; projecting pan heads would hit the lid.
4. Seat the diametric magnet into the knob's center post with nonconductive adhesive. Its lower face is nominally z=15 mm, **1.65 mm above the AS5600 package top**. Center it over U2. Avoid other magnets and ferromagnetic screws near the sensing axis.
5. Lower the complete rotor over the stationary stem. Align the inner retainer with the stem's three screw pilots. Insert the three M2 × 8 pan-head screws through the roof access bores and secure the **inner race only**. The heads sit below the roof; do not clamp bearing shields or the outer race. The rotating outer retainer is nominally 0.4 mm above the fixed lid. For disassembly, undo these same three accessible screws and lift off the rotor before touching the outer retainer.
6. Check a full turn in both directions without rubbing. Verify sensor MD is set and ML/MH remain clear across the full rotation. If the field is too strong, use the N42 variant or recess the magnet slightly further; if too weak, adjust seating carefully while preserving package clearance. Re-run the count tests after every magnetic or mechanical change.

The assembled solid model is Ø72 × 31 mm, before feet. CAD checks do not establish printed fit, bearing drag, actual magnetic strength, stiffness or drop resistance. Those remain prototype tests.
