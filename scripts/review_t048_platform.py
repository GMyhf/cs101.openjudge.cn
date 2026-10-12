#!/usr/bin/env python3
"""Revalidate T-048 references on OpenJudge; resume from recorded submissions."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from oj_submit import FINAL_VERDICTS, Session

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "collab/t048-platform-review.json"
NUMBERS = tuple(str(number) for number in range(31293, 31299))


def main():
    rows = json.loads(REPORT.read_text(encoding="utf-8"))["results"] if REPORT.exists() else []
    session = Session().login()

    def save():
        REPORT.write_text(json.dumps({
            "task": "T-048", "updated_at": datetime.now(timezone.utc).isoformat(),
            "total": len(NUMBERS),
            "accepted": sum(row.get("verdict") == "Accepted" for row in rows),
            "results": rows,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for number in NUMBERS:
        source_path = ROOT / f"data/openjudge/tests/30000-/{number}_made/samplecode.py"
        source = source_path.read_text(encoding="utf-8")
        digest = hashlib.sha256(source.encode()).hexdigest()
        row = next((row for row in rows if row["problem_id"] == number
                    and row["source_sha256"] == digest), None)
        if row and row.get("verdict") in FINAL_VERDICTS:
            print(f"{number}: {row['verdict']} #{row['solution_id']} (recorded)", flush=True)
            continue
        if row is None:
            solution_id = session.submit(number, source, "Python3")
            row = {"problem_id": number, "group": "practice", "language": "Python3",
                   "source_path": str(source_path.relative_to(ROOT)),
                   "source_sha256": digest, "solution_id": solution_id,
                   "verdict": "PENDING"}
            rows[:] = [old for old in rows if old["problem_id"] != number]
            rows.append(row)
            save()
            print(f"{number}: submitted #{solution_id}", flush=True)
        row.update(session.poll(row["solution_id"]))
        save()
        print(f"{number}: {row['verdict']} #{row['solution_id']}", flush=True)
    return 0 if len(rows) == len(NUMBERS) and all(row["verdict"] == "Accepted" for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
