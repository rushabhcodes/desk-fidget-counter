# Firmware 6.0.0 / RP2040 PCB F1

The included `build/desk-knob.uf2`, `.bin` and `.hex` target **RP2040 PCB F1**, with external **Winbond W25Q16JVSNIQ 2 MB flash** at **0x10000000**. They do not target the earlier STM32 boards. F1 retains the E13 circular button, optical sensor, FRAM and Waveshare 19192 display.

## Build and program

```sh
bash scripts/test-firmware.sh
bash firmware/bootstrap.sh
python3 validation/check-firmware-image.py
```

The bootstrap pins Raspberry Pi Pico SDK 2.2.0 (`a1438dff1d38bd9c65dbd693f0e5db4b9ae91779`), TinyUSB 0.21.0 (`dae3f9a366bfcddbf9dcf1b48d7500286a849539`) and Arm GNU 14.3.Rel1 (archive SHA-256 is checked). It installs dependencies locally; CMake, Ninja, host C++ and Python 3 are required. The supplied compiler archive is Linux x86_64. Other hosts can install a compatible Arm GNU compiler and run `make -C firmware PICO_TOOLCHAIN_PATH=/absolute/path/bin` after fetching the pinned SDK/TinyUSB. CMake obtains Pico's picotool 2.2.0 to generate UF2. SDK startup/linker code replaces the old STM32 startup.

J4 is the top-entry JST PH6 service connector. Pins 1–6 are **VTref 3.3V, SWDIO, SWCLK, RUN, GND, BOOTSEL**. USB powers the target; VTref is probe sense. Use a CMSIS-DAP probe or Raspberry Pi Debug Probe supported by OpenOCD's RP2040 target. [Physical connector map](../manufacturing/WIRING.md).

```sh
openocd -f interface/cmsis-dap.cfg -f target/rp2040.cfg \
  -c 'program firmware/build/desk-knob.elf verify reset exit'
```

For USB recovery, bridge **J4 pin 6 BOOTSEL to pin 5 GND**, pulse **RUN (pin 4) to GND**, release RUN, then remove the BOOTSEL bridge. The ROM should expose **RPI-RP2**. Copy `desk-knob.uf2` onto that volume. Pin 6 reaches flash CS through R6 (1 kΩ); R7 (10 kΩ) pulls CS high. Do not use the old STM32 BOOT0-to-3.3V procedure. Verify both boot methods on the first assembled board. J4 is beneath the removable fixed screen; remove the programming harness before final assembly.

The schematic and generated `board-pins.h` share [reference/rp2040.json](../reference/rp2040.json); run `python3 scripts/generate-board-pins.py --check` after edits. RP2040 runs at 48 MHz from the USB PLL; the unused system PLL is powered down.

## Behaviour

GPIO20/GPIO21 feed PIO0 state machine 0, using Raspberry Pi’s BSD-licensed quadrature program. PIO collects edges during display/FRAM transfers. The 4 MHz state machine clock supports a configured 400,000 edge/s acquisition ceiling; that is not a measured optical speed rating. Schmitt inputs are enabled; the previous STM32 timer digital filter is not present. The 48-slot ring gives **192 edges/revolution** and six edges per HID wheel unit (**32 units/turn**). Completed displacement ±192 increments the unsigned 64-bit total; reversal cancels unfinished progress. Sampling targets 2ms. An invalid journal, sample gap above 20ms or jump above 48 edges discards uncertain progress. Measure the actual usable speed envelope.

The side-actuated GPIO0 front button uses the MCU's internal pull-up and 25ms debounce. Boot starts in Count-only mode. A short press changes Scroll / Count-only on release, clearing queued wheel motion while counting continues. A three-second hold clears/initializes FRAM once and does not change mode on release; the display shows progress and confirmation. A button held at boot or resume must be released before any action. Unused GPIOs remain at reset defaults; there is no separate reset button or LED. Detach/suspend clears motion queues; the powered-down optical sensor cannot measure turns while suspended. A new baseline is taken on resume.

FRAM uses I2C0 GPIO5 SCL/GPIO4 SDA at approximately 300kHz, address 0x50. Completed turns update alternating 32-byte records at 0/64: sequence, 64-bit count, CRC32 and a commit marker written last, followed by read-back. Unknown FRAM requires `RESET CONFIRM` or a deliberate three-second button hold. Previously committed records remain compatible. An unplug during a write may restore the previous committed turn count; no battery or reserve supply completes in-flight transactions.

The display uses SPI0 mode 0, 12MHz, GPIO18 SCK/GPIO19 MOSI, GPIO16 reset, GPIO23 backlight, GPIO17 CS and GPIO22 DC. One 480-byte RGB565 row is sent per task; there is no full framebuffer. Each refresh uses a coherent snapshot. The **module tab faces -X**, with **MADCTL 0xA8** for this mounting. Verify orientation and colours physically. A bounded transport fault blanks the screen while counting/USB continue. No MISO is present: a transport-success flag cannot prove the screen is connected or displaying correctly.

Laptop clock/date, CPU/RAM percentages and laptop battery/AC come from the local [companion](../companion/README.md). Samples expire after five seconds, then placeholders and `HOST OFFLINE` appear. Desktop/no-sensor machines show `NO HOST BATTERY`. The clock/calendar advances between samples and handles midnight/leap-year rollover. Turn count and scroll state remain visible. Invalid storage shows `HOLD 3S TO INIT`; holding displays progress, and successful clear shows `COUNT CLEARED`. A PIO acquisition fault uses the compatible `TIMER ERROR` display and `encoder_timer_running` console field.

## USB power

The USB descriptor is **bus-powered, 100mA**, HID mouse wheel + CDC. GPIO1 enables U4 TPS22919 only when USB is configured and awake. Before cutting the peripheral supply, firmware drives all LCD signals low to prevent back-powering. Resume ramps the rail, resets the scanline/init state and initializes the display again. LCD and IR are off before configuration and during suspend; the FRAM and MCU retain the always-on 3.3V rail.

USB suspend current, VBUS inrush and wake timing require physical measurement. During suspend, firmware disables the IR/LCD rail and encoder state machine, cancels the 1 ms application wake timer and uses WFI, leaving USB clocked for resume. This is not the STM32 Stop-mode implementation. Measure the actual whole-board suspend current with the SWD probe disconnected; no measured USB compliance is claimed. No remote wake-up is advertised. A charger without a data host will not configure the device and will not enable its display/encoder.

## CDC console

Newline-terminated ASCII, maximum 63 bytes per command, DTR asserted. `scripts/count.py` verifies application identity before reset or status operations. Close the dashboard companion before opening another program on the same serial port.

| Command | Result |
|---|---|
| `STATUS` / `COUNT` | JSON with device/protocol/firmware identity, turns, progress, storage_ok, encoder_timer_running, scroll_on, rejected, lcd_transport_ok, host_data_fresh |
| `RESET CONFIRM` | Commit zero or report storage failure |
| `VERSION` | RP2040 F1 / firmware 6.0.0 / TinyUSB 0.21.0 |
| `DASH …` | Validated clock/date/metrics; full field contract in companion guide |
| `HELP` | Command list |

The count formatter handles UINT64_MAX without libc 64-bit formatting. Native tests cover counter wraps/reversals/faults, torn FRAM records, malformed metric packets, stale data, calendar rollover and scanline buffer bounds. ARM image checks inspect boot2 ROM CRC, actual USB descriptors, vector bounds, and RP2040 UF2 family/payload consistency. Those checks do not establish physical optical response or host interoperability.

USB **CAFE:4011** is TinyUSB's development VID/PID, shared by other projects. Use authorized identifiers before commercial distribution. Native HID scrolling needs no companion; CDC dashboard telemetry needs the companion running.
