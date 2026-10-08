import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def max_concurrent_connections(n, intervals):\n    events = []\n    for start, end in intervals:\n        events.append((start, 1))  # 开始 +1\n        events.append((end, -1))   # 结束 -1\n\n    # 按时间排序，时间相同时结束事件在前\n    events.sort(key=lambda x: (x[0], x[1]))\n\n    current = 0\n    max_concurrent = 0\n    for time, delta in events:\n        current += delta\n        max_concurrent = max(max_concurrent, current)\n\n    return max_concurrent\n\n# 主程序处理多组数据\nt = int(input())\nfor _ in range(t):\n    n = int(input())\n    intervals = [tuple(map(int, input().split())) for _ in range(n)]\n    print(max_concurrent_connections(n, intervals))\n\n\n'
SAMPLE_IN = '2\n2\n1 2\n2 3\n2\n1 3\n2 4\n'
SAMPLE_OUT = '1\n2\n'
def generate_case(r):
    rows = []
    for _ in range(r.randint(2, 8)):
        intervals = []
        for _ in range(r.randint(2, 12)):
            x = r.randint(0, 100); intervals.append((x, x + r.randint(1, 30)))
        rows.append([str(len(intervals))] + [f"{x} {y}" for x, y in intervals])
    return str(len(rows)) + "\n" + "\n".join("\n".join(row) for row in rows) + "\n"

import re
INT = re.compile(r"0|[1-9][0-9]*")

def valid(text):
    """题面契约：第一行 t (t<=100)；每组第一行 n (1<=n<=100)，接下来 n 行两个整数 x y，0<=x<y<=10^9。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not INT.fullmatch(lines[0]):
        return False
    t = int(lines[0])
    if not 1 <= t <= 100:
        return False
    p = 1
    for _ in range(t):
        if p >= len(lines) or not INT.fullmatch(lines[p]):
            return False
        n = int(lines[p]); p += 1
        if not 1 <= n <= 100 or p + n > len(lines):
            return False
        for line in lines[p:p + n]:
            parts = line.split(" ")
            if len(parts) != 2 or not all(INT.fullmatch(x) for x in parts):
                return False
            x, y = map(int, parts)
            if not 0 <= x < y <= 10**9:
                return False
        p += n
    return p == len(lines)

def _fmt(groups):
    return str(len(groups)) + "\n" + "".join(f"{len(g)}\n" + "".join(f"{x} {y}\n" for x, y in g) for g in groups)

def extra_cases():
    r = random.Random(253020)
    cases = []
    cases.append(_fmt([[(0, 10**9)]]))  # 最小：t=1, n=1，端点取到值域两端
    # 首尾相接的链（答案 1）、完全相同区间（答案 n）、严格嵌套（答案 n）、同点开始/结束混合
    chain = [(i * 10**7, (i + 1) * 10**7) for i in range(100)]
    r.shuffle(chain)
    same = [(123456789, 987654321)] * 100
    nest = [(i, 10**9 - i) for i in range(100)]
    r.shuffle(nest)
    touch = [(5, 6)] * 50 + [(6, 7)] * 50
    r.shuffle(touch)
    cases.append(_fmt([chain, same, nest, touch, [(0, 1)], [(999999999, 10**9), (0, 999999999)]]))
    # t=100，每组 n=100，大值域随机
    groups = []
    for _ in range(100):
        g = []
        for _ in range(100):
            x = r.randint(0, 10**9 - 1); g.append((x, r.randint(x + 1, min(10**9, x + r.choice([10, 10**6, 10**9])))))
        groups.append(g)
    cases.append(_fmt(groups))
    # t=100，小值域密集，大量端点重合
    groups = []
    for _ in range(100):
        g = []
        for _ in range(r.randint(1, 100)):
            x = r.randint(0, 20); g.append((x, r.randint(x + 1, 21)))
        groups.append(g)
    cases.append(_fmt(groups))
    # t=100，大值域上端点重合（坐标为 10^8 的倍数）
    groups = []
    for _ in range(100):
        g = []
        for _ in range(100):
            x = r.randint(0, 9); g.append((x * 10**8, r.randint(x + 1, 10) * 10**8))
        groups.append(g)
    cases.append(_fmt(groups))
    return cases

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        extras = extra_cases()  # 末尾若干组：边界与满规模（catalog 固定 20 组）
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            elif index >= 20 - len(extras):
                content = extras[index - (20 - len(extras))]
                assert content not in seen, index
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(25302 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            seen.append(content)
            assert valid(content), index
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
