"""Validate local Markdown targets, maintained Python syntax and snapshot hashes.

Uses only the standard library. External URLs and externally supplied datasets,
checkpoints and author source trees are outside this structural check.
"""
import ast
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[([^\]\n]+)\]\(([^)\n]+)\)")


def check():
    errors = []
    links = 0
    for path in ROOT.rglob("*.md"):
        if any(part in {".git", ".venv", "venv", "__pycache__"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8-sig")
        for match in LINK.finditer(text):
            target = match[2].strip().strip("<>").split("#", 1)[0]
            if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            links += 1
            resolved = (path.parent / unquote(target)).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)}: invalid local target {target}")
    map_root = ROOT / "mappa_interattiva"
    map_data = json.loads((map_root / "contenuti.json").read_text(encoding="utf-8-sig"))
    registry = json.loads((map_root / "fonti.js").read_text(encoding="utf-8").split("=", 1)[1].strip().removesuffix(";"))
    for item in map_data["nodes"] + map_data["edges"]:
        for source in item.get("sources", []):
            target = registry.get(source)
            if target is None:
                errors.append(f"Unconfigured map source: {source}")
            elif not re.match(r"https?://", target):
                resolved = (ROOT / target).resolve()
                if not resolved.is_relative_to(ROOT) or not resolved.is_file():
                    errors.append(f"Invalid map source target: {target}")
    html = (map_root / "index.html").read_text(encoding="utf-8")
    for target in re.findall(r'(?:src|href)="([^"#]+)"', html):
        if not re.match(r"https?://", target) and not (map_root / target).is_file():
            errors.append(f"Invalid map asset: {target}")
    sources = list((ROOT / "integration_prototype").glob("*.py"))
    sources += list((ROOT / "SuperFlex/src/shape_tools").glob("*.py"))
    sources += list((ROOT / "tools").glob("*.py"))
    for path in sources:
        try:
            ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        except SyntaxError as error:
            errors.append(str(error))
    manifest = json.loads((ROOT / "context/evidence/publication_inventory.json").read_text(encoding="utf-8"))
    for row in manifest["files"]:
        path = (ROOT / row["path"]).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            errors.append(f"Missing inventory file: {row['path']}")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
            errors.append(f"Hash mismatch: {row['path']}")
    for error in errors:
        print(error, file=sys.stderr)
    print(f"Local links: {links}; Python sources: {len(sources)}; hashes: {len(manifest['files'])}; errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(check())
