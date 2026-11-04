#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. USB CDC console; requires pyserial==3.5."""
import argparse, json, time
import serial
from serial.tools import list_ports
p=argparse.ArgumentParser(description='Desk knob count console')
p.add_argument('command',nargs='?',choices=['status','reset'],default='status')
p.add_argument('--port',help='e.g. /dev/ttyACM0, COM5 or /dev/cu.usbmodem...')
p.add_argument('--list',action='store_true',help='List serial ports and exit')
p.add_argument('--confirm',action='store_true',help='Deliberately clear the retained count')
p.add_argument('--reset',action='store_true',help='Legacy explicit reset flag')
a=p.parse_args()
ports=list(list_ports.comports())
if a.list:
    for device in ports:print(f'{device.device}: {device.description}')
    raise SystemExit(0)
if a.command=='reset' and not a.confirm:p.error('Reset clears the count; add --confirm')
port=a.port
if not port:
    found=[x.device for x in ports if x.vid==0xcafe and x.pid==0x4011]
    if len(found)!=1:p.error('Use --port; expected exactly one desk knob')
    port=found[0]
with serial.Serial(port,115200,timeout=3,write_timeout=3) as s:
    time.sleep(.2);s.reset_input_buffer()
    if a.command=='reset' or a.reset:
        s.write(b'RESET CONFIRM\n');answer=s.readline().decode().strip()
        if answer!='OK RESET':raise SystemExit(answer or 'Reset timed out')
    s.write(b'STATUS\n');line=s.readline().decode().strip()
    if not line:raise SystemExit('No response; check firmware, cable and serial-port permissions')
    data=json.loads(line);print(json.dumps(data,indent=2))
    if not data['storage_ok']:raise SystemExit('Storage is uninitialized or failed; use reset --confirm only to clear it deliberately')
