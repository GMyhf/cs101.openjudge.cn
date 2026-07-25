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
REFERENCE_SOURCE = "# https://www.geeksforgeeks.org/naive-algorithm-for-pattern-searching/\n# Naive Pattern Searching algorithm\ndef search(pat, txt):\n    M = len(pat)\n    N = len(txt)\n\n    res = []\n    # A loop to slide pat[] one by one */\n    #for i in range(N - M + 1):\n    i = 0\n    while i < N - M + 1:\n        j = 0\n\n        # For current index i, check\n        # for pattern match */\n        while(j < M):\n            if (txt[i + j] != pat[j]):\n                i = i+j + 1\n                break\n            j += 1\n\n        if (j == M):\n            res.append(str(i))\n            i += M\n\n    return res\n\n\nn = int(input())\nfor _ in range(n):\n    txt, pat = input().split()\n    ans = search(pat, txt)\n    if ans:\n        print(' '.join(ans))\n    else:\n        print('no')\n"

def g20352(r):
    x=[]
    for _ in range(r.randint(1,5)): x.append("".join(r.choice("abc") for _ in range(r.randint(4,16)))+" "+"".join(r.choice("abc") for _ in range(r.randint(1,3))))
    return str(len(x))+"\n"+"\n".join(x)+"\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20352(random.Random(NUMBER + i + attempt * 1000))
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
