#!/usr/bin/env python3
"""Codeforces 2254F Whiplash -- generator, input contract, oracle and build.

Statement: t (1<=t<=1e4) tests; each has even n (2<=n<=2e5), arrays a,b of n
non-negative integers < 2^30; sum of n <= 2e5.  Operation: pick i, XOR all other
a[j] with a[i].  Determine if a -> b.

Solution: extend a with xor(a) to get multiset of size n+1; same for b.
a -> b iff the two multisets are equal.

Shapes:
  0   Problem samples (6 test cases).
  1   n=2 edge cases: a==b, a!=b, zeros.
  2   Many small n=2..6 random tests packed together.
  3   a==b (always YES).
  4   All zeros (always YES).
  5   Single element differs (often NO).
  6   Large values near 2^30.
  7   n=2e5, random (stress).
  8   n=2e5, a and b are permutations of each other with same XOR.
  9   Structured: a[i] = i, b constructed to be YES.
  10  Many n=4 tests, mix of YES/NO.
  11  n=2e5, all same value.
  12  t=1e4 tests with n=2 (sum n = 2e4).
  13  n=2e5, a has one element different from b.
  14  Random with controlled XOR to make YES.
  15  n=2e5, a and b have same multiset but different XOR sums (NO).
  16  n=2e5, high bit patterns.
  17  Mixed structured tests.
  18  n=2e5, a[i] = b[i] ^ constant.
  19  Boundary: n=2, max values.
"""
from __future__ import annotations
import random
import subprocess
import sys
from pathlib import Path

SAMPLE = (
    "6\n"
    "2\n1 2\n1 0\n"
    "4\n1 2 4 7\n6 7 5 3\n"
    "4\n1 2 4 8\n8 4 2 1\n"
    "4\n1 2 3 4\n1 2 4 5\n"
    "4\n1 2 0 3\n3 3 0 3\n"
    "6\n3 5 6 9 10 12\n6 5 3 12 15 9\n"
)
SAMPLE_OUT = "NO\nYES\nYES\nNO\nNO\nYES\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def oracle(text):
    """Compute answer using the same logic as the reference solution."""
    data = text.split()
    t = int(data[0]); pos = 1; out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = [int(data[pos + i]) for i in range(n)]; pos += n
        b = [int(data[pos + i]) for i in range(n)]; pos += n
        xa = 0
        for x in a:
            xa ^= x
        xb = 0
        for x in b:
            xb ^= x
        c = sorted([x ^ xa for x in a] + [xa])
        d = sorted([x ^ xb for x in b] + [xb])
        out.append("YES" if c == d else "NO")
    return "\n".join(out) + "\n"


def valid(text):
    """Check input constraints."""
    data = text.split()
    if not data:
        return False
    t = int(data[0])
    if not (1 <= t <= 10000):
        return False
    pos = 1
    total_n = 0
    for _ in range(t):
        n = int(data[pos]); pos += 1
        if n < 2 or n > 200000 or n % 2 != 0:
            return False
        total_n += n
        if total_n > 200000:
            return False
        for i in range(n):
            if not (0 <= int(data[pos + i]) < (1 << 30)):
                return False
        pos += n
        for i in range(n):
            if not (0 <= int(data[pos + i]) < (1 << 30)):
                return False
        pos += n
    return pos == len(data)


def generate(seed, attempt=0):
    """Generate a test case based on seed."""
    r = random.Random(2254_000_000 + seed * 7919 + attempt * 31)

    if seed == 1:
        # n=2 edge cases
        cases = [
            (2, [0, 0], [0, 0]),
            (2, [1, 1], [1, 1]),
            (2, [1, 2], [1, 0]),
            (2, [5, 5], [0, 0]),
            (2, [3, 7], [7, 3]),
        ]
        idx = attempt % len(cases)
        n, a, b = cases[idx]
        return f"1\n{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"

    elif seed == 2:
        # Many small n=2..6 random tests
        count = r.randint(10, 50)
        lines = [str(count)]
        for _ in range(count):
            n = r.choice([2, 4, 6])
            a = [r.randint(0, 15) for _ in range(n)]
            b = [r.randint(0, 15) for _ in range(n)]
            lines.append(str(n))
            lines.append(" ".join(map(str, a)))
            lines.append(" ".join(map(str, b)))
        return "\n".join(lines) + "\n"

    elif seed == 3:
        # a == b (always YES)
        n = r.choice([2, 4, 10, 100])
        a = [r.randint(0, 1000) for _ in range(n)]
        return f"1\n{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, a))}\n"

    elif seed == 4:
        # All zeros
        n = r.choice([2, 4, 100, 1000])
        a = [0] * n
        b = [0] * n
        return f"1\n{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"

    elif seed == 5:
        # Single element differs
        n = r.choice([2, 4, 10])
        a = [r.randint(0, 100) for _ in range(n)]
        b = a[:]
        idx = r.randint(0, n - 1)
        b[idx] = r.randint(0, 100)
        return f"1\n{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"

    elif seed == 6:
        # Large values near 2^30
        n = r.choice([2, 4, 10])
        a = [r.randint((1 << 29), (1 << 30) - 1) for _ in range(n)]
        b = [r.randint((1 << 29), (1 << 30) - 1) for _ in range(n)]
        return f"1\n{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"

    elif seed == 7:
        # n=2e5, random (stress)
        n = 200000
        a = [r.randint(0, (1 << 30) - 1) for _ in range(n)]
        b = [r.randint(0, (1 << 30) - 1) for _ in range(n)]
        return f"1\n{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"

    elif seed == 8:
        # n=2e5, a and b are permutations with same XOR
        n = 200000
        a = [r.randint(0, 1000000) for _ in range(n)]
        b = a[:]
        r.shuffle(b)
        return f"1\n{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"

    elif seed == 9:
        # Structured: a[i] = i, b constructed to be YES
        n = r.choice([4, 10, 100])
        a = list(range(n))
        xa = 0
        for x in a:
            xa ^= x
        c = [x ^ xa for x in a] + [xa]
        c_sorted = sorted(c)
        b_ext = c_sorted[:n]
        b = b_ext
        return f"1\n{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"

    elif seed == 10:
        # Many n=4 tests
        count = r.randint(20, 100)
        lines = [str(count)]
        for _ in range(count):
            n = 4
            a = [r.randint(0, 100) for _ in range(n)]
            b = [r.randint(0, 100) for _ in range(n)]
            lines.append(str(n))
            lines.append(" ".join(map(str, a)))
            lines.append(" ".join(map(str, b)))
        return "\n".join(lines) + "\n"

    elif seed == 11:
        # All same value
        n = 200000
        v = r.randint(0, 1000000)
        a = [v] * n
        b = [v] * n
        return f"1\n{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"

    elif seed == 12:
        # t=1e4 tests with n=2
        count = 10000
        lines = [str(count)]
        for _ in range(count):
            n = 2
            a = [r.randint(0, 1000) for _ in range(n)]
            b = [r.randint(0, 1000) for _ in range(n)]
            lines.append(str(n))
            lines.append(" ".join(map(str, a)))
            lines.append(" ".join(map(str, b)))
        return "\n".join(lines) + "\n"

    elif seed == 13:
        # n=2e5, one element different
        n = 200000
        a = [r.randint(0, 1000000) for _ in range(n)]
        b = a[:]
        idx = r.randint(0, n - 1)
        b[idx] = r.randint(0, 1000000)
        return f"1\n{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"

    elif seed == 14:
        # Random with controlled XOR to make YES
        n = r.choice([4, 10, 100])
        a = [r.randint(0, 1000) for _ in range(n)]
        xa = 0
        for x in a:
            xa ^= x
        c = [x ^ xa for x in a] + [xa]
        c_sorted = sorted(c)
        b_ext = c_sorted[:n]
        b = b_ext
        r.shuffle(b)
        return f"1\n{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"

    elif seed == 15:
        # Same multiset but different XOR sums (NO)
        n = 200000
        a = [r.randint(0, 1000000) for _ in range(n)]
        b = a[:]
        r.shuffle(b)
        if n > 2:
            b[0] = b[0] ^ 1
            b[1] = b[1] ^ 1
        return f"1\n{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"

    elif seed == 16:
        # High bit patterns
        n = r.choice([4, 10, 100])
        a = [r.randint(0, (1 << 30) - 1) for _ in range(n)]
        b = [r.randint(0, (1 << 30) - 1) for _ in range(n)]
        return f"1\n{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"

    elif seed == 17:
        # Mixed structured tests
        count = r.randint(10, 50)
        lines = [str(count)]
        for _ in range(count):
            n = r.choice([2, 4, 6, 8])
            a = [r.randint(0, 100) for _ in range(n)]
            if r.random() < 0.5:
                b = a[:]
                r.shuffle(b)
            else:
                b = [r.randint(0, 100) for _ in range(n)]
            lines.append(str(n))
            lines.append(" ".join(map(str, a)))
            lines.append(" ".join(map(str, b)))
        return "\n".join(lines) + "\n"

    elif seed == 18:
        # a[i] = b[i] ^ constant
        n = 200000
        const = r.randint(0, 1000000)
        a = [r.randint(0, 1000000) for _ in range(n)]
        b = [x ^ const for x in a]
        return f"1\n{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"

    elif seed == 19:
        # n=2, max values
        a = [(1 << 30) - 1, (1 << 30) - 2]
        b = [(1 << 30) - 3, (1 << 30) - 4]
        return f"1\n2\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"

    else:
        # Default: random
        n = r.choice([2, 4, 6, 10, 20])
        a = [r.randint(0, 1000) for _ in range(n)]
        b = [r.randint(0, 1000) for _ in range(n)]
        return f"1\n{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"


def build():
    out = Path(__file__).with_name("data")
    out.mkdir(exist_ok=True)
    cases = [SAMPLE]
    for seed in range(1, 40):
        attempt = 0
        case = generate(seed, attempt)
        while case in cases:
            attempt += 1
            case = generate(seed, attempt)
        cases.append(case)

    for index, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"invalid {index}")
        answer = subprocess.run(
            [sys.executable, str(REFERENCE)],
            input=case,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        if answer != oracle(case):
            raise SystemExit(f"oracle disagreement {index}")
        if index == 0 and answer.split() != SAMPLE_OUT.split():
            raise SystemExit(f"第 0 组与题面样例输出不符：{answer!r} != {SAMPLE_OUT!r}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")
    print(f"Generated {len(cases)} test cases")


if __name__ == "__main__":
    build()
