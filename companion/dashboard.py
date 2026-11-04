#!/usr/bin/env python3
"""Send local computer metrics to Desk Knob over USB CDC. No network use."""
# SPDX-License-Identifier: MIT
import argparse
from datetime import datetime
import json
import math
import sys
import time


def tenths(percent):
    value = float(percent)
    if not math.isfinite(value):
        raise ValueError("Metric is not finite")
    return min(1000, max(0, round(value * 10)))


def sample(metrics, now=None):
    now = now or datetime.now()
    cpu = tenths(metrics.cpu_percent(interval=None))
    ram = tenths(metrics.virtual_memory().percent)
    battery = metrics.sensors_battery()
    bat = -1 if battery is None else min(100, max(0, round(battery.percent)))
    ac = int(battery.power_plugged) if battery is not None else 0
    return f"DASH {now:%H:%M:%S %Y-%m-%d} {cpu} {ram} {bat} {ac}\n".encode("ascii")


def identify(port):
    # The development VID/PID is shared by other TinyUSB examples. Match our
    # application identity before transmitting any telemetry, even for --port.
    port.reset_input_buffer()
    port.write(b"\nSTATUS\n")
    deadline = time.monotonic() + 2
    for _ in range(20):
        if time.monotonic() >= deadline:
            break
        line = port.readline(512)
        try:
            status = json.loads(line)
        except (ValueError, UnicodeError):
            continue
        if isinstance(status, dict):
            return status.get("device") == "desk-fidget-counter" and status.get("protocol") == 1
    return False


def connect(serial, list_ports, requested=None):
    names = [requested] if requested else [p.device for p in list_ports.comports()
                                         if p.vid == 0xCAFE and p.pid == 0x4011]
    matches = []
    for name in names:
        port = None
        try:
            port = serial.Serial(name, 115200, timeout=.15, write_timeout=1)
            if identify(port):
                matches.append(port)
                port = None
        except (serial.SerialException, OSError):
            pass
        finally:
            if port is not None:
                port.close()
    if len(matches) != 1:
        for port in matches:
            port.close()
        if len(matches) > 1:
            raise RuntimeError("Multiple Desk Knobs found; select one with --port")
        raise OSError("Desk Knob not found; check USB, firmware and serial-port permissions")
    return matches[0]


def run(args):
    import psutil
    if args.sample:
        psutil.cpu_percent(interval=.2)
        sys.stdout.buffer.write(sample(psutil))
        return
    import serial
    from serial.tools import list_ports
    psutil.cpu_percent(interval=None)  # Prime the first CPU interval.
    last_error = None
    while True:
        try:
            with connect(serial, list_ports, args.port) as port:
                print(f"Dashboard connected: {port.port}", file=sys.stderr)
                last_error = None
                heartbeat = time.monotonic()
                while True:
                    started = time.monotonic()
                    port.write(sample(psutil))
                    # Confirm application identity/liveness periodically. This
                    # also reads errors instead of filling the CDC receive FIFO.
                    if started - heartbeat >= 5:
                        if not identify(port):
                            raise OSError("Dashboard handshake lost")
                        heartbeat = started
                    if args.once:
                        return
                    time.sleep(max(0, 1 - (time.monotonic() - started)))
        except (serial.SerialException, OSError) as error:
            if args.once:
                raise
            if str(error) != last_error:
                print(str(error) + "; retrying every 2 seconds", file=sys.stderr)
                last_error = str(error)
            time.sleep(2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", help="Explicit CDC port, e.g. /dev/cu.usbmodem… or COM5")
    parser.add_argument("--once", action="store_true", help="Send one update and exit")
    parser.add_argument("--sample", action="store_true", help="Print local metrics without opening USB")
    args = parser.parse_args()
    try:
        run(args)
    except KeyboardInterrupt:
        pass
    except (ImportError, OSError, RuntimeError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
