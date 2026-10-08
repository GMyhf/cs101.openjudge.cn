"""5333 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 5333
SAMPLE_IN = '3\n8\n5\n8\n'
SAMPLE_OUT = '34\n'
REFERENCE_SOURCE = 'import heapq\n\ndef minimum_cost(planks):\n    heapq.heapify(planks)  # 将木板列表转换为最小堆\n    total_cost = 0\n\n    while len(planks) > 1:\n        # 取出最短的两块木板\n        shortest1 = heapq.heappop(planks)\n        shortest2 = heapq.heappop(planks)\n\n        # 计算切割的成本，并将切割后得到的木板长度加入堆\n        cost = shortest1 + shortest2\n        total_cost += cost\n        heapq.heappush(planks, cost)\n\n    return total_cost\n\n# 读取输入\nn = int(input())\nplanks = []\nfor _ in range(n):\n    length = int(input())\n    planks.append(length)\n\n# 调用函数计算最小成本\nresult = minimum_cost(planks)\n\n# 输出结果\nprint(result)\n'

def valid(text):
    """题面契约：第 1 行 N（1<=N<=20000）；第 2..N+1 行各一个整数 Li（1<=Li<=50000）。"""
    lines = text.split("\n")
    while lines and lines[-1].strip() == "":
        lines.pop()
    try:
        h = lines[0].split()
        if len(h) != 1:
            return False
        n = int(h[0])
        if not 1 <= n <= 20000 or len(lines) != n + 1:
            return False
        for ln in lines[1:]:
            t = ln.split()
            if len(t) != 1 or not 1 <= int(t[0]) <= 50000:
                return False
    except (ValueError, IndexError):
        return False
    return True


def g5333(r, plan):
    n, kind = plan
    if isinstance(n, tuple):
        n = r.randint(*n)
    if kind == "max":
        values = [50000] * n
    elif kind == "one":
        values = [1] * n
    elif kind == "sorted":
        values = sorted(r.randint(1, 50000) for _ in range(n))
    elif kind == "rsorted":
        values = sorted((r.randint(1, 50000) for _ in range(n)), reverse=True)
    elif kind == "skew":      # 少数很长 + 大量很短
        values = [r.randint(1, 10) for _ in range(n)]
        for i in r.sample(range(n), max(1, n // 50)):
            values[i] = r.randint(40000, 50000)
    elif kind == "pow":       # 斐波那契式长度，合并树极不平衡
        a, b = 1, 1; values = []
        while len(values) < n:
            values.append(a); a, b = b, a + b
            if a > 50000:
                a, b = 1, 1
        r.shuffle(values)
    elif kind == "high":
        values = [r.randint(45000, 50000) for _ in range(n)]
    else:
        values = [r.randint(1, 50000) for _ in range(n)]
    return str(n) + "\n" + "\n".join(map(str, values)) + "\n"


PLAN = [
    (1, "rand"), (1, "max"), (2, "rand"), (2, "one"), ((3, 8), "rand"), ((3, 8), "pow"),
    ((10, 100), "rand"), ((10, 100), "skew"), ((100, 2000), "rand"), ((100, 2000), "sorted"),
    ((2000, 10000), "rsorted"), ((2000, 10000), "pow"), (20000, "rand"), (20000, "max"),
    (20000, "one"), (20000, "high"), (20000, "skew"), (20000, "sorted"), (19999, "rand"),
]


def build_cases():
    return [SAMPLE_IN] + [g5333(random.Random(NUMBER + i), PLAN[i - 1]) for i in range(1, 20)]


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
    assert all(valid(c) for c in cases)
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
