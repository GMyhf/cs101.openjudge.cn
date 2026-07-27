#!/usr/bin/env python3
from __future__ import annotations

import inspect
import json
import os
import random
import subprocess
import sys
import tempfile
import concurrent.futures
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collab/t004-round13-manifest.json"
REPORT = ROOT / "collab/t004-round13-report.json"
TESTS = ROOT / "data/openjudge/tests"
sys.path.insert(0, str(ROOT / "scripts"))
from build_001a import bucket
import t004_common as common


def g24755(r): return f"{r.randint(2, 12)}\n"

def g24830(r):
    n = r.randint(2, 100)
    h = [r.randint(0, 10000) for _ in range(n)]
    if r.random() < .65:
        start = r.randint(0, 9999); h = [max(0, start - i * r.randint(1, 100)) for i in range(n)]
    return f"{n}\n{' '.join(map(str, h))}\n"

def g24837(r):
    p = r.randint(100, 10**8); x = r.randint(1, 9); y = r.randint(2, 9)
    q = (p - x * r.randint(1, min(30, (p - 1) // x))
         if r.random() < .55 else r.randint(1, 10**8))
    return f"{p} {q} {x} {y}\n"

def g25139(r):
    letters = list("ABCDE")
    def word(): return "".join(r.choice(letters[:r.randint(2, 5)]) for _ in range(r.randint(1, 6)))
    a, b = word(), word(); c = word()
    known = r.choice(["A A BC", "ABCD BCD ACEA", "A A B"])
    return f"3\nA A BC\n{a} {b} {c}\n{known}\n"

def g25274(r): return "[[1, 2, 3], 'abc', [1, 3], 4]\n"

def g25301(r):
    n = r.randint(2, 60); rows = []
    for i in range(n):
        month, day = r.randint(1, 12), r.randint(1, 28)
        rows.append(f"{50800000 + i:08d} {month} {day}")
    return f"{n}\n" + "\n".join(rows) + "\n"

def g25394(r):
    k = r.randint(1, 5); rows = []
    for _ in range(k):
        n = r.randint(4, 8)
        rows += [str(n), " ".join(str(r.randint(1, 13)) for _ in range(n))]
    return f"{k}\n" + "\n".join(rows) + "\n"

def g25580(r):
    h, l, n = r.randint(1, 99999), r.randint(0, 9999), r.randint(1, 99)
    vs = [f"{r.uniform(0.1, 999):.3f}" for _ in range(n)]
    return f"{h} {l} {n}\n{' '.join(vs)}\n"

def g25684(r):
    m, c = r.randint(1, 20), r.randint(1, 100)
    rows = [f"{r.randint(1, 100)} {r.randint(0, 100000)} {r.randint(1, 10)}" for _ in range(m)]
    return f"{m} {c}\n" + "\n".join(rows) + "\n"

def g25711(r):
    n = r.randint(2, 80); m = r.randint(1, n); rows = []
    for i in range(n):
        courses = r.randint(1, 5); vals = []
        for _ in range(courses): vals += [str(r.randint(60, 100)), str(r.randint(1, 6))]
        rows.append(f"{2201000000 + i} " + " ".join(vals))
    return f"{n} {m}\n" + "\n".join(rows) + "\n"

def g26144(r): return f"{r.randint(1, 9)}\n"

def g26267(r):
    n, m = r.randint(1, 10000), r.randint(1, 1000)
    t = "".join(r.choice("ABCD") for _ in range(m)); s = "".join(r.choice("ABCD") for _ in range(n))
    if r.random() < .5 and m <= n:
        at = r.randint(0, n - m); s = s[:at] + t + s[at + m:]
    return f"{s}\n{t}\n"

def g26273(r):
    n = r.randint(1, 10000)
    unit = "".join(r.choice("abc") for _ in range(r.randint(2, 30)))
    return (unit * ((n + len(unit) - 1) // len(unit)))[:n] + "\n"

def g26588(r):
    t = r.randint(1, 20); rows = [str(t)]
    for _ in range(t): rows.append("".join(r.choice("0123456789") for _ in range(r.randint(1, 100))) )
    return "\n".join(rows) + "\n"

def g26835(r):
    n = r.randint(2, 30); edges = []
    for i in range(1, n): edges.append((r.randrange(i), i, float(r.randint(1, 99999))))
    seen = {(min(a, b), max(a, b)) for a, b, _ in edges}
    target = min(4999, n * (n - 1) // 2)
    while len(edges) < target:
        a, b = r.sample(range(n), 2); key = (min(a, b), max(a, b))
        if key not in seen: seen.add(key); edges.append((a, b, r.uniform(0, 99999)))
    r.shuffle(edges)
    return f"{n} {len(edges)}\n" + "\n".join(f"{a} {b} {w:.3f}" for a, b, w in edges) + "\n"

def g26998(r):
    t = r.randint(1, 8); rows = [str(t)]
    for _ in range(t):
        n = r.randint(1, 100); rows += [str(n), " ".join(str(r.randint(1, 10**9)) for _ in range(n))]
    return "\n".join(rows) + "\n"

def g27277(r):
    coins = sorted(set(r.randint(1, 100) for _ in range(r.randint(2, 5))))
    return " ".join(map(str, coins)) + f"\n{r.randint(0, 10000)}\n"

def g27278(r):
    m = r.randint(1, 10); n = r.randint(m, 100); d = [r.randint(0, m) for _ in range(n)]
    for i in range(1, m + 1): d[r.randrange(n)] = i
    a = [r.randint(0, 100000) for _ in range(m)]
    if r.random() < .3:
        m, n = 1, r.randint(2, 100); d, a = [0] * (n - 1) + [1], [n - 1]
    return f"{n} {m}\n{' '.join(map(str, d))}\n{' '.join(map(str, a))}\n"

def g27307(r):
    n = r.randint(1, 100); hp = [r.randint(1, 1000) for _ in range(n)]; tm = [r.randint(1, 1000) for _ in range(n)]
    return f"{n}\n{' '.join(map(str, hp))}\n{' '.join(map(str, tm))}\n"

def g27311(r):
    n = r.randint(1, 10000); p = [r.randint(0, 10000) for _ in range(n)]; t = [r.randint(0, 10000) for _ in range(n)]
    return f"{n}\n{' '.join(map(str, p))}\n{' '.join(map(str, t))}\n"


GENERATORS = {n: globals()[f"g{n}"] for n in (24755, 24830, 24837, 25139, 25274, 25301, 25394, 25580, 25684, 25711, 26144, 26267, 26273, 26588, 26835, 26998, 27277, 27278, 27307, 27311)}


def scale_case(n):
    if n == 24755:
        return "8\n"
    if n == 26144:
        return "7\n"
    if n == 26267:
        return "A" * 1000000 + "\n" + "A" * 1000 + "\n"
    if n == 26273:
        return ("abcdefghij" * 10000) + "\n"
    if n == 26835:
        edges = [(i - 1, i, float(i)) for i in range(1, 99)]
        for i in range(99):
            for j in range(i + 2, min(99, i + 12)):
                edges.append((i, j, float(10000 + i * 99 + j)))
        return "99 %d\n%s\n" % (len(edges), "\n".join(f"{a} {b} {w:.3f}" for a, b, w in edges))
    if n == 27311:
        return "100000\n" + " ".join(str(i % 10001) for i in range(100000)) + "\n" + " ".join(str((i * 7) % 10001) for i in range(100000)) + "\n"
    return None


def run_source(source, text):
    with tempfile.TemporaryDirectory(prefix="t004-r13-run-") as d:
        path = Path(d) / "main.py"; path.write_text(source)
        x = subprocess.run([sys.executable, str(path)], input=text, text=True, capture_output=True, timeout=60)
        if x.returncode: raise RuntimeError(x.stderr[-1000:] or str(x.returncode))
        return x.stdout


def constraint_rows(n, cases):
    def check(label, pred, bad):
        good = bool(all(pred(x) for x in cases)); bad_value = bool(pred(bad))
        return [(label, good)], (bad, [(label, bad_value)])
    if n == 24755: return check("1 < n < 13", lambda x: 1 < int(x) < 13, "13\n")
    if n == 24830: return check("n is 2..100 and heights are 0..10000", lambda x: (lambda a: 2 <= int(a[0]) <= 100 and len(a[1:]) == int(a[0]) and all(0 <= int(v) <= 10000 for v in a[1:]))(x.split()), "2\n0 10001\n")
    if n == 24837: return check("p,q are positive and x,y are positive integers", lambda x: all(int(v) > 0 for v in x.split()), "0 1 1 2\n")
    if n == 25139: return check("each word uses only A..E and has length at most 10", lambda x: all(1 <= len(w) <= 10 and set(w) <= set("ABCDE") for w in x.split()[1:]), "1\nA F B\n")
    if n == 25274: return [], ("[[1, 2, 3], 'abc', [1, 3], 4]\n", [])
    if n == 25301: return check("month/day are valid", lambda x: all(1 <= int(l.split()[1]) <= 12 and 1 <= int(l.split()[2]) <= 31 for l in x.splitlines()[1:]), "1\n1 13 1\n")
    if n == 25394: return check("N is 4..8 and card points are 1..13", lambda x: all(4 <= int(v) <= 8 for v in x.splitlines()[1::2]) and all(1 <= int(v) <= 13 for v in x.split()), "1\n3\n1 2 3\n")
    if n == 25580: return check("H,L,n,v satisfy stated positive bounds", lambda x: (lambda a: 0 < float(a[0]) < 100000 and 0 <= float(a[1]) < 10000 and 0 < int(a[2]) < 100 and all(0 < float(v) < 1000 for v in a[3:]))(x.split()), "1 0 1\n0\n")
    if n == 25684: return check("requested intervals lie in seats 0..1e6", lambda x: all(0 <= int(v) <= 1000000 for l in x.splitlines()[1:] for v in (l.split()[1], str(int(l.split()[1])+int(l.split()[2])))), "1 1\n1 1000000 1\n")
    if n == 25711: return check("scores are 0..100 and credits are positive", lambda x: all(0 <= int(v) <= 100 for l in x.splitlines()[1:] for v in l.split()[1::2]), "1 1\n2201000000 101 1\n")
    if n == 26144: return check("1 <= n <= 9", lambda x: 1 <= int(x) <= 9, "10\n")
    if n == 26267: return check("S and T are nonempty uppercase strings", lambda x: all(v.isupper() and v.isalpha() for v in x.split()), "A\nA1\n")
    if n == 26273: return check("string is lowercase and length 1..1e6", lambda x: 1 <= len(x.strip()) <= 1000000 and x.strip().islower(), "A\n")
    if n == 26588: return check("count is 1..99 and strings contain digits", lambda x: int(x.splitlines()[0]) == len(x.splitlines())-1 and 1 <= int(x.splitlines()[0]) < 100, "0\n")
    if n == 26835: return check("edge endpoints are distinct valid vertices", lambda x: (lambda a: all(0 <= int(v) < int(a[0].split()[0]) for l in a[1:] for v in l.split()[:2]) and all(l.split()[0] != l.split()[1] for l in a[1:]))(x.splitlines()), "2 1\n0 2 1\n")
    if n == 26998: return check("sequence values are positive and <= 1e9", lambda x: all(1 <= int(v) <= 1000000000 for v in x.split()[2:]), "1\n1\n0\n")
    if n == 27277: return check("coin denominations and amount are nonnegative within bounds", lambda x: all(1 <= int(v) <= 10000 for v in x.splitlines()[0].split()) and 0 <= int(x.splitlines()[1]) <= 10000, "1 2\n10001\n")
    if n == 27278: return check("n,m and study requirements are within bounds", lambda x: (lambda a: 1 <= int(a[1]) <= 10 and int(a[0]) >= int(a[1]) and all(0 <= int(v) <= 100000 for v in a[-int(a[1]):]))(x.split()), "1 2\n1\n1 1\n")
    if n == 27307: return check("n is positive and hp/time are positive", lambda x: all(int(v) > 0 for v in x.split()), "1\n0\n1\n")
    if n == 27311: return check("N<=100000 and temperatures are nonnegative <=10000", lambda x: (lambda a: int(a[0]) == len(a[1:])//2 and 0 <= int(a[0]) <= 100000 and all(0 <= int(v) <= 10000 for v in a[1:]))(x.split()), "1\n0\n10001\n")
    raise KeyError(n)


def write_producecase(made, source, generator, sample, extra):
    text = ("import random, subprocess, sys, tempfile\nfrom pathlib import Path\n"
            f"REFERENCE={source!r}\nSAMPLE={sample!r}\nEXTRA_CASE={extra!r}\nGENERATOR_NAME={generator.__name__!r}\n"
            + inspect.getsource(generator) + "\n"
            + "def run(text):\n    with tempfile.TemporaryDirectory(prefix='producecase-') as d:\n        p=Path(d)/'main.py'; p.write_text(REFERENCE)\n        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=60)\n        if x.returncode: raise SystemExit(x.stderr)\n        return x.stdout\n"
            + "def scale_case():\n    if EXTRA_CASE is not None: return EXTRA_CASE\n    if GENERATOR_NAME == 'g26267': return 'A'*1000000+'\\n'+'A'*1000+'\\n'\n    if GENERATOR_NAME == 'g26273': return ('abcdefghij'*10000)+'\\n'\n    if GENERATOR_NAME == 'g26835':\n        e=[(i-1,i,float(i)) for i in range(1,99)]\n        for i in range(99):\n            for j in range(i+2,min(99,i+12)): e.append((i,j,float(10000+i*99+j)))\n        return '99 %d\\n'%len(e)+'\\n'.join(f'{a} {b} {w:.3f}' for a,b,w in e)+'\\n'\n    if GENERATOR_NAME == 'g27311': return '100000\\n'+' '.join(str(i%10001) for i in range(100000))+'\\n'+' '.join(str((i*7)%10001) for i in range(100000))+'\\n'\n    return None\n"
            + "def main():\n    d=Path('data'); d.mkdir(exist_ok=True)\n    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]\n    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))\nif __name__=='__main__': main()\n")
    (made / "producecase.py").write_text(text)


def main():
    manifest = json.loads(MANIFEST.read_text()); report = []
    selected = {int(x) for x in os.environ.get("T004_ONLY", "").split(",") if x}
    if selected and REPORT.exists():
        old = json.loads(REPORT.read_text()).get("entries", [])
        report.extend(entry for entry in old if int(entry["local_number"]) not in selected)
    for entry in manifest["entries"]:
        n = int(entry["local_number"]); gen = GENERATORS[n]; sample = entry["sample_input"]
        if selected and n not in selected:
            continue
        source = (ROOT / f"scripts/t004_platform_accepted_{n:05d}.py").read_text()
        a = entry["existing_accepted"]; reference_kind = f"platform Accepted Python3 #{a['solution_id']}"
        made = TESTS / bucket(n) / f"{n:05d}_made"; data = made / "data"; data.mkdir(parents=True, exist_ok=True)
        for p in data.glob("*"): p.unlink()
        extra = scale_case(n)
        cases = [sample] + ([extra] if extra else []) + [gen(random.Random(s)) for s in range(1, 21)]
        outputs = [run_source(source, c) for c in cases]
        for i, c in enumerate(cases): (data/f"{i}.in").write_text(c); (data/f"{i}.out").write_text(outputs[i])
        header = (f"# External reference: statistics page /practice/{n:05d}/\n# Accepted submission: {a['solution_id']}\n# Source: {a['source_url']}\n# License: not declared on the submission page; no license is inferred.\n\n")
        (made / "samplecode.py").write_text(source if source.startswith("# External reference:") else header + source)
        write_producecase(made, source, gen, sample, extra)
        rows, counter = constraint_rows(n, cases[1:])
        fixed = n == 25274
        domain_exemption = ("题面输入是固定字面量，输入域只有一种，去重低于15不适用" if fixed else
                            "题面 n 的合法取值只有 2..12，共 11 种" if n == 24755 else
                            "题面 n 的合法取值只有 1..9，共 9 种" if n == 26144 else None)
        audit = common.audit(made, cases=cases[1:], outputs=outputs[1:], sample_input=sample,
            sample_output=entry.get("sample_output"), sample_output_exemption=entry.get("sample_output_exemption"),
            exemption=domain_exemption,
            constraints=rows, constraint_counterexample=counter,
            constraint_exemption=("题面输入是固定字面量，只有一种可机械验证的输入" if fixed else None))
        for s in range(20000): gen(random.Random(s))
        smoke_cases = [gen(random.Random(100000+s)) for s in range(400)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda text: run_source(source, text), smoke_cases))
        audit["scale_summary"] = {"max_case_chars": max(map(len, cases)), "max_generated_seed": 20}
        report.append({"local_number": n, "title": entry["title"], "reference_source": reference_kind,
            "statistics_url": f"http://cs101.openjudge.cn{entry['submit_path']}statistics/", "source_url": a["source_url"],
            "license_status": "not declared on the submission page; no license is inferred.", "generator": gen.__name__,
            "generator_seed_smoke": {"seeds": 20000, "status": "passed"}, "reference_seed_smoke": {"seeds": 400, "status": "passed"},
            "test_cases": len(cases), "constraints": rows, "constraint_counterexample": counter,
            "self_audit": audit, "sample_reproduced": audit["sample_is_case_zero"]["status"] == "passed",
            "producecase_reproduced": audit["byte_reproduction"]["status"] == "passed"})
        print(n, "built", flush=True)
    pending = common.pending_rework_status(manifest.get("pending_rework", []), TESTS)
    REPORT.write_text(json.dumps({"batch":"T-004 round13", "updated_at":datetime.now(timezone.utc).isoformat(),
                                  "pending_rework_status": pending, "entries":report}, ensure_ascii=False, indent=2)+"\n")


if __name__ == "__main__": main()
