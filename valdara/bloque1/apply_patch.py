#!/usr/bin/env python3
"""Apply the audited source-only Valdara patch without compiling/linking a ROM."""
from pathlib import Path
from hashlib import sha256
import base64,zlib,json,subprocess,tempfile
R=Path(__file__).resolve().parents[2]
B=R/'valdara/bloque1'
manifest=json.loads((B/'patch_manifest.json').read_text())
contents=base64.b85decode((B/'engine_patch.b85').read_text().strip())
patch=zlib.decompress(contents)
state={}
for name,digest in manifest.items():
 p=R/name
 assert p.is_file(),('missing baseline',name)
 current=sha256(p.read_bytes()).hexdigest()
 if current==digest['source_sha256']:state[name]='source'
 elif current==digest['patched_sha256']:state[name]='patched'
 else:raise AssertionError(('unexpected file modification',name,current))
if all(x=='patched' for x in state.values()):
 print('PASS: Block 1 engine patch is already installed (idempotent)')
elif all(x=='source' for x in state.values()):
 with tempfile.NamedTemporaryFile(suffix='.patch') as p:
  p.write(patch);p.flush()
  subprocess.run(['patch','--dry-run','--batch','-p1','-i',p.name],cwd=R,check=True)
  subprocess.run(['patch','--batch','-p1','-i',p.name],cwd=R,check=True)
 assert all(sha256((R/name).read_bytes()).hexdigest()==d['patched_sha256'] for name,d in manifest.items())
 print('PASS: applied audited Valdara Block 1 patch to 14 native source files')
else:
 raise AssertionError(('partial install detected; no mutation',state))
assert not list(R.glob('*.gba')), 'Never create GBA ROM in this stage'