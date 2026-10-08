import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = "while True:\n    n=int(input())\n    if n==0:\n        break\n    movie=[tuple(int(i) for i in input().split()) for _ in range(n)]\n    movie.sort(key=lambda x:(x[1],x[0]))\n    cborder=-float('inf')\n    cnt=0\n    for start,end in movie:\n        if start>=cborder:\n            cnt+=1\n            cborder=end\n    print(cnt)"
SAMPLE = '8\n3 4\n0 7 \n3 8 \n15 19\n15 20\n10 15\n8 18 \n6 12 \n0\n'
GENERATOR_NAME = 'g4151'
def valid(text):
    """题面契约：多组数据，每组首行 n（n<=100，n=0 表示结束），随后 n 行各两个 0..1000 的整数。
    生成时额外保证每个区间左端点小于右端点（题面样例如此），valid 只核题面明说的部分。"""
    lines = text.split("\n")
    while lines and lines[-1].strip() == "":
        lines.pop()
    pos = 0
    try:
        while True:
            if pos >= len(lines):
                return False
            h = lines[pos].split(); pos += 1
            if len(h) != 1:
                return False
            n = int(h[0])
            if n == 0:
                return pos == len(lines)
            if not 1 <= n <= 100:
                return False
            for _ in range(n):
                if pos >= len(lines):
                    return False
                v = [int(x) for x in lines[pos].split()]; pos += 1
                if len(v) != 2 or not all(0 <= x <= 1000 for x in v):
                    return False
    except ValueError:
        return False


def _set(r, n, kind):
    z = []
    if kind == "chain":      # 首尾相接的一串，端点重合可以都看
        x = r.randint(0, 50)
        for _ in range(n):
            y = min(1000, x + r.randint(1, 9))
            if y <= x:
                x, y = 999, 1000
            z.append((x, y)); x = y
    elif kind == "nested":   # 层层嵌套，最多看 1 部
        c = r.randint(400, 600)
        for k in range(n):
            w = n - k + r.randint(0, 3)
            z.append((max(0, c - w * 4), min(1000, c + w * 4)))
    elif kind == "same":     # 完全相同的区间
        a = r.randint(0, 999); b = r.randint(a + 1, 1000)
        z = [(a, b)] * n
    elif kind == "long_first":   # 卡“按开始时间贪心”：一部开始最早却很长
        z.append((0, 1000))
        for _ in range(n - 1):
            a = r.randint(1, 990); z.append((a, a + r.randint(1, 10)))
    elif kind == "short_cross":  # 卡“按长度贪心”：短区间跨在两个长区间交界
        for k in range(n):
            if k % 3 == 2:
                m = (k // 3) * 30 + 20
                z.append((m - 2, m + 2))
            else:
                base = (k // 3) * 30
                z.append((base + (0 if k % 3 == 0 else 20), base + (20 if k % 3 == 0 else 30)))
        z = [(min(a, 999), min(max(b, a + 1), 1000)) for a, b in z]
    elif kind == "small":
        for _ in range(n):
            a = r.randint(0, 20); z.append((a, a + r.randint(1, 5)))
    else:
        for _ in range(n):
            a = r.randint(0, 999); z.append((a, r.randint(a + 1, min(1000, a + r.choice([5, 50, 300, 1000])))))
    r.shuffle(z)
    return f"{n}\n" + "\n".join(f"{a} {b}" for a, b in z) + "\n"


# 每组文件：若干 (n 范围, 类型) 的数据集
PLAN = [
    [(1, "rand")], [(1, "same"), (2, "same"), (2, "chain")], [((1, 5), "small")] * 5,
    [((5, 12), "rand")] * 6, [((5, 12), "small")] * 8, [((8, 15), "chain")] * 3,
    [((8, 15), "nested")] * 3, [((8, 15), "long_first")] * 4, [((9, 15), "short_cross")] * 4,
    [((10, 15), "rand"), ((10, 15), "small"), ((10, 15), "chain")],
    [((15, 30), "rand")] * 5, [((15, 30), "small")] * 5, [((30, 60), "rand")] * 5,
    [((30, 60), "long_first")] * 3, [((30, 60), "short_cross")] * 3, [((60, 99), "rand")] * 5,
    [(100, "rand")], [(100, "rand")] * 3, [(100, "chain")], [(100, "nested")], [(100, "same")],
    [(100, "long_first")], [(100, "short_cross")], [(100, "small")] * 3,
    [(100, "rand")] * 10, [((1, 100), "rand")] * 20, [((1, 100), "small")] * 20,
    [((1, 15), "rand")] * 30, [((1, 15), "small")] * 30, [((1, 15), "chain")] * 10,
    [(100, "rand")] * 30, [(100, "chain"), (100, "nested"), (100, "rand")] * 5,
    [((50, 100), "rand")] * 15, [(99, "rand")], [((1, 3), "rand")] * 15,
    [((5, 15), "nested")] * 10, [((5, 15), "long_first")] * 10, [((5, 15), "short_cross")] * 10,
    [(100, "rand")] * 50,
]


def g4151(r, plan):
    out = []
    for n, kind in plan:
        if isinstance(n, tuple):
            n = r.randint(*n)
        out.append(_set(r, n, kind))
    return "".join(out) + "0\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[g4151(random.Random(seed), PLAN[seed-1]) for seed in range(1, 40)]
    assert all(valid(c) for c in cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
