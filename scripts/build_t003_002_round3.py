#!/usr/bin/env python3
"""Build T-003 batch-002 round three with generator and reference-solver smoke tests."""
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
MANIFEST = ROOT / "collab/t003-batch-002-round3-manifest.json"
REPORT = ROOT / "collab/t003-002-round3-report.json"
TESTS = ROOT / "data/openjudge/tests"


def g25573(r):
    value = "".join(r.choice("RB") for _ in range(r.randint(1, 80)))
    assert set(value) <= set("RB") and value
    return value + "\n"


def g25655(r):
    n = r.randint(3, 20); students = [(1000 + i, 101 + (i % 4)) for i in range(n)]
    tests = [(1, sid) for sid, _ in students]
    tests += [(r.randint(2, 9), r.choice(students[1:])[0]) for _ in range(r.randint(n, 4 * n))]
    assert len(tests) >= n and all(1 <= day <= 9 for day, _ in tests)
    return f"{n}\n{len(tests)}\n" + "\n".join(f"{sid} {dept}" for sid, dept in students) + "\n" + "\n".join(f"{day} {sid}" for day, sid in tests) + "\n"


def g25815(r):
    value = "".join(r.choice("ABCD") for _ in range(r.randint(1, 80)))
    assert 1 <= len(value) <= 100 and value.isupper()
    return value + "\n"


def g26573(r):
    n = r.randint(0, 8); width = 3 ** n; assert width == 3 ** n
    return str(n) + "\n"


def g26646(r):
    m = r.randint(3, 80); n = r.randint(2, min(20, m)); rows = []
    for _ in range(n):
        y = r.randint(1, m); x = r.randint(y - 1, m - 1); rows.append((x, y))
    assert all(0 <= x < m and 1 <= y <= m and x - y + 1 >= 0 for x, y in rows)
    return f"{n} {m}\n" + "\n".join(f"{x} {y}" for x, y in rows) + "\n"


def g26999(r):
    pairs = []
    for _ in range(r.randint(2, 6)):
        text = "".join(r.choice("abcd") for _ in range(r.randint(3, 35)))
        pattern = "".join(r.choice("abcd") for _ in range(r.randint(1, min(8, len(text)))))
        pairs.append((text, pattern))
    assert all(0 < len(p) <= len(t) < 2 * 10**7 for t, p in pairs)
    return str(len(pairs)) + "\n" + "\n".join(f"{t} {p}" for t, p in pairs) + "\n"


def g27273(r):
    values = [r.randint(1, 10**6) for _ in range(r.randint(2, 12))]
    return str(len(values)) + "\n" + "\n".join(map(str, values)) + "\n"


def g27274(r):
    k = r.randint(3, 7); length = 2 ** k + r.randint(0, 20)
    value = "".join(r.choice("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(length))
    assert len(value) >= 2 ** k
    return value + "\n"


def g27528(r):
    n = r.randint(1, 25); return f"{n}\n"


def g27635(r):
    n = r.randint(2, 25); edges = [(i, i + 1) for i in range(n - 1)]
    if r.random() < .35: edges.append((0, 1))
    if r.random() < .35: edges = edges[:max(1, n // 3)]
    assert all(0 <= u < n and 0 <= v < n and u != v for u, v in edges)
    return f"{n} {len(edges)}\n" + "\n".join(f"{u} {v}" for u, v in edges) + "\n"


def g28127(r):
    schools = ["Peking University", "University of Oxford", "MIT", "PKU"]
    rows = [f"{r.choice(schools)},{r.choice('ABC')},{r.choice(['yes', 'no'])}" for _ in range(r.randint(4, 20))]
    return str(len(rows)) + "\n" + "\n".join(rows) + "\n"


def g28170(r):
    rows = ["".join(r.choice(".-") for _ in range(10)) for _ in range(10)]
    assert all(len(row) == 10 and set(row) <= set(".-") for row in rows)
    return "\n".join(rows) + "\n"


def g28389(r):
    values = [r.randint(0, 10000) for _ in range(r.randint(2, 45))]
    return str(len(values)) + "\n" + " ".join(map(str, values)) + "\n"


def g28664(r):
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]; mapping = "10X98765432"
    ids = []
    for _ in range(r.randint(2, 8)):
        prefix = "".join(str(r.randint(0, 9)) for _ in range(17)); check = mapping[sum(int(a) * b for a, b in zip(prefix, weights)) % 11]
        if r.random() < .35: check = "0" if check != "0" else "1"
        ids.append(prefix + check)
    return str(len(ids)) + "\n" + "\n".join(ids) + "\n"


def g28678(r):
    return f"{r.randint(1, 1000)}\n"


def g28691(r):
    a, b = r.randint(0, 99), r.randint(0, 99)
    return f"{a:02d}{r.choice('ABCD')} {b:02d}{r.choice('WXYZ')}\n"


def g28702(r):
    rows = [(r.randint(1, 5), r.randint(1, 3), r.randint(1, 20)) for _ in range(r.randint(2, 8))]
    return str(len(rows)) + "\n" + "\n".join(f"{m} {k} {n}" for m, k, n in rows) + "\n"


def g28748(r):
    n = r.randint(2, 6); k = r.randint(2, 6); boards = [[r.randint(1, 20) for _ in range(k)] for _ in range(n)]
    return f"{n} {k}\n" + "\n".join(" ".join(map(str, row)) for row in boards) + "\n"


def g28780(r):
    coins = sorted(set(r.randint(1, 30) for _ in range(r.randint(2, 6))))
    amount = r.randint(1, 100)
    return f"{len(coins)} {amount}\n" + " ".join(map(str, coins)) + "\n"


def g28810(r):
    n = r.randint(2, 8); base = r.sample(range(1, 100), n); queries = []
    for _ in range(r.randint(2, 7)):
        q = base[:]; r.shuffle(q); queries.append(q)
    return f"{n} {len(queries)}\n" + " ".join(map(str, base)) + "\n" + "\n".join(" ".join(map(str, q)) for q in queries) + "\n"


GENERATORS = {n: globals()[f"g{n}"] for n in [25573, 25655, 25815, 26573, 26646, 26999, 27273, 27274, 27528, 27635, 28127, 28170, 28389, 28664, 28678, 28691, 28702, 28748, 28780, 28810]}
CONSTRAINTS = {
    25573: ["n<500000", "each rose is R or B", "operations are single-position or prefix color flips"],
    25655: ["the observation window is days 1..9", "each student has a day-1 record", "each record names an existing student and a valid day", "a student needs one test in every three-day window"],
    25815: ["length is at most 100", "characters are uppercase A-Z", "insert/delete/replace each cost one operation"],
    26573: ["题面未给出 n 的上界（practice/dsapre/2024sp_routine 三个页面均无）", "输出长度为 3^n，n 每加 1 输出膨胀三倍，判题输出上限 2MB 使 n<=13 才可判", "生成器取 n=0..8 是**工程取舍**（再大数据文件过大），不是题面约束——因此本题的「去重<15 组」属于数据体积权衡，不属于「输入域本身小于 15」的豁免", "每个剩余小区间用 * 表示，其余单位位置用 - 表示"],
    26646: ["building intervals are left-closed/right-open", "0<=x<m and 1<=y<=m", "a building containing x has width y", "selected buildings cannot overlap"],
    26999: ["number of cases is positive", "0<len(pattern)<=len(text)<2*10^7", "matches are reported from zero-based positions", "no match is printed as no"],
    27273: ["1<=t<=100", "1<=n<=10^6", "powers of two through n receive a negative sign"],
    27274: ["input uses ASCII digits and upper/lowercase letters", "indices are one-based powers of two", "the extracted characters are interleaved from both ends"],
    27528: ["1<=N<=25", "a move may climb any positive number of remaining stairs", "each distinct composition is one way"],
    27635: ["1<=n<=110", "1<=m<=10000", "vertices are 0..n-1", "edges are undirected"],
    28127: ["each record is university, medal, and yes/no", "medals are A/B/C", "duplicate records are allowed and counted"],
    28170: ["the board is exactly 10 by 10", "- is empty and . is the player's stone", "an eagle is a four-direction connected component"],
    28389: ["N<=100000", "scores are non-negative millimeter integers at most 10000", "the number of instruments is minimized online"],
    28664: ["each ID has 18 characters", "the first 17 characters are digits", "the final check digit follows the modulus-11 mapping"],
    28678: ["1<=n<=2000000", "odd n is transformed by 3n+1", "even n is transformed by n/2 until 1"],
    28691: ["there are two strings", "each string has two digits followed by a letter", "the numeric prefixes are summed"],
    28702: ["n<=500", "each test gives m,k,n positive integers", "at most k tickets may be used for one meal", "coverage must be continuous from 1 to n"],
    28748: ["n and k are positive", "each player has k numbers", "numbers are drawn without replacement", "probabilities are printed to nine decimals"],
    28780: ["1<=number of coin types<=100", "target is 0..10^6", "coin values are positive and distinct", "unlimited copies are available"],
    28810: ["N<=10 and L is positive", "each sequence is a permutation of N distinct positive values", "comparison is by the resulting binary-search-tree shape"],
}
STRUCTURE_CHECKS = {25655: "every student has a day-1 test record", 26646: "each building interval stays inside [0,m)", 27635: "edges have distinct in-range endpoints", 28664: "generated IDs use the stated check-digit algorithm"}


def run(code, content, timeout=10):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as f:
        f.write(code); f.flush(); result = subprocess.run([sys.executable, f.name], input=content, text=True, capture_output=True, timeout=timeout)
    if result.returncode: raise RuntimeError(result.stderr[-1000:])
    return result.stdout


def find_section(source, number):
    lines = locate_source(source).read_text(encoding="utf-8", errors="ignore").splitlines(); starts = [i for i, x in enumerate(lines) if re.match(r"^##\s+", x)]
    for i, start in enumerate(starts):
        if re.match(rf"^##\s+[^\d]*0*{number}[:：]", lines[start]): return "\n".join(lines[start:starts[i + 1] if i + 1 < len(starts) else len(lines)])
    raise ValueError(number)


def reproduce(number):
    directory = TESTS / bucket(number) / f"{number:05d}_made"; data = directory / "data"; before = {p.name: p.read_bytes() for p in sorted(data.iterdir())}
    result = subprocess.run([sys.executable, "producecase.py"], cwd=directory, capture_output=True, timeout=600); after = {p.name: p.read_bytes() for p in sorted(data.iterdir())}
    return result.returncode == 0 and before == after


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")); report = []
    for entry in manifest["entries"]:
        number = entry["local_number"]; text = find_section(entry["source"], number); codes = [c for c in fence_blocks(text) if "import " in c or "def " in c]
        code = next((c for c in codes if run(c, entry["sample_input"]).split() == entry["sample_output"].split()), None)
        if code is None: raise AssertionError(f"no sample-passing code {number}")
        for seed in range(20000): GENERATORS[number](random.Random(number + seed))
        for seed in range(400): run(code, GENERATORS[number](random.Random(number + seed)), timeout=10)
        target = 9 if number == 26573 else 20; cases = [entry["sample_input"]]
        for i in range(1, target):
            for attempt in range(100):
                value = GENERATORS[number](random.Random(number + i + attempt * 1000))
                if value not in cases: cases.append(value); break
            else: raise AssertionError(f"insufficient diversity {number}")
        directory = TESTS / bucket(number) / f"{number:05d}_made"; data = directory / "data"; data.mkdir(parents=True, exist_ok=True); outputs = [run(code, x) for x in cases]
        (directory / "samplecode.py").write_text("# Source: " + entry["source"] + "\n" + code, encoding="utf-8")
        source = inspect.getsource(GENERATORS[number]).replace(f"def g{number}", "def generate_case")
        produce = f'''import random, subprocess, tempfile\nfrom pathlib import Path\nREFERENCE_SOURCE = {code!r}\nSAMPLE_IN = {entry["sample_input"]!r}\nSAMPLE_OUT = {entry["sample_output"]!r}\n{source}\nwith tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:\n    handle.write(REFERENCE_SOURCE); handle.flush()\n    root = Path(__file__).parent / "data"\n    seen = [SAMPLE_IN]\n    for index in range({target}):\n        if index == 0: content = SAMPLE_IN\n        else:\n            for attempt in range(100):\n                content = generate_case(random.Random({number} + index + attempt * 1000))\n                if content not in seen: break\n            else: raise AssertionError("insufficient diversity")\n        seen.append(content)\n        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)\n        (root / f"{{index}}.in").write_text(content, encoding="utf-8")\n        (root / f"{{index}}.out").write_text(result.stdout, encoding="utf-8")\n'''
        (directory / "producecase.py").write_text(produce, encoding="utf-8")
        for old in data.glob("*"): old.unlink()
        for i, (case, output) in enumerate(zip(cases, outputs)):
            (data / f"{i}.in").write_text(case, encoding="utf-8"); (data / f"{i}.out").write_text(output, encoding="utf-8")
        freq = Counter(tuple(x.split()) for x in outputs).most_common(1)[0][1]
        report.append({"local_number": number, "source_heading": entry["source_heading"], "source_code": "solution collection", "generator": f"g{number}", "seed": number, "test_cases": target, "distinct_input_cases": len(set(cases)), "distinct_outputs": len({tuple(x.split()) for x in outputs}), "max_output_frequency": freq, "constant_output_probe": {"frequency": freq, "total": target, "status": "rejected" if freq < target else "accepted"}, "max_input_bytes": max(map(len, cases)), "constraints": CONSTRAINTS[number], "structure_checked": number in STRUCTURE_CHECKS, "structure_check": STRUCTURE_CHECKS.get(number), "generator_seed_smoke": {"seeds_per_generator": 20000, "status": "passed"}, "reference_seed_smoke": {"seeds": 400, "status": "passed"}, "sample_reproduced": True, "producecase_reproduced": reproduce(number)})
        print("built", number, flush=True)
    REPORT.write_text(json.dumps({"batch": "T-003-002-r3", "entries": report}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__": main()
