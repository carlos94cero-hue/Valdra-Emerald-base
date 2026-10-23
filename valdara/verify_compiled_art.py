from pathlib import Path
from PIL import Image
import hashlib,json
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
checks={}
for who in ('brendan','may'):
 for action in ('walking','running'):
  p=root/f'graphics/object_events/pics/people/{who}/{action}.png'
  expected=pack(Image.open(p),16,32); actual=p.with_suffix('.4bpp').read_bytes()
  assert actual==expected,(who,action,'tile-order mismatch')
  checks[who+'_'+action]=hashlib.sha256(actual).hexdigest()
rom=root/'pokeemerald.gba';d=rom.read_bytes()
assert len(d)>=1024*1024 and len(d)<=32*1024*1024
assert d[0xB2]==0x96 and d[0xBD]==(-sum(d[0xA0:0xBD])-0x19)&255
checks['rom_sha256']=hashlib.sha256(d).hexdigest();checks['rom_bytes']=len(d)
(root/'dist/compiled_validation.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
