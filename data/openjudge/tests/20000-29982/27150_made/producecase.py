#!/usr/bin/env python3
"""27150 Divisibility by Eight 加强版 —— 生成器、输入契约与数据构建（配 checker.py 特判）。

2026-09-17 重写。旧数据 21 组全是 NO，因为「有解时答案不唯一」而只敢出无解的情况，
判不出任何「把有解判成 NO」的错法。现在题目有了 checker.py，任何合法删法都接受，
于是有解/无解都出。

题面：一个不超过 200 万位、没有前导零的非负整数。删掉若干位（可以不删），剩下至少一位、
没有前导零（单独的 `0` 合法）、能被 8 整除；有则输出 YES 与结果，否则 NO。

判别力按「这题会怎么错」排（seed → 形状）：
  1-2   题面另外两个样例（`10` → 0、`111111` → NO）；第 0 组是 `3454`
  3-4   一位数输入：`0`（YES 0，忘了 0 本身是 8 的倍数的挂）、`4`（NO）
  5     9…92：唯一解族是三位 992（只查一二位的挂）
  6     2626…：偶数很多却无解（「有偶数就能凑」的挂）
  7     200 万位随机奇数：无解
  8     1…14514：解是 144/544，不是连续子串（只查连续窗口的挂）
  9-10  2 1…1 4 / 7 6…6 2：唯一解 24 / 72 的两位相隔 200 万位
  11    随机「刚好无解」前缀 + 一位，使解只能是三位子序列
  12    随机奇数中间夹一个 0：解要用到那个 0
  13    3…3 里撒三个 0 与一个 8：补前导零枚举（`000`、`008`）的挂
  14    随机数字且整个数被 8 整除：允许输出很长的结果（考 checker 的子序列检查）
  15-17 平台原数据形状 1222222222 循环（112）、5…56（56）、3…36（336）
  18    随机「刚好无解」（含偶数）200 万位
  19    4…42：无解
  20    3…38：唯一一位解在最末
参考解 samplecode.py 用「枚举 8 的倍数查子序列」；构建时用完全不同的线性状态机
（记录已出现的一位、两位子序列模 8 的余数）独立复核有无解，再逐组调用 checker：
参考解必须通过，另外构造两份不同的合法结果必须通过，几份错误输出必须被拒。
"""
from __future__ import annotations
import random
import subprocess
import sys
import tempfile
from pathlib import Path

NUMBER = 27150
HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
CHECKER = HERE / "checker.py"
INPUT_DOMAIN = "一个不超过200万位的非负整数，且没有前导零。"
MAX_DIGITS = 2_000_000
SAMPLE = "3454\n"
SAMPLE_OUT = "YES\n344\n"          # 题面样例 1 的输出（任何合法结果都行，checker 必须接受它）
OTHER_SAMPLES = (("10\n", "YES\n0\n"), ("111111\n", "NO\n"))


# ---------- 独立 oracle：线性状态机 ----------
def _step(state, digit):
    """state = (一位子序列集合, 两位子序列模 8 集合)；返回 (是否出现解, 新 state)。"""
    ones, twos = state
    if digit % 8 == 0:
        return True, state
    if any((10 * a + digit) % 8 == 0 for a in ones) or any((10 * v + digit) % 8 == 0 for v in twos):
        return True, state
    return False, (ones | {digit}, twos | frozenset((10 * a + digit) % 8 for a in ones))


def oracle_solvable(text):
    state, cache = (frozenset(), frozenset()), {}
    for ch in text.strip():
        key = (state, ch)
        if key not in cache:
            cache[key] = _step(state, int(ch))
        hit, state = cache[key]
        if hit:
            return True
    return False


def _no_answer_digits(r, length, weights):
    """逐位随机，只挑不会产生解的数字；首位非零。返回 (字符串, 末状态)。"""
    state, out, cache = (frozenset(), frozenset()), [], {}
    for _ in range(length):
        if state not in cache:
            allowed = [d for d in range(1, 10) if not _step(state, d)[0]]
            cache[state] = allowed
        allowed = cache[state]
        d = r.choices(allowed, [weights[x] for x in allowed])[0]
        out.append(d)
        state = _step(state, d)[1]
    return "".join(map(str, out)), state


def generate(number, seed):
    assert number == NUMBER
    r = random.Random(number * 1_000_003 + seed)
    big = MAX_DIGITS
    if seed <= 2:
        return OTHER_SAMPLES[seed - 1][0]
    if seed == 3:
        return "0\n"
    if seed == 4:
        return "4\n"
    if seed == 5:
        return "9" * (big - 1) + "2\n"
    if seed == 6:
        return "26" * (big // 2) + "\n"
    if seed == 7:
        return "".join(r.choice("13579") for _ in range(big)) + "\n"
    if seed == 8:
        return "1" * (big - 4) + "4514\n"
    if seed == 9:
        return "2" + "1" * (big - 2) + "4\n"
    if seed == 10:
        return "7" + "6" * (big - 2) + "2\n"
    if seed == 11:
        # 偶数权重压低，避免状态太快饱和；末位挑一个只能组成三位解的数字
        body, (ones, twos) = _no_answer_digits(r, 1_000_000, {1: 5, 2: 1, 3: 5, 4: 1, 5: 5, 6: 1, 7: 5, 9: 5})
        tails = [d for d in range(1, 10) if d % 8
                 and not any((10 * a + d) % 8 == 0 for a in ones)
                 and any((10 * v + d) % 8 == 0 for v in twos)]
        assert tails, "seed 11 的无解前缀找不到只能凑三位解的末位"
        return body + str(r.choice(tails)) + "\n"
    if seed == 12:
        half = big // 2
        return ("".join(r.choice("13579") for _ in range(half - 1)) + "0"
                + "".join(r.choice("13579") for _ in range(half)) + "\n")
    if seed == 13:
        chars = ["3"] * big
        for p in sorted(r.sample(range(1, big - 1), 3)):
            chars[p] = "0"
        chars[r.randrange(big // 2, big - 1)] = "8"
        return "".join(chars) + "\n"
    if seed == 14:
        length = 1_000_000
        head = str(r.randint(1, 9)) + "".join(r.choice("0123456789") for _ in range(length - 4))
        tail = r.choice([t for t in range(0, 1000, 8)])
        return head + f"{tail:03d}\n"
    if seed == 15:
        return "1222222222" * (big // 10) + "\n"
    if seed == 16:
        return "5" * (big - 1) + "6\n"
    if seed == 17:
        return "3" * (big - 1) + "6\n"
    if seed == 18:
        body, _ = _no_answer_digits(r, big, {d: 1 for d in range(1, 10)})
        return body + "\n"
    if seed == 19:
        return "4" * (big - 1) + "2\n"
    return "3" * (big - 1) + "8\n"


def valid(number, text):
    """题面：一行一个不超过 200 万位的非负整数，没有前导零。"""
    if number != NUMBER or not text.endswith("\n") or text.count("\n") != 1:
        return False
    digits = text[:-1]
    return (1 <= len(digits) <= MAX_DIGITS and digits.isascii() and digits.isdigit()
            and (digits == "0" or digits[0] != "0"))


# ---------- 构造别的合法结果 / 错误结果，喂 checker ----------
def _alternatives(digits, reference):
    """两份与参考答案不同写法的合法结果（可能与参考相同，调用方只要求合法）。"""
    words = reference.split()
    if words[0] == "NO":
        return []
    found = []
    # 1) 取最后出现的合法三位/两位/一位子序列（从右往左贪心）
    for value in range(992, -1, -8):
        text = str(value); position = len(digits)
        for ch in reversed(text):
            position = digits.rfind(ch, 0, position)
            if position < 0:
                break
        else:
            found.append(text); break
    # 2) 找到一个三位解 (i,j,k) 后，把 i 之前的整段前缀接在前面（前缀首位非零），得到很长的结果
    for value in range(104, 1000, 8):
        text = str(value); position, spots = 0, []
        for ch in text:
            position = digits.find(ch, position)
            if position < 0:
                break
            spots.append(position); position += 1
        else:
            prefix = digits[:spots[0]]
            found.append(prefix + text); break
    return found


def _wrongs(digits, reference):
    words = reference.split()
    bad = ["", "yes\n", "YES\n", "NO NO\n", "\x00\xff garbage\n", "YES\n" + "9" * 5000 + "\n"]
    if words[0] == "NO":
        bad += ["YES\n0\n", "YES\n8\n", "YES\n" + digits[:3] + "\n"]
    else:
        ans = words[1]
        bad += ["NO\n", f"YES\n{ans}\n{ans}\n", f"YES\n0{ans}\n", "YES\n" + "8" * (len(digits) + 1) + "\n",
                f"YES\n{ans}1\n" if ans != "0" else "YES\n1\n"]
    return bad


def _check(case, output, answer):
    with tempfile.TemporaryDirectory() as temp:
        paths = []
        for name, data in (("in", case), ("out", output), ("ans", answer)):
            path = Path(temp) / name
            path.write_bytes(data.encode("latin-1") if name == "out" else data.encode())
            paths.append(str(path))
        code = subprocess.run([sys.executable, "-I", str(CHECKER), *paths], capture_output=True).returncode
    if code not in (0, 42):
        raise SystemExit(f"checker 自身出错（退出码 {code}）")
    return code == 0


def _build():
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    for path in out.glob("*"):
        path.unlink()
    cases = [SAMPLE] + [generate(NUMBER, seed) for seed in range(1, 21)]
    if len(set(cases)) != len(cases):
        raise SystemExit("两组输入撞了，数据必须互异")
    kinds = {True: 0, False: 0}
    for index, case in enumerate(cases):
        if not valid(NUMBER, case):
            raise SystemExit(f"case {index} violates the input contract")
        result = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                                capture_output=True, timeout=120, check=True)
        answer = result.stdout
        digits = case.strip()
        solvable = oracle_solvable(case)
        kinds[solvable] += 1
        if (answer.split()[0] == "YES") != solvable:
            raise SystemExit(f"case {index}: 参考解与状态机 oracle 的有无解不一致")
        if not _check(case, answer, answer):
            raise SystemExit(f"case {index}: checker 不接受参考解")
        if index == 0 and not _check(case, SAMPLE_OUT, answer):
            raise SystemExit("checker 不接受题面样例输出")
        for sample_in, sample_out in OTHER_SAMPLES:
            if case == sample_in and not _check(case, sample_out, answer):
                raise SystemExit(f"case {index}: checker 不接受题面样例输出")
        for alt in _alternatives(digits, answer):
            if not _check(case, f"YES\n{alt}\n", answer):
                raise SystemExit(f"case {index}: checker 拒绝了另一种合法结果")
        for bad in _wrongs(digits, answer):
            if _check(case, bad, answer):
                raise SystemExit(f"case {index}: checker 接受了错误输出 {bad[:40]!r}")
        if len(case.encode()) > 3 * 1024 * 1024 or len(answer.encode()) > 1_500_000:
            raise SystemExit(f"case {index} 超出体积上限")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")
    if not (kinds[True] >= 8 and kinds[False] >= 5):
        raise SystemExit(f"有解/无解分布不对：{kinds}")


if __name__ == "__main__":
    _build()
