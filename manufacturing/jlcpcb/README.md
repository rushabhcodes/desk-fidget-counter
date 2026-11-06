# JLCPCB upload guide — one prototype, India

Use **v5.4.0 / PCB E3 / mechanics E4**. You place the order and handle shipping/payment. No order has been placed. JLCPCB's Gerber parser accepted the board on 6 November 2026 and detected **2 layers, 68 × 83.2 mm**. This is parser acceptance, not an engineering DFM sign-off.

## Files to upload

| Step | File | Contents |
|---|---|---|
| PCB fabrication | `../desk-knob-reve3-gerbers.zip` | Authoritative Gerbers and drills; upload this ZIP, not the full project ZIP |
| Complete assembly request | `BOM-complete.csv` + `CPL-complete.csv` | **38** fitted references, all top, including through-hole J4 |
| SMT assembly, J4 fitted locally | `BOM-smt.csv` + `CPL-smt.csv` | **37** fitted references; solder the genuine JST J4 header after SMT assembly |
| Engineering reference | `physical-pin-map.csv` and `../../previews/assembly-top.svg` | Actual physical pin positions and top assembly drawing |
| Verification | `checks.json` | Source/output hashes, population and coordinate checks |

Keep each BOM with its matching CPL. J6's optional header is **DNP** in both sets; its pads take the shortened display cable later. The display, bearing, screws, adhesives, foam and printed housing are separate purchases in the root README.

These CSVs follow JLCPCB's [BOM fields](https://jlcpcb.com/help/article/bill-of-materials-for-pcb-assembly) and [CPL fields](https://jlcpcb.com/help/article/pick-place-file-for-pcb-assembly): UTF-8, millimetres, `Top`, counter-clockwise degrees. **Negative Y is intentional** and shares the KiCad Gerber origin. Do not take absolute values or move/mirror only the CPL. Every location is checked against its source footprint origin. Rotations are normalized to 0–360° without guessed feeder corrections.

## PCB order settings

| Field | Selection |
|---|---|
| Material | FR-4, Tg ≥135°C |
| Layers / thickness | **2 / 1.6 mm** |
| Dimensions | **68 × 83.2 mm** (either orientation) |
| Copper | 1 oz outer copper |
| Finish / mask / silk | ENIG / green / white |
| Actual minimum trace / copper gap | 0.10 / 0.15 mm |
| Actual vias | **Ø0.20 mm drills / Ø0.60 mm pads**; preserve drill files |
| Format | Single PCB; JLCPCB may add external rails/panelization for assembly |
| Test | Full electrical test and any tests required by the chosen process |
| Quantity | Target **one complete prototype**; select the smallest offered bare-board quantity and request one assembled board through Standard Assembly if available in your quote |

Select the **0.2 mm drill class**, not 0.3 mm. In the live quote, this displayed a high-precision notice automatically selecting Kelvin testing and plugged vias. Review those options/cost using the actual **0.20/0.60 mm** geometry; the class caption's 0.30/0.35 mm pad sizes are not this board's pad sizes. Do not enlarge drills or alter Gerbers to bypass a quote warning.

Paste for engineering review:

> Two-layer 1.6 mm FR-4, 68 × 83.2 mm. One closed outer profile and one closed routed inner window. Minimum trace 0.10 mm, clearance 0.15 mm; vias drill 0.20 / pad 0.60 mm. J1 USB-C and SW1 intentionally overhang their supported PCB tips; retain their lands/slots. All components on TOP. Do not fit J6. Verify exact manufacturer/MPN, feeder origin and rotation against the physical-pin map and top drawing. J1 mouth faces +Y; SW1 actuator faces −Y. Add assembly rails/fiducials outside the finished board as necessary; preserve finished outline, window and placements.

JLCPCB's [published copper rules](https://jlcpcb.com/help/article/jlcpcb-copper-weight) allow 0.10 mm tracks on 1–2 layer FR-4 with 1 oz copper. Keep 1 oz; 2 oz would require wider tracks.

## Match the components

`../../reference/jlcpcb-parts.json` records exact MPNs, packages, known catalogue codes and primary sources checked on 6 November 2026. **Catalogue identity is not a stock reservation or current assembly-eligibility guarantee.** Check manufacturer as well as MPN; ST USBLC6-2SC6 and TI SN74LVC2G17DBVR have similarly named parts from other manufacturers.

- **U2, Vishay TCUT1600X01_A:** no exact JLCPCB catalogue code was verified. Use JLCPCB Global Sourcing/consignment for this exact part, or buy and fit it locally. [DigiKey's exact part](https://www.digikey.com/en/products/detail/vishay-semiconductor-opto-division/TCUT1600X01-A/25823737) was active and stocked when checked. It is a dual-channel, 3 mm-fork sensor; do not substitute TCPT/TCST or a single-channel part.
- **J4, JST B6B-PH-K-S(LF)(SN):** through-hole. Match supported manual assembly in the complete set, or use the SMT-only set and solder J4 locally. Its code is blank because an exact catalogue match was not verified.
- **C6/C12/C18:** Samsung **CL21A475KOFNNNE / C1746**, 4.7 µF, 16 V, ±10%, X5R, 0805, replacing obsolete Murata GRM21BR61A475KA73L. Lands and nominal 2.0 × 1.25 × 1.25 mm body are retained.
- Verify U3 FRAM and SW1 availability/service eligibility in the matching page. Do not accept an unselected required component as a completed device. If fitting U2 locally, deselect it consistently in the order BOM/CPL and record the omission; operation still requires it.

Compare the final preview against physical copper pins, particularly U1/U3–U7, asymmetric U2, J1/J4 and SW1's actuation direction. JLCPCB [documents differing library zero-angle conventions](https://jlcpcb.com/help/article/pcb-assembly-faqs-part-2); a generic red dot is insufficient. The supplied map includes all physical pad centres in the Gerber frame. A logged-in JLCPCB feeder preview has **not** been approved by this package.

## Prints and final assembly

The PCB order alone is not the complete device. Supply Waveshare **19192** with its included lead, a **6712ZZ 60 × 75 × 7 mm** bearing, eight prints, six PORON pads, adhesives and screws from the shopping list. Solder the shortened lead into J6, program through J4 and follow ASSEMBLY.md/BRINGUP.md.

Print the three fit coupons first. The design requires **±0.10 mm bearing-fit diameters and ±0.10 mm relative mating heights** after calibration/finishing. JLC3DP's [standard FDM tolerance](https://jlc3dp.com/help/article/3d-printing-design-guideline) is **±0.3 mm within 100 mm and ±0.4 mm for holes**; it does **not** meet this fit budget. Request critical-dimension finishing/inspection, or calibrate and print locally. Do not assume a default-tolerance enclosure order will fit. Preserve the 0.8 mm encoder wall and verify 950 nm opacity of the actual material.

## Shipping to India

Select **India** and your actual address/postal code in your own checkout. The checkout/carrier determines shipping and import charges; this package contains no delivered-price quote. JLCPCB's [shipping information](https://jlcpcb.com/help/article/shipping-methods-and-delivery-time) and [customs guidance](https://jlcpcb.com/help/article/customs%2C-duties-and-taxes) describe destination charges and India's courier KYC process. Supply any identification directly through the verified supplier/carrier flow. No identity documents are stored in this public project.

Physical power, USB, counting and print-fit checks remain in `../../validation/BRINGUP.md`. Unpublished bearing/cable details retain the accepted approximations.
