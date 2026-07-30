#!/usr/bin/env python3
"""Replace a phase-2 reference with another Accepted source that matches legacy outputs."""
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

import oj_submit
import t028_phase2_common as common
from t028_phase2_fetch_accepted import all_rows, source_from_page

ROOT = Path(__file__).resolve().parents[1]
SELECTION = ROOT / "collab/t028-phase2-reference-selection.json"
SOURCE_DIR = ROOT / "scripts/t028_phase2_accepted"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("number", type=int)
    parser.add_argument("--language", choices=("Python3", "G++"),
                        help="test only one language after the preferred language is exhausted")
    opts = parser.parse_args()
    payload = json.loads(SELECTION.read_text(encoding="utf-8"))
    entry = next(row for row in payload["entries"] if int(row["number"]) == opts.number)
    session = oj_submit.Session().login()
    candidates = all_rows(session, entry["statistics_url"])
    languages = (opts.language,) if opts.language else ("Python3", "G++")
    candidates = [row for language in languages for row in candidates
                  if row[1] == "Accepted" and row[2] == language]
    for solution_id, _verdict, language in candidates:
        if solution_id == str(entry.get("solution_id")):
            continue
        source_url = f"{oj_submit.HOST}/{entry['submit_group']}/solution/{solution_id}/"
        try:
            source = source_from_page(session._get(source_url))
            marker, suffix = ("#", ".py") if language == "Python3" else ("//", ".cpp")
            header = (f"{marker} External reference: {entry['statistics_url']}\n"
                      f"{marker} Accepted submission: {solution_id}\n"
                      f"{marker} Source: {source_url}\n"
                      f"{marker} License: not declared on the submission page; no license is inferred.\n\n")
            full_source = header + source
            with tempfile.TemporaryDirectory(prefix="t028-compatible-") as folder:
                command = common.compile_source(full_source, language, Path(folder))
                check = common.archive_check(command, entry)
            print(f"{solution_id} {language}: {check['status']}", flush=True)
            if check["status"] != "passed":
                continue
            old_path = ROOT / entry["source_path"]
            new_path = SOURCE_DIR / f"{opts.number:05d}{suffix}"
            if old_path != new_path and old_path.exists():
                old_path.unlink()
            new_path.write_text(full_source, encoding="utf-8")
            entry.update({"language": language, "solution_id": solution_id,
                          "source_path": str(new_path.relative_to(ROOT)),
                          "source_url": source_url,
                          "compatibility_check": check})
            SELECTION.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8")
            print(f"selected {solution_id} for {opts.number:05d}")
            return 0
        except Exception as exc:
            print(f"{solution_id} {language}: {type(exc).__name__}: {exc}", flush=True)
    print(f"no compatible Accepted source found for {opts.number:05d}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
