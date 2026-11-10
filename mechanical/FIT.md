# E13 print and fit checks

The bearing is one purchased **6712ZZ, 60×75×7 mm**, with two metal shields. [Maysme's catalogue](https://maysmeprecision.com/Show/?Cid=677) confirms that boundary. Race/shield details, ball count and grooves in the detailed model are accepted engineering approximations, not manufacturer CAD. The product viewer presents the complete bearing as one object.

## Calibrate the bearing fits

The E13 enclosure uses Ploopy-style **hand-push fits** instead of screw-on bearing retainers. Nominal CAD mating diameters are **60.00 mm for the stationary post and 75.00 mm for the grip pocket**. The inner race rests on the lid shoulder; the outer race seats against the grip shoulder. No thread, separate clamp or lower retainer is involved.

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
- The USB socket mouth is recessed 2.51 mm from the enlarged body's outer circle. The lid has a matching plug-shoulder relief; the USB plug approach gauge is 13.4×6.9 mm. Verify your actual cable's undimensioned mating details and clearance below the rotor. The front button must release cleanly at full pretravel.
- H1 is a separately ordered crimped JST-SH8-to-PH8 harness with44±1mm free insulation between housing exits. CAD renders nominalØ0.61mm wire and checksØ0.8mm at43/44/45mm lengths. Plug engagement and static3.3mm U-bend remain engineering approximations; verify actual crimped harness fit, retention, no pinch/strain and electrical continuity. Both ends unplug. Keep all wires stationary inside the optical track.

[fit-budget.json](fit-budget.json) separates positive running margins from the push-fit calibration requirement. [geometry-check.json](geometry-check.json) records nominal collisions, tolerance envelopes, actual package/screen/wire checks, four race-specific interfaces and access checks. These are design checks under the stated assumptions; physical prototype validation is still required.

## Captive front button

The E13 button is a **14×7 mm rounded curved segment** with **R44.5 mm** on its outside face. It follows the circular side wall and stays **0.2 mm inside the Ø89.4 mm body** at rest; it moves farther inward during its 0.6 mm stroke. A shallow 0.2 mm thumb dish identifies the press area at Z6.4 mm. The matching rounded opening leaves 0.4 mm nominal running clearance. The grip has a continuous 1.6×1.6 mm lower-edge bevel to make room for a fingertip pressing the recessed button.

PCB F1 replaces the electronics with RP2040 while retaining the E6 outline and switch datums. The body grows by 4.6 mm in diameter to absorb the button within the circle; height remains 19.5 mm. The original B3U-3000P switch stays at (0, −40.9) mm, with its actuator face at Y−42.85 mm. The printed contact boss starts at Y−43.05 mm, leaving the same 0.2 mm nominal released gap. Full stroke gives 0.4 mm nominal switch displacement. Actual placement and print error can change closure and overtravel, so calibrate the first physical assembly.

Two **foam return stacks** push the retaining ears against their outward stops. Cut four **2×1.6 mm** pieces from the specified **1.57 mm PORON 4701-30-20062-04**. Each stack uses two layers with **0.05 mm 467MP** between them and against the fixed backing; leave its front face unbonded. Put one stack in each outer pocket at X±8.8 mm, Z6.8 mm. The rear backing faces are at Y−36.85 mm. The 2.75 mm nominal released cavity gives 15.6% nominal compression, rising to 34.7% at the stop. The declared thickness/cavity/adhesive tolerances give 0.056 mm minimum released precompression and 44.1% maximum calculated compression. Force, foam set, friction and life remain physical checks.

Print the cap **ears down and curved face up**, using the supplied −90° X-rotated STL. Use a brim and supports under the hidden rear apron/contact boss; keep support contact off the rail and stop faces. Remove all support and burrs before measuring the running clearances. Drop the cap into the open-top guides, gently compress the return stacks behind its ears, then fit the lid. Rigid stops limit inward travel and retain the cap outward; the lid captures it vertically.

Check the centre and both ends of the button with the lid fully tightened. Verify no switch preload at rest, electrical closure before the stop, free return, no fixed-housing contact, and finger clearance while rotating the grip. The fingertip checks use a stated 12 mm spherical gauge and separately apply case-relative and PCB registration errors; they do not establish comfort for every hand size. Trim the contact boss only as needed, then repeat closure and return checks. Do not use foam force to overcome a binding guide.
