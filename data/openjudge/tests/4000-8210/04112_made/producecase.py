"""04112 情报破译 测试数据生成器：固定种子，重跑逐字节可复现。

第 0 组是题面样例。其余组先造明文，再按题面规则加密得到输入（第 i 个单词反转后每个字母
循环后移 i 位，i 每行从 1 重新数），期望输出用独立的解密函数算出，并断言解密结果等于明文。
覆盖：单字母、无字母行、行首空格、数字/标点分隔单词（ab3cd）、一行超过 26 / 52 个单词
（位移要模 26）、大小写混合、超长单词、多行（每行重新计数）、大规模行。
"""
import random
import re
from pathlib import Path

SAMPLE_IN = 'fiU umncv oolz  ioex jhfqu,  zg uh zqI nlaxO  ockl yz kmpzgE.\nfX gxcj , ghlsxffr cxmG K.\nab3cd\n'
SAMPLE_OUT = 'The talks will  take place,  at an Air Force  base on Sunday.\nWe have , occupied City F.\naz3ba\n'  # 空格与输入逐一对应


def valid(text):
    """题面只说「若干行，每行一个字符串，可以以空格开头」，没有给字符集与长度的具体上界。
    这里只核格式：至少一行、以换行结尾、每行非空且只含可打印 ASCII（含空格）。"""
    if not text.endswith("\n") or text == "\n":
        return False
    lines = text[:-1].split("\n")
    return all(line and re.fullmatch(r"[\x20-\x7e]+", line) for line in lines)


def shift(c, k):
    base = 65 if c.isupper() else 97
    return chr((ord(c) - base + k) % 26 + base)


def transform_line(line, sign):
    cnt = [0]

    def f(m):
        cnt[0] += 1
        return "".join(shift(c, sign * cnt[0]) for c in m.group()[::-1])

    return re.sub(r"[A-Za-z]+", f, line)


def encrypt(plain):
    return "".join(transform_line(x, +1) + "\n" for x in plain.split("\n")[:-1])


def solve(text):
    return "".join(transform_line(x, -1) + "\n" for x in text.split("\n")[:-1])


LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
SEPS = [" ", " ", " ", " ", ", ", ". ", "  ", "-", "3", "'", "!", " 42 ", "?", ";", ":", "(", ")", '"']


def rword(r, lo=1, hi=10):
    return "".join(r.choice(LETTERS) for _ in range(r.randint(lo, hi)))


def rline(r, words, lead=False, lo=1, hi=10):
    parts = [" " * r.randint(1, 4)] if lead else []
    for i in range(words):
        parts.append(rword(r, lo, hi))
        if i + 1 < words:
            parts.append(r.choice(SEPS))
    tail = r.choice(["", ".", "!", "?", " 2023"])
    return "".join(parts) + tail


def from_plain(lines):
    plain = "".join(x + "\n" for x in lines)
    enc = encrypt(plain)
    assert solve(enc) == plain
    return enc


def build_cases():
    r = random.Random(4112)
    cases = [
        SAMPLE_IN,
        "A\n", "a! 1\n", "Z z\n",
        from_plain(["123 ,.!? 456"]),                                    # 没有字母
        from_plain(["   Leading spaces here", "  x", " Hello, World!"]), # 行首空格
        from_plain(["ab3cd4ef5gh,ij.kl"]),                               # 数字/标点分隔
        from_plain([" ".join("w" + LETTERS[i % 52] for i in range(30))]),   # 30 个单词，位移超 26
        from_plain([" ".join(rword(r, 1, 3) for _ in range(60))]),       # 超过 52 个单词
        from_plain(["Zz Aa zZ aA yY Bb"]),
        from_plain([rword(r, 2000, 2000)]),                              # 超长单词
        from_plain(["The quick brown fox jumps over the lazy dog."] * 5),  # 每行重新计数
        from_plain(["x"] * 30),
    ]
    for _ in range(12):
        cases.append(from_plain([rline(r, r.randint(1, 15), r.random() < .3) for _ in range(r.randint(1, 6))]))
    for _ in range(6):
        cases.append(from_plain([rline(r, r.randint(20, 120), r.random() < .3) for _ in range(r.randint(1, 10))]))
    cases.append(from_plain([rline(r, r.randint(1, 30), r.random() < .3) for _ in range(3000)]))
    cases.append(from_plain([rline(r, 100000, False, 1, 4)]))
    cases.append(from_plain([rline(r, r.randint(1000, 5000), True) for _ in range(20)]))
    cases.append(from_plain([rline(r, 40000, True, 5, 12) for _ in range(1)]))
    while len(cases) < 40:
        cases.append(from_plain([rline(r, r.randint(1, 8), r.random() < .5) for _ in range(r.randint(1, 3))]))
    return cases


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN and solve(SAMPLE_IN) == SAMPLE_OUT
    assert len(cases) == 40 and len(set(cases)) == len(cases)
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for i, c in enumerate(cases):
        assert valid(c), i
        (root / f"{i}.in").write_text(c)
        (root / f"{i}.out").write_text(solve(c))


if __name__ == "__main__":
    main()
