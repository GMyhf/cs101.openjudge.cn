#!/usr/bin/env python3
"""Backfill reviewable statement anchors for T-028 phase-2 rounds 15-19."""
from __future__ import annotations

import importlib
import json
from pathlib import Path

import t028_phase2_common as common

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    filled = 0
    for round_number in range(15, 20):
        module = importlib.import_module(f"t028_phase2_round{round_number}")
        manifest_path = ROOT / "collab" / f"t028-round{round_number}-manifest.json"
        report_path = ROOT / "collab" / f"t028-round{round_number}-report.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        report = json.loads(report_path.read_text(encoding="utf-8"))
        entries = {int(row["local_number"]): row for row in manifest["entries"]}
        for row in report["entries"]:
            number = int(row["local_number"])
            entry = entries[number]
            row["input_domain"] = {
                "statement_quote": common.input_domain_quote(entry, module, number),
                "generated_extremes": common.generated_extremes(
                    common.OPENJUDGE / entry["made_dir"] / "data"),
            }
            filled += 1
        report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if filled != 100:
        raise SystemExit(f"expected 100 phase-2 entries, backfilled {filled}")
    print(f"backfilled input_domain for {filled} entries in rounds 15-19")


if __name__ == "__main__":
    main()
