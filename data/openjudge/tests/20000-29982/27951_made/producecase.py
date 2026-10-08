import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'from collections import deque\n\nM, N = map(int, input().split())\nwords = list(map(int, input().split()))\n\nmemory = deque()\nlookups = 0\n\nfor word in words:\n    if word not in memory:\n        if len(memory) == M:\n            memory.popleft()\n        memory.append(word)\n        lookups += 1\n\nprint(lookups)\n'
SAMPLE_IN = '3 7\n1 2 1 5 4 4 1\n'
def valid(text):
    """题面：共 2 行，空格分隔；第一行正整数 M N（M<=100，N<=1000），第二行 N 个不超过 1000 的非负整数。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    def nums(line):
        parts = line.split(" ")
        if not all(x.isdigit() and x == str(int(x)) for x in parts):
            return None
        return list(map(int, parts))
    a, b = nums(lines[0]), nums(lines[1])
    if a is None or b is None or len(a) != 2:
        return False
    m, n = a
    return 1 <= m <= 100 and 1 <= n <= 1000 and len(b) == n and all(0 <= x <= 1000 for x in b)


def fmt(m, words):
    return f"{m} {len(words)}\n" + " ".join(map(str, words)) + "\n"


def generate_case(r):
    kind = r.random()
    if kind < .35:  # 小规模随机
        m = r.randint(1, 10); n = r.randint(1, 60); hi = r.randint(0, 30)
    elif kind < .7:  # 中等规模，字母表在 M 附近，FIFO 与 LRU 结果不同
        m = r.randint(1, 100); n = r.randint(100, 1000); hi = max(0, m + r.randint(-5, 30))
    else:  # 满规模
        m = r.randint(1, 100); n = 1000; hi = r.choice([m, m + 1, 2 * m, 1000])
    lo = r.choice([0, 0, max(0, 1000 - hi)])
    words = [r.randint(lo, min(1000, lo + hi)) for _ in range(n)]
    return fmt(m, words)


def fixed_cases(r):
    return [
        '3 8\n1 5 2 7 1 4 2 1\n',                             # 题面样例二，答案 7
        fmt(1, [0]),                                            # 最小规模
        fmt(100, [1000]),
        fmt(1, [r.choice([0, 1000]) for _ in range(1000)]),     # M=1，只有两个词
        fmt(100, [7] * 1000),                                   # 全是同一个词
        fmt(100, list(range(1000))),                            # 互不相同
        fmt(100, [i % 101 for i in range(1000)]),               # 101 个词循环：FIFO 每次都要查
        fmt(100, [i % 100 for i in range(1000)]),               # 恰好装满后全命中
        fmt(100, [r.randint(0, 1000) for _ in range(1000)]),    # 满规模、全值域
        fmt(3, [1, 2, 1, 3, 1, 4, 1, 5, 1, 6, 1, 7] * 80),      # 命中不刷新顺序（区分 LRU）
        fmt(50, [r.randint(0, 60) for _ in range(1000)]),
    ]


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        fixed = fixed_cases(random.Random(279510))
        for index in range(40):
            if index == 0: content = SAMPLE_IN
            elif index <= len(fixed): content = fixed[index - 1]
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(27951 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content), index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
