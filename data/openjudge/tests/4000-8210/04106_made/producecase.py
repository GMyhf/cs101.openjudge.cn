"""04106 出现两次的字符 测试数据生成器：固定种子，重跑逐字节可复现。

第 0 组是题面样例；其余组覆盖：最小串、区分大小写、多个恰好出现 2 次的字符
（取「首次出现位置更靠前」者；生成时保证首次出现顺序与第二次出现顺序给出同一答案，
避免题面「比较靠前」的歧义）、出现 3/4 次的干扰字符、长串里答案位置很靠后
（卡 s.count 逐个试的 O(L^2) 写法）、大量短串。
"""
import random
import re
from collections import Counter
from pathlib import Path

SAMPLE_IN = '3\nfarewell\n20150106\nPekingUniversity\n'
SAMPLE_OUT = 'e\n1\ne\n'
ALPHA = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
INT_MAX = 2 ** 31 - 1


def valid(text):
    """题面契约：第一行正整数 n（int 范围），其后恰 n 行，每行由大小写字母和数字构成，
    且每个串里必有恰好出现 2 次的字符。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*", lines[0]):
        return False
    n = int(lines[0])
    if n > INT_MAX or len(lines) != n + 1:
        return False
    for s in lines[1:]:
        if not re.fullmatch(r"[A-Za-z0-9]+", s):
            return False
        if 2 not in Counter(s).values():
            return False
    return True


def answer(s):
    cnt = Counter(s)
    for c in s:
        if cnt[c] == 2:
            return c
    raise ValueError("no char appears exactly twice")


def unambiguous(s):
    """按首次出现取的答案与按第二次出现取的答案一致。"""
    cnt = Counter(s)
    seen = Counter()
    for c in s:
        if cnt[c] == 2:
            seen[c] += 1
            if seen[c] == 2:
                return c == answer(s)
    return False


def solve(text):
    lines = text.split("\n")
    n = int(lines[0])
    return "".join(answer(s) + "\n" for s in lines[1:1 + n])


def rand_string(r, length, alpha=ALPHA):
    """随机串：若干字符出现 2 次（至少一个），其余出现 1 或 >=3 次。"""
    while True:
        k = r.randint(1, min(len(alpha), 12))
        chars = r.sample(alpha, k)
        w = []
        twice = 0
        for c in chars:
            m = r.choice([1, 2, 2, 3, 4, 5, 7])
            twice += m == 2
            w += [c] * m
        if twice == 0:
            w += [r.choice([c for c in alpha if c not in chars])] * 2 if len(chars) < len(alpha) else []
        heavy = [c for c in chars if w.count(c) >= 3]
        while heavy and len(w) < length:
            w.append(r.choice(heavy))
        r.shuffle(w)
        s = "".join(w)
        if 2 in Counter(s).values() and unambiguous(s):
            return s


def multi_case(r, n, lo, hi, alpha=ALPHA):
    return f"{n}\n" + "".join(rand_string(r, r.randint(lo, hi), alpha) + "\n" for _ in range(n))


def long_late(r, total):
    """单个长串：前半段全是出现很多次的字符，答案首次出现在中部，
    其后再放几个也恰好出现 2 次但更靠后的字符。"""
    pool = r.sample(ALPHA, 50)
    rest = [c for c in ALPHA if c not in pool]
    ans, others = rest[0], rest[1:5]
    half = total // 2
    left = [r.choice(pool) for _ in range(half)]
    right = [r.choice(pool) for _ in range(total - half - 2 - 2 * len(others))]
    # 保证 pool 里每个字符出现次数 >= 3
    for c in pool:
        left += [c] * 3
    r.shuffle(left)
    mid = [ans]
    tail = right[:]
    pos = r.randint(len(tail) // 4, len(tail) // 2)
    tail.insert(pos, ans)
    # 其他恰好 2 次的字符都放在答案第二次出现之后
    for c in others:
        p1 = r.randint(pos + 1, len(tail))
        tail.insert(p1, c)
        p2 = r.randint(p1 + 1, len(tail))
        tail.insert(p2, c)
    s = "".join(left + mid + tail)
    assert answer(s) == ans and unambiguous(s)
    return "1\n" + s + "\n"


def long_early(r, total):
    """单个长串，答案就在开头（O(L) 正解与暴力都能过，主要考规模与读入）。"""
    pool = r.sample(ALPHA, 40)
    rest = [c for c in ALPHA if c not in pool]
    ans = rest[0]
    body = [r.choice(pool) for _ in range(total - 2)]
    for c in pool:
        body += [c] * 3
    r.shuffle(body)
    s = ans + "".join(body[: len(body) // 3]) + ans + "".join(body[len(body) // 3:])
    assert answer(s) == ans
    return "1\n" + s + "\n"


def build_cases():
    fixed = [
        "1\naa\n",                         # 最小
        "1\n00\n",
        "1\naAabb\n",                      # 区分大小写：a 恰 2 次（不区分会得 b）
        "2\nbaba\nZzYyZY\n",               # 多个 2 次字符：取靠前的而非字典序最小
        "1\naaabb\n",                      # 出现 3 次的不算
        "1\naaaabcbc\n",                   # 出现 4 次（偶数）的不算
        "3\nxyzxzy\n9ab9\nAbcdefghijklmnopqrstuvwxyzA\n",
        "1\n" + ALPHA + ALPHA[::-1] + "\n",  # 62 个字符都恰 2 次，答案 a
        "1\n" + "a" * 3 + "B" * 5 + "1" * 7 + "c" + "Q" + "Q" + "c" * 4 + "\n",
    ]
    cases = [SAMPLE_IN] + fixed
    r = random.Random(4106)
    for i in range(12):
        cases.append(multi_case(r, r.randint(5, 30), 2, 40))
    for i in range(4):
        cases.append(multi_case(r, r.randint(5, 30), 2, 40, alpha="abcABC012"))
    for i in range(4):
        cases.append(multi_case(r, r.randint(50, 200), 50, 400))
    cases.append(multi_case(r, 60000, 2, 6, alpha="abAB01"))   # 大量短串
    cases.append(multi_case(r, 30000, 10, 25))
    cases.append(long_early(r, 900000))
    cases.append(long_early(r, 500000))
    cases.append(long_late(r, 900000))
    cases.append(long_late(r, 600000))
    cases.append(long_late(r, 200000))
    while len(cases) < 40:
        cases.append(multi_case(r, r.randint(1, 10), 2, 15))
    return cases


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN and solve(SAMPLE_IN) == SAMPLE_OUT
    assert len(set(cases)) == len(cases)
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for i, c in enumerate(cases):
        assert valid(c), i
        (root / f"{i}.in").write_text(c)
        (root / f"{i}.out").write_text(solve(c))


if __name__ == "__main__":
    main()
