#!/usr/bin/env python3
"""Use existing platform Accepted submissions as external round6 oracles."""
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "collab/t004-round6-external-reference-2026-07-26.json"
sys.path.insert(0, str(ROOT / "scripts"))
from oj_submit import Session  # noqa: E402


def accepted_rows(page):
    rows = []
    for row in re.findall(r"<tr.*?</tr>", page, re.S | re.I):
        if not re.search(r'class="result-right"[^>]*>Accepted<', row, re.I):
            continue
        match = re.search(r'/practice/solution/(\d+)/', row)
        language = re.search(r'class="language".*?>([^<]+)<', row, re.S | re.I)
        if match and language:
            rows.append((language.group(1).strip(), match.group(1)))
    return rows


def source_from_page(page):
    match = re.search(r'<pre class="[^"]*">(.*?)</pre>', page, re.S | re.I)
    if not match:
        raise RuntimeError("solution page has no source pre block")
    return html.unescape(match.group(1)).replace("\r\n", "\n")


def run_source(source, language, input_data, work):
    if language == "Python3":
        command = [sys.executable, "main.py"]
    elif language == "G++":
        binary = work / "main"
        compiled = subprocess.run(
            ["g++", "-std=c++17", "-O2", "main.cpp", "-o", str(binary)],
            cwd=work, capture_output=True, text=True, timeout=30)
        if compiled.returncode:
            return None, "compile error"
        command = [str(binary)]
    else:
        raise RuntimeError(f"unsupported external language: {language}")
    try:
        result = subprocess.run(command, cwd=work, input=input_data,
                                capture_output=True, text=True, timeout=20)
    except subprocess.TimeoutExpired:
        return None, "local timeout"
    if result.returncode:
        return None, f"exit {result.returncode}"
    return result.stdout.split(), None


def main():
    session = Session().login()
    manifest = json.loads((ROOT / "collab/t004-round6-manifest.json").read_text())
    entries = []
    with tempfile.TemporaryDirectory(prefix="t004-r6-external-") as temp:
        temp = Path(temp)
        for item in manifest["entries"]:
            number = int(item["local_number"])
            stats = session._get(f"http://cs101.openjudge.cn/practice/{number:05d}/statistics/")
            rows = accepted_rows(stats)
            choice = next(((lang, sid) for lang, sid in rows if lang == "Python3"), None)
            if choice is None:
                choice = next(((lang, sid) for lang, sid in rows if lang == "G++"), None)
            row = {"local_number": f"{number:05d}", "accepted_found": bool(choice)}
            if choice is None:
                row["status"] = "NO_PREFERRED_ACCEPTED"
                entries.append(row)
                print(number, row["status"], flush=True)
                continue
            language, solution_id = choice
            source = source_from_page(session._get(
                f"http://cs101.openjudge.cn/practice/solution/{solution_id}/"))
            work = temp / f"{number:05d}"
            work.mkdir()
            filename = "main.py" if language == "Python3" else "main.cpp"
            (work / filename).write_text(source)
            made = next((ROOT / "data/openjudge/tests").glob(
                f"*/{number:05d}_made"))
            mismatches = []
            errors = []
            for case in sorted((made / "data").glob("*.in"), key=lambda p: int(p.stem)):
                expected = (made / "data" / f"{case.stem}.out").read_text().split()
                actual, error = run_source(source, language, case.read_text(), work)
                if error:
                    errors.append({"case": int(case.stem), "error": error})
                elif actual != expected:
                    mismatches.append({"case": int(case.stem),
                                       "expected_tokens": len(expected),
                                       "actual_tokens": len(actual)})
            row.update({"language": language, "solution_id": solution_id,
                        "cases": 21, "mismatches": mismatches, "errors": errors,
                        "status": "passed" if not mismatches and not errors else "failed"})
            entries.append(row)
            print(number, language, solution_id, row["status"], flush=True)
    REPORT.write_text(json.dumps({"batch": "T-004 round6 external Accepted references",
                                  "updated_at": datetime.now(timezone.utc).isoformat(),
                                  "entries": entries}, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
