# Assembly / Mechanics E4 with PCB Rev E3

The nominal product is **Ø84.8×22.3 mm** before feet. The fixed screen sits inside the bearing's bore; the cable and screen connector occupy the main PCB's routed central window. All main-board components mount on top. The grip begins at z10.8 mm, with the USB-C port and front mode button below it.

[Assembled model](mechanical/cad/assembled.glb), [exploded model](mechanical/cad/exploded.glb), [height budget and design research](mechanical/LOW_PROFILE.md), [CAD rebuilding](mechanical/README.md).

![Assembled design](mechanical/assembly.png)

## Additional hardware

| Qty | Part |
|---|---|
| 1 | Waveshare **19192** non-touch 1.28-inch GC9A01 module; use and shorten its included PH2.0-to-jumper cable; no extra display harness |
| 1 | **Maysme 6712ZZ**, 60 mm ID ×75 mm OD ×7 mm, two metal shields; published envelope with user-authorized approximate internal geometry; mounting basis in [FIT.md](mechanical/FIT.md) |
| 1 | PHR-6 programming cable with appropriate JST SPH crimp contacts, terminated for the SWD probe |
| 11 | DIN 965 M2×6 countersunk screws: two chassis, three bearing inner clamp, three outer retainer, three screen bezel |
| 3 | DIN 965 M2×10 countersunk screws for the screen cradle/base posts |
| 1 | Thin transfer-adhesive annulus, 0.05–0.06 mm; 3M 467MP or verified equivalent |
| 6 | PORON 4701-30-20062-04 pads, 1.57 mm free thickness: four Ø4 mm and two Ø2.6 mm; 467MP adhesive under E4 lid |
| — | 3M 5413 insulating tape (0.069 mm total); optional three Ø5×1 mm removable silicone feet cut from sheet |

J4 **B6B-PH**, Omron **B3U-3000P** and the optical sensor are in the electronic BOM. J6 is the cable termination row; its optional male header is DNP. The compact build has 38 populated PCB parts. Rev B's smaller bearing, PCB, base and retainer set are incompatible with these mechanics.

## Print preparation

Print all eight product parts from [mechanical/stl](mechanical/stl): `base`, `lid`, `knob`, `outer-retainer`, `bearing-clamp`, `encoder-skirt`, `inner-retainer` (screen cradle), `screen-bezel`. Print the bearing coupons before the full set; [FIT.md](mechanical/FIT.md) gives their dimensions and acceptance checks. Start with PETG, 0.2 mm layers and four or more perimeters; tune bearing seats against actual parts. The grip, lower retainer and optical skirt are exported inverted in print orientation. Remove any supports from the bearing seats and optical apertures. Prepare the nominal Ø1.6 mm pilot holes for M2×0.4 threads with a suitable tap; check actual printed diameter first. Leave the Ø2.2 mm clearance holes unthreaded.

Use filament tested opaque at **950 nm** for `encoder-skirt`. Visible black colour alone is insufficient. Its 48 slots are about 1.64 mm wide, with a 0.8 mm radial track (two 0.4 mm extrusion lines). Clean strings without changing individual slot widths. The skirt's upper bonding annulus must be flat; test the chosen adhesive on the actual printed plastics and allow the specified cure/dwell time. The optical skirt is light and does not retain the bearing.

## Board assembly and first power

1. Reflow all SMT components on the top side. Inspect U4 load-switch pin 1 and the common-collector optical sensor orientation against the [datasheet contracts](reference/DATASHEETS.md).
2. Install J4 from above. J6's eight plated holes are solder terminations for the included display wires; leave its optional header unpopulated. Trim and deburr all tails to ≤0.8 mm. Inspect the solder wells and add thin insulating film so no sharp metal can contact the base.
3. Power by USB and flash the included firmware 5.0.0 using J4. Physical pin order is **3V3 VREF, SWDIO, SWCLK, NRST, GND, BOOT0**; VREF is probe sense, not power input. [Firmware instructions](firmware/README.md).
4. Shorten and dress the display's included cable following [WIRING.md](manufacturing/WIRING.md); keep its PH display plug. Solder board ends into J6 and meter every channel. J4 pin 1 is (−5,20.5). J6 pin 1 is (−21.5,4.39), followed by VCC/GND/DIN/CLK/CS/DC/RST/BL in −Y steps of 2.54 mm. Firmware assignments are unchanged.

Use physical pin-1 marks, not wire colour or a guessed viewing direction. The screen uses 3.3 V input and logic.

## Mechanical assembly

1. Use the included Waveshare display lead. Trial-route, shorten and solder its board end at J6; retain the original PH display plug. No custom cable, housing or crimp-contact purchase is required. Follow [physical wiring](manufacturing/WIRING.md), and check all eight signal continuities. There is no internal battery.
2. Seat the PCB over its four locating pegs, component side up. The front PCB tab carries SW1's original side actuator through the 8 mm case aperture. The base supports the tab underneath; two soft pads under the E4 lid capture it from above. There is **no printed button plunger or cap**.
3. Attach the six PORON discs under the lid using 0.05 mm 467MP: four Ø4 mm at the PCB locating-hole axes and two Ø2.6 mm at (±6,−37) mm. Free foam is 1.57 mm; the assembled model compresses it to 1.05 mm beneath 0.05 mm adhesive. Dress all wires inside the fixed window, then install the lid with its two DIN 965 M2×6 screws. Verify that the actual stock wires fit the modelled envelopes without tension or sharp bends. Check direct actuation and clean release of the original switch. The native actuator projects 0.65 mm beyond the side wall, and remains 0.25 mm beyond it at the datasheet's maximum 0.40 mm pretravel. Do not force or side-load it. The case is Ø84.8×22.3 mm; the actuator makes total front-to-back depth about 85.25 mm.
4. Confirm the actual bearing's race faces satisfy [FIT.md](mechanical/FIT.md). Place the lower outer-race retainer on the chassis, below the future bearing. Keep its three screw holes aligned with the underside Ø4.4 mm driver windows. Fit the bearing over the 59.80 mm stationary post; the housing pocket is 75.20 mm. The nominal 0.4 mm gap above the shortened post lets the upper clamp seat on the inner race. Fasten `bearing-clamp` with three DIN 965 M2×6 countersunk screws; its intended contact is the inner race only. Check actual contact and clearance to the shields and outer race before tightening.
5. Bond the opaque `encoder-skirt` concentrically under the grip's central web, using its upper annulus and a 0.05–0.06 mm adhesive layer. Keep tape and adhesive out of the track slots. Lower the grip/skirt over the bearing, carefully guiding the skirt between the sensor arms. The skirt and fixed screen supports must not touch at any angle.
6. Park the rotor so all three lower-retainer holes align with the chassis/base Ø4.4 mm driver windows. Insert the three DIN 965 M2×6 countersunk screws **upwards** through those windows into the grip. The upper shoulder and lower retainer capture the outer race. The housing wall ends 0.4 mm above the retainer, allowing it to seat on the race before touching the housing. Do not preload the shield or clamp both races together.
7. Fit `inner-retainer`, the screen cradle, onto the three independent base posts. Fasten with DIN 965 M2×10 countersunk screws. These posts rise inside the PCB window and optical skirt; they never cross a rotating radial web.
8. Connect the screen and route its cable inside the skirt, with no loose loop in the moving track. Orient the screen's connector tab toward **−X (left)**. Seat only the carrier PCB's edges on the cradle. The official module STEP sets the rear connector at +X and the front at Z=20.9 mm. Seat the original PH display plug fully and follow the eight modelled static wire bends; keep the cable entirely inside the optical skirt. Unplug the short harness before lifting the display for service.
9. Fit the fixed screen bezel using three DIN 965 M2×6 countersunk screws. Tighten gently without bowing the module or loading the active glass. The bezel/grip radial gap is 0.8 mm. A 0.4 mm underside relief keeps the lip clear of the front glass; retain the carrier without tightening against the active area. Rotate through full turns and verify freedom before adding removable feet over the Ø4.4 mm driver windows.
10. Initialize FRAM once with USB `RESET CONFIRM`. Check ten turns in either direction, partial reversal, Count-only mode, scrolling, both USB-C orientations and power-cut retention using [BRINGUP.md](validation/BRINGUP.md).

The rear USB-C receptacle sits at the side wall on an integral PCB tab. Its metal face is 0.15 mm beyond the wall (0.05 mm behind the wider base-floor edge). The 22 mm opening and approach gauge allow the specified L-com CAU4CC-40M-1M plug’s nominal **12.9×6.4 mm** section plus its general ±0.5 mm dimensional tolerance. The PCB ends 1.25 mm behind the socket face, clearing the plastic plug body. Check the actual chosen cable and undimensioned mating details. Do not force a larger plug under the rotor. The screen and wires remain stationary. The front button has an 8×4 mm opening (Z2.8–6.8 mm); four worst-case PCB positions are checked for direct fingertip access below the rotating ring: a short press selects Scroll / Count-only, a three-second hold clears the retained count. The screen shows hold progress and confirmation. This clears FRAM count, not the MCU. J4 retains NRST/BOOT0 for programming and remains beneath the removable screen.

The CAD validates nominal solid intersections and a full swept optical ring. It does not establish printed fit, bearing drag, adhesive reliability, cable flexibility, optical contrast, or USB behaviour on real hardware.

Rev E3 uses the official screen STEP, nominal package models, matching bezel pillars and the new USB-only board/firmware together. The LCD carrier/support collision found with the real tab geometry was removed by moving the three bezel-pillar axes to angles 0°,120°,240° at radius 21.1 mm. Full 3D source provenance and remaining model simplifications are in [mechanical/vendor/README.md](mechanical/vendor/README.md).

Rev E3 uses chassis screw axes (±27.6,±27.6) mm and the supported front PCB tab. Use the complete **E4 print set and six PORON pads with the E3 PCB**. The old E3 lid has no pad clearance. No printed button nose, travel stop or tip is present. The USB tab and housing overhang are intentional; the original connector lands, slots and locator drills are retained.

The detailed bearing/cable geometry uses the requested best approximations where online supplier data is missing. The fit budget targets calibrated bearing-fit diameters within ±0.10 mm and relative printed heights within ±0.10 mm. Race contacts and complete rotating tolerance envelopes are checked in CAD. Physical bring-up remains the first-prototype step; it is not represented as a completed test.
