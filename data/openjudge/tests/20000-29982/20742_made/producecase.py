"""20742 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 30 组数据（n=1..30 全覆盖）。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import re
import subprocess
import tempfile
from pathlib import Path

NUMBER = 20742
SAMPLE_IN = '4\n'
SAMPLE_OUT = '4\n'
REFERENCE_SOURCE = 'def tribonacci(n):\n    if n == 0:\n        return 0\n    elif n <= 2:\n        return 1\n    trib = [0, 1, 1] + [0] * (n - 2)\n    for i in range(3, n + 1):\n        trib[i] = trib[i - 1] + trib[i - 2] + trib[i - 3]\n    return trib[n]\n\n# 读取输入并处理\nn = int(input())\nprint(tribonacci(n))\n'

def g20742(r): return str(r.randint(1,30))+"\n"


def valid(text):
    """题面：输入一个正整数 n，1<=n<=30。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    line = text[:-1]
    if not re.fullmatch(r"[1-9][0-9]*", line):
        return False
    return 1 <= int(line) <= 30

def build_cases():
    # 值域只有 30 个，直接全覆盖：先保留原有 19 组（种子不变），再按升序补齐缺的 n（含上限 30、下限 1）
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20742(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    for n in range(1, 31):
        value = f"{n}\n"
        if value not in cases:
            cases.append(value)
    assert len(cases) == 30
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
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
