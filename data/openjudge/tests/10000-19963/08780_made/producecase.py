import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='n = int(input())\na = [*map(int, input().split())]\ndp = [1] * n\nmaxn = -1\nfor i in range(n):\n    for j in range(i):\n        if a[j] >= a[i]:\n            dp[i] = max(dp[i], dp[j] + 1)\n    maxn = max(maxn, dp[i])\nprint(maxn)'
SAMPLE='8\n389 207 155 300 299 170 158 65\n'
GENERATOR_NAME='g8780'
def g8780(r):
    n=r.randint(1,15); return f"{n}\n"+" ".join(str(r.randint(1,30000)) for _ in range(n))+"\n"

def valid(text):
    """题面：第一行 N（1<=N<=15）；第二行 N 个不大于 30000 的正整数。"""
    lines = text.split("\n")
    if len(lines) != 3 or lines[2] != "":
        return False
    head = lines[0].split()
    if len(head) != 1 or not head[0].isdigit():
        return False
    n = int(head[0])
    vals = lines[1].split()
    if not 1 <= n <= 15 or len(vals) != n:
        return False
    return all(v.isdigit() and 1 <= int(v) <= 30000 for v in vals)


def extra_cases():
    """2026-10 审计补充：原数据值域 1..30000 随机，几乎没有相等高度，
    「可以等于」写成严格小于也能全过；也没有 N=1、单调、全相等、取值边界。"""
    r = random.Random(87800)
    out = [[30000], [1], [5] * 15, [30000] * 15,
           list(range(30000, 29985, -1)), list(range(1, 16)),
           [7, 7, 3, 3, 3, 9, 1, 1], [1, 30000, 1, 30000, 1, 30000, 1],
           sorted([r.randint(1, 30000) for _ in range(15)], reverse=True)]
    for _ in range(8):                       # 小值域：大量相等，卡「严格小于」
        n = r.randint(8, 15)
        out.append([r.randint(1, 4) for _ in range(n)])
    return [f"{len(a)}\n" + " ".join(map(str, a)) + "\n" for a in out]


def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    cases+=[c for c in extra_cases() if c not in cases]
    assert all(valid(c) for c in cases), "题面：1<=N<=15，高度为不大于 30000 的正整数"
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
