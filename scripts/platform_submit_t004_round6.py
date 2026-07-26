#!/usr/bin/env python3
"""Submit T-004 round6 reference programs and record platform verdicts."""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collab/t004-round6-manifest.json"
REPORT = ROOT / "collab/t004-round6-platform-2026-07-26.json"
sys.path.insert(0, str(ROOT / "scripts"))
from oj_submit import Session, escalate  # noqa: E402


def main():
    if not os.environ.get("OJ_USER") or not os.environ.get("OJ_PASS"):
        raise SystemExit("需要 OJ_USER / OJ_PASS 环境变量")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    only = {int(x) for x in os.environ.get("T004_ONLY", "").split(",") if x}
    targets = []
    for item in manifest["entries"]:
        number = int(item["local_number"])
        if only and number not in only:
            continue
        made = next((ROOT / "data/openjudge/tests").glob(f"*/{number:05d}_made"))
        cpp = made / "samplecode.cpp"
        py = made / "samplecode.py"
        if cpp.exists():
            targets.append((number, cpp.read_text(encoding="utf-8"), "G++"))
        elif py.exists():
            targets.append((number, py.read_text(encoding="utf-8"), "Python3"))
        else:
            raise SystemExit(f"{number}: no samplecode.cpp or samplecode.py")

    started = datetime.now(timezone.utc).isoformat()
    session = Session().login()
    previous = json.loads(REPORT.read_text(encoding="utf-8")) if REPORT.exists() else {"entries": []}
    old = {row["local_number"]: row for row in previous.get("entries", [])}
    rows = [old[number] for number in sorted(old)
            if not only or int(number) not in only]
    for index, (number, source, language) in enumerate(targets, 1):
        row = {"local_number": f"{number:05d}", "group": "practice",
               "source_language": language}
        try:
            if language == "G++":
                result = session.run(f"{number:05d}", source, "G++", group="practice")
                row.update({"final": result["verdict"],
                            "attempts": [{"language": "G++", **result}]})
            else:
                row.update(escalate(session, f"{number:05d}", source,
                                    tiers=("Python3", "PyPy3"), group="practice"))
        except Exception as exc:  # keep the batch moving; report the exact issue
            row.update({"final": "SUBMIT_ERROR", "error": str(exc)})
        rows.append(row)
        print(f"[{index}/{len(targets)}] {number:05d}: {row['final']}", flush=True)

    report = {
        "batch": "T-004 round6 platform check",
        "started_at": started,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(rows),
        "entries": rows,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")


if __name__ == "__main__":
    main()
