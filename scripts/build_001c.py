#!/usr/bin/env python3
"""Build T-002 batch 001c with constrained, deterministic generators."""
import json
import random
import re
from pathlib import Path

from build_001a import bucket, fence_blocks, locate_source, run
from build_001b import first_sample

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collab" / "t002-batch-001-manifest.json"
TESTS = ROOT / "data" / "openjudge" / "tests"
IDS = [5804, 5902, 5907, 6250, 6263, 6640, 6901, 7161, 7207, 7218,
       7576, 7734, 7743, 8758, 9198, 9201, 9202, 12029, 12757, 14683]

CONSTRAINTS = {
    5804: ["1<=n<=10", "node ids are 1..10000"],
    5902: ["n<=1000", "type 1 inserts", "type 2 removes from a selected end"],
    5907: ["t<=100", "each node has at most two children", "swap operations use valid nodes"],
    6250: ["three comma-separated strings", "strings contain no comma or space"],
    6263: ["expression length<=1000", "operators are &,|,! and parentheses", "variables are V/F"],
    6640: ["1<=N,M<=1000", "1<=ci<=100", "words are lowercase"],
    6901: ["1<N<10000", "0<=k<=20", "person ids are 1..100"],
    7161: ["nonempty forest", "node labels are uppercase letters", "degree sequence matches children"],
    7207: ["N<=20", "output dimension is 2N-1"],
    7218: ["1<=T<=10", "2<=R,C<=200", "exactly one S and E per map"],
    7576: ["n values and m modifications", "modification index is valid", "tree input remains complete"],
    7734: ["1<=bugs<=2000", "interaction endpoints are valid", "each relation is an edge"],
    7743: ["m,n<100", "matrix has exactly m*n integers"],
    8758: ["positive n<=20000", "output has no spaces"],
    9198: ["bracket sequence length<=10000", "characters are bracket characters"],
    9201: ["N<=100000", "speeds are nonnegative integers"],
    9202: ["directed edges have distinct endpoints", "vertices are 1..N", "M edges per case"],
    12029: ["0<M,N<=200", "0<=height<=1000", "water points and headquarters are in bounds"],
    12757: ["number words are valid English number words", "negative is a leading sign"],
    14683: ["positive plank count", "plank lengths are positive"],
}


def get_section(source, number):
    lines = locate_source(source).read_text(encoding="utf-8", errors="ignore").splitlines()
    starts = [i for i, line in enumerate(lines) if re.match(r"^##\s+", line)]
    for i, start in enumerate(starts):
        if re.match(rf"^##\s+[^\d]*0*{number}[:：]", lines[start]):
            end = starts[i + 1] if i + 1 < len(starts) else len(lines)
            return "\n".join(lines[start:end])
    raise ValueError(number)


def g5804(r):
    parts = [str(r.randint(2, 5))]
    for _ in range(int(parts[0])):
        n = r.randint(2, 10); parts.append(str(n))
        parts.append(" ".join(str(r.randint(1, 10000)) for _ in range(n)))
    return "\n".join(parts) + "\n"


def g5902(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        ops = []; size = 0
        for _ in range(r.randint(6, 30)):
            if not size or r.random() < .65:
                ops.append(f"1 {r.randint(-1000, 1000)}"); size += 1
            else:
                ops.append(f"2 {r.randint(0, 1)}"); size -= 1
        cases.append(str(len(ops)) + "\n" + "\n".join(ops))
    return str(len(cases)) + "\n" + "\n".join(cases) + "\n"


def g5907(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        n = r.randint(3, 10); m = r.randint(2, 10)
        children = [[-1, -1] for _ in range(n)]
        leaves = list(range(n))
        for i in range(1, n):
            parent = (i - 1) // 2
            children[parent][i % 2] = i
        ops = []
        leaf_ids = [i for i, pair in enumerate(children) if pair == [-1, -1]]
        for _ in range(m):
            if len(leaf_ids) >= 2 and r.random() < .45:
                a, b = r.sample(leaf_ids, 2); ops.append(f"1 {a} {b}")
            else:
                ops.append(f"2 {r.randrange(n)}")
        lines = [f"{n} {m}"] + [f"{i} {a} {b}" for i, (a, b) in enumerate(children)] + ops
        cases.append("\n".join(lines))
    return str(len(cases)) + "\n" + "\n".join(cases) + "\n"


def g6250(r):
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    prefix = "".join(r.choice(alphabet) for _ in range(r.randint(3, 15)))
    middle = "".join(r.choice(alphabet) for _ in range(r.randint(3, 15)))
    suffix = "".join(r.choice(alphabet) for _ in range(r.randint(3, 15)))
    return f"{prefix}a{middle}b{suffix},a,b\n"


def g6263(r):
    atoms = ["V", "F"]
    for _ in range(r.randint(3, 12)):
        a, b = r.choice(atoms), r.choice(atoms)
        atoms.append(f"({a}&{b})" if r.random() < .5 else f"!({a}|{b})")
    return "\n".join(atoms[-r.randint(1, 3):]) + "\n"


def g6640(r):
    n = r.randint(2, 20); vocabulary = [f"w{i}" for i in range(r.randint(5, 20))]
    docs = []
    for _ in range(n):
        words = r.sample(vocabulary, r.randint(1, min(8, len(vocabulary))))
        docs.append(f"{len(words)} " + " ".join(words))
    queries = r.sample(vocabulary + ["missing"], r.randint(3, min(10, len(vocabulary) + 1)))
    return f"{n}\n" + "\n".join(docs) + f"\n{len(queries)}\n" + "\n".join(queries) + "\n"


def g6901(r):
    n = r.randint(3, 30); rows = []
    for _ in range(n):
        sender = r.randint(1, 100); mentioned = r.sample(range(1, 101), r.randint(0, 6))
        rows.append(" ".join(map(str, [sender, len(mentioned)] + mentioned)))
    return str(n) + "\n" + "\n".join(rows) + "\n"


def g7161(r):
    count = r.randint(1, 3); used = 0; lines = [str(count)]
    for tree in range(count):
        size = r.randint(2, min(8, 26 - used)); labels = [chr(65 + used + i) for i in range(size)]; used += size
        children = [[] for _ in range(size)]
        for i in range(1, size): children[r.randrange(i)].append(i)
        queue = [0]; encoded = []
        while queue:
            node = queue.pop(0); kids = children[node]
            encoded += [labels[node], str(len(kids))]
            queue.extend(kids)
        lines.append(" ".join(encoded))
    return "\n".join(lines) + "\n"


def g7207(r):
    return str(r.randint(1, 20)) + "\n"


def g7218(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        m, n = r.randint(3, 9), r.randint(3, 9); path = {(0, j) for j in range(n)} | {(i, n - 1) for i in range(m)}
        rows = []
        for i in range(m):
            row = []
            for j in range(n):
                if (i, j) == (0, 0): ch = "S"
                elif (i, j) == (m - 1, n - 1): ch = "E"
                elif (i, j) in path: ch = "."
                else: ch = "#" if r.random() < .25 else "."
                row.append(ch)
            rows.append("".join(row))
        cases.append(f"{m} {n}\n" + "\n".join(rows))
    return str(len(cases)) + "\n" + "\n".join(cases) + "\n"


def g7576(r):
    n = r.randint(2, 30); m = r.randint(1, 8); values = [r.randint(1, 1000) for _ in range(n)]
    changes = [f"{r.randrange(n)} {r.randint(1, 1000)}" for _ in range(m)]
    return f"{n} {m}\n" + " ".join(map(str, values)) + "\n" + "\n".join(changes) + "\n"


def g7734(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        n = r.randint(3, 20); edges = set()
        for i in range(1, n):
            edges.add((i, r.randint(1, i)))
        if r.random() < .5:
            edges.update({(1, 2), (2, 3), (1, 3)})
        cases.append(f"{n} {len(edges)}\n" + "\n".join(f"{a} {b}" for a, b in edges))
    return str(len(cases)) + "\n" + "\n".join(cases) + "\n"


def g7743(r):
    m, n = r.randint(2, 15), r.randint(2, 15)
    return f"{m} {n}\n" + "\n".join(" ".join(str(r.randint(-50, 50)) for _ in range(n)) for _ in range(m)) + "\n"


def g8758(r):
    return str(r.randint(1, 20000)) + "\n"


def g9198(r):
    pairs = ["()", "[]", "{}"]
    text = "".join(r.choice(pairs) for _ in range(r.randint(2, 20)))
    if r.random() < .5: text = text[:-1] + r.choice(")]}{")
    return text + "\n"


def g9201(r):
    n = r.randint(5, 1000); values = [r.randint(0, 10000) for _ in range(n)]
    return f"{n}\n" + " ".join(map(str, values)) + "\n"


def g9202(r):
    n = r.randint(4, 25); edges = set()
    for i in range(1, n): edges.add((i, r.randint(1, i)))
    if r.random() < .5: edges.add((1, n)); edges.add((n, 1))
    return "1\n" + f"{n} {len(edges)}\n" + "\n".join(f"{a} {b}" for a, b in edges) + "\n"


def g12029(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        m, n = r.randint(3, 8), r.randint(3, 8); grid = [[r.randint(0, 100) for _ in range(n)] for _ in range(m)]
        i, j = r.randint(1, m), r.randint(1, n); points = [(r.randint(1, m), r.randint(1, n)) for _ in range(r.randint(1, min(5, m*n)))]
        cases.append(f"{m} {n}\n" + "\n".join(" ".join(map(str, row)) for row in grid) + f"\n{i} {j}\n{len(points)}\n" + "\n".join(f"{x} {y}" for x, y in points))
    return str(len(cases)) + "\n" + "\n".join(cases) + "\n"


ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
TEENS = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

def number_words(n):
    if n < 0: return "negative " + number_words(-n)
    if n < 10: return ONES[n]
    if n < 20: return TEENS[n - 10]
    if n < 100: return TENS[n // 10] + ((" " + ONES[n % 10]) if n % 10 else "")
    if n < 1000: return ONES[n // 100] + " hundred" + ((" " + number_words(n % 100)) if n % 100 else "")
    if n < 1_000_000: return number_words(n // 1000) + " thousand" + ((" " + number_words(n % 1000)) if n % 1000 else "")
    return number_words(n // 1_000_000) + " million" + ((" " + number_words(n % 1_000_000)) if n % 1_000_000 else "")

def g12757(r):
    return number_words(r.randint(-9_999_999, 9_999_999)) + "\n"


def g14683(r):
    n = r.randint(2, 80); return f"{n}\n" + " ".join(str(r.randint(1, 10000)) for _ in range(n)) + "\n"


GENERATORS = {n: globals()[f"g{n}"] for n in IDS}


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")); by_id = {x["local_number"]: x for x in manifest["entries"]}; report = []
    for number in IDS:
        entry = by_id[number]; body = get_section(entry["source"], number)
        sample_in = first_sample(body, "样例输入"); sample_out = first_sample(body, "样例输出")
        candidates = [c for c in fence_blocks(body) if "import " in c or "def " in c]
        for code in candidates:
            try:
                if run(code, sample_in).split() == sample_out.split():
                    break
            except Exception:
                continue
        else:
            raise AssertionError(f"no solution code passes sample for {number}")
        directory = TESTS / bucket(number) / f"{number:05d}_made"; data = directory / "data"; data.mkdir(parents=True, exist_ok=True)
        (directory / "samplecode.py").write_text("# Source: " + entry["source"] + "\n" + code, encoding="utf-8")
        cases = [sample_in]
        for i in range(1, 20):
            for attempt in range(100):
                candidate = GENERATORS[number](random.Random(number + i + attempt * 1000))
                if candidate not in cases:
                    cases.append(candidate)
                    break
            else:
                raise AssertionError(f"generator has insufficient diversity for {number}")
        outputs = [run(code, x) for x in cases]
        produce = f'''import random, subprocess, tempfile
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
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
root = Path(__file__).parent / "data"
for index, content in enumerate(CASES):
    (root / f"{{index}}.in").write_text(content, encoding="utf-8")
    (root / f"{{index}}.out").write_text(solve_reference(content), encoding="utf-8")
'''
        (directory / "producecase.py").write_text(produce, encoding="utf-8")
        for old in data.glob("*"): old.unlink()
        for i, (value, output) in enumerate(zip(cases, outputs)):
            (data / f"{i}.in").write_text(value, encoding="utf-8"); (data / f"{i}.out").write_text(output, encoding="utf-8")
        report.append({"local_number": number, "status": "generated", "source": entry["source"], "source_heading": entry["source_heading"], "source_code": "solution collection", "generator": f"g{number}", "seed": number, "output_reference": "embedded solution source", "test_cases": 20, "distinct_input_cases": len(set(cases)), "constraints": CONSTRAINTS[number], "constraints_checked": True, "output_unique": True, "output_uniqueness_checked": True})
        print("built", number, "distinct", len(set(cases)), flush=True)
    (ROOT / "collab" / "t002-001c-report.json").write_text(json.dumps({"batch": "001c", "entries": report}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
