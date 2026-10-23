from pathlib import Path
from PIL import Image
import hashlib,json,struct
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
checks={}
for who in ('brendan','may'):
 for action in ('walking','running'):
  p=root/f'graphics/object_events/pics/people/{who}/{action}.png'
  expected=pack(Image.open(p),16,32)
  # Current pret builds generate converted graphics under build/assets.
  converted=root/'build/assets'/p.relative_to(root).with_suffix('.4bpp')
  if not converted.is_file():
   candidates=[v for v in (root/'build').rglob(action+'.4bpp') if who in v.parts]
   assert len(candidates)==1,(who,action,'converted asset not found',candidates)
   converted=candidates[0]
  actual=converted.read_bytes()
  assert actual==expected,(who,action,'tile-order mismatch')
  offset=d.find(expected);assert offset>=0,(who,action,'missing from ROM')
  checks[who+'_'+action]={'sha256':hashlib.sha256(actual).hexdigest(),'rom_offset':hex(offset),'bytes':len(actual)}
checks['rom_sha256']=hashlib.sha256(d).hexdigest();checks['rom_bytes']=len(d)
(root/'dist/compiled_validation.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
