#!/usr/bin/env python3
from __future__ import annotations

import inspect
import json
import os
import random
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collab/t004-round16-manifest.json"
REPORT = ROOT / "collab/t004-round16-report.json"
TESTS = ROOT / "data/openjudge/tests"
sys.path.insert(0, str(ROOT / "scripts"))
from build_001a import bucket
import t004_common as common


def g29647(r):
    n = r.randint(2, 80); value = [r.randint(0, 100) for _ in range(n)]
    edges = [f"{i} {r.randint(1, i - 1)}" for i in range(2, n + 1)]
    return f"{n}\n" + "\n".join(map(str, value)) + "\n" + "\n".join(edges) + "\n"


def g29656(r):
    n = r.randint(1, 100); left = [0] * (n + 1); right = [0] * (n + 1)
    free = [1]
    for node in range(2, n + 1):
        while True:
            parent = r.choice(free)
            side = r.choice((0, 1))
            if side == 0 and not left[parent]: left[parent] = node; break
            if side == 1 and not right[parent]: right[parent] = node; break
        free.append(node)
        if left[parent] and right[parent]: free.remove(parent)
    return f"{n}\n" + "\n".join(f"{left[i]} {right[i]}" for i in range(1, n + 1)) + "\n"


def g29657(r):
    n1, n2, n3 = (r.randint(1, 35) for _ in range(3)); k = r.randint(0, 50)
    arrays = [[r.randint(-100, 100) for _ in range(n)] for n in (n1, n2, n3)]
    return f"{n1} {n2} {n3} {k}\n" + "\n".join(" ".join(map(str, a)) for a in arrays) + "\n"


def g29662(r):
    n, m = r.randint(1, 30), r.randint(1, 30)
    rows = [[r.randint(0, 1) for _ in range(m)] for _ in range(n)]
    return f"{n} {m}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + "\n"


def g29677(r):
    rows = [str(r.randint(1, 4))]
    for _ in range(int(rows[0])):
        n = r.randint(2, 45); target = list(range(1, n + 1)); r.shuffle(target)
        distance = [r.randint(0, n) for _ in range(n)]
        rows.extend((str(n), " ".join(map(str, target)), " ".join(map(str, distance))))
    return "\n".join(rows) + "\n"


def g29694(r):
    return " ".join(str(r.randint(1, 6)) for _ in range(r.randint(2, 120))) + "\n"


def g29739(r):
    s = "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(20, 150)))
    length = r.randint(1, min(20, len(s))); start = r.randint(0, len(s) - length)
    t = s[start:start + length]
    p = "".join("1" if s.startswith(t, i) else "0" for i in range(len(s)))
    return s + "\n" + p + "\n"


def g29742(r):
    return " ".join(r.choice(("PO", "PI", "PA")) for _ in range(r.randint(1, 120))) + "\n"


def g29750(r):
    n = r.randint(1, 11); return f"{n}\n" + " ".join(str(r.randint(0, 1)) for _ in range(n)) + "\n"


def g29778(r):
    n = r.randint(1, 2000); return f"{n}\n" + "\n".join(str(r.randint(0, 10**6)) for _ in range(n)) + "\n"


def g29853(r):
    n = r.randint(1, 100); a = [r.randint(-1000, 1000) for _ in range(n)]; b = [r.randint(-1000, 1000) for _ in range(n)]
    return f"{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"


def g29940(r):
    n = r.randint(1, 200); return f"{n}\n" + " ".join(str(r.randint(-1000, 1000)) for _ in range(n)) + "\n"


def g29945(r): return f"{r.randint(1, 100000)}\n"


def g29946(r):
    n = r.randint(1, 100); s = str(r.randint(1, 9)) + "".join(str(r.randint(0, 9)) for _ in range(n - 1)); return f"{s}\n{r.randint(0, n - 1)}\n"


def g30022(r):
    n = r.randint(2, 45); k, s = r.sample(range(n), 2)
    matrix = [[0 if i == j else int(r.random() < .35) for j in range(n)] for i in range(n)]
    return f"{n} {k} {s}\n" + "\n".join(" ".join(map(str, row)) for row in matrix) + "\n"


def g30023(r):
    atoms = [("H", 1), ("He", 4), ("C", 12), ("O", 16), ("F", 19), ("Na", 23), ("Al", 27), ("Cu", 64)]
    formulas = []
    for _ in range(r.randint(1, 30)):
        a, b = r.choice(atoms)[0], r.choice(atoms)[0]
        formulas.append(f"{a}{r.randint(1, 4)}({b}{r.randint(1, 3)}){r.randint(1, 4)}")
    return f"{len(atoms)} {len(formulas)}\n" + "\n".join(f"{a} {w}" for a, w in atoms) + "\n" + "\n".join(formulas) + "\n"


def g30041(r):
    n, m = r.randint(1, 35), r.randint(1, 35); rows = []
    for _ in range(n):
        row = sorted(r.randint(0, 100) for _ in range(m)); rows.append(" ".join(map(str, row)))
    return f"{n} {m}\n" + "\n".join(rows) + "\n"


def g30044(r): return f"{r.randint(0, 1000)}\n"


def g30061(r):
    n = r.randint(1, 1000); m = r.randint(0, n); values = r.sample(range(n), m)
    return f"{n} {m}\n" + (" ".join(map(str, values)) + "\n" if values else "\n")


def g30085(r):
    n = r.randint(1, 200); w = r.randint(1, 2000); prices = [r.randint(1, w) for _ in range(n)]
    return f"{w}\n{n}\n" + "\n".join(map(str, prices)) + "\n"


GENERATORS = {n: globals()[f"g{n}"] for n in (29647, 29656, 29657, 29662, 29677, 29694, 29739, 29742, 29750, 29778, 29853, 29940, 29945, 29946, 30022, 30023, 30041, 30044, 30061, 30085)}


def run_many(source, cases):
    with tempfile.TemporaryDirectory(prefix="t004-r16-") as d:
        path = Path(d) / "main.py"; path.write_text(source)
        output = []
        for case in cases:
            result = subprocess.run([sys.executable, str(path)], input=case, text=True, capture_output=True, timeout=120)
            if result.returncode: raise RuntimeError(f"reference failed: {result.stderr[-500:]}")
            output.append(result.stdout)
        return output


def constraint(n, cases):
    checks = {
        29647: [("n>=2 and n-1 relations", lambda x: (lambda a: int(a[0]) >= 2 and len(a) == 1 + int(a[0]) + 2 * (int(a[0]) - 1))(x.split()), "2\n0\n" )],
        29656: [("binary-tree child ids are in 0..n", lambda x: (lambda a: all(0 <= int(v) <= int(a[0]) for v in a[1:]))(x.split()), "1\n2 0\n")],
        29657: [("array lengths are positive", lambda x: all(int(v) > 0 for v in x.split()[:3]), "0 1 1 0\n0\n1\n1\n")],
        29662: [("grid cells are binary", lambda x: all(v in {"0", "1"} for v in x.split()[2:]), "1 1\n2\n")],
        29677: [("target positions are in 1..N", lambda x: (lambda a: all(1 <= int(v) <= int(a[1]) for v in a[2:2 + int(a[1])]))(x.split()), "1\n2\n0 3\n0 0\n")],
        29694: [("syllable numbers are 1..6", lambda x: all(1 <= int(v) <= 6 for v in x.split()), "0\n")],
        29739: [("S is lowercase and T is binary", lambda x: (lambda a: a[0].islower() and set(a[1]) <= {"0", "1"})(x.split()), "A\n2\n")],
        29742: [("sentence consists of PO/PI/PA syllables", lambda x: all(v in {"PO", "PI", "PA"} for v in x.split()), "PX\n")],
        29750: [("disk states are binary", lambda x: all(v in {"0", "1"} for v in x.split()[1:]), "1\n2\n")],
        29778: [("n equals the number of values", lambda x: len(x.split()) == int(x.split()[0]) + 1, "2\n1\n")],
        29853: [("both arrays have n values", lambda x: len(x.split()) == 1 + 2 * int(x.split()[0]), "2\n1\n1\n1\n")],
        29940: [("n equals the number of scores", lambda x: len(x.split()) == int(x.split()[0]) + 1, "2\n1\n")],
        29945: [("n is positive", lambda x: int(x.strip()) > 0, "0\n")],
        29946: [("k is in 0..number length-1", lambda x: (lambda a: 0 <= int(a[1]) < len(a[0]))(x.split()), "12\n2\n")],
        30022: [("adjacency matrix is n by n", lambda x: (lambda a: len(a) == 3 + int(a[0]) * int(a[0]))(x.split()), "2 0 1\n0 1\n")],
        30023: [("formula count matches n", lambda x: (lambda a: len(a) == 2 + 2 * int(a[0]) + int(a[1]))(x.split()), "1 2\nH 1\nH\n")],
        30041: [("rows and columns match n,m", lambda x: (lambda a: len(a) == 2 + int(a[0]) * int(a[1]))(x.split()), "2 2\n1\n")],
        30044: [("index is in 0..1000", lambda x: 0 <= int(x.strip()) <= 1000, "1001\n")],
        30061: [("reported ids are in 0..N-1", lambda x: (lambda a: all(0 <= int(v) < int(a[0]) for v in a[2:]))(x.split()), "2 1\n2\n")],
        30085: [("prices are positive and at most W", lambda x: (lambda a: all(1 <= int(v) <= int(a[0]) for v in a[2:]))(x.split()), "10\n1\n11\n")],
    }
    rows = [(label, all(pred(case) for case in cases)) for label, pred, *_ in checks[n]]
    bad = [(bad_input, [(label, bool(pred(bad_input)))]) for label, pred, bad_input in checks[n]]
    return rows, bad[0]


def write_producecase(made, source, gen, sample):
    runner = """
from pathlib import Path
import random, subprocess, sys, tempfile
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
"""
    text = "import random\n" + f"REFERENCE={source!r}\nSAMPLE={sample!r}\nGENERATOR_NAME={gen.__name__!r}\n" + inspect.getsource(gen) + runner
    (made / "producecase.py").write_text(text)


def main():
    manifest = json.loads(MANIFEST.read_text()); report = []
    for entry in manifest["entries"]:
        n = int(entry["local_number"]); source = (ROOT / f"scripts/t004_platform_accepted_{n}.py").read_text(); gen = GENERATORS[n]
        cases = [entry["sample_input"]] + [gen(random.Random(seed)) for seed in range(1, 21)]
        outputs = run_many(source, cases)
        made = TESTS / bucket(n) / f"{n:05d}_made"; data = made / "data"; data.mkdir(parents=True, exist_ok=True)
        for path in data.glob("*"): path.unlink()
        for i, case in enumerate(cases): (data / f"{i}.in").write_text(case); (data / f"{i}.out").write_text(outputs[i])
        (made / "samplecode.py").write_text(source); write_producecase(made, source, gen, entry["sample_input"])
        rows, counterexample = constraint(n, cases[1:])
        audit = common.audit(made, cases=cases[1:], outputs=outputs[1:], sample_input=entry["sample_input"], sample_output=entry["sample_output"], constraints=rows, constraint_counterexample=counterexample)
        for seed in range(20000): gen(random.Random(seed))
        run_many(source, [gen(random.Random(100000 + seed)) for seed in range(400)])
        accepted = entry["existing_accepted"]
        report.append({"local_number": n, "title": entry["title"], "reference_source": f"platform Accepted Python3 #{accepted['solution_id']}", "statistics_url": f"http://cs101.openjudge.cn{entry['submit_path']}statistics/", "source_url": accepted["source_url"], "license_status": "not declared on the submission page; no license is inferred.", "generator": gen.__name__, "generator_seed_smoke": {"seeds": 20000, "status": "passed"}, "reference_seed_smoke": {"seeds": 400, "status": "passed"}, "test_cases": len(cases), "constraints": rows, "constraint_counterexample": counterexample, "self_audit": audit, "sample_reproduced": audit["sample_is_case_zero"]["status"] == "passed", "producecase_reproduced": audit["byte_reproduction"]["status"] == "passed"})
        print(n, "built", flush=True)
    REPORT.write_text(json.dumps({"batch": "T-004 round16", "updated_at": datetime.now(timezone.utc).isoformat(), "pending_rework_status": {"status": "passed", "items": []}, "entries": report}, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__": main()
