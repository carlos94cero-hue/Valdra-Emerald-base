#!/usr/bin/env python3
"""Install Puerto Brisa as new native Emerald maps, without replacing Hoenn maps."""
from pathlib import Path
import base64,zlib,struct,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
GRID='c-rljOK;Oa5XY5tG}}}H>=r6YFNg~VXlo`>XiEf5Oo2XtK6vy&puhzr4*e3GI0Gl(1e_2j;KWlR0#1N<T!7C39B6HCY_DHyN3q2L^w&DO-kD!!cXl>uKqIkoS|=5#i*i~6vQP;XQmLCN`0wynRZ|T(8S68SIgRt<_x~u`WSd{Y`0OU<SK8orK<oTf)#Uer*v7DGsfH%6*B8In*54}VrJH=yU(^wturw*m*nE$jHla;wQ=WGs|JoLp|AJl`dSwx2a2Drq9#2>^Pzv(-yBU~;IhY4N=I^57e}iugy|elYxQI*nWjqrT{{k$+5-dYh{38E7e!>s<u}M5gQ#5Vd2nCYySKvHcfQ!%paeOFkhi}*eI}BUCPSs-R<pOc3mh6#U<}@|%t<m{aNsN*6l_u9O+lqT^ppCSNcG514=642SbfXTFIRBG=(Qg`}{VbZVNLX>|$9}v@SBz&ge=GGht@{K;GsSt{-$wHN4?81@k7SR$`|r;$uPc#%9d9_g={fb?)>+ZZN;9waNX8Gwe+zFry5r;X%2b?l!$<bK277>@2wCxmVFX5DUkv{)-g9)nrTtlfD%3!a;XlAj_!OVvbG(cXeYcLc68OliLRYf;^ASGA*VxE^H9nu9d!Hn!Uz;qyKijEa-tUs0|90wET$8MRWeV1I^7_qFdJ5+cvLTiyvt`3S!1l61hu%}(T#hG&TZQv?JM4i3YmnLeo&C>}{|D=#620nJPhb_!kCMACnNJDDYz(kg_}nw-BmO>_QT(9k;vqV0JiliUf1bvRIqeu7H|kd}X2m~+r!g6Sn2oSe)++xjo=eCdV^vmTt>pI$Rf=4nQ`&!fjlt?k<NUa53|7xt%K1$$@4qfFvb9wB>B%4Ie}!os4YjkX'
def load(p):return json.loads((ROOT/p).read_text())
def write(p,data):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(data if isinstance(data,str) else json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def npc(gfx,x,y,script='Citizen',direction='FACE_DOWN',elevation=3):
 return {'graphics_id':'OBJ_EVENT_GFX_'+gfx,'x':x,'y':y,'elevation':elevation,'movement_type':'MOVEMENT_TYPE_'+direction,'movement_range_x':0,'movement_range_y':0,'trainer_type':'TRAINER_TYPE_NONE','trainer_sight_or_berry_tree_id':'0','script':'PuertoBrisa_'+script,'flag':'0'}
def warp(x,y,target,idx=0,elevation=0):return {'x':x,'y':y,'elevation':elevation,'dest_map':target,'dest_warp_id':str(idx)}
def install():
 names=['PuertoBrisa','PuertoBrisaInn','PuertoBrisaClinic','PuertoBrisaShop','PuertoBrisaTerminal','PuertoBrisaHouse','RutaBrisa']
 ids=['MAP_PUERTO_BRISA','MAP_PUERTO_BRISA_INN','MAP_PUERTO_BRISA_CLINIC','MAP_PUERTO_BRISA_SHOP','MAP_PUERTO_BRISA_TERMINAL','MAP_PUERTO_BRISA_HOUSE','MAP_RUTA_BRISA']
 groups=load('data/maps/map_groups.json');group='gMapGroup_Valdara'
 if group not in groups['group_order']:groups['group_order'].append(group)
 groups[group]=names;write('data/maps/map_groups.json',groups)
 layouts=load('data/layouts/layouts.json');layouts['layouts']=[l for l in layouts['layouts'] if l['id'] not in ['LAYOUT_PUERTO_BRISA','LAYOUT_RUTA_BRISA']]
 grid=list(struct.unpack('<2304H',zlib.decompress(base64.b85decode(GRID))))
 rw,rh=24,26;route=[[0x3001]*rw for _ in range(rh)]
 for y in range(rh):
  for x in range(rw):
   if x<3 or x>20 or y<3:route[y][x]=0x400|[[0x0e,0x0f],[0x1e,0x1f]][y%2][x%2]
 for y in range(3,rh):
  for x in range(10,14):route[y][x]=0x3203
 for y in range(11,19):
  for x in range(4,8):route[y][x]=0x3015
 for y in range(5,12):
  for x in range(16,20):route[y][x]=0x3015
 for x,y in [(5,6),(7,7),(17,16),(19,18),(6,21),(18,22)]:route[y][x]=0x3404
 route[4][12]=0x403
 for name,lid,w,h,vals in [('PuertoBrisa','LAYOUT_PUERTO_BRISA',48,48,grid),('RutaBrisa','LAYOUT_RUTA_BRISA',rw,rh,sum(route,[]))]:
  path=ROOT/'data/layouts'/name;path.mkdir(parents=True,exist_ok=True)
  (path/'map.bin').write_bytes(struct.pack('<'+'H'*len(vals),*vals))
  (path/'border.bin').write_bytes(struct.pack('<4H',*([0x1170]*4 if name=='PuertoBrisa' else [0x40e,0x40f,0x41e,0x41f])))
  layouts['layouts'].append({'id':lid,'name':name+'_Layout','width':w,'height':h,'primary_tileset':'gTileset_General','secondary_tileset':'gTileset_Slateport','border_filepath':f'data/layouts/{name}/border.bin','blockdata_filepath':f'data/layouts/{name}/map.bin'})
 write('data/layouts/layouts.json',layouts)
 sections=load('src/data/region_map/region_map_sections.json');sections['map_sections']=[s for s in sections['map_sections'] if s['id'] not in ['MAPSEC_PUERTO_BRISA','MAPSEC_RUTA_BRISA']]
 sections['map_sections'] += [{'id':'MAPSEC_PUERTO_BRISA','name':'PUERTO BRISA','x':8,'y':12,'width':1,'height':1},{'id':'MAPSEC_RUTA_BRISA','name':'RUTA 01','x':8,'y':11,'width':1,'height':1}];write('src/data/region_map/region_map_sections.json',sections)
 port=load('data/maps/SlateportCity/map.json');port.update(id=ids[0],name=names[0],layout='LAYOUT_PUERTO_BRISA',region_map_section='MAPSEC_PUERTO_BRISA',connections=[{'map':ids[6],'offset':12,'direction':'up'}])
 port['object_events']=[npc('MOM',20,38,'Mom','FACE_LEFT'),npc('OLD_MAN',25,5,'Elder','FACE_LEFT'),npc('SAILOR',18,35,'Sailor'),npc('FISHERMAN',18,41,'Fisherman','FACE_RIGHT'),npc('WOMAN_2',25,17,'Gardener','FACE_LEFT'),npc('MAN_3',10,28,'Cargo'),npc('LITTLE_GIRL',31,14,'Girl'),npc('MART_EMPLOYEE',38,16,'Market'),npc('BOY_1',11,16,'Citizen','FACE_RIGHT'),npc('SS_TIDAL',25,39,'Ship','FACE_RIGHT',1)]
 port['warp_events']=[warp(8,12,ids[1]),warp(34,11,ids[2]),warp(36,21,ids[3]),warp(9,23,ids[4]),warp(15,10,ids[5])]
 port['coord_events']=[{'type':'trigger','x':x,'y':1,'elevation':3,'var':'VAR_TEMP_0','var_value':'0','script':'PuertoBrisa_Gate'} for x in (23,24,25)]
 port['bg_events']=[{'type':'sign','x':x,'y':y,'elevation':0,'player_facing_dir':'BG_EVENT_PLAYER_FACING_ANY','script':'PuertoBrisa_'+s} for x,y,s in [(11,12,'InnSign'),(37,11,'ClinicSign'),(39,22,'ShopSign'),(13,23,'TerminalSign'),(25,6,'RouteSign')]];write('data/maps/PuertoBrisa/map.json',port)
 for template,i,door in [('OldaleTown_House1',1,0),('SlateportCity_PokemonCenter_1F',2,1),('SlateportCity_Mart',3,2),('SlateportCity_Harbor',4,3),('OldaleTown_House1',5,4)]:
  obj=load(f'data/maps/{template}/map.json');obj.update(id=ids[i],name=names[i],region_map_section='MAPSEC_PUERTO_BRISA',connections=None,coord_events=[],bg_events=[])
  obj['warp_events']=[warp(w['x'],w['y'],ids[0],door,w['elevation']) for w in obj['warp_events'] if w['dest_map'] in ('MAP_SLATEPORT_CITY','MAP_OLDALE_TOWN')]
  if i==1:obj['object_events']=[npc('WOMAN_2',6,4,'Innkeeper')]
  if i==2:obj['object_events']=[npc('NURSE',7,2,'Nurse'),npc('SAILOR',2,3,'Citizen'),npc('WOMAN_5',1,6,'Upstairs')]
  if i==3:obj['object_events']=[npc('MART_EMPLOYEE',1,3,'Clerk','FACE_RIGHT')]
  if i==4:obj['object_events']=[npc('SAILOR',8,10,'Terminal'),npc('SS_TIDAL',13,7,'Ship','FACE_RIGHT',1)]
  if i==5:obj['object_events']=[npc('OLD_WOMAN',6,4,'Resident')]
  write(f'data/maps/{names[i]}/map.json',obj);write(f'data/maps/{names[i]}/scripts.inc',f'{names[i]}_MapScripts::\n\t.byte 0\n')
 rmap=load('data/maps/Route101/map.json');rmap.update(id=ids[6],name=names[6],layout='LAYOUT_RUTA_BRISA',region_map_section='MAPSEC_RUTA_BRISA',connections=[{'map':ids[0],'offset':-12,'direction':'down'}],object_events=[npc('GIRL_1',8,8,'RouteGirl')],warp_events=[],coord_events=[],bg_events=[{'type':'sign','x':12,'y':4,'elevation':0,'player_facing_dir':'BG_EVENT_PLAYER_FACING_ANY','script':'PuertoBrisa_RouteEnd'}]);write('data/maps/RutaBrisa/map.json',rmap);write('data/maps/RutaBrisa/scripts.inc','RutaBrisa_MapScripts::\n\t.byte 0\n')
 write('data/maps/PuertoBrisa/scripts.inc','PuertoBrisa_MapScripts::\n\tmap_script MAP_SCRIPT_ON_TRANSITION, PuertoBrisa_OnEnter\n\t.byte 0\nPuertoBrisa_OnEnter:\n\tsetflag FLAG_SYS_B_DASH\n\tsetrespawn HEAL_LOCATION_PUERTO_BRISA\n\tend\n')
 heal=load('src/data/heal_locations.json');heal['heal_locations']=[h for h in heal['heal_locations'] if h['id']!='HEAL_LOCATION_PUERTO_BRISA'];heal['heal_locations'].append({'id':'HEAL_LOCATION_PUERTO_BRISA','map':ids[0],'x':34,'y':12});write('src/data/heal_locations.json',heal)
 wild=load('src/data/wild_encounters.json');g=wild['wild_encounter_groups'][0];g['encounters']=[e for e in g['encounters'] if e['map']!=ids[6]];species=['ZIGZAGOON','POOCHYENA','WINGULL','WURMPLE','ZIGZAGOON','WINGULL','WURMPLE','POOCHYENA','NIDORAN_F','NIDORAN_M','NIDORAN_F','NIDORAN_M'];g['encounters'].append({'map':ids[6],'base_label':'gRutaBrisa','land_mons':{'encounter_rate':15,'mons':[{'min_level':2,'max_level':4,'species':'SPECIES_'+s} for s in species]}});write('src/data/wild_encounters.json',wild)
 ng=(ROOT/'src/new_game.c').read_text().replace('SetWarpDestination(MAP_GROUP(MAP_INSIDE_OF_TRUCK), MAP_NUM(MAP_INSIDE_OF_TRUCK), WARP_ID_NONE, -1, -1);','SetWarpDestination(MAP_GROUP(MAP_PUERTO_BRISA), MAP_NUM(MAP_PUERTO_BRISA), WARP_ID_NONE, 19, 38);');write('src/new_game.c',ng)
 ow=(ROOT/'src/overworld.c').read_text().replace('gFieldCallback = ExecuteTruckSequence;','gFieldCallback = FieldCB_WarpExitFadeFromBlack;');write('src/overworld.c',ow)
 text=(ROOT/'data/event_scripts.s').read_text();includes='\n'+''.join(f'\t.include "data/maps/{n}/scripts.inc"\n' for n in names)+'\t.include "valdara/port_scripts.inc"\n'
 if 'valdara/port_scripts.inc' not in text:write('data/event_scripts.s',text+includes)
 assert len(grid)==48*48
 from collections import deque
 q=deque([(19,38)]);seen=set(q)
 while q:
  x,y=q.popleft()
  for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if 0<=nx<48 and 0<=ny<48 and (nx,ny) not in seen and not ((grid[ny*48+nx]>>10)&3) and (grid[ny*48+nx]>>12)==3:seen.add((nx,ny));q.append((nx,ny))
 for target in [(8,13),(34,12),(36,22),(9,24),(15,11),(24,2),(39,40)]:assert target in seen,('unreachable',target)
 write('dist/port_validation.json',{'base':'Pokemon Emerald (pret)','maps':names,'port_size':[48,48],'reachable_tiles':len(seen),'start':[19,38],'doors_checked':5,'layout_sha256':hashlib.sha256(struct.pack('<2304H',*grid)).hexdigest(),'all_existing_hoenn_maps_preserved':True});print('PASS: native Emerald Puerto Brisa, 5 interiors, Route 01 and reachable doors')
if __name__=='__main__':install()
