#!/usr/bin/env python3
"""Codeforces 37C Old Berland Language —— 生成器、输入契约与数据构建（配 checker.py 特判）。

2026-09-17 新建。题面：N（1≤N≤1000）个词长 l_i（1≤l_i≤1000），构造两两不为前缀的 0/1 词，
按输入顺序输出；无解输出 NO；答案不唯一，由 checker.py 判。

有解 ⇔ Kraft 和 Σ2^(-l_i) ≤ 1。判别力按「这题会怎么错」排（seed → 形状）：
  1      题面样例 2（`1 1 1` → NO）；第 0 组是样例 1
  2-4    n=1 l=1、n=1 l=1000、`1 1`（Kraft 恰为 1 的最小情形）
  5      1..999 再加一个 999，打乱：Kraft 恰为 1（用 `< 1` 判的挂）
  6      1..998、998、1000，打乱：Kraft = 1 + 2^-1000（浮点求和得 1.0，判成 YES 的挂）
  7      1..999、1000，打乱：Kraft = 1 - 2^-1000
  8-9    1000 个 10（YES）/ 1000 个 9（NO）
  10-11  24 个 9 + 976 个 10（恰为 1）/ 25 个 9 + 975 个 10（超 1），打乱
  12     1000 个 1000：输出约 1 MB（逐位拼字符串、按 2^1000 建树的挂）
  13-15  随机满二叉树的叶子深度（恰为 1）、其中一片叶子上移一层（超 1）、删一片叶子（< 1）
  16     `3 3 2 1`：长度降序（不排序、按输入顺序贪心分配的挂）
  17     `2 2 2 2 2`：NO
  18     专往最深的叶子分裂的深树，词长接近 1000，打乱，恰为 1
  19     1000 个 8..12 的随机长度
  20     1..990、8 个 994、2 个 992，打乱，恰为 1
参考解 samplecode.py 用「规范前缀码」整数移位分配；构建时用逐层数空闲结点的模拟独立复核
有无解，再逐组调用 checker：参考解必须通过，两份不同的合法词表（按位取反；换同长词的顺序后
异或一条随机掩码）必须通过，几份错误输出必须被拒。
"""
from __future__ import annotations
import random
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
CHECKER = HERE / "checker.py"
INPUT_DOMAIN = "The first line contains one integer N (1≤N≤1000). The second line contains N space-separated integers — the lengths of these words. All the lengths are natural numbers not exceeding 1000."
SAMPLES = (("3\n1 2 3\n", "YES\n0\n10\n110\n"), ("3\n1 1 1\n", "NO\n"))
MAX_N = MAX_L = 1000


def _fmt(lengths):
    return f"{len(lengths)}\n{' '.join(map(str, lengths))}\n"


def _shuffled(r, lengths):
    lengths = list(lengths); r.shuffle(lengths); return lengths


def _random_tree(r, leaves, deep=False):
    """从一片根叶子开始反复分裂，得到叶子深度（Kraft 和恰为 1）。"""
    depths = [0]
    while len(depths) < leaves:
        if deep and r.random() < 0.9:
            index = max(range(len(depths)), key=lambda i: (depths[i] < MAX_L, depths[i]))
        else:
            index = r.randrange(len(depths))
        if depths[index] >= MAX_L:
            continue
        d = depths.pop(index)
        depths += [d + 1, d + 1]
    return depths


def generate(seed):
    r = random.Random(37_000_003 + seed * 7919)
    if seed == 1:
        return SAMPLES[1][0]
    if seed == 2:
        return _fmt([1])
    if seed == 3:
        return _fmt([1000])
    if seed == 4:
        return _fmt([1, 1])
    if seed == 5:
        return _fmt(_shuffled(r, list(range(1, 1000)) + [999]))
    if seed == 6:
        return _fmt(_shuffled(r, list(range(1, 999)) + [998, 1000]))
    if seed == 7:
        return _fmt(_shuffled(r, list(range(1, 1000)) + [1000]))
    if seed == 8:
        return _fmt([10] * 1000)
    if seed == 9:
        return _fmt([9] * 1000)
    if seed == 10:
        return _fmt(_shuffled(r, [9] * 24 + [10] * 976))
    if seed == 11:
        return _fmt(_shuffled(r, [9] * 25 + [10] * 975))
    if seed == 12:
        return _fmt([1000] * 1000)
    if seed in (13, 14, 15):
        depths = _shuffled(r, _random_tree(r, r.randint(400, 600)))
        if seed == 14:
            index = r.choice([i for i, d in enumerate(depths) if d >= 2])
            depths[index] -= 1
        if seed == 15:
            depths.pop(r.randrange(len(depths)))
        return _fmt(depths)
    if seed == 16:
        return _fmt([3, 3, 2, 1])
    if seed == 17:
        return _fmt([2] * 5)
    if seed == 18:
        return _fmt(_shuffled(r, _random_tree(r, 1000, deep=True)))
    if seed == 19:
        return _fmt([r.randint(8, 12) for _ in range(1000)])
    return _fmt(_shuffled(r, list(range(1, 991)) + [994] * 8 + [992] * 2))


def valid(text):
    """题面：第一行 N（1≤N≤1000）；第二行 N 个空格分隔的自然数，都不超过 1000。"""
    if not text.endswith("\n") or text.count("\n") != 2:
        return False
    first, second = text[:-1].split("\n")
    if not first.isdigit() or not all(x.isdigit() for x in second.split(" ")):
        return False
    n, lengths = int(first), [int(x) for x in second.split(" ")]
    return 1 <= n <= MAX_N and len(lengths) == n and all(1 <= l <= MAX_L for l in lengths)


def oracle_solvable(text):
    """逐层模拟：深度 d 的空闲结点数 = 上一层空闲数 × 2 − 这一层要用掉的词数。"""
    lengths = list(map(int, text.split()[1:]))
    count = [0] * (MAX_L + 1)
    for l in lengths:
        count[l] += 1
    free = 1
    for depth in range(1, MAX_L + 1):
        free = min(free * 2, MAX_N + 1) - count[depth]
        if free < 0:
            return False
    return True


def _alternatives(text, reference):
    tokens = reference.split()
    if tokens[0] == "NO":
        return []
    lengths = list(map(int, text.split()[1:]))
    flipped = [w.translate(str.maketrans("01", "10")) for w in tokens[1:]]
    # 同长的词按输入倒序重新分派，再异或同一条掩码（异或同一掩码不改变前缀关系）
    by_length = {}
    for index, l in enumerate(lengths):
        by_length.setdefault(l, []).append(index)
    permuted = list(tokens[1:])
    for indices in by_length.values():
        for a, b in zip(indices, reversed(indices)):
            permuted[a] = tokens[1:][b]
    mask = "".join(random.Random(len(lengths)).choice("01") for _ in range(MAX_L - 1)) + "1"
    mask = mask[::-1]
    masked = ["".join("1" if c != m else "0" for c, m in zip(w, mask)) for w in permuted]
    return ["YES\n" + "\n".join(flipped) + "\n", "YES\n" + "\n".join(masked) + "\n"]


def _wrongs(text, reference):
    tokens = reference.split()
    lengths = list(map(int, text.split()[1:]))
    bad = ["", "yes\n", "NO NO\n", "\x00\xff\n", "YES\n" + "0" * 5000 + "\n"]
    if tokens[0] == "NO":
        return bad + ["YES\n" + "\n".join("0" * l for l in lengths) + "\n",
                      "YES\n" + "\n".join(format(i, "b").zfill(l)[-l:] for i, l in enumerate(lengths)) + "\n"]
    words = tokens[1:]
    bad += ["NO\n", "YES\n" + "\n".join(words[:-1]) + "\n", "YES\n" + "\n".join(words + ["0"]) + "\n",
            "YES\n" + "\n".join(w.replace("1", "2", 1) if "1" in w else w[:-1] + "2" for w in words) + "\n"]
    shortest = min(range(len(words)), key=lambda i: lengths[i])
    longer = [i for i in range(len(words)) if lengths[i] > lengths[shortest]]
    if longer:   # 让某个更长的词以最短的词开头
        j = longer[0]; changed = list(words)
        changed[j] = words[shortest] + words[j][len(words[shortest]):]
        bad.append("YES\n" + "\n".join(changed) + "\n")
        if lengths[j] != lengths[shortest]:
            swapped = list(words); swapped[j], swapped[shortest] = swapped[shortest], swapped[j]
            bad.append("YES\n" + "\n".join(swapped) + "\n")
    same = [i for i in range(len(words)) if lengths[i] == lengths[shortest] and i != shortest]
    if same:
        duplicated = list(words); duplicated[same[0]] = words[shortest]
        bad.append("YES\n" + "\n".join(duplicated) + "\n")
    return bad


def _check(case, output, answer):
    with tempfile.TemporaryDirectory() as temp:
        paths = []
        for name, data in (("in", case), ("out", output), ("ans", answer)):
            path = Path(temp) / name
            path.write_bytes(data.encode("latin-1"))
            paths.append(str(path))
        code = subprocess.run([sys.executable, "-I", str(CHECKER), *paths], capture_output=True).returncode
    if code not in (0, 42):
        raise SystemExit(f"checker 自身出错（退出码 {code}）")
    return code == 0


def build():
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    for path in out.glob("*"):
        path.unlink()
    cases = [SAMPLES[0][0]] + [generate(seed) for seed in range(1, 21)]
    if len(set(cases)) != len(cases):
        raise SystemExit("两组输入撞了，数据必须互异")
    kinds = {True: 0, False: 0}
    for index, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"case {index} violates the input contract")
        answer = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                                capture_output=True, timeout=120, check=True).stdout
        solvable = oracle_solvable(case)
        kinds[solvable] += 1
        if (answer.split()[0] == "YES") != solvable:
            raise SystemExit(f"case {index}: 参考解与逐层模拟的有无解不一致")
        if not _check(case, answer, answer):
            raise SystemExit(f"case {index}: checker 不接受参考解")
        for sample_in, sample_out in SAMPLES:
            if case == sample_in and not _check(case, sample_out, answer):
                raise SystemExit(f"case {index}: checker 不接受题面样例输出")
        alternatives = _alternatives(case, answer)
        if alternatives and alternatives[0] == answer:
            raise SystemExit(f"case {index}: 按位取反的词表竟与参考相同")
        for alt in alternatives:
            if not _check(case, alt, answer):
                raise SystemExit(f"case {index}: checker 拒绝了另一种合法词表")
        for bad in _wrongs(case, answer):
            if _check(case, bad, answer):
                raise SystemExit(f"case {index}: checker 接受了错误输出 {bad[:40]!r}")
        if len(case.encode()) > 3 * 1024 * 1024 or len(answer.encode()) > 1_500_000:
            raise SystemExit(f"case {index} 超出体积上限")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")
    if not (kinds[True] >= 10 and kinds[False] >= 6):
        raise SystemExit(f"有解/无解分布不对：{kinds}")


if __name__ == "__main__":
    build()
