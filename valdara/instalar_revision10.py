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
# Retratos provisionales coherentes con los sprites de movimiento.
# Se obtienen del primer frame frontal, sin introducir arte externo sin validar.
for name in ("brendan", "may"):
    walking = root / "graphics/object_events/pics/people" / name / "walking.png"
    with Image.open(walking) as source:
        frame = source.crop((0, 0, 16, 32))
        portrait = Image.new("P", (64, 64), 0)
        portrait.putpalette(source.getpalette())
        enlarged = frame.resize((32, 64), Image.NEAREST)
        portrait.paste(enlarged, (16, 0))
        portrait.save(root / "graphics/trainers/front_pics" / f"{name}.png", transparency=0)
    print(f"Retrato provisional instalado: {name} (64x64)")
print("AVISO: retratos provisionales; no son ilustraciones finales aprobadas.")
