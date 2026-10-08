import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "MOD = 10**9 + 7\n\nimport sys\n\ndef main():\n    data = sys.stdin.read().split()\n    it = iter(data)\n    N = int(next(it)); L = int(next(it)); M_val = int(next(it))\n    start = [int(next(it)) for _ in range(N)]\n    mid = [int(next(it)) for _ in range(N)]\n    end = [int(next(it)) for _ in range(N)]\n    \n    M = M_val\n    \n    # Precompute start_mod\n    start_mod = [0] * M\n    for x in start:\n        start_mod[x % M] += 1\n    \n    # Precompute mid_mod\n    mid_mod = [0] * M\n    for x in mid:\n        mid_mod[x % M] += 1\n    \n    # Precompute last_cost = mid + end\n    last_mod = [0] * M\n    for i in range(N):\n        cost = (mid[i] + end[i]) % M\n        last_mod[cost] += 1\n\n    # Convolution function\n    def convolve(a, b):\n        res = [0] * M\n        for i in range(M):\n            if a[i]:\n                ai = a[i]\n                for j in range(M):\n                    if b[j]:\n                        res[(i + j) % M] = (res[(i + j) % M] + ai * b[j]) % MOD\n        return res\n\n    # Identity kernel\n    identity = [0] * M\n    identity[0] = 1\n\n    if L == 2:\n        cur = start_mod[:]\n    else:\n        # Compute mid_mod^(L-2) under convolution\n        def power_conv(base, exp):\n            result = identity[:]\n            base = base[:]\n            while exp:\n                if exp & 1:\n                    result = convolve(result, base)\n                base = convolve(base, base)\n                exp //= 2\n            return result\n        \n        mid_power = power_conv(mid_mod, L - 2)\n        cur = convolve(start_mod, mid_power)\n    \n    # Now combine with last_mod\n    ans = 0\n    for r in range(M):\n        needed = (M - r) % M\n        ans = (ans + cur[r] * last_mod[needed]) % MOD\n    \n    print(ans)\n\nif __name__ == '__main__':\n    main()\n"
SAMPLE_IN = '2 3 13\n4 6\n2 1\n3 4\n'
def valid(text):
    """题面契约：恰四行；首行 N L M，1<=N<=10^6，2<=L<=10^5，2<=M<=100；
    其后三行各 N 个整数，0<=cost<=M。"""
    import re
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if len(lines) != 4:
        return False
    num = re.compile(r'0|[1-9][0-9]*')
    rows = []
    for line in lines:
        parts = line.split(' ')
        if not all(num.fullmatch(p) for p in parts):
            return False
        rows.append([int(p) for p in parts])
    if len(rows[0]) != 3:
        return False
    n, layers, mod = rows[0]
    if not (1 <= n <= 10 ** 6 and 2 <= layers <= 10 ** 5 and 2 <= mod <= 100):
        return False
    return all(len(row) == n and all(0 <= x <= mod for x in row) for row in rows[1:])

def _case(r, n, layers, mod, kind='rand'):
    if kind == 'zero':
        rows = [[r.choice((0, mod)) for _ in range(n)] for _ in range(3)]
    elif kind == 'max':
        rows = [[mod] * n for _ in range(3)]
    elif kind == 'few':
        vals = [r.randint(0, mod) for _ in range(2)]
        rows = [[r.choice(vals) for _ in range(n)] for _ in range(3)]
    else:
        rows = [[r.randint(0, mod) for _ in range(n)] for _ in range(3)]
    return f"{n} {layers} {mod}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + "\n"

def generate_case(r, index):
    if index == 1: return "1 2 2\n1\n0\n1\n"
    if index == 2: return _case(r, 1, 100000, 100)
    if index == 3: return "3 2 5\n5 5 5\n5 5 5\n5 5 5\n"
    if index <= 14:   # 小规模，可暴力枚举
        return _case(r, r.randint(1, 5), r.randint(2, 6), r.randint(2, 12), r.choice(['rand', 'rand', 'few', 'zero']))
    if index <= 22:   # 中等规模
        return _case(r, r.randint(100, 2000), r.randint(2, 2000), r.randint(2, 100))
    # data/ 合计须 <= 10MB：N 贴近单个 .in 1MB 上限的只留 23、24、31 三组，其余 N 缩小（L 仍取上限附近）
    if index <= 30:   # L 取上限附近、M 取大：卡 O(L*M^2) 朴素 DP
        mod = r.choice([100, 100, 97, r.randint(50, 100)])
        n = r.randint(60000, 85000) if index <= 24 else r.randint(20000, 30000)
        return _case(r, n, r.randint(99000, 100000) if index < 29 else 100000, mod)
    if index <= 34:   # M 一位数时 N 可以更大
        return _case(r, 150000 if index == 31 else 50000, r.randint(90000, 100000), r.randint(2, 9))
    if index == 35: return _case(r, 30000, 100000, 100, 'max')      # 全部代价 = M -> N^L
    if index == 36: return _case(r, 30000, 99999, 100, 'zero')
    if index == 37: return _case(r, 80000, 100000, 2, 'few')
    if index == 38: return _case(r, 1000, 2, 100)                   # L=2 边界
    return _case(r, 1000, 3, 100)

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(40):
            if index == 0:
                content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(29741 + index + attempt * 1000), index)
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content), index
            assert len(content) <= 1 << 20, index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == '__main__':
    main()
