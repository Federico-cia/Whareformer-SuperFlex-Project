"""Refresh the publication inventory after all checks, without including itself recursively."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'.git', '__pycache__', '.pytest_cache', '.ruff_cache', 'backup', '.venv', 'venv'}
target = ROOT / 'context/evidence/publication_inventory.json'
rows = []
for path in sorted(ROOT.rglob('*')):
    if not path.is_file() or any(x in EXCLUDED for x in path.relative_to(ROOT).parts) or path == target:
        continue
    if path.suffix in {'.pyc', '.log', '.tmp', '.partial'}:
        continue
    data = path.read_bytes()
    rows.append({'path': path.relative_to(ROOT).as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
with target.open('w', encoding='utf-8', newline='\n') as stream:
    stream.write(json.dumps({'schema': 2, 'date': '2026-11-22', 'base_commit': 'baa24708d800b1c438e1fad401e011f6fac6743d', 'scope': 'Current geometry code, approved option-A map, concise memory, selected evidence. Colleague files preserved; no new raw data, weights, personal access or backups.', 'files': rows}, indent=2) + '\n')
print(f'Inventory: {len(rows)} files')
