import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='from collections import deque\nM, N = map(int, input().split())\nwords = [int(x) for x in input().split()]\nq = deque()\nlength = 0\ndict = [False]*(max(words)+1)\nres = 0\nfor word in words:\n    if dict[word]:\n        continue\n    if length == M:\n        x = q.popleft()\n        dict[x] = False\n    else:\n        length += 1\n    res += 1\n    dict[word] = True\n    q.append(word)\nprint(res)'
SAMPLE='3 7 \n1 2 1 5 4 4 1\n'
GENERATOR_NAME='g9199'
def g9199(r):
    m,n=r.randint(1,20),r.randint(1,60); z=[r.randint(0,1000000) for _ in range(n)]
    return f"{m} {n}\n"+" ".join(map(str,z))+"\n"

def valid(text):
    """题面：第一行 M N（1<=N,M<=1000000）；第二行 N 个不超过 1000000 的非负整数。"""
    lines = text.split("\n")
    if len(lines) != 3 or lines[2] != "":
        return False
    head = lines[0].split()
    if len(head) != 2 or not all(t.isdigit() for t in head):
        return False
    m, n = map(int, head)
    if not (1 <= m <= 1000000 and 1 <= n <= 1000000):
        return False
    words = lines[1].split()
    return len(words) == n and all(w.isdigit() and int(w) <= 1000000 for w in words)


def fmt(m, z):
    return f"{m} {len(z)}\n" + " ".join(map(str, z)) + "\n"


def extra_cases():
    """2026-10 审计补充：原数据单词取自 0..1000000、N<=60，几乎从不重复，
    答案恒等于 N，「内存命中」分支没被覆盖；也没有大规模数据。
    这里补小词表（大量命中，FIFO 与 LRU 结果不同）、M=1、M>=N、取值边界，
    以及受 1MB 输入限制下能放的最大规模（卡逐个扫描内存的 O(NM) 写法）。"""
    r = random.Random(91990)
    out = [fmt(1, [0]), fmt(1000000, [1000000]), fmt(1, [5, 5, 5, 5]),
           fmt(1, [1, 2, 1, 2, 1, 2]), fmt(2, [1, 2, 1, 3, 1, 2, 3, 1]),
           fmt(1000000, [0, 1000000, 0, 1000000, 7]), fmt(3, [0, 1, 2, 3, 0, 1, 2, 3])]
    for m, n, k in ((2, 40, 4), (3, 60, 5), (5, 200, 8), (10, 500, 15), (50, 2000, 80)):
        out.append(fmt(m, [r.randrange(k) for _ in range(n)]))
    out.append(fmt(600, [r.randrange(1000) for _ in range(200000)]))
    out.append(fmt(1000000, [r.randrange(1000) for _ in range(200000)]))
    pool = r.sample(range(1000001), 80000)
    out.append(fmt(50000, [r.choice(pool) for _ in range(120000)]))
    out.append(fmt(1, [r.randrange(3) for _ in range(200000)]))
    return out


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
    assert all(valid(c) for c in cases), "题面：1<=N,M<=1000000，单词为不超过 1000000 的非负整数"
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
