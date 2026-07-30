#!/usr/bin/env python3
"""Identify and materialize verified GMyhf-owned OpenJudge test data."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

import oj_submit
from index_tests import SPECIAL_JUDGE_GLOBAL_NUMBERS

ROOT = Path(__file__).resolve().parents[1]
OPENJUDGE = ROOT / "data" / "openjudge"
OWNERSHIP = ROOT / "collab" / "gmyhf-editable-problems.json"
AUDIT = ROOT / "collab" / "gmyhf-data-audit.json"
LOCAL_JUDGE = ROOT / "collab" / "gmyhf-localjudge.json"
LOCAL_OUTPUT_LIMIT = 2 * 1024 * 1024
ARCHIVE_BUCKETS = {"1000-1999", "2000-2999", "3000-3682"}
RUNTIME_MARGIN_LIMIT = 0.75
# Claude reviewed the largest cases of every materialized problem in 961acb7e.
# These four do not retain enough wall-clock margin for stable local judging.
RUNTIME_MARGIN_REJECTIONS = {
    28190: {"max_case_ms": 4330, "case_limit_ms": 4000},
    30179: {"max_case_ms": 6500, "case_limit_ms": 5000},
    30908: {"max_case_ms": 15100, "case_limit_ms": 20000},
    30937: {"max_case_ms": 12710, "case_limit_ms": 10000},
}


class AdminProblemParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = None
        self.cell = None
        self.text = []
        self.operation_hrefs = []
        self.page_numbers = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "tr":
            self.row = {}
        elif tag == "td" and self.row is not None:
            self.cell = attrs.get("class", "")
            self.text = []
        elif tag == "a":
            href = attrs.get("href", "")
            match = re.search(r"[?&]page=(\d+)", href)
            if match:
                self.page_numbers.add(int(match.group(1)))
            if self.row is not None and self.cell == "operation":
                self.operation_hrefs.append(href)

    def handle_data(self, data):
        if self.cell:
            self.text.append(data)

    def handle_endtag(self, tag):
        if tag == "td" and self.cell and self.row is not None:
            self.row[self.cell] = " ".join("".join(self.text).split())
            if self.cell == "operation":
                self.row["operation_hrefs"] = list(self.operation_hrefs)
                self.operation_hrefs = []
            self.cell = None
            self.text = []
        elif tag == "tr" and self.row is not None:
            if self.row.get("number", "").isdigit():
                self.rows.append(self.row)
            self.row = None


def parse_admin_page(page):
    parser = AdminProblemParser()
    parser.feed(page)
    editable = []
    for row in parser.rows:
        edit_url = next((href for href in row.get("operation_hrefs", [])
                         if "/admin/problems/edit/" in href), None)
        if edit_url:
            editable.append({
                "global_number": int(row["number"]),
                "title": row.get("title", ""),
                "author": row.get("author", ""),
                "created": row.get("date", ""),
                "edit_url": edit_url,
            })
    return editable, parser.page_numbers


def fetch_ownership():
    session = oj_submit.Session().login()
    first = session._get(f"{oj_submit.HOST}/admin/problems/")
    entries, pages = parse_admin_page(first)
    max_page = max(pages, default=1)
    for page_number in range(2, max_page + 1):
        page = session._get(f"{oj_submit.HOST}/admin/problems/?page={page_number}")
        found, _ = parse_admin_page(page)
        for entry in found:
            entry["page"] = page_number
        entries.extend(found)
        if page_number % 20 == 0:
            print(f"admin pages: {page_number}/{max_page}", flush=True)
    by_number = {entry["global_number"]: entry for entry in entries}
    payload = {
        "policy": "operation column contains /admin/problems/edit/",
        "source": f"{oj_submit.HOST}/admin/problems/",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "editable_count": len(by_number),
        "entries": [by_number[number] for number in sorted(by_number)],
    }
    OWNERSHIP.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


ISSUE_FIELDS = ("missing_outputs", "mismatched", "excluded_invalid_inputs",
                "excluded_broken_oracles")


def validation_evidence():
    evidence = {}
    for report_path in sorted((ROOT / "collab").glob("*report.json")):
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for entry in report.get("entries", []):
            number = entry.get("global_number")
            archive = entry.get("archive_cross_check", {})
            if number is None or not archive.get("dirs"):
                continue
            issues = {field: archive.get(field, []) for field in ISSUE_FIELDS
                      if archive.get(field)}
            row = evidence.setdefault(int(number), {"passed_dirs": set(), "issues": [], "reports": set()})
            row["reports"].add(str(report_path.relative_to(ROOT)))
            if archive.get("status") == "passed" and not issues:
                row["passed_dirs"].update(archive["dirs"])
            else:
                row["issues"].append({
                    "report": str(report_path.relative_to(ROOT)),
                    "status": archive.get("status"),
                    "details": issues,
                })
    return evidence


def directory_pairs(source):
    """Pairs covered by archive_cross_check: directory root and data/, not rglob."""
    inputs = list(source.glob("*.in")) + list((source / "data").glob("*.in"))
    pairs = []
    for input_path in sorted(inputs):
        output_path = input_path.with_suffix(".out")
        if output_path.is_file():
            pairs.append((input_path, output_path))
    return pairs


def all_directory_pairs(source):
    pairs = []
    for input_path in sorted(source.rglob("*.in")):
        output_path = input_path.with_suffix(".out")
        if output_path.is_file():
            pairs.append((input_path, output_path))
    return pairs


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def made_directories():
    result = {}
    for path in OPENJUDGE.glob("tests/*/*_made"):
        match = re.match(r"0*(\d+)_made$", path.name)
        if match:
            result[int(match.group(1))] = path
    return result


def audit(materialize=False, replace_materialized=False):
    ownership = json.loads(OWNERSHIP.read_text(encoding="utf-8"))
    editable = {int(row["global_number"]): row for row in ownership["entries"]}
    catalog = json.loads((OPENJUDGE / "catalog.json").read_text(encoding="utf-8"))
    catalog_numbers = {int(row["global_number"]) for row in catalog["problems"]}
    made = made_directories()
    evidence = validation_evidence()
    rows = []
    totals = {"eligible": 0, "partial_eligible": 0, "requires_special_judge": 0,
              "original_problem": 0,
              "unverified": 0, "without_made": 0, "materialized": 0,
              "cases": 0, "bytes": 0}

    if materialize and replace_materialized:
        for destination in OPENJUDGE.glob("tests/*/*_GMyhf"):
            if destination.parent.parent != OPENJUDGE / "tests" or not destination.name.endswith("_GMyhf"):
                raise RuntimeError(f"unsafe replacement target {destination}")
            shutil.rmtree(destination)

    for number in sorted(set(editable) & catalog_numbers):
        made_dir = made.get(number)
        if made_dir is None:
            status = "without_made"
            totals[status] += 1
            rows.append({"global_number": number, "title": editable[number]["title"], "status": status})
            continue
        if number in SPECIAL_JUDGE_GLOBAL_NUMBERS:
            status = "requires_special_judge"
            totals[status] += 1
            rows.append({
                "global_number": number,
                "title": editable[number]["title"],
                "status": status,
                "made_dir": str(made_dir.relative_to(ROOT)),
                "reason": "multiple valid outputs require a special judge; exact token data disabled",
            })
            continue
        proof = evidence.get(number)
        pairs = []
        excluded_pairs = []
        issues = []
        if not proof:
            status = "unverified"
        elif proof["issues"]:
            status = "original_problem"
        elif not proof["passed_dirs"]:
            status = "unverified"
        else:
            missing = [path for path in proof["passed_dirs"]
                       if not (OPENJUDGE / path).is_dir()]
            status = "unverified" if missing else "eligible"
            if status == "eligible":
                for source_dir in proof["passed_dirs"]:
                    source = OPENJUDGE / source_dir
                    covered = directory_pairs(source)
                    pairs.extend((source_dir, inp, out) for inp, out in covered)
                    covered_inputs = {inp for inp, _out in covered}
                    for input_path, output_path in all_directory_pairs(source):
                        if input_path not in covered_inputs:
                            excluded_pairs.append({
                                "source_input": str(input_path.relative_to(OPENJUDGE)),
                                "source_output": str(output_path.relative_to(OPENJUDGE)),
                                "reason": "not covered by archive_cross_check glob scope",
                            })
                if made_dir.parent.name in ARCHIVE_BUCKETS:
                    status = "unverified"
                    issues.append({"status": "archive_bucket_excluded",
                                   "bucket": made_dir.parent.name})
                oversized = []
                for _source_dir, _input_path, output_path in pairs:
                    if output_path.stat().st_size > LOCAL_OUTPUT_LIMIT:
                        oversized.append({
                            "path": str(output_path.relative_to(OPENJUDGE)),
                            "bytes": output_path.stat().st_size,
                            "limit": LOCAL_OUTPUT_LIMIT,
                        })
                if oversized:
                    status = "original_problem"
                    issues.append({"status": "local_output_limit_exceeded", "details": oversized})
                runtime = RUNTIME_MARGIN_REJECTIONS.get(number)
                if runtime:
                    status = "original_problem"
                    issues.append({
                        "status": "insufficient_runtime_margin",
                        **runtime,
                        "ratio": round(runtime["max_case_ms"] / runtime["case_limit_ms"], 4),
                        "required_max_ratio": RUNTIME_MARGIN_LIMIT,
                        "source": "Claude review commit 961acb7e",
                    })
                if status == "eligible":
                    if not pairs:
                        status = "original_problem"
                        issues.append({"status": "no_exact-judge-safe_original_cases"})
                    elif excluded_pairs:
                        status = "partial_eligible"
        totals[status] += 1
        row = {
            "global_number": number,
            "title": editable[number]["title"],
            "status": status,
            "made_dir": str(made_dir.relative_to(ROOT)),
        }
        if proof:
            row["evidence_reports"] = sorted(proof["reports"])
            row["source_dirs"] = sorted(proof["passed_dirs"])
            row["issues"] = proof["issues"] + issues
        if excluded_pairs:
            row["excluded_pairs"] = excluded_pairs
        if status in {"eligible", "partial_eligible"}:
            if not pairs:
                row["status"] = "unverified"
                row["reason"] = "validated source directories contain no .in/.out pairs"
                totals[status] -= 1
                totals["unverified"] += 1
            else:
                row["case_count"] = len(pairs)
                row["byte_count"] = sum(inp.stat().st_size + out.stat().st_size
                                        for _, inp, out in pairs)
                totals["cases"] += row["case_count"]
                totals["bytes"] += row["byte_count"]
                destination = made_dir.with_name(made_dir.name[:-5] + "_GMyhf")
                if destination.is_dir():
                    row["materialized_dir"] = str(destination.relative_to(ROOT))
                    totals["materialized"] += 1
                elif materialize:
                    data = destination / "data"
                    data.mkdir(parents=True)
                    files = []
                    stable_indexes = {}
                    if excluded_pairs:
                        ordinal = 0
                        for source_dir in proof["passed_dirs"]:
                            source = OPENJUDGE / source_dir
                            for input_path, _output_path in all_directory_pairs(source):
                                stable_indexes[(source_dir, input_path)] = ordinal
                                ordinal += 1
                    for sequence, (source_dir, input_path, output_path) in enumerate(pairs):
                        index = stable_indexes.get((source_dir, input_path), sequence)
                        target_input = data / f"{index}.in"
                        target_output = data / f"{index}.out"
                        shutil.copyfile(input_path, target_input)
                        shutil.copyfile(output_path, target_output)
                        files.append({
                            "case": index,
                            "source_dir": source_dir,
                            "source_input": str(input_path.relative_to(OPENJUDGE)),
                            "source_output": str(output_path.relative_to(OPENJUDGE)),
                            "input_sha256": sha256(target_input),
                            "output_sha256": sha256(target_output),
                        })
                    provenance = {
                        "owner": "GMyhf",
                        "ownership_evidence": str(OWNERSHIP.relative_to(ROOT)),
                        "validation_reports": sorted(proof["reports"]),
                        "global_number": number,
                        "files": files,
                    }
                    if excluded_pairs:
                        provenance["excluded_pairs"] = excluded_pairs
                    (destination / "SOURCE.json").write_text(
                        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                    row["materialized_dir"] = str(destination.relative_to(ROOT))
                    totals["materialized"] += 1
        rows.append(row)

    payload = {
        "policy": ("editable admin problem; copy only archive_cross_check-covered pairs; "
                   "require local output/runtime margin and exact-judge-safe outputs"),
        "ownership_source": str(OWNERSHIP.relative_to(ROOT)),
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "totals": totals,
        "entries": rows,
    }
    AUDIT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(totals, ensure_ascii=False))
    return payload


def verify_active():
    sys.path.insert(0, str(ROOT))
    import judge

    audit_payload = json.loads(AUDIT.read_text(encoding="utf-8"))
    catalog = json.loads((OPENJUDGE / "catalog.json").read_text(encoding="utf-8"))["problems"]
    entries = []
    for index, row in enumerate((entry for entry in audit_payload["entries"]
                                 if entry.get("materialized_dir")), 1):
        number = int(row["global_number"])
        aliases = [entry for entry in catalog if int(entry["global_number"]) == number]
        problem = next((entry for entry in aliases if entry["book"] == "practice"), aliases[0])
        made_dir = ROOT / row["made_dir"]
        sources = (("python3", made_dir / "samplecode.py"),
                   ("cpp", made_dir / "samplecode.cpp"),
                   ("cpp", made_dir / "samplecode_ac.cpp"))
        language, source_path = next(((language, path) for language, path in sources if path.is_file()),
                                     (None, None))
        if source_path is None:
            result = {"status": "Missing Reference"}
        else:
            result = judge.judge(problem["book"], problem["id"], language,
                                 source_path.read_text(encoding="utf-8"),
                                 collect_case_times=True)
        entries.append({
            "global_number": number,
            "book": problem["book"],
            "problem": problem["id"],
            "language": language,
            "reference": str(source_path.relative_to(ROOT)) if source_path else None,
            **result,
        })
        if index % 20 == 0 or result.get("status") != "Accepted":
            print(f"local judge: {index}/{audit_payload['totals']['materialized']} "
                  f"{number} {result.get('status')}", flush=True)
    failed = [row for row in entries if row["status"] != "Accepted" or
              (row.get("timing_audit") or {}).get("status") != "passed"]
    payload = {
        "source": str(AUDIT.relative_to(ROOT)),
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "count": len(entries),
        "accepted": sum(row["status"] == "Accepted" for row in entries),
        "runtime_margin_policy": "every case must use at most 75% of its local CPU-second limit",
        "failed": failed,
        "entries": entries,
    }
    LOCAL_JUDGE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"local judge accepted: {payload['accepted']}/{payload['count']}")
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch-ownership", action="store_true")
    parser.add_argument("--materialize", action="store_true")
    parser.add_argument("--replace-materialized", action="store_true",
                        help="replace all existing _GMyhf directories; requires --materialize")
    parser.add_argument("--verify-active", action="store_true")
    args = parser.parse_args()
    if args.replace_materialized and not args.materialize:
        parser.error("--replace-materialized requires --materialize")
    if args.fetch_ownership:
        fetch_ownership()
    if not OWNERSHIP.exists():
        parser.error(f"missing {OWNERSHIP}; run with --fetch-ownership")
    audit(materialize=args.materialize, replace_materialized=args.replace_materialized)
    if args.verify_active:
        result = verify_active()
        if result["failed"]:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
