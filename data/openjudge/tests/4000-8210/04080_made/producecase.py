"""4080 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4080
SAMPLE_IN = '4\n1 1 3 5\n'
SAMPLE_OUT = '17\n'
REFERENCE_SOURCE = 'import heapq\n\ndef min_weighted_path_length(n, weights):\n    heapq.heapify(weights)\n    total = 0\n    while len(weights) > 1:\n        a = heapq.heappop(weights)\n        b = heapq.heappop(weights)\n        combined = a + b\n        total += combined\n        heapq.heappush(weights, combined)\n    return total\n\n# 读取输入\nn = int(input())\nweights = list(map(int, input().split()))\nprint(min_weighted_path_length(n, weights))\n'

def g4080(r):
    n = r.randint(2, 100)          # 题面：2<=N<=100
    return f"{n}\n" + " ".join(str(r.randint(1, 1000)) for _ in range(n)) + "\n"

def valid(text):
    """题面契约：第一行 n（2<=N<=100），第二行 n 个整数权值。"""
    lines = text.split("\n")
    if not text.endswith("\n") or lines[-1] != "":
        return False
    lines = lines[:-1]
    if len(lines) != 2:
        return False
    try:
        head = lines[0].split()
        if len(head) != 1:
            return False
        n = int(head[0])
        ws = [int(t) for t in lines[1].split()]
    except ValueError:
        return False
    return 2 <= n <= 100 and len(ws) == n


def _fmt(ws):
    return f"{len(ws)}\n" + " ".join(map(str, ws)) + "\n"


def extra_cases():
    """补边界：n=2/3 最小规模、n=100 满规模、全等权、大量重复、逆序。"""
    r = random.Random(NUMBER * 7 + 1)
    return [
        _fmt([7, 3]),
        _fmt([5, 5]),
        _fmt([1, 2, 3]),
        _fmt([1] * 100),
        _fmt([1000] * 100),
        _fmt([r.randint(1, 1000) for _ in range(100)]),
        _fmt(sorted((r.randint(1, 1000) for _ in range(100)), reverse=True)),
        _fmt([r.randint(1, 10) for _ in range(100)]),
        _fmt([2 ** (i % 10) for i in range(100)]),
        _fmt([r.randint(1, 1000) for _ in range(99)]),
    ]


def build_cases():
    return [SAMPLE_IN] + [g4080(random.Random(NUMBER + i)) for i in range(1, 20)] + extra_cases()

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
