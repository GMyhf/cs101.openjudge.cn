#!/usr/bin/env python3
"""29986 猜数 —— 预设代码题的数据构建。

平台的做法（题面原样公开）：把 `preset_code.py` 拼在学生代码前面。预设代码从 stdin 读两个
整数 io1、io2，随机取秘密数 ans∈[0,1000]；学生每调用一次 query 它就往 stdout 写一行 io1，
猜中后补足到 15 行、再写 io2（不换行）。所以**不论学生怎么猜，只要 15 次内猜中、自己不往
stdout 写东西，输出就恒为 15 行 io1 + io2**；猜不中或询问超过 15 次会触发 assert（RE），
多写东西会 WA。秘密数每次运行都随机，所以同一份数据能反复检验策略本身。

toexpr 只编码第 0..9 位，io1/io2 必须 < 1024；这里取 [1, 1023] 且两者不等。
第 0 组没有「官方样例输入」（题面的样例是文字过程），取 io1=1、io2=2。
"""
from __future__ import annotations
import random
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
PRESET = HERE / "preset_code.py"
REFERENCE = HERE / "samplecode.py"


def generate(seed):
    if seed == 0:
        return 1, 2
    r = random.Random(29986 * 1_000_003 + seed)
    io1 = r.randint(1, 1023)
    io2 = r.choice([v for v in range(1, 1024) if v != io1])
    return io1, io2


def expected(io1, io2):
    return f"{io1}\n" * 15 + f"{io2}"


def valid(text):
    rows = text.split("\n")
    return (len(rows) == 3 and rows[2] == "" and all(row.isdigit() for row in rows[:2])
            and all(1 <= int(row) <= 1023 for row in rows[:2]) and rows[0] != rows[1])


def build():
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    cases = [generate(seed) for seed in range(21)]
    assert len(set(cases)) == 21
    program = PRESET.read_text(encoding="utf-8").rstrip("\n") + "\n" + REFERENCE.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / "main.py"
        path.write_text(program, encoding="utf-8")
        for index, (io1, io2) in enumerate(cases):
            text = f"{io1}\n{io2}\n"
            assert valid(text), index
            for _ in range(5):            # 秘密数每次随机：多跑几次都必须一样
                result = subprocess.run([sys.executable, "-I", str(path)], input=text, text=True,
                                        capture_output=True, timeout=10, env={"PATH": "/usr/bin:/bin"})
                if result.returncode or result.stdout != expected(io1, io2):
                    raise SystemExit(f"case {index}: reference output {result.stdout!r} {result.stderr[-300:]}")
            (out / f"{index}.in").write_text(text, encoding="utf-8")
            (out / f"{index}.out").write_text(expected(io1, io2), encoding="utf-8")


if __name__ == "__main__":
    build()
