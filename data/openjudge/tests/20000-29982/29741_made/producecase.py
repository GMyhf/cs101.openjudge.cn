import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "MOD = 10**9 + 7\n\nimport sys\n\ndef main():\n    data = sys.stdin.read().split()\n    it = iter(data)\n    N = int(next(it)); L = int(next(it)); M_val = int(next(it))\n    start = [int(next(it)) for _ in range(N)]\n    mid = [int(next(it)) for _ in range(N)]\n    end = [int(next(it)) for _ in range(N)]\n    \n    M = M_val\n    \n    # Precompute start_mod\n    start_mod = [0] * M\n    for x in start:\n        start_mod[x % M] += 1\n    \n    # Precompute mid_mod\n    mid_mod = [0] * M\n    for x in mid:\n        mid_mod[x % M] += 1\n    \n    # Precompute last_cost = mid + end\n    last_mod = [0] * M\n    for i in range(N):\n        cost = (mid[i] + end[i]) % M\n        last_mod[cost] += 1\n\n    # Convolution function\n    def convolve(a, b):\n        res = [0] * M\n        for i in range(M):\n            if a[i]:\n                ai = a[i]\n                for j in range(M):\n                    if b[j]:\n                        res[(i + j) % M] = (res[(i + j) % M] + ai * b[j]) % MOD\n        return res\n\n    # Identity kernel\n    identity = [0] * M\n    identity[0] = 1\n\n    if L == 2:\n        cur = start_mod[:]\n    else:\n        # Compute mid_mod^(L-2) under convolution\n        def power_conv(base, exp):\n            result = identity[:]\n            base = base[:]\n            while exp:\n                if exp & 1:\n                    result = convolve(result, base)\n                base = convolve(base, base)\n                exp //= 2\n            return result\n        \n        mid_power = power_conv(mid_mod, L - 2)\n        cur = convolve(start_mod, mid_power)\n    \n    # Now combine with last_mod\n    ans = 0\n    for r in range(M):\n        needed = (M - r) % M\n        ans = (ans + cur[r] * last_mod[needed]) % MOD\n    \n    print(ans)\n\nif __name__ == '__main__':\n    main()\n"
SAMPLE_IN = '2 3 13\n4 6\n2 1\n3 4\n'
def generate_case(r):
    n, layers, mod = r.randint(2, 6), r.randint(2, 7), r.randint(2, 10)
    rows = [[r.randint(0, mod) for _ in range(n)] for _ in range(3)]
    assert all(len(row) == n and all(0 <= x <= mod for x in row) for row in rows)
    return f"{n} {layers} {mod}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(29741 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
