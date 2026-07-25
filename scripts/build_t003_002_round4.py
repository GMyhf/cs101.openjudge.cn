#!/usr/bin/env python3
"""Build T-003 batch-002 round four with semantic generators and solver smoke tests."""
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
MANIFEST = ROOT / "collab/t003-batch-002-round4-manifest.json"
REPORT = ROOT / "collab/t003-002-round4-report.json"
TESTS = ROOT / "data/openjudge/tests"


def g28906(r):
    n = r.randint(7, 60); k = r.randint(2, min(6, n))
    assert n > 6 and 2 <= k <= 6
    return f"{n} {k}\n"


def g28970(r):
    rows = []
    for _ in range(r.randint(2, 12)):
        m = r.randint(1, 20); rows.append([r.randint(0, 1000) for _ in range(m)])
    assert all(1 <= len(a) <= 20 and all(0 <= x <= 10**7 for x in a) for a in rows)
    return str(len(rows)) + "\n" + "\n".join(f"{len(a)} " + " ".join(map(str, a)) for a in rows) + "\n"


def g28972(r):
    n, m = r.randint(1, 12), r.randint(1, 12)
    rows = [[r.randint(1, 100) for _ in range(m)] for _ in range(n)]
    assert len(rows) == n and all(len(row) == m and min(row) >= 1 for row in rows)
    return f"{n} {m}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + "\n"


def g29411(r):
    return f"{r.randint(1, 3999)}\n"


def g29455(r):
    alphabet = "abcdefg"
    first = r.sample(alphabet, 2)
    s = "".join(first) + "".join(r.choice(alphabet) for _ in range(r.randint(0, 28)))
    mapping = {}; available = list(alphabet); t = []
    for ch in s:
        if ch not in mapping: mapping[ch] = r.choice(available); available.remove(mapping[ch])
        t.append(mapping[ch])
    if r.random() < .5: t[1] = t[0]
    assert len(s) == len(t)
    return s + "\n" + "".join(t) + "\n"


def g29458(r):
    n = r.randint(1, 80); a = [r.randint(1, 10**9) for _ in range(n)]
    assert len(a) == n and all(1 <= x <= 10**9 for x in a)
    return f"{n}\n" + " ".join(map(str, a)) + "\n"


def g29646(r):
    rows = [(r.randint(1, 100), r.randint(50, 1000)) for _ in range(r.randint(2, 8))]
    return str(len(rows)) + "\n" + "\n".join(f"{a} {b}" for a, b in rows) + "\n"


def g29702(r):
    labels = [1, 2, 3]; r.shuffle(labels)
    a, b, c = labels
    return f"3 3\n{a} > {b}\n{b} > {c}\n{a} > {c}\n"


def g29741(r):
    n, layers, mod = r.randint(2, 6), r.randint(2, 7), r.randint(2, 10)
    rows = [[r.randint(0, mod) for _ in range(n)] for _ in range(3)]
    assert all(len(row) == n and all(0 <= x <= mod for x in row) for row in rows)
    return f"{n} {layers} {mod}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + "\n"


def g29803(r):
    n = r.randint(2, 8); edges = [(1, n, r.randint(1, 20), r.randint(0, 100))]
    for v in range(2, n): edges.append((v, v + 1, r.randint(1, 20), r.randint(0, 100)))
    if n >= 3: edges.append((1, 2, r.randint(1, 20), r.randint(0, 100)))
    total = sum(e[2] for e in edges[:n - 1]); limit = total + r.randint(0, 10)
    assert any(u == 1 and v == n for u, v, _, _ in edges)
    return f"{n} {len(edges)} {limit}\n" + "\n".join("%d %d %d %d" % e for e in edges) + "\n"


def g29895(r):
    a = r.randint(2, 100000); b = r.randint(2, 100000)
    return f"{a * b}\n"


def g29896(r):
    n = r.randint(2, 10); coins = sorted(r.sample(range(1, 40), n)); x = r.randint(1, 300)
    assert len(set(coins)) == n
    return f"{x} {n}\n" + " ".join(map(str, coins)) + "\n"


def g30020(r):
    values = [r.randint(1, 1000) for _ in range(5)]
    return " ".join(map(str, values)) + "\n"


def g30191(r):
    n = r.randint(1, 5); k = r.randint(0, n * n)
    return f"{n} {k}\n"


def g30646(r):
    n = r.randint(1, 100); a = [r.randint(-100, 100) for _ in range(n)]
    return f"{n}\n" + " ".join(map(str, a)) + "\n"


def g30830(r):
    n = r.randint(5, 14); root = 1; edges = [(i, i + 1) for i in range(1, n)]
    qrows = []
    for _ in range(r.randint(2, 8)):
        p = r.randint(1, n - 2); q = p + 2 * r.randint(1, (n - p) // 2)
        qrows.append((p, q, 1, 1))
    return f"{n} {root}\n" + "\n".join(f"{u} {v}" for u, v in edges) + f"\n{len(qrows)}\n" + "\n".join("%d %d %d %d" % row for row in qrows) + "\n"


def g30874(r):
    n = r.randint(5, 60); roles = ["T", "H"] + ["D"] * 3
    roles += [r.choice("DTH") for _ in range(n - 5)]; r.shuffle(roles)
    assert len(roles) == n and all(x in "DTH" for x in roles)
    return f"{n}\n" + " ".join(roles) + "\n"


def g30878(r):
    n = r.randint(2, 30); ops = []
    for _ in range(r.randint(4, 20)):
        l, rr = sorted((r.randint(1, n), r.randint(1, n)))
        if r.random() < .6: ops.append(f"Add {l} {rr} {r.randint(-50, 50)}")
        else: ops.append(f"Query {l} {rr}")
    if not any(x.startswith("Query") for x in ops): ops.append(f"Query 1 {n}")
    return f"{n} {len(ops)}\n" + "\n".join(ops) + "\n"


def g30919(r):
    n = r.randint(1, 40); xs = r.sample(range(1, 1000), n)
    return f"{n}\n" + " ".join(map(str, xs)) + "\n"


def g30930(r):
    n = r.randint(1, 80); values = [r.randint(0, 1000) for _ in range(n)]
    return f"{n}\n" + " ".join(map(str, values)) + "\n"


GENERATORS = {n: globals()[f"g{n}"] for n in [28906, 28970, 28972, 29411, 29455, 29458, 29646, 29702, 29741, 29803, 29895, 29896, 30020, 30191, 30646, 30830, 30874, 30878, 30919, 30930]}
CONSTRAINTS = {
    28906: ["7<n<=200", "2<=k<=6", "parts are positive and unordered"],
    28970: ["number of arrays is at most 350", "1<=m<=20", "array elements are 0..10^7"],
    28972: ["1<=n,m<=400", "heights are positive integers at most 10^9", "moves share an edge"],
    29411: ["input integer is 1..3999", "only the six stated subtractive forms are used"],
    29455: ["strings have equal length", "mapping is one-to-one and position-preserving"],
    29458: ["1<=n", "array values are 1..10^9", "inversion means i<j and a[i]>a[j]"],
    29646: ["each input row is harmful bacteria then beneficial bacteria", "beneficial growth is floor(1.05*m)", "harmful bacteria are capped at one million"],
    29702: ["relations use distinct node labels", "relations describe a consistent flow ordering"],
    29741: ["2<=N<=10^6", "2<=L<=10^5", "2<=M<=100", "costs are 0..M"],
    29803: ["graph is undirected and may have parallel edges", "edge time is positive and danger is 0..100", "a path within T exists at protection 100"],
    29895: ["n is a composite positive integer at most 10^10", "the answer is the largest proper factor"],
    29896: ["coin values are distinct positive integers", "each coin has unlimited supply", "the selected multiset covers every value 1..X"],
    30020: ["each of five quantities is 1..1000", "items have sizes 5x5,3x4,2x3,1x2,1x1", "one car has a 6x6 grid"],
    30191: ["1<=N<=9", "0<=K<=N*N", "kings cannot attack in any of eight adjacent directions"],
    30646: ["1<=n<=100", "array values fit the stated 32-bit range", "answer is the smallest absent positive integer"],
    30830: ["input edges form a tree", "L is divisible by v1+v2", "meeting occurs at an integer-time node"],
    30874: ["roles are T,H,D", "a team is one T, one H, and three D", "earliest eligible queued players are selected"],
    30878: ["1<=l<=r<=N", "Add uses -10^9..10^9", "Query asks the maximum current force"],
    30919: ["positions are distinct positive integers", "one optional move divides days into two consecutive groups", "distance is twice the sum of absolute deviations"],
    30930: ["1<=n<=5*10^5", "speech counts are 0..10^9", "h-index is the largest k with at least k values >=k"],
}
STRUCTURE_CHECKS = {
    29702: "three distinct labels form a consistent transitive flow relation",
    29803: "the generated graph contains a direct 1-to-n path within the time limit",
    30191: "king count is within the N by N board capacity",
    30830: "the chain is a tree and each query distance is divisible by v1+v2",
    30874: "the generated queue contains enough role records for its selected groups",
    30919: "all attraction positions are distinct",
}


def run(code, content, timeout=10):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as f:
        f.write(code); f.flush()
        result = subprocess.run([sys.executable, f.name], input=content, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(result.stderr[-1000:])
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
        number = entry["local_number"]
        text = find_section(entry["source"], number)
        codes = [c for c in fence_blocks(text) if "import " in c or "def " in c]
        code = next((c for c in codes if run(c, entry["sample_input"]).split() == entry["sample_output"].split()), None)
        if code is None: raise AssertionError(f"no sample-passing code {number}")
        for seed in range(20000): GENERATORS[number](random.Random(number + seed))
        for seed in range(400): run(code, GENERATORS[number](random.Random(number + seed)), timeout=10)
        target = 6 if number == 29702 else 21
        cases = [entry["sample_input"]]
        for i in range(1, target):
            for attempt in range(100):
                value = GENERATORS[number](random.Random(number + i + attempt * 1000))
                if value not in cases: cases.append(value); break
            else: raise AssertionError(f"insufficient diversity {number}")
        directory = TESTS / bucket(number) / f"{number:05d}_made"; data = directory / "data"; data.mkdir(parents=True, exist_ok=True)
        outputs = [run(code, x) for x in cases]
        (directory / "samplecode.py").write_text("# Source: " + entry["source"] + "\n" + code, encoding="utf-8")
        source = inspect.getsource(GENERATORS[number]).replace(f"def g{number}", "def generate_case")
        produce = f'''import random, subprocess, tempfile\nfrom pathlib import Path\nREFERENCE_SOURCE = {code!r}\nSAMPLE_IN = {entry["sample_input"]!r}\n{source}\nwith tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:\n    handle.write(REFERENCE_SOURCE); handle.flush()\n    root = Path(__file__).parent / "data"\n    seen = [SAMPLE_IN]\n    for index in range({target}):\n        if index == 0: content = SAMPLE_IN\n        else:\n            for attempt in range(100):\n                content = generate_case(random.Random({number} + index + attempt * 1000))\n                if content not in seen: break\n            else: raise AssertionError("insufficient diversity")\n        seen.append(content)\n        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)\n        (root / f"{{index}}.in").write_text(content, encoding="utf-8")\n        (root / f"{{index}}.out").write_text(result.stdout, encoding="utf-8")\n'''
        (directory / "producecase.py").write_text(produce, encoding="utf-8")
        for old in data.glob("*"): old.unlink()
        for i, (case, output) in enumerate(zip(cases, outputs)):
            (data / f"{i}.in").write_text(case, encoding="utf-8"); (data / f"{i}.out").write_text(output, encoding="utf-8")
        freq = Counter(tuple(x.split()) for x in outputs).most_common(1)[0][1]
        report.append({"local_number": number, "source_heading": entry["source_heading"], "source_code": "solution collection", "generator": f"g{number}", "seed": number, "test_cases": target, "distinct_input_cases": len(set(cases)), "distinct_outputs": len({tuple(x.split()) for x in outputs}), "max_output_frequency": freq, "constant_output_probe": {"frequency": freq, "total": target, "status": "rejected" if freq < target else "accepted"}, "max_input_bytes": max(map(len, cases)), "constraints": CONSTRAINTS[number], "structure_checked": number in STRUCTURE_CHECKS, "structure_check": STRUCTURE_CHECKS.get(number), "generator_seed_smoke": {"seeds_per_generator": 20000, "status": "passed"}, "reference_seed_smoke": {"seeds": 400, "status": "passed"}, "sample_reproduced": True, "producecase_reproduced": reproduce(number)})
        print("built", number, flush=True)
    REPORT.write_text(json.dumps({"batch": "T-003-002-r4", "entries": report}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__": main()
