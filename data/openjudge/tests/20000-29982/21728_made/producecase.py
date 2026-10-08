import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def main():\n    n = int(input())\n    # Read experiment durations. There are n numbers.\n    durations = list(map(int, input().split()))\n    # Read the order of students. There are n numbers.\n    order = list(map(int, input().split()))\n\n    total_waiting_time = 0\n    current_time = 0\n    # Process students in the given order.\n    for student in order:\n        total_waiting_time += current_time\n        # Convert student id (1-indexed) to index (0-indexed)\n        current_time += durations[student - 1]\n\n    average_waiting_time = total_waiting_time / n\n    # Output the average waiting time rounded to two decimals.\n    print(f"{average_waiting_time:.2f}")\n\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE_IN = '10\n81 365 72 99 22 7 444 203 1024 203\n6 5 3 1 4 8 10 2 7 9\n'
SAMPLE_OUT = '431.90\n'
def generate_case(r):
    n = r.randint(2, 30); durations = [r.randint(1, 1000) for _ in range(n)]; order = list(range(1, n + 1)); r.shuffle(order)
    assert all(x > 0 for x in durations) and sorted(order) == list(range(1, n + 1))
    return f"{n}\n" + " ".join(map(str, durations)) + "\n" + " ".join(map(str, order)) + "\n"

def valid(text):
    """题面：输入 3 行。第一行 n（学生人数，n<=1000，此处要求 n>=1）；
    第二行 n 个整数 T1..Tn（时长，题面未给上界，这里只要求非负整数）；
    第三行 n 个整数 s1..sn，是 1..n 的一个排列（学生编号从 1 到 n）；数据间一个空格。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 3:
        return False

    def ints(line):
        toks = line.split(" ")
        if any(not t.isdigit() or (len(t) > 1 and t[0] == "0") for t in toks):
            return None
        return list(map(int, toks))

    a, t, o = ints(lines[0]), ints(lines[1]), ints(lines[2])
    if a is None or t is None or o is None or len(a) != 1:
        return False
    n = a[0]
    if not 1 <= n <= 1000 or len(t) != n or len(o) != n:
        return False
    return sorted(o) == list(range(1, n + 1))

def _exact_half(durations, order):
    """平均值恰好落在 x.xx5：四舍五入与二进制浮点的 half-even 结果可能不同，避开这种数据。"""
    n = len(order); cur = tot = 0
    for s in order:
        tot += cur; cur += durations[s - 1]
    return (tot * 200) % n == 0 and (tot * 100) % n != 0

def _fmt(durations, order):
    n = len(order)
    return f"{n}\n" + " ".join(map(str, durations)) + "\n" + " ".join(map(str, order)) + "\n"

def extra_case(k):
    r = random.Random(217280 + k)
    while True:
        if k == 0:
            d, o = [r.randint(1, 1000)], [1]                 # n=1，答案 0.00
        elif k == 1:
            d = [r.randint(1, 1000) for _ in range(2)]; o = [2, 1]
        elif k == 2:                                         # 顺序为恒等排列
            n = 1000; d = [r.randint(1, 1000) for _ in range(n)]; o = list(range(1, n + 1))
        elif k == 3:                                         # 逆序排列（按编号求和会错）
            n = 1000; d = [r.randint(1, 1000) for _ in range(n)]; o = list(range(n, 0, -1))
        elif k in (4, 5):                                    # 总等待时间超过 2^31（卡 32 位整型）
            n = 1000; d = [r.randint(4000, 5000) for _ in range(n)]; o = list(range(1, n + 1)); r.shuffle(o)
        elif k == 6:                                         # 时长有重复、含 0 以外的小值
            n = r.randint(500, 1000); d = [r.randint(1, 3) for _ in range(n)]; o = list(range(1, n + 1)); r.shuffle(o)
        elif k == 7:                                         # 平均值非整数，结尾需要补 0（如 x.10）
            n = 10; d = [r.randint(1, 1000) for _ in range(n)]; o = list(range(1, n + 1)); r.shuffle(o)
        else:
            n = r.choice([1000, r.randint(2, 1000)])
            d = [r.randint(1, 1024) for _ in range(n)]; o = list(range(1, n + 1)); r.shuffle(o)
        if not _exact_half(d, o):
            return _fmt(d, o)
        k += 100  # 换个随机流再试

def main():
    assert SAMPLE_IN == '10\n81 365 72 99 22 7 444 203 1024 203\n6 5 3 1 4 8 10 2 7 9\n'
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(40):
            if index == 0:
                content = SAMPLE_IN
            elif index < 20:
                for attempt in range(100):
                    content = generate_case(random.Random(21728 + index + attempt * 1000))
                    _, d_line, o_line = content.split("\n")[:3]
                    if content not in seen and not _exact_half(list(map(int, d_line.split())), list(map(int, o_line.split()))): break
                else: raise AssertionError('insufficient diversity')
            else:
                content = extra_case(index - 20)
                assert content not in seen, index
            assert valid(content), index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
