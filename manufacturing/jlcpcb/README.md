# JLCPCB handoff guidance — one prototype, India

Use the [current verified fabrication/assembly ZIP](../../release/desk-knob-e6-e12-fabrication.zip) and its [upload guide](../current/README.md). It contains one matching E6 Gerber/drill set, complete and SMT-only BOM/CPL pairs, the physical pin map and fresh validation evidence. No supplier upload or order has been made. [Board requirements](../README.md) and [review results](../../validation/REPORT.md) describe the checked source.

**Do not order the historical v5.4.0 outputs.** Their FRAM footprint was undersized and several library zero angles differed. Those generated files have been removed from this working revision. Export a complete new set from the corrected source; never mix revisions.

## Upload and final review

1. Use PCB E6 and the exact **XUNPU TYPEC-309-ACP16L65 / C2909598** USB connector. Its 0.60×1.50/1.60 mm shield slots meet the normal ≥2:1 guidance; the old short-slot connector is removed. Do not substitute a superficially similar USB-C part without qualifying its footprint. [Selection evidence](../../reference/usb-connector-selection.json).
2. Upload `manufacturing/current/Gerbers-E6.zip`, containing the current copper, mask, paste, silk, outline, plated drills and NPTH drills together. Keep two layers, 1.6 mm FR-4, 1 oz copper, ENIG, 68×83.5 mm outline extents and the routed inner window. Current vias are **Ø0.30 mm drills / Ø0.60 mm pads**, replacing the old Ø0.20 mm drills. Preserve the actual drill files.
3. Use a matching current BOM and CPL pair: **39 fitted components, all top**, including JST PH6 J4 and JST SM08B-SRSS-TB(LF)(SN)/C160407 SMT J6. The 38-placement SMT-only option leaves only J4 for local through-hole soldering.
4. Match exact manufacturer/MPN/catalogue IDs from [the part catalogue](../../reference/jlcpcb-parts.json). Use JLCPCB's documented [BOM](https://jlcpcb.com/help/article/bill-of-materials-for-pcb-assembly) and [CPL](https://jlcpcb.com/help/article/pick-place-file-for-pcb-assembly) fields. Keep the CPL origin consistent with the exported Gerbers; never take absolute values or mirror only the placement file.
5. Inspect every placement against its real copper and physical pin 1, particularly U1/U3–U7, U2, J1/J4 and SW1. Library zero angles differ, as [JLCPCB explains](https://jlcpcb.com/help/article/pcb-assembly-faqs-part-2). Request engineering confirmation of feeder origin/rotation. J1 faces +Y; the side button faces −Y. Preserve the supported overhanging housings, finished outline and window. Assembly rails/fiducials may be added outside that finished outline by the supplier.
6. Recheck availability, assembly eligibility, price, quantity minimums and India shipping/import charges in your new quote. Keep placement confirmation manual. You place/pay the order; none has been placed here.

The [top assembly view](../../previews/assembly-top.svg) marks actual physical pin 1. Source adapters preserve the imported physical pad numbering and copper/drill geometry; the [footprint check](../../validation/check-jlc-footprints.ts) compares all **179 pads across 39 references**, including fitted J6. Supplier feeder approval is a separate step from that geometry check.

The screen, bearing, fasteners, adhesives, foam and six printed parts are separate from PCB assembly. Order one H1 crimped JST-SH8-to-PH8 replacement cable. The supplied Waveshare jumper lead is unused. [Wiring](../WIRING.md), [parts list](../../README.md) and [first-build tests](../../validation/BRINGUP.md).

## Current catalogue availability

A fresh read-only check on **9 November 2026** matched all **23 fitted MPN/catalogue lines** and found public catalogue quantities covering two nominal boards per line. All records were marked purchasable. The MCU showed 32 units; USB connector 1,105; optical sensor 1,305; keyed display socket 175,126. [Current exact-line evidence](../current/checks/public-sourcing.json). These are not reserved quantities, a feeder approval or a lead-time/price guarantee. Review minimum purchases, attrition, allocation and the final quote before payment.

Fresh BOM/CPL sets match 39 complete or 38 SMT placements and all 179 physical pin coordinates. The current authenticated supplier feeder/origin/rotation and engineering DFM preview remains unverified; complete that preview for these exact files. The historical v5.4.0 preview does not approve this package. Red assembly dots mark physical pin 1, with USB A1 for J1.

## Historical availability and cost evidence

On 6 November 2026 the signed-in **old v5.4.0 draft** matched **22/22 BOM lines and 38 top placements**. Its placement preview exposed the footprint/angle defects, so it was not approved for ordering. This establishes historical part matching only; the corrected layout has not been uploaded as part of this task.

- U2 is genuine **Vishay TCUT1600X01 / C511085**, stocked pre-PCN material. The `_A` version, C24626661, was unavailable. [Vishay's PCN](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6165/PCN-OPT-1311-2024-REV-0.pdf) documents unchanged fit/form/function for its wafer change. Retain the dual-channel part and verify optical performance on the prototype.
- J4 is genuine **JST B6B-PH-K-S(LF)(SN) / C131342**, found through TSCI's JLCPCB search; it was selected for Standard manual assembly.
- C6/C12/C18 use stocked **Samsung CL21A475KOFNNNE / C1746**, 4.7 µF/16 V/X5R/0805, replacing the obsolete Murata selection.

The [point-in-time review](../../reference/jlcpcb-cost-review.json) records selected codes, quantities and costs. The old baseline was **$190.15** for five bare boards and two Standard assemblies before shipping/import: PCB $72.21, PCBA $117.94, including $22.64 parts and $32.55 feeder loading. The form required five bare/minimum two assembled boards, leaving extras for a one-device prototype. This is not a quote or stock reservation for the corrected board.

TSCI search also found inexpensive Basic alternatives C25804, C25803, C14663, C15849 and C1525. They are discovery candidates, not approved substitutions; the selected passives were already stocked and inexpensive. [Standard PCBA pricing](https://jlcpcb.com/help/article/pcb-assembly-price) charges feeder loading for Basic as well as Extended parts, so changing labels alone does not remove that cost. Qualify any future substitution against package, ratings, footprint, stock and assembly process, then rerun checks.
