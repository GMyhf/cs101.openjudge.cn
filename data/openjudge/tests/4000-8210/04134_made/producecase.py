import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'n = int(input())\narr = list(map(int, input().split()))\nm = int(input())\n\nfor _ in range(m):\n    x = int(input())\n\n    # --- 手写二分（不能使用函数） ---\n    l, r = 0, n-1\n    while l <= r:\n        mid = (l + r) // 2\n        if arr[mid] < x:\n            l = mid + 1\n        else:\n            r = mid - 1\n    pos = l\n    # --- 二分结束 ---\n\n    candidates = []\n    if pos < n:\n        candidates.append(arr[pos])\n    if pos > 0:\n        candidates.append(arr[pos - 1])\n\n    # 选和 x 最接近的，如果差一样，取较小的\n    best = min(candidates, key=lambda v: (abs(v - x), v))\n\n    print(best)'
SAMPLE = '3\n2 5 8\n2\n10\n5\n'
GENERATOR_NAME = 'g4134'
def g4134(r):
    n=r.randint(5,30); a=sorted(r.sample(range(300),n))
    q=[r.randint(0,300) for _ in range(r.randint(4,12))]
    return f"{n}\n{' '.join(map(str,a))}\n{len(q)}\n"+"\n".join(map(str,q))+"\n"

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
