#!/usr/bin/env python3
"""Thorough no-ROM checks for Valdara's active native Emerald species tables."""
from pathlib import Path
from PIL import Image
from collections import Counter
import json, re, hashlib, subprocess, sys, unicodedata

ROOT=Path(__file__).resolve().parents[2]
CAT=ROOT/'valdara/species/catalog_250.json'
REPORT=ROOT/'valdara/species/native_validation.json'
STATS=['baseHP','baseAttack','baseDefense','baseSpAttack','baseSpDefense','baseSpeed']
FIELDS=['hp','attack','defense','sp_attack','sp_defense','speed']

def block(src,slot):
    m=re.search(r'(?m)^\s*\[SPECIES_'+re.escape(slot)+r'\]\s*=\s*\{',src)
    assert m,slot
    i=m.end()-1;depth=0
    for k in range(i,len(src)):
        if src[k]=='{':depth+=1
        if src[k]=='}':
            depth-=1
            if not depth:return src[i:k+1]
    assert False,'unbalanced '+slot

def test():
    before={str(p):p.stat().st_size for p in ROOT.rglob('*.gba')}
    data=json.loads(CAT.read_text()); info=json.loads(REPORT.read_text())
    entries=data['entries'];assert len(entries)==250
    source=(ROOT/'include/constants/species.h').read_text()
    idmap={int(v):name for name,v in re.findall(r'^#define SPECIES_(\w+)\s+(\d+)\s*$',source,re.M) if 1<=int(v)<=250}
    assert len(idmap)==250
    alias=(ROOT/'include/constants/valdara_species.h').read_text()
    names=(ROOT/'src/data/text/species_names.h').read_text()
    stats=(ROOT/'src/data/pokemon/species_info.h').read_text()
    evolved=(ROOT/'src/data/pokemon/evolution.h').read_text()
    icon_src=(ROOT/'src/pokemon_icon.c').read_text()
    front=(ROOT/'src/data/pokemon_graphics/front_pic_coordinates.h').read_text()
    back=(ROOT/'src/data/pokemon_graphics/back_pic_coordinates.h').read_text()
    ability_specs=0;stats_count=0; art_count=0; exact_type=0; type_pending=0
    for e in entries:
        i=e['number'];slot=idmap[i]; n=e['gba_name'].upper()
        assert 1<=i<=250 and len(n)<=10,(i,n)
        assert re.search(r'\[SPECIES_'+slot+r'\]\s*=\s*_\("'+re.escape(n)+r'"\)',names), (i,n)
        assert f'#define SPECIES_VALDARA_{i:03d} SPECIES_{slot}' in alias
        b=block(stats,slot)
        if e['stat']:
            vals={}
            for attr,key in zip(STATS,FIELDS):
                match=re.search(r'\.'+attr+r'\s*=\s*(\d+)',b)
                assert match,(i,attr)
                vals[key]=int(match.group(1))
                assert vals[key]==e['stat'][key],(i,attr,vals[key],e['stat'][key])
            assert sum(vals.values())==e['stat']['total']
            stats_count+=1
        if e['engine_type_tokens']:
            target=e['engine_type_tokens'];want=target if len(target)==2 else target*2
            assert re.search(r'\.types\s*=\s*\{\s*'+want[0]+r'\s*,\s*'+want[1]+r'\s*\}',b),(i,want)
            exact_type+=1
        else:type_pending+=1
        ability_specs+=len(e['ability_spec'])
        if e['art_slug']:
            art_count+=1
            path=ROOT/'graphics/pokemon'/slot.lower();source_path=ROOT/'graphics/valdara_nevarios'/e['art_slug']
            for f, size in [('front.png',(64,64)),('back.png',(64,64)),('anim_front.png',(64,128)),('icon.png',(32,64))]:
                img=Image.open(path/f);assert img.mode=='P' and img.size==size
                assert max(img.getdata())<=15,(i,f)
                assert (source_path/f).is_file()
                if f!='icon.png':assert (path/f).read_bytes()==(source_path/f).read_bytes()
            assert (path/'normal.pal').read_bytes()==(source_path/'normal.pal').read_bytes()
            assert re.search(r'\[SPECIES_'+slot+r'\]\s*=\s*[012]\s*,',icon_src[icon_src.index('const u8 gMonIconPaletteIndices[]'):])
            assert f'[SPECIES_{slot}]' in front and f'[SPECIES_{slot}]' in back
    approved_simple=[x for x in data['evolutions'] if x['status']=='APROBADO' and re.fullmatch(r'Nivel\s+\d+',x['condition'],re.I)]
    assert len(approved_simple)==2
    assert all(f'[SPECIES_{idmap[i]}]' in evolved for i in range(1,251))
    # No duplicates after removing vanilla evolution rules; all native 1..250 entries unique.
    for i in range(1,251):
        assert len(re.findall(r'^\s*\[SPECIES_'+idmap[i]+r'\]\s*=',evolved,re.M))==1,(i,idmap[i])
    # Approved 690-BST finals must survive unchanged in active native game table.
    for i in [7,8,9,10,11,12]:
        assert entries[i-1]['stat']['total']==690
    assert info['approved_6_stats_active']==stats_count
    assert info['original_graphics_active']==art_count==11
    assert info['names_active']==250 and info['types_active_exact_supported']==exact_type
    assert all(e['source_name'] not in (e['gba_name'],) for e in entries if e['number'] in (159,160,161))
    assert ability_specs>=18
    assert before=={str(p):p.stat().st_size for p in ROOT.rglob('*.gba')}
    # Conservative asset/build validation only. No emulator or ROM is built.
    checks={'registered_names':250,'six_stat_profiles_active':stats_count,'original_art_active':art_count,
      'type_pairs_exact':exact_type,'type_unavailable_or_ambiguous':type_pending,
      'preserved_ability_specs':ability_specs,'supported_evolutions_active':len(approved_simple),
      'pending_species_original_art':250-art_count,'rom_created':False,'status':'PASS static native table tests'}
    (ROOT/'valdara/species/test_results.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
    print('PASS',checks)
    return checks

if __name__=='__main__':test()