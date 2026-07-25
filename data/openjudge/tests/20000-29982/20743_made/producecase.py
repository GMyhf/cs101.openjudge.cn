"""20743 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 20743
SAMPLE_IN = '(eg(en(duj))po)\n'
SAMPLE_OUT = 'openjudge\n'
REFERENCE_SOURCE = "def reverse_parentheses(s):\n    stack = []\n    for char in s:\n        if char == ')':\n            temp = []\n            while stack and stack[-1] != '(':\n                temp.append(stack.pop())\n            # remove the opening parenthesis\n            if stack:\n                stack.pop()\n            # add the reversed characters back to the stack\n            stack.extend(temp)\n        else:\n            stack.append(char)\n    return ''.join(stack)\n\n# 读取输入并处理\ns = input().strip()\nprint(reverse_parentheses(s))\n"

def g20743(r): return "("+"".join(r.choice("abcd") for _ in range(r.randint(1,20)))+")"+"".join(r.choice("abcd") for _ in range(r.randint(0,5)))+"\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20743(random.Random(NUMBER + i + attempt * 1000))
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
