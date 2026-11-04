# Physical prototype bring-up / Rev B

These measurements are outstanding. Software checks and envelope CAD do not establish hardware operation. Use current-limited bench power and the specified protected cell; record instruments, firmware tag, results and photographs here.

## Power and charging

- [ ] Inspect the bare PCB against Gerbers; check 3V3/SYS/BAT/VBUS isolation, solder bridges, USB shield ground and U4 exposed pad.
- [ ] Test first without the pouch. Confirm 3V3 and charger output, correct battery connector polarity and no unexpected heating.
- [ ] Confirm PH8 pin order/continuity and correct 3.3 V screen input before connection. Measure display/IR/system current in battery, USB and suspend states.
- [ ] Attach insulated pouch NTC. Sweep the real thermistor over temperature; verify firmware CE window and the independent charger TS gate. Open/short NTC must disable charging.
- [ ] Measure charge current (nominal 201 mA), precharge, termination, restart, timeout and pouch/charger temperatures. Check charger power-path operation with the screen running.
- [ ] Verify USB100 before enumeration, USB500 after configuration and suspend input mode. Test a current-limited USB source and both USB-C orientations.
- [ ] Test USB/battery handover during continuous rotation, persistent low-battery gating and protected-cell cutoff. Measure usable runtime; do not infer it from nominal cell capacity.

## Programming, USB and screen

- [ ] Verify JST J4 physical pins and 3.3 V VREF sense, flash via SWD, verify memory and exercise BOOT0/NRST ROM recovery.
- [ ] Initialize FRAM with `RESET CONFIRM`. Confirm power-cut journal recovery during every stage of a save; unknown/corrupt records must show `RESET VIA USB`.
- [ ] Confirm CDC and HID enumeration on intended OSes, USB-C flips, rapid hotplug, suspend/resume and no replay of queued wheel movement.
- [ ] Confirm GC9A01 cold/warm startup, colour order, 90° mounting orientation, backlight, full 20-digit count layout and live battery/charge/scroll/USB states. Compare voltage readout to a meter.
- [ ] Unplug/replug the LCD and disturb its SPI wiring. The write-only interface cannot prove screen presence; ensure any stalled transport leaves counting/USB responsive.

## Optical counting and controls

- [ ] Verify TCUT common collector to 3V3, separate emitter pulldowns and approximately 14 mA IR LED current. Inspect tall sensor solder joints and orientation.
- [ ] Scope both Schmitt inputs and PB4/PB5 outputs through one revolution. Confirm high/low margins, approximately 90° phase, **48 periods/channel and exactly 192 combined edges/revolution**.
- [ ] Test the printed skirt's 950 nm opacity, slot dimensions, axial/radial alignment, dust, sunlight and indoor lighting. A visibly black print may transmit IR. Replace material if contrast is inadequate.
- [ ] Compare 10, 100 and 1000 measured turns in both directions; exercise slow single-edge motion, reversals, stopping on transitions and varied speeds. Establish the speed at which no counts are missed while LCD and FRAM run.
- [ ] Confirm clockwise wheel direction; swap channel mapping or invert the firmware direction if the intended feel needs it. Count magnitude must remain correct.
- [ ] Toggle scrolling off/on while rotating: count must continue and no old USB motion may replay. Check 20 ms switch debounce, both stable positions and recessed lever access.
- [ ] Simulate blocked optics, missing channels, loose encoder material and extreme speed. No optical amplitude feedback is fitted; measure/document failure behaviour rather than treating timer-running as optical health.

## Assembly and endurance

- [ ] Print the fit coupon, measure the bearing seats and tune printer-specific tolerances.
- [ ] Inspect the actual Waveshare module's rear components, PH8 housing and cable bend. Confirm the model's connector allowance and edge-only support; never tighten against a backside component.
- [ ] Confirm bearing outer/inner races are separately captured, screw heads and pilots clear, and the rotor group can be assembled/removed in the documented order.
- [ ] Measure bezel/grip clearance (nominal .6 mm radial), skirt/lid clearance (.5 mm axial) and sensor gap clearance (1 mm radial per side). Rotate under hand pressure in both directions with no rub.
- [ ] Confirm every cable stays fixed and clear of the bearing/encoder; battery tray and strap do not compress the pouch or abrade leads.
- [ ] Test USB plug fit through the recessed opening, toggle finger access, service JST access, bearing feel, long rotation endurance and intended desk loads.
