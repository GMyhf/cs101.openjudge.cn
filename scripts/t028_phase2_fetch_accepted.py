#!/usr/bin/env python3
"""Fetch existing platform-Accepted references for T-028 phase 2."""
from __future__ import annotations

import argparse
import html
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import oj_submit

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "collab" / "t028-phase2-candidates.json"
OUTPUT = ROOT / "collab" / "t028-phase2-reference-selection.json"
SOURCE_DIR = ROOT / "scripts" / "t028_phase2_accepted"


def rows(page: str):
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", page, re.S | re.I):
        solution = re.search(r"/solution/(\d+)/", row)
        verdict = re.search(r'class="result[^>]*>\s*(?:<[^>]+>)*\s*([^<]+)', row)
        language = re.search(r'class="language"[^>]*>\s*<a[^>]*>([^<]+)', row)
        if solution and verdict and language:
            yield (solution.group(1), html.unescape(verdict.group(1)).strip(),
                   html.unescape(language.group(1)).strip())


def all_rows(session, statistics: str):
    first = session._get(statistics)
    pages = [int(value) for value in re.findall(r"[?&]page=(\d+)", first)]
    found = list(rows(first))
    for page in range(2, max(pages, default=1) + 1):
        found.extend(rows(session._get(f"{statistics}?page={page}")))
    return found


def source_from_page(page: str) -> str:
    blocks = re.findall(r"<pre[^>]*>(.*?)</pre>", page, re.S | re.I)
    sources = [html.unescape(re.sub(r"<[^>]+>", "", block)) for block in blocks]
    sources = [source for source in sources if len(source.strip()) > 40]
    if len(sources) != 1:
        raise RuntimeError(f"expected one source block, found {len(sources)}")
    return "\n".join(line.rstrip() for line in sources[0].strip().splitlines()) + "\n"


def save(payload: dict) -> None:
    payload["updated_at"] = datetime.now(timezone.utc).isoformat()
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--round", type=int, help="fetch one round only")
    parser.add_argument("--delay", type=float, default=0.15)
    opts = parser.parse_args()
    candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))["entries"]
    if opts.round is not None:
        candidates = [row for row in candidates if int(row["round"]) == opts.round]

    previous = {int(row["priority"]): row for row in (
        json.loads(OUTPUT.read_text(encoding="utf-8")).get("entries", [])
        if OUTPUT.exists() else [])}
    payload = {"task": "T-028", "phase": 2,
               "selection_policy": "existing Accepted Python3, then existing Accepted G++",
               "entries": list(previous.values())}
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    session = oj_submit.Session().login()
    failures = 0
    for index, entry in enumerate(candidates, 1):
        priority = int(entry["priority"])
        if previous.get(priority, {}).get("status") == "selected":
            print(f"[{index:3d}/{len(candidates)}] priority {priority}: already selected", flush=True)
            continue
        if index > 1 and opts.delay:
            time.sleep(opts.delay)
        number = int(entry["number"])
        group, problem_id = entry["submit_group"], entry["submit_id"]
        statistics = f"{oj_submit.HOST}/{group}/{problem_id}/statistics/"
        try:
            candidates_on_platform = all_rows(session, statistics)
            choice = next((row for row in candidates_on_platform
                           if row[1] == "Accepted" and row[2] == "Python3"), None)
            if choice is None:
                choice = next((row for row in candidates_on_platform
                               if row[1] == "Accepted" and row[2] == "G++"), None)
            if choice is None:
                result = {**entry, "status": "missing",
                          "reason": "no existing Accepted Python3 or G++ submission",
                          "statistics_url": statistics}
                failures += 1
            else:
                solution_id, _verdict, language = choice
                source_url = f"{oj_submit.HOST}/{group}/solution/{solution_id}/"
                source = source_from_page(session._get(source_url))
                marker, suffix = ("#", ".py") if language == "Python3" else ("//", ".cpp")
                header = (f"{marker} External reference: {statistics}\n"
                          f"{marker} Accepted submission: {solution_id}\n"
                          f"{marker} Source: {source_url}\n"
                          f"{marker} License: not declared on the submission page; no license is inferred.\n\n")
                path = SOURCE_DIR / f"{number:05d}{suffix}"
                path.write_text(header + source, encoding="utf-8")
                result = {**entry, "status": "selected", "language": language,
                          "solution_id": solution_id,
                          "source_path": str(path.relative_to(ROOT)),
                          "source_url": source_url, "statistics_url": statistics}
        except Exception as exc:
            result = {**entry, "status": "fetch_failed",
                      "reason": f"{type(exc).__name__}: {exc}"[:240],
                      "statistics_url": statistics}
            failures += 1
        previous[priority] = result
        payload["entries"] = [previous[key] for key in sorted(previous)]
        save(payload)
        detail = result.get("language") or result.get("reason")
        print(f"[{index:3d}/{len(candidates)}] priority {priority} {number:05d}: "
              f"{result['status']} {detail}", flush=True)

    payload["entries"] = [previous[key] for key in sorted(previous)]
    payload["selected"] = sum(row["status"] == "selected" for row in payload["entries"])
    payload["unresolved"] = [row["priority"] for row in payload["entries"]
                             if row["status"] != "selected"]
    save(payload)
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {payload['selected']} selected, "
          f"{len(payload['unresolved'])} unresolved")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
