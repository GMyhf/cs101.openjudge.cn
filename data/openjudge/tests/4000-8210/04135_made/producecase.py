"""4135 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4135
SAMPLE_IN = '7 5\n100\n400\n300\n100\n500\n101\n400\n'
SAMPLE_OUT = '500\n'
REFERENCE_SOURCE = 'def minMaxMonthlyExpense(N, M, expenses):\n    def can_split(max_expense):\n        """ 判断是否能合并至多 M 个花费，使最大花费不超过 max_expense """\n        months = 1  # 记录当前使用的月份数\n        current_sum = 0 # 当前月的开销\n        for cost in expenses:\n            if current_sum + cost > max_expense:\n                months += 1\n                if months > M:\n                    return False\n                current_sum = cost\n            else:\n                current_sum += cost\n        return True\n\n    # 可能的最小开销范围。所以二分是在 [left, right) 区间内进行的\n    left, right = max(expenses), sum(expenses) + 1\n    ans = -1\n    while left < right: # 二分查找最小的 "最大月度开销"\n        mid = (left + right) // 2\n        if can_split(mid):\n            ans = mid   # 记录可行的 `mid`\n            right = mid # 继续尝试更小的值\n        else:\n            left = mid + 1\n    return ans\n\n# 读取输入\nN, M = map(int, input().split())\nexpenses = [int(input()) for _ in range(N)]\n\n# 计算并输出答案\nprint(minMaxMonthlyExpense(N, M, expenses))\n'

def g4135(r):
    n = r.randint(5, 100); months = r.randint(1, n)
    values = [r.randint(1, 10000) for _ in range(n)]
    return f"{n} {months}\n" + "\n".join(map(str, values)) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4135(random.Random(NUMBER + i)) for i in range(1, 20)]

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
