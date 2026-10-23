#!/usr/bin/env python3
"""Restore all Valdara Nevarios battle assets using only the Python standard library.
No ROM, sprite substitutions or species table edits take place here.
"""
from pathlib import Path
import struct,zlib,base64,binascii,json,hashlib
ROOT=Path(__file__).resolve().parent
PAYLOAD=ROOT/'sprite_payload.json'
MANIFEST=ROOT/'manifest.json'
OUT=ROOT/'assets'

def png_chunk(name,data):
    return struct.pack('>I',len(data))+name+data+struct.pack('>I',binascii.crc32(name+data)&0xffffffff)

def indexed_png(width,height,pix,colors):
    assert width%8==0 and height%8==0 and len(pix)==width*height and len(colors)==48
    assert max(pix)<16
    header=struct.pack('>IIBBBBB',width,height,8,3,0,0,0)
    pal=colors
    alpha=bytes([0]+[255]*15)
    lines=b''.join(b'\0'+pix[y*width:(y+1)*width] for y in range(height))
    return (b'\x89PNG\r\n\x1a\n'+png_chunk(b'IHDR',header)+png_chunk(b'PLTE',pal)
            +png_chunk(b'tRNS',alpha)+png_chunk(b'IDAT',zlib.compress(lines,9))
            +png_chunk(b'IEND',b''))

def tiles(data,width,height):
    assert len(data)==width*height and width%8==0 and height%8==0
    out=bytearray()
    for ty in range(0,height,8):
        for tx in range(0,width,8):
            for y in range(8):
                for x in range(0,8,2):
                    at=(ty+y)*width+(tx+x)
                    out.append(data[at]|data[at+1]<<4)
    assert len(out)==width*height//2
    return bytes(out)

def gba_palette(raw):
    out=bytearray()
    for i in range(0,48,3):
        r,g,b=raw[i:i+3]
        out.extend(struct.pack('<H',(r>>3)|((g>>3)<<5)|((b>>3)<<10)))
    assert len(out)==32
    return bytes(out)

def jasc(raw):
    return 'JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,raw[i:i+3])) for i in range(0,48,3))+'\n'

def animation(front):
    assert len(front)==4096
    frame2=b''.join(front[(y+1)*64:(y+2)*64] if y<63 else b'\0'*64 for y in range(64))
    assert frame2!=front
    return front+frame2

def icon(front):
    """Two 32x32 snapshots in one 32x64 Emerald icon sheet."""
    points=[(x,y) for y in range(64) for x in range(64) if front[y*64+x]!=0]
    if not points:raise ValueError('No opaque sprite pixels')
    xx=[p[0] for p in points];yy=[p[1] for p in points]
    x0,x1=min(xx),max(xx);y0,y1=min(yy),max(yy)
    ww=x1-x0+1;hh=y1-y0+1
    s=min(28/ww,29/hh)
    outw=max(1,round(ww*s));outh=max(1,round(hh*s))
    dest=bytearray(32*64)
    for frame in range(2):
        dx=(32-outw)//2;dy=29-outh+32*frame+frame
        for iy in range(outh):
            sy=min(y1,y0+int((iy+.5)*hh/outh))
            for ix in range(outw):
                sx=min(x1,x0+int((ix+.5)*ww/outw))
                dest[(dy+iy)*32+dx+ix]=front[sy*64+sx]
    return bytes(dest)

def write_asset(path,name,pix,size,pal):
    path.mkdir(parents=True,exist_ok=True)
    w,h=size
    (path/(name+'.png')).write_bytes(indexed_png(w,h,pix,pal))
    (path/(name+'.4bpp')).write_bytes(tiles(pix,w,h))

def main():
    data=json.loads(PAYLOAD.read_text())
    m=json.loads(MANIFEST.read_text())
    assert data['format']=='Valdara.Nevarios.4bpp.2026-10-v1'
    assert set(data['species'])==set(m['species']) and set(data['items'])==set(m['items'])
    for name,compressed in data['species'].items():
        raw=zlib.decompress(base64.b85decode(compressed))
        if len(raw)!=8240:raise ValueError(name+' length')
        colors=raw[:48];front=raw[48:4144];back=raw[4144:]
        p=OUT/name
        write_asset(p,'front',front,(64,64),colors)
        write_asset(p,'back',back,(64,64),colors)
        write_asset(p,'anim_front',animation(front),(64,128),colors)
        write_asset(p,'icon',icon(front),(32,64),colors)
        (p/'normal.pal').write_text(jasc(colors))
        (p/'normal.gbapal').write_bytes(gba_palette(colors))
    for name,compressed in data['items'].items():
        raw=zlib.decompress(base64.b85decode(compressed))
        if len(raw)!=624:raise ValueError(name+' length')
        pal=raw[:48];pix=raw[48:]
        p=OUT/'items'/name
        write_asset(p,'icon',pix,(24,24),pal)
        (p/'normal.pal').write_text(jasc(pal))
        (p/'icon.gbapal').write_bytes(gba_palette(pal))
    print('Generated GBA art for',len(data['species']),'Nevarios and',len(data['items']),'items; no ROM')

if __name__=='__main__':main()
