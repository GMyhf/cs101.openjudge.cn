import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import heapq\nimport sys\n\ndef main():\n    data = sys.stdin.read().split()\n    n = int(data[0])\n    A = list(map(int, data[1:1+n]))\n    \n    lo = []  # max-heap: store negative values\n    hi = []  # min-heap\n    \n    result = []\n    \n    for i, num in enumerate(A):\n        # Push to lo first\n        heapq.heappush(lo, -num)\n        \n        # Move the largest in lo to hi to maintain order\n        heapq.heappush(hi, -heapq.heappop(lo))\n        \n        # If hi has more elements, move smallest back to lo\n        if len(hi) > len(lo):\n            heapq.heappush(lo, -heapq.heappop(hi))\n        \n        # After processing odd number of elements (1st, 3rd, 5th, ...)\n        if i % 2 == 0:  # 0-indexed: i=0 -> 1 element, i=2 -> 3 elements, etc.\n            median = -lo[0]\n            result.append(str(median))\n    \n    print("\\n".join(result))\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE_IN = '7\n1 3 5 7 9 11 6\n'
SAMPLE_OUT = '1\n3\n5\n6\n'
def generate_case(r):
    n = r.choice([5, 7, 9, 11, 21, 51]); values = [r.randint(0, 1000) for _ in range(n)]
    assert n % 2 == 1 and all(0 <= x <= 10**9 for x in values)
    return f"{n}\n" + " ".join(map(str, values)) + "\n"

N_MAX = 100000


def valid(text):
    """题面：第 1 行正整数 N（N<=100000）；第 2 行 N 个非负整数 A_i（A_i<=1e9）。N 未保证为奇数。"""
    try:
        lines = text.split('\n')
        while lines and lines[-1].strip() == '':
            lines.pop()
        if len(lines) != 2 or len(lines[0].split()) != 1:
            return False
        n = int(lines[0])
        if not 1 <= n <= N_MAX:
            return False
        a = lines[1].split()
        return len(a) == n and all(0 <= int(v) <= 10**9 for v in a)
    except ValueError:
        return False


def fmt(values):
    return f"{len(values)}\n" + " ".join(map(str, values)) + "\n"


def specials():
    r = random.Random(21509)
    big = lambda: [r.randint(0, 10**9) for _ in range(N_MAX)]
    return [
        fmt([10**9]),                                         # N=1，取值上界
        fmt([0, 7]),                                          # N 为偶数：只输出前 1 个
        fmt([5, 0, 5, 3]),                                    # 偶数 N、含 0 与重复
        fmt([r.randint(0, 10**9) for _ in range(3000)]),      # 偶数 N=3000
        fmt([r.randint(0, 10) for _ in range(2999)]),         # 大量重复值
        fmt(big()),                                           # N=1e5 满规模随机
        fmt(sorted(big())),                                   # 升序
        fmt(sorted(big(), reverse=True)[:N_MAX - 1]),         # 降序，N=99999
        fmt([12345678] * N_MAX),                              # 全相等
        fmt([r.choice([0, 10**9]) for _ in range(N_MAX - 1)]),   # 只有两种极值
    ]


def main():
    assert SAMPLE_IN == '7\n1 3 5 7 9 11 6\n'
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        contents = []
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(21509 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError('insufficient diversity')
            seen.append(content)
            contents.append(content)
        contents += specials()
        assert all(valid(c) for c in contents) and len(set(contents)) == len(contents)
        for index, content in enumerate(contents):
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
