#!/usr/bin/env python3
"""Activate verified per-problem Codeforces rebuilds without regenerating data."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIRROR = ROOT / "data" / "openjudge"
CATALOG = MIRROR / "catalog.json"
FLOAT_REBUILDS = {"2208C"}


def cases_for(problem_id: str):
    root = MIRROR / "tests" / "codeforces" / f"{problem_id}_made"
    required = (root / "samplecode.py", root / "producecase.py")
    if not all(path.is_file() for path in required):
        raise ValueError(f"{problem_id}: missing single-problem source")
    data = root / "data"
    cases = []
    for index in range(21):
        input_path, output_path = data / f"{index}.in", data / f"{index}.out"
        if not input_path.is_file() or not output_path.is_file():
            raise ValueError(f"{problem_id}: missing paired case {index}")
        cases.append({"input": str(input_path.relative_to(MIRROR)),
                      "output": str(output_path.relative_to(MIRROR))})
    if len({(MIRROR / case["input"]).read_bytes() for case in cases}) != 21:
        raise ValueError(f"{problem_id}: inputs are not all distinct")
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("problem", nargs="+", help="Codeforces IDs with verified *_made directories")
    options = parser.parse_args()
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    rows = {(item.get("book"), item.get("id")): item for item in catalog["problems"]}
    for problem_id in options.problem:
        row = rows.get(("codeforces", problem_id))
        if row is None:
            raise SystemExit(f"unknown Codeforces problem: {problem_id}")
        cases = cases_for(problem_id)
        row.update({"tests": True, "test_count": len(cases), "test_cases": cases,
                    "data_status": "rebuilt_tests"})
        if problem_id in FLOAT_REBUILDS:
            row["comparison"] = "float_tokens"
    # Match index_tests.py: its canonical JSON product has no terminal newline.
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"activated {len(options.problem)} Codeforces rebuilds")


if __name__ == "__main__":
    main()
