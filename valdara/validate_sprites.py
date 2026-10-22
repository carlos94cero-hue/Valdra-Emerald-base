#!/usr/bin/env python3
"""Preflight para recursos GBA de los protagonistas de Valdara."""
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
for name in ("brendan","may"):
    for rel,expected in (
        (f"graphics/trainers/front_pics/{name}.png",(64,64)),
        (f"graphics/object_events/pics/people/{name}/walking.png",None),
    ):
        p=root/rel
        with Image.open(p) as im:
            if expected and im.size!=expected:
                raise SystemExit(f"{rel}: tamaño {im.size}, esperado {expected}")
            if not expected and (im.width%16 or im.height%32):
                raise SystemExit(f"{rel}: hoja no divisible en 16x32")
            if im.mode!="P":
                raise SystemExit(f"{rel}: requiere PNG indexado, obtenido {im.mode}")
            indices=set(im.getdata())
            if max(indices)>15:
                raise SystemExit(f"{rel}: indice {max(indices)} supera paleta de 16 colores")
            if 0 not in indices:
                raise SystemExit(f"{rel}: falta indice transparente 0")
            print("OK",rel,im.size,len(indices),"indices")
    pal=root/f"graphics/object_events/palettes/{name}.pal"
    lines=pal.read_text().splitlines()
    if lines[:3]!=["JASC-PAL","0100","16"] or len(lines)!=19:
        raise SystemExit(f"{pal}: cabecera o número de colores incorrecto")
    print("OK",pal)
print("Recursos técnicamente validados; pendiente revisión visual y animaciones.")
