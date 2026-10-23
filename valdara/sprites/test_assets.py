#!/usr/bin/env python3
from pathlib import Path
import hashlib,struct
ROOT=Path(__file__).resolve().parents[2]
EXPECTED={
 'valdara/emerald_arte_20261023/brendan_walking.png':('44d5bf84395d73c7ea7d2ba95f64d90612ff28f1',144,32),
 'valdara/emerald_arte_20261023/brendan_running.png':('779d6d5e08dbb37d96852033f536c4a8b8207063',144,32),
 'valdara/emerald_arte_20261023/may_walking.png':('cf625f9a3d107e3a4542b120a0dc1bb0832cbe82',144,32),
 'valdara/emerald_arte_20261023/may_running.png':('3f734050b1baa25c68e3d118c1780ce917c50659',144,32),
 'valdara/emerald_arte_20261023/brendan_portrait.png':('8a4640ef05f0267f472ca9552ff4778db0f439b9',64,64),
 'valdara/emerald_arte_20261023/may_portrait.png':('63f100c0e33ac389e82cc25ee5fcd75eed1f5ebc',64,64)}
def blob(data): return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def png(path,w,h):
 data=path.read_bytes();assert data[:8]==b'\x89PNG\r\n\x1a\n'
 size=struct.unpack('>I',data[8:12])[0];assert data[12:16]==b'IHDR' and size==13
 iw,ih,depth,ctype=struct.unpack('>IIBB',data[16:26])
 assert (iw,ih)==(w,h),(path,iw,ih)
 assert depth==4 and ctype==3,(path,depth,ctype)
 assert b'PLTE' in data and b'tRNS' in data,path
 return data
for p,(sha,w,h) in EXPECTED.items():
 data=png(ROOT/p,w,h);assert blob(data)==sha,(p,blob(data),sha)
pairs=[('brendan','male'),('may','female')]
for who,_ in pairs:
 base=ROOT/f'valdara/emerald_arte_20261023/{who}_walking.png'
 run=ROOT/f'valdara/emerald_arte_20261023/{who}_running.png'
 assert base.read_bytes()!=run.read_bytes(),who
 assert (ROOT/f'graphics/object_events/pics/people/{who}/walking.png').read_bytes()==base.read_bytes()
 assert (ROOT/f'graphics/object_events/pics/people/{who}/running.png').read_bytes()==run.read_bytes()
 assert (ROOT/f'graphics/trainers/front_pics/{who}.png').read_bytes()==(ROOT/f'valdara/emerald_arte_20261023/{who}_portrait.png').read_bytes()
 for pal in [ROOT/f'graphics/object_events/palettes/{who}.pal',ROOT/f'graphics/object_events/palettes/{who}_reflection.pal',ROOT/f'graphics/trainers/palettes/{who}.pal']:
  lines=pal.read_text().splitlines();assert lines[:3]==['JASC-PAL','0100','16'] and len(lines[3:])==16,pal
print('PASS: 2 protagonistas; caminar/correr distintos; 9 frames; 16x32; retratos 64x64')
print('PASS: assets aprobados == recursos reales del juego; paletas GBA de 16 colores')
print('PASS: no ROM requerida para esta validación')
