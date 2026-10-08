"""4122 切割回文 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 40 组数据。

第 0 组为题面样例，1-3 组沿用原有手造组；其余覆盖长度 1、可暴力核对的小规模组、
T=20 且长度 1000 的满规模组（随机 26 字母 / 二元字母表 / 全同字母 / 回文拼接 / 斐波那契串等）。

参考解 REFERENCE：中心扩展 + 最少切割 DP，O(n^2)。
原先内嵌的通用脚本（同目录 samplecode.py）对每对 (i, j) 做切片比较，是 O(n^3)，
只用作交叉核对，不再用来生成答案。
"""
import random
import re
import subprocess
import tempfile
from pathlib import Path

SAMPLE_IN = '3\nabaacca\nabcd\nabcba\n'
SAMPLE_OUT = '1\n3\n0\n'
REFERENCE = r'''
import sys

def min_cut(s):
    n = len(s)
    cut = list(range(-1, n))          # cut[i]：前 i 个字符的最少切割数，cut[0] = -1
    for c in range(n):
        for l, r in ((c, c), (c, c + 1)):
            while l >= 0 and r < n and s[l] == s[r]:
                if cut[l] + 1 < cut[r + 1]:
                    cut[r + 1] = cut[l] + 1
                l -= 1
                r += 1
    return cut[n]

data = sys.stdin.read().split()
t = int(data[0])
print("\n".join(str(min_cut(s)) for s in data[1:1 + t]))
'''
B = ["1\na\n", "1\naaaaaaaa\n", "1\nabcddcba\n"]
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def valid(text):
    """题面：第一行 T（T <= 20）；随后 T 行，每行一个只含小写字母、长度不超过 1000 的字符串
    （空串没有意义，要求长度至少 1）。"""
    if not isinstance(text, str) or not text.endswith("\n") or "\r" in text:
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*", lines[0]):
        return False
    t = int(lines[0])
    if not 1 <= t <= 20 or len(lines) != 1 + t:
        return False
    return all(re.fullmatch(r"[a-z]{1,1000}", s) for s in lines[1:])


def rand_str(r, n, alpha):
    return "".join(r.choice(alpha) for _ in range(n))


def pal_concat(r, n, alpha):
    # 若干随机回文拼接，长度恰为 n
    out = ""
    while len(out) < n:
        half = rand_str(r, r.randint(1, 40), alpha)
        p = half + (half[-2::-1] if r.random() < 0.5 else half[::-1])
        out += p
    return out[:n]


def fib_str(n):
    a, b = "a", "ab"
    while len(b) < n:
        a, b = b, b + a
    return b[:n]


def near_pal(r, n, alpha):
    half = rand_str(r, n // 2, alpha)
    s = list(half + ("" if n % 2 == 0 else r.choice(alpha)) + half[::-1])
    i = r.randrange(n)
    s[i] = r.choice([c for c in alpha if c != s[i]] or alpha)
    return "".join(s)


def pack(strings):
    return f"{len(strings)}\n" + "".join(s + "\n" for s in strings)


def build_cases():
    r = random.Random(4122)
    cases = [SAMPLE_IN] + B
    cases.append(pack(list(LETTERS[:20])))                                          # 4 T=20，长度 1
    for _ in range(5, 15):                                                          # 5-14 小规模
        cases.append(pack([rand_str(r, r.randint(1, 12), LETTERS[:r.randint(1, 3)])
                           for _ in range(r.randint(5, 20))]))
    for _ in range(15, 25):                                                         # 15-24 中规模
        gens = [lambda n: rand_str(r, n, LETTERS[:r.randint(1, 26)]),
                lambda n: pal_concat(r, n, LETTERS[:r.randint(2, 5)]),
                lambda n: near_pal(r, n, LETTERS[:r.randint(2, 4)])]
        cases.append(pack([r.choice(gens)(r.randint(50, 300)) for _ in range(20)]))
    for _ in range(25, 30):                                                         # 25-29 满规模，26 字母
        cases.append(pack([rand_str(r, 1000, LETTERS) for _ in range(20)]))
    for _ in range(30, 33):                                                         # 30-32 满规模，二元字母表
        cases.append(pack([rand_str(r, 1000, "ab") for _ in range(20)]))
    cases.append(pack([pal_concat(r, 1000, LETTERS[:r.randint(2, 4)]) for _ in range(20)]))   # 33
    cases.append(pack([fib_str(1000)] + [fib_str(r.randint(900, 999)) for _ in range(19)]))  # 34
    cases.append(pack(["a" * 1000, "a" * 999 + "b", "b" + "a" * 999, "a" * 500 + "b" + "a" * 499]
                      + [rand_str(r, 1000, "abc") for _ in range(16)]))                       # 35 全同字母
    cases.append(pack([("ab" * 500), ("abc" * 334)[:1000], ("aab" * 334)[:1000]]
                      + [rand_str(r, 1000, "ab") for _ in range(17)]))                        # 36 周期串
    cases.append(pack([(LETTERS * 39)[:1000]] + [rand_str(r, 1000, LETTERS) for _ in range(19)]))  # 37 答案 999
    cases.append(pack([near_pal(r, 1000, LETTERS[:r.randint(2, 26)]) for _ in range(20)]))     # 38 近回文
    cases.append(pack([r.choice([rand_str(r, 1000, "abcd"), pal_concat(r, 1000, "ab"),
                                 near_pal(r, 1000, "ab")]) for _ in range(20)]))             # 39 混合
    return cases


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert len(cases) == 40 and len(set(cases)) == len(cases), "组数不对或存在重复组"
    with tempfile.NamedTemporaryFile("w", suffix=".py") as f:
        f.write(REFERENCE)
        f.flush()
        d = Path(__file__).parent / "data"
        for i, c in enumerate(cases):
            assert valid(c), i
            p = subprocess.run(["python3", f.name], input=c, text=True, capture_output=True, check=True)
            if i == 0:
                assert p.stdout == SAMPLE_OUT, "参考解跑不出样例输出"
            (d / f"{i}.in").write_text(c)
            (d / f"{i}.out").write_text(p.stdout)


if __name__ == "__main__":
    main()
