import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'def is_match(pattern, s):\n    m, n = len(pattern), len(s)\n    dp = [[False] * (n + 1) for _ in range(m + 1)]\n    \n    dp[0][0] = True  # 空模式匹配空串\n    \n    # 处理模式开头的 \'*\'\n    for i in range(1, m + 1):\n        if pattern[i - 1] == \'*\':\n            dp[i][0] = dp[i - 1][0]\n        else:\n            break  # 一旦出现非 \'*\'，后面不可能匹配空串\n    \n    for i in range(1, m + 1):\n        for j in range(1, n + 1):\n            if pattern[i - 1] == \'*\':\n                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]\n            elif pattern[i - 1] == \'?\' or pattern[i - 1] == s[j - 1]:\n                dp[i][j] = dp[i - 1][j - 1]\n    \n    return dp[m][n]\n\n\nif __name__ == "__main__":\n    pattern = input().strip()\n    s = input().strip()\n    \n    if is_match(pattern, s):\n        print("matched")\n    else:\n        print("not matched")'
SAMPLE = '1*456?\n11111114567\n'
GENERATOR_NAME = 'g6252'
# 题面：两行，每行一个不超过 20 个字符的字符串；第一行可含 ? 和 *，第二行不含通配符。
# 空行按「不是字符串」处理（按 token 读入的写法会读不到第二行）。
def valid(text):
    if not text.endswith("\n") or "\r" in text:
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    p, s = lines
    if not (1 <= len(p) <= 20 and 1 <= len(s) <= 20):
        return False
    if any(c.isspace() or not c.isprintable() for c in p + s):
        return False
    return "*" not in s and "?" not in s


def g6252(r):
    # 原始生成方式（第二行可能为空，已不再使用）
    p="".join(r.choice("abc*?") for _ in range(r.randint(2,10)))
    s="".join(r.choice("abc") for _ in range(r.randint(0,12)))
    return f"{p}\n{s}\n"


def instantiate(r, p, alpha, budget):
    """按模式造一个能匹配的串，长度不超过 budget；造不出返回 None。"""
    out = []
    for c in p:
        if c == "*":
            out.append("".join(r.choice(alpha) for _ in range(r.choice([0, 0, 1, 2, r.randint(0, 6)]))))
        elif c == "?":
            out.append(r.choice(alpha))
        else:
            out.append(c)
    s = "".join(out)
    return s if 1 <= len(s) <= budget else None


def g6252_hard(r, kind):
    alpha = r.choice(["abc", "ab", "0123456789", "1245678", "aA1"])
    plen = 20 if kind in ("max", "maxmis") else r.randint(1, 20)
    while True:
        star = r.choice([0.0, 0.1, 0.25, 0.5])
        q = r.choice([0.0, 0.1, 0.3])
        p = "".join("*" if r.random() < star else "?" if r.random() < q else r.choice(alpha) for _ in range(plen))
        if kind == "allstar":
            p = "*" * r.randint(1, 20)
        s = instantiate(r, p, alpha, 20)
        if s is None:
            continue
        if kind in ("mis", "maxmis"):
            # 在能匹配的串上做一次小改动，多数会变成不匹配
            op = r.choice(["sub", "ins", "del"])
            i = r.randrange(len(s))
            if op == "sub":
                s = s[:i] + r.choice(alpha.replace(s[i], "") or alpha) + s[i + 1:]
            elif op == "ins" and len(s) < 20:
                s = s[:i] + r.choice(alpha) + s[i:]
            elif op == "del" and len(s) > 1:
                s = s[:i] + s[i + 1:]
        if kind == "max" and len(s) < 15:
            continue
        return f"{p}\n{s}\n"


FIXED = [
    "*\na\n",                      # 只有星号
    "?\na\n",                      # 单个问号
    "?\nab\n",                     # 问号只代一个字符
    "a\nb\n",
    "1?456\n1aa456\n",             # 题面描述中的反例
    "2*77?8\n237708\n",            # 题面描述中的正例
    "********************\n12345678901234567890\n",
    "????????????????????\n1234567890123456789\n",
    "*a*a*a*a*a*a*a*a*a*b\naaaaaaaaaaaaaaaaaaaa\n",   # 回溯写法的最坏情形
    "abc*\nab\n",
]


def build_cases():
    kinds = ["max", "max", "maxmis", "maxmis", "allstar"] + ["ok", "mis"] * 12
    cases = [SAMPLE] + FIXED
    for i, k in enumerate(kinds):
        for attempt in range(100):
            v = g6252_hard(random.Random(6252 * 100 + i + attempt * 1000), k)
            if v not in cases:
                cases.append(v)
                break
        else:
            raise AssertionError("生成器多样性不足")
    return cases


def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=build_cases()
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
