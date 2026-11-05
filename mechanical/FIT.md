# Rev E3 fit measurements

The checked CAD has no nominal solid intersections. **The enclosure is not tolerance-qualified.** A bearing envelope, supplier screen STEP and software collision check do not establish that a particular print and purchased parts will fit. Use this sheet to record the first prototype measurements before approving a fabrication/assembly run.

## Bearing selection and coupons

The selected catalogue item is [Maysme **6712ZZ**](https://maysmeprecision.com/Show/?Cid=677), chrome steel, **60 mm bore ×75 mm OD ×7 mm width**, with two metal shields. The manufacturer's page confirms these boundary dimensions and configuration. It does not publish race-face diameters, abutments, starting torque or a dimensioned CAD model. Availability and quantity-one supply still need confirmation with a seller; the link is not a stock guarantee. A same-size replacement requires the same checks below. A 6812/61812 is a different size and is not a substitute.

Print one coupon file at a time, with the product's PETG, orientation, layer height, perimeter count and slicer compensation. Each STL contains two separate 3 mm-high rings: the larger outside ring tests the bearing OD; the smaller ring tests the bearing bore. The dimension values are generated in [fit-coupons.json](fit-coupons.json).

| STL | Bearing pocket ID | Stationary stem OD | Intended use |
|---|---:|---:|---|
| `fit-coupon-tight.stl` | 75.00 mm | 59.95 mm | Tighter comparison; do not force onto bearing |
| `fit-coupon.stl` | 75.10 mm | 59.85 mm | Current product dimensions |
| `fit-coupon-loose.stl` | 75.30 mm | 59.65 mm | Looser comparison |

Measure the printed diameters and actual bearing, then select dimensions giving a removable slip fit with acceptably low play. Do not press through the shields or transmit fitting force across the balls. These samples characterize diameter only; a 3 mm coupon does not prove the full 7 mm seat's roundness, taper or axial retention. Apply the chosen dimensions to `bearing_pocket_id` and `bearing_stem_od` in `parameters.json`, regenerate all prints/CAD and repeat the geometry checks before using a changed set.

The stationary shoulder and upper clamp extend to **R31.20 mm**. They must contact only the inner race. The grip shoulder and lower retainer begin at **R36.20 mm**. They must contact only the outer race. Check both bearing faces, including chamfers, shield recesses and any protruding shield. If a contact overlaps a shield, obtain a dimensioned drawing or measure the race diameters and revise these contact lands. **Do not infer these dimensions from the silver render.**

Rotate the bare bearing and record its feel before installation. Fit the inner clamp, then the outer retainer, checking rotation after each tightening step. Any new binding, shield contact or axial preload requires correction. The nominal axial capture is 7.00 mm against a nominal 7.00 mm bearing; no tolerance or preload margin has been established. The CAD bearing remains a solid catalogue envelope with a steel material; it does not claim accurate race/shield internals.

## Clearance sensitivity

The example print error below is an **assumed sensitivity case**, not a printer specification or measured capability. Supplier bearing and screen tolerances are not supplied in this project's sources. Therefore even a positive example result is not a worst-case qualification.

| Interface | Nominal clearance | Example sensitivity / implication |
|---|---:|---|
| 60 mm bore / 59.85 mm printed stem | 0.15 mm diametral | Stem +0.20 mm alone gives **−0.05 mm** interference; calibrate with coupon |
| 75.10 mm pocket / 75 mm bearing OD | 0.10 mm diametral | Pocket −0.20 mm alone gives **−0.10 mm** interference |
| Ø2.70 PCB holes / Ø2.50 printed locator pegs | 0.20 mm diametral | Peg +0.20 mm consumes clearance before PCB/drill tolerances |
| PCB top / lid capture pads | 0.00 mm at Z4.20 | Board thickness and print height variation can pinch or loosen PCB; measure rather than force the lid shut |
| Fixed bezel / grip | 0.60 mm radial | Each surface 0.20 mm toward gap leaves 0.20 mm before eccentricity/runout |
| Front glass / bezel relief | 0.20 mm axial | One 0.20 mm adverse height error consumes relief; no added foam is modelled |
| Trimmed solder tails / well floor | 0.60 mm before insulation | 3M 5413's 0.069 mm thickness leaves 0.531 mm nominal; remove sharp ends and inspect physically |
| USB approach envelope / rotor | 1.50 mm vertical | Includes the specified plug's drawing tolerance; print height, connector placement and actual mating still need checking |
| Ø4.40 driver window / Ø3.80 screw head | 0.60 mm diametral | Test the actual screw head and screwdriver shaft before closing the product |

## Required measurement record

| Item | Record before signoff | Current status |
|---|---|---|
| Bearing | Manufacturer/lot, bore, OD, width, inner/outer usable face diameters on both sides, free rotation before/after retention | Not measured |
| Prints | Actual coupon IDs/ODs, selected compensation, full seat taper/roundness, glass relief, rotor runout and direct-button return | Not printed |
| Supplied display lead | Insulation OD, PH housing dimensions, safely dressed bends, actual per-wire trim lengths, solder-end support and eight continuity results | Not measured |
| Display | Purchased module matches 19192 STEP; carrier/tab/bosses supported without glass/PCB load | Not measured |
| PCB and fasteners | Actual board thickness, pegs/capture-pad fit, solder-tail clearance, M2 thread engagement, driver access | Not measured |
| USB and operation | Actual plug fully mates in both orientations; mechanical rotation, optical counting, host USB and retained count tested | Not tested |

Complete the operating checks in [BRINGUP.md](../validation/BRINGUP.md). A filled measurement record, rather than a passing render, is the physical-fit evidence still needed for the fabrication-ready goal.
