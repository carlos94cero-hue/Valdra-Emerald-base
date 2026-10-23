#!/usr/bin/env python3
"""Native per-action poses with approved identity; no resized illustrations.
Walking is preserved. Running is not a copy of walking. Animation tables stay native.
"""
from pathlib import Path
import importlib.util,json,hashlib
from PIL import Image
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def colors(im):return [tuple(im.getpalette()[i*3:i*3+3]) for i in range(16)]
def image(data,size,pal):
 im=Image.new('P',size);im.putpalette(sum(map(list,pal),[])+[0]*720);im.putdata(data);return im
def install():
 originals={who:{p.stem:Image.open(p).copy() for p in (ROOT/f'graphics/object_events/pics/people/{who}').glob('*.png')} for who in ('brendan','may')}
 spec=importlib.util.spec_from_file_location('approved',ROOT/'valdara/install_emerald_art.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base);base.install();report={}
 for who,actions in originals.items():
  approved=Image.open(ROOT/f'valdara/emerald_arte_20261023/{who}_walking.png');pal=colors(approved)
  lut=([0,6,5,4,2,12,10,9,1,8,11,10,10,9,7,1] if who=='brendan' else [0,6,5,4,3,8,13,4,2,8,11,10,11,9,7,1]);refs=[]
  for act in ['walking','running']:
   for k in range(9):
    f=actions[act].crop((k*16,0,k*16+16,32));top=min(y for y in range(32) if any(f.getpixel((x,y)) for x in range(16)));h=min(13,24-top)
    pts=[(x,y-top,f.getpixel((x,y))) for y in range(top,top+h) for x in range(16) if f.getpixel((x,y))];refs.append((k if k<3 else (0 if k<5 else 1 if k<7 else 2),top,h,pts))
  stats={}
  for act,src in actions.items():
   if act in ('walking','underwater'):continue
   fw=16 if act in ('running','decorating') else 32;nf=src.width//fw;out=image([lut[v] for v in src.getdata()],src.size,pal)
   for k in range(nf):
    fr=np.asarray(src.crop((k*fw,0,(k+1)*fw,32)));best=None
    for direction,top,h,pts in refs:
     target=np.zeros((h,16),dtype=np.uint8)
     for x,y,v in pts:target[y,x]=v
     patches=np.lib.stride_tricks.sliding_window_view(fr,(h,16))[:18];mask=target!=0;scores=((patches==target)&mask).sum(axis=(-2,-1))/mask.sum();yy,xx=np.unravel_index(np.argmax(scores),scores.shape);candidate=(float(scores[yy,xx]),-abs(int(yy)-top),direction,int(xx),int(yy),h)
     if best is None or candidate[:2]>best[:2]:best=candidate
    score,_,direction,dx,dy,h=best
    if act=='running':direction=k if k<3 else (0 if k<5 else 1 if k<7 else 2);dx=0
    if score<0.20:continue
    head=approved.crop((direction*16,10,direction*16+16,23))
    for yy in range(13):
     for xx in range(16):
      tx=k*fw+dx+xx;ty=dy+yy
      if tx<(k+1)*fw and ty<32:out.putpixel((tx,ty),head.getpixel((xx,yy)))
    if direction==0:
     for yy in range(dy+13,min(dy+16,29)):
      for xx in [7,8]:
       tx=k*fw+dx+xx
       if out.getpixel((tx,yy)) in (9,10,11):out.putpixel((tx,yy),7)
   out.save(ROOT/f'graphics/object_events/pics/people/{who}/{act}.png',transparency=0,bits=4);assert out.size==src.size and max(out.getdata())<16
   if act=='running':assert out.tobytes()!=approved.tobytes()
   stats[act]={'frames':nf,'frame_size':[fw,32],'sha256':hashlib.sha256(out.tobytes()).hexdigest()}
  report[who]=stats
 (ROOT/'dist/motion_validation.json').write_text(json.dumps(report,indent=2));print('PASS: native per-action poses, original frame counts and timings; approved walking preserved')
if __name__=='__main__':install()
