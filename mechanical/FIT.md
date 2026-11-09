# E12 print and fit checks

The bearing is one purchased **6712ZZ, 60×75×7 mm**, with two metal shields. [Maysme's catalogue](https://maysmeprecision.com/Show/?Cid=677) confirms that boundary. Race/shield details, ball count and grooves in the detailed model are accepted engineering approximations, not manufacturer CAD. The product viewer presents the complete bearing as one object.

## Calibrate the bearing fits

The E12 enclosure uses Ploopy-style **hand-push fits** instead of screw-on bearing retainers. Nominal CAD mating diameters are **60.00 mm for the stationary post and 75.00 mm for the grip pocket**. The inner race rests on the lid shoulder; the outer race seats against the grip shoulder. No thread, separate clamp or lower retainer is involved.

Print the nominal coupon with the same material, orientation and settings as the product. Its two rings reproduce the mating diameters over the full 7 mm bearing width. Use the actual bearing to check both fits before committing to the larger prints:

| Coupon | Pocket ID | Post OD |
|---|---:|---:|
| `fit-coupon-tight` | 74.90 mm | 60.10 mm |
| `fit-coupon` | 75.00 mm | 60.00 mm |
| `fit-coupon-loose` | 75.20 mm | 59.80 mm |

Start with the nominal pair. The alternatives help identify printer compensation; they are not additional product parts. Correct printer fit compensation locally rather than uniformly scaling the enclosure, which would also move the encoder track, screw axes and port openings.

A suitable fit seats with light, even hand pressure, stays seated during normal handling and allows the bearing to spin freely. Stop if force is required; do not hammer, force a fit with screws or accept a loose assembly. Check pull-off retention and drag on the completed prototype. CAD intersection tests cannot certify friction, creep or a printer's dimensional capability.

## Printing

Use the orientations in `print-poses.json`. Base and screen carrier print flat; grip and bezel print front-face down. The lid requires support beneath its annular plate above the PCB capture feet. Keep support contact off the bearing mating surfaces. A 0.4 mm nozzle, 0.2 mm layers and six perimeters and 35–50% infill are starting settings. Use PLA for the product parts and coupons. The two 23×4 mm screen-support walls have 7 mm-wide splayed roots and full-height webs to the screw axes; they replace the unbraced Ø4 mm columns. All six product STLs must remain single connected, watertight solids. Geometry and section size do not establish a load rating; check the actual PLA print for flex, layer separation and screw-hole cracks before installing the display.

The integral encoder wall is **0.8 mm**, with 48 slots. Its material must be tested opaque at **950 nm**; visible black colour is insufficient evidence. Clear stringing from the slots without changing the track radius or damaging its fingers. Check the complete rotation before powering the device.

## Other interfaces

- The six PCB pads use **PORON 4701-30-20062-04**, 1.57 mm nominal, with 0.05 mm 467MP adhesive. The model compresses the foam to 1.05 mm; PCB thickness variation is included in the fit budget.
- The glass relief remains 0.4 mm. E9 reserves 2 mm beneath the actual screen PCB profile for rear electronics omitted by its supplier STEP, with 0.4 mm lateral carrier clearance; actual component heights remain a prototype check. The two M2×10 screws secure the bezel and carrier through their plastic supports; do not use the glass as a screw stop. Inspect the real module's support and retention before final tightening.
- The bezel/grip radial gap is 0.8 mm. The sensor fork is 3 mm wide around the 0.8 mm optical wall. The full moving envelopes include the stated print, bearing, PCB and assembly errors.
- The USB plug approach gauge is 13.4×6.9 mm. Verify your actual cable's undimensioned mating details and clearance below the rotor. The front button must release cleanly at full pretravel.
- H1 is a separately ordered crimped JST-SH8-to-PH8 harness with44±1mm free insulation between housing exits. CAD renders nominalØ0.61mm wire and checksØ0.8mm at43/44/45mm lengths. Plug engagement and static3.3mm U-bend remain engineering approximations; verify actual crimped harness fit, retention, no pinch/strain and electrical continuity. Both ends unplug. Keep all wires stationary inside the optical track.

[fit-budget.json](fit-budget.json) separates positive running margins from the push-fit calibration requirement. [geometry-check.json](geometry-check.json) records nominal collisions, tolerance envelopes, actual package/screen/wire checks, four race-specific interfaces and access checks. These are design checks under the stated assumptions; physical prototype validation is still required.

## Captive front button

The E12 paddle has a **14×6.6 mm rounded face** with a shallow 0.2 mm thumb dish at Z6.4 mm, two 2 mm-wide rails and broad retaining ears. Its lower apron covers the front PCB tab. It operates the existing B3U-3000P on the unchanged E6 PCB. The raised face clears a nominal 12 mm spherical fingertip above the desk by 0.4 mm, or 0.14 mm at the tested −0.26 mm height shift. This checks one stated fingertip gauge rather than all hand sizes. The face is 1.75 times wider than E11 and its nominal rectangular press area is 2.89 times larger. Guides and both sets of stops sit inside the circular shell. Inward travel remains 0.6 mm; the face projects 1.8 mm beyond the Ø84.8 mm body at rest and 1.2 mm at the stop.

Two **foam return stacks** push the ears against the outward stops, so return through the 0.2 mm switch gap does not depend on the switch spring. Cut four **2×1.6 mm** rectangles from the already specified **1.57 mm PORON 4701-30-20062-04**. Each stack uses two pieces: bond the rear layer to the fixed backing and bond the front layer to it, using **0.05 mm 467MP** at each bond. Leave the front contact face unbonded. Fit one stack in each outer pocket, centred at X±8.8 mm, Z6.8 mm. The rear backing faces are at Y−35.45 mm. Drop the paddle into its open-top guides, compressing the stacks gently behind the ears, then install the lid. Keep adhesive and loose foam off the guide faces.

The 2.75 mm nominal rest cavity compresses each stack by 15.6%; full press compresses it by 34.7%. With the declared ±10% foam thickness, ±0.1 mm relative cavity error and ±0.02 mm combined adhesive thickness, calculated minimum rest precompression is 0.056 mm and maximum foam compression is 44.1%. These are dimensional checks; return force, friction, permanent set and cycle life remain unmeasured. Both rigid inward stops carry the final travel limit; the foam is separate from those stops.

Print the cap front face down, using the supplied 90° X-rotated STL. Use a brim if needed and local support beneath the outboard ears; remove it from the retention and sliding surfaces. The rails and thin contact boss grow from the face. The base guide floors still need local support. Deburr the 0.4 mm guide clearances and remove all support from the sliding surfaces. Check an off-centre press at both ends of the paddle as well as the centre, and verify free return with the lid fully tightened.

The contact boss starts 0.2 mm ahead of the nominal actuator and reaches 0.4 mm nominal switch displacement at the stop. [Omron's B3U datasheet](https://omronfs.omron.com/en_US/ecb/products/pdf/en-b3u.pdf) specifies a 0.1–0.4 mm side-switch pretravel; it does not certify this enclosure's overtravel. Actual PCB registration, switch placement and print tolerance still require calibration. Verify electrical closure before the stop, no switch preload at rest, free release and no fixed-housing contact. Trim the contact boss only as needed and recheck closure. The added foam must not be used to force a binding guide or compensate for a mis-seated PCB.
