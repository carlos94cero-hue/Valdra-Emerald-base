#!/usr/bin/env python3
"""Write Valdara's first 250 regional species to *active* Emerald source tables.

This installs approved names, supported types and exact approved 6-stat profiles
into the existing 001–250 species slots, and installs original graphics for the
11 creatures whose art exists. It does NOT pretend pending art, Fairy types or
unimplemented abilities are battle-ready. No ROM is built or launched.

The original numbered Emerald slot is kept as a stable numeric ID so all of the
engine's icon/front/back/palette tables remain synchronized. Other Hoenn IDs
>250 remain untouched. This repurposes Kanto/Johto data in a development branch
rather than adding 250 to NUM_SPECIES prematurely.
"""
from __future__ import annotations
import json
import re
import hashlib
import shutil
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'valdara/species/catalog_250.json'
REPORT=ROOT/'valdara/species/native_validation.json'
STA=['baseHP','baseAttack','baseDefense','baseSpAttack','baseSpDefense','baseSpeed']
FIELDS=['hp','attack','defense','sp_attack','sp_defense','speed']
SLOT_RE=re.compile(r'^#define SPECIES_([A-Z0-9_]+)\s+(\d+)\s*$',re.M)


def load_ids():
    st=(ROOT/'include/constants/species.h').read_text()
    ids={int(n):s for s,n in SLOT_RE.findall(st) if 1<=int(n)<=250}
    assert len(ids)==250,('Cannot identify first 250 native species IDs',len(ids))
    return ids


def replace_slot(text,slot,func):
    # Literal C designated initializer for one existing species.
    needle='[SPECIES_'+slot+']'
    loc=re.search(r'(?m)^\s*'+re.escape(needle)+r'\s*=',text)
    if not loc:raise ValueError('Missing native species table entry '+slot)
    rest=text[loc.end():]
    brace=rest.find('{')
    if brace<0:raise ValueError('Missing braced species value '+slot)
    begin=loc.end()+brace
    level=1;i=begin+1
    while level and i<len(text):
        if text[i]=='{':level+=1
        elif text[i]=='}':level-=1
        i+=1
    if level:raise ValueError('Unbalanced C block '+slot)
    before=text[begin:i]
    after=func(before)
    return text[:begin]+after+text[i:]


def entry_name_replace(text,slot,name):
    # Preserve stable symbol ID; replace the actual runtime string.
    pattern=r'(?m)^(\s*\[SPECIES_'+re.escape(slot)+r'\]\s*=\s*_)\("[^"]*"\)(,?)'
    out,n=re.subn(pattern,lambda m:f'{m.group(1)}("{name.upper()}"){m.group(2)}',text)
    if n!=1:raise ValueError(('Species display name missing',slot,n))
    return out


def update_stats(block,stat):
    for prop,field in zip(STA,FIELDS):
        r=r'(?m)^(\s*\.'+prop+r'\s*=\s*)(\d+)(\s*,)'
        block,n=re.subn(r,lambda m:m.group(1)+str(stat[field])+m.group(3),block)
        if n!=1:raise ValueError(('Missing stat',prop))
    return block


def update_types(block,tokens):
    t=tokens if len(tokens)==2 else tokens*2
    patt=r'(\.types\s*=\s*\{)\s*TYPE_[A-Z_]+\s*,\s*TYPE_[A-Z_]+\s*(\})'
    new,n=re.subn(patt,lambda m:m.group(1)+' '+t[0]+', '+t[1]+' '+m.group(2),block)
    if n!=1:raise ValueError('Missing types field')
    return new


def update_gender(block,ratio):
    pat=r'(?m)^(\s*\.genderRatio\s*=\s*)([^,\n]+)(,)'
    new,n=re.subn(pat,lambda m:m.group(1)+ratio+m.group(3),block)
    if n!=1:raise ValueError('Missing genderRatio')
    return new


def palette_text(rgb):
    assert len(rgb)==16
    return 'JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,col)) for col in rgb)+'\n'


def pal_read(path):
    lines=Path(path).read_text().splitlines()
    assert lines[0]=='JASC-PAL' and lines[2]=='16'
    return [tuple(map(int,line.split())) for line in lines[3:19]]


def remake_icon(src,shared_pals):
    src=Image.open(src)
    src.load()
    assert src.mode=='P' and src.size==(32,64)
    assert max(src.getdata())<=15
    origpal=[tuple(src.getpalette()[i*3:i*3+3]) for i in range(16)]
    idx=list(src.getdata())
    best=None
    for pal_index,pal in enumerate(shared_pals):
        lookup=[0]
        for col in origpal[1:]:
            candidates=[sum((col[c]-v[c])**2 for c in range(3)) for v in pal[1:]]
            lookup.append(1+min(range(15),key=lambda i:candidates[i]))
        out=[lookup[x] for x in idx]
        loss=sum(sum((origpal[x][c]-pal[lookup[x]][c])**2 for c in range(3)) for x in idx if x)
        if best is None or loss<best[0]:best=(loss,pal_index,pal,out)
    _,index,pal,data=best
    img=Image.new('P',(32,64))
    img.putpalette([v for rgb in pal for v in rgb]+[0]*720)
    img.putdata(data)
    img.info['transparency']=0
    return img,index


def bounds(im):
    im=im.convert('P')
    pix=list(im.getdata());coords=[(i%im.width,i//im.width) for i,v in enumerate(pix) if v]
    if not coords:return (8,8,0)
    xmin=min(x for x,y in coords);xmax=max(x for x,y in coords)
    ymin=min(y for x,y in coords);ymax=max(y for x,y in coords)
    w=min(64, ((xmax-xmin+1+7)//8)*8)
    h=min(64, ((ymax-ymin+1+7)//8)*8)
    yoffset=max(0,63-ymax)
    return w,h,yoffset


def update_coord(text,slot,dimensions):
    w,h,y=dimensions
    pat=r'(?m)^(\s*\[SPECIES_'+re.escape(slot)+r'\]\s*=\s*\{\s*\.size\s*=\s*)MON_COORDS_SIZE\(\d+,\s*\d+\)(,\s*\.y_offset\s*=\s*)\d+\s*(\},?)'
    out,n=re.subn(pat,lambda m:m.group(1)+f'MON_COORDS_SIZE({w}, {h})'+m.group(2)+str(y)+m.group(3),text)
    if n!=1:raise ValueError(('coords not found',slot,n))
    return out


def update_icon_index(text,slot,index):
    pat=r'(?m)^(\s*\[SPECIES_'+re.escape(slot)+r'\]\s*=\s*)(\d+)(,)'
    # In pokemon_icon.c, just one matching target exists in gMonIconPaletteIndices
    start=text.index('const u8 gMonIconPaletteIndices[]')
    pre,part=text[:start],text[start:]
    out,n=re.subn(pat,lambda m:m.group(1)+str(index)+m.group(3),part)
    if n!=1:raise ValueError(('icon palette index not found',slot))
    return pre+out


def add_alias_header(ids,catalog):
    path=ROOT/'include/constants/valdara_species.h'
    lines=['#ifndef GUARD_VALDARA_SPECIES_H','#define GUARD_VALDARA_SPECIES_H','',
           '// Original species catalogue IDs (1..250) mapped to stable Emerald internal slots.',
           '// These names are alias symbols; the 1..250 numeric IDs are RESERVED for Valdara.',
           '// No legacy species constants are removed or renumbered.','']
    for e in catalog:
        n=e['number'];lines.append(f'#define SPECIES_VALDARA_{n:03d} SPECIES_{ids[n]}')
    lines+=['', '#endif // GUARD_VALDARA_SPECIES_H','']
    path.write_text('\n'.join(lines))
    original=ROOT/'include/constants/species.h'
    txt=original.read_text()
    marker='#include "constants/valdara_species.h"'
    if marker not in txt:
        txt=txt.replace('#endif  // GUARD_CONSTANTS_SPECIES_H',marker+'\n\n#endif  // GUARD_CONSTANTS_SPECIES_H')
        original.write_text(txt)


def clear_legacy_evolutions_and_safe_approved(table,ids,relations):
    """Replace only the first 250 evolution entries, never other Emerald species."""
    safe=[]
    by_from={}
    for e in relations:
        if e['status']!='APROBADO':continue
        cond=e['condition'].strip().lower()
        m=re.fullmatch(r'nivel\s+(\d{1,2})',cond)
        if not m:continue
        a=ids[e['from']];b=ids[e['to']];level=int(m.group(1))
        safe.append((a,b,level,e['from'],e['to']))
        by_from.setdefault(a,[]).append((b,level))
    for slot in [ids[i] for i in range(1,251)]:
        pat=r'(?m)^[ \t]*\[SPECIES_'+re.escape(slot)+r'\][ \t]*='
        match=re.search(pat,table)
        if match is None:continue
        i=table.find('{',match.end())
        if i<0:raise ValueError('Evolution initializer without opening brace '+slot)
        depth=0;end=i
        while end<len(table):
            if table[end]=='{':depth+=1
            elif table[end]=='}':
                depth-=1
                if depth==0:
                    end+=1;break
            end+=1
        if depth:raise ValueError('Unbalanced evolution table '+slot)
        while end<len(table) and table[end] in ' \t':end+=1
        if end<len(table) and table[end]==',':end+=1
        table=table[:match.start()]+table[end:]
    lines=[]
    for i in range(1,251):
        name='SPECIES_'+ids[i]
        edges=by_from.get(ids[i],[])
        if len(edges)>5:raise ValueError('Too many supported evolutions '+name)
        if edges:
            body=', '.join('{EVO_LEVEL, '+str(level)+', SPECIES_'+b+'}' for b,level in edges)
            lines.append('    ['+name+'] = {'+body+'},')
        else:
            lines.append('    ['+name+'] = {{0}},')
    needle='\n};'
    pos=table.rfind(needle)
    if pos<0:raise ValueError('Evolution table end missing')
    table=table[:pos]+'\n    // Valdara 001–250: cleared inherited Emerald evolutions; approved simple links only.\n'+'\n'.join(lines)+'\n'+table[pos:]
    return table,safe


def install():
    data=json.loads(DATA.read_text());entry=data['entries'];ids=load_ids()
    names_path=ROOT/'src/data/text/species_names.h'
    stats_path=ROOT/'src/data/pokemon/species_info.h'
    evol_path=ROOT/'src/data/pokemon/evolution.h'
    name_text=names_path.read_text();stat_text=stats_path.read_text();evo_text=evol_path.read_text()
    info={'mapped_species':250,'names_active':0,'approved_6_stats_active':0,'approved_stat_variants_preserved':0,
          'types_active_exact_supported':0,'types_pending_unimplemented_or_ambiguous':0,
          'original_graphics_active':0,'original_graphics_pending':0,
          'abilities_effects_await_battle_engine':0,'approved_evolutions_deferred':0,
          'inherited_emerald_stats_temporary':0,'engine_slot_map':{},'art_palette_indexes':{},
          'status':'native source registration; no ROM built'}
    for e in entry:
        num=e['number'];slot=ids[num];name=e['gba_name'];
        info['engine_slot_map'][str(num)]={'slot':num,'species_constant':'SPECIES_'+slot,'display':name,'original_title':e['name']}
        name_text=entry_name_replace(name_text,slot,name);info['names_active']+=1
        stat=e['stat'];tokens=e['engine_type_tokens']
        gender=None
        if num in (1,3,5,7,8,9):gender='MON_MALE'
        if num in (2,4,6,10,11,12):gender='MON_FEMALE'
        if num in (159,160,161):gender='MON_GENDERLESS'
        def change(block):
            if stat:block=update_stats(block,stat)
            if tokens:block=update_types(block,tokens)
            if gender:block=update_gender(block,gender)
            return block
        stat_text=replace_slot(stat_text,slot,change)
        info['approved_6_stats_active']+=bool(stat)
        info['approved_stat_variants_preserved']+=len(e['stat_variants'])
        info['types_active_exact_supported']+=bool(tokens)
        info['types_pending_unimplemented_or_ambiguous']+=not bool(tokens)
        info['original_graphics_pending']+=not bool(e['art_slug'])
        info['abilities_effects_await_battle_engine']+=bool(e['ability_spec'])
        info['inherited_emerald_stats_temporary']+=not bool(stat)
    names_path.write_text(name_text);stats_path.write_text(stat_text)
    evo_text,safe=clear_legacy_evolutions_and_safe_approved(evo_text,ids,data['evolutions'])
    evol_path.write_text(evo_text)
    info['approved_evolutions_implemented_simple']=[{'from':i,'to':j,'level':lvl} for a,b,lvl,i,j in safe]
    info['approved_evolutions_deferred']=sum(r['status']=='APROBADO' for r in data['evolutions'])-len(safe)
    add_alias_header(ids,entry)
    # Install 11 finalized sprite resource sheets in active graphics/pokemon folders.
    graphics=ROOT/'graphics/valdara_nevarios'; icon_c=ROOT/'src/pokemon_icon.c'
    icon_text=icon_c.read_text();
    front_c=(ROOT/'src/data/pokemon_graphics/front_pic_coordinates.h')
    back_c=(ROOT/'src/data/pokemon_graphics/back_pic_coordinates.h')
    front_text=front_c.read_text();back_text=back_c.read_text()
    palette_files=[ROOT/f'graphics/pokemon/icon_palettes/icon_palette_{i}.pal' for i in range(3)]
    shared=[pal_read(p) for p in palette_files]
    for e in entry:
        if not e['art_slug']:continue
        n=e['number'];slug=e['art_slug'];source=graphics/slug
        # Slot sprites are stored under the Emerald legacy directory, so ALL
        # the existing native front/back/icon pointers remain valid automatically.
        legacy=ROOT/f'graphics/pokemon/{ids[n].lower()}'
        assert legacy.is_dir(), legacy
        for filename in ('front.png','back.png','anim_front.png','normal.pal'):
            assert (source/filename).is_file(),source/filename
            shutil.copy2(source/filename,legacy/filename)
        shutil.copy2(source/'normal.pal',legacy/'shiny.pal')  # no unapproved shiny variant invented
        icon,pal_index=remake_icon(source/'icon.png',shared)
        icon.save(legacy/'icon.png',transparency=0,bits=4)
        icon_text=update_icon_index(icon_text,ids[n],pal_index)
        front_text=update_coord(front_text,ids[n],bounds(Image.open(source/'front.png')))
        back_text=update_coord(back_text,ids[n],bounds(Image.open(source/'back.png')))
        info['art_palette_indexes'][e['art_slug']]=pal_index
        info['original_graphics_active']+=1
    icon_c.write_text(icon_text);front_c.write_text(front_text);back_c.write_text(back_text)
    # Do not change the installed Emerald move pools or standard ability semantics
    # until approved abilities/moves have battle hooks. All design specs remain
    # in catalog_250.json with exact values and explicit states.
    info['ability_runtime_hook']='pending: design specs preserved; not declared functional'
    info['move_runtime_hook']='pending: exclusive movement effects not generated'
    info['art_remaining']=250-info['original_graphics_active']
    # Route scripts use the regional IDs, not an unrelated legacy Nidoran slot.
    story=ROOT/'valdara/port_scripts.inc'
    if story.is_file():
        txt=story.read_text()
        txt=txt.replace('givemon SPECIES_NIDORAN_M, 5','givemon SPECIES_VALDARA_001, 5')
        txt=txt.replace('givemon SPECIES_NIDORAN_F, 5','givemon SPECIES_VALDARA_002, 5')
        txt=txt.replace('Tengo dos NIDORAN.', 'Tengo dos ESCUALÍN.')
        txt=txt.replace('NIDORAN hembra','ESCUALÍN hembra').replace('NIDORAN macho','ESCUALÍN macho')
        story.write_text(txt)
    install_port=ROOT/'valdara/install_port.py'
    if install_port.is_file():
        script=install_port.read_text()
        original="species=['ZIGZAGOON','POOCHYENA','WINGULL','WURMPLE','ZIGZAGOON','WINGULL','WURMPLE','POOCHYENA','NIDORAN_F','NIDORAN_M','NIDORAN_F','NIDORAN_M']"
        adapted="species=['VALDARA_131','VALDARA_133','VALDARA_135','VALDARA_137','VALDARA_131','VALDARA_135','VALDARA_137','VALDARA_133','VALDARA_147','VALDARA_149','VALDARA_147','VALDARA_149']"
        if original in script:script=script.replace(original,adapted)
        elif adapted not in script:raise ValueError('Unknown route encounter schema: review install_port.py')
        install_port.write_text(script)
    info['regional_port_starter_ids']=[1,2]
    info['regional_route_01_slots']=[131,133,135,137,147,149]
    info['source_data_sha256']=hashlib.sha256(DATA.read_bytes()).hexdigest()
    REPORT.write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
    print('PASS: native names',info['names_active'],'stats',info['approved_6_stats_active'],
          'graphics',info['original_graphics_active'],'types',info['types_active_exact_supported'],
          'safe evolutions',len(safe),'pending artwork',info['art_remaining'])

if __name__=='__main__':install()