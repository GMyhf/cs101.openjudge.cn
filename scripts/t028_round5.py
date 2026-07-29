#!/usr/bin/env python3
"""Build T-028 round 5 (corrected priorities 61 through 80)."""
from __future__ import annotations

import inspect
import json
import random
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import t004_common as common
from build_001b import first_sample
from select_solution_batch import SOURCES, sections

ROOT = Path(__file__).resolve().parents[1]
OPENJUDGE = ROOT / "data" / "openjudge"
CANDIDATES = ROOT / "collab" / "t028-candidates.json"
SOURCE_URLS = {
    0: "https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md",
    1: "https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md",
}
TARGETS = list(range(61, 81))
SOURCE_CODE_INDEX = {number: 2 for number in (
    1258, 1661, 1664, 1703, 1958, 2812, 1042, 2226, 1064, 1185,
    2229, 2533, 2659, 2946, 1037, 1160, 1944, 2385, 2711, 2797,
)}

LABELS = {
    1258: "3<=N<=100 and every case contains an N by N symmetric distance matrix",
    1661: "each case has 1<=N<=1000, ordered platform endpoints, and Y/MAX within bounds",
    1664: "1<=M,N<=10 for every apple-and-plate case",
    1703: "1<=case IDs<=N<=100000 and every operation is A or D",
    1958: "the problem has no input",
    2812: "1<=R,C<=5000 and 3<=N<=5000 distinct rice coordinates lie inside the field",
    1042: "2<=n<=25, 1<=h<=16, nonnegative fish/decrease values, and positive travel times",
    2226: "1<=R,C<=50 and the grid contains only '*' and '.'",
    1064: "1<=N,K<=10000 and every cable length is 1m..100km at centimetre precision",
    1185: "1<=N<=100, 1<=M<=10, and every terrain cell is P or H",
    2229: "1<=N<=1000000",
    2533: "1<=N<=1000 and every sequence value is in 0..10000",
    2659: "1<=A,B,K<=100, bomb centres are on-board, and every diameter is odd in 1..99",
    2946: "the operation count matches and every operation is plus, minus, or multiply",
    1037: "1<=K<=100, 1<=N<=20, and C selects an existing alternating permutation",
    1160: "1<=P<=V<=300 and village coordinates are strictly increasing in 1..10000",
    1944: "1<=N<=1000, 1<=P<=10000, and communication pairs are unique valid barns",
    2385: "1<=T<=1000, 1<=W<=30, and each falling apple is from tree 1 or 2",
    2711: "2<=N<=100 and every height is in 130..230",
    2797: "2..1000 distinct lowercase words each have length 1..20",
}

INVALID = {
    1258: "2\n0 1\n1 0\n", 1661: "1\n0 0 1 1\n", 1664: "1\n11 1\n",
    1703: "1\n3 1\nX 1 2\n", 1958: "unexpected\n", 2812: "2 2\n3\n1 1\n1 1\n2 2\n",
    1042: "1\n1\n0\n0\n0\n", 2226: "1 1\nX\n", 1064: "1 0\n1.00\n",
    1185: "1 1\nX\n", 2229: "1000001\n", 2533: "2\n0 10001\n",
    2659: "2 2 1\n3 1 2 1\n", 2946: "0 1\ndivide 2\n", 1037: "1\n21 1\n",
    1160: "2 1\n5 5\n", 1944: "3 2\n1 2\n2 1\n", 2385: "1 31\n1\n",
    2711: "2\n129 231\n", 2797: "abc\nabc\n",
}


def fence_counts(n):
    if n == 1:
        return 1
    count = [[[0, 0] for _ in range(n + 1)] for _ in range(n + 1)]
    count[1][1] = [1, 1]
    for size in range(2, n + 1):
        for first in range(1, size + 1):
            count[size][first][0] = sum(count[size - 1][second][1]
                                            for second in range(first, size))
            count[size][first][1] = sum(count[size - 1][second][0]
                                            for second in range(1, first))
    return sum(sum(count[n][first]) for first in range(1, n + 1))


def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    if number == 1258:
        cases = []
        for _ in range(r.randint(1, 3)):
            n = r.randint(3, 18)
            matrix = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    matrix[i][j] = matrix[j][i] = r.randint(1, 100000)
            cases.append(str(n) + "\n" + "\n".join(" ".join(map(str, row)) for row in matrix))
        return "\n".join(cases) + "\n"
    if number == 1661:
        cases = []
        for _ in range(r.randint(1, 4)):
            n = r.randint(1, 12); y = r.randint(2, 200); max_drop = y
            platforms = []
            for height in r.sample(range(1, y), min(n, y - 1)):
                left = r.randint(20, 1000); platforms.append((left, left + r.randint(1, 30), height))
            while len(platforms) < n:
                left = 1100 + len(platforms) * 40; platforms.append((left, left + 10, 1))
            cases.append(f"{n} 0 {y} {max_drop}\n" + "\n".join("%d %d %d" % p for p in platforms))
        return str(len(cases)) + "\n" + "\n".join(cases) + "\n"
    if number == 1664:
        values = [(r.randint(1, 10), r.randint(1, 10)) for _ in range(r.randint(1, 20))]
        return str(len(values)) + "\n" + "\n".join(f"{m} {n}" for m, n in values) + "\n"
    if number == 1703:
        cases = []
        for _ in range(r.randint(1, 4)):
            n = r.randint(3, 80); gangs = [0, 1] + [r.randrange(2) for _ in range(n - 2)]; ops = []
            for _ in range(r.randint(3, 100)):
                a, b = r.sample(range(n), 2)
                if r.random() < .55:
                    while gangs[a] == gangs[b]: b = r.randrange(n)
                    ops.append(f"D {a+1} {b+1}")
                else: ops.append(f"A {a+1} {b+1}")
            cases.append(f"{n} {len(ops)}\n" + "\n".join(ops))
        return str(len(cases)) + "\n" + "\n".join(cases) + "\n"
    if number == 1958:
        return ""
    if number == 2812:
        rows, cols = r.randint(5, 40), r.randint(5, 40); planted_row = r.randint(1, rows)
        points = {(planted_row, col) for col in range(1, cols + 1)}
        target = r.randint(max(3, cols), min(rows * cols, cols + 80))
        while len(points) < target: points.add((r.randint(1, rows), r.randint(1, cols)))
        points = list(points); r.shuffle(points)
        return f"{rows} {cols}\n{len(points)}\n" + "\n".join(f"{x} {y}" for x, y in points) + "\n"
    if number == 1042:
        cases = []
        for _ in range(r.randint(1, 3)):
            n = r.randint(2, 8); h = r.randint(1, 5)
            fish = [r.randint(0, 100) for _ in range(n)]; decreases = [r.randint(0, 20) for _ in range(n)]
            travel = [r.randint(1, min(12, h * 12)) for _ in range(n - 1)]
            cases.append("\n".join((str(n), str(h), " ".join(map(str, fish)),
                                     " ".join(map(str, decreases)), " ".join(map(str, travel)))))
        return "\n".join(cases) + "\n0\n"
    if number == 2226:
        rows, cols = r.randint(1, 18), r.randint(1, 18)
        grid = ["".join(r.choice("***...") for _ in range(cols)) for _ in range(rows)]
        return f"{rows} {cols}\n" + "\n".join(grid) + "\n"
    if number == 1064:
        n, k = r.randint(1, 80), r.randint(1, 500)
        lengths = [r.randint(100, 10_000_000) for _ in range(n)]
        return f"{n} {k}\n" + "\n".join(f"{x//100}.{x%100:02d}" for x in lengths) + "\n"
    if number == 1185:
        rows, cols = r.randint(1, 25), r.randint(1, 10)
        return f"{rows} {cols}\n" + "\n".join("".join(r.choice("PPPH") for _ in range(cols)) for _ in range(rows)) + "\n"
    if number == 2229:
        return f"{r.randint(1, 1_000_000)}\n"
    if number == 2533:
        values = [r.randint(0, 10000) for _ in range(r.randint(1, 200))]
        return f"{len(values)}\n" + " ".join(map(str, values)) + "\n"
    if number == 2659:
        rows, cols, count = r.randint(1, 30), r.randint(1, 30), r.randint(1, 30)
        bombs = [(r.randint(1, rows), r.randint(1, cols), r.randrange(1, 100, 2), r.randint(0, 1))
                 for _ in range(count)]
        return f"{rows} {cols} {count}\n" + "\n".join("%d %d %d %d" % b for b in bombs) + "\n"
    if number == 2946:
        value, count = r.randint(-100, 100), r.randint(1, 30); operations = []
        for _ in range(count): operations.append((r.choice(("plus", "minus", "multiply")), r.randint(-5, 5)))
        return f"{value} {count}\n" + "\n".join(f"{op} {x}" for op, x in operations) + "\n"
    if number == 1037:
        values = []
        for _ in range(r.randint(1, 8)):
            n = r.randint(1, 10); values.append((n, r.randint(1, fence_counts(n))))
        return str(len(values)) + "\n" + "\n".join(f"{n} {c}" for n, c in values) + "\n"
    if number == 1160:
        villages = sorted(r.sample(range(1, 10001), r.randint(1, 100)))
        return f"{len(villages)} {r.randint(1, min(30, len(villages)))}\n" + " ".join(map(str, villages)) + "\n"
    if number == 1944:
        n = r.randint(2, 80); all_pairs = [(a, b) for a in range(1, n + 1) for b in range(a + 1, n + 1)]
        pairs = r.sample(all_pairs, r.randint(1, min(200, len(all_pairs))))
        return f"{n} {len(pairs)}\n" + "\n".join(f"{a} {b}" for a, b in pairs) + "\n"
    if number == 2385:
        total, walks = r.randint(1, 200), r.randint(1, 30)
        return f"{total} {walks}\n" + "\n".join(str(r.randint(1, 2)) for _ in range(total)) + "\n"
    if number == 2711:
        heights = [r.randint(130, 230) for _ in range(r.randint(2, 100))]
        return f"{len(heights)}\n" + " ".join(map(str, heights)) + "\n"
    if number == 2797:
        words = set(); target = r.randint(2, 60)
        while len(words) < target:
            words.add("".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(1, 20))))
        words = sorted(words); r.shuffle(words)
        return "\n".join(words) + "\n"
    raise KeyError(number)


def valid(number, text):
    try:
        tokens = text.split()
        if number == 1958: return not tokens
        if number == 1258:
            p = 0; seen = 0
            while p < len(tokens):
                n = int(tokens[p]); p += 1; seen += 1
                if not 3 <= n <= 100 or p + n*n > len(tokens): return False
                matrix = list(map(int, tokens[p:p+n*n])); p += n*n
                if any(matrix[i*n+i] != 0 for i in range(n)): return False
                if any(matrix[i*n+j] != matrix[j*n+i] for i in range(n) for j in range(n)): return False
            return seen > 0 and p == len(tokens)
        if number in (1661, 1664, 1703):
            it = iter(tokens); cases = int(next(it))
            if number == 1664:
                return 0 <= cases <= 20 and all(1 <= int(x) <= 10 for x in it) and len(tokens) == 1 + 2*cases
            for _ in range(cases):
                if number == 1661:
                    n,x,y,m = (int(next(it)) for _ in range(4))
                    if not (1 <= n <= 1000 and -20000 <= x <= 20000 and 0 < y <= 20000 and m > 0): return False
                    for _ in range(n):
                        a,b,h=(int(next(it)) for _ in range(3))
                        if not (-20000 <= a < b <= 20000 and 0 < h < y): return False
                else:
                    n,ops=int(next(it)),int(next(it))
                    if not 1 <= n <= 100000 or not 0 <= ops <= 100000:return False
                    for _ in range(ops):
                        op,a,b=next(it),int(next(it)),int(next(it))
                        if op not in ('A','D') or not (1<=a<=n and 1<=b<=n):return False
            return not list(it)
        if number == 2812:
            r,c,n=map(int,tokens[:3]); pts=list(map(int,tokens[3:])); pairs=list(zip(pts[::2],pts[1::2]))
            return 1<=r<=5000 and 1<=c<=5000 and 3<=n<=5000 and len(pairs)==n and len(set(pairs))==n and all(1<=x<=r and 1<=y<=c for x,y in pairs)
        if number == 1042:
            p=0;seen=0
            while int(tokens[p]) != 0:
                n=int(tokens[p]);h=int(tokens[p+1]);p+=2;seen+=1
                if not (2<=n<=25 and 1<=h<=16):return False
                f=list(map(int,tokens[p:p+n]));p+=n;d=list(map(int,tokens[p:p+n]));p+=n;t=list(map(int,tokens[p:p+n-1]));p+=n-1
                if min(f+d)<0 or any(not 1<=x<=192 for x in t):return False
            return seen and p==len(tokens)-1
        if number == 2226:
            r,c=map(int,tokens[:2]);g=tokens[2:];return 1<=r<=50 and 1<=c<=50 and len(g)==r and all(len(x)==c and set(x)<={'*','.'} for x in g)
        if number == 1064:
            n,k=map(int,tokens[:2]);vals=tokens[2:];return 1<=n<=10000 and 1<=k<=10000 and len(vals)==n and all(100<=round(float(x)*100)<=10_000_000 and '.' in x and len(x.rsplit('.',1)[1])==2 for x in vals)
        if number == 1185:
            n,m=map(int,tokens[:2]);g=tokens[2:];return 1<=n<=100 and 1<=m<=10 and len(g)==n and all(len(x)==m and set(x)<={'P','H'} for x in g)
        if number == 2229:return len(tokens)==1 and 1<=int(tokens[0])<=1_000_000
        if number == 2533:
            n=int(tokens[0]);a=list(map(int,tokens[1:]));return 1<=n<=1000 and len(a)==n and all(0<=x<=10000 for x in a)
        if number == 2659:
            a,b,k=map(int,tokens[:3]);v=list(map(int,tokens[3:]));bombs=list(zip(v[::4],v[1::4],v[2::4],v[3::4]));return 1<=a<=100 and 1<=b<=100 and 1<=k<=100 and len(bombs)==k and all(1<=r<=a and 1<=s<=b and 1<=p<=99 and p%2 and t in (0,1) for r,s,p,t in bombs)
        if number == 2946:
            count=int(tokens[1]);ops=tokens[2:];return len(ops)==2*count and all(ops[i] in ('plus','minus','multiply') and int(ops[i+1])==float(ops[i+1]) for i in range(0,len(ops),2))
        if number == 1037:
            count=int(tokens[0]);v=list(map(int,tokens[1:]));pairs=list(zip(v[::2],v[1::2]));return 1<=count<=100 and len(pairs)==count and all(1<=n<=20 and 1<=c<=fence_counts(n) for n,c in pairs)
        if number == 1160:
            v,p=map(int,tokens[:2]);a=list(map(int,tokens[2:]));return 1<=p<=v<=300 and len(a)==v and a==sorted(set(a)) and all(1<=x<=10000 for x in a)
        if number == 1944:
            n,p=map(int,tokens[:2]);v=list(map(int,tokens[2:]));pairs=[tuple(sorted(x)) for x in zip(v[::2],v[1::2])];return 1<=n<=1000 and 1<=p<=10000 and len(pairs)==p and len(set(pairs))==p and all(1<=a<b<=n for a,b in pairs)
        if number == 2385:
            t,w=map(int,tokens[:2]);a=list(map(int,tokens[2:]));return 1<=t<=1000 and 1<=w<=30 and len(a)==t and set(a)<={1,2}
        if number == 2711:
            n=int(tokens[0]);a=list(map(int,tokens[1:]));return 2<=n<=100 and len(a)==n and all(130<=x<=230 for x in a)
        if number == 2797:return 2<=len(tokens)<=1000 and len(set(tokens))==len(tokens) and all(1<=len(x)<=20 and x.isalpha() and x.islower() and x.isascii() for x in tokens)
    except (ValueError, IndexError, StopIteration, ZeroDivisionError):
        return False
    return False


def clean(value):
    return "\n".join(line.rstrip() for line in value.strip().splitlines()) + "\n"


def run_source(source, input_text):
    with tempfile.TemporaryDirectory() as folder:
        script = Path(folder) / "solution.py"; script.write_text(source, encoding="utf-8")
        result = subprocess.run([sys.executable, "-I", str(script)], input=input_text, text=True,
                                capture_output=True, timeout=120)
        if result.returncode:
            raise RuntimeError(result.stderr[-500:])
        return result.stdout.rstrip() + "\n"


def normalise_1258_archive(text):
    tokens = text.split(); p = 0; cases = []
    while p < len(tokens):
        n = int(tokens[p]); p += 1; values = tokens[p:p+n*n]; p += n*n
        cases.append(str(n) + "\n" + "\n".join(" ".join(values[i:i+n]) for i in range(0, n*n, n)))
    return "\n".join(cases) + "\n"


def archive_check(source, entry):
    paths = [path for rel in entry.get("oracle_dirs", [entry["oracle_dir"]])
             for path in sorted((OPENJUDGE / rel).glob("*.in"))]
    mismatched = []
    for path in paths:
        text = path.read_text(errors="replace")
        if entry["number"] == 1258: text = normalise_1258_archive(text)
        expected = path.with_suffix(".out").read_text(errors="replace")
        try: got = run_source(source, text)
        except Exception: mismatched.append(path.name); continue
        if got.replace("\x1a", " ").split() != expected.replace("\x1a", " ").split():
            mismatched.append(path.name)
    return {"status": "passed" if paths and not mismatched else "FAILED", "cases": len(paths),
            "mismatched": mismatched, "method": "exact tokens after adapting legacy physical matrix lines"}


def source_sections(numbers):
    selected = {}
    for source_index, path in enumerate(SOURCES):
        for number, title, body, codes, _samples in sections(path):
            if number in numbers and number not in selected:
                code_index = SOURCE_CODE_INDEX[number]
                selected[number] = (title, body, codes[code_index], path, code_index, source_index)
    return selected


def write_producecase(made, number, source, sample):
    program = ("import random,subprocess,sys,tempfile\nfrom pathlib import Path\n" +
               inspect.getsource(fence_counts) + inspect.getsource(generate) +
               f"\nREFERENCE={source!r}\nNUMBER={number}\nSAMPLE={sample!r}\n" +
               "def run(x):\n with tempfile.TemporaryDirectory() as d:\n  p=Path(d)/'m.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)\n  if q.returncode:raise SystemExit(q.stderr)\n  return q.stdout.rstrip()+'\\n'\n" +
               "def main():\n d=Path('data');d.mkdir(exist_ok=True)\n for p in d.glob('*'):p.unlink()\n for i,x in enumerate([SAMPLE]+[generate(NUMBER,s) for s in range(1,21)]):\n  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))\n" +
               "if __name__=='__main__':main()\n")
    (made / "producecase.py").write_text(program, encoding="utf-8")


def main():
    candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))["entries"]
    chosen = [row for row in candidates if row["priority"] in TARGETS]
    if [row["priority"] for row in chosen] != TARGETS:
        raise SystemExit("priority 61..80 selection changed")
    selected = source_sections({row["number"] for row in chosen})
    if set(selected) != {row["number"] for row in chosen}:
        raise SystemExit(f"missing solution collection sections: {set(row['number'] for row in chosen) - set(selected)}")
    platform_path = ROOT / "collab" / "t028-round5-platform.json"
    platform = {int(row["local_number"]): row for row in json.loads(platform_path.read_text()).get("results", [])} if platform_path.exists() else {}
    manifest, report = [], []
    for entry in chosen:
        number = int(entry["number"]); title, body, raw, path, code_index, source_index = selected[number]
        sample = "" if number == 1958 else clean(first_sample(body, "样例输入"))
        sample_output = None if number == 1958 else clean(first_sample(body, "样例输出"))
        attribution = (f"# Source collection: {path}\n# Heading: {number}: {title}\n"
                       f"# Fenced code block index: {code_index}\n# Source URL: {SOURCE_URLS[source_index]}\n"
                       f"# Upstream problem: http://cs101.openjudge.cn/{entry['submit_group']}/{entry['submit_id']}/\n"
                       "# License: not declared in source collection; no license is inferred.\nimport sys\n")
        source = attribution + clean(raw)
        cross = archive_check(source, entry)
        if cross["status"] != "passed": raise SystemExit(f"{number} archive cross-check failed: {cross}")
        cases = [sample] + [generate(number, seed) for seed in range(1, 21)]
        outputs = [run_source(source, case) for case in cases]
        made_rel = str(Path(entry["oracle_dir"]).parent / f"{number:05d}_made")
        made = OPENJUDGE / made_rel; data = made / "data"; data.mkdir(parents=True, exist_ok=True)
        for old in data.glob("*"): old.unlink()
        for index, (case, output) in enumerate(zip(cases, outputs)):
            (data / f"{index}.in").write_text(case, encoding="utf-8")
            (data / f"{index}.out").write_text(output, encoding="utf-8")
        (made / "samplecode.py").write_text(source, encoding="utf-8")
        write_producecase(made, number, source, sample)
        constraint_rows = [(LABELS[number], all(valid(number, case) for case in cases[1:]))]
        no_input = "the statement defines exactly one empty input" if number == 1958 else None
        audit = common.audit(made, cases=cases[1:], outputs=outputs[1:], sample_input=sample,
                             sample_output=sample_output, sample_output_exemption=no_input,
                             exemption=no_input, constraints=constraint_rows if not no_input else None,
                             constraint_counterexample=(INVALID[number].strip(), [(LABELS[number], valid(number, INVALID[number]))]) if not no_input else None,
                             constraint_exemption=no_input)
        smoke_bad = [seed for seed in range(20_000) if not valid(number, generate(number, seed))]
        platform_row = platform.get(number)
        status = "passed" if not audit["failed"] and not smoke_bad and (not platform_row or platform_row.get("verdict") == "Accepted") else "FAILED"
        manifest.append({**entry, "local_number": number, "title": title, "made_dir": made_rel,
                         "sample_input": sample, "solution_collection": str(path),
                         "solution_code_index": code_index, "pending_rework": []})
        report.append({"local_number": number, "global_number": entry["global_number"], "title": title,
                       "priority": entry["priority"], "tier": entry["tier"], "status": status,
                       "reference_source": "human-provided solution collection",
                       "solution_collection": str(path), "solution_code_index": code_index,
                       "source_url": SOURCE_URLS[source_index], "license_status": "not declared; no license is inferred",
                       "submission_id": platform_row.get("solution_id") if platform_row else None,
                       "platform_verdict": platform_row.get("verdict") if platform_row else "not_run",
                       "archive_cross_check": cross, "generator": "generate",
                       "generator_seed_smoke": {"seeds": 20_000, "status": "passed" if not smoke_bad else "FAILED", "failed_seeds": smoke_bad[:8]},
                       "test_cases": len(cases), "max_input_bytes": max(len(case.encode()) for case in cases),
                       "max_output_bytes": max(len(output.encode()) for output in outputs),
                       "constraints": constraint_rows, "constraint_counterexample": INVALID[number].strip(),
                       "self_audit": audit})
        print(f"{number:05d} built", flush=True)
    (ROOT / "collab" / "t028-round5-manifest.json").write_text(json.dumps({"task":"T-028","round":5,"count":20,"priority_range":[61,80],"entries":manifest}, ensure_ascii=False, indent=2)+"\n")
    failed = [row["local_number"] for row in report if row["status"] != "passed"]
    (ROOT / "collab" / "t028-round5-report.json").write_text(json.dumps({"task":"T-028","round":5,"updated_at":datetime.now(timezone.utc).isoformat(),"count":20,"pending_rework_status":common.pending_rework_status([],OPENJUDGE/"tests"),"entries":report,"failed":failed},ensure_ascii=False,indent=2)+"\n")
    if failed: raise SystemExit(f"self-audit failed: {failed}")


if __name__ == "__main__": main()
