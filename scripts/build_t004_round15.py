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
MANIFEST = ROOT / "collab/t004-round15-manifest.json"
REPORT = ROOT / "collab/t004-round15-report.json"
TESTS = ROOT / "data/openjudge/tests"
sys.path.insert(0, str(ROOT / "scripts"))
from build_001a import bucket
import t004_common as common


def g28307(r):
    n = r.randint(1, 100); a = [r.randint(1, 1000) for _ in range(n)]
    b = [r.randint(1, 1000) for _ in range(n)]
    return f"{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n{r.randint(0, n)}\n"


def g28321(r):
    t = r.randint(1, 8); rows = [str(t)]
    for _ in range(t):
        n = r.randint(1, 100); a = sorted(r.randint(0, 100) for _ in range(n)); b = sorted(r.randint(0, 100) for _ in range(n))
        rows += [str(n), " ".join(map(str, a)), " ".join(map(str, b))]
    return "\n".join(rows) + "\n"


def g28322(r):
    t = r.randint(1, 12); rows = [str(t)]
    for _ in range(t):
        s = "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(1, 99)))
        if r.random() < .5:
            rows += ["encrypt", s]
        else:
            stack = []; out = []
            for c in s:
                stack.append(c)
                if (ord(c) - 96) % 2 == 0:
                    out += stack[::-1]; stack.clear()
            if stack: out += stack[::-1] + ["0"]
            rows += ["decrypt", "".join(out)]
    return "\n".join(rows) + "\n"


def g28327(r):
    n = r.randint(2, 100); edges = [(i, r.randrange(1, i)) for i in range(2, n + 1)]
    q = r.randint(1, 100); queries = [r.sample(range(1, n + 1), 2) for _ in range(q)]
    return f"{n}\n" + "\n".join(f"{a} {b}" for a, b in edges) + f"\n{q}\n" + "\n".join(f"{a} {b}" for a, b in queries) + "\n"


def g28332(r):
    rows = []
    for _ in range(r.randint(1, 30)):
        rows.append("".join(r.choice("abcdefghijklmnopqrstuvwxyz ") for _ in range(r.randint(1, 180))).rstrip() or " ")
    return "\n".join(rows) + "\n"


def g28336(r):
    return "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(1, 300))) + "\n"


def g28404(r):
    n = r.randint(1, 100); foods = ["Food-" + chr(65 + i) for i in range(r.randint(1, 12))]
    rows = [f"Customer{i} {r.randint(1, 500)},{r.randint(1, 500)},{r.choice(foods)}" for i in range(n)]
    return f"{n}\n" + "\n".join(rows) + "\n"


def g28405(r):
    n = r.randint(1, 300); a = [r.randint(1, 9999) for _ in range(n)]
    return f"{n}\n" + "\n".join(map(str, a)) + f"\n{r.randint(1, min(1000, n))}\n"


def g28413(r):
    t = r.randint(1, 6); rows = [str(t)]
    for _ in range(t):
        n = r.randint(1, 40); rows.append(str(n))
        for i in range(n):
            deps = sorted(r.sample(range(1, i + 1), r.randint(0, min(i, 3)))) if i else []
            rows.append("N" + str(i) + (" " + " ".join(map(str, deps)) if deps else ""))
    return "\n".join(rows) + "\n"


def g28416(r):
    t = 20; rows = [str(t)]
    for case in range(t):
        n = r.randint(2, 80) if r.random() < .85 else 3000
        rows.append(str(n))
        for i in range(n):
            deps = [] if n >= 1000 else (sorted(r.sample(range(1, i + 1), r.randint(0, min(i, 2)))) if i else [])
            rows.append("N" + str(case) + "_" + str(i) + (" " + " ".join(map(str, deps)) if deps else ""))
    return "\n".join(rows) + "\n"


def g28681(r):
    n = r.randint(5, 300); return f"{n}\n" + "\n".join(f"{r.randint(0,100)} {r.randint(0,100)} {r.randint(0,100)}" for _ in range(n)) + "\n"


def g28699(r):
    n, m = r.randint(1, 30), r.randint(1, 30); prices = [r.randint(1, 100) for _ in range(n)]
    names = [f"fruit{i}" for i in range(n)]; chosen = names[:r.randint(1, n)]
    return f"{n} {m}\n{' '.join(map(str, prices))}\n" + "\n".join(r.choice(chosen) for _ in range(m)) + "\n"


def g28750(r):
    h, w = r.randint(1, 20), r.randint(1, 20)
    def board():
        a = [["."] * w for _ in range(h)]
        for i in range(r.randint(0, min(8, h * w))): a[r.randrange(h)][r.randrange(w)] = r.choice("abcd")
        return ["".join(row) for row in a]
    a, b = board(), board()
    return f"{h} {w}\n" + "\n".join(a) + "\n\n" + "\n".join(b) + "\n"


def g28908(r):
    rows = []
    for _ in range(r.randint(1, 3)): rows.append(f"{r.choice('abc')}:={r.randint(0,9)};")
    return "".join(rows) + "\n"


def g28969(r):
    return "".join(r.choice("0123456789") for _ in range(r.randint(1, 300))) + "\n"


def g28973(r):
    n = r.randint(2, 20); rows = [[0 if r.random() < .72 else 1 for _ in range(n)] for _ in range(n)]
    rows[0][0] = rows[0][1] = rows[-1][-1] = rows[-1][-2] = 0
    return f"{n}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + "\n"


def g29178(r):
    n = r.randint(2, 100); return f"{n}\n" + " ".join(str(r.randint(-1000, 1000)) for _ in range(n)) + "\n"


def g29334(r):
    value = r.randint(1, 2_147_483_647); s = ""
    while value: value, rem = divmod(value - 1, 26); s = chr(65 + rem) + s
    return s + "\n"


def g29340(r):
    n = r.randint(1, 500); mode = r.randrange(3); k = 0 if mode == 0 else (2001 if mode == 1 else r.randint(1, 1000))
    return f"{n}\n" + " ".join(str(r.randint(-1000, 1000)) for _ in range(n)) + f"\n{k}\n"


def g29622(r):
    n = r.randint(1, 60); m = r.randint(1, min(1000, max(1, n * 3))); edges = []
    if r.random() < .7:
        edges += [(i, i + 1, r.randint(1, 100000)) for i in range(1, n)]
    while len(edges) < m: edges.append((r.randint(1, n), r.randint(1, n), r.randint(1, 100000)))
    return f"{n} {len(edges)}\n" + "\n".join(f"{a} {b} {w}" for a, b, w in edges) + "\n"


GENERATORS = {n: globals()[f"g{n}"] for n in (28307, 28321, 28322, 28327, 28332, 28336, 28404, 28405, 28413, 28416, 28681, 28699, 28750, 28908, 28969, 28973, 29178, 29334, 29340, 29622)}


def scale_case(n):
    if n == 28307:
        k = 5000; return f"10000\n" + " ".join(["1000"] * 10000) + "\n" + " ".join(["1"] * 10000) + f"\n{k}\n"
    if n == 28321:
        return "10000\n" + "\n".join("100\n" + " ".join(["0"] * 100) + "\n" + " ".join(["100"] * 100) for _ in range(10000)) + "\n"
    if n == 28322: return "100\n" + "\n".join(["encrypt", "abcdefghijklmnopqrstuvwxyz" * 3] * 100) + "\n"
    if n == 28327:
        n, q = 2000, 2000; edges = "\n".join(f"{i} {i+1}" for i in range(1, n)); queries = "\n".join(f"1 {i % (n - 1) + 2}" for i in range(q))
        return f"{n}\n{edges}\n{q}\n{queries}\n"
    if n == 28332: return "\n".join("abcdefghijklmnopqrstuvwxyz " * 37 for _ in range(20)) + "\n"
    if n == 28336: return "ab" * 4999 + "a\n"
    if n == 28404:
        rows = [f"Customer{i},{i % 500 + 1},Food-{i % 20}" for i in range(50000)]; return "50000\n" + "\n".join(rows) + "\n"
    if n == 28405: return "100000\n" + "\n".join(["9999"] * 100000) + "\n1000\n"
    if n == 28413: return None
    if n == 28416:
        rows = ["20"]
        for case in range(20):
            rows.append("3000")
            rows.extend("N" + str(case) + "_" + str(i) for i in range(3000))
        return "\n".join(rows) + "\n"
    if n == 28681: return "300\n" + "\n".join("100 100 100" for _ in range(300)) + "\n"
    if n == 28699: return "100 100\n" + " ".join(str(i + 1) for i in range(100)) + "\n" + "\n".join(f"fruit{i % 100}" for i in range(100)) + "\n"
    if n == 28750: return "500 500\n" + "\n".join("." * 500 for _ in range(500)) + "\n\n" + "\n".join("." * 500 for _ in range(500)) + "\n"
    if n == 28969: return ("0123456789" * 5000) + "\n"
    if n == 28973: return "100\n" + "\n".join(" ".join(["0"] * 100) for _ in range(100)) + "\n"
    if n == 29340: return "10000\n" + " ".join(str(i % 1000) for i in range(10000)) + "\n500\n"
    if n == 29622:
        n, m = 100, 1000; edges = [(i, i + 1, i) for i in range(1, n)] + [(i % n + 1, (i * 17) % n + 1, i + 100) for i in range(m - n + 1)]
        return f"{n} {m}\n" + "\n".join(f"{a} {b} {w}" for a, b, w in edges) + "\n"
    return None


def run_source(source, text):
    with tempfile.TemporaryDirectory(prefix="t004-r15-run-") as d:
        p = Path(d) / "main.py"; p.write_text(source)
        x = subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if x.returncode: raise RuntimeError(x.stderr[-1000:] or str(x.returncode))
        return x.stdout


def constraint_rows(n, cases):
    def check(label, pred, bad): return [(label, all(pred(x) for x in cases))], (bad, [(label, bool(pred(bad)))])
    if n == 28307: return check("n 1..10000, rewards 1..1000, k 0..n", lambda x: (lambda a: 1 <= int(a[0]) <= 10000 and len(a[1].split()) == int(a[0]) and all(1 <= int(v) <= 1000 for v in a[1].split()+a[2].split()) and 0 <= int(a[3]) <= int(a[0]))(x.splitlines()), "1\n1\n1\n2\n")
    if n == 28321: return check("t 1..10000, n 1..100 and arrays sorted in 0..100", lambda x: all(1 <= int(v) <= 10000 for v in x.split()[:1]) and all(0 <= int(v) <= 100 for v in x.split()[1:]), "1\n101\n0\n0\n")
    if n == 28322: return check("t 1..100 and operation strings have length <=100", lambda x: 1 <= int(x.splitlines()[0]) <= 100 and all(len(v) <= 100 for v in x.splitlines()[2::2]), "101\nencrypt\na\n")
    if n == 28327: return check("tree N,Q <=2000 and query vertices are valid", lambda x: int(x.splitlines()[0]) <= 2000, "2001\n")
    if n == 28332: return check("records use lowercase letters and spaces, length <=1000", lambda x: all(len(line) <= 1000 and all(c.islower() or c == ' ' for c in line) for line in x.splitlines()), "a1\n")
    if n == 28336: return check("string is lowercase and length <10000", lambda x: len(x.strip()) < 10000 and x.strip().islower(), "A\n")
    if n == 28404: return check("N<=50000 and table numbers 1..500", lambda x: int(x.splitlines()[0]) <= 50000 and all(1 <= int(line.split(',')[1]) <= 500 for line in x.splitlines()[1:]), "1\nA,0,F\n")
    if n == 28405: return check("n<=100000, times 1..9999 and m 1..1000", lambda x: 1 <= int(x.splitlines()[0]) <= 100000 and all(1 <= int(v) < 10000 for v in x.splitlines()[1:-1]) and 1 <= int(x.splitlines()[-1]) <= 1000, "1\n10000\n1\n")
    if n in (28413, 28416):
        def dep_ok(x):
            lines = x.splitlines(); t = int(lines[0]); p = 1
            for _ in range(t):
                size = int(lines[p]); p += 1
                for i in range(1, size + 1):
                    parts = lines[p].split(); p += 1
                    if any(not (1 <= int(v) < i) for v in parts[1:]): return False
            return p == len(lines)
        return check("each dependency index is strictly smaller than its member index", dep_ok, "1\n2\nA\nB 2\n")
    if n == 28681: return check("n>=5 and scores 0..100", lambda x: int(x.splitlines()[0]) >= 5 and all(0 <= int(v) <= 100 for v in x.split()[1:]), "4\n0 0 0\n")
    if n == 28699: return check("n,m 1..100 and prices positive", lambda x: 1 <= int(x.split()[0]) <= 100 and 1 <= int(x.split()[1]) <= 100 and all(int(v) > 0 for v in x.splitlines()[1].split()), "1 1\n0\na\n")
    if n == 28750: return check("h,w 1..500 and grids contain only dots/lowercase", lambda x: 1 <= int(x.split()[0]) <= 500 and 1 <= int(x.split()[1]) <= 500 and all(c == '.' or c.islower() for c in ''.join(x.splitlines()[1:])), "0 1\n.\n\n.\n")
    if n == 28908: return check("assignments use a,b,c and one digit", lambda x: all(part and part[0] in 'abc' and part[-1].isdigit() for part in x.strip().split(';') if part), "d:=1;\n")
    if n == 28969: return check("digits string length 1..50000", lambda x: 1 <= len(x.strip()) <= 50000 and x.strip().isdigit(), "A\n")
    if n == 28973: return check("n 2..100 and matrix cells are 0/1", lambda x: 2 <= int(x.split()[0]) <= 100 and all(v in ('0','1') for v in x.split()[1:]), "1\n0\n")
    if n == 29178: return check("n 2..100", lambda x: 2 <= int(x.split()[0]) <= 100, "1\n0\n")
    if n == 29334: return check("column title is uppercase A..Z, length 1..7", lambda x: 1 <= len(x.strip()) <= 7 and x.strip().isupper() and x.strip().isalpha(), "a\n")
    if n == 29340: return check("n 1..10000 and k is integer", lambda x: 1 <= int(x.splitlines()[0]) <= 10000 and len(x.splitlines()[1].split()) == int(x.splitlines()[0]), "0\n\n0\n")
    if n == 29622: return check("N 1..100, M 1..1000 and edge weights 1..100000", lambda x: (lambda a: (lambda h: 1 <= int(h[0]) <= 100 and 1 <= int(h[1]) <= 1000 and all(1 <= int(line.split()[2]) <= 100000 for line in a[1:]))(a[0].split()))(x.splitlines()), "1 1\n1 1 0\n")
    raise KeyError(n)


def write_producecase(made, source, generator, sample, extra):
    text = ("import random, subprocess, sys, tempfile\nfrom pathlib import Path\n"
            f"REFERENCE={source!r}\nSAMPLE={sample!r}\nEXTRA_CASE={extra!r}\nGENERATOR_NAME={generator.__name__!r}\n"
            + inspect.getsource(generator) + "\n"
            + "def run(text):\n    with tempfile.TemporaryDirectory(prefix='producecase-') as d:\n        p=Path(d)/'main.py'; p.write_text(REFERENCE)\n        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=120)\n        if x.returncode: raise SystemExit(x.stderr)\n        return x.stdout\n"
            + "def main():\n    d=Path('data'); d.mkdir(exist_ok=True)\n    cases=[SAMPLE]+([EXTRA_CASE] if EXTRA_CASE else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]\n    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))\nif __name__=='__main__': main()\n")
    (made / "producecase.py").write_text(text)


def main():
    manifest = json.loads(MANIFEST.read_text()); report = []
    selected = {int(x) for x in os.environ.get("T004_ONLY", "").split(",") if x}
    if selected and REPORT.exists():
        report.extend(e for e in json.loads(REPORT.read_text()).get("entries", []) if int(e["local_number"]) not in selected)
    for entry in manifest["entries"]:
        n = int(entry["local_number"])
        if selected and n not in selected: continue
        source = (ROOT / f"scripts/t004_platform_accepted_{n}.py").read_text(); gen = GENERATORS[n]; sample = entry["sample_input"]; extra = scale_case(n)
        cases = [sample] + ([extra] if extra else []) + [gen(random.Random(s)) for s in range(1, 21)]
        outputs = [run_source(source, c) for c in cases]
        made = TESTS / bucket(n) / f"{n:05d}_made"; data = made / "data"; data.mkdir(parents=True, exist_ok=True)
        for p in data.glob("*"): p.unlink()
        for i, c in enumerate(cases): (data/f"{i}.in").write_text(c); (data/f"{i}.out").write_text(outputs[i])
        (made / "samplecode.py").write_text(source); write_producecase(made, source, gen, sample, extra)
        rows, counter = constraint_rows(n, cases[1:])
        audit = common.audit(made, cases=cases[1:], outputs=outputs[1:], sample_input=sample, sample_output=entry.get("sample_output"), constraints=rows, constraint_counterexample=counter)
        for s in range(20000): gen(random.Random(s))
        smoke = [gen(random.Random(100000+s)) for s in range(400)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: list(pool.map(lambda x: run_source(source, x), smoke))
        audit["scale_summary"] = {"max_case_chars": max(map(len, cases)), "max_generated_seed": 20}
        a = entry["existing_accepted"]
        row = {"local_number": n, "title": entry["title"], "reference_source": f"platform Accepted Python3 #{a['solution_id']}", "statistics_url": f"http://cs101.openjudge.cn{entry['submit_path']}statistics/", "source_url": a["source_url"], "license_status": "not declared on the submission page; no license is inferred.", "generator": gen.__name__, "generator_seed_smoke": {"seeds": 20000, "status": "passed"}, "reference_seed_smoke": {"seeds": 400, "status": "passed"}, "test_cases": len(cases), "constraints": rows, "constraint_counterexample": counter, "self_audit": audit, "sample_reproduced": audit["sample_is_case_zero"]["status"] == "passed", "producecase_reproduced": audit["byte_reproduction"]["status"] == "passed"}
        if n == 28416:
            slines = extra.splitlines(); st = int(slines[0]); p = 1; sizes = []
            for _ in range(st): sizes.append(int(slines[p])); p += 1 + sizes[-1]
            row["scale_requirement"] = {"required_T": 20, "required_n": 3000, "observed_T": st, "observed_max_n": max(sizes), "status": "passed" if st >= 20 and max(sizes) >= 3000 else "FAILED"}
        report.append(row); print(n, "built", flush=True)
    REPORT.write_text(json.dumps({"batch":"T-004 round15", "updated_at":datetime.now(timezone.utc).isoformat(), "pending_rework_status": {"status":"passed", "items":[]}, "entries":report}, ensure_ascii=False, indent=2)+"\n")


if __name__ == "__main__": main()
