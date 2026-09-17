#!/usr/bin/env python3
"""2109C3 Hacking Numbers (Hard Version) -- hidden-data generator, contract and build.

Written for this repository as a hand-off artifact; no external source, no external license.
The same file serves 2109C1 / C2 / C3; only PROBLEM below differs.

Hidden data (read by interactor.py, shown in the "run sample" box), the statement's Hacks format:
    t                1 <= t <= 5000
    n x              t lines; n = target given to the program, x = the unknown integer,
                     1 <= n, x <= 1e9
.out lists the per-test command limit (C1: 7, C2: 4, C3: f(n) = 2 if n == 81 else 3), one per
line; the interactor does not read it.

Case 0 is the statement's example: test 1 has x = 9, n = 100; test 2 has x = 1234, n = 5.

Shapes are chosen around how strategies go wrong (all reduce x first, then add n - c):
  * assuming two "digit" leave a single digit (really up to 16): x with S(S(x)) in 9..16;
  * binary descent missing a step (add -8/-4/-2 without -1): x with S(S(x)) even;
  * "digit, mul 9, digit" (S(9*S(x)) can be 18): x with S(x) in {11, 21, 22, ...};
  * "mul 9, digit" with one digit only (S(9x) up to 81);
  * other nine-strings ("mul 99999999, digit" is not constant);
  * spending a no-op "add 0" when n equals the constant: n = 1, 9, 81 (C3: f(81) = 2);
  * extremes x, n in {1, 1e9}, x = n, powers of ten and 10^k - 1, t = 5000 for speed.
Build: every case passes valid(), the reference (samplecode.py) is run through
judge.run_interactive against interactor.py and must be accepted, and every naive strategy in
NAIVE that is wrong for this version must be rejected by at least one case (checked by an
in-process simulation of the jury).
"""
from __future__ import annotations

import random
import re
import sys
import tempfile
from pathlib import Path

PROBLEM = "2109C3"

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
REFERENCE = HERE / "samplecode.py"
INTERACTOR_REL = f"tests/codeforces/{PROBLEM}_made/interactor.py"
SAMPLE = "2\n100 9\n5 1234\n"
MAX_T, MAX_V, BIG = 5000, 10 ** 9, 10 ** 18
SPECIAL_N = [1, 2, 8, 9, 10, 16, 17, 18, 72, 80, 81, 82, 100, 999, 1000,
             99999999, 100000000, 999999998, 999999999, 1000000000]


def limit_for(n):
    if PROBLEM == "2109C1":
        return 7
    if PROBLEM == "2109C2":
        return 4
    return 2 if n == 81 else 3


# ---------------------------------------------------------------- contract

LINE_INT = r"(?:[1-9][0-9]*)"


def valid(text):
    if not re.fullmatch(rf"{LINE_INT}\n(?:{LINE_INT} {LINE_INT}\n)*", text):
        return False
    lines = text.split("\n")[:-1]
    t = int(lines[0])
    if not 1 <= t <= MAX_T or len(lines) != t + 1:
        return False
    for line in lines[1:]:
        n, x = map(int, line.split())
        if not (1 <= n <= MAX_V and 1 <= x <= MAX_V):
            return False
    return len(text.encode()) <= 1024 * 1024


def parse(text):
    nums = list(map(int, text.split()))
    return [(nums[1 + 2 * i], nums[2 + 2 * i]) for i in range(nums[0])]


def fmt(pairs):
    return f"{len(pairs)}\n" + "".join(f"{n} {x}\n" for n, x in pairs)


# ---------------------------------------------------------------- generators

def S(v):
    return sum(map(int, str(v)))


def uniform(r):
    return r.randint(1, MAX_V)


def log_uniform(r):
    """Random number of digits (1..10), then a uniform value with that many digits (<= 1e9)."""
    k = r.randint(1, 10)
    return MAX_V if k == 10 else r.randint(10 ** (k - 1), 10 ** k - 1)


def with_digit_sum(r, s):
    """A number < 1e9 (9 digit slots) whose digit sum is s, 1 <= s <= 81."""
    digits = [0] * 9
    left = s
    while left:
        i = r.randrange(9)
        if digits[i] < 9:
            digits[i] += 1
            left -= 1
    return int("".join(map(str, digits)))


def edgy_x(r):
    return r.choice([1, 2, 9, 10, 11, 99, 100, 999999999, 1000000000, 999999997, 899999999,
                     123456789, 987654321, 10 ** r.randint(0, 9), 10 ** r.randint(1, 9) - 1])


SUM_DD_HIGH = [s for s in range(1, 82) if S(s) >= 9]           # S(S(x)) in 9..16
SUM_DD_EVEN = [s for s in range(1, 82) if S(s) % 2 == 0]
SUM_9TRAP = [s for s in range(1, 82) if S(9 * s) != 9]         # S(x) with S(9*S(x)) = 18


def generate(seed, attempt=0):
    base = {"2109C1": 1, "2109C2": 2, "2109C3": 3}[PROBLEM]
    r = random.Random(2109_000_000 + base * 1_000_003 + seed * 7919 + attempt * 104729)
    T = MAX_T
    if seed == 1:
        return fmt([(1, 1)])
    if seed == 2:
        return fmt([(MAX_V, MAX_V)])
    if seed == 3:
        return fmt([(1, 999999999)])
    if seed == 4:
        return fmt([(81, MAX_V)])
    if seed == 5:      # uniform
        return fmt([(uniform(r), uniform(r)) for _ in range(T)])
    if seed == 6:      # n = 81 everywhere (C3: only 2 commands allowed)
        return fmt([(81, r.choice([uniform(r), log_uniform(r), edgy_x(r)])) for _ in range(T)])
    if seed == 7:      # exhaustive small n x small x
        return fmt([(n, x) for n in range(1, 101) for x in range(1, 51)])
    if seed == 8:      # S(S(x)) >= 9, small n
        return fmt([(1 + i % 20, with_digit_sum(r, r.choice(SUM_DD_HIGH))) for i in range(T)])
    if seed == 9:      # every digit sum 1..81 for x
        return fmt([(log_uniform(r), with_digit_sum(r, 1 + i % 81)) for i in range(T)])
    if seed == 10:     # x = n
        pairs = []
        for _ in range(T):
            v = r.choice([uniform(r), log_uniform(r), r.choice(SPECIAL_N)])
            pairs.append((v, v))
        return fmt(pairs)
    if seed == 11:     # "digit, mul 9, digit" trap
        return fmt([(log_uniform(r), with_digit_sum(r, r.choice(SUM_9TRAP))) for _ in range(T)])
    if seed == 12:     # n = 1e9
        return fmt([(MAX_V, r.choice([uniform(r), edgy_x(r)])) for _ in range(T)])
    if seed == 13:     # powers of ten and neighbours for x, special n
        xs = sorted({v for k in range(10) for v in (10 ** k - 1, 10 ** k, 10 ** k + 1)
                     if 1 <= v <= MAX_V})
        return fmt([(SPECIAL_N[i % len(SPECIAL_N)], xs[(i // len(SPECIAL_N)) % len(xs)])
                    for i in range(T)])
    if seed == 14:     # special n, random x
        return fmt([(r.choice(SPECIAL_N), r.choice([uniform(r), edgy_x(r)])) for _ in range(T)])
    if seed == 15:     # x = 1..5000
        return fmt([(T + 1 - x, x) for x in range(1, T + 1)])
    if seed == 16:     # x near 1e9, n near 1
        return fmt([(1 + i, MAX_V - i) for i in range(T)])
    if seed == 17:     # log-uniform
        return fmt([(log_uniform(r), log_uniform(r)) for _ in range(T)])
    if seed == 18:     # n in the digit-sum range 1..81, S(S(x)) even (descent missing -1)
        return fmt([(r.randint(1, 81), with_digit_sum(r, r.choice(SUM_DD_EVEN))) for _ in range(T)])
    if seed == 19:     # n = 9 and n = 1 (constants of the C2 / C1 approaches)
        return fmt([(r.choice([1, 9]), r.choice([uniform(r), edgy_x(r), log_uniform(r)]))
                    for _ in range(T)])
    if seed == 20:     # mixed, t = 2500
        pairs = []
        for _ in range(2500):
            kind = r.randrange(5)
            n = r.choice([uniform(r), log_uniform(r), r.choice(SPECIAL_N)])
            if kind == 0:
                x = with_digit_sum(r, r.randint(1, 81))
            elif kind == 1:
                x = edgy_x(r)
            elif kind == 2:
                x = n
            else:
                x = r.choice([uniform(r), log_uniform(r)])
            pairs.append((n, x))
        return fmt(pairs)
    raise ValueError(seed)


# ---------------------------------------------------------------- naive strategies (simulated)

def descent(n, steps):
    return [("digit",), ("digit",)] + [("add", -s) for s in steps] + [("add", n - 1)]


NAIVE = {
    # name: (commands for target n, versions where the strategy is wrong)
    "digit x2 then assume <= 8 (add -4 -2 -1)": (lambda n: descent(n, [4, 2, 1]), {"2109C1", "2109C2", "2109C3"}),
    "digit x2, descent without add -1": (lambda n: descent(n, [8, 4, 2]), {"2109C1", "2109C2", "2109C3"}),
    "digit, mul 9, digit": (lambda n: [("digit",), ("mul", 9), ("digit",), ("add", n - 9)], {"2109C1", "2109C2", "2109C3"}),
    "mul 9, one digit": (lambda n: [("mul", 9), ("digit",), ("add", n - 9)], {"2109C1", "2109C2", "2109C3"}),
    "mul 99999999, digit": (lambda n: [("mul", 99999999), ("digit",), ("add", n - 72)], {"2109C1", "2109C2", "2109C3"}),
    "mul 999999999, digit, add n-81 even for n=81": (lambda n: [("mul", 999999999), ("digit",), ("add", n - 81)], {"2109C3"}),
    "C1 approach (7 commands)": (lambda n: descent(n, [8, 4, 2, 1]), {"2109C2", "2109C3"}),
    "C2 approach (mul 9, digit, digit, add)": (lambda n: [("mul", 9), ("digit",), ("digit",)] + ([("add", n - 9)] if n != 9 else []), {"2109C3"}),
}


def simulate(commands, n, x):
    if len(commands) > limit_for(n):
        return False
    for command in commands:
        if command[0] == "digit":
            x = S(x)
            continue
        op, y = command
        if op == "add" and 1 <= x + y <= BIG:
            x += y
        elif op == "mul" and 1 <= x * y <= BIG:
            x *= y
    return x == n


# ---------------------------------------------------------------- build

def run_reference(text, workdir):
    sys.path.insert(0, str(ROOT))
    import judge
    command, failure = judge.prepare_program(Path(workdir), "python3", REFERENCE.read_text())
    if failure is not None:
        raise SystemExit(f"reference does not prepare: {failure}")
    answer = "".join(f"{limit_for(n)}\n" for n, _ in parse(text))
    result = judge.run_interactive(command, INTERACTOR_REL, text.encode(), answer.encode(), Path(workdir),
                                   cpu_seconds=4, address_space_bytes=768 * 1024 * 1024,
                                   file_size_bytes=2 * 1024 * 1024)
    return answer, result


def build():
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    cases = [SAMPLE]
    for seed in range(1, 21):
        attempt = 0
        case = generate(seed)
        while case in cases:
            attempt += 1
            case = generate(seed, attempt)
        cases.append(case)
    caught = {name: 0 for name in NAIVE}
    for index, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"case {index}: violates input contract")
        pairs = parse(case)
        for name, (strategy, wrong_in) in NAIVE.items():
            if PROBLEM in wrong_in and not all(simulate(strategy(n), n, x) for n, x in pairs):
                caught[name] += 1
        with tempfile.TemporaryDirectory(prefix="c2109-") as workdir:
            answer, result = run_reference(case, workdir)
        if result["outcome"] != "accepted":
            raise SystemExit(f"case {index}: reference {result['outcome']}: {result['message']}")
        print(f"case {index}: t={len(pairs)} accepted in {result['time_ms']} ms")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")
    for name, (_, wrong_in) in NAIVE.items():
        if PROBLEM in wrong_in:
            print(f"naive '{name}': rejected by {caught[name]} cases")
            if caught[name] == 0:
                raise SystemExit(f"naive strategy '{name}' is not rejected by any case")


if __name__ == "__main__":
    build()
