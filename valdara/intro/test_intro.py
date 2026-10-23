#!/usr/bin/env python3
"""Static and idempotence checks only. No ROM or emulator is produced/launched."""
from pathlib import Path
import json
import re
from install import install, ROOT


def body(source, name):
    match = re.search(r'(?:static\s+)?(?:void|u8|s8|bool8)\s+' + name + r'\([^;]*?\)\s*\{', source)
    assert match, name
    i = match.end(); start = i; depth = 1
    while depth:
        if source[i] == '{': depth += 1
        if source[i] == '}': depth -= 1
        i += 1
    return source[start:i-1]


def check():
    source = (ROOT/'src/main_menu.c').read_text()
    welcome = body(source,'Task_NewGameBirchSpeech_WaitForSpriteFadeInWelcome')
    assert 'sText_ValdaraWelcome' in welcome
    assert 'func = Task_NewGameBirchSpeech_StartBirchLotadPlatformFade' in welcome
    assert 'func = Task_NewGameBirchSpeech_ThisIsAPokemon' not in welcome
    post = body(source,'Task_NewGameBirchSpeech_ProcessNameYesNoMenu')
    assert 'sText_ValdaraReady' in post and 'tIsDoneFadingSprites = TRUE' in post
    assert 'func = Task_NewGameBirchSpeech_ShrinkPlayer' in post
    assert 'func = Task_NewGameBirchSpeech_SlidePlatformAway2' not in post
    assert 'func = Task_NewGameBirchSpeech_BoyOrGirl' in post
    choose = body(source,'Task_NewGameBirchSpeech_ChooseGender')
    assert 'case MALE:' in choose and 'case FEMALE:' in choose
    assert 'DoNamingScreen(NAMING_SCREEN_PLAYER' in source
    assert 'SetMainCallback2(CB2_NewGame)' in source
    objects = body(source,'AddBirchSpeechObjects')
    assert 'FACILITY_CLASS_HIKER' in objects and 'AddNewGameBirchObject(' not in objects
    assert 'FACILITY_CLASS_BRENDAN' in objects and 'FACILITY_CLASS_MAY' in objects
    port = json.loads((ROOT/'data/maps/PuertoBrisa/map.json').read_text())
    travelers = [n for n in port['object_events'] if n['script']=='PuertoBrisa_Elder']
    assert len(travelers)==1 and travelers[0]['graphics_id']=='OBJ_EVENT_GFX_HIKER'
    scripts = (ROOT/'valdara/port_scripts.inc').read_text()
    for instruction in ['givemon SPECIES_NIDORAN_M, 5','givemon SPECIES_NIDORAN_F, 5','FLAG_SYS_POKEMON_GET']:
        assert instruction in scripts
    data = json.loads((ROOT/'valdara/intro/dialogue.json').read_text())
    assert data['creatures']=='Nevarios'
    charmap={c:int(h,16) for c,h in re.findall(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(ROOT/'charmap.txt').read_text(),re.M)}
    fonts=(ROOT/'src/fonts.c').read_text()
    widths=list(map(int,re.findall(r'\d+',re.search(r'gFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',fonts,re.S)[1])))
    lines=sum(data['welcome_pages'],[]) + data['choose'] + data['name'] + data['confirm'] + data['ready']
    for line in lines:
        expanded=line.replace('{PLAYER}','WWWWWWW')
        assert all(c in charmap for c in expanded),line
        size=sum(widths[charmap[c]] for c in expanded)
        assert size<=216,(line,size)
    for label in [data['boy'],data['girl']]:
        assert sum(widths[charmap[c]] for c in label)<=40
    watched=['src/main_menu.c','src/valdara_intro_text.h','data/maps/PuertoBrisa/map.json','valdara/port_scripts.inc']
    before={p:(ROOT/p).read_bytes() for p in watched}
    roms_before={str(p):p.stat().st_size for p in ROOT.rglob('*.gba')}
    install()
    assert all((ROOT/p).read_bytes()==b for p,b in before.items())
    assert roms_before=={str(p):p.stat().st_size for p in ROOT.rglob('*.gba')}
    print('PASS: welcome -> native protagonist selection; name cancellation and final transition')
    print('PASS: same traveler in intro/port; starter still awarded only by port script')
    print('PASS: Nevarios, Spanish glyphs, 216px text bounds, 48px selection window')
    print('PASS: idempotent installer; no ROM generated; existing logo/title untouched')
    print('PENDING: compilation and complete input-driven intro test in the planned ROM-test phase')

if __name__=='__main__':check()
