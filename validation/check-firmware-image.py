#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Inspect the actual linked image and its USB descriptors."""
from pathlib import Path
import argparse, json, struct, subprocess
p=argparse.ArgumentParser();p.add_argument('--nm',default='arm-none-eabi-nm');a=p.parse_args()
root=Path(__file__).resolve().parents[1]
image=(root/'firmware/build/desk-knob.bin').read_bytes()
syms={}
for line in subprocess.check_output([a.nm,'-S',str(root/'firmware/build/desk-knob.elf')],text=True).splitlines():
    f=line.split()
    if len(f)==4:syms[f[3]]=(int(f[0],16),int(f[1],16))
def symbol(name):
    address,size=syms[name];i=address-0x08000000
    return image[i:i+size]
sp,reset=struct.unpack_from('<II',image)
assert sp==0x20004000 and reset&1 and 0x08000000<=reset<0x08000000+len(image)
assert len(image)<=128*1024
cfg=symbol('config');dev=symbol('device');hid=symbol('hid_report')
assert len(dev)==18 and dev[0:2]==bytes([18,1])
assert struct.unpack_from('<HH',dev,8)==(0xcafe,0x4011)
assert struct.unpack_from('<H',cfg,2)[0]==len(cfg)==100
assert cfg[4]==3 and cfg[7]==0xc0 and cfg[8]==250
interfaces=[];endpoints=[];i=0
while i<len(cfg):
    n,t=cfg[i:i+2];assert n>=2
    block=cfg[i:i+n]
    if t==4:interfaces.append((block[2],block[5]))
    if t==5:endpoints.append(block[2])
    i+=n
assert i==len(cfg) and interfaces==[(0,2),(1,10),(2,3)]
assert set(endpoints)=={0x81,0x02,0x82,0x83} and len(endpoints)==4
assert b'\x09\x38' in hid, 'HID Wheel usage must exist'
assert b'\x81\x06' in hid, 'Relative motion input must exist'
irq=struct.unpack_from('<I',image,47*4)[0]
assert irq&1 and 0x08000000<=irq<0x08000000+len(image)
print(json.dumps({'image_bytes':len(image),'stack_top':hex(sp),'reset_vector':hex(reset),'usb_interfaces':interfaces,'usb_endpoints':[hex(x) for x in endpoints],'usb_configuration_bytes':len(cfg),'requested_usb_mA':cfg[8]*2,'hid_report_bytes':len(hid)},indent=2))
