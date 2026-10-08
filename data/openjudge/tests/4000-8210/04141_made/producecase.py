"""4141 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 32 组数据。

2026-10-07 审计加强：原 19 组随机数据每种砝码只取 0..4 枚，总重最多 164g，
离题面「总重<=1000」很远，按枚数逐一枚举（乘积级 DFS）的写法也能过。
第 1..19 组保持原样，追加第 20..31 组：总重贴近或等于 1000 的满规模组、
单一砝码 1000 枚、只有 20g、只有 1 枚砝码等边界。参考解改用按重量的可达性 DP
（原 DFS 在满规模组上要枚举上亿种组合），两者在第 0..19 组上输出一致。

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
DFS_SOURCE = "# 蒋子轩23工学院\n'''\n深度优先搜索算法，用于计算一组给定权重的砝码的不同重量组合的数量。\n\n代码中的变量weights是权重列表，表示不同砝码的重量。变量max_w是一个列表，\n用于表示每个砝码的最大使用数量。\n\n函数dfs是一个递归函数，用于遍历所有可能的砝码组合。index参数表示当前考虑的砝码索引，\ncur_w参数表示当前已经组合的重量。当index等于6时，表示已经尝试了所有的砝码，递归结束。\n如果cur_w不等于0，则将其添加到集合w中。递归过程中，\n使用一个循环遍历所有可能的使用该砝码个数，并递归调用dfs函数计算下一个砝码的组合。\n\n在主程序部分，将输入的最大使用数量存储在max_w列表中。通过调用dfs(0,0)开始计算所有可能的\n砝码重量组合。最后，输出集合w的长度，即不同重量组合的数量。\n'''\n\nweights = [1, 2, 3, 5, 10, 20]\n\n\ndef dfs(index, cur_w):\n\t# 已尝试所有可能砝码，递归结束\n    if index == 6:\n        if cur_w != 0:\n            w.add(cur_w)\n        return\n    #遍历所有可能的使用该砝码个数\n    for i in range(max_w[index]+1):\n        dfs(index+1, cur_w+i*weights[index])\n\n\nmax_w = list(map(int, input().split()))\n#使用set自动去重\nw = set()\ndfs(0, 0)\nprint(f'Total={len(w)}')\n\n"
# 参考解：按重量做可达性 DP，O(总枚数 * 1000)。
REFERENCE_SOURCE = (
    "a = list(map(int, input().split()))\n"
    "w = (1, 2, 3, 5, 10, 20)\n"
    "ok = [True] + [False] * 1000\n"
    "for cnt, wt in zip(a, w):\n"
    "    for _ in range(cnt):\n"
    "        for x in range(1000, wt - 1, -1):\n"
    "            if ok[x - wt]:\n"
    "                ok[x] = True\n"
    "print(f'Total={sum(ok) - 1}')\n"
)
WEIGHTS = (1, 2, 3, 5, 10, 20)


def valid(text):
    """题面：一行六个整数 a1..a6，单个空格隔开；总重 a1+2a2+3a3+5a4+10a5+20a6 <= 1000。

    题面写「正整数」，但样例 `1 1 0 0 0 0` 自己就有 0，所以这里放宽到非负整数。
    """
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 1:
        return False
    tok = lines[0].split(" ")
    if len(tok) != 6:
        return False
    if not all(t.isdigit() and (t == "0" or t[0] != "0") for t in tok):
        return False
    a = list(map(int, tok))
    return sum(x * w for x, w in zip(a, WEIGHTS)) <= 1000

def g4141(r):
    return " ".join(str(r.randint(0, 4)) for _ in range(6)) + "\n"

def g4141_full(r, low):
    """随机挑砝码往里加，直到总重落在 [low, 1000]。"""
    while True:
        a = [0] * 6
        total = 0
        while True:
            k = r.randrange(6)
            if total + WEIGHTS[k] > 1000:
                break
            a[k] += 1
            total += WEIGHTS[k]
        # 再用能放下的最轻砝码补满
        for k in range(6):
            while total + WEIGHTS[k] <= 1000 and r.random() < 0.5:
                a[k] += 1
                total += WEIGHTS[k]
        if total >= low:
            return " ".join(map(str, a)) + "\n"


FIXED = [
    "1000 0 0 0 0 0\n",      # 只有 1g，满总重
    "0 0 0 0 0 50\n",        # 只有 20g，满总重
    "0 0 0 0 0 1\n",         # 只有一枚砝码
    "160 80 54 32 16 8\n",   # 每种都很多，总重 962，按枚数枚举要上亿种组合
    "0 500 0 0 0 0\n",       # 只有 2g：只能称偶数
    "0 0 1 0 0 49\n",        # 3g 一枚 + 20g，总重 983
]


def build_cases():
    cases = [SAMPLE_IN] + [g4141(random.Random(NUMBER + i)) for i in range(1, 20)]
    cases += FIXED
    cases += [g4141_full(random.Random(NUMBER * 100 + i), 900 + 10 * i) for i in range(6)]
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
    assert len(set(cases)) == len(cases), "组间不得重复"
    for index, content in enumerate(cases):
        assert valid(content), f"第 {index} 组越出题面约束"
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
