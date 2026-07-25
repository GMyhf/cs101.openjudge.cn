"""5804 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 5804
SAMPLE_IN = '3\n2\n8 5\n3\n8 5 6\n3\n4 10 11\n'
SAMPLE_OUT = '2\n1\n2\n'
REFERENCE_SOURCE = 'import sys\n\ndef find_lca_of_two(a, b):\n    """查找两个节点 a 和 b 的最近公共祖先"""\n    while a != b:\n        if a > b:\n            a //= 2  # 较大者向上爬\n        else:\n            b //= 2  # 较大者向上爬\n    return a\n\ndef solve():\n    # 使用 sys.stdin.read().split() 处理所有空格/换行符分割的输入\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    ptr = 0\n    t_str = input_data[ptr]\n    ptr += 1\n    t = int(t_str)\n    \n    for _ in range(t):\n        n = int(input_data[ptr])\n        ptr += 1\n        \n        # 读取当前组的 n 个节点\n        nodes = []\n        for _ in range(n):\n            nodes.append(int(input_data[ptr]))\n            ptr += 1\n            \n        if not nodes:\n            continue\n        \n        # 迭代处理：先取第一个数作为初始 LCA，然后不断与后面的数求 LCA\n        res_lca = nodes[0]\n        for i in range(1, n):\n            res_lca = find_lca_of_two(res_lca, nodes[i])\n        \n        # 输出结果\n        print(res_lca)\n\nif __name__ == "__main__":\n    solve()\n'

def g5804(r):
    parts = [str(r.randint(2, 5))]
    for _ in range(int(parts[0])):
        n = r.randint(2, 10); parts.append(str(n))
        parts.append(" ".join(str(r.randint(1, 10000)) for _ in range(n)))
    return "\n".join(parts) + "\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g5804(random.Random(NUMBER + i + attempt * 1000))
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
