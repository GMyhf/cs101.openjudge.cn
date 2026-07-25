"""20644 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 20644
SAMPLE_IN = '3 4\n0111\n1111\n0111\n'
SAMPLE_OUT = '15\n'
REFERENCE_SOURCE = 'm,n = map(int, input().split())\nmatrix = []\nfor i in range(m):\n    matrix.append(list(map(int, list(input()))))\n\ndef check(matrix, i, j, step):\n    for x in range(i, i+step+1):\n        for y in range(j, j+step+1):\n            if matrix[x][y] == 0:\n                return False\n    return True\n\ncnt = 0\nstep = 0\n\nwhile step <= min(m, n):\n    for i in range(m-step):\n        for j in range(n-step):\n            if check(matrix, i, j, step):\n                cnt += 1\n    step += 1\n\nprint(cnt)\n'

def g20644(r):
    m,n=r.randint(2,10),r.randint(2,10); return f"{m} {n}\n"+"\n".join("".join(r.choice("01") for _ in range(n)) for _ in range(m))+"\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20644(random.Random(NUMBER + i + attempt * 1000))
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
