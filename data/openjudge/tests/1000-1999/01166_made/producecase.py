"""01166 The Clocks 测试数据生成器。

第 0 组是题面样例；其余组：最长答案（27 步）、每个单步操作对应的状态、
答案很长/很短的状态和随机状态。答案由 samplecode.py 给出，
生成时再用穷举 4^9 种操作组合的结果逐组核对。
"""
import itertools
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = "3 3 0\n2 2 2\n2 1 2\n"
EFFECT = ["ABDE", "ABC", "BCEF", "ADG", "BDEFH", "CFI", "DEGH", "GHI", "EFHI"]
CASES = 40


def valid(text):
    """严格核输入：3 行，每行 3 个 0..3 的整数，单空格分隔。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 3:
        return False
    for line in lines:
        parts = line.split(" ")
        if len(parts) != 3 or any(p not in ("0", "1", "2", "3") for p in parts):
            return False
    return True


def all_solutions():
    """穷举：状态 -> 每个操作的次数（0..3）。题面保证答案唯一，这里断言之。"""
    table = {}
    for cnt in itertools.product(range(4), repeat=9):
        st = [0] * 9
        for m, k in enumerate(cnt):
            for ch in EFFECT[m]:
                st[ord(ch) - 65] += k
        st = tuple((-x) % 4 for x in st)
        assert st not in table
        table[st] = cnt
    return table


def to_text(st):
    return "\n".join(" ".join(map(str, st[i:i + 3])) for i in (0, 3, 6)) + "\n"


def brute_answer(table, text):
    st = tuple(int(x) for x in text.split())
    cnt = table[st]
    return " ".join(str(m + 1) for m in range(9) for _ in range(cnt[m]))


def main():
    rng = random.Random(1166)
    table = all_solutions()
    by_len = {}
    for st, cnt in table.items():
        by_len.setdefault(sum(cnt), []).append(st)
    for v in by_len.values():
        v.sort()
    cases = [SAMPLE]
    seen = {SAMPLE}

    def add(st):
        t = to_text(st)
        if t not in seen and sum(table[st]) > 0:
            seen.add(t)
            cases.append(t)

    add(by_len[27][0])                         # 唯一的 27 步状态（每个操作 3 次）
    for st in rng.sample(by_len[26], 3):       # 26 步
        add(st)
    for st in rng.sample(by_len[25], 2):
        add(st)
    for m in range(9):                         # 只需一次操作 m+1 的状态
        cnt = [0] * 9
        cnt[m] = 1
        st = next(s for s, c in table.items() if list(c) == cnt)
        add(st)
    for st in rng.sample(by_len[2], 2):
        add(st)
    all_states = sorted(table)
    while len(cases) < CASES:
        add(rng.choice(all_states))

    out = Path("data")
    out.mkdir(exist_ok=True)
    for p in out.glob("*"):
        p.unlink()
    for i, text in enumerate(cases):
        assert valid(text), i
        res = subprocess.run([sys.executable, "-I", "samplecode.py"], input=text, text=True,
                             capture_output=True, timeout=60, check=True).stdout.rstrip() + "\n"
        assert res.strip() == brute_answer(table, text), i
        (out / f"{i}.in").write_text(text)
        (out / f"{i}.out").write_text(res)
    assert (out / "0.out").read_text() == "4 5 8 9\n"


if __name__ == "__main__":
    main()
