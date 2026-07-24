#!/usr/bin/env python3
"""Select the first solution-backed missing-problem batch for T-002."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "openjudge" / "catalog.json"
OUTPUT = ROOT / "collab" / "t002-batch-001-manifest.json"
SKIPS = ROOT / "collab" / "t002-special-judge-skips.md"
SOURCES = [
    Path("/home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md"),
    Path("/home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md"),
]


def problem_number(value):
    match = re.search(r"(\d+)$", value)
    return int(match.group(1)) if match else None


def sections(path):
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    starts = [i for i, line in enumerate(lines) if re.match(r"^##\s+", line)]
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(lines)
        heading = lines[start]
        match = re.match(r"^##\s+[^\d]*(\d+)[:：]\s*(.*)$", heading)
        if not match:
            continue
        body = "\n".join(lines[start:end])
        codes = re.findall(r"```(?:python|py)?\s*\n(.*?)```", body, re.S | re.I)
        samples = re.findall(r"(?:样例输入|Sample Input|sample input)\s*\n+```\n(.*?)```", body, re.S | re.I)
        yield int(match.group(1)), match.group(2).strip(), body, codes, samples


def skip_numbers():
    if not SKIPS.exists():
        return set()
    return {
        int(match.group(1))
        for match in re.finditer(r"\|\s*0*(\d+)\s*\|", SKIPS.read_text(encoding="utf-8"))
    }


def main():
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    missing = {
        problem_number(item["id"])
        for item in catalog["problems"]
        if not item.get("test_cases")
    }
    skipped = skip_numbers()
    selected = {}
    for source in SOURCES:
        for number, title, body, codes, samples in sections(source):
            if number not in missing or number in skipped or number in selected or not codes or not samples:
                continue
            python_codes = [code for code in codes if "import " in code or "def " in code]
            if not python_codes:
                continue
            selected[number] = {
                "local_number": number,
                "title": title,
                "source": str(source),
                "source_heading": f"{number}: {title}",
                "python_solution_count": len(python_codes),
                "sample_input": samples[0].strip() + "\n",
            }
    batch = [selected[number] for number in sorted(selected)[:100]]
    result = {
        "batch": "T-002-001",
        "selection_rule": "catalog test_cases is empty, solution source exists, sample input exists, skip-list excluded",
        "excluded_skip_numbers": sorted(skipped),
        "candidate_count": len(selected),
        "selected_count": len(batch),
        "entries": batch,
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"selected {len(batch)} of {len(selected)} solution-backed missing problems")


if __name__ == "__main__":
    main()
