"""4123 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4123
SAMPLE_IN = '1\n5 4 0 0\n'
SAMPLE_OUT = '32\n'
REFERENCE_SOURCE = 'maxn = 10;\nsx = [-2,-1,1,2, 2, 1,-1,-2] # 马的横向移动\nsy = [ 1, 2,2,1,-1,-2,-2,-1] # 马的纵向移动\n\nans = 0;\n \ndef Dfs(dep: int, x: int, y: int):\n    #是否已经全部走完\n    if n*m == dep:\n        global ans\n        ans += 1\n        return\n    \n    #对于每个可以走的点\n    for r in range(8):\n        s = x + sx[r]\n        t = y + sy[r]\n        if chess[s][t]==False and 0<=s<n and 0<=t<m :\n            chess[s][t]=True\n            Dfs(dep+1, s, t)\n            chess[s][t] = False; #回溯\n \n\nfor _ in range(int(input())):\n    n,m,x,y = map(int, input().split())\n    chess = [[False]*maxn for _ in range(maxn)]  #False表示没有走过\n    ans = 0\n    chess[x][y] = True\n    Dfs(1, x, y)\n    print(ans)\n'

def g4123(r):
    n, m = r.choice([(1, 2), (2, 3), (3, 3), (3, 4), (4, 3), (4, 4), (5, 4)])
    x, y = r.randrange(n), r.randrange(m)
    return f"1\n{n} {m} {x} {y}\n"

def build_cases():
    return [SAMPLE_IN] + [g4123(random.Random(NUMBER + i)) for i in range(1, 20)]

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
