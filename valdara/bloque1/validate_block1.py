#!/usr/bin/env python3
"""Static integration audit, constrained to approved source facts. NEVER compiles a ROM."""
from pathlib import Path
import hashlib, json, re, subprocess, tempfile
R=Path(__file__).resolve().parents[2]
B=R/'valdara/bloque1'
catalog=json.loads((R/'valdara/species/catalog_250.json').read_text())
entries=catalog['entries']
assert len(entries)==250
assert len([e for e in entries if e.get('art_slug')])==11
assert [e['name'] for e in entries[158:161]]==['Nevarión','Umbrálix','Límbora']
for e in entries[:2]:
 assert e['stat']['total'] in (290,300)
for e in entries[6:12]:
 assert sum(e['stat'][k] for k in ('hp','attack','defense','sp_attack','sp_defense','speed'))==690
for e in entries[2:6]:
 for v in e['stat_variants'].values():
  assert sum(v[k] for k in ('hp','attack','defense','sp_attack','sp_defense','speed'))==v['total']

species=(R/'src/data/pokemon/species_info.h').read_text()
ids={int(v):k for k,v in re.findall(r'^#define SPECIES_([A-Z0-9_]+)\s+(\d+)',(R/'include/constants/species.h').read_text(),re.M)}
for i in range(1,13):
 key=ids[i];start=species.index(f'    [SPECIES_{key}] =');end=species.index('    },',start)
 block=species[start:end]
 assert '.abilities' in block and 'ABILITY_NONE' in block
 for e in entries[6:12]:
  if e['number']==i:
   nums=[int(x) for x in re.findall(r'\.base(?:HP|Attack|Defense|Speed|SpAttack|SpDefense)\s*=\s*(\d+)',block)]
   assert len(nums)==6 and sum(nums)==690,(i,nums)

ability_json=json.loads((B/'abilities.json').read_text());assert len(ability_json)==24
assert len([x for x in ability_json if x['battle_effect_status']=='implemented'])==11
ability_names=(R/'src/data/text/abilities.h').read_text();ability_defs=(R/'include/constants/abilities.h').read_text()
for a in ability_json:
 assert len(a['screen_name'])<=12
 assert f'#define {a["key"]} {a["id"]}' in ability_defs
 assert f'[{a["key"]}]' in ability_names
assert '#define ABILITIES_COUNT 102' in ability_defs
moves=(R/'valdara/bloque1/movimientos_aprobados.json')
move_specs=json.loads(moves.read_text())
assert len([x for x in move_specs if x['code'].startswith('V')])==15
assert all(x['pp'] in (5,10,15) for x in move_specs)
assert len([x for x in move_specs if x.get('native_status')=='active'])==3
for name in ('ECLIPSE_ABSOLUTO','NOCHE_ETERNA','FURIA_CONTINENTAL'):
 sym='MOVE_VALDARA_'+name
 assert sym in (R/'include/constants/moves.h').read_text()
 assert '['+sym+']' in (R/'src/data/battle_moves.h').read_text()
 assert '['+sym+']' in (R/'src/data/text/move_names.h').read_text()
 assert '['+sym+' - 1]' in (R/'src/data/text/move_descriptions.h').read_text()
 assert sym in (R/'data/battle_anim_scripts.s').read_text()
assert '#define MOVES_COUNT 358' in (R/'include/constants/moves.h').read_text()
assert 'MOVE_VALDARA_ECLIPSE_ABSOLUTO' in (R/'src/pokemon.c').read_text()
assert 'ValdaraBreedingTarget' in (R/'src/pokemon.c').read_text()
assert 'ValdaraRouteAbility' in (R/'src/pokemon.c').read_text()
assert 'ABILITY_VALDARA_GRACIA_GUARDIANA' in (R/'src/battle_util.c').read_text()
assert (R/'valdara/nevarios/manifest.json').exists()
assert not list(R.glob('*.gba')),'A ROM must never be produced in this phase'

with tempfile.TemporaryDirectory() as d:
 for src,binname in [('breeding_test.c','breeding_test'),('ability_test.c','ability_test')]:
  out=Path(d)/binname
  cmd=['cc','-std=c11','-Wall','-Wextra','-Werror','-pedantic','-iquote',str(R/'include'),str(B/'tests'/src),'-o',str(out)]
  subprocess.run(cmd,check=True)
  subprocess.run([str(out)],check=True)

report={
 'version':'Bloque 1 / ingeniería sin ROM',
 'status':'PASS native pure C tests + source & data consistency',
 'rom_generated':False,
 'original_species_art':11,
 'starter_sprites':8,
 'mythic_sprites':3,
 'three_evolution_routes':True,
 'branch_boundaries':'Macho 1-3-5-(7,8,9), Hembra 2-4-6-(10,11,12)',
 'exact_approved_final_bst':690,
 'intermediate_route_stat_sets':12,
 'ability_names_registered':24,
 'active_effects_implemented':11,
 'hidden_abilities_pending_real_engine':6,
 'mythic_ability_effects_pending_approved_details':6,
 'new_original_battle_moves_native':3,
 'approved_movement_specs_archived':18,
 'moves_pending_full_mechanics':15,
 'status_limits':[
  'No full GBA ROM build or emulator test by explicit request',
  '3 active new moves reuse existing Emerald battle animations',
  'No physical/special split for other Dark moves; Eclipse specifically uses approved physical category',
  'Fairy type unavailable in vanilla Emerald; those signatures remain data-only',
  '3 mythic exclusive attacks have approved names and PP only, not safe to assign invented power',
  'Voluntad Umbría knockout trigger and hidden abilities are not enabled in this stage',
  'Story events must call route scripts before first evolution and the two mission completion scripts',
  'Mythic creatures preserve approved BST=800 target but do not have six approved numbers'
 ]}
(B/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))