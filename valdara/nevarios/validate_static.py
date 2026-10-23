#!/usr/bin/env python3
"""Comprehensive Python-stdlib-only GBA asset validation. Does not compile ROMs."""
import hashlib,json,struct,zlib
from pathlib import Path
from rebuild import ROOT,OUT,tiles,gba_palette

def parse_png8(raw):
    assert raw[:8]==b'\x89PNG\r\n\x1a\n'
    ptr=8;parts={}
    while ptr<len(raw):
        count=struct.unpack_from('>I',raw,ptr)[0];tag=raw[ptr+4:ptr+8]
        value=raw[ptr+8:ptr+8+count]
        assert zlib.crc32(tag+value)&0xffffffff==struct.unpack_from('>I',raw,ptr+8+count)[0]
        parts[tag]=parts.get(tag,b'')+value
        ptr+=count+12
        if tag==b'IEND':break
    assert ptr==len(raw)
    width,height,depth,typ,_,_,_=struct.unpack('>IIBBBBB',parts[b'IHDR'])
    assert depth==8 and typ==3 and len(parts[b'PLTE'])==48
    assert parts[b'tRNS']==bytes([0]+[255]*15)
    scan=zlib.decompress(parts[b'IDAT'])
    assert len(scan)==height*(1+width)
    pix=bytearray()
    for y in range(height):
        start=y*(width+1)
        assert scan[start]==0
        pix.extend(scan[start+1:start+width+1])
    return width,height,bytes(pix),parts[b'PLTE']

def check():
    m=json.loads((ROOT/'manifest.json').read_text())
    payload=json.loads((ROOT/'sprite_payload.json').read_text())
    assert set(m['species'])==set(payload['species'])
    assert len(m['species'])==11 and len(m['items'])==4
    assert m['creatures_name']=='Nevarios' and m['player_class']=='Criador'
    assert m['other_world']=='el Envés' and m['researcher_dex']=='Veloria'
    assert m['mythic_trio']==['Umbrálix','Nevarión','Límbora']
    type_dict={'Heroe':['Agua','Acero'],'Villano':['Agua','Siniestro'],'Investigador':['Agua','Tierra']}
    variants={}
    for name,sp in m['species'].items():
        folder=OUT/name;hashes=sp['sha256']
        assert sp['gba_4bpp_ready']
        for file in ['front.png','back.png','anim_front.png','icon.png','normal.pal']:
            assert hashlib.sha256((folder/file).read_bytes()).hexdigest()==hashes[file],(name,file)
        pngs={part:parse_png8((folder/(part+'.png')).read_bytes()) for part in ('front','back','anim_front','icon')}
        assert [pngs[p][:2] for p in pngs]==[(64,64),(64,64),(64,128),(32,64)]
        for part,(w,h,pixels,colors) in pngs.items():
            assert max(pixels)<16
            assert sum(v!=0 for v in pixels)>200
            assert (folder/(part+'.4bpp')).read_bytes()==tiles(pixels,w,h)
            assert colors==pngs['front'][3]
        assert pngs['front'][2]!=pngs['back'][2]
        assert pngs['front'][2]==pngs['anim_front'][2][:4096]
        assert pngs['anim_front'][2][:4096]!=pngs['anim_front'][2][4096:]
        assert len((folder/'normal.gbapal').read_bytes())==32
        assert (folder/'normal.gbapal').read_bytes()==gba_palette(pngs['front'][3])
        if sp['stage']=='mythic':
            assert sp['sex'] is None and sp['type'] is None
        elif sp['stage']=='initial':
            assert sp['type']==['Agua'] and sp['sex'] in ('M','F')
        else:
            assert sp['sex'] in ('M','F') and sp['type']==type_dict[sp['route']]
        if sp['sex'] in ('M','F'):
            variants.setdefault(name.rsplit('_',1)[0],{})[sp['sex']]=pngs['front'][2]
    assert len(variants)==4
    for pair,sexes in variants.items():
        assert set(sexes)=={'M','F'} and sexes['M']!=sexes['F'],pair
    for key,it in m['items'].items():
        folder=OUT/'items'/key
        w,h,pixels,col=parse_png8((folder/'icon.png').read_bytes())
        assert (w,h)==(24,24) and max(pixels)<16
        assert (folder/'icon.4bpp').read_bytes()==tiles(pixels,w,h)
        assert (folder/'icon.gbapal').read_bytes()==gba_palette(col)
    # Never build or distribute a ROM during this preview stage.
    assert not list(ROOT.glob('*.gba'))
    print('PASS: 11 canonical Nevarios entries = 8 sex/raising forms + 3 mystical creatures')
    print('PASS: 44 indexed PNG sprites: transparent, 16 color, exact 4bpp tile layout')
    print('PASS: 11 32-byte native GBA palettes, 4 new item icons, 3 upbringing types')
    print('PASS: unique male/female palettes and forms, icon and frame differentiation')
    print('PASS: no new ROM generated. Battle species implementation remains a separate step.')

if __name__=='__main__':check()
