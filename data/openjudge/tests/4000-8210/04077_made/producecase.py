"""4077 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4077
SAMPLE_IN = '3\n'
SAMPLE_OUT = '5\n'
REFERENCE_SOURCE = 'def count_sequences(n):\n    def dfs(push_num, stack, popped):\n        nonlocal count\n        # 如果已经弹出了 n 个数，说明这个出栈序列是合法的\n        if popped == n:\n            count += 1\n            return\n        # 尝试进栈：如果还有数字没进栈\n        if push_num <= n:\n            stack.append(push_num)\n            dfs(push_num + 1, stack, popped)\n            stack.pop()\n        # 尝试出栈：如果栈不空\n        if stack:\n            top = stack.pop()\n            dfs(push_num, stack, popped + 1)\n            stack.append(top)\n\n    count = 0\n    dfs(1, [], 0)\n    return count\n\n# 读取输入\nn = int(input())\nprint(count_sequences(n))\n'

def g4077(r): return f"{r.randint(1, 12)}\n"

def build_cases():
    return [SAMPLE_IN] + [g4077(random.Random(NUMBER + i)) for i in range(1, 20)]

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
