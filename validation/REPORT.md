# Rev A / v1.0.1 validation record

Reviewed 2026-11-04. This is a fabrication package validated in software. No physical prototype has been manufactured or measured by this project.

| Check | Actual result |
|---|---|
| Strict TypeScript | Passed |
| tscircuit netlist and schematic placement | Passed; no placement recommendations |
| tscircuit PCB placement | 0 errors, 0 warnings |
| Full source build | 1 circuit passed; no circuit error records |
| Copper shorts | None detected |
| Connectivity contract | 57 components; physical pin mapping, distinct rails, every connected pin has copper; two actual JST through-holes |
| KiCad 10.0.7 DRC after normal zone refill | **0 violations, 0 unconnected items**, no item exclusions |
| Actual Gerber/Excellon parsing | 9 graphical layers; Ø64 mm outline; 133 plated round drills, 4 plated slots, 8 NPTH; source drill counts match |
| BOM / placement | 57 source components, 54 populated placements; J3/J4/J5 DNP |
| Counter C tests | CW/CCW, wraps, backtracking, slow motion, mode gates, stale/invalid/jump rejection, saturation, CRC corruption, 32 interrupted prefixes and temperature-window boundaries passed |
| ARM firmware | Linked for STM32F072CB; 57,216-byte binary; 128 KiB flash / 16 KiB RAM target |
| Linked-image inspection | Correct stack/reset/USB interrupt vectors; CDC control/data + HID interfaces; four distinct endpoints; wheel relative-input descriptor |
| Mechanical geometry | Seven positive-volume watertight STL meshes; moving part, cell, connector and control clearances checked |

`logs/` records the commands' actual outputs. `kicad-drc.json`, `manufacturing-inspection.json`, `firmware-image-check.json` and `mechanical/geometry-check.json` provide machine-readable evidence. Top/bottom native PCB previews, source schematic sheets, assembly drawings and **plotted Gerber copper** views are in `previews/` and were visually inspected.

The source build emits two non-failing tool notices: a React list-key warning in schematic rendering and an optional saved-escape-path cache warning for the GND net. The circuit still builds with no circuit errors; the published prescribed routing, connectivity test, short check and independent DRC validate the actual copper. No routing or electrical checks were suppressed. KiCad's default ignored check categories (missing courtyard, track centering on vias, tuning profiles, symbol footprint filters and footprint pad-type classification) remain listed in its JSON report; they were not changed to clear an electrical failure. Gerbonara accepts KiCad's redundant post-header G90 with a syntax warning and parses all drill geometry.

Manufacturing finalization is explicit: source-derived pads/nets/routes are preserved, floating ground islands removed by refill, the QFN paste aperture reduced, and MCU corner silk shortened to clear solder-mask openings. The Gerber bundle is plotted from that final checked board. `release-manifest.json` binds the inputs and generated artifacts with SHA-256; the `v1.0.1` Git tag identifies the exact published source commit.

The 350 mAh protected cell was selected to clear the bottom JST housing. Nominal software-checked gaps are 2.0 mm cell-to-PCB, 1.65 mm sensor-package-to-magnet and 0.4 mm rotating-retainer-to-lid. Printing tolerances, cell swelling, leads, wiring and hand pressure still require a fit trial. Source inventory snapshots are observations, not purchase guarantees.

Required physical verification remains in [BRINGUP.md](BRINGUP.md): USB enumeration and electrical/current compliance; charge current, NTC window and thermal behavior; power-path handover; angle sampling rate and magnetic alignment; counting accuracy at measured speeds; power-cut journal recovery; battery runtime; and printed fit/bearing feel. The first board order is a prototype-validation run. The firmware uses TinyUSB's development VID/PID and needs authorized identifiers before commercial distribution.

Patch v1.0.1 replaces libc-dependent 64-bit printf formatting with a tested decimal conversion. The clean Ubuntu ARM build exposed the earlier PRIu64 availability difference; the console now handles zero, values above 32 bits and UINT64_MAX without optional libc format macros. PCB, routing, mechanics and fabrication files are unchanged from v1.0.0.
