# Validation and prototype bring-up

Software checks and hardware measurements are different deliverables. The release validation report and command logs record the checks actually run. The checklist below requires a manufactured, assembled prototype and remains **unperformed** until measurements are attached.

## Software acceptance

- Strict TypeScript check of the authored source.
- tscircuit netlist, schematic placement, PCB placement, full routing, and copper-short checks with no suppressed electrical checks.
- Independent KiCad DRC with the declared manufacturer rules, zone refill, no DRC exclusions, and no unconnected items.
- Generated Gerber and Excellon files parsed and rendered for inspection; layer presence, outline, slots and hole count checked.
- BOM populated with manufacturer part numbers; DNP programming interfaces identified; placement coordinates tied to the final PCB.
- Native tests of the embedded counting implementation: both directions, wrap, backtracking, slow one-LSB motion, scroll gate transitions, stale/invalid/jump rejection, counter saturation, CRC corruption, interrupted record prefixes and thermal-gate boundaries.
- ARM firmware successfully linked against the STM32F072CB memory map. Release manifest hashes tie the source, binary, board and fabrication bundle together.
- Printable meshes are watertight with positive volume. Nominal moving-part and battery clearances are checked from assembly coordinates.

## Before applying power

- [ ] Inspect bare-board dimensions, 2.7 mm mount holes, USB shield slots and connector locator holes.
- [ ] Inspect QFN EP joint and orientation of every IC, USB connector, LED and JST connector. Meter BAT+, GND and 3V3; check for unexpected shorts.
- [ ] Leave battery disconnected; use current-limited USB power at 5 V / 100 mA. Record idle input current, SYS and 3V3. Confirm no overheating.
- [ ] Verify PA13/PA14 SWD access, MCU ID and firmware programming/verification. Confirm the executable starts at 0x08000000.
- [ ] Check NTC open and short faults both hold CE high. At room temperature, measure TS and TEMP_ADC and compare against the divider calculation. Verify CE behavior before connecting a cell.

## USB and power path

- [ ] Enumerate HID + CDC on Windows, Linux and macOS with C-to-C and A-to-C data cables, including connector reversal.
- [ ] Measure input current before configuration, after configuration, during suspend and on resume; validate USB100/USB500/suspend EN logic and the descriptor's requested power.
- [ ] Scope D+/D− at the connector and MCU; verify signal integrity at full-speed, no unintended back-power on disconnect and adequate ESD return paths. The PCB is a short-run 12 Mbit/s USB design, not a certified USB product.
- [ ] With a protected cell installed, verify battery-only operation, live plug/unplug, simultaneous counting and charging, CV termination, recharge, input droop and absence of resets through handover.
- [ ] Measure actual charge current across the cell voltage range. Verify charger temperature, cell temperature and safety-timer behavior. Temperature-test the NTC/CE window across bias/divider tolerance and the cell's permitted 0–45°C charging range. Do not infer cell temperature from board temperature.
- [ ] Discharge slowly on a bench simulator to verify the 3.45 V software fault threshold and count preservation; separately verify the chosen cell protector's limits using its manufacturer's procedure.

## Rotation and persistence

- [ ] Confirm AS5600 0x36 and FRAM 0x50, then initialize the count explicitly. Verify STATUS reports storage_ok and magnet_ok true.
- [ ] Scope I2C rise time and sample interval. Measure maximum gap during USB traffic, FRAM commits and console requests. Reject unexplained gaps; establish a documented maximum usable rotation rate.
- [ ] Sweep the knob through 360° and inspect MD/MH/ML, raw-angle monotonicity and zero-crossing behavior. Adjust magnet centering/gap and recheck at all temperatures of interest.
- [ ] Run known marked turns: 100 clockwise, 100 counterclockwise, alternating half-turns, +180/−540°, small jitter, slow motion and a range of speeds. Compare against an independent optical/mechanical reference.
- [ ] Disable scrolling during rotation: counts must continue and the computer must receive no wheel reports. Re-enable without stale movement. Repeat disconnected, during suspend, on resume and while charging.
- [ ] Power-cycle after an acknowledged count/reset. Inject power loss at different points in a FRAM commit and verify recovery chooses the last valid record. Measure the maximum last-turn loss window and document it.
- [ ] Disconnect/remove the magnet and interrupt I2C. Confirm invalid data does not add phantom turns and recovery starts with a fresh baseline.

## Mechanical acceptance

- [ ] Fit the coupon first. Measure actual bearing fits, retention, axial/radial play and printed part dimensions.
- [ ] Confirm countersunk outer-retainer screws are flush; verify 0.4 mm nominal rotor-to-lid clearance through a full turn under hand pressure.
- [ ] Confirm inner retainer contacts only the inner race and outer retainer only the outer race. Check screw-head clearance under the roof and magnet-post clearance through the collar.
- [ ] Inspect cell insulation, ribbon tension, swelling allowance, connector/wire bend radius and trimmed solder tails. No fastener or moving part may press on the pouch.
- [ ] Test reset-plunger return, switch access, LED visibility, USB cable insertion/removal and case retention. Assess bearing drag, feel, stiffness and drop resistance.

The first fabrication run is a prototype-validation run. Production qualification, regulatory testing and commercial USB identifier assignment remain separate work.
