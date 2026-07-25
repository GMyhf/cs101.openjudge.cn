#!/usr/bin/env python3
"""Build the final T-003 batch-002 round with semantic generators."""
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
MANIFEST = ROOT / "collab/t003-batch-002-round5-manifest.json"
REPORT = ROOT / "collab/t003-002-round5-report.json"
TESTS = ROOT / "data/openjudge/tests"


def g23555(r):
    n = r.randint(2, 8); cells = [(i, j) for i in range(n) for j in range(n)]
    r.shuffle(cells); m1 = r.randint(1, min(12, len(cells))); xcells = cells[:m1]
    r.shuffle(cells); m2 = r.randint(1, min(12, len(cells))); ycells = cells[:m2]
    if not any(j == k for _, j in xcells for k, _ in ycells):
        xcells[0] = (xcells[0][0], ycells[0][0])
    xv = [(i, j, r.choice([x for x in range(-9, 10) if x])) for i, j in xcells]
    yv = [(i, j, r.choice([x for x in range(-9, 10) if x])) for i, j in ycells]
    assert len({(i, j) for i, j, _ in xv}) == m1 and len({(i, j) for i, j, _ in yv}) == m2
    assert all(v != 0 and 0 <= i < n and 0 <= j < n for i, j, v in xv + yv)
    return f"{n} {m1} {m2}\n" + "\n".join(f"{i} {j} {v}" for i, j, v in xv + yv) + "\n"


def g24390(r):
    n = r.randint(2, 12); bits = [0] * n
    steps = r.randint(1, 12)
    for _ in range(steps):
        i = r.randrange(n)
        for j in (i - 1, i, i + 1):
            if 0 <= j < n: bits[j] ^= 1
    assert all(x in (0, 1) for x in bits)
    return f"{n}\n" + "".join(map(str, bits)) + "\n"


def g24677(r):
    if r.random() < .65:
        parts = [str(r.randint(0, 500)) for _ in range(4)]
        value = "".join(parts)
    else:
        value = "".join(r.choice("0123456789") for _ in range(r.randint(1, 24)))
    assert len(value) <= 30 and value.isdigit()
    return value + "\n"


def g27237(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        start = r.randint(1, 3); pos = start; path = []
        for _ in range(r.randint(2, 5)):
            if pos <= 1 or r.random() < .55:
                path.append("H"); pos *= 3
            else:
                path.append("O"); pos //= 2
        end = pos; path = "".join(path)
        if end == start:
            path = "H"; end = start * 3
        assert 1 <= start <= 1000 and 1 <= end <= 1000 and 1 <= len(path) <= 25
        cases.append((start, end))
    return "\n".join(f"{a} {b}" for a, b in cases) + "\n0 0\n"


def g27301(r):
    n = r.randint(1, 20); plants = [r.randint(1, 30) for _ in range(n)]
    a = max(plants) + r.randint(0, 15); b = max(plants) + r.randint(0, 15)
    assert a > max(plants) - 1 and b > max(plants) - 1
    return f"{n} {a} {b}\n" + " ".join(map(str, plants)) + "\n"


def g27306(r):
    n = r.randint(3, 15); labels = [r.randrange(2) for _ in range(n)]; edges = []
    for _ in range(r.randint(2, min(20, n * (n - 1) // 2))):
        a, b = r.sample(range(n), 2); edges.append((a, b, labels[a] ^ labels[b]))
    if r.random() < .5:
        a, b = r.sample(range(n), 2); edges.append((a, b, 1 - (labels[a] ^ labels[b])))
    assert all(0 <= a < n and 0 <= b < n and c in (0, 1) for a, b, c in edges)
    return f"{n} {len(edges)}\n" + "\n".join(f"{a} {b} {c}" for a, b, c in edges) + "\n"


def g27310(r):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; blocks = []
    for _ in range(4): blocks.append("".join(r.choice(alphabet) for _ in range(6)))
    words = []
    for _ in range(r.randint(4, 10)):
        if r.random() < .55:
            chosen = r.sample(range(4), r.randint(1, 4)); word = "".join(r.choice(blocks[i]) for i in chosen)
        else:
            word = "".join(r.choice(alphabet) for _ in range(r.randint(1, 4)))
        words.append(word)
    assert all(1 <= len(w) <= 4 and w.isupper() for w in words)
    return str(len(words)) + "\n" + "\n".join(blocks + words) + "\n"


def g27351(r):
    n = r.randint(2, 12); all_edges = [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]
    r.shuffle(all_edges); m = r.randint(0, min(30, len(all_edges))); edges = sorted(all_edges[:m])
    assert len(edges) == len(set(edges)) and all(1 <= a < b <= n for a, b in edges)
    return f"{n} {m}\n" + "\n".join(f"{a} {b}" for a, b in edges) + ("\n" if edges else "")


def g27951(r):
    m = r.randint(1, 10); n = r.randint(1, 60); words = [r.randint(0, 30) for _ in range(n)]
    assert 1 <= m <= 100 and len(words) == n and all(0 <= x <= 1000 for x in words)
    return f"{m} {n}\n" + " ".join(map(str, words)) + "\n"


def g28701(r):
    n = r.randint(2, 25); k = r.randint(1, n - 1); times = [r.randint(1, 100) for _ in range(n)]
    assert 0 < k <= n and all(0 < x <= 1000000 for x in times)
    return f"{n} {k}\n" + " ".join(map(str, times)) + "\n"


def g28776(r):
    n = r.randint(1, 8); king_a, king_b = r.randint(1, 10), r.randint(1, 10)
    ministers = [(r.randint(1, 10), r.randint(1, 10)) for _ in range(n)]
    return f"{n}\n{king_a} {king_b}\n" + "\n".join(f"{a} {b}" for a, b in ministers) + "\n"


def g31041(r):
    n = r.randint(2, 80); k = r.randint(1, n); avals = r.sample(range(1, 10**9), n); bvals = r.sample(range(1, 10**9), n)
    assert len(set(avals)) == n and len(set(bvals)) == n
    return f"{n} {k}\n" + "\n".join(f"{a} {b}" for a, b in zip(avals, bvals)) + "\n"


GENERATORS = {n: globals()[f"g{n}"] for n in [23555, 24390, 24677, 27237, 27301, 27306, 27310, 27351, 27951, 28701, 28776, 31041]}
CONSTRAINTS = {
    23555: ["matrix dimension is n*n", "stored coordinates are zero-based and unique within each matrix", "stored values are nonzero", "product output is sorted by row then column"],
    24390: ["1<=N<=20", "input is a binary string of length N", "the generated state is reachable from a uniform color by legal adjacent flips"],
    24677: ["0<=len(S)<=30", "the four coordinates are decimal substrings", "safe coordinates are 0..500 without leading zero"],
    27237: ["1<=n,m<=1000", "H maps x to 3x and O maps x to floor(x/2)", "0 0 terminates input", "generated targets have a legal path of at most 25 hops"],
    27301: ["n<=100", "capacities exceed every plant requirement", "Alice proceeds left-to-right and Bob right-to-left", "refill is only allowed when the next plant cannot be fully watered"],
    27306: ["0<=plant indices<n", "each relation is same/different", "the generated batch includes consistent and contradictory parity systems"],
    27310: ["there are four blocks with six uppercase letters each", "each requested word has 1..4 uppercase letters", "a block can be used at most once per word"],
    27351: ["1<=a<b<=n for every distinct weight-1 edge", "m<=n(n-1)/2", "the graph is complete with listed edges having weight 1 and all others weight 0"],
    27951: ["M<=100 and N<=1000", "word values are nonnegative and at most 1000", "memory is FIFO and starts empty"],
    28701: ["0<k<=n", "n<=1000", "each frying time is a positive integer at most 1000000", "the fryer always contains exactly k pieces"],
    28776: ["1<=n<=100", "king and ministers' hand values are 1..10", "each order is evaluated using the product of preceding left hands"],
    31041: ["1<=K<=N<=1000000", "A and B values are positive and have no ties", "the first round selects the top K A values and the second selects the top B among them"],
}
STRUCTURE_CHECKS = {
    23555: "each sparse matrix has unique in-range nonzero coordinates",
    24390: "the initial bit state is obtained by legal flips from all zero",
    27237: "each target is produced by replaying a legal H/O path",
    27306: "relations are generated from a parity assignment, with an explicit contradictory relation for NO cases",
    27351: "weight-1 edges are unique, ordered, and in range",
    31041: "A and B are each tie-free, as required by the two voting rounds",
}


def run(code, content, timeout=10):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as f:
        f.write(code); f.flush()
        result = subprocess.run([sys.executable, f.name], input=content, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(result.stderr[-1200:])
    return result.stdout


def find_section(source, number):
    lines = locate_source(source).read_text(encoding="utf-8", errors="ignore").splitlines()
    starts = [i for i, x in enumerate(lines) if re.match(r"^##\s+", x)]
    for i, start in enumerate(starts):
        if re.search(rf"0*{number}[:：]", lines[start]):
            return "\n".join(lines[start:starts[i + 1] if i + 1 < len(starts) else len(lines)])
    raise ValueError(number)


def reproduce(number):
    directory = TESTS / bucket(number) / f"{number:05d}_made"; data = directory / "data"
    before = {p.name: p.read_bytes() for p in sorted(data.iterdir())}
    result = subprocess.run([sys.executable, "producecase.py"], cwd=directory, capture_output=True, timeout=600)
    after = {p.name: p.read_bytes() for p in sorted(data.iterdir())}
    return result.returncode == 0 and before == after


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")); report = []
    for entry in manifest["entries"]:
        number = entry["local_number"]; text = find_section(entry["source"], number)
        codes = [c for c in fence_blocks(text) if "import " in c or "def " in c]
        code = next((c for c in codes if run(c, entry["sample_input"]).split() == entry["sample_output"].split()), None)
        if code is None: raise AssertionError(f"no sample-passing code {number}")
        for seed in range(20000): GENERATORS[number](random.Random(number + seed))
        for seed in range(400): run(code, GENERATORS[number](random.Random(number + seed)), timeout=10)
        cases = [entry["sample_input"]]
        for i in range(1, 21):
            for attempt in range(100):
                value = GENERATORS[number](random.Random(number + i + attempt * 1000))
                if value not in cases: cases.append(value); break
            else: raise AssertionError(f"insufficient diversity {number}")
        directory = TESTS / bucket(number) / f"{number:05d}_made"; data = directory / "data"; data.mkdir(parents=True, exist_ok=True)
        outputs = [run(code, x) for x in cases]
        (directory / "samplecode.py").write_text("# Source: " + entry["source"] + "\n" + code, encoding="utf-8")
        source = inspect.getsource(GENERATORS[number]).replace(f"def g{number}", "def generate_case")
        produce = f'''import random, subprocess, tempfile\nfrom pathlib import Path\nREFERENCE_SOURCE = {code!r}\nSAMPLE_IN = {entry["sample_input"]!r}\n{source}\nwith tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:\n    handle.write(REFERENCE_SOURCE); handle.flush()\n    root = Path(__file__).parent / "data"\n    seen = [SAMPLE_IN]\n    for index in range(21):\n        if index == 0: content = SAMPLE_IN\n        else:\n            for attempt in range(100):\n                content = generate_case(random.Random({number} + index + attempt * 1000))\n                if content not in seen: break\n            else: raise AssertionError("insufficient diversity")\n        seen.append(content)\n        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)\n        (root / f"{{index}}.in").write_text(content, encoding="utf-8")\n        (root / f"{{index}}.out").write_text(result.stdout, encoding="utf-8")\n'''
        (directory / "producecase.py").write_text(produce, encoding="utf-8")
        for old in data.glob("*"): old.unlink()
        for i, (case, output) in enumerate(zip(cases, outputs)):
            (data / f"{i}.in").write_text(case, encoding="utf-8"); (data / f"{i}.out").write_text(output, encoding="utf-8")
        freq = Counter(tuple(x.split()) for x in outputs).most_common(1)[0][1]
        report.append({"local_number": number, "source_heading": entry["source_heading"], "source_code": "solution collection", "generator": f"g{number}", "seed": number, "test_cases": 21, "distinct_input_cases": len(set(cases)), "distinct_outputs": len({tuple(x.split()) for x in outputs}), "max_output_frequency": freq, "constant_output_probe": {"frequency": freq, "total": 21, "status": "rejected" if freq < 21 else "accepted"}, "max_input_bytes": max(map(len, cases)), "constraints": CONSTRAINTS[number], "structure_checked": number in STRUCTURE_CHECKS, "structure_check": STRUCTURE_CHECKS.get(number), "generator_seed_smoke": {"seeds_per_generator": 20000, "status": "passed"}, "reference_seed_smoke": {"seeds": 400, "status": "passed"}, "sample_reproduced": True, "producecase_reproduced": reproduce(number)})
        print("built", number, flush=True)
    REPORT.write_text(json.dumps({"batch": "T-003-002-r5", "entries": report}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__": main()
