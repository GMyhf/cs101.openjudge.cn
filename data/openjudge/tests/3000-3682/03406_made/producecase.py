"""3406 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 3406
SAMPLE_IN = '6 40\n6\n18\n11\n13\n19\n11\n'
SAMPLE_OUT = '3\n'
REFERENCE_SOURCE = '# 蒋子轩23工学院\ndef min_cows_to_reach(N, B):\n\t# 二分查找变形，找大于等于B的最小索引\n    left, right = 1, N\n    while left < right:  #注意不能取等\n        mid = (left + right) // 2 #左偏\n        if prefix_sum[mid]>=B:  #等于时继续向左找\n            right = mid   #注意不-1，\n        else:\n            left = mid + 1\n    return left  #return不取等的那个\nN, B = map(int, input().split())\ncows = [int(input()) for _ in range(N)]\n#优先选择高的\ncows.sort(reverse=True)\n#计算前缀和\nprefix_sum = [0] * (len(cows) + 1)\nfor i in range(1, len(cows)+1):\n    prefix_sum[i] = prefix_sum[i-1] + cows[i-1]\nprint(min_cows_to_reach(N, B))\n'

def g3406(r):
    n = r.randint(1, 30); heights = [r.randint(1, 100) for _ in range(n)]
    return f"{n} {r.randint(max(1, n), sum(heights))}\n" + "\n".join(map(str, heights)) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g3406(random.Random(NUMBER + i)) for i in range(1, 20)]

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
