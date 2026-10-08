"""03259 求满足约束条件的四位数或六位数 测试数据生成器。

题面输入只有 4 或 6 两种取值，题面样例为空，所以没有样例组。
共 20 组，4 与 6 交替出现（值域只有两个，组间重复不可避免）。
答案由 samplecode.py 给出，并用独立的数学写法逐组核对。
"""
import subprocess
import sys
from pathlib import Path

CASES = 20


def valid(text):
    """严格核输入：一行，只能是 4 或 6。"""
    return text in ("4\n", "6\n")


def brute(n):
    h = n // 2
    lo, hi = 10 ** (n - 1), 10 ** n
    return " ".join(str(x) for x in range(lo, hi)
                    if (x // 10 ** h + x % 10 ** h) ** 2 == x)


def main():
    cases = ["4\n" if s % 2 else "6\n" for s in range(1, CASES + 1)]
    out = Path("data")
    out.mkdir(exist_ok=True)
    for p in out.glob("*"):
        p.unlink()
    for i, text in enumerate(cases):
        assert valid(text), i
        res = subprocess.run([sys.executable, "-I", "samplecode.py"], input=text, text=True,
                             capture_output=True, timeout=60, check=True).stdout
        res = "\n".join(line.rstrip() for line in res.rstrip().splitlines()) + "\n"
        assert res.strip() == brute(int(text)), i
        (out / f"{i}.in").write_text(text)
        (out / f"{i}.out").write_text(res)


if __name__ == "__main__":
    main()
