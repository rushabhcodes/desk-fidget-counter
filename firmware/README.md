# Firmware 2.0.0 / PCB Rev B

Included [BIN](build/desk-knob.bin) and [HEX](build/desk-knob.hex) files target STM32F072CBT6 at **0x08000000**. Use these with the Rev B optical board and screen; Rev A magnetic hardware needs its earlier tagged firmware.

## Build and flash

```sh
bash scripts/test-firmware.sh
bash firmware/bootstrap.sh
python3 validation/check-firmware-image.py
```

The bootstrap script pins TinyUSB 0.21.0 and the CMSIS dependencies to recorded commits. Install an ARM embedded GCC/newlib toolchain and Make. It can also use `make -C firmware TOOLCHAIN=/path/to/arm-none-eabi- TINYUSB=/path/to/tinyusb`.

J4 is a populated **JST-PH 2.0 mm six-pin B6B-PH-K-S** top-entry header. Physical pins 1→6 are **VREF 3V3, SWDIO, SWCLK, NRST, GND, BOOT0**. On the PCB they run from (−5,−20) to (+5,−20) in 2 mm increments. Power the board from USB or its protected battery; VREF is a probe voltage-sense output. Leave BOOT0 unconnected for ordinary SWD programming. Match probe grounds and use 3.3 V logic.

Example with OpenOCD and an ST-Link:

```sh
openocd -f interface/stlink.cfg -f target/stm32f0x.cfg \
  -c 'program firmware/build/desk-knob.hex verify reset exit'
```

STM32CubeProgrammer can flash the HEX through SWD. For ROM USB DFU recovery, connect J4 BOOT0 to VREF, pulse NRST low, release reset and use CubeProgrammer USB DFU at 0x08000000. Disconnect the BOOT0 bridge and reset afterwards. J5 was removed; recovery uses J4 pin 6. J4 is under the removable rotor.

## Counter, display and power behaviour

- PB4/PB5 AF1 feed **TIM3 encoder mode 3**. Both edges of both channels are counted, with approximately 3.3 µs input filters. A 48-slot ring produces **192 edges/revolution**. A 16-bit hardware timer continues collecting edges while display rows or FRAM writes run.
- Signed timer deltas unwrap across 65535/0. Completed ±192 displacement increments the unsigned 64-bit count, with partial reversal cancelled algebraically. Every six edges produces one USB wheel unit, giving 32 units/revolution.
- Samples are serviced at a 2 ms target interval. Invalid storage, low battery, a sample gap over 20 ms or a delta over 48 edges discards partial progress and queued scrolling. This avoids guessed motion after faults. Measure the usable speed envelope in the prototype.
- PA0 reads the **left G12AH toggle** with 20 ms debounce. USB detach, suspend or toggle-off clears queued wheel data. Counting continues on battery and with scrolling off. The internal PA1 service button resets after a three-second hold; USB `RESET CONFIRM` is the normal assembled-device reset.
- I2C1 PB6/PB7 serves FRAM at 0x50. Each completed turn updates alternating 32-byte records at addresses 0/64, with sequence, 64-bit count, CRC32 and a commit marker written last. Saves are read back. Unknown initial FRAM requires deliberate reset/initialization. Rev A journal records remain compatible.
- SPI2 PB13/PB15 uses mode 0 at 12 MHz. PB10 reset, PB11 backlight, PA8 CS and PB14 DC control the **GC9A01**. Initialization and sleep-out waits are nonblocking. Each task sends one 480-byte RGB565 scanline; there is no full framebuffer. UI refreshes use a coherent snapshot of count, voltage and status. A bounded transport failure blanks the screen while USB/counting continue.
- The module is physically rotated 90° with its tab to +X; MADCTL 0x68 matches this mounting. Confirm displayed orientation and colours on the real module.
- The screen shows battery voltage directly, charge state, scroll toggle and USB readiness. `RESET VIA USB` indicates invalid/uninitialized storage. Battery below 3.45 V for three 100 ms readings stops motion acceptance. The protected cell provides a separate final undervoltage cutoff.
- BQ24074 starts at USB100, switches to USB500 after configuration, and enters suspend input mode when USB sleeps. Hardware pulldowns enforce the initial mode. A pouch NTC plus firmware CE gate permits charging only inside the conservative 450–1300 mV TS range.

The timer-running and LCD-transport fields report digital configuration/transport state. There is no MISO or optical amplitude feedback: they cannot detect an unplugged display, blocked optical path, translucent skirt, dirt or a missing channel. Physical contrast and exact 192-edge counts must be verified with a logic analyser.

## USB console

CDC commands end with a newline. Install `pyserial==3.5` with `python -m pip install pyserial==3.5`. PySerial helper: `python scripts/count.py --list`, then `python scripts/count.py --port /dev/ttyACM0 status` or `... reset --confirm`.

| Command | Response |
|---|---|
| `COUNT` / `STATUS` | JSON: turns, progress, storage_ok, encoder_timer_running, scroll_on, battery_mv, low_battery, rejected, lcd_transport_ok, charger_mode |
| `RESET CONFIRM` | Commits zero or returns a storage error |
| `VERSION` | Rev B / firmware 2.0.0 / TinyUSB 0.21.0 |
| `HELP` | Available commands |

Total formatting handles the full 64-bit range without optional libc printf support. The HID interface is a standard relative mouse wheel; CDC supplies count/reset access. Development USB VID/PID are **CAFE:4011**; obtain authorized production identifiers before commercial distribution. Physical USB electrical and host interoperability tests remain outstanding.
