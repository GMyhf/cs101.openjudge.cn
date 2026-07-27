import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/15291 statistics, Accepted solution 45990573.\n# Source: http://cs101.openjudge.cn/practice/solution/45990573/\n# Statistics: http://cs101.openjudge.cn/practice/15291/statistics/\n# License: not declared on submission page; no license inferred\n# print(猫猫)\na, b, c = map(int, input().split())\nwhile a:\n    z = 0;\n    d = [list(map(int, input().split())) for i in range(a)];\n    e = [list(map(int, input().split())) for i in range(b)];\n    f = [list(map(int, input().split())) for i in range(c)];\n\n    # 归一化坐标。即减去各自的最小坐标值，使得每个形状的左下角位于 (0, 0)。\n    g, h, k, l, o, p = min(i[0] for i in d), min(i[1] for i in d), min(i[0] for i in e), min(i[1] for i in e), min(\n        i[0] for i in f), min(i[1] for i in f);\n    i, j, m, n, q, r = max(i[0] for i in d) - g, max(i[1] for i in d) - h, max(i[0] for i in e) - k, max(\n        i[1] for i in e) - l, max(i[0] for i in f) - o, max(i[1] for i in f) - p;\n\n    # 计算每个形状的边界，用于后续的移动范围确定。\n    for y in range(a): d[y][0] -= g;d[y][1] -= h\n    for y in range(b): e[y][0] -= k;e[y][1] -= l\n    for y in range(c): f[y][0] -= o;f[y][1] -= p\n\n    # 初始化冲突矩阵。用于记录冲突情况和搜索路径。\n    s = [20 * [1] for i in range(20)];\n    t = [20 * [1] for i in range(20)];\n    u = [20 * [1] for i in range(20)];\n    v = [[[20 * [0] for i in range(20)] for i in range(20)] for i in range(20)];\n    w = [[k - g, l - h, o - g, p - h]];\n    x = []\n\n    # 计算冲突矩阵。计算形状 d 和形状 e 在各种相对位置下的冲突情况。\n    for a in range(-m, i + 1):\n        for b in range(-n, j + 1):\n            c = 1\n            for g in d:\n                for h in e:\n                    if g == [h[0] + a, h[1] + b]: c = 0;break\n                if c == 0: break\n            s[a][b] = c\n\n    # 类似地，计算其他两个冲突矩阵 t 和 u。\n    for a in range(-q, i + 1):\n        for b in range(-r, j + 1):\n            c = 1\n            for g in d:\n                for h in f:\n                    if g == [h[0] + a, h[1] + b]: c = 0;break\n                if c == 0: break\n            t[a][b] = c\n    for a in range(-q, m + 1):\n        for b in range(-r, n + 1):\n            c = 1\n            for g in e:\n                for h in f:\n                    if g == [h[0] + a, h[1] + b]: c = 0;break\n                if c == 0: break\n            u[a][b] = c\n\n    # 广度优先搜索。如果找到了一个满足条件的状态，则输出步骤数 z；否则，如果 z 不为零，则输出 -1 表示没有找到解决方案。\n    while w:\n        for a in w:\n            if v[a[0]][a[1]][a[2]][a[3]]: continue\n            v[a[0]][a[1]][a[2]][a[3]] = 1\n            if (i < a[0] or -m > a[0] or j < a[1] or -n > a[1]) * (i < a[2] or -q > a[2] or j < a[3] or -r > a[3]) * (\n                    m < a[2] - a[0] or -q > a[2] - a[0] or n < a[3] - a[1] or -r > a[3] - a[1]): print(\n                z);z = -1;x = [];break\n            if a[0] <= 10 >= a[2]:\n                if s[a[0] + 1][a[1]] * t[a[2] + 1][a[3]]: x.append([a[0] + 1, a[1], a[2] + 1, a[3]])\n            if -11 < a[0] and -11 < a[2]:\n                if s[a[0] - 1][a[1]] * t[a[2] - 1][a[3]]: x.append([a[0] - 1, a[1], a[2] - 1, a[3]])\n            if a[1] <= 10 >= a[3]:\n                if s[a[0]][a[1] + 1] * t[a[2]][a[3] + 1]: x.append([a[0], a[1] + 1, a[2], a[3] + 1])\n            if -11 < a[1] and -11 < a[3]:\n                if s[a[0]][a[1] - 1] * t[a[2]][a[3] - 1]: x.append([a[0], a[1] - 1, a[2], a[3] - 1])\n            if a[0] <= 10:\n                if s[a[0] + 1][a[1]] * u[a[2] + ~a[0]][a[3] - a[1]]: x.append([a[0] + 1, a[1], a[2], a[3]])\n            if -11 < a[0]:\n                if s[a[0] - 1][a[1]] * u[a[2] + 1 - a[0]][a[3] - a[1]]: x.append([a[0] - 1, a[1], a[2], a[3]])\n            if a[1] <= 10:\n                if s[a[0]][a[1] + 1] * u[a[2] - a[0]][a[3] + ~a[1]]: x.append([a[0], a[1] + 1, a[2], a[3]])\n            if -11 < a[1]:\n                if s[a[0]][a[1] - 1] * u[a[2] - a[0]][a[3] + 1 - a[1]]: x.append([a[0], a[1] - 1, a[2], a[3]])\n            if a[2] <= 10:\n                if t[a[2] + 1][a[3]] * u[a[2] + 1 - a[0]][a[3] - a[1]]: x.append([a[0], a[1], a[2] + 1, a[3]])\n            if -11 < a[2]:\n                if t[a[2] - 1][a[3]] * u[a[2] + ~a[0]][a[3] - a[1]]: x.append([a[0], a[1], a[2] - 1, a[3]])\n            if a[3] <= 10:\n                if t[a[2]][a[3] + 1] * u[a[2] - a[0]][a[3] + 1 - a[1]]: x.append([a[0], a[1], a[2], a[3] + 1])\n            if -11 < a[3]:\n                if t[a[2]][a[3] - 1] * u[a[2] - a[0]][a[3] + ~a[1]]: x.append([a[0], a[1], a[2], a[3] - 1])\n        w, x = x, [];\n        z += 1\n\n    # 循环继续。如果当前案例没有解决方案，则输出 -1。\n    if z: print(-1)\n    a, b, c = map(int, input().split())\n'
LANGUAGE='Python3'
SAMPLE='3 12 5\n2 1\n2 2\n1 2\n0 0\n0 1\n0 2\n0 3\n0 4\n1 0\n1 4\n2 0\n2 4\n3 0\n3 1\n3 4\n2 3\n3 3\n4 3\n4 4\n4 2\n1 1 1\n0 0\n1 1\n2 2\n0 0 0\n'
GENERATOR_NAME='g15291'
def g15291(r):
    # Keep the blocks inside the 0..9 board, but deliberately include overlap
    # so that the answer is not almost always the trivial 0.
    x, y = r.randint(2, 7), r.randint(2, 7)
    mode = r.randrange(4)
    if mode == 0:
        blocks = [[(x, y)], [(x, y)], [(x, y)]]
    elif mode == 1:
        blocks = [[(x, y)], [(x, y)], [(x + 1, y)]]
    elif mode == 2:
        blocks = [[(x, y)], [(x + 1, y)], [(x + 2, y)]]
    else:
        blocks = [[(x, y), (x, y + 1)], [(x, y), (x, y + 1)], [(x + 1, y), (x + 1, y + 1)]]
    rows = [f"{len(block)}\n" + "\n".join(f"{a} {b}" for a, b in block) for block in blocks]
    return f"{len(blocks[0])} {len(blocks[1])} {len(blocks[2])}\n" + "\n".join(
        f"{a} {b}" for block in blocks for a, b in block) + "\n0 0 0\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        d=Path(d); src=d/'main.py'
        src.write_text(REFERENCE); cmd=[sys.executable,str(src)]
        if LANGUAGE=="G++":
            exe=d/"main"; subprocess.run(["g++","-std=c++17","-O2",str(src),"-o",str(exe)],check=True)
            cmd=[str(exe)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()
