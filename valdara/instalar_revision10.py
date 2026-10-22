#!/usr/bin/env python3
"""Instalación de las hojas R10, solo cuando estén presentes los PNG y paletas revisados."""
from pathlib import Path
from PIL import Image
import shutil
root=Path(__file__).resolve().parents[1]
for name in ("brendan","may"):
    source=root/f"{name}_walking_144x32.png"
    palette=root/f"{name}.pal"
    if not source.is_file() or not palette.is_file():
        raise SystemExit(f"Falta recurso de revisión 10: {source.name} / {palette.name}. No se ha modificado la ROM.")
    with Image.open(source) as im:
        if im.size!=(144,32) or im.mode!="P":
            raise SystemExit(f"Formato no compatible: {source.name}, {im.size}, {im.mode}")
        if max(im.getdata())>15:
            raise SystemExit(f"Más de 16 índices en {source.name}")
    rows=palette.read_text().splitlines()
    if rows[:3]!=["JASC-PAL","0100","16"] or len(rows)!=19:
        raise SystemExit(f"Paleta inválida: {palette.name}")
    dest=root/"graphics/object_events/pics/people"/name/"walking.png"
    destpal=root/"graphics/object_events/palettes"/f"{name}.pal"
    shutil.copyfile(source,dest)
    shutil.copyfile(palette,destpal)
    print(f"Instalado {name}: 9 frames de 16x32 y paleta de 16 colores")
# Retratos de selección: solo se reemplazan cuando ambos recursos están presentes.
portraits = [root / f"{name}_seleccion_64x64.png" for name in ("brendan", "may")]
if all(p.is_file() for p in portraits):
    for name, source in zip(("brendan", "may"), portraits):
        with Image.open(source) as im:
            if im.size != (64, 64) or im.mode != "P" or max(im.getdata()) > 15:
                raise SystemExit(f"Retrato inválido: {source.name}")
        shutil.copyfile(source, root / "graphics/trainers/front_pics" / f"{name}.png")
        print(f"Retrato instalado: {name}")
else:
    print("ATENCIÓN: selección de personaje conserva retratos originales; faltan ambos PNG de 64x64.")
