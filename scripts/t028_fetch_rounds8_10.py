#!/usr/bin/env python3
"""Fetch existing Accepted references for T-028 priorities 121 through 180."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

import oj_submit
from select_solution_batch import SOURCES, sections

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "collab" / "t028-candidates.json"
COLLECTION_NUMBERS = {1062, 1067, 1091, 1113, 1154, 1183, 1193, 1236,
                      2159, 2186, 2318, 2698, 2745, 3129}


def rows(page):
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", page, re.S | re.I):
        solution = re.search(r"/solution/(\d+)/", row)
        verdict = re.search(r'class="result[^>]*>\s*(?:<[^>]+>)*\s*([^<]+)', row)
        language = re.search(r'class="language"[^>]*>\s*<a[^>]*>([^<]+)', row)
        if solution and verdict and language:
            yield solution.group(1), html.unescape(verdict.group(1)).strip(), html.unescape(language.group(1)).strip()


def source_from_page(page):
    blocks = re.findall(r"<pre[^>]*>(.*?)</pre>", page, re.S | re.I)
    sources = [html.unescape(re.sub(r"<[^>]+>", "", block)) for block in blocks]
    sources = [source for source in sources if len(source.strip()) > 40]
    if len(sources) != 1:
        raise RuntimeError(f"expected one source block, found {len(sources)}")
    return "\n".join(line.rstrip() for line in sources[0].strip().splitlines()) + "\n"


def main():
    entries = [x for x in json.loads(CANDIDATES.read_text())["entries"]
               if 121 <= int(x["priority"]) <= 180 and int(x["number"]) not in COLLECTION_NUMBERS | {0}]
    session = oj_submit.Session().login()
    selected = []
    for index, entry in enumerate(entries, 1):
        number = int(entry["number"]); group = entry["submit_group"]; problem_id = entry["submit_id"]
        statistics = f"{oj_submit.HOST}/{group}/{problem_id}/statistics/"
        candidates = list(rows(session._get(statistics)))
        choice = next((x for x in candidates if x[1] == "Accepted" and x[2] == "Python3"), None)
        if choice is None:
            choice = next((x for x in candidates if x[1] == "Accepted" and x[2] == "G++"), None)
        if choice is None:
            raise RuntimeError(f"{number}: no Python3 or G++ Accepted submission")
        solution_id, _verdict, language = choice
        source_url = f"{oj_submit.HOST}/{group}/solution/{solution_id}/"
        source = source_from_page(session._get(source_url))
        marker = "#" if language == "Python3" else "//"
        suffix = ".py" if language == "Python3" else ".cpp"
        header = (f"{marker} External reference: {statistics}\n"
                  f"{marker} Accepted submission: {solution_id}\n"
                  f"{marker} Source: {source_url}\n"
                  f"{marker} License: not declared on the submission page; no license is inferred.\n\n")
        path = ROOT / "scripts" / f"t028_platform_accepted_{number:05d}{suffix}"
        path.write_text(header + source, encoding="utf-8")
        selected.append({"local_number": number, "group": group, "problem_id": problem_id,
                         "language": language, "solution_id": solution_id,
                         "source_path": str(path.relative_to(ROOT)), "source_url": source_url,
                         "statistics_url": statistics})
        print(f"[{index:2d}/{len(entries)}] {number:05d} {language} #{solution_id}", flush=True)
    output = ROOT / "collab" / "t028-rounds8-10-reference-selection.json"
    output.write_text(json.dumps({"task": "T-028", "priority_range": [121, 180],
                                  "collection_numbers": sorted(COLLECTION_NUMBERS),
                                  "excluded": [{"priority": 173, "local_number": 0,
                                                "reason": "permanent output-size exclusion"}],
                                  "platform_references": selected}, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
