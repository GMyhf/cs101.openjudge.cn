import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'import sys\nimport heapq\ndef solve():\n    input_data = sys.stdin.read().strip().split()\n    t = int(input_data[0])\n    idx = 1\n    results = []\n    for _ in range(t):\n        m = int(input_data[idx])\n        idx += 1\n        n = int(input_data[idx])\n        idx += 1\n        sequences = []\n        for _ in range(m):\n            seq = []\n            for _ in range(n):\n                seq.append(int(input_data[idx]))\n                idx += 1\n            seq.sort()\n            sequences.append(seq)\n        candidates = sequences[0][:]\n        for i in range(1, m):\n            current_seq = sequences[i]\n            heap = []\n            for val in candidates:\n                heapq.heappush(heap, (val + current_seq[0], 0))\n            new_candidates = []\n            for _ in range(n):\n                if not heap:\n                    break\n                current_sum, pos = heapq.heappop(heap)\n                new_candidates.append(current_sum)\n                if pos + 1 < n:\n                    next_sum = current_sum - current_seq[pos] + current_seq[pos + 1]\n                    heapq.heappush(heap, (next_sum, pos + 1))\n            candidates = new_candidates\n        results.append(" ".join(map(str, candidates)))\n    return "\\n".join(results)\nif __name__ == "__main__":\n    print(solve())'
SAMPLE = '1\n2 3\n1 2 3\n2 2 3\n'
GENERATOR_NAME = 'g6648'
def g6648(r):
    m,n=r.randint(1,5),r.randint(1,8); z=[sorted(r.randint(0,100) for _ in range(n)) for _ in range(m)]
    return f"1\n{m} {n}\n"+"\n".join(" ".join(map(str,x)) for x in z)+"\n"

def valid(text):
    """题面：第一行 T；每组第一行 m n（0<m<=100，0<n<=2000），随后 m 行，每行 n 个不大于 10000 的非负整数。"""
    try:
        lines = text.split("\n")
        if lines[-1] != "": return False
        lines = lines[:-1]
        def ints(ln):
            t = ln.split(" ")
            if any(x != str(int(x)) for x in t): raise ValueError
            return list(map(int, t))
        (t,) = ints(lines[0])
        if t < 1: return False
        pos = 1
        for _ in range(t):
            m, n = ints(lines[pos]); pos += 1
            if not (1 <= m <= 100 and 1 <= n <= 2000): return False
            for _ in range(m):
                row = ints(lines[pos]); pos += 1
                if len(row) != n or not all(0 <= x <= 10000 for x in row): return False
        return pos == len(lines)
    except Exception:
        return False

def block(r, m, n, hi=10000, mode="rand"):
    rows = []
    for _ in range(m):
        if mode == "same":
            row = [r.randint(0, hi)] * n
        elif mode == "zero":
            row = [0] * n
        elif mode == "max":
            row = [10000] * n
        else:
            row = [r.randint(0, hi) for _ in range(n)]
        r.shuffle(row)
        rows.append(" ".join(map(str, row)))
    return f"{m} {n}\n" + "\n".join(rows) + "\n"

def multi(r, blocks):
    return f"{len(blocks)}\n" + "".join(blocks)

EXTRA = [
    lambda r: multi(r, [block(r, 1, 1, mode="zero")]),
    lambda r: multi(r, [block(r, 1, 1, mode="max"), block(r, 100, 1), block(r, 1, 7)]),
    lambda r: multi(r, [block(r, 100, 1, mode="max")]),
    lambda r: multi(r, [block(r, r.randint(1, 6), r.randint(1, 6), hi=r.choice([3, 50, 10000])) for _ in range(10)]),
    lambda r: multi(r, [block(r, 1, 2000)]),
    lambda r: multi(r, [block(r, 2, 2000)]),
    lambda r: multi(r, [block(r, 100, 50, hi=20), block(r, 50, 100), block(r, 3, 300, mode="same")]),
    lambda r: multi(r, [block(r, 100, 2000, hi=999)]),
    lambda r: multi(r, [block(r, 80, 2000)]),
    lambda r: multi(r, [block(r, 100, 2000)]),
    lambda r: multi(r, [block(r, 100, 2000, hi=9)]),
    lambda r: multi(r, [block(r, 20, 2000), block(r, 20, 2000, hi=99), block(r, 20, 2000, mode="same")]),
]

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    cases+=[f(random.Random(6648+i)) for i,f in enumerate(EXTRA)]
    assert all(valid(c) for c in cases)
    assert len(set(cases))==len(cases)
    assert all(len(c.encode()) <= 1000000 for c in cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
