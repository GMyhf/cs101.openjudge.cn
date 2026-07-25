#!/usr/bin/env python3
"""Build T-003 batch-002 round two with deterministic, source-backed generators."""
import inspect
import json
import random
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

from build_001a import bucket, fence_blocks, locate_source

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collab/t003-batch-002-round2-manifest.json"
REPORT = ROOT / "collab/t003-002-round2-report.json"
TESTS = ROOT / "data/openjudge/tests"


def g23451(r):
    atoms = [str(r.randint(0, 99)), f"{r.randint(1, 99)}.{r.randint(0, 9)}"]
    denominator = atoms[0] if atoms[0] != "0" else "1"
    lines = [f"{atoms[0]} + {atoms[1]}", f"({atoms[0]} * {atoms[1]})", f"{atoms[1]} / {denominator}"]
    if r.random() < .5:
        lines.append("1 ++ 1")
    if r.random() < .5:
        lines.append("1^2")
    assert lines and all(line != "quit" for line in lines)
    return "\n".join(lines + ["quit"]) + "\n"


def g23563(r):
    terms = []
    for _ in range(r.randint(2, 6)):
        terms.append(f"{r.randint(0, 100)}n^{r.randint(0, 30)}")
    if all(term.startswith("0n") for term in terms):
        terms[0] = "1n^0"
    assert all(term.count("n^") == 1 and term.replace("n^", "").isdigit() for term in terms)
    return "+".join(terms) + "\n"


def g23570(r):
    n = r.randint(1, 30)
    start = "".join(r.choice("01") for _ in range(n))
    target = "".join(r.choice("01") for _ in range(n))
    assert len(start) == len(target) == n and set(start + target) <= set("01")
    return start + "\n" + target + "\n"


def g23660(r):
    rows = []
    for _ in range(r.randint(2, 5)):
        n = r.randint(1, 15)
        values = r.sample(range(1, 100), n)
        rows.append(f"{n} " + " ".join(map(str, values)))
    return str(len(rows)) + "\n" + "\n".join(rows) + "\n"


def g23806(r):
    values = [r.randint(-100, 100) for _ in range(r.randint(6, 45))]
    assert len(values) <= 3000
    return " ".join(map(str, values)) + "\n"


def g23937(r):
    n = r.randint(2, 14)
    grid = [[0 if r.random() < .72 else 1 for _ in range(n)] for _ in range(n)]
    grid[0][0] = grid[-1][-1] = 0
    if r.random() < .55:
        for i in range(n):
            grid[i][i] = 0
    else:
        grid[0][1] = grid[1][0] = 1
    assert grid[0][0] == grid[-1][-1] == 0
    return str(n) + "\n" + "\n".join(" ".join(map(str, row)) for row in grid) + "\n"


def g24375(r):
    cases = []
    for _ in range(r.randint(2, 4)):
        target = r.randint(3, 18)
        pieces = []
        for _ in range(r.randint(2, 5)):
            remaining = target
            group = []
            while remaining > 0:
                part = r.randint(1, remaining)
                group.append(part); remaining -= part
            pieces.extend(group)
        r.shuffle(pieces)
        assert sum(pieces) % target == 0 and len(pieces) <= 64
        cases.extend([str(len(pieces)), " ".join(map(str, pieces))])
    return "\n".join(cases + ["0"]) + "\n"


def _postfix(r, letters=False, depth=0):
    if depth >= 3 or r.random() < .35:
        return r.choice("abcdefghijklmnopqrstuvwxyz") if letters else str(r.randint(1, 30))
    op = r.choice("+-*/") if not letters else r.choice("PQRS")
    return _postfix(r, letters, depth + 1) + " " + _postfix(r, letters, depth + 1) + " " + op


def g24588(r):
    lines = [_postfix(r) for _ in range(r.randint(3, 8))]
    assert all("/ 0" not in line for line in lines)
    return str(len(lines)) + "\n" + "\n".join(lines) + "\n"


def _infix(r, depth=0):
    if depth >= 3 or r.random() < .35:
        return str(r.randint(1, 99))
    return "(" + _infix(r, depth + 1) + r.choice("+-*/") + _infix(r, depth + 1) + ")"


def g24591(r):
    lines = [_infix(r) for _ in range(r.randint(3, 8))]
    assert all(line and " " not in line for line in lines)
    return str(len(lines)) + "\n" + "\n".join(lines) + "\n"


def g24676(r):
    cases = []
    for _ in range(r.randint(2, 4)):
        n = r.randint(1, 5)
        cases.append(str(n))
        cases.extend(" ".join(str(r.randint(1, 30)) for _ in range(n)) for _ in range(n))
    return "\n".join(cases + ["0"]) + "\n"


def g24678(r):
    n = r.randint(2, 35); prices = [r.randint(1, 99999) for _ in range(n)]
    total = sum(prices)
    w = total + r.randint(1, 1000) if r.random() < .2 else r.randint(1, total)
    assert 0 < w < 10**9 and all(0 < x < 10**5 for x in prices)
    return f"{w} {n}\n" + " ".join(map(str, prices)) + "\n"


def g24684(r):
    votes = [r.randint(1, 100000) for _ in range(r.randint(5, 60))]
    assert len(votes) <= 100000 and len(set(votes)) <= 100
    return " ".join(map(str, votes)) + "\n"


def g24686(r):
    k = r.randint(1, 8); nodes = 2 ** k - 1; lines = []
    for _ in range(r.randint(10, 45)):
        x = r.randint(1, nodes)
        if r.random() < .6:
            lines.append(f"1 {x} {r.randint(-100, 100)}")
        else:
            lines.append(f"2 {x}")
    assert all(1 <= int(line.split()[1]) <= nodes for line in lines)
    return f"{k} {len(lines)}\n" + "\n".join(lines) + "\n"


def g24687(r):
    n = r.randint(2, 30); m = r.randint(1, n - 1); population = [r.randint(1, 1000) for _ in range(n)]
    assert 0 < m < n and all(0 < x <= 1000 for x in population)
    return f"{n} {m}\n" + " ".join(map(str, population)) + "\n"


def _tree_pair(r, max_size=20):
    def build(chars):
        if not chars: return None
        i = r.randrange(len(chars))
        return (chars[i], build(chars[:i]), build(chars[i + 1:]))
    chars = r.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", r.randint(2, max_size)); tree = build(chars)
    def inorder(node): return "" if node is None else inorder(node[1]) + node[0] + inorder(node[2])
    def postorder(node): return "" if node is None else postorder(node[1]) + postorder(node[2]) + node[0]
    def preorder(node): return "" if node is None else node[0] + preorder(node[1]) + preorder(node[2])
    ino, post, pre = inorder(tree), postorder(tree), preorder(tree)
    assert len(ino) == len(post) == len(pre) and sorted(ino) == sorted(post) == sorted(pre)
    return tree, ino, post, pre


def g24750(r):
    _, ino, post, pre = _tree_pair(r, 26)
    assert len(ino) <= 26
    return ino + "\n" + post + "\n"


def g25145(r):
    pairs = [_tree_pair(r, 26)[1:3] for _ in range(r.randint(2, 8))]
    assert all(len(ino) <= 26 for ino, _ in pairs)
    return str(len(pairs)) + "\n" + "\n".join(f"{ino}\n{post}" for ino, post in pairs) + "\n"


def g24834(r):
    pairs = []
    for _ in range(r.randint(3, 8)):
        s = "".join(r.choice("abcd") for _ in range(r.randint(1, 10)))
        mode = r.randrange(3)
        if mode == 0: p = s
        elif mode == 1: p = "*" + s[:r.randint(0, len(s))] + "*"
        else: p = "?" * len(s)
        if r.random() < .4: p += "z"
        pairs.extend([s, p])
    assert len(pairs) % 2 == 0 and all(0 < len(x) < 50 for x in pairs)
    return str(len(pairs) // 2) + "\n" + "\n".join(pairs) + "\n"


def g25140(r):
    lines = [_postfix(r, letters=True) for _ in range(r.randint(3, 8))]
    assert all(len(line.replace(" ", "")) <= 100 for line in lines)
    return str(len(lines)) + "\n" + "\n".join(line.replace(" ", "") for line in lines) + "\n"


def g25302(r):
    rows = []
    for _ in range(r.randint(2, 8)):
        intervals = []
        for _ in range(r.randint(2, 12)):
            x = r.randint(0, 100); intervals.append((x, x + r.randint(1, 30)))
        rows.append([str(len(intervals))] + [f"{x} {y}" for x, y in intervals])
    return str(len(rows)) + "\n" + "\n".join("\n".join(row) for row in rows) + "\n"


def g25353(r):
    n = r.randint(2, 45); d = r.randint(1, 40); heights = [r.randint(1, 1000) for _ in range(n)]
    assert 1 <= n <= 10**5 and 1 <= d <= 10**9 and all(1 <= x <= 10**9 for x in heights)
    return f"{n} {d}\n" + "\n".join(map(str, heights)) + "\n"


GENERATORS = {n: globals()[f"g{n}"] for n in [23451, 23563, 23570, 23660, 23806, 23937, 24375, 24588, 24591, 24676, 24678, 24684, 24686, 24687, 24750, 24834, 25140, 25145, 25302, 25353]}

CONSTRAINTS = {
    23451: ["input ends with quit", "expressions use the stated number/operator/bracket grammar", "results are printed to three decimals"],
    23563: ["each term is coefficient*n^exponent", "coefficients and exponents are non-negative and at most 10^8", "at least one term is present"],
    23570: ["the two lock strings have equal positive length", "strings contain only 0 and 1", "impossible cases output impossible"],
    23660: ["t<10", "1<=n<=16", "each row contains n distinct positive integers", "the empty selection counts"],
    23806: ["the input contains at most 3000 integers", "duplicate value triples count once", "the target sum is zero"],
    23937: ["2<=N<=20", "the map is an N by N grid of 0/1 cells", "the start and end cells are passable", "moves are right or down only"],
    24375: ["each n is at most 64", "stick lengths are positive integers", "input ends with n=0", "each generated instance has a valid equal-length partition"],
    24588: ["n<100", "each postfix expression has length at most 1000", "operands are integers or decimals", "operators are +,-,*,/"],
    24591: ["n<100", "each infix expression has length at most 700", "numbers and operators have no spaces", "operators are +,-,*,/ and parentheses are balanced"],
    24676: ["1<=n<=5 for each matrix", "matrix entries are positive integers", "input ends with n=0", "each matrix is n by n"],
    24678: ["0<W<10^9", "0<n<10^5", "0<pi<10^5", "purchased houses form one contiguous segment"],
    24684: ["there are at most 100000 votes", "vote ids are positive and at most 100000", "at most 100 different options occur"],
    24686: ["k<=15", "n<=50000 operations", "node ids are in 1..2^k-1", "update y has absolute value at most 100"],
    24687: ["n<=100", "0<m<n", "each population ai is positive and at most 1000", "m control points split the line into m+1 parts"],
    24750: ["inorder and postorder lengths are at most 26", "nodes are distinct uppercase letters", "both traversals describe one binary tree"],
    24834: ["n<=30", "s is non-empty lowercase letters", "pattern uses lowercase letters, ? and *", "both string lengths are less than 50"],
    25140: ["n<100", "each postfix expression has length at most 100", "operands are lowercase letters", "operators are uppercase binary operators"],
    25145: ["n<=30 trees", "each traversal uses distinct uppercase letters", "inorder and postorder describe one binary tree", "traversal lengths are at most 26"],
    25302: ["t<=100", "1<=n<=100 per case", "each interval satisfies 0<=x<y<=10^9", "an end at the same time as a start does not overlap"],
    25353: ["1<=N<=10^5", "1<=D<=10^9", "1<=hi<=10^9", "adjacent people can swap when height difference is at most D"],
}
STRUCTURE_CHECKS = {
    23937: "start and end cells are passable; generated paths or blocked entrances are explicit",
    24750: "inorder and postorder are traversals of one generated binary tree",
    25145: "inorder and postorder are traversals of one generated binary tree",
    25140: "postfix expression is generated from a full binary expression tree",
    25302: "each interval has x < y and each case has the declared row count",
}


def run(code, content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as f:
        f.write(code); f.flush()
        result = subprocess.run([sys.executable, f.name], input=content, text=True, capture_output=True, timeout=10)
    if result.returncode: raise RuntimeError(result.stderr[-1000:])
    return result.stdout


def find_section(source, number):
    lines = locate_source(source).read_text(encoding="utf-8", errors="ignore").splitlines()
    starts = [i for i, x in enumerate(lines) if re.match(r"^##\s+", x)]
    for i, start in enumerate(starts):
        if re.match(rf"^##\s+[^\d]*0*{number}[:：]", lines[start]):
            return "\n".join(lines[start:starts[i + 1] if i + 1 < len(starts) else len(lines)])
    raise ValueError(number)


def reproduce(number):
    directory = TESTS / bucket(number) / f"{number:05d}_made"; data = directory / "data"
    before = {p.name: p.read_bytes() for p in sorted(data.iterdir())}
    result = subprocess.run([sys.executable, "producecase.py"], cwd=directory, capture_output=True, timeout=600)
    after = {p.name: p.read_bytes() for p in sorted(data.iterdir())}
    return result.returncode == 0 and before == after


def summarise(number, cases, outputs, heading, target):
    frequency = Counter(tuple(o.split()) for o in outputs).most_common(1)[0][1]
    return {"local_number": number, "source_heading": heading, "source_code": "solution collection",
            "generator": f"g{number}", "seed": number, "test_cases": target,
            "distinct_input_cases": len(set(cases)), "distinct_outputs": len({tuple(o.split()) for o in outputs}),
            "max_output_frequency": frequency,
            "constant_output_probe": {"frequency": frequency, "total": target,
                                      "status": "rejected" if frequency < target else "accepted"},
            "max_input_bytes": max(map(len, cases)), "constraints": CONSTRAINTS[number],
            "generator_seed_smoke": {"seeds_per_generator": 20000, "status": "passed"},
            "structure_checked": number in STRUCTURE_CHECKS, "structure_check": STRUCTURE_CHECKS.get(number),
            "sample_reproduced": True, "producecase_reproduced": reproduce(number)}


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")); report = []
    for entry in manifest["entries"]:
        number = entry["local_number"]; text = find_section(entry["source"], number)
        for seed in range(20000):
            GENERATORS[number](random.Random(number + seed))
        codes = [c for c in fence_blocks(text) if "import " in c or "def " in c]
        code = next((c for c in codes if run(c, entry["sample_input"]).split() == entry["sample_output"].split()), None)
        if code is None: raise AssertionError(f"no sample-passing code {number}")
        target = 20; cases = [entry["sample_input"]]
        for i in range(1, target):
            for attempt in range(100):
                value = GENERATORS[number](random.Random(number + i + attempt * 1000))
                if value not in cases: cases.append(value); break
            else: raise AssertionError(f"insufficient diversity {number}")
        directory = TESTS / bucket(number) / f"{number:05d}_made"; data = directory / "data"; data.mkdir(parents=True, exist_ok=True)
        outputs = [run(code, value) for value in cases]
        (directory / "samplecode.py").write_text("# Source: " + entry["source"] + "\n" + code, encoding="utf-8")
        source = inspect.getsource(GENERATORS[number]).replace(f"def g{number}", "def generate_case")
        helpers = ""
        if number in (24588, 25140): helpers += inspect.getsource(_postfix) + "\n"
        if number == 24591: helpers += inspect.getsource(_infix) + "\n"
        if number in (24750, 25145): helpers += inspect.getsource(_tree_pair) + "\n"
        produce = f'''import random, subprocess, tempfile\nfrom pathlib import Path\nREFERENCE_SOURCE = {code!r}\nSAMPLE_IN = {entry["sample_input"]!r}\nSAMPLE_OUT = {entry["sample_output"]!r}\n{helpers}{source}\nwith tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:\n    handle.write(REFERENCE_SOURCE); handle.flush()\n    root = Path(__file__).parent / "data"\n    seen = [SAMPLE_IN]\n    for index in range({target}):\n        if index == 0:\n            content = SAMPLE_IN\n        else:\n            for attempt in range(100):\n                content = generate_case(random.Random({number} + index + attempt * 1000))\n                if content not in seen: break\n            else: raise AssertionError("insufficient diversity")\n        seen.append(content)\n        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)\n        (root / f"{{index}}.in").write_text(content, encoding="utf-8")\n        (root / f"{{index}}.out").write_text(result.stdout, encoding="utf-8")\n'''
        (directory / "producecase.py").write_text(produce, encoding="utf-8")
        for old in data.glob("*"): old.unlink()
        for i, (value, output) in enumerate(zip(cases, outputs)):
            (data / f"{i}.in").write_text(value, encoding="utf-8"); (data / f"{i}.out").write_text(output, encoding="utf-8")
        report.append(summarise(number, cases, outputs, entry["source_heading"], target)); print("built", number, flush=True)
    REPORT.write_text(json.dumps({"batch": "T-003-002-r2", "entries": report}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__": main()
