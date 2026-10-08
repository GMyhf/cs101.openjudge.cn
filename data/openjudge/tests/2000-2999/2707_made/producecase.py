import random, subprocess, sys, tempfile
from pathlib import Path
import math

def _fmt2707(a, b, c, alt=False):
    """按题面公式算出期望行；alt=True 换一种运算顺序，用来剔除结果落在舍入临界处的系数。"""
    if b == 0: b = -b
    delta = b * b - 4 * a * c if alt else b ** 2 - 4 * a * c
    if delta > 0:
        q = math.sqrt(delta)
        x1, x2 = ((-b / (2 * a) + q / (2 * a)), (-b / (2 * a) - q / (2 * a))) if alt else ((-b + q) / (2 * a), (-b - q) / (2 * a))
        return f"x1={x1:.5f};x2={x2:.5f}"
    if delta == 0:
        return f"x1=x2={-b / (2 * a):.5f}"
    d = math.sqrt(-delta) / (2 * a); re = -b / (2 * a)
    return f"x1={re:.5f}+{d:.5f}i;x2={re:.5f}-{d:.5f}i"

def _ok2707(a, b, c):
    """只要 a>0：a<0 时题面的求根公式与 x1/x2 排序规则互相矛盾；避开 -0 输出与判别式贴近 0 的不稳定情形。"""
    if a <= 0: return False
    if b == 0 and c >= 0: return False      # 实部为 ±0，C 的 printf 与题面「去掉负号」的要求冲突
    delta = b * b - 4 * a * c
    if delta != 0 and abs(delta) < 1e-3: return False
    if (b * b - 4 * a * c == 0) != (b ** 2 - 4 * a * c == 0): return False
    out = _fmt2707(a, b, c)
    if "-0.00000" in out: return False
    return out == _fmt2707(a, b, c, alt=True)

def g2707(r, seed):
    def num(lo, hi, kind):
        if kind == 0: return float(r.randint(lo, hi))
        if kind == 1: return r.randint(lo * 10, hi * 10) / 10
        return r.randint(lo * 100, hi * 100) / 100
    def show(x, kind):
        if kind == 3 or mode_is_equal[0]: return str(int(x)) if x == int(x) else repr(x)
        return f"{x:.{max(kind, 1)}f}"
    mode_is_equal = [False]
    def row(mode):
        while True:
            kind = r.randint(0, 3); k = kind if kind < 3 else 0
            if mode == "equal":      # 判别式恰为 0：a、根都取二进制可精确表示的值
                a = r.choice([0.25, 0.5, 1, 1.5, 2, 2.5, 3, 4, 8]) * r.choice([1, 1, 2, 4])
                t = r.choice([-1, 1]) * r.randint(1, 160) / 8
                b, c = -2 * a * t, a * t * t
                kind = 1 if kind == 0 else kind
            elif mode == "real":
                a = num(1, 50, k) or 1.0; b = num(-100, 100, k); c = num(-100, 0, k) if r.random() < .3 else num(-100, 100, k)
            elif mode == "complex":
                a = num(1, 50, k) or 1.0; b = num(-100, 100, k); c = num(1, 100, k)
                if b * b >= 4 * a * c: continue
            elif mode == "c0":
                a = num(1, 50, k) or 1.0; b = num(-100, 100, k); c = 0.0
            elif mode == "b0":
                a = num(1, 50, k) or 1.0; b = 0.0; c = -abs(num(1, 100, k))
            elif mode == "big":
                a = num(1, 1000, 2); b = num(-1000, 1000, 2); c = num(-1000, 1000, 2)
            else:  # tiny
                a = num(1, 9, 2) / 10 or 0.1; b = num(-9, 9, 2) / 10; c = num(-9, 9, 2) / 10
            mode_is_equal[0] = mode == "equal"
            text = " ".join(show(x, kind) for x in (a, b, c))
            if any(t.startswith("-") and float(t) == 0 for t in text.split()): continue   # 不写 "-0.0"
            a, b, c = map(float, text.split())   # 以写进文件的数值为准再检查一遍
            if mode == "equal" and b * b - 4 * a * c != 0: continue
            if a <= 0 or not _ok2707(a, b, c): continue
            return text
    modes = ["real", "complex", "equal", "c0", "b0", "big", "tiny"]
    if seed == 1: rows = ["1 2 1", "1 0 -4", "1 -5 0", "2 0 -2"]
    elif seed == 2: rows = [row("equal") for _ in range(12)]
    elif seed == 3: rows = [row("complex") for _ in range(12)]
    elif seed <= 5: rows = [row(r.choice(modes)) for _ in range(1000)]
    elif seed == 6: rows = [row("real")]
    else: rows = [row(modes[i % 7]) for i in range(7)] + [row(r.choice(modes)) for _ in range(r.randint(0, 25))]
    r.shuffle(rows)
    return str(len(rows)) + "\n" + "\n".join(rows) + "\n"

def valid(text):
    """题面：第一行方程数目 n；其后 n 行每行三个浮点数 a b c（空格隔开），a 不等于 0。"""
    import re
    if not text.endswith("\n"): return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*", lines[0]) or len(lines) != int(lines[0]) + 1: return False
    num = r"[-+]?(\d+(\.\d*)?|\.\d+)"
    for ln in lines[1:]:
        if not re.fullmatch(f"{num} {num} {num}", ln): return False
        if float(ln.split()[0]) == 0: return False
    return True

REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 2707: 求一元二次方程的根\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/routine/02707/\n# License: not declared in source collection; no license is inferred.\nimport math\nn = int(input())\nfor i in range(n):\n    a, b, c = map(float, input().split())\n    if b == 0:\n        b = -b\n    delta = b ** 2 - 4 * a * c\n    if delta > 0:\n        x1 = (-b + math.sqrt(delta)) / (2 * a)\n        x2 = (-b - math.sqrt(delta)) / (2 * a)\n        print(f"x1={x1:.5f};x2={x2:.5f}")\n    elif delta == 0:\n        t = (-b) / (2 * a)\n        print(f"x1=x2={t:.5f}")\n    else:\n        d = math.sqrt(-delta) / (2 * a)\n        re = (-b) / (2 * a)\n        print(f"x1={re:.5f}+{d:.5f}i;x2={re:.5f}-{d:.5f}i")\n'
SAMPLE='3\n1.0 3.0 1.0\n2.0 -4.0 2.0\n1.0 2.0 8.0\n'
GENERATOR='g2707'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed), seed) for seed in range(1, 40)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
