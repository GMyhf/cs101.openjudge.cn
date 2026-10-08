"""20027 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 20027
SAMPLE_IN = 'a\n1\n'
SAMPLE_OUT = 'c\n'
REFERENCE_SOURCE = 'def str_to_num(s):\n    """将字符串s转换为对应的26进制数字（a->0, b->1, ...）"""\n    num = 0\n    for c in s:\n        num = num * 26 + (ord(c) - ord(\'a\'))\n    return num\n\ndef num_to_str(num, length):\n    """将数字num转换为固定长度length的26进制字符串"""\n    s = [\'a\'] * length\n    for i in range(length-1, -1, -1):\n        s[i] = chr((num % 26) + ord(\'a\'))\n        num //= 26\n    return "".join(s)\n\nif __name__ == \'__main__\':\n    a = input().strip()\n    k = int(input().strip())\n    num_a = str_to_num(a)\n    num_b = num_a + (k + 1)  # a 与 b 之间正好有 k 个字符串\n    b = num_to_str(num_b, len(a))\n    print(b)\n'

def _num(s):
    v = 0
    for c in s:
        v = v * 26 + ord(c) - 97
    return v


def valid(text):
    """题面：两行，第一行全小写字母串 a，第二行正整数 k；数据保证有解（a 之后至少还有 k+1 个同长串）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    a, k = lines
    if not a or not all("a" <= c <= "z" for c in a):
        return False
    if not k.isdigit() or k[0] == "0":
        return False
    return _num(a) + int(k) + 1 <= 26 ** len(a) - 1


def g20027(r): return "".join(r.choice("abc") for _ in range(r.randint(1,5)))+"\n"+str(r.randint(1,100))+"\n"


def _str(v, n):
    out = []
    for _ in range(n):
        out.append(chr(97 + v % 26))
        v //= 26
    return "".join(reversed(out))


def g_big(r, n, kmax):
    """长串 + 大 k，保证有解：k ≤ min(kmax, 剩余可用数)。"""
    total = 26 ** n
    while True:
        a = "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n))
        room = total - 1 - _num(a) - 1
        if room >= 1:
            k = r.randint(1, min(kmax, room))
            return a + "\n" + str(k) + "\n"


# 手工边界：结果恰为全 z、多位连续进位、k 很大
EXTRA = [
    "aaz\n10\n",                     # 题面样例 2
    "x\n1\n",                        # x -> z（恰好到头）
    "azzzzz\n1\n",                   # 连续进位 -> baaaab
    "azzzzzzzzzzzzzzzzzz\n1\n",      # 长串连续进位
    "a\n24\n",                       # 单字母最大 k
    "aaaaaaaaaaaaaaaaaaaa\n" + str(26 ** 20 - 2) + "\n",   # 恰好到 zzzz...z，k 超 64 位
    "mzzzzzzzzzzzzzzzzzzz\n" + str(10 ** 18) + "\n",
    "abcdefghijklmnopqrstuvwxyz\n999999999\n",
    "zzzzzzzzzzzzzzzzzzzw\n1\n",      # zzz..w +2 = zzz..y
]

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20027(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases and valid(value):
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    cases.extend(EXTRA)
    r = random.Random(NUMBER * 7 + 1)
    for n, kmax in [(8, 10 ** 9), (12, 10 ** 9), (15, 10 ** 18), (20, 10 ** 18),
                    (30, 10 ** 30), (50, 10 ** 60), (100, 10 ** 120), (200, 10 ** 250)]:
        cases.append(g_big(r, n, kmax))
    assert len(set(cases)) == len(cases)
    assert all(valid(c) for c in cases)
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
