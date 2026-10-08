import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "def min_employees(tasks, t):\n    left, right = 1, max(tasks)\n    while left < right:\n        mid = (left + right) // 2\n        total_hours = sum((task + mid - 1) // mid for task in tasks)\n        if total_hours > t:\n            left = mid + 1\n        else:\n            right = mid\n    return left\n\n# 读取输入并处理\ntasks = list(map(int, input().split(',')))\nt = int(input())\nprint(min_employees(tasks, t))\n"
SAMPLE_IN = '1,2,5,9\n5\n'
SAMPLE_OUT = '5\n'
def generate_case(r):
    a = [r.randint(1, 50) for _ in range(r.randint(2, 20))]; t = r.randint(max(a), sum(a))
    assert all(x > 0 for x in a) and t >= max(a)
    return ",".join(map(str, a)) + "\n" + str(t) + "\n"

def valid(text):
    """题面：第一行逗号分隔的正整数数列（各任务工时），第二行一个正整数 t；
    保证有解：不考虑 t < 数列长度的情况，即 t >= len(数列)。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    def pos(x):
        return x.isdigit() and x.isascii() and x[0] != "0"
    parts = lines[0].split(",")
    if not parts or not all(pos(x) for x in parts) or not pos(lines[1]):
        return False
    return int(lines[1]) >= len(parts)


def extra_cases():
    """补充：原 20 组工时 <=50、n<=20，从 k=1 线性试到 max 也能过，且没有 t=n（答案=max）、
    t>=sum（答案=1）、单任务等边界。规模组用 n=5e4、工时到 1e9，答案在 1e8 量级，卡掉线性枚举 k。"""
    r = random.Random(20746)
    fmt = lambda a, t: ",".join(map(str, a)) + "\n" + str(t) + "\n"
    out = [
        fmt([1], 1), fmt([7], 1), fmt([7], 3), fmt([10, 10], 100),
        fmt([3, 9, 27], 3),          # t = n，答案 = max
        fmt([4, 4, 4, 4], 16),       # t = sum，答案 1
        fmt([1, 1, 1, 1000000000], 4),
        fmt([999999937, 1000000000], 5),
    ]
    for n, hi in [(100, 1000), (1000, 10**6), (10000, 10**9)]:
        a = [r.randint(1, hi) for _ in range(n)]
        out.append(fmt(a, r.randint(n, n * 3)))
    n = 50000
    a = [r.randint(1, 10**9) for _ in range(n)]
    out.append(fmt(a, n))                       # 答案 = max(a)
    a = [r.randint(1, 10**9) for _ in range(n)]
    out.append(fmt(a, n + 7))
    a = [r.randint(10**8, 10**9) for _ in range(n)]
    out.append(fmt(a, n * 5))
    a = [r.randint(1, 10**4) for _ in range(n)]
    out.append(fmt(a, sum(a)))                  # 答案 1
    a = [r.randint(1, 10**9) for _ in range(n)]
    # t 取 sum/5e4（约 5e8），答案约 5e4：仍卡线性枚举 k，同时 t 落在 32 位有符号整数内（题面未给值域，不额外要求 long long 读 t）
    out.append(fmt(a, sum(a) // 50000))
    return out


def main():
    assert SAMPLE_IN == '1,2,5,9\n5\n'
    cases = [SAMPLE_IN]
    for index in range(1, 20):
        for attempt in range(100):
            content = generate_case(random.Random(20746 + index + attempt * 1000))
            if content not in cases: break
        else: raise AssertionError('insufficient diversity')
        cases.append(content)
    for content in extra_cases():
        assert content not in cases
        cases.append(content)
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        root.mkdir(exist_ok=True)
        for index, content in enumerate(cases):
            assert valid(content), index
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
    assert (root / "0.out").read_text() == SAMPLE_OUT


if __name__ == "__main__":
    main()
