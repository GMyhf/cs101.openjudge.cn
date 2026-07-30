#!/usr/bin/env python3
"""Shared builder for T-028 phase 2 non-_made test replacements."""
from __future__ import annotations

import html
import inspect
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import t004_common as audit_common

ROOT = Path(__file__).resolve().parents[1]
OPENJUDGE = ROOT / "data" / "openjudge"
CANDIDATES = ROOT / "collab" / "t028-phase2-candidates.json"
SELECTION = ROOT / "collab" / "t028-phase2-reference-selection.json"


def clean(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.strip().splitlines()) + "\n"


def page_sample(entry: dict, label: str) -> str:
    page = (OPENJUDGE / "pages" / f"{entry['submit_group']}__{entry['submit_id']}.html")
    text = page.read_text(encoding="utf-8", errors="replace")
    match = re.search(rf"<dt>\s*{label}\s*</dt>\s*<dd>(.*?)</dd>", text, re.S | re.I)
    if not match:
        return ""
    blocks = re.findall(r"<pre[^>]*>(.*?)</pre>", match.group(1), re.S | re.I)
    value = blocks[0] if blocks else match.group(1)
    value = re.sub(r"^\s*<b>.*?</b>\s*", "", value, count=1, flags=re.S | re.I)
    value = re.split(r"<b>.*?</b>", value, maxsplit=1, flags=re.S | re.I)[0]
    value = html.unescape(re.sub(r"<[^>]+>", "", value)).replace("\r", "")
    return "" if value.strip() in {"", "无", "None"} else clean(value)


def compile_source(source: str, language: str, folder: Path) -> list[str]:
    if language == "Python3":
        path = folder / "solution.py"
        path.write_text(source, encoding="utf-8")
        return [sys.executable, "-I", str(path)]
    path, binary = folder / "solution.cpp", folder / "solution"
    path.write_text(source, encoding="utf-8")
    result = subprocess.run(["g++", "-std=c++20", "-O2", "-pipe", str(path), "-o", str(binary)],
                            capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError(result.stderr[-1000:])
    return [str(binary)]


def run(command: list[str], input_text: str) -> str:
    result = subprocess.run(command, input=input_text, text=True, capture_output=True,
                            timeout=120)
    if result.returncode:
        raise RuntimeError((result.stderr or result.stdout)[-1000:])
    return "\n".join(line.rstrip() for line in result.stdout.rstrip().splitlines()) + "\n"


def generated_extremes(data: Path) -> dict | None:
    values = []
    for path in sorted(data.glob("*.in")):
        for token in path.read_text(encoding="utf-8", errors="replace").split():
            if re.fullmatch(r"-?\d{1,18}", token):
                values.append(int(token))
    return ({"max_int": max(values), "min_int": min(values)}
            if values else {"integer_tokens": 0})


def archive_check(command: list[str], entry: dict) -> dict:
    paths = []
    for relative in entry["source_dirs"]:
        directory = OPENJUDGE / relative
        paths.extend(directory.glob("*.in"))
        paths.extend((directory / "data").glob("*.in"))
    paths = sorted(set(paths))
    missing, mismatched = [], []
    for path in paths:
        output = path.with_suffix(".out")
        if not output.exists():
            missing.append(str(path.relative_to(OPENJUDGE)))
            continue
        try:
            got = run(command, path.read_text(encoding="utf-8", errors="replace"))
        except Exception as exc:
            mismatched.append({"input": str(path.relative_to(OPENJUDGE)),
                               "reason": f"{type(exc).__name__}: {exc}"[:160]})
            continue
        expected = output.read_text(encoding="utf-8", errors="replace")
        if got.replace("\x1a", " ").split() != expected.replace("\x1a", " ").split():
            mismatched.append({"input": str(path.relative_to(OPENJUDGE)),
                               "expected": expected.split()[:8], "actual": got.split()[:8]})
    usable = len(paths) - len(missing)
    return {"status": "passed" if usable and not mismatched else "FAILED",
            "cases": usable, "dirs": entry["source_dirs"],
            "missing_outputs": missing, "mismatched": mismatched,
            "method": "existing Accepted source recomputed every legacy input; output tokens compared"}


def write_producecase(made: Path, generator_module, number: int, source: str,
                      language: str, sample: str) -> None:
    generator_source = Path(inspect.getsourcefile(generator_module)).read_text(encoding="utf-8")
    generator_source = generator_source.split("\nif __name__", 1)[0]
    program = (generator_source + "\n\n" +
        "import subprocess as _subprocess, sys as _sys, tempfile as _tempfile\n"
        "from pathlib import Path as _Path\n" +
        f"REFERENCE={source!r}\nLANGUAGE={language!r}\nNUMBER={number}\nSAMPLE={sample!r}\n" +
        "def _build():\n"
        " with _tempfile.TemporaryDirectory() as folder:\n"
        "  folder=_Path(folder);src=folder/('s.py' if LANGUAGE=='Python3' else 's.cpp');src.write_text(REFERENCE)\n"
        "  cmd=[_sys.executable,'-I',str(src)]\n"
        "  if LANGUAGE!='Python3':\n"
        "   exe=folder/'s';_subprocess.run(['g++','-std=c++20','-O2','-pipe',str(src),'-o',str(exe)],check=True);cmd=[str(exe)]\n"
        "  out=_Path('data');out.mkdir(exist_ok=True)\n"
        "  for path in out.glob('*'):path.unlink()\n"
        "  cases=([SAMPLE] if SAMPLE else [])+[generate(NUMBER,seed) for seed in range(1,21)]\n"
        "  for index,case in enumerate(cases):\n"
        "   result=_subprocess.run(cmd,input=case,text=True,capture_output=True,timeout=120,check=True)\n"
        "   answer='\\n'.join(line.rstrip() for line in result.stdout.rstrip().splitlines())+'\\n'\n"
        "   (out/f'{index}.in').write_text(case);(out/f'{index}.out').write_text(answer)\n"
        "if __name__=='__main__':_build()\n")
    (made / "producecase.py").write_text(program, encoding="utf-8")


def build_round(round_number: int, generator_module) -> None:
    all_candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))["entries"]
    entries = [row for row in all_candidates if int(row["round"]) == round_number]
    expected = list(range((round_number - 15) * 20 + 1,
                          min((round_number - 14) * 20, len(all_candidates)) + 1))
    if [int(row["priority"]) for row in entries] != expected:
        raise SystemExit(f"round {round_number} priority selection changed")
    numbers = {int(row["number"]) for row in entries}
    if numbers != set(generator_module.NUMBERS):
        raise SystemExit(f"round {round_number} generator coverage mismatch: "
                         f"missing={sorted(numbers - set(generator_module.NUMBERS))}, "
                         f"extra={sorted(set(generator_module.NUMBERS) - numbers)}")
    references = {int(row["priority"]): row for row in
                  json.loads(SELECTION.read_text(encoding="utf-8"))["entries"]}
    platform_path = ROOT / "collab" / f"t028-round{round_number}-platform.json"
    platform = ({int(row["local_number"]): row for row in
                 json.loads(platform_path.read_text(encoding="utf-8")).get("results", [])}
                if platform_path.exists() else {})
    manifest, report = [], []
    for entry in entries:
        number, priority = int(entry["number"]), int(entry["priority"])
        reference = references[priority]
        if reference["status"] != "selected":
            raise SystemExit(f"priority {priority}: reference is {reference['status']}")
        source = (ROOT / reference["source_path"]).read_text(encoding="utf-8")
        language = reference["language"]
        sample = generator_module.SAMPLE_INPUTS.get(number, page_sample(entry, "样例输入"))
        sample_output = generator_module.SAMPLE_OUTPUTS.get(number, page_sample(entry, "样例输出"))
        with tempfile.TemporaryDirectory(prefix="t028-phase2-") as folder:
            command = compile_source(source, language, Path(folder))
            no_archive_reason = getattr(generator_module, "NO_ARCHIVE_REASONS", {}).get(number)
            cross = ({"status": "passed", "cases": 0, "dirs": [],
                      "no_archive_reason": no_archive_reason,
                      "method": "legacy oracle excluded with a problem-specific audited reason"}
                     if no_archive_reason else archive_check(command, entry))
            if cross["status"] != "passed":
                raise SystemExit(f"{number:05d} legacy cross-check failed: {cross}")
            cases = ([sample] if sample else []) + [generator_module.generate(number, seed)
                                                     for seed in range(1, 21)]
            existing_data = OPENJUDGE / entry["made_dir"] / "data"
            cached_inputs = [path.read_text(encoding="utf-8") for path in
                             sorted(existing_data.glob("*.in"), key=lambda path: int(path.stem))]
            cached_outputs = [path.read_text(encoding="utf-8") for path in
                              sorted(existing_data.glob("*.out"), key=lambda path: int(path.stem))]
            outputs = cached_outputs if cached_inputs == cases and len(cached_outputs) == len(cases) \
                else [run(command, case) for case in cases]
        made_rel = entry["made_dir"]
        made, data = OPENJUDGE / made_rel, OPENJUDGE / made_rel / "data"
        data.mkdir(parents=True, exist_ok=True)
        for old in data.glob("*"):
            old.unlink()
        for index, (case, output) in enumerate(zip(cases, outputs)):
            (data / f"{index}.in").write_text(case, encoding="utf-8")
            (data / f"{index}.out").write_text(output, encoding="utf-8")
        suffix = "py" if language == "Python3" else "cpp"
        (made / f"samplecode.{suffix}").write_text(source, encoding="utf-8")
        write_producecase(made, generator_module, number, source, language, sample)

        generated = cases[1:] if sample else cases
        generated_outputs = outputs[1:] if sample else outputs
        label = generator_module.LABELS[number]
        invalid = generator_module.INVALID[number]
        checks = [(label, all(generator_module.valid(number, case) for case in generated))]
        audit = audit_common.audit(
            made, cases=generated, outputs=generated_outputs,
            sample_input=sample or cases[0], sample_output=sample_output,
            sample_output_exemption=(None if sample_output else
                                     "the mirrored statement has no machine-readable sample output"),
            exemption=generator_module.EXEMPTIONS.get(number), constraints=checks,
            constraint_counterexample=(invalid.strip(),
                                       [(label, generator_module.valid(number, invalid))]))
        smoke = [seed for seed in range(2000)
                 if not generator_module.valid(number, generator_module.generate(number, seed))]
        platform_row = platform.get(number)
        status = "passed" if not audit["failed"] and not smoke and (
            not platform_row or platform_row.get("verdict") == "Accepted") else "FAILED"
        manifest.append({**entry, "local_number": number, "sample_input": sample,
                         "reference_language": language,
                         "reference_source_path": reference["source_path"],
                         "reference_solution_id": reference["solution_id"],
                         "pending_rework": []})
        report.append({"local_number": number, "global_number": entry["global_number"],
                       "title": entry["title"], "priority": priority, "phase": 2,
                       "status": status, "reference_source": reference.get(
                           "reference_source", "existing platform Accepted submission"),
                       "reference_language": language,
                       "reference_solution_id": reference["solution_id"],
                       "source_url": reference["source_url"],
                       "license_status": reference.get(
                           "license_status", "not declared; no license is inferred"),
                       "submission_id": platform_row.get("solution_id") if platform_row else None,
                       "platform_verdict": platform_row.get("verdict") if platform_row else "not_run",
                       "archive_cross_check": cross, "generator": "generate",
                       "generator_seed_smoke": {"seeds": 2000,
                                                "status": "passed" if not smoke else "FAILED",
                                                "failed_seeds": smoke[:8]},
                       "test_cases": len(cases),
                       "max_input_bytes": max(len(case.encode()) for case in cases),
                       "max_output_bytes": max(len(output.encode()) for output in outputs),
                       "constraint": label, "constraint_counterexample": invalid.strip(),
                       **({"multi_answer_exemption":
                           generator_module.MULTI_ANSWER_EXEMPTIONS[number]}
                          if number in getattr(generator_module, "MULTI_ANSWER_EXEMPTIONS", {}) else {}),
                       **({"input_domain": {
                           "statement_quote": generator_module.INPUT_DOMAINS[number],
                           "generated_extremes": generated_extremes(data),
                       }} if number in getattr(generator_module, "INPUT_DOMAINS", {}) else {}),
                       "self_audit": audit})
        print(f"{number:05d} built ({language}, legacy={cross['cases']})", flush=True)

    manifest_path = ROOT / "collab" / f"t028-round{round_number}-manifest.json"
    report_path = ROOT / "collab" / f"t028-round{round_number}-report.json"
    manifest_path.write_text(json.dumps({"task": "T-028", "phase": 2,
        "round": round_number, "count": len(manifest), "priority_range": [expected[0], expected[-1]],
        "entries": manifest}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    failed = [row["local_number"] for row in report if row["status"] != "passed"]
    report_path.write_text(json.dumps({"task": "T-028", "phase": 2,
        "round": round_number, "updated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(report), "priority_range": [expected[0], expected[-1]],
        "pending_rework_status": audit_common.pending_rework_status([], OPENJUDGE / "tests"),
        "entries": report, "failed": failed}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    if failed:
        raise SystemExit(f"round {round_number} self-audit failed: {failed}")
