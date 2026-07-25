"""4144 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4144
SAMPLE_IN = '5\n1 10\n2 4\n3 6\n5 8\n4 7\n'
SAMPLE_OUT = '4\n1\n2\n3\n2\n4\n'
REFERENCE_SOURCE = '# 时间调度问题\n# cows元素：（start, end, index，）\nimport heapq\nmax_num = 1\nn = int(input())\ncows = []\nnumber = [0]*n  # 记录每一只牛所在的畜栏\nfor i in range(n):\n    cows.append(list(map(int, input().split())))\nfor i in range(n):\n    cows[i].append(i)  # 为每只牛添加编号后再排序\n\ncows.sort(key=lambda x: x[0]) # 先按开始时间排序\ncolumn = []  # 创建列表【畜栏】\nheapq.heappush(column, [cows[0][1], 0]) # 初始时只有一个元素，即为第一只牛的结束时间\nnumber[cows[0][2]] = 1  # 第一只牛默认在第一个畜栏\n\nfor i in range(1, len(cows)):  # 对之后的每只牛遍历\n    k = heapq.heappop(column)\n    if k[0] < cows[i][0]: # 最早结束的已经结束，新的牛可使用该畜栏\n        heapq.heappush(column, [cows[i][1], k[1]])\n        number[cows[i][2]] = k[1]+1\n    else:\n        heapq.heappush(column, k)\n        heapq.heappush(column, [cows[i][1], max_num])\n        max_num += 1\n        number[cows[i][2]] = max_num\n\nprint(len(column))  # 【畜栏】的长度即为畜栏数量\nfor i in number:\n    print(i)\n'

def g4144(r):
    n = r.randint(5, 100)
    intervals = []
    for _ in range(n):
        a = r.randint(1, 1_000_000); b = r.randint(a, min(1_000_000, a + 50_000))
        intervals.append(f"{a} {b}")
    return str(n) + "\n" + "\n".join(intervals) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4144(random.Random(NUMBER + i)) for i in range(1, 20)]

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
