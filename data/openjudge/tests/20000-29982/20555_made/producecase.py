"""20555 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 20555
SAMPLE_IN = '( not ( True or False ) ) and ( False or True and True )\n'
SAMPLE_OUT = '0\n'
REFERENCE_SOURCE = 'def evaluate_expression(expression):\n    # Replace logical operators with Python equivalents\n    expression = expression.replace("not", "not ").replace("and", " and ").replace("or", " or ")\n    # Evaluate the expression\n    return int(eval(expression))\n\n# 读取输入并处理\nexpression = input()\nprint(evaluate_expression(expression))\n'

def g20555(r):
    a=r.choices(["True","False"],k=4); op1=r.choice(["and","or"]); op2=r.choice(["and","or"]); return f"( {a[0]} {op1} {a[1]} ) {op2} ( not {a[2]} or {a[3]} )\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20555(random.Random(NUMBER + i + attempt * 1000))
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
