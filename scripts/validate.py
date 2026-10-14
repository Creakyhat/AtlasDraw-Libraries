#!/usr/bin/env python3
"""Checks every .atlasdrawlib under libraries/ and writes libraries.json, the index the website reads.

    python scripts/validate.py           # check, then rewrite libraries.json
    python scripts/validate.py --check   # check, and fail if libraries.json is out of date (used by CI)
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIBRARIES = ROOT / "libraries"
INDEX = ROOT / "libraries.json"
FORMAT_VERSION = 1
ID_PATTERN = re.compile(r"^[a-z0-9]+(\.[a-z0-9]+(-[a-z0-9]+)*)+$")
SPDX_ALLOWED = {"CC-BY-4.0", "CC0-1.0", "MIT"}


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def check_library(path: Path, errors: list, item_ids: dict) -> dict | None:
    rel = path.relative_to(ROOT).as_posix()

    def fail(message: str):
        errors.append(f"{rel}: {message}")

    try:
        raw = path.read_bytes()
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as ex:
        fail(f"not valid JSON ({ex})")
        return None

    if data.get("type") != "atlasdrawlib":
        fail('"type" must be "atlasdrawlib"')
        return None
    if data.get("version") != FORMAT_VERSION:
        fail(f'"version" must be {FORMAT_VERSION}')

    for field in ("id", "name", "description", "licence", "category"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            fail(f'"{field}" is required')
    author = data.get("author")
    if not isinstance(author, dict) or not str(author.get("name", "")).strip():
        fail('"author.name" is required')
    if data.get("licence") and data["licence"] not in SPDX_ALLOWED:
        fail(f'"licence" must be one of {sorted(SPDX_ALLOWED)}')
    if data.get("id") and not ID_PATTERN.match(data["id"]):
        fail('"id" must look like "publisher.library-name" (lower case)')
    tags = data.get("tags", [])
    if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
        fail('"tags" must be a list of strings')

    # libraries/<category>/<library>/<library>.atlasdrawlib
    parts = path.relative_to(LIBRARIES).parts
    if len(parts) != 3:
        fail("must be at libraries/<category>/<library>/<library>.atlasdrawlib")
    else:
        category_folder, library_folder, file_name = parts
        if data.get("category") and slug(data["category"]) != category_folder:
            fail(f'is in "{category_folder}/" but its category "{data["category"]}" means "{slug(data["category"])}/"')
        if file_name != f"{library_folder}.atlasdrawlib":
            fail(f'file should be named "{library_folder}.atlasdrawlib"')

    items = data.get("items")
    if not isinstance(items, list) or not items:
        fail('"items" must be a non-empty list')
        items = []
    for n, item in enumerate(items):
        where = f"item {n + 1}"
        if not isinstance(item, dict):
            fail(f"{where} isn't an object")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id:
            fail(f'{where} has no "id"')
        elif item_id in item_ids:
            fail(f'{where} id "{item_id}" is also used in {item_ids[item_id]}')
        else:
            item_ids[item_id] = rel
        if not isinstance(item.get("name"), str) or not item["name"].strip():
            fail(f'{where} ({item_id}) has no "name"')
        elements = item.get("elements")
        if not isinstance(elements, list) or not any(isinstance(e, dict) and not e.get("isDeleted") for e in elements):
            fail(f"{where} ({item_id}) has no elements")

    preview = path.parent / "preview.png"
    if not preview.exists():
        fail("needs a preview.png beside it")

    return {
        "id": data.get("id"),
        "name": data.get("name"),
        "description": data.get("description"),
        "author": author,
        "licence": data.get("licence"),
        "category": data.get("category"),
        "tags": tags,
        "items": len(items),
        "file": rel,
        "preview": preview.relative_to(ROOT).as_posix() if preview.exists() else None,
        "size": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def main() -> int:
    check_only = "--check" in sys.argv[1:]
    errors: list = []
    item_ids: dict = {}
    entries = []
    library_ids = {}

    for p in sorted(LIBRARIES.rglob("*")):
        if p.is_file() and p.suffix != ".atlasdrawlib" and p.name != "preview.png":
            errors.append(f"{p.relative_to(ROOT).as_posix()}: only .atlasdrawlib files and preview.png belong under libraries/")

    for path in sorted(LIBRARIES.rglob("*.atlasdrawlib")):
        entry = check_library(path, errors, item_ids)
        if entry is None:
            continue
        if entry["id"] in library_ids:
            errors.append(f'{entry["file"]}: library id "{entry["id"]}" is also used by {library_ids[entry["id"]]}')
        library_ids[entry["id"]] = entry["file"]
        entries.append(entry)

    if errors:
        print("\n".join(errors))
        print(f"\n{len(errors)} problem(s).")
        return 1

    entries.sort(key=lambda e: (e["category"].lower(), e["name"].lower()))
    index = json.dumps({"formatVersion": FORMAT_VERSION, "libraries": entries}, indent=2, ensure_ascii=False) + "\n"
    if check_only:
        if not INDEX.exists() or INDEX.read_text(encoding="utf-8") != index:
            print("libraries.json is out of date: run python scripts/validate.py and commit the result.")
            return 1
    else:
        INDEX.write_text(index, encoding="utf-8", newline="\n")
    print(f"{len(entries)} librar{'y' if len(entries) == 1 else 'ies'}, {len(item_ids)} items: all good.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
