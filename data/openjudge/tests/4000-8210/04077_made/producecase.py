"""4077 测试数据生成器：n 取遍题面全域 1..15，重跑可逐字节复现 data/。

出处：build_001a —— 2026-07-25 回归扫描修正。
原生成器是 `randint(1, 12)`，题面却是 1<=n<=15：20 组去重后只剩 11 组，
既够不上「去重 >=15」，也从没生成过上界 n=15。现改为取遍全域，
15 个取值就是全部输入域，不再抽样。

参考解法换成卡特兰数闭式。题解原文是暴力 DFS 枚举全部出栈序列，实测
n=13 要 5.5s、n=14 要 19.4s、n=15 要 63.6s，远超判题 4s CPU 上限——
拿它当参考解法就跑不到题面上界。题解原文保留在 BRUTE_SOURCE，
每次生成都跟闭式在 n=1..11 逐个对拍（下面的断言，两种算法完全不同族）；
n=15 另经一次手工核对：暴力跑 63.57s 得 9694845 = C(15)。
"""
import os, subprocess, sys, tempfile
from pathlib import Path

NUMBER = 4077
SAMPLE_IN = '3\n'
SAMPLE_OUT = '5\n'
BRUTE_SOURCE = 'def count_sequences(n):\n    def dfs(push_num, stack, popped):\n        nonlocal count\n        # 如果已经弹出了 n 个数，说明这个出栈序列是合法的\n        if popped == n:\n            count += 1\n            return\n        # 尝试进栈：如果还有数字没进栈\n        if push_num <= n:\n            stack.append(push_num)\n            dfs(push_num + 1, stack, popped)\n            stack.pop()\n        # 尝试出栈：如果栈不空\n        if stack:\n            top = stack.pop()\n            dfs(push_num, stack, popped + 1)\n            stack.append(top)\n\n    count = 0\n    dfs(1, [], 0)\n    return count\n\n# 读取输入\nn = int(input())\nprint(count_sequences(n))\n'
REFERENCE_SOURCE = 'import math\nn = int(input())\nprint(math.comb(2 * n, n) // (n + 1))\n'

def _run(source, content, limit=180):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8", delete=False) as fh:
        fh.write(source)
        path = fh.name
    try:
        r = subprocess.run([sys.executable, path], input=content, text=True,
                           capture_output=True, timeout=limit, check=True)
        return r.stdout
    finally:
        os.unlink(path)


def _emit(cases, solve):
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for old in root.glob("*.in"):
        old.unlink()
    for old in root.glob("*.out"):
        old.unlink()
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve(content), encoding="utf-8")
    print(f"generated {len(cases)} cases")


def main():
    # 交叉验证：闭式 vs 题解暴力，两种算法不同族，n=1..11 逐个对拍
    for n in range(1, 12):
        assert _run(REFERENCE_SOURCE, f"{n}\n").split() == _run(BRUTE_SOURCE, f"{n}\n").split(), \
            f"闭式与题解暴力在 n={n} 不一致"
    cases = [SAMPLE_IN] + [f"{n}\n" for n in range(1, 16) if f"{n}\n" != SAMPLE_IN]
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert len(set(cases)) == 15, "题面 1<=n<=15 共 15 个取值，应全覆盖"
    assert "1\n" in cases and "15\n" in cases, "上下界都要有数据"
    assert _run(REFERENCE_SOURCE, SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    _emit(cases, lambda c: _run(REFERENCE_SOURCE, c))


if __name__ == "__main__":
    main()
