from pathlib import Path
from PIL import Image
import hashlib,json,subprocess
root=Path(__file__).resolve().parents[1]
def pack(im,fw,fh):
 p=list(im.getdata());w,h=im.size;out=bytearray()
 for fy in range(0,h,fh):
  for fx in range(0,w,fw):
   for ty in range(0,fh,8):
    for tx in range(0,fw,8):
     for y in range(8):
      for x in range(0,8,2):
       off=(fy+ty+y)*w+fx+tx+x;out.append(p[off]|p[off+1]<<4)
 return bytes(out)
rom=root/'pokeemerald.gba';d=rom.read_bytes()
assert 1024*1024<=len(d)<=32*1024*1024
assert d[0xB2]==0x96 and d[0xBD]==((-sum(d[0xA0:0xBD])-0x19)&255)
symbols={}
for line in subprocess.check_output(['arm-none-eabi-nm',str(root/'pokeemerald.elf')],text=True).splitlines():
 parts=line.split()
 if len(parts)==3:
  try:symbols[parts[2]]=int(parts[0],16)
  except ValueError:pass
checks={}
for who in ('brendan','may'):
 for action,suffix in (('walking','Normal'),('running','Running')):
  p=root/f'graphics/object_events/pics/people/{who}/{action}.png'
  expected=pack(Image.open(p),16,32)
  symbol='gObjectEventPic_'+who.capitalize()+suffix
  assert symbol in symbols,('missing symbol',symbol)
  offset=symbols[symbol]-0x08000000
  actual=d[offset:offset+len(expected)]
  assert actual==expected,(who,action,'ROM data differs from approved PNG',hex(offset))
  checks[who+'_'+action]={'symbol':symbol,'sha256':hashlib.sha256(actual).hexdigest(),'rom_offset':hex(offset),'bytes':len(actual)}
checks['rom_sha256']=hashlib.sha256(d).hexdigest();checks['rom_bytes']=len(d)
(root/'dist/compiled_validation.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
