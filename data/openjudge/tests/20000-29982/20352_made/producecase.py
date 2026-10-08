"""20352 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 20352
SAMPLE_IN = '4\nababcdefgabdefab ab\naaaaaaaaa a\naaaaaaaaa aaa \n112123323 a\n'
SAMPLE_OUT = '0 2 9 14\n0 1 2 3 4 5 6 7 8\n0 3 6\nno\n'
# 原参考解（geeksforgeeks 的「朴素匹配」改写）失配时 i = i+j+1 直接跳过，会漏掉匹配：
# 例如 s1="aab", s2="ab" 应输出 1，它输出 no。改成从左到右贪心、找到一处后跳过 len(s2) 的写法。
REFERENCE_SOURCE = """\
def search(pat, txt):
    res = []
    i = txt.find(pat)
    while i != -1:
        res.append(str(i))
        i = txt.find(pat, i + len(pat))
    return res


n = int(input())
for _ in range(n):
    txt, pat = input().split()
    ans = search(pat, txt)
    if ans:
        print(' '.join(ans))
    else:
        print('no')
"""

# 题面：第一行整数 n；接下来 n 行，每行两个不带空格的字符串 s1 s2（题面样例第 3 行末尾带一个空格，
# 故允许行末空格）。题面未给 n 与串长的范围。


def valid(text):
    import re
    if not text.endswith("\n") or text.endswith("\n\n"):
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*", lines[0]):
        return False
    n = int(lines[0])
    if len(lines) != n + 1:
        return False
    return all(re.fullmatch(r"[!-~]+ [!-~]+ *", line) for line in lines[1:])


def _rs(r, alpha, k):
    return "".join(r.choice(alpha) for _ in range(k))


# 手工边界：s2==s1、s2 比 s1 长、奇数长 aa、重叠 aba、失配后不能整段跳过（aab/ab、aaab/aab）、
# 首尾位置命中、单字符串
_EDGE = ["aaaaa aa", "ababa aba", "aab ab", "aaab aab", "abcabc abcabc", "ab abc", "a a", "a b",
         "xyzxyz z", "zzzx zx", "abababab abab", "aaaaaaaab aaab", "mississippi issi", "mississippi ss",
         "0101010 010", "12121212 1212", "baaaaab aab", "cacacb cacb"]


def g20352(r, seed):
    if seed == 1:
        return f"{len(_EDGE)}\n" + "\n".join(_EDGE) + "\n"
    x = []
    if seed <= 5:      # 原来的形状
        for _ in range(r.randint(1, 5)):
            x.append(_rs(r, "abc", r.randint(4, 16)) + " " + _rs(r, "abc", r.randint(1, 3)))
    elif seed <= 10:   # 小字母表、多行：大量重叠与失配回退
        for _ in range(r.randint(20, 100)):
            alpha = r.choice(("ab", "ab", "abc", "01"))
            p = _rs(r, alpha, r.randint(1, 5))
            t = "".join(p if r.random() < .3 else r.choice(alpha) for _ in range(r.randint(1, 40)))
            x.append(t + " " + p)
    elif seed <= 13:   # 周期串：s1 = p 的若干次重复（中间夹杂扰动），s2 = p 的一部分重复
        for _ in range(r.randint(5, 20)):
            p = _rs(r, "ab", r.randint(1, 4))
            t = "".join(p + (r.choice("ab") if r.random() < .1 else "") for _ in range(r.randint(10, 500)))
            x.append(t + " " + (p * r.randint(1, 3))[: r.randint(1, 3 * len(p))])
    elif seed <= 16:   # 长串
        for _ in range(r.randint(2, 5)):
            alpha = r.choice(("ab", "abc", "abcdefghij"))
            p = _rs(r, alpha, r.randint(1, 8))
            t = "".join(p if r.random() < .2 else r.choice(alpha) for _ in range(r.randint(10000, 50000)))
            x.append(t + " " + p)
    else:              # 最长：s1 约 2*10^5，形如 a…ab，s2 = a^k b（失配回退最多的情形）
        k = r.choice((1, 2, 5, 30))
        t = "".join(("a" * r.randint(0, 2 * k)) + "b" for _ in range(200000 // (k + 1)))
        x.append(t + " " + "a" * k + "b")
        x.append("a" * 200000 + " " + "a" * r.choice((1, 2, 3, 7)))
    return str(len(x)) + "\n" + "\n".join(x) + "\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20352(random.Random(NUMBER + i + attempt * 1000), i)
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    return cases

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
