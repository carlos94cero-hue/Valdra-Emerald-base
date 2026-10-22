#!/usr/bin/env python3
"""Valdara v2: sustituye píxeles reales en retratos y sprites de mapa.
Prueba de identificación visual, NO arte definitivo.
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
for person in ("brendan","may"):
    gender="male" if person=="brendan" else "female"
    pic=ROOT/f"graphics/trainers/front_pics/{person}.png"
    image=Image.open(pic).convert("RGBA")
    w,h=image.size
    # Insignia visible 'V' en el retrato, sin alterar tamaño ni silueta.
    # Posición relativa centrada sobre el torso.
    d=ImageDraw.Draw(image)
    cx=w//2; cy=int(h*.67)
    tone=(238,194,73,255) if gender=="male" else (116,230,214,255)
    dark=(24,37,59,255)
    for dx,dy in [(-7,-4),(-5,-1),(-3,2),(0,5),(3,2),(5,-1),(7,-4)]:
        d.rectangle((cx+dx-1,cy+dy-1,cx+dx+1,cy+dy+1),fill=dark)
        d.point((cx+dx,cy+dy),fill=tone)
    pal=image.convert("RGB").quantize(colors=15,method=0)
    # Preserve transparent pixels explicitly, reserving palette index zero.
    raw=pal.getpalette()[:45]
    result=Image.new("P",(w,h),0)
    result.putpalette([0,0,0]+raw+[0]*(768-48))
    alpha=image.getchannel("A")
    for y in range(h):
        for x in range(w):
            if alpha.getpixel((x,y))>=128:
                result.putpixel((x,y),pal.getpixel((x,y))+1)
    result.save(pic,transparency=0)
    print("VALDARA INTRO:",pic,w,h)

    walk=ROOT/f"graphics/object_events/pics/people/{person}/walking.png"
    spr=Image.open(walk)
    if spr.mode!="P":
        spr=spr.convert("P",palette=Image.Palette.ADAPTIVE,colors=16)
    # Mantener estructura de fotogramas y paleta propia de Emerald.
    # Un parche de color reconocible en el torso, dentro de cada celda 16x32.
    # La paleta real del overworld se carga desde el archivo JASC separado.
    w,h=spr.size
    cols=w//16; rows=h//32
    assert cols>0 and rows>0 and w%16==0 and h%32==0,(w,h)
    # Elegir índice visible distinto de transparencia, en todas las celdas.
    for row in range(rows):
        for col in range(cols):
            ox=col*16;oy=row*32
            for dx,dy in [(7,15),(8,15),(7,16),(8,16),(7,17),(8,17)]:
                spr.putpixel((ox+dx,oy+dy),12)
    spr.save(walk,transparency=0)
    palette=ROOT/f"graphics/object_events/palettes/{person}.pal"
    lines=palette.read_text().splitlines()
    assert lines[0]=="JASC-PAL" and lines[2]=="16"
    lines[3+12]="238 194 73" if gender=="male" else "116 230 214"
    palette.write_text("\n".join(lines)+"\n")
    print("VALDARA MAP:",walk,w,h,"frames",cols*rows)
print("VALDARA: retratos y walking actualizados. Verificar en partida nueva.")
