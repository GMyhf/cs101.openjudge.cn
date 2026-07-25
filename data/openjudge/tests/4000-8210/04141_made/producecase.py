"""4141 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4141
SAMPLE_IN = '1 1 0 0 0 0\n'
SAMPLE_OUT = 'Total=3\n'
REFERENCE_SOURCE = "# 蒋子轩23工学院\n'''\n深度优先搜索算法，用于计算一组给定权重的砝码的不同重量组合的数量。\n\n代码中的变量weights是权重列表，表示不同砝码的重量。变量max_w是一个列表，\n用于表示每个砝码的最大使用数量。\n\n函数dfs是一个递归函数，用于遍历所有可能的砝码组合。index参数表示当前考虑的砝码索引，\ncur_w参数表示当前已经组合的重量。当index等于6时，表示已经尝试了所有的砝码，递归结束。\n如果cur_w不等于0，则将其添加到集合w中。递归过程中，\n使用一个循环遍历所有可能的使用该砝码个数，并递归调用dfs函数计算下一个砝码的组合。\n\n在主程序部分，将输入的最大使用数量存储在max_w列表中。通过调用dfs(0,0)开始计算所有可能的\n砝码重量组合。最后，输出集合w的长度，即不同重量组合的数量。\n'''\n\nweights = [1, 2, 3, 5, 10, 20]\n\n\ndef dfs(index, cur_w):\n\t# 已尝试所有可能砝码，递归结束\n    if index == 6:\n        if cur_w != 0:\n            w.add(cur_w)\n        return\n    #遍历所有可能的使用该砝码个数\n    for i in range(max_w[index]+1):\n        dfs(index+1, cur_w+i*weights[index])\n\n\nmax_w = list(map(int, input().split()))\n#使用set自动去重\nw = set()\ndfs(0, 0)\nprint(f'Total={len(w)}')\n\n"

def g4141(r):
    return " ".join(str(r.randint(0, 4)) for _ in range(6)) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4141(random.Random(NUMBER + i)) for i in range(1, 20)]

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
