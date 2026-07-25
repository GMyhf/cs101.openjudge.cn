#!/usr/bin/env python3
"""Select the next solution-backed T-003 batch after T-002-001."""
import json
import re
from pathlib import Path

from build_001a import locate_source

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/openjudge/catalog.json"
SKIPS = ROOT / "collab/t002-special-judge-skips.md"
OUT = ROOT / "collab/t003-batch-002-manifest.json"
POOL_OUT = ROOT / "collab/t003-batch-002-candidates.json"
SOURCES = [
    Path("/home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md"),
    Path("/home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md"),
]


def sections(path):
    path = locate_source(str(path))
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    starts = [i for i, line in enumerate(lines) if re.match(r"^##\s+", line)]
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(lines)
        match = re.match(r"^##\s+[^\d]*(\d+)[:：]\s*(.*)$", lines[start])
        if not match:
            continue
        text = "\n".join(lines[start:end])
        codes = re.findall(r"```(?:python|py)?\s*\n(.*?)```", text, re.S | re.I)
        samples = re.findall(r"(?:样例输入|Sample Input|sample input)\s*\n+```\n(.*?)```", text, re.S | re.I)
        yield int(match.group(1)), match.group(2).strip(), codes, samples


def number(value):
    match = re.search(r"(\d+)$", value)
    return int(match.group(1)) if match else None


def skipped():
    return {int(x) for x in re.findall(r"\|\s*0*(\d+)\s*\|", SKIPS.read_text(encoding="utf-8"))}


def made_numbers():
    result = set()
    for path in (ROOT / "data/openjudge/tests").glob("*/*_made"):
        value = number(path.name[:-5])
        if value is not None:
            result.add(value)
    return result


def main():
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))["problems"]
    missing = {number(item["id"]) for item in catalog if not item.get("test_cases")}
    excluded = skipped() | made_numbers()
    candidates = {}
    for source in SOURCES:
        for local, title, codes, samples in sections(source):
            if local not in missing or local in excluded or local in candidates:
                continue
            usable = [code for code in codes if "import " in code or "def " in code]
            if not usable or not samples:
                continue
            candidates[local] = {
                "local_number": local,
                "title": title,
                "source": str(locate_source(str(source))),
                "source_heading": f"{local}: {title}",
                "python_solution_count": len(usable),
                "sample_input": samples[0].strip() + "\n",
                "selection_source": "solution-backed candidate pool",
            }
    ordered = [candidates[key] for key in sorted(candidates)]
    manifest = {
        "batch": "T-003-002",
        "selection_rule": "catalog test_cases empty, no existing _made directory, Python solution and sample present, special-judge skip excluded",
        "candidate_count": len(ordered),
        "selected_count": min(20, len(ordered)),
        "excluded_special_judge": sorted(skipped()),
        "excluded_existing_made": sorted(made_numbers()),
        "entries": ordered[:20],
    }
    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    POOL_OUT.write_text(json.dumps({"batch": "T-003-002", "candidates": ordered}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"selected {len(ordered[:20])} of {len(ordered)} candidates")
    print("batch:", ", ".join(f"{x['local_number']:05d}" for x in ordered[:20]))


if __name__ == "__main__":
    main()
