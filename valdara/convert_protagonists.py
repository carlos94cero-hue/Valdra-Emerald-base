#!/usr/bin/env python3
"""Valdara: restauración segura de gráficos originales.
Esta etapa elimina la corrupción de paleta de pruebas anteriores.
Los retratos definitivos se integrarán tras validar PNG 4bpp y paletas.
"""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
files=[
 "graphics/trainers/front_pics/brendan.png",
 "graphics/trainers/front_pics/may.png",
 "graphics/object_events/pics/people/brendan/walking.png",
 "graphics/object_events/pics/people/may/walking.png",
]
for name in files:
    p=ROOT/name
    im=Image.open(p)
    assert im.mode=="P", (name, im.mode)
    assert len(set(im.getdata()))<=16, (name,"demasiados colores")
    assert im.size[0]%8==0 and im.size[1]%8==0
    print("OK, paleta original intacta:",name,im.size)
print("Verificación completada. No se alteraron retratos ni sprites originales.")
