# Assembly / Rev C

The nominal product is **Ø86×22.3 mm** before feet. The fixed screen sits inside the bearing's bore; the battery and screen connector share the main PCB's routed central window. All main-board components mount on top. The grip begins at z10.8 mm, with the USB-C port and left toggle below it.

[Assembled model](mechanical/cad/assembled.glb), [exploded model](mechanical/cad/exploded.glb), [height budget and design research](mechanical/LOW_PROFILE.md), [CAD rebuilding](mechanical/README.md).

![Assembled design](mechanical/assembly.png)

## Additional hardware

| Qty | Part |
|---|---|
| 1 | Waveshare **19192** non-touch 1.28-inch GC9A01 module and PH2.0 eight-wire cable |
| 1 | **6712ZZ**, 60 mm ID ×75 mm OD ×7 mm shielded bearing; verify actual race contact widths |
| 1 | Adafruit **2750** protected 350 mAh LiPo; verify plug polarity with a meter |
| 1 | Insulated Semitec **103AT-2** NTC, bonded to the pouch; direct wiring to J3 |
| 1 | PHR-6 programming cable with appropriate JST SPH crimp contacts, terminated for the SWD probe |
| 11 | M2×6 countersunk screws: two chassis, three bearing inner clamp, three outer retainer, three screen bezel |
| 3 | M2×10 countersunk screws for the screen cradle/base posts |
| 1 | Thin transfer-adhesive annulus, 0.05–0.06 mm; 3M 467MP or verified equivalent |
| — | Thin insulating film, pouch-retaining ribbon, LCD edge padding and removable feet |

J2 **S2B-PH**, J4 **B6B-PH**, J6 **S8B-PH**, NKK **G12AH** and the optical sensor are in the electronic BOM. Rev B's smaller bearing, PCB, base and retainer set are incompatible with these mechanics.

## Print preparation

Print all nine product parts from [mechanical/stl](mechanical/stl): `base`, `lid`, `knob`, `outer-retainer`, `bearing-clamp`, `encoder-skirt`, `inner-retainer` (screen cradle), `screen-bezel`, `button-plunger`. Print the fit coupon before the full set. Start with PETG, 0.2 mm layers and four or more perimeters; tune bearing seats against actual parts. The grip, lower retainer and optical skirt are exported inverted in print orientation. Remove any supports from the bearing seats and optical apertures.

Use filament tested opaque at **950 nm** for `encoder-skirt`. Visible black colour alone is insufficient. Its 48 slots are about 1.64 mm wide, with a 1 mm radial track. Clean strings without changing individual slot widths. The skirt's upper bonding annulus must be flat; test the chosen adhesive on the actual printed plastics and allow the specified cure/dwell time. The optical skirt is light and does not retain the bearing.

## Board assembly and first power

1. Reflow all SMT components on the top side. Inspect U4's exposed pad and the common-collector optical sensor orientation against the [datasheet contracts](reference/DATASHEETS.md).
2. Install all through-hole components from above. J2 and J6 are **side-entry** PH headers facing into the PCB window; J4 is top-entry. J3 is unpopulated: solder the NTC leads directly. Trim and deburr **all** through-hole tails to ≤0.8 mm. Inspect the solder wells and add thin insulating film so no sharp metal can contact the base or pouch.
3. With the battery disconnected, power by USB and flash the included Rev C firmware using J4. Physical pin order is **3V3 VREF, SWDIO, SWCLK, NRST, GND, BOOT0**; VREF is probe sense, not power input. [Firmware instructions](firmware/README.md).
4. Verify each cable with a continuity meter before mating. On J2, pin 1 at **(18.5,−8)** is BAT+ and pin 2 at **(18.5,−10)** is GND. On J4, pin 1 is **(−5,20.5)**. On J6, pin 1 is **(−19.5,−10.5)**, continuing in 2 mm steps toward +Y.

| J6 pin | Screen signal | MCU / supply |
|---|---|---|
| 1 | BL | PB11 |
| 2 | RST | PB10 |
| 3 | DC | PB14 |
| 4 | CS | PA8 |
| 5 | CLK | PB13 through R27 |
| 6 | DIN | PB15 through R28 |
| 7 | GND | Ground |
| 8 | VCC | 3.3 V |

Use physical pin-1 marks, not wire colour or a guessed viewing direction. The screen uses 3.3 V input and logic.

## Mechanical assembly

1. Insulate and attach the NTC to the pouch. Seat the pouch gently in its base tray and retain it with a ribbon. Keep leads clear of the three screen posts and screw bosses. The battery occupies the PCB window rather than sitting under the board.
2. Put the PCB over the four Ø2.5 mm locating pegs. The component side faces up. Check every solder tail against its individual floor well. Seat the reset plunger on SW2 at (−5,−30). Connect the battery only after confirming polarity.
3. Connect J6's cable and keep it inside the optical track. Install the fixed chassis (`lid`) and its two M2×6 countersunk screws. Its four pads capture the PCB at the NPTH positions. Confirm the USB and left toggle recesses are clear. Chassis pilot holes provide 4.8 mm nominal screw engagement.
4. Place the lower outer-race retainer on the chassis, below the future bearing. Keep its three screw holes aligned with the underside driver windows. Fit the bearing over the 59.85 mm stationary post. Fasten `bearing-clamp` with three M2×6 countersunk screws; it contacts the inner race only. Check clearance to the shields and outer race.
5. Bond the opaque `encoder-skirt` concentrically under the grip's central web, using its upper annulus and a 0.05–0.06 mm adhesive layer. Keep tape and adhesive out of the track slots. Lower the grip/skirt over the bearing, carefully guiding the skirt between the sensor arms. The skirt and fixed screen supports must not touch at any angle.
6. Park the rotor so all three lower-retainer holes align with the chassis/base driver windows. Insert the three M2×6 countersunk screws **upwards** through those windows into the grip. The upper shoulder and lower retainer capture the outer race. Do not preload the shield or clamp both races together.
7. Fit `inner-retainer`, the screen cradle, onto the three independent base posts. Fasten with M2×10 countersunk screws. These posts rise inside the PCB window and optical skirt; they never cross a rotating radial web.
8. Connect the screen and route its cable inside the skirt, with no loose loop in the moving track. Orient the screen's connector tab toward **+X (right)**. Seat only the carrier PCB's edges on the cradle. The model reserves 8 mm for the rear connector; inspect actual components and cable bends before tightening.
9. Fit the fixed screen bezel using three M2×6 countersunk screws. Tighten gently without bowing the module or loading the active glass. The bezel/grip radial gap is 0.6 mm. Rotate through full turns and verify freedom before adding removable feet over the driver windows.
10. Initialize FRAM once with USB `RESET CONFIRM`. Check ten turns in either direction, partial reversal, toggle-off counting, scrolling, both USB-C orientations and power-cut retention using [BRINGUP.md](validation/BRINGUP.md).

The side USB opening accepts a nominal **13 mm-wide ×8 mm-high** plug overmould; check the chosen cable. Do not force a larger plug under the rotor. The screen and wires remain stationary. Normal count read/reset uses USB; J4 and SW2 are service controls beneath the screen/rotor.

The CAD validates nominal solid intersections and a full swept optical ring. It does not establish printed fit, bearing drag, adhesive reliability, cable flexibility, optical contrast, charging or USB behaviour on real hardware.
