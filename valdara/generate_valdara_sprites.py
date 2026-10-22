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
 """Dibujo por píxeles con contornos, sombras y silueta de entrenador GBA."""
 female=gender=="female"
 def px(x,y,color):
  put(im,(ox+x*scale,oy+y*scale,ox+(x+1)*scale-1,oy+(y+1)*scale-1),color)
 def rect(x1,y1,x2,y2,color):
  for y in range(y1,y2+1):
   for x in range(x1,x2+1):px(x,y,color)
 # Silueta compacta de 16x32: gorra curvada, cabello, cuello y mochila.
 for y,x1,x2 in [(2,6,9),(3,4,11),(4,3,12),(5,3,12),(6,4,11),
                 (7,4,11),(8,4,11),(9,5,10),(10,5,10),(11,6,9)]:
  rect(x1,y,x2,y,1)
 rect(4,5,11,9,2)
 if view!="back":rect(5,6,10,10,5)
 else:rect(4,6,11,10,2)
 if female:
  rect(3,7,4,12,2);rect(11,7,12,12,2)
  px(3,11,3);px(12,12,3)
 else:
  px(4,8,3);px(11,8,3)
 # Gorra con visera, insignia y dos niveles de sombra
 cap=14 if female else 8
 light=15 if female else 10
 rect(4,3,11,4,cap)
 rect(5,2,10,2,light)
 rect(3,5,12,5,cap)
 rect(4,5,6,5,light)
 px(8,3,11);px(9,3,7)
 if view=="front":
  px(6,8,1);px(9,8,1);px(7,10,4)
 elif view=="left":px(5,8,1)
 elif view=="right":px(10,8,1)
 # Cuello, chaqueta, mochila y correa diagonal
 rect(6,11,9,12,4)
 rect(4,13,11,21,1)
 rect(5,13,10,20,14 if female else 8)
 rect(6,13,9,19,7)
 for y in range(14,20):px(5+(y-14)//3,y,11)
 rect(7,16,8,18,11)
 if view=="back":
  rect(5,14,10,20,2)
  rect(6,15,9,19,3)
  px(7,16,11);px(8,16,11)
 # Brazos con puños, pose asimétrica en la marcha
 left=1 if step==1 else 0
 right=1 if step==2 else 0
 rect(2,14+left,3,19+left,1)
 rect(12,14+right,13,19+right,1)
 rect(3,15+left,3,18+left,14 if female else 9)
 rect(12,15+right,12,18+right,14 if female else 9)
 rect(2,20+left,3,21+left,5)
 rect(12,20+right,13,21+right,5)
 # Cinturón, pantalón, piernas alternadas y botas
 rect(5,21,10,22,2)
 rect(5,23,7,26+left,8)
 rect(9,23,11,26+right,8)
 rect(5,27+left,7,29+left,3)
 rect(9,27+right,11,29+right,3)
 rect(4,29+left,7,30+left,1)
 rect(9,29+right,12,30+right,1)
 px(5,29+left,9);px(10,29+right,9)
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
