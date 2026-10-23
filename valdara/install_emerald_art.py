#!/usr/bin/env python3
"""Install the approved Valdara protagonists into Emerald source assets."""
from pathlib import Path
from PIL import Image
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'valdara/emerald_arte_20261023'
EXPECTED={
 'brendan_walking.png':'44d5bf84395d73c7ea7d2ba95f64d90612ff28f1',
 'brendan_running.png':'779d6d5e08dbb37d96852033f536c4a8b8207063',
 'may_walking.png':'cf625f9a3d107e3a4542b120a0dc1bb0832cbe82',
 'may_running.png':'3f734050b1baa25c68e3d118c1780ce917c50659',
 'brendan_portrait.png':'8a4640ef05f0267f472ca9552ff4778db0f439b9',
 'may_portrait.png':'63f100c0e33ac389e82cc25ee5fcd75eed1f5ebc'}
def blob(path):
 data=path.read_bytes()
 return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def check(path,size):
 assert blob(path)==EXPECTED[path.name],path
 im=Image.open(path);im.load()
 assert im.mode=='P' and im.size==size,(path,im.mode,im.size)
 assert max(im.getdata())<16 and im.info.get('transparency')==0,path
 return im
def palette(im): return [tuple(im.getpalette()[i:i+3]) for i in range(0,48,3)]
def write_pal(path,colors):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n')
def remap(path,colors,oldpal=None):
 if not path.exists(): return
 im=Image.open(path);im.load();assert im.mode=='P',path
 old=oldpal or [tuple(im.getpalette()[i:i+3]) for i in range(0,48,3)]
 lut=[0]
 for r,g,b in old[1:]:
  lut.append(min(range(1,16),key=lambda k:3*(r-colors[k][0])**2+5*(g-colors[k][1])**2+2*(b-colors[k][2])**2))
 out=Image.new('P',im.size);out.putpalette([v for c in colors for v in c]+[0]*720)
 out.putdata([lut[p] for p in im.getdata()]);out.save(path,transparency=0,bits=4)
def install():
 report={'scope':'walking, distinct running, selection portraits and palette-consistent special actions','characters':{}}
 for who in ('brendan','may'):
  walk=check(ASSETS/f'{who}_walking.png',(144,32))
  run=check(ASSETS/f'{who}_running.png',(144,32))
  portrait=check(ASSETS/f'{who}_portrait.png',(64,64))
  assert walk.tobytes()!=run.tobytes(),(who,'running must differ from walking')
  colors=palette(walk); assert palette(run)==colors,(who,'running palette')
  folder=ROOT/f'graphics/object_events/pics/people/{who}'
  for path in folder.glob('*.png'):
   if path.name not in ('walking.png','running.png','underwater.png'): remap(path,colors)
  walk.save(folder/'walking.png',transparency=0,bits=4)
  run.save(folder/'running.png',transparency=0,bits=4)
  for suffix in ('','_reflection'): write_pal(ROOT/f'graphics/object_events/palettes/{who}{suffix}.pal',colors)
  trainerpal=ROOT/f'graphics/trainers/palettes/{who}.pal'
  lines=trainerpal.read_text().splitlines();oldpal=[tuple(map(int,s.split())) for s in lines[3:19]]
  facecolors=palette(portrait)
  remap(ROOT/f'graphics/trainers/back_pics/{who}.png',facecolors,oldpal)
  portrait.save(ROOT/f'graphics/trainers/front_pics/{who}.png',transparency=0,bits=4)
  write_pal(trainerpal,facecolors)
  report['characters'][who]={'walking_frames':9,'running_frames':9,'frame_size':[16,32],'portrait':[64,64],'colors':16,'running_distinct':True}
 out=ROOT/'dist';out.mkdir(exist_ok=True)
 (out/'asset_validation.json').write_text(json.dumps(report,indent=2))
 print(json.dumps(report,indent=2))
if __name__=='__main__': install()
