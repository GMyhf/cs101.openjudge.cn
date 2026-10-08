"""08466 火柴棒等式 测试数据生成器。

题面：输入一个整数 n（n≤24）。取值只有 0..24，规范写法全覆盖共 25 组
（第 0 组是题面样例 n=5），另加 3 组同值不同空白写法（无行尾换行、
行尾空格、多一个空行）的较大 n，凑足 28 组且两两不同。
答案由 samplecode.py 给出，并用独立的暴力枚举逐组核对。
"""
import re
import subprocess
import sys
from pathlib import Path

SAMPLE = "5\n"
STICKS = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]


def valid(text):
    """严格核输入：一个不带前导零的整数 0..24，前后只允许空格/换行。"""
    m = re.fullmatch(r"[ \n]*(0|[1-9][0-9]*)[ \n]*", text)
    return bool(m) and int(m.group(1)) <= 24


def cost(x):
    return sum(STICKS[int(c)] for c in str(x))


def brute_all():
    """独立暴力：返回 n=0..24 的答案表。

    n≤24 时 A、B、C 三个数共用 n-4≤20 根火柴，每位数字至少 2 根；
    A 若有 5 位（≥10 根），C≥A 也至少 10 根，再加 B≥2 根就超过 20，
    所以 A、B 都小于 10000。先按单个数至多 16 根筛候选再两两枚举。
    """
    c = [cost(x) for x in range(20000)]
    cand = [x for x in range(10000) if c[x] <= 16]
    cnt = [0] * 25
    for a in cand:
        for b in cand:
            if c[a] + c[b] <= 18:
                t = c[a] + c[b] + c[a + b] + 4
                if t <= 24:
                    cnt[t] += 1
    return cnt


def main():
    cases = [SAMPLE] + [f"{n}\n" for n in range(25) if n != 5]
    cases += ["24", "23 \n", "22\n\n"]
    assert len(set(cases)) == len(cases)
    answers = brute_all()
    out = Path("data")
    out.mkdir(exist_ok=True)
    for p in out.glob("*"):
        p.unlink()
    for i, text in enumerate(cases):
        assert valid(text), i
        n = int(text)
        res = subprocess.run([sys.executable, "-I", "samplecode.py"], input=text, text=True,
                             capture_output=True, timeout=60, check=True).stdout.rstrip() + "\n"
        assert res == f"{answers[n]}\n", (i, res, answers[n])
        (out / f"{i}.in").write_text(text)
        (out / f"{i}.out").write_text(res)
    assert (out / "0.out").read_text() == "0\n"


if __name__ == "__main__":
    main()
