#!/usr/bin/env python3
"""Build the machine-readable completion report for T-004 round 19.

Round 19 is a historical cleanup: it records the two entries recovered by the
full report sweep, while the actual data is rebuilt by the owning round
builders.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "collab" / "t004-round19-report.json"


def entry(path: str, number: int) -> dict:
    report = json.loads((ROOT / path).read_text(encoding="utf-8"))
    for row in report["entries"]:
        if int(row["local_number"]) == number:
            if row["self_audit"]["failed"]:
                raise SystemExit(f"{path}: {number} still has failed checks")
            return row
    raise SystemExit(f"{path}: missing {number}")


def main() -> None:
    r4140 = entry("collab/t004-round5-report.json", 4140)
    r15291 = entry("collab/t004-round9-report.json", 15291)
    if r4140["test_cases"] != 1:
        raise SystemExit("4140 must have exactly one test case")
    if r4140["self_audit"]["constant_output_probe"]["status"] != "exempted":
        raise SystemExit("4140 must be explicitly exempted")
    if r15291["self_audit"]["constant_output_probe"]["status"] != "rejected":
        raise SystemExit("15291 constant-output probe must be rejected")
    if r15291["self_audit"]["distinct_cases"]["status"] != "passed":
        raise SystemExit("15291 distinct-case check must pass")

    payload = {
        "batch": "T-004 round19 (historical cleanup)",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "count": 2,
        "entries": [
            {
                "local_number": 4140,
                "source_round": 5,
                "status": "passed",
                "test_cases": r4140["test_cases"],
                "constant_output_probe": r4140["self_audit"]["constant_output_probe"],
                "distinct_cases": r4140["self_audit"]["distinct_cases"],
                "constraint_checklist": r4140["self_audit"]["constraint_checklist"],
                "sample_is_case_zero": r4140["self_audit"]["sample_is_case_zero"],
                "samplecode_recompute": r4140["self_audit"]["samplecode_recompute"],
                "byte_reproduction": r4140["self_audit"]["byte_reproduction"],
            },
            {
                "local_number": 15291,
                "source_round": 9,
                "status": "passed",
                "test_cases": r15291["test_cases"],
                "nonzero_generated_outputs": sum(
                    1 for i in range(1, 21)
                    if (ROOT / "data/openjudge/tests/10000-19963/15291_made/data" / f"{i}.out")
                    .read_text(encoding="utf-8").split() != ["0"]
                ),
                "constant_output_probe": r15291["self_audit"]["constant_output_probe"],
                "distinct_cases": r15291["self_audit"]["distinct_cases"],
                "constraint_checklist": r15291["self_audit"]["constraint_checklist"],
                "sample_is_case_zero": r15291["self_audit"]["sample_is_case_zero"],
                "samplecode_recompute": r15291["self_audit"]["samplecode_recompute"],
                "byte_reproduction": r15291["self_audit"]["byte_reproduction"],
            },
        ],
        "failed": [],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
