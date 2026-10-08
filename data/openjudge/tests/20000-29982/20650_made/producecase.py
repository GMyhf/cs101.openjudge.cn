"""20650 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 33 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 20650
SAMPLE_IN = 'ABCBDAB\nBDCABA\n'
SAMPLE_OUT = '4\n'
REFERENCE_SOURCE = 'def longest_common_subsequence(s1, s2):\n    dp = [[0 for _ in range(len(s2)+1)] for _ in range(len(s1)+1)]\n    for i in range(len(s1)):\n        for j in range(len(s2)):\n            if s1[i] == s2[j]:\n                dp[i+1][j+1] = dp[i][j] + 1\n            else:\n                dp[i+1][j+1] = max(dp[i+1][j], dp[i][j+1])\n    return dp[len(s1)][len(s2)]\n\ns1 = input()\ns2 = input()\nprint(longest_common_subsequence(s1, s2))\n'

def g20650(r):
    return "".join(r.choice("ABCDE") for _ in range(r.randint(2,20)))+"\n"+"".join(r.choice("ABCDE") for _ in range(r.randint(2,20)))+"\n"

def valid(text):
    """题面：一共两行，分别是两个序列（字符数组）。题面未给长度上限与字符集，
    这里只核格式：恰好两行、每行非空、行内不含空白字符。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    return len(lines) == 2 and all(line and not any(c.isspace() for c in line) for line in lines)


def extra_cases():
    """补充：原 20 组长度都 <=20、字符集只有 ABCDE，指数级枚举子序列也能过，且没有答案为 0、
    单字符、完全相同、一方是另一方子序列等边界。题面没给长度上限（内存 10MB），规模取到 500。"""
    r = random.Random(NUMBER)
    rnd = lambda k, alpha: "".join(r.choice(alpha) for _ in range(k))
    out = [
        "A\nA\n",                                   # 最小规模，答案 1
        "A\nB\n",                                   # 最小规模，答案 0
        "ABCABC\nXYZXYZ\n",                         # 无公共字符，答案 0
        "HELLOWORLD\nHELLOWORLD\n",                 # 完全相同
        "ACEGIKMOQS\nABCDEFGHIJKLMNOPQRST\n",       # 前者是后者的子序列
        "ZYXWVUTSRQ\nQRSTUVWXYZ\n",                 # 逆序，答案 1
        rnd(40, "AB") + "\n" + rnd(40, "AB") + "\n",  # 卡指数级枚举
        rnd(60, "ABCDEFGHIJ") + "\n" + rnd(55, "ABCDEFGHIJ") + "\n",
        rnd(200, "ACGT") + "\n" + rnd(180, "ACGT") + "\n",
        rnd(500, "ABCDEFGHIJKLMNOPQRSTUVWXYZ") + "\n" + rnd(500, "ABCDEFGHIJKLMNOPQRSTUVWXYZ") + "\n",
        rnd(500, "AB") + "\n" + rnd(499, "AB") + "\n",
        "A" * 500 + "\n" + "B" * 499 + "A" + "\n",   # 答案 1，长串
        rnd(500, "abcXYZ019") + "\n" + rnd(300, "abcXYZ019") + "\n",
    ]
    return out


def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20650(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    for value in extra_cases():
        assert value not in cases
        cases.append(value)
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
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
