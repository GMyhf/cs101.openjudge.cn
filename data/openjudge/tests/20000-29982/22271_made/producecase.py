import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\nfrom collections import Counter\n\ndef main():\n    # 读取输入\n    input_data = sys.stdin.read().strip().split(\'\\n\')\n    N = int(input_data[0])  # 树的总数\n    tree_names = input_data[1:]  # 每棵树的种类名称\n\n    # 统计每种树的数量\n    tree_counter = Counter(tree_names)\n\n    # 按字典序排序\n    sorted_trees = sorted(tree_counter.items())\n\n    # 输出结果\n    for tree, count in sorted_trees:\n        percentage = (count / N) * 100\n        print(f"{tree} {percentage:.4f}%")\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE_IN = '4\nApple\nCherry\nPear\nPeach\n'
SAMPLE_OUT = 'Apple 25.0000% \nCherry 25.0000%\nPeach 25.0000%\nPear 25.0000%\n'
def generate_case(r):
    names = ["Oak", "Pine", "Birch", "Maple", "Cedar", "Elm"]; n = r.randint(5, 30); values = [r.choice(names) for _ in range(n)]
    assert 1 <= n <= 100000 and len(values) == n
    return str(n) + "\n" + "\n".join(values) + "\n"

import re
from collections import Counter
from fractions import Fraction

NAME_RE = re.compile(r"[A-Za-z ]{1,30}")

def valid(text):
    """题面：首行正整数 N（N<=100000）；随后 N 行，每行一个由不超过 30 个英文字母和空格组成的种类名称。"""
    if not text.endswith("\n"): return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit(): return False
    n = int(lines[0])
    if not 1 <= n <= 100000 or len(lines) != n + 1: return False
    return all(NAME_RE.fullmatch(x) for x in lines[1:])

def unambiguous(names):
    """百分比第 5 位小数恰为 5（四舍五入有歧义）或 count/N*100 与 count*100/N 打印不同的数据不要。"""
    n = len(names)
    for c in set(Counter(names).values()):
        if (Fraction(10 ** 6 * c, n) * 2).denominator == 1 and Fraction(10 ** 6 * c, n).denominator != 1: return False
        if f"{c / n * 100:.4f}" != f"{c * 100 / n:.4f}": return False
    return True

def extra_cases():
    """补充：N=1e5 满规模、名称含空格/大小写混排/前缀关系、最长 30 字符、N=1、单一种类（追加在原 20 组之后）。"""
    r = random.Random(222710); out = []
    UP, LO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"
    def word(lo, hi): return r.choice(UP + LO) + "".join(r.choice(LO + UP[:3]) for _ in range(r.randint(lo, hi) - 1))
    def name(maxlen):
        while True:
            parts = [word(1, 8) for _ in range(r.randint(1, 3))]
            s = " ".join(parts)
            if len(s) <= maxlen: return s
    def case(names):
        assert unambiguous(names)
        return f"{len(names)}\n" + "\n".join(names) + "\n"
    def pick(pool, n, skew):
        while True:
            names = [pool[min(len(pool) - 1, int(r.paretovariate(1.2)) - 1)] if skew else r.choice(pool) for _ in range(n)]
            if unambiguous(names): return names
    # 前缀/大小写/空格混排的易错名称
    tricky = ["Apple", "apple", "Apple tree", "Apple Tree", "Appletree", "A", "a", "Z", "z", "Ab", "AB", "aB", "Pine", "Pine Pine", "Pine x"]
    out.append(case(pick(tricky + [name(12) for _ in range(200)], 100000, True)))     # N=1e5（文件 < 1MB）
    out.append(case(pick([name(10) for _ in range(30000)], 100000, False)))            # N=1e5，约 2.9 万种
    long30 = []
    while len(long30) < 3000:
        s = name(30)
        if len(s) >= 25: long30.append((s + " " + word(1, 30))[:30].rstrip())
    out.append(case(pick(long30, 25000, False)))                                       # 名称接近 30 字符
    out.append(case(pick(tricky, 15, False)))
    out.append(case(tricky[:]))
    out.append(case(["Oak tree"]))                                                     # N=1
    out.append(case(["Birch"] * 99999))                                               # 单一种类 100.0000%
    out.append(case(["Pine"] * 2 + ["Oak"]))                                          # 66.6667% / 33.3333%
    out.append(case(["a b"] + ["ab"] * 6 + ["A B"]))                                   # 1/8 = 12.5000%
    out.append(case(pick([name(15) for _ in range(7)], 99991, False)))                 # 质数 N
    return out

def main():
    assert SAMPLE_IN == '4\nApple\nCherry\nPear\nPeach\n'
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(22271 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError('insufficient diversity')
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
        for index, content in enumerate(extra_cases(), start=20):
            assert valid(content) and content not in seen
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=30, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
    assert all(valid(c) for c in seen)

if __name__ == "__main__":
    main()
