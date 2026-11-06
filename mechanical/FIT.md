# Mechanics E4 fit basis for PCB E3

The fabrication package uses published component boundaries and the requested **best approximations** where detailed supplier data is unavailable. Estimated dimensions remain identified as estimates. This is a design for a first prototype, with calibrated FDM targets; it is not represented as physically tested production hardware.

## Bearing interfaces

The purchased part remains **6712ZZ, 60 mm bore ×75 mm OD ×7 mm width, two metal shields**. [Maysme's catalogue](https://maysmeprecision.com/Show/?Cid=677) confirms the envelope and shielded option. The six-piece model adds separate chamfered races, two recessed shields, balls and a cage. Its internal dimensions, 44-ball count and groove details are engineering/visual approximations in `parameters.json`, not a drawing for manufacturing a bearing.

The same-size open **NSK NB712A** provides a mounting analogue: [NSK E1153a, printed pages 4–5](https://www.nsk.com/content/dam/nsk/common/catalogs/ctrgPdf/bearings/e1153a.pdf#page=4) gives shaft shoulder da ≥62 mm, housing shoulder Da ≤73 mm, maximum fillet 0.3 mm. Those values inform the estimated Maysme interfaces; NSK is not the selected purchased part and its data does not certify Maysme internals.

E4 uses a **Ø62 mm inner-race contact**, **Ø73 mm outer-race contact**, **Ø59.80 mm stem**, and **Ø75.20 mm pocket**. The post ends 0.4 mm below the nominal upper clamp and the rotating housing wall ends 0.4 mm above its lower retainer. Tightening therefore seats each retainer on its own race before a printed hard stop. Both races are retained independently; the rotor is free to settle axially with bearing width. The CAD checks all four intended race contacts and rejects contact with a shield, cage, balls or the opposite race.

The approximated flat race faces provide 0.7 mm nominal radial contact width outside their edge chamfers. These contact widths and estimated shield recess are accepted model assumptions. Do not use the ball/cage model as a load, precision or life rating.

## Print calibration and numerical fit budget

Use PETG at 0.2 mm layers, ≥4 requested perimeters on structural parts, with the optical wall printed as two 0.4 mm lines. The optical wall is **0.8 mm**, so the fixed sensor's 3 mm gap has 1.1 mm nominal radial clearance per side. Print the three coupon choices with the final material, orientation and slicer compensation. Target **±0.10 mm on bearing-fit diameters** and **±0.10 mm relative mating height**. The budget is a required calibration target and an engineering estimate, not a claim about an uncalibrated printer.

| Coupon STL | Pocket ID | Stem OD |
|---|---:|---:|
| `fit-coupon-tight.stl` | 75.10 mm | 59.90 mm |
| `fit-coupon.stl` | 75.20 mm | 59.80 mm |
| `fit-coupon-loose.stl` | 75.40 mm | 59.60 mm |

Each file contains two separate 3 mm-high rings. The larger ring tests bearing OD, the smaller ring tests the bore. A short coupon does not establish full-seat taper; trial-fit the complete seats too. Update `bearing_pocket_id` / `bearing_stem_od` and regenerate the complete print set when compensating a particular printer.

[fit-budget.json](fit-budget.json) records the assumptions and calculations. Bearing diameters are allowed ±0.02 mm and width ±0.20 mm as conservative estimates, not Maysme tolerances. PCB thickness is allowed ±0.16 mm. The case/lid alignment, printed surface and SMT placement allowances are included explicitly.

| Result under the stated budget | Remaining margin |
|---|---:|
| Stem / bore, minimum diametral clearance | 0.08 mm |
| Pocket / bearing, minimum diametral clearance | 0.08 mm |
| PCB hole / locator peg, minimum diametral clearance | 0.35 mm |
| Bezel / grip after estimated eccentricity and print errors | 0.18 mm radial |
| Optical fork after positional errors and circular-track sagitta | 0.075 mm radial |
| Optical slot / beam after estimated height errors | 0.19 mm axial |
| Front glass / relieved bezel | 0.20 mm axial |
| Each retainer / printed hard stop | 0.10 mm axial |
| Each bearing-retainer M2 screw, minimum thread engagement | 4.10 mm |
| USB plug gauge / lower rotor | 1.04 mm vertical |

The geometric check expands complete circular rotor envelopes by **0.62 mm XY / 0.30 mm Z** against fixed prints, and **0.945 mm XY / 0.46 mm Z** against PCB hardware and cable. Filling grooves and screw holes covers every rotor angle. The front opening is 8×4 mm (Z2.8–6.8 mm); four worst-case PCB positions are checked for fingertip access at maximum switch travel. The larger envelope accounts for bearing fits, PCB locator play, lid alignment and estimated package placement. The full selected package meshes and the official screen geometry remain in these checks.

## Compliant PCB capture

Use six Rogers **PORON 4701-30-20062-04** foam discs: four Ø4 mm at the PCB mounting-hole axes and two Ø2.6 mm at (±6,−37) mm. [Rogers 4701-30 data](https://www.rogerscorp.com/-/media/project/rogerscorp/documents/elastomeric-material-solutions/poron/english/data-sheets/17-006-poron-4701-30-very-soft.pdf) supports the 320 kg/m³ grade, 1.57 mm thickness and ±10% thickness tolerance. Attach them under the E4 lid with 0.05 mm 467MP adhesive.

The assembled CAD shows 1.05 mm compressed foam plus 0.05 mm adhesive in the 1.10 mm space above the PCB. The budget gives approximately **6.6–54.8% compression**, including PCB, printing, foam and adhesive allowances. A 60% upper compression limit is our engineering criterion, not a Rogers operating rating. The four locator pegs are reduced to Ø2.2 mm. The pads restrain the supported board without forcing it between rigid nominally coincident planes. The E3 lid has no room for these pads: use the complete E4 set.

## Supplied display cable

Use the **cable included with Waveshare 19192**, keeping its factory display PH plug and shortening/soldering the PCB end at J6. No replacement display lead or extra connector contacts are required. The model uses **Ø1.2 mm wire**, a **Ø1.5 mm clearance check**, a nominal PH plug, and an estimated static dressed path. The 3 mm dressing radius describes its XZ projection; the actual 3D centreline minimum is calculated per wire in [harness.json](harness.json), rather than claimed as a supplier bend rating.

The insulated spans are approximately 37 mm; leave about 2.55 mm stripped at the PCB end and trim each wire to its dressed path. Trial-route before cutting. Wires are fixed in service. Their OD, conductor size, contact microgeometry and bend limits remain estimates because the supplier resources found publish only the cable type and 20 cm nominal length. Check continuity by signal labels rather than colour.

## First-prototype checks

Before extended use or a production order, carry out [BRINGUP.md](../validation/BRINGUP.md): physical fit and free rotation, correct retainer seating, supplied-wire dressing/continuity, pad compression, original button access, USB insertion, 950 nm optical contrast/counting, and host USB operation. These checks are not marked as performed. The accepted approximations allow the digital fabrication package to proceed without supplier replies; they do not turn estimates into measurements.
