"""14683 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 14683
SAMPLE_IN = '3 \n1 2 9\n'
SAMPLE_OUT = '15\n'
REFERENCE_SOURCE = 'import heapq\n\nn = int(input())\nl = list(map(int, input().split()))\nheapq.heapify(l)\nans = 0\n\nwhile len(l) > 1:\n    a = heapq.heappop(l)\n    b = heapq.heappop(l)\n    ans += a + b\n    heapq.heappush(l, a + b)\n\nprint(ans)\n'

def g14683(r):
    n = r.randint(2, 80); return f"{n}\n" + " ".join(str(r.randint(1, 10000)) for _ in range(n)) + "\n"

def huffman_cost(a):
    import heapq
    h = list(a); heapq.heapify(h); s = 0
    while len(h) > 1:
        x = heapq.heappop(h) + heapq.heappop(h); s += x; heapq.heappush(h, x)
    return s


def valid(text):
    """题面：两行；第一行 n (1<=n<=10000)；第二行 n 个整数 ai (1<=ai<=20000)，空格分隔；
    保证答案 < 2^31。题面样例第一行带行尾空格，故行尾空白放行。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    first = lines[0].split()
    if len(first) != 1 or not first[0].isdigit():
        return False
    n = int(first[0])
    a = lines[1].split()
    if not 1 <= n <= 10000 or len(a) != n or not all(x.isdigit() for x in a):
        return False
    a = list(map(int, a))
    if not all(1 <= x <= 20000 for x in a):
        return False
    return huffman_cost(a) < 2 ** 31


def fmt(a):
    return f"{len(a)}\n" + " ".join(map(str, a)) + "\n"


def designed():
    r = random.Random(NUMBER * 3)
    out = [[20000], [1], [7, 3], [20000, 20000], [5, 5, 5, 5, 5]]
    out.append([1] * 10000)
    out.append([r.randint(1, 20000) for _ in range(10000)])
    out.append([r.randint(1, 20000) for _ in range(10000)])
    out.append(list(range(10000, 0, -1)))
    out.append([r.randint(1, 3) for _ in range(10000)])
    out.append([2 ** (i % 15) for i in range(10000)])          # 1..16384 的幂次混排
    out.append(sorted(r.randint(1, 20000) for _ in range(10000)))
    out.append([1] * 9999 + [20000])
    # 答案贴近 2^31 上限：全等值 v，取最大的 v 使答案 < 2^31（卡 int 溢出的累加错法之外的边界）
    lo, hi = 1, 20000
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if huffman_cost([mid] * 10000) < 2 ** 31: lo = mid
        else: hi = mid - 1
    out.append([lo] * 10000)
    big = [20000] * 10000
    while huffman_cost(big) >= 2 ** 31:   # 从全 20000 起随机压低若干堆，直到答案刚好落进 2^31 以内
        for _ in range(25):
            big[r.randrange(10000)] = r.randint(1, 20000)
    out.append(big)
    return [fmt(a) for a in out]


def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g14683(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    cases += designed()   # 第 20 组起：n=1、满规模 n=10000、值域上界、答案贴近 2^31
    assert len(set(cases)) == len(cases)
    assert all(valid(c) for c in cases), "有数据越出题面约束"
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
