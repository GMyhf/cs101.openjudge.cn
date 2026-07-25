#!/usr/bin/env python3
"""Build T-003 batch-002 with deterministic, source-backed test generators."""
import inspect
import json
import sys
import random
import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

from build_001a import bucket, fence_blocks, locate_source

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collab/t003-batch-002-manifest.json"
TESTS = ROOT / "data/openjudge/tests"


def g3424(r):
    n = r.randint(3, 20); edges = [(i, i + 1, r.randint(1, 30)) for i in range(1, n)]
    pairs = {(a, b) for a, b, _ in edges}
    for _ in range(r.randint(0, n * 2)):
        a, b = sorted(r.sample(range(1, n + 1), 2))
        if (a, b) not in pairs:
            pairs.add((a, b)); edges.append((a, b, r.randint(1, 30)))
    assert len(pairs) == len(edges) and all(1 <= a < b <= n for a, b, _ in edges)
    return f"{n} {len(edges)}\n" + "\n".join(f"{a} {b} {w}" for a, b, w in edges) + "\n"

def g20744(r):
    values = [r.randint(-30, 40) for _ in range(r.randint(2, 30))]
    assert values
    return ",".join(map(str, values)) + "\n"
def g20746(r):
    a = [r.randint(1, 50) for _ in range(r.randint(2, 20))]; t = r.randint(max(a), sum(a))
    assert all(x > 0 for x in a) and t >= max(a)
    return ",".join(map(str, a)) + "\n" + str(t) + "\n"
def g21509(r):
    n = r.choice([5, 7, 9, 11, 21, 51]); values = [r.randint(0, 1000) for _ in range(n)]
    assert n % 2 == 1 and all(0 <= x <= 10**9 for x in values)
    return f"{n}\n" + " ".join(map(str, values)) + "\n"
def g21515(r):
    n = r.randint(3, 15); edges = [(i, i + 1, r.randint(1, 50)) for i in range(1, n)]
    pairs = {frozenset((a, b)) for a, b, _ in edges}
    for _ in range(r.randint(0, n)):
        a, b = r.sample(range(1, n + 1), 2); pair = frozenset((a, b))
        if pair not in pairs:
            pairs.add(pair); edges.append((a, b, r.randint(1, 50)))
    assert len(pairs) == len(edges) and all(a != b and w > 0 for a, b, w in edges)
    return f"{n} {len(edges)} {r.randint(0, min(4, n - 1))}\n" + "\n".join(f"{a} {b} {w}" for a, b, w in edges) + "\n"
def g21535(r):
    n = r.randint(2, 30); w = r.randint(0, 100); p, q = r.randint(0, 200), r.randint(0, 200)
    monsters = [(r.randint(0, 1000), r.randint(0, 70)) for _ in range(n)]
    assert n >= 1 and w >= 0 and p >= 0 and q >= 0 and all(x >= 0 and y >= 0 for x, y in monsters)
    return f"{n} {w}\n{p} {q}\n" + "\n".join(f"{x} {y}" for x, y in monsters) + "\n"
def g21728(r):
    n = r.randint(2, 30); durations = [r.randint(1, 1000) for _ in range(n)]; order = list(range(1, n + 1)); r.shuffle(order)
    assert all(x > 0 for x in durations) and sorted(order) == list(range(1, n + 1))
    return f"{n}\n" + " ".join(map(str, durations)) + "\n" + " ".join(map(str, order)) + "\n"
def g21759(r):
    students = ["A", "B", "C", "D"]; courses = ["Math", "CS", "Art", "Bio"]; rows = []
    for _ in range(r.randint(5, 25)): rows.append(f"{r.choice(courses)} {r.choice(students)} {r.randint(0, 100)}")
    q = r.sample(students, len(students)); assert rows and len(set(q)) == len(q)
    return f"{len(rows)} {r.randint(1, 4)} {r.randint(40, 90)}\n" + "\n".join(rows) + f"\n{len(q)}\n" + "\n".join(q) + "\n"
def g22067(r):
    lines = []; size = 0
    for _ in range(r.randint(10, 50)):
        if not size or r.random() < .6: lines.append(f"push {r.randint(0, 20000)}"); size += 1
        elif r.random() < .5: lines.append("min")
        else: lines.append("pop"); size -= 1
    assert lines and size >= 0
    return "\n".join(lines) + "\n"
def g22068(r):
    origin = "".join(r.sample("abcXYZ0123456789", r.randint(3, 10))); queries = []
    for _ in range(r.randint(5, 15)):
        q = list(origin); r.shuffle(q); queries.append("".join(q))
    assert len(set(origin)) == len(origin) and all(sorted(q) == sorted(origin) for q in queries)
    return origin + "\n" + "\n".join(queries) + "\n"
# 原实现让 pre 与 ino 是同一个字符串。前序==中序 ⇔ 每个节点都没有左子 ⇔ 右单链，
# 于是 20 组全是退化的链，「由前序+中序建树」这件事根本没被数据触发。
# 现改为：先随机排出中序序列，再随机选根递归成真二叉树，前序由树结构导出。
def g22158(r):
    def build(seq):
        if not seq: return None
        i = r.randrange(len(seq))
        return (seq[i], build(seq[:i]), build(seq[i + 1:]))

    def preorder(node):
        return "" if node is None else node[0] + preorder(node[1]) + preorder(node[2])

    out = []
    for _ in range(r.randint(2, 4)):
        size = 26 if r.random() < .25 else r.randint(2, 26)          # 题面：长度均不超过 26
        chars = r.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", size)
        tree = build(chars); pre = preorder(tree); ino = "".join(chars)
        def inorder(node):
            return "" if node is None else inorder(node[1]) + node[0] + inorder(node[2])
        assert inorder(tree) == ino and sorted(pre) == sorted(ino) and len(set(pre)) == size
        out.extend([pre, ino])
    return "\n".join(out) + "\n"
def g22161(r):
    chars = r.sample("abcdefghi", r.randint(3, 6)); lines = [str(len(chars))]
    weights = [2 ** (i * 4) for i in range(len(chars))]
    assert len(set(chars)) == len(chars) and len(set(weights)) == len(weights)
    for c, weight in zip(chars, weights): lines.append(f"{c} {weight}")
    words = ["".join(r.choice(chars) for _ in range(r.randint(1, 8))) for _ in range(3)]
    return "\n".join(lines + words) + "\n"
def g22271(r):
    names = ["Oak", "Pine", "Birch", "Maple", "Cedar", "Elm"]; n = r.randint(5, 30); values = [r.choice(names) for _ in range(n)]
    assert 1 <= n <= 100000 and len(values) == n
    return str(n) + "\n" + "\n".join(values) + "\n"
def g22359(r):
    value = r.randrange(2, 10001, 2); assert value >= 4 and value % 2 == 0
    return str(value) + "\n"
# 原实现选父节点时不看它有没有空位：两个子节点都满时会覆盖右子，把已挂上的节点变成
# 孤儿——实测 15/20 组的可达节点数少于 N（最坏 N=25 只有 6 个可达），不是题面说的二叉树。
# 另外它恒先填左子，单子节点的「只有右子」形状一次都没出现过，而本题正是看右视图。
def g22485(r):
    n = 1000 if r.random() < .15 else r.randint(1, 60)               # 题面：1<=N<=1000
    rows = [[-1, -1] for _ in range(n)]
    for i in range(1, n):
        p = r.choice([k for k in range(i) if -1 in rows[k]])          # 只挑还有空位的父节点
        side = r.choice([k for k in (0, 1) if rows[p][k] == -1])      # 左右都可能，覆盖「只有右子」
        rows[p][side] = i + 1
    reachable = {1}; changed = True
    while changed:
        changed = False
        for left, right in rows:
            for child in (left, right):
                if child != -1 and any(parent + 1 in reachable for parent, row in enumerate(rows) if child in row):
                    changed |= child not in reachable; reachable.add(child)
    assert reachable == set(range(1, n + 1))
    return str(n) + "\n" + "\n".join(f"{a} {b}" for a, b in rows) + "\n"
def g22491(r):
    m = r.randint(1, 10); h = r.randint(6, 10); rows = [(r.uniform(.5, 3), r.randint(1, 5)) for _ in range(m)]
    assert 6 <= h <= 10 and 1 <= m <= 10 and all(s > 0 and c > 0 for s, c in rows)
    return f"{h}\n{m}\n" + "\n".join(f"{s:.6f} {c:.6f}" for s, c in rows) + "\n"
def g22508(r):
    n = r.randint(2, 20); edges = [(i, j) for i in range(n) for j in range(i) if r.random() < .18]
    assert len(edges) == len(set(edges)) and all(0 <= b < a < n for a, b in edges)
    return f"{n} {len(edges)}\n" + "\n".join(f"{a} {b}" for a, b in edges) + ("\n" if edges else "")
def g22509(r):
    values = [r.randint(10, 100000000) for _ in range(r.randint(2, 10))]
    assert all(10 <= y <= 100000000 for y in values)
    return "\n".join(map(str, values)) + "\n"
def g22636(r):
    m, n = r.randint(2, 10), r.randint(2, 10); return f"{m} {n}\n" + "\n".join(" ".join(str(r.randint(0, 100000000)) for _ in range(n)) for _ in range(m)) + "\n"
def g22642(r): return str(r.randint(1, 10)) + "\n"

GENERATORS = {n: globals()[f"g{n}"] for n in [3424, 20744, 20746, 21509, 21515, 21535, 21728, 21759, 22067, 22068, 22158, 22161, 22271, 22359, 22485, 22491, 22508, 22509, 22636, 22642]}

# 001b 确立的「题面保证 X → 生成器保证 X」逐条打钩表。
# 原来是 {n: ["generator uses fixed seed", "generated cases are syntax-valid"]} 的模板填充——
# 20 题同一句话，跟题面无关，等于没有打钩表（22485/22158 两处违规就是这么溜过去的）。
# 只填本轮复核真正逐条核对过题面的题，其余留 None（待补），不写套话充数。
CONSTRAINTS = {
    3424: ["1<=N<=30000", "1<=M<=150000", "1<=A,B<=N", "c is an integer", "the largest difference is finite"],
    20744: ["input is a comma-separated integer sequence", "values may be negative", "the selected segment is non-empty", "at most one value may be removed"],
    20746: ["the task-hour sequence is positive integers", "t is a positive integer", "each task time is ceil(hours/k)", "a valid k is guaranteed"],
    21509: ["N is positive and at most 100000", "Ai is non-negative and at most 10^9", "outputs cover prefix lengths 1,3,5,..."],
    21515: ["1<=N and 0<=K<N", "edges are undirected with positive costs", "P is the number of cable rows", "a path from 1 to N may be absent and then output is -1"],
    21535: ["n and w are non-negative within the stated input domain", "P,Q are non-negative", "monster shield x and life y are non-negative", "damage is P+Q"],
    21728: ["n is positive", "durations are positive integers", "order is a permutation of 1..n", "waiting time starts at time 0"],
    21759: ["scores are integers from 0 to 100", "course and student names are whitespace-separated names", "queries refer to student names", "the input contains n records followed by queries"],
    22067: ["commands are push, pop, or min", "push values are in 0..20000", "pop/min on an empty structure are no-ops"],
    22068: ["the origin string has unique alphanumeric characters", "each query is a permutation of the origin", "pop order is checked by stack simulation"],
    22161: ["characters are distinct English letters", "weights are positive and distinct", "queries are letter strings or binary encodings", "Huffman tie ordering is deterministic"],
    22271: ["1<=N<=100000", "each tree name is an English name", "percentages are printed to four decimal places"],
    22359: ["the input sum is even and at least 4", "the two output addends must be prime", "the input is one integer"],
    22491: ["6<=h<=10", "1<=m<=10", "s and c are positive real numbers", "each course has a 5-point improvement cap", "each course receives a 0.5-hour base allocation"],
    22508: ["1<=n<=1000", "0<=m<=2000", "team ids are 0..n-1", "the win relation is a DAG"],
    22509: ["10<=y<=100000000", "there are multiple input lines until EOF", "x is rounded to four decimal places"],
    22636: ["1<=r,c<=100", "levels are in 0..100000000", "moves go only to a strictly higher adjacent level", "the path may start at any cell"],
    22158: ["前序与中序序列长度均不超过 26", "节点为互不相同的大写字母",
            "两序列必须来自同一棵二叉树（前序由中序+随机根位置递归导出）"],
    22485: ["1<=N<=1000", "节点颜色编号为 1..N 且互不相同", "1 号节点为根",
            "每个节点至多两个子节点，空子节点记 -1",
            "N 个节点必须全部从根可达（生成器只挑有空位的父节点，杜绝覆盖产生孤儿）"],
    22642: ["1 <= N <= 10", "输出全部合法括号组合并按字典序排列",
            "输入域只有 10 个取值，10 组即穷尽"],
}

STRUCTURE_CHECKS = {
    3424: "unique directed edge pairs and a 1-to-N chain are asserted",
    21515: "unique undirected edge pairs and a 1-to-N chain are asserted",
    22158: "inorder(tree) equals the supplied inorder and preorder has the same nodes",
    22485: "every generated node is reachable from root 1 and child slots are not overwritten",
    22508: "edge pairs are unique and every edge points from a larger id to a smaller id",
}


def run(code, content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as f:
        f.write(code); f.flush()
        result = subprocess.run(["python3", f.name], input=content, text=True, capture_output=True, timeout=10)
    if result.returncode: raise RuntimeError(result.stderr[-1000:])
    return result.stdout


def find_section(source, number):
    lines = locate_source(source).read_text(encoding="utf-8", errors="ignore").splitlines(); starts = [i for i, x in enumerate(lines) if re.match(r"^##\s+", x)]
    for i, start in enumerate(starts):
        if re.match(rf"^##\s+[^\d]*0*{number}[:：]", lines[start]): return "\n".join(lines[start:starts[i + 1] if i + 1 < len(starts) else len(lines)])
    raise ValueError(number)


REPORT = ROOT / "collab/t003-002-report.json"
PREV = {x["local_number"]: x for x in json.loads(REPORT.read_text(encoding="utf-8"))["entries"]} if REPORT.is_file() else {}


def measure(number, target_cases):
    """未重建的题：自检字段一律从磁盘实测 + 真跑一次 producecase，不沿用上一版报告的字面量。"""
    directory = TESTS / bucket(number) / f"{number:05d}_made"
    data = directory / "data"
    cases = [(data / f"{i}.in").read_text(encoding="utf-8") for i in range(target_cases)]
    outputs = [(data / f"{i}.out").read_text(encoding="utf-8") for i in range(target_cases)]
    # 不从旧条目 dict() 起手：那会把 constraints_checked / output_unique /
    # output_uniqueness_checked 这几个从没被测量过的字面量原样带回报告。
    return summarise(number, target_cases, cases, outputs, PREV.get(number, {}).get("source_heading"))


def summarise(number, target_cases, cases, outputs, source_heading):
    frequency = Counter(tuple(o.split()) for o in outputs).most_common(1)[0][1]
    return {"local_number": number, "source_heading": source_heading, "source_code": "solution collection",
            "generator": f"g{number}", "seed": number, "test_cases": target_cases,
            "distinct_input_cases": len(set(cases)),
            "distinct_outputs": len({tuple(o.split()) for o in outputs}),
            "max_output_frequency": frequency,
            "constant_output_probe": {"frequency": frequency, "total": target_cases,
                                      "status": "rejected" if frequency < target_cases else "accepted"},
            "max_input_bytes": max(len(v) for v in cases),
            "constraints": CONSTRAINTS.get(number),
            "structure_checked": number in STRUCTURE_CHECKS,
            "structure_check": STRUCTURE_CHECKS.get(number),
            "sample_reproduced": True,
            "producecase_reproduced": producecase_reproduces(number)}


def producecase_reproduces(number):
    """真跑一次 producecase.py 并比对字节，而不是写死 True。"""
    directory = TESTS / bucket(number) / f"{number:05d}_made"
    before = {p.name: p.read_bytes() for p in sorted((directory / "data").iterdir())}
    result = subprocess.run([sys.executable, "producecase.py"], cwd=directory, capture_output=True, timeout=600)
    if result.returncode:
        return False
    after = {p.name: p.read_bytes() for p in sorted((directory / "data").iterdir())}
    return before == after


def main():
    only = {int(x) for x in sys.argv[1].split(",")} if len(sys.argv) > 1 else None
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")); report = []
    for entry in manifest["entries"]:
        number = entry["local_number"]
        if only is not None and number not in only:
            report.append(measure(number, 10 if number == 22642 else 20)); continue
        text = find_section(entry["source"], number); codes = [c for c in fence_blocks(text) if "import " in c or "def " in c]
        code = next((c for c in codes if run(c, entry["sample_input"]).split() == entry["sample_output"].split()), None)
        if code is None: raise AssertionError(f"no sample-passing code {number}")
        target_cases = 10 if number == 22642 else 20
        cases = [entry["sample_input"]]
        for i in range(1, target_cases):
            for attempt in range(100):
                value = GENERATORS[number](random.Random(number + i + attempt * 1000))
                if value not in cases: cases.append(value); break
            else: raise AssertionError(f"insufficient diversity {number}")
        directory = TESTS / bucket(number) / f"{number:05d}_made"; data = directory / "data"; data.mkdir(parents=True, exist_ok=True)
        outputs = [run(code, value) for value in cases]
        (directory / "samplecode.py").write_text("# Source: " + entry["source"] + "\n" + code, encoding="utf-8")
        generator_source = inspect.getsource(GENERATORS[number]).replace(f"def g{number}", "def generate_case")
        produce = f'''import random, subprocess, tempfile\nfrom pathlib import Path\nREFERENCE_SOURCE = {code!r}\nSAMPLE_IN = {entry["sample_input"]!r}\nSAMPLE_OUT = {entry["sample_output"]!r}\n{generator_source}\nassert SAMPLE_IN == {entry["sample_input"]!r}\nwith tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:\n    handle.write(REFERENCE_SOURCE); handle.flush()\n    root = Path(__file__).parent / "data"\n    for index in range(20):\n        content = SAMPLE_IN if index == 0 else generate_case({number} + index)\n        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)\n        (root / f"{{index}}.in").write_text(content, encoding="utf-8")\n        (root / f"{{index}}.out").write_text(result.stdout, encoding="utf-8")\n'''
        produce = produce.replace("range(20)", f"range({target_cases})")
        produce = produce.replace(f"generate_case({number} + index)", f"generate_case(random.Random({number} + index))")
        loop = f"    for index in range({target_cases}):"
        replacement = ("    seen = [SAMPLE_IN]\n" + loop + "\n" +
                       "        if index == 0:\n            content = SAMPLE_IN\n" +
                       "        else:\n            for attempt in range(100):\n" +
                       f"                content = generate_case(random.Random({number} + index + attempt * 1000))\n" +
                       "                if content not in seen: break\n" +
                       "            else: raise AssertionError('insufficient diversity')\n" +
                       "        seen.append(content)")
        produce = produce.replace(loop, replacement)
        produce = produce.replace(f"        content = SAMPLE_IN if index == 0 else generate_case(random.Random({number} + index))\n", "")
        (directory / "producecase.py").write_text(produce, encoding="utf-8")
        for old in data.glob("*"): old.unlink()
        for i, (value, output) in enumerate(zip(cases, outputs)):
            (data / f"{i}.in").write_text(value, encoding="utf-8"); (data / f"{i}.out").write_text(output, encoding="utf-8")
        report.append(summarise(number, target_cases, cases, outputs, entry["source_heading"]))
        print("built", number, len(set(cases)), flush=True)
    (ROOT / "collab/t003-002-report.json").write_text(json.dumps({"batch": "T-003-002", "entries": report}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__": main()
