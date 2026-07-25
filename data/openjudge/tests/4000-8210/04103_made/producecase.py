"""4103 测试数据生成器：n 取遍题面全域 1..20，重跑可逐字节复现 data/。

出处：build_001a —— 2026-07-25 回归扫描修正。
原生成器是 `randint(1, 15)`，题面却是 n<=20：20 组去重后只剩 12 组，最大只到 14。
现改为取遍全域 1..20，20 个取值就是全部输入域。

参考解法换成线性递推 f(n)=2*f(n-1)+f(n-2)（f(0)=1, f(1)=3）。题解原文是
暴力搜索全部路径，实测 n=15 要 12.0s、n=18 要 143.5s，跑不到题面上界 20。
题解原文保留在 BRUTE_SOURCE，每次生成都跟递推在 n=1..12 逐个对拍
（穷举路径 vs 闭式递推，不同族）；n=18 另经手工核对：暴力得 9369319 = f(18)。
"""
import os, subprocess, sys, tempfile
from pathlib import Path

NUMBER = 4103
SAMPLE_IN = '2\n'
SAMPLE_OUT = '7\n'
BRUTE_SOURCE = 'n = int(input())\nstep = [[1, 0], [-1, 0], [0, 1]]\nnum = 1\n\n\ndef dfs(x, y, m, visited):\n    global num\n    if m == 0:\n        return\n    visited.append([x, y])\n    num -= 1\n    for j in range(3):\n        if [x+step[j][0], y+step[j][1]] not in visited:\n            num += 1\n            lista = []\n            lista += visited\n            dfs(x+step[j][0], y+step[j][1], m-1, lista)\n\n\ndfs(0, 0, n, [])\nprint(num)\n'
REFERENCE_SOURCE = 'n = int(input())\na, b = 1, 3            # f(0)=1, f(1)=3, f(k)=2*f(k-1)+f(k-2)\nfor _ in range(max(0, n - 1)):\n    a, b = b, 2 * b + a\nprint(b if n >= 1 else a)\n'

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
    for n in range(1, 13):
        assert _run(REFERENCE_SOURCE, f"{n}\n").split() == _run(BRUTE_SOURCE, f"{n}\n").split(), \
            f"递推与题解暴力在 n={n} 不一致"
    cases = [SAMPLE_IN] + [f"{n}\n" for n in range(1, 21) if f"{n}\n" != SAMPLE_IN]
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert len(set(cases)) == 20, "题面 n<=20 应覆盖 1..20 全部取值"
    assert "1\n" in cases and "20\n" in cases, "上下界都要有数据"
    assert _run(REFERENCE_SOURCE, SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    _emit(cases, lambda c: _run(REFERENCE_SOURCE, c))


if __name__ == "__main__":
    main()
