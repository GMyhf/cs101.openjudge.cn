import random, re, subprocess, sys, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def min_houses_to_buy(W, n, prices):\n    min_length = n + 1  # 初始化为最大长度+1，表示不可能的情况\n    current_sum = 0     # 当前窗口的价格总和\n    left = 0            # 窗口的左边界\n\n    # 遍历房屋价格数组\n    for right in range(n):\n        current_sum += prices[right]  # 扩展窗口的右边界\n\n        # 当当前总和大于等于W时，尝试缩小窗口的大小\n        while current_sum >= W and left <= right:\n            min_length = min(min_length, right - left + 1)\n            current_sum -= prices[left]  # 缩小窗口的左边界\n            left += 1\n\n    # 如果min_length没有更新，说明没有找到满足条件的窗口\n    return min_length if min_length <= n else 0\n\n# 读取输入\nW, n = map(int, input().split())\nprices = list(map(int, input().split()))\n\n# 计算结果并打印\nprint(min_houses_to_buy(W, n, prices))\n\n'
SAMPLE_IN = '7 6\n1 3 5 2 1 4\n'
SAMPLE_OUT = '2\n'


def valid(text):
    """题面：两行；第一行 W n（0<W<10^9, 0<n<10^5，空格分开）；第二行 n 个整数 pi（0<pi<10^5）。"""
    lines = text.split("\n")
    if len(lines) != 3 or lines[2] != "":
        return False
    head = lines[0].split(" ")
    if len(head) != 2 or not all(re.fullmatch(r"[1-9]\d*", t) for t in head):
        return False
    w, n = map(int, head)
    if not (0 < w < 10**9 and 0 < n < 10**5):
        return False
    ps = lines[1].split(" ")
    return len(ps) == n and all(re.fullmatch(r"[1-9]\d*", t) and int(t) < 10**5 for t in ps)


def old_case(r):
    n = r.randint(2, 35); prices = [r.randint(1, 99999) for _ in range(n)]
    total = sum(prices)
    w = total + r.randint(1, 1000) if r.random() < .2 else r.randint(1, total)
    return f"{w} {n}\n" + " ".join(map(str, prices)) + "\n"


def fmt(w, prices):
    return f"{w} {len(prices)}\n" + " ".join(map(str, prices)) + "\n"


def build_cases():
    cases, seen = [SAMPLE_IN], [SAMPLE_IN]
    for index in range(1, 9):                         # 原随机小数据保留前 8 组
        for attempt in range(100):
            content = old_case(random.Random(24678 + index + attempt * 1000))
            if content not in seen: break
        seen.append(content); cases.append(content)
    r = random.Random(246780)
    N = 99999
    cases.append(fmt(5, [5]))                         # n=1，恰好够
    cases.append(fmt(6, [5]))                         # n=1，不够 -> 0
    cases.append(fmt(15, [1, 2, 3, 4, 5]))            # 需要全买，总和恰等于 W
    p = [r.randint(1, 99999) for _ in range(1000)]
    cases.append(fmt(sum(p) + 1, p))                  # 全买也不够 -> 0
    cases.append(fmt(99999, [1] * 500 + [99999] + [1] * 499))   # 单套即可
    # 大规模
    p = [r.randint(1, 99999) for _ in range(N)]
    cases.append(fmt(999999999, p))                   # 答案约 2 万，前缀和超 32 位
    p = [r.randint(1, 9999) for _ in range(N)]
    cases.append(fmt(sum(p[50:]), p))                 # 答案接近 n，卡 O(n*答案)
    p = [r.randint(1, 9999) for _ in range(N)]
    cases.append(fmt(999999999, p))                   # 总和 < W -> 0
    p = [r.choice([1, 1, 1, 1, 99999]) for _ in range(N)]
    cases.append(fmt(r.randint(10**8, 5 * 10**8), p))
    p = [1] * N
    cases.append(fmt(N, p))                           # 全 1，W=n -> n
    p = [r.randint(1, 99999) for _ in range(N)]
    cases.append(fmt(r.randint(1, 99999), p))         # W 很小，答案 1 或 2
    return cases


def main():
    cases = build_cases()
    assert len(cases) == 20 and len(set(cases)) == 20 and all(valid(c) for c in cases)
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        for index, content in enumerate(cases):
            result = subprocess.run([sys.executable, handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            if index == 0: assert result.stdout == SAMPLE_OUT
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
