#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Check RP2040 boot2, vectors, USB and UF2."""
from pathlib import Path
import argparse, binascii, hashlib, json, struct, subprocess
p=argparse.ArgumentParser()
p.add_argument('--nm',default='firmware/.deps/toolchain/bin/arm-none-eabi-nm')
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
image=(root/'firmware/build/desk-knob.bin').read_bytes()
base=0x10000000
syms={}
for line in subprocess.check_output([a.nm,'-S',str(root/'firmware/build/desk-knob.elf')],text=True).splitlines():
    f=line.split()
    if len(f)==4:syms[f[3]]=(int(f[0],16),int(f[1],16))
def symbol(name):
    address,size=syms[name]; i=address-base
    assert 0<=i<len(image) and i+size<=len(image),name
    return image[i:i+size]
def bitrev(n,bits):return int(f'{n:0{bits}b}'[::-1],2)
# Boot ROM CRC follows the Pico SDK pad_checksum algorithm.
crc=bitrev((binascii.crc32(bytes(bitrev(b,8) for b in image[:252]),0)^0xffffffff)&0xffffffff,32)
assert struct.unpack_from('<I',image,252)[0]==crc,'Boot2 ROM CRC'
sp,reset=struct.unpack_from('<II',image,256)
assert 0x20000000<sp<=0x20042000 and sp%8==0
assert reset&1 and base+256<=reset<base+len(image)
assert len(image)<=2*1024*1024
irq=struct.unpack_from('<I',image,256+(16+5)*4)[0] # USBCTRL_IRQ = 5
assert irq&1 and base+256<=irq<base+len(image)
# Pico SDK copies vectors to RAM; TinyUSB installs its shared USB handler at
# dcd_init rather than replacing the default handler in the flash vector table.
assert syms['dcd_rp2040_irq'][1]>0 and syms['irq_add_shared_handler'][1]>0
dcd=(root/'firmware/.deps/tinyusb/src/portable/raspberrypi/rp2040/dcd_rp2040.c').read_text()
assert 'irq_add_shared_handler(USBCTRL_IRQ, dcd_rp2040_irq,' in dcd
cfg=symbol('config');dev=symbol('device');hid=symbol('hid_report')
assert len(dev)==18 and dev[:2]==bytes([18,1])
assert struct.unpack_from('<HH',dev,8)==(0xcafe,0x4011)
assert struct.unpack_from('<H',dev,12)[0]==0x0600
assert struct.unpack_from('<H',cfg,2)[0]==len(cfg)==100
assert cfg[4]==3 and cfg[7]==0x80 and cfg[8]==50
interfaces=[];endpoints=[];i=0
while i<len(cfg):
    n,t=cfg[i:i+2];assert n>=2
    block=cfg[i:i+n]
    if t==4:interfaces.append((block[2],block[5]))
    if t==5:endpoints.append(block[2])
    i+=n
assert i==len(cfg) and interfaces==[(0,2),(1,10),(2,3)]
assert set(endpoints)=={0x81,0x02,0x82,0x83} and len(endpoints)==4
assert bytes([9,56]) in hid and bytes([129,6]) in hid
uf2=(root/'firmware/build/desk-knob.uf2').read_bytes()
assert len(uf2)%512==0
blocks={}
for i in range(0,len(uf2),512):
    b=uf2[i:i+512]
    m0,m1,flags,address,size,index,count,family=struct.unpack_from('<8I',b)
    assert (m0,m1)==(0x0a324655,0x9e5d5157)
    assert struct.unpack_from('<I',b,508)[0]==0x0ab16f30
    assert flags==0x2000 and family==0xe48bff56 and size==256
    assert count==len(uf2)//512 and index not in blocks
    assert address==base+index*256
    blocks[index]=b[32:32+size]
payload=b''.join(blocks[i] for i in range(len(blocks)))
assert payload[:len(image)]==image and set(payload[len(image):])<={0},'UF2 payload matches BIN'
hex_bytes={};upper=0;eof=False
for line in (root/'firmware/build/desk-knob.hex').read_text().splitlines():
    assert line.startswith(':') and not eof
    record=bytes.fromhex(line[1:]);assert sum(record)%256==0
    size,address,kind=record[0],int.from_bytes(record[1:3],'big'),record[3]
    assert len(record)==size+5
    data=record[4:4+size]
    if kind==0:
        for j,value in enumerate(data):
            offset=upper+address+j-base
            assert 0<=offset<len(image) and image[offset]==value
            assert offset not in hex_bytes
            hex_bytes[offset]=value
    elif kind==4:assert size==2;upper=int.from_bytes(data,'big')<<16
    elif kind==5:assert size==4 and base<=int.from_bytes(data,'big')<base+len(image)
    elif kind==1:assert size==0;eof=True
    else:raise AssertionError(('Unexpected Intel HEX record',kind))
assert eof and len(hex_bytes)>len(image)*.95
print(json.dumps({'target':'RP2040 F1 / Winbond W25Q16JV 2MB','image_bytes':len(image),
 'bin_sha256':hashlib.sha256(image).hexdigest(),'boot2_crc32':hex(crc),'boot2_crc_valid':True,
 'vector_address':hex(base+256),'stack_top':hex(sp),'reset_vector':hex(reset),'usb_irq':hex(irq),
 'uf2_blocks':len(blocks),'uf2_family':'0xe48bff56','uf2_matches_bin':True,'hex_data_matches_bin':True,
 'usb_interfaces':interfaces,'usb_endpoints':[hex(x) for x in endpoints],
 'usb_configuration_bytes':len(cfg),'requested_usb_mA':cfg[8]*2,'hid_report_bytes':len(hid)},indent=2))
