#!/usr/bin/env python3
"""Inspección no destructiva de sprites de Valdara antes de reemplazar recursos."""
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
for character in ("brendan","may"):
    path=root/"graphics/object_events/pics/people"/character/"walking.png"
    with Image.open(path) as im:
        print(f"{character}: {path.relative_to(root)} = {im.width}x{im.height}, mode={im.mode}")
        if im.width != 144 or im.height != 32:
            raise SystemExit(f"Hoja inesperada: {path}")
        if im.mode != "P":
            raise SystemExit(f"Se esperaba imagen indexada: {path}")
        print("9 fotogramas de 16x32 en una tira horizontal.")
print("NOTA: la geometría no demuestra el orden de animación ni la calidad artística.")
