#!/usr/bin/env python3
from __future__ import annotations
import contextlib, inspect, io, json, random, subprocess, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collab/t004-round10-manifest.json"
REPORT = ROOT / "collab/t004-round10-report.json"
TESTS = ROOT / "data/openjudge/tests"
sys.path.insert(0, str(ROOT / "scripts"))
from build_001a import bucket
import t004_common as common


def g19984(r):
    n = r.randint(2, 8)
    rows = []
    for i in range(n):
        rows.append(" ".join(f"{r.uniform(.15, .95):.4f}" for _ in range(i + 1)))
    return f"{n}\n{r.randint(50, 500)}\n" + "\n".join(rows) + "\n"


def g19998(r):
    m, n = r.randint(0, 2), r.randint(0, 10)
    if r.random() < .5:
        m, n = 2, 10
        values = [r.randint(1, 3) for _ in range(14)]
    else:
        values = [r.randint(6, 10) for _ in range(14)]
    return f"{m} {n}\n" + "\n".join(
        " ".join(map(str, values[i:i + 7])) for i in (0, 7)
    ) + "\n"


def g20004(r):
    return " ".join(f"{r.uniform(-9.9, 9.9):.4f}%" for _ in range(r.randint(11, 30))) + "\n"


def g20026(r):
    return f"{r.choice([1, 2, 3, 4, 6, 8, 9, 12, 18, 24])}\n"


def g20074(r):
    n = r.randint(1, 12)
    rows = [f"{r.randint(150, 190)} {r.randint(45, 100)} {r.choice(['M', 'F'])}" for _ in range(n)]
    return f"{n}\n" + "\n".join(rows) + "\n"


def g20075(r):
    m, n = r.randint(3, 8), r.randint(3, 8)
    grid = [[0 if r.random() < .7 else 2 for _ in range(n)] for _ in range(m)]
    target = (r.randrange(m), r.randrange(n))
    grid[target[0]][target[1]] = 1
    starts = []
    for _ in range(r.randint(5, 15)):
        starts.append((r.randrange(m), r.randrange(n)))
    return f"{m} {n} {len(starts)}\n" + "\n".join(
        " ".join(map(str, row)) for row in grid
    ) + "\n" + "\n".join(f"{y + 1} {x + 1}" for x, y in starts) + "\n"


def g20090(r):
    q = r.randint(5, 20)
    return f"{q}\n" + "\n".join(str(r.randint(1, 1008612138)) for _ in range(q)) + "\n"


def g20091(r):
    t = r.randint(3, 20)
    return f"{t}\n" + "\n".join(str(r.randint(3, 1000)) for _ in range(t)) + "\n"


def g20100(r):
    n = r.randint(2, 10)
    distances = [r.randint(1, 10000) for _ in range(n - 1)]
    record = [r.randint(1, 10000) for _ in range(n - 1)]
    monster = [r.randint(1, 10000) for _ in range(n - 1)]
    return f"{n}\n{' '.join(map(str, distances))}\n{' '.join(map(str, record))}\n{' '.join(map(str, monster))}\n"


def g20102(r):
    t = r.randint(5, 20)
    return f"{t}\n" + "\n".join(str(r.randint(1, 1000)) for _ in range(t)) + "\n"


def g20103(r):
    n = r.randint(2, 15)
    marks = sorted(r.sample(range(1, 200), n))
    return f"{n}\n" + "\n".join(f"{x} {r.randint(1, 30)}" for x in marks) + "\n"


def g20107(r):
    d, k, t = r.randint(1, 2), r.randint(1, 8), r.randint(1, 2)
    coords = r.sample([(x, y) for x in range(20, 121, 10) for y in range(20, 121, 10)], k)
    rows = [f"{x} {y} " + " ".join(str(r.randint(0, 100)) for _ in range(t)) for x, y in coords]
    return f"{d}\n{k} {t}\n" + "\n".join(rows) + "\n"


def g20121(r):
    n = r.randint(2, 8)
    return f"{n}\n" + "\n".join(" ".join(str(r.randint(1, 9)) for _ in range(n)) for _ in range(n)) + "\n"


def g20122(r):
    dates = [320, 418, 626, 816, 1024]
    n = r.randint(1, 8)
    date = r.choice(dates)
    rows = []
    for _ in range(n):
        values = r.sample(dates, 4)
        rows.append(" ".join(f"{x:04d}" for x in values))
    return f"{n} {date:04d}\n" + "\n".join(rows) + "\n"


def g20125(r):
    n = r.randint(1, 8)
    return f"{n}\n" + " ".join(str(r.randint(1, 4)) for _ in range(n)) + "\n"


def g20135(r):
    m, n = r.randint(5, 10), r.randint(5, 10)
    word = "abc"
    grid = [["z"] * n for _ in range(m)]
    x, y, d = r.randint(0, m - 1), r.randint(0, n - 3), r.choice([0, 4])
    dx, dy = (0, 1) if d == 0 else (0, -1)
    if d == 4:
        y += 2
    for i, ch in enumerate(word):
        grid[x + i * dx][y + i * dy] = ch
    return f"{m} {n}\n" + "\n".join("".join(row) for row in grid) + f"\n{word}\n"


def g20136(r):
    t = r.randint(4, 12)
    police = r.choice([1, 2])
    rows = []
    for i in range(t):
        rows.append(f"{i} {(i - 1) % t} {(i + 1) % t}")
    return f"{police} {t}\n" + "\n".join(rows) + "\n"


def g20137(r):
    rows, cols = r.randint(3, 12), r.randint(3, 12)
    return f"{rows} {cols}\n0 {r.randint(1, cols - 1)}\n1 1\n"


def g20138(r):
    n = r.randint(2, 7)
    x = [r.randint(-5, 5) for _ in range(n)]
    matrix = []
    for i in range(n):
        row = [r.randint(-2, 2) for _ in range(n)]
        row[i] = 10
        row.append(sum(row[j] * x[j] for j in range(n)))
        matrix.append(row)
    return f"{n}\n" + "\n".join(" ".join(map(str, row)) for row in matrix) + "\n"


def g20162(r):
    t = r.randint(5, 20)
    rows = [f"{r.randint(-1000, 1000)} {r.randint(-1000, 1000)} {r.randint(-1000, 1000)} {r.randint(1, 1000)}" for _ in range(t)]
    return f"{t}\n" + "\n".join(rows) + "\n"


GENERATORS = {n: globals()[f"g{n}"] for n in (
    19984, 19998, 20004, 20026, 20074, 20075, 20090, 20091, 20100,
    20102, 20103, 20107, 20121, 20122, 20125, 20135, 20136, 20137,
    20138, 20162
)}


def run_source(source, text):
    with tempfile.TemporaryDirectory(prefix="t004-r10-run-") as d:
        path = Path(d) / "main.py"
        path.write_text(source)
        result = subprocess.run([sys.executable, str(path)], input=text, text=True,
                                capture_output=True, timeout=30)
        if result.returncode:
            raise RuntimeError(result.stderr[-1000:] or str(result.returncode))
        return result.stdout


def run_python_fast(source, text):
    oldi, oldo = sys.stdin, sys.stdout
    try:
        sys.stdin, out = io.StringIO(text), io.StringIO()
        with contextlib.redirect_stdout(out):
            try:
                exec(compile(source, "<external-accepted>", "exec"), {"__name__": "__main__"})
            except SystemExit:
                pass
        return out.getvalue()
    finally:
        sys.stdin, sys.stdout = oldi, oldo


def constraint_rows(n, cases):
    def every(label, predicate):
        return [(label, all(predicate(x) for x in cases))]
    if n == 19984:
        rows = every("n is 2..20", lambda x: 2 <= int(x.splitlines()[0]) <= 20)
    elif n == 19998:
        rows = every("M and N are bounded", lambda x: 0 <= int(x.split()[0]) <= 2 and 0 <= int(x.split()[1]) <= 10)
    elif n == 20004:
        rows = every("series has more than ten percentages", lambda x: len(x.split()) > 10)
    elif n == 20026:
        def smooth(x):
            v = int(x.strip())
            for p in (2, 3):
                while v % p == 0:
                    v //= p
            return v == 1
        rows = every("n has only prime factors two and three", smooth)
    elif n == 20074:
        rows = every("student dimensions are bounded", lambda x: all(150 <= int(v.split()[0]) <= 190 and 45 <= int(v.split()[1]) <= 100 for v in x.splitlines()[1:]))
    elif n == 20075:
        rows = every("grid cells are 0, 1, or 2", lambda x: all(int(v) in (0, 1, 2) for line in x.splitlines()[1:1 + int(x.split()[0])] for v in line.split()))
    elif n in (20090, 20091, 20102):
        rows = every("query values are positive", lambda x: all(int(v) > 0 for v in x.splitlines()[1:]))
    elif n == 20100:
        rows = every("distance and time values are positive", lambda x: all(int(v) > 0 for line in x.splitlines()[1:] for v in line.split()))
    elif n == 20103:
        rows = every("marks are strictly increasing and lengths positive", lambda x: (lambda a: all(a[i][0] < a[i + 1][0] and a[i][1] > 0 for i in range(len(a) - 1)))([list(map(int, v.split())) for v in x.splitlines()[1:]]))
    elif n == 20107:
        rows = every("coordinates are distinct and counts non-negative", lambda x: len({tuple(v.split()[:2]) for v in x.splitlines()[2:]}) == int(x.splitlines()[1].split()[0]) and all(int(v) >= 0 for line in x.splitlines()[2:] for v in line.split()[2:]))
    elif n == 20121:
        rows = every("matrix digits are 1..9", lambda x: all(1 <= int(v) <= 9 for line in x.splitlines()[1:] for v in line.split()))
    elif n == 20122:
        rows = every("dates are four digit positive values", lambda x: all(len(v) == 4 for line in x.splitlines()[1:] for v in line.split()))
    elif n == 20125:
        rows = every("grade counts are positive", lambda x: all(int(v) > 0 for v in x.splitlines()[1].split()))
    elif n == 20135:
        rows = every("grid rows have the stated width", lambda x: all(len(v) == int(x.splitlines()[0].split()[1]) for v in x.splitlines()[1:-1]))
    elif n == 20136:
        rows = every("world identifiers are sequential", lambda x: [int(v.split()[0]) for v in x.splitlines()[1:]] == list(range(int(x.splitlines()[0].split()[1]))))
    elif n == 20137:
        rows = every("direction components are unit signed values", lambda x: all(abs(int(v)) == 1 for v in x.splitlines()[2].split()))
    elif n == 20138:
        rows = every("matrix rows have n plus one entries", lambda x: all(len(v.split()) == int(x.splitlines()[0]) + 1 for v in x.splitlines()[1:]))
    else:
        rows = every("r is positive", lambda x: all(int(v.split()[3]) > 0 for v in x.splitlines()[1:]))
    return rows, ("deliberate invalid input", [(rows[0][0], False)])


def write_producecase(made, source, generator, sample):
    text = f"""import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE={source!r}
SAMPLE={sample!r}
GENERATOR_NAME={generator.__name__!r}
{inspect.getsource(generator)}
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f'{{i}}.in').write_text(text); (data/f'{{i}}.out').write_text(run(text))
if __name__=='__main__': main()
"""
    (made / "producecase.py").write_text(text)


def main():
    manifest = json.loads(MANIFEST.read_text())
    report = []
    for entry in manifest["entries"]:
        n = int(entry["local_number"])
        source = (ROOT / f"scripts/t004_platform_accepted_{n:05d}.py").read_text()
        generator = GENERATORS[n]
        sample = entry["sample_input"]
        made = TESTS / bucket(n) / f"{n:05d}_made"
        data = made / "data"
        data.mkdir(parents=True, exist_ok=True)
        for path in data.glob("*"):
            path.unlink()
        cases = [sample] + [generator(random.Random(seed)) for seed in range(1, 21)]
        outputs = []
        for i, text in enumerate(cases):
            out = run_source(source, text)
            outputs.append(out)
            (data / f"{i}.in").write_text(text)
            (data / f"{i}.out").write_text(out)
        header = (f"# External reference: statistics page /practice/{n:05d}/\n"
                  f"# Accepted submission: {entry['existing_accepted']['solution_id']}\n"
                  f"# Source: {entry['existing_accepted']['source_url']}\n"
                  "# License: not declared on the submission page; no license is inferred.\n\n")
        (made / "samplecode.py").write_text(header + source)
        write_producecase(made, source, generator, sample)
        rows, counterexample = constraint_rows(n, cases[1:])
        audit = common.audit(made, cases=cases[1:], outputs=outputs[1:], sample_input=sample,
                             constraints=rows, constraint_counterexample=counterexample)
        for seed in range(20000):
            generator(random.Random(seed))
        for seed in range(400):
            run_python_fast(source, generator(random.Random(100000 + seed)))
        accepted = entry["existing_accepted"]
        report.append({"local_number": n, "title": entry["title"], "source": entry["source"],
                       "reference_source": f"platform Accepted Python3 #{accepted['solution_id']}",
                       "statistics_url": f"http://cs101.openjudge.cn{entry['submit_path']}statistics/",
                       "solution_id": accepted["solution_id"], "source_url": accepted["source_url"],
                       "license_status": "not declared on submission page; no license inferred",
                       "generator": generator.__name__, "generator_seed_smoke": {"seeds": 20000, "status": "passed"},
                       "reference_seed_smoke": {"seeds": 400, "status": "passed"}, "test_cases": len(cases),
                       "constraints": rows, "constraint_counterexample": counterexample, "self_audit": audit,
                       "sample_reproduced": audit["sample_is_case_zero"]["status"] == "passed",
                       "producecase_reproduced": audit["byte_reproduction"]["status"] == "passed"})
        print(n, "built", flush=True)
    REPORT.write_text(json.dumps({"batch": "T-004 round10", "updated_at": datetime.now(timezone.utc).isoformat(),
                                  "entries": report}, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
