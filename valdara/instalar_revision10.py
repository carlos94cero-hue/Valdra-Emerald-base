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
        if filename.endswith("_seleccion_64x64.png"):
            with Image.open(src) as portrait:
                rgb = portrait.getpalette()[:48]
                if len(rgb) != 48:
                    raise SystemExit(f"Paleta de retrato incompleta: {filename}")
                pal_lines = ["JASC-PAL", "0100", "16"]
                pal_lines += [f"{rgb[i]} {rgb[i+1]} {rgb[i+2]}" for i in range(0, 48, 3)]
                destpal = root / "graphics/trainers/palettes" / f"{name}.pal"
                jobs.append(("\n".join(pal_lines) + "\n", destpal))
    pal = root / f"{name}.pal"
    if not pal.is_file():
        raise SystemExit(f"Falta paleta {name}.pal. No se instalarán gráficos.")
    lines = pal.read_text().splitlines()
    if lines[:3] != ["JASC-PAL", "0100", "16"] or len(lines) != 19:
        raise SystemExit(f"Paleta inválida: {name}.pal")
    jobs.append((pal, root / "graphics/object_events/palettes" / f"{name}.pal"))

for src, dest in jobs:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(src, str):
        dest.write_text(src)
        print(f"Paleta del retrato instalada: {dest.relative_to(root)}")
    else:
        shutil.copyfile(src, dest)
        print(f"Instalado: {src.name} -> {dest.relative_to(root)}")
print("Valdara R13: selección, movimiento y paletas de retrato instalados.")
