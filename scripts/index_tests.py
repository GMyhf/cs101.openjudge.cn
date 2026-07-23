#!/usr/bin/env python3
"""Index OpenJudge .in/.out pairs according to numeric problem IDs."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "data" / "openjudge"
TESTS = MIRROR / "tests"
BUCKETS = {"1000-1999", "2000-2999", "3000-3682", "4000-8210", "10000-19963", "20000-29982", "30000-"}

def numeric(value):
    match = re.search(r"(\d+)$", value)
    return int(match.group(1)) if match else None

def directory_numeric(value):
    match = re.search(r"(\d+)", value)
    return int(match.group(1)) if match else None

def main():
    by_number = {}
    for bucket in BUCKETS:
        root = TESTS / bucket
        if not root.is_dir(): continue
        for directory in root.iterdir():
            if not directory.is_dir(): continue
            number = directory_numeric(directory.name)
            if number is None: continue
            pairs = []
            inputs = {p.stem: p for p in directory.glob("*.in")}
            outputs = {p.stem: p for p in directory.glob("*.out")}
            for stem in sorted(inputs.keys() & outputs.keys()):
                pairs.append({"input": str(inputs[stem].relative_to(MIRROR)), "output": str(outputs[stem].relative_to(MIRROR))})
            if pairs:
                by_number.setdefault(number, []).extend(pairs)

    catalog_path = MIRROR / "catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    matched = 0
    for item in catalog["problems"]:
        number = numeric(item["id"])
        cases = by_number.get(number, [])
        item["tests"] = bool(cases)
        item["test_count"] = len(cases)
        item["test_cases"] = cases
        if cases: matched += 1
    (MIRROR / "test_index.json").write_text(json.dumps({"buckets": sorted(BUCKETS), "matched_catalog_problems": matched, "indexed_problem_numbers": len(by_number), "catalog": catalog}, ensure_ascii=False, indent=2), encoding="utf-8")
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"indexed {len(by_number)} numeric problem directories; {matched}/{len(catalog['problems'])} catalog problems have tests")

if __name__ == "__main__": main()
