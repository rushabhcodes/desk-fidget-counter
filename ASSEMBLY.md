# Assembly / Rev B

The screen, its cradle and wires stay fixed. Only the grip, bearing outer race and black encoder retainer rotate. The nominal envelope is **Ø80×47 mm** before feet.

Open the [assembled tscircuit project](https://tscircuit.com/rushabhcodes/desk-fidget-counter), [assembled GLB](mechanical/cad/assembled.glb), or [exploded GLB](mechanical/cad/exploded.glb). The PCB and seven printed pieces are in their assembly poses. Purchased hardware uses dimensioned envelope models; cable routing and vendor internals are omitted. [CAD rebuilding and coordinates](mechanical/README.md) explain that distinction.

![Exploded assembly](mechanical/exploded.png)

## Hardware beyond the PCB BOM

| Qty | Item |
|---|---|
| 1 | Waveshare **19192**, non-touch 1.28inch LCD Module, GC9A01, 240×240; supplied PH2.0 eight-wire cable |
| 1 | NSK **6806ZZ** or identical 30 mm ID ×42 mm OD ×7 mm shielded bearing |
| 1 | Adafruit **2750**, protected 1S 3.7 V 350 mAh LiPo, with matching PH2 plug; check polarity with a meter |
| 1 | Semitec **103AT-2** 10 kΩ NTC, insulated and taped to the pouch; leads soldered at J3 |
| 1 | PH2.0 six-way programming cable: PHR-6 housing and suitable JST SPH-series crimp contacts; terminate at your SWD probe |
| 4 | M2.5×6 pan-head screws for the PCB |
| 2 | M2×10 pan-head screws for fixed lid (3.5 mm engagement into base bosses) |
| 3 | M2×8 pan-head screws for fixed inner-race clamp/cradle |
| 6 | M2×6 countersunk screws: three encoder plate, three screen bezel |
| 1 | 4 mm fabric ribbon, insulating tape/foam, thin LCD edge padding and removable feet |

The electronic BOM includes **NKK G12AH**, JST J2/J4/J6 and the optical sensor; do not buy the old Rev A slide switch, AS5600 or magnet. Screen module variants with a touch controller or integrated MCU have different geometry/pinouts and are not substitutions.

## Print preparation

Print `base`, `lid`, `knob`, `outer-retainer`, `inner-retainer`, `screen-bezel` and `button-plunger` from [mechanical/stl](mechanical/stl). Print the fit coupon first. PETG, 0.2 mm layers and at least four perimeters are starting settings. The grip and encoder retainer STLs are inverted with their upper faces against the bed. The cradle cantilevers, grip bearing lip and lid port bridges need removable supports. Keep bearing seats, optical apertures and the cable bore free of support material.

**Print the encoder retainer in opaque carbon-black material and test its IR opacity.** It has 48 open slots about 1.64 mm wide, a 1.0 mm radial skirt and a solid upper collar. Clear/gold/translucent filament is unsuitable for this part. Remove strings without widening individual slots. Start with the supplied 0.15/0.10 mm diametral bearing clearances; tune with the coupon. Retainers capture races axially, so a forceful press fit is unnecessary.

## Board, firmware and wiring

1. Reflow top SMT components, including U4's exposed ground pad. The dual optical sensor has a common collector, not a common emitter. Match its emitter-side marking and the physical A/K/C/E drawing in [references](reference/DATASHEETS.md).
2. Hand-solder the left-facing G12AH toggle, bottom PH2 battery connector, top PH6 programming connector and top PH8 display connector. J3 is the only unpopulated connector footprint; solder the NTC wires directly into it. Inspect through-hole joints before mounting. **Trim and deburr J4/J6 solder tails to at most 0.8 mm below the PCB.** This leaves a nominal 1.2 mm gap to the cell envelope. Fix a thin insulating barrier under the board over these tails; no sharp metal may contact or press the pouch.
3. With the pouch disconnected, power over USB and flash the included Rev B firmware through J4. J4 pin order is **3V3 VREF, SWDIO, SWCLK, NRST, GND, BOOT0**. VREF is a probe sense output. See [flashing instructions](firmware/README.md).
4. Verify screen cable continuity end-to-end before connecting it. J6 follows the Waveshare schematic's physical connector numbering:

| Pin | Signal | MCU / supply |
|---|---|---|
| 1 | BL | PB11 |
| 2 | RST | PB10 |
| 3 | DC | PB14 |
| 4 | CS | PA8 |
| 5 | CLK | PB13 through R27 |
| 6 | DIN | PB15 through R28 |
| 7 | GND | Ground |
| 8 | VCC | 3.3 V |

Use the connector's physical pin-1 mark, not wire colours or a guessed viewing direction. A straight-through PH8 cable should preserve these numbers. The module supports 3.3 V input/logic; this board supplies 3.3 V. Do not apply USB 5 V to the signal pins.

## Mechanical assembly

1. Tape the insulated NTC to the protected pouch, place the pouch in the base tray and retain it gently with the fabric ribbon. Keep its leads clear of screw bosses. Plug J2 in only after confirming BAT+/GND polarity. The nominal pouch-to-PCB allowance is 2 mm.
2. Fasten the PCB at the four standoffs. Put the reset plunger on SW2 at (0,−29). Thread the PH8 cable through the lid's hollow post, then plug J6 in. Seat the fixed lid, keeping the cable away from the optical sensor and skirt path. Fasten the two lid screws. The +Y USB opening and the left toggle recess must be clear.
3. On the bench, insert the bearing into the grip from below, then fit the black encoder retainer from below and fasten its three countersunk screws. The grip shoulder and retainer capture the outer race. Lower this complete rotor/bearing group over the fixed 29.85 mm post to the z22 shoulder. Guide the skirt centrally into U2's 3 mm gap without contact. For removal, lift this whole group off before undoing its underside screws; the exploded drawing shows relationships rather than a required disassembly path.
4. Fasten the inner-retainer/cradle to the fixed post with three M2×8 screws. Its plate contacts the inner race; the grip and lower retainer contact the outer race. The screw heads end at z32.2. Keep the cable in the central bore and the right-side notch; leave slack without any loop entering the bearing or optical track.
5. Connect the screen cable. Seat the module with its tab/connector toward **+X (right)** on the cradle's edge ledges. No support should press a backside component. The model reserves 8 mm below the PCB for the rear connector, but compare the real module and cable before tightening. Add thin edge padding as needed without loading the active glass.
6. Fit the fixed screen bezel with three countersunk M2×6 screws. Tighten only enough to retain the module; never bow the PCB or clamp the glass. The window radius is 16.6 mm around a 16.2 mm active radius. Rotate the grip through full turns and check the nominal 0.6 mm radial bezel clearance.
7. Initialize FRAM with USB `RESET CONFIRM`. Confirm 10 complete rotations in either direction add 10, partial reversal cancels, and toggle-off leaves counting active. Check scrolling in an editor, both USB-C orientations, unplug/replug and power-cut retention.

J4 and the internal reset button are service controls beneath the removable rotor. Normal reset/readout is available through USB without disassembly. The screen is non-touch.

The nominal encoder-to-lid gap is 0.5 mm; its solid swept volume passes the model checks. Printed tolerances, bearing drag, screw preload, rear LCD components, cable bend radius, IR contrast and real-life accuracy still need the physical checks in [BRINGUP.md](validation/BRINGUP.md).
