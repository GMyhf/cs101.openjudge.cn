#!/usr/bin/env python3
"""Build T-028 round 1 after cross-checking every scraped case."""
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
MANIFEST = ROOT / "collab" / "t028-round1-manifest.json"
REPORT = ROOT / "collab" / "t028-round1-report.json"
PLATFORM = ROOT / "collab" / "t028-round1-platform.json"
SOURCE_URLS = {
    0: "https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md",
    1: "https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md",
}

# (solution collection index, zero-based fenced-code index). Each selected block
# was independently run against all existing scraped cases before being listed.
SOURCE_SPEC = {
    1061: (0, 2), 1125: (0, 2), 1145: (1, 3), 1321: (0, 2),
    1328: (0, 2), 1384: (0, 2), 1577: (1, 5), 1611: (1, 2),
    2192: (1, 2), 2406: (0, 2), 2442: (1, 2), 2499: (1, 2),
    2689: (0, 2), 2701: (0, 2), 2707: (0, 2), 2749: (0, 2),
    2753: (0, 2), 2766: (0, 2), 2786: (0, 2), 2792: (0, 2),
}


def g1061(r):
    # The collected reference divides by (a*i)%L.  A prime circumference and
    # non-zero speed difference keep that expression non-zero for i=1..L-1.
    L = r.choice([101, 211, 307, 401, 503, 601, 701, 809, 907, 1009, 2003, 3001, 4001])
    x = r.randrange(L); y = r.randrange(L)
    while y == x: y = r.randrange(L)
    m = r.randrange(1, L); n = r.randrange(1, L)
    while n == m: n = r.randrange(1, L)
    return f"{x} {y} {m} {n} {L}\n"


def g1125(r):
    n = r.randint(2, 18); rows = []
    for i in range(1, n + 1):
        edges = {(i % n) + 1: r.randint(1, 10)}
        for _ in range(r.randint(0, min(5, n - 1))):
            j = r.randint(1, n)
            if j != i: edges[j] = r.randint(1, 10)
        rows.append(str(len(edges)) + " " + " ".join(f"{j} {w}" for j, w in sorted(edges.items())))
    return str(n) + "\n" + "\n".join(rows) + "\n0\n"


def g1145(r):
    def tree(depth):
        if depth == 0 or r.random() < .22: return "()", []
        value = r.randint(-30, 30); left, lp = tree(depth - 1); right, rp = tree(depth - 1)
        paths = [value + x for x in lp + rp] or [value]
        return f"({value}{left}{right})", paths
    expression, paths = tree(r.randint(2, 5))
    target = r.choice(paths) if paths and r.random() < .55 else r.randint(-100, 100)
    return f"{target} {expression}\n"


def g1321(r):
    blocks = []
    for _ in range(r.randint(1, 3)):
        n = r.randint(1, 8); k = r.randint(1, n)
        board = ["".join(r.choice("##.") for _ in range(n)) for _ in range(n)]
        blocks.append(f"{n} {k}\n" + "\n".join(board))
    return "\n".join(blocks) + "\n-1 -1\n"


def g1328(r):
    blocks = []
    for _ in range(r.randint(1, 3)):
        n, d = r.randint(1, 25), r.randint(1, 30)
        points = [f"{r.randint(-80,80)} {r.randint(0,d + (5 if r.random()<.15 else 0))}" for _ in range(n)]
        blocks.append(f"{n} {d}\n" + "\n".join(points) + "\n\n")
    return "".join(blocks) + "0 0\n"


def g1384(r):
    out = [str(r.randint(1, 4))]
    for _ in range(int(out[0])):
        empty = r.randint(1, 300); target = empty + r.randint(1, 600); n = r.randint(1, 12)
        out += [f"{empty} {target}", str(n)]
        out += [f"{r.randint(1,100)} {r.randint(1,80)}" for _ in range(n)]
    return "\n".join(out) + "\n"


def g1577(r):
    def layers(order):
        root = order[0]; left = [x for x in order[1:] if x < root]; right = [x for x in order[1:] if x > root]
        a, b = layers(left) if left else [], layers(right) if right else []
        out = []
        for i in range(max(len(a), len(b))): out.append((a[i] if i < len(a) else "") + (b[i] if i < len(b) else ""))
        out.append(root); return out
    datasets = []
    for _ in range(r.randint(1, 3)):
        letters = r.sample(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), r.randint(1, 18))
        datasets += layers(letters) + ["*"]
    datasets[-1] = "$"
    return "\n".join(datasets) + "\n"


def g1611(r):
    blocks = []
    for _ in range(r.randint(1, 3)):
        n, m = r.randint(1, 80), r.randint(0, 30); rows = []
        for _ in range(m):
            members = r.sample(range(n), r.randint(1, min(n, 10)))
            rows.append(str(len(members)) + " " + " ".join(map(str, members)))
        blocks.append(f"{n} {m}\n" + ("\n".join(rows) + "\n" if rows else ""))
    return "".join(blocks) + "0 0\n"


def g2192(r):
    rows = []
    for _ in range(r.randint(1, 12)):
        a = "".join(r.choice("abcde") for _ in range(r.randint(1, 18)))
        b = "".join(r.choice("abcde") for _ in range(r.randint(1, 18)))
        aa, bb, c = list(a), list(b), []
        while aa or bb:
            src = aa if not bb or (aa and r.random() < .5) else bb; c.append(src.pop(0))
        if r.random() < .35: c[r.randrange(len(c))] = "z"
        rows.append(f"{a} {b} {''.join(c)}")
    return str(len(rows)) + "\n" + "\n".join(rows) + "\n"


def g2406(r):
    rows = []
    for _ in range(r.randint(1, 15)):
        base = "".join(r.choice("abcd") for _ in range(r.randint(1, 18)))
        rows.append(base * r.randint(1, 15))
    return "\n".join(rows) + "\n.\n"


def g2442(r):
    out = [str(r.randint(1, 3))]
    for _ in range(int(out[0])):
        m, n = r.randint(2, 8), r.randint(1, 35); out.append(f"{m} {n}")
        out += [" ".join(str(r.randint(0, 10000)) for _ in range(n)) for _ in range(m)]
    return "\n".join(out) + "\n"


def g2499(r):
    rows = []
    for _ in range(r.randint(1, 15)):
        a = b = 1
        for _ in range(r.randint(0, 25)):
            if r.random() < .5: a += b
            else: b += a
        rows.append(f"{a} {b}")
    return str(len(rows)) + "\n" + "\n".join(rows) + "\n"


def g2689(r):
    return "".join(r.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789") for _ in range(r.randint(1, 79))) + "\n"


def g2701(r): return str(r.randint(1, 99)) + "\n"


def g2707(r):
    rows = []
    for _ in range(r.randint(3, 15)):
        a = r.choice([x for x in range(-20, 21) if x]); b = r.randint(-30, 30); c = r.randint(-30, 30)
        rows.append(f"{a} {b} {c}")
    return str(len(rows)) + "\n" + "\n".join(rows) + "\n"


def g2749(r):
    values = [r.randint(2, 500) for _ in range(r.randint(1, 12))]
    return str(len(values)) + "\n" + "\n".join(map(str, values)) + "\n"


def g2753(r):
    values = [r.randint(1, 20) for _ in range(r.randint(1, 15))]
    return str(len(values)) + "\n" + "\n".join(map(str, values)) + "\n"


def g2766(r):
    n = r.randint(1, 18); values = [str(r.randint(-127, 127)) for _ in range(n*n)]
    return str(n) + "\n" + "\n".join(" ".join(values[i*n:(i+1)*n]) for i in range(n)) + "\n"


def g2786(r):
    values = [r.randint(1, 999999) for _ in range(r.randint(1, 20))]
    return str(len(values)) + "\n" + "\n".join(map(str, values)) + "\n"


def g2792(r):
    out = [str(r.randint(1, 6))]
    for _ in range(int(out[0])):
        p, q = r.randint(1, 40), r.randint(1, 40)
        out += [str(r.randint(1, 200)), str(p), " ".join(str(r.randint(1,100)) for _ in range(p)), str(q), " ".join(str(r.randint(1,100)) for _ in range(q))]
    return "\n".join(out) + "\n"


GENERATORS = {n: globals()[f"g{n}"] for n in SOURCE_SPEC}

CONSTRAINTS = {
    1061: "exactly five integers with x != y, positive m/n, and 0 < L < 2100000000",
    1125: "each data set has 1..100 brokers, valid contact/time pairs, and final terminator 0",
    1145: "each query has an integer target and a balanced LISP binary-tree expression",
    1321: "each board has 1 <= k <= n <= 8 and exactly n rows of n '#' or '.' cells",
    1328: "each radar case has n >= 1, d >= 0, exactly n integer points, and final 0 0",
    1384: "each pig has 1 <= E <= F <= 10000 and positive coin values and weights",
    1577: "leaf layers contain only sorted uppercase letters and end with '*' or final '$'",
    1611: "each group member is in 0..n-1 and every data set is followed by final 0 0",
    2192: "T is 1..1000; first strings are 1..200 letters and len(c)=len(a)+len(b)",
    2406: "at least one printable string has length 1..1000000 before the final '.' line",
    2442: "each case has 1 <= m <= 100, 1 <= n <= 2000, and m*n nonnegative integers",
    2499: "each scenario is a positive valid tree node pair bounded by 1000000000",
    2689: "the single input line has fewer than 80 characters",
    2701: "n is a single positive integer smaller than 100",
    2707: "the declared number of equations is present and every quadratic coefficient a is nonzero",
    2749: "the declared values are all integers satisfying 1 < a < 32768",
    2753: "the declared Fibonacci indices are all integers satisfying 1 <= a <= 20",
    2766: "N is 1..100 followed by exactly N*N integers, each in -127..127",
    2786: "the declared Pell indices are all integers satisfying 1 <= k < 1000000",
    2792: "each case has positive s,a,b <= 10000 and exactly a/b positive elements <=10000",
}

COUNTEREXAMPLES = {
    1061: "1 1 3 4 5\n",
    1125: "101\n0\n",
    1145: "10 (3()()\n",
    1321: "2 1\n##\n#X\n-1 -1\n",
    1328: "1 -1\n0 0\n\n0 0\n",
    1384: "1\n10 5\n1\n1 1\n",
    1577: "A1\n$\n",
    1611: "3 1\n1 3\n0 0\n",
    2192: "1\na b a\n",
    2406: ".\n",
    2442: "1\n2 2\n0 0\n0 -1\n",
    2499: "1\n0 1\n",
    2689: "X" * 80 + "\n",
    2701: "100\n",
    2707: "1\n0 1 1\n",
    2749: "1\n1\n",
    2753: "1\n21\n",
    2766: "2\n1 2 3\n",
    2786: "1\n1000000\n",
    2792: "1\n10\n1\n0\n1\n10\n",
}


def source_sections():
    found = {}
    for source_index, source in enumerate(SOURCES):
        for number, title, body, codes, _samples in sections(source):
            if number in SOURCE_SPEC and SOURCE_SPEC[number][0] == source_index:
                code_index = SOURCE_SPEC[number][1]
                found[number] = (title, body, codes[code_index], source, code_index)
    missing = sorted(set(SOURCE_SPEC) - set(found))
    if missing: raise SystemExit(f"missing solution sections: {missing}")
    return found


def clean_lines(text):
    """Remove source-document trailing spaces without changing token semantics."""
    return "\n".join(line.rstrip() for line in text.rstrip().splitlines()) + "\n"


def run_source(source, input_text, timeout=120):
    with tempfile.TemporaryDirectory(prefix="t028-") as folder:
        script = Path(folder) / "main.py"; script.write_text(source, encoding="utf-8")
        result = subprocess.run([sys.executable, "-I", str(script)], input=input_text,
                                text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError((result.stderr or result.stdout)[-500:])
    return result.stdout


def cross_check(source, entry):
    scraped = OPENJUDGE / entry["scraped_dir"]
    mismatched = []
    inputs = sorted(scraped.glob("*.in"))
    for path in inputs:
        expected = path.with_suffix(".out")
        if not expected.exists() or run_source(source, path.read_text(errors="replace")).split() != expected.read_text(errors="replace").split():
            mismatched.append(path.name)
    return {"status": "passed" if inputs and not mismatched else "FAILED",
            "cases": len(inputs), "mismatched": mismatched}


def meaningful_check(number, text):
    """Check the stated constraint named in CONSTRAINTS; malformed text is false."""
    try:
        lines, tokens = text.splitlines(), text.split()
        if number == 1061:
            x, y, m, n, length = map(int, tokens)
            return x != y and m > 0 and n > 0 and 0 < length < 2100000000
        if number == 1125:
            pos = 0
            while int(lines[pos]) != 0:
                count = int(lines[pos]); pos += 1
                if not 1 <= count <= 100: return False
                for broker in range(1, count + 1):
                    row = list(map(int, lines[pos].split())); pos += 1
                    if len(row) != 1 + 2 * row[0]: return False
                    if any(not 1 <= row[i] <= count or row[i] == broker or not 1 <= row[i+1] <= 10
                           for i in range(1, len(row), 2)): return False
            return pos == len(lines) - 1
        if number == 1145: return bool(lines) and "(" in text and text.count("(") == text.count(")")
        if number == 1321:
            pos = 0
            while lines[pos] != "-1 -1":
                n, k = map(int, lines[pos].split()); pos += 1
                if not 1 <= k <= n <= 8: return False
                board = lines[pos:pos+n]; pos += n
                if len(board) != n or any(len(row) != n or not set(row) <= set("#.") for row in board): return False
            return pos == len(lines) - 1
        if number == 1328:
            pos = 0
            while lines[pos] != "0 0":
                n, d = map(int, lines[pos].split()); pos += 1
                if n < 1 or d < 0 or len(lines) < pos + n: return False
                if any(len(lines[pos+i].split()) != 2 for i in range(n)): return False
                pos += n
                while pos < len(lines) and not lines[pos].strip(): pos += 1
            return pos == len(lines) - 1
        if number == 1384:
            pos = 1; cases = int(lines[0])
            for _ in range(cases):
                empty, full = map(int, lines[pos].split()); pos += 1
                count = int(lines[pos]); pos += 1
                if not 1 <= empty <= full <= 10000 or count < 1: return False
                coins = [tuple(map(int, line.split())) for line in lines[pos:pos+count]]; pos += count
                if len(coins) != count or any(value <= 0 or weight <= 0 for value, weight in coins): return False
            return pos == len(lines)
        if number == 1577:
            return lines[-1] == "$" and all(x in ("*", "$") or x.isupper() and x.isalpha() and "".join(sorted(x)) == x for x in lines)
        if number == 1611:
            pos = 0
            while lines[pos] != "0 0":
                n, m = map(int, lines[pos].split()); pos += 1
                if not 0 < n <= 30000 or not 0 <= m <= 500: return False
                for _ in range(m):
                    row = list(map(int, lines[pos].split())); pos += 1
                    if len(row) != row[0] + 1 or any(not 0 <= member < n for member in row[1:]): return False
            return pos == len(lines) - 1
        if number == 2192:
            return 1 <= int(lines[0]) <= 1000 and int(lines[0]) == len(lines)-1 and all(
                len(parts := row.split()) == 3 and all(word.isalpha() for word in parts)
                and 1 <= len(parts[0]) <= 200 and 1 <= len(parts[1]) <= 200
                and len(parts[2]) == len(parts[0]) + len(parts[1]) for row in lines[1:])
        if number == 2406: return len(lines) >= 2 and lines[-1] == "." and all(1 <= len(x) <= 1000000 for x in lines[:-1])
        if number == 2442:
            pos = 1; cases = int(lines[0])
            for _ in range(cases):
                m, n = map(int, lines[pos].split()); pos += 1
                if not 1 <= m <= 100 or not 1 <= n <= 2000: return False
                rows = lines[pos:pos+m]; pos += m
                if len(rows) != m or any(len(row.split()) != n or any(int(v) < 0 for v in row.split()) for row in rows): return False
            return pos == len(lines)
        if number == 2499: return int(lines[0]) == len(lines)-1 and all(1 <= int(v) <= 1000000000 for v in tokens[1:])
        if number == 2689: return len(lines) == 1 and len(lines[0]) < 80
        if number == 2701: return len(tokens) == 1 and 1 <= int(tokens[0]) < 100
        if number == 2707: return int(lines[0]) == len(lines)-1 and all(float(x.split()[0]) != 0 for x in lines[1:])
        if number == 2749: return int(lines[0]) == len(lines)-1 and all(1 < int(v) < 32768 for v in lines[1:])
        if number == 2753: return int(lines[0]) == len(lines)-1 and all(1 <= int(v) <= 20 for v in lines[1:])
        if number == 2766: return 1 <= int(tokens[0]) <= 100 and len(tokens) == 1 + int(tokens[0])**2 and all(-127 <= int(v) <= 127 for v in tokens[1:])
        if number == 2786: return int(lines[0]) == len(lines)-1 and all(1 <= int(v) < 1000000 for v in lines[1:])
        if number == 2792:
            pos = 1; cases = int(lines[0])
            for _ in range(cases):
                target = int(lines[pos]); a = int(lines[pos+1]); av = list(map(int, lines[pos+2].split()))
                b = int(lines[pos+3]); bv = list(map(int, lines[pos+4].split())); pos += 5
                if not 1 <= target <= 10000 or not 1 <= a <= 10000 or len(av) != a: return False
                if not 1 <= b <= 10000 or len(bv) != b or any(not 1 <= v <= 10000 for v in av+bv): return False
            return pos == len(lines)
    except (IndexError, ValueError, TypeError):
        return False
    return False


def write_producecase(made, source, generator, sample):
    runner = f'''\nREFERENCE={source!r}\nSAMPLE={sample!r}\nGENERATOR={generator.__name__!r}\n\ndef run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1,21)]
    for i,case in enumerate(cases):
        (data/f"{{i}}.in").write_text(case); (data/f"{{i}}.out").write_text(run(case))
if __name__=="__main__": main()
'''
    text = "import random, subprocess, sys, tempfile\nfrom pathlib import Path\n" + inspect.getsource(generator) + runner
    (made / "producecase.py").write_text(text, encoding="utf-8")


def main():
    all_candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))["entries"]
    candidates = {int(e["number"]): e for e in all_candidates}
    selected = source_sections()
    platform_rows = {}
    if PLATFORM.exists():
        platform = json.loads(PLATFORM.read_text(encoding="utf-8"))
        platform_rows = {int(row["local_number"]): row for row in platform.get("results", [])}

    # The cross-check is deliberately complete and precedes every output write.
    cross = {n: cross_check(selected[n][2], candidates[n]) for n in SOURCE_SPEC}
    failed_cross = {n: row for n, row in cross.items() if row["status"] != "passed"}
    if failed_cross: raise SystemExit(f"scraped cross-check failed; no data written: {failed_cross}")

    manifest_entries = []
    for n in SOURCE_SPEC:
        title, body, _source, source_path, code_index = selected[n]
        manifest_entries.append({**candidates[n], "local_number": n, "title": title,
            "sample_input": clean_lines(first_sample(body, "样例输入")),
            "sample_output": clean_lines(first_sample(body, "样例输出")),
            "solution_collection": str(source_path), "solution_code_index": code_index,
            "pending_rework": []})
    exclusions = [
        {"number": 1077, "reason": "multiple valid move sequences conflict with exact-output judging"},
        *[{"number": n, "reason": "no collected solution reproduced all scraped outputs"} for n in (1276, 1426, 1852, 2039)],
    ]
    MANIFEST.write_text(json.dumps({"task":"T-028", "round":1, "count":20,
        "selection_rule":"solution collection reference, at least two scraped cases, deterministic exact output",
        "entries":manifest_entries, "selection_exclusions":exclusions}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

    report_entries = []
    for entry in manifest_entries:
        n = entry["local_number"]; title, _body, raw_source, source_path, code_index = selected[n]
        source_index = SOURCE_SPEC[n][0]
        upstream_path = f"/{entry['books'][0]}/{entry['ids'][0]}/"
        attribution = (f"# Source collection: {source_path}\n# Heading: {n}: {title}\n"
                       f"# Fenced code block index: {code_index}\n"
                       f"# Source URL: {SOURCE_URLS[source_index]}\n"
                       f"# Upstream problem: http://cs101.openjudge.cn{upstream_path}\n"
                       "# License: not declared in source collection; no license is inferred.\n")
        source = attribution + clean_lines(raw_source)
        generator = GENERATORS[n]; sample = entry["sample_input"]
        cases = [sample] + [generator(random.Random(seed)) for seed in range(1, 21)]
        outputs = [run_source(source, case) for case in cases]
        made = OPENJUDGE / entry["made_dir"]; data = made / "data"; data.mkdir(parents=True, exist_ok=True)
        for old in data.glob("*"): old.unlink()
        for i, case in enumerate(cases):
            (data/f"{i}.in").write_text(case, encoding="utf-8")
            (data/f"{i}.out").write_text(outputs[i], encoding="utf-8")
        (made/"samplecode.py").write_text(source, encoding="utf-8")
        write_producecase(made, source, generator, sample)

        generated = cases[1:]; invalid = COUNTEREXAMPLES[n]; label = CONSTRAINTS[n]
        rows = [(label, all(meaningful_check(n, c) for c in generated))]
        audit = common.audit(made, cases=generated, outputs=outputs[1:], sample_input=sample,
            sample_output=entry["sample_output"], constraints=rows,
            constraint_counterexample=(invalid.strip(), [(rows[0][0], meaningful_check(n, invalid))]))
        for seed in range(20000): generator(random.Random(seed))
        platform_row = platform_rows.get(n)
        platform_failed = platform_row is not None and platform_row.get("verdict") != "Accepted"
        report_entries.append({"local_number":n, "title":title,
            "status":"passed" if not audit["failed"] and not platform_failed else "FAILED",
            "reference_source":"solution collection code reproduced all scraped cases",
            "solution_collection":str(source_path), "solution_code_index":code_index,
            "submission_id":platform_row.get("solution_id") if platform_row else None,
            "platform_verdict":platform_row.get("verdict") if platform_row else "not_run",
            "submission_id_note":None if platform_row else "not recorded in source collection",
            "statistics_url":f"http://cs101.openjudge.cn{upstream_path}statistics/",
            "source_url":SOURCE_URLS[source_index],
            "license_status":"not declared in source collection; no license is inferred",
            "generator":generator.__name__, "generator_seed_smoke":{"seeds":20000,"status":"passed"},
            "test_cases":len(cases), "max_input_bytes":max(map(len,cases)),
            "max_output_bytes":max(map(len,outputs)), "scraped_cross_check":cross[n],
            "constraints":rows, "constraint_counterexample":invalid.strip(), "self_audit":audit})
        print(n, "built", flush=True)

    failed = [e["local_number"] for e in report_entries if e["status"] != "passed"]
    payload = {"task":"T-028", "round":1, "updated_at":datetime.now(timezone.utc).isoformat(),
        "count":len(report_entries), "pending_rework_status":common.pending_rework_status([], OPENJUDGE/"tests"),
        "selection_exclusions":exclusions, "entries":report_entries, "failed":failed}
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    if failed: raise SystemExit(f"self-audit failed: {failed}")


if __name__ == "__main__": main()
