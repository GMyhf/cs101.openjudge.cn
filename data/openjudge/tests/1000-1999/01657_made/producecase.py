import random, subprocess, sys, tempfile
from pathlib import Path

import re

def valid(text):
    # 题面：第一行组数 t（0<=t<=20）；随后 t 行，每行两个位置「字母 a..h + 数字 1..8」，起点在前、终点在后。
    lines = text.split("\n")
    if lines and lines[-1] == "": lines.pop()
    if not lines or not re.fullmatch(r"\d+", lines[0].strip()): return False
    t = int(lines[0])
    if not 0 <= t <= 20 or len(lines) != t + 1: return False
    return all(re.fullmatch(r"\s*[a-h][1-8]\s+[a-h][1-8]\s*", ln) for ln in lines[1:])

SQ = [c + d for c in "abcdefgh" for d in "12345678"]

def build_cases():
    r = random.Random(1657)
    cases = []
    def fmt(pairs): return f"{len(pairs)}\n" + "".join(f"{a} {b}\n" for a, b in pairs)
    # 边界：t=0、起终点相同、四个角、同色/异色、同行同列同斜线
    cases.append("0\n")
    cases.append(fmt([("a1", "a1"), ("h8", "h8"), ("d4", "d4"), ("a1", "h8"), ("a8", "h1"), ("a1", "h1"),
                      ("a1", "a8"), ("h1", "a8"), ("a1", "b1"), ("a1", "b2"), ("a1", "b3"), ("c3", "a1")]))
    cases.append(fmt([("e4", x) for x in ["e4", "e5", "f5", "h7", "b1", "a8", "h1", "e1", "a4", "g8",
                                         "d3", "c6", "b4", "f6", "h4", "e8", "a5", "c2", "g2", "h8"]]))
    # 遍历：把 64x64 中按距离类型挑出的组分到多个文件里，每组 20 行
    pairs = [(a, b) for a in SQ for b in SQ]
    r.shuffle(pairs)
    same = [(a, a) for a in SQ]
    while len(cases) < 39:
        k = r.randint(1, 20) if len(cases) % 4 else 20
        rows = [pairs.pop() for _ in range(k)]
        if len(cases) % 3 == 0:
            rows[r.randrange(k)] = r.choice(same)
        cases.append(fmt(rows))
    return cases

REFERENCE='# External reference: http://cs101.openjudge.cn/practice/01657/statistics/\n# Accepted submission: 52486260\n# Source: http://cs101.openjudge.cn/practice/solution/52486260/\n# License: not declared on the submission page; no license is inferred.\n\ndef King(x, y):\n    steps = max(x, y)\n    return steps\n\ndef Queen(x, y):\n    if x == y or x == 0 or y == 0:\n        steps = 1\n    else:\n        steps = 2\n    return steps\n\ndef Rook(x, y):\n    if x == 0 or y == 0:\n        return 1\n    else:\n        return 2\n\ndef Bishop(x, y):\n    if (x + y) % 2 != 0:\n        return "Inf"\n    elif x == y:\n        return 1\n    else:\n        return 2\n\n\nt = int(input())\n\nfor _ in range(t):\n    start, end = input().split()\n    x_1 = start[0]\n    y_1 = int(start[1])\n    x_2 = end[0]\n    y_2 = int(end[1])\n    dx = abs(ord(x_2) - ord(x_1))\n    dy = abs(y_2 - y_1)\n    if dx == 0 and dy == 0:\n        print(\'0 0 0 0\')\n    else:\n        print(King(dx, dy), Queen(dx, dy), Rook(dx, dy), Bishop(dx, dy))\n'
LANGUAGE='Python3'
SAMPLE='2\na1 c3\nf5 f8\n'

def run_all(cases):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp); src = tmp/('s.py' if LANGUAGE == 'Python3' else 's.cpp'); src.write_text(REFERENCE)
        cmd = [sys.executable, '-I', str(src)]
        if LANGUAGE != 'Python3':
            exe = tmp/'s'; subprocess.run(['g++', '-std=c++20', '-O2', '-pipe', str(src), '-o', str(exe)], check=True); cmd = [str(exe)]
        outs = []
        for x in cases:
            q = subprocess.run(cmd, input=x, text=True, capture_output=True, timeout=120, check=True)
            outs.append('\n'.join(line.rstrip() for line in q.stdout.rstrip().splitlines()) + '\n')
        return outs

def main():
    cases = [SAMPLE] + build_cases()
    for i, x in enumerate(cases):
        assert valid(x), f"第 {i} 组不满足题面约束"
    outs = run_all(cases)
    out = Path('data'); out.mkdir(exist_ok=True)
    for p in out.glob('*'): p.unlink()
    for i, (x, y) in enumerate(zip(cases, outs)):
        (out/f'{i}.in').write_text(x); (out/f'{i}.out').write_text(y)

if __name__ == '__main__':
    main()
