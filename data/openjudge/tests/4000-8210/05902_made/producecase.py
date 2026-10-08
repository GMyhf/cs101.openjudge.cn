"""5902 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 40 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 5902
SAMPLE_IN = '2\n5\n1 2\n1 3\n1 4\n2 0\n2 1\n6\n1 1\n1 2\n1 3\n2 0\n2 1\n2 0\n'
SAMPLE_OUT = '3\nNULL\n'
REFERENCE_SOURCE = "from collections import deque\n\nfor _ in range(int(input())):\n    n=int(input())\n    q=deque([])\n    for i in range(n):\n        a,b=map(int,input().split())\n        if a==1:\n            q.append(b)\n        else:\n            if b==0:\n                q.popleft()\n            else:\n                q.pop()\n    if q:\n        print(*q)\n    else:\n        print('NULL')\n"

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

# 题面：第一行 t；每组第一行 n（n <= 1000），随后 n 行操作 "1 x"（x 为整数）或 "2 c"（c 为 0/1）。
# 题面未说空队出队怎么办，这里按隐含保证：出队时队列非空。
def valid(text):
    if not text.endswith("\n") or "\r" in text:
        return False
    lines = text[:-1].split("\n")
    def num(t):
        return t.isdigit() and (t == "0" or t[0] != "0")
    def sint(t):
        return num(t[1:]) if t[:1] == "-" and t != "-0" else num(t)
    if not num(lines[0]) or int(lines[0]) < 1:
        return False
    t = int(lines[0]); i = 1
    for _ in range(t):
        if i >= len(lines) or not num(lines[i]):
            return False
        n = int(lines[i]); i += 1
        if not 1 <= n <= 1000 or i + n > len(lines):
            return False
        size = 0
        for ln in lines[i:i + n]:
            toks = ln.split(" ")
            if len(toks) != 2:
                return False
            if toks[0] == "1" and sint(toks[1]):
                size += 1
            elif toks[0] == "2" and toks[1] in ("0", "1"):
                if size == 0:
                    return False
                size -= 1
            else:
                return False
        i += n
    return i == len(lines)


def ops_group(r, n, push_p, end_empty=False, xr=1000):
    ops = []; size = 0
    for k in range(n):
        left = n - k
        if end_empty and size >= left:
            ops.append(f"2 {r.randint(0, 1)}"); size -= 1
        elif not size or r.random() < push_p:
            ops.append(f"1 {r.randint(-xr, xr)}"); size += 1
        else:
            ops.append(f"2 {r.randint(0, 1)}"); size -= 1
    if end_empty and size:
        return ops_group(r, n, push_p, end_empty, xr)
    return str(n) + "\n" + "\n".join(ops)


def g5902_hard(r, kind):
    groups = []
    if kind == "min":
        groups = [ops_group(r, 1, 1)]
    elif kind == "max1":
        groups = [ops_group(r, 1000, 0.55, xr=10**9)]
    elif kind == "empty":
        groups = [ops_group(r, r.choice([2, 4, 1000, 1000, 998]), 0.5, end_empty=True) for _ in range(5)]
    elif kind == "many":
        for _ in range(r.randint(50, 100)):
            n = r.choice([1, 2, 3, r.randint(1, 1000), 1000])
            groups.append(ops_group(r, n, r.choice([0.5, 0.55, 0.7, 1.0]),
                                    end_empty=(n % 2 == 0 and r.random() < 0.3), xr=r.choice([9, 1000, 10**9])))
    else:
        for _ in range(r.randint(3, 10)):
            n = r.randint(1, 1000)
            groups.append(ops_group(r, n, r.choice([0.5, 0.6, 0.8]), xr=r.choice([9, 1000])))
    return str(len(groups)) + "\n" + "\n".join(groups) + "\n"


def build_cases():
    kinds = ["min", "max1", "max1", "empty", "many", "many", "many"] + ["mix"] * 13
    return build_cases_base() + [g5902_hard(random.Random(NUMBER * 100 + i), k) for i, k in enumerate(kinds)]


def build_cases_base():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g5902(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    return cases

def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
