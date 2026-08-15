#!/usr/bin/env python3
"""02934 字符串插入 —— 生成器、输入契约与数据构建。

题面对输入只给了两条硬约束（`INPUT_DOMAIN` 里是逐字原话）：`str` 不超过 10 个字符、
`substr` 恰好 3 个字符。参考实现按 `cin >> str >> substr` 读，所以两个 token 之间
只能是空白，token 自身不含空白。生成器按这两条走，`valid()` 是同一条契约的反向校验。

`SHAPES` 不是为了「多来点随机」，而是把这题真正会挂人的几种形状都摆上：
  · `tie`    —— 最大字符出现多次，题面明写「若有多个最大则只考虑第一个」，
                写成「插在最后一个最大字符后面」的解法只会在这里挂；
  · `tail`   —— 最大字符在末尾，插入退化成追加，`insert(pos+1, …)` 越界的写法在这里挂；
  · `head`   —— 最大字符在开头；
  · `uniform`—— 整串同一个字符，全体并列最大；
  · `shortest`/`longest` —— 题面允许的长度两端（1 和 10）。
字符集取数字+大写+小写，跨越三段 ASCII 区间（'0'<'A'<'a'），
比大小写单开一档更能验「比的是 ASCII 而不是字母序」。
"""
from __future__ import annotations
import random

NUMBER = 2934
INPUT_DOMAIN = "str的字符个数不超过10，substr的字符个数为3"
LABEL = "each line holds str (1..10 chars) and substr (exactly 3 chars), no whitespace inside either"
INVALID = "abcdefghijk xyz\n"          # str 有 11 个字符，越过题面的 10
SAMPLE = "abcab eee\n12343 555\n"

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
SHAPES = ("plain", "shortest", "longest", "tie", "tail", "head", "uniform")


def _word(r, length):
    return "".join(r.choice(ALPHABET) for _ in range(length))


def _line(r, shape):
    if shape == "shortest":
        text = _word(r, 1)
    elif shape == "longest":
        text = _word(r, 10)
    elif shape == "uniform":
        text = r.choice(ALPHABET) * r.randint(2, 10)
    elif shape in ("tie", "tail", "head"):
        top = r.choice("vwxyz")
        body = [r.choice("abcdefghij") for _ in range(r.randint(2, 10))]
        if shape == "tie":
            first, second = sorted(r.sample(range(len(body)), 2))
            body[first] = body[second] = top
        elif shape == "tail":
            body[-1] = top
        else:
            body[0] = top
        text = "".join(body)
    else:
        text = _word(r, r.randint(1, 10))
    return f"{text} {_word(r, 3)}"


def generate(number, seed):
    if number != NUMBER:
        raise KeyError(number)
    r = random.Random(number * 1_000_003 + seed)
    # 每组至少带上一种指定形状，其余随机 —— 20 组下来七种形状都被覆盖到。
    shapes = [SHAPES[(seed - 1) % len(SHAPES)]]
    shapes += [r.choice(SHAPES) for _ in range(r.randint(0, 7))]
    r.shuffle(shapes)
    return "".join(_line(r, shape) + "\n" for shape in shapes)


def valid(number, text):
    if number != NUMBER:
        raise KeyError(number)
    lines = text.rstrip("\n").splitlines()
    if not lines:
        return False
    for line in lines:
        parts = line.split(" ")
        if len(parts) != 2:
            return False
        head, tail = parts
        if not 1 <= len(head) <= 10 or len(tail) != 3:
            return False
        if any(not character.isprintable() or character.isspace()
               for character in head + tail):
            return False
    return True


import subprocess as _subprocess, sys as _sys, tempfile as _tempfile
from pathlib import Path as _Path
REFERENCE = _Path(__file__).with_name("samplecode.cpp")
LANGUAGE = "G++"


def _build():
    with _tempfile.TemporaryDirectory() as folder:
        folder = _Path(folder)
        source = folder / "main.cpp"
        source.write_text(REFERENCE.read_text(encoding="utf-8"), encoding="utf-8")
        binary = folder / "main"
        _subprocess.run(["g++", "-std=c++20", "-O2", "-pipe", str(source), "-o", str(binary)],
                        check=True)
        out = _Path(__file__).with_name("data")
        out.mkdir(exist_ok=True)
        for path in out.glob("*"):
            path.unlink()
        cases = [SAMPLE] + [generate(NUMBER, seed) for seed in range(1, 21)]
        for index, case in enumerate(cases):
            if not valid(NUMBER, case):
                raise SystemExit(f"case {index} violates the input contract: {case!r}")
            result = _subprocess.run([str(binary)], input=case, text=True,
                                     capture_output=True, timeout=120, check=True)
            answer = "\n".join(line.rstrip() for line in result.stdout.rstrip().splitlines()) + "\n"
            (out / f"{index}.in").write_text(case, encoding="utf-8")
            (out / f"{index}.out").write_text(answer, encoding="utf-8")


if __name__ == "__main__":
    _build()
