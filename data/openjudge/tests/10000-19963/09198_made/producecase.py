"""9198 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 9198
SAMPLE_IN = '{}[(){}]()\n'
SAMPLE_OUT = 'Yes\n'
REFERENCE_SOURCE = 'def is_beautiful_brackets(sequence):\n    stack = []\n    # 对应关系字典，键为右括号，值为对应的左括号\n    bracket_pairs = {\')\': \'(\', \']\': \'[\', \'}\': \'{\'}\n    \n    for bracket in sequence:\n        if bracket in bracket_pairs.values():\n            # 若是左括号，压入栈中\n            stack.append(bracket)\n        elif bracket in bracket_pairs:\n            # 若是右括号，检查栈顶元素是否匹配\n            if stack and stack[-1] == bracket_pairs[bracket]:\n                stack.pop()\n            else:\n                return "No"\n        else:\n            # 输入不合法的字符时，直接返回No\n            return "No"\n    # 栈为空表示括号序列美观\n    return "Yes" if not stack else "No"\n\n# 输入处理\nsequence = input().strip()\n\n# 输出结果\nprint(is_beautiful_brackets(sequence))\n'

def g9198(r):
    pairs = ["()", "[]", "{}"]
    text = "".join(r.choice(pairs) for _ in range(r.randint(2, 20)))
    if r.random() < .5: text = text[:-1] + r.choice(")]}{")
    return text + "\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g9198(random.Random(NUMBER + i + attempt * 1000))
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
