#!/usr/bin/env python3
"""Fetch platform-Accepted references for T-028 priorities 181 through 252."""
from __future__ import annotations

import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import oj_submit

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "collab" / "t028-candidates.json"
OUTPUT = ROOT / "collab" / "t028-rounds11-14-reference-selection.json"


def rows(page):
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", page, re.S | re.I):
        solution = re.search(r"/solution/(\d+)/", row)
        verdict = re.search(r'class="result[^>]*>\s*(?:<[^>]+>)*\s*([^<]+)', row)
        language = re.search(r'class="language"[^>]*>\s*<a[^>]*>([^<]+)', row)
        if solution and verdict and language:
            yield (solution.group(1), html.unescape(verdict.group(1)).strip(),
                   html.unescape(language.group(1)).strip())


def all_rows(session, statistics):
    first = session._get(statistics)
    pages = [int(value) for value in re.findall(r'[?&]page=(\d+)', first)]
    found = list(rows(first))
    for page in range(2, max(pages, default=1) + 1):
        found.extend(rows(session._get(f"{statistics}?page={page}")))
    return found


def source_from_page(page):
    blocks = re.findall(r"<pre[^>]*>(.*?)</pre>", page, re.S | re.I)
    sources = [html.unescape(re.sub(r"<[^>]+>", "", block)) for block in blocks]
    sources = [source for source in sources if len(source.strip()) > 40]
    if len(sources) != 1:
        raise RuntimeError(f"expected one source block, found {len(sources)}")
    return "\n".join(line.rstrip() for line in sources[0].strip().splitlines()) + "\n"


def main():
    entries = [entry for entry in json.loads(CANDIDATES.read_text(encoding="utf-8"))["entries"]
               if entry["tier"] == 1 and 181 <= int(entry["priority"]) <= 252]
    session = oj_submit.Session().login()
    selected = []
    for index, entry in enumerate(entries, 1):
        number = int(entry["number"])
        group, problem_id = entry["submit_group"], entry["submit_id"]
        statistics = f"{oj_submit.HOST}/{group}/{problem_id}/statistics/"
        candidates = all_rows(session, statistics)
        choice = next((row for row in candidates
                       if row[1] == "Accepted" and row[2] == "Python3"), None)
        if choice is None:
            choice = next((row for row in candidates
                           if row[1] == "Accepted" and row[2] == "G++"), None)
        if choice is None:
            raise RuntimeError(f"{number}: no Python3 or G++ Accepted submission")
        solution_id, _verdict, language = choice
        source_url = f"{oj_submit.HOST}/{group}/solution/{solution_id}/"
        source = source_from_page(session._get(source_url))
        marker, suffix = ("#", ".py") if language == "Python3" else ("//", ".cpp")
        header = (f"{marker} External reference: {statistics}\n"
                  f"{marker} Accepted submission: {solution_id}\n"
                  f"{marker} Source: {source_url}\n"
                  f"{marker} License: not declared on the submission page; no license is inferred.\n\n")
        path = ROOT / "scripts" / f"t028_platform_accepted_{number:05d}{suffix}"
        path.write_text(header + source, encoding="utf-8")
        selected.append({"priority": entry["priority"], "local_number": number,
                         "global_number": entry["global_number"], "group": group,
                         "problem_id": problem_id, "language": language,
                         "solution_id": solution_id,
                         "source_path": str(path.relative_to(ROOT)),
                         "source_url": source_url, "statistics_url": statistics})
        print(f"[{index:2d}/{len(entries)}] priority {entry['priority']} "
              f"{group}/{problem_id} {language} #{solution_id}", flush=True)
    OUTPUT.write_text(json.dumps({"task": "T-028", "priority_range": [181, 252],
                                  "updated_at": datetime.now(timezone.utc).isoformat(),
                                  "platform_references": selected},
                                 ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({len(selected)} references)")


if __name__ == "__main__":
    main()
