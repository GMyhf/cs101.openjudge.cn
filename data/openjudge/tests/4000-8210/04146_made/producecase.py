"""4146 测试数据生成器：n 取遍题面全域 [0,100] 的 21 个采样点，重跑可逐字节复现 data/。

出处：build_001a —— 2026-07-25 回归扫描修正。
原生成器是 `choice([0,1,2,3,5,10,25,50,100])`——只有 9 个候选却抽 19 次，
20 组去重后只剩 7 组，且下界 0 和上界 100 都没抽中。现改为固定取样点，
覆盖 0 与 100 两端，小值段加密（答案在小 n 上变化最碎）。
"""
from pathlib import Path

SAMPLE_IN = '3\n'
SAMPLE_OUT = '5\n'
PICKS = [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 14, 18, 23, 30, 38, 47, 58, 70, 83, 95, 100]


def solve_text(text):
    n = int(text.split()[0])
    ans = 0
    for a in range(n + 1):
        for b in range(n + 1):
            for c in range(n + 1):
                if (a + b) % 2 == 0 and (b + c) % 3 == 0 and (a + b + c) % 5 == 0:
                    ans = max(ans, a + b + c)
    return str(ans) + "\n"


def main():
    assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip(), "参考解法跑不出样例输出"
    cases = [SAMPLE_IN] + [f"{n}\n" for n in PICKS if f"{n}\n" != SAMPLE_IN]
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert all(0 <= int(c) <= 100 for c in cases), "题面 0<=n<=100"
    assert "0\n" in cases and "100\n" in cases, "上下界都要有数据"
    assert len(set(cases)) >= 15, "去重后至少 15 组"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for old in list(root.glob("*.in")) + list(root.glob("*.out")):
        old.unlink()
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
    print(f"generated {len(cases)} cases for 04146")


if __name__ == "__main__":
    main()
