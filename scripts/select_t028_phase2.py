#!/usr/bin/env python3
"""Select global problems whose active tests still come only from non-_made dirs."""
from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPENJUDGE = ROOT / "data" / "openjudge"
CATALOG = OPENJUDGE / "catalog.json"
OUTPUT = ROOT / "collab" / "t028-phase2-candidates.json"


def source_dir(path: str) -> Path:
    value = Path(path)
    return value.parent.parent if value.parent.name == "data" else value.parent


def local_number(problem_id: str) -> int:
    match = re.search(r"(\d+)$", problem_id)
    if not match:
        raise ValueError(f"problem ID has no numeric suffix: {problem_id}")
    return int(match.group(1))


def directory_number(name: str) -> int | None:
    match = re.search(r"(\d+)", name)
    return int(match.group(1)) if match else None


def title_for(entry: dict) -> str:
    page = OPENJUDGE / "pages" / f"{entry['book']}__{entry['id']}.html"
    text = page.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"<title>\s*OpenJudge\s*-\s*(.*?)\s*</title>", text, re.I | re.S)
    if not match:
        raise ValueError(f"missing title in {page.relative_to(ROOT)}")
    value = html.unescape(re.sub(r"<[^>]+>", "", match.group(1))).strip()
    prefix = re.escape(entry["id"]) + r"\s*:\s*"
    return re.sub(rf"^{prefix}", "", value)


def made_dir(number: int, sources: list[str]) -> str:
    matching = [Path(path) for path in sources
                if directory_number(Path(path).name) == number]
    if matching:
        bucket = matching[0].parent.name
    elif number < 1000:
        bucket = "0000-0999"
    elif number < 2000:
        bucket = "1000-1999"
    elif number < 3000:
        bucket = "2000-2999"
    elif number <= 3682:
        bucket = "3000-3682"
    elif number <= 8210:
        bucket = "4000-8210"
    elif number <= 19963:
        bucket = "10000-19963"
    elif number <= 29982:
        bucket = "20000-29982"
    else:
        bucket = "30000-"
    return f"tests/{bucket}/{number:05d}_made"


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))["problems"]
    by_global: dict[int, list[dict]] = defaultdict(list)
    for entry in catalog:
        by_global[int(entry["global_number"])].append(entry)

    candidates = []
    for global_number, aliases in by_global.items():
        sources = sorted({str(source_dir(case["input"]))
                          for entry in aliases
                          for case in entry.get("test_cases", [])})
        if not sources or any(Path(path).name.endswith("_made") for path in sources):
            continue
        practice = next((entry for entry in aliases if entry["book"] == "practice"), None)
        representative = practice or aliases[0]
        number = local_number(representative["id"])
        unique_cases = {(case["input"], case["output"])
                        for entry in aliases for case in entry.get("test_cases", [])}
        candidates.append({
            "global_number": global_number,
            "number": number,
            "title": title_for(representative),
            "practice_id": practice["id"] if practice else None,
            "missing_practice_entry": practice is None,
            "submit_group": representative["book"],
            "submit_id": representative["id"],
            "book_count": len(aliases),
            "books": sorted(entry["book"] for entry in aliases),
            "current_test_count": len(unique_cases),
            "source_dirs": sources,
            "made_dir": made_dir(number, sources),
        })

    candidates.sort(key=lambda row: (-row["book_count"], row["current_test_count"],
                                     row["number"], row["global_number"]))
    for priority, row in enumerate(candidates, 1):
        row["priority"] = priority
        row["round"] = 15 + (priority - 1) // 20

    payload = {
        "task": "T-028",
        "phase": 2,
        "description": "Replace every active non-_made test source with reproducible project-made data",
        "selection_rule": "unique global problem; active test_cases exist and all source dirs are non-_made",
        "priority_rule": "more books first, then fewer existing cases, then local/global number",
        "count": len(candidates),
        "round_range": [15, 15 + (len(candidates) - 1) // 20],
        "entries": candidates,
    }
    if len(candidates) != 208:
        raise ValueError(f"expected the audited baseline of 208 candidates, got {len(candidates)}")
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(candidates)} global problems, "
          f"rounds {payload['round_range'][0]}-{payload['round_range'][1]}")


if __name__ == "__main__":
    main()
