#!/usr/bin/env python3
"""Submit the T-002/T-003 generated reference programs to cs101.

Credentials are read by ``oj_submit.Session`` from OJ_USER/OJ_PASS.  This
script deliberately records platform results only; it never stores secrets.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "collab/t002-t003-platform-check-2026-07-26.json"
REPORTS = [
    "collab/t002-001a-report.json", "collab/t002-001b-report.json",
    "collab/t002-001c-report.json", "collab/t002-001d-report.json",
    "collab/t003-002-report.json", "collab/t003-002-round2-report.json",
    "collab/t003-002-round3-report.json", "collab/t003-002-round4-report.json",
    "collab/t003-002-round5-report.json",
]
sys.path.insert(0, str(ROOT / "scripts"))
from oj_submit import Session, escalate  # noqa: E402


def made_dir(number):
    matches = sorted((ROOT / "data/openjudge/tests").glob(f"*/{number:05d}_made"))
    if len(matches) != 1:
        raise RuntimeError(f"{number}: expected one _made directory, found {matches}")
    return matches[0]


def targets():
    seen = {}
    for filename in REPORTS:
        doc = json.loads((ROOT / filename).read_text(encoding="utf-8"))
        for entry in doc.get("entries", []):
            number = int(entry["local_number"])
            if number in seen:
                continue
            directory = made_dir(number)
            source = directory / "samplecode.py"
            if not source.exists():
                raise RuntimeError(f"{number}: missing samplecode.py")
            seen[number] = {"local_number": number, "source_report": filename,
                            "source_path": str(source.relative_to(ROOT)),
                            "group": "practice", "source": source.read_text(encoding="utf-8")}
    return [seen[number] for number in sorted(seen)]


def save(rows, started):
    output = {"batch": "T-002/T-003 platform rescan",
              "started_at": started, "updated_at": datetime.now(timezone.utc).isoformat(),
              "count": len(rows), "entries": [{k: v for k, v in row.items() if k != "source"}
                                                 for row in rows]}
    REPORT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    if not os.environ.get("OJ_USER") or not os.environ.get("OJ_PASS"):
        raise SystemExit("需要 OJ_USER / OJ_PASS 环境变量")
    all_targets = targets()
    started = datetime.now(timezone.utc).isoformat()
    previous = json.loads(REPORT.read_text(encoding="utf-8")) if REPORT.exists() else {"entries": []}
    old = {row["local_number"]: row for row in previous.get("entries", [])}
    session = Session().login()
    rows = []
    for index, target in enumerate(all_targets, 1):
        number = target["local_number"]
        if number in old and old[number].get("final") not in (None, "TIMEOUT_POLLING"):
            rows.append(old[number])
            print(f"[{index}/{len(all_targets)}] {number}: keep {old[number]['final']}", flush=True)
            continue
        row = {k: v for k, v in target.items() if k != "source"}
        try:
            result = escalate(session, f"{number:05d}", target["source"], group=target["group"])
            row.update(result)
        except RuntimeError as exc:
            row.update({"final": "NOT_SUBMITTABLE", "error": str(exc)})
        rows.append(row)
        save(rows, started)
        print(f"[{index}/{len(all_targets)}] {number}: {row['final']}", flush=True)
    save(rows, started)


if __name__ == "__main__":
    main()
