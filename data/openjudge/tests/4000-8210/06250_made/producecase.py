"""6250 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 40 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 6250
SAMPLE_IN = 'abcd123ab888efghij45ef67kl,ab,ef\n'
SAMPLE_OUT = '18\n'
REFERENCE_SOURCE = "# 23n2300017735(夏天明BrightSummer)\ndef find(s, pat):\n    nex = [0]\n    for i, p in enumerate(pat[1:], 1):\n        tmp = nex[i-1]\n        while True:\n            if p == pat[tmp]:\n                nex.append(tmp+1)\n                break\n            elif tmp:\n                tmp = nex[tmp-1]\n            else:\n                nex.append(0)\n                break\n    j = 0\n    for i, char in enumerate(s):\n        while True:\n            if char == pat[j]:\n                j += 1\n                if j == len(pat):\n                    return i\n                break\n            elif j:\n                j = nex[j-1]\n            else:\n                break\n\ns, p1, p2 = input().split(',')\ntry:\n    assert((ans := len(s)-find(s, p1)-find(s[::-1], p2[::-1])-2) >= 0)\n    print(ans)\nexcept (TypeError, AssertionError):\n    print(-1)\n"

def g6250(r):
    # S1/S2 用互不相交的字母表(xy/wv),填充串不含这四个字母:
    # 出现与否完全由构造决定,才能可靠制造 -1 分支(缺失/次序颠倒)
    filler = "abcdefghij0123456789"
    body = lambda: "".join(r.choice(filler) for _ in range(r.randint(3, 15)))
    s1 = "".join(r.choice("xy") for _ in range(r.randint(1, 3)))
    s2 = "".join(r.choice("wv") for _ in range(r.randint(1, 3)))
    roll = r.random()
    if roll < 0.15:
        s = body() + s2 + body()                     # S1 缺失 → -1
    elif roll < 0.30:
        s = body() + s2 + body() + s1 + body()       # 次序颠倒 → -1
    else:
        s = body() + s1 + body() + s2 + body()       # 正常跨距
    return f"{s},{s1},{s2}\n"

# 题面：一行 "S,S1,S2"，S 长度不超过 300，S1、S2 长度不超过 10，三者都不含逗号和空格。
def valid(text):
    if not text.endswith("\n"):
        return False
    body = text[:-1]
    if any(c in body for c in "\n\r \t"):
        return False
    parts = body.split(",")
    if len(parts) != 3:
        return False
    s, s1, s2 = parts
    return 1 <= len(s) <= 300 and 1 <= len(s1) <= 10 and 1 <= len(s2) <= 10 and body.isprintable()


def g6250_hard(r, kind):
    alpha = r.choice(["ab", "ab", "abc", "a", "xyz01"])
    rnd = lambda k: "".join(r.choice(alpha) for _ in range(k))
    if kind == "max":
        s = rnd(300); s1 = rnd(r.randint(1, 3)); s2 = rnd(r.randint(1, 3))
    elif kind == "long_pat":
        # 自重叠的长模式串：卡掉写错失配函数的 KMP
        unit = rnd(r.randint(1, 3))
        s1 = (unit * 10)[:10]; s2 = (rnd(2) * 5)[:r.randint(8, 10)]
        s = rnd(r.randint(0, 50)) + s1[:-1] + s1 + rnd(r.randint(0, 200)) + s2 + s2[1:] + rnd(r.randint(0, 20))
        s = s[:300]
    elif kind == "same":
        s1 = s2 = rnd(r.randint(1, 4))
        s = rnd(r.randint(1, 300))
    elif kind == "adjacent":
        s1 = rnd(r.randint(1, 10)); s2 = rnd(r.randint(1, 10))
        s = s1 + s2 if r.random() < 0.5 else rnd(r.randint(0, 5)) + s1 + s2
    elif kind == "cross":
        # S1 与 S2 只能交叉出现（如 aba 里找 ab 与 ba） → -1
        core = r.choice([("aba", "ab", "ba"), ("aaa", "aa", "aa"), ("abcab", "abca", "cab"), ("xyzxy", "xyzx", "zxy")])
        s, s1, s2 = core
        pad = "".join(r.choice("0123456789") for _ in range(r.randint(0, 100)))
        s = pad + s + pad[::-1]
    elif kind == "missing":
        s = rnd(r.randint(1, 300)); s1 = rnd(r.randint(1, 10)); s2 = "q" + rnd(r.randint(0, 9))
        if r.random() < 0.5:
            s1, s2 = s2, s1
    elif kind == "tiny":
        s = rnd(r.randint(1, 3)); s1 = rnd(r.randint(1, 2)); s2 = rnd(r.randint(1, 2))
    else:
        s = rnd(r.randint(1, 300)); s1 = rnd(r.randint(1, 6)); s2 = rnd(r.randint(1, 6))
    return f"{s},{s1},{s2}\n"


def build_cases():
    kinds = ["max", "max", "long_pat", "long_pat", "long_pat", "same", "same", "adjacent", "adjacent",
             "cross", "cross", "missing", "missing", "tiny", "tiny", "rand", "rand", "rand", "rand", "rand"]
    base = build_cases_base(); out = []
    for i, k in enumerate(kinds):
        for attempt in range(100):
            v = g6250_hard(random.Random(NUMBER * 100 + i + attempt * 1000), k)
            if v not in base + out:
                out.append(v)
                break
        else:
            raise AssertionError("生成器多样性不足")
    return base + out


def build_cases_base():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g6250(random.Random(NUMBER + i + attempt * 1000))
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
