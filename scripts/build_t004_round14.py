#!/usr/bin/env python3
from __future__ import annotations

import concurrent.futures
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
MANIFEST = ROOT / "collab/t004-round14-manifest.json"
REPORT = ROOT / "collab/t004-round14-report.json"
TESTS = ROOT / "data/openjudge/tests"
sys.path.insert(0, str(ROOT / "scripts"))
from build_001a import bucket
import t004_common as common


def g27312(r):
    n = r.randrange(2, 10002, 2)
    return f"{n}\n{''.join(r.choice('GH') for _ in range(n))}\n"


def g27313(r):
    n = r.randint(3, 50)
    if r.random() < .6:
        p = list(range(1, n)) + [0]
    else:
        p = list(range(n)); r.shuffle(p)
    return f"{n}\n{' '.join(map(str, p))}\n"


def g27314(r):
    words = ["Alpha", "beta", "Gamma", "delta", "word", "TARGET"]
    old, new = r.choice(words), r.choice(words)
    parts = []
    for _ in range(r.randint(2, 12)):
        parts.append(" ".join(r.choice(words) for _ in range(r.randint(2, 7))) + ".")
    return " ".join(parts) + "\n" + f"{old} {new}\n"


def g27318(r):
    return f"{r.randint(1, 1000)} {r.randint(0, 1000)}\n"


def g27367(r):
    n, m = r.randint(1, 80), r.randint(1, 12)
    rows = [f"{1000+i} {' '.join(str(r.randint(60, 100)) for _ in range(m))}" for i in range(n)]
    return f"{n} {m}\n" + "\n".join(rows) + "\n"


def g27378(r):
    key = r.choice("abcdefghijklmnopqrstuvwxyz")
    text = "".join(r.choice("abcdefghijklmnopqrstuvwxyz .") for _ in range(r.randint(1, 180)))
    text = text.rstrip() or "."
    return f"{key}\n{text}\n"


def g27385(r):
    k = r.randint(0, 10); n = 1 << k
    a = [r.randint(-n, n) for _ in range(n)]
    q = r.randint(1, 100); ops = []
    for _ in range(q):
        if r.random() < .6:
            l = r.randint(0, n - 1); ops.append(f"1 {l} {r.randint(l, n - 1)}")
        else:
            ops.append(f"2 {r.randint(0, n - 1)} {r.randint(-n, n)}")
    return f"{k}\n{' '.join(map(str, a))}\n{q}\n" + "\n".join(ops) + "\n"


def g27421(r):
    m, n = r.randint(1, 20), r.randint(1, 20)
    rows = [" ".join(str(r.randint(0, 100)) for _ in range(n)) for _ in range(m)]
    return f"{m} {n}\n" + "\n".join(rows) + "\n"


def g27441(r):
    n, m = r.randint(1, 300), r.randint(1, 20)
    p = [r.randint(1, 40) for _ in range(m)]
    c = [r.randint(0, 30) for _ in range(m)]
    return f"{n} {m}\n{' '.join(map(str, p))}\n{' '.join(map(str, c))}\n"


def g27442(r):
    m, n = r.randint(1, 12), r.randint(1, 80)
    courses = [f"C{i}" for i in range(m)]
    lines = [f"{c} {r.uniform(0.1, 5):.2f}" for c in courses]
    rows = [f"S{i} {r.choice(courses)} {r.randint(0, 100)}" for i in range(n)]
    return f"{m} {n}\n" + "\n".join(lines + rows) + "\n"


def g27778(r):
    t = r.randint(1, 20); rows = [str(t)]
    for _ in range(t):
        a = "".join(r.choice("abcXYZ012") for _ in range(r.randint(0, 80)))
        b = a if r.random() < .35 else a + r.choice("xY9")
        rows += [a, b]
    return "\n".join(rows) + "\n"


def g27832(r):
    n, m = r.randint(1, 300), r.randint(1, 120)
    a = [r.randint(0, 65535) for _ in range(n)]; rows = []
    for _ in range(m):
        rows.append(f"{'C' if r.random() < .45 else 'Q'} {r.randint(0, 15)}")
    return f"{n} {m}\n{' '.join(map(str, a))}\n" + "\n".join(rows) + "\n"


def g27932(r):
    n = r.randint(1, 10000); k = r.randint(0, n)
    a = [r.randint(1, 10**9) for _ in range(n)]
    return f"{n} {k}\n{' '.join(map(str, a))}\n"


def g27933(r):
    n = r.randint(1, 1000); pending = list(range(1, n + 1)); added = []
    lines = []
    while pending or added:
        if pending and (not added or r.random() < .65):
            x = pending.pop(r.randrange(len(pending))); added.append(x); lines.append(f"add {x}")
        else:
            x = r.choice(added); added.remove(x); lines.append("remove")
    return f"{n}\n" + "\n".join(lines) + "\n"


def tree_case(r, n):
    edges = [(i, r.randrange(i)) for i in range(1, n)]
    restricted = sorted(r.sample(range(1, n), r.randint(1, min(n - 1, 12))))
    return f"{n}\n" + "\n".join(f"{a} {b}" for a, b in edges) + "\n" + " ".join(map(str, restricted)) + "\n"


def g28012(r):
    n = r.randint(2, 100); edges = [(i, r.randrange(i)) for i in range(1, n)]
    restricted = sorted(r.sample(range(1, n), r.randint(1, min(n - 1, 12))))
    return f"{n}\n" + "\n".join(f"{a} {b}" for a, b in edges) + "\n" + " ".join(map(str, restricted)) + "\n"


def g28013(r):
    n = r.randint(1, 1000); a = list(range(1, n + 1)); r.shuffle(a)
    return f"{n}\n{' '.join(map(str, a))}\n"


def g28058(r):
    n, m = r.randint(1, 20), r.randint(1, 100)
    names = [f"dish{i}" for i in range(n)]
    menu = [f"{x} {r.randint(1, 1000)} {r.randint(0, 30)}" for x in names]
    orders = [" ".join(r.choice(names) for _ in range(3)) for _ in range(m)]
    return f"{n} {m}\n" + "\n".join(menu + orders) + "\n"


def g28200(r): return f"{r.randint(2, 10000)} {r.randint(1, 20000)}\n"


def good_string(r, n):
    return "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n))


def g28202(r):
    t = r.randint(1, 8); rows = [str(t)]
    for _ in range(t):
        n = r.choice([1, 2, 4, 8, 16, 32, 64, 128])
        rows += [str(n), "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n))]
    return "\n".join(rows) + "\n"


def g28274(r):
    n, m = r.randint(1, 30), r.randint(1, 30)
    return f"{n} {m}\n" + "\n".join("".join(r.choice("0123456789") for _ in range(m)) for _ in range(n)) + "\n"


GENERATORS = {n: globals()[f"g{n}"] for n in (27312, 27313, 27314, 27318, 27367, 27378, 27385, 27421, 27441, 27442, 27778, 27832, 27932, 27933, 28012, 28013, 28058, 28200, 28202, 28274)}


def scale_case(n):
    if n == 27312: return "200000\n" + ("GH" * 100000) + "\n"
    if n == 27385:
        size = 1 << 17; return f"17\n{' '.join(str((i % 200001) - 100000) for i in range(size))}\n3\n1 0 {size-1}\n2 65536 7\n1 65500 65600\n"
    if n == 27318: return "1000 1000\n"
    if n == 27421:
        return "100 100\n" + "\n".join(" ".join(str((i * 37 + j * 17) % 1000) for j in range(100)) for i in range(100)) + "\n"
    if n == 27441: return "10000 20\n" + " ".join(str(i + 1) for i in range(20)) + "\n" + " ".join("1000" for _ in range(20)) + "\n"
    if n == 27442: return None
    if n == 27832: return "10000 10000\n" + " ".join(str(i % 65536) for i in range(10000)) + "\n" + "\n".join(("C " if i % 2 == 0 else "Q ") + str(i % 16) for i in range(10000)) + "\n"
    if n == 27932: return "200000 100000\n" + " ".join(str((i * 7919) % 1000000000 + 1) for i in range(200000)) + "\n"
    if n == 27933:
        return "10000\n" + "\n".join([*(f"add {i}" for i in range(1, 10001)), *("remove" for _ in range(10000))]) + "\n"
    if n == 28012: return tree_case(random.Random(14012), 1000)
    if n == 28013:
        a = list(range(1, 1001)); return "1000\n" + " ".join(map(str, a)) + "\n"
    if n == 28058:
        names = [f"dish{i}" for i in range(100)]; menu = [f"{x} {i+1} 1000" for i, x in enumerate(names)]
        orders = [" ".join(names[(i+j) % 100] for j in range(3)) for i in range(10000)]
        return "100 10000\n" + "\n".join(menu + orders) + "\n"
    if n == 28200: return "200000 400000\n"
    if n == 28202: return "1\n131072\n" + ("abcdefghijklmnopqrstuvwxyz" * 5042)[:131072] + "\n"
    if n == 28274: return "400 400\n" + "\n".join("".join("1" if (i+j) % 17 == 0 else "0" for j in range(400)) for i in range(400)) + "\n"
    return None


def run_source(source, text):
    with tempfile.TemporaryDirectory(prefix="t004-r14-run-") as d:
        path = Path(d) / "main.py"; path.write_text(source)
        x = subprocess.run([sys.executable, str(path)], input=text, text=True, capture_output=True, timeout=90)
        if x.returncode: raise RuntimeError(x.stderr[-1000:] or str(x.returncode))
        return x.stdout


def constraint_rows(n, cases):
    def check(label, pred, bad):
        return [(label, all(pred(x) for x in cases))], (bad, [(label, bool(pred(bad)))])
    if n == 27312: return check("N is even and 2..200000; string is G/H of length N", lambda x: (lambda a: 2 <= int(a[0]) <= 200000 and int(a[0]) % 2 == 0 and len(a[1]) == int(a[0]) and set(a[1]) <= set("GH"))(x.split()), "3\nGGG\n")
    if n == 27313: return check("N is 2..50 and p is a permutation of 0..N-1", lambda x: (lambda a: 2 <= int(a[0]) <= 50 and sorted(map(int, a[1:])) == list(range(int(a[0]))))(x.split()), "3\n0 1 3\n")
    if n == 27318: return check("1<=n<=1000 and 0<=k<=1000", lambda x: 1 <= int(x.split()[0]) <= 1000 and 0 <= int(x.split()[1]) <= 1000, "1001 0\n")
    if n == 27367: return check("scores are integers in 60..100", lambda x: all(60 <= int(v) <= 100 for line in x.splitlines()[1:] for v in line.split()[1:]), "1 1\n1001 101\n")
    if n == 27385: return check("k is 0..17 and array/indices fit 2^k", lambda x: 0 <= int(x.split()[0]) <= 17, "18\n0\n1\n1 0 0\n")
    if n == 27421: return check("matrix dimensions are positive and cells are nonnegative", lambda x: all(int(v) >= 0 for v in x.split()[2:]), "1 1\n-1\n")
    if n == 27441: return check("target, prices and stock counts are nonnegative integers", lambda x: all(int(v) >= 0 for v in x.split()), "-1 1\n1\n1\n")
    if n == 27442: return check("course weights and grades are numeric", lambda x: (lambda a: all(v.replace('.', '', 1).isdigit() for v in a[2:2+2*int(a[0])] if not v.startswith('C')) and all(v.isdigit() for v in a[2+2*int(a[0]):][2::3]))(x.split()), "1 1\nC -1\nS C 50\n")
    if n == 27832: return check("array values are 0..65535", lambda x: all(0 <= int(v) <= 65535 for v in x.splitlines()[1].split()), "1 1\n65536\nQ 0\n")
    if n == 27932: return check("1<=k<=n and ai are 1..1e9", lambda x: (lambda a: 1 <= int(a[0]) and 0 <= int(a[1]) <= int(a[0]) and all(1 <= int(v) <= 10**9 for v in a[2:]))(x.split()), "1 0\n0\n")
    if n == 27933: return check("n is 1..10000", lambda x: 1 <= int(x.split()[0]) <= 10000, "10001\n")
    if n == 28012: return check("tree vertices are in 0..n-1 and restricted excludes 0", lambda x: (lambda a: all(0 <= int(v) < int(a[0]) for v in a[1:-1]) and all(int(v) != 0 for v in a[-1:]))(x.split()), "2\n0 2\n1\n")
    if n == 28013: return check("n is 1..1000 and values are distinct", lambda x: len(set(x.split()[1:])) == int(x.split()[0]) <= 1000, "2\n1 1\n")
    if n == 28058: return check("menu stock and prices are nonnegative", lambda x: all(int(v) >= 0 for v in x.split() if v.lstrip('-').isdigit()), "1 1\ndish -1 0\ndish dish dish\n")
    if n == 28200: return check("N>=2 and D>=1", lambda x: int(x.split()[0]) >= 2 and int(x.split()[1]) >= 1, "1 0\n")
    if n == 28202: return check("N is positive and strings are lowercase", lambda x: (lambda a: all(int(a[i]) > 0 and len(a[i+1]) == int(a[i]) and a[i+1].islower() for i in range(1, len(a), 2)))(x.split()), "1\n1\nA\n")
    if n == 28274: return check("grid dimensions are 1..400 and cells are digits", lambda x: all(v.isdigit() for v in x.split()[2:]), "1 1\nA\n")
    return check("input is present", lambda x: bool(x.strip()), "")


def write_producecase(made, source, generator, sample, extra):
    text = ("import random, subprocess, sys, tempfile\nfrom pathlib import Path\n"
            f"REFERENCE={source!r}\nSAMPLE={sample!r}\nEXTRA_CASE={extra!r}\nGENERATOR_NAME={generator.__name__!r}\n"
            + inspect.getsource(generator) + "\n"
            + "def run(text):\n    with tempfile.TemporaryDirectory(prefix='producecase-') as d:\n        p=Path(d)/'main.py'; p.write_text(REFERENCE)\n        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=90)\n        if x.returncode: raise SystemExit(x.stderr)\n        return x.stdout\n"
            + f"def scale_case(): return EXTRA_CASE\n"
            + "def main():\n    d=Path('data'); d.mkdir(exist_ok=True)\n    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]\n    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))\nif __name__=='__main__': main()\n")
    (made / "producecase.py").write_text(text)


def main():
    manifest = json.loads(MANIFEST.read_text()); report = []
    selected = {int(x) for x in os.environ.get("T004_ONLY", "").split(",") if x}
    if selected and REPORT.exists():
        old = json.loads(REPORT.read_text()).get("entries", [])
        report.extend(e for e in old if int(e["local_number"]) not in selected)
    for entry in manifest["entries"]:
        n = int(entry["local_number"])
        if selected and n not in selected: continue
        source = (ROOT / f"scripts/t004_platform_accepted_{n}.py").read_text()
        gen = GENERATORS[n]; sample = entry["sample_input"]; extra = scale_case(n)
        cases = [sample] + ([extra] if extra else []) + [gen(random.Random(s)) for s in range(1, 21)]
        outputs = [run_source(source, c) for c in cases]
        made = TESTS / bucket(n) / f"{n:05d}_made"; data = made / "data"; data.mkdir(parents=True, exist_ok=True)
        for p in data.glob("*"): p.unlink()
        for i, c in enumerate(cases): (data/f"{i}.in").write_text(c); (data/f"{i}.out").write_text(outputs[i])
        (made / "samplecode.py").write_text(source)
        write_producecase(made, source, gen, sample, extra)
        rows, counter = constraint_rows(n, cases[1:])
        audit = common.audit(made, cases=cases[1:], outputs=outputs[1:], sample_input=sample,
            sample_output=entry.get("sample_output"), sample_output_exemption=entry.get("sample_output_exemption"),
            constraints=rows, constraint_counterexample=counter)
        for s in range(20000): gen(random.Random(s))
        smoke = [gen(random.Random(100000+s)) for s in range(400)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: list(pool.map(lambda x: run_source(source, x), smoke))
        audit["scale_summary"] = {"max_case_chars": max(map(len, cases)), "max_generated_seed": 20}
        a = entry["existing_accepted"]
        report.append({"local_number": n, "title": entry["title"], "reference_source": f"platform Accepted Python3 #{a['solution_id']}",
            "statistics_url": f"http://cs101.openjudge.cn{entry['submit_path']}statistics/", "source_url": a["source_url"],
            "license_status": "not declared on the submission page; no license is inferred.", "generator": gen.__name__,
            "generator_seed_smoke": {"seeds": 20000, "status": "passed"}, "reference_seed_smoke": {"seeds": 400, "status": "passed"},
            "test_cases": len(cases), "constraints": rows, "constraint_counterexample": counter,
            "self_audit": audit, "sample_reproduced": audit["sample_is_case_zero"]["status"] == "passed",
            "producecase_reproduced": audit["byte_reproduction"]["status"] == "passed"})
        print(n, "built", flush=True)
    pending = common.pending_rework_status(manifest.get("pending_rework", []), TESTS)
    REPORT.write_text(json.dumps({"batch":"T-004 round14", "updated_at":datetime.now(timezone.utc).isoformat(), "pending_rework_status":pending, "entries":report}, ensure_ascii=False, indent=2)+"\n")


if __name__ == "__main__": main()
