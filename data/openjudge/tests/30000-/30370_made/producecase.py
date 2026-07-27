import random
REFERENCE='# External reference: /practice/30370/statistics/\n# Accepted submission: 52723545\n# Source: http://cs101.openjudge.cn/practice/solution/52723545/\n# License: not declared on the submission page; no license is inferred.\n\nimport bisect\n\ndef main():\n    import sys\n    input = sys.stdin.read\n    data = input().split()\n    n = int(data[0])\n    a = list(map(int, data[1:n+1]))\n    \n    ans = 0\n    # 遍历所有可能的选中人数k\n    for k in range(0, n + 1):\n        # 二分查找：第一个 >=k 的位置 = 小于k的元素个数\n        cnt = bisect.bisect_left(a, k)\n        # 条件1：小于k的元素数量恰好等于k\n        # 条件2：数组中没有元素等于k\n        if cnt == k and (cnt == n or a[cnt] != k):\n            ans += 1\n    print(ans)\n\nif __name__ == "__main__":\n    main()'
SAMPLE='8\n0 2 3 3 6 6 7 7\n'
GENERATOR_NAME='g30370'
CPP=False
def g30370(r):
    n = r.randint(1, 100); return f"{n}\n{' '.join(map(str, sorted(r.randint(0,n) for _ in range(n))))}\n"

from pathlib import Path
import subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/('main.cpp' if CPP else 'main.py'); p.write_text(REFERENCE)
        if CPP:
            exe=Path(d)/'main'; c=subprocess.run(['g++','-O2','-std=c++17',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise SystemExit(c.stderr)
            cmd=[str(exe)]
        else: cmd=[sys.executable,str(p)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
