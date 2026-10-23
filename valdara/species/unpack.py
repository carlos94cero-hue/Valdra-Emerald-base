#!/usr/bin/env python3
"""Restore the audited human-readable 250-species catalog from its lossless blob."""
import base64
import json
import zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
raw=zlib.decompress(base64.b85decode((ROOT/'catalog_250.b85').read_text().strip()))
value=json.loads(raw)
assert value['schema']=='valdara.native.emerald.250.v1' and len(value['entries'])==250
out=ROOT/'catalog_250.json'
out.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
print('Restored',out.name,'-',len(value['entries']),'registered regional entries')