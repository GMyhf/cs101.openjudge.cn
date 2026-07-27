#!/usr/bin/env python3
"""Refresh the cross-round pending-rework gate from the checked-in data."""
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import t004_common as common

manifest_path = ROOT / "collab/t004-round13-manifest.json"
report_path = ROOT / "collab/t004-round13-report.json"
manifest = json.loads(manifest_path.read_text())
report = json.loads(report_path.read_text())
report["pending_rework_status"] = common.pending_rework_status(
    manifest.get("pending_rework", []), ROOT / "data/openjudge/tests"
)
report["pending_rework_checked_at"] = datetime.now(timezone.utc).isoformat()
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(report["pending_rework_status"], ensure_ascii=False, indent=2))
