#!/usr/bin/env python3
"""Valdara: prueba de personajes clásicos en selección y mapa.
Conserva el pixel art original y sus animaciones; aplica una paleta Valdara.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = [
    ("graphics/object_events/pics/people/brendan/walking.png", "male"),
    ("graphics/object_events/pics/people/may/walking.png", "female"),
    ("graphics/trainers/front_pics/brendan.png", "male"),
    ("graphics/trainers/front_pics/may.png", "female"),
]
def transform(r,g,b,gender):
    # Mantener luces, sombras y líneas originales, variando sutilmente ropa.
    if b > r*1.15 and b > g*1.08:
        return (max(0,int(r*.78)), min(255,int(g*1.05)), min(255,int(b*1.07)))
    if gender=="female" and r > g*1.38 and r > b*1.2 and r>75:
        return (min(255,int(r*.80)), min(255,int(g*.92)), min(255,int(b*1.25)))
    if gender=="male" and g > r*1.2 and g > b*1.1 and g>65:
        return (int(r*.8), int(g*.86), min(255,int(b*1.25)))
    return (r,g,b)
for relative,gender in ASSETS:
    path=ROOT/relative
    image=Image.open(path)
    if image.mode!="P":
        image=image.convert("P",palette=Image.Palette.ADAPTIVE,colors=16)
    pal=image.getpalette() or []
    colors=pal[:48]+[0]*max(0,48-len(pal))
    new=[]
    for i in range(16):
        rgb=tuple(colors[3*i:3*i+3])
        new.extend(transform(*rgb,gender))
    image.putpalette(new+[0]*(768-len(new)))
    image.save(path,transparency=image.info.get("transparency",0))
    print("Valdara:",relative,image.size)
print("Selección de personaje: sprites de entrenador modificados; mapa: walking modificado.")
