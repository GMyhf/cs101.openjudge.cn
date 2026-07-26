import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'import sys\nimport heapq\ndef solve():\n    input_data = sys.stdin.read().strip().split()\n    t = int(input_data[0])\n    idx = 1\n    results = []\n    for _ in range(t):\n        m = int(input_data[idx])\n        idx += 1\n        n = int(input_data[idx])\n        idx += 1\n        sequences = []\n        for _ in range(m):\n            seq = []\n            for _ in range(n):\n                seq.append(int(input_data[idx]))\n                idx += 1\n            seq.sort()\n            sequences.append(seq)\n        candidates = sequences[0][:]\n        for i in range(1, m):\n            current_seq = sequences[i]\n            heap = []\n            for val in candidates:\n                heapq.heappush(heap, (val + current_seq[0], 0))\n            new_candidates = []\n            for _ in range(n):\n                if not heap:\n                    break\n                current_sum, pos = heapq.heappop(heap)\n                new_candidates.append(current_sum)\n                if pos + 1 < n:\n                    next_sum = current_sum - current_seq[pos] + current_seq[pos + 1]\n                    heapq.heappush(heap, (next_sum, pos + 1))\n            candidates = new_candidates\n        results.append(" ".join(map(str, candidates)))\n    return "\\n".join(results)\nif __name__ == "__main__":\n    print(solve())'
SAMPLE = '1\n2 3\n1 2 3\n2 2 3\n'
GENERATOR_NAME = 'g6648'
def g6648(r):
    m,n=r.randint(1,5),r.randint(1,8); z=[sorted(r.randint(0,100) for _ in range(n)) for _ in range(m)]
    return f"1\n{m} {n}\n"+"\n".join(" ".join(map(str,x)) for x in z)+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
