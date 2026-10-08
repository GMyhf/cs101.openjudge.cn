import random, subprocess, sys, tempfile
from pathlib import Path

import string

def valid(text):
    # 题面：每组两个字符串，以任意空白分隔；只能核格式（题面没给长度上限）
    toks = text.split()
    if not toks or len(toks) % 2:
        return False
    return all(t.isascii() and t.isprintable() for t in toks)

ALNUM = string.ascii_letters + string.digits

def rand_str(r, n, alpha):
    return "".join(r.choice(alpha) for _ in range(n))

def sep(r):
    return r.choice([" ", " ", "   ", "\t", " \t  ", "          "])

def build_cases():
    r = random.Random(1458)
    cases = []
    # 小规模随机（小字母表，答案分布散）
    for _ in range(14):
        pairs = [(rand_str(r, r.randint(1, 25), "abcde"), rand_str(r, r.randint(1, 25), "abcde"))
                 for _ in range(r.randint(1, 6))]
        cases.append(pairs)
    # 边界：单字符相等/不等、完全相同、子序列、无公共字符、逆序
    cases.append([("a", "a"), ("a", "b"), ("z", "zzzz"), ("ab", "ba")])
    s = rand_str(r, 60, "abc"); cases.append([(s, s), (s, s[::-1]), (s, s[::3])])
    cases.append([(rand_str(r, 40, "abcdef"), rand_str(r, 40, "uvwxyz")), ("0123456789", "9876543210")])
    cases.append([("x", rand_str(r, 300, "abcdefghijklmnopqrstuvwy")), (rand_str(r, 300, "ab"), "b")])
    # 中等规模
    for alpha in ["ab", "ACGT", string.ascii_lowercase, ALNUM, "ab", "abcdefgh"]:
        pairs = [(rand_str(r, r.randint(50, 200), alpha), rand_str(r, r.randint(50, 200), alpha))
                 for _ in range(r.randint(3, 8))]
        cases.append(pairs)
    # 大规模：长度到 500，卡掉无记忆化的指数递归
    for alpha in ["ab", "ACGT", string.ascii_lowercase, ALNUM, "abc"]:
        pairs = [(rand_str(r, 500, alpha), rand_str(r, 500, alpha))]
        pairs += [(rand_str(r, r.randint(400, 500), alpha), rand_str(r, r.randint(400, 500), alpha))
                  for _ in range(5)]
        cases.append(pairs)
    big = rand_str(r, 500, "abcd")
    cases.append([(big, big), (big, "".join(c for c in big if c != "a")), (big[::-1], big)])
    # 一大一小、多组短串混合
    cases.append([(rand_str(r, 500, "ab"), rand_str(r, 3, "ab")) for _ in range(6)])
    cases.append([(rand_str(r, r.randint(1, 8), "abc"), rand_str(r, r.randint(1, 8), "abc")) for _ in range(200)])
    while len(cases) < 39:
        cases.append([(rand_str(r, r.randint(100, 300), "abcde"), rand_str(r, r.randint(100, 300), "abcde")) for _ in range(4)])
    return ["".join(a + sep(r) + b + "\n" for a, b in pairs) for pairs in cases]

REFERENCE='# External reference: http://cs101.openjudge.cn/practice/01458/statistics/\n# Accepted submission: 51703529\n# Source: http://cs101.openjudge.cn/practice/solution/51703529/\n# License: not declared on the submission page; no license is inferred.\n\nwhile True:\n    try:\n        sa, sb = input().split()\n        m, n = len(sa), len(sb)\n        dp = [[0]*(n+1) for _ in range(m+1)]\n        for i in range(1, m+1):\n            for j in range(1, n+1):\n                if sa[i-1] == sb[j-1]:\n                    dp[i][j] = dp[i-1][j-1]+1\n                else:\n                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n        print(dp[m][n])\n    except EOFError:\n        break\n'
LANGUAGE='Python3'
SAMPLE='abcfbc         abfcab\nprogramming    contest\nabcd           mnp\n'

def run_all(cases):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp); src = tmp/('s.py' if LANGUAGE == 'Python3' else 's.cpp'); src.write_text(REFERENCE)
        cmd = [sys.executable, '-I', str(src)]
        if LANGUAGE != 'Python3':
            exe = tmp/'s'; subprocess.run(['g++', '-std=c++20', '-O2', '-pipe', str(src), '-o', str(exe)], check=True); cmd = [str(exe)]
        outs = []
        for x in cases:
            q = subprocess.run(cmd, input=x, text=True, capture_output=True, timeout=120, check=True)
            outs.append('\n'.join(line.rstrip() for line in q.stdout.rstrip().splitlines()) + '\n')
        return outs

def main():
    cases = [SAMPLE] + build_cases()
    for i, x in enumerate(cases):
        assert valid(x), f"第 {i} 组不满足题面约束"
    outs = run_all(cases)
    out = Path('data'); out.mkdir(exist_ok=True)
    for p in out.glob('*'): p.unlink()
    for i, (x, y) in enumerate(zip(cases, outs)):
        (out/f'{i}.in').write_text(x); (out/f'{i}.out').write_text(y)

if __name__ == '__main__':
    main()
