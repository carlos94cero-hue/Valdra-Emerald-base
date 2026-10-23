from pathlib import Path
import subprocess,json
root=Path(__file__).resolve().parents[1];symbols={}
for line in subprocess.check_output(['arm-none-eabi-nm',str(root/'pokeemerald.elf')],text=True).splitlines():
 p=line.split()
 if len(p)==3:
  try:symbols[p[2]]=int(p[0],16)
  except ValueError:pass
names=['gMain','gSaveBlock1Ptr','gSaveBlock2Ptr','gPlayerAvatar','gObjectEvents','CB2_NewGame']
group=json.loads((root/'data/maps/map_groups.json').read_text())['group_order'].index('gMapGroup_Valdara')
(root/'dist/port_symbols.h').write_text(''.join(f'#define S_{n} 0x{symbols[n]:08x}u\n' for n in names)+f'#define VALDARA_MAP_GROUP {group}\n')
