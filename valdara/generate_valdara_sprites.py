#!/usr/bin/env python3
"""Genera retratos y sprites de Valdara con una paleta única, indexada y segura."""
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
COLORS=[(0,0,0),(35,33,48),(75,56,62),(134,87,71),(205,145,103),
 (245,197,148),(255,226,185),(247,247,238),(29,58,93),(56,111,166),
 (99,163,205),(225,183,71),(55,99,75),(110,155,105),(141,42,66),(204,70,85)]
PAL=[n for c in COLORS for n in c]+[0]*(768-48)
def canvas(size):
 im=Image.new("P",size,0);im.putpalette(PAL);return im
def put(im,coords,fill):
 ImageDraw.Draw(im).rectangle(coords,fill=fill)
def character(im,ox,oy,gender,view,step=0,scale=1):
 # Pixel art dibujado por capas; silueta centrada, sin fondo.
 def rect(x1,y1,x2,y2,c):
  put(im,(ox+x1*scale,oy+y1*scale,ox+(x2+1)*scale-1,oy+(y2+1)*scale-1),c)
 female=gender=="female"
 # Cabello y gorro; espalda, frontal y perfil.
 rect(4,3,11,10,2)
 rect(5,4,10,10,4 if view!="back" else 2)
 rect(3,3,12,5,14 if female else 8)
 rect(4,2,11,3,15 if female else 9)
 rect(5,1,10,2,2)
 if female:
  rect(3,7,4,13,2);rect(11,7,12,13,2)
 if view=="front":
  rect(6,8,6,8,1);rect(9,8,9,8,1)
 elif view=="left":rect(5,8,5,8,1)
 elif view=="right":rect(10,8,10,8,1)
 # cuello, mochila y chaqueta de viajero
 rect(6,11,9,12,5)
 if view=="back":rect(3,12,12,21,2);rect(4,13,11,19,11)
 rect(4,13,11,22,9 if not female else 14)
 rect(6,13,9,21,7)
 rect(7,15,8,18,11)
 rect(2,14,3,21+(step==1),9 if not female else 14)
 rect(12,14,13,21+(step==2),9 if not female else 14)
 rect(2,22,3,23,5);rect(12,22,13,23,5)
 if female:rect(4,22,11,25,8)
 else:rect(4,22,11,24,8)
 rect(4,25,7,29+(step==1),1)
 rect(9,25,11,29+(step==2),1)
 rect(3,29+(step==1),7,30+(step==1),2)
 rect(9,29+(step==2),12,30+(step==2),2)
def save(im,path):
 path.parent.mkdir(parents=True,exist_ok=True)
 im.save(path,transparency=0)
def palette(path):
 path.write_text("JASC-PAL\n0100\n16\n"+"\n".join(f"{r} {g} {b}" for r,g,b in COLORS)+"\n")
for name,gender in [("brendan","male"),("may","female")]:
 # Retrato: tamaño original 64x64. Dibujado a 2x, centrado y sin fondos.
 portrait=canvas((64,64))
 character(portrait,16,0,gender,"front",0,2)
 # No se usa transparencia indexada para sombrear; índice 0 reservado.
 save(portrait,ROOT/f"graphics/trainers/front_pics/{name}.png")
 # Overworld: cada celda 16x32; se conserva tamaño de hoja original
 original=Image.open(ROOT/f"graphics/object_events/pics/people/{name}/walking.png")
 width,height=original.size
 assert width%16==0 and height%32==0,(name,width,height)
 cols=width//16;rows=height//32
 sheet=canvas((width,height))
 # Emerald walking usa 9 frames: front, back, side (3 por dirección).
 # Las posiciones restantes, si existen, usan el ciclo lateral.
 views=["front","back","left","right"]
 for i in range(cols*rows):
  view=views[min(i//3,3)]
  character(sheet,(i%cols)*16,(i//cols)*32,gender,view,i%3)
 save(sheet,ROOT/f"graphics/object_events/pics/people/{name}/walking.png")
 palette(ROOT/f"graphics/object_events/palettes/{name}.pal")
 print(name,"portrait",portrait.size,"walking",sheet.size,"frames",cols*rows)
print("Sprites Valdara generados: 16 colores, transparencia índice 0.")
