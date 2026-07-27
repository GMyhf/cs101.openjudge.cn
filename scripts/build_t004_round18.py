#!/usr/bin/env python3
from __future__ import annotations

import inspect
import json
import random
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collab/t004-round18-manifest.json"
REPORT = ROOT / "collab/t004-round18-report.json"
TESTS = ROOT / "data/openjudge/tests"
sys.path.insert(0, str(ROOT / "scripts"))
from build_001a import bucket
import t004_common as common


def g31042(r):
    """Generate two related line-oriented files with changes and LCS ties."""
    alphabet = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta"]
    size = r.randint(2, 45)
    old = [f"    {r.choice(alphabet)}_{i % 9}" if r.random() < .2 else f"{r.choice(alphabet)}_{i % 9}" for i in range(size)]
    new = []
    for line in old:
        action = r.random()
        if action < .18:
            continue
        if action < .42:
            new.append(f"+generated_{r.randint(0, 20)}")
        new.append(line if r.random() < .78 else f"{r.choice(alphabet)}_{r.randint(0, 8)}")
    for _ in range(r.randint(0, 8)):
        new.insert(r.randint(0, len(new)), r.choice(alphabet) + "_inserted")
    if not new:
        new = ["replacement"]
    return f"{len(old)}\n" + "\n".join(old) + f"\n{len(new)}\n" + "\n".join(new) + "\n"


def run_many(source, cases):
    with tempfile.TemporaryDirectory(prefix="t004-r18-") as d:
        path = Path(d) / "main.py"
        path.write_text(source)
        outputs = []
        for case in cases:
            result = subprocess.run([sys.executable, str(path)], input=case, text=True,
                                    capture_output=True, timeout=120)
            if result.returncode:
                raise RuntimeError(result.stderr[-1000:] or str(result.returncode))
            outputs.append(result.stdout)
        return outputs


def valid_input(text):
    lines = text.splitlines()
    if not lines or not lines[0].isdigit():
        return False
    n = int(lines[0]); m_index = n + 1
    if m_index >= len(lines) or not lines[m_index].isdigit():
        return False
    return len(lines) == m_index + 1 + int(lines[m_index])


def constraint(cases):
    label = "input has exactly N old lines and M new lines"
    rows = [(label, all(valid_input(case) for case in cases))]
    bad = "2\nold only\n1\n"
    return rows, (bad, [(label, valid_input(bad))])


def write_producecase(made, source, sample, generator):
    runner = """
from pathlib import Path
import random, subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        path=Path(d)/'main.py'; path.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(path)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1,21)]
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(run(case))
if __name__=='__main__': main()
"""
    text = "import random\n" + f"REFERENCE={source!r}\nSAMPLE={sample!r}\nGENERATOR={generator.__name__!r}\n" + inspect.getsource(generator) + runner
    (made / "producecase.py").write_text(text)


def main():
    manifest = json.loads(MANIFEST.read_text())
    entry = manifest["entries"][0]
    number = int(entry["local_number"])
    source = (ROOT / f"scripts/t004_platform_accepted_{number}.py").read_text()
    cases = [entry["sample_input"]] + [g31042(random.Random(seed)) for seed in range(1, 21)]
    outputs = run_many(source, cases)
    made = TESTS / bucket(number) / f"{number:05d}_made"
    data = made / "data"; data.mkdir(parents=True, exist_ok=True)
    for path in data.glob("*"): path.unlink()
    for i, case in enumerate(cases):
        (data / f"{i}.in").write_text(case)
        (data / f"{i}.out").write_text(outputs[i])
    (made / "samplecode.py").write_text(source)
    write_producecase(made, source, entry["sample_input"], g31042)
    rows, counterexample = constraint(cases[1:])
    audit = common.audit(made, cases=cases[1:], outputs=outputs[1:],
                         sample_input=entry["sample_input"],
                         sample_output=entry["sample_output"],
                         constraints=rows,
                         constraint_counterexample=counterexample)
    for seed in range(20000):
        g31042(random.Random(seed))
    run_many(source, [g31042(random.Random(100000 + seed)) for seed in range(400)])
    accepted = entry["existing_accepted"]
    report = {
        "batch": "T-004 round18",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "judge_fidelity_warning": manifest["judge_fidelity_warning"],
        "entries": [{
            "local_number": number,
            "title": entry["title"],
            "reference_source": f"platform Accepted Python3 #{accepted['solution_id']}",
            "statistics_url": f"http://cs101.openjudge.cn{entry['submit_path']}statistics/",
            "source_url": accepted["source_url"],
            "license_status": "not declared on the submission page; no license is inferred.",
            "generator": "g31042",
            "generator_seed_smoke": {"seeds": 20000, "status": "passed"},
            "reference_seed_smoke": {"seeds": 400, "status": "passed"},
            "test_cases": len(cases),
            "constraints": rows,
            "constraint_counterexample": counterexample,
            "self_audit": audit,
            "sample_reproduced": audit["sample_is_case_zero"]["status"] == "passed",
            "producecase_reproduced": audit["byte_reproduction"]["status"] == "passed",
        }],
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(number, "built", "failed=", audit["failed"])


if __name__ == "__main__":
    main()
