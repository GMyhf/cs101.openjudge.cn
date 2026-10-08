import random, subprocess, sys, tempfile
from pathlib import Path
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def _merge(r, a, b, bias=.5):
    aa, bb, c = list(a), list(b), []
    while aa or bb:
        src = aa if not bb or (aa and r.random() < bias) else bb; c.append(src.pop(0))
    return c

def _row(r, la, lb, alpha, mode):
    a = "".join(r.choice(alpha) for _ in range(la))
    b = "".join(r.choice(alpha) for _ in range(lb))
    c = _merge(r, a, b, r.choice([.5, .1, .9]))
    if mode == "yes":
        pass
    elif mode == "sub":  # 某个字符换成别的字母（可能只是大小写不同）
        k = r.randrange(len(c)); ch = c[k]
        c[k] = ch.swapcase() if r.random() < .5 and ch.isalpha() else r.choice([x for x in alpha + "Zz" if x != ch])
    elif mode == "swap":  # 交换两个不同字符：字母多重集不变，只是次序错
        ks = [k for k in range(len(c) - 1) if c[k] != c[k + 1]]
        if ks:
            k = r.choice(ks); c[k], c[k + 1] = c[k + 1], c[k]
    elif mode == "shuffle":
        r.shuffle(c)
    return f"{a} {b} {''.join(c)}"

def _hard(r, n):
    # 几乎全是同一字母、只在末尾有差异：不带记忆化的回溯是指数级
    x, y = r.choice([("a", "b"), ("A", "a"), ("z", "y")])
    rows = []
    for _ in range(n):
        la, lb = r.randint(150, 200), r.randint(150, 200)
        kind = r.randrange(4)
        if kind == 0:    # 全 x，c 末位是 y：no
            a, b, c = x * la, x * lb, x * (la + lb - 1) + y
        elif kind == 1:  # 两串都以 y 结尾：yes
            a, b, c = x * (la - 1) + y, x * (lb - 1) + y, x * (la + lb - 2) + y + y
        elif kind == 2:  # 两串都以 y 结尾，c 只有一个 y：no
            a, b, c = x * (la - 1) + y, x * (lb - 1) + y, x * (la + lb - 1) + y
        else:            # 一串以 y 结尾，y 放在 c 中段：yes 当且仅当 y 前 x 的个数够
            a, b = x * (la - 1) + y, x * lb
            k = r.randint(la - 3, la + 2); c = x * k + y + x * (la + lb - 1 - k)
        rows.append(f"{a} {b} {c}")
    return rows

def g2192(r, seed):
    modes = ["yes", "yes", "sub", "swap", "shuffle"]
    if seed == 1:
        rows = ["a b ab", "a b ba", "a b bb", "A a aA", "A a aa", "z z zz"]
    elif seed <= 12:  # 小规模随机，含大小写
        alpha = r.choice(["ab", "aA", "abcde", LETTERS])
        rows = [_row(r, r.randint(1, 18), r.randint(1, 18), alpha, r.choice(modes)) for _ in range(r.randint(1, 12))]
    elif seed <= 22:  # 单组长度到 200 上限
        alpha = r.choice(["ab", "aA", "abc", LETTERS])
        rows = [_row(r, r.randint(150, 200), r.randint(150, 200), alpha, r.choice(modes)) for _ in range(r.randint(10, 25))]
        rows[0] = _row(r, 200, 200, alpha, "yes"); rows[-1] = _row(r, 200, 200, alpha, "swap")
    elif seed <= 28:  # 卡指数回溯
        rows = _hard(r, r.randint(5, 20))
    elif seed <= 35:  # 组数到 1000 上限，串较短
        alpha = r.choice(["ab", "aA", "abc", LETTERS])
        rows = [_row(r, r.randint(1, 20), r.randint(1, 20), alpha, r.choice(modes)) for _ in range(1000)]
    else:  # 1000 组混合长度
        alpha = r.choice(["ab", "abc", LETTERS])
        rows = []
        for _ in range(1000):
            la = 200 if r.random() < .01 else r.randint(1, 40); lb = 200 if r.random() < .01 else r.randint(1, 40)
            rows.append(_row(r, la, lb, alpha, r.choice(modes)))
    return str(len(rows)) + "\n" + "\n".join(rows) + "\n"

def valid(text):
    """题面：首行 1..1000 的正整数 n；随后 n 行，每行三个由大小写字母组成、以单个空格分隔的串；
    前两串长度 1..200；第三串长度等于前两串长度之和。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit() or lines[0][0] == "0":
        return False
    n = int(lines[0])
    if not 1 <= n <= 1000 or len(lines) != n + 1:
        return False
    for line in lines[1:]:
        parts = line.split(" ")
        if len(parts) != 3 or not all(p and p.isascii() and p.isalpha() for p in parts):
            return False
        a, b, c = parts
        if not (1 <= len(a) <= 200 and 1 <= len(b) <= 200 and len(c) == len(a) + len(b)):
            return False
    return True

REFERENCE='# 参考解（本仓重写）：按 c 的前缀推进，维护可达的 a 已用长度集合，最坏 O(|a||b|)。\nimport sys\ndef main():\n    data = sys.stdin.read().split()\n    n = int(data[0]); out = []\n    for t in range(n):\n        a, b, c = data[1 + 3 * t: 4 + 3 * t]\n        ok = len(c) == len(a) + len(b)\n        cur = {0}\n        if ok:\n            for k, ch in enumerate(c):\n                nxt = set()\n                for i in cur:\n                    j = k - i\n                    if i < len(a) and a[i] == ch: nxt.add(i + 1)\n                    if j < len(b) and b[j] == ch: nxt.add(i)\n                cur = nxt\n                if not cur: break\n        out.append("Data set %d: %s" % (t + 1, "yes" if ok and cur else "no"))\n    print("\\n".join(out))\nmain()\n'
SAMPLE='3\ncat tree tcraete\ncat tree catrtee\ncat tree cttaree\n'
GENERATOR='g2192'

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
