import random
REFERENCE='# External reference: /practice/30217/statistics/\n# Accepted submission: 52829473\n# Source: http://cs101.openjudge.cn/practice/solution/52829473/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\nimport bisect\n\ndef solve():\n    # 快速读取输入\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    N = int(input_data[0])\n    T = int(input_data[1])\n    \n    # 齿轮的最大齿数限制为 1,000,000\n    MAX_VAL = 1000000\n    pos = [None] * (MAX_VAL + 1)\n    \n    # 读取齿轮数据\n    A = [int(x) for x in input_data[2:2+N]]\n    \n    # 记录每个数值出现的所有 1-based 索引位置\n    for idx in range(1, N + 1):\n        val = A[idx - 1]\n        if pos[val] is None:\n            pos[val] = []\n        pos[val].append(idx)\n        \n    # 遍历每个 i，寻找符合条件的最小 j\n    for i in range(1, N + 1):\n        val = A[i - 1]\n        target = T - val\n        \n        # 目标值必须在合法范围内\n        if 1 <= target <= MAX_VAL:\n            lst = pos[target]\n            if lst is not None:\n                # 使用二分查找在递增的索引列表中寻找第一个大于 i 的位置\n                idx_in_lst = bisect.bisect_right(lst, i)\n                if idx_in_lst < len(lst):\n                    j = lst[idx_in_lst]\n                    print(f"{i} {j}")\n                    return\n\nif __name__ == \'__main__\':\n    solve()'
SAMPLE='4 10\n1 3 7 9\n'
GENERATOR_NAME='g30217'
CPP=False
def g30217(r):
    n = r.randint(2, 80); a = [r.randint(1, 1000) for _ in range(n)]; i = r.randrange(n-1); a[i+1] = 1001-a[i]
    return f"{n} {1001}\n{' '.join(map(str,a))}\n"

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
