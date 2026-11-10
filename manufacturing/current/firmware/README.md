# Firmware 6.0.0 — RP2040 F1 only

These four images match RP2040 PCB F1 with Winbond W25Q16JVSNIQ 2 MB flash. The binary/HEX flash base is **0x10000000**. They are incompatible with historical STM32 boards. No factory programming is requested.

USB powers the board. J4 pins 1–6 are VTref 3.3V, SWDIO, SWCLK, RUN, GND, BOOTSEL. VTref is probe sense. With a suitable CMSIS-DAP / Raspberry Pi Debug Probe and RP2040-capable OpenOCD, run from the kit root:

```sh
openocd -f interface/cmsis-dap.cfg -f target/rp2040.cfg \
  -c 'program firmware/desk-knob.elf verify reset exit'
```

For ROM USB recovery, bridge J4 pin 6 to pin 5, pulse RUN pin 4 to GND, release RUN, then remove the BOOTSEL bridge. Copy **desk-knob.uf2** to the RPI-RP2 volume. BOOTSEL reaches flash CS through 1 kΩ. Check the physical pin map in WIRING.md and verify both boot methods on the first assembled board.

The linked image is 35,692 bytes; boot2 CRC, vector bounds, HID/CDC USB descriptors, Intel HEX and RP2040 UF2 family/payload checks passed. Dependencies are Pico SDK 2.2.0 and TinyUSB 0.21.0; notices are included. GPIO-map.json is the hardware/firmware contract.

After first power, deliberately initialize a fresh FRAM by holding the front button for three seconds. Test USB suspend/resume/current, display, optical phase/speed and button return before closing the enclosure. See BRINGUP.md and the repository firmware guide for the source build and companion application.
