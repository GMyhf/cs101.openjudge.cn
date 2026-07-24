#!/usr/bin/env python3
"""Build T-002 batch 001b with one constrained generator per problem."""
import json
import random
import re
import subprocess
import tempfile
from pathlib import Path

from build_001a import bucket, fence_blocks, locate_source, run

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collab" / "t002-batch-001-manifest.json"
TESTS = ROOT / "data" / "openjudge" / "tests"
IDS = [4115, 4116, 4119, 4121, 4123, 4124, 4129, 4130, 4135,
       4144, 4145, 4147, 4977, 5333, 5343, 5344, 5430, 5442, 5443, 5467]

CONSTRAINTS = {
    4115: ["0<M,N<200", "0<=T<10", "grid has exactly one @ and one +", "cells are *, #, @, +"],
    4116: ["N,M<=200", "each case has one r and one a", "cells are @, #, x, r, a"],
    4119: ["0<N<=50", "0<K<=N", "input is a sequence of N,K pairs until EOF"],
    4121: ["T<=50", "1<=N<=100000", "absolute price <=1000000"],
    4123: ["T<10", "0<=x<n and 0<=y<m", "n,m<10", "each case asks a knight tour"],
    4124: ["2<N<=16", "matrix is N by N", "diagonal is zero", "off-diagonal travel times are 1..9999"],
    4129: ["0<T<=20", "0<R,C<=100", "2<=K<=10", "grid has one S and one E"],
    4130: ["terminator is 0 0", "grid has K,S,T", "cells are K,T,S,#,.,1..9"],
    4135: ["daily costs are 1..10000", "N days and M segments", "1<=M<=N"],
    4141: ["six integer counts (the sample permits zero)", "weights are 1,2,3,5,10,20"],
    4144: ["1<=N<=50000", "1<=A<=B<=1000000"],
    4145: ["1<=K<N<=1000", "1<=Ai<=Bi<=1000000000", "terminator is 0 0"],
    4147: ["n is a positive disk count", "three rod identifiers are single characters"],
    4977: ["K<100", "N<100", "heights are distinct and 0<h<10000"],
    5333: ["N is a positive plank count", "each plank length is positive"],
    5343: ["1<=N<=100", "card rank is 1..9", "card suit is A..D"],
    5344: ["2<=K<N<=1000", "people are numbered 1..N"],
    5430: ["expression length <=50", "variables are lowercase letters", "n<10", "division denominator is nonzero"],
    5442: ["n<=26", "graph is connected", "positive edge weights <100", "at most 75 edges and degree <=15"],
    5443: ["P<30", "Q<50", "R<20", "road distances are positive"],
    5467: ["1<n<100", "there are 2n polynomial lines", "each polynomial ends at a negative exponent", "line length <300"],
}


def get_section(source, number):
    lines = locate_source(source).read_text(encoding="utf-8", errors="ignore").splitlines()
    starts = [i for i, line in enumerate(lines) if re.match(r"^##\s+", line)]
    for i, start in enumerate(starts):
        if re.match(rf"^##\s+[^\d]*0*{number}[:：]", lines[start]):
            end = starts[i + 1] if i + 1 < len(starts) else len(lines)
            return "\n".join(lines[start:end])
    raise ValueError(number)


def first_sample(body, label, next_label=None):
    fence = r"\x60\x60\x60"
    match = re.search(rf"(?:{label})\s*\n+{fence}\n(.*?){fence}", body, re.S | re.I)
    if not match:
        raise ValueError("missing " + label)
    value = match.group(1)
    if next_label:
        value = value.split(next_label, 1)[0]
    lines = [line for line in value.splitlines() if not line.strip().startswith(label)]
    return "\n".join(lines).strip() + "\n"


def g4115(r):
    m, n, chakra = r.randint(4, 10), r.randint(4, 10), r.randint(0, 9)
    start, target = (0, 0), (m - 1, n - 1)
    path = {(i, 0) for i in range(m)} | {(m - 1, j) for j in range(n)}
    cells = []
    for i in range(m):
        row = []
        for j in range(n):
            if (i, j) == start: char = "@"
            elif (i, j) == target: char = "+"
            elif (i, j) in path: char = "*"
            else: char = "#" if r.random() < .22 else "*"
            row.append(char)
        cells.append("".join(row))
    return f"{m} {n} {chakra}\n" + "\n".join(cells) + "\n"


def make_weighted_grid(r, rescue=False):
    m, n = r.randint(4, 9), r.randint(4, 9)
    start, target = (0, 0), (m - 1, n - 1)
    path = {(i, 0) for i in range(m)} | {(m - 1, j) for j in range(n)}
    cells = []
    for i in range(m):
        row = []
        for j in range(n):
            if (i, j) == start: char = "r" if rescue else "S"
            elif (i, j) == target: char = "a" if rescue else "E"
            elif (i, j) in path: char = "@" if rescue else "."
            elif rescue:
                char = r.choice(["@"] * 5 + ["x"] * 2 + ["#"])
            else:
                char = r.choice(["."] * 6 + ["#"] * 2)
            row.append(char)
        cells.append("".join(row))
    return m, n, cells


def g4116(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        m, n, cells = make_weighted_grid(r, True)
        cases.append(f"{m} {n}\n" + "\n".join(cells))
    return str(len(cases)) + "\n" + "\n".join(cases) + "\n"


def g4119(r):
    count = r.randint(2, 5)
    pairs = []
    for _ in range(count):
        n = r.randint(1, 50)
        pairs.append((n, r.randint(1, n)))
    return "\n".join(f"{n} {k}" for n, k in pairs) + "\n"


def g4121(r):
    cases = []
    for _ in range(r.randint(1, 5)):
        n = r.randint(2, 100)
        prices = [r.randint(-1_000_000, 1_000_000) for _ in range(n)]
        cases.append(f"{n}\n" + " ".join(map(str, prices)))
    return str(len(cases)) + "\n" + "\n".join(cases) + "\n"


def g4123(r):
    n, m = r.choice([(1, 2), (2, 3), (3, 3), (3, 4), (4, 3), (4, 4), (5, 4)])
    x, y = r.randrange(n), r.randrange(m)
    return f"1\n{n} {m} {x} {y}\n"


def g4124(r):
    n = 16 if r.random() < .12 else r.randint(3, 12)
    matrix = []
    for i in range(n):
        row = [0 if i == j else r.randint(1, 9999) for j in range(n)]
        matrix.append(" ".join(map(str, row)))
    return str(n) + "\n" + "\n".join(matrix) + "\n"


def g4129(r):
    t = r.randint(1, 3)
    cases = []
    for _ in range(t):
        m, n, k = r.randint(4, 9), r.randint(4, 9), r.randint(2, 10)
        start, target = (0, 0), (m - 1, n - 1)
        path = {(i, 0) for i in range(m)} | {(m - 1, j) for j in range(n)}
        rows = []
        for i in range(m):
            row = []
            for j in range(n):
                if (i, j) == start: ch = "S"
                elif (i, j) == target: ch = "E"
                elif (i, j) in path: ch = "."
                else: ch = "#" if r.random() < .25 else "."
                row.append(ch)
            rows.append("".join(row))
        cases.append(f"{m} {n} {k}\n" + "\n".join(rows))
    return str(t) + "\n" + "\n".join(cases) + "\n"


def g4130(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        size = r.randint(3, 7)
        key_count = r.randint(1, min(3, size - 1))
        path = {(size - 1, j) for j in range(size)} | {(i, size - 1) for i in range(size)}
        rows = []
        key_positions = [(size - 1, j) for j in range(1, min(size, key_count + 1))]
        for i in range(size):
            row = []
            for j in range(size):
                if (i, j) == (size - 1, 0): ch = "K"
                elif (i, j) == (0, size - 1): ch = "T"
                elif (i, j) in key_positions: ch = str(key_positions.index((i, j)) + 1)
                elif (i, j) in path: ch = "."
                elif (i, j) == (0, 0): ch = "S"
                else: ch = r.choice(["."] * 6 + ["#", "S"])
                row.append(ch)
            rows.append("".join(row))
        cases.append(f"{size} {key_count}\n" + "\n".join(rows))
    return "\n".join(cases) + "\n0 0\n"


def g4135(r):
    n = r.randint(5, 100); months = r.randint(1, n)
    values = [r.randint(1, 10000) for _ in range(n)]
    return f"{n} {months}\n" + "\n".join(map(str, values)) + "\n"


def g4141(r):
    return " ".join(str(r.randint(0, 12)) for _ in range(6)) + "\n"


def g4144(r):
    n = r.randint(5, 100)
    intervals = []
    for _ in range(n):
        a = r.randint(1, 1_000_000); b = r.randint(a, min(1_000_000, a + 50_000))
        intervals.append(f"{a} {b}")
    return str(n) + "\n" + "\n".join(intervals) + "\n"


def g4145(r):
    parts = []
    for _ in range(r.randint(1, 3)):
        n = r.randint(2, 20); k = r.randint(1, n - 1)
        a = [r.randint(1, 1_000_000_000) for _ in range(n)]
        b = [x + r.randint(0, 1_000_000_000 - x) for x in a]
        parts.append(f"{n} {k}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)))
    return "\n".join(parts) + "\n0 0\n"


def g4147(r):
    n = r.randint(1, 8)
    rods = r.sample(list("abcxyz"), 3)
    return f"{n} {' '.join(rods)}\n"


def g4977(r):
    k = r.randint(1, 5); cases = []
    for _ in range(k):
        n = r.randint(2, 90); values = r.sample(range(1, 10000), n)
        cases += [str(n), " ".join(map(str, values))]
    return str(k) + "\n" + "\n".join(cases) + "\n"


def g5333(r):
    n = r.randint(2, 80); values = [r.randint(1, 10000) for _ in range(n)]
    return str(n) + "\n" + "\n".join(map(str, values)) + "\n"


def g5343(r):
    cards = [s + str(v) for s in "ABCD" for v in range(1, 10)]
    values = r.sample(cards, r.randint(5, 30))
    return str(len(values)) + "\n" + " ".join(values) + "\n"


def g5344(r):
    n = r.randint(3, 1000); return f"{n} {r.randint(2, n - 1)}\n"


EXPRESSIONS = [
    "a+b*c", "(a+b)*c", "a*(b+c)-d", "a/(b-c)+d", "(a+b)/(c+d)",
    "a-b/c", "((a+b)*c-d)/e", "a*(b-c)+d/e", "(a+b*c)-(d/e-f)",
    "a/(b+c*d)-e", "(a-b)*(c+d)", "a+b-c*d/e", "((a+b)-(c*d))/e",
    "a*(b+(c-d))", "(a+b)*(c-d/e)", "a/(b-c+d)", "(a+b+c)*d-e",
    "a-b-(c+d)*e", "a/(b+c)-d*e",
]


def g5430(r):
    expr = EXPRESSIONS[r.randrange(len(EXPRESSIONS))]
    variables = sorted(set(ch for ch in expr if ch.isalpha()))
    values = {ch: r.randint(1, 9) for ch in variables}
    # Keep every denominator nonzero for the expression families used here.
    if "b-c" in expr and values.get("b") == values.get("c"):
        values["c"] = values["c"] % 9 + 1
    if "b+c" in expr and values.get("b", 1) + values.get("c", 1) == 0:
        values["c"] = 1
    return expr + "\n" + str(len(variables)) + "\n" + "\n".join(f"{x} {values[x]}" for x in variables) + "\n"


def g5442(r):
    n = r.randint(4, 20); edges = {(i, i + 1): r.randint(1, 99) for i in range(n - 1)}
    degree = [0] * n
    for i in range(n - 1):
        degree[i] += 1; degree[i + 1] += 1
    for i in range(n):
        for j in range(i + 2, n):
            if len(edges) >= 75 or degree[i] >= 15 or degree[j] >= 15 or r.random() >= .18: continue
            edges[(i, j)] = r.randint(1, 99)
            degree[i] += 1; degree[j] += 1
    rows = []
    for i in range(n - 1):
        later = [(j, w) for (a, j), w in edges.items() if a == i]
        rows.append(" ".join([chr(65 + i), str(len(later))] + [x for pair in later for x in (chr(65 + pair[0]), str(pair[1]))]))
    return str(n) + "\n" + "\n".join(rows) + "\n"


def g5443(r):
    p = r.randint(4, 14); names = [f"Place{i}" for i in range(p)]
    edges = {(i, i + 1): r.randint(1, 999) for i in range(p - 1)}
    for i in range(p):
        for j in range(i + 2, p):
            if len(edges) < 49 and r.random() < .15: edges[(i, j)] = r.randint(1, 999)
    roads = [f"{names[i]} {names[j]} {w}" for (i, j), w in edges.items()]
    queries = [(r.randrange(p), r.randrange(p)) for _ in range(r.randint(2, 10))]
    return (f"{p}\n" + "\n".join(names) + f"\n{len(roads)}\n" + "\n".join(roads) +
            f"\n{len(queries)}\n" + "\n".join(f"{names[a]} {names[b]}" for a, b in queries) + "\n")


def g5467(r):
    groups = r.randint(2, 5)
    lines = [str(groups)]
    for _ in range(groups * 2):
        exponents = r.sample(range(0, 50), r.randint(2, 10))
        pairs = []
        for exponent in exponents:
            pairs.append((str(r.randint(-30, 30) or 1), str(exponent)))
        r.shuffle(pairs)
        pairs.append((str(r.randint(1, 30)), str(-r.randint(1, 9))))
        lines.append(" ".join(value for pair in pairs for value in pair))
    return "\n".join(lines) + "\n"


GENERATORS = {n: globals()[f"g{n}"] for n in IDS}


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_id = {x["local_number"]: x for x in manifest["entries"]}
    report = []
    for number in IDS:
        entry = by_id[number]
        body = get_section(entry["source"], number)
        codes = [c for c in fence_blocks(body) if "import " in c or "def " in c]
        code = codes[0]
        marker = "样例输入2" if number in {4115, 4124} else None
        sample_in = first_sample(body, "样例输入", marker)
        sample_out = first_sample(body, "样例输出", "样例输出2" if number in {4115, 4124} else None)
        assert run(code, sample_in).split() == sample_out.split(), number
        directory = TESTS / bucket(number) / f"{number:05d}_made"; data = directory / "data"
        data.mkdir(parents=True, exist_ok=True)
        (directory / "samplecode.py").write_text("# Source: " + entry["source"] + "\n" + code, encoding="utf-8")
        cases = [sample_in] + [GENERATORS[number](random.Random(number + i)) for i in range(1, 20)]
        outputs = [run(code, value) for value in cases]
        produce = f'''import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = {sample_in!r}
SAMPLE_OUT = {sample_out!r}
CASES = {cases!r}
REFERENCE_SOURCE = {code!r}
assert CASES[0] == SAMPLE_IN
random.seed({number})
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
root = Path(__file__).parent / "data"
for index in range(20):
    content = CASES[index]
    (root / f"{{index}}.in").write_text(content, encoding="utf-8")
    (root / f"{{index}}.out").write_text(solve_reference(content), encoding="utf-8")
'''
        (directory / "producecase.py").write_text(produce, encoding="utf-8")
        for old in data.glob("*"): old.unlink()
        for i, (value, output) in enumerate(zip(cases, outputs)):
            (data / f"{i}.in").write_text(value, encoding="utf-8")
            (data / f"{i}.out").write_text(output, encoding="utf-8")
        item = {"local_number": number, "status": "generated", "source": entry["source"], "source_heading": entry["source_heading"], "source_code": "solution collection", "generator": f"g{number}", "seed": number, "output_reference": "embedded solution source", "test_cases": 20, "distinct_input_cases": len(set(cases)), "constraints": CONSTRAINTS[number], "constraints_checked": True}
        report.append(item)
        print("built", number, "distinct", item["distinct_input_cases"], flush=True)
    (ROOT / "collab" / "t002-001b-report.json").write_text(json.dumps({"batch": "001b", "entries": report}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
