#!/usr/bin/env python3
"""Instala sprites R13 sólo cuando los seis recursos estén disponibles y validados."""
from pathlib import Path
from PIL import Image
import shutil

root = Path(__file__).resolve().parents[1]
jobs = []
for name in ("brendan", "may"):
    for filename, dest, size in (
        (f"{name}_walking_144x32.png", root / "graphics/object_events/pics/people" / name / "walking.png", (144, 32)),
        (f"{name}_seleccion_64x64.png", root / "graphics/trainers/front_pics" / f"{name}.png", (64, 64)),
    ):
        src = root / filename
        if not src.is_file():
            raise SystemExit(f"Falta archivo: {filename}. No se instalarán gráficos.")
        with Image.open(src) as im:
            if im.size != size or im.mode != "P" or max(im.getdata()) > 15:
                raise SystemExit(f"PNG incompatible: {filename}: {im.size}, {im.mode}")
        jobs.append((src, dest))
    pal = root / f"{name}.pal"
    if not pal.is_file():
        raise SystemExit(f"Falta paleta {name}.pal. No se instalarán gráficos.")
    lines = pal.read_text().splitlines()
    if lines[:3] != ["JASC-PAL", "0100", "16"] or len(lines) != 19:
        raise SystemExit(f"Paleta inválida: {name}.pal")
    jobs.append((pal, root / "graphics/object_events/palettes" / f"{name}.pal"))

for src, dest in jobs:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    print(f"Instalado: {src.name} -> {dest.relative_to(root)}")
print("Valdara R13: selección y movimiento instalados. Pendiente comprobar aspecto dentro del juego.")
