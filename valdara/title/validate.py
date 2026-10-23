#!/usr/bin/env python3
"""Validate the native title assets without building or linking a game ROM."""
from pathlib import Path
import hashlib
import struct
import subprocess
import tempfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PNG = ROOT / 'graphics/title_screen/valdara/title.png'

def validate():
    image = Image.open(PNG)
    image.load()
    assert image.mode == 'P' and image.size == (240, 160)
    assert len(image.getpalette()) == 768
    assert image.info.get('transparency') is None
    raw = bytes(image.getdata())
    assert 255 in raw
    assert all(raw[y * 240 + x] != 255 for y in range(140) for x in range(240))
    assert 600 * 64 < 31 * 2048, 'Tiles overlap screenblock 31'
    assert 31 * 2048 + 2048 == 65536
    subprocess.run(['make', '-s', '-C', 'tools/gbagfx'], cwd=ROOT, check=True)
    gfx = ROOT / 'tools/gbagfx/gbagfx'
    with tempfile.TemporaryDirectory(prefix='valdara-title-') as tmp:
        tmp = Path(tmp)
        tiles = tmp / 'title.8bpp'
        compressed = tmp / 'title.8bpp.lz'
        palette = tmp / 'title.gbapal'
        unpacked = tmp / 'unpacked.8bpp'
        for source, target in ((PNG, tiles), (tiles, compressed), (compressed, unpacked), (PNG, palette)):
            subprocess.run([str(gfx), str(source), str(target)], cwd=ROOT, check=True)
        data = tiles.read_bytes()
        assert len(data) == 38400
        assert unpacked.read_bytes() == data
        assert len(palette.read_bytes()) == 512
        decoded = bytearray(240 * 160)
        for ty in range(20):
            for tx in range(30):
                tile = (ty * 30 + tx) * 64
                for y in range(8):
                    start = (ty * 8 + y) * 240 + tx * 8
                    decoded[start:start + 8] = data[tile + y * 8:tile + y * 8 + 8]
        assert bytes(decoded) == raw, 'Tile order differs from preview'
        colors = struct.unpack('<256H', palette.read_bytes())
        original = image.getpalette()
        for i, color in enumerate(colors):
            r, g, b = original[i * 3:i * 3 + 3]
            assert color == ((r >> 3) | ((g >> 3) << 5) | ((b >> 3) << 10))
    print('PASS: exact PNG/tiles round trip; 600 tiles; RGB555 palette; isolated prompt; no VRAM overlap')
    print('PNG SHA256:', hashlib.sha256(PNG.read_bytes()).hexdigest())
    print('No .gba or .elf output was generated.')

if __name__ == '__main__':
    validate()
