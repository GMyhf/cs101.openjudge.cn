"""4103 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4103
SAMPLE_IN = '2\n'
SAMPLE_OUT = '7\n'
REFERENCE_SOURCE = 'n = int(input())\nstep = [[1, 0], [-1, 0], [0, 1]]\nnum = 1\n\n\ndef dfs(x, y, m, visited):\n    global num\n    if m == 0:\n        return\n    visited.append([x, y])\n    num -= 1\n    for j in range(3):\n        if [x+step[j][0], y+step[j][1]] not in visited:\n            num += 1\n            lista = []\n            lista += visited\n            dfs(x+step[j][0], y+step[j][1], m-1, lista)\n\n\ndfs(0, 0, n, [])\nprint(num)\n'

def g4103(r): return f"{r.randint(1, 15)}\n"

def build_cases():
    return [SAMPLE_IN] + [g4103(random.Random(NUMBER + i)) for i in range(1, 20)]

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
