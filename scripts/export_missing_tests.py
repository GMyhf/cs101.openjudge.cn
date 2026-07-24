#!/usr/bin/env python3
"""Export catalog entries that still have no indexed test cases."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "openjudge" / "catalog.json"
OUTPUT = ROOT / "collab" / "t002-missing-tests.json"


def number(value):
    match = re.search(r"(\d+)$", value)
    return int(match.group(1)) if match else None


def main():
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    missing = []
    seen = set()
    for item in catalog["problems"]:
        if item.get("test_cases"):
            continue
        local_number = number(item["id"])
        entry = {
            "book": item["book"],
            "id": item["id"],
            "local_number": local_number,
            "path": item["path"],
        }
        missing.append(entry)
        if local_number is not None:
            seen.add(local_number)

    result = {
        "source": "data/openjudge/catalog.json",
        "catalog_entries_without_tests": len(missing),
        "unique_local_numbers_without_tests": len(seen),
        "entries": missing,
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"exported {len(missing)} catalog entries and {len(seen)} unique local numbers "
        f"to {OUTPUT.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
