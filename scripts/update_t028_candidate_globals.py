#!/usr/bin/env python3
"""Attach global identities to T-028 candidates and merge book aliases."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "openjudge" / "catalog.json"
CANDIDATES = ROOT / "collab" / "t028-candidates.json"


def local_number(problem_id):
    match = re.search(r"(\d+)$", problem_id)
    return int(match.group(1)) if match else None


def main():
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))["problems"]
    payload = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    by_global = defaultdict(list)
    practice_by_local = {}
    globals_by_local = defaultdict(set)
    for item in catalog:
        global_number = int(item["global_number"])
        by_global[global_number].append(item)
        number = local_number(item["id"])
        globals_by_local[number].add(global_number)
        if item["book"] == "practice":
            practice_by_local[number] = global_number

    grouped = defaultdict(list)
    for entry in payload["entries"]:
        number = int(entry["number"])
        global_number = entry.get("global_number") or practice_by_local.get(number)
        if global_number is None:
            choices = globals_by_local[number]
            if len(choices) != 1:
                raise ValueError(f"candidate {number} has ambiguous global identity: {choices}")
            global_number = next(iter(choices))
        grouped[int(global_number)].append(entry)

    entries = []
    removed = []
    for global_number, old_rows in grouped.items():
        records = by_global[global_number]
        priorities = sorted({int(row["priority"]) for row in old_rows}
                            | {int(p) for row in old_rows for p in row.get("retired_priorities", [])})
        primary = min(old_rows, key=lambda row: int(row["priority"]))
        preferred_number = int(primary["number"])
        practice_records = [row for row in records if row["book"] == "practice"]
        practice = next((row for row in practice_records
                         if local_number(row["id"]) == preferred_number), None)
        if practice is None and practice_records:
            practice = min(practice_records, key=lambda row: local_number(row["id"]))
        canonical = practice or min(records, key=lambda row: (int(primary["number"]) != local_number(row["id"]),
                                                              row["book"], row["id"]))

        current_count = max(int(row.get("test_count", 0)) for row in records)
        # Priorities <=60 are completed historical rows and remain as review
        # evidence. Later false candidates disappear once another local alias
        # proves that the global problem already has enough data.
        if priorities[0] > 60 and current_count >= 5:
            removed.append({"global_number": global_number, "priorities": priorities,
                            "reason": "global alias already has at least five indexed cases"})
            continue

        oracle_dirs = sorted({path for row in old_rows
                              for path in row.get("oracle_dirs", [row.get("oracle_dir")]) if path})
        row = dict(primary)
        row.update({
            "number": local_number(canonical["id"]),
            "global_number": global_number,
            "practice_id": practice["id"] if practice else None,
            "submit_group": canonical["book"],
            "submit_id": canonical["id"],
            "ids": sorted({record["id"] for record in records}),
            "books": sorted({record["book"] for record in records}),
            "book_count": len({record["book"] for record in records}),
            "oracle_dirs": oracle_dirs,
            "oracle_cases": sum(int(old.get("oracle_cases", 0)) for old in old_rows),
            "in_solution_collection": any(old.get("in_solution_collection") for old in old_rows),
            "featured_book": any(old.get("featured_book") for old in old_rows),
            "priority": priorities[0],
        })
        if len(priorities) > 1:
            row["retired_priorities"] = priorities[1:]
        else:
            row.pop("retired_priorities", None)
        entries.append(row)

    entries.sort(key=lambda row: int(row["priority"]))
    payload["generated_for"] = "2026-07-29 global-number identity correction"
    payload["note"] = ("Entries are grouped by the globally unique number parsed from each mirrored problem page. "
                       "`number` and `practice_id` are the total-library ID used by test directories and submissions.")
    payload["counts"].update({
        "total": len(entries),
        "tier1_zero_data": sum(int(row["tier"]) == 1 for row in entries),
        "tier2_under_five": sum(int(row["tier"]) == 2 for row in entries),
        "with_oracle": sum(bool(row.get("oracle_dirs")) for row in entries),
        "no_oracle": sum(not row.get("oracle_dirs") for row in entries),
        "in_solution_collection": sum(bool(row.get("in_solution_collection")) for row in entries),
        "featured_book": sum(bool(row.get("featured_book")) for row in entries),
    })
    payload["entries"] = entries
    payload["removed_after_global_merge"] = removed
    CANDIDATES.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {len(entries)} global candidates; removed {len(removed)} false candidates")


if __name__ == "__main__":
    main()
