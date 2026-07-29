#!/usr/bin/env python3
"""Submit a T-028 round's reference solutions and record platform verdicts."""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("round", type=int)
    parser.add_argument("--only", help="comma-separated local problem numbers")
    parser.add_argument("--delay", type=float, default=0, help="seconds to wait between submissions")
    opts = parser.parse_args()
    only = {int(x) for x in opts.only.split(",")} if opts.only else None
    manifest_path = ROOT / "collab" / f"t028-round{opts.round}-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    jobs = [e for e in manifest["entries"] if only is None or int(e["local_number"]) in only]

    import oj_submit
    session = oj_submit.Session().login()
    output = ROOT / "collab" / f"t028-round{opts.round}-platform.json"
    previous = []
    if only and output.exists():
        previous = json.loads(output.read_text(encoding="utf-8")).get("results", [])
    results = [row for row in previous if int(row["local_number"]) not in (only or set())]
    for index, entry in enumerate(jobs, 1):
        if index > 1 and opts.delay:
            time.sleep(opts.delay)
        number = int(entry["local_number"])
        language = entry.get("reference_language", "Python3")
        suffix = "py" if language == "Python3" else "cpp"
        source = (ROOT / "data" / "openjudge" / entry["made_dir"] / f"samplecode.{suffix}").read_text(encoding="utf-8")
        group = entry.get("submit_group", "practice")
        problem_id = entry.get("submit_id") or entry.get("practice_id") or f"{number:05d}"
        error = None
        for _attempt in range(3):
            try:
                result = session.run(problem_id, source, language, group)
                error = None
                break
            except Exception as exc:  # Network resets and transient 5xx are common.
                error = f"{type(exc).__name__}: {exc}"[:160]
        if error:
            result = {"verdict": "SUBMIT_FAILED", "solution_id": None, "error": error}
        row = {"local_number": number, "global_number": entry.get("global_number"),
               "group": group, "problem_id": problem_id,
               "language": language, **result}
        results.append(row)
        results.sort(key=lambda item: next(i for i, entry in enumerate(manifest["entries"])
                                           if int(entry["local_number"]) == int(item["local_number"])))
        print(f"[{index:2d}/{len(jobs)}] {number}: {result['verdict']} "
              f"#{result['solution_id']}", flush=True)
        output.write_text(json.dumps({"task": "T-028", "round": opts.round,
            "updated_at": datetime.now(timezone.utc).isoformat(), "results": results},
            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    rejected = [r["local_number"] for r in results if r["verdict"] != "Accepted"]
    payload = {"task": "T-028", "round": opts.round,
               "updated_at": datetime.now(timezone.utc).isoformat(),
               "accepted": len(results) - len(rejected), "total": len(results),
               "not_accepted": rejected, "results": results}
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output.relative_to(ROOT)}")
    return 1 if rejected else 0


if __name__ == "__main__":
    raise SystemExit(main())
