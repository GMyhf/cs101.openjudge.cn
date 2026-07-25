"""6250 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

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
REFERENCE_SOURCE = "# 23n2300017735(夏天明BrightSummer)\ndef find(s, pat):\n    nex = [0]\n    for i, p in enumerate(pat[1:], 1):\n        tmp = nex[i-1]\n        while True:\n            if p == pat[tmp]:\n                nex.append(tmp+1)\n                break\n            elif tmp:\n                tmp = nex[tmp-1]\n            else:\n                nex.append(0)\n                break\n    j = 0\n    for i, char in enumerate(s):\n        while True:\n            if char == pat[j]:\n                j += 1\n                if j == len(pat):\n                    return i\n                break\n            elif j:\n                j -= nex[j]\n            else:\n                break\n\ns, p1, p2 = input().split(',')\ntry:\n    assert((ans := len(s)-find(s, p1)-find(s[::-1], p2[::-1])-2) >= 0)\n    print(ans)\nexcept (TypeError, AssertionError):\n    print(-1)\n"

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

def build_cases():
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
