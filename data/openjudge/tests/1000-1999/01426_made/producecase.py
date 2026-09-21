#!/usr/bin/env python3
"""01426 Find The Multiple —— 生成器、输入契约、special judge 自检与数据构建。

题面：每行一个 n（1 <= n <= 200，镜像页里被 `<` 吃掉，见 `INPUT_DOMAIN`），读到 0 结束；
每个 n 输出一个只含 0/1、不超过 100 位的非零倍数，答案不唯一，判题走同目录 `checker.py`。

`.out` 是 `samplecode.py`（BFS，位数最少、数值最小）的输出，只是**一个**正确答案。

`SHAPES` 按「这题会怎么错」排：
  · `sweep_up` / `sweep_down` / `sweep_shuffled` —— 1..200 全扫，任何对某个 n 算错的都挂。
  · `long_answers`  —— 198（19 位）、99（18 位）、189、144 等最短答案最长的 n，
        搜索深度写死 18 位以内、或用 32 位整数存数的挂。
  · `pigeonhole_trap` —— 193、181、179 等：「1, 11, 111, … 里找两个同余」的鸽巢构造
        会给出 100 位以上的数，违反位数上限。
  · `powers_2_5`    —— 128、125、200 等只含 2/5 因子的 n，答案是 10 的幂或其倍数。
  · `already_binary` —— 1、10、11、101、110、111 本身就是 0/1 数。
  · `single_*`      —— 只有一个询问（198 / 1），不读到 0 就停或只处理首个的差别在这里看不出，
        放在一起是为了覆盖「一行一个就结束」的最小文件。
  · `random_mix`    —— 随机多重集。
  · `bulk`          —— 几千个询问，每个都现算 BFS 的写法要跑得动；`bulk_198` 每行都是最长答案。
  · `multiples_of_9` / `primes` —— 需要 9 个 1 的 n；素数 n 的最短答案位数分布最散。

构建时每组都要：参考解输出被 checker 接受；题面样例输出（第 0 组）被接受；
`ALTERNATIVES` 里几种不同的正确构造全部被接受且至少有一组与 `.out` 不同；
`WRONG` 里每个典型错解至少被拒一组。
"""
from __future__ import annotations
import random
import subprocess
import sys
import tempfile
from pathlib import Path

NUMBER = 1426
HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
CHECKER = HERE / "checker.py"
INPUT_DOMAIN = "The input file may contain multiple test cases. Each line contains a value of n (1 <= n <= 200). A line containing a zero terminates the input."
SAMPLE = "2\n6\n19\n0\n"
SAMPLE_OUT = "10\n100100100100100100\n111111111111111111\n"   # 题面「样例输出」逐字
MAX_N = 200
MAX_DIGITS = 100

PRIMES = [p for p in range(2, MAX_N + 1) if all(p % q for q in range(2, p))]


def _smallest(n, _cache={}):
    """与 samplecode 独立的朴素写法：按位数从小到大枚举 0/1 串，首位为 1。"""
    if n in _cache:
        return _cache[n]
    for length in range(1, MAX_DIGITS + 1):
        for bits in range(1 << (length - 1), 1 << length):
            if int(bin(bits)[2:]) % n == 0:
                _cache[n] = bin(bits)[2:]
                return _cache[n]
    raise AssertionError(n)


def _pigeonhole_digits(n):
    """鸽巢构造 R_{j-i}·10^i 的位数（j 即总位数）。"""
    seen, r = {}, 0
    for k in range(1, n + 2):
        r = (r * 10 + 1) % n
        if r == 0:
            return k
        if r in seen:
            return k
        seen[r] = k
    raise AssertionError(n)


PIGEONHOLE_TRAP = sorted(n for n in range(1, MAX_N + 1) if _pigeonhole_digits(n) > MAX_DIGITS)
LONG = sorted(range(1, MAX_N + 1), key=lambda n: -len(_smallest(n)))[:12]


def _render(ns):
    return "".join(f"{n}\n" for n in ns) + "0\n"


def generate(number, seed):
    assert number == NUMBER
    r = random.Random(number * 1_000_003 + seed)
    full = list(range(1, MAX_N + 1))
    if seed == 1:
        ns = full
    elif seed == 2:
        ns = full[::-1]
    elif seed == 3:
        ns = full * 2; r.shuffle(ns)
    elif seed == 4:
        ns = [r.choice(LONG) for _ in range(300)]
    elif seed == 5:
        ns = PIGEONHOLE_TRAP * 3; r.shuffle(ns)
    elif seed == 6:
        ns = [n for n in full if all(n % p for p in PRIMES if p not in (2, 5))]
        r.shuffle(ns)
    elif seed == 7:
        ns = [n for n in full if set(str(n)) <= {"0", "1"}] * 4; r.shuffle(ns)
    elif seed == 8:
        ns = [198]
    elif seed == 9:
        ns = [1]
    elif seed <= 13:
        ns = [r.randint(1, MAX_N) for _ in range(r.randint(1, 60 * seed))]
    elif seed <= 16:
        ns = [r.randint(1, MAX_N) for _ in range(r.randint(2000, 5000))]
    elif seed == 17:
        ns = [198] * 5000
    elif seed == 18:
        ns = list(range(9, MAX_N + 1, 9)) * 5; r.shuffle(ns)
    elif seed == 19:
        ns = PRIMES * 3; r.shuffle(ns)
    else:
        ns = [n for n in full if len(_smallest(n)) >= 10] + [1, 2, 5, 10, 199, 200]
        r.shuffle(ns)
    return _render(ns)


def valid(number, text):
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if lines[-1] != "0" or len(lines) < 2:
        return False
    return all(line.isascii() and line.isdigit() and str(int(line)) == line
               and 1 <= int(line) <= MAX_N for line in lines[:-1])


# ---- 另几种正确解（输出与参考解不同）与典型错解，构建时逐组过 checker ----

def _queries(text):
    ns = []
    for token in text.split():
        if int(token) == 0:
            break
        ns.append(int(token))
    return ns


def _largest(n, _cache={}):
    """不超过 100 位的最大 0/1 倍数：从最高位往下贪心，能放 1 就放 1。"""
    if n not in _cache:
        reach = [{0}]                      # reach[i]：只用最低 i 位能凑出的余数
        for i in range(MAX_DIGITS):
            p = pow(10, i, n)
            reach.append(reach[i] | {(x + p) % n for x in reach[i]})
        need, digits = 0, []
        for i in range(MAX_DIGITS - 1, -1, -1):
            want = (need - pow(10, i, n)) % n
            if want in reach[i]:
                digits.append("1"); need = want
            else:
                digits.append("0")
        _cache[n] = "".join(digits).lstrip("0")
    return _cache[n]


def _pigeonhole(n):
    seen, r = {}, 0
    for k in range(1, n + 2):
        r = (r * 10 + 1) % n
        if r == 0:
            return "1" * k
        if r in seen:
            j = seen[r]
            return "1" * (k - j) + "0" * j
        seen[r] = k


ALTERNATIVES = {
    "largest_100_digits": lambda n: _largest(n),
    "smallest_padded_to_100": lambda n: _smallest(n).ljust(MAX_DIGITS, "0"),
    "pigeonhole_or_smallest": lambda n: _pigeonhole(n) if len(_pigeonhole(n)) <= MAX_DIGITS else _smallest(n),
}
WRONG = {
    "pigeonhole_over_100_digits": lambda n: _pigeonhole(n),
    "depth_limit_18": lambda n: _smallest(n) if len(_smallest(n)) <= 18 else "1" * 18,
    "repunit_same_length": lambda n: "1" * len(_smallest(n)),
    "leading_zero_when_n_mod_7": lambda n: ("0" if n % 7 == 0 else "") + _smallest(n),
}
WRONG_WHOLE = {
    "first_query_only": lambda ns, f: f(ns[0]) + "\n" if ns else "",
    "stops_before_last": lambda ns, f: "".join(f(n) + "\n" for n in ns[:-1]),
}


def _run_solution(fn, text):
    return "".join(fn(n) + "\n" for n in _queries(text))


def check(case, output, answer):
    with tempfile.TemporaryDirectory() as temp:
        paths = []
        for name, data in (("in", case), ("out", output), ("ans", answer)):
            path = Path(temp) / name
            path.write_text(data, encoding="utf-8")
            paths.append(str(path))
        result = subprocess.run([sys.executable, "-I", str(CHECKER), *paths],
                                capture_output=True, timeout=30)
    if result.returncode not in (0, 42):
        raise SystemExit(f"checker 出错：{result.returncode} {result.stderr[-500:]!r}")
    return result.returncode == 0


def _build():
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    for path in out.glob("*"):
        path.unlink()
    cases = [SAMPLE] + [generate(NUMBER, seed) for seed in range(1, 40)]
    if len(set(cases)) != len(cases):
        raise SystemExit("两组输入撞了，数据必须互异")
    differs = dict.fromkeys(ALTERNATIVES, False)
    rejected = dict.fromkeys([*WRONG, *WRONG_WHOLE], 0)
    for index, case in enumerate(cases):
        if not valid(NUMBER, case):
            raise SystemExit(f"case {index} violates the input contract")
        answer = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                                capture_output=True, timeout=120, check=True).stdout
        if [len(x) for x in answer.split()] != [len(_smallest(n)) for n in _queries(case)]:
            raise SystemExit(f"case {index}: 参考解不是最短答案（与朴素枚举不符）")
        if not check(case, answer, answer):
            raise SystemExit(f"case {index}: 参考解输出被 checker 拒绝")
        if index == 0 and not check(case, SAMPLE_OUT, answer):
            raise SystemExit("题面样例输出被 checker 拒绝")
        for name, fn in ALTERNATIVES.items():
            output = _run_solution(fn, case)
            if not check(case, output, answer):
                raise SystemExit(f"case {index}: 正确解 {name} 被 checker 拒绝")
            differs[name] |= output != answer
        for name, fn in WRONG.items():
            rejected[name] += not check(case, _run_solution(fn, case), answer)
        for name, fn in WRONG_WHOLE.items():
            rejected[name] += not check(case, fn(_queries(case), _smallest), answer)
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")
    if not all(differs.values()):
        raise SystemExit(f"有正确解与 .out 完全相同，checker 没被真正考到：{differs}")
    if not all(rejected.values()):
        raise SystemExit(f"有错解一组都没被拒：{rejected}")
    print("wrong solutions rejected on:", rejected)


if __name__ == "__main__":
    _build()
