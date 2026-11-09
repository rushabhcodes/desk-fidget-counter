# E8 print and fit checks

The bearing is one purchased **6712ZZ, 60×75×7 mm**, with two metal shields. [Maysme's catalogue](https://maysmeprecision.com/Show/?Cid=677) confirms that boundary. Race/shield details, ball count and grooves in the detailed model are accepted engineering approximations, not manufacturer CAD. The product viewer presents the complete bearing as one object.

## Calibrate the bearing fits

The E8 enclosure uses Ploopy-style **hand-push fits** instead of screw-on bearing retainers. Nominal CAD mating diameters are **60.00 mm for the stationary post and 75.00 mm for the grip pocket**. The inner race rests on the lid shoulder; the outer race seats against the grip shoulder. No thread, separate clamp or lower retainer is involved.

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
- The glass relief remains 0.4 mm. The two M2×10 screws secure the bezel and carrier through their plastic supports; do not use the glass as a screw stop. Inspect the real module's support and retention before final tightening.
- The bezel/grip radial gap is 0.8 mm. The sensor fork is 3 mm wide around the 0.8 mm optical wall. The full moving envelopes include the stated print, bearing, PCB and assembly errors.
- The USB plug approach gauge is 13.4×6.9 mm. Verify your actual cable's undimensioned mating details and clearance below the rotor. The front button must release cleanly at full pretravel.
- The supplied LCD lead uses the accepted Ø1.2 mm render / Ø1.5 mm clearance envelope. Actual wire OD and bend limits are unpublished; mate sideways and trial-route before shortening. Modelled insulated paths are about 50 mm with a 3.3 mm display-end U bend; leave practical assembly slack. Actual bend limits are unverified. Keep all wires stationary inside the optical track.

[fit-budget.json](fit-budget.json) separates positive running margins from the push-fit calibration requirement. [geometry-check.json](geometry-check.json) records nominal collisions, tolerance envelopes, actual package/screen/wire checks, four race-specific interfaces and access checks. These are design checks under the stated assumptions; physical prototype validation is still required.

## Captive front button

The rounded 8×4 mm face presses the existing B3U-3000P. Two raised arms reach around the switch to retaining ears inside the circular shell. Drop the fork into the two open-top base guides before installing the lid. The internal stops limit nominal inward travel to 0.6 mm; the lid captures the ears. There is no fixed external button pod. The face projects 1.8 mm beyond the Ø84.8 mm base at rest and 1.2 mm at full travel. The contact boss starts 0.2 mm ahead of the switch; at the stop it reaches the datasheet maximum pretravel of 0.4 mm. The switch may return the cap only to the end of its free play. Nominal slide clearance is 0.4 mm per side. Print the cap with its flat arm/ear tops on the bed, using the supplied inverted pose. Use a small brim and local support beneath the face/boss if needed for your bridging settings; remove all support and burrs from the sliding/contact surfaces. The guide floors in the base also need local support beneath their internal overhangs. Test these small features before committing to a full print.

Actual switch position, print tolerance, sliding friction and safe overtravel are not established by this CAD. Test continuity and free release with the real board before final closure. Trim the boss only as needed to remove preload; confirm it still closes before the stop. The cap must not touch the fixed switch housing. No force or service-life guarantee is inferred from the nominal sweep.
